/**
 * 統合テスト: ログインAPI
 * 要求仕様ID: TNT.3-AUTH.1, ACC.1-AUTH.1
 * テスト対象: src/app/api/auth/login/route.ts
 */

import { PrismaClient } from '@prisma/client'
import { setupTestDatabase, teardownTestDatabase, cleanupTestData } from '../../../helpers/setup'
import { createMockPOSTRequest } from '../../../helpers/mock-request'
import {
  createTestTenant,
  createTestDepartment,
  createTestEmployee,
  createTestUserAuth,
  createTestUserComplete
} from '../../../helpers/test-data-factory'

describe('API統合テスト: ログイン', () => {
  let prisma: PrismaClient
  let POST: (request: Request) => Promise<Response>

  beforeAll(async () => {
    prisma = await setupTestDatabase()

    // POST関数を動的インポート
    const module = await import('@/app/api/auth/login/route')
    POST = module.POST
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  beforeEach(async () => {
    await cleanupTestData(prisma)
  })

  describe('正常系テスト', () => {
    test('正しいログインIDとパスワードでログインできること', async () => {
      // Arrange: テストデータ作成
      const tenant = await createTestTenant(prisma, {
        tenant_code: 'DEFAULT',
        tenant_name: 'デフォルトテナント',
        domain_name: 'default.example.com'
      })

      const department = await createTestDepartment(prisma, {
        department_code: 'DEPT001',
        department_name: 'テスト部署'
      })

      const { employee, userAuth } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'test_user',
        email: 'test@example.com',
        password: 'password123',
        department_id: 'DEPT001'
      })

      // Act: ログインAPIを呼び出し
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: 'test_user',
          password: 'password123',
          tenantCode: 'DEFAULT'
        }
      )

      const response = await POST(request)
      const responseData = await response.json()

      // Assert: レスポンスの検証
      expect(response.status).toBe(200)
      expect(responseData.success).toBe(true)
      expect(responseData.data).toBeDefined()
      expect(responseData.data.accessToken).toBeDefined()
      expect(responseData.data.refreshToken).toBeDefined()
      expect(responseData.data.user).toBeDefined()
      expect(responseData.data.user.loginId).toBe('test_user')
      expect(responseData.data.user.employeeId).toBe(employee.id)
      expect(responseData.data.tenant).toBeDefined()
      expect(responseData.data.tenant.code).toBe('DEFAULT')
    })

    test('テナントコードを省略した場合、デフォルトテナントでログインできること', async () => {
      // Arrange
      const tenant = await createTestTenant(prisma, {
        tenant_code: 'DEFAULT',
        tenant_name: 'デフォルトテナント'
      })

      await createTestUserComplete(prisma, {
        login_id: 'user_without_tenant',
        password: 'password123'
      })

      // Act
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: 'user_without_tenant',
          password: 'password123'
        }
      )

      const response = await POST(request)
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(200)
      expect(responseData.success).toBe(true)
      expect(responseData.data.tenant.code).toBe('DEFAULT')
    })
  })

  describe('異常系テスト', () => {
    test('ログインIDが存在しない場合、401エラーが返ること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'DEFAULT'
      })

      // Act
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: 'nonexistent_user',
          password: 'password123',
          tenantCode: 'DEFAULT'
        }
      )

      const response = await POST(request)
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(401)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('AUTHENTICATION_ERROR')
      expect(responseData.error.message).toBe('ログインIDまたはパスワードが正しくありません')
    })

    test('パスワードが間違っている場合、401エラーが返ること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'DEFAULT'
      })

      await createTestUserComplete(prisma, {
        login_id: 'test_user',
        password: 'correct_password'
      })

      // Act
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: 'test_user',
          password: 'wrong_password',
          tenantCode: 'DEFAULT'
        }
      )

      const response = await POST(request)
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(401)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('AUTHENTICATION_ERROR')
    })

    test('ログインIDが未入力の場合、400エラーが返ること', async () => {
      // Act
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: '',
          password: 'password123'
        }
      )

      const response = await POST(request)
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(400)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('VALIDATION_ERROR')
      expect(responseData.error.message).toBe('ログインIDとパスワードは必須です')
    })

    test('パスワードが未入力の場合、400エラーが返ること', async () => {
      // Act
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: 'test_user',
          password: ''
        }
      )

      const response = await POST(request)
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(400)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('VALIDATION_ERROR')
    })

    test('存在しないテナントコードの場合、400エラーが返ること', async () => {
      // Arrange
      await createTestUserComplete(prisma, {
        login_id: 'test_user',
        password: 'password123'
      })

      // Act
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: 'test_user',
          password: 'password123',
          tenantCode: 'NONEXISTENT_TENANT'
        }
      )

      const response = await POST(request)
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(400)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('TENANT_NOT_FOUND')
    })
  })

  describe('データベーストランザクションテスト', () => {
    test('ログイン成功時、last_login_atが更新されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'DEFAULT'
      })

      const { userAuth } = await createTestUserComplete(prisma, {
        login_id: 'test_user',
        password: 'password123'
      })

      const beforeLogin = userAuth.last_login_at

      // Act
      const request = createMockPOSTRequest(
        'http://localhost:3000/api/auth/login',
        {
          loginId: 'test_user',
          password: 'password123',
          tenantCode: 'DEFAULT'
        }
      )

      await POST(request)

      // Assert: データベースの状態を確認
      const updatedUserAuth = await prisma.userAuth.findUnique({
        where: { user_id: userAuth.user_id }
      })

      expect(updatedUserAuth?.last_login_at).not.toBe(beforeLogin)
      expect(updatedUserAuth?.last_login_at).toBeInstanceOf(Date)
      expect(updatedUserAuth?.failed_login_count).toBe(0)
    })
  })
})
