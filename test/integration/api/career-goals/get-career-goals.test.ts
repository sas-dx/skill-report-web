/**
 * 統合テスト: キャリア目標API
 * 要求仕様ID: CAR.1-PLAN.1
 * テスト対象: src/app/api/career-goals/[user_id]/route.ts
 */

import { PrismaClient } from '@prisma/client'
import { setupTestDatabase, teardownTestDatabase, cleanupTestData } from '../../../helpers/setup'
import { createMockGETRequest } from '../../../helpers/mock-request'
import {
  createTestTenant,
  createTestUserComplete,
  createTestGoalProgress
} from '../../../helpers/test-data-factory'

describe('API統合テスト: キャリア目標取得', () => {
  let prisma: PrismaClient
  let GET: (request: Request, context: any) => Promise<Response>

  beforeAll(async () => {
    prisma = await setupTestDatabase()

    // GET関数を動的インポート
    const module = await import('@/app/api/career-goals/[user_id]/route')
    GET = module.GET
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  beforeEach(async () => {
    await cleanupTestData(prisma)
  })

  describe('正常系テスト', () => {
    test('ユーザーのキャリア目標を取得できること', async () => {
      // Arrange: テストデータ作成
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001',
        login_id: 'test_user',
        password: 'password123'
      })

      await createTestGoalProgress(
        prisma,
        employee.id,
        'TENANT001',
        'SYSTEM',
        {
          goal_title: 'フルスタックエンジニアになる'
        }
      )

      // Act: キャリア目標取得APIを呼び出し
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}`
      )

      // x-user-idヘッダーを追加
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert: レスポンスの検証
      expect(response.status).toBe(200)
      expect(responseData.success).toBe(true)
      expect(responseData.data).toBeDefined()
      expect(responseData.data.goals).toBeDefined()
      expect(responseData.data.goals).toHaveLength(1)
      expect(responseData.data.goals[0].title).toBe('フルスタックエンジニアになる')
      expect(responseData.data.stats).toBeDefined()
      expect(responseData.data.stats.totalGoals).toBe(1)
    })

    test('ヘッダーのx-user-idが優先されること', async () => {
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

      await createTestGoalProgress(
        prisma,
        employee1.id,
        'TENANT001',
        'SYSTEM',
        {
          goal_title: 'Employee1の目標'
        }
      )

      await createTestGoalProgress(
        prisma,
        employee2.id,
        'TENANT001',
        'SYSTEM',
        {
          goal_title: 'Employee2の目標'
        }
      )

      // Act: URLパラメータはemployee1だが、ヘッダーでemployee2を指定
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee1.id}`
      )
      request.headers.set('x-user-id', employee2.id)

      const response = await GET(request, { params: { user_id: employee1.id } })
      const responseData = await response.json()

      // Assert: ヘッダーのuser_idが優先され、employee2の目標が返る
      expect(response.status).toBe(200)
      expect(responseData.data.goals[0].title).toBe('Employee2の目標')
    })

    test('年度フィルターで目標を絞り込めること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 2023年の目標
      await prisma.goalProgress.create({
        data: {
          goal_id: `GOAL_2023_${Date.now()}`,
          employee_id: employee.id,
          goal_title: '2023年の目標',
          goal_description: 'Description',
          goal_category: 'skill',
          goal_type: 'individual',
          priority_level: 'high',
          target_value: 100.0,
          current_value: 50.0,
          unit: '%',
          start_date: new Date('2023-01-01'),
          target_date: new Date('2023-12-31'),
          progress_rate: 50.0,
          achievement_status: 'in_progress',
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // 2024年の目標
      await prisma.goalProgress.create({
        data: {
          goal_id: `GOAL_2024_${Date.now()}`,
          employee_id: employee.id,
          goal_title: '2024年の目標',
          goal_description: 'Description',
          goal_category: 'skill',
          goal_type: 'individual',
          priority_level: 'high',
          target_value: 100.0,
          current_value: 30.0,
          unit: '%',
          start_date: new Date('2024-01-01'),
          target_date: new Date('2024-12-31'),
          progress_rate: 30.0,
          achievement_status: 'in_progress',
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // Act: 2023年の目標のみ取得
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}?year=2023`
      )
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert: 2023年の目標のみ返却される
      expect(response.status).toBe(200)
      expect(responseData.data.goals).toHaveLength(1)
      expect(responseData.data.goals[0].title).toBe('2023年の目標')
    })

    test('ステータスフィルターで目標を絞り込めること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // アクティブな目標
      await prisma.goalProgress.create({
        data: {
          goal_id: `GOAL_ACTIVE_${Date.now()}`,
          employee_id: employee.id,
          goal_title: 'アクティブな目標',
          goal_description: 'Description',
          goal_category: 'skill',
          goal_type: 'individual',
          priority_level: 'high',
          target_value: 100.0,
          current_value: 50.0,
          unit: '%',
          start_date: new Date('2024-01-01'),
          target_date: new Date('2024-12-31'),
          progress_rate: 50.0,
          achievement_status: 'in_progress',
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // 完了した目標
      await prisma.goalProgress.create({
        data: {
          goal_id: `GOAL_COMPLETED_${Date.now()}`,
          employee_id: employee.id,
          goal_title: '完了した目標',
          goal_description: 'Description',
          goal_category: 'skill',
          goal_type: 'individual',
          priority_level: 'high',
          target_value: 100.0,
          current_value: 100.0,
          unit: '%',
          start_date: new Date('2024-01-01'),
          target_date: new Date('2024-12-31'),
          progress_rate: 100.0,
          achievement_status: 'completed',
          completion_date: new Date('2024-11-01'),
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // Act: アクティブな目標のみ取得
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}?status=active`
      )
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert: アクティブな目標のみ返却される
      expect(response.status).toBe(200)
      expect(responseData.data.goals).toHaveLength(1)
      expect(responseData.data.goals[0].title).toBe('アクティブな目標')
      expect(responseData.data.goals[0].status).toBe('in_progress')
    })

    test('統計情報が正しく計算されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // 3つの目標を作成（未着手、進行中、完了）
      const statuses = ['not_started', 'in_progress', 'completed']
      for (let i = 0; i < statuses.length; i++) {
        await prisma.goalProgress.create({
          data: {
            goal_id: `GOAL_${statuses[i]}_${Date.now()}_${i}`,
            employee_id: employee.id,
            goal_title: `目標${i + 1}`,
            goal_description: 'Description',
            goal_category: 'skill',
            goal_type: 'individual',
            priority_level: 'high',
            target_value: 100.0,
            current_value: i * 50.0,
            unit: '%',
            start_date: new Date('2024-01-01'),
            target_date: new Date('2024-12-31'),
            progress_rate: i * 50.0,
            achievement_status: statuses[i],
            tenant_id: 'TENANT001',
            created_by: 'SYSTEM',
            updated_by: 'SYSTEM'
          }
        })
      }

      // Act
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}`
      )
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert: 統計情報が正しい
      expect(responseData.data.stats.totalGoals).toBe(3)
      expect(responseData.data.stats.notStartedGoals).toBe(1)
      expect(responseData.data.stats.inProgressGoals).toBe(1)
      expect(responseData.data.stats.completedGoals).toBe(1)
      expect(responseData.data.stats.completionRate).toBeGreaterThan(0)
    })
  })

  describe('異常系テスト', () => {
    test('user_idが未指定の場合、400エラーが返ること', async () => {
      // Act: user_idなしでリクエスト
      const request = createMockGETRequest(
        'http://localhost:3000/api/career-goals/'
      )

      const response = await GET(request, { params: { user_id: '' } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(400)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('INVALID_PARAMETER')
      expect(responseData.error.message).toBe('ユーザーIDが必要です')
    })

    test('無効な年度指定の場合、400エラーが返ること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // Act: 無効な年度（2100年）
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}?year=2100`
      )
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(400)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('INVALID_YEAR')
    })

    test('無効なステータス指定の場合、400エラーが返ること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      // Act: 無効なステータス
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}?status=invalid`
      )
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert
      expect(response.status).toBe(400)
      expect(responseData.success).toBe(false)
      expect(responseData.error.code).toBe('INVALID_STATUS')
    })
  })

  describe('データ形式テスト', () => {
    test('優先度が正しく変換されること（high → 5）', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await prisma.goalProgress.create({
        data: {
          goal_id: `GOAL_HIGH_${Date.now()}`,
          employee_id: employee.id,
          goal_title: '高優先度の目標',
          goal_description: 'Description',
          goal_category: 'skill',
          goal_type: 'individual',
          priority_level: 'high',
          target_value: 100.0,
          current_value: 50.0,
          unit: '%',
          start_date: new Date('2024-01-01'),
          target_date: new Date('2024-12-31'),
          progress_rate: 50.0,
          achievement_status: 'in_progress',
          tenant_id: 'TENANT001',
          created_by: 'SYSTEM',
          updated_by: 'SYSTEM'
        }
      })

      // Act
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}`
      )
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert: priority_level 'high' が priority 5 に変換される
      expect(responseData.data.goals[0].priority).toBe(5)
    })

    test('日付がISO8601形式で返されること', async () => {
      // Arrange
      await createTestTenant(prisma, {
        tenant_code: 'TENANT001'
      })

      const { employee } = await createTestUserComplete(prisma, {
        employee_code: 'EMP001'
      })

      await createTestGoalProgress(
        prisma,
        employee.id,
        'TENANT001',
        'SYSTEM'
      )

      // Act
      const request = createMockGETRequest(
        `http://localhost:3000/api/career-goals/${employee.id}`
      )
      request.headers.set('x-user-id', employee.id)

      const response = await GET(request, { params: { user_id: employee.id } })
      const responseData = await response.json()

      // Assert: ISO8601形式の日付
      expect(responseData.data.goals[0].created_at).toMatch(/^\d{4}-\d{2}-\d{2}T/)
      expect(responseData.data.goals[0].updated_at).toMatch(/^\d{4}-\d{2}-\d{2}T/)
      expect(responseData.data.goals[0].target_date).toMatch(/^\d{4}-\d{2}-\d{2}T/)
    })
  })
})
