/**
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-014_プロフィール更新履歴API.md
 * 実装内容: プロフィール更新履歴取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';

export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'UNAUTHORIZED',
            message: '認証が必要です'
          }
        },
        { status: 401 }
      );
    }

    if (!authResult.userId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_TOKEN',
            message: '無効な認証トークンです'
          }
        },
        { status: 401 }
      );
    }

    const { userId } = params;
    const { searchParams } = new URL(request.url);
    const limit = parseInt(searchParams.get('limit') || '10');
    const offset = parseInt(searchParams.get('offset') || '0');

    // userIdが'me'の場合は認証されたユーザーのIDを使用
    const targetUserId = userId === 'me' ? (authResult.employeeId || authResult.userId) : userId;

    console.log('History API - Params:', { userId, targetUserId, limit, offset });
    console.log('History API - Auth result:', { 
      authUserId: authResult.userId, 
      authEmployeeId: authResult.employeeId,
      requestedUserId: userId 
    });

    // 権限チェック：自分の履歴のみ閲覧可能
    const currentEmployeeId = authResult.employeeId || authResult.userId;
    if (targetUserId !== currentEmployeeId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'FORBIDDEN',
            message: '他のユーザーの履歴は閲覧できません'
          }
        },
        { status: 403 }
      );
    }

    // AuditLogテーブルから更新履歴を取得
    const auditLogs = await prisma.auditLog.findMany({
      where: {
        target_id: targetUserId,
        target_table: 'Employee',
        action_type: 'UPDATE'
      },
      orderBy: {
        created_at: 'desc'
      },
      take: limit,
      skip: offset,
      select: {
        id: true,
        user_id: true,
        action_type: true,
        target_table: true,
        target_id: true,
        old_values: true,
        new_values: true,
        created_at: true
      }
    });

    console.log('Found audit logs:', auditLogs.length);

    // フィールド名のマッピング
    const fieldNameMap: Record<string, string> = {
      'full_name': '氏名',
      'full_name_kana': '氏名（カナ）',
      'email': 'メールアドレス',
      'phone': '電話番号',
      'department_id': '部署',
      'position_id': '役職'
    };

    // 履歴データの変換
    const history = await Promise.all(
      auditLogs.map(async (log) => {
        try {
          const oldValues = (log.old_values ? JSON.parse(log.old_values) : {}) as any;
          const newValues = (log.new_values ? JSON.parse(log.new_values) : {}) as any;
          
          console.log('Processing log:', { 
            id: log.id, 
            oldValues, 
            newValues,
            created_at: log.created_at 
          });
          
          // 変更されたフィールドを特定
          const changedFields = Object.keys(newValues);
          
          // 複数フィールドが変更された場合は最初のフィールドを代表として表示
          const primaryField = changedFields[0];
          if (!primaryField) {
            console.log('No primary field found for log:', log.id);
            return null; // フィールドが特定できない場合はスキップ
          }
          
          const fieldDisplayName = fieldNameMap[primaryField] || primaryField;
          
          let oldDisplayValue = oldValues[primaryField] || '';
          let newDisplayValue = newValues[primaryField] || '';
          
          // 部署・役職の場合は名前を取得
          if (primaryField === 'department_id') {
            if (oldDisplayValue) {
              const oldDept = await prisma.department.findUnique({
                where: { department_code: oldDisplayValue }
              });
              oldDisplayValue = oldDept?.department_name || oldDisplayValue;
            }
            if (newDisplayValue) {
              const newDept = await prisma.department.findUnique({
                where: { department_code: newDisplayValue }
              });
              newDisplayValue = newDept?.department_name || newDisplayValue;
            }
          } else if (primaryField === 'position_id') {
            if (oldDisplayValue) {
              const oldPos = await prisma.position.findUnique({
                where: { position_code: oldDisplayValue }
              });
              oldDisplayValue = oldPos?.position_name || oldDisplayValue;
            }
            if (newDisplayValue) {
              const newPos = await prisma.position.findUnique({
                where: { position_code: newDisplayValue }
              });
              newDisplayValue = newPos?.position_name || newDisplayValue;
            }
          }

          const historyItem = {
            id: log.id.toString(),
            updated_at: log.created_at ? log.created_at.toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
            field_name: fieldDisplayName,
            old_value: oldDisplayValue || '（未設定）',
            new_value: newDisplayValue || '（未設定）',
            updated_by_name: log.user_id || 'システム',
            reason: 'プロフィール更新'
          };
          
          console.log('Created history item:', historyItem);
          return historyItem;
        } catch (error) {
          console.error('Error processing audit log:', log.id, error);
          return null;
        }
      })
    );

    // nullを除外
    const filteredHistory = history.filter(item => item !== null);

    return NextResponse.json({
      success: true,
      data: {
        history: filteredHistory,
        pagination: {
          total: auditLogs.length,
          limit,
          offset,
          hasMore: auditLogs.length === limit
        }
      }
    });

  } catch (error) {
    console.error('History fetch error:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'サーバー内部エラーが発生しました'
        }
      },
      { status: 500 }
    );
  }
}
