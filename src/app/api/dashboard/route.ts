// API-091: ダッシュボードデータ取得API
import { NextRequest, NextResponse } from 'next/server';
import { verifyAuth } from '@/lib/auth';
import { PrismaClient } from '@prisma/client';
import type { DashboardData } from '@/types/dashboard';

const prisma = new PrismaClient();

export async function GET(request: NextRequest) {
  try {
    // 認証確認
    const authResult = await verifyAuth(request);
    if (!authResult.success || !authResult.userId) {
      return NextResponse.json(
        { success: false, error: '認証が必要です' },
        { status: 401 }
      );
    }

    const userId = authResult.userId;
    const employeeId = authResult.employeeId || userId;
    const tenantId = 'default'; // TODO: テナントIDを取得

    console.log('Dashboard API - Auth result:', authResult);
    console.log('Dashboard API - Using:', { userId, employeeId });

    // ユーザー情報を取得
    const user = await prisma.employee.findFirst({
      where: {
        employee_code: employeeId,
        is_deleted: false
      }
    });

    console.log('Dashboard API - User found:', { 
      found: !!user, 
      searchedBy: employeeId,
      foundUser: user ? { id: user.id, code: user.employee_code } : null 
    });

    if (!user) {
      return NextResponse.json(
        { success: false, error: 'ユーザーが見つかりません' },
        { status: 404 }
      );
    }

    // 部門とポジション情報を取得
    let department = null;
    let position = null;
    
    if (user.department_id) {
      department = await prisma.department.findFirst({
        where: { department_code: user.department_id }
      });
    }
    
    if (user.position_id) {
      position = await prisma.position.findFirst({
        where: { position_code: user.position_id }
      });
    }

    // キャリアプランと同じユーザーIDを使用するためemployee_codeを使用
    // キャリアプランは'000001'を使用している
    const actualEmployeeId = user.employee_code || user.id;
    console.log('Dashboard API - Using actualEmployeeId:', actualEmployeeId);

    // 並列でデータを取得
    const [
      skillData,
      goalData,
      certificationData,
      workData,
      notificationData,
      taskData,
      teamData
    ] = await Promise.all([
      getSkillSummary(actualEmployeeId, tenantId),
      getGoalSummary(actualEmployeeId, tenantId),
      getCertificationSummary(actualEmployeeId, tenantId),
      getWorkSummary(actualEmployeeId, tenantId),
      getNotifications(userId, tenantId),
      getTasks(userId, tenantId),
      user.position_id && isManagerPosition(user.position_id) 
        ? getTeamSummary(actualEmployeeId, tenantId) 
        : null
    ]);

    // ダッシュボードデータを構築
    const dashboardData: DashboardData = {
      user_info: {
        user_id: user.id,
        employee_id: user.employee_code || '',
        name: user.full_name || '',
        email: user.email || '',
        department_id: user.department_id || '',
        department_name: department?.department_name || '',
        position_id: user.position_id || '',
        position_name: position?.position_name || '',
        avatar_url: undefined,
        last_login: undefined
      },
      skill_summary: skillData,
      goal_summary: goalData,
      certification_summary: certificationData,
      work_summary: workData,
      ...(teamData ? { team_summary: teamData } : {}),
      notifications: notificationData,
      tasks: taskData,
      analytics: generateAnalytics(skillData, goalData),
      recommendations: generateRecommendations(skillData, goalData, certificationData),
      last_updated: new Date()
    };

    return NextResponse.json({
      success: true,
      data: dashboardData
    });

  } catch (error) {
    console.error('Dashboard data fetch error:', error);
    return NextResponse.json(
      { success: false, error: 'データの取得に失敗しました' },
      { status: 500 }
    );
  }
}

// スキルサマリー取得
async function getSkillSummary(userId: string, tenantId: string) {
  const skills = await prisma.skillRecord.findMany({
    where: {
      employee_id: userId,
      is_deleted: false
    },
    orderBy: {
      updated_at: 'desc'
    }
  });

  // レベル別集計
  const skillsByLevel = {
    none: 0,
    basic: 0,
    intermediate: 0,
    advanced: 0
  };

  // カテゴリ別集計
  const categoryMap = new Map();

  skills.forEach((skill: any) => {
    // レベル集計
    const level = skill.skill_level || 0;
    switch (level) {
      case 0: skillsByLevel.none++; break;
      case 1: skillsByLevel.basic++; break;
      case 2: skillsByLevel.intermediate++; break;
      case 3: skillsByLevel.advanced++; break;
    }

    // カテゴリ集計
    const categoryId = 'default';
    const categoryName = 'スキル';
      
    if (!categoryMap.has(categoryId)) {
      categoryMap.set(categoryId, {
        category_id: categoryId,
        category_name: categoryName,
        count: 0,
        total_score: 0
      });
    }
    
    const category = categoryMap.get(categoryId);
    category.count++;
    category.total_score += skill.skill_level || 0;
  });

  // カテゴリ別データを配列に変換
  const skillsByCategory = Array.from(categoryMap.values()).map(cat => ({
    category_id: cat.category_id,
    category_name: cat.category_name,
    count: cat.count,
    average_level: cat.count > 0 ? cat.total_score / cat.count : 0
  }));

  // 最近の更新（最新5件）
  const recentUpdates = skills.slice(0, 5).map((skill: any) => ({
    skill_id: skill.id,
    skill_name: skill.skill_name || '',
    old_level: getLevelLabel((skill.skill_level || 0) - 1),
    new_level: getLevelLabel(skill.skill_level || 0),
    updated_at: skill.updated_at
  }));

  // トップスキル（評価が高い順に5件）
  const topSkills = skills
    .filter((s: any) => s.skill_level >= 2)
    .slice(0, 5)
    .map((skill: any) => ({
      skill_id: skill.id,
      skill_name: skill.skill_name || '',
      level: getLevelLabel(skill.skill_level),
      category_name: 'スキル'
    }));

  // 成長トレンド（仮データ）
  const growthTrend = generateGrowthTrend();

  return {
    total_skills: skills.length,
    skills_by_level: skillsByLevel,
    skills_by_category: skillsByCategory,
    recent_updates: recentUpdates,
    top_skills: topSkills,
    growth_trend: growthTrend
  };
}

