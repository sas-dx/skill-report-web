import { PrismaClient } from '@prisma/client'
import { mockDeep, mockReset, DeepMockProxy } from 'jest-mock-extended'

/**
 * Prismaクライアントのモック
 * jest-mock-extendedを使用した型安全なモック実装
 */

// Prismaクライアントのモック化
jest.mock('@/database/prisma/client', () => ({
  __esModule: true,
  default: mockDeep<PrismaClient>(),
  prisma: mockDeep<PrismaClient>(),
}))

// モックインスタンスの取得
import prisma from '@/database/prisma/client'

// テスト前にモックをリセット
beforeEach(() => {
  mockReset(prismaMock)
})

// エクスポート
export const prismaMock = prisma as unknown as DeepMockProxy<PrismaClient>
