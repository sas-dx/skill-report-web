/**
 * 統合テスト: スキルカテゴリマスタAPI
 * 要求仕様ID: SKL.1-CAT.1
 * テスト対象: src/app/api/skill-categories/route.ts
 */

import { PrismaClient } from '@prisma/client'
import { setupTestDatabase, teardownTestDatabase, cleanupTestData } from '../../../helpers/setup'
import { createAuthenticatedMockRequest, createMockGETRequest } from '../../../helpers/mock-request'
import {
  createTestTenant,
  createTestUserComplete,
  createTestSkillCategory
} from '../../../helpers/test-data-factory'

describe('API統合テスト: スキルカテゴリマスタ取得', () => {
  let prisma: PrismaClient
  let GET: (request: Request) => Promise<Response>

  beforeAll(async () => {
    prisma = await setupTestDatabase()

    // GET関数を動的インポート
    const module = await import('@/app/api/skill-categories/route')
    GET = module.GET
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  beforeEach(async () => {
    await cleanupTestData(prisma)
  })

  describe('正常系テスト', () => {
    test('認証済みユーザーがスキルカテゴリ一覧を取得できること', async () => {
      // Arrange: テストデータ作成
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'test_user',
        password: 'password123'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT001',
        category_name: 'プログラミング'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT002',
        category_name: 'データベース'
      })

      // Act: スキルカテゴリ取得APIを呼び出し
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: レスポンスの検証
      expect(response.status).toBe(200)
      expect(responseData.success).toBe(true)
      expect(responseData.data).toBeDefined()
      expect(responseData.data.flatCategories).toHaveLength(2)
      expect(responseData.data.summary).toBeDefined()
      expect(responseData.data.summary.totalCategories).toBe(2)
    })

    test('activeOnlyパラメータでアクティブなカテゴリのみ取得できること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // アクティブなカテゴリ
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT_ACTIVE',
          category_name: 'アクティブカテゴリ',
          category_type: 'technical',
          category_level: 1,
          display_order: 1,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: true
        }
      })

      // 非アクティブなカテゴリ
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT_INACTIVE',
          category_name: '非アクティブカテゴリ',
          category_type: 'technical',
          category_level: 1,
          display_order: 2,
          category_status: 'inactive',
          is_system_category: false,
          is_leaf_category: true
        }
      })

      // Act: activeOnly=true（デフォルト）で取得
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories?activeOnly=true',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: アクティブなカテゴリのみ返却される
      expect(response.status).toBe(200)
      expect(responseData.data.flatCategories).toHaveLength(1)
      expect(responseData.data.flatCategories[0].categoryName).toBe('アクティブカテゴリ')
    })

    test('階層構造が正しく構築されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 親カテゴリ
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT_PARENT',
          category_name: '親カテゴリ',
          category_type: 'technical',
          category_level: 1,
          display_order: 1,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: false
        }
      })

      // 子カテゴリ
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT_CHILD',
          category_name: '子カテゴリ',
          parent_category_id: 'CAT_PARENT',
          category_type: 'technical',
          category_level: 2,
          display_order: 1,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: true
        }
      })

      // Act
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: 階層構造が正しい
      expect(responseData.data.hierarchicalCategories).toHaveLength(1)
      expect(responseData.data.hierarchicalCategories[0].categoryName).toBe('親カテゴリ')
      expect(responseData.data.hierarchicalCategories[0].children).toHaveLength(1)
      expect(responseData.data.hierarchicalCategories[0].children[0].categoryName).toBe('子カテゴリ')
    })

    test('表示順でソートされること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 表示順3
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT003',
          category_name: 'カテゴリC',
          category_type: 'technical',
          category_level: 1,
          display_order: 3,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: true
        }
      })

      // 表示順1
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT001',
          category_name: 'カテゴリA',
          category_type: 'technical',
          category_level: 1,
          display_order: 1,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: true
        }
      })

      // 表示順2
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT002',
          category_name: 'カテゴリB',
          category_type: 'technical',
          category_level: 1,
          display_order: 2,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: true
        }
      })

      // Act
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: 表示順でソートされている
      expect(responseData.data.flatCategories[0].categoryName).toBe('カテゴリA')
      expect(responseData.data.flatCategories[1].categoryName).toBe('カテゴリB')
      expect(responseData.data.flatCategories[2].categoryName).toBe('カテゴリC')
    })

    test('フラット形式と階層形式の両方が返されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT001',
        category_name: 'テストカテゴリ'
      })

      // Act
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: 両方の形式が返される
      expect(responseData.data.flatCategories).toBeDefined()
      expect(responseData.data.hierarchicalCategories).toBeDefined()
      expect(responseData.data.flatCategories).toHaveLength(1)
      expect(responseData.data.hierarchicalCategories).toHaveLength(1)
    })
  })

  describe('異常系テスト', () => {
    test('認証なしでアクセスすると401エラーが返ること', async () => {
      // Act: 認証なしでリクエスト
      const request = createMockGETRequest(
        'http://localhost:3000/api/skill-categories'
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(401)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('AUTHENTICATION_ERROR')
    })
  })

  describe('サマリー情報テスト', () => {
    test('カテゴリ統計が正しく計算されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // アクティブなシステムカテゴリ
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT_SYS',
          category_name: 'システムカテゴリ',
          category_type: 'technical',
          category_level: 1,
          display_order: 1,
          category_status: 'active',
          is_system_category: true,
          is_leaf_category: true
        }
      })

      // アクティブなユーザーカテゴリ（リーフ）
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT_USER',
          category_name: 'ユーザーカテゴリ',
          category_type: 'technical',
          category_level: 1,
          display_order: 2,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: true
        }
      })

      // 親カテゴリ（非リーフ）
      await prisma.skillCategory.create({
        data: {
          category_code: 'CAT_PARENT',
          category_name: '親カテゴリ',
          category_type: 'technical',
          category_level: 1,
          display_order: 3,
          category_status: 'active',
          is_system_category: false,
          is_leaf_category: false
        }
      })

      // Act
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: 統計情報が正しい
      expect(responseData.data.summary.totalCategories).toBe(3)
      expect(responseData.data.summary.activeCategories).toBe(3)
      expect(responseData.data.summary.systemCategories).toBe(1)
      expect(responseData.data.summary.leafCategories).toBe(2)
    })

    test('最終更新日が返されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT001',
        category_name: 'テストカテゴリ'
      })

      // Act
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: 最終更新日が数値で返される
      expect(responseData.data.summary.lastUpdated).toBeGreaterThan(0)
      expect(typeof responseData.data.summary.lastUpdated).toBe('number')
    })
  })

  describe('フィルター情報テスト', () => {
    test('適用されたフィルター情報が返されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT001',
        category_name: 'テストカテゴリ'
      })

      // Act: includeHierarchy=true, includeStats=true, activeOnly=true
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skill-categories?includeHierarchy=true&includeStats=true&activeOnly=true',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request)
      const responseData = await response.json()

      // Assert: フィルター情報が返される
      expect(responseData.data.filters).toBeDefined()
      expect(responseData.data.filters.includeHierarchy).toBe(true)
      expect(responseData.data.filters.includeStats).toBe(true)
      expect(responseData.data.filters.activeOnly).toBe(true)
    })
  })
})
