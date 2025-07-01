/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: 
 *   - docs/design/api/specs/API定義書_API-031_キャリア目標取得API.md
 *   - docs/design/api/specs/API定義書_API-032_キャリア目標更新API.md
 * 実装内容: 
 *   - キャリア目標取得API (API-031)
 *   - キャリア目標更新API (API-032)
 */

import { NextRequest, NextResponse } from 'next/server';

// リクエスト型定義
interface RelatedSkill {
  skill_id: string;
  target_level: number;
}

interface ActionPlan {
  action_id?: string;
  title: string;
  description?: string;
  due_date: string;
  status: 'not_started' | 'in_progress' | 'completed';
  completed_date?: string;
}

interface Feedback {
  feedback_id?: string;
  comment: string;
}

interface CareerGoal {
  goal_id?: string;
  goal_type?: 'short_term' | 'mid_term' | 'long_term';
  title?: string;
  description?: string;
  target_date?: string;
  status?: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled';
  priority?: number;
  related_skills?: RelatedSkill[];
  action_plans?: ActionPlan[];
  feedback?: Feedback[];
}

interface UpdateCareerGoalRequest {
  year: number;
  operation_type: 'add' | 'update' | 'delete';
  career_goals: CareerGoal[];
}

// レスポンス型定義
interface UpdatedGoal {
  goal_id: string;
  goal_type: string;
  title: string;
  status: string;
  updated_at: string;
}

interface UpdateCareerGoalResponse {
  user_id: string;
  year: number;
  updated_goals: UpdatedGoal[];
  operation_type: string;
  operation_result: string;
  last_updated: string;
  last_updated_by: string;
}

// キャリア目標取得API用の型定義
interface Milestone {
  id: string;
  title: string;
  description: string;
  status: 'completed' | 'in_progress' | 'not_started';
  completedAt?: string;
  targetDate?: string;
  weight: number;
}

interface Progress {
  percentage: number;
  milestones?: Milestone[];
  completedAt?: string;
}

interface Metrics {
  skillAssessmentScore?: number;
  targetScore?: number;
  projectsCompleted?: number;
  targetProjects?: number;
  mentoringSessions?: number;
  targetSessions?: number;
  studyHours?: number;
  targetHours?: number;
  practiceTestScore?: number;
  currentScore?: number;
  improvementFromStart?: number;
  teamSize?: number;
  projectProgress?: number;
  teamSatisfaction?: number;
  targetSatisfaction?: number;
}

interface CareerGoalDetail {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: 'high' | 'medium' | 'low';
  status: 'not_started' | 'in_progress' | 'completed' | 'on_hold' | 'cancelled';
  targetLevel?: string;
  currentLevel?: string;
  progress: Progress;
  targetDate: string;
  createdAt: string;
  updatedAt: string;
  metrics?: Metrics;
}

interface GoalCategory {
  id: string;
  name: string;
  description: string;
  weight: number;
  progress: number;
  goals: CareerGoalDetail[];
}

interface OverallProgress {
  completionRate: number;
  totalGoals: number;
  completedGoals: number;
  inProgressGoals: number;
  notStartedGoals: number;
  lastUpdated: string;
}

interface Recommendation {
  type: 'skill_gap' | 'timeline_adjustment' | 'resource_allocation';
  priority: 'high' | 'medium' | 'low';
  title: string;
  description: string;
  targetGoal: string;
  suggestedActions: string[];
}

interface ManagerFeedback {
  lastReviewDate: string;
  overallRating: number;
  comments: string;
  suggestions: string[];
  nextReviewDate: string;
}

interface User {
  id: string;
  name: string;
  department: string;
  position: string;
  currentLevel: string;
}

interface CareerGoalsData {
  year: number;
  overallProgress: OverallProgress;
  categories: GoalCategory[];
  recommendations: Recommendation[];
  nextReviewDate: string;
  managerFeedback: ManagerFeedback;
}

interface GetCareerGoalsResponse {
  success: true;
  data: {
    user: User;
    careerGoals: CareerGoalsData;
  };
}

interface ErrorResponse {
  success?: false;
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
): Promise<NextResponse<UpdateCareerGoalResponse | ErrorResponse>> {
  try {
    const userId = params.user_id;

    // 認証チェック（テスト用に一時的に無効化）
    // const authHeader = request.headers.get('authorization');
    // if (!authHeader || !authHeader.startsWith('Bearer ')) {
    //   return NextResponse.json(
    //     {
    //       error: {
    //         code: 'UNAUTHORIZED',
    //         message: '認証が必要です'
    //       }
    //     },
    //     { status: 401 }
    //   );
    // }

    // ユーザーIDの存在チェック
    if (!userId || userId.trim() === '') {
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

    // リクエストボディの取得
    let requestBody: UpdateCareerGoalRequest;
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

    // 必須パラメータの検証
    if (!requestBody.year || !requestBody.operation_type || !requestBody.career_goals) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: '必須パラメータが不足しています'
          }
        },
        { status: 400 }
      );
    }

    // 年度の妥当性チェック
    const currentYear = new Date().getFullYear();
    if (requestBody.year < 2020 || requestBody.year > currentYear + 5) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_YEAR',
            message: '年度が不正です',
            details: '有効な年度を指定してください'
          }
        },
        { status: 400 }
      );
    }

    // 操作タイプの検証
    if (!['add', 'update', 'delete'].includes(requestBody.operation_type)) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_OPERATION',
            message: '操作タイプが不正です',
            details: 'add, update, delete のいずれかを指定してください'
          }
        },
        { status: 400 }
      );
    }

    // キャリア目標の検証
    for (const goal of requestBody.career_goals) {
      // 更新・削除時のgoal_id必須チェック
      if ((requestBody.operation_type === 'update' || requestBody.operation_type === 'delete') && !goal.goal_id) {
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

      // 追加・更新時の必須項目チェック
      if (requestBody.operation_type === 'add' || requestBody.operation_type === 'update') {
        if (!goal.goal_type || !goal.title || !goal.target_date || !goal.status || goal.priority === undefined) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_PARAMETER',
                message: 'パラメータが不正です',
                details: '目標タイプ、タイトル、目標達成予定日、ステータス、優先度は必須項目です'
              }
            },
            { status: 400 }
          );
        }

        // 目標タイプの検証
        if (!['short_term', 'mid_term', 'long_term'].includes(goal.goal_type)) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_GOAL_TYPE',
                message: '目標タイプが不正です'
              }
            },
            { status: 400 }
          );
        }

        // ステータスの検証
        if (!['not_started', 'in_progress', 'completed', 'postponed', 'cancelled'].includes(goal.status)) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_STATUS',
                message: 'ステータスが不正です'
              }
            },
            { status: 400 }
          );
        }

        // 優先度の検証
        if (goal.priority < 1 || goal.priority > 5) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_PRIORITY',
                message: '優先度が不正です',
                details: '優先度は1-5の範囲で指定してください'
              }
            },
            { status: 400 }
          );
        }

        // タイトルの文字数チェック
        if (goal.title && goal.title.length > 100) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_PARAMETER',
                message: 'パラメータが不正です',
                details: 'タイトルは100文字以内で入力してください'
              }
            },
            { status: 400 }
          );
        }

        // 説明の文字数チェック
        if (goal.description && goal.description.length > 1000) {
          return NextResponse.json(
            {
              error: {
                code: 'INVALID_PARAMETER',
                message: 'パラメータが不正です',
                details: '説明は1000文字以内で入力してください'
              }
            },
            { status: 400 }
          );
        }
      }
    }

    // モック実装：操作タイプに応じた処理
    const currentDateTime = new Date().toISOString();
    const updatedGoals: UpdatedGoal[] = [];

    for (const goal of requestBody.career_goals) {
      let goalId: string;
      let goalType: string;
      let title: string;
      let status: string;

      switch (requestBody.operation_type) {
        case 'add':
          // 新規目標ID生成（モック）
          goalId = `G${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
          goalType = goal.goal_type!;
          title = goal.title!;
          status = goal.status!;
          break;

        case 'update':
          // 既存目標の更新（モック）
          goalId = goal.goal_id!;
          goalType = goal.goal_type!;
          title = goal.title!;
          status = goal.status!;
          break;

        case 'delete':
          // 目標の削除（論理削除）（モック）
          goalId = goal.goal_id!;
          goalType = 'unknown'; // 削除時は既存データから取得する想定
          title = 'deleted_goal'; // 削除時は既存データから取得する想定
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
        updated_at: currentDateTime
      });
    }

    // 成功レスポンス
    const response: UpdateCareerGoalResponse = {
      user_id: userId,
      year: requestBody.year,
      updated_goals: updatedGoals,
      operation_type: requestBody.operation_type,
      operation_result: 'success',
      last_updated: currentDateTime,
      last_updated_by: userId
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('キャリア目標更新API エラー:', error);
    
    return NextResponse.json(
      {
        error: {
          code: 'SYSTEM_ERROR',
          message: 'システムエラーが発生しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * キャリア目標取得API
 * GET /api/career-goals/{user_id}
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { user_id: string } }
): Promise<NextResponse<GetCareerGoalsResponse | ErrorResponse>> {
  try {
    const userId = params.user_id;
    const { searchParams } = new URL(request.url);

    // 認証チェック（テスト用に一時的に無効化）
    // const authHeader = request.headers.get('authorization');
    // if (!authHeader || !authHeader.startsWith('Bearer ')) {
    //   return NextResponse.json(
    //     {
    //       error: {
    //         code: 'UNAUTHORIZED',
    //         message: '認証が必要です'
    //       }
    //     },
    //     { status: 401 }
    //   );
    // }

    // ユーザーIDの存在チェック
    if (!userId || userId.trim() === '') {
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

    // クエリパラメータの取得
    const includeProgress = searchParams.get('includeProgress') !== 'false';
    const includeHistory = searchParams.get('includeHistory') === 'true';
    const yearParam = searchParams.get('year');
    const statusParam = searchParams.get('status');

    // 年度の設定（デフォルト：現在年度）
    const currentYear = new Date().getFullYear();
    let targetYear = currentYear;
    
    if (yearParam) {
      const parsedYear = parseInt(yearParam, 10);
      if (isNaN(parsedYear) || parsedYear < 2020 || parsedYear > currentYear + 5) {
        return NextResponse.json(
          {
            error: {
              code: 'INVALID_YEAR',
              message: '無効な年度指定',
              details: '有効な年度を指定してください'
            }
          },
          { status: 400 }
        );
      }
      targetYear = parsedYear;
    }

    // ステータスフィルタの検証
    if (statusParam && !['active', 'completed', 'all'].includes(statusParam)) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_STATUS',
            message: '無効なステータス指定',
            details: 'active, completed, all のいずれかを指定してください'
          }
        },
        { status: 400 }
      );
    }

    // モックデータの生成
    const currentDateTime = new Date().toISOString();
    
    const mockUser: User = {
      id: userId,
      name: '田中太郎',
      department: 'エンジニアリング部',
      position: 'シニアエンジニア',
      currentLevel: 'L3'
    };

    const mockCareerGoals: CareerGoalsData = {
      year: targetYear,
      overallProgress: {
        completionRate: 0.65,
        totalGoals: 8,
        completedGoals: 3,
        inProgressGoals: 4,
        notStartedGoals: 1,
        lastUpdated: currentDateTime
      },
      categories: [
        {
          id: 'technical_skills',
          name: '技術スキル',
          description: '技術的な能力向上',
          weight: 0.4,
          progress: 0.7,
          goals: [
            {
              id: 'goal_001',
              title: 'React.js マスター',
              description: 'React.jsの上級レベルまでスキルアップし、チームのテックリードとして活動する',
              category: 'technical_skills',
              priority: 'high',
              status: 'in_progress',
              targetLevel: 'advanced',
              currentLevel: 'intermediate',
              progress: {
                percentage: 0.75,
                milestones: [
                  {
                    id: 'milestone_001',
                    title: '基礎学習完了',
                    description: 'React基礎コースの受講完了',
                    status: 'completed',
                    completedAt: '2025-02-15T09:00:00Z',
                    weight: 0.2
                  },
                  {
                    id: 'milestone_002',
                    title: '実践プロジェクト参加',
                    description: 'Reactを使用した実際のプロジェクトに参加',
                    status: 'completed',
                    completedAt: '2025-04-20T15:30:00Z',
                    weight: 0.3
                  },
                  {
                    id: 'milestone_003',
                    title: '上級機能習得',
                    description: 'Context API、Hooks、パフォーマンス最適化の習得',
                    status: 'in_progress',
                    targetDate: '2025-07-31',
                    weight: 0.3
                  },
                  {
                    id: 'milestone_004',
                    title: 'チーム指導',
                    description: 'チームメンバーへのReact指導・メンタリング',
                    status: 'not_started',
                    targetDate: '2025-09-30',
                    weight: 0.2
                  }
                ]
              },
              targetDate: '2025-09-30',
              createdAt: '2025-01-10T09:00:00Z',
              updatedAt: currentDateTime,
              metrics: {
                skillAssessmentScore: 3.2,
                targetScore: 4.0,
                projectsCompleted: 2,
                targetProjects: 3,
                mentoringSessions: 0,
                targetSessions: 5
              }
            },
            {
              id: 'goal_002',
              title: 'AWS認定取得',
              description: 'AWS Solutions Architect Associate認定を取得する',
              category: 'technical_skills',
              priority: 'medium',
              status: 'in_progress',
              progress: {
                percentage: 0.4,
                milestones: [
                  {
                    id: 'milestone_005',
                    title: '学習計画策定',
                    status: 'completed',
                    completedAt: '2025-03-01T09:00:00Z',
                    description: '',
                    weight: 0.2
                  },
                  {
                    id: 'milestone_006',
                    title: '模擬試験合格',
                    status: 'in_progress',
                    targetDate: '2025-07-15',
                    description: '',
                    weight: 0.4
                  },
                  {
                    id: 'milestone_007',
                    title: '本試験受験',
                    status: 'not_started',
                    targetDate: '2025-08-31',
                    description: '',
                    weight: 0.4
                  }
                ]
              },
              targetDate: '2025-08-31',
              createdAt: '2025-02-01T09:00:00Z',
              updatedAt: currentDateTime,
              metrics: {
                studyHours: 45,
                targetHours: 120,
                practiceTestScore: 65,
                targetScore: 80
              }
            }
          ]
        },
        {
          id: 'leadership',
          name: 'リーダーシップ',
          description: 'チームリーダーとしての能力向上',
          weight: 0.3,
          progress: 0.5,
          goals: [
            {
              id: 'goal_003',
              title: 'プロジェクトリーダー経験',
              description: '中規模プロジェクトのリーダーとして成功を収める',
              category: 'leadership',
              priority: 'high',
              status: 'in_progress',
              progress: {
                percentage: 0.6,
                milestones: [
                  {
                    id: 'milestone_008',
                    title: 'リーダーシップ研修受講',
                    status: 'completed',
                    completedAt: '2025-03-15T14:00:00Z',
                    description: '',
                    weight: 0.2
                  },
                  {
                    id: 'milestone_009',
                    title: 'プロジェクト開始',
                    status: 'completed',
                    completedAt: '2025-04-01T09:00:00Z',
                    description: '',
                    weight: 0.3
                  },
                  {
                    id: 'milestone_010',
                    title: '中間評価',
                    status: 'in_progress',
                    targetDate: '2025-06-30',
                    description: '',
                    weight: 0.3
                  },
                  {
                    id: 'milestone_011',
                    title: 'プロジェクト完了',
                    status: 'not_started',
                    targetDate: '2025-09-30',
                    description: '',
                    weight: 0.2
                  }
                ]
              },
              targetDate: '2025-09-30',
              createdAt: '2025-03-01T09:00:00Z',
              updatedAt: currentDateTime,
              metrics: {
                teamSize: 5,
                projectProgress: 0.6,
                teamSatisfaction: 4.2,
                targetSatisfaction: 4.0
              }
            }
          ]
        },
        {
          id: 'business_skills',
          name: 'ビジネススキル',
          description: 'ビジネス理解と提案力の向上',
          weight: 0.2,
          progress: 0.3,
          goals: [
            {
              id: 'goal_004',
              title: 'ビジネス分析スキル習得',
              description: '要件定義とビジネス分析の基礎スキルを習得する',
              category: 'business_skills',
              priority: 'medium',
              status: 'not_started',
              progress: {
                percentage: 0.0,
                milestones: [
                  {
                    id: 'milestone_012',
                    title: 'BA研修受講',
                    status: 'not_started',
                    targetDate: '2025-07-01',
                    description: '',
                    weight: 0.5
                  },
                  {
                    id: 'milestone_013',
                    title: '実践演習',
                    status: 'not_started',
                    targetDate: '2025-08-31',
                    description: '',
                    weight: 0.5
                  }
                ]
              },
              targetDate: '2025-10-31',
              createdAt: '2025-01-15T09:00:00Z',
              updatedAt: currentDateTime
            }
          ]
        },
        {
          id: 'personal_development',
          name: '自己啓発',
          description: '個人的な成長と学習',
          weight: 0.1,
          progress: 0.8,
          goals: [
            {
              id: 'goal_005',
              title: '英語力向上',
              description: 'TOEIC 800点以上を達成する',
              category: 'personal_development',
              priority: 'low',
              status: 'completed',
              progress: {
                percentage: 1.0,
                completedAt: '2025-04-15T10:00:00Z'
              },
              targetDate: '2025-06-30',
              createdAt: '2025-01-05T09:00:00Z',
              updatedAt: '2025-04-15T10:00:00Z',
              metrics: {
                currentScore: 820,
                targetScore: 800,
                improvementFromStart: 120
              }
            }
          ]
        }
      ],
      recommendations: [
        {
          type: 'skill_gap',
          priority: 'high',
          title: 'React.js学習加速',
          description: '目標達成のため、週末の学習時間を増やすことを推奨',
          targetGoal: 'goal_001',
          suggestedActions: [
            '週末の学習時間を2時間増加',
            'オンライン勉強会への参加',
            '実践プロジェクトでのアウトプット強化'
          ]
        },
        {
          type: 'timeline_adjustment',
          priority: 'medium',
          title: 'AWS認定スケジュール見直し',
          description: '現在の進捗では目標達成が困難。スケジュール調整を検討',
          targetGoal: 'goal_002',
          suggestedActions: [
            '目標日を1ヶ月延期',
            '学習時間の確保（週5時間→8時間）',
            'メンターのサポート依頼'
          ]
        }
      ],
      nextReviewDate: '2025-06-30',
      managerFeedback: {
        lastReviewDate: '2025-05-15T14:00:00Z',
        overallRating: 4.2,
        comments: '技術スキルの向上が顕著。リーダーシップ面でも成長が見られる。',
        suggestions: [
          'プロジェクトマネジメントスキルの強化',
          '後輩指導の機会を増やす'
        ],
        nextReviewDate: '2025-06-30T14:00:00Z'
      }
    };

    // ステータスフィルタの適用
    if (statusParam && statusParam !== 'all') {
      mockCareerGoals.categories = mockCareerGoals.categories.map(category => ({
        ...category,
        goals: category.goals.filter(goal => {
          if (statusParam === 'active') {
            return goal.status === 'in_progress' || goal.status === 'not_started';
          } else if (statusParam === 'completed') {
            return goal.status === 'completed';
          }
          return true;
        })
      })).filter(category => category.goals.length > 0);
    }

    // 進捗情報を含めない場合の処理
    if (!includeProgress) {
      mockCareerGoals.categories = mockCareerGoals.categories.map(category => ({
        ...category,
        goals: category.goals.map(goal => {
          const { metrics, ...goalWithoutMetrics } = goal;
          return {
            ...goalWithoutMetrics,
            progress: { percentage: goal.progress.percentage }
          };
        })
      }));
    }

    const response: GetCareerGoalsResponse = {
      success: true,
      data: {
        user: mockUser,
        careerGoals: mockCareerGoals
      }
    };

    return NextResponse.json(response, { status: 200 });

  } catch (error) {
    console.error('キャリア目標取得API エラー:', error);
    
    return NextResponse.json(
      {
        error: {
          code: 'SYSTEM_ERROR',
          message: 'システムエラーが発生しました',
          details: error instanceof Error ? error.message : '不明なエラー'
        }
      },
      { status: 500 }
    );
  }
}

/**
 * キャリア目標追加API
 * POST /api/career-goals/{user_id}
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { user_id: string } }
): Promise<NextResponse<UpdateCareerGoalResponse | ErrorResponse>> {
  try {
    const userId = params.user_id;

    // 認証チェック（テスト用に一時的に無効化）
    // const authHeader = request.headers.get('authorization');
    // if (!authHeader || !authHeader.startsWith('Bearer ')) {
    //   return NextResponse.json(
    //     {
    //       error: {
    //         code: 'UNAUTHORIZED',
    //         message: '認証が必要です'
    //       }
    //     },
    //     { status: 401 }
    //   );
    // }

    // ユーザーIDの存在チェック
    if (!userId || userId.trim() === '') {
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

    // リクエストボディの取得
    let requestBody: any;
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

    // 必須パラメータの検証
    if (!requestBody.title || !requestBody.target_date || !requestBody.status) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: 'タイトル、目標達成予定日、ステータスは必須項目です'
          }
        },
        { status: 400 }
      );
    }

    // 年度の設定（デフォルト：現在年度）
    const currentYear = new Date().getFullYear();
    const targetYear = requestBody.year || currentYear;

    // 年度の妥当性チェック
    if (targetYear < 2020 || targetYear > currentYear + 5) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_YEAR',
            message: '年度が不正です',
            details: '有効な年度を指定してください'
          }
        },
        { status: 400 }
      );
    }

    // ステータスの検証
    if (!['not_started', 'in_progress', 'completed', 'postponed', 'cancelled'].includes(requestBody.status)) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_STATUS',
            message: 'ステータスが不正です'
          }
        },
        { status: 400 }
      );
    }

    // 優先度の検証（デフォルト値設定）
    const priority = requestBody.priority || 3;
    if (priority < 1 || priority > 5) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PRIORITY',
            message: '優先度が不正です',
            details: '優先度は1-5の範囲で指定してください'
          }
        },
        { status: 400 }
      );
    }

    // タイトルの文字数チェック
    if (requestBody.title.length > 100) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: 'タイトルは100文字以内で入力してください'
          }
        },
        { status: 400 }
      );
    }

    // 説明の文字数チェック
    if (requestBody.description && requestBody.description.length > 1000) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_PARAMETER',
            message: 'パラメータが不正です',
            details: '説明は1000文字以内で入力してください'
          }
        },
        { status: 400 }
      );
    }

    // 目標タイプの設定（デフォルト値）
    const goalType = requestBody.goal_type || 'short_term';
    if (!['short_term', 'mid_term', 'long_term'].includes(goalType)) {
      return NextResponse.json(
        {
          error: {
            code: 'INVALID_GOAL_TYPE',
            message: '目標タイプが不正です'
          }
        },
        { status: 400 }
      );
    }

    // モック実装：新規目標の作成
    const currentDateTime = new Date().toISOString();
    const goalId = `G${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;

    const updatedGoal: UpdatedGoal = {
      goal_id: goalId,
      goal_type: goalType,
      title: requestBody.title,
      status: requestBody.status,
      updated_at: currentDateTime
    };

    // 成功レスポンス
    const response: UpdateCareerGoalResponse = {
      user_id: userId,
      year: targetYear,
      updated_goals: [updatedGoal],
      operation_type: 'add',
      operation_result: 'success',
      last_updated: currentDateTime,
      last_updated_by: userId
    };

    return NextResponse.json(response, { status: 201 });

  } catch (error) {
    console.error('キャリア目標追加API エラー:', error);
    
    return NextResponse.json(
      {
        error: {
          code: 'SYSTEM_ERROR',
          message: 'システムエラーが発生しました',
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
      'Access-Control-Allow-Methods': 'GET, POST, PUT, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    },
  });
}
