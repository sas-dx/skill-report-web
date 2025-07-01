/**
 * 要求仕様ID: CAR.1-PLAN.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_CAR_Plan_キャリアプラン画面.md
 * 実装内容: キャリア関連の型定義
 */

// ============================================================================
// API レスポンス型定義
// ============================================================================

/**
 * API-700: キャリア初期データ取得APIのレスポンス型
 */
export interface CareerInitResponse {
  success: boolean;
  data?: {
    career_goal: CareerGoalData;
    skill_categories: SkillCategory[];
    positions: Position[];
  };
  error?: {
    code: string;
    message: string;
    details?: string;
  };
  timestamp: string;
}

/**
 * キャリア目標データ（API-700レスポンス用）
 */
export interface CareerGoalData {
  id?: string;
  target_position: string;
  target_date: string;
  target_description: string;
  current_level: string;
  target_level: string;
  progress_percentage: number;
  plan_status?: 'ACTIVE' | 'INACTIVE' | 'COMPLETED';
  last_review_date?: string | null;
  next_review_date?: string | null;
}

/**
 * スキルカテゴリ
 */
export interface SkillCategory {
  id: string;
  name: string;
  short_name: string;
  type: string;
  parent_id: string | null;
  level: number;
  description: string;
  icon_url: string | null;
  color_code: string;
}

/**
 * ポジション
 */
export interface Position {
  id: string;
  name: string;
  short_name: string;
  level: number;
  rank: number;
  category: string;
  authority_level: number;
  is_management: boolean;
  is_executive: boolean;
  description: string;
}

// ============================================================================
// API-701: キャリア目標更新API関連型定義
// ============================================================================

/**
 * 関連スキル
 */
export interface RelatedSkill {
  skill_id: string;
  target_level: number;
}

/**
 * アクションプラン
 */
export interface ActionPlan {
  action_id?: string;
  title: string;
  description?: string;
  due_date: string;
  status: 'not_started' | 'in_progress' | 'completed';
  completed_date?: string;
}

/**
 * フィードバック
 */
export interface Feedback {
  feedback_id?: string;
  comment: string;
}

/**
 * キャリア目標（API更新用）
 */
export interface CareerGoalApiData {
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

/**
 * キャリア目標更新リクエスト
 */
export interface CareerGoalUpdateRequest {
  year: number;
  operation_type: 'add' | 'update' | 'delete';
  career_goals: CareerGoalApiData[];
}

/**
 * 更新された目標
 */
export interface UpdatedGoal {
  goal_id: string;
  goal_type: string;
  title: string;
  status: string;
  updated_at: string;
}

/**
 * キャリア目標更新レスポンス
 */
export interface CareerGoalUpdateResponse {
  user_id: string;
  year: number;
  updated_goals: UpdatedGoal[];
  operation_type: string;
  operation_result: string;
  last_updated: string;
  last_updated_by: string;
}

// ============================================================================
// フロントエンド用型定義
// ============================================================================

/**
 * キャリア目標ステータス
 */
export type CareerGoalStatus = 'not_started' | 'in_progress' | 'completed' | 'postponed' | 'cancelled';

/**
 * キャリア目標優先度
 */
export type CareerGoalPriority = 1 | 2 | 3; // 1: high, 2: medium, 3: low

/**
 * フロントエンド用キャリア目標
 */
export interface CareerGoal {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  status: CareerGoalStatus;
  priority: CareerGoalPriority;
  target_date?: string;
  progress_percentage: number;
  created_at: string;
  updated_at: string;
}

/**
 * キャリア目標フォーム
 */
export interface CareerGoalForm {
  position: string;
  targetYear: string;
  description: string;
}

/**
 * アクションプランアイテム（フロントエンド用）
 */
export interface ActionPlanItem {
  id: string;
  item: string;
  skill: string;
  deadline: string;
  status: '未着手' | '進行中' | '完了';
  priority?: number;
  description?: string;
}

/**
 * スキルギャップデータ
 */
export interface SkillGapData {
  label: string;
  current: number;
  target: number;
  category?: string;
  skill_id?: string;
}

/**
 * 進捗データ
 */
export interface ProgressData {
  overall_progress: number;
  skill_progress: SkillProgress[];
  action_plan_progress: ActionPlanProgress;
  last_updated: string;
}

/**
 * スキル進捗
 */
export interface SkillProgress {
  skill_name: string;
  current_level: number;
  target_level: number;
  progress_percentage: number;
  category: string;
}

/**
 * アクションプラン進捗
 */
export interface ActionPlanProgress {
  total_count: number;
  completed_count: number;
  in_progress_count: number;
  not_started_count: number;
  completion_rate: number;
}

/**
 * 上司コメント
 */
export interface SupervisorComment {
  id?: string;
  comment: string;
  supervisor_name: string;
  supervisor_id: string;
  created_at: string;
  updated_at: string;
}

// ============================================================================
// エラー型定義
// ============================================================================

/**
 * APIエラーレスポンス
 */
export interface ApiError {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}

/**
 * フォームエラー
 */
export interface FormError {
  field: string;
  message: string;
}

/**
 * バリデーションエラー
 */
export interface ValidationErrors {
  [key: string]: string;
}

// ============================================================================
// ユーティリティ型
// ============================================================================

/**
 * ローディング状態
 */
export interface LoadingState {
  isLoading: boolean;
  error: string | null;
}

/**
 * 操作状態
 */
export interface OperationState extends LoadingState {
  isSuccess: boolean;
}

/**
 * ページネーション
 */
export interface Pagination {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

/**
 * ソート設定
 */
export interface SortConfig {
  field: string;
  direction: 'asc' | 'desc';
}

/**
 * フィルター設定
 */
export interface FilterConfig {
  status?: string[];
  priority?: number[];
  category?: string[];
  dateRange?: {
    start: string;
    end: string;
  };
}
