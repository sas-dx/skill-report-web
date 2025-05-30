# BatchTypes バッチ処理型定義書

## 1. 基本情報

- **部品名**: BatchTypes
- **カテゴリ**: 共有型定義 - バッチ処理
- **責務**: バッチ処理関連の型定義・インターフェース
- **依存関係**: なし（基盤型定義）
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 概要

### 2.1 目的

BatchTypesは、バッチ処理システム全体で使用される型定義を提供します。ジョブ、スケジューラー、キュー、ログなどのバッチ処理に関連するすべての型を統一的に管理し、型安全性を確保します。

### 2.2 適用範囲

- バッチジョブの実行・管理
- スケジューリング機能
- ジョブキューイング
- 実行履歴・ログ管理
- 監視・メトリクス収集

---

## 3. 基本型定義

### 3.1 ジョブ関連型

```typescript
/**
 * ジョブの実行状態
 */
export type JobStatus = 
  | 'pending'     // 実行待ち
  | 'queued'      // キュー待ち
  | 'running'     // 実行中
  | 'completed'   // 完了
  | 'failed'      // 失敗
  | 'cancelled'   // キャンセル
  | 'retrying'    // リトライ中
  | 'timeout'     // タイムアウト
  | 'skipped';    // スキップ

/**
 * ジョブの優先度
 */
export type JobPriority = 'low' | 'normal' | 'high' | 'critical';

/**
 * ジョブの実行タイプ
 */
export type JobExecutionType = 
  | 'scheduled'   // 定期実行
  | 'manual'      // 手動実行
  | 'delayed'     // 遅延実行
  | 'triggered'   // イベント駆動実行
  | 'retry';      // リトライ実行

/**
 * ジョブカテゴリ
 */
export type JobCategory = 
  | 'data-sync'       // データ同期
  | 'statistics'      // 統計集計
  | 'cleanup'         // データクリーンアップ
  | 'report'          // レポート生成
  | 'notification'    // 通知送信
  | 'backup'          // バックアップ
  | 'maintenance'     // メンテナンス
  | 'import'          // データインポート
  | 'export'          // データエクスポート
  | 'validation'      // データ検証
  | 'migration'       // データ移行
  | 'monitoring';     // 監視

/**
 * 実行環境
 */
export type ExecutionEnvironment = 'development' | 'staging' | 'production';

/**
 * リトライ戦略
 */
export type RetryStrategy = 
  | 'fixed'           // 固定間隔
  | 'exponential'     // 指数バックオフ
  | 'linear'          // 線形増加
  | 'custom';         // カスタム
```

### 3.2 スケジュール関連型

```typescript
/**
 * スケジュールタイプ
 */
export type ScheduleType = 
  | 'cron'        // cron式
  | 'interval'    // 間隔実行
  | 'once'        // 一回実行
  | 'event';      // イベント駆動

/**
 * スケジュール状態
 */
export type ScheduleStatus = 
  | 'active'      // 有効
  | 'inactive'    // 無効
  | 'paused'      // 一時停止
  | 'expired'     // 期限切れ
  | 'error';      // エラー

/**
 * 曜日
 */
export type DayOfWeek = 
  | 'sunday'
  | 'monday'
  | 'tuesday'
  | 'wednesday'
  | 'thursday'
  | 'friday'
  | 'saturday';

/**
 * 月
 */
export type Month = 
  | 'january' | 'february' | 'march' | 'april'
  | 'may' | 'june' | 'july' | 'august'
  | 'september' | 'october' | 'november' | 'december';
```

### 3.3 ログ・監視関連型

```typescript
/**
 * ログレベル
 */
export type LogLevel = 'debug' | 'info' | 'warn' | 'error' | 'fatal';

/**
 * メトリクスタイプ
 */
export type MetricType = 
  | 'counter'     // カウンター
  | 'gauge'       // ゲージ
  | 'histogram'   // ヒストグラム
  | 'timer';      // タイマー

/**
 * アラートレベル
 */
export type AlertLevel = 'info' | 'warning' | 'critical';

/**
 * 通知チャンネル
 */
export type NotificationChannel = 
  | 'email'
  | 'slack'
  | 'teams'
  | 'webhook'
  | 'sms';
```

---

## 4. インターフェース定義

### 4.1 ジョブ関連インターフェース

