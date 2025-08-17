/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリアパス個別操作API
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { Decimal } from '@prisma/client/runtime/library';

/**
 * キャリアパス更新API
 * PUT /api/career/path/[id]
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
): Promise<NextResponse> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || '000001';
    const stepId = params.id;
    const body = await request.json();
    
    console.log('PUT Request - stepId:', stepId, 'userId:', userId);

    // サンプルデータのIDの場合は新規作成として処理
    if (stepId.startsWith('step_')) {
      console.log('サンプルデータのIDを検出。新規作成として処理します。');
      
      // 新規作成
      const newId = `CAREER_PATH_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      const newPath = await prisma.goalProgress.create({
        data: {
          id: newId,  // 主キー
          goal_id: newId,  // ユニークキー
          employee_id: userId,
          goal_type: 'CAREER_PATH',
          goal_title: body.position_name,
          goal_description: body.description,
          goal_category: 'CAREER',
          priority_level: String(body.position_level || 1),
          target_date: body.target_date ? new Date(body.target_date) : null,
          start_date: new Date(),
          achievement_status: body.status === 'completed' ? 'COMPLETED' : 
                              body.status === 'in_progress' ? 'IN_PROGRESS' : 'NOT_STARTED',
          milestones: JSON.stringify(body.milestones || []),
          obstacles: JSON.stringify(body.prerequisites || []),
          support_needed: JSON.stringify(body.required_skills || []),
          related_skill_items: JSON.stringify(body.required_skills || []),
          tenant_id: 'default',
          created_by: userId,
          updated_by: userId,
          created_at: new Date(),
          updated_at: new Date(),
          is_deleted: false
        }
      });

      return NextResponse.json({
        success: true,
        data: {
          step_id: newPath.id,
          message: 'キャリアパスステップが作成されました'
        }
      });
    }

    // 既存のキャリアパスを確認
    const existingPath = await prisma.goalProgress.findFirst({
      where: {
        id: stepId,  // idで検索
        employee_id: userId,
        goal_type: 'CAREER_PATH',
        is_deleted: false
      }
    });

    if (!existingPath) {
      console.log('キャリアパスが見つかりません:', stepId);
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'CAREER_PATH_NOT_FOUND',
            message: '指定されたキャリアパスが見つかりません'
          }
        },
        { status: 404 }
      );
    }

    // キャリアパスを更新
    const updatedPath = await prisma.goalProgress.update({
      where: { id: stepId },  // idで更新
      data: {
        goal_title: body.position_name,
        goal_description: body.description,
        priority_level: String(body.position_level || 1),
        target_date: body.target_date ? new Date(body.target_date) : null,
        achievement_status: body.status === 'completed' ? 'COMPLETED' : 
                           body.status === 'in_progress' ? 'IN_PROGRESS' : 'NOT_STARTED',
        progress_rate: body.progress_percentage ? new Decimal(body.progress_percentage) : null,
        milestones: JSON.stringify(body.milestones || []),
        obstacles: JSON.stringify(body.prerequisites || []),
        support_needed: JSON.stringify(body.required_skills || []),
        related_skill_items: JSON.stringify(body.required_skills || []),
        updated_by: userId,
        updated_at: new Date()
      }
    });

    return NextResponse.json({
      success: true,
      data: {
        step_id: updatedPath.id,
        message: 'キャリアパスステップが更新されました'
      }
    });

  } catch (error) {
    console.error('キャリアパス更新エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'CAREER_PATH_UPDATE_ERROR',
          message: 'キャリアパスの更新に失敗しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * キャリアパス削除API
 * DELETE /api/career/path/[id]
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
): Promise<NextResponse> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || '000001';
    const stepId = params.id;
    
    console.log('DELETE Request - stepId:', stepId, 'userId:', userId);
    
    // サンプルデータのIDの場合は何もしない
    if (stepId.startsWith('step_')) {
      console.log('サンプルデータは削除できません');
      return NextResponse.json({
        success: true,
        data: {
          deleted_step_id: stepId,
          message: 'サンプルデータは削除されません'
        }
      });
    }

    // 既存のキャリアパスを確認
    const existingPath = await prisma.goalProgress.findFirst({
      where: {
        id: stepId,  // idで検索
        employee_id: userId,
        goal_type: 'CAREER_PATH',
        is_deleted: false
      }
    });

    if (!existingPath) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'CAREER_PATH_NOT_FOUND',
            message: '指定されたキャリアパスが見つかりません'
          }
        },
        { status: 404 }
      );
    }

    // 論理削除
    await prisma.goalProgress.update({
      where: { id: stepId },  // idで更新
      data: {
        is_deleted: true,
        updated_by: userId,
        updated_at: new Date()
      }
    });

    return NextResponse.json({
      success: true,
      data: {
        deleted_step_id: stepId,
        message: 'キャリアパスステップが削除されました'
      }
    });

  } catch (error) {
    console.error('キャリアパス削除エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'CAREER_PATH_DELETE_ERROR',
          message: 'キャリアパスの削除に失敗しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * OPTIONS メソッド（CORS対応）
 */
export async function OPTIONS(request: NextRequest): Promise<NextResponse> {
  return new NextResponse(null, {
    status: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-user-id',
    },
  });
}