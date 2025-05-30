# SkillService 定義書

## 1. 基本情報

- **部品名**: SkillService
- **カテゴリ**: ビジネスサービス
- **責務**: スキル情報の業務ロジック処理
- **依存関係**: SkillRepository, ValidationService, NotificationService
- **作成日**: 2025/05/30
- **最終更新**: 2025/05/30

---

## 2. インターフェース仕様

### 2.1 メソッド一覧

| メソッド名 | 引数 | 戻り値 | 説明 |
|-----------|------|--------|------|
| getSkills | `userId: string, filters?: SkillFilters` | `Promise<SkillItem[]>` | ユーザーのスキル一覧取得 |
| getSkillById | `skillId: string, userId: string` | `Promise<SkillItem>` | 特定スキル取得 |
| createSkill | `userId: string, skill: CreateSkillRequest` | `Promise<SkillItem>` | スキル新規作成 |
| updateSkill | `skillId: string, userId: string, updates: UpdateSkillRequest` | `Promise<SkillItem>` | スキル更新 |
| deleteSkill | `skillId: string, userId: string` | `Promise<void>` | スキル削除 |
| bulkUpdateSkills | `userId: string, updates: BulkUpdateRequest[]` | `Promise<SkillItem[]>` | スキル一括更新 |
| validateSkill | `skill: SkillItem` | `ValidationResult` | スキル情報検証 |
| getSkillStatistics | `userId: string` | `Promise<SkillStatistics>` | スキル統計情報取得 |
| exportSkills | `userId: string, format: ExportFormat` | `Promise<Buffer>` | スキルデータエクスポート |
| importSkills | `userId: string, data: Buffer, format: ImportFormat` | `Promise<ImportResult>` | スキルデータインポート |

### 2.2 型定義

```typescript
export interface SkillItem {
  id: string;
  userId: string;
  skillName: string;
  category: SkillCategory;
  level: SkillLevel;
  experience: number;
  lastUsed: Date;
  target: boolean;
  comments?: string;
  certifications?: string[];
  projects?: string[];
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateSkillRequest {
  skillName: string;
  category: SkillCategory;
  level: SkillLevel;
  experience: number;
  lastUsed: Date;
  target: boolean;
  comments?: string;
  certifications?: string[];
  projects?: string[];
}

export interface UpdateSkillRequest extends Partial<CreateSkillRequest> {
  isDraft?: boolean;
}

export interface SkillFilters {
  category?: SkillCategory[];
  level?: SkillLevel[];
  target?: boolean;
  search?: string;
  sortBy?: 'skillName' | 'category' | 'level' | 'experience' | 'lastUsed' | 'createdAt';
  sortOrder?: 'asc' | 'desc';
  limit?: number;
  offset?: number;
}

export interface BulkUpdateRequest {
  skillId: string;
  updates: UpdateSkillRequest;
}

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
}

export interface ValidationError {
  field: string;
  message: string;
  code: string;
}

export interface SkillStatistics {
  totalSkills: number;
  skillsByCategory: Record<SkillCategory, number>;
  skillsByLevel: Record<SkillLevel, number>;
  targetSkills: number;
  averageExperience: number;
  recentlyUsedSkills: number;
  topCategories: Array<{ category: SkillCategory; count: number }>;
  levelDistribution: Array<{ level: SkillLevel; percentage: number }>;
}

export type ExportFormat = 'json' | 'csv' | 'xlsx';
export type ImportFormat = 'json' | 'csv' | 'xlsx';

export interface ImportResult {
  success: boolean;
  imported: number;
  failed: number;
  errors: ImportError[];
}

export interface ImportError {
  row: number;
  field: string;
  message: string;
}

export type SkillCategory = 
  | 'プログラミング言語'
  | 'フレームワーク・ライブラリ'
  | 'データベース'
  | 'クラウド・インフラ'
  | 'ツール・その他';

export type SkillLevel = '初級' | '中級' | '上級' | 'エキスパート';
```

---

## 3. 実装仕様