```typescript
/**
 * ジョブ設定インターフェース
 */
export interface JobConfig {
  /** ジョブ名 */
  name: string;
  
  /** ジョブの説明 */
  description?: string;
  
  /** ジョブカテゴリ */
  category: JobCategory;
  
  /** 優先度 */
  priority: JobPriority;
  
  /** タイムアウト時間（ミリ秒） */
  timeout: number;
  
  /** リトライ設定 */
  retry: RetryConfig;
  
  /** 並行実行制御 */
  concurrency: ConcurrencyConfig;
  
  /** 通知設定 */
  notifications: NotificationConfig;
  
  /** リソース制限 */
  resources?: ResourceLimits;
  
  /** 依存関係 */
  dependencies?: JobDependency[];
  
  /** タグ */
  tags?: string[];
  
  /** メタデータ */
  metadata?: Record<string, any>;
}

/**
 * リトライ設定
 */
export interface RetryConfig {
  /** 最大リトライ回数 */
  maxAttempts: number;
  
  /** リトライ間隔（ミリ秒） */
  delay: number;
  
  /** リトライ戦略 */
  strategy: RetryStrategy;
  
  /** 最大遅延時間（ミリ秒） */
  maxDelay?: number;
  
  /** リトライ対象エラー */
  retryableErrors?: string[];
  
  /** リトライ除外エラー */
  nonRetryableErrors?: string[];
  
  /** カスタムリトライ関数 */
  customRetryFn?: (error: Error, attempt: number) => boolean;
}

/**
 * 並行実行制御設定
 */
export interface ConcurrencyConfig {
  /** 同時実行を許可するか */
  allowConcurrent: boolean;
  
  /** 最大同時実行数 */
  maxConcurrent?: number;
  
  /** 同一ジョブの重複実行を許可するか */
  allowDuplicates?: boolean;
  
  /** 実行グループ */
  executionGroup?: string;
}

/**
 * 通知設定
 */
export interface NotificationConfig {
  /** 成功時に通知するか */
  onSuccess: boolean;
  
  /** 失敗時に通知するか */
  onFailure: boolean;
  
  /** リトライ時に通知するか */
  onRetry?: boolean;
  
  /** 長時間実行時に通知するか */
  onLongRunning?: boolean;
  
  /** 通知先 */
  recipients?: string[];
  
  /** 通知チャンネル */
  channels?: NotificationChannel[];
  
  /** 通知テンプレート */
  template?: string;
}

/**
 * リソース制限
 */
export interface ResourceLimits {
  /** 最大メモリ使用量（MB） */
  maxMemoryMB?: number;
  
  /** 最大CPU使用率（%） */
  maxCpuPercent?: number;
  
  /** 最大ディスク使用量（MB） */
  maxDiskMB?: number;
  
  /** 最大ネットワーク帯域（Mbps） */
  maxNetworkMbps?: number;
}

/**
 * ジョブ依存関係
 */
export interface JobDependency {
  /** 依存ジョブ名 */
  jobName: string;
  
  /** 依存タイプ */
  type: 'success' | 'completion' | 'failure';
  
  /** タイムアウト（ミリ秒） */
  timeout?: number;
}

/**
 * ジョブ実行結果
 */
export interface JobResult {
  /** 実行成功フラグ */
  success: boolean;
  
  /** 処理件数 */
  processedCount: number;
  
  /** 成功件数 */
  successCount: number;
  
  /** 失敗件数 */
  failureCount: number;
  
  /** スキップ件数 */
  skippedCount?: number;
  
  /** 実行時間（ミリ秒） */
  duration: number;
  
  /** 結果メッセージ */
  message: string;
  
  /** エラー情報（失敗時） */
  error?: JobError;
  
  /** 警告一覧 */
  warnings?: JobWarning[];
  
  /** 追加データ */
  data?: any;
  
  /** メトリクス */
  metrics?: JobMetrics;
}

/**
 * ジョブエラー
 */
export interface JobError {
  /** エラーコード */
  code: string;
  
  /** エラーメッセージ */
  message: string;
  
  /** スタックトレース */
  stack?: string;
  
  /** エラー詳細 */
  details?: any;
  
  /** 原因エラー */
  cause?: JobError;
  
  /** リトライ可能フラグ */
  retryable?: boolean;
}

/**
 * ジョブ警告
 */
export interface JobWarning {
  /** 警告コード */
  code: string;
  
  /** 警告メッセージ */
  message: string;
  
  /** 警告詳細 */
  details?: any;
}

/**
 * ジョブメトリクス
 */
export interface JobMetrics {
  /** メモリ使用量（MB） */
  memoryUsageMB: number;
  
  /** CPU使用率（%） */
  cpuUsagePercent: number;
  
  /** ディスク使用量（MB） */
  diskUsageMB?: number;
  
  /** ネットワーク使用量（MB） */
  networkUsageMB?: number;
  
  /** データベースクエリ数 */
  dbQueryCount?: number;
  
  /** API呼び出し数 */
  apiCallCount?: number;
  
  /** カスタムメトリクス */
  custom?: Record<string, number>;
}

/**
 * ジョブ実行コンテキスト
 */
export interface JobContext {
  /** ジョブID */
  jobId: string;
  
  /** 実行ID */
  executionId: string;
  
  /** 実行開始時刻 */
  startedAt: Date;
  
  /** 実行ユーザー */
  userId?: string;
  
  /** 実行パラメータ */
  parameters: Record<string, any>;
  
  /** 実行環境 */
  environment: ExecutionEnvironment;
  
  /** ドライランフラグ */
  dryRun: boolean;
  
  /** 実行タイプ */
  executionType: JobExecutionType;
  
  /** スケジュールID（定期実行の場合） */
  scheduleId?: string;
  
  /** 親ジョブID（子ジョブの場合） */
  parentJobId?: string;
  
  /** 実行トレースID */
  traceId?: string;
  
  /** 実行コンテキストデータ */
  contextData?: Record<string, any>;
}

/**
 * ジョブ進捗情報
 */
export interface JobProgress {
  /** 現在の処理件数 */
  current: number;
  
  /** 総件数 */
  total: number;
  
  /** 進捗率（0-100） */
  percentage: number;
  
  /** 現在の処理内容 */
  currentTask: string;
  
  /** 推定残り時間（ミリ秒） */
  estimatedTimeRemaining?: number;
  
  /** 処理速度（件/秒） */
  processingRate?: number;
  
  /** 段階情報 */
  stage?: JobStage;
  
  /** 詳細進捗 */
  details?: Record<string, any>;
}

/**
 * ジョブ段階情報
 */
export interface JobStage {
  /** 現在の段階 */
  current: number;
  
  /** 総段階数 */
  total: number;
  
  /** 段階名 */
  name: string;
  
  /** 段階の説明 */
  description?: string;
}
```

