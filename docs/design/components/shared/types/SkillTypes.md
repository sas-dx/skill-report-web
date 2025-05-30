# SkillTypes 型定義書

## 1. 基本情報

- **部品名**: SkillTypes
- **カテゴリ**: 共有型定義
- **責務**: スキル関連の型定義・インターフェース
- **依存関係**: なし（基盤型定義）
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 型定義一覧

### 2.1 基本型定義

```typescript
/**
 * スキルカテゴリの列挙型
 */
export type SkillCategory = 
  | 'プログラミング言語'
  | 'フレームワーク・ライブラリ'
  | 'データベース'
  | 'クラウド・インフラ'
  | 'ツール・その他';

/**
 * スキルレベルの列挙型
 */
export type SkillLevel = '初級' | '中級' | '上級' | 'エキスパート';

/**
 * スキルレベルの数値表現
 */
export type SkillLevelNumeric = 1 | 2 | 3 | 4;

/**
 * スキルの優先度
 */
export type SkillPriority = 'low' | 'medium' | 'high' | 'critical';

/**
 * スキルの状態
 */
export type SkillStatus = 'active' | 'inactive' | 'deprecated' | 'learning';
```

### 2.2 コアインターフェース

```typescript
/**
 * スキルアイテムの基本インターフェース
 */
export interface SkillItem {
  /** スキルの一意識別子 */
  id: string;
  
  /** スキルを所有するユーザーのID */
  userId: string;
  
  /** スキル名 */
  skillName: string;
  
  /** スキルカテゴリ */
  category: SkillCategory;
  
  /** スキルレベル */
  level: SkillLevel;
  
  /** 経験年数（小数点可） */
  experience: number;
  
  /** 最終使用日 */
  lastUsed: Date;
  
  /** 目標スキルフラグ */
  target: boolean;
  
  /** コメント・備考（オプション） */
  comments?: string;
  
  /** 関連資格のID配列（オプション） */
  certifications?: string[];
  
  /** 関連プロジェクトのID配列（オプション） */
  projects?: string[];
  
  /** 作成日時 */
  createdAt: Date;
  
  /** 更新日時 */
  updatedAt: Date;
  
  /** 削除日時（論理削除用、オプション） */
  deletedAt?: Date;
}

/**
 * スキル作成リクエストの型
 */
export interface CreateSkillRequest {
  /** スキル名 */
  skillName: string;
  
  /** スキルカテゴリ */
  category: SkillCategory;
  
  /** スキルレベル */
  level: SkillLevel;
  
  /** 経験年数 */
  experience: number;
  
  /** 最終使用日 */
  lastUsed: Date;
  
  /** 目標スキルフラグ */
  target: boolean;
  
  /** コメント・備考（オプション） */
  comments?: string;
  
  /** 関連資格のID配列（オプション） */
  certifications?: string[];
  
  /** 関連プロジェクトのID配列（オプション） */
  projects?: string[];
}

/**
 * スキル更新リクエストの型
 */
export interface UpdateSkillRequest extends Partial<CreateSkillRequest> {
  /** 下書き保存フラグ */
  isDraft?: boolean;
}

/**
 * スキル一括更新リクエストの型
 */
export interface BulkUpdateRequest {
  /** 更新対象のスキルID */
  skillId: string;
  
  /** 更新内容 */
  updates: UpdateSkillRequest;
}
```

### 2.3 フィルター・検索関連

```typescript
/**
 * スキル検索・フィルター条件
 */
export interface SkillFilters {
  /** カテゴリフィルター */
  category?: SkillCategory[];
  
  /** レベルフィルター */
  level?: SkillLevel[];
  
  /** 目標スキルフィルター */
  target?: boolean;
  
  /** 検索キーワード */
  search?: string;
  
  /** ソート項目 */
  sortBy?: SkillSortField;
  
  /** ソート順序 */
  sortOrder?: SortOrder;
  
  /** 取得件数制限 */
  limit?: number;
  
  /** オフセット */
  offset?: number;
  
  /** 経験年数の範囲フィルター */
  experienceRange?: {
    min?: number;
    max?: number;
  };
  
  /** 最終使用日の範囲フィルター */
  lastUsedRange?: {
    from?: Date;
    to?: Date;
  };
  
  /** 作成日の範囲フィルター */
  createdAtRange?: {
    from?: Date;
    to?: Date;
  };
}

/**
 * ソート可能なフィールド
 */
export type SkillSortField = 
  | 'skillName'
  | 'category'
  | 'level'
  | 'experience'
  | 'lastUsed'
  | 'createdAt'
  | 'updatedAt';

/**
 * ソート順序
 */
export type SortOrder = 'asc' | 'desc';

/**
 * ページネーション情報
 */
export interface PaginationInfo {
  /** 現在のページ番号 */
  page: number;
  
  /** 1ページあたりの件数 */
  limit: number;
  
  /** 総件数 */
  total: number;
  
  /** 総ページ数 */
  totalPages: number;
  
  /** 前のページが存在するか */
  hasPrevious: boolean;
  
  /** 次のページが存在するか */
  hasNext: boolean;
}

/**
 * ページネーション付きスキル一覧のレスポンス
 */
export interface PaginatedSkillsResponse {
  /** スキル一覧 */
  skills: SkillItem[];
  
  /** ページネーション情報 */
  pagination: PaginationInfo;
}
```

### 2.4 統計・分析関連

```typescript
/**
 * スキル統計情報
 */
export interface SkillStatistics {
  /** 総スキル数 */
  totalSkills: number;
  
  /** カテゴリ別スキル数 */
  skillsByCategory: Record<SkillCategory, number>;
  
  /** レベル別スキル数 */
  skillsByLevel: Record<SkillLevel, number>;
  
  /** 目標スキル数 */
  targetSkills: number;
  
  /** 平均経験年数 */
  averageExperience: number;
  
  /** 最近使用したスキル数（3ヶ月以内） */
  recentlyUsedSkills: number;
  
  /** 上位カテゴリ */
  topCategories: Array<{
    category: SkillCategory;
    count: number;
    percentage: number;
  }>;
  
  /** レベル分布（パーセンテージ） */
  levelDistribution: Array<{
    level: SkillLevel;
    count: number;
    percentage: number;
  }>;
  
  /** 経験年数分布 */
  experienceDistribution: Array<{
    range: string;
    count: number;
    percentage: number;
  }>;
  
  /** 月別スキル追加数（過去12ヶ月） */
  monthlySkillAdditions: Array<{
    month: string;
    count: number;
  }>;
}

/**
 * スキル成長トレンド
 */
export interface SkillGrowthTrend {
  /** スキルID */
  skillId: string;
  
  /** スキル名 */
  skillName: string;
  
  /** 成長履歴 */
  growthHistory: Array<{
    date: Date;
    level: SkillLevel;
    experience: number;
    notes?: string;
  }>;
  
  /** 成長率（月あたり） */
  growthRate: number;
  
  /** 予測される次のレベル到達日 */
  predictedNextLevelDate?: Date;
}

/**
 * スキル比較データ
 */
export interface SkillComparison {
  /** 比較対象のスキル */
  skills: SkillItem[];
  
  /** 比較メトリクス */
  metrics: {
    /** 平均経験年数 */
    averageExperience: number;
    
    /** 最も高いレベル */
    highestLevel: SkillLevel;
    
    /** 最も低いレベル */
    lowestLevel: SkillLevel;
    
    /** 最近使用したスキル */
    mostRecentlyUsed: SkillItem;
    
    /** 最も古いスキル */
    oldestSkill: SkillItem;
  };
}
```

### 2.5 インポート・エクスポート関連

```typescript
/**
 * エクスポート形式
 */
export type ExportFormat = 'json' | 'csv' | 'xlsx' | 'pdf';

/**
 * インポート形式
 */
export type ImportFormat = 'json' | 'csv' | 'xlsx';

/**
 * エクスポート設定
 */
export interface ExportOptions {
  /** エクスポート形式 */
  format: ExportFormat;
  
  /** 含めるフィールド */
  includeFields?: (keyof SkillItem)[];
  
  /** フィルター条件 */
  filters?: SkillFilters;
  
  /** ファイル名（拡張子なし） */
  filename?: string;
  
  /** 追加メタデータを含めるか */
  includeMetadata?: boolean;
}

/**
 * インポート結果
 */
export interface ImportResult {
  /** インポート成功フラグ */
  success: boolean;
  
  /** インポート成功件数 */
  imported: number;
  
  /** インポート失敗件数 */
  failed: number;
  
  /** スキップ件数 */
  skipped: number;
  
  /** エラー詳細 */
  errors: ImportError[];
  
  /** 警告メッセージ */
  warnings: ImportWarning[];
  
  /** インポートされたスキルのID一覧 */
  importedSkillIds: string[];
}

/**
 * インポートエラー
 */
export interface ImportError {
  /** 行番号 */
  row: number;
  
  /** エラーが発生したフィールド */
  field: string;
  
  /** エラーメッセージ */
  message: string;
  
  /** エラーコード */
  code: string;
  
  /** 元の値 */
  originalValue?: any;
}

/**
 * インポート警告
 */
export interface ImportWarning {
  /** 行番号 */
  row: number;
  
  /** 警告メッセージ */
  message: string;
  
  /** 警告コード */
  code: string;
}
```

