/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/api/specs/API定義書_API-032_キャリア目標更新API.md
 * 実装内容: キャリア目標更新API (API-032)
 */

import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';

// リクエストボディのバリデーションスキーマ
const RelatedSkillSchema = z.object({
  skill_id: z.string(),
  target_level: z.number().min(1).max(5)
});

const ActionPlanSchema = z.object({
  action_id: z.string().optional(),
  title: z.string().max(100),
  description: z.string().max(500).optional(),
  due_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  status: z.enum(['not_started', 'in_progress', 'completed']),
  completed_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional()
});

const FeedbackSchema = z.object({
  feedback_id: z.string().optional(),
  comment: z.string().max(500)
});

const CareerGoalSchema = z.object({
  goal_id: z.string().optional(),
  goal_type: z.enum(['short_term', 'mid_term', 'long_term']).optional(),
  title: z.string().max(100).optional(),
  description: z.string().max(1000).optional(),
  target_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  status: z.enum(['not_started', 'in_progress', 'completed', 'postponed', 'cancelled']).optional(),
  priority: z.number().min(1).max(5).optional(),
  related_skills: z.array(RelatedSkillSchema).optional(),
  action_plans: z.array(ActionPlanSchema).optional(),
  feedback: z.array(FeedbackSchema).optional()
});

const RequestBodySchema = z.object({
  year: z.number().min(2020).max(2030),
  operation_type: z.enum(['add', 'update', 'delete']),
  career_goals: z.array(CareerGoalSchema)
});

// レスポンス型定義
interface UpdatedGoal {
  goal_id: string;
  goal_type: string;
  title: string;
  status: string;
  updated_at: string;
}

interface ApiResponse {
  user_id: string;
  year: number;
  updated_goals: UpdatedGoal[];
  operation_type: string;
  operation_result: string;
  last_updated: string;
  last_updated_by: string;
}

interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}