// 目標サマリー取得
async function getGoalSummary(userId: string, tenantId: string) {
  console.log('[getGoalSummary] userId:', userId);
  
  const goals = await prisma.goalProgress.findMany({
    where: {
      employee_id: userId,
      is_deleted: false
    },
    orderBy: {
      target_date: 'asc'
    }
  });
  
  console.log('[getGoalSummary] 目標数:', goals.length);

  // 目標をステータス別に分類
  const completedGoals = goals.filter((g: any) => 
    g.achievement_status === 'completed' || 
    g.achievement_status === 'achieved'
  );
  
  const currentGoals = goals.filter((g: any) => 
    g.achievement_status === 'in_progress' || 
    g.achievement_status === 'pending' ||
    g.achievement_status === 'NOT_STARTED'
  );
  
  // キャリアプランAPIと同じ計算ロジックを使用
  // 全目標のprogress_rateの平均を計算（キャンセル・延期も含む）
  let totalProgress = 0;
  
  goals.forEach((goal: any) => {
    // Prisma Decimal型の変換処理
    let progressValue = 0;
    if (goal.progress_rate !== null && goal.progress_rate !== undefined) {
      // Decimalオブジェクトの場合、toString()で文字列に変換
      progressValue = typeof goal.progress_rate === 'object' 
        ? parseFloat(goal.progress_rate.toString()) 
        : Number(goal.progress_rate);
    }
    totalProgress += progressValue;
  });
  
  // キャリアプランと同じ計算：全目標のprogress_rateの平均
  const overallProgress = goals.length > 0 
    ? totalProgress / goals.length 
    : 0;
  
  console.log('[getGoalSummary] 総進捗:', totalProgress, '目標数:', goals.length, '平均:', Math.round(overallProgress) + '%');

  // 期限が近い目標（30日以内）
  const thirtyDaysFromNow = new Date();
  thirtyDaysFromNow.setDate(thirtyDaysFromNow.getDate() + 30);
  
  const upcomingDeadlines = currentGoals
    .filter((g: any) => g.target_date && g.target_date <= thirtyDaysFromNow)
    .slice(0, 5)
    .map((goal: any) => ({
      goal_id: goal.goal_id,
      goal_title: goal.goal_title || '',
      deadline: goal.target_date!,
      progress: typeof goal.progress_rate === 'object'
        ? parseFloat(goal.progress_rate.toString())
        : Number(goal.progress_rate || goal.achievement_rate || 0)
    }));

  // 最近の達成（最新5件）
  const recentAchievements = completedGoals
    .slice(0, 5)
    .map((goal: any) => ({
      goal_id: goal.goal_id,
      goal_title: goal.goal_title || '',
      achieved_at: goal.completion_date || goal.updated_at
    }));

  // 進捗トレンド（仮データ）
  const progressTrend = generateProgressTrend();

  return {
    total_goals: goals.length,
    current_goals: currentGoals.length,
    completed_goals: completedGoals.length,
    overall_progress: Math.round(overallProgress),
    upcoming_deadlines: upcomingDeadlines,
    recent_achievements: recentAchievements,
    progress_trend: progressTrend
  };
}

// 資格サマリー取得
async function getCertificationSummary(userId: string, tenantId: string) {
  // PDUテーブルから資格取得済みのデータを取得
  const userCertifications = await prisma.pDU.findMany({
    where: {
      employee_id: userId,
      activity_type: 'certification',
      approval_status: 'approved',
      is_deleted: false
    },
    orderBy: {
      activity_date: 'desc'
    }
  });

  // 推奨資格の取得（参考情報として）
  const recommendedCertifications = await prisma.certification.findMany({
    where: {
      is_recommended: true,
      is_deleted: false
    },
    orderBy: {
      certification_name: 'asc'
    },
    take: 5
  });

  // 有効な資格をカウント（現在は全て有効とみなす）
  // 将来的には資格マスタと連携して有効期限を管理
  const activeCertifications = userCertifications;

  // 期限切れが近い資格（現在は空配列を返す）
  // 将来的には資格マスタの有効期限情報と連携
  const expiringSoon: Array<{
    certification_id: string;
    certification_name: string;
    expiry_date: Date;
  }> = [];

  // 最近取得した資格（最新5件）
  const recentCertifications = userCertifications.slice(0, 5).map(cert => ({
    certification_id: cert.pdu_id || cert.certificate_number || '',
    certification_name: cert.activity_name || '',
    acquired_date: cert.activity_date || new Date()
  }));

  return {
    total_certifications: userCertifications.length,
    active_certifications: activeCertifications.length,
    expiring_soon: expiringSoon,
    recent_certifications: recentCertifications
  };
}

