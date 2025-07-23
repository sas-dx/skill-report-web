/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: 
 *   - docs/design/api/specs/API定義書_API-033_目標進捗取得API.md
 *   - docs/design/api/specs/API定義書_API-034_目標進捗更新API.md
 * 実装内容: 目標進捗管理API
 */

import { NextRequest, NextResponse } from 'next/server'
import { getGoalProgress, updateGoalProgress } from '@/lib/services/goalProgressService'
import { createAuditLog } from '@/lib/auditLogger'

/**
 * API-033: 目標進捗取得API
 * GET /api/career-progress/[user_id]
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { user_id: string } }
) {
  try {
    const { user_id } = params
    const { searchParams } = new URL(request.url)
    
    // クエリパラメータを取得
    const year = searchParams.get('year') ? parseInt(searchParams.get('year')!) : undefined
    const goalId = searchParams.get('goal_id') || undefined
    const includeCompleted = searchParams.get('include_completed') !== 'false'
    const includeDetails = searchParams.get('include_details') === 'true'

    // 入力値検証
    if (!user_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'ユーザーIDは必須です',
          details: [{ field: 'user_id', message: 'ユーザーIDが指定されていません' }]
        }
      }, { status: 400 })
    }

    if (year && (year < 2020 || year > 2030)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '年度は2020年から2030年の範囲で指定してください',
          details: [{ field: 'year', message: '無効な年度が指定されています' }]
        }
      }, { status: 400 })
    }

    // 目標進捗情報を取得
    const progressData = await getGoalProgress(
      user_id,
      year,
      goalId,
      includeCompleted,
      includeDetails
    )

    // 監査ログを記録（READ操作は監査対象外のため、コメントアウト）
    // await createAuditLog({
    //   userId: user_id,
    //   actionType: 'READ',
    //   targetTable: 'TRN_CareerPlan',
    //   targetId: goalId || 'all',
    //   newValues: {
    //     year: year || new Date().getFullYear(),
    //     include_completed: includeCompleted,
    //     include_details: includeDetails
    //   }
    // })

    return NextResponse.json({
      success: true,
      data: progressData,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('目標進捗取得API エラー:', error)

    if (error instanceof Error) {
      switch (error.message) {
        case 'GOAL_PROGRESS_FETCH_ERROR':
          return NextResponse.json({
            success: false,
            error: {
              code: 'GOAL_PROGRESS_FETCH_ERROR',
              message: '目標進捗情報の取得に失敗しました'
            }
          }, { status: 500 })

        case 'USER_NOT_FOUND':
          return NextResponse.json({
            success: false,
            error: {
              code: 'USER_NOT_FOUND',
              message: '指定されたユーザーが見つかりません'
            }
          }, { status: 404 })

        default:
          return NextResponse.json({
            success: false,
            error: {
              code: 'INTERNAL_SERVER_ERROR',
              message: 'システムエラーが発生しました'
            }
          }, { status: 500 })
      }
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 })
  }
}

/**
 * API-034: 目標進捗更新API
 * PUT /api/career-progress/[user_id]
 */
export async function PUT(
  request: NextRequest,
  { params }: { params: { user_id: string } }
) {
  try {
    const { user_id } = params
    const body = await request.json()

    // 入力値検証
    if (!user_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: 'ユーザーIDは必須です',
          details: [{ field: 'user_id', message: 'ユーザーIDが指定されていません' }]
        }
      }, { status: 400 })
    }

    if (!body.goal_id) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '目標IDは必須です',
          details: [{ field: 'goal_id', message: '目標IDが指定されていません' }]
        }
      }, { status: 400 })
    }

    if (!body.update_type) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '更新タイプは必須です',
          details: [{ field: 'update_type', message: '更新タイプが指定されていません' }]
        }
      }, { status: 400 })
    }

    const validUpdateTypes = ['status', 'action_plan', 'milestone', 'skill_level', 'feedback']
    if (!validUpdateTypes.includes(body.update_type)) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '無効な更新タイプです',
          details: [{ 
            field: 'update_type', 
            message: `更新タイプは次のいずれかを指定してください: ${validUpdateTypes.join(', ')}` 
          }]
        }
      }, { status: 400 })
    }

    if (!body.update_data) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: '更新データは必須です',
          details: [{ field: 'update_data', message: '更新データが指定されていません' }]
        }
      }, { status: 400 })
    }

    // 更新タイプ別の詳細検証
    const validationError = validateUpdateData(body.update_type, body.update_data)
    if (validationError) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
          message: validationError.message,
          details: validationError.details
        }
      }, { status: 400 })
    }

    // 更新者情報を取得（実際の実装では認証情報から取得）
    const updatedBy = request.headers.get('x-user-id') || user_id

    // 目標進捗を更新
    const updateResult = await updateGoalProgress(
      user_id,
      {
        goal_id: body.goal_id,
        update_type: body.update_type,
        update_data: body.update_data,
        comment: body.comment
      },
      updatedBy
    )

    return NextResponse.json({
      success: true,
      data: updateResult,
      timestamp: new Date().toISOString()
    })

  } catch (error) {
    console.error('目標進捗更新API エラー:', error)

    if (error instanceof Error) {
      switch (error.message) {
        case 'GOAL_NOT_FOUND':
          return NextResponse.json({
            success: false,
            error: {
              code: 'GOAL_NOT_FOUND',
              message: '指定された目標が見つかりません'
            }
          }, { status: 404 })

        case 'INVALID_UPDATE_TYPE':
          return NextResponse.json({
            success: false,
            error: {
              code: 'INVALID_UPDATE_TYPE',
              message: '無効な更新タイプです'
            }
          }, { status: 400 })

        case 'ACTION_PLAN_NOT_FOUND':
          return NextResponse.json({
            success: false,
            error: {
              code: 'ACTION_PLAN_NOT_FOUND',
              message: '指定された行動計画が見つかりません'
            }
          }, { status: 404 })

        case 'MILESTONE_NOT_FOUND':
          return NextResponse.json({
            success: false,
            error: {
              code: 'MILESTONE_NOT_FOUND',
              message: '指定されたマイルストーンが見つかりません'
            }
          }, { status: 404 })

        case 'SKILL_NOT_FOUND':
          return NextResponse.json({
            success: false,
            error: {
              code: 'SKILL_NOT_FOUND',
              message: '指定されたスキルが見つかりません'
            }
          }, { status: 404 })

        case 'STATUS_UPDATE_ERROR':
        case 'ACTION_PLAN_UPDATE_ERROR':
        case 'MILESTONE_UPDATE_ERROR':
        case 'SKILL_LEVEL_UPDATE_ERROR':
        case 'FEEDBACK_ADD_ERROR':
          return NextResponse.json({
            success: false,
            error: {
              code: error.message,
              message: '更新処理に失敗しました'
            }
          }, { status: 500 })

        default:
          return NextResponse.json({
            success: false,
            error: {
              code: 'INTERNAL_SERVER_ERROR',
              message: 'システムエラーが発生しました'
            }
          }, { status: 500 })
      }
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 })
  }
}

/**
 * 更新データの詳細検証
 */
function validateUpdateData(updateType: string, updateData: any): { message: string; details: any[] } | null {
  switch (updateType) {
    case 'status':
      if (!updateData.status) {
        return {
          message: 'ステータスは必須です',
          details: [{ field: 'status', message: 'ステータスが指定されていません' }]
        }
      }
      const validStatuses = ['not_started', 'in_progress', 'completed', 'postponed', 'cancelled']
      if (!validStatuses.includes(updateData.status)) {
        return {
          message: '無効なステータスです',
          details: [{ 
            field: 'status', 
            message: `ステータスは次のいずれかを指定してください: ${validStatuses.join(', ')}` 
          }]
        }
      }
      break

    case 'action_plan':
      if (!updateData.action_id) {
        return {
          message: '行動計画IDは必須です',
          details: [{ field: 'action_id', message: '行動計画IDが指定されていません' }]
        }
      }
      if (!updateData.status) {
        return {
          message: 'ステータスは必須です',
          details: [{ field: 'status', message: 'ステータスが指定されていません' }]
        }
      }
      break

    case 'milestone':
      if (!updateData.milestone_id) {
        return {
          message: 'マイルストーンIDは必須です',
          details: [{ field: 'milestone_id', message: 'マイルストーンIDが指定されていません' }]
        }
      }
      if (!updateData.status) {
        return {
          message: 'ステータスは必須です',
          details: [{ field: 'status', message: 'ステータスが指定されていません' }]
        }
      }
      break

    case 'skill_level':
      if (!updateData.skill_id) {
        return {
          message: 'スキルIDは必須です',
          details: [{ field: 'skill_id', message: 'スキルIDが指定されていません' }]
        }
      }
      if (typeof updateData.current_level !== 'number' || updateData.current_level < 1 || updateData.current_level > 4) {
        return {
          message: 'スキルレベルは1から4の範囲で指定してください',
          details: [{ field: 'current_level', message: '無効なスキルレベルです' }]
        }
      }
      break

    case 'feedback':
      if (!updateData.feedback_text || updateData.feedback_text.trim() === '') {
        return {
          message: 'フィードバック内容は必須です',
          details: [{ field: 'feedback_text', message: 'フィードバック内容が指定されていません' }]
        }
      }
      if (updateData.feedback_text.length > 1000) {
        return {
          message: 'フィードバック内容は1000文字以内で入力してください',
          details: [{ field: 'feedback_text', message: 'フィードバック内容が長すぎます' }]
        }
      }
      break
  }

  return null
}
