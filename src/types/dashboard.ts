// ダッシュボード関連の型定義

// ユーザー情報
export interface DashboardUserInfo {
  user_id: string;
  employee_id: string;
  name: string;
  email: string;
  department_id: string;
  department_name: string;
  position_id: string;
  position_name: string;
  avatar_url?: string | undefined;
  last_login?: Date | undefined;
}

// スキルサマリー
export interface DashboardSkillSummary {
  total_skills: number;
  skills_by_level: {
    none: number;      // ×
    basic: number;     // △
    intermediate: number; // ○
    advanced: number;  // ◎
  };
  skills_by_category: Array<{
    category_id: string;
    category_name: string;
    count: number;
    average_level: number;
  }>;
  recent_updates: Array<{
    skill_id: string;
    skill_name: string;
    old_level: string;
    new_level: string;
    updated_at: Date;
  }>;
  top_skills: Array<{
    skill_id: string;
    skill_name: string;
    level: string;
    category_name: string;
  }>;
  growth_trend: Array<{
    month: string;
    score: number;
  }>;
}

// 目標サマリー
export interface DashboardGoalSummary {
  total_goals: number;
  current_goals: number;
  completed_goals: number;
  overall_progress: number;
  upcoming_deadlines: Array<{
    goal_id: string;
    goal_title: string;
    deadline: Date;
    progress: number;
  }>;
  recent_achievements: Array<{
    goal_id: string;
    goal_title: string;
    achieved_at: Date;
  }>;
  progress_trend: Array<{
    month: string;
    progress: number;
  }>;
}

// 資格サマリー
export interface DashboardCertificationSummary {
  total_certifications: number;
  active_certifications: number;
  expiring_soon: Array<{
    certification_id: string;
    certification_name: string;
    expiry_date: Date;
  }>;
  recent_certifications: Array<{
    certification_id: string;
    certification_name: string;
    acquired_date: Date;
  }>;
}

// 作業実績サマリー
export interface DashboardWorkSummary {
  monthly_hours: {
    total: number;
    by_category: Array<{
      category: string;
      hours: number;
    }>;
  };
  recent_projects: Array<{
    project_id: string;
    project_name: string;
    role: string;
    period: string;
    skills_used: string[];
  }>;
  skill_utilization: Array<{
    skill_name: string;
    hours: number;
    percentage: number;
  }>;
}

// チームサマリー（管理者用）
export interface DashboardTeamSummary {
  team_members: number;
  team_skill_coverage: number;
  skill_gaps: Array<{
    skill_name: string;
    required_level: string;
    current_level: string;
    gap: number;
  }>;
  top_performers: Array<{
    user_id: string;
    name: string;
    achievement_rate: number;
  }>;
}

// 通知
export interface DashboardNotification {
  notification_id: string;
  type: 'info' | 'warning' | 'success' | 'error';
  title: string;
  message: string;
  created_at: Date;
  is_read: boolean;
  priority: 'low' | 'medium' | 'high';
  action_url?: string;
}

// アナリティクス
export interface DashboardAnalytics {
  skill_growth_chart: {
    labels: string[];
    datasets: Array<{
      label: string;
      data: number[];
    }>;
  };
  goal_progress_chart: {
    labels: string[];
    datasets: Array<{
      label: string;
      data: number[];
    }>;
  };
  skill_distribution: {
    labels: string[];
    data: number[];
  };
}

// 推奨事項
export interface DashboardRecommendation {
  type: 'skill' | 'certification' | 'training' | 'goal';
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  action_label: string;
  action_url: string;
}

// タスク
export interface DashboardTask {
  task_id: string;
  title: string;
  description: string;
  type: string;
  priority: 'low' | 'medium' | 'high';
  due_date?: Date;
  status: 'pending' | 'in_progress' | 'completed';
  action_url: string;
}

// ダッシュボード設定
export interface DashboardSettings {
  user_id: string;
  layout: 'default' | 'compact';
  visible_sections: string[];
  section_order: string[];
  refresh_interval: number; // 秒単位
  theme: 'light' | 'dark' | 'auto';
  chart_type: 'line' | 'bar' | 'radar';
  notifications_enabled: boolean;
}

// メインダッシュボードデータ
export interface DashboardData {
  user_info: DashboardUserInfo;
  skill_summary: DashboardSkillSummary;
  goal_summary: DashboardGoalSummary;
  certification_summary: DashboardCertificationSummary;
  work_summary: DashboardWorkSummary;
  team_summary?: DashboardTeamSummary; // 管理者のみ
  notifications: DashboardNotification[];
  tasks: DashboardTask[];
  analytics: DashboardAnalytics;
  recommendations: DashboardRecommendation[];
  last_updated: Date;
}

// APIレスポンス
export interface DashboardResponse {
  success: boolean;
  data?: DashboardData;
  error?: string;
}

export interface DashboardSectionResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface DashboardSettingsResponse {
  success: boolean;
  data?: DashboardSettings;
  error?: string;
}