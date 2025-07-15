/**
 * 要求仕様ID: API-021, API-022
 * 対応設計書: docs/design/api/specs/API定義書_API-021_スキル情報取得API.md
 * 対応設計書: docs/design/api/specs/API定義書_API-022_スキル情報更新API.md
 * テスト内容: スキル情報取得・更新APIのテスト
 */

import { NextRequest } from 'next/server';
import { GET, POST } from '@/app/api/skills/route';

// Prismaのモック
jest.mock('@/lib/prisma', () => ({
  prisma: {
    skillRecord: {
      findMany: jest.fn(),
      create: jest.fn(),
    },
    skillItem: {
      findMany: jest.fn(),
      findUnique: jest.fn(),
    },
    skillCategory: {
      findMany: jest.fn(),
      findUnique: jest.fn(),
    },
  },
}));

describe('スキル情報API テスト', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /api/skills - スキル情報取得', () => {
    it('正常系: ユーザーのスキル情報を正常に取得できる', async () => {
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
      const request = new NextRequest('http://localhost:3000/api/skills?userId=user001');

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

    it('正常系: データベースエラー時にモックデータを返す', async () => {
      // Prismaモックでエラーを発生させる
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.findMany.mockRejectedValue(new Error('Database connection failed'));

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills?userId=1');

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
      expect(responseData.error.message).toBe('スキル情報の取得に失敗しました');
    });
  });

  describe('POST /api/skills - スキル情報作成', () => {
    it('正常系: 新しいスキル情報を正常に作成できる', async () => {
      // モックデータの設定
      const mockCreatedRecord = {
        id: 'skill-new-001',
        tenant_id: 'default',
        employee_id: 'user001',
        skill_item_id: 'react-001',
        skill_level: 4,
        self_assessment: 4,
        manager_assessment: null,
        last_used_date: new Date('2024-12-01'),
        acquisition_date: new Date('2024-06-01'),
        certification_id: null,
        evidence_description: 'React開発プロジェクト参加',
        skill_status: 'active',
        learning_hours: 80,
        project_experience_count: 3,
        is_deleted: false,
        created_at: new Date(),
        updated_at: new Date(),
        created_by: 'user001',
        updated_by: 'user001',
      };

      const mockSkillItem = {
        skill_code: 'react-001',
        skill_name: 'React',
        skill_category_id: 'frontend-001',
      };

      const mockSkillCategory = {
        category_code: 'frontend-001',
        category_name: 'フロントエンド',
      };

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.create.mockResolvedValue(mockCreatedRecord);
      prisma.skillItem.findUnique.mockResolvedValue(mockSkillItem);
      prisma.skillCategory.findUnique.mockResolvedValue(mockSkillCategory);

      // リクエストボディの作成
      const requestBody = {
        employeeId: 'user001',
        skillItemId: 'react-001',
        skillLevel: 4,
        selfAssessment: 4,
        lastUsedDate: '2024-12-01',
        acquisitionDate: '2024-06-01',
        evidenceDescription: 'React開発プロジェクト参加',
        skillStatus: 'active',
        learningHours: 80,
        projectExperienceCount: 3,
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(201);
      expect(responseData.success).toBe(true);
      expect(responseData.data).toMatchObject({
        id: 'skill-new-001',
        userId: 'user001',
        skillCategoryId: 'frontend-001',
        skillCategoryName: 'フロントエンド',
        skillName: 'React',
        skillLevel: 4,
        selfAssessment: 4,
        lastUsedDate: '2024-12-01',
        acquisitionDate: '2024-06-01',
        evidenceDescription: 'React開発プロジェクト参加',
        skillStatus: 'active',
        learningHours: 80,
        projectExperienceCount: 3,
      });
    });

    it('異常系: 必須パラメータが不足している場合', async () => {
      // 不完全なリクエストボディ
      const requestBody = {
        skillLevel: 3,
        // employeeId, skillItemId が不足
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
      expect(responseData.error.message).toBe('スキルアイテムID、スキルレベル、従業員IDは必須です');
    });

    it('異常系: スキルレベルが範囲外の場合', async () => {
      // 無効なスキルレベルのリクエストボディ
      const requestBody = {
        employeeId: 'user001',
        skillItemId: 'js-001',
        skillLevel: 5, // 範囲外（1-4が有効）
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
      expect(responseData.error.message).toBe('スキルレベルは1から4の範囲で入力してください');
    });

    it('正常系: データベースエラー時にモック作成を実行', async () => {
      // Prismaモックでエラーを発生させる
      const { prisma } = require('@/lib/prisma');
      prisma.skillRecord.create.mockRejectedValue(new Error('Database connection failed'));

      // リクエストボディの作成
      const requestBody = {
        employeeId: 'user001',
        skillItemId: 'js-001',
        skillLevel: 3,
        skillName: 'JavaScript',
        skillCategoryId: 1,
        experienceYears: 2,
        lastUsedDate: '2024-12-01',
        certifications: [],
        projects: [],
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills', {
        method: 'POST',
        body: JSON.stringify(requestBody),
        headers: {
          'Content-Type': 'application/json',
        },
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(201);
      expect(responseData.success).toBe(true);
      expect(responseData.source).toBe('mock');
      expect(responseData.data).toBeDefined();
      expect(responseData.data.skillLevel).toBe(3);
    });
  });
});
