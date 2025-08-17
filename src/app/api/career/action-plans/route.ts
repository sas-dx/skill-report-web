/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: アクションプラン一覧取得・作成API (API-703, API-706)
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';
import { 
  ActionPlan,
  ActionPlanGetResponse,
  ActionPlanCreateRequest,
  ActionPlanCreateResponse
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
 * 入力値バリデーション（作成用）
 */
function validateActionPlanCreateRequest(data: any): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (!data.title || typeof data.title !== 'string' || data.title.trim().length === 0) {
    errors.push('タイトルは必須です');
  }

  if (data.title && data.title.length > 200) {
    errors.push('タイトルは200文字以内で入力してください');
  }

  if (!data.due_date || typeof data.due_date !== 'string') {
    errors.push('期限は必須です');
  } else {
    const dueDate = new Date(data.due_date);
    if (isNaN(dueDate.getTime())) {
      errors.push('期限の形式が正しくありません');
    }
  }

  if (data.description && data.description.length > 1000) {
    errors.push('説明は1000文字以内で入力してください');
  }

  if (data.priority && !['high', 'medium', 'low'].includes(data.priority)) {
    errors.push('優先度は high, medium, low のいずれかを指定してください');
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
 * アクションプラン取得API (API-703)
 * GET /api/career/action-plans
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<ActionPlanGetResponse>> {
  try {
    // ヘッダーからユーザーIDを取得（デフォルト値として000001を使用）
    const userId = request.headers.get('x-user-id') || '000001';
    
    console.log('ActionPlans GET - userId:', userId);

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const page = parseInt(searchParams.get('page') || '1');
    const limit = parseInt(searchParams.get('limit') || '20');
    const status = searchParams.get('status');
    const priority = searchParams.get('priority');
    const category = searchParams.get('category');

    // フィルタ条件の構築
    const whereConditions: any = {
      employee_id: userId,
      is_deleted: false,
      goal_type: 'ACTION_PLAN' // アクションプランとして識別
    };

    if (status) {
      const achievementStatus = mapActionStatusToAchievementStatus(status);
      whereConditions.achievement_status = achievementStatus;
    }

    if (priority) {
      const priorityLevel = mapActionPriorityToPriorityLevel(priority);
      whereConditions.priority_level = priorityLevel;
    }

    if (category) {
      whereConditions.goal_category = category;
    }

    // 総件数取得
    const totalCount = await prisma.goalProgress.count({
      where: whereConditions
    });

    // データ取得（ページネーション付き）
    const actionPlans = await prisma.goalProgress.findMany({
      where: whereConditions,
      orderBy: [
        { priority_level: 'asc' },
        { target_date: 'asc' },
        { created_at: 'desc' }
      ],
      skip: (page - 1) * limit,
      take: limit
    });

    // レスポンス形式に変換
    const responseData: ActionPlanGetResponse = {
      success: true,
      data: {
        action_plans: actionPlans.map(transformGoalProgressToActionPlan),
        total_count: totalCount,
        pagination: {
          page,
          limit,
          total_pages: Math.ceil(totalCount / limit)
        }
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { 
      status: 200,
      headers: {
        'Content-Type': 'application/json; charset=utf-8'
      }
    });

  } catch (error) {
    console.error('アクションプラン取得API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'ACTION_PLAN_GET_ERROR',
          message: 'アクションプランの取得に失敗しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        },
        timestamp: new Date().toISOString()
      },
      { status: 500 }
    );
  }
}

/**
 * アクションプラン追加API (API-706)
 * POST /api/career/action-plans
 */
export async function POST(
  request: NextRequest
): Promise<NextResponse<ActionPlanCreateResponse>> {
  try {
    // ヘッダーからユーザーIDを取得（デフォルト値として000001を使用）
    const userId = request.headers.get('x-user-id') || '000001';
    
    console.log('ActionPlans POST - userId:', userId);

    // リクエストボディの取得
    const requestData: ActionPlanCreateRequest = await request.json();

    // 入力値バリデーション
    const validation = validateActionPlanCreateRequest(requestData);
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

    // 新規アクションプランの作成
    const goalId = `AP${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const recordId = `GP${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const newActionPlan = await prisma.goalProgress.create({
      data: {
        id: recordId,
        goal_id: goalId,
        employee_id: userId,
        goal_title: requestData.title,
        goal_description: requestData.description || '',
        goal_category: requestData.category || 'ACTION_PLAN',
        goal_type: 'ACTION_PLAN',
        priority_level: mapActionPriorityToPriorityLevel(requestData.priority || 'medium'),
        target_date: new Date(requestData.due_date),
        achievement_status: 'not_started',
        progress_rate: 0,
        related_career_plan_id: requestData.related_career_plan_id || null,
        related_skill_items: requestData.related_skill_id || null,
        tenant_id: 'default', // 将来のマルチテナント対応
        created_by: userId,
        updated_by: userId,
        created_at: new Date(),
        updated_at: new Date(),
        is_deleted: false
      }
    });

    // レスポンス形式に変換
    const responseData: ActionPlanCreateResponse = {
      success: true,
      data: {
        action_plan: transformGoalProgressToActionPlan(newActionPlan)
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { 
      status: 201,
      headers: {
        'Content-Type': 'application/json; charset=utf-8'
      }
    });

  } catch (error) {
    console.error('アクションプラン追加API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'ACTION_PLAN_CREATE_ERROR',
          message: 'アクションプランの作成に失敗しました',
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
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-user-id',
    },
  });
}