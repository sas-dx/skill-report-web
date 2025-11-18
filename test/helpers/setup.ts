/**
 * 統合テスト用データベースセットアップユーティリティ
 * 要求仕様ID: TEST-INT.1
 * 実装ガイド: docs/testing/04_統合テスト実装ガイド.md
 */

import { PrismaClient } from '@prisma/client'
import { execSync } from 'child_process'

let prisma: PrismaClient | undefined

/**
 * テスト用データベースのセットアップ
 * - テスト用データベースURLを設定
 * - Prismaマイグレーションを実行
 * - データベース接続を確立
 */
export const setupTestDatabase = async () => {
  const testDatabaseUrl = process.env.TEST_DATABASE_URL ||
    'postgresql://test_user:test_password@localhost:5434/skill_report_test_db'

  process.env.DATABASE_URL = testDatabaseUrl

  prisma = new PrismaClient({
    datasources: {
      db: { url: testDatabaseUrl }
    }
  })

  try {
    // Prismaマイグレーションを実行
    execSync('npx prisma migrate deploy --schema=src/database/prisma/schema.prisma', {
      env: { ...process.env, DATABASE_URL: testDatabaseUrl },
      stdio: 'inherit'
    })

    await prisma.$connect()
    console.log('✅ Test database connected')
  } catch (error) {
    console.error('❌ Test database setup failed:', error)
    throw error
  }

  return prisma
}

/**
 * テスト用データベースのクリーンアップと切断
 */
export const teardownTestDatabase = async () => {
  if (prisma) {
    await prisma.$disconnect()
    console.log('✅ Test database disconnected')
  }
}

/**
 * テストデータのクリーンアップ
 * - 全テーブルのデータを削除（TRUNCATE CASCADE）
 * - 外部キー制約を考慮した順序で削除
 */
export const cleanupTestData = async (prismaClient: PrismaClient) => {
  const tables = [
    // トランザクションテーブル（子テーブル）から削除
    'TRN_SkillRecord',
    'TRN_TrainingHistory',
    'TRN_ProjectRecord',
    'TRN_GoalProgress',
    'TRN_CareerPlan',
    // マスタテーブル（親テーブル）を削除
    'MST_Employee',
    'MST_Skill',
    'MST_Department',
    'MST_SkillCategory'
  ]

  for (const table of tables) {
    try {
      await prismaClient.$executeRawUnsafe(`TRUNCATE TABLE "${table}" CASCADE`)
    } catch (error) {
      console.warn(`⚠️  Failed to truncate table ${table}:`, error)
      // テーブルが存在しない場合はスキップ
    }
  }

  console.log('✅ Test data cleaned')
}

export { prisma }
