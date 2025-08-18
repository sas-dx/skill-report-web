/**
 * 要求仕様ID: PLT.1-WEB.1
 * 設計書: docs/design/architecture/技術スタック設計書.md
 * 実装内容: Prisma Client設定
 */

import { PrismaClient, Prisma } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;

/**
 * Prismaエラーハンドリング関数
 */
export function handlePrismaError(error: any): Error {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    switch (error.code) {
      case 'P2002':
        return new Error('UNIQUE_CONSTRAINT_VIOLATION');
      case 'P2025':
        return new Error('RECORD_NOT_FOUND');
      case 'P2003':
        return new Error('FOREIGN_KEY_CONSTRAINT_VIOLATION');
      default:
        return new Error('DATABASE_ERROR');
    }
  }
  
  if (error instanceof Prisma.PrismaClientUnknownRequestError) {
    return new Error('UNKNOWN_DATABASE_ERROR');
  }
  
  if (error instanceof Prisma.PrismaClientValidationError) {
    return new Error('VALIDATION_ERROR');
  }
  
  return error instanceof Error ? error : new Error('UNKNOWN_ERROR');
}
