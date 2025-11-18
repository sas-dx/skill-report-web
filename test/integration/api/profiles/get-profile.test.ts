/**
 * 統合テスト: プロフィールAPI
 * 要求仕様ID: PRO.1-BASE.1
 * 対応設計書: docs/design/api/specs/API定義書_API-011_プロフィール取得API.md
 */

import { PrismaClient } from '@prisma/client';
import {
  setupTestDatabase,
  teardownTestDatabase,
  cleanupTestData,
  setupBasicTestContext,
  createTestDepartment,
  assertSuccessResponse,
  assertErrorResponse,
  assertAuthenticationError,
  assertAuthorizationError,
  assertNotFoundError,
  assertDateFieldsISO8601,
  assertRequiredFields
} from '@/test/helpers';
import { createAuthenticatedMockRequest } from '@/test/helpers/mock-request';

describe('API統合テスト: プロフィール取得', () => {
  let prisma: PrismaClient;
  let GET: (request: Request, context: { params: { userId: string } }) => Promise<Response>;
  let PUT: (request: Request, context: { params: { userId: string } }) => Promise<Response>;

  beforeAll(async () => {
    prisma = await setupTestDatabase();
    const module = await import('@/app/api/profiles/[userId]/route');
    GET = module.GET;
    PUT = module.PUT;
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  beforeEach(async () => {
    await cleanupTestData(prisma);
  });

  describe('GET /api/profiles/[userId] - プロフィール取得', () => {
    describe('正常系テスト', () => {
      test('基本的なプロフィールを取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/profiles/${employee.employee_code}`,
          employee.employee_code,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.profile).toBeDefined();
        expect(responseData.data.profile.id).toBe(employee.employee_code);
        expect(responseData.data.profile.email).toBe(employee.email);

        // personalInfo検証
        assertRequiredFields(responseData.data.profile.personalInfo, [
          'displayName',
          'phoneNumber'
        ]);

        // organizationInfo検証
        assertRequiredFields(responseData.data.profile.organizationInfo, [
          'departmentId',
          'departmentName',
          'positionId',
          'employmentType'
        ]);

        // systemInfo検証
        assertRequiredFields(responseData.data.profile.systemInfo, [
          'status',
          'role',
          'permissions'
        ]);
        assertDateFieldsISO8601(responseData.data.profile.systemInfo, ['createdAt', 'updatedAt']);
      });

      test('"me"パラメータで自分のプロフィールを取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（userIdに'me'を指定）
        const request = createAuthenticatedMockRequest(
          'http://localhost:3000/api/profiles/me',
          employee.employee_code,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: 'me' } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.profile.id).toBe(employee.employee_code);
      });

      test('includeSkillSummaryオプションでスキルサマリーを取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（includeSkillSummary=true）
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/profiles/${employee.employee_code}?includeSkillSummary=true`,
          employee.employee_code,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.skillSummary).toBeDefined();
        expect(responseData.data.skillSummary.totalSkills).toBeDefined();
        expect(responseData.data.skillSummary.skillsByLevel).toBeDefined();
      });

      test('includeGoalSummaryオプションで目標サマリーを取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（includeGoalSummary=true）
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/profiles/${employee.employee_code}?includeGoalSummary=true`,
          employee.employee_code,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.goalSummary).toBeDefined();
        expect(responseData.data.goalSummary.currentGoals).toBeDefined();
        expect(responseData.data.goalSummary.overallProgress).toBeDefined();
      });

      test('includeHistoryオプションで更新履歴を取得できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（includeHistory=true）
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/profiles/${employee.employee_code}?includeHistory=true`,
          employee.employee_code,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.updateHistory).toBeDefined();
        expect(Array.isArray(responseData.data.updateHistory)).toBe(true);
      });
    });

    describe('異常系テスト', () => {
      test('認証エラーの場合、401エラーが返されること', async () => {
        // 認証なしリクエスト作成
        const request = new Request('http://localhost:3000/api/profiles/EMP001', {
          method: 'GET'
        });

        // API実行
        const response = await GET(request, { params: { userId: 'EMP001' } });
        const responseData = await response.json();

        // レスポンス検証
        assertAuthenticationError(response, responseData);
      });

      test('userIdが未指定の場合、400エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（userIdなし）
        const request = createAuthenticatedMockRequest(
          'http://localhost:3000/api/profiles/',
          employee.employee_code,
          {
            method: 'GET',
            employeeId: employee.id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: '' } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'INVALID_PARAMETER', 400);
      });

      test('他人のプロフィールを取得しようとした場合、403エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employees } = await (async () => {
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

          return { tenant, employees: [emp1, emp2] };
        })();

        // employee1がemployee2のプロフィールを取得しようとする
        const request = createAuthenticatedMockRequest(
          `http://localhost:3000/api/profiles/${employees[1].employee_code}`,
          employees[0].employee_code,
          {
            method: 'GET',
            employeeId: employees[0].id
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: employees[1].employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertAuthorizationError(response, responseData);
      });

      test('存在しないユーザーIDの場合、404エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（存在しないuserID）
        const request = createAuthenticatedMockRequest(
          'http://localhost:3000/api/profiles/INVALID_USER',
          'INVALID_USER',
          {
            method: 'GET',
            employeeId: 'invalid_id'
          }
        );

        // API実行
        const response = await GET(request, { params: { userId: 'INVALID_USER' } });
        const responseData = await response.json();

        // レスポンス検証
        assertNotFoundError(response, responseData);
      });
    });
  });

  describe('PUT /api/profiles/[userId] - プロフィール更新', () => {
    describe('正常系テスト', () => {
      test('プロフィールを更新できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成
        const request = new Request(`http://localhost:3000/api/profiles/${employee.employee_code}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            first_name: '太郎',
            last_name: 'テスト更新',
            first_name_kana: 'タロウ',
            last_name_kana: 'テストコウシン',
            email: 'updated@example.com'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.last_name).toBe('テスト更新');
        expect(responseData.data.first_name).toBe('太郎');
        expect(responseData.data.email).toBe('updated@example.com');
        assertDateFieldsISO8601(responseData.data, ['updated_at']);
      });

      test('"me"パラメータで自分のプロフィールを更新できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成
        const request = new Request('http://localhost:3000/api/profiles/me', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            first_name: '花子',
            last_name: 'テスト'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: 'me' } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.first_name).toBe('花子');
      });

      test('部署と役職を更新できること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        const department = await createTestDepartment(prisma, {
          department_code: 'DEPT002',
          department_name: '新部署'
        });

        // リクエスト作成
        const request = new Request(`http://localhost:3000/api/profiles/${employee.employee_code}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            organization_info: {
              department_id: department.department_code,
              position_id: 'POS002'
            }
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertSuccessResponse(response, responseData);
        expect(responseData.data.department.department_id).toBe(department.department_code);
      });
    });

    describe('異常系テスト', () => {
      test('認証エラーの場合、401エラーが返されること', async () => {
        // 認証なしリクエスト作成
        const request = new Request('http://localhost:3000/api/profiles/EMP001', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            first_name: '太郎'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: 'EMP001' } });
        const responseData = await response.json();

        // レスポンス検証
        assertAuthenticationError(response, responseData);
      });

      test('不正なメールアドレスの場合、400エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（不正なメール）
        const request = new Request(`http://localhost:3000/api/profiles/${employee.employee_code}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            email: 'invalid-email'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'INVALID_PARAMETER', 400);
      });

      test('カタカナ以外の文字が含まれる場合、400エラーが返されること', async () => {
        // テストデータ作成
        const { tenant, employee } = await setupBasicTestContext(prisma);

        // リクエスト作成（不正なカナ）
        const request = new Request(`http://localhost:3000/api/profiles/${employee.employee_code}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': employee.employee_code,
            'x-employee-id': employee.id
          },
          body: JSON.stringify({
            first_name_kana: 'たろう'  // ひらがな
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: employee.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'INVALID_PARAMETER', 400);
      });

      test('他人のプロフィールを更新しようとした場合、403エラーが返されること', async () => {
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

        // employee1がemployee2のプロフィールを更新しようとする
        const request = new Request(`http://localhost:3000/api/profiles/${emp2.employee_code}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': emp1.employee_code,
            'x-employee-id': emp1.id
          },
          body: JSON.stringify({
            first_name: '更新'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: emp2.employee_code } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'PERMISSION_DENIED', 403);
      });

      test('存在しないユーザーIDの場合、404エラーが返されること', async () => {
        // リクエスト作成
        const request = new Request('http://localhost:3000/api/profiles/INVALID_USER', {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'x-user-id': 'INVALID_USER',
            'x-employee-id': 'invalid_id'
          },
          body: JSON.stringify({
            first_name: '太郎'
          })
        });

        // API実行
        const response = await PUT(request, { params: { userId: 'INVALID_USER' } });
        const responseData = await response.json();

        // レスポンス検証
        assertErrorResponse(response, responseData, 'USER_NOT_FOUND', 404);
      });
    });
  });
});