### 2.6 バリデーション関連

```typescript
/**
 * バリデーション結果
 */
export interface ValidationResult {
  /** バリデーション成功フラグ */
  isValid: boolean;
  
  /** エラー一覧 */
  errors: ValidationError[];
  
  /** 警告一覧 */
  warnings: ValidationWarning[];
}

/**
 * バリデーションエラー
 */
export interface ValidationError {
  /** エラーが発生したフィールド */
  field: string;
  
  /** エラーメッセージ */
  message: string;
  
  /** エラーコード */
  code: string;
  
  /** エラーの詳細情報 */
  details?: Record<string, any>;
}

/**
 * バリデーション警告
 */
export interface ValidationWarning {
  /** 警告が発生したフィールド */
  field: string;
  
  /** 警告メッセージ */
  message: string;
  
  /** 警告コード */
  code: string;
}

/**
 * スキル名の重複チェック結果
 */
export interface DuplicateCheckResult {
  /** 重複しているか */
  isDuplicate: boolean;
  
  /** 重複している既存スキル */
  existingSkill?: SkillItem;
  
  /** 類似スキル一覧 */
  similarSkills: Array<{
    skill: SkillItem;
    similarity: number;
  }>;
}
```

### 2.7 UI関連型

```typescript
/**
 * スキルフォームの状態
 */
export interface SkillFormState {
  /** フォームデータ */
  data: Partial<CreateSkillRequest>;
  
  /** バリデーションエラー */
  errors: Record<string, string>;
  
  /** フォームの変更フラグ */
  isDirty: boolean;
  
  /** フォームの有効性 */
  isValid: boolean;
  
  /** 送信中フラグ */
  isSubmitting: boolean;
  
  /** 自動保存中フラグ */
  isAutoSaving: boolean;
}

/**
 * スキル表示設定
 */
export interface SkillDisplayOptions {
  /** 表示形式 */
  viewMode: 'list' | 'grid' | 'card';
  
  /** 表示するフィールド */
  visibleFields: (keyof SkillItem)[];
  
  /** グループ化設定 */
  groupBy?: SkillSortField;
  
  /** 色分け設定 */
  colorBy?: 'category' | 'level' | 'target' | 'none';
  
  /** 密度設定 */
  density: 'compact' | 'comfortable' | 'spacious';
}

/**
 * スキル選択状態
 */
export interface SkillSelectionState {
  /** 選択されたスキルのID一覧 */
  selectedSkillIds: string[];
  
  /** 全選択フラグ */
  isAllSelected: boolean;
  
  /** 部分選択フラグ */
  isPartiallySelected: boolean;
  
  /** 選択可能フラグ */
  isSelectable: boolean;
}
```

### 2.8 API関連型

```typescript
/**
 * API レスポンスの基本型
 */
export interface ApiResponse<T = any> {
  /** 成功フラグ */
  success: boolean;
  
  /** レスポンスデータ */
  data: T;
  
  /** メッセージ */
  message: string;
  
  /** エラー情報（失敗時） */
  error?: {
    code: string;
    message: string;
    details?: any;
  };
  
  /** メタデータ */
  meta?: {
    timestamp: string;
    requestId: string;
    version: string;
  };
}

/**
 * スキル一覧取得のAPIレスポンス
 */
export type GetSkillsResponse = ApiResponse<PaginatedSkillsResponse>;

/**
 * スキル作成のAPIレスポンス
 */
export type CreateSkillResponse = ApiResponse<SkillItem>;

/**
 * スキル更新のAPIレスポンス
 */
export type UpdateSkillResponse = ApiResponse<SkillItem>;

/**
 * スキル削除のAPIレスポンス
 */
export type DeleteSkillResponse = ApiResponse<null>;

/**
 * スキル統計のAPIレスポンス
 */
export type GetSkillStatisticsResponse = ApiResponse<SkillStatistics>;

/**
 * スキルエクスポートのAPIレスポンス
 */
export type ExportSkillsResponse = ApiResponse<{
  downloadUrl: string;
  filename: string;
  size: number;
  expiresAt: string;
}>;

/**
 * スキルインポートのAPIレスポンス
 */
export type ImportSkillsResponse = ApiResponse<ImportResult>;
```

---

## 3. 定数定義

### 3.1 スキル関連定数

```typescript
/**
 * スキルカテゴリ一覧
 */
export const SKILL_CATEGORIES: SkillCategory[] = [
  'プログラミング言語',
  'フレームワーク・ライブラリ',
  'データベース',
  'クラウド・インフラ',
  'ツール・その他'
];

/**
 * スキルレベル一覧
 */
export const SKILL_LEVELS: SkillLevel[] = [
  '初級',
  '中級', 
  '上級',
  'エキスパート'
];

/**
 * スキルレベルの数値マッピング
 */
export const SKILL_LEVEL_NUMERIC_MAP: Record<SkillLevel, SkillLevelNumeric> = {
  '初級': 1,
  '中級': 2,
  '上級': 3,
  'エキスパート': 4
};

/**
 * スキルレベルの色マッピング
 */
export const SKILL_LEVEL_COLOR_MAP: Record<SkillLevel, string> = {
  '初級': '#10B981',      // green-500
  '中級': '#3B82F6',      // blue-500
  '上級': '#F59E0B',      // amber-500
  'エキスパート': '#EF4444' // red-500
};

/**
 * スキルカテゴリの色マッピング
 */
export const SKILL_CATEGORY_COLOR_MAP: Record<SkillCategory, string> = {
  'プログラミング言語': '#8B5CF6',           // violet-500
  'フレームワーク・ライブラリ': '#06B6D4',    // cyan-500
  'データベース': '#84CC16',                // lime-500
  'クラウド・インフラ': '#F97316',          // orange-500
  'ツール・その他': '#6B7280'              // gray-500
};
```

### 3.2 バリデーション定数

```typescript
/**
 * スキル名の最大文字数
 */
export const SKILL_NAME_MAX_LENGTH = 100;

/**
 * コメントの最大文字数
 */
export const SKILL_COMMENT_MAX_LENGTH = 500;

/**
 * 経験年数の最大値
 */
export const SKILL_EXPERIENCE_MAX = 50;

/**
 * 一括操作の最大件数
 */
export const BULK_OPERATION_MAX_COUNT = 100;

/**
 * インポート可能な最大ファイルサイズ（MB）
 */
export const IMPORT_MAX_FILE_SIZE_MB = 10;

/**
 * インポート可能な最大レコード数
 */
export const IMPORT_MAX_RECORDS = 1000;
```

### 3.3 UI関連定数

```typescript
/**
 * ページネーションのデフォルト設定
 */
export const DEFAULT_PAGINATION = {
  page: 1,
  limit: 20,
  maxLimit: 100
};

/**
 * 検索のデバウンス時間（ミリ秒）
 */
export const SEARCH_DEBOUNCE_MS = 300;

/**
 * 自動保存の間隔（ミリ秒）
 */
export const AUTO_SAVE_INTERVAL_MS = 2000;

/**
 * キャッシュの有効期限（秒）
 */
export const CACHE_TTL = {
  SKILLS: 300,      // 5分
  STATISTICS: 600,  // 10分
  FILTERS: 1800     // 30分
};
```

---

## 4. ユーティリティ型

### 4.1 型変換ユーティリティ

```typescript
/**
 * スキルレベルを数値に変換
 */
export type SkillLevelToNumeric<T extends SkillLevel> = 
  T extends '初級' ? 1 :
  T extends '中級' ? 2 :
  T extends '上級' ? 3 :
  T extends 'エキスパート' ? 4 :
  never;

/**
 * 数値をスキルレベルに変換
 */
export type NumericToSkillLevel<T extends SkillLevelNumeric> = 
  T extends 1 ? '初級' :
  T extends 2 ? '中級' :
  T extends 3 ? '上級' :
  T extends 4 ? 'エキスパート' :
  never;

/**
 * スキルアイテムから特定フィールドのみを抽出
 */
export type PickSkillFields<T extends keyof SkillItem> = Pick<SkillItem, T>;

/**
 * スキルアイテムから特定フィールドを除外
 */
export type OmitSkillFields<T extends keyof SkillItem> = Omit<SkillItem, T>;

/**
 * スキルアイテムの部分型（すべてオプション）
 */
export type PartialSkillItem = Partial<SkillItem>;

/**
 * スキルアイテムの必須フィールドのみ
 */
export type RequiredSkillFields = Required<Pick<SkillItem, 
  'skillName' | 'category' | 'level' | 'experience' | 'lastUsed' | 'target'
>>;
```