### 3.1 技術スタック
- **Node.js**: 20.x
- **TypeScript**: 5.x
- **Express**: 4.x
- **Prisma**: 5.x（ORM）
- **Zod**: 3.x（バリデーション）
- **ExcelJS**: 4.x（Excel処理）
- **csv-parser**: 3.x（CSV処理）

### 3.2 クラス構造

```typescript
import { PrismaClient } from '@prisma/client';
import { SkillRepository } from '@/repositories/SkillRepository';
import { ValidationService } from '@/services/ValidationService';
import { NotificationService } from '@/services/NotificationService';
import { CacheService } from '@/services/CacheService';
import { skillValidationSchema } from '@/schemas/skillSchemas';
import { 
  SkillItem, 
  CreateSkillRequest, 
  UpdateSkillRequest, 
  SkillFilters,
  SkillStatistics,
  ValidationResult,
  ExportFormat,
  ImportFormat,
  ImportResult
} from './SkillService.types';

export class SkillService {
  constructor(
    private skillRepository: SkillRepository,
    private validationService: ValidationService,
    private notificationService: NotificationService,
    private cacheService: CacheService
  ) {}

  /**
   * ユーザーのスキル一覧を取得
   */
  async getSkills(userId: string, filters?: SkillFilters): Promise<SkillItem[]> {
    // 入力値検証
    this.validateUserId(userId);
    
    // キャッシュキー生成
    const cacheKey = this.generateCacheKey('skills', userId, filters);
    
    // キャッシュから取得試行
    const cached = await this.cacheService.get<SkillItem[]>(cacheKey);
    if (cached) {
      return cached;
    }

    try {
      // データベースから取得
      const skills = await this.skillRepository.findByUserId(userId, filters);
      
      // キャッシュに保存（5分間）
      await this.cacheService.set(cacheKey, skills, 300);
      
      return skills;
    } catch (error) {
      throw new Error(`スキル一覧の取得に失敗しました: ${error.message}`);
    }
  }

  /**
   * 特定のスキルを取得
   */
  async getSkillById(skillId: string, userId: string): Promise<SkillItem> {
    this.validateSkillId(skillId);
    this.validateUserId(userId);

    try {
      const skill = await this.skillRepository.findById(skillId);
      
      if (!skill) {
        throw new Error('スキルが見つかりません');
      }
      
      if (skill.userId !== userId) {
        throw new Error('このスキルにアクセスする権限がありません');
      }
      
      return skill;
    } catch (error) {
      throw new Error(`スキルの取得に失敗しました: ${error.message}`);
    }
  }

  /**
   * 新しいスキルを作成
   */
  async createSkill(userId: string, skillData: CreateSkillRequest): Promise<SkillItem> {
    this.validateUserId(userId);
    
    // バリデーション実行
    const validationResult = await this.validateSkillData(skillData);
    if (!validationResult.isValid) {
      throw new ValidationError('入力データが無効です', validationResult.errors);
    }

    // 重複チェック
    await this.checkDuplicateSkill(userId, skillData.skillName);

    try {
      // スキル作成
      const newSkill = await this.skillRepository.create({
        ...skillData,
        userId,
        createdAt: new Date(),
        updatedAt: new Date()
      });

      // キャッシュクリア
      await this.clearUserSkillsCache(userId);

      // 通知送信（非同期）
      this.notificationService.sendSkillCreatedNotification(userId, newSkill)
        .catch(error => console.error('通知送信エラー:', error));

      return newSkill;
    } catch (error) {
      throw new Error(`スキルの作成に失敗しました: ${error.message}`);
    }
  }

  /**
   * スキルを更新
   */
  async updateSkill(
    skillId: string, 
    userId: string, 
    updates: UpdateSkillRequest
  ): Promise<SkillItem> {
    this.validateSkillId(skillId);
    this.validateUserId(userId);

    // 既存スキル取得・権限確認
    const existingSkill = await this.getSkillById(skillId, userId);

    // バリデーション実行
    const mergedData = { ...existingSkill, ...updates };
    const validationResult = await this.validateSkillData(mergedData);
    if (!validationResult.isValid) {
      throw new ValidationError('更新データが無効です', validationResult.errors);
    }

    // 重複チェック（スキル名変更時のみ）
    if (updates.skillName && updates.skillName !== existingSkill.skillName) {
      await this.checkDuplicateSkill(userId, updates.skillName, skillId);
    }

    try {
      // スキル更新
      const updatedSkill = await this.skillRepository.update(skillId, {
        ...updates,
        updatedAt: new Date()
      });

      // キャッシュクリア
      await this.clearUserSkillsCache(userId);

      // 下書き保存でない場合は通知送信
      if (!updates.isDraft) {
        this.notificationService.sendSkillUpdatedNotification(userId, updatedSkill)
          .catch(error => console.error('通知送信エラー:', error));
      }

      return updatedSkill;
    } catch (error) {
      throw new Error(`スキルの更新に失敗しました: ${error.message}`);
    }
  }

  /**
   * スキルを削除
   */
  async deleteSkill(skillId: string, userId: string): Promise<void> {
    this.validateSkillId(skillId);
    this.validateUserId(userId);

    // 既存スキル取得・権限確認
    const existingSkill = await this.getSkillById(skillId, userId);

    try {
      // スキル削除
      await this.skillRepository.delete(skillId);

      // キャッシュクリア
      await this.clearUserSkillsCache(userId);

      // 通知送信（非同期）
      this.notificationService.sendSkillDeletedNotification(userId, existingSkill)
        .catch(error => console.error('通知送信エラー:', error));
    } catch (error) {
      throw new Error(`スキルの削除に失敗しました: ${error.message}`);
    }
  }

  /**
   * スキル一括更新
   */
  async bulkUpdateSkills(
    userId: string, 
    updates: BulkUpdateRequest[]
  ): Promise<SkillItem[]> {
    this.validateUserId(userId);

    if (updates.length === 0) {
      throw new Error('更新対象のスキルが指定されていません');
    }

    if (updates.length > 100) {
      throw new Error('一度に更新できるスキルは100件までです');
    }

    // 全スキルの権限確認
    for (const update of updates) {
      await this.getSkillById(update.skillId, userId);
    }

    try {
      // トランザクション内で一括更新
      const updatedSkills = await this.skillRepository.bulkUpdate(updates);

      // キャッシュクリア
      await this.clearUserSkillsCache(userId);

      return updatedSkills;
    } catch (error) {
      throw new Error(`スキルの一括更新に失敗しました: ${error.message}`);
    }
  }

  /**
   * スキル統計情報を取得
   */
  async getSkillStatistics(userId: string): Promise<SkillStatistics> {
    this.validateUserId(userId);

    const cacheKey = this.generateCacheKey('statistics', userId);
    const cached = await this.cacheService.get<SkillStatistics>(cacheKey);
    if (cached) {
      return cached;
    }

    try {
      const skills = await this.getSkills(userId);
      
      const statistics: SkillStatistics = {
        totalSkills: skills.length,
        skillsByCategory: this.calculateCategoryDistribution(skills),
        skillsByLevel: this.calculateLevelDistribution(skills),
        targetSkills: skills.filter(skill => skill.target).length,
        averageExperience: this.calculateAverageExperience(skills),
        recentlyUsedSkills: this.calculateRecentlyUsedSkills(skills),
        topCategories: this.getTopCategories(skills),
        levelDistribution: this.getLevelDistributionPercentage(skills)
      };

      // キャッシュに保存（10分間）
      await this.cacheService.set(cacheKey, statistics, 600);

      return statistics;
    } catch (error) {
      throw new Error(`統計情報の取得に失敗しました: ${error.message}`);
    }
  }

  /**
   * スキルデータをエクスポート
   */
  async exportSkills(userId: string, format: ExportFormat): Promise<Buffer> {
    this.validateUserId(userId);

    try {
      const skills = await this.getSkills(userId);
      
      switch (format) {
        case 'json':
          return this.exportToJson(skills);
        case 'csv':
          return this.exportToCsv(skills);
        case 'xlsx':
          return this.exportToExcel(skills);
        default:
          throw new Error(`サポートされていないエクスポート形式: ${format}`);
      }
    } catch (error) {
      throw new Error(`エクスポートに失敗しました: ${error.message}`);
    }
  }

  /**
   * スキルデータをインポート
   */
  async importSkills(
    userId: string, 
    data: Buffer, 
    format: ImportFormat
  ): Promise<ImportResult> {
    this.validateUserId(userId);

    try {
      let skillsData: CreateSkillRequest[];
      
      switch (format) {
        case 'json':
          skillsData = this.parseJsonImport(data);
          break;
        case 'csv':
          skillsData = await this.parseCsvImport(data);
          break;
        case 'xlsx':
          skillsData = await this.parseExcelImport(data);
          break;
        default:
          throw new Error(`サポートされていないインポート形式: ${format}`);
      }

      return await this.processImportData(userId, skillsData);
    } catch (error) {
      throw new Error(`インポートに失敗しました: ${error.message}`);
    }
  }

  // プライベートメソッド

  private validateUserId(userId: string): void {
    if (!userId || typeof userId !== 'string') {
      throw new Error('有効なユーザーIDが必要です');
    }
  }

  private validateSkillId(skillId: string): void {
    if (!skillId || typeof skillId !== 'string') {
      throw new Error('有効なスキルIDが必要です');
    }
  }

  private async validateSkillData(data: any): Promise<ValidationResult> {
    return this.validationService.validate(skillValidationSchema, data);
  }

  private async checkDuplicateSkill(
    userId: string, 
    skillName: string, 
    excludeSkillId?: string
  ): Promise<void> {
    const existingSkill = await this.skillRepository.findByUserIdAndName(
      userId, 
      skillName
    );
    
    if (existingSkill && existingSkill.id !== excludeSkillId) {
      throw new Error('同じ名前のスキルが既に登録されています');
    }
  }

  private generateCacheKey(type: string, userId: string, filters?: any): string {
    const filterStr = filters ? JSON.stringify(filters) : '';
    return `skill:${type}:${userId}:${filterStr}`;
  }

  private async clearUserSkillsCache(userId: string): Promise<void> {
    const patterns = [
      `skill:skills:${userId}:*`,
      `skill:statistics:${userId}:*`
    ];
    
    for (const pattern of patterns) {
      await this.cacheService.deletePattern(pattern);
    }
  }

  private calculateCategoryDistribution(skills: SkillItem[]): Record<SkillCategory, number> {
    const distribution: Record<SkillCategory, number> = {
      'プログラミング言語': 0,
      'フレームワーク・ライブラリ': 0,
      'データベース': 0,
      'クラウド・インフラ': 0,
      'ツール・その他': 0
    };

    skills.forEach(skill => {
      distribution[skill.category]++;
    });

    return distribution;
  }

  private calculateLevelDistribution(skills: SkillItem[]): Record<SkillLevel, number> {
    const distribution: Record<SkillLevel, number> = {
      '初級': 0,
      '中級': 0,
      '上級': 0,
      'エキスパート': 0
    };

    skills.forEach(skill => {
      distribution[skill.level]++;
    });

    return distribution;
  }

  private calculateAverageExperience(skills: SkillItem[]): number {
    if (skills.length === 0) return 0;
    
    const totalExperience = skills.reduce((sum, skill) => sum + skill.experience, 0);
    return Math.round((totalExperience / skills.length) * 10) / 10;
  }

  private calculateRecentlyUsedSkills(skills: SkillItem[]): number {
    const threeMonthsAgo = new Date();
    threeMonthsAgo.setMonth(threeMonthsAgo.getMonth() - 3);
    
    return skills.filter(skill => skill.lastUsed >= threeMonthsAgo).length;
  }

  private getTopCategories(skills: SkillItem[]): Array<{ category: SkillCategory; count: number }> {
    const categoryCount = this.calculateCategoryDistribution(skills);
    
    return Object.entries(categoryCount)
      .map(([category, count]) => ({ category: category as SkillCategory, count }))
      .sort((a, b) => b.count - a.count)
      .slice(0, 5);
  }

  private getLevelDistributionPercentage(skills: SkillItem[]): Array<{ level: SkillLevel; percentage: number }> {
    if (skills.length === 0) return [];
    
    const levelCount = this.calculateLevelDistribution(skills);
    
    return Object.entries(levelCount)
      .map(([level, count]) => ({
        level: level as SkillLevel,
        percentage: Math.round((count / skills.length) * 100)
      }));
  }

  private exportToJson(skills: SkillItem[]): Buffer {
    const jsonData = JSON.stringify(skills, null, 2);
    return Buffer.from(jsonData, 'utf-8');
  }

  private exportToCsv(skills: SkillItem[]): Buffer {
    const headers = [
      'スキル名', 'カテゴリ', 'レベル', '経験年数', '最終使用日', 
      '目標スキル', 'コメント', '作成日', '更新日'
    ];
    
    const rows = skills.map(skill => [
      skill.skillName,
      skill.category,
      skill.level,
      skill.experience.toString(),
      skill.lastUsed.toISOString().split('T')[0],
      skill.target ? 'はい' : 'いいえ',
      skill.comments || '',
      skill.createdAt.toISOString().split('T')[0],
      skill.updatedAt.toISOString().split('T')[0]
    ]);

    const csvContent = [headers, ...rows]
      .map(row => row.map(cell => `"${cell}"`).join(','))
      .join('\n');

    return Buffer.from(csvContent, 'utf-8');
  }

  private async exportToExcel(skills: SkillItem[]): Promise<Buffer> {
    const ExcelJS = require('exceljs');
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('スキル一覧');

    // ヘッダー設定
    worksheet.columns = [
      { header: 'スキル名', key: 'skillName', width: 20 },
      { header: 'カテゴリ', key: 'category', width: 25 },
      { header: 'レベル', key: 'level', width: 15 },
      { header: '経験年数', key: 'experience', width: 12 },
      { header: '最終使用日', key: 'lastUsed', width: 15 },
      { header: '目標スキル', key: 'target', width: 12 },
      { header: 'コメント', key: 'comments', width: 30 },
      { header: '作成日', key: 'createdAt', width: 15 },
      { header: '更新日', key: 'updatedAt', width: 15 }
    ];

    // データ追加
    skills.forEach(skill => {
      worksheet.addRow({
        skillName: skill.skillName,
        category: skill.category,
        level: skill.level,
        experience: skill.experience,
        lastUsed: skill.lastUsed.toISOString().split('T')[0],
        target: skill.target ? 'はい' : 'いいえ',
        comments: skill.comments || '',
        createdAt: skill.createdAt.toISOString().split('T')[0],
        updatedAt: skill.updatedAt.toISOString().split('T')[0]
      });
    });

    // スタイル設定
    worksheet.getRow(1).font = { bold: true };
    worksheet.getRow(1).fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FFE0E0E0' }
    };

    return await workbook.xlsx.writeBuffer() as Buffer;
  }

  private parseJsonImport(data: Buffer): CreateSkillRequest[] {
    try {
      const jsonData = JSON.parse(data.toString('utf-8'));
      return Array.isArray(jsonData) ? jsonData : [jsonData];
    } catch (error) {
      throw new Error('JSONファイルの解析に失敗しました');
    }
  }

  private async parseCsvImport(data: Buffer): Promise<CreateSkillRequest[]> {
    // CSV解析実装
    // 実際の実装では csv-parser ライブラリを使用
    throw new Error('CSV インポートは未実装です');
  }

  private async parseExcelImport(data: Buffer): Promise<CreateSkillRequest[]> {
    // Excel解析実装
    // 実際の実装では ExcelJS ライブラリを使用
    throw new Error('Excel インポートは未実装です');
  }

  private async processImportData(
    userId: string, 
    skillsData: CreateSkillRequest[]
  ): Promise<ImportResult> {
    const result: ImportResult = {
      success: true,
      imported: 0,
      failed: 0,
      errors: []
    };

    for (let i = 0; i < skillsData.length; i++) {
      try {
        await this.createSkill(userId, skillsData[i]);
        result.imported++;
      } catch (error) {
        result.failed++;
        result.errors.push({
          row: i + 1,
          field: 'general',
          message: error.message
        });
      }
    }

    result.success = result.failed === 0;
    return result;
  }
}

// カスタムエラークラス
export class ValidationError extends Error {
  constructor(message: string, public errors: ValidationError[]) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

---

## 4. 使用例・サンプルコード

### 4.1 コントローラーでの使用例

```typescript
import { Request, Response } from 'express';
import { SkillService } from '@/services/SkillService';
import { ResponseUtils } from '@/utils/ResponseUtils';

export class SkillController {
  constructor(private skillService: SkillService) {}

  async getSkills(req: Request, res: Response) {
    try {
      const userId = req.user.id;
      const filters = req.query as SkillFilters;
      
      const skills = await this.skillService.getSkills(userId, filters);
      
      return ResponseUtils.success(res, skills, 'スキル一覧を取得しました');
    } catch (error) {
      return ResponseUtils.error(res, error.message, 500);
    }
  }

  async createSkill(req: Request, res: Response) {
    try {
      const userId = req.user.id;
      const skillData = req.body as CreateSkillRequest;
      
      const newSkill = await this.skillService.createSkill(userId, skillData);
      
      return ResponseUtils.success(res, newSkill, 'スキルを作成しました', 201);
    } catch (error) {
      if (error instanceof ValidationError) {
        return ResponseUtils.validationError(res, error.errors);
      }
      return ResponseUtils.error(res, error.message, 500);
    }
  }

  async updateSkill(req: Request, res: Response) {
    try {
      const { skillId } = req.params;
      const userId = req.user.id;
      const updates = req.body as UpdateSkillRequest;
      
      const updatedSkill = await this.skillService.updateSkill(skillId, userId, updates);
      
      return ResponseUtils.success(res, updatedSkill, 'スキルを更新しました');
    } catch (error) {
      if (error instanceof ValidationError) {
        return ResponseUtils.validationError(res, error.errors);
      }
      return ResponseUtils.error(res, error.message, 500);
    }
  }

