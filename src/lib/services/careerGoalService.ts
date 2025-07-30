/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: 
 *   - docs/design/api/specs/API定義書_API-031_キャリア目標取得API.md
 *   - docs/design/api/specs/API定義書_API-032_キャリア目標更新API.md
 * 実装内容: キャリア目標データベース操作サービス
 */

import { prisma, handlePrismaError } from '@/lib/prisma'
import { Prisma } from '@prisma/client'

// データベース型からAPI型への変換用インターフェース
export interface CareerGoalDB {
  id: string
  goal_id: string | null
  employee_id: string | null
  goal_title: string | null
  goal_description: string | null
  goal_category: string | null
  goal_type: string | null
  priority_level: string | null
  target_date: Date | null
  start_date: Date | null
  progress_rate: Prisma.Decimal | null
  achievement_status: string | null
  completion_date: Date | null
  achievement_rate: Prisma.Decimal | null
  self_evaluation: number | null
  evaluation_comments: string | null
  related_skill_items: string | null
  milestones: string | null
  obstacles: string | null
  support_needed: string | null
  tenant_id: string
  created_at: Date
  updated_at: Date
  created_by: string
  updated_by: string
  is_deleted: boolean
}

// 新規目標作成用の型
export interface CreateCareerGoalData {
  title: string
  description?: string
  goal_type: 'short_term' | 'mid_term' | 'long_term'
  goal_category?: string
  priority: number
  target_date: string
  status: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled'
  related_skills?: Array<{
    skill_id: string
    target_level: number
  }>
  action_plans?: Array<{
    title: string
    description?: string
    due_date: string
    status: 'not_started' | 'in_progress' | 'completed'
  }>
}

// 目標更新用の型
export interface UpdateCareerGoalData {
  goal_id: string
  title?: string
  description?: string
  goal_type?: 'short_term' | 'mid_term' | 'long_term'
  goal_category?: string
  priority?: number
  target_date?: string
  status?: 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled'
  progress_rate?: number
  achievement_rate?: number
  self_evaluation?: number
  evaluation_comments?: string
  milestones?: string
  obstacles?: string
  support_needed?: string
}

/**
 * ユーザーのキャリア目標を取得
 */
export async function getCareerGoals(
  userId: string,
  year?: number,
  status?: 'active' | 'completed' | 'all'
): Promise<CareerGoalDB[]> {
  try {
    const currentYear = year || new Date().getFullYear()
    const startDate = new Date(`${currentYear}-01-01`)
    const endDate = new Date(`${currentYear + 1}-01-01`)

    // ステータスフィルタの設定
    let statusFilter: any = {}
    if (status === 'active') {
      statusFilter = {
        achievement_status: {
          in: ['not_started', 'in_progress']
        }
      }
    } else if (status === 'completed') {
      statusFilter = {
        achievement_status: 'completed'
      }
    }

    const goals = await prisma.goalProgress.findMany({
      where: {
        employee_id: userId,
        start_date: {
          gte: startDate,
          lt: endDate
        },
        is_deleted: false,
        ...statusFilter
      },
      orderBy: [
        { priority_level: 'desc' },
        { target_date: 'asc' },
        { created_at: 'desc' }
      ]
    })

    return goals
  } catch (error) {
    console.error('キャリア目標取得エラー:', error)
    throw handlePrismaError(error)
  }
}

/**
 * 新規キャリア目標を作成
 */
