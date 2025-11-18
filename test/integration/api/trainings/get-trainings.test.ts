/**
 * 統合テスト: 研修API
 * 要求仕様ID: TRN.1-ATT.1
 * 対応設計書: docs/design/api/specs/API定義書_API-051_研修記録取得API.md
 */

import { PrismaClient } from '@prisma/client';
import {
  setupTestDatabase,
  teardownTestDatabase,
  cleanupTestData,
  setupBasicTestContext,
  createTestTrainingHistory,
  assertSuccessResponse,
  assertCreatedResponse,
  assertErrorResponse,
  assertNotFoundError,
  assertPaginationStructure,
  assertDateFieldsISO8601,
  assertDescendingOrder
} from '@/test/helpers';
import { createAuthenticatedMockRequest } from '@/test/helpers/mock-request';

describe('API統合テスト: 研修記録', () => {
  let prisma: PrismaClient;
  let GET: (request: Request, context: { params: { userId: string } }) => Promise<Response>;
  let POST: (request: Request, context: { params: { userId: string } }) => Promise<Response>;
  let PUT: (request: Request, context: { params: { userId: string } }) => Promise<Response>;

  beforeAll(async () => {
    prisma = await setupTestDatabase();
    const module = await import('@/app/api/trainings/[userId]/route');
    GET = module.GET;
    POST = module.POST;
    PUT = module.PUT;
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  beforeEach(async () => {
    await cleanupTestData(prisma);
  });

  describe('GET /api/trainings/[userId] - 研修記録取得', () => {
    describe('正常系テスト', () => {
      test('基本的な研修記録一覧を取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // 研修記録を作成
        await createTestTrainingHistory(prisma, employee.id, tenant.id, 'system', {
          training_name: 'React基礎講座'
        });

        await createTestTrainingHistory(prisma, employee.id, tenant.id, 'system', {
          training_name: 'TypeScript応用'
        });

        // リクエスト作成
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/trainings/${employee.id}`,
          employee.id,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.trainings).toHaveLength(2);

        // ページネーション検証
        assertPaginationStructure(responseData.data.pagination);
        expect(responseData.data.pagination.total).toBe(2);

        // 日付降順でソートされていることを確認
        assertDescendingOrder(responseData.data.trainings, (t) => new Date(t.start_date).getTime());
      });

      test('研修記録が0件の場合、空配列が返されること', async () => {
        // テストデータ作成（研修記録なし）
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/trainings/${employee.id}`,
          employee.id,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.trainings).toHaveLength(0);
        expect(responseData.data.pagination.total).toBe(0);
      });

      test('年フィルターで特定年の研修記録のみ取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // 2023年の研修
        await prisma.trainingHistory.create({
          data: {
            training_history_id: 'TRN_2023_001',
            employee_id: employee.id,
            training_program_id: 'TPROG001',
            training_name: '2023年研修',
            training_type: 'technical',
            training_category: 'programming',
            provider_name: 'テスト研修機関',
            start_date: new Date('2023-06-01'),
            end_date: new Date('2023-06-05'),
            duration_hours: 40.0,
            location: 'オンライン',
            attendance_status: 'completed',
            tenant_id: tenant.id,
            created_by: 'system',
            updated_by: 'system'
          }
        });

        // 2024年の研修
        await prisma.trainingHistory.create({
          data: {
            training_history_id: 'TRN_2024_001',
            employee_id: employee.id,
            training_program_id: 'TPROG001',
            training_name: '2024年研修',
            training_type: 'technical',
            training_category: 'programming',
            provider_name: 'テスト研修機関',
            start_date: new Date('2024-06-01'),
            end_date: new Date('2024-06-05'),
            duration_hours: 40.0,
            location: 'オンライン',
            attendance_status: 'completed',
            tenant_id: tenant.id,
            created_by: 'system',
            updated_by: 'system'
          }
        });

        // リクエスト作成（year=2024）
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/trainings/${employee.id}?year=2024`,
          employee.id,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.trainings).toHaveLength(1);
        expect(responseData.data.trainings[0].training_name).toBe('2024年研修');
      });

      test('カテゴリフィルターで特定カテゴリの研修のみ取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // programming カテゴリ
        await prisma.trainingHistory.create({
          data: {
            training_history_id: 'TRN_PROG_001',
            employee_id: employee.id,
            training_program_id: 'TPROG001',
            training_name: 'プログラミング研修',
            training_type: 'technical',
            training_category: 'programming',
            provider_name: 'テスト研修機関',
            start_date: new Date('2024-06-01'),
            end_date: new Date('2024-06-05'),
            duration_hours: 40.0,
            location: 'オンライン',
            attendance_status: 'completed',
            tenant_id: tenant.id,
            created_by: 'system',
            updated_by: 'system'
          }
        });

        // management カテゴリ
        await prisma.trainingHistory.create({
          data: {
            training_history_id: 'TRN_MGMT_001',
            employee_id: employee.id,
            training_program_id: 'TPROG002',
            training_name: 'マネジメント研修',
            training_type: 'business',
            training_category: 'management',
            provider_name: 'テスト研修機関',
            start_date: new Date('2024-07-01'),
            end_date: new Date('2024-07-05'),
            duration_hours: 40.0,
            location: 'オンライン',
            attendance_status: 'completed',
            tenant_id: tenant.id,
            created_by: 'system',
            updated_by: 'system'
          }
        });

        // リクエスト作成（category=programming）
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/trainings/${employee.id}?category=programming`,
          employee.id,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.trainings).toHaveLength(1);
        expect(responseData.data.trainings[0].training_category).toBe('programming');
      });

      test('ステータスフィルターで特定ステータスの研修のみ取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // completed ステータス
        await createTestTrainingHistory(prisma, employee.id, tenant.id, 'system', {
          training_name: '完了研修'
        });

        // planned ステータス
        await prisma.trainingHistory.create({
          data: {
            training_history_id: 'TRN_PLANNED_001',
            employee_id: employee.id,
            training_program_id: 'TPROG001',
            training_name: '予定研修',
            training_type: 'technical',
            training_category: 'programming',
            provider_name: 'テスト研修機関',
            start_date: new Date('2025-06-01'),
            end_date: new Date('2025-06-05'),
            duration_hours: 40.0,
            location: 'オンライン',
            attendance_status: 'planned',
            tenant_id: tenant.id,
            created_by: 'system',
            updated_by: 'system'
          }
        });

        // リクエスト作成（status=planned）
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/trainings/${employee.id}?status=planned`,
          employee.id,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.trainings).toHaveLength(1);
        expect(responseData.data.trainings[0].attendance_status).toBe('planned');
      });

      test('ページネーション（limit/offset）が正しく動作すること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // 5件の研修を作成
        for (let i = 1; i <= 5; i++) {
          await prisma.trainingHistory.create({
            data: {
              training_history_id: `TRN_PAGE_${i}`,
              employee_id: employee.id,
              training_program_id: 'TPROG001',
              training_name: `研修 ${i}`,
              training_type: 'technical',
              training_category: 'programming',
              provider_name: 'テスト研修機関',
              start_date: new Date(`2024-0${i}-01`),
              end_date: new Date(`2024-0${i}-05`),
              duration_hours: 40.0,
              location: 'オンライン',
              attendance_status: 'completed',
              tenant_id: tenant.id,
              created_by: 'system',
              updated_by: 'system'
            }
          });
        }

        // リクエスト作成（limit=2, offset=1）
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/trainings/${employee.id}?limit=2&offset=1`,
          employee.id,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.trainings).toHaveLength(2);
        assertPaginationStructure(responseData.data.pagination, 2, 1);
        expect(responseData.data.pagination.has_more).toBe(true);
      });
    });

    describe('異常系テスト', () => {
      test('存在しないユーザーIDの場合、404エラーが返されること', async () => {
        // リクエスト作成
        const request = createAuthenticatedMockRequest(
          'http://localhost:3000/api/trainings/invalid_user_id',
          'invalid_user_id',
          {
            method: 'GET',
            employeeId: 'invalid_user_id'
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: 'invalid_user_id' } });
        const responseData = await response.json();

        // レスポンス検証
        assertNotFoundError(response, responseData);
      });
    });
  });

  describe('POST /api/trainings/[userId] - 研修記録登録', () => {
    describe('正常系テスト', () => {
      test('新しい研修記録を登録できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成
        const request = new Request(`http://localhost:3000/api/trainings/${employee.employee_code}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            name: 'AWS認定試験対策講座',
            category: 'cloud',
            start_date: '2024-06-01',
            end_date: '2024-06-05',
            duration_hours: 40,
            provider: 'AWS Training',
            location: 'オンライン',
            status: 'completed'
          })
        });

        // API実行
        const response = await POST(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertCreatedResponse(response, responseData);
        expect(responseData.data.name).toBe('AWS認定試験対策講座');
        expect(responseData.data.category).toBe('cloud');
        expect(responseData.data.status).toBe('completed');
        assertDateFieldsISO8601(responseData.data, ['created_at']);
      });
    });

    describe('異常系テスト', () => {
      test('必須フィールドが未指定の場合、400エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（nameなし）
        const request = new Request(`http://localhost:3000/api/trainings/${employee.employee_code}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            category: 'programming',
            start_date: '2024-06-01',
            end_date: '2024-06-05'
          })
        });

        // API実行
        const response = await POST(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'INVALID_PARAMETER', 400);
      });

      test('開始日が終了日より後の場合、400エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（start_date > end_date）
        const request = new Request(`http://localhost:3000/api/trainings/${employee.employee_code}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            name: 'テスト研修',
            category: 'programming',
            start_date: '2024-06-10',
            end_date: '2024-06-01',
            duration_hours: 40
          })
        });

        // API実行
        const response = await POST(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'INVALID_PARAMETER', 400);
      });

      test('存在しないユーザーIDの場合、404エラーが返されること', async () => {
        // リクエスト作成
        const request = new Request('http://localhost:3000/api/trainings/INVALID_USER', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': 'INVALID_USER',
            'x-employee-id': 'invalid_id'
          },
          body: JSON.stringify({
            name: 'テスト研修',
            category: 'programming',
            start_date: '2024-06-01',
            end_date: '2024-06-05',
            duration_hours: 40
          })
        });

        // API実行
        const response = await POST(request, { params: { userId: 'INVALID_USER' } });
        const responseData = await response.json();

        // レスポンス検証
        assertNotFoundError(response, responseData);
      });
    });
  });

  describe('PUT /api/trainings/[userId] - 研修記録更新', () => {
    describe('正常系テスト', () => {
      test('研修記録を更新できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // 研修記録を作成
        const training = await createTestTrainingHistory(prisma, employee.id, tenant.id, 'system', {
          training_name: '初期研修名'
        });

        // リクエスト作成
        const request = new Request(`http://localhost:3000/api/trainings/${employee.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.id,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            training_id: training.id,
            name: '更新後研修名',
            status: 'completed',
            completion_rate: 100,
            score: 85
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.name).toBe('更新後研修名');
        expect(responseData.data.status).toBe('completed');
        expect(responseData.data.score).toBe(85);
        assertDateFieldsISO8601(responseData.data, ['updated_at']);
      });
    });

    describe('異常系テスト', () => {
      test('training_idが未指定の場合、400エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（training_idなし）
        const request = new Request(`http://localhost:3000/api/trainings/${employee.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.id,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            name: '更新後研修名'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'INVALID_PARAMETER', 400);
      });

      test('存在しない研修IDの場合、404エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（存在しないtraining_id）
        const request = new Request(`http://localhost:3000/api/trainings/${employee.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.id,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            training_id: 'invalid_training_id',
            name: '更新後研修名'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: employee.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'TRAINING_NOT_FOUND', 404);
      });

      test('他人の研修記録を更新しようとした場合、403エラーが返されること', async () => {
        // テストデータ作成
        const tenant = await prisma.tenant.create({
          data: {
            tenant_code: 'TEST_TENANT',
            tenant_name: 'テストテナント',
            tenant_name_en: 'Test Tenant',
            domain_name: 'test.example.com',
            status: 'active'
          }
        });

        const emp1 = await prisma.employee.create({
          data: {
            employee_code: 'EMP001',
            full_name: 'テスト太郎',
            full_name_kana: 'テストタロウ',
            email: 'test1@example.com',
            phone: '090-1234-5678',
            hire_date: new Date('2020-04-01'),
            birth_date: new Date('1990-01-01'),
            gender: 'male',
            department_id: 'DEPT001',
            position_id: 'POS001',
            job_type_id: 'JOB001',
            employment_status: 'regular',
            employee_status: 'active'
          }
        });

        const emp2 = await prisma.employee.create({
          data: {
            employee_code: 'EMP002',
            full_name: 'テスト次郎',
            full_name_kana: 'テストジロウ',
            email: 'test2@example.com',
            phone: '090-1234-5679',
            hire_date: new Date('2020-04-01'),
            birth_date: new Date('1991-01-01'),
            gender: 'male',
            department_id: 'DEPT001',
            position_id: 'POS001',
            job_type_id: 'JOB001',
            employment_status: 'regular',
            employee_status: 'active'
          }
        });

        // emp2の研修を作成
        const training = await createTestTrainingHistory(prisma, emp2.id, tenant.id, 'system');

        // emp1がemp2の研修を更新しようとする
        const request = new Request(`http://localhost:3000/api/trainings/${emp1.id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': emp1.id,
            'x-employee-id': emp1.id
          },
          body: JSON.stringify({
            training_id: training.id,
            name: '不正更新'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: emp1.id } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'FORBIDDEN', 403);
      });
    });
  });
});
