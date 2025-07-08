/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/api/specs/API定義書_API-081_ダッシュボードデータ取得API.md
 * 実装内容: ダッシュボードデータ取得API（API-081準拠）
 */

import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth, createAuthErrorResponse } from '@/lib/authHelpers';
import { prisma } from '@/lib/prisma';

export async function GET(request: NextRequest) {
  try {
    // 認証チェック
    const user = await verifyAuth(request);

    // クエリパラメータの取得
    const { searchParams } = new URL(request.url);
    const userId = searchParams.get('user_id') || user.employeeCode;
    const widgetsParam = searchParams.get('widgets');
    const year = searchParams.get('year') ? parseInt(searchParams.get('year')!) : new Date().getFullYear();
    const month = searchParams.get('month') ? parseInt(searchParams.get('month')!) : new Date().getMonth() + 1;

    // 権限チェック（他のユーザーのダッシュボードを見る場合）
    if (userId !== user.employeeCode) {
      const hasPermission = await checkDashboardPermission(user.employeeCode, userId);
      if (!hasPermission) {
        return NextResponse.json({
          success: false,
          error: {
            code: 'PERMISSION_DENIED',
            message: '権限がありません',
            details: '他のユーザーのダッシュボード情報を閲覧する権限がありません。'
          }
        }, { status: 403 });
      }
    }

    // 対象ユーザーの存在確認
    const targetUser = await getTargetUser(userId);
    if (!targetUser) {
      return NextResponse.json({
        success: false,
        error: {
          code: 'USER_NOT_FOUND',
          message: '指定されたユーザーが見つかりません'
        }
      }, { status: 404 });
    }

    // 取得するウィジェットの決定
    const requestedWidgets = widgetsParam ? widgetsParam.split(',') : [
      'tasks', 'skills', 'trainings', 'work_records', 'notifications', 'goals', 'team', 'calendar'
    ];

    // ウィジェットデータを並行取得
    const widgetPromises: Record<string, Promise<any>> = {};
    
    if (requestedWidgets.includes('tasks')) {
      widgetPromises.tasks = getTasksWidget(targetUser.employee_code);
    }
    if (requestedWidgets.includes('skills')) {
      widgetPromises.skills = getSkillsWidget(targetUser.employee_code);
    }
    if (requestedWidgets.includes('trainings')) {
      widgetPromises.trainings = getTrainingsWidget(targetUser.employee_code);
    }
    if (requestedWidgets.includes('work_records')) {
      widgetPromises.work_records = getWorkRecordsWidget(targetUser.employee_code, year, month);
    }
    if (requestedWidgets.includes('notifications')) {
      widgetPromises.notifications = getNotificationsWidget(targetUser.employee_code);
    }
    if (requestedWidgets.includes('goals')) {
      widgetPromises.goals = getGoalsWidget(targetUser.employee_code);
    }
    if (requestedWidgets.includes('team')) {
      widgetPromises.team = getTeamWidget(targetUser.employee_code);
    }
    if (requestedWidgets.includes('calendar')) {
      widgetPromises.calendar = getCalendarWidget(targetUser.employee_code, year, month);
    }

    const [widgets, systemNotices] = await Promise.all([
      Promise.all(Object.entries(widgetPromises).map(async ([key, promise]) => [key, await promise])),
      getSystemNotices()
    ]);

    const widgetsData = Object.fromEntries(widgets);

    return NextResponse.json({
      success: true,
      data: {
        user: {
          employeeCode: targetUser.employee_code,
          fullName: targetUser.full_name,
          email: targetUser.email || '',
          departmentId: targetUser.department_id,
          positionId: targetUser.position_id
        },
        profile: {
          employee_code: targetUser.employee_code,
          full_name: targetUser.full_name,
          full_name_kana: targetUser.full_name_kana,
          email: targetUser.email,
          phone: targetUser.phone,
          hire_date: targetUser.hire_date,
          department_id: targetUser.department_id,
          position_id: targetUser.position_id,
          job_type_id: targetUser.job_type_id,
          employment_status: targetUser.employment_status,
          employee_status: targetUser.employee_status
        },
        skillSummary: {
          levelCounts: widgetsData.skills?.level_counts || { level1: 0, level2: 0, level3: 0, level4: 0, total: 0 },
          recentSkills: widgetsData.skills?.top_skills ? widgetsData.skills.top_skills.map((skill: any) => ({
            skill_item_id: skill.skill_id,
            skill_level: skill.level,
            updated_at: widgetsData.skills?.last_updated_at || new Date().toISOString()
          })) : [],
          lastUpdated: widgetsData.skills?.last_updated_at || null
        },
        recentTraining: widgetsData.trainings?.recent_completions || [],
        goalProgress: widgetsData.goals?.upcoming_milestones || [],
        notifications: widgetsData.notifications?.recent_notifications || [],
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
        code: 'SYSTEM_ERROR',
        message: 'システムエラーが発生しました'
      }
    }, { status: 500 });
  }
}

