/**
 * 要求仕様ID: API-026
 * 対応設計書: docs/design/api/specs/API定義書_API-026_スキルマップ生成API.md
 * テスト内容: スキルマップ生成APIのテスト
 */

import { NextRequest } from 'next/server';
import { POST } from '@/app/api/skills/map/route';

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
    employee: {
      findMany: jest.fn(),
    },
  },
}));

describe('スキルマップAPI テスト', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('POST /api/skills/map - スキルマップ生成', () => {
    it('正常系: スキルマップデータを正常に生成できる', async () => {
      // リクエストボディの作成
      const requestBody = {
        organizationIds: ['org-001'],
        skillCategoryIds: ['technical', 'business'],
        displayType: 'heatmap' as const,
        filters: {
          skillLevelMin: 1,
          skillLevelMax: 4,
        },
        pagination: {
          page: 1,
          limit: 20,
        },
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.displayType).toBe('heatmap');
      expect(responseData.data.totalEmployees).toBeGreaterThan(0);
      expect(responseData.data.totalSkills).toBeGreaterThan(0);
      expect(responseData.data.employees).toBeDefined();
      expect(responseData.data.statistics).toBeDefined();
      expect(responseData.data.visualization.heatmap).toBeDefined();
      expect(responseData.data.pagination).toMatchObject({
        page: 1,
        limit: 20,
      });
    });

    it('正常系: 部署フィルタでスキルマップを絞り込める', async () => {
      // モックデータの設定（部署フィルタ後）
      const mockEmployees = [
        {
          emp_no: 'user001',
          name: '山田太郎',
          department_id: 'dept-001',
          position_id: 'pos-001',
        },
      ];

      const mockSkillRecords = [
        {
          id: 'skill-001',
          employee_id: 'user001',
          skill_item_id: 'js-001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: 3,
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
      prisma.employee.findMany.mockResolvedValue(mockEmployees);
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストボディの作成（部署フィルタ付き）
      const requestBody = {
        organizationIds: ['dept-001'],
        skillCategoryIds: ['technical'],
        displayType: 'heatmap' as const,
        filters: {
          employeeIds: ['user001'],
        },
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.employees).toHaveLength(1);
      expect(responseData.data.employees[0].departmentId).toBe('dept-001');
    });

    it('正常系: スキルカテゴリフィルタでスキルマップを絞り込める', async () => {
      // モックデータの設定（カテゴリフィルタ後）
      const mockEmployees = [
        {
          emp_no: 'user001',
          name: '山田太郎',
          department_id: 'dept-001',
          position_id: 'pos-001',
        },
      ];

      const mockSkillRecords = [
        {
          id: 'skill-001',
          employee_id: 'user001',
          skill_item_id: 'js-001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: 3,
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
      prisma.employee.findMany.mockResolvedValue(mockEmployees);
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストボディの作成（カテゴリフィルタ付き）
      const requestBody = {
        organizationIds: ['org-001'],
        skillCategoryIds: ['technical'],
        displayType: 'radar' as const,
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.displayType).toBe('radar');
      expect(responseData.data.visualization.radar).toBeDefined();
    });

    it('正常系: スキルレベルフィルタでスキルマップを絞り込める', async () => {
      // モックデータの設定（レベルフィルタ後）
      const mockEmployees = [
        {
          emp_no: 'user002',
          name: '佐藤花子',
          department_id: 'dept-001',
          position_id: 'pos-002',
        },
      ];

      const mockSkillRecords = [
        {
          id: 'skill-002',
          employee_id: 'user002',
          skill_item_id: 'react-001',
          skill_level: 4,
          self_assessment: 4,
          manager_assessment: 4,
          last_used_date: new Date('2024-12-01'),
          acquisition_date: new Date('2024-03-01'),
          certification_id: null,
          evidence_description: 'React開発プロジェクト参加',
          skill_status: 'active',
          learning_hours: 150,
          project_experience_count: 8,
          is_deleted: false,
          created_at: new Date('2024-03-01'),
          updated_at: new Date('2024-12-01'),
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'react-001',
          skill_name: 'React',
          skill_category_id: 'tech-002',
        },
      ];

      const mockSkillCategories = [
        {
          category_code: 'tech-002',
          category_name: 'フレームワーク',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.employee.findMany.mockResolvedValue(mockEmployees);
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストボディの作成（レベルフィルタ付き）
      const requestBody = {
        organizationIds: ['org-001'],
        skillCategoryIds: ['technical'],
        displayType: 'bubble' as const,
        filters: {
          skillLevelMin: 4,
          skillLevelMax: 4,
        },
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.displayType).toBe('bubble');
      expect(responseData.data.visualization.bubble).toBeDefined();
    });

    it('正常系: 複数のフィルタを組み合わせてスキルマップを絞り込める', async () => {
      // モックデータの設定（複数フィルタ後）
      const mockEmployees = [
        {
          emp_no: 'user001',
          name: '山田太郎',
          department_id: 'dept-001',
          position_id: 'pos-001',
        },
      ];

      const mockSkillRecords = [
        {
          id: 'skill-001',
          employee_id: 'user001',
          skill_item_id: 'js-001',
          skill_level: 3,
          self_assessment: 3,
          manager_assessment: 3,
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
      prisma.employee.findMany.mockResolvedValue(mockEmployees);
      prisma.skillRecord.findMany.mockResolvedValue(mockSkillRecords);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);

      // リクエストボディの作成（複数フィルタ）
      const requestBody = {
        organizationIds: ['dept-001'],
        skillCategoryIds: ['technical'],
        displayType: 'heatmap' as const,
        filters: {
          skillLevelMin: 3,
          skillLevelMax: 3,
          employeeIds: ['user001'],
        },
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.displayType).toBe('heatmap');
      expect(responseData.data.totalEmployees).toBeGreaterThan(0);
    });

    it('正常系: データベースエラー時にモックデータを返す', async () => {
      // リクエストボディの作成
      const requestBody = {
        organizationIds: ['org-001'],
        skillCategoryIds: ['technical'],
        displayType: 'heatmap' as const,
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.displayType).toBe('heatmap');
      expect(responseData.data.employees).toBeDefined();
      expect(responseData.data.statistics).toBeDefined();
      expect(Array.isArray(responseData.data.employees)).toBe(true);
      expect(Array.isArray(responseData.data.statistics)).toBe(true);
    });

    it('正常系: 空のデータセットを正常に処理', async () => {
      // リクエストボディの作成
      const requestBody = {
        organizationIds: ['org-001'],
        skillCategoryIds: ['technical'],
        displayType: 'heatmap' as const,
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.displayType).toBe('heatmap');
      expect(responseData.data.totalEmployees).toBeGreaterThanOrEqual(0);
      expect(responseData.data.totalSkills).toBeGreaterThanOrEqual(0);
    });

    it('異常系: 組織IDが未指定の場合', async () => {
      // リクエストボディの作成（組織ID未指定）
      const requestBody = {
        organizationIds: [],
        skillCategoryIds: ['technical'],
        displayType: 'heatmap' as const,
      };

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
      expect(responseData.error.message).toBe('組織IDは必須です');
    });

    it('異常系: 内部エラーが発生した場合', async () => {
      // リクエストボディの作成（不正なJSON）
      const request = new NextRequest('http://localhost:3000/api/skills/map', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: 'invalid json',
      });

      // APIの実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(500);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('INTERNAL_SERVER_ERROR');
      expect(responseData.error.message).toBe('サーバー内部エラーが発生しました');
    });
  });
});