  async deleteSkill(req: Request, res: Response) {
    try {
      const { skillId } = req.params;
      const userId = req.user.id;
      
      await this.skillService.deleteSkill(skillId, userId);
      
      return ResponseUtils.success(res, null, 'スキルを削除しました');
    } catch (error) {
      return ResponseUtils.error(res, error.message, 500);
    }
  }

  async getStatistics(req: Request, res: Response) {
    try {
      const userId = req.user.id;
      
      const statistics = await this.skillService.getSkillStatistics(userId);
      
      return ResponseUtils.success(res, statistics, '統計情報を取得しました');
    } catch (error) {
      return ResponseUtils.error(res, error.message, 500);
    }
  }

  async exportSkills(req: Request, res: Response) {
    try {
      const userId = req.user.id;
      const format = req.query.format as ExportFormat || 'json';
      
      const data = await this.skillService.exportSkills(userId, format);
      
      const filename = `skills_${new Date().toISOString().split('T')[0]}.${format}`;
      const contentType = this.getContentType(format);
      
      res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
      res.setHeader('Content-Type', contentType);
      
      return res.send(data);
    } catch (error) {
      return ResponseUtils.error(res, error.message, 500);
    }
  }

  private getContentType(format: ExportFormat): string {
    switch (format) {
      case 'json': return 'application/json';
      case 'csv': return 'text/csv';
      case 'xlsx': return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
      default: return 'application/octet-stream';
    }
  }
}
```

### 4.2 依存性注入での使用例

```typescript
import { Container } from 'inversify';
import { SkillService } from '@/services/SkillService';
import { SkillRepository } from '@/repositories/SkillRepository';
import { ValidationService } from '@/services/ValidationService';
import { NotificationService } from '@/services/NotificationService';
import { CacheService } from '@/services/CacheService';

// DIコンテナ設定
const container = new Container();

container.bind<SkillRepository>('SkillRepository').to(SkillRepository);
container.bind<ValidationService>('ValidationService').to(ValidationService);
container.bind<NotificationService>('NotificationService').to(NotificationService);
container.bind<CacheService>('CacheService').to(CacheService);

container.bind<SkillService>('SkillService').to(SkillService);

// 使用