/**
 * 対象ユーザーの情報を取得
 */
async function getTargetUser(userId: string) {
  return await prisma.employee.findUnique({
    where: { employee_code: userId }
  });
}

/**
 * ダッシュボード閲覧権限をチェック
 */
async function checkDashboardPermission(requesterId: string, targetUserId: string): Promise<boolean> {
  // 自分自身の場合は常に許可
  if (requesterId === targetUserId) {
    return true;
  }

  // TODO: 実際の権限チェックロジックを実装
  // - 部下のダッシュボード：マネージャーは閲覧可能
  // - 同部署のダッシュボードサマリー：部署管理者は閲覧可能
  // - 全社員のダッシュボードサマリー：人事担当者・管理者は閲覧可能
  
  return false; // 現在は他者の閲覧を禁止
}

/**
 * タスクウィジェットデータを取得
 */
async function getTasksWidget(employeeId: string) {
  // TODO: タスク管理システムとの連携実装
  // 現在はモックデータを返す
  return {
    total_count: 15,
    completed_count: 8,
    overdue_count: 2,
    upcoming_tasks: [
      {
        task_id: "task-12345",
        title: "スキル評価シートの提出",
        due_date: "2025-07-31",
        priority: 3,
        status: "in_progress",
        category: "評価"
      },
      {
        task_id: "task-23456",
        title: "プロジェクト進捗報告書作成",
        due_date: "2025-08-05",
        priority: 2,
        status: "not_started",
        category: "報告"
      }
    ]
  };
}

/**
 * スキルウィジェットデータを取得
 */
async function getSkillsWidget(employeeId: string) {
  try {
    // 実際のスキルデータを取得（リレーションなしで取得）
    const skillRecords = await prisma.skillRecord.findMany({
      where: {
        employee_id: employeeId
      },
      orderBy: {
        updated_at: 'desc'
      }
    });

    // スキルアイテム情報を別途取得
    const skillItemIds = skillRecords.map(record => record.skill_item_id).filter(Boolean) as string[];
    const skillItems = await prisma.skillItem.findMany({
      where: {
        skill_code: {
          in: skillItemIds
        }
      }
    });

    // スキルカテゴリ情報を別途取得
    const categoryIds = skillItems.map(item => item.skill_category_id).filter(Boolean) as string[];
    const skillCategories = await prisma.skillCategory.findMany({
      where: {
        category_code: {
          in: categoryIds
        }
      }
    });

    // スキルレベル別の集計
    const levelCounts = {
      level1: 0,
      level2: 0,
      level3: 0,
      level4: 0,
      total: skillRecords.length
    };

    skillRecords.forEach(record => {
      const level = record.skill_level;
      if (level && level >= 1 && level <= 4) {
        levelCounts[`level${level}` as keyof typeof levelCounts]++;
      }
    });

    // 平均レベル計算
    const totalLevels = skillRecords.reduce((sum, record) => sum + (record.skill_level || 0), 0);
    const averageLevel = skillRecords.length > 0 ? Number((totalLevels / skillRecords.length).toFixed(1)) : 0;

    // スキル情報をマップ化
    const skillItemMap = new Map(skillItems.map(item => [item.skill_code, item]));
    const categoryMap = new Map(skillCategories.map(cat => [cat.category_code || '', cat]));

    // トップスキル（レベル3以上）
    const topSkills = skillRecords
      .filter(record => (record.skill_level || 0) >= 3)
      .slice(0, 5)
      .map(record => {
        const skillItem = skillItemMap.get(record.skill_item_id || '');
        const category = skillItem && skillItem.skill_category_id ? categoryMap.get(skillItem.skill_category_id) : null;
        
        return {
          skill_id: record.skill_item_id || '',
          skill_name: skillItem?.skill_name || 'Unknown Skill',
          level: record.skill_level || 0,
          category: category?.category_name || 'Unknown Category'
        };
      });

    // 改善エリア（レベル2以下）
    const improvementAreas = skillRecords
      .filter(record => (record.skill_level || 0) <= 2)
      .slice(0, 5)
      .map(record => {
        const skillItem = skillItemMap.get(record.skill_item_id || '');
        const category = skillItem && skillItem.skill_category_id ? categoryMap.get(skillItem.skill_category_id) : null;
        
        return {
          skill_id: record.skill_item_id || '',
          skill_name: skillItem?.skill_name || 'Unknown Skill',
          level: record.skill_level || 0,
          category: category?.category_name || 'Unknown Category'
        };
      });

    // 最終更新日
    const lastUpdated = skillRecords.length > 0 && skillRecords[0] && skillRecords[0].updated_at ? skillRecords[0].updated_at.toISOString() : null;

    return {
      total_skills: skillRecords.length,
      average_level: averageLevel,
      level_counts: levelCounts,
      top_skills: topSkills,
      improvement_areas: improvementAreas,
      skill_status: skillRecords.length > 0 ? "submitted" : "draft",
      last_updated_at: lastUpdated
    };
  } catch (error) {
    console.error('Skills widget error:', error);
    return {
      total_skills: 0,
      average_level: 0,
      level_counts: { level1: 0, level2: 0, level3: 0, level4: 0, total: 0 },
      top_skills: [],
      improvement_areas: [],
      skill_status: "draft",
      last_updated_at: null
    };
  }
}