---

## 5. 定数定義

### 5.1 ジョブ関連定数

```typescript
/**
 * ジョブカテゴリ一覧
 */
export const JOB_CATEGORIES: JobCategory[] = [
  'data-sync',
  'statistics',
  'cleanup',
  'report',
  'notification',
  'backup',
  'maintenance',
  'import',
  'export',
  'validation',
  'migration',
  'monitoring'
];

/**
 * ジョブ優先度一覧
 */
export const JOB_PRIORITIES: JobPriority[] = [
  'low',
  'normal',
  'high',
  'critical'
];

/**
 * ジョブ状態一覧
 */
export const JOB_STATUSES: JobStatus[] = [
  'pending',
  'queued',
  'running',
  'completed',
  'failed',
  'cancelled',
  'retrying',
  'timeout',
  'skipped'
];

/**
 * デフォルトタイムアウト時間（ミリ秒）
 */
export const DEFAULT_TIMEOUTS = {
  JOB_EXECUTION: 300000,      // 5分
  CONDITION_CHECK: 30000,     // 30秒
  QUEUE_PROCESSING: 60000,    // 1分
  HEALTH_CHECK: 10000,        // 10秒
  NOTIFICATION: 15000         // 15秒
};

/**
 * デフォルトリトライ設定
 */
export const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxAttempts: 3,
  delay: 5000,
  strategy: 'exponential',
  maxDelay: 300000
};

/**
 * ジョブエラーコード
 */
export const JOB_ERROR_CODES = {
  // 一般的なエラー
  UNKNOWN_ERROR: 'JOB_UNKNOWN_ERROR',
  TIMEOUT_ERROR: 'JOB_TIMEOUT_ERROR',
  CANCELLED_ERROR: 'JOB_CANCELLED_ERROR',
  
  // 設定エラー
  INVALID_CONFIG: 'JOB_INVALID_CONFIG',
  MISSING_PARAMETER: 'JOB_MISSING_PARAMETER',
  INVALID_PARAMETER: 'JOB_INVALID_PARAMETER',
  
  // 実行エラー
  EXECUTION_ERROR: 'JOB_EXECUTION_ERROR',
  DEPENDENCY_ERROR: 'JOB_DEPENDENCY_ERROR',
  RESOURCE_ERROR: 'JOB_RESOURCE_ERROR',
  
  // データエラー
  DATA_ACCESS_ERROR: 'JOB_DATA_ACCESS_ERROR',
  DATA_VALIDATION_ERROR: 'JOB_DATA_VALIDATION_ERROR',
  DATA_CORRUPTION_ERROR: 'JOB_DATA_CORRUPTION_ERROR',
  
  // ネットワークエラー
  NETWORK_ERROR: 'JOB_NETWORK_ERROR',
  API_ERROR: 'JOB_API_ERROR',
  CONNECTION_ERROR: 'JOB_CONNECTION_ERROR',
  
  // 認証・認可エラー
  AUTHENTICATION_ERROR: 'JOB_AUTHENTICATION_ERROR',
  AUTHORIZATION_ERROR: 'JOB_AUTHORIZATION_ERROR',
  PERMISSION_ERROR: 'JOB_PERMISSION_ERROR'
} as const;
```

---

## 6. ユーティリティ型

### 6.1 型変換ユーティリティ

```typescript
/**
 * ジョブ状態から色を取得する型
 */
export type JobStatusColor<T extends JobStatus> = 
  T extends 'completed' ? 'green' :
  T extends 'running' ? 'blue' :
  T extends 'failed' ? 'red' :
  T extends 'cancelled' ? 'gray' :
  T extends 'pending' | 'queued' ? 'yellow' :
  'orange';

/**
 * 優先度から数値を取得する型
 */
export type PriorityToNumber<T extends JobPriority> = 
  T extends 'low' ? 1 :
  T extends 'normal' ? 2 :
  T extends 'high' ? 3 :
  T extends 'critical' ? 4 :
  never;

/**
 * ジョブ設定から特定フィールドのみを抽出
 */
export type PickJobConfigFields<T extends keyof JobConfig> = Pick<JobConfig, T>;

/**
 * ジョブ設定から特定フィールドを除外
 */
export type OmitJobConfigFields<T extends keyof JobConfig> = Omit<JobConfig, T>;

/**
 * ジョブ結果の部分型（すべてオプション）
 */
export type PartialJobResult = Partial<JobResult>;

/**
 * 必須ジョブ設定フィールドのみ
 */
export type RequiredJobConfigFields = Required<Pick<JobConfig, 
  'name' | 'category' | 'priority' | 'timeout' | 'retry' | 'concurrency' | 'notifications'
>>;
```

### 6.2 条件付き型

```typescript
/**
 * 成功したジョブのみを抽出する型
 */
export type SuccessfulJob = JobResult & { success: true };

/**
 * 失敗したジョブのみを抽出する型
 */
export type FailedJob = JobResult & { success: false; error: JobError };

/**
 * 特定カテゴリのジョブ設定型
 */
export type JobConfigByCategory<T extends JobCategory> = JobConfig & { category: T };

/**
 * 特定優先度のジョブ設定型
 */
export type JobConfigByPriority<T extends JobPriority> = JobConfig & { priority: T };

/**
 * 実行時間による条件付きジョブ結果型
 */
export type LongRunningJob<T extends number> = JobResult & { duration: T };
```

---

## 7. 型ガード関数

