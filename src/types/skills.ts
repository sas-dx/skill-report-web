/**
 * 要求仕様ID: SKL.1-HIER.1, SKL.1-EVAL.1
 * 対応設計書: docs/design/screens/specs/画面定義書_SCR_SKL_Skill_スキル管理画面.md
 * 実装内容: スキル管理関連の型定義
 */

// スキル階層構造
export interface SkillHierarchy {
  id: string;
  name: string;
  category: string;
  subcategory?: string | undefined;
  parentId?: string;
  children?: SkillHierarchy[];
  level: number; // 階層レベル（1: カテゴリ, 2: サブカテゴリ, 3: スキル項目）
  description?: string;
}

// ユーザースキル情報
export interface UserSkill {
  id: string;
  skillId: string;
  userId: string;
  skillName: string;
  category: string;
  subcategory?: string | undefined;
  level: 1 | 2 | 3 | 4; // ×/△/○/◎
  acquiredDate?: string;
  experienceYears?: number;
  lastUsed?: string;
  remarks?: string;
  createdAt: string;
  updatedAt: string;
}

// スキルマスタ情報
export interface SkillMaster {
  id: string;
  name: string;
  category: string;
  subcategory?: string;
  description?: string;
  isActive: boolean;
  sortOrder: number;
}

// 資格情報
export interface Certification {
  id: string;
  userId: string;
  certificationName: string;
  organizationName?: string;
  acquiredDate: string;
  expiryDate?: string;
  score?: string;
  credentialId?: string;
  relatedSkills?: string[];
  remarks?: string;
  createdAt: string;
  updatedAt: string;
}

// 資格マスタ
export interface CertificationMaster {
  id: string;
  name: string;
  organizationName: string;
  category: string;
  validityPeriod?: number; // 有効期間（月）
  isActive: boolean;
  description?: string;
}

// スキル検索結果
export interface SkillSearchResult {
  skills: SkillMaster[];
  total: number;
  page: number;
  limit: number;
}

// スキル評価レベル
export type SkillLevel = 1 | 2 | 3 | 4;

export const SKILL_LEVELS = {
  1: { symbol: '×', label: '未経験', color: 'text-red-500 bg-red-50' },
  2: { symbol: '△', label: '基礎レベル', color: 'text-yellow-500 bg-yellow-50' },
  3: { symbol: '○', label: '実務レベル', color: 'text-blue-500 bg-blue-50' },
  4: { symbol: '◎', label: 'エキスパート', color: 'text-green-500 bg-green-50' }
} as const;

// スキルカテゴリ
export const SKILL_CATEGORIES = [
  '技術スキル',
  '開発スキル', 
  '業務スキル',
  '管理スキル',
  '生産スキル'
] as const;

export type SkillCategory = typeof SKILL_CATEGORIES[number];

// API レスポンス型
export interface SkillApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  timestamp: string;
}

export interface SkillApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: any;
  };
  timestamp: string;
}

// フォーム用型
export interface SkillFormData {
  skillId: string;
  level: SkillLevel;
  acquiredDate?: string | undefined;
  experienceYears?: number | undefined;
  lastUsed?: string | undefined;
  remarks?: string | undefined;
}

// スキル検索フィルタ
export interface SkillSearchFilters {
  keyword?: string;
  categoryId?: string;
  subcategoryId?: string;
  minLevel?: number;
  maxLevel?: number;
  hasExperience?: boolean;
  isActive?: boolean;
}

// スキルカテゴリ（検索用）
export interface SkillCategoryWithId {
  id: string;
  name: string;
  subcategories?: SkillCategoryWithId[];
}

export interface CertificationFormData {
  certificationName: string;
  organizationName?: string;
  acquiredDate: string;
  expiryDate?: string;
  score?: string;
  credentialId?: string;
  relatedSkills?: string[];
  remarks?: string;
}

// 検索・フィルタ用型
export interface SkillSearchParams {
  keyword?: string;
  category?: string;
  subcategory?: string;
  level?: SkillLevel;
  minLevel?: number;
  maxLevel?: number;
  hasExperience?: boolean;
  isActive?: boolean;
  page?: number;
  limit?: number;
}

export interface SkillFilterOptions {
  categories: string[];
  subcategories: string[];
  levels: SkillLevel[];
  experienceRange: {
    min: number;
    max: number;
  };
}
