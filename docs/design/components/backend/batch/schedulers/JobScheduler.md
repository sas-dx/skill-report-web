# JobScheduler ジョブスケジューラー 定義書

## 1. 基本情報

- **部品名**: JobScheduler
- **カテゴリ**: バッチ共通部品 - スケジューラー
- **責務**: バッチジョブのスケジューリング・実行管理
- **依存関係**: node-cron, BaseJob, JobQueue
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 概要

### 2.1 目的

JobSchedulerは、バッチジョブの定期実行、即座実行、キュー管理を行うスケジューラーです。cron式による柔軟なスケジューリング、ジョブの並行実行制御、失敗時の自動リトライなどの機能を提供します。

### 2.2 主要機能

1. **スケジューリング機能**
   - cron式による定期実行
   - 即座実行（手動実行）
   - 遅延実行（指定時刻実行）
   - 条件付き実行

2. **実行管理**
   - ジョブキューイング
   - 並行実行制御
   - 優先度制御
   - タイムアウト管理

3. **監視・制御**
   - 実行状況監視
   - ジョブキャンセル
   - 実行履歴管理
   - メトリクス収集

---

## 3. インターフェース仕様

### 3.1 型定義

```typescript
/**
 * スケジュール設定
 */
export interface ScheduleConfig {
  /** スケジュール名 */
  name: string;
  
  /** cron式 */
  cronExpression: string;
  
  /** タイムゾーン */
  timezone?: string;
  
  /** 有効フラグ */
  enabled: boolean;
  
  /** 開始日時 */
  startDate?: Date;
  
  /** 終了日時 */
  endDate?: Date;
  
  /** 最大実行回数 */
  maxExecutions?: number;
  
  /** 実行条件 */
  condition?: ScheduleCondition;
}

/**
 * 実行条件
 */
export interface ScheduleCondition {
  /** 条件チェック関数 */
  check: () => Promise<boolean>;
  
  /** 条件の説明 */
  description: string;
  
  /** 条件チェックのタイムアウト（ミリ秒） */
  timeout?: number;
}

/**
 * ジョブ実行要求
 */
export interface JobExecutionRequest {
  /** ジョブクラス */
  jobClass: new () => BaseJob;
  
  /** 実行パラメータ */
  parameters?: Record<string, any>;
  
  /** 実行ユーザー */
  userId?: string;
  
  /** 優先度 */
  priority?: JobPriority;
  
  /** 遅延実行時間（ミリ秒） */
  delay?: number;
  
  /** 実行予定時刻 */
  scheduledAt?: Date;
  
  /** ドライランフラグ */
  dryRun?: boolean;
}

/**
 * スケジュール済みジョブ情報
 */
export interface ScheduledJob {
  /** スケジュールID */
  scheduleId: string;
  
  /** ジョブクラス */
  jobClass: new () => BaseJob;
  
  /** スケジュール設定 */
  schedule: ScheduleConfig;
  
  /** 実行パラメータ */
  parameters: Record<string, any>;
  
  /** 次回実行予定時刻 */
  nextExecution: Date;
  
  /** 最終実行時刻 */
  lastExecution?: Date;
  
  /** 実行回数 */
  executionCount: number;
  
  /** 作成日時 */
  createdAt: Date;
  
  /** 更新日時 */
  updatedAt: Date;
}

/**
 * 実行中ジョブ情報
 */
export interface RunningJob {
  /** 実行ID */
  executionId: string;
  
  /** ジョブインスタンス */
  jobInstance: BaseJob;
  
  /** 実行コンテキスト */
  context: JobContext;
  
  /** 開始時刻 */
  startedAt: Date;
  
  /** 実行タイプ */
  executionType: 'scheduled' | 'manual' | 'delayed';
  
  /** スケジュールID（定期実行の場合） */
  scheduleId?: string;
}

/**
 * スケジューラー統計情報
 */
export interface SchedulerStatistics {
  /** 登録済みスケジュール数 */
  totalSchedules: number;
  
  /** 有効なスケジュール数 */
  activeSchedules: number;
  
  /** 実行中ジョブ数 */
  runningJobs: number;
  
  /** キュー待ちジョブ数 */
  queuedJobs: number;
  
  /** 今日の実行回数 */
  todayExecutions: number;
  
  /** 今日の成功回数 */
  todaySuccesses: number;
  
  /** 今日の失敗回数 */
  todayFailures: number;
  
  /** 平均実行時間（ミリ秒） */
  averageExecutionTime: number;
  
  /** 最終実行時刻 */
  lastExecutionTime?: Date;
}
```

### 3.2 JobSchedulerクラス

```typescript
/**
 * ジョブスケジューラークラス
 */
export class JobScheduler {
  private scheduledJobs: Map<string, ScheduledJob> = new Map();
  private runningJobs: Map<string, RunningJob> = new Map();
  private cronJobs: Map<string, cron.ScheduledTask> = new Map();
  private jobQueue: JobQueue;
  private logger: Logger;
  private isRunning: boolean = false;
  private maxConcurrentJobs: number = 10;

  constructor(options?: {
    maxConcurrentJobs?: number;
    queueOptions?: any;
  }) {
    this.maxConcurrentJobs = options?.maxConcurrentJobs || 10;
    this.jobQueue = new JobQueue(options?.queueOptions);
    this.logger = new Logger('JobScheduler');
  }

  /**
   * スケジューラーを開始
   */
  public async start(): Promise<void> {
    if (this.isRunning) {
      this.logger.warn('スケジューラーは既に実行中です');
      return;
    }

    this.isRunning = true;
    this.logger.info('ジョブスケジューラーを開始しました');

    // 既存のスケジュールを復元
    await this.restoreSchedules();
    
    // キューの処理を開始
    await this.jobQueue.start();
    
    // 定期的なヘルスチェック
    this.startHealthCheck();
  }

  /**
   * スケジューラーを停止
   */
  public async stop(): Promise<void> {
    if (!this.isRunning) {
      return;
    }

    this.isRunning = false;
    this.logger.info('ジョブスケジューラーを停止中...');

    // 全てのcronジョブを停止
    for (const [scheduleId, cronJob] of this.cronJobs) {
      cronJob.stop();
      this.logger.debug(`スケジュール停止: ${scheduleId}`);
    }

    // 実行中ジョブの完了を待機
    await this.waitForRunningJobs();
    
    // キューを停止
    await this.jobQueue.stop();
    
    this.logger.info('ジョブスケジューラーを停止しました');
  }

  /**
   * ジョブをスケジュールに登録
   */
  public async scheduleJob(
    jobClass: new () => BaseJob,
    schedule: ScheduleConfig,
    parameters: Record<string, any> = {}
  ): Promise<string> {
    const scheduleId = this.generateScheduleId();
    
    const scheduledJob: ScheduledJob = {
      scheduleId,
      jobClass,
      schedule,
      parameters,
      nextExecution: this.calculateNextExecution(schedule.cronExpression, schedule.timezone),
      executionCount: 0,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    this.scheduledJobs.set(scheduleId, scheduledJob);

    if (schedule.enabled) {
      await this.activateSchedule(scheduleId);
    }

    this.logger.info(`ジョブをスケジュールに登録: ${schedule.name}`, {
      scheduleId,
      cronExpression: schedule.cronExpression,
      nextExecution: scheduledJob.nextExecution
    });

    return scheduleId;
  }

  /**
   * スケジュールを有効化
   */
  private async activateSchedule(scheduleId: string): Promise<void> {
    const scheduledJob = this.scheduledJobs.get(scheduleId);
    if (!scheduledJob) {
      throw new Error(`スケジュールが見つかりません: ${scheduleId}`);
    }

    const cronJob = cron.schedule(
      scheduledJob.schedule.cronExpression,
      async () => {
        await this.executeScheduledJob(scheduleId);
      },
      {
        scheduled: false,
        timezone: scheduledJob.schedule.timezone || 'Asia/Tokyo'
      }
    );

    this.cronJobs.set(scheduleId, cronJob);
    cronJob.start();

    this.logger.debug(`スケジュール有効化: ${scheduleId}`);
  }

  /**
   * スケジュール済みジョブを実行
   */
  private async executeScheduledJob(scheduleId: string): Promise<void> {
    const scheduledJob = this.scheduledJobs.get(scheduleId);
    if (!scheduledJob) {
      this.logger.error(`スケジュールが見つかりません: ${scheduleId}`);
      return;
    }

    // 実行条件チェック
    if (scheduledJob.schedule.condition) {
      const conditionMet = await this.checkCondition(scheduledJob.schedule.condition);
      if (!conditionMet) {
        this.logger.info(`実行条件が満たされていません: ${scheduledJob.schedule.name}`);
        return;
      }
    }

    // 最大実行回数チェック
    if (scheduledJob.schedule.maxExecutions && 
        scheduledJob.executionCount >= scheduledJob.schedule.maxExecutions) {
      this.logger.info(`最大実行回数に達しました: ${scheduledJob.schedule.name}`);
      await this.disableSchedule(scheduleId);
      return;
    }

    // 終了日時チェック
    if (scheduledJob.schedule.endDate && new Date() > scheduledJob.schedule.endDate) {
      this.logger.info(`終了日時を過ぎました: ${scheduledJob.schedule.name}`);
      await this.disableSchedule(scheduleId);
      return;
    }

    // ジョブを実行キューに追加
    const request: JobExecutionRequest = {
      jobClass: scheduledJob.jobClass,
      parameters: scheduledJob.parameters,
      userId: 'system'
    };

    await this.executeJob(request, 'scheduled', scheduleId);

    // 実行回数を更新
    scheduledJob.executionCount++;
    scheduledJob.lastExecution = new Date();
    scheduledJob.nextExecution = this.calculateNextExecution(
      scheduledJob.schedule.cronExpression,
      scheduledJob.schedule.timezone
    );
    scheduledJob.updatedAt = new Date();
  }

  /**
   * ジョブを即座に実行
   */
  public async executeJobNow(request: JobExecutionRequest): Promise<string> {
    return await this.executeJob(request, 'manual');
  }

  /**
   * ジョブを遅延実行
   */
  public async executeJobLater(request: JobExecutionRequest): Promise<string> {
    if (request.delay) {
      setTimeout(async () => {
        await this.executeJob(request, 'delayed');
      }, request.delay);
      
      return `delayed-${Date.now()}`;
    }
    
    if (request.scheduledAt) {
      const delay = request.scheduledAt.getTime() - Date.now();
      if (delay > 0) {
        setTimeout(async () => {
          await this.executeJob(request, 'delayed');
        }, delay);
        
        return `scheduled-${Date.now()}`;
      }
    }

    // 即座実行
    return await this.executeJob(request, 'manual');
  }

  /**
   * ジョブを実行
   */
  private async executeJob(
    request: JobExecutionRequest,
    executionType: 'scheduled' | 'manual' | 'delayed',
    scheduleId?: string
  ): Promise<string> {
    // 同時実行数チェック
    if (this.runningJobs.size >= this.maxConcurrentJobs) {
      this.logger.warn('最大同時実行数に達しています。キューに追加します。');
      return await this.jobQueue.enqueue(request, executionType, scheduleId);
    }

    const executionId = this.generateExecutionId();
    const jobInstance = new request.jobClass();

    const context: JobContext = {
      jobId: jobInstance.getConfig().name,
      executionId,
      startedAt: new Date(),
      userId: request.userId,
      parameters: request.parameters || {},
      environment: process.env.NODE_ENV as any || 'development',
      dryRun: request.dryRun || false
    };

    const runningJob: RunningJob = {
      executionId,
      jobInstance,
      context,
      startedAt: new Date(),
      executionType,
      scheduleId
    };

    this.runningJobs.set(executionId, runningJob);

    this.logger.info(`ジョブ実行開始: ${context.jobId}`, {
      executionId,
      executionType,
      scheduleId
    });

    // 非同期でジョブを実行
    this.runJobAsync(runningJob);

    return executionId;
  }

  /**
   * ジョブを非同期実行
   */
  private async runJobAsync(runningJob: RunningJob): Promise<void> {
    try {
      const result = await runningJob.jobInstance.run(runningJob.context);
      
      this.logger.info(`ジョブ実行完了: ${runningJob.context.jobId}`, {
        executionId: runningJob.executionId,
        success: result.success,
        duration: result.duration
      });

      // 実行履歴を保存
      await this.saveExecutionHistory(runningJob, result);

    } catch (error) {
      this.logger.error(`ジョブ実行エラー: ${runningJob.context.jobId}`, {
        executionId: runningJob.executionId,
        error: error.message
      });

    } finally {
      // 実行中ジョブから削除
      this.runningJobs.delete(runningJob.executionId);
      
      // キューから次のジョブを実行
      await this.processNextQueuedJob();
    }
  }

  /**
   * 次のキューイングされたジョブを処理
   */
  private async processNextQueuedJob(): Promise<void> {
    if (this.runningJobs.size >= this.maxConcurrentJobs) {
      return;
    }

    const nextJob = await this.jobQueue.dequeue();
    if (nextJob) {
      await this.executeJob(nextJob.request, nextJob.executionType, nextJob.scheduleId);
    }
  }

  /**
   * 実行条件をチェック
   */
  private async checkCondition(condition: ScheduleCondition): Promise<boolean> {
    try {
      const timeout = condition.timeout || 30000; // 30秒デフォルト
      
      return await Promise.race([
        condition.check(),
        new Promise<boolean>((_, reject) => 
          setTimeout(() => reject(new Error('条件チェックタイムアウト')), timeout)
        )
      ]);
      
    } catch (error) {
      this.logger.warn(`実行条件チェックに失敗: ${condition.description}`, {
        error: error.message
      });
      return false;
    }
  }

  /**
   * スケジュールを無効化
   */
  public async disableSchedule(scheduleId: string): Promise<void> {
    const scheduledJob = this.scheduledJobs.get(scheduleId);
    if (!scheduledJob) {
      throw new Error(`スケジュールが見つかりません: ${scheduleId}`);
    }

    scheduledJob.schedule.enabled = false;
    scheduledJob.updatedAt = new Date();

    const cronJob = this.cronJobs.get(scheduleId);
    if (cronJob) {
      cronJob.stop();
      this.cronJobs.delete(scheduleId);
    }

    this.logger.info(`スケジュール無効化: ${scheduledJob.schedule.name}`);
  }

  /**
   * ジョブをキャンセル
   */
  public async cancelJob(executionId: string): Promise<boolean> {
    const runningJob = this.runningJobs.get(executionId);
    if (!runningJob) {
      return false;
    }

    await runningJob.jobInstance.cancel();
    this.runningJobs.delete(executionId);

    this.logger.info(`ジョブキャンセル: ${runningJob.context.jobId}`, {
      executionId
    });

    return true;
  }

  /**
   * 統計情報を取得
   */
  public getStatistics(): SchedulerStatistics {
    const activeSchedules = Array.from(this.scheduledJobs.values())
      .filter(job => job.schedule.enabled).length;

    // 今日の実行履歴から統計を計算（実装は省略）
    const todayStats = this.calculateTodayStatistics();

    return {
      totalSchedules: this.scheduledJobs.size,
      activeSchedules,
      runningJobs: this.runningJobs.size,
      queuedJobs: this.jobQueue.getQueueSize(),
      todayExecutions: todayStats.executions,
      todaySuccesses: todayStats.successes,
      todayFailures: todayStats.failures,
      averageExecutionTime: todayStats.averageTime,
      lastExecutionTime: todayStats.lastExecution
    };
  }

  /**
   * 実行中ジョブ一覧を取得
   */
  public getRunningJobs(): RunningJob[] {
    return Array.from(this.runningJobs.values());
  }

  /**
   * スケジュール一覧を取得
   */
  public getScheduledJobs(): ScheduledJob[] {
    return Array.from(this.scheduledJobs.values());
  }

  // プライベートメソッド（実装詳細は省略）
  private generateScheduleId(): string {
    return `schedule-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private generateExecutionId(): string {
    return `exec-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private calculateNextExecution(cronExpression: string, timezone?: string): Date {
    // cron式から次回実行時刻を計算
    const parser = require('cron-parser');
    const interval = parser.parseExpression(cronExpression, {
      tz: timezone || 'Asia/Tokyo'
    });
    return interval.next().toDate();
  }

  private async restoreSchedules(): Promise<void> {
    // データベースからスケジュール情報を復元
    // 実装は省略
  }

  private async saveExecutionHistory(runningJob: RunningJob, result: JobResult): Promise<void> {
    // 実行履歴をデータベースに保存
    // 実装は省略
  }

  private calculateTodayStatistics(): any {
    // 今日の統計を計算
    // 実装は省略
    return {
      executions: 0,
      successes: 0,
      failures: 0,
      averageTime: 0,
      lastExecution: undefined
    };
  }

  private async waitForRunningJobs(): Promise<void> {
    // 実行中ジョブの完了を待機
    const maxWaitTime = 300000; // 5分
    const startTime = Date.now();

    while (this.runningJobs.size > 0 && (Date.now() - startTime) < maxWaitTime) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }

    if (this.runningJobs.size > 0) {
      this.logger.warn(`${this.runningJobs.size}個のジョブが実行中のまま停止します`);
    }
  }

  private startHealthCheck(): void {
    // 定期的なヘルスチェック
    setInterval(() => {
      this.performHealthCheck();
    }, 60000); // 1分間隔
  }

  private performHealthCheck(): void {
    // ヘルスチェック実行
    const stats = this.getStatistics();
    this.logger.debug('ヘルスチェック', stats);
  }
}
```

---

## 4. 実装例

### 4.1 スケジューラーの初期化と使用例

```typescript
// スケジューラーの初期化
const scheduler = new JobScheduler({
  maxConcurrentJobs: 5
});

// スケジューラー開始
await scheduler.start();

// 定期実行ジョブの登録
const scheduleId = await scheduler.scheduleJob(
  SkillStatisticsJob,
  {
    name: 'daily-skill-statistics',
    cronExpression: '0 2 * * *', // 毎日午前2時
    timezone: 'Asia/Tokyo',
    enabled: true,
    condition: {
      check: async () => {
        // 平日のみ実行
        const today = new Date();
        const dayOfWeek = today.getDay();
        return dayOfWeek >= 1 && dayOfWeek <= 5;
      },
      description: '平日のみ実行'
    }
  },
  {
    targetDate: new Date().toISOString().split('T')[0]
  }
);

// 即座実行
const executionId = await scheduler.executeJobNow({
  jobClass: SkillStatisticsJob,
  parameters: { force: true },
  userId: 'admin',
  dryRun: false
});

// 遅延実行（1時間後）
await scheduler.executeJobLater({
  jobClass: CleanupJob,
  delay: 3600000, // 1時間
  parameters: { olderThan: '30d' }
});

// 統計情報取得
const stats = scheduler.getStatistics();
console.log('スケジューラー統計:', stats);

// スケジューラー停止
await scheduler.stop();
```

### 4.2 カスタム実行条件の例

```typescript
// データベース接続チェック
const dbCondition: ScheduleCondition = {
  check: async () => {
    try {
      await database.ping();
      return true;
    } catch {
      return false;
    }
  },
  description: 'データベース接続確認',
  timeout: 10000
};

// 外部API可用性チェック
const apiCondition: ScheduleCondition = {
  check: async () => {
    try {
      const response = await fetch('https://api.example.com/health');
      return response.ok;
    } catch {
      return false;
    }
  },
  description: '外部API可用性確認',
  timeout: 15000
};

// 複合条件
const combinedCondition: ScheduleCondition = {
  check: async () => {
    const dbOk = await dbCondition.check();
    const apiOk = await apiCondition.check();
    return dbOk && apiOk;
  },
  description: 'データベースと外部API両方の可用性確認',
  timeout: 20000
};
```

---

## 5. テスト仕様

### 5.1 単体テスト

```typescript
describe('JobScheduler', () => {
  let scheduler: JobScheduler;

  beforeEach(async () => {
    scheduler = new JobScheduler({ maxConcurrentJobs: 2 });
    await scheduler.start();
  });

  afterEach(async () => {
    await scheduler.stop();
  });

  describe('スケジュール登録', () => {
    test('ジョブが正常にスケジュールされる', async () => {
      const scheduleId = await scheduler.scheduleJob(
        TestJob,
        {
          name: 'test-schedule',
          cronExpression: '0 0 * * *',
          enabled: true
        }
      );

      expect(scheduleId).toBeDefined();
      
      const scheduledJobs = scheduler.getScheduledJobs();
      expect(scheduledJobs).toHaveLength(1);
      expect(scheduledJobs[0].scheduleId).toBe(scheduleId);
    });

    test('無効なcron式でエラーが発生する', async () => {
      await expect(scheduler.scheduleJob(
        TestJob,
        {
          name: 'invalid-schedule',
          cronExpression: 'invalid-cron',
          enabled: true
        }
      )).rejects.toThrow();
    });
  });

  describe('即座実行', () => {
    test('ジョブが即座に実行される', async () => {
      const executionId = await scheduler.executeJobNow({
        jobClass: TestJob,
        parameters: { test: true }
      });

      expect(executionId).toBeDefined();
      
      // 実行完了まで待機
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      const runningJobs = scheduler.getRunningJobs();
      expect(runningJobs.find(job => job.executionId === executionId)).toBeUndefined();
    });
  });

  describe('同時実行制御', () => {
    test('最大同時実行数が制御される', async () => {
      // 3つのジョブを同時実行（最大2つまで）
      const promises = [
        scheduler.executeJobNow({ jobClass: LongRunningTestJob }),
        scheduler.executeJobNow({ jobClass: LongRunningTestJob }),
        scheduler.executeJobNow({ jobClass: LongRunningTestJob })
      ];

      await Promise.all(promises);

      const runningJobs = scheduler.getRunningJobs();
      expect(runningJobs.length).toBeLessThanOrEqual(2);
    });
  });
});
```

### 5.2 統合テスト

```typescript
describe('JobScheduler 統合テスト', () => {
  test('実際のcronスケジュールでジョブが実行される', async () => {
    const scheduler = new JobScheduler();
    await scheduler.start();

    let executionCount = 0;
    
    class CounterJob extends BaseJob {
      constructor() {
        super({
          name: 'counter-job',
          priority: 'normal',
          timeout: 5000,
          retry: { maxAttempts: 1, delay: 1000, exponentialBackoff: false },
          concurrency: { allowConcurrent: true },
          notifications: { onSuccess: false, onFailure: false }
        });
      }

      protected async execute(): Promise<Partial<JobResult>> {
        executionCount++;
        return { successCount: 1, message: 'カウンター更新' };
      }
    }

    // 5秒間隔で実行
    await scheduler.scheduleJob(
      CounterJob,
      {
        name: 'counter-schedule',
        cronExpression: '*/5 * * * * *', // 5秒間隔
        enabled: true
      }
    );

    // 15秒待機（3回実行されるはず）
    await new Promise(resolve => setTimeout(resolve, 15000));

    expect(executionCount).toBeGreaterThanOrEqual(2);
    expect(executionCount).toBeLessThanOrEqual(4);

    await scheduler.stop();
  });
});
```

---

## 6. パフォーマンス要件

### 6.1 スケジューリング性能

- **スケジュール登録**: 100ms以内
- **即座実行**: 50ms以内（キューイング時間除く）
- **cron評価**: 10ms以内

### 6.2 同時実行性能

- **最大同時実行ジョブ数**: 設定可能（デフォルト10個）
- **キュー処理**: 1秒以内に次のジョブを開始
- **メモリ使用量**: ジョブあたり50MB以下

### 6.3 監視性能

- **統計情報取得**: 100ms以内
- **実行状況更新**: リアルタイム
- **ログ出力**: 非同期処理

---

## 7. 運用要件

### 7.1 設定管理

- **環境変数**: タイムゾーン、最大同時実行数等
- **設定ファイル**: ス