// 作業実績サマリー取得
async function getWorkSummary(userId: string, tenantId: string) {
  // 今月の作業実績を取得
  const startOfMonth = new Date();
  startOfMonth.setDate(1);
  startOfMonth.setHours(0, 0, 0, 0);

  const workRecords = await prisma.projectRecord.findMany({
    where: {
      employee_id: userId,
      start_date: {
        gte: startOfMonth
      },
      is_deleted: false
    },
    orderBy: {
      start_date: 'desc'
    }
  });

  // 月間時間集計
  const monthlyHoursByCategory = new Map<string, number>();
  let totalMonthlyHours = 0;

  workRecords.forEach((record: any) => {
    const hours = 8; // TODO: 実際の作業時間を計算
    totalMonthlyHours += hours;
    
    const category = record.project_type || 'その他';
    monthlyHoursByCategory.set(
      category,
      (monthlyHoursByCategory.get(category) || 0) + hours
    );
  });

  // 最近のプロジェクト（最新5件）
  const projectMap = new Map();
  workRecords.forEach((record: any) => {
    if (!projectMap.has(record.id)) {
      projectMap.set(record.id, {
        project_id: record.id,
        project_name: record.project_name || '',
        role: record.role || '',
        period: `${record.start_date?.toLocaleDateString()} - ${record.end_date?.toLocaleDateString() || '継続中'}`,
        skills_used: []
      });
    }
  });
  
  const recentProjects = Array.from(projectMap.values()).slice(0, 5);

  // スキル利用状況（仮データ）
  const skillUtilization = [
    { skill_name: 'JavaScript', hours: 40, percentage: 25 },
    { skill_name: 'TypeScript', hours: 32, percentage: 20 },
    { skill_name: 'React', hours: 24, percentage: 15 },
    { skill_name: 'Node.js', hours: 16, percentage: 10 },
    { skill_name: 'その他', hours: 48, percentage: 30 }
  ];

  return {
    monthly_hours: {
      total: totalMonthlyHours,
      by_category: Array.from(monthlyHoursByCategory.entries()).map(([category, hours]) => ({
        category,
        hours
      }))
    },
    recent_projects: recentProjects,
    skill_utilization: skillUtilization
  };
}

// 通知取得
async function getNotifications(userId: string, tenantId: string) {
  const notifications = await prisma.notification.findMany({
    where: {
      recipient_id: userId,
      is_deleted: false
    },
    orderBy: {
      created_at: 'desc'
    },
    take: 10
  });

  return notifications.map((notif: any) => ({
    notification_id: notif.id,
    type: (notif.type || 'info') as 'info' | 'warning' | 'success' | 'error',
    title: notif.title || '',
    message: notif.message || '',
    created_at: notif.created_at,
    is_read: notif.is_read || false,
    priority: (notif.priority || 'medium') as 'low' | 'medium' | 'high',
    action_url: notif.action_url || undefined
  }));
}

// タスク取得
async function getTasks(userId: string, tenantId: string) {
  // タスクモデルが存在しないため、空配列を返す
  const tasks: any[] = [];
  /*
  const tasks = await prisma.task.findMany({
    where: {
      assignee_id: userId,
      status: {
        not: 'completed'
      },
      is_deleted: false
    },
    orderBy: [
      { priority: 'desc' },
      { due_date: 'asc' }
    ],
    take: 10
  });
  */

  return tasks.map((task: any) => ({
    task_id: task.id,
    title: task.title || '',
    description: task.description || '',
    type: task.type || '',
    priority: (task.priority || 'medium') as 'low' | 'medium' | 'high',
    due_date: task.due_date || undefined,
    status: (task.status || 'pending') as 'pending' | 'in_progress' | 'completed',
    action_url: `/tasks/${task.id}`
  }));
}

// チームサマリー取得（管理者用）
async function getTeamSummary(userId: string, tenantId: string) {
  // チームメンバーを取得（モデルが存在しないため空配列）
  const teamMembers: any[] = [];
  /*
  const teamMembers = await prisma.teamMember.findMany({
    where: {
      team: {
        manager_id: userId,
        is_deleted: false
      },
      is_deleted: false
    },
    include: {
      employee: true
    }
  });
  */

  // スキルギャップ分析（仮データ）
  const skillGaps = [
    { skill_name: 'AWS', required_level: '◎', current_level: '○', gap: 1 },
    { skill_name: 'Docker', required_level: '○', current_level: '△', gap: 1 },
    { skill_name: 'Kubernetes', required_level: '○', current_level: '×', gap: 2 }
  ];

  // トップパフォーマー（仮データ）
  const topPerformers = teamMembers.slice(0, 3).map((member: any) => ({
    user_id: member.employee_id,
    name: member.employee?.name || '',
    achievement_rate: Math.floor(Math.random() * 30) + 70
  }));

  return {
    team_members: teamMembers.length,
    team_skill_coverage: 75, // 仮の値
    skill_gaps: skillGaps,
    top_performers: topPerformers
  };
}

