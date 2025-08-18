/**
 * 要求仕様ID: WPM.1-DET.1
 * 対応設計書: docs/design/api/specs/API定義書_API-041_作業実績取得API.md
 * 実装内容: 作業実績取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { prisma } from '@/lib/prisma';
import {
  createSuccessResponse,
  createErrorResponse,
  createAuthErrorResponse,
  createAuthorizationErrorResponse,
  createNotFoundErrorResponse
} from '@/lib/api-utils';

// 作業実績取得API
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  try {
    // 認証チェック（オプショナル）
    const authResult = await verifyAuth(request);
    
    // トークンがない場合はデフォルトユーザーを使用（開発用）
    if (!authResult.success) {
      console.log('Work GET - No auth token, using default user');
      // デフォルトの認証結果を作成
      authResult.success = true;
      authResult.userId = 'USER000001';
      authResult.employeeId = '000001';
      authResult.loginId = '000001';
    }

    if (!params || !params.userId) {
      return createErrorResponse(
        'INVALID_PARAMETER',
        'ユーザーIDが指定されていません',
        undefined,
        400
      );
    }

    const { userId } = params;
    const currentUserId = authResult.userId;

    // userIdが'me'の場合は認証されたユーザーのIDを使用
    const targetUserId = userId === 'me' ? (authResult.employeeId || currentUserId) : userId;

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const year = searchParams.get('year');
    const status = searchParams.get('status');
    const projectCode = searchParams.get('projectCode');
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '10');

    // 権限チェック（自分以外の作業実績を見る場合）
    const currentEmployeeId = authResult.employeeId || currentUserId;
    if (targetUserId !== currentEmployeeId) {
      // TODO: 管理者権限チェックを実装
      // 現在は暫定的に403を返す
      return createAuthorizationErrorResponse();
    }

    // プロジェクト実績の取得
    const whereCondition: any = {
      employee_id: targetUserId,
      is_deleted: false
    };

    // フィルタリング条件の追加
    if (year) {
      const startOfYear = new Date(`${year}-01-01`);
      const endOfYear = new Date(`${year}-12-31`);
      whereCondition.start_date = {
        gte: startOfYear,
        lte: endOfYear
      };
    }

    if (status) {
      whereCondition.project_status = status;
    }

    if (projectCode) {
      whereCondition.project_code = projectCode;
    }

    // ページネーション計算
    const skip = (page - 1) * limit;

    // データ取得
    const [projectRecords, totalCount] = await Promise.all([
      prisma.projectRecord.findMany({
        where: whereCondition,
        orderBy: {
          start_date: 'desc'
        },
        skip: skip,
        take: limit
      }),
      prisma.projectRecord.count({
        where: whereCondition
      })
    ]);

    // サマリー情報の生成
    const summary = {
      total_projects: totalCount,
      active_projects: await prisma.projectRecord.count({
        where: {
          ...whereCondition,
          project_status: 'ACTIVE'
        }
      }),
      completed_projects: await prisma.projectRecord.count({
        where: {
          ...whereCondition,
          project_status: 'COMPLETED'
        }
      }),
      on_hold_projects: await prisma.projectRecord.count({
        where: {
          ...whereCondition,
          project_status: 'ON_HOLD'
        }
      })
    };

    // レスポンスデータの整形
    const formattedRecords = projectRecords.map(record => {
      // technologies_usedのパース
      let technologies = [];
      if (record.technologies_used) {
        try {
          technologies = JSON.parse(record.technologies_used);
        } catch {
          // JSON形式でない場合はカンマ区切りとして扱う
          technologies = record.technologies_used.split(',').map(t => t.trim());
        }
      }
      
      // achievementsのパース
      let achievements = [];
      if (record.achievements) {
        try {
          achievements = JSON.parse(record.achievements);
        } catch {
          achievements = [record.achievements];
        }
      }
      
      return {
        id: record.project_record_id,
        project_name: record.project_name,
        project_code: record.project_code,
        role: record.role_title,
        start_date: record.start_date?.toISOString().split('T')[0] || '',
        end_date: record.end_date?.toISOString().split('T')[0] || '',
        status: record.project_status || 'ACTIVE',
        description: record.responsibilities || '',
        technologies: technologies,
        achievements: achievements,
        team_size: record.team_size || 1,
        responsibilities: record.responsibilities ? [record.responsibilities] : [],
        created_at: record.created_at?.toISOString() || '',
        updated_at: record.updated_at?.toISOString() || ''
      };
    });

    // 技術スタックの集計
    const allTechnologies = new Set<string>();
    formattedRecords.forEach(record => {
      record.technologies.forEach((tech: string) => allTechnologies.add(tech));
    });
    
    const summaryWithTech = {
      ...summary,
      total_technologies: allTechnologies.size
    };

    // ページネーション情報
    const pagination = {
      page,
      limit,
      total: totalCount,
      totalPages: Math.ceil(totalCount / limit),
      hasNext: page * limit < totalCount,
      hasPrev: page > 1
    };

    return createSuccessResponse({
      records: formattedRecords,
      summary: summaryWithTech,
      pagination
    });

  } catch (error) {
    console.error('作業実績取得エラー:', error);
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    );
  }
}