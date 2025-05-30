# BatchLogger バッチログ管理定義書

## 1. 基本情報

- **部品名**: BatchLogger
- **カテゴリ**: バックエンド - バッチユーティリティ
- **責務**: バッチ処理専用のログ管理・出力機能
- **依存関係**: BatchTypes
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 概要

### 2.1 目的

BatchLoggerは、バッチ処理における包括的なログ管理機能を提供します。実行ログ、エラーログ、パフォーマンスメトリクス、監査ログなどを統一的に管理し、運用・監視・デバッグを支援します。

### 2.2 特徴

- 構造化ログ出力
- 複数出力先対応（ファイル、データベース、外部サービス）
- ログレベル制御
- パフォーマンス計測
- 自動ローテーション
- 検索・フィルタリング機能

---

## 3. インターフェース定義

### 3.1 基本インターフェース

```typescript
import { LogLevel, JobContext, JobResult, JobError } from '@/types/BatchTypes';

/**
 * ログエントリ
 */
interface LogEntry {
  /** ログID */
  id: string;
  
  /** タイムスタンプ */
  timestamp: Date;
  
  /** ログレベル */
  level: LogLevel;
  
  /** メッセージ */
  message: string;
  
  /** ジョブコンテキスト */
  context?: JobContext;
  
  /** 追加データ */
  data?: Record<string, any>;
  
  /** エラー情報 */
  error?: JobError;
  
  /** メトリクス */
  metrics?: LogMetrics;
  
  /** タグ */
  tags?: string[];
  
  /** ソース */
  source?: string;
  
  /** トレースID */
  traceId?: string;
  
  /** スパンID */
  spanId?: string;
}

/**
 * ログメトリクス
 */
interface LogMetrics {
  /** 実行時間（ミリ秒） */
  duration?: number;
  
  /** メモリ使用量（MB） */
  memoryUsage?: number;
  
  /** CPU使用率（%） */
  cpuUsage?: number;
  
  /** 処理件数 */
  processedCount?: number;
  
  /** カスタムメトリクス */
  custom?: Record<string, number>;
}

/**
 * ログ設定
 */
interface LoggerConfig {
  /** ログレベル */
  level: LogLevel;
  
  /** 出力先設定 */
  outputs: LogOutput[];
  
  /** フォーマット設定 */
  format: LogFormat;
  
  /** ローテーション設定 */
  rotation?: RotationConfig;
  
  /** フィルタ設定 */
  filters?: LogFilter[];
  
  /** バッファ設定 */
  buffer?: BufferConfig;
  
  /** 非同期出力 */
  async?: boolean;
  
  /** エラー時の動作 */
  errorHandling?: ErrorHandlingConfig;
}

/**
 * ログ出力先
 */
interface LogOutput {
  /** 出力タイプ */
  type: 'console' | 'file' | 'database' | 'elasticsearch' | 'cloudwatch' | 'custom';
  
  /** 出力先設定 */
  config: OutputConfig;
  
  /** 有効フラグ */
  enabled: boolean;
  
  /** 最小ログレベル */
  minLevel?: LogLevel;
  
  /** 最大ログレベル */
  maxLevel?: LogLevel;
  
  /** フォーマッター */
  formatter?: LogFormatter;
}

/**
 * BatchLoggerメインクラス
 */
export class BatchLogger {
  private config: LoggerConfig;
  private outputs: Map<string, LogOutput>;
  private buffer: LogEntry[];
  private timers: Map<string, number>;
  private metrics: Map<string, LogMetrics>;

  constructor(config: LoggerConfig) {
    this.config = config;
    this.outputs = new Map();
    this.buffer = [];
    this.timers = new Map();
    this.metrics = new Map();
    
    this.initializeOutputs();
  }

  /**
   * デバッグログ出力
   */
  debug(message: string, data?: any, context?: JobContext): void {
    this.log('debug', message, data, context);
  }

  /**
   * 情報ログ出力
   */
  info(message: string, data?: any, context?: JobContext): void {
    this.log('info', message, data, context);
  }

  /**
   * 警告ログ出力
   */
  warn(message: string, data?: any, context?: JobContext): void {
    this.log('warn', message, data, context);
  }

  /**
   * エラーログ出力
   */
  error(message: string, error?: Error | JobError, context?: JobContext): void {
    this.log('error', message, { error }, context);
  }

  /**
   * 致命的エラーログ出力
   */
  fatal(message: string, error?: Error | JobError, context?: JobContext): void {
    this.log('fatal', message, { error }, context);
  }

  /**
   * ジョブ開始ログ
   */
  jobStart(context: JobContext): void {
    this.startTimer(context.executionId);
    this.info(`ジョブ開始: ${context.jobId}`, {
      executionId: context.executionId,
      parameters: context.parameters,
      executionType: context.executionType
    }, context);
  }

  /**
   * ジョブ完了ログ
   */
  jobComplete(context: JobContext, result: JobResult): void {
    const duration = this.endTimer(context.executionId);
    
    if (result.success) {
      this.info(`ジョブ完了: ${context.jobId}`, {
        executionId: context.executionId,
        duration,
        processedCount: result.processedCount,
        successCount: result.successCount,
        failureCount: result.failureCount
      }, context);
    } else {
      this.error(`ジョブ失敗: ${context.jobId}`, result.error, context);
    }
  }

  /**
   * 進捗ログ
   */
  progress(context: JobContext, current: number, total: number, message?: string): void {
    const percentage = Math.round((current / total) * 100);
    this.info(message || `進捗: ${percentage}%`, {
      executionId: context.executionId,
      current,
      total,
      percentage
    }, context);
  }

  /**
   * メトリクス記録
   */
  recordMetrics(key: string, metrics: LogMetrics): void {
    this.metrics.set(key, metrics);
    this.debug('メトリクス記録', { key, metrics });
  }

  /**
   * パフォーマンス計測開始
   */
  startTimer(key: string): void {
    this.timers.set(key, Date.now());
  }

  /**
   * パフォーマンス計測終了
   */
  endTimer(key: string): number {
    const startTime = this.timers.get(key);
    if (!startTime) return 0;
    
    const duration = Date.now() - startTime;
    this.timers.delete(key);
    return duration;
  }

  /**
   * ログ検索
   */
  async search(query: LogSearchQuery): Promise<LogEntry[]> {
    // 実装: ログ検索機能
    return [];
  }

  /**
   * ログ統計取得
   */
  async getStatistics(period: TimePeriod): Promise<LogStatistics> {
    // 実装: ログ統計機能
    return {} as LogStatistics;
  }

  /**
   * ログ出力
   */
  private log(level: LogLevel, message: string, data?: any, context?: JobContext): void {
    if (!this.shouldLog(level)) return;

    const entry: LogEntry = {
      id: this.generateLogId(),
      timestamp: new Date(),
      level,
      message,
      context,
      data,
      traceId: context?.traceId,
      source: 'BatchLogger'
    };

    if (this.config.async) {
      this.buffer.push(entry);
      this.flushBufferIfNeeded();
    } else {
      this.writeToOutputs(entry);
    }
  }

  /**
   * ログレベル判定
   */
  private shouldLog(level: LogLevel): boolean {
    const levels: LogLevel[] = ['debug', 'info', 'warn', 'error', 'fatal'];
    const currentLevelIndex = levels.indexOf(this.config.level);
    const logLevelIndex = levels.indexOf(level);
    
    return logLevelIndex >= currentLevelIndex;
  }

  /**
   * 出力先への書き込み
   */
  private async writeToOutputs(entry: LogEntry): Promise<void> {
    const promises = Array.from(this.outputs.values())
      .filter(output => output.enabled && this.shouldOutputToTarget(entry, output))
      .map(output => this.writeToOutput(entry, output));

    await Promise.allSettled(promises);
  }

  /**
   * 個別出力先への書き込み
   */
  private async writeToOutput(entry: LogEntry, output: LogOutput): Promise<void> {
    try {
      const formatter = output.formatter || this.getDefaultFormatter(output.type);
      const formattedEntry = formatter.format(entry);

      switch (output.type) {
        case 'console':
          console.log(formattedEntry);
          break;
        case 'file':
          await this.writeToFile(formattedEntry, output.config);
          break;
        case 'database':
          await this.writeToDatabase(entry, output.config);
          break;
        case 'elasticsearch':
          await this.writeToElasticsearch(entry, output.config);
          break;
        case 'cloudwatch':
          await this.writeToCloudWatch(entry, output.config);
          break;
        case 'custom':
          await this.writeToCustomOutput(entry, output.config);
          break;
      }
    } catch (error) {
      this.handleOutputError(error, output);
    }
  }

  /**
   * ファイル出力
   */
  private async writeToFile(formattedEntry: string, config: FileOutputConfig): Promise<void> {
    const fs = await import('fs/promises');
    const path = await import('path');
    
    const logFile = this.getLogFilePath(config);
    await fs.appendFile(logFile, formattedEntry + '\n');
    
    // ローテーション処理
    if (this.config.rotation) {
      await this.rotateLogFileIfNeeded(logFile);
    }
  }

  /**
   * データベース出力
   */
  private async writeToDatabase(entry: LogEntry, config: DatabaseOutputConfig): Promise<void> {
    // 実装: データベースへのログ出力
  }

  /**
   * Elasticsearch出力
   */
  private async writeToElasticsearch(entry: LogEntry, config: ElasticsearchOutputConfig): Promise<void> {
    // 実装: Elasticsearchへのログ出力
  }

  /**
   * CloudWatch出力
   */
  private async writeToCloudWatch(entry: LogEntry, config: CloudWatchOutputConfig): Promise<void> {
    // 実装: CloudWatchへのログ出力
  }

  /**
   * カスタム出力
   */
  private async writeToCustomOutput(entry: LogEntry, config: CustomOutputConfig): Promise<void> {
    if (config.handler) {
      await config.handler(entry);
    }
  }

  /**
   * バッファフラッシュ
   */
  private async flushBufferIfNeeded(): Promise<void> {
    if (!this.config.buffer) return;
    
    const shouldFlush = 
      this.buffer.length >= this.config.buffer.maxSize ||
      (this.config.buffer.flushInterval && this.isFlushIntervalExceeded());

    if (shouldFlush) {
      await this.flushBuffer();
    }
  }

  /**
   * バッファ全体フラッシュ
   */
  private async flushBuffer(): Promise<void> {
    const entries = [...this.buffer];
    this.buffer = [];

    for (const entry of entries) {
      await this.writeToOutputs(entry);
    }
  }

  /**
   * ログID生成
   */
  private generateLogId(): string {
    return `log_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 出力先初期化
   */
  private initializeOutputs(): void {
    this.config.outputs.forEach((output, index) => {
      this.outputs.set(`output_${index}`, output);
    });
  }

  /**
   * デフォルトフォーマッター取得
   */
  private getDefaultFormatter(type: string): LogFormatter {
    switch (type) {
      case 'console':
        return new ConsoleFormatter();
      case 'file':
        return new FileFormatter();
      case 'database':
        return new DatabaseFormatter();
      default:
        return new JSONFormatter();
    }
  }

  /**
   * 出力対象判定
   */
  private shouldOutputToTarget(entry: LogEntry, output: LogOutput): boolean {
    if (output.minLevel && !this.isLevelAbove(entry.level, output.minLevel)) {
      return false;
    }
    
    if (output.maxLevel && !this.isLevelBelow(entry.level, output.maxLevel)) {
      return false;
    }
    
    return true;
  }

  /**
   * ログレベル比較
   */
  private isLevelAbove(level: LogLevel, minLevel: LogLevel): boolean {
    const levels: LogLevel[] = ['debug', 'info', 'warn', 'error', 'fatal'];
    return levels.indexOf(level) >= levels.indexOf(minLevel);
  }

  private isLevelBelow(level: LogLevel, maxLevel: LogLevel): boolean {
    const levels: LogLevel[] = ['debug', 'info', 'warn', 'error', 'fatal'];
    return levels.indexOf(level) <= levels.indexOf(maxLevel);
  }

  /**
   * エラーハンドリング
   */
  private handleOutputError(error: Error, output: LogOutput): void {
    if (this.config.errorHandling?.fallbackToConsole) {
      console.error(`ログ出力エラー (${output.type}):`, error);
    }
    
    if (this.config.errorHandling?.disableOnError) {
      output.enabled = false;
    }
  }
}
```

---

## 4. フォーマッター実装

### 4.1 基本フォーマッター

```typescript
/**
 * ログフォーマッター基底クラス
 */
abstract class LogFormatter {
  abstract format(entry: LogEntry): string;
}

/**
 * JSONフォーマッター
 */
class JSONFormatter extends LogFormatter {
  format(entry: LogEntry): string {
    return JSON.stringify({
      timestamp: entry.timestamp.toISOString(),
      level: entry.level.toUpperCase(),
      message: entry.message,
      jobId: entry.context?.jobId,
      executionId: entry.context?.executionId,
      traceId: entry.traceId,
      data: entry.data,
      error: entry.error,
      metrics: entry.metrics
    });
  }
}

/**
 * コンソールフォーマッター
 */
class ConsoleFormatter extends LogFormatter {
  format(entry: LogEntry): string {
    const timestamp = entry.timestamp.toISOString();
    const level = entry.level.toUpperCase().padEnd(5);
    const jobInfo = entry.context ? `[${entry.context.jobId}]` : '';
    
    let message = `${timestamp} ${level} ${jobInfo} ${entry.message}`;
    
    if (entry.data) {
      message += ` | Data: ${JSON.stringify(entry.data)}`;
    }
    
    if (entry.error) {
      message += ` | Error: ${entry.error.message}`;
    }
    
    return message;
  }
}

/**
 * ファイルフォーマッター
 */
class FileFormatter extends LogFormatter {
  format(entry: LogEntry): string {
    const timestamp = entry.timestamp.toISOString();
    const level = entry.level.toUpperCase();
    const jobId = entry.context?.jobId || 'SYSTEM';
    const executionId = entry.context?.executionId || '';
    
    const parts = [
      timestamp,
      level,
      jobId,
      executionId,
      entry.message
    ];
    
    if (entry.data) {
      parts.push(JSON.stringify(entry.data));
    }
    
    if (entry.error) {
      parts.push(`ERROR: ${entry.error.message}`);
      if (entry.error.stack) {
        parts.push(`STACK: ${entry.error.stack}`);
      }
    }
    
    return parts.join(' | ');
  }
}

/**
 * データベースフォーマッター
 */
class DatabaseFormatter extends LogFormatter {
  format(entry: LogEntry): string {
    // データベース挿入用のオブジェクトを返す
    return JSON.stringify({
      id: entry.id,
      timestamp: entry.timestamp,
      level: entry.level,
      message: entry.message,
      job_id: entry.context?.jobId,
      execution_id: entry.context?.executionId,
      trace_id: entry.traceId,
      data: entry.data ? JSON.stringify(entry.data) : null,
      error_code: entry.error?.code,
      error_message: entry.error?.message,
      error_stack: entry.error?.stack,
      metrics: entry.metrics ? JSON.stringify(entry.metrics) : null,
      tags: entry.tags ? entry.tags.join(',') : null
    });
  }
}
```

---

## 5. 設定例

### 5.1 基本設定

```typescript
const loggerConfig: LoggerConfig = {
  level: 'info',
  async: true,
  format: {
    type: 'json',
    includeStackTrace: true,
    includeMetrics: true
  },
  outputs: [
    {
      type: 'console',
      enabled: true,
      minLevel: 'warn',
      config: {},
      formatter: new ConsoleFormatter()
    },
    {
      type: 'file',
      enabled: true,
      config: {
        filePath: '/var/log/batch/batch.log',
        maxSize: '100MB',
        maxFiles: 10
      },
      formatter: new FileFormatter()
    },
    {
      type: 'database',
      enabled: true,
      minLevel: 'error',
      config: {
        connectionString: 'postgresql://...',
        tableName: 'batch_logs'
      }
    }
  ],
  rotation: {
    type: 'daily',
    maxSize: '100MB',
    maxFiles: 30,
    compress: true
  },
  buffer: {
    maxSize: 1000,
    flushInterval: 5000
  },
  errorHandling: {
    fallbackToConsole: true,
    disableOnError: false,
    retryAttempts: 3
  }
};

const logger = new BatchLogger(loggerConfig);
```

### 5.2 使用例

```typescript
// ジョブ実行時の使用例
class SkillStatisticsJob extends BaseJob {
  private logger: BatchLogger;

  constructor() {
    super();
    this.logger = new BatchLogger(loggerConfig);
  }

  async execute(context: JobContext): Promise<JobResult> {
    this.logger.jobStart(context);
    
    try {
      this.logger.info('統計処理開始', { targetDate: new Date() }, context);
      
      // 処理実行
      const skills = await this.getSkills();
      this.logger.info(`スキルデータ取得完了: ${skills.length}件`, null, context);
      
      let processed = 0;
      for (const skill of skills) {
        try {
          await this.processSkill(skill);
          processed++;
          
          // 進捗ログ
          if (processed % 100 === 0) {
            this.logger.progress(context, processed, skills.length);
          }
        } catch (error) {
          this.logger.error(`スキル処理エラー: ${skill.id}`, error, context);
        }
      }
      
      const result: JobResult = {
        success: true,
        processedCount: skills.length,
        successCount: processed,
        failureCount: skills.length - processed,
        duration: 0,
        message: '統計処理完了'
      };
      
      this.logger.jobComplete(context, result);
      return result;
      
    } catch (error) {
      const result: JobResult = {
        success: false,
        processedCount: 0,
        successCount: 0,
        failureCount: 0,
        duration: 0,
        message: '統計処理失敗',
        error: {
          code: 'STATISTICS_ERROR',
          message: error.message,
          stack: error.stack
        }
      };
      
      this.logger.jobComplete(context, result);
      return result;
    }
  }
}
```

---

## 6. 監視・運用機能

### 6.1 ログ検索・分析

```typescript
/**
 * ログ検索クエリ
 */
interface LogSearchQuery {
  /** 開始日時 */
  startDate?: Date;
  
  /** 終了日時 */
  endDate?: Date;
  
  /** ログレベル */
  levels?: LogLevel[];
  
  /** ジョブID */
  jobIds?: string[];
  
  /** メッセージ検索 */
  messagePattern?: string;
  
  /** エラーコード */
  errorCodes?: string[];
  
  /** タグ */
  tags?: string[];
  
  /** 制限件数 */
  limit?: number;
  
  /** オフセット */
  offset?: number;
  
  /** ソート順 */
  sortBy?: 'timestamp' | 'level' | 'jobId';
  
  /** ソート方向 */
  sortOrder?: 'asc' | 'desc';
}

/**
 * ログ統計
 */
interface LogStatistics {
  /** 期間 */
  period: TimePeriod;
  
  /** 総ログ数 */
  totalLogs: number;
  
  /** レベル別統計 */
  byLevel: Record<LogLevel, number>;
  
  /** ジョブ別統計 */
  byJob: Record<string, JobLogStatistics>;
  
  /** エラー統計 */
  errorStatistics: ErrorStatistics;
  
  /** パフォーマンス統計 */
  performanceStatistics: PerformanceStatistics;
}

/**
 * ログ分析ツール
 */
class LogAnalyzer {
  constructor(private logger: BatchLogger) {}

  /**
   * エラー傾向分析
   */
  async analyzeErrorTrends(period: TimePeriod): Promise<ErrorTrendAnalysis> {
    const query: LogSearchQuery = {
      startDate: period.start,
      endDate: period.end,
      levels: ['error', 'fatal']
    };
    
    const errorLogs = await this.logger.search(query);
    
    return {
      totalErrors: errorLogs.length,
      errorsByCode: this.groupByErrorCode(errorLogs),
      errorsByJob: this.groupByJob(errorLogs),
      timeDistribution: this.analyzeTimeDistribution(errorLogs),
      recommendations: this.generateRecommendations(errorLogs)
    };
  }

  /**
   * パフォーマンス分析
   */
  async analyzePerformance(period: TimePeriod): Promise<PerformanceAnalysis> {
    // 実装: パフォーマンス分析
    return {} as PerformanceAnalysis;
  }

  /**
   * アラート生成
   */
  async generateAlerts(): Promise<LogAlert[]> {
    // 実装: アラート生成
    return [];
  }
}
```

---

## 7. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 8. 関連ドキュメント

- [共通部品定義書](../../../共通部品定義書.md)
- [BaseJob 定義書](../jobs/BaseJob.md)
- [JobScheduler 定義書](../schedulers/JobScheduler.md)
- [BatchTypes 型定義書](../../shared/types/BatchTypes.md)

---

このBatchLoggerにより、バッチ処理の包括的なログ管理と運用監視を実現します。