// ヘルパー関数
function isManagerPosition(positionId: string): boolean {
  // 管理職判定ロジック（実際の要件に応じて調整）
  return ['MGR', 'DIR', 'GM'].includes(positionId);
}

function getLevelLabel(level: number | null): string {
  switch (level) {
    case 0: return '×';
    case 1: return '△';
    case 2: return '○';
    case 3: return '◎';
    default: return '×';
  }
}

function generateGrowthTrend() {
  // 過去6ヶ月の成長トレンド（仮データ）
  const months = ['7月', '8月', '9月', '10月', '11月', '12月'];
  return months.map(month => ({
    month,
    score: Math.floor(Math.random() * 20) + 60
  }));
}

function generateProgressTrend() {
  // 過去6ヶ月の進捗トレンド（仮データ）
  const months = ['7月', '8月', '9月', '10月', '11月', '12月'];
  return months.map(month => ({
    month,
    progress: Math.floor(Math.random() * 30) + 50
  }));
}

function generateAnalytics(skillData: any, goalData: any) {
  // アナリティクスデータ生成
  return {
    skill_growth_chart: {
      labels: ['7月', '8月', '9月', '10月', '11月', '12月'],
      datasets: [
        {
          label: 'スキルスコア',
          data: [65, 68, 70, 72, 75, 78]
        }
      ]
    },
    goal_progress_chart: {
      labels: ['7月', '8月', '9月', '10月', '11月', '12月'],
      datasets: [
        {
          label: '目標達成率',
          data: [50, 55, 60, 65, 70, 75]
        }
      ]
    },
    skill_distribution: {
      labels: ['フロントエンド', 'バックエンド', 'インフラ', 'その他'],
      data: [8, 6, 4, 6]
    }
  };
}

function generateRecommendations(skillData: any, goalData: any, certificationData: any) {
  // 推奨事項生成
  const recommendations = [];

  // スキル関連の推奨
  if (skillData.skills_by_level.none > 5) {
    recommendations.push({
      type: 'skill' as const,
      title: '未習得スキルの学習',
      description: `${skillData.skills_by_level.none}個の未習得スキルがあります。優先度の高いものから学習を開始しましょう。`,
      priority: 'high' as const,
      action_label: 'スキル管理へ',
      action_url: '/skills'
    });
  }

  // 目標関連の推奨
  if (goalData.current_goals === 0) {
    recommendations.push({
      type: 'goal' as const,
      title: '目標の設定',
      description: '現在設定されている目標がありません。キャリア目標を設定しましょう。',
      priority: 'medium' as const,
      action_label: '目標設定へ',
      action_url: '/career'
    });
  }

  // 資格関連の推奨
  if (certificationData.expiring_soon.length > 0) {
    recommendations.push({
      type: 'certification' as const,
      title: '資格の更新',
      description: `${certificationData.expiring_soon.length}個の資格が期限切れ間近です。更新手続きを確認してください。`,
      priority: 'high' as const,
      action_label: '資格管理へ',
      action_url: '/certifications'
    });
  }

  // 研修関連の推奨
  recommendations.push({
    type: 'training' as const,
    title: '推奨研修',
    description: 'あなたのスキルセットに基づいて、React Advancedコースの受講をお勧めします。',
    priority: 'low' as const,
    action_label: '研修一覧へ',
    action_url: '/trainings'
  });

  return recommendations;
}