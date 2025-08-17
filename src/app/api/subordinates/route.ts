/**
 * 部下管理API
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { verifyAuth } from '@/lib/auth';

/**
 * 部下の追加
 * POST /api/subordinates
 */
export async function POST(request: NextRequest) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.employeeId) {
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

    const managerId = authResult.employeeId;
    const body = await request.json();
    const { subordinateId } = body;

    if (!subordinateId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_REQUEST',
            message: '部下のIDが指定されていません'
          }
        },
        { status: 400 }
      );
    }

    // 管理職権限の確認
    const manager = await prisma.employee.findUnique({
      where: { employee_code: managerId },
      include: {
        position: true
      }
    });

    if (!manager || !manager.position || manager.position.position_level < 3) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'PERMISSION_DENIED',
            message: '部下を管理する権限がありません'
          }
        },
        { status: 403 }
      );
    }

    // 部下として追加する従業員が存在するか確認
    const subordinate = await prisma.employee.findUnique({
      where: { employee_code: subordinateId }
    });

    if (!subordinate) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'SUBORDINATE_NOT_FOUND',
            message: '指定された従業員が見つかりません'
          }
        },
        { status: 404 }
      );
    }

    // すでに他の上司がいるか確認
    if (subordinate.manager_id && subordinate.manager_id !== managerId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'ALREADY_ASSIGNED',
            message: 'この従業員はすでに他の上司に割り当てられています'
          }
        },
        { status: 400 }
      );
    }

    // 部下として登録
    await prisma.employee.update({
      where: { employee_code: subordinateId },
      data: {
        manager_id: managerId,
        updated_at: new Date()
      }
    });

    return NextResponse.json({
      success: true,
      data: {
        message: '部下を追加しました',
        subordinateId,
        managerId
      }
    });

  } catch (error) {
    console.error('部下追加エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'サーバーエラーが発生しました'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * 部下の削除
 * DELETE /api/subordinates
 */
export async function DELETE(request: NextRequest) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.employeeId) {
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

    const managerId = authResult.employeeId;
    const { searchParams } = new URL(request.url);
    const subordinateId = searchParams.get('subordinateId');

    if (!subordinateId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'INVALID_REQUEST',
            message: '部下のIDが指定されていません'
          }
        },
        { status: 400 }
      );
    }

    // 部下が自分の管理下にあるか確認
    const subordinate = await prisma.employee.findUnique({
      where: { employee_code: subordinateId }
    });

    if (!subordinate || subordinate.manager_id !== managerId) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'NOT_YOUR_SUBORDINATE',
            message: 'この従業員はあなたの部下ではありません'
          }
        },
        { status: 403 }
      );
    }

    // 部下から削除（manager_idをnullに）
    await prisma.employee.update({
      where: { employee_code: subordinateId },
      data: {
        manager_id: null,
        updated_at: new Date()
      }
    });

    return NextResponse.json({
      success: true,
      data: {
        message: '部下をリストから削除しました',
        subordinateId
      }
    });

  } catch (error) {
    console.error('部下削除エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'サーバーエラーが発生しました'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * 部下一覧の取得
 * GET /api/subordinates
 */
export async function GET(request: NextRequest) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.employeeId) {
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

    const managerId = authResult.employeeId;

    // 部下一覧を取得
    const subordinates = await prisma.employee.findMany({
      where: {
        manager_id: managerId,
        is_deleted: false
      },
      select: {
        employee_code: true,
        full_name: true,
        email: true,
        position_id: true,
        department_id: true
      }
    });

    // 部下の詳細情報を取得
    const subordinatesWithDetails = await Promise.all(
      subordinates.map(async (sub) => {
        const position = sub.position_id ? 
          await prisma.position.findUnique({ 
            where: { position_code: sub.position_id } 
          }) : null;
        
        const department = sub.department_id ?
          await prisma.department.findUnique({
            where: { department_code: sub.department_id }
          }) : null;

        return {
          employee_id: sub.employee_code,
          name: sub.full_name,
          email: sub.email,
          position: position?.position_name || '未設定',
          department: department?.department_name || '未設定'
        };
      })
    );

    return NextResponse.json({
      success: true,
      data: {
        subordinates: subordinatesWithDetails,
        total: subordinatesWithDetails.length
      }
    });

  } catch (error) {
    console.error('部下一覧取得エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'INTERNAL_SERVER_ERROR',
          message: 'サーバーエラーが発生しました'
        }
      },
      { status: 500 }
    );
  }
}