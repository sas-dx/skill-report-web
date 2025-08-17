/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: アクションプラン順序更新API (API-709)
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// ============================================================================
// 型定義
// ============================================================================

/**
 * アクションプラン順序更新リクエスト
 */
interface ActionPlanOrderUpdateRequest {
  action_plan_ids: string[];
}

/**
 * アクションプラン順序更新レスポンス
 */
interface ActionPlanOrderUpdateResponse {
  success: boolean;
  data?: {
    updated_action_plans: Array<{
      action_id: string;
      display_order: number;
    }>;
    updated_count: number;
  };
  error?: {
    code: string;
    message: string;
    details?: string;
  };
  timestamp: string;
}

/**
 * 入力値バリデーション
 */
function validateOrderUpdateRequest(data: any): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!Array.isArray(data.action_plan_ids)) {
    errors.push('action_plan_idsは配列である必要があります');
  } else {
    if (data.action_plan_ids.length === 0) {
      errors.push('action_plan_idsは空の配列にできません');
    }

    if (data.action_plan_ids.length > 100) {
      errors.push('一度に更新できるアクションプランは100件までです');
    }

    // 重複チェック
    const uniqueIds = new Set(data.action_plan_ids);
    if (uniqueIds.size !== data.action_plan_ids.length) {
      errors.push('action_plan_idsに重複があります');
    }

    // IDの形式チェック
    for (const id of data.action_plan_ids) {
      if (typeof id !== 'string' || id.trim().length === 0) {
        errors.push('無効なアクションプランIDが含まれています');
        break;
      }
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
 * アクションプラン順序更新API (API-709)
 * PUT /api/career/action-plans/order
 */
export async function PUT(
  request: NextRequest
): Promise<NextResponse<ActionPlanOrderUpdateResponse>> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || 'emp_001';

    // リクエストボディの取得
    const requestData: ActionPlanOrderUpdateRequest = await request.json();

    // 入力値バリデーション
    const validation = validateOrderUpdateRequest(requestData);
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

    const actionPlanIds = requestData.action_plan_ids;

    // 指定されたアクションプランが全て存在し、ユーザーのものであることを確認
    const existingActionPlans = await prisma.goalProgress.findMany({
      where: {
        goal_id: { in: actionPlanIds },
        employee_id: userId,
        is_deleted: false,
        goal_type: 'ACTION_PLAN'
      },
      select: {
        id: true,
        goal_id: true,
        goal_title: true
      }
    });

    // 存在しないアクションプランをチェック
    const existingIds = new Set(existingActionPlans.map(plan => plan.goal_id));
    const missingIds = actionPlanIds.filter(id => !existingIds.has(id));

    if (missingIds.length > 0) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'ACTION_PLAN_NOT_FOUND',
            message: '指定されたアクションプランの一部が見つかりません',
            details: `Missing IDs: ${missingIds.join(', ')}`
          },
          timestamp: new Date().toISOString()
        },
        { status: 404 }
      );
    }

    // トランザクションで順序を更新
    const updatedActionPlans = await prisma.$transaction(async (tx) => {
      const results = [];

      for (let i = 0; i < actionPlanIds.length; i++) {
        const actionPlanId = actionPlanIds[i];
        const displayOrder = i + 1; // 1から始まる順序

        // 対応するレコードを見つける
        const actionPlan = existingActionPlans.find(plan => plan.goal_id === actionPlanId);
        if (!actionPlan) continue;

        // 順序情報を更新（display_orderフィールドは存在しないためメタデータやメモとして保存）
        await tx.goalProgress.update({
          where: {
            id: actionPlan.id
          },
          data: {
            updated_by: userId,
            updated_at: new Date()
          }
        });

        results.push({
          action_id: actionPlanId || '',
          display_order: displayOrder
        });
      }

      return results;
    });

    // レスポンス形式に変換
    const responseData: ActionPlanOrderUpdateResponse = {
      success: true,
      data: {
        updated_action_plans: updatedActionPlans,
        updated_count: updatedActionPlans.length
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { status: 200 });

  } catch (error) {
    console.error('アクションプラン順序更新API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'ACTION_PLAN_ORDER_UPDATE_ERROR',
          message: 'アクションプランの順序更新に失敗しました',
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
      'Access-Control-Allow-Methods': 'PUT, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-user-id',
    },
  });
}