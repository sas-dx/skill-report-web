/**
 * 統合テスト: 作業実績取得API
 * 要求仕様ID: WPM.1-DET.1
 * テスト対象: src/app/api/work/[userId]/route.ts
 */

import { PrismaClient } from '@prisma/client'
import { setupTestDatabase, teardownTestDatabase, cleanupTestData } from '../../../helpers/setup'
import { createAuthenticatedMockRequest, createMockGETRequest } from '../../../helpers/mock-request'
import {
  createTestTenant,
  createTestUserComplete,
  createTestProjectRecord
} from '../../../helpers/test-data-factory'

describe('API統合テスト: 作業実績取得', () => {
  let prisma: PrismaClient
  let GET: (request: Request, context: any) => Promise<Response>

  beforeAll(async () => {
    prisma = await setupTestDatabase()

    // GET関数を動的インポート
    const module = await import('@/app/api/work/[userId]/route')
    GET = module.GET
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  beforeEach(async () => {
    await cleanupTestData(prisma)
  })

  describe('正常系テスト', () => {
    test('認証済みユーザーが自分の作業実績を取得できること', async () => {
      // Arrange: テストデータ作成
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'test_user',
        password: 'password123'
      })

      await createTestProjectRecord(
        prisma,
        employee.id,
        'TENANT001',
        'SYSTEM',
        {
          project_name: 'テストプロジェクト1',
          project_code: 'PRJ001'
        }
      )

      // Act: 作業実績取得APIを呼び出し
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee.id}`,
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
      expect(responseData.data.records).toHaveLength(1)
      expect(responseData.data.records[0].projectName).toBe('テストプロジェクト1')
      expect(responseData.data.records[0].projectCode).toBe('PRJ001')
      expect(responseData.data.summary).toBeDefined()
      expect(responseData.data.summary.total_projects).toBe(1)
    })

    test('userIdに"me"を指定すると認証ユーザー自身の作業実績を取得できること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'test_user'
      })

      await createTestProjectRecord(
        prisma,
        employee.id,
        'TENANT001',
        'SYSTEM',
        {
          project_name: 'マイプロジェクト'
        }
      )

      // Act: 'me' パラメータで作業実績取得
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/work/me',
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
      expect(responseData.data.records).toHaveLength(1)
      expect(responseData.data.records[0].projectName).toBe('マイプロジェクト')
    })

    test('ページネーションが正しく機能すること', async () => {
      // Arrange: 複数のプロジェクトレコードを作成
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 15件のプロジェクトレコードを作成
      for (let i = 1; i <= 15; i++) {
        await createTestProjectRecord(
          prisma,
          employee.id,
          'TENANT001',
          'SYSTEM',
          {
            project_name: `プロジェクト${i}`,
            project_code: `PRJ${String(i).padStart(3, '0')}`
          }
        )
      }

      // Act: ページ1（limit 10）を取得
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee.id}?page=1&limit=10`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: 10件のレコードが返る
      expect(response.status).toBe(200)
      expect(responseData.data.records).toHaveLength(10)
      expect(responseData.data.summary.total_projects).toBe(15)
      expect(responseData.data.pagination.page).toBe(1)
      expect(responseData.data.pagination.limit).toBe(10)
      expect(responseData.data.pagination.total_pages).toBe(2)

      // Act: ページ2を取得
      const request2 = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee.id}?page=2&limit=10`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response2 = await GET(request2, { params: { userId: employee.id } })
      const responseData2 = await response2.json()

      // Assert: 残り5件のレコードが返る
      expect(responseData2.data.records).toHaveLength(5)
      expect(responseData2.data.pagination.page).toBe(2)
    })

    test('プロジェクトコードでフィルタリングできること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await createTestProjectRecord(
        prisma,
        employee.id,
        'TENANT001',
        'SYSTEM',
        {
          project_name: 'プロジェクトA',
          project_code: 'PRJ_A'
        }
      )

      await createTestProjectRecord(
        prisma,
        employee.id,
        'TENANT001',
        'SYSTEM',
        {
          project_name: 'プロジェクトB',
          project_code: 'PRJ_B'
        }
      )

      // Act: PRJ_Aでフィルター
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee.id}?projectCode=PRJ_A`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: PRJ_Aのみ返却される
      expect(response.status).toBe(200)
      expect(responseData.data.records).toHaveLength(1)
      expect(responseData.data.records[0].projectCode).toBe('PRJ_A')
    })

    test('年度でフィルタリングできること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 2023年のプロジェクト
      await prisma.projectRecord.create({
        data: {
          project_record_id: `PRJ_2023_${Date.now()}`,
          employee_id: employee.id,
          project_name: '2023年プロジェクト',
          project_code: 'PRJ2023',
          project_type: 'development',
          start_date: new Date('2023-06-01'),
          end_date: new Date('2023-12-31'),
          project_status: 'completed',
          is_confidential: false,
          is_public_reference: true,
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // 2024年のプロジェクト
      await prisma.projectRecord.create({
        data: {
          project_record_id: `PRJ_2024_${Date.now()}`,
          employee_id: employee.id,
          project_name: '2024年プロジェクト',
          project_code: 'PRJ2024',
          project_type: 'development',
          start_date: new Date('2024-01-01'),
          end_date: new Date('2024-12-31'),
          project_status: 'active',
          is_confidential: false,
          is_public_reference: true,
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // Act: 2023年でフィルター
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee.id}?year=2023`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: 2023年のプロジェクトのみ返却される
      expect(response.status).toBe(200)
      expect(responseData.data.records).toHaveLength(1)
      expect(responseData.data.records[0].projectCode).toBe('PRJ2023')
    })

    test('ステータスでフィルタリングできること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // アクティブなプロジェクト
      await prisma.projectRecord.create({
        data: {
          project_record_id: `PRJ_ACTIVE_${Date.now()}`,
          employee_id: employee.id,
          project_name: 'アクティブプロジェクト',
          project_code: 'PRJ_ACTIVE',
          project_type: 'development',
          start_date: new Date('2024-01-01'),
          project_status: 'ACTIVE',
          is_confidential: false,
          is_public_reference: true,
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // 完了したプロジェクト
      await prisma.projectRecord.create({
        data: {
          project_record_id: `PRJ_COMPLETED_${Date.now()}`,
          employee_id: employee.id,
          project_name: '完了プロジェクト',
          project_code: 'PRJ_COMPLETED',
          project_type: 'development',
          start_date: new Date('2023-01-01'),
          end_date: new Date('2023-12-31'),
          project_status: 'COMPLETED',
          is_confidential: false,
          is_public_reference: true,
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // Act: ACTIVEステータスでフィルター
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee.id}?status=ACTIVE`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: アクティブなプロジェクトのみ返却される
      expect(response.status).toBe(200)
      expect(responseData.data.records).toHaveLength(1)
      expect(responseData.data.records[0].projectStatus).toBe('ACTIVE')
    })
  })

  describe('異常系テスト', () => {
    test('他人の作業実績にアクセスすると403エラーが返ること', async () => {
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

      // Act: employee1として employee2の作業実績にアクセス
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee2.id}`,
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
    })

    test('userIdパラメータが未指定の場合、400エラーが返ること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // Act: userIdが空
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/work/',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: '' } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(400)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('INVALID_PARAMETER')
    })
  })

  describe('サマリー情報テスト', () => {
    test('プロジェクトステータス別の集計が正しく計算されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 各ステータスのプロジェクトを作成
      const statuses = ['ACTIVE', 'COMPLETED', 'ON_HOLD']
      for (const status of statuses) {
        await prisma.projectRecord.create({
          data: {
            project_record_id: `PRJ_${status}_${Date.now()}`,
            employee_id: employee.id,
            project_name: `${status}プロジェクト`,
            project_code: `PRJ_${status}`,
            project_type: 'development',
            start_date: new Date('2024-01-01'),
            project_status: status,
            is_confidential: false,
            is_public_reference: true,
            tenant_id: 'TENANT001',
            created_by: 'SYSTEM',
            updated_by: 'SYSTEM'
          }
        })
      }

      // Act
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/work/${employee.id}`,
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      )

      const response = await GET(request, { params: { userId: employee.id } })
      const responseData = await response.json()

      // Assert: 各ステータス1件ずつ
      expect(responseData.data.summary.total_projects).toBe(3)
      expect(responseData.data.summary.active_projects).toBe(1)
      expect(responseData.data.summary.completed_projects).toBe(1)
      expect(responseData.data.summary.on_hold_projects).toBe(1)
    })
  })
})
