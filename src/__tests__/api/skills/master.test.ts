/**
 * 要求仕様ID: API-023
 * 対応設計書: docs/design/api/specs/API定義書_API-023_スキルマスタ取得API.md
 * テスト内容: スキルマスタ取得APIのテスト
 */

import { NextRequest } from 'next/server';
import { GET } from '@/app/api/skills/master/route';

// Prismaのモック
jest.mock('@/lib/prisma', () => ({
  prisma: {
    skillCategory: {
      findMany: jest.fn(),
    },
    skillItem: {
      findMany: jest.fn(),
    },
  },
}));

describe('スキルマスタAPI テスト', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('GET /api/skills/master - スキルマスタ取得', () => {
    it('正常系: スキルマスタ情報を正常に取得できる', async () => {
      // モックデータの設定
      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
          parent_category_code: null,
          category_level: 1,
          display_order: 1,
          is_active: true,
          description: 'プログラミング言語に関するスキル',
        },
        {
          category_code: 'tech-002',
          category_name: 'フレームワーク',
          parent_category_code: null,
          category_level: 1,
          display_order: 2,
          is_active: true,
          description: 'フレームワークに関するスキル',
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001',
          skill_level_definition: JSON.stringify({
            1: '基本的な構文を理解している',
            2: '簡単なアプリケーションを作成できる',
            3: '複雑なアプリケーションを作成できる',
            4: '他者に指導できるレベル',
          }),
          is_active: true,
          display_order: 1,
          description: 'JavaScript プログラミング言語',
        },
        {
          skill_code: 'react-001',
          skill_name: 'React',
          skill_category_id: 'tech-002',
          skill_level_definition: JSON.stringify({
            1: '基本的なコンポーネントを作成できる',
            2: 'Hooksを使用したアプリケーションを作成できる',
            3: '状態管理を含む複雑なアプリケーションを作成できる',
            4: 'パフォーマンス最適化やアーキテクチャ設計ができる',
          }),
          is_active: true,
          display_order: 1,
          description: 'React フロントエンドライブラリ',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/master');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.categories).toHaveLength(2);
      expect(responseData.data.skills).toHaveLength(2);

      // カテゴリデータの検証
      expect(responseData.data.categories[0]).toMatchObject({
        categoryCode: 'tech-001',
        categoryName: 'プログラミング言語',
        parentCategoryCode: null,
        categoryLevel: 1,
        displayOrder: 1,
        isActive: true,
        description: 'プログラミング言語に関するスキル',
      });

      // スキルアイテムデータの検証
      expect(responseData.data.skills[0]).toMatchObject({
        skillCode: 'js-001',
        skillName: 'JavaScript',
        skillCategoryId: 'tech-001',
        isActive: true,
        displayOrder: 1,
        description: 'JavaScript プログラミング言語',
      });

      // スキルレベル定義の検証
      expect(responseData.data.skills[0].skillLevelDefinition).toEqual({
        1: '基本的な構文を理解している',
        2: '簡単なアプリケーションを作成できる',
        3: '複雑なアプリケーションを作成できる',
        4: '他者に指導できるレベル',
      });

      expect(responseData.timestamp).toBeDefined();
    });

    it('正常系: カテゴリフィルタを指定してスキルマスタを取得', async () => {
      // モックデータの設定（フィルタ後）
      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
          parent_category_code: null,
          category_level: 1,
          display_order: 1,
          is_active: true,
          description: 'プログラミング言語に関するスキル',
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001',
          skill_level_definition: JSON.stringify({
            1: '基本的な構文を理解している',
            2: '簡単なアプリケーションを作成できる',
            3: '複雑なアプリケーションを作成できる',
            4: '他者に指導できるレベル',
          }),
          is_active: true,
          display_order: 1,
          description: 'JavaScript プログラミング言語',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);

      // リクエストの作成（カテゴリフィルタ付き）
      const request = new NextRequest('http://localhost:3000/api/skills/master?category=tech-001');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.categories).toHaveLength(1);
      expect(responseData.data.skills).toHaveLength(1);
      expect(responseData.data.categories[0].categoryCode).toBe('tech-001');
      expect(responseData.data.skills[0].skillCategoryId).toBe('tech-001');
    });

    it('正常系: データベースエラー時にモックデータを返す', async () => {
      // Prismaモックでエラーを発生させる
      const { prisma } = require('@/lib/prisma');
      prisma.skillCategory.findMany.mockRejectedValue(new Error('Database connection failed'));

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/master');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.source).toBe('mock');
      expect(responseData.data.categories).toBeDefined();
      expect(responseData.data.skills).toBeDefined();
      expect(Array.isArray(responseData.data.categories)).toBe(true);
      expect(Array.isArray(responseData.data.skills)).toBe(true);
    });

    it('正常系: 空のデータセットを正常に処理', async () => {
      // 空のモックデータの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillCategory.findMany.mockResolvedValue([]);
      prisma.skillItem.findMany.mockResolvedValue([]);

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/master');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.categories).toHaveLength(0);
      expect(responseData.data.skills).toHaveLength(0);
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
      expect(responseData.error.message).toBe('スキルマスタ情報の取得に失敗しました');
    });

    it('正常系: 階層構造のカテゴリを正常に処理', async () => {
      // 階層構造のモックデータ
      const mockSkillCategories = [
        {
          category_code: 'tech-001',
          category_name: 'プログラミング言語',
          parent_category_code: null,
          category_level: 1,
          display_order: 1,
          is_active: true,
          description: 'プログラミング言語に関するスキル',
        },
        {
          category_code: 'tech-001-01',
          category_name: 'JavaScript系',
          parent_category_code: 'tech-001',
          category_level: 2,
          display_order: 1,
          is_active: true,
          description: 'JavaScript関連の技術',
        },
        {
          category_code: 'tech-001-02',
          category_name: 'Python系',
          parent_category_code: 'tech-001',
          category_level: 2,
          display_order: 2,
          is_active: true,
          description: 'Python関連の技術',
        },
      ];

      const mockSkillItems = [
        {
          skill_code: 'js-001',
          skill_name: 'JavaScript',
          skill_category_id: 'tech-001-01',
          skill_level_definition: JSON.stringify({
            1: '基本的な構文を理解している',
            2: '簡単なアプリケーションを作成できる',
            3: '複雑なアプリケーションを作成できる',
            4: '他者に指導できるレベル',
          }),
          is_active: true,
          display_order: 1,
          description: 'JavaScript プログラミング言語',
        },
      ];

      // Prismaモックの設定
      const { prisma } = require('@/lib/prisma');
      prisma.skillCategory.findMany.mockResolvedValue(mockSkillCategories);
      prisma.skillItem.findMany.mockResolvedValue(mockSkillItems);

      // リクエストの作成
      const request = new NextRequest('http://localhost:3000/api/skills/master');

      // APIの実行
      const response = await GET(request);
      const responseData = await response.json();

      // レスポンスの検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.categories).toHaveLength(3);
      
      // 階層構造の検証
      const parentCategory = responseData.data.categories.find(
        (cat: any) => cat.categoryCode === 'tech-001'
      );
      const childCategory = responseData.data.categories.find(
        (cat: any) => cat.categoryCode === 'tech-001-01'
      );
      
      expect(parentCategory.parentCategoryCode).toBeNull();
      expect(parentCategory.categoryLevel).toBe(1);
      expect(childCategory.parentCategoryCode).toBe('tech-001');
      expect(childCategory.categoryLevel).toBe(2);
    });
  });
});
