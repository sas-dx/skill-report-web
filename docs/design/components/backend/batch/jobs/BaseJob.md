# BaseJob バッチジョブ基盤 定義書

## 1. 基本情報

- **部品名**: BaseJob
- **カテゴリ**: バッチ共通部品 - ジョブ基盤
- **責務**: バッチジョブの基盤クラス・共通機能提供
- **依存関係**: なし（基盤クラス）
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 概要

### 2.1 目的

BaseJobは、すべてのバッチジョブが継承する基盤クラスです。共通的なジョブ実行フロー、エラーハンドリング、ログ出力、進捗管理などの機能を提供し、個別のバッチジョブ実装を簡素化します。

### 2.2 主要機能

1. **ジョブライフサイクル管理**
   - 実行前処理（setup）
   - メイン処理（execute）
   - 実行後処理（cleanup）
   - エラー処理（onError）

2. **共通機能**
   - ログ出力
   - 進捗管理
   - 実行時間計測
   - リトライ機能
   - 状態管理

3. **設定管理**
   - ジョブ設定の読み込み
   - 環境変数の管理
   - デフォルト値の提供

---

## 3. インターフェース仕様

### 3.1 型定義

```typescript
/**
 * ジョブの実行状態
 */
export type JobStatus = 
  | 'pending'     // 実行待ち
  | 'running'     // 実行中
  | 'completed'   // 完了
  | 'failed'      // 失敗
  | 'cancelled'   // キャンセル
  | 'retrying';   // リトライ中

/**
 * ジョブの優先度
 */
export type JobPriority = 'low' | 'normal' | 'high' | 'critical';

/**
 * ジョブ設定インターフェース
 */
export interface JobConfig {
  /** ジョブ名 */
  name: string;
  
  /** ジョブの説明 */
  description?: string;
  
  /** 優先度 */
  priority: JobPriority;
  
  /** タイムアウト時間（ミリ秒） */
  timeout: number;
  
  /** リトライ設定 */
  retry: {
    /** 最大リトライ回数 */
    maxAttempts: number;
    /** リトライ間隔（ミリ秒） */
    delay: number;
    /** 指数バックオフを使用するか */
    exponentialBackoff: boolean;
  };
  
  /** 並行実行制御 */
  concurrency: {
    /** 同時実行を許可するか */
    allowConcurrent: boolean;
    /** 最大同時実行数 */
    maxConcurrent?: number;
  };
  
  /** 通知設定 */
  notifications: {
    /** 成功時に通知するか */
    onSuccess: boolean;
    /** 失敗時に通知するか */
    onFailure: boolean;
    /** 通知先 */
    recipients?: string[];
  };
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
  
  /** 実行時間（ミリ秒） */
  duration: number;
  
  /** 結果メッセージ */
  message: string;
  
  /** エラー情報（失敗時） */
  error?: {
    code: string;
    message: string;
    stack?: string;
    details?: any;
  };
  
  /** 追加データ */
  data?: any;
}

/**
 * ジョブ実行コンテキスト
 */
export interface JobContext {
  /** ジョブID */
  jobId: string;
  
  /** 実行ID（同じジョブの複数実行を区別） */
  executionId: string;
  
  /** 実行開始時刻 */
  startedAt: Date;
  
  /** 実行ユーザー */
  userId?: string;
  
  /** 実行パラメータ */
  parameters: Record<string, any>;
  
  /** 実行環境 */
  environment: 'development' | 'staging' | 'production';
  
  /** ドライランフラグ */
  dryRun: boolean;
}

/**
 * 進捗情報
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
}
```

### 3.2 BaseJobクラス

```typescript
/**
 * バッチジョブ基盤クラス
 */
export abstract class BaseJob {
  protected config: JobConfig;
  protected context: JobContext;
  protected logger: Logger;
  protected status: JobStatus = 'pending';
  protected progress: JobProgress;
  protected startTime: number;
  protected retryCount: number = 0;

  constructor(config: JobConfig) {
    this.config = config;
    this.logger = new Logger(`Job:${config.name}`);
    this.progress = {
      current: 0,
      total: 0,
      percentage: 0,
      currentTask: '初期化中'
    };
  }

  /**
   * ジョブを実行する
   */
  public async run(context: JobContext): Promise<JobResult> {
    this.context = context;
    this.startTime = Date.now();
    
    try {
      this.logger.info(`ジョブ開始: ${this.config.name}`, {
        jobId: context.jobId,
        executionId: context.executionId,
        parameters: context.parameters
      });

      // 実行前処理
      await this.setup();
      
      // メイン処理
      this.status = 'running';
      const result = await this.executeWithTimeout();
      
      // 実行後処理
      await this.cleanup();
      
      this.status = 'completed';
      
      const finalResult: JobResult = {
        success: true,
        processedCount: this.progress.current,
        successCount: result.successCount || this.progress.current,
        failureCount: result.failureCount || 0,
        duration: Date.now() - this.startTime,
        message: result.message || 'ジョブが正常に完了しました',
        data: result.data
      };

      this.logger.info('ジョブ完了', finalResult);
      
      // 成功通知
      if (this.config.notifications.onSuccess) {
        await this.sendNotification('success', finalResult);
      }
      
      return finalResult;

    } catch (error) {
      return await this.handleError(error);
    }
  }

  /**
   * 実行前処理（サブクラスでオーバーライド可能）
   */
  protected async setup(): Promise<void> {
    this.updateProgress(0, 0, '実行前処理中');
  }

  /**
   * メイン処理（サブクラスで実装必須）
   */
  protected abstract execute(): Promise<Partial<JobResult>>;

  /**
   * 実行後処理（サブクラスでオーバーライド可能）
   */
  protected async cleanup(): Promise<void> {
    this.updateProgress(this.progress.current, this.progress.total, '実行後処理中');
  }

  /**
   * エラー処理（サブクラスでオーバーライド可能）
   */
  protected async onError(error: Error): Promise<void> {
    this.logger.error('ジョブエラー', {
      error: error.message,
      stack: error.stack,
      jobId: this.context.jobId
    });
  }

  /**
   * タイムアウト付きで実行
   */
  private async executeWithTimeout(): Promise<Partial<JobResult>> {
    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error(`ジョブがタイムアウトしました (${this.config.timeout}ms)`));
      }, this.config.timeout);

      this.execute()
        .then(result => {
          clearTimeout(timeoutId);
          resolve(result);
        })
        .catch(error => {
          clearTimeout(timeoutId);
          reject(error);
        });
    });
  }

  /**
   * エラーハンドリング
   */
  private async handleError(error: Error): Promise<JobResult> {
    this.status = 'failed';
    
    await this.onError(error);
    
    const result: JobResult = {
      success: false,
      processedCount: this.progress.current,
      successCount: 0,
      failureCount: this.progress.current,
      duration: Date.now() - this.startTime,
      message: `ジョブが失敗しました: ${error.message}`,
      error: {
        code: 'JOB_EXECUTION_ERROR',
        message: error.message,
        stack: error.stack
      }
    };

    this.logger.error('ジョブ失敗', result);

    // リトライ判定
    if (this.shouldRetry(error)) {
      this.status = 'retrying';
      this.retryCount++;
      
      const delay = this.calculateRetryDelay();
      this.logger.info(`${delay}ms後にリトライします (${this.retryCount}/${this.config.retry.maxAttempts})`);
      
      await this.sleep(delay);
      return await this.run(this.context);
    }

    // 失敗通知
    if (this.config.notifications.onFailure) {
      await this.sendNotification('failure', result);
    }

    return result;
  }

  /**
   * リトライ判定
   */
  private shouldRetry(error: Error): boolean {
    if (this.retryCount >= this.config.retry.maxAttempts) {
      return false;
    }

    // 特定のエラーはリトライしない
    const nonRetryableErrors = [
      'VALIDATION_ERROR',
      'AUTHENTICATION_ERROR',
      'AUTHORIZATION_ERROR'
    ];

    return !nonRetryableErrors.some(code => error.message.includes(code));
  }

  /**
   * リトライ遅延時間計算
   */
  private calculateRetryDelay(): number {
    const baseDelay = this.config.retry.delay;
    
    if (this.config.retry.exponentialBackoff) {
      return baseDelay * Math.pow(2, this.retryCount - 1);
    }
    
    return baseDelay;
  }

  /**
   * 進捗更新
   */
  protected updateProgress(current: number, total: number, task: string): void {
    this.progress = {
      current,
      total,
      percentage: total > 0 ? Math.round((current / total) * 100) : 0,
      currentTask: task,
      estimatedTimeRemaining: this.calculateEstimatedTime(current, total)
    };

    this.logger.debug('進捗更新', this.progress);
  }

  /**
   * 推定残り時間計算
   */
  private calculateEstimatedTime(current: number, total: number): number | undefined {
    if (current === 0 || total === 0) return undefined;
    
    const elapsed = Date.now() - this.startTime;
    const rate = current / elapsed;
    const remaining = total - current;
    
    return Math.round(remaining / rate);
  }

  /**
   * 通知送信
   */
  private async sendNotification(type: 'success' | 'failure', result: JobResult): Promise<void> {
    try {
      // 通知実装は NotificationService に委譲
      const notificationService = new NotificationService();
      
      await notificationService.sendJobNotification({
        type,
        jobName: this.config.name,
        result,
        recipients: this.config.notifications.recipients
      });
    } catch (error) {
      this.logger.warn('通知送信に失敗しました', { error: error.message });
    }
  }

  /**
   * スリープ
   */
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * ジョブキャンセル
   */
  public async cancel(): Promise<void> {
    this.status = 'cancelled';
    this.logger.info('ジョブがキャンセルされました');
  }

  /**
   * 現在の状態取得
   */
  public getStatus(): JobStatus {
    return this.status;
  }

  /**
   * 現在の進捗取得
   */
  public getProgress(): JobProgress {
    return { ...this.progress };
  }

  /**
   * ジョブ設定取得
   */
  public getConfig(): JobConfig {
    return { ...this.config };
  }
}
```

---

## 4. 実装例

### 4.1 具体的なジョブ実装例

```typescript
/**
 * スキル統計集計ジョブの実装例
 */
export class SkillStatisticsJob extends BaseJob {
  private skillService: SkillService;

  constructor() {
    super({
      name: 'skill-statistics',
      description: 'スキル統計データの集計',
      priority: 'normal',
      timeout: 300000, // 5分
      retry: {
        maxAttempts: 3,
        delay: 5000,
        exponentialBackoff: true
      },
      concurrency: {
        allowConcurrent: false
      },
      notifications: {
        onSuccess: true,
        onFailure: true,
        recipients: ['admin@example.com']
      }
    });

    this.skillService = new SkillService();
  }

  protected async setup(): Promise<void> {
    await super.setup();
    
    // データベース接続確認
    await this.skillService.healthCheck();
    
    this.logger.info('スキル統計集計ジョブの準備完了');
  }

  protected async execute(): Promise<Partial<JobResult>> {
    const users = await this.skillService.getAllUsers();
    this.updateProgress(0, users.length, 'ユーザー統計集計開始');

    let successCount = 0;
    let failureCount = 0;

    for (let i = 0; i < users.length; i++) {
      const user = users[i];
      
      try {
        this.updateProgress(i + 1, users.length, `${user.name}の統計集計中`);
        
        // ドライランチェック
        if (!this.context.dryRun) {
          await this.skillService.calculateUserStatistics(user.id);
        }
        
        successCount++;
        
      } catch (error) {
        this.logger.warn(`ユーザー${user.id}の統計集計に失敗`, { error: error.message });
        failureCount++;
      }
    }

    return {
      successCount,
      failureCount,
      message: `統計集計完了: 成功${successCount}件, 失敗${failureCount}件`,
      data: {
        totalUsers: users.length,
        successCount,
        failureCount
      }
    };
  }

  protected async cleanup(): Promise<void> {
    await super.cleanup();
    
    // キャッシュクリア
    await this.skillService.clearStatisticsCache();
    
    this.logger.info('スキル統計集計ジョブのクリーンアップ完了');
  }
}
```

### 4.2 ジョブ実行例

```typescript
// ジョブの実行
async function runSkillStatisticsJob() {
  const job = new SkillStatisticsJob();
  
  const context: JobContext = {
    jobId: 'skill-stats-001',
    executionId: `exec-${Date.now()}`,
    startedAt: new Date(),
    userId: 'system',
    parameters: {
      targetDate: '2025-05-30'
    },
    environment: 'production',
    dryRun: false
  };

  const result = await job.run(context);
  
  if (result.success) {
    console.log('ジョブが正常に完了しました:', result);
  } else {
    console.error('ジョブが失敗しました:', result.error);
  }
}
```

---

## 5. テスト仕様

### 5.1 単体テスト

```typescript
describe('BaseJob', () => {
  let mockJob: TestJob;
  let mockContext: JobContext;

  beforeEach(() => {
    mockJob = new TestJob();
    mockContext = {
      jobId: 'test-job',
      executionId: 'test-exec',
      startedAt: new Date(),
      parameters: {},
      environment: 'development',
      dryRun: false
    };
  });

  describe('正常系', () => {
    test('ジョブが正常に実行される', async () => {
      const result = await mockJob.run(mockContext);
      
      expect(result.success).toBe(true);
      expect(result.processedCount).toBeGreaterThan(0);
      expect(result.duration).toBeGreaterThan(0);
    });

    test('進捗が正しく更新される', async () => {
      const progressSpy = jest.spyOn(mockJob, 'getProgress');
      
      await mockJob.run(mockContext);
      
      expect(progressSpy).toHaveBeenCalled();
      const progress = mockJob.getProgress();
      expect(progress.percentage).toBe(100);
    });
  });

  describe('異常系', () => {
    test('タイムアウト時にエラーが発生する', async () => {
      const timeoutJob = new TimeoutTestJob();
      
      const result = await timeoutJob.run(mockContext);
      
      expect(result.success).toBe(false);
      expect(result.error?.message).toContain('タイムアウト');
    });

    test('リトライが正しく動作する', async () => {
      const retryJob = new RetryTestJob();
      
      const result = await retryJob.run(mockContext);
      
      // 最大リトライ回数まで実行される
      expect(retryJob.getRetryCount()).toBe(3);
    });
  });
});

// テスト用のジョブクラス
class TestJob extends BaseJob {
  constructor() {
    super({
      name: 'test-job',
      priority: 'normal',
      timeout: 10000,
      retry: { maxAttempts: 3, delay: 1000, exponentialBackoff: false },
      concurrency: { allowConcurrent: true },
      notifications: { onSuccess: false, onFailure: false }
    });
  }

  protected async execute(): Promise<Partial<JobResult>> {
    this.updateProgress(0, 100, 'テスト実行中');
    
    for (let i = 1; i <= 100; i++) {
      await new Promise(resolve => setTimeout(resolve, 10));
      this.updateProgress(i, 100, `処理中: ${i}/100`);
    }

    return {
      successCount: 100,
      failureCount: 0,
      message: 'テストジョブ完了'
    };
  }
}
```

### 5.2 統合テスト

```typescript
describe('BaseJob 統合テスト', () => {
  test('実際のサービスとの連携', async () => {
    const skillService = new SkillService();
    const job = new SkillStatisticsJob();
    
    const context: JobContext = {
      jobId: 'integration-test',
      executionId: 'test-exec',
      startedAt: new Date(),
      parameters: {},
      environment: 'development',
      dryRun: true // ドライランで実行
    };

    const result = await job.run(context);
    
    expect(result.success).toBe(true);
    expect(result.processedCount).toBeGreaterThanOrEqual(0);
  });
});
```

---

## 6. パフォーマンス要件

### 6.1 実行時間

- **小規模ジョブ**: 1分以内
- **中規模ジョブ**: 10分以内
- **大規模ジョブ**: 1時間以内

### 6.2 メモリ使用量

- **最大メモリ使用量**: 512MB以下
- **メモリリーク**: 検出されないこと
- **ガベージコレクション**: 適切に動作すること

### 6.3 同時実行

- **最大同時実行ジョブ数**: 10個
- **リソース競合**: 発生しないこと
- **デッドロック**: 発生しないこと

---

## 7. セキュリティ要件

### 7.1 認証・認可

- **実行権限**: 適切な権限を持つユーザーのみ実行可能
- **パラメータ検証**: 入力パラメータの妥当性検証
- **ログ出力**: 機密情報の出力禁止

### 7.2 データ保護

- **データアクセス**: 必要最小限のデータのみアクセス
- **一時ファイル**: 実行後に確実に削除
- **エラー情報**: 機密情報を含まないエラーメッセージ

---

## 8. 運用要件

### 8.1 監視

- **実行状況**: リアルタイム監視
- **リソース使用量**: CPU・メモリ・ディスク使用量監視
- **エラー率**: エラー発生率の監視

### 8.2 ログ

- **ログレベル**: DEBUG, INFO, WARN, ERROR
- **ログ形式**: 構造化ログ（JSON形式）
- **ログ保持期間**: 30日間

### 8.3 アラート

- **失敗時**: 即座にアラート通知
- **長時間実行**: 予想実行時間を超過した場合
- **リソース不足**: メモリ・ディスク不足時

---

## 9. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 10. 関連ドキュメント

- [共通部品定義書](../../共通部品定義書.md)
- [JobScheduler 定義書](../schedulers/JobScheduler.md)
- [BatchLogger 定義書](../utils/BatchLogger.md)
- [バッチ処理アーキテクチャ](../../../architecture/BatchArchitecture.md)

---

この BaseJob 定義書により、統一されたバッチジョブ基盤を提供し、開発効率と品質の向上を実現します。
