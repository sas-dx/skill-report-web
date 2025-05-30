# FileHandler ファイル処理共通部品定義書

## 1. 基本情報

- **部品名**: FileHandler
- **カテゴリ**: 共通ユーティリティ - ファイル処理
- **責務**: ファイルのインポート・エクスポート・変換処理
- **依存関係**: なし（基盤ユーティリティ）
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. 概要

### 2.1 目的

FileHandlerは、Webアプリケーションにおけるファイルの読み込み、書き出し、形式変換を統一的に処理する共通部品です。CSV、Excel、JSON、PDF等の多様なファイル形式に対応し、ブラウザ環境での安全なファイル操作を提供します。

### 2.2 特徴

- 多様なファイル形式対応（CSV、Excel、JSON、PDF、画像）
- ブラウザ環境での安全なファイル処理
- 大容量ファイルのストリーミング処理
- 進捗表示とキャンセル機能
- エラーハンドリングとバリデーション
- TypeScript型安全性

---

## 3. インターフェース定義

### 3.1 基本インターフェース

```typescript
/**
 * ファイル処理設定
 */
interface FileHandlerConfig {
  /** 最大ファイルサイズ（バイト） */
  maxFileSize: number;
  
  /** 許可するファイル形式 */
  allowedTypes: string[];
  
  /** エンコーディング */
  encoding: 'utf-8' | 'shift-jis' | 'euc-jp';
  
  /** チャンクサイズ（ストリーミング処理用） */
  chunkSize: number;
  
  /** 進捗コールバック */
  onProgress?: (progress: number) => void;
  
  /** エラーコールバック */
  onError?: (error: FileError) => void;
}

/**
 * ファイル情報
 */
interface FileInfo {
  /** ファイル名 */
  name: string;
  
  /** ファイルサイズ */
  size: number;
  
  /** MIMEタイプ */
  type: string;
  
  /** 最終更新日 */
  lastModified: Date;
  
  /** ファイルハッシュ */
  hash?: string;
}

/**
 * インポート結果
 */
interface ImportResult<T = any> {
  /** 成功フラグ */
  success: boolean;
  
  /** インポートされたデータ */
  data: T[];
  
  /** 処理件数 */
  totalCount: number;
  
  /** 成功件数 */
  successCount: number;
  
  /** エラー件数 */
  errorCount: number;
  
  /** エラー詳細 */
  errors: ImportError[];
  
  /** 処理時間（ミリ秒） */
  duration: number;
  
  /** メタデータ */
  metadata?: Record<string, any>;
}

/**
 * エクスポート設定
 */
interface ExportConfig {
  /** ファイル名 */
  filename: string;
  
  /** ファイル形式 */
  format: 'csv' | 'excel' | 'json' | 'pdf';
  
  /** ヘッダー情報 */
  headers?: string[];
  
  /** 列設定 */
  columns?: ColumnConfig[];
  
  /** フィルタ設定 */
  filters?: FilterConfig[];
  
  /** ソート設定 */
  sort?: SortConfig[];
  
  /** ページング設定 */
  pagination?: PaginationConfig;
  
  /** スタイル設定（Excel/PDF用） */
  styling?: StylingConfig;
}

/**
 * FileHandlerメインクラス
 */
export class FileHandler {
  private config: FileHandlerConfig;
  private abortController: AbortController | null = null;

  constructor(config: FileHandlerConfig) {
    this.config = config;
  }

  /**
   * ファイルインポート
   */
  async import<T = any>(
    file: File,
    parser: FileParser<T>,
    options?: ImportOptions
  ): Promise<ImportResult<T>> {
    const startTime = Date.now();
    
    try {
      // ファイル検証
      this.validateFile(file);
      
      // ファイル読み込み
      const content = await this.readFile(file, options?.encoding);
      
      // データ解析
      const parseResult = await parser.parse(content, {
        onProgress: this.config.onProgress,
        signal: this.abortController?.signal
      });
      
      const duration = Date.now() - startTime;
      
      return {
        success: parseResult.errors.length === 0,
        data: parseResult.data,
        totalCount: parseResult.totalCount,
        successCount: parseResult.successCount,
        errorCount: parseResult.errors.length,
        errors: parseResult.errors,
        duration,
        metadata: parseResult.metadata
      };
      
    } catch (error) {
      const duration = Date.now() - startTime;
      
      return {
        success: false,
        data: [],
        totalCount: 0,
        successCount: 0,
        errorCount: 1,
        errors: [{
          row: 0,
          column: '',
          message: error.message,
          code: 'IMPORT_ERROR'
        }],
        duration
      };
    }
  }

  /**
   * ファイルエクスポート
   */
  async export<T = any>(
    data: T[],
    config: ExportConfig,
    formatter: FileFormatter<T>
  ): Promise<void> {
    try {
      // データ前処理
      const processedData = this.preprocessData(data, config);
      
      // ファイル生成
      const content = await formatter.format(processedData, config);
      
      // ダウンロード実行
      await this.downloadFile(content, config.filename, formatter.getMimeType());
      
    } catch (error) {
      this.config.onError?.(new FileError('EXPORT_ERROR', error.message));
      throw error;
    }
  }

  /**
   * ファイル読み込み
   */
  private async readFile(file: File, encoding = 'utf-8'): Promise<string> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      
      reader.onload = (event) => {
        resolve(event.target?.result as string);
      };
      
      reader.onerror = () => {
        reject(new FileError('READ_ERROR', 'ファイルの読み込みに失敗しました'));
      };
      
      reader.onprogress = (event) => {
        if (event.lengthComputable) {
          const progress = (event.loaded / event.total) * 100;
          this.config.onProgress?.(progress);
        }
      };
      
      if (encoding === 'utf-8') {
        reader.readAsText(file, 'UTF-8');
      } else {
        reader.readAsText(file, encoding);
      }
    });
  }

  /**
   * ファイル検証
   */
  private validateFile(file: File): void {
    // ファイルサイズチェック
    if (file.size > this.config.maxFileSize) {
      throw new FileError(
        'FILE_TOO_LARGE',
        `ファイルサイズが上限（${this.formatFileSize(this.config.maxFileSize)}）を超えています`
      );
    }
    
    // ファイル形式チェック
    const isAllowedType = this.config.allowedTypes.some(type => {
      if (type.startsWith('.')) {
        return file.name.toLowerCase().endsWith(type.toLowerCase());
      }
      return file.type === type;
    });
    
    if (!isAllowedType) {
      throw new FileError(
        'INVALID_FILE_TYPE',
        `許可されていないファイル形式です。対応形式: ${this.config.allowedTypes.join(', ')}`
      );
    }
  }

  /**
   * データ前処理
   */
  private preprocessData<T>(data: T[], config: ExportConfig): T[] {
    let processedData = [...data];
    
    // フィルタ適用
    if (config.filters) {
      processedData = this.applyFilters(processedData, config.filters);
    }
    
    // ソート適用
    if (config.sort) {
      processedData = this.applySorting(processedData, config.sort);
    }
    
    // ページング適用
    if (config.pagination) {
      processedData = this.applyPagination(processedData, config.pagination);
    }
    
    return processedData;
  }

  /**
   * ファイルダウンロード
   */
  private async downloadFile(
    content: string | Blob,
    filename: string,
    mimeType: string
  ): Promise<void> {
    const blob = content instanceof Blob ? content : new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    
    try {
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.style.display = 'none';
      
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
    } finally {
      URL.revokeObjectURL(url);
    }
  }

  /**
   * 処理キャンセル
   */
  cancel(): void {
    if (this.abortController) {
      this.abortController.abort();
      this.abortController = null;
    }
  }

  /**
   * ファイルサイズフォーマット
   */
  private formatFileSize(bytes: number): string {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }
    
    return `${size.toFixed(1)} ${units[unitIndex]}`;
  }

  /**
   * フィルタ適用
   */
  private applyFilters<T>(data: T[], filters: FilterConfig[]): T[] {
    return data.filter(item => {
      return filters.every(filter => {
        const value = this.getNestedValue(item, filter.field);
        return this.evaluateFilter(value, filter);
      });
    });
  }

  /**
   * ソート適用
   */
  private applySorting<T>(data: T[], sortConfigs: SortConfig[]): T[] {
    return data.sort((a, b) => {
      for (const config of sortConfigs) {
        const aValue = this.getNestedValue(a, config.field);
        const bValue = this.getNestedValue(b, config.field);
        
        const comparison = this.compareValues(aValue, bValue);
        if (comparison !== 0) {
          return config.direction === 'desc' ? -comparison : comparison;
        }
      }
      return 0;
    });
  }

  /**
   * ページング適用
   */
  private applyPagination<T>(data: T[], pagination: PaginationConfig): T[] {
    const start = (pagination.page - 1) * pagination.limit;
    const end = start + pagination.limit;
    return data.slice(start, end);
  }

  /**
   * ネストした値の取得
   */
  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }

  /**
   * 値の比較
   */
  private compareValues(a: any, b: any): number {
    if (a === b) return 0;
    if (a == null) return -1;
    if (b == null) return 1;
    
    if (typeof a === 'string' && typeof b === 'string') {
      return a.localeCompare(b);
    }
    
    return a < b ? -1 : 1;
  }

  /**
   * フィルタ評価
   */
  private evaluateFilter(value: any, filter: FilterConfig): boolean {
    switch (filter.operator) {
      case 'equals':
        return value === filter.value;
      case 'contains':
        return String(value).toLowerCase().includes(String(filter.value).toLowerCase());
      case 'startsWith':
        return String(value).toLowerCase().startsWith(String(filter.value).toLowerCase());
      case 'endsWith':
        return String(value).toLowerCase().endsWith(String(filter.value).toLowerCase());
      case 'greaterThan':
        return Number(value) > Number(filter.value);
      case 'lessThan':
        return Number(value) < Number(filter.value);
      case 'greaterThanOrEqual':
        return Number(value) >= Number(filter.value);
      case 'lessThanOrEqual':
        return Number(value) <= Number(filter.value);
      case 'in':
        return Array.isArray(filter.value) && filter.value.includes(value);
      case 'notIn':
        return Array.isArray(filter.value) && !filter.value.includes(value);
      default:
        return true;
    }
  }
}
```

---

## 4. パーサー実装

### 4.1 CSVパーサー

```typescript
/**
 * CSVパーサー
 */
export class CSVParser<T = any> implements FileParser<T> {
  private delimiter: string;
  private hasHeader: boolean;
  private mapper: (row: string[]) => T;

  constructor(options: CSVParserOptions<T>) {
    this.delimiter = options.delimiter || ',';
    this.hasHeader = options.hasHeader ?? true;
    this.mapper = options.mapper;
  }

  async parse(content: string, options?: ParseOptions): Promise<ParseResult<T>> {
    const lines = this.splitLines(content);
    const data: T[] = [];
    const errors: ImportError[] = [];
    let headers: string[] = [];
    
    let startIndex = 0;
    if (this.hasHeader && lines.length > 0) {
      headers = this.parseLine(lines[0]);
      startIndex = 1;
    }

    for (let i = startIndex; i < lines.length; i++) {
      if (options?.signal?.aborted) {
        throw new Error('処理がキャンセルされました');
      }

      try {
        const row = this.parseLine(lines[i]);
        if (row.length === 0) continue; // 空行をスキップ
        
        const item = this.mapper(row);
        data.push(item);
        
        // 進捗更新
        if (options?.onProgress && i % 100 === 0) {
          const progress = (i / lines.length) * 100;
          options.onProgress(progress);
        }
        
      } catch (error) {
        errors.push({
          row: i + 1,
          column: '',
          message: error.message,
          code: 'PARSE_ERROR'
        });
      }
    }

    return {
      data,
      totalCount: lines.length - startIndex,
      successCount: data.length,
      errors,
      metadata: {
        headers,
        delimiter: this.delimiter,
        encoding: 'utf-8'
      }
    };
  }

  private splitLines(content: string): string[] {
    return content.split(/\r?\n/);
  }

  private parseLine(line: string): string[] {
    const result: string[] = [];
    let current = '';
    let inQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
      const char = line[i];
      
      if (char === '"') {
        if (inQuotes && line[i + 1] === '"') {
          current += '"';
          i++; // Skip next quote
        } else {
          inQuotes = !inQuotes;
        }
      } else if (char === this.delimiter && !inQuotes) {
        result.push(current.trim());
        current = '';
      } else {
        current += char;
      }
    }
    
    result.push(current.trim());
    return result;
  }
}
```

### 4.2 Excelパーサー

```typescript
/**
 * Excelパーサー
 */
export class ExcelParser<T = any> implements FileParser<T> {
  private sheetName?: string;
  private hasHeader: boolean;
  private mapper: (row: any[]) => T;

  constructor(options: ExcelParserOptions<T>) {
    this.sheetName = options.sheetName;
    this.hasHeader = options.hasHeader ?? true;
    this.mapper = options.mapper;
  }

  async parse(content: string, options?: ParseOptions): Promise<ParseResult<T>> {
    // Excel解析にはライブラリ（xlsx等）を使用
    const XLSX = await import('xlsx');
    
    // Base64デコード（ファイルがBase64エンコードされている場合）
    const workbook = XLSX.read(content, { type: 'binary' });
    
    const sheetName = this.sheetName || workbook.SheetNames[0];
    const worksheet = workbook.Sheets[sheetName];
    
    if (!worksheet) {
      throw new Error(`シート "${sheetName}" が見つかりません`);
    }

    const jsonData = XLSX.utils.sheet_to_json(worksheet, {
      header: this.hasHeader ? 1 : undefined,
      defval: ''
    });

    const data: T[] = [];
    const errors: ImportError[] = [];

    for (let i = 0; i < jsonData.length; i++) {
      if (options?.signal?.aborted) {
        throw new Error('処理がキャンセルされました');
      }

      try {
        const row = Object.values(jsonData[i]);
        const item = this.mapper(row);
        data.push(item);
        
        if (options?.onProgress && i % 100 === 0) {
          const progress = (i / jsonData.length) * 100;
          options.onProgress(progress);
        }
        
      } catch (error) {
        errors.push({
          row: i + (this.hasHeader ? 2 : 1),
          column: '',
          message: error.message,
          code: 'PARSE_ERROR'
        });
      }
    }

    return {
      data,
      totalCount: jsonData.length,
      successCount: data.length,
      errors,
      metadata: {
        sheetName,
        totalSheets: workbook.SheetNames.length,
        sheetNames: workbook.SheetNames
      }
    };
  }
}
```

---

## 5. フォーマッター実装

### 5.1 CSVフォーマッター

```typescript
/**
 * CSVフォーマッター
 */
export class CSVFormatter<T = any> implements FileFormatter<T> {
  private delimiter: string;
  private includeHeader: boolean;

  constructor(options: CSVFormatterOptions = {}) {
    this.delimiter = options.delimiter || ',';
    this.includeHeader = options.includeHeader ?? true;
  }

  async format(data: T[], config: ExportConfig): Promise<string> {
    const lines: string[] = [];
    
    // ヘッダー行
    if (this.includeHeader && config.headers) {
      lines.push(this.formatRow(config.headers));
    }
    
    // データ行
    for (const item of data) {
      const row = this.extractRowData(item, config.columns);
      lines.push(this.formatRow(row));
    }
    
    return lines.join('\n');
  }

  getMimeType(): string {
    return 'text/csv;charset=utf-8';
  }

  private formatRow(row: string[]): string {
    return row.map(cell => {
      const cellStr = String(cell || '');
      
      // カンマ、改行、ダブルクォートが含まれている場合はクォートで囲む
      if (cellStr.includes(this.delimiter) || 
          cellStr.includes('\n') || 
          cellStr.includes('\r') || 
          cellStr.includes('"')) {
        return `"${cellStr.replace(/"/g, '""')}"`;
      }
      
      return cellStr;
    }).join(this.delimiter);
  }

  private extractRowData(item: T, columns?: ColumnConfig[]): string[] {
    if (!columns) {
      return Object.values(item as any);
    }
    
    return columns.map(column => {
      const value = this.getNestedValue(item, column.field);
      return column.formatter ? column.formatter(value) : String(value || '');
    });
  }

  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }
}
```

### 5.2 Excelフォーマッター

```typescript
/**
 * Excelフォーマッター
 */
export class ExcelFormatter<T = any> implements FileFormatter<T> {
  async format(data: T[], config: ExportConfig): Promise<Blob> {
    const XLSX = await import('xlsx');
    
    // ワークブック作成
    const workbook = XLSX.utils.book_new();
    
    // データ変換
    const worksheetData = this.prepareWorksheetData(data, config);
    
    // ワークシート作成
    const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
    
    // スタイル適用
    if (config.styling) {
      this.applyStyles(worksheet, config.styling);
    }
    
    // ワークシートをワークブックに追加
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Sheet1');
    
    // Excelファイル生成
    const excelBuffer = XLSX.write(workbook, {
      bookType: 'xlsx',
      type: 'array'
    });
    
    return new Blob([excelBuffer], {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    });
  }

  getMimeType(): string {
    return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
  }

  private prepareWorksheetData(data: T[], config: ExportConfig): any[][] {
    const result: any[][] = [];
    
    // ヘッダー行
    if (config.headers) {
      result.push(config.headers);
    }
    
    // データ行
    for (const item of data) {
      const row = this.extractRowData(item, config.columns);
      result.push(row);
    }
    
    return result;
  }

  private extractRowData(item: T, columns?: ColumnConfig[]): any[] {
    if (!columns) {
      return Object.values(item as any);
    }
    
    return columns.map(column => {
      const value = this.getNestedValue(item, column.field);
      return column.formatter ? column.formatter(value) : value;
    });
  }

  private applyStyles(worksheet: any, styling: StylingConfig): void {
    // スタイル適用の実装
    // XLSXライブラリの機能を使用してセルスタイルを設定
  }

  private getNestedValue(obj: any, path: string): any {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  }
}
```

---

## 6. 使用例

### 6.1 CSVインポート

```typescript
import { FileHandler, CSVParser } from '@/utils/FileHandler';

// スキルデータのインポート
interface SkillData {
  name: string;
  category: string;
  level: string;
  description: string;
}

const fileHandler = new FileHandler({
  maxFileSize: 10 * 1024 * 1024, // 10MB
  allowedTypes: ['.csv', 'text/csv'],
  encoding: 'utf-8',
  chunkSize: 1024,
  onProgress: (progress) => {
    console.log(`進捗: ${progress}%`);
  },
  onError: (error) => {
    console.error('エラー:', error);
  }
});

const csvParser = new CSVParser<SkillData>({
  delimiter: ',',
  hasHeader: true,
  mapper: (row) => ({
    name: row[0],
    category: row[1],
    level: row[2],
    description: row[3]
  })
});

// ファイルインポート実行
const handleFileImport = async (file: File) => {
  try {
    const result = await fileHandler.import(file, csvParser);
    
    if (result.success) {
      console.log(`${result.successCount}件のデータをインポートしました`);
      console.log('データ:', result.data);
    } else {
      console.log(`${result.errorCount}件のエラーがありました`);
      console.log('エラー:', result.errors);
    }
  } catch (error) {
    console.error('インポートに失敗しました:', error);
  }
};
```

### 6.2 Excelエクスポート

```typescript
import { ExcelFormatter } from '@/utils/FileHandler';

// スキルデータのエクスポート
const skills: SkillData[] = [
  { name: 'JavaScript', category: 'プログラミング', level: '上級', description: 'Web開発言語' },
  { name: 'React', category: 'フレームワーク', level: '中級', description: 'UIライブラリ' }
];

const excelFormatter = new ExcelFormatter<SkillData>();

const exportConfig: ExportConfig = {
  filename: 'skills.xlsx',
  format: 'excel',
  headers: ['スキル名', 'カテゴリ', 'レベル', '説明'],
  columns: [
    { field: 'name', formatter: (value) => value },
    { field: 'category', formatter: (value) => value },
    { field: 'level', formatter: (value) => value },
    { field: 'description', formatter: (value) => value }
  ],
  styling: {
    headerStyle: {
      font: { bold: true },
      fill: { fgColor: { rgb: 'CCCCCC' } }
    }
  }
};

// エクスポート実行
const handleExport = async () => {
  try {
    await fileHandler.export(skills, exportConfig, excelFormatter);
    console.log('エクスポートが完了しました');
  } catch (error) {
    console.error('エクスポートに失敗しました:', error);
  }
};
```

---

## 7. 変更履歴

| 日付 | バージョン | 変更内容 | 担当者 |
|------|-----------|----------|--------|
| 2025/05/30 | 1.0.0 | 初版作成 | 開発チーム |

---

## 8. 関連ドキュメント

- [共通部品定義書](../../共通部品定義書.md)
- [SkillTypes 型定義書](../types/SkillTypes.md)
- [Form コンポーネント](../../frontend/ui-components/Form.md)

---

このFileHandlerにより、統一されたファイル処理機能とデータの入出力管理を実現します。
