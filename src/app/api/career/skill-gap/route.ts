/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: スキルギャップ取得API (API-702)
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// レスポンス型定義
interface SkillGapData {
  skill_categories: Array<{
    category_id: string;
    category_name: string;
    current_level: number;
    target_level: number;
    gap_score: number;
    skills: Array<{
      skill_id: string;
      skill_name: string;
      current_level: number;
      target_level: number;
      gap_score: number;
      priority: 'HIGH' | 'MEDIUM' | 'LOW';
    }>;
  }>;
  overall_gap_score: number;
  priority_skills: Array<{
    skill_id: string;
    skill_name: string;
    category_name: string;
    gap_score: number;
    recommended_actions: string[];
  }>;
  radar_chart_data: {
    labels: string[];
    current_levels: number[];
    target_levels: number[];
  };
}

interface SkillGapResponse {
  success: true;
  data: {
    skill_gap_data: SkillGapData;
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
 * スキルレベルを正規化（1-4スケール）
 */
function normalizeSkillLevel(level: number | null): number {
  if (!level || level < 1) return 1;
  if (level > 4) return 4;
  return level;
}

/**
 * ギャップスコアを計算（0-100スケール）
 */
function calculateGapScore(currentLevel: number, targetLevel: number): number {
  if (targetLevel <= currentLevel) return 0;
  const maxGap = 3; // 最大ギャップ（レベル1→4）
  const actualGap = targetLevel - currentLevel;
  return Math.round((actualGap / maxGap) * 100);
}

/**
 * 優先度を決定
 */
function determinePriority(gapScore: number): 'HIGH' | 'MEDIUM' | 'LOW' {
  if (gapScore >= 75) return 'HIGH';
  if (gapScore >= 50) return 'MEDIUM';
  return 'LOW';
}

/**
 * 推奨アクションを生成
 */
function generateRecommendedActions(skillName: string, gapScore: number): string[] {
  const actions: string[] = [];
  
  if (gapScore >= 75) {
    actions.push(`${skillName}の基礎研修を受講する`);
    actions.push(`${skillName}関連の資格取得を検討する`);
    actions.push(`実践プロジェクトでの${skillName}活用機会を探す`);
  } else if (gapScore >= 50) {
    actions.push(`${skillName}の応用研修を受講する`);
    actions.push(`${skillName}を活用したプロジェクトに参加する`);
  } else if (gapScore > 0) {
    actions.push(`${skillName}の最新動向をキャッチアップする`);
    actions.push(`${skillName}の実践経験を積む`);
  }
  
  return actions;
}

/**
 * スキルギャップ取得API
 * GET /api/career/skill-gap
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<SkillGapResponse | ErrorResponse>> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || 'emp_001';

    // ユーザーの現在のスキルレベルを取得
    const currentSkills = await prisma.skillRecord.findMany({
      where: {
        employee_id: userId,
        is_deleted: false
      }
    });

    // スキルカテゴリ一覧を取得
    const skillCategories = await prisma.skillCategory.findMany({
      where: {
        is_deleted: false,
        category_status: 'ACTIVE'
      },
      orderBy: {
        display_order: 'asc'
      }
    });

    // スキル詳細情報を取得
    const skillItems = await prisma.skillItem.findMany({
      where: {
        is_deleted: false
      }
    });

    // ユーザーのキャリアプランから目標スキルレベルを取得
    const careerPlan = await prisma.careerPlan.findFirst({
      where: {
        employee_id: userId,
        is_deleted: false,
        plan_status: 'ACTIVE'
      }
    });

    // スキルマップを作成
    const skillMap = new Map();
    skillItems.forEach(skill => {
      skillMap.set(skill.skill_code, skill);
    });

    // カテゴリマップを作成
    const categoryMap = new Map();
    skillCategories.forEach(category => {
      categoryMap.set(category.category_code, category);
    });

    // スキルギャップデータを構築
    const skillGapCategories: any[] = [];
    const radarLabels: string[] = [];
    const radarCurrentLevels: number[] = [];
    const radarTargetLevels: number[] = [];
    const prioritySkills: any[] = [];

    let totalGapScore = 0;
    let skillCount = 0;

    // カテゴリごとにスキルギャップを計算
    for (const category of skillCategories.slice(0, 8)) { // レーダーチャート用に最大8カテゴリ
      const categorySkills = currentSkills.filter(skill => {
        const skillItem = skillMap.get(skill.skill_item_id);
        return skillItem && skillItem.skill_category_id === category.category_code;
      });

      let categoryCurrent = 0;
      let categoryTarget = 0;
      let categorySkillCount = 0;
      const categorySkillDetails: any[] = [];

      // カテゴリ内のスキルを処理
      for (const skillRecord of categorySkills.slice(0, 5)) { // カテゴリあたり最大5スキル
        const skillItem = skillMap.get(skillRecord.skill_item_id);
        if (!skillItem) continue;

        const currentLevel = normalizeSkillLevel(skillRecord.skill_level);
        const targetLevel = normalizeSkillLevel((skillRecord.skill_level || 1) + 1); // デフォルトで1レベル上を目標
        const gapScore = calculateGapScore(currentLevel, targetLevel);

        categoryCurrent += currentLevel;
        categoryTarget += targetLevel;
        categorySkillCount++;

        const skillDetail = {
          skill_id: skillItem.skill_code,
          skill_name: skillItem.skill_name || 'Unknown Skill',
          current_level: currentLevel,
          target_level: targetLevel,
          gap_score: gapScore,
          priority: determinePriority(gapScore)
        };

        categorySkillDetails.push(skillDetail);

        // 優先度の高いスキルを抽出
        if (gapScore >= 50) {
          prioritySkills.push({
            skill_id: skillItem.skill_code,
            skill_name: skillItem.skill_name || 'Unknown Skill',
            category_name: category.category_name || 'Unknown Category',
            gap_score: gapScore,
            recommended_actions: generateRecommendedActions(skillItem.skill_name || 'Unknown Skill', gapScore)
          });
        }

        totalGapScore += gapScore;
        skillCount++;
      }

      // カテゴリ平均を計算
      const avgCurrent = categorySkillCount > 0 ? categoryCurrent / categorySkillCount : 1;
      const avgTarget = categorySkillCount > 0 ? categoryTarget / categorySkillCount : 2;
      const categoryGapScore = calculateGapScore(avgCurrent, avgTarget);

      skillGapCategories.push({
        category_id: category.category_code,
        category_name: category.category_name || 'Unknown Category',
        current_level: Math.round(avgCurrent * 10) / 10,
        target_level: Math.round(avgTarget * 10) / 10,
        gap_score: categoryGapScore,
        skills: categorySkillDetails
      });

      // レーダーチャート用データ
      radarLabels.push(category.category_name_short || category.category_name || 'Unknown');
      radarCurrentLevels.push(Math.round(avgCurrent * 10) / 10);
      radarTargetLevels.push(Math.round(avgTarget * 10) / 10);
    }

    // 全体のギャップスコアを計算
    const overallGapScore = skillCount > 0 ? Math.round(totalGapScore / skillCount) : 0;

    // 優先度順にソート
    prioritySkills.sort((a, b) => b.gap_score - a.gap_score);

    const skillGapData: SkillGapData = {
      skill_categories: skillGapCategories,
      overall_gap_score: overallGapScore,
      priority_skills: prioritySkills.slice(0, 10), // 上位10スキル
      radar_chart_data: {
        labels: radarLabels,
        current_levels: radarCurrentLevels,
        target_levels: radarTargetLevels
      }
    };

    const responseData: SkillGapResponse = {
      success: true,
      data: {
        skill_gap_data: skillGapData
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { status: 200 });

  } catch (error) {
    console.error('スキルギャップ取得API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'SKILL_GAP_DATA_ERROR',
          message: 'スキルギャップデータの取得に失敗しました',
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
