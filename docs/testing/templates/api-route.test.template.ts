/**
 * 要求仕様ID: [仕様ID]
 * API-XXX: [API名] テストファイル
 * 実装日: YYYY-MM-DD
 * 実装者: [実装者名]
 */

import { NextRequest } from 'next/server';
import { prismaMock } from '@/__mocks__/prisma';
import { createAuthenticatedRequest } from '@/__tests__/helpers/nextRequest.helper';
import {
  expectCompleteSuccessResponse,
  expectCreatedResponse,
  expectValidationErrorResponse,
  expectUnauthorizedResponse,
  getResponseData,
} from '@/__tests__/helpers/apiResponse.helper';
import {
  // 必要なファクトリをインポート
  createMockUser,
  createMockCareerPlan,
} from '@/__tests__/helpers/prismaFactories';

// 動的インポート関数
async function importGETFunction() {
  const module = await import('./route');
  return module.GET;
}

async function importPOSTFunction() {
  const module = await import('./route');
  return module.POST;
}

async function importPUTFunction() {
  const module = await import('./route');
  return module.PUT;
}

async function importDELETEFunction() {
  const module = await import('./route');
  return module.DELETE;
}

describe('API-XXX: [API名]', () => {
  // ======================
  // GET テスト
  // ======================
  describe('GET /api/[endpoint]', () => {
    beforeEach(() => {
      // モックデータのセットアップ
      prismaMock.model.findMany.mockResolvedValue([
        createMockUser() as any,
      ]);
    });

    describe('正常系', () => {
      test('データを正常に取得できること', async () => {
        // Arrange
        const GET = await importGETFunction();
        const request = createAuthenticatedRequest('emp_001');

        // Act
        const response = await GET(request);

        // Assert
        const data = await expectCompleteSuccessResponse(response, ['items']);
        expect(data.data.items).toHaveLength(1);
      });

      test('ユーザーIDに基づいてフィルタリングされること', async () => {
        // Arrange
        const GET = await importGETFunction();
        const request = createAuthenticatedRequest('emp_001');

        // Act
        const response = await GET(request);

        // Assert
        await expectCompleteSuccessResponse(response, ['items']);
        expect(prismaMock.model.findMany).toHaveBeenCalledWith({
          where: { employee_id: 'emp_001' },
        });
      });
    });

    describe('異常系', () => {
      test('認証エラーの場合、401を返すこと', async () => {
        // Arrange
        const GET = await importGETFunction();
        const request = createAuthenticatedRequest('');

        // Act
        const response = await GET(request);

        // Assert
        const { status, data } = await getResponseData(response);
        expectUnauthorizedResponse(response, data);
      });

      test('データベースエラーの場合、500を返すこと', async () => {
        // Arrange
        prismaMock.model.findMany.mockRejectedValue(
          new Error('Database error')
        );
        const GET = await importGETFunction();
        const request = createAuthenticatedRequest('emp_001');

        // Act
        const response = await GET(request);

        // Assert
        expect(response.status).toBe(500);
      });
    });

    describe('エッジケース', () => {
      test('データが0件の場合、空配列を返すこと', async () => {
        // Arrange
        prismaMock.model.findMany.mockResolvedValue([]);
        const GET = await importGETFunction();
        const request = createAuthenticatedRequest('emp_001');

        // Act
        const response = await GET(request);

        // Assert
        const data = await expectCompleteSuccessResponse(response, ['items']);
        expect(data.data.items).toHaveLength(0);
      });
    });
  });

  // ======================
  // POST テスト
  // ======================
  describe('POST /api/[endpoint]', () => {
    beforeEach(() => {
      // モックデータのセットアップ
      const createdData = createMockUser();
      prismaMock.model.create.mockResolvedValue(createdData as any);
    });

    describe('正常系', () => {
      test('有効なデータでリソースを作成できること', async () => {
        // Arrange
        const POST = await importPOSTFunction();
        const requestData = {
          name: 'テストデータ',
          description: '説明文',
        };
        const request = createAuthenticatedRequest('emp_001', {
          'content-type': 'application/json',
        });
        (request as any).json = jest.fn().mockResolvedValue(requestData);

        // Act
        const response = await POST(request);

        // Assert
        const data = await expectCreatedResponse(response, ['id', 'name']);
        expect(prismaMock.model.create).toHaveBeenCalledWith({
          data: expect.objectContaining({
            employee_id: 'emp_001',
            name: 'テストデータ',
          }),
        });
      });
    });

    describe('異常系', () => {
      test('必須フィールドが欠けている場合、400を返すこと', async () => {
        // Arrange
        const POST = await importPOSTFunction();
        const invalidData = {}; // 必須フィールドなし
        const request = createAuthenticatedRequest('emp_001');
        (request as any).json = jest.fn().mockResolvedValue(invalidData);

        // Act
        const response = await POST(request);

        // Assert
        const { status, data } = await getResponseData(response);
        expectValidationErrorResponse(response, data);
      });

      test('重複データの場合、400を返すこと', async () => {
        // Arrange
        prismaMock.model.create.mockRejectedValue(
          new Error('Unique constraint failed')
        );
        const POST = await importPOSTFunction();
        const requestData = { name: '重複データ' };
        const request = createAuthenticatedRequest('emp_001');
        (request as any).json = jest.fn().mockResolvedValue(requestData);

        // Act
        const response = await POST(request);

        // Assert
        expect(response.status).toBe(400);
      });
    });
  });

  // ======================
  // PUT テスト
  // ======================
  describe('PUT /api/[endpoint]/[id]', () => {
    beforeEach(() => {
      const updatedData = createMockUser({ name: '更新後' });
      prismaMock.model.update.mockResolvedValue(updatedData as any);
    });

    describe('正常系', () => {
      test('リソースを更新できること', async () => {
        // Arrange
        const PUT = await importPUTFunction();
        const updateData = { name: '更新後の名前' };
        const request = createAuthenticatedRequest('emp_001');
        (request as any).json = jest.fn().mockResolvedValue(updateData);

        // Act
        const response = await PUT(request, { params: { id: 'target_id' } });

        // Assert
        const data = await expectCompleteSuccessResponse(response);
        expect(prismaMock.model.update).toHaveBeenCalledWith({
          where: { id: 'target_id' },
          data: expect.objectContaining(updateData),
        });
      });
    });

    describe('異常系', () => {
      test('存在しないIDの場合、404を返すこと', async () => {
        // Arrange
        prismaMock.model.update.mockRejectedValue(
          new Error('Record not found')
        );
        const PUT = await importPUTFunction();
        const request = createAuthenticatedRequest('emp_001');
        (request as any).json = jest.fn().mockResolvedValue({ name: '更新' });

        // Act
        const response = await PUT(request, { params: { id: 'invalid_id' } });

        // Assert
        expect(response.status).toBe(404);
      });
    });
  });

  // ======================
  // DELETE テスト
  // ======================
  describe('DELETE /api/[endpoint]/[id]', () => {
    beforeEach(() => {
      const deletedData = createMockUser();
      prismaMock.model.delete.mockResolvedValue(deletedData as any);
    });

    describe('正常系', () => {
      test('リソースを削除できること', async () => {
        // Arrange
        const DELETE = await importDELETEFunction();
        const request = createAuthenticatedRequest('emp_001');

        // Act
        const response = await DELETE(request, { params: { id: 'target_id' } });

        // Assert
        expect(response.status).toBe(200);
        expect(prismaMock.model.delete).toHaveBeenCalledWith({
          where: { id: 'target_id' },
        });
      });
    });

    describe('異常系', () => {
      test('存在しないIDの場合、404を返すこと', async () => {
        // Arrange
        prismaMock.model.delete.mockRejectedValue(
          new Error('Record not found')
        );
        const DELETE = await importDELETEFunction();
        const request = createAuthenticatedRequest('emp_001');

        // Act
        const response = await DELETE(request, { params: { id: 'invalid_id' } });

        // Assert
        expect(response.status).toBe(404);
      });
    });
  });

  // ======================
  // レスポンス形式テスト
  // ======================
  describe('レスポンス形式テスト', () => {
    test('レスポンスが正しい形式であること', async () => {
      // Arrange
      const GET = await importGETFunction();
      const request = createAuthenticatedRequest('emp_001');

      // Act
      const response = await GET(request);
      const responseData = await response.json();

      // Assert
      expect(responseData).toHaveProperty('success');
      expect(responseData).toHaveProperty('data');
      expect(responseData).toHaveProperty('timestamp');
      expect(typeof responseData.success).toBe('boolean');
      expect(typeof responseData.timestamp).toBe('string');
    });
  });

  // ======================
  // パフォーマンステスト（オプション）
  // ======================
  describe('パフォーマンステスト', () => {
    test('レスポンス時間が1秒以内であること', async () => {
      // Arrange
      const GET = await importGETFunction();
      const request = createAuthenticatedRequest('emp_001');

      // Act
      const startTime = Date.now();
      const response = await GET(request);
      const endTime = Date.now();
      const executionTime = endTime - startTime;

      // Assert
      expect(response.status).toBe(200);
      expect(executionTime).toBeLessThan(1000);
    });
  });
});
