/**
 * 要求仕様ID: PLT.1-WEB.1
 * 対応設計書: docs/design/database/prisma/schema.prisma
 * 実装内容: Prismaクライアント設定
 */

import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

// データベース接続テスト用のヘルパー関数
export async function testDatabaseConnection(): Promise<boolean> {
  try {
    await prisma.$queryRaw`SELECT 1`;
    return true;
  } catch (error) {
    console.error('Database connection failed:', error);
    return false;
  }
}

// Prismaクライアントの適切な終了処理
export async function disconnectPrisma(): Promise<void> {
  await prisma.$disconnect();
}
