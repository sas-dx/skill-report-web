/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: 
 *   - docs/design/api/specs/API定義書_API-033_目標進捗取得API.md
 *   - docs/design/api/specs/API定義書_API-034_目標進捗更新API.md
 * 実装内容: 目標進捗管理API
 */

import { NextRequest, NextResponse } from 'next/server'
import { prisma } from '@/lib/prisma'
import { 
  createSuccessResponse, 
  createErrorResponse,
  createAuthErrorResponse,
  createValidationErrorResponse 
} from '@/lib/api-utils'
import { verifyAuth } from '@/lib/auth'
import { Prisma } from '@prisma/client'

/**
 * API-033: 目標進捗取得API
 * GET /api/career-progress/[user_id]
 */
export async function GET(
  request: NextRequest,
  { params }: { params: { user_id: string } }
) {
  try {
    // 認証チェック
    const authResult = await verifyAuth(request)
    if (!authResult.success) {
      return createAuthErrorResponse()
    }

    const { user_id } = params
    const { searchParams } = new URL(request.url)
    const goalId = searchParams.get('goal_id')
    const year = searchParams.get('year')

    // 基本的な検索条件
    const whereCondition: any = {
      employee_id: user_id,
      is_deleted: false
    }

    // 特定の目標IDが指定された場合
    if (goalId) {
      whereCondition.OR = [
        { goal_id: goalId },
        { id: goalId }
      ]
    }

    // 年度フィルタ
    if (year) {
      const yearNum = parseInt(year)
      const startDate = new Date(`${yearNum}-01-01`)
      const endDate = new Date(`${yearNum + 1}-01-01`)
      whereCondition.start_date = {
        gte: startDate,
        lt: endDate
      }
    }

    // 進捗データを取得
    const progressData = await prisma.goalProgress.findMany({
      where: whereCondition,
      orderBy: [
        { priority_level: 'desc' },
        { created_at: 'desc' }
      ]
    })

    // レスポンスデータの整形
    const formattedProgress = progressData.map(progress => ({
      id: progress.id,
      goal_id: progress.goal_id,
      title: progress.goal_title,
      description: progress.goal_description,
      goal_type: progress.goal_type,
      category: progress.goal_category,
      priority: progress.priority_level === 'high' ? 5 : 
                progress.priority_level === 'medium' ? 3 : 1,
      target_date: progress.target_date?.toISOString(),
      start_date: progress.start_date?.toISOString(),
      status: progress.achievement_status,
      progress_rate: progress.progress_rate ? Number(progress.progress_rate) : 0,
      achievement_rate: progress.achievement_rate ? Number(progress.achievement_rate) : 0,
      completion_date: progress.completion_date?.toISOString(),
      self_evaluation: progress.self_evaluation,
      evaluation_comments: progress.evaluation_comments,
      milestones: progress.milestones ? JSON.parse(progress.milestones as string) : [],
      obstacles: progress.obstacles,
      support_needed: progress.support_needed,
      created_at: progress.created_at.toISOString(),
      updated_at: progress.updated_at.toISOString()
    }))

    // 全体の進捗サマリーを計算
    const summary = {
      total_goals: formattedProgress.length,
      completed: formattedProgress.filter(p => p.status === 'completed').length,
      in_progress: formattedProgress.filter(p => p.status === 'in_progress').length,
      not_started: formattedProgress.filter(p => p.status === 'not_started').length,
      average_progress: formattedProgress.length > 0 
        ? Math.round(formattedProgress.reduce((sum, p) => sum + p.progress_rate, 0) / formattedProgress.length)
        : 0
    }

    return createSuccessResponse({
      progress: formattedProgress,
      summary
    })

  } catch (error) {
    console.error('目標進捗取得エラー:', error)
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    )
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
    // 認証チェック
    const authResult = await verifyAuth(request)
    if (!authResult.success) {
      return createAuthErrorResponse()
    }

    const { user_id } = params
    const body = await request.json()

    // 必須パラメータチェック
    if (!body.goal_id) {
      return createValidationErrorResponse([
        { field: 'goal_id', message: '目標IDは必須です' }
      ])
    }

    // 既存の目標を検索
    const existingGoal = await prisma.goalProgress.findFirst({
      where: {
        OR: [
          { goal_id: body.goal_id },
          { id: body.goal_id }
        ],
        employee_id: user_id,
        is_deleted: false
      }
    })

    if (!existingGoal) {
      return createErrorResponse(
        'GOAL_NOT_FOUND',
        '指定された目標が見つかりません',
        undefined,
        404
      )
    }

    // 更新データの準備
    const updateData: any = {
      updated_at: new Date(),
      updated_by: user_id
    }

    // 進捗率の更新
    if (body.progress_rate !== undefined) {
      const rate = Math.max(0, Math.min(100, body.progress_rate))
      updateData.progress_rate = new Prisma.Decimal(rate)
      
      // 100%になった場合は自動的に完了ステータスに
      if (rate === 100 && !body.status) {
        updateData.achievement_status = 'completed'
        updateData.completion_date = new Date()
        updateData.achievement_rate = new Prisma.Decimal(100)
      }
    }

    // 達成率の更新
    if (body.achievement_rate !== undefined) {
      updateData.achievement_rate = new Prisma.Decimal(
        Math.max(0, Math.min(100, body.achievement_rate))
      )
    }

    // ステータスの更新
    if (body.status) {
      updateData.achievement_status = body.status
      if (body.status === 'completed') {
        updateData.completion_date = new Date()
        if (!body.progress_rate) {
          updateData.progress_rate = new Prisma.Decimal(100)
        }
        if (!body.achievement_rate) {
          updateData.achievement_rate = new Prisma.Decimal(100)
        }
      }
    }

    // 自己評価の更新
    if (body.self_evaluation !== undefined) {
      updateData.self_evaluation = body.self_evaluation
    }

    // 評価コメントの更新
    if (body.evaluation_comments !== undefined) {
      updateData.evaluation_comments = body.evaluation_comments
    }

    // マイルストーンの更新
    if (body.milestones) {
      updateData.milestones = JSON.stringify(body.milestones)
    }

    // 障害事項の更新
    if (body.obstacles !== undefined) {
      updateData.obstacles = body.obstacles
    }

    // 必要なサポートの更新
    if (body.support_needed !== undefined) {
      updateData.support_needed = body.support_needed
    }

    // データベース更新
    const updatedGoal = await prisma.goalProgress.update({
      where: {
        id: existingGoal.id
      },
      data: updateData
    })

    // レスポンスデータの整形
    const responseData = {
      id: updatedGoal.id,
      goal_id: updatedGoal.goal_id,
      title: updatedGoal.goal_title,
      status: updatedGoal.achievement_status,
      progress_rate: updatedGoal.progress_rate ? Number(updatedGoal.progress_rate) : 0,
      achievement_rate: updatedGoal.achievement_rate ? Number(updatedGoal.achievement_rate) : 0,
      updated_at: updatedGoal.updated_at.toISOString()
    }

    return createSuccessResponse({
      message: '進捗が更新されました',
      progress: responseData
    })

  } catch (error) {
    console.error('目標進捗更新エラー:', error)
    return createErrorResponse(
      'INTERNAL_SERVER_ERROR',
      'サーバーエラーが発生しました',
      error instanceof Error ? error.message : '不明なエラー',
      500
    )
  }
}
