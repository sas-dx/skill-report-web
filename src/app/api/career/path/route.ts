/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリアパス取得API (API-703)
 */

import { NextRequest, NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

// レスポンス型定義
interface CareerPathStep {
  step_id: string;
  position_name: string;
  position_level: number;
  required_skills: Array<{
    skill_id: string;
    skill_name: string;
    required_level: number;
    current_level: number;
    is_achieved: boolean;
  }>;
  estimated_duration: string;
  prerequisites: string[];
  description: string;
  is_current: boolean;
  is_completed: boolean;
}

interface CareerPathData {
  path_id: string;
  path_name: string;
  current_position: string;
  target_position: string;
  total_duration: string;
  completion_percentage: number;
  steps: CareerPathStep[];
  alternative_paths: Array<{
    path_id: string;
    path_name: string;
    target_position: string;
    estimated_duration: string;
  }>;
}

interface CareerPathResponse {
  success: true;
  data: {
    career_path: CareerPathData;
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
 * スキル達成状況を判定
 */
function isSkillAchieved(currentLevel: number, requiredLevel: number): boolean {
  return currentLevel >= requiredLevel;
}

/**
 * 完了率を計算
 */
function calculateCompletionPercentage(steps: CareerPathStep[]): number {
  if (steps.length === 0) return 0;
  
  const completedSteps = steps.filter(step => step.is_completed).length;
  return Math.round((completedSteps / steps.length) * 100);
}

/**
 * キャリアパス取得API
 * GET /api/career/path
 */
export async function GET(
  request: NextRequest
): Promise<NextResponse<CareerPathResponse | ErrorResponse>> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || 'emp_001';

    // クエリパラメータを取得
    const { searchParams } = new URL(request.url);
    const targetPosition = searchParams.get('target_position');

    // ユーザーの現在のポジション情報を取得
    const employee = await prisma.employee.findFirst({
      where: {
        id: userId,
        is_deleted: false
      }
    });

    if (!employee) {
      return NextResponse.json(
        {
          success: false,
          error: {
            code: 'EMPLOYEE_NOT_FOUND',
            message: '従業員情報が見つかりません'
          },
          timestamp: new Date().toISOString()
        },
        { status: 404 }
      );
    }

    // ユーザーのキャリアプランを取得
    const careerPlan = await prisma.careerPlan.findFirst({
      where: {
        employee_id: userId,
        is_deleted: false,
        plan_status: 'ACTIVE'
      }
    });

    // ポジション一覧を取得
    const positions = await prisma.position.findMany({
      where: {
        is_deleted: false,
        position_status: 'ACTIVE'
      },
      orderBy: {
        position_level: 'asc'
      }
    });

    // ユーザーの現在のスキルレベルを取得
    const userSkills = await prisma.skillRecord.findMany({
      where: {
        employee_id: userId,
        is_deleted: false
      }
    });

    // スキル詳細情報を取得
    const skillItems = await prisma.skillItem.findMany({
      where: {
        is_deleted: false
      }
    });

    // スキルマップを作成
    const skillMap = new Map();
    skillItems.forEach(skill => {
      skillMap.set(skill.skill_code, skill);
    });

    // ユーザースキルマップを作成
    const userSkillMap = new Map();
    userSkills.forEach(skill => {
      userSkillMap.set(skill.skill_item_id, skill.skill_level || 1);
    });

    // 現在のポジションを特定
    const currentPosition = employee.position_id || 'JUNIOR_ENGINEER';
    const currentPositionInfo = positions.find(p => p.position_code === currentPosition);

    // 目標ポジションを決定
    const targetPos = targetPosition || careerPlan?.target_position_id || 'SENIOR_ENGINEER';
    const targetPositionInfo = positions.find(p => p.position_code === targetPos);

    // キャリアパスのステップを生成
    const careerSteps: CareerPathStep[] = [];

    // サンプルキャリアパスデータを生成
    const sampleSteps = [
      {
        step_id: 'step_001',
        position_name: 'ジュニアエンジニア',
        position_level: 1,
        required_skills: [
          {
            skill_id: 'PROG_001',
            skill_name: 'JavaScript',
            required_level: 2,
            current_level: userSkillMap.get('PROG_001') || 1,
            is_achieved: isSkillAchieved(userSkillMap.get('PROG_001') || 1, 2)
          },
          {
            skill_id: 'PROG_002',
            skill_name: 'HTML/CSS',
            required_level: 2,
            current_level: userSkillMap.get('PROG_002') || 1,
            is_achieved: isSkillAchieved(userSkillMap.get('PROG_002') || 1, 2)
          }
        ],
        estimated_duration: '6ヶ月',
        prerequisites: ['基本的なプログラミング知識'],
        description: 'Webアプリケーション開発の基礎を習得し、チームでの開発に参加できるレベル',
        is_current: currentPosition === 'JUNIOR_ENGINEER',
        is_completed: (userSkillMap.get('PROG_001') || 1) >= 2 && (userSkillMap.get('PROG_002') || 1) >= 2
      },
      {
        step_id: 'step_002',
        position_name: 'エンジニア',
        position_level: 2,
        required_skills: [
          {
            skill_id: 'PROG_003',
            skill_name: 'React.js',
            required_level: 3,
            current_level: userSkillMap.get('PROG_003') || 1,
            is_achieved: isSkillAchieved(userSkillMap.get('PROG_003') || 1, 3)
          },
          {
            skill_id: 'PROG_004',
            skill_name: 'Node.js',
            required_level: 2,
            current_level: userSkillMap.get('PROG_004') || 1,
            is_achieved: isSkillAchieved(userSkillMap.get('PROG_004') || 1, 2)
          }
        ],
        estimated_duration: '12ヶ月',
        prerequisites: ['ジュニアエンジニアレベルのスキル習得'],
        description: 'フロントエンド・バックエンド両方の開発ができ、独立してタスクを完了できるレベル',
        is_current: currentPosition === 'ENGINEER',
        is_completed: (userSkillMap.get('PROG_003') || 1) >= 3 && (userSkillMap.get('PROG_004') || 1) >= 2
      },
      {
        step_id: 'step_003',
        position_name: 'シニアエンジニア',
        position_level: 3,
        required_skills: [
          {
            skill_id: 'ARCH_001',
            skill_name: 'システム設計',
            required_level: 3,
            current_level: userSkillMap.get('ARCH_001') || 1,
            is_achieved: isSkillAchieved(userSkillMap.get('ARCH_001') || 1, 3)
          },
          {
            skill_id: 'MGMT_001',
            skill_name: 'チームリーダーシップ',
            required_level: 2,
            current_level: userSkillMap.get('MGMT_001') || 1,
            is_achieved: isSkillAchieved(userSkillMap.get('MGMT_001') || 1, 2)
          }
        ],
        estimated_duration: '18ヶ月',
        prerequisites: ['エンジニアレベルのスキル習得', '複数プロジェクトでの実績'],
        description: '技術的なリーダーシップを発揮し、アーキテクチャ設計やチーム指導ができるレベル',
        is_current: currentPosition === 'SENIOR_ENGINEER',
        is_completed: (userSkillMap.get('ARCH_001') || 1) >= 3 && (userSkillMap.get('MGMT_001') || 1) >= 2
      }
    ];

    // 代替キャリアパスを生成
    const alternativePaths = [
      {
        path_id: 'path_002',
        path_name: 'プロダクトマネージャーパス',
        target_position: 'プロダクトマネージャー',
        estimated_duration: '24ヶ月'
      },
      {
        path_id: 'path_003',
        path_name: 'テックリードパス',
        target_position: 'テックリード',
        estimated_duration: '30ヶ月'
      },
      {
        path_id: 'path_004',
        path_name: 'アーキテクトパス',
        target_position: 'ソリューションアーキテクト',
        estimated_duration: '36ヶ月'
      }
    ];

    // 完了率を計算
    const completionPercentage = calculateCompletionPercentage(sampleSteps);

    const careerPathData: CareerPathData = {
      path_id: careerPlan?.career_plan_id || 'default_path_001',
      path_name: careerPlan?.plan_name || 'エンジニアキャリアパス',
      current_position: currentPositionInfo?.position_name || 'ジュニアエンジニア',
      target_position: targetPositionInfo?.position_name || 'シニアエンジニア',
      total_duration: '36ヶ月',
      completion_percentage: completionPercentage,
      steps: sampleSteps,
      alternative_paths: alternativePaths
    };

    const responseData: CareerPathResponse = {
      success: true,
      data: {
        career_path: careerPathData
      },
      timestamp: new Date().toISOString()
    };

    return NextResponse.json(responseData, { status: 200 });

  } catch (error) {
    console.error('キャリアパス取得API エラー:', error);
    
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'CAREER_PATH_ERROR',
          message: 'キャリアパスの取得に失敗しました',
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