export async function createCareerGoal(
  userId: string,
  goalData: CreateCareerGoalData
): Promise<CareerGoalDB> {
  try {
    const goalId = `G${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    const careerPlanId = `CP${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    const currentDateTime = new Date()

    // 優先度レベルの変換（1-5 → high/medium/low）
    let priorityLevel: string
    if (goalData.priority >= 4) {
      priorityLevel = 'high'
    } else if (goalData.priority >= 2) {
      priorityLevel = 'medium'
    } else {
      priorityLevel = 'low'
    }

    // 関連スキルとアクションプランをJSON文字列に変換
    const relatedSkillsJson = goalData.related_skills ? JSON.stringify(goalData.related_skills) : null
    const actionPlansJson = goalData.action_plans ? JSON.stringify(goalData.action_plans) : null

    // トランザクションで両テーブルに登録
    const result = await prisma.$transaction(async (tx) => {
      // 1. TRN_GoalProgress に詳細な目標データを登録
      const newGoal = await tx.goalProgress.create({
        data: {
          id: `goal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
          goal_id: goalId,
          employee_id: userId,
          goal_title: goalData.title,
          goal_description: goalData.description || null,
          goal_category: goalData.goal_category || 'general',
          goal_type: goalData.goal_type,
          priority_level: priorityLevel,
          target_date: new Date(goalData.target_date),
          start_date: currentDateTime,
          achievement_status: goalData.status,
          progress_rate: new Prisma.Decimal(0),
          achievement_rate: new Prisma.Decimal(0),
          related_skill_items: relatedSkillsJson,
          milestones: actionPlansJson,
          tenant_id: 'default', // シングルテナント環境
          created_by: userId,
          updated_by: userId,
          is_deleted: false
        }
      })

      // 2. 既存のアクティブなキャリアプランがあるかチェック
      const existingCareerPlan = await tx.careerPlan.findFirst({
        where: {
          employee_id: userId,
          is_deleted: false,
          plan_status: 'ACTIVE'
        }
      })

      if (existingCareerPlan) {
        // 既存のキャリアプランを更新
        await tx.careerPlan.update({
          where: {
            career_plan_id: existingCareerPlan.career_plan_id
          },
          data: {
            plan_description: goalData.title,
            target_level: goalData.goal_type === 'long_term' ? 'SENIOR' : 
                         goalData.goal_type === 'mid_term' ? 'INTERMEDIATE' : 'JUNIOR',
            plan_end_date: new Date(goalData.target_date),
            progress_percentage: new Prisma.Decimal(0),
            priority_level: priorityLevel,
            updated_at: currentDateTime
          }
        })
      } else {
        // 新規キャリアプランを作成
        await tx.careerPlan.create({
          data: {
            career_plan_id: careerPlanId,
            employee_id: userId,
            plan_name: `${goalData.title} - キャリアプラン`,
            plan_description: goalData.title,
            plan_type: goalData.goal_type,
            current_level: 'JUNIOR',
            target_level: goalData.goal_type === 'long_term' ? 'SENIOR' : 
                         goalData.goal_type === 'mid_term' ? 'INTERMEDIATE' : 'JUNIOR',
            plan_start_date: currentDateTime,
            plan_end_date: new Date(goalData.target_date),
            plan_status: 'ACTIVE',
            progress_percentage: new Prisma.Decimal(0),
            priority_level: priorityLevel,
            required_skills: relatedSkillsJson,
            development_actions: actionPlansJson,
            is_deleted: false
          }
        })
      }

      return newGoal
    })

    return result
  } catch (error) {
    console.error('キャリア目標作成エラー:', error)
    throw handlePrismaError(error)
  }
}

/**
 * キャリア目標を更新
 */
export async function updateCareerGoal(
  userId: string,
  updateData: UpdateCareerGoalData
): Promise<CareerGoalDB> {
  try {
    // 既存の目標が存在するかチェック
    const existingGoal = await prisma.goalProgress.findFirst({
      where: {
        goal_id: updateData.goal_id,
        employee_id: userId,
        is_deleted: false
      }
    })

    if (!existingGoal) {
      throw new Error('GOAL_NOT_FOUND')
    }

    // トランザクションで両テーブルを更新
    const result = await prisma.$transaction(async (tx) => {
      // 1. TRN_GoalProgress の更新データ準備
      const updateFields: any = {
        updated_by: userId,
        updated_at: new Date()
      }

      if (updateData.title !== undefined) {
        updateFields.goal_title = updateData.title
      }
      if (updateData.description !== undefined) {
        updateFields.goal_description = updateData.description
      }
      if (updateData.goal_type !== undefined) {
        updateFields.goal_type = updateData.goal_type
      }
      if (updateData.goal_category !== undefined) {
        updateFields.goal_category = updateData.goal_category
      }
      if (updateData.priority !== undefined) {
        // 優先度レベルの変換
        let priorityLevel: string
        if (updateData.priority >= 4) {
          priorityLevel = 'high'
        } else if (updateData.priority >= 2) {
          priorityLevel = 'medium'
        } else {
          priorityLevel = 'low'
        }
        updateFields.priority_level = priorityLevel
      }
      if (updateData.target_date !== undefined) {
        updateFields.target_date = new Date(updateData.target_date)
      }
      if (updateData.status !== undefined) {
        updateFields.achievement_status = updateData.status
        
        // 完了時の処理
        if (updateData.status === 'completed') {
          updateFields.completion_date = new Date()
          updateFields.progress_rate = new Prisma.Decimal(100)
          updateFields.achievement_rate = new Prisma.Decimal(100)
        }
      }
      if (updateData.progress_rate !== undefined) {
        updateFields.progress_rate = new Prisma.Decimal(updateData.progress_rate)
      }

      // TRN_GoalProgress を更新
      const updatedGoal = await tx.goalProgress.update({
        where: {
          id: existingGoal.id
        },
        data: updateFields
      })

      // 2. 対応するキャリアプランも更新
      const existingCareerPlan = await tx.careerPlan.findFirst({
        where: {
          employee_id: userId,
          is_deleted: false,
          plan_status: 'ACTIVE'
        }
      })

      if (existingCareerPlan) {
        const careerPlanUpdateFields: any = {
          updated_at: new Date()
        }

        if (updateData.title !== undefined) {
          careerPlanUpdateFields.plan_description = updateData.title
        }
        if (updateData.goal_type !== undefined) {
          careerPlanUpdateFields.target_level = updateData.goal_type === 'long_term' ? 'SENIOR' : 
                                               updateData.goal_type === 'mid_term' ? 'INTERMEDIATE' : 'JUNIOR'
        }
        if (updateData.target_date !== undefined) {
          careerPlanUpdateFields.plan_end_date = new Date(updateData.target_date)
        }
        if (updateData.priority !== undefined) {
          let priorityLevel: string
          if (updateData.priority >= 4) {
            priorityLevel = 'high'
          } else if (updateData.priority >= 2) {
            priorityLevel = 'medium'
          } else {
            priorityLevel = 'low'
          }
          careerPlanUpdateFields.priority_level = priorityLevel
        }
        if (updateData.progress_rate !== undefined) {
          careerPlanUpdateFields.progress_percentage = new Prisma.Decimal(updateData.progress_rate)
        }
        if (updateData.status === 'completed') {
          careerPlanUpdateFields.plan_status = 'COMPLETED'
          careerPlanUpdateFields.progress_percentage = new Prisma.Decimal(100)
        }

        await tx.careerPlan.update({
          where: {
            career_plan_id: existingCareerPlan.career_plan_id
          },
          data: careerPlanUpdateFields
        })
      }

      return updatedGoal
    })

    return result
  } catch (error) {
    console.error('キャリア目標更新エラー:', error)
    throw handlePrismaError(error)
  }
}

/**
 * キャリア目標を削除（論理削除）
 */
export async function deleteCareerGoal(userId: string, goalId: string): Promise<boolean> {
  try {
    console.log('削除処理開始:', { userId, goalId, goalIdType: typeof goalId })

    // まず goalProgress テーブルから検索
    const goalProgressSearchConditions = {
      OR: [
        { goal_id: goalId },
        { id: goalId }
      ],
      employee_id: userId,
      is_deleted: false
    }

    const existingGoalProgress = await prisma.goalProgress.findFirst({
      where: goalProgressSearchConditions
    })

    if (existingGoalProgress) {
      console.log('goalProgress テーブルで目標を発見:', existingGoalProgress.id)
      
      await prisma.goalProgress.update({
        where: {
          id: existingGoalProgress.id
        },
        data: {
          is_deleted: true,
          achievement_status: 'cancelled',
          updated_by: userId,
          updated_at: new Date()
        }
      })

      console.log('goalProgress 削除処理完了:', existingGoalProgress.id)
      return true
    }

    // goalProgress で見つからない場合、careerPlan テーブルから検索
    const careerPlanSearchConditions = {
      career_plan_id: goalId,
      employee_id: userId,
      is_deleted: false
    }

    const existingCareerPlan = await prisma.careerPlan.findFirst({
      where: careerPlanSearchConditions
    })

    if (existingCareerPlan) {
      console.log('careerPlan テーブルで目標を発見:', existingCareerPlan.career_plan_id)
      
      await prisma.careerPlan.update({
        where: {
          career_plan_id: existingCareerPlan.career_plan_id
        },
        data: {
          is_deleted: true,
          plan_status: 'INACTIVE',
          updated_at: new Date()
        }
      })

      console.log('careerPlan 削除処理完了:', existingCareerPlan.career_plan_id)
      return true
    }

    // どちらのテーブルでも見つからない場合
    console.error('目標が見つかりません:', { userId, goalId })
    
    // デバッグ用：利用可能な目標を表示
    const allGoalProgress = await prisma.goalProgress.findMany({
      where: {
        employee_id: userId,
        is_deleted: false
      },
      select: {
        id: true,
        goal_id: true,
        goal_title: true
      }
    })

    const allCareerPlans = await prisma.careerPlan.findMany({
      where: {
        employee_id: userId,
        is_deleted: false
      },
      select: {
        career_plan_id: true,
        plan_description: true
      }
    })

    console.log('利用可能な goalProgress:', allGoalProgress)
    console.log('利用可能な careerPlan:', allCareerPlans)
    
    throw new Error('GOAL_NOT_FOUND')
  } catch (error) {
    console.error('キャリア目標削除エラー:', error)
    
    // GOAL_NOT_FOUNDエラーはそのまま再スロー
    if (error instanceof Error && error.message === 'GOAL_NOT_FOUND') {
      throw error
    }
    
    throw handlePrismaError(error)
  }
}

/**
 * ユーザーの目標統計情報を取得
 */
export async function getCareerGoalStats(userId: string, year?: number): Promise<{
  totalGoals: number
  completedGoals: number
  inProgressGoals: number
  notStartedGoals: number
  completionRate: number
}> {
  try {
    const currentYear = year || new Date().getFullYear()
    const startDate = new Date(`${currentYear}-01-01`)
    const endDate = new Date(`${currentYear + 1}-01-01`)

    const stats = await prisma.goalProgress.groupBy({
      by: ['achievement_status'],
      where: {
        employee_id: userId,
        start_date: {
          gte: startDate,
          lt: endDate
        },
        is_deleted: false
      },
      _count: {
        achievement_status: true
      }
    })

    let totalGoals = 0
    let completedGoals = 0
    let inProgressGoals = 0
    let notStartedGoals = 0

    stats.forEach(stat => {
      const count = stat._count.achievement_status
      totalGoals += count

      switch (stat.achievement_status) {
        case 'completed':
          completedGoals += count
          break
        case 'in_progress':
          inProgressGoals += count
          break
        case 'not_started':
          notStartedGoals += count
          break
      }
    })

    const completionRate = totalGoals > 0 ? (completedGoals / totalGoals) * 100 : 0

    return {
      totalGoals,
      completedGoals,
      inProgressGoals,
      notStartedGoals,
      completionRate: Math.round(completionRate * 100) / 100
    }
  } catch (error) {
    console.error('キャリア目標統計取得エラー:', error)
    throw handlePrismaError(error)
  }
}

/**
 * スキルカテゴリ一覧を取得
 */
export async function getSkillCategories(): Promise<any[]> {
  try {
    const categories = await prisma.skillCategory.findMany({
      where: {
        is_deleted: false,
        category_status: 'ACTIVE'
      },
      orderBy: [
        { category_level: 'asc' },
        { display_order: 'asc' }
      ]
    })

    return categories
  } catch (error) {
    console.error('スキルカテゴリ取得エラー:', error)
    throw handlePrismaError(error)
  }
}

/**
 * ポジション一覧を取得
 */
export async function getPositions(): Promise<any[]> {
  try {
    const positions = await prisma.position.findMany({
      where: {
        is_deleted: false,
        position_status: 'ACTIVE'
      },
      orderBy: [
        { position_level: 'asc' },
        { sort_order: 'asc' }
      ]
    })

    return positions
  } catch (error) {
    console.error('ポジション取得エラー:', error)
    throw handlePrismaError(error)
  }
}

/**
 * アクティブなキャリアプランを取得
 */
export async function getActiveCareerPlan(userId: string): Promise<any | null> {
  try {
    const careerPlan = await prisma.careerPlan.findFirst({
      where: {
        employee_id: userId,
        is_deleted: false,
        plan_status: 'ACTIVE'
      },
      orderBy: {
        plan_start_date: 'desc'
      }
    })

    return careerPlan
  } catch (error) {
    console.error('キャリアプラン取得エラー:', error)
    throw handlePrismaError(error)
  }
}
