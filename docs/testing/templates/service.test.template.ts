/**
 * [サービス名]のテスト
 *
 * 実装日: YYYY-MM-DD
 * 実装者: [実装者名]
 */

import { prismaMock } from '@/__mocks__/prisma';
import {
  // テスト対象の関数をインポート
  getItemById,
  getAllItems,
  createItem,
  updateItem,
  deleteItem,
} from '../[service-name].service';
import {
  // 必要なファクトリをインポート
  createMockUser,
  createMockCareerPlan,
} from '@/__tests__/helpers/prismaFactories';

describe('[サービス名]', () => {
  // ======================
  // 取得系テスト（単一）
  // ======================
  describe('getItemById', () => {
    test('アイテムが存在する場合、アイテム情報を返す', async () => {
      // Arrange
      const mockItem = createMockUser();
      prismaMock.model.findUnique.mockResolvedValue(mockItem as any);

      // Act
      const result = await getItemById(1);

      // Assert
      expect(result).toEqual(mockItem);
      expect(prismaMock.model.findUnique).toHaveBeenCalledWith({
        where: { id: 1 },
      });
      expect(prismaMock.model.findUnique).toHaveBeenCalledTimes(1);
    });

    test('アイテムが存在しない場合、nullを返す', async () => {
      // Arrange
      prismaMock.model.findUnique.mockResolvedValue(null);

      // Act
      const result = await getItemById(999);

      // Assert
      expect(result).toBeNull();
      expect(prismaMock.model.findUnique).toHaveBeenCalledWith({
        where: { id: 999 },
      });
    });

    test('データベースエラーが発生した場合、エラーをスローする', async () => {
      // Arrange
      const dbError = new Error('Database connection failed');
      prismaMock.model.findUnique.mockRejectedValue(dbError);

      // Act & Assert
      await expect(getItemById(1)).rejects.toThrow('Database connection failed');
    });
  });

  // ======================
  // 取得系テスト（一覧）
  // ======================
  describe('getAllItems', () => {
    test('複数のアイテムを取得できる', async () => {
      // Arrange
      const mockItems = [
        createMockUser({ user_id: 1, name: 'ユーザー1' }),
        createMockUser({ user_id: 2, name: 'ユーザー2' }),
        createMockUser({ user_id: 3, name: 'ユーザー3' }),
      ];
      prismaMock.model.findMany.mockResolvedValue(mockItems as any);

      // Act
      const result = await getAllItems();

      // Assert
      expect(result).toHaveLength(3);
      expect(result).toEqual(mockItems);
      expect(prismaMock.model.findMany).toHaveBeenCalledWith({
        orderBy: { id: 'asc' },
      });
    });

    test('アイテムが存在しない場合、空配列を返す', async () => {
      // Arrange
      prismaMock.model.findMany.mockResolvedValue([]);

      // Act
      const result = await getAllItems();

      // Assert
      expect(result).toEqual([]);
      expect(result).toHaveLength(0);
    });

    test('フィルタ条件が適用されること', async () => {
      // Arrange
      const mockItems = [createMockUser({ status: 'ACTIVE' })];
      prismaMock.model.findMany.mockResolvedValue(mockItems as any);

      // Act
      const result = await getAllItems({ status: 'ACTIVE' });

      // Assert
      expect(result).toHaveLength(1);
      expect(prismaMock.model.findMany).toHaveBeenCalledWith({
        where: { status: 'ACTIVE' },
        orderBy: { id: 'asc' },
      });
    });
  });

  // ======================
  // 作成系テスト
  // ======================
  describe('createItem', () => {
    test('新しいアイテムを作成できる', async () => {
      // Arrange
      const newItemData = {
        name: '新規アイテム',
        description: '説明文',
      };
      const createdItem = createMockUser({
        id: 999,
        ...newItemData,
      });
      prismaMock.model.create.mockResolvedValue(createdItem as any);

      // Act
      const result = await createItem(newItemData);

      // Assert
      expect(result).toEqual(createdItem);
      expect(result.id).toBe(999);
      expect(result.name).toBe('新規アイテム');
      expect(prismaMock.model.create).toHaveBeenCalledWith({
        data: newItemData,
      });
    });

    test('重複する識別子の場合、エラーをスローする', async () => {
      // Arrange
      const duplicateItemData = {
        name: '重複アイテム',
        code: 'DUPLICATE',
      };
      prismaMock.model.create.mockRejectedValue(
        new Error('Unique constraint failed on the fields: (`code`)')
      );

      // Act & Assert
      await expect(createItem(duplicateItemData)).rejects.toThrow(
        'Unique constraint failed'
      );
    });

    test('必須フィールドが欠けている場合、エラーをスローする', async () => {
      // Arrange
      const invalidData = {}; // 必須フィールドなし
      prismaMock.model.create.mockRejectedValue(
        new Error('Required field missing')
      );

      // Act & Assert
      await expect(createItem(invalidData)).rejects.toThrow(
        'Required field missing'
      );
    });
  });

  // ======================
  // 更新系テスト
  // ======================
  describe('updateItem', () => {
    test('アイテムを更新できる', async () => {
      // Arrange
      const updateData = {
        name: '更新後の名前',
        description: '更新後の説明',
      };
      const updatedItem = createMockUser({
        id: 1,
        ...updateData,
      });
      prismaMock.model.update.mockResolvedValue(updatedItem as any);

      // Act
      const result = await updateItem(1, updateData);

      // Assert
      expect(result).toEqual(updatedItem);
      expect(result.name).toBe('更新後の名前');
      expect(prismaMock.model.update).toHaveBeenCalledWith({
        where: { id: 1 },
        data: updateData,
      });
    });

    test('存在しないアイテムを更新しようとした場合、エラーをスローする', async () => {
      // Arrange
      prismaMock.model.update.mockRejectedValue(
        new Error('Record to update not found')
      );

      // Act & Assert
      await expect(updateItem(999, { name: '更新' })).rejects.toThrow(
        'Record to update not found'
      );
    });

    test('部分更新ができる', async () => {
      // Arrange
      const partialUpdate = { name: '名前のみ更新' };
      const updatedItem = createMockUser({
        id: 1,
        name: '名前のみ更新',
        description: '既存の説明',  // 変更されない
      });
      prismaMock.model.update.mockResolvedValue(updatedItem as any);

      // Act
      const result = await updateItem(1, partialUpdate);

      // Assert
      expect(result.name).toBe('名前のみ更新');
      expect(result.description).toBe('既存の説明');
    });
  });

  // ======================
  // 削除系テスト
  // ======================
  describe('deleteItem', () => {
    test('アイテムを削除できる', async () => {
      // Arrange
      const itemToDelete = createMockUser({ id: 1 });
      prismaMock.model.delete.mockResolvedValue(itemToDelete as any);

      // Act
      const result = await deleteItem(1);

      // Assert
      expect(result).toEqual(itemToDelete);
      expect(prismaMock.model.delete).toHaveBeenCalledWith({
        where: { id: 1 },
      });
    });

    test('存在しないアイテムを削除しようとした場合、エラーをスローする', async () => {
      // Arrange
      prismaMock.model.delete.mockRejectedValue(
        new Error('Record to delete does not exist')
      );

      // Act & Assert
      await expect(deleteItem(999)).rejects.toThrow(
        'Record to delete does not exist'
      );
    });

    test('論理削除の場合、is_deletedフラグが更新される', async () => {
      // Arrange
      const softDeletedItem = createMockUser({
        id: 1,
        is_deleted: true,
      });
      prismaMock.model.update.mockResolvedValue(softDeletedItem as any);

      // Act
      const result = await deleteItem(1, { soft: true });

      // Assert
      expect(result.is_deleted).toBe(true);
      expect(prismaMock.model.update).toHaveBeenCalledWith({
        where: { id: 1 },
        data: { is_deleted: true },
      });
    });
  });

  // ======================
  // ビジネスロジックテスト
  // ======================
  describe('ビジネスロジック', () => {
    test('特定条件で処理が実行されること', async () => {
      // Arrange
      const mockItem = createMockUser({ status: 'PENDING' });
      prismaMock.model.findUnique.mockResolvedValue(mockItem as any);
      prismaMock.model.update.mockResolvedValue({
        ...mockItem,
        status: 'APPROVED',
      } as any);

      // Act
      const result = await processItem(1);

      // Assert
      expect(result.status).toBe('APPROVED');
      expect(prismaMock.model.update).toHaveBeenCalled();
    });

    test('条件を満たさない場合、処理がスキップされること', async () => {
      // Arrange
      const mockItem = createMockUser({ status: 'COMPLETED' });
      prismaMock.model.findUnique.mockResolvedValue(mockItem as any);

      // Act
      const result = await processItem(1);

      // Assert
      expect(result.status).toBe('COMPLETED');
      expect(prismaMock.model.update).not.toHaveBeenCalled();
    });
  });

  // ======================
  // トランザクションテスト
  // ======================
  describe('トランザクション処理', () => {
    test('複数操作が原子性を保って実行されること', async () => {
      // Arrange
      const item1 = createMockUser({ id: 1 });
      const item2 = createMockUser({ id: 2 });

      prismaMock.$transaction.mockImplementation(async (callback) => {
        return await callback(prismaMock);
      });

      prismaMock.model.create.mockResolvedValueOnce(item1 as any);
      prismaMock.model.create.mockResolvedValueOnce(item2 as any);

      // Act
      const result = await createMultipleItems([
        { name: 'Item 1' },
        { name: 'Item 2' },
      ]);

      // Assert
      expect(result).toHaveLength(2);
      expect(prismaMock.$transaction).toHaveBeenCalled();
    });

    test('トランザクション内でエラーが発生した場合、ロールバックされること', async () => {
      // Arrange
      prismaMock.$transaction.mockRejectedValue(
        new Error('Transaction failed')
      );

      // Act & Assert
      await expect(
        createMultipleItems([{ name: 'Item 1' }])
      ).rejects.toThrow('Transaction failed');
    });
  });

  // ======================
  // モックリセット確認
  // ======================
  describe('モックのリセット確認', () => {
    test('各テスト間でモックがリセットされることを確認', async () => {
      // このテストは、beforeEach でモックがリセットされることを確認します
      // 前のテストでの呼び出し履歴がクリアされているはずです

      // Arrange
      const mockItem = createMockUser();
      prismaMock.model.findUnique.mockResolvedValue(mockItem as any);

      // Act
      await getItemById(1);

      // Assert: このテストでは1回だけ呼ばれているはず
      expect(prismaMock.model.findUnique).toHaveBeenCalledTimes(1);
    });
  });
});