### 4.2 条件付き型

```typescript
/**
 * 目標スキルのみを抽出する型
 */
export type TargetSkill = SkillItem & { target: true };

/**
 * 特定カテゴリのスキル型
 */
export type SkillByCategory<T extends SkillCategory> = SkillItem & { category: T };

/**
 * 特定レベルのスキル型
 */
export type SkillByLevel<T extends SkillLevel> = SkillItem & { level: T };

/**
 * 経験年数による条件付きスキル型
 */
export type ExperiencedSkill<T extends number> = SkillItem & { experience: T };
```

---

## 5. 型ガード関数

```typescript
/**
 * スキルカテゴリの型ガード
 */
export function isSkillCategory(value: any): value is SkillCategory {
  return SKILL_CATEGORIES.includes(value);
}

/**
 * スキルレベルの型ガード
 */
export function isSkillLevel(value: any): value is SkillLevel {
  return SKILL_LEVELS.includes(value);
}

/**
 * スキルアイテムの型ガード
 */
export function isSkillItem(value: any): value is SkillItem {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof value.id === 'string' &&
    typeof value.userId === 'string' &&
    typeof value.skillName === 'string' &&
    isSkillCategory(value.category) &&
    isSkillLevel(value.level) &&
    typeof value.experience === 'number' &&
    value.lastUsed instanceof Date &&
    typeof value.target === 'boolean' &&
    value.createdAt instanceof Date &&
    value.updatedAt instanceof Date
  );
}

/**
 * 目標スキルの型ガード
 */
export function isTargetSkill(skill: SkillItem): skill is TargetSkill {
  return skill.target === true;
}

/**
 * 最近使用したスキルの型ガード（3ヶ月以内）
 */
export function isRecentlyUsedSkill(skill: SkillItem): boolean {
  const threeMonthsAgo = new Date();
  threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
  return skill.lastUsed >= threeMonthsAgo;
}
```

---

## 6. 使用例

### 6.1 基本的な使用例

```typescript
import { 
  SkillItem, 
  CreateSkillRequest, 
  SkillFilters,
  isSkillItem,
  SKILL_CATEGORIES 
} from '@/types/SkillTypes';

// スキル作成
const newSkill: CreateSkillRequest = {
  skillName: 'TypeScript',
  category: 'プログラミング言語',
  level: '上級',
  experience: 3.5,
  lastUsed: new Date(),
  target: true,
  comments: 'フロントエンド開発で主に使用'
};

// フィルター設定
const filters: SkillFilters = {
  category: ['プログラミング言語', 'フレームワーク・ライブラリ'],
  level: ['上級', 'エキスパート'],
  target: true,
  sortBy: 'experience',
  sortOrder: 'desc',
  limit: 10
};

// 型ガードの使用
function processSkill(data: unknown) {
  if (isSkillItem(data)) {
    console.log(`スキル: ${data.skillName}, レベル: ${data.level}`);
  }
}
```

### 6.2 高度な使用例

```typescript
// 条件付き型の使用
type ProgrammingSkills = SkillByCategory<'プログラミング言語'>;
type ExpertSkills = SkillByLevel<'エキスパート'>;

// ユーティリティ型の使用
type SkillSummary = PickSkillFields<'id' | 'skillName' | 'level' | 'category'>;
type SkillWithoutMeta = OmitSkillFields<'createdAt' | 'updatedAt' | 'deletedAt'>;

// 統計データの処理
function analyzeSkills(skills: SkillItem[]): SkillStatistics {
  const targetSkills = skills.filter(isTargetSkill);
  const recentSkills = skills.filter(isRecentlyUsedSkill);
  
  return {
    totalSkills: skills.length,
    targetSkills: targetSkills.length,
    recentlyUsedSkills: recentSkills.length,
    // ... その他の統計
  } as SkillStatistics;
}
```

---

## 7. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 8. 関連ドキュメント

- [共通部品定義書](../../共通部品定義書.md)
- [SkillForm コンポーネント](../../frontend/business-components/SkillForm.md)
- [SkillService](../../backend/services/SkillService.md)
- [API仕様書](../schemas/OpenAPISpec.md)

---

この型定義書により、フロントエンド・バックエンド間で一貫した型安全性を確保し、開発効率と品質を向上させます。
