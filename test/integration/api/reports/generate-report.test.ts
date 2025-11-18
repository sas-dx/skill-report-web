/**
 * 統合テスト: レポート生成API
 * 要求仕様ID: RPT.1-GEN.1
 * 対応設計書: docs/design/api/specs/API定義書_API-061_レポート生成API.md
 */

import { PrismaClient } from '@prisma/client';
import { setupTestDatabase, teardownTestDatabase, cleanupTestData } from '@/test/helpers/setup';
import { createAuthenticatedMockRequest } from '@/test/helpers/mock-request';
import { createTestTenant, createTestEmployee } from '@/test/helpers/test-data-factory';

describe('API統合テスト: レポート生成', () => {
  let prisma: PrismaClient;
  let POST: (request: Request) => Promise<Response>;

  beforeAll(async () => {
    prisma = await setupTestDatabase();
    const module = await import('@/app/api/reports/generate/route');
    POST = module.POST;
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  beforeEach(async () => {
    await cleanupTestData(prisma);
  });

  describe('正常系テスト', () => {
    test('基本的なレポート生成リクエストができること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma, { id: 'tenant_001' });
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // レポートテンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_001',
          tenant_id: tenant.id,
          template_code: 'SKILL_REPORT',
          template_name: 'スキルレポート',
          description: 'スキル集計レポート',
          report_category: 'SKILL',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'テストレポート',
          parameters: {
            startDate: '2025-01-01',
            endDate: '2025-01-31'
          }
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(201);
      expect(responseData.success).toBe(true);
      expect(responseData.data.reportId).toBeDefined();
      expect(responseData.data.templateId).toBe(template.id);
      expect(responseData.data.reportTitle).toBe('テストレポート');
      expect(responseData.data.category).toBe('SKILL');
      expect(responseData.data.format).toBe('PDF');
      expect(responseData.data.status).toBe('PENDING');

      // ISO8601形式の日付確認
      expect(responseData.data.requestedAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
      expect(responseData.data.expiresAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);

      // DBにレコードが作成されていることを確認
      const reportGeneration = await prisma.reportGeneration.findFirst({
        where: { id: responseData.data.reportId }
      });
      expect(reportGeneration).not.toBeNull();
      expect(reportGeneration?.generation_status).toBe('PENDING');
      expect(reportGeneration?.requested_by).toBe(employee.id);
    });

    test('パラメータなしでレポート生成リクエストができること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma, { id: 'tenant_002' });
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // レポートテンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_002',
          tenant_id: tenant.id,
          template_code: 'SUMMARY_REPORT',
          template_name: 'サマリーレポート',
          description: '全体サマリー',
          report_category: 'SUMMARY',
          output_format: 'EXCEL',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成（パラメータなし）
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'サマリーレポート2025'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(201);
      expect(responseData.success).toBe(true);
      expect(responseData.data.format).toBe('EXCEL');
    });

    test('有効期限が30日後に設定されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // レポートテンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_expiry_001',
          tenant_id: tenant.id,
          template_code: 'TEST_REPORT',
          template_name: 'テストレポート',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: '有効期限テスト'
        })
      });

      // API実行
      const requestedAt = new Date();
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(201);

      // DBから取得して有効期限を確認
      const reportGeneration = await prisma.reportGeneration.findFirst({
        where: { id: responseData.data.reportId }
      });

      // 30日後（±1日の誤差許容）
      const expectedExpiryDate = new Date(requestedAt);
      expectedExpiryDate.setDate(expectedExpiryDate.getDate() + 30);

      const actualExpiryDate = reportGeneration?.expires_at;
      expect(actualExpiryDate).not.toBeNull();

      if (actualExpiryDate) {
        const diffInDays = Math.abs(
          (actualExpiryDate.getTime() - expectedExpiryDate.getTime()) / (1000 * 60 * 60 * 24)
        );
        expect(diffInDays).toBeLessThan(1); // 1日以内の誤差
      }
    });

    test('レポートIDが一意に生成されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // レポートテンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_unique_001',
          tenant_id: tenant.id,
          template_code: 'UNIQUE_TEST',
          template_name: 'ユニークテスト',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // 2つのリクエストを作成
      const request1 = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'レポート1'
        })
      });

      const request2 = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'レポート2'
        })
      });

      // API実行
      const response1 = await POST(request1);
      const responseData1 = await response1.json();

      // 少し待機
      await new Promise(resolve => setTimeout(resolve, 10));

      const response2 = await POST(request2);
      const responseData2 = await response2.json();

      // レスポンス検証（IDが異なること）
      expect(response1.status).toBe(201);
      expect(response2.status).toBe(201);
      expect(responseData1.data.reportId).not.toBe(responseData2.data.reportId);
    });

    test('初期状態がPENDINGであること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // レポートテンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_status_001',
          tenant_id: tenant.id,
          template_code: 'STATUS_TEST',
          template_name: 'ステータステスト',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'ステータス確認'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(201);
      expect(responseData.data.status).toBe('PENDING');

      // DBでも確認
      const reportGeneration = await prisma.reportGeneration.findFirst({
        where: { id: responseData.data.reportId }
      });
      expect(reportGeneration?.generation_status).toBe('PENDING');
      expect(reportGeneration?.started_at).toBeNull();
      expect(reportGeneration?.completed_at).toBeNull();
    });
  });

  describe('異常系テスト', () => {
    test('認証エラーの場合、401エラーが返されること', async () => {
      // 認証なしリクエスト作成
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          templateId: 'template_001',
          reportTitle: 'テストレポート'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(401);
      expect(responseData.success).toBe(false);
    });

    test('templateIdが未指定の場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // リクエスト作成（templateIdなし）
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          reportTitle: 'テストレポート'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
      expect(responseData.error.details).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            field: 'templateId',
            message: 'テンプレートIDは必須です'
          })
        ])
      );
    });

    test('reportTitleが未指定の場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // リクエスト作成（reportTitleなし）
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: 'template_001'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.details).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            field: 'reportTitle',
            message: 'レポートタイトルは必須です'
          })
        ])
      );
    });

    test('無効なテンプレートIDの場合、404エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // リクエスト作成（存在しないテンプレートID）
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: 'invalid_template_id',
          reportTitle: 'テストレポート'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(404);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('NOT_FOUND');
    });

    test('非アクティブなテンプレートの場合、404エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 非アクティブなテンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_inactive_001',
          tenant_id: tenant.id,
          template_code: 'INACTIVE_TEST',
          template_name: '非アクティブテンプレート',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: false,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'テストレポート'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(404);
      expect(responseData.success).toBe(false);
    });

    test('無効な日付形式の場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // テンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_date_001',
          tenant_id: tenant.id,
          template_code: 'DATE_TEST',
          template_name: '日付テスト',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成（無効な日付）
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'テストレポート',
          parameters: {
            startDate: 'invalid-date',
            endDate: '2025-01-31'
          }
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.details).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            field: 'parameters.startDate'
          })
        ])
      );
    });

    test('開始日が終了日より後の場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // テンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_date_range_001',
          tenant_id: tenant.id,
          template_code: 'DATE_RANGE_TEST',
          template_name: '日付範囲テスト',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成（開始日 > 終了日）
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'テストレポート',
          parameters: {
            startDate: '2025-02-01',
            endDate: '2025-01-01'
          }
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.details).toEqual(
        expect.arrayContaining([
          expect.objectContaining({
            field: 'parameters',
            message: '開始日は終了日より前である必要があります'
          })
        ])
      );
    });

    test('不正なJSONの場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // リクエスト作成（不正なJSON）
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: 'invalid json'
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('VALIDATION_ERROR');
    });
  });

  describe('データ形式テスト', () => {
    test('パラメータがJSON文字列として保存されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // テンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_params_001',
          tenant_id: tenant.id,
          template_code: 'PARAMS_TEST',
          template_name: 'パラメータテスト',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      const testParams = {
        startDate: '2025-01-01',
        endDate: '2025-01-31',
        department: 'IT',
        includeInactive: false
      };

      // リクエスト作成
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'パラメータ確認',
          parameters: testParams
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(201);

      // DBから取得してパラメータを確認
      const reportGeneration = await prisma.reportGeneration.findFirst({
        where: { id: responseData.data.reportId }
      });

      expect(reportGeneration?.parameters).not.toBeNull();
      const savedParams = JSON.parse(reportGeneration?.parameters || '{}');
      expect(savedParams).toEqual(testParams);
    });

    test('レスポンスの日付がISO8601形式であること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // テンプレートを作成
      const template = await prisma.reportTemplate.create({
        data: {
          id: 'template_iso_001',
          tenant_id: tenant.id,
          template_code: 'ISO_TEST',
          template_name: 'ISO形式テスト',
          report_category: 'TEST',
          output_format: 'PDF',
          is_active: true,
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = new Request('http://localhost:3000/api/reports/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          templateId: template.id,
          reportTitle: 'ISO形式確認'
        })
      });

      // API実行
      const response = await POST(request);
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(201);
      expect(responseData.data.requestedAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
      expect(responseData.data.expiresAt).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}/);
    });
  });
});
