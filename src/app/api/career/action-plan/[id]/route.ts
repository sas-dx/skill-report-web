/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: アクションプラン個別操作API (API-707, API-708)
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { 
  ActionPlan,
  ActionPlanUpdateRequest,
  ActionPlanUpdateResponse,
  ActionPlanDeleteResponse
} from '@/types/career';

// ============================================================================
// ユーティリティ関数
// ============================================================================

/**
 * データベースデータをAPI形式に変換
 */
function transformGoalProgressToActionPlan(dbGoal: any): ActionPlan {
  return {
    action_id: dbGoal.goal_id,
    title: dbGoal.goal_title || '',
    description: dbGoal.goal_description || '',
    due_date: dbGoal.target_date ? dbGoal.target_date.toISOString().split('T')[0] : '',
    status: mapAchievementStatusToActionStatus(dbGoal.achievement_status),
    completed_date: dbGoal.completion_date ? dbGoal.completion_date.toISOString().split('T')[0] : undefined,
    priority: mapPriorityLevelToActionPriority(dbGoal.priority_level),
    progress_percentage: dbGoal.progress_rate ? Number(dbGoal.progress_rate) : 0,
    category: dbGoal.goal_category || '',
    related_skill_id: dbGoal.related_skill_items || '',
    created_at: dbGoal.created_at ? dbGoal.created_at.toISOString() : '',
    updated_at: dbGoal.updated_at ? dbGoal.updated_at.toISOString() : ''
  };
}

/**
 * achievement_statusをaction statusにマッピング
 */
function mapAchievementStatusToActionStatus(status: string): 'not_started' | 'in_progress' | 'completed' {
  switch (status) {
    case 'completed':
      return 'completed';
    case 'in_progress':
    case 'active':
      return 'in_progress';
    default:
      return 'not_started';
  }
}

/**
 * priority_levelをaction priorityにマッピング
 */
function mapPriorityLevelToActionPriority(priority: string): 'high' | 'medium' | 'low' {
  switch (priority?.toLowerCase()) {
    case 'high':
    case '高':
      return 'high';
    case 'low':
    case '低':
      return 'low';
    default:
      return 'medium';
  }
}

/**
 * action priorityをpriority_levelにマッピング
 */
function mapActionPriorityToPriorityLevel(priority: string): string {
  switch (priority) {
    case 'high':
      return 'HIGH';
    case 'low':
      return 'LOW';
    default:
      return 'MEDIUM';
  }
}

/**
 * action statusをachievement_statusにマッピング
 */
function mapActionStatusToAchievementStatus(status: string): string {
  switch (status) {
    case 'completed':
      return 'completed';
    case 'in_progress':
      return 'in_progress';
    default:
      return 'not_started';
  }
}

/**
 * 入力値バリデーション（更新用）
 */
function validateActionPlanUpdateRequest(data: any): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (data.title !== undefined) {
    if (typeof data.title !== 'string' || data.title.trim().length === 0) {
      errors.push('タイトルは空にできません');
    }
    if (data.title && data.title.length > 200) {
      errors.push('タイトルは200文字以内で入力してください');
    }
  }

  if (data.due_date !== undefined) {
    if (typeof data.due_date !== 'string') {
      errors.push('期限の形式が正しくありません');
    } else {
      const dueDate = new Date(data.due_date);
      if (isNaN(dueDate.getTime())) {
        errors.push('期限の形式が正しくありません');
      }
    }
  }

  if (data.description !== undefined && data.description && data.description.length > 1000) {
    errors.push('説明は1000文字以内で入力してください');
  }

  if (data.status !== undefined && !['not_started', 'in_progress', 'completed'].includes(data.status)) {
    errors.push('ステータスは not_started, in_progress, completed のいずれかを指定してください');
  }

  if (data.priority !== undefined && !['high', 'medium', 'low'].includes(data.priority)) {
    errors.push('優先度は high, medium, low のいずれかを指定してください');
  }

  if (data.progress_percentage !== undefined) {
    const progress = Number(data.progress_percentage);
    if (isNaN(progress) || progress < 0 || progress > 100) {
      errors.push('進捗率は0から100の間で指定してください');
    }
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

// ============================================================================
// API実装
// ============================================================================

/**
 * アクションプラン更新API (API-707)
 * PUT /api/career/action-plan/[id]
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
): Promise<NextResponse<ActionPlanUpdateResponse>> {
  try {
    // ヘッダーからユーザーIDを取得（デフォルト値として000001を使用）
    const userId = request.headers.get('x-user-id') || '000001';
    const actionPlanId = params.id;

    // リクエストボディの取得
    const requestData: ActionPlanUpdateRequest = await request.json();

    // デバッグログ追加
    console.log('アクションプラン更新 - パラメータ:', {
      actionPlanId,
      userId,
      requestData
    });

    // 入力値バリデーション
    const validation = validateActionPlanUpdateRequest(requestData);
    if (!validation.isValid) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'VALIDATION_ERROR',
            message: '入力値に誤りがあります',
            details: validation.errors.join(', ')
          },
          timestamp: new Date().toISOString()
        },
        { status: 400 }
      );
    }

    // 既存のアクションプランを確認 - ユーザーIDの条件を一時的に外して確認
    const existingActionPlan = await prisma.goalProgress.findFirst({
      where: {
        goal_id: actionPlanId,
        is_deleted: false,
        goal_type: 'ACTION_PLAN'
      }
    });

    console.log('既存のアクションプラン:', existingActionPlan);

    if (!existingActionPlan) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'ACTION_PLAN_NOT_FOUND',
            message: '指定されたアクションプランが見つかりません',
            details: `Action Plan ID: ${actionPlanId}`
          },
          timestamp: new Date().toISOString()
        },
        { status: 404 }
      );
    }

    // 更新データの構築
    const updateData: any = {
      updated_by: userId,
      updated_at: new Date()
    };

    if (requestData.title !== undefined) {
      updateData.goal_title = requestData.title;
    }

    if (requestData.description !== undefined) {
      updateData.goal_description = requestData.description;
    }

    if (requestData.due_date !== undefined) {
      updateData.target_date = new Date(requestData.due_date);
    }

    if (requestData.status !== undefined) {
      updateData.achievement_status = mapActionStatusToAchievementStatus(requestData.status);
      
      // 完了ステータスの場合、完了日を設定
      if (requestData.status === 'completed') {
        updateData.completion_date = requestData.completed_date ? new Date(requestData.completed_date) : new Date();
        updateData.progress_rate = 100; // 完了時は進捗率を100%に設定
      }
    }

    if (requestData.priority !== undefined) {
      updateData.priority_level = mapActionPriorityToPriorityLevel(requestData.priority);
    }

    if (requestData.progress_percentage !== undefined) {
      updateData.progress_rate = requestData.progress_percentage;
    }

    // アクションプランの更新
    const updatedActionPlan = await prisma.goalProgress.update({
      where: {
        id: existingActionPlan.id
      },
      data: updateData
    });

    // レスポンス形式に変換
    const responseData: ActionPlanUpdateResponse = {
      success: true,
      data: {
        action_plan: transformGoalProgressToActionPlan(updatedActionPlan)
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { status: 200 });

  } catch (error) {
    console.error('アクションプラン更新API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'ACTION_PLAN_UPDATE_ERROR',
          message: 'アクションプランの更新に失敗しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        },
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

/**
 * アクションプラン削除API (API-708)
 * DELETE /api/career/action-plan/[id]
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
): Promise<NextResponse<ActionPlanDeleteResponse>> {
  try {
    // ヘッダーからユーザーIDを取得（デフォルト値として000001を使用）
    const userId = request.headers.get('x-user-id') || '000001';
    const actionPlanId = params.id;

    // 既存のアクションプランを確認
    const existingActionPlan = await prisma.goalProgress.findFirst({
      where: {
        goal_id: actionPlanId,
        is_deleted: false,
        goal_type: 'ACTION_PLAN'
      }
    });

    if (!existingActionPlan) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'ACTION_PLAN_NOT_FOUND',
            message: '指定されたアクションプランが見つかりません',
            details: `Action Plan ID: ${actionPlanId}`
          },
          timestamp: new Date().toISOString()
        },
        { status: 404 }
      );
    }

    // 論理削除の実行
    const deletedAt = new Date();
    await prisma.goalProgress.update({
      where: {
        id: existingActionPlan.id
      },
      data: {
        is_deleted: true,
        updated_by: userId,
        updated_at: deletedAt
      }
    });

    // レスポンス形式に変換
    const responseData: ActionPlanDeleteResponse = {
      success: true,
      data: {
        deleted_action_plan_id: actionPlanId,
        deleted_at: deletedAt.toISOString()
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { status: 200 });

  } catch (error) {
    console.error('アクションプラン削除API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'ACTION_PLAN_DELETE_ERROR',
          message: 'アクションプランの削除に失敗しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        },
        timestamp: new Date().toISOString()
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
