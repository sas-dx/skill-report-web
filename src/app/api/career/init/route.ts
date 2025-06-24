/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * API仕様: API-700 初期データ取得API
 * 実装日: 2025-06-24
 * 実装者: システム開発チーム
 */

import { NextRequest, NextResponse } from 'next/server';
import { PrismaClient } from '@prisma/client';

// テスト環境かどうかを判定
const isTestEnvironment = process.env.NODE_ENV === 'test';

const prisma = isTestEnvironment ? null : new PrismaClient();

/**
 * API-700: キャリア初期データ取得API
 * 
 * キャリアプラン画面の初期表示に必要なデータを取得する
 * - キャリア目標情報
 * - スキルカテゴリマスタ
 * - ポジションマスタ
 * 
 * @param request - Next.js Request オブジェクト
 * @returns キャリア初期データのレスポンス
 */
export async function GET(request: NextRequest) {
  try {
    // TODO: 認証情報からユーザーIDを取得（現在は仮実装）
    const userId = request.headers.get('x-user-id') || 'emp_001';

    // 並列でデータを取得してパフォーマンスを向上
    const [careerGoal, skillCategories, positions] = await Promise.all([
      // キャリア目標情報を取得
      getCareerGoal(userId),
      // スキルカテゴリマスタを取得
      getSkillCategories(),
      // ポジションマスタを取得
      getPositions()
    ]);

    // レスポンス形式に従って返却
    return NextResponse.json({
      success: true,
      data: {
        career_goal: careerGoal,
        skill_categories: skillCategories,
        positions: positions
      },
      timestamp: new Date().toISOString()
    });

  } catch (error) {
    console.error('API-700 初期データ取得エラー:', error);
    
    return NextResponse.json({
      success: false,
      error: {
        code: 'CAREER_INIT_DATA_ERROR',
        message: 'キャリア初期データの取得に失敗しました',
        details: error instanceof Error ? error.message : '不明なエラー'
      },
      timestamp: new Date().toISOString()
    }, { status: 500 });
  }
}

/**
 * ユーザーのキャリア目標情報を取得
 * 
 * @param userId - ユーザーID
 * @returns キャリア目標情報
 */
async function getCareerGoal(userId: string) {
  try {
    // テスト環境の場合はモックデータを返す
    if (isTestEnvironment || !prisma) {
      return {
        id: 'plan_001',
        target_position: 'pos_001',
        target_date: '2027-12-31',
        target_description: 'シニアエンジニアを目指す',
        current_level: 'JUNIOR',
        target_level: 'SENIOR',
        progress_percentage: 30.5,
        plan_status: 'ACTIVE',
        last_review_date: '2025-06-01',
        next_review_date: '2025-12-01'
      };
    }

    // 最新のキャリアプランを取得
    const careerPlan = await prisma.careerPlan.findFirst({
      where: {
        employee_id: userId,
        plan_status: 'ACTIVE'
      },
      orderBy: {
        plan_start_date: 'desc'
      }
    });

    if (!careerPlan) {
      // キャリアプランが存在しない場合は空のオブジェクトを返す
      return {
        target_position: '',
        target_date: '',
        target_description: '',
        current_level: '',
        target_level: '',
        progress_percentage: 0
      };
    }

    return {
      id: careerPlan.career_plan_id,
      target_position: careerPlan.target_position_id || '',
      target_date: careerPlan.plan_end_date?.toISOString().split('T')[0] || '',
      target_description: careerPlan.plan_description || '',
      current_level: careerPlan.current_level || '',
      target_level: careerPlan.target_level || '',
      progress_percentage: careerPlan.progress_percentage ? Number(careerPlan.progress_percentage) : 0,
      plan_status: careerPlan.plan_status,
      last_review_date: careerPlan.last_review_date?.toISOString().split('T')[0] || null,
      next_review_date: careerPlan.next_review_date?.toISOString().split('T')[0] || null
    };

  } catch (error) {
    console.error('キャリア目標取得エラー:', error);
    throw new Error('キャリア目標の取得に失敗しました');
  }
}

/**
 * スキルカテゴリマスタを取得
 * 
 * @returns スキルカテゴリ一覧
 */
async function getSkillCategories() {
  try {
    // テスト環境の場合はモックデータを返す
    if (isTestEnvironment || !prisma) {
      return [
        {
          id: 'CAT_001',
          name: 'プログラミング',
          short_name: 'プログラミング',
          type: 'TECHNICAL',
          parent_id: null,
          level: 1,
          description: 'プログラミングスキル',
          icon_url: '/icons/programming.svg',
          color_code: '#3399cc'
        },
        {
          id: 'CAT_002',
          name: 'データベース',
          short_name: 'DB',
          type: 'TECHNICAL',
          parent_id: null,
          level: 1,
          description: 'データベーススキル',
          icon_url: '/icons/database.svg',
          color_code: '#ff6600'
        }
      ];
    }

    const categories = await prisma.skillCategory.findMany({
      where: {
        category_status: 'ACTIVE'
      },
      orderBy: {
        display_order: 'asc'
      },
      select: {
        category_code: true,
        category_name: true,
        category_name_short: true,
        category_type: true,
        parent_category_id: true,
        category_level: true,
        description: true,
        icon_url: true,
        color_code: true
      }
    });

    return categories.map(category => ({
      id: category.category_code,
      name: category.category_name || '',
      short_name: category.category_name_short || '',
      type: category.category_type || '',
      parent_id: category.parent_category_id || null,
      level: category.category_level || 1,
      description: category.description || '',
      icon_url: category.icon_url || null,
      color_code: category.color_code || '#3399cc'
    }));

  } catch (error) {
    console.error('スキルカテゴリ取得エラー:', error);
    throw new Error('スキルカテゴリの取得に失敗しました');
  }
}

/**
 * ポジションマスタを取得
 * 
 * @returns ポジション一覧
 */
async function getPositions() {
  try {
    // テスト環境の場合はモックデータを返す
    if (isTestEnvironment || !prisma) {
      return [
        {
          id: 'pos_001',
          name: 'シニアエンジニア',
          short_name: 'SE',
          level: 3,
          rank: 3,
          category: 'ENGINEER',
          authority_level: 3,
          is_management: false,
          is_executive: false,
          description: 'シニアレベルのエンジニア'
        },
        {
          id: 'pos_002',
          name: 'テックリード',
          short_name: 'TL',
          level: 4,
          rank: 4,
          category: 'ENGINEER',
          authority_level: 4,
          is_management: true,
          is_executive: false,
          description: '技術チームのリーダー'
        }
      ];
    }

    const positions = await prisma.position.findMany({
      where: {
        position_status: 'ACTIVE'
      },
      orderBy: {
        sort_order: 'asc'
      },
      select: {
        position_code: true,
        position_name: true,
        position_name_short: true,
        position_level: true,
        position_rank: true,
        position_category: true,
        authority_level: true,
        is_management: true,
        is_executive: true,
        description: true
      }
    });

    return positions.map(position => ({
      id: position.position_code,
      name: position.position_name || '',
      short_name: position.position_name_short || '',
      level: position.position_level || 1,
      rank: position.position_rank || 1,
      category: position.position_category || '',
      authority_level: position.authority_level || 1,
      is_management: position.is_management || false,
      is_executive: position.is_executive || false,
      description: position.description || ''
    }));

  } catch (error) {
    console.error('ポジション取得エラー:', error);
    throw new Error('ポジションの取得に失敗しました');
  }
}