```typescript
/**
 * ジョブカテゴリの型ガード
 */
export function isJobCategory(value: any): value is JobCategory {
  return JOB_CATEGORIES.includes(value);
}

/**
 * ジョブ優先度の型ガード
 */
export function isJobPriority(value: any): value is JobPriority {
  return JOB_PRIORITIES.includes(value);
}

/**
 * ジョブ状態の型ガード
 */
export function isJobStatus(value: any): value is JobStatus {
  return JOB_STATUSES.includes(value);
}

/**
 * ジョブ設定の型ガード
 */
export function isJobConfig(value: any): value is JobConfig {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof value.name === 'string' &&
    isJobCategory(value.category) &&
    isJobPriority(value.priority) &&
    typeof value.timeout === 'number' &&
    typeof value.retry === 'object' &&
    typeof value.concurrency === 'object' &&
    typeof value.notifications === 'object'
  );
}

/**
 * ジョブ結果の型ガード
 */
export function isJobResult(value: any): value is JobResult {
  return (
    typeof value === 'object' &&
    value !== null &&
    typeof value.success === 'boolean' &&
    typeof value.processedCount === 'number' &&
    typeof value.successCount === 'number' &&
    typeof value.failureCount === 'number' &&
    typeof value.duration === 'number' &&
    typeof value.message === 'string'
  );
}

/**
 * 成功したジョブの型ガード
 */
export function isSuccessfulJob(result: JobResult): result is SuccessfulJob {
  return result.success === true;
}

/**
 * 失敗したジョブの型ガード
 */
export function isFailedJob(result: JobResult): result is FailedJob {
  return result.success === false && result.error !== undefined;
}

/**
 * 長時間実行ジョブの型ガード（1時間以上）
 */
export function isLongRunningJob(result: JobResult): boolean {
  return result.duration >= 3600000; // 1時間
}

/**
 * 高優先度ジョブの型ガード
 */
export function isHighPriorityJob(config: JobConfig): boolean {
  return config.priority === 'high' || config.priority === 'critical';
}

/**
 * リトライ可能エラーの型ガード
 */
export function isRetryableError(error: JobError): boolean {
  const nonRetryableErrors = [
    JOB_ERROR_CODES.AUTHENTICATION_ERROR,
    JOB_ERROR_CODES.AUTHORIZATION_ERROR,
    JOB_ERROR_CODES.PERMISSION_ERROR,
    JOB_ERROR_CODES.INVALID_CONFIG,
    JOB_ERROR_CODES.INVALID_PARAMETER
  ];
  
  return !nonRetryableErrors.includes(error.code as any);
}
```

---

## 8. 使用例

### 8.1 基本的な使用例

```typescript
import { 
  JobConfig, 
  JobResult, 
  isJobConfig,
  isSuccessfulJob,
  JOB_CATEGORIES,
  DEFAULT_RETRY_CONFIG 
} from '@/types/BatchTypes';

// ジョブ設定の作成
const jobConfig: JobConfig = {
  name: 'skill-statistics-job',
  description: 'スキル統計の集計処理',
  category: 'statistics',
  priority: 'normal',
  timeout: 300000,
  retry: DEFAULT_RETRY_CONFIG,
  concurrency: {
    allowConcurrent: false,
    maxConcurrent: 1
  },
  notifications: {
    onSuccess: true,
    onFailure: true,
    recipients: ['admin@example.com']
  },
  tags: ['daily', 'statistics'],
  metadata: {
    version: '1.0.0',
    owner: 'data-team'
  }
};

// 型ガードの使用
function processJobResult(data: unknown) {
  if (isJobConfig(data)) {
    console.log(`ジョブ設定: ${data.name}, カテゴリ: ${data.category}`);
  }
}

// 結果の処理
function handleJobResult(result: JobResult) {
  if (isSuccessfulJob(result)) {
    console.log(`ジョブ成功: ${result.successCount}件処理`);
  } else {
    console.error(`ジョブ失敗: ${result.error?.message}`);
  }
}
```

### 8.2 高度な使用例

```typescript
// 条件付き型の使用
type StatisticsJobConfig = JobConfigByCategory<'statistics'>;
type CriticalJobConfig = JobConfigByPriority<'critical'>;

// ユーティリティ型の使用
type JobSummary = PickJobConfigFields<'name' | 'category' | 'priority'>;
type JobWithoutMeta = OmitJobConfigFields<'metadata' | 'tags'>;

// 統計データの処理
function analyzeJobResults(results: JobResult[]): {
  successful: SuccessfulJob[];
  failed: FailedJob[];
  longRunning: JobResult[];
} {
  const successful = results.filter(isSuccessfulJob);
  const failed = results.filter(isFailedJob);
  const longRunning = results.filter(isLongRunningJob);
  
  return { successful, failed, longRunning };
}
```

---

## 9. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 10. 関連ドキュメント

- [共通部品定義書](../../共通部品定義書.md)
- [BaseJob 定義書](../../backend/batch/jobs/BaseJob.md)
- [JobScheduler 定義書](../../backend/batch/schedulers/JobScheduler.md)
- [SkillTypes 型定義書](./SkillTypes.md)
- [バッチ処理アーキテクチャ](../../../architecture/BatchArchitecture.md)

---

この BatchTypes 型定義書により、バッチ処理システム全体で統一された型安全性を確保し、開発効率と品質を向上させます。