/**
 * キャリア目標更新API
 * PUT /api/career-goals/{user_id}
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { user_id: string } }
): Promise<NextResponse<ApiResponse | ErrorResponse>> {
  try {
    const { user_id } = params;
    
    // 認証チェック（簡易実装）
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        {
          error: {
            code: 'UNAUTHORIZED',
            message: '認証が必要です'
          }
        },
        { status: 401 }
      );
    }

    // リクエストボディの取得とバリデーション
    let requestBody;
    try {
      requestBody = await request.json();
    } catch (error) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: 'リクエストボディの形式が正しくありません'
          }
        },
        { status: 400 }
      );
    }

    // バリデーション実行
    const validationResult = RequestBodySchema.safeParse(requestBody);
    if (!validationResult.success) {
      const errorDetails = validationResult.error.errors
        .map(err => `${err.path.join('.')}: ${err.message}`)
        .join(', ');
      
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: errorDetails
          }
        },
        { status: 400 }
      );
    }

    const { year, operation_type, career_goals } = validationResult.data;

    // ユーザーIDの存在チェック（モック実装）
    if (!user_id || user_id.trim() === '') {
      return NextResponse.json(
        {
          error: {
            code: 'USER_NOT_FOUND',
            message: 'ユーザーが見つかりません'
          }
        },
        { status: 404 }
      );
    }

    // 過去年度の変更チェック
    const currentYear = new Date().getFullYear();
    if (year < currentYear) {
      return NextResponse.json(
        {
          error: {
            code: 'PAST_YEAR_MODIFICATION',
            message: '過去の年度は変更できません'
          }
        },
        { status: 400 }
      );
    }

    // 操作タイプ別のバリデーション
    for (const goal of career_goals) {
      if (operation_type === 'update' || operation_type === 'delete') {
        if (!goal.goal_id) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_PARAMETER',
                message: 'パラメータが不正です',
                details: '更新・削除時は目標IDが必須です'
              }
            },
            { status: 400 }
          );
        }
      }

      if (operation_type === 'add' || operation_type === 'update') {
        if (!goal.goal_type || !goal.title || !goal.target_date || !goal.status || goal.priority === undefined) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_PARAMETER',
                message: 'パラメータが不正です',
                details: '新規追加・更新時は目標タイプ、タイトル、目標達成予定日、ステータス、優先度が必須です'
              }
            },
            { status: 400 }
          );
        }
      }
    }

    // 現在時刻
    const now = new Date().toISOString();

    // モック実装：操作タイプに応じた処理
    const updatedGoals: UpdatedGoal[] = [];

    for (const goal of career_goals) {
      let goalId: string;
      let goalType: string;
      let title: string;
      let status: string;

      switch (operation_type) {
        case 'add':
          goalId = `G${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          goalType = goal.goal_type!;
          title = goal.title!;
          status = goal.status!;
          break;

        case 'update':
          goalId = goal.goal_id!;
          goalType = goal.goal_type!;
          title = goal.title!;
          status = goal.status!;
          break;

        case 'delete':
          goalId = goal.goal_id!;
          goalType = 'unknown'; // 削除時は既存データから取得する想定
          title = 'deleted_goal';
          status = 'cancelled';
          break;

        default:
          continue;
      }

      updatedGoals.push({
        goal_id: goalId,
        goal_type: goalType,
        title: title,
        status: status,
        updated_at: now
      });
    }

    // 成功レスポンス
    const response: ApiResponse = {
      user_id: user_id,
      year: year,
      updated_goals: updatedGoals,
      operation_type: operation_type,
      operation_result: 'success',
      last_updated: now,
      last_updated_by: user_id // 実際の実装では認証情報から取得
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('キャリア目標更新API エラー:', error);
    
    return NextResponse.json(
      {
        error: {
          code: 'SYSTEM_ERROR',
          message: 'システムエラーが発生しました'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * キャリア目標作成API
 * POST /api/career-goals/{user_id}
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { user_id: string } }
): Promise<NextResponse<ApiResponse | ErrorResponse>> {
  try {
    const { user_id } = params;
    
    // 認証チェック（簡易実装）
    const authHeader = request.headers.get('authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return NextResponse.json(
        {
          error: {
            code: 'UNAUTHORIZED',
            message: '認証が必要です'
          }
        },
        { status: 401 }
      );
    }

    // リクエストボディの取得とバリデーション
    let requestBody;
    try {
      requestBody = await request.json();
    } catch (error) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: 'リクエストボディの形式が正しくありません'
          }
        },
        { status: 400 }
      );
    }

    // POSTの場合は直接CareerGoalオブジェクトを受け取る
    const year = requestBody.year || new Date().getFullYear();
    
    // 必須フィールドの簡易バリデーション
    if (!requestBody.title || !requestBody.status) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: 'タイトルとステータスは必須です'
          }
        },
        { status: 400 }
      );
    }

    const career_goals = [requestBody];

    // ユーザーIDの存在チェック（モック実装）
    if (!user_id || user_id.trim() === '') {
      return NextResponse.json(
        {
          error: {
            code: 'USER_NOT_FOUND',
            message: 'ユーザーが見つかりません'
          }
        },
        { status: 404 }
      );
    }

    // 現在時刻
    const now = new Date().toISOString();

    // 新規目標作成
    const goal = career_goals[0];
    if (!goal) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: 'キャリア目標データが必要です'
          }
        },
        { status: 400 }
      );
    }

    const goalId = `G${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const updatedGoal: UpdatedGoal = {
      goal_id: goalId,
      goal_type: goal.goal_type || 'short_term',
      title: goal.title || '',
      status: goal.status || 'not_started',
      updated_at: now
    };

    // 成功レスポンス
    const response: ApiResponse = {
      user_id: user_id,
      year: year,
      updated_goals: [updatedGoal],
      operation_type: 'add',
      operation_result: 'success',
      last_updated: now,
      last_updated_by: user_id
    };

    return NextResponse.json(response, { status: 201 });

  } catch (error) {
    console.error('キャリア目標作成API エラー:', error);
    
    return NextResponse.json(
      {
        error: {
          code: 'SYSTEM_ERROR',
          message: 'システムエラーが発生しました'
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
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
