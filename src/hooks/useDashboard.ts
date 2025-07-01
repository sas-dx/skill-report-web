/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/screens/specs/画面設計書_SCR-DASHBOARD_ダッシュボード画面.md
 * 実装内容: ダッシュボードデータ取得カスタムフック
 */

'use client';

import { useState, useEffect } from 'react';

export interface DashboardUser {
  employeeCode: string;
  fullName: string;
  email: string;
  departmentId: string | null;
  positionId: string | null;
}

export interface EmployeeProfile {
  employee_code: string;
  full_name: string;
  full_name_kana: string | null;
  email: string | null;
  phone: string | null;
  hire_date: Date | null;
  department_id: string | null;
  position_id: string | null;
  job_type_id: string | null;
  employment_status: string | null;
  employee_status: string | null;
}

export interface SkillSummary {
  levelCounts: {
    level1: number;
    level2: number;
    level3: number;
    level4: number;
    total: number;
  };
  recentSkills: Array<{
    skill_item_id: string | null;
    skill_level: number | null;
    updated_at: Date;
  }>;
  lastUpdated: Date | null;
}

export interface TrainingHistory {
  training_name: string | null;
  training_type: string | null;
  start_date: Date | null;
  end_date: Date | null;
  completion_rate: number | null;
  certificate_obtained: boolean | null;
  grade: string | null;
}

export interface GoalProgress {
  goal_title: string | null;
  goal_category: string | null;
  progress_rate: number | null;
  target_date: Date | null;
  achievement_status: string | null;
  priority_level: string | null;
}

export interface Notification {
  notification_id: string | null;
  title: string | null;
  message: string | null;
  notification_type: string | null;
  priority_level: string | null;
  created_at: Date;
  action_url: string | null;
  action_label: string | null;
}

export interface DashboardData {
  user: DashboardUser;
  profile: EmployeeProfile | null;
  skillSummary: SkillSummary;
  recentTraining: TrainingHistory[];
  goalProgress: GoalProgress[];
  notifications: Notification[];
  lastUpdated: string;
}

export interface UseDashboardReturn {
  data: DashboardData | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export function useDashboard(): UseDashboardReturn {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch('/api/dashboard', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include', // Cookieを含める
      });

      if (!response.ok) {
        if (response.status === 401) {
          throw new Error('認証が必要です。ログインしてください。');
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const result = await response.json();

      if (!result.success) {
        throw new Error(result.error?.message || 'データの取得に失敗しました');
      }

      // 日付文字列をDateオブジェクトに変換
      const processedData = {
        ...result.data,
        profile: result.data.profile ? {
          ...result.data.profile,
          hire_date: result.data.profile.hire_date ? new Date(result.data.profile.hire_date) : null,
        } : null,
        skillSummary: {
          ...result.data.skillSummary,
          recentSkills: result.data.skillSummary.recentSkills.map((skill: any) => ({
            ...skill,
            updated_at: new Date(skill.updated_at)
          })),
          lastUpdated: result.data.skillSummary.lastUpdated ? new Date(result.data.skillSummary.lastUpdated) : null,
        },
        recentTraining: result.data.recentTraining.map((training: any) => ({
          ...training,
          start_date: training.start_date ? new Date(training.start_date) : null,
          end_date: training.end_date ? new Date(training.end_date) : null,
        })),
        goalProgress: result.data.goalProgress.map((goal: any) => ({
          ...goal,
          target_date: goal.target_date ? new Date(goal.target_date) : null,
        })),
        notifications: result.data.notifications.map((notification: any) => ({
          ...notification,
          created_at: new Date(notification.created_at)
        }))
      };

      setData(processedData);
    } catch (err) {
      console.error('Dashboard data fetch error:', err);
      setError(err instanceof Error ? err.message : '不明なエラーが発生しました');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  return {
    data,
    loading,
    error,
    refetch: fetchDashboardData
  };
}

/**
 * スキルレベルの表示名を取得
 */
export function getSkillLevelName(level: number): string {
  switch (level) {
    case 1: return '基礎';
    case 2: return '応用';
    case 3: return '熟練';
    case 4: return '専門';
    default: return '不明';
  }
}

/**
 * 目標の優先度の表示名を取得
 */
export function getPriorityLevelName(priority: string): string {
  switch (priority) {
    case 'HIGH': return '高';
    case 'MEDIUM': return '中';
    case 'LOW': return '低';
    default: return '不明';
  }
}

/**
 * 達成状況の表示名を取得
 */
export function getAchievementStatusName(status: string): string {
  switch (status) {
    case 'IN_PROGRESS': return '進行中';
    case 'PENDING': return '保留中';
    case 'COMPLETED': return '完了';
    case 'CANCELLED': return 'キャンセル';
    default: return '不明';
  }
}

/**
 * 通知の優先度に応じたスタイルクラスを取得
 */
export function getNotificationPriorityClass(priority: string): string {
  switch (priority) {
    case 'HIGH': return 'bg-red-100 text-red-800 border-red-200';
    case 'MEDIUM': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
    case 'LOW': return 'bg-blue-100 text-blue-800 border-blue-200';
    default: return 'bg-gray-100 text-gray-800 border-gray-200';
  }
}
