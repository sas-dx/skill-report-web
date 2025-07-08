/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: 
 *   - docs/design/api/specs/API定義書_API-031_キャリア目標取得API.md
 *   - docs/design/api/specs/API定義書_API-032_キャリア目標更新API.md
 * 実装内容: キャリア目標API（取得・作成・更新）
 */

import { NextRequest, NextResponse } from 'next/server'
import { 
  getCareerGoals, 
  createCareerGoal, 
  updateCareerGoal, 
  deleteCareerGoal,
  getCareerGoalStats,
  CreateCareerGoalData,
  UpdateCareerGoalData,
  CareerGoalDB
} from '@/lib/services/careerGoalService'
import { Prisma } from '@prisma/client'

// API型定義
interface CareerGoalResponse {
  id: string
  goal_id: string
  title: string
  description?: string | undefined
  goal_type: string
  goal_category?: string | undefined
  priority: number
  target_date: string
  status: string
  progress_rate: number
  achievement_rate: number
  related_skills?: any[] | undefined
  action_plans?: any[] | undefined
  created_at: string
  updated_at: string
}

interface CareerGoalStatsResponse {
  totalGoals: number
  completedGoals: number
  inProgressGoals: number
  notStartedGoals: number
  completionRate: number
}

// データベース型からAPI型への変換
function convertToApiFormat(dbGoal: CareerGoalDB): CareerGoalResponse {
  // 優先度レベルの変換（high/medium/low → 1-5）
  let priority: number
  switch (dbGoal.priority_level) {
    case 'high':
      priority = 5
      break
    case 'medium':
      priority = 3
      break
    case 'low':
      priority = 1
      break
    default:
      priority = 3
  }

  // JSON文字列をオブジェクトに変換
  let relatedSkills: any[] = []
  let actionPlans: any[] = []

  try {
    if (dbGoal.related_skill_items) {
      relatedSkills = JSON.parse(dbGoal.related_skill_items)
    }
  } catch (error) {
    console.warn('関連スキル情報のパースに失敗:', error)
  }

  try {
    if (dbGoal.milestones) {
      actionPlans = JSON.parse(dbGoal.milestones)
    }
  } catch (error) {
    console.warn('アクションプラン情報のパースに失敗:', error)
  }

  return {
    id: dbGoal.id,
    goal_id: dbGoal.goal_id || '',
    title: dbGoal.goal_title || '',
    description: dbGoal.goal_description || undefined,
    goal_type: dbGoal.goal_type || 'short_term',
    goal_category: dbGoal.goal_category || undefined,
    priority: priority,
    target_date: dbGoal.target_date?.toISOString() || '',
    status: dbGoal.achievement_status || 'not_started',
    progress_rate: dbGoal.progress_rate ? Number(dbGoal.progress_rate) : 0,
    achievement_rate: dbGoal.achievement_rate ? Number(dbGoal.achievement_rate) : 0,
    related_skills: relatedSkills.length > 0 ? relatedSkills : undefined,
    action_plans: actionPlans.length > 0 ? actionPlans : undefined,
    created_at: dbGoal.created_at.toISOString(),
    updated_at: dbGoal.updated_at.toISOString()
  }
}

/**
 * キャリア目標取得API
 * GET /api/career-goals/{user_id}
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { user_id: string } }
) {
  try {
    const { user_id } = params
    const { searchParams } = new URL(request.url)
    const year = searchParams.get('year')
    const status = searchParams.get('status')

    // パラメータバリデーション
    if (!user_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PARAMETER',
          message: 'ユーザーIDが必要です'
        }
      }, { status: 400 })
    }

    // 年度の設定
    let targetYear: number | undefined
    if (year) {
      const parsedYear = parseInt(year, 10)
      if (isNaN(parsedYear) || parsedYear < 2020 || parsedYear > new Date().getFullYear() + 5) {
        return NextResponse.json({
          success: false,
          error: {
            code: 'INVALID_YEAR',
            message: '無効な年度指定です'
          }
        }, { status: 400 })
      }
      targetYear = parsedYear
    }

    // ステータスフィルタの検証
    let statusFilter: 'active' | 'completed' | 'all' | undefined
    if (status) {
      if (!['active', 'completed', 'all'].includes(status)) {
        return NextResponse.json({
          success: false,
          error: {
            code: 'INVALID_STATUS',
            message: '無効なステータス指定です'
          }
        }, { status: 400 })
      }
      statusFilter = status as 'active' | 'completed' | 'all'
    }

    // キャリア目標を取得
    const goals = await getCareerGoals(user_id, targetYear, statusFilter)
    
    // 統計情報を取得
    const stats = await getCareerGoalStats(user_id, targetYear)

    // API形式に変換
    const apiGoals = goals.map(convertToApiFormat)

    return NextResponse.json({
      success: true,
      data: {
        goals: apiGoals,
        stats: stats
      },
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('キャリア目標取得エラー:', error)
    
    if (error && typeof error === 'object' && 'code' in error) {
      return NextResponse.json({
        success: false,
        error: error
      }, { status: 400 })
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'サーバーエラーが発生しました'
      }
    }, { status: 500 })
  }
}

/**
 * キャリア目標作成API
 * POST /api/career-goals/{user_id}
 */
export async function POST(
  request: NextRequest,
  { params }: { params: { user_id: string } }
) {
  try {
    const { user_id } = params
    const body = await request.json()

    // パラメータバリデーション
    if (!user_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PARAMETER',
          message: 'ユーザーIDが必要です'
        }
      }, { status: 400 })
    }

    // 必須項目のバリデーション
    if (!body.title || !body.goal_type || !body.target_date) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '必須項目が不足しています',
          details: [
            { field: 'title', message: 'タイトルは必須です' },
            { field: 'goal_type', message: '目標タイプは必須です' },
            { field: 'target_date', message: '目標日は必須です' }
          ]
        }
      }, { status: 400 })
    }

    // 目標タイプの検証
    if (!['short_term', 'mid_term', 'long_term'].includes(body.goal_type)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_GOAL_TYPE',
          message: '無効な目標タイプです'
        }
      }, { status: 400 })
    }

    // ステータスの検証
    const status = body.status || 'not_started'
    if (!['not_started', 'in_progress', 'completed', 'postponed', 'cancelled'].includes(status)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_STATUS',
          message: '無効なステータスです'
        }
      }, { status: 400 })
    }

    // 優先度の検証
    const priority = body.priority || 3
    if (priority < 1 || priority > 5) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PRIORITY',
          message: '優先度は1-5の範囲で指定してください'
        }
      }, { status: 400 })
    }

    // 作成データの準備
    const createData: CreateCareerGoalData = {
      title: body.title,
      description: body.description,
      goal_type: body.goal_type,
      goal_category: body.goal_category,
      priority: priority,
      target_date: body.target_date,
      status: status,
      related_skills: body.related_skills,
      action_plans: body.action_plans
    }

    // キャリア目標を作成
    const newGoal = await createCareerGoal(user_id, createData)

    // API形式に変換
    const apiGoal = convertToApiFormat(newGoal)

    return NextResponse.json({
      success: true,
      data: {
        goal: apiGoal
      },
      timestamp: new Date().toISOString()
    }, { status: 201 })

  } catch (error) {
    console.error('キャリア目標作成エラー:', error)
    
    if (error && typeof error === 'object' && 'code' in error) {
      return NextResponse.json({
        success: false,
        error: error
      }, { status: 400 })
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'サーバーエラーが発生しました'
      }
    }, { status: 500 })
  }
}

/**
 * キャリア目標更新API
 * PUT /api/career-goals/{user_id}
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { user_id: string } }
) {
  try {
    const { user_id } = params
    const body = await request.json()

    // パラメータバリデーション
    if (!user_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PARAMETER',
          message: 'ユーザーIDが必要です'
        }
      }, { status: 400 })
    }

    if (!body.goal_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PARAMETER',
          message: '目標IDが必要です'
        }
      }, { status: 400 })
    }

    // 目標タイプの検証（指定されている場合）
    if (body.goal_type && !['short_term', 'mid_term', 'long_term'].includes(body.goal_type)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_GOAL_TYPE',
          message: '無効な目標タイプです'
        }
      }, { status: 400 })
    }

    // ステータスの検証（指定されている場合）
    if (body.status && !['not_started', 'in_progress', 'completed', 'postponed', 'cancelled'].includes(body.status)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_STATUS',
          message: '無効なステータスです'
        }
      }, { status: 400 })
    }

    // 優先度の検証（指定されている場合）
    if (body.priority !== undefined && (body.priority < 1 || body.priority > 5)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PRIORITY',
          message: '優先度は1-5の範囲で指定してください'
        }
      }, { status: 400 })
    }

    // 更新データの準備
    const updateData: UpdateCareerGoalData = {
      goal_id: body.goal_id,
      title: body.title,
      description: body.description,
      goal_type: body.goal_type,
      goal_category: body.goal_category,
      priority: body.priority,
      target_date: body.target_date,
      status: body.status,
      progress_rate: body.progress_rate,
      achievement_rate: body.achievement_rate,
      self_evaluation: body.self_evaluation,
      evaluation_comments: body.evaluation_comments,
      milestones: body.milestones,
      obstacles: body.obstacles,
      support_needed: body.support_needed
    }

    // キャリア目標を更新
    const updatedGoal = await updateCareerGoal(user_id, updateData)

    // API形式に変換
    const apiGoal = convertToApiFormat(updatedGoal)

    return NextResponse.json({
      success: true,
      data: {
        goal: apiGoal
      },
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('キャリア目標更新エラー:', error)
    
    if (error && typeof error === 'object' && 'message' in error) {
      if (error.message === 'GOAL_NOT_FOUND') {
        return NextResponse.json({
          success: false,
          error: {
            code: 'GOAL_NOT_FOUND',
            message: '指定された目標が見つかりません'
          }
        }, { status: 404 })
      }
    }

    if (error && typeof error === 'object' && 'code' in error) {
      return NextResponse.json({
        success: false,
        error: error
      }, { status: 400 })
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'サーバーエラーが発生しました'
      }
    }, { status: 500 })
  }
}

/**
 * キャリア目標削除API
 * DELETE /api/career-goals/{user_id}
 */
export async function DELETE(
  request: NextRequest,
  { params }: { params: { user_id: string } }
) {
  try {
    const { user_id } = params
    const { searchParams } = new URL(request.url)
    const goalId = searchParams.get('goal_id')

    // パラメータバリデーション
    if (!user_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PARAMETER',
          message: 'ユーザーIDが必要です'
        }
      }, { status: 400 })
    }

    if (!goalId) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'INVALID_PARAMETER',
          message: '目標IDが必要です'
        }
      }, { status: 400 })
    }

    // キャリア目標を削除
    const result = await deleteCareerGoal(user_id, goalId)

    if (!result) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'GOAL_NOT_FOUND',
          message: '指定された目標が見つかりません'
        }
      }, { status: 404 })
    }

    return NextResponse.json({
      success: true,
      data: {
        message: '目標が正常に削除されました',
        goal_id: goalId
      },
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('キャリア目標削除エラー:', error)
    
    if (error && typeof error === 'object' && 'message' in error) {
      if (error.message === 'GOAL_NOT_FOUND') {
        return NextResponse.json({
          success: false,
          error: {
            code: 'GOAL_NOT_FOUND',
            message: '指定された目標が見つかりません'
          }
        }, { status: 404 })
      }
    }

    if (error && typeof error === 'object' && 'code' in error) {
      return NextResponse.json({
        success: false,
        error: error
      }, { status: 400 })
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'サーバーエラーが発生しました'
      }
    }, { status: 500 })
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
  })
}
