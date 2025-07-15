/**
 * 要求仕様ID: API-030
 * 対応設計書: docs/design/api/specs/API定義書_API-030_スキル検索API.md
 * テスト内容: スキル検索APIのテスト
 */

import { NextRequest } from 'next/server';
import { GET } from '@/app/api/skills/search/route';

// Prismaのモック
jest.mock('@/lib/prisma', () => ({
  prisma: {
    skillRecord: {
      findMany: jest.fn(),
    },
    skillItem: {
      findMany: jest.fn(),
    },
    skillCategory: {
      findMany: jest.fn(),
    },
  },
}));

describe('スキル検索API テスト', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /api/skills/search - スキル検索', () => {
    it('正常系: キーワード検索で正常に結果を取得できる', async () => {
      // モックデータの設定
      const mockSkillRecords = [
        {
          id: 'skill-001',
          employee_id: 'user001',
          skill_item_id: 'js-001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: null,
          last_used_date: new Date('2024-12-01'),
          acquisition_date: new Date('2024-01-01'),
          certification_id: null,
          evidence_description: 'JavaScript開発経験',
          skill_status: 'active',
          learning_hours: 100,
          project_experience_count: 5,
          is_deleted: false,
          created_at: new Date('2024-01-01'),
          updated_at: new Date('2024-12-01'),
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001',
        },
      ];

      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/search?keyword=JavaScript');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data).toHaveLength(1);
      expect(responseData.data[0]).toMatchObject({
        id: 'skill-001',
        userId: 'user001',
        skillCategoryId: 'tech-001',
        skillCategoryName: 'プログラミング言語',
        skillName: 'JavaScript',
        skillLevel: 3,
        selfAssessment: 3,
        managerAssessment: null,
        lastUsedDate: '2024-12-01',
        acquisitionDate: '2024-01-01',
        evidenceDescription: 'JavaScript開発経験',
        skillStatus: 'active',
        learningHours: 100,
        projectExperienceCount: 5,
      });
      expect(responseData.count).toBe(1);
      expect(responseData.timestamp).toBeDefined();
    });

    it('正常系: カテゴリフィルタで検索結果を絞り込める', async () => {
      // モックデータの設定
      const mockSkillRecords = [
        {
          id: 'skill-001',
          employee_id: 'user001',
          skill_item_id: 'js-001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: null,
          last_used_date: new Date('2024-12-01'),
          acquisition_date: new Date('2024-01-01'),
          certification_id: null,
          evidence_description: 'JavaScript開発経験',
          skill_status: 'active',
          learning_hours: 100,
          project_experience_count: 5,
          is_deleted: false,
          created_at: new Date('2024-01-01'),
          updated_at: new Date('2024-12-01'),
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001',
        },
      ];

      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストの作成（カテゴリフィルタ付き）
      const request = new NextRequest('http://localhost:3000/api/skills/search?category=tech-001&keyword=JavaScript');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data).toHaveLength(1);
      expect(responseData.data[0].skillCategoryId).toBe('tech-001');
    });

    it('正常系: スキルレベルフィルタで検索結果を絞り込める', async () => {
      // モックデータの設定
      const mockSkillRecords = [
        {
          id: 'skill-001',
          employee_id: 'user001',
          skill_item_id: 'js-001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: null,
          last_used_date: new Date('2024-12-01'),
          acquisition_date: new Date('2024-01-01'),
          certification_id: null,
          evidence_description: 'JavaScript開発経験',
          skill_status: 'active',
          learning_hours: 100,
          project_experience_count: 5,
          is_deleted: false,
          created_at: new Date('2024-01-01'),
          updated_at: new Date('2024-12-01'),
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001',
        },
      ];

      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストの作成（スキルレベルフィルタ付き）
      const request = new NextRequest('http://localhost:3000/api/skills/search?level=3&keyword=JavaScript');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data).toHaveLength(1);
      expect(responseData.data[0].skillLevel).toBe(3);
    });

    it('正常系: ページネーション機能が正常に動作する', async () => {
      // モックデータの設定（複数件）
      const mockSkillRecords = Array.from({ length: 25 }, (_, index) => ({
        id: `skill-${String(index + 1).padStart(3, '0')}`,
        employee_id: `user${String(index + 1).padStart(3, '0')}`,
        skill_item_id: 'js-001',
        skill_level: (index % 4) + 1,
        self_assessment: (index % 4) + 1,
        manager_assessment: null,
        last_used_date: new Date('2024-12-01'),
        acquisition_date: new Date('2024-01-01'),
        certification_id: null,
        evidence_description: `JavaScript開発経験 ${index + 1}`,
        skill_status: 'active',
        learning_hours: 100 + index,
        project_experience_count: 5 + index,
        is_deleted: false,
        created_at: new Date('2024-01-01'),
        updated_at: new Date('2024-12-01'),
      }));

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001',
        },
      ];

      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
        },
      ];

      // Prismaモックの設定（ページネーション対応）
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords.slice(0, 20)); // 1ページ目（20件）
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストの作成（ページネーション付き）
      const request = new NextRequest('http://localhost:3000/api/skills/search?keyword=JavaScript&page=1&limit=20');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data).toHaveLength(20);
      expect(responseData.pagination).toMatchObject({
        page: 1,
        limit: 20,
        total: 25,
        totalPages: 2,
      });
    });

    it('正常系: 検索結果が0件の場合', async () => {
      // 空のモックデータの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockResolvedValue([]);
      prisma.skillItem.findMany.mockResolvedValue([]);
      prisma.skillCategory.findMany.mockResolvedValue([]);

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/search?keyword=NonExistentSkill');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data).toHaveLength(0);
      expect(responseData.count).toBe(0);
    });

    it('正常系: データベースエラー時にモックデータを返す', async () => {
      // Prismaモックでエラーを発生させる
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockRejectedValue(new Error('Database connection failed'));

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/search?keyword=JavaScript');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.source).toBe('mock');
      expect(responseData.data).toBeDefined();
      expect(Array.isArray(responseData.data)).toBe(true);
    });

    it('異常系: 無効なページ番号が指定された場合', async () => {
      // リクエストの作成（無効なページ番号）
      const request = new NextRequest('http://localhost:3000/api/skills/search?keyword=JavaScript&page=0');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
      expect(responseData.error.message).toBe('ページ番号は1以上の整数である必要があります');
    });

    it('異常系: 無効なリミット値が指定された場合', async () => {
      // リクエストの作成（無効なリミット値）
      const request = new NextRequest('http://localhost:3000/api/skills/search?keyword=JavaScript&limit=101');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
      expect(responseData.error.message).toBe('リミット値は1から100の範囲で指定してください');
    });

    it('異常系: 無効なスキルレベルが指定された場合', async () => {
      // リクエストの作成（無効なスキルレベル）
      const request = new NextRequest('http://localhost:3000/api/skills/search?keyword=JavaScript&level=5');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
      expect(responseData.error.message).toBe('スキルレベルは1から4の範囲で指定してください');
    });

    it('正常系: 複数の検索条件を組み合わせた検索', async () => {
      // モックデータの設定
      const mockSkillRecords = [
        {
          id: 'skill-001',
          employee_id: 'user001',
          skill_item_id: 'js-001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: null,
          last_used_date: new Date('2024-12-01'),
          acquisition_date: new Date('2024-01-01'),
          certification_id: null,
          evidence_description: 'JavaScript開発経験',
          skill_status: 'active',
          learning_hours: 100,
          project_experience_count: 5,
          is_deleted: false,
          created_at: new Date('2024-01-01'),
          updated_at: new Date('2024-12-01'),
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001',
        },
      ];

      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストの作成（複数条件）
      const request = new NextRequest(
        'http://localhost:3000/api/skills/search?keyword=JavaScript&category=tech-001&level=3&status=active&page=1&limit=10'
      );

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data).toHaveLength(1);
      expect(responseData.data[0]).toMatchObject({
        skillName: 'JavaScript',
        skillCategoryId: 'tech-001',
        skillLevel: 3,
        skillStatus: 'active',
      });
    });

    it('異常系: 内部エラーが発生した場合', async () => {
      // NextRequestのコンストラクタでエラーを発生させる
      const invalidRequest = {
        url: 'invalid-url',
        headers: {
          get: jest.fn().mockReturnValue(null),
        },
        cookies: {
          get: jest.fn().mockReturnValue(null),
        },
      } as unknown as NextRequest;

      // APIの実行
      const response = await GET(invalidRequest);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(500);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('INTERNAL_SERVER_ERROR');
      expect(responseData.error.message).toBe('スキル検索に失敗しました');
    });
  });
});