/**
 * 研修ウィジェットデータを取得
 */
async function getTrainingsWidget(employeeId: string) {
  try {
    // TODO: 実際の研修データ取得実装
    // 現在はモックデータを返す
    return {
      completed_count: 12,
      planned_count: 3,
      upcoming_trainings: [
        {
          training_id: "training-001",
          training_name: "Next.js 14 実践研修",
          start_date: "2025-08-15",
          end_date: "2025-08-16",
          status: "planned",
          category: "技術研修"
        },
        {
          training_id: "training-002",
          training_name: "プロジェクトマネジメント基礎",
          start_date: "2025-09-01",
          end_date: "2025-09-02",
          status: "planned",
          category: "マネジメント"
        }
      ],
      recent_completions: [
        {
          training_id: "training-003",
          training_name: "TypeScript応用",
          start_date: "2025-06-10",
          end_date: "2025-06-11",
          status: "completed",
          category: "技術研修"
        },
        {
          training_id: "training-004",
          training_name: "セキュリティ基礎",
          start_date: "2025-05-20",
          end_date: "2025-05-21",
          status: "completed",
          category: "セキュリティ"
        }
      ]
    };
  } catch (error) {
    console.error('Trainings widget error:', error);
    return {
      completed_count: 0,
      planned_count: 0,
      upcoming_trainings: [],
      recent_completions: []
    };
  }
}

/**
 * 作業実績ウィジェットデータを取得
 */
async function getWorkRecordsWidget(employeeId: string, year: number, month: number) {
  try {
    // TODO: 実際の作業実績データ取得実装
    // 現在はモックデータを返す
    return {
      monthly_hours: 152,
      monthly_target: 160,
      completion_rate: 95.0,
      by_category: {
        "開発": 120,
        "会議": 20,
        "ドキュメント作成": 8,
        "その他": 4
      },
      recent_records: [
        {
          record_id: "record-1",
          date: "2025-07-08",
          project_name: "スキル報告書システム",
          task: "ダッシュボードAPI実装",
          hours: 8,
          category: "開発"
        },
        {
          record_id: "record-2",
          date: "2025-07-07",
          project_name: "スキル報告書システム",
          task: "設計レビュー",
          hours: 2,
          category: "会議"
        },
        {
          record_id: "record-3",
          date: "2025-07-07",
          project_name: "スキル報告書システム",
          task: "フロントエンド実装",
          hours: 6,
          category: "開発"
        }
      ]
    };
  } catch (error) {
    console.error('Work records widget error:', error);
    return {
      monthly_hours: 0,
      monthly_target: 160,
      completion_rate: 0,
      by_category: {},
      recent_records: []
    };
  }
}

/**
 * 通知ウィジェットデータを取得
 */
async function getNotificationsWidget(employeeId: string) {
  try {
    // 未読通知数
    const unreadCount = await prisma.notification.count({
      where: {
        recipient_id: employeeId,
        read_status: 'UNREAD'
      }
    });

    // 最近の通知
    const recentNotifications = await prisma.notification.findMany({
      where: {
        recipient_id: employeeId
      },
      orderBy: {
        created_at: 'desc'
      },
      take: 5,
      select: {
        notification_id: true,
        title: true,
        message: true,
        notification_type: true,
        priority_level: true,
        created_at: true,
        action_url: true,
        action_label: true,
        read_status: true
      }
    });

    return {
      unread_count: unreadCount,
      recent_notifications: recentNotifications.map(notification => ({
        notification_id: notification.notification_id,
        type: notification.notification_type?.toLowerCase() || 'other',
        title: notification.title,
        message: notification.message,
        created_at: notification.created_at ? notification.created_at.toISOString() : new Date().toISOString(),
        is_read: notification.read_status === 'READ',
        link: notification.action_url || ''
      }))
    };
  } catch (error) {
    console.error('Notifications widget error:', error);
    return {
      unread_count: 0,
      recent_notifications: []
    };
  }
}

