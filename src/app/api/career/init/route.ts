/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア初期データ取得API (API-700)
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// レスポンス型定義
interface CareerGoalData {
  id?: string;
  target_position?: string;
  target_date?: string;
  target_description?: string;
  current_level?: string;
  target_level?: string;
  progress_percentage?: number;
  plan_status?: 'ACTIVE' | 'INACTIVE' | 'COMPLETED';
  last_review_date?: string | null;
  next_review_date?: string | null;
}

interface SkillCategory {
  id: string;
  name: string;
  short_name: string;
  type: string;
  parent_id: string | null;
  level: number;
  description: string;
  icon_url: string | null;
  color_code: string;
}

interface Position {
  id: string;
  name: string;
  short_name: string;
  level: number;
  rank: number;
  category: string;
  authority_level: number;
  is_management: boolean;
  is_executive: boolean;
  description: string;
}

interface CareerInitResponse {
  success: true;
  data: {
    career_goal: CareerGoalData;  // 互換性のため残す
    career_goals: CareerGoalData[];  // 複数目標に対応
    skill_categories: SkillCategory[];
    positions: Position[];
  };
  timestamp: string;
}

interface ErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: string;
  };
  timestamp: string;
}

/**
 * データベースデータをAPI形式に変換
 */
function transformCareerPlanToAPI(careerPlan: any): CareerGoalData {
  if (!careerPlan) {
    return {};
  }

  return {
    id: careerPlan.career_plan_id || '',
    target_position: careerPlan.target_position_id || '',
    target_date: careerPlan.plan_end_date ? careerPlan.plan_end_date.toISOString().split('T')[0] : '',
    target_description: careerPlan.plan_description || '',
    current_level: careerPlan.current_level || 'JUNIOR',
    target_level: careerPlan.target_level || 'SENIOR',
    progress_percentage: careerPlan.progress_percentage ? Number(careerPlan.progress_percentage) : 0,
    plan_status: careerPlan.plan_status || 'ACTIVE',
    last_review_date: careerPlan.last_review_date ? careerPlan.last_review_date.toISOString().split('T')[0] : null,
    next_review_date: careerPlan.next_review_date ? careerPlan.next_review_date.toISOString().split('T')[0] : null
  };
}

function transformSkillCategoryToAPI(category: any): SkillCategory {
  return {
    id: category.category_code || '',
    name: category.category_name || '',
    short_name: category.category_name_short || category.category_name || '',
    type: category.category_type || 'TECHNICAL',
    parent_id: category.parent_category_id || null,
    level: category.category_level || 1,
    description: category.description || '',
    icon_url: category.icon_url || null,
    color_code: category.color_code || '#3B82F6'
  };
}

function transformPositionToAPI(position: any): Position {
  return {
    id: position.position_code || '',
    name: position.position_name || '',
    short_name: position.position_name_short || position.position_name || '',
    level: position.position_level || 1,
    rank: position.position_rank || position.position_level || 1,
    category: position.position_category || 'GENERAL',
    authority_level: position.authority_level || 1,
    is_management: position.is_management || false,
    is_executive: position.is_executive || false,
    description: position.description || ''
  };
}

/**
 * キャリア初期データ取得API
 * GET /api/career/init
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<CareerInitResponse | ErrorResponse>> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || 'emp_001';

    // クエリパラメータから年度を取得
    const { searchParams } = new URL(request.url);
    const year = searchParams.get('year') ? parseInt(searchParams.get('year')!) : new Date().getFullYear();

    // 1. キャリアプランデータを取得（複数）
    const careerPlans = await prisma.careerPlan.findMany({
      where: {
        employee_id: userId,
        is_deleted: false
      },
      orderBy: {
        created_at: 'desc'
      }
    });
    
    // アクティブなプランを優先
    const careerPlan = careerPlans.find(plan => plan.plan_status === 'ACTIVE') || careerPlans[0];

    // 2. スキルカテゴリデータを取得
    const skillCategories = await prisma.skillCategory.findMany({
      where: {
        is_deleted: false
      },
      orderBy: [
        { category_level: 'asc' },
        { category_name: 'asc' }
      ]
    });

    // 3. ポジションデータを取得
    const positions = await prisma.position.findMany({
      where: {
        is_deleted: false
      },
      orderBy: [
        { position_level: 'asc' },
        { position_rank: 'asc' }
      ]
    });

    // レスポンス形式に変換
    const responseData: CareerInitResponse = {
      success: true,
      data: {
        career_goal: transformCareerPlanToAPI(careerPlan),  // 互換性のため残す
        career_goals: careerPlans.map(transformCareerPlanToAPI),  // 複数目標を返す
        skill_categories: skillCategories.map(transformSkillCategoryToAPI),
        positions: positions.map(transformPositionToAPI)
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { status: 200 });

  } catch (error) {
    console.error('キャリア初期データ取得API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'CAREER_INIT_ERROR',
          message: 'キャリア初期データの取得に失敗しました',
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
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, x-user-id',
    },
  });
}
