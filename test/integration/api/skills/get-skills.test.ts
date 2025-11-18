/**
 * 統合テスト: スキル情報取得API
 * 要求仕様ID: SKL.1-GET.1
 * テスト対象: src/app/api/skills/[userId]/route.ts
 */

import { PrismaClient } from '@prisma/client'
import { setupTestDatabase, teardownTestDatabase, cleanupTestData } from '../../../helpers/setup'
import { createAuthenticatedMockRequest, createMockGETRequest } from '../../../helpers/mock-request'
import {
  createTestTenant,
  createTestUserComplete,
  createTestSkillCategory,
  createTestSkillItem,
  createTestSkillRecord
} from '../../../helpers/test-data-factory'

describe('API統合テスト: スキル情報取得', () => {
  let prisma: PrismaClient
  let GET: (request: Request, context: any) => Promise<Response>

  beforeAll(async () => {
    prisma = await setupTestDatabase()

    // GET関数を動的インポート
    const module = await import('@/app/api/skills/[userId]/route')
    GET = module.GET
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  beforeEach(async () => {
    await cleanupTestData(prisma)
  })

  describe('正常系テスト', () => {
    test('認証済みユーザーが自分のスキル情報を取得できること', async () => {
      // Arrange: テストデータ作成
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'test_user',
        password: 'password123'
      })

      const category = await createTestSkillCategory(prisma, {
        category_code: 'CAT001',
        category_name: 'プログラミング'
      })

      const skillItem = await createTestSkillItem(prisma, {
        skill_code: 'SKILL001',
        skill_name: 'JavaScript',
        skill_category_id: 'CAT001'
      })

      await createTestSkillRecord(
        prisma,
        employee.id,
        'SKILL001',
        'TENANT001',
        'SYSTEM',
        {
          skill_level: 3,
          self_assessment: 3
        }
      )

      // Act: スキル情報取得APIを呼び出し
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/skills/${employee.id}`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: レスポンスの検証
      expect(response.status).toBe(200)
      expect(responseData.success).toBe(true)
      expect(responseData.data).toBeDefined()
      expect(responseData.data.summary.totalSkills).toBe(1)
      expect(responseData.data.skills).toHaveLength(1)
      expect(responseData.data.skills[0].categoryId).toBe('CAT001')
      expect(responseData.data.skills[0].categoryName).toBe('プログラミング')
      expect(responseData.data.skills[0].skills).toHaveLength(1)
      expect(responseData.data.skills[0].skills[0].skillName).toBe('JavaScript')
      expect(responseData.data.skills[0].skills[0].skillLevel).toBe(3)
    })

    test('userIdに"me"を指定すると認証ユーザー自身のスキルを取得できること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'test_user'
      })

      const skillItem = await createTestSkillItem(prisma, {
        skill_code: 'SKILL001',
        skill_name: 'TypeScript'
      })

      await createTestSkillRecord(
        prisma,
        employee.id,
        'SKILL001',
        'TENANT001',
        'SYSTEM'
      )

      // Act: 'me' パラメータでスキル取得
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skills/me',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: 'me' } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(200)
      expect(responseData.success).toBe(true)
      expect(responseData.data.summary.totalSkills).toBe(1)
    })

    test('カテゴリフィルターでスキルを絞り込めること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT001',
        category_name: 'プログラミング'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT002',
        category_name: 'データベース'
      })

      const skillItem1 = await createTestSkillItem(prisma, {
        skill_code: 'SKILL001',
        skill_name: 'JavaScript',
        skill_category_id: 'CAT001'
      })

      const skillItem2 = await createTestSkillItem(prisma, {
        skill_code: 'SKILL002',
        skill_name: 'PostgreSQL',
        skill_category_id: 'CAT002'
      })

      await createTestSkillRecord(
        prisma,
        employee.id,
        'SKILL001',
        'TENANT001',
        'SYSTEM'
      )

      await createTestSkillRecord(
        prisma,
        employee.id,
        'SKILL002',
        'TENANT001',
        'SYSTEM'
      )

      // Act: カテゴリフィルターを適用
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/skills/${employee.id}?categoryId=CAT001`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: CAT001のスキルのみ返却される
      expect(response.status).toBe(200)
      expect(responseData.success).toBe(true)
      expect(responseData.data.summary.totalSkills).toBe(1)
      expect(responseData.data.filters.categoryId).toBe('CAT001')
    })

    test('複数のスキルがカテゴリ別にグループ化されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await createTestSkillCategory(prisma, {
        category_code: 'CAT001',
        category_name: 'プログラミング'
      })

      // 同じカテゴリに複数スキル
      await createTestSkillItem(prisma, {
        skill_code: 'SKILL001',
        skill_name: 'JavaScript',
        skill_category_id: 'CAT001'
      })

      await createTestSkillItem(prisma, {
        skill_code: 'SKILL002',
        skill_name: 'TypeScript',
        skill_category_id: 'CAT001'
      })

      await createTestSkillRecord(
        prisma,
        employee.id,
        'SKILL001',
        'TENANT001',
        'SYSTEM',
        { skill_level: 3 }
      )

      await createTestSkillRecord(
        prisma,
        employee.id,
        'SKILL002',
        'TENANT001',
        'SYSTEM',
        { skill_level: 4 }
      )

      // Act
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/skills/${employee.id}`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: 1つのカテゴリに2つのスキル
      expect(response.status).toBe(200)
      expect(responseData.data.summary.totalSkills).toBe(2)
      expect(responseData.data.skills).toHaveLength(1)
      expect(responseData.data.skills[0].skills).toHaveLength(2)
      expect(responseData.data.skills[0].categoryName).toBe('プログラミング')
    })
  })

  describe('異常系テスト', () => {
    test('認証なしでアクセスすると401エラーが返ること', async () => {
      // Act: 認証なしでリクエスト
      const request = createMockGETRequest(
        'http://localhost:3000/api/skills/EMP001'
      )

      const response = await GET(request, { params: { userId: 'EMP001' } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(401)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('AUTHENTICATION_ERROR')
    })

    test('他人のスキル情報にアクセスすると403エラーが返ること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee: employee1 } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'user1'
      })

      const { employee: employee2 } = await createTestUserComplete(prisma, {
        employee_code: 'EMP002',
        login_id: 'user2'
      })

      // Act: employee1として employee2のスキルにアクセス
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/skills/${employee2.id}`,
        employee1.id,
        {
          method: 'GET',
          employeeId: employee1.id
        }
      )

      const response = await GET(request, { params: { userId: employee2.id } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(403)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('AUTHORIZATION_ERROR')
      expect(responseData.error.message).toBe('自分以外のスキル情報にはアクセスできません')
    })

    test('存在しないユーザーIDを指定すると404エラーが返ること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // Act: 存在しないユーザーID
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/skills/NONEXISTENT',
        employee.id,
        {
          method: 'GET',
          employeeId: 'NONEXISTENT'
        }
      )

      const response = await GET(request, { params: { userId: 'NONEXISTENT' } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(404)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('NOT_FOUND')
    })
  })

  describe('スキルレベル表記テスト', () => {
    test('スキルレベルが正しく日本語表記に変換されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      const skillItem = await createTestSkillItem(prisma, {
        skill_code: 'SKILL001',
        skill_name: 'JavaScript'
      })

      await createTestSkillRecord(
        prisma,
        employee.id,
        'SKILL001',
        'TENANT001',
        'SYSTEM',
        {
          skill_level: 4,
          self_assessment: 3
        }
      )

      // Act
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/skills/${employee.id}`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: レベル4は◎、レベル3は○
      expect(responseData.data.skills[0].skills[0].skillLevelDisplay).toBe('◎')
      expect(responseData.data.skills[0].skills[0].selfAssessmentDisplay).toBe('○')
    })
  })

  describe('サマリー情報テスト', () => {
    test('スキルレベル別の集計が正しく計算されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 異なるレベルのスキルを複数作成
      for (let i = 1; i <= 4; i++) {
        await createTestSkillItem(prisma, {
          skill_code: `SKILL00${i}`,
          skill_name: `Skill ${i}`
        })

        await createTestSkillRecord(
          prisma,
          employee.id,
          `SKILL00${i}`,
          'TENANT001',
          'SYSTEM',
          { skill_level: i }
        )
      }

      // Act
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/skills/${employee.id}`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: 各レベル1件ずつ
      expect(responseData.data.summary.totalSkills).toBe(4)
      expect(responseData.data.summary.skillsByLevel['×']).toBe(1)
      expect(responseData.data.summary.skillsByLevel['△']).toBe(1)
      expect(responseData.data.summary.skillsByLevel['○']).toBe(1)
      expect(responseData.data.summary.skillsByLevel['◎']).toBe(1)
    })
  })
})