/**
 * 目標ウィジェットデータを取得
 */
async function getGoalsWidget(employeeId: string) {
  try {
    // 総目標数
    const totalGoals = await prisma.goalProgress.count({
      where: {
        employee_id: employeeId
      }
    });

    // 達成済目標数
    const completedGoals = await prisma.goalProgress.count({
      where: {
        employee_id: employeeId,
        achievement_status: 'ACHIEVED'
      }
    });

    // 進捗率の平均
    const goalProgressData = await prisma.goalProgress.findMany({
      where: {
        employee_id: employeeId,
        achievement_status: {
          in: ['IN_PROGRESS', 'PENDING']
        }
      },
      select: {
        progress_rate: true
      }
    });

    const averageProgress = goalProgressData.length > 0 
      ? Number((goalProgressData.reduce((sum, goal) => sum + Number(goal.progress_rate || 0), 0) / goalProgressData.length).toFixed(1))
      : 0;

    // 直近のマイルストーン
    const upcomingMilestones = await prisma.goalProgress.findMany({
      where: {
        employee_id: employeeId,
        target_date: {
          gte: new Date()
        }
      },
      orderBy: {
        target_date: 'asc'
      },
      take: 3,
      select: {
        goal_id: true,
        goal_title: true,
        target_date: true,
        progress_rate: true
      }
    });

    return {
      total_goals: totalGoals,
      completed_goals: completedGoals,
      progress_rate: averageProgress,
      upcoming_milestones: upcomingMilestones.map((goal, index) => ({
        milestone_id: `milestone-${index + 1}`,
        goal_id: goal.goal_id,
        title: goal.goal_title,
        due_date: goal.target_date?.toISOString().split('T')[0] || '',
        progress: goal.progress_rate || 0
      })),
      goal_status: "submitted" // TODO: 実際のステータス取得
    };
  } catch (error) {
    console.error('Goals widget error:', error);
    return {
      total_goals: 0,
      completed_goals: 0,
      progress_rate: 0,
      upcoming_milestones: [],
      goal_status: "draft"
    };
  }
}

/**
 * チームウィジェットデータを取得
 */
async function getTeamWidget(employeeId: string) {
  try {
    // TODO: チーム情報の実装
    // 現在はモックデータを返す
    return {
      team_name: "開発チーム",
      manager: {
        user_id: "manager001",
        user_name: "山田 部長",
        email: "yamada@example.com",
        position: "部長"
      },
      member_count: 8,
      recent_updates: [
        {
          update_id: "update-1",
          user_id: "user001",
          user_name: "佐藤 太郎",
          type: "skill",
          title: "Java スキルレベルを更新",
          updated_at: new Date().toISOString()
        }
      ]
    };
  } catch (error) {
    console.error('Team widget error:', error);
    return {
      team_name: "",
      manager: null,
      member_count: 0,
      recent_updates: []
    };
  }
}

/**
 * カレンダーウィジェットデータを取得
 */
async function getCalendarWidget(employeeId: string, year: number, month: number) {
  try {
    // TODO: カレンダーイベントの実装
    // 現在はモックデータを返す
    return {
      year: year,
      month: month,
      events: [
        {
          event_id: "event-1",
          title: "プロジェクト会議",
          start_date: new Date(year, month - 1, 15, 10, 0).toISOString(),
          end_date: new Date(year, month - 1, 15, 11, 0).toISOString(),
          type: "meeting",
          location: "会議室A",
          is_all_day: false
        }
      ]
    };
  } catch (error) {
    console.error('Calendar widget error:', error);
    return {
      year: year,
      month: month,
      events: []
    };
  }
}

/**
 * システムお知らせを取得
 */
async function getSystemNotices() {
  try {
    const now = new Date();
    
    // TODO: システムお知らせテーブルの実装
    // 現在はモックデータを返す
    return [
      {
        notice_id: "notice-1",
        title: "システムメンテナンスのお知らせ",
        content: "7月15日（月）午前2時〜6時にシステムメンテナンスを実施します。",
        importance: "high",
        start_date: "2025-07-01",
        end_date: "2025-07-15",
        created_at: "2025-07-01T10:00:00+09:00"
      }
    ];
  } catch (error) {
    console.error('System notices error:', error);
    return [];
  }
}
