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
  milestones: string[];  // milestonesを追加
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
 * キャリアパス作成API
 * POST /api/career/path
 */
export async function POST(
  request: NextRequest
): Promise<NextResponse> {
  try {
    // ヘッダーからユーザーIDを取得
    const userId = request.headers.get('x-user-id') || '000001';
    const body = await request.json();

    // キャリアパスステップをTRN_GoalProgressに保存
    const id = `CAREER_PATH_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    const newCareerPath = await prisma.goalProgress.create({
      data: {
        id: id,  // 主キー
        goal_id: id,  // ユニークキー
        employee_id: userId,
        goal_type: 'CAREER_PATH',
        goal_title: body.position_name,
        goal_description: body.description,
        goal_category: 'CAREER',
        priority_level: String(body.position_level || 1),
        target_date: body.target_date ? new Date(body.target_date) : null,
        start_date: new Date(),
        achievement_status: 'NOT_STARTED',
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
        step_id: newCareerPath.id,
        message: 'キャリアパスステップが作成されました'
      }
    }, { status: 201 });

  } catch (error) {
    console.error('キャリアパス作成エラー:', error);
    return NextResponse.json(
      {
        success: false,
        error: {
          code: 'CAREER_PATH_CREATE_ERROR',
          message: 'キャリアパスの作成に失敗しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        }
      },
      { status: 500 }
    );
  }
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
    const userId = request.headers.get('x-user-id') || '000001';

    // クエリパラメータを取得
    const { searchParams } = new URL(request.url);
    const targetPosition = searchParams.get('target_position');

    // ユーザーの現在のポジション情報を取得
    const employee = await prisma.employee.findFirst({
      where: {
        employee_code: userId,
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

    // ユーザーのキャリアパスを取得（TRN_GoalProgressから）
    const careerPlans = await prisma.goalProgress.findMany({
      where: {
        employee_id: userId,
        goal_type: 'CAREER_PATH',
        is_deleted: false
      },
      orderBy: {
        created_at: 'asc'
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
    const targetPos = targetPosition || 'SENIOR_ENGINEER';
    const targetPositionInfo = positions.find(p => p.position_code === targetPos);

    // キャリアパスのステップを生成
    const careerSteps: CareerPathStep[] = [];
    
    // 代替キャリアパスを定義（スコープ外でも使用するため、ここで定義）
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

    // 保存されたキャリアパスからステップを生成
    console.log('取得したキャリアパス数:', careerPlans.length);
    if (careerPlans.length > 0) {
      careerPlans.forEach((plan, index) => {
        console.log(`プラン${index}: id=${plan.id}, goal_title=${plan.goal_title}`);
        
        // スキル情報のパース
        const requiredSkills = plan.support_needed ? 
          (typeof plan.support_needed === 'string' ? 
            JSON.parse(plan.support_needed) : plan.support_needed) : [];
        
        // 前提条件のパース
        const prerequisites = plan.obstacles ? 
          (typeof plan.obstacles === 'string' ? 
            JSON.parse(plan.obstacles) : plan.obstacles) : [];
        
        // マイルストーンのパース
        const milestones = plan.milestones ? 
          (typeof plan.milestones === 'string' ? 
            JSON.parse(plan.milestones) : plan.milestones) : [];

        careerSteps.push({
          step_id: plan.id,  // idフィールドを使用
          position_name: plan.goal_title || '',
          position_level: parseInt(plan.priority_level || '1'),
          required_skills: requiredSkills.map((skill: any) => ({
            skill_id: skill.skill_id || '',
            skill_name: skill.skill_name || '',
            required_level: skill.required_level || 1,
            current_level: userSkillMap.get(skill.skill_id) || 1,
            is_achieved: (userSkillMap.get(skill.skill_id) || 1) >= (skill.required_level || 1)
          })),
          estimated_duration: '',
          prerequisites: prerequisites,
          milestones: milestones,
          description: plan.goal_description || '',
          is_current: plan.achievement_status === 'IN_PROGRESS',
          is_completed: plan.achievement_status === 'COMPLETED'
        });
      });
    } else {
      // データがない場合はサンプルデータを生成
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
        milestones: ['基礎研修完了', '初めてのプロジェクト参加'],
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
        milestones: ['フルスタック開発経験', 'コードレビュー実施'],
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
        milestones: ['アーキテクチャ設計経験', 'チームリード経験', '技術選定主導'],
        description: '技術的なリーダーシップを発揮し、アーキテクチャ設計やチーム指導ができるレベル',
        is_current: currentPosition === 'SENIOR_ENGINEER',
        is_completed: (userSkillMap.get('ARCH_001') || 1) >= 3 && (userSkillMap.get('MGMT_001') || 1) >= 2
      }
    ];

      // サンプルデータをキャリアステップに追加
      careerSteps.push(...sampleSteps);
    }

    // 完了率を計算
    const completionPercentage = calculateCompletionPercentage(careerSteps);

    const careerPathData: CareerPathData = {
      path_id: careerPlans[0]?.id || 'default_path_001',
      path_name: 'エンジニアキャリアパス',
      current_position: currentPositionInfo?.position_name || 'ジュニアエンジニア',
      target_position: targetPositionInfo?.position_name || 'シニアエンジニア',
      total_duration: '36ヶ月',
      completion_percentage: completionPercentage,
      steps: careerSteps,
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
