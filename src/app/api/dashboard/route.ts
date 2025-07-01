/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 * 実装内容: ダッシュボードデータ取得API
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth, createAuthErrorResponse } from '@/lib/authHelpers';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    // 認証チェック
    const user = await verifyAuth(request);

    // ダッシュボードに必要なデータを並行取得
    const [
      employeeProfile,
      skillSummary,
      recentTraining,
      goalProgress,
      notifications
    ] = await Promise.all([
      // プロフィール情報
      getEmployeeProfile(user.employeeCode),
      // スキル概要
      getSkillSummary(user.employeeId),
      // 最近の研修履歴
      getRecentTraining(user.employeeId),
      // 目標進捗
      getGoalProgress(user.employeeId),
      // 通知情報
      getNotifications(user.employeeId)
    ]);

    return NextResponse.json({
      success: true,
      data: {
        user: {
          employeeCode: user.employeeCode,
          fullName: user.fullName,
          email: user.email,
          departmentId: user.departmentId,
          positionId: user.positionId
        },
        profile: employeeProfile,
        skillSummary,
        recentTraining,
        goalProgress,
        notifications,
        lastUpdated: new Date().toISOString()
      }
    });

  } catch (error) {
    console.error('Dashboard API Error:', error);
    
    if (error instanceof Error && error.message.includes('認証')) {
      return createAuthErrorResponse(error.message);
    }

    return NextResponse.json({
      success: false,
      error: {
        code: 'INTERNAL_SERVER_ERROR',
        message: 'ダッシュボードデータの取得に失敗しました'
      }
    }, { status: 500 });
  }
}

/**
 * 従業員プロフィール情報を取得
 */
async function getEmployeeProfile(employeeCode: string) {
  const employee = await prisma.employee.findUnique({
    where: { employee_code: employeeCode },
    select: {
      employee_code: true,
      full_name: true,
      full_name_kana: true,
      email: true,
      phone: true,
      hire_date: true,
      department_id: true,
      position_id: true,
      job_type_id: true,
      employment_status: true,
      employee_status: true
    }
  });

  return employee;
}

/**
 * スキル概要情報を取得
 */
async function getSkillSummary(employeeId: string) {
  // スキル記録の統計を取得
  const skillStats = await prisma.skillRecord.groupBy({
    by: ['skill_level'],
    where: {
      employee_id: employeeId
    },
    _count: {
      skill_level: true
    }
  });

  // レベル別の集計
  const levelCounts = {
    level1: 0,
    level2: 0,
    level3: 0,
    level4: 0,
    total: 0
  };

  skillStats.forEach(stat => {
    const level = stat.skill_level;
    const count = stat._count.skill_level;
    
    if (level === 1) levelCounts.level1 = count;
    else if (level === 2) levelCounts.level2 = count;
    else if (level === 3) levelCounts.level3 = count;
    else if (level === 4) levelCounts.level4 = count;
    
    levelCounts.total += count;
  });

  // 最近更新されたスキル
  const recentSkills = await prisma.skillRecord.findMany({
    where: {
      employee_id: employeeId
    },
    orderBy: {
      updated_at: 'desc'
    },
    take: 5,
    select: {
      skill_item_id: true,
      skill_level: true,
      updated_at: true
    }
  });

  return {
    levelCounts,
    recentSkills,
    lastUpdated: recentSkills[0]?.updated_at || null
  };
}

/**
 * 最近の研修履歴を取得
 */
async function getRecentTraining(employeeId: string) {
  const training = await prisma.trainingHistory.findMany({
    where: {
      employee_id: employeeId
    },
    orderBy: {
      start_date: 'desc'
    },
    take: 5,
    select: {
      training_name: true,
      training_type: true,
      start_date: true,
      end_date: true,
      completion_rate: true,
      certificate_obtained: true,
      grade: true
    }
  });

  return training;
}

/**
 * 目標進捗を取得
 */
async function getGoalProgress(employeeId: string) {
  const goals = await prisma.goalProgress.findMany({
    where: {
      employee_id: employeeId,
      achievement_status: {
        in: ['IN_PROGRESS', 'PENDING']
      }
    },
    orderBy: {
      target_date: 'asc'
    },
    take: 5,
    select: {
      goal_title: true,
      goal_category: true,
      progress_rate: true,
      target_date: true,
      achievement_status: true,
      priority_level: true
    }
  });

  return goals;
}

/**
 * 通知情報を取得
 */
async function getNotifications(employeeId: string) {
  const notifications = await prisma.notification.findMany({
    where: {
      recipient_id: employeeId,
      read_status: 'UNREAD'
    },
    orderBy: {
      created_at: 'desc'
    },
    take: 10,
    select: {
      notification_id: true,
      title: true,
      message: true,
      notification_type: true,
      priority_level: true,
      created_at: true,
      action_url: true,
      action_label: true
    }
  });

  return notifications;
}
