import { PrismaClient } from '@prisma/client'
import { mockDeep, mockReset, DeepMockProxy } from 'jest-mock-extended'

/**
 * Prismaクライアントのモック
 * jest-mock-extendedを使用した型安全なモック実装
 */

// Prismaクライアントのモック化
jest.mock('@/lib/prisma', () => ({
  __esModule: true,
  prisma: mockDeep<PrismaClient>(),
}))

// モックインスタンスの取得
import { prisma } from '@/lib/prisma'

// テスト前にモックをリセット
beforeEach(() => {
  mockReset(prismaMock)
})

// エクスポート
export const prismaMock = prisma as unknown as DeepMockProxy<PrismaClient>
