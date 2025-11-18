/**
 * ユーザーサービスのテスト（Prismaモック使用例）
 *
 * このテストファイルは、jest-mock-extendedを使用したPrismaモックの
 * 実践的な使用方法を示すサンプルです。
 */

import { prismaMock } from '@/__mocks__/prisma'
import {
  getUserById,
  getAllUsers,
  createUser,
  countUsers,
  deleteUser,
} from '../user.service'
import type { MST_User } from '@prisma/client'
import { createMockUser } from '@/__tests__/helpers/prismaFactories'

describe('ユーザーサービス', () => {
  describe('getUserById', () => {
    it('ユーザーが存在する場合、ユーザー情報を返す', async () => {
      // Arrange: モックデータを準備
      const mockUser = createMockUser()
      prismaMock.mST_User.findUnique.mockResolvedValue(mockUser)

      // Act: 関数を実行
      const result = await getUserById(1)

      // Assert: 結果を検証
      expect(result).toEqual(mockUser)
      expect(prismaMock.mST_User.findUnique).toHaveBeenCalledWith({
        where: { user_id: 1 },
      })
      expect(prismaMock.mST_User.findUnique).toHaveBeenCalledTimes(1)
    })

    it('ユーザーが存在しない場合、nullを返す', async () => {
      // Arrange
      prismaMock.mST_User.findUnique.mockResolvedValue(null)

      // Act
      const result = await getUserById(999)

      // Assert
      expect(result).toBeNull()
      expect(prismaMock.mST_User.findUnique).toHaveBeenCalledWith({
        where: { user_id: 999 },
      })
    })

    it('データベースエラーが発生した場合、エラーをスローする', async () => {
      // Arrange
      const dbError = new Error('Database connection failed')
      prismaMock.mST_User.findUnique.mockRejectedValue(dbError)

      // Act & Assert
      await expect(getUserById(1)).rejects.toThrow('Database connection failed')
    })
  })

  describe('getAllUsers', () => {
    it('複数のユーザーを取得できる', async () => {
      // Arrange
      const mockUsers = [
        createMockUser({ user_id: 1, name: 'ユーザー1' }),
        createMockUser({ user_id: 2, name: 'ユーザー2' }),
        createMockUser({ user_id: 3, name: 'ユーザー3' }),
      ]
      prismaMock.mST_User.findMany.mockResolvedValue(mockUsers)

      // Act
      const result = await getAllUsers()

      // Assert
      expect(result).toHaveLength(3)
      expect(result).toEqual(mockUsers)
      expect(prismaMock.mST_User.findMany).toHaveBeenCalledWith({
        orderBy: { user_id: 'asc' },
      })
    })

    it('ユーザーが存在しない場合、空配列を返す', async () => {
      // Arrange
      prismaMock.mST_User.findMany.mockResolvedValue([])

      // Act
      const result = await getAllUsers()

      // Assert
      expect(result).toEqual([])
      expect(result).toHaveLength(0)
    })
  })

  describe('createUser', () => {
    it('新しいユーザーを作成できる', async () => {
      // Arrange
      const newUserData = {
        employee_id: 'EMP999',
        name: '新規ユーザー',
        email: 'new@example.com',
        role: 'user',
      }
      const createdUser = createMockUser({
        user_id: 999,
        ...newUserData,
      })
      prismaMock.mST_User.create.mockResolvedValue(createdUser)

      // Act
      const result = await createUser(newUserData)

      // Assert
      expect(result).toEqual(createdUser)
      expect(result.user_id).toBe(999)
      expect(result.name).toBe('新規ユーザー')
      expect(prismaMock.mST_User.create).toHaveBeenCalledWith({
        data: newUserData,
      })
    })

    it('重複するメールアドレスの場合、エラーをスローする', async () => {
      // Arrange
      const duplicateUserData = {
        employee_id: 'EMP001',
        name: 'テストユーザー',
        email: 'test@example.com',
        role: 'user',
      }
      prismaMock.mST_User.create.mockRejectedValue(
        new Error('Unique constraint failed on the fields: (`email`)')
      )

      // Act & Assert
      await expect(createUser(duplicateUserData)).rejects.toThrow(
        'Unique constraint failed'
      )
    })
  })

  describe('countUsers', () => {
    it('ユーザー数を正しくカウントする', async () => {
      // Arrange
      prismaMock.mST_User.count.mockResolvedValue(42)

      // Act
      const result = await countUsers()

      // Assert
      expect(result).toBe(42)
      expect(prismaMock.mST_User.count).toHaveBeenCalledTimes(1)
    })

    it('ユーザーが存在しない場合、0を返す', async () => {
      // Arrange
      prismaMock.mST_User.count.mockResolvedValue(0)

      // Act
      const result = await countUsers()

      // Assert
      expect(result).toBe(0)
    })
  })

  describe('deleteUser', () => {
    it('ユーザーを削除できる', async () => {
      // Arrange
      const userToDelete = createMockUser({ user_id: 1 })
      prismaMock.mST_User.delete.mockResolvedValue(userToDelete)

      // Act
      const result = await deleteUser(1)

      // Assert
      expect(result).toEqual(userToDelete)
      expect(prismaMock.mST_User.delete).toHaveBeenCalledWith({
        where: { user_id: 1 },
      })
    })

    it('存在しないユーザーを削除しようとした場合、エラーをスローする', async () => {
      // Arrange
      prismaMock.mST_User.delete.mockRejectedValue(
        new Error('Record to delete does not exist')
      )

      // Act & Assert
      await expect(deleteUser(999)).rejects.toThrow(
        'Record to delete does not exist'
      )
    })
  })

  describe('モックのリセット確認', () => {
    it('各テスト間でモックがリセットされることを確認', async () => {
      // このテストは、beforeEach でモックがリセットされることを確認します
      // 前のテストでの呼び出し履歴がクリアされているはずです

      // Arrange
      const mockUser = createMockUser()
      prismaMock.mST_User.findUnique.mockResolvedValue(mockUser)

      // Act
      await getUserById(1)

      // Assert: このテストでは1回だけ呼ばれているはず（前のテストの履歴は残っていない）
      expect(prismaMock.mST_User.findUnique).toHaveBeenCalledTimes(1)
    })
  })
})
