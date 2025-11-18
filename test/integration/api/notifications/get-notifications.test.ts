/**
 * 統合テスト: 通知取得API
 * 要求仕様ID: NTF.1-LIST.1
 * 対応設計書: docs/design/api/specs/API定義書_API-091_通知取得API.md
 */

import { PrismaClient } from '@prisma/client';
import { setupTestDatabase, teardownTestDatabase, cleanupTestData } from '@/test/helpers/setup';
import { createMockGETRequest, createAuthenticatedMockRequest } from '@/test/helpers/mock-request';
import { createTestTenant, createTestEmployee } from '@/test/helpers/test-data-factory';

describe('API統合テスト: 通知取得', () => {
  let prisma: PrismaClient;
  let GET: (request: Request, context: { params: { userId: string } }) => Promise<Response>;
  let PUT: (request: Request, context: { params: { userId: string } }) => Promise<Response>;

  beforeAll(async () => {
    prisma = await setupTestDatabase();
    const module = await import('@/app/api/notifications/[userId]/route');
    GET = module.GET;
    PUT = module.PUT;
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  beforeEach(async () => {
    await cleanupTestData(prisma);
  });

  describe('正常系テスト', () => {
    test('基本的な通知一覧を取得できること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma, { tenant_code: 'TEST_TENANT' });
      const employee = await createTestEmployee(prisma, {
        tenant_id: tenant.id,
        employee_code: 'EMP001'
      });

      // 通知を作成
      const notification1 = await prisma.notification.create({
        data: {
          id: 'notif_001',
          notification_id: 'notif_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '新しい通知',
          message: 'テスト通知メッセージ',
          read_status: 'unread',
          priority_level: 'normal',
          is_deleted: false,
          created_at: new Date('2025-01-15T10:00:00Z'),
          created_by: 'system'
        }
      });

      const notification2 = await prisma.notification.create({
        data: {
          id: 'notif_002',
          notification_id: 'notif_002',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'warning',
          title: '警告通知',
          message: '警告メッセージ',
          read_status: 'read',
          priority_level: 'high',
          read_at: new Date('2025-01-16T10:00:00Z'),
          is_deleted: false,
          created_at: new Date('2025-01-14T10:00:00Z'),
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}`,
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
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.notifications).toHaveLength(2);

      // 優先度と作成日時でソートされていること（高優先度→最新）
      expect(responseData.data.notifications[0].id).toBe('notif_002');
      expect(responseData.data.notifications[1].id).toBe('notif_001');

      // サマリー情報の検証
      expect(responseData.data.summary.total).toBe(2);
      expect(responseData.data.summary.unread).toBe(1);
      expect(responseData.data.summary.read).toBe(1);

      // ページネーション情報の検証
      expect(responseData.data.pagination.limit).toBe(20);
      expect(responseData.data.pagination.offset).toBe(0);
      expect(responseData.data.pagination.hasMore).toBe(false);
    });

    test('"me"パラメータで自分の通知を取得できること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 通知を作成
      await prisma.notification.create({
        data: {
          id: 'notif_me_001',
          notification_id: 'notif_me_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: 'My Notification',
          message: 'Test message',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成（userIdに'me'を指定）
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/notifications/me',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      );

      // API実行
      const response = await GET(request, { params: { userId: 'me' } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.notifications).toHaveLength(1);
      expect(responseData.data.notifications[0].title).toBe('My Notification');
    });

    test('ステータスフィルター（unread）で未読通知のみ取得できること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 未読通知
      await prisma.notification.create({
        data: {
          id: 'notif_unread_001',
          notification_id: 'notif_unread_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '未読通知',
          message: 'Unread message',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // 既読通知
      await prisma.notification.create({
        data: {
          id: 'notif_read_001',
          notification_id: 'notif_read_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '既読通知',
          message: 'Read message',
          read_status: 'read',
          read_at: new Date(),
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成（status=unread）
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}?status=unread`,
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
      expect(response.status).toBe(200);
      expect(responseData.data.notifications).toHaveLength(1);
      expect(responseData.data.notifications[0].title).toBe('未読通知');
      expect(responseData.data.notifications[0].is_read).toBe(false);
    });

    test('ステータスフィルター（read）で既読通知のみ取得できること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 未読通知
      await prisma.notification.create({
        data: {
          id: 'notif_unread_002',
          notification_id: 'notif_unread_002',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '未読通知',
          message: 'Unread message',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // 既読通知
      await prisma.notification.create({
        data: {
          id: 'notif_read_002',
          notification_id: 'notif_read_002',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '既読通知',
          message: 'Read message',
          read_status: 'read',
          read_at: new Date(),
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成（status=read）
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}?status=read`,
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
      expect(response.status).toBe(200);
      expect(responseData.data.notifications).toHaveLength(1);
      expect(responseData.data.notifications[0].title).toBe('既読通知');
      expect(responseData.data.notifications[0].is_read).toBe(true);
    });

    test('タイプフィルターで特定タイプの通知のみ取得できること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // info通知
      await prisma.notification.create({
        data: {
          id: 'notif_info_001',
          notification_id: 'notif_info_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: 'Info通知',
          message: 'Info message',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // warning通知
      await prisma.notification.create({
        data: {
          id: 'notif_warning_001',
          notification_id: 'notif_warning_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'warning',
          title: 'Warning通知',
          message: 'Warning message',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成（type=warning）
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}?type=warning`,
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
      expect(response.status).toBe(200);
      expect(responseData.data.notifications).toHaveLength(1);
      expect(responseData.data.notifications[0].type).toBe('warning');
      expect(responseData.data.notifications[0].title).toBe('Warning通知');
    });

    test('ページネーション（limit/offset）が正しく動作すること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 5件の通知を作成
      for (let i = 1; i <= 5; i++) {
        await prisma.notification.create({
          data: {
            id: `notif_page_${i}`,
            notification_id: `notif_page_${i}`,
            tenant_id: tenant.id,
            recipient_id: employee.id,
            notification_type: 'info',
            title: `通知 ${i}`,
            message: `Message ${i}`,
            read_status: 'unread',
            priority_level: 'normal',
            is_deleted: false,
            created_at: new Date(`2025-01-${10 + i}T10:00:00Z`),
            created_by: 'system'
          }
        });
      }

      // リクエスト作成（limit=2, offset=1）
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}?limit=2&offset=1`,
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
      expect(response.status).toBe(200);
      expect(responseData.data.notifications).toHaveLength(2);
      expect(responseData.data.pagination.limit).toBe(2);
      expect(responseData.data.pagination.offset).toBe(1);
      expect(responseData.data.pagination.hasMore).toBe(true);

      // 2番目と3番目の通知が取得されていること（作成日時降順）
      expect(responseData.data.notifications[0].title).toBe('通知 4');
      expect(responseData.data.notifications[1].title).toBe('通知 3');
    });

    test('削除済み通知は取得されないこと', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 有効な通知
      await prisma.notification.create({
        data: {
          id: 'notif_active_001',
          notification_id: 'notif_active_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '有効な通知',
          message: 'Active message',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // 削除済み通知
      await prisma.notification.create({
        data: {
          id: 'notif_deleted_001',
          notification_id: 'notif_deleted_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '削除済み通知',
          message: 'Deleted message',
          read_status: 'unread',
          is_deleted: true,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}`,
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
      expect(response.status).toBe(200);
      expect(responseData.data.notifications).toHaveLength(1);
      expect(responseData.data.notifications[0].title).toBe('有効な通知');
    });

    test('通知のメタデータ（personalization_data）がJSONパースされること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // メタデータ付き通知
      await prisma.notification.create({
        data: {
          id: 'notif_meta_001',
          notification_id: 'notif_meta_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: 'メタデータ付き通知',
          message: 'Message with metadata',
          read_status: 'unread',
          personalization_data: JSON.stringify({ key1: 'value1', key2: 'value2' }),
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}`,
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
      expect(response.status).toBe(200);
      expect(responseData.data.notifications[0].metadata).toEqual({
        key1: 'value1',
        key2: 'value2'
      });
    });
  });

  describe('異常系テスト', () => {
    test('認証エラーの場合、401エラーが返されること', async () => {
      // 認証なしリクエスト作成
      const request = createMockGETRequest('http://localhost:3000/api/notifications/user_001');

      // API実行
      const response = await GET(request, { params: { userId: 'user_001' } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(401);
      expect(responseData.success).toBe(false);
    });

    test('userIdが未指定の場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // リクエスト作成（userIdなし）
      const request = createAuthenticatedMockRequest(
        'http://localhost:3000/api/notifications/',
        employee.id,
        {
          method: 'GET',
          employeeId: employee.id
        }
      );

      // API実行
      const response = await GET(request, { params: { userId: '' } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('INVALID_PARAMETER');
    });

    test('他人の通知を取得しようとした場合、403エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee1 = await createTestEmployee(prisma, {
        tenant_id: tenant.id,
        employee_code: 'EMP001'
      });
      const employee2 = await createTestEmployee(prisma, {
        tenant_id: tenant.id,
        employee_code: 'EMP002'
      });

      // employee2の通知を作成
      await prisma.notification.create({
        data: {
          id: 'notif_emp2_001',
          notification_id: 'notif_emp2_001',
          tenant_id: tenant.id,
          recipient_id: employee2.id,
          notification_type: 'info',
          title: 'Employee2の通知',
          message: 'Message for employee2',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // employee1がemployee2の通知を取得しようとする
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee2.id}`,
        employee1.id,
        {
          method: 'GET',
          employeeId: employee1.id
        }
      );

      // API実行
      const response = await GET(request, { params: { userId: employee2.id } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(403);
      expect(responseData.success).toBe(false);
    });
  });

  describe('通知既読API (PUT) テスト', () => {
    test('通知を既読にできること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 未読通知を作成
      const notification = await prisma.notification.create({
        data: {
          id: 'notif_mark_read_001',
          notification_id: 'notif_mark_read_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '未読通知',
          message: 'To be marked as read',
          read_status: 'unread',
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = new Request(`http://localhost:3000/api/notifications/${employee.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          notificationIds: ['notif_mark_read_001']
        })
      });

      // API実行
      const response = await PUT(request, { params: { userId: employee.id } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.updated).toBe(1);

      // DBで既読になっていることを確認
      const updatedNotification = await prisma.notification.findUnique({
        where: { id: 'notif_mark_read_001' }
      });
      expect(updatedNotification?.read_status).toBe('read');
      expect(updatedNotification?.read_at).not.toBeNull();
    });

    test('複数の通知を一括既読にできること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 3件の未読通知を作成
      await prisma.notification.createMany({
        data: [
          {
            id: 'notif_bulk_001',
            notification_id: 'notif_bulk_001',
            tenant_id: tenant.id,
            recipient_id: employee.id,
            notification_type: 'info',
            title: '通知1',
            message: 'Message 1',
            read_status: 'unread',
            is_deleted: false,
            created_by: 'system'
          },
          {
            id: 'notif_bulk_002',
            notification_id: 'notif_bulk_002',
            tenant_id: tenant.id,
            recipient_id: employee.id,
            notification_type: 'info',
            title: '通知2',
            message: 'Message 2',
            read_status: 'unread',
            is_deleted: false,
            created_by: 'system'
          },
          {
            id: 'notif_bulk_003',
            notification_id: 'notif_bulk_003',
            tenant_id: tenant.id,
            recipient_id: employee.id,
            notification_type: 'info',
            title: '通知3',
            message: 'Message 3',
            read_status: 'unread',
            is_deleted: false,
            created_by: 'system'
          }
        ]
      });

      // リクエスト作成
      const request = new Request(`http://localhost:3000/api/notifications/${employee.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          notificationIds: ['notif_bulk_001', 'notif_bulk_002', 'notif_bulk_003']
        })
      });

      // API実行
      const response = await PUT(request, { params: { userId: employee.id } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.updated).toBe(3);

      // DBで全て既読になっていることを確認
      const readCount = await prisma.notification.count({
        where: {
          notification_id: {
            in: ['notif_bulk_001', 'notif_bulk_002', 'notif_bulk_003']
          },
          read_status: 'read'
        }
      });
      expect(readCount).toBe(3);
    });

    test('既に既読の通知は更新されないこと', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 既読通知を作成
      await prisma.notification.create({
        data: {
          id: 'notif_already_read_001',
          notification_id: 'notif_already_read_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '既読通知',
          message: 'Already read',
          read_status: 'read',
          read_at: new Date('2025-01-10T10:00:00Z'),
          is_deleted: false,
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = new Request(`http://localhost:3000/api/notifications/${employee.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          notificationIds: ['notif_already_read_001']
        })
      });

      // API実行
      const response = await PUT(request, { params: { userId: employee.id } });
      const responseData = await response.json();

      // レスポンス検証（更新件数が0であること）
      expect(response.status).toBe(200);
      expect(responseData.success).toBe(true);
      expect(responseData.data.updated).toBe(0);
    });

    test('notificationIdsが未指定の場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // リクエスト作成（notificationIdsなし）
      const request = new Request(`http://localhost:3000/api/notifications/${employee.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({})
      });

      // API実行
      const response = await PUT(request, { params: { userId: employee.id } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('INVALID_PARAMETER');
    });

    test('notificationIdsが配列でない場合、400エラーが返されること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // リクエスト作成（notificationIdsが文字列）
      const request = new Request(`http://localhost:3000/api/notifications/${employee.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'x-user-id': employee.id,
          'x-employee-id': employee.id
        },
        body: JSON.stringify({
          notificationIds: 'notif_001'
        })
      });

      // API実行
      const response = await PUT(request, { params: { userId: employee.id } });
      const responseData = await response.json();

      // レスポンス検証
      expect(response.status).toBe(400);
      expect(responseData.success).toBe(false);
      expect(responseData.error.code).toBe('INVALID_PARAMETER');
    });
  });

  describe('データ形式テスト', () => {
    test('レスポンスの日付がISO8601形式であること', async () => {
      // テストデータ作成
      const tenant = await createTestTenant(prisma);
      const employee = await createTestEmployee(prisma, { tenant_id: tenant.id });

      // 通知を作成
      await prisma.notification.create({
        data: {
          id: 'notif_date_001',
          notification_id: 'notif_date_001',
          tenant_id: tenant.id,
          recipient_id: employee.id,
          notification_type: 'info',
          title: '日付確認通知',
          message: 'Date format test',
          read_status: 'read',
          read_at: new Date('2025-01-15T14:30:00Z'),
          expiry_date: new Date('2025-02-15T14:30:00Z'),
          is_deleted: false,
          created_at: new Date('2025-01-10T10:00:00Z'),
          created_by: 'system'
        }
      });

      // リクエスト作成
      const request = createAuthenticatedMockRequest(
        `http://localhost:3000/api/notifications/${employee.id}`,
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
      expect(response.status).toBe(200);
      const notification = responseData.data.notifications[0];

      // ISO8601形式であることを確認
      expect(notification.created_at).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
      expect(notification.read_at).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
      expect(notification.expires_at).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$/);
    });
  });
});
