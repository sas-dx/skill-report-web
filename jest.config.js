/**
 * Jest設定ファイル
 * 要求仕様ID: TST.1-UNIT.1
 * 対応設計書: docs/testing/03_ユニットテスト実装ガイド.md
 */

const nextJest = require('next/jest')

const createJestConfig = nextJest({
  // Next.jsアプリのパスを指定
  dir: './',
})

// Jestのカスタム設定
const customJestConfig = {
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  moduleNameMapper: {
    // tsconfig.jsonのpathsと同じエイリアスを設定
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  testEnvironment: 'node',
  testMatch: [
    '**/__tests__/**/*.test.ts',
    '**/__tests__/**/*.test.tsx',
    '**/tests/**/*.test.ts',
    '**/tests/**/*.test.tsx'
  ],
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/database/prisma/migrations/**',
    '!src/database/prisma/seed.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  testTimeout: 10000, // 10秒のタイムアウト
}

// createJestConfigは非同期関数なので、Jestが設定を読み込めるようにエクスポート
module.exports = createJestConfig(customJestConfig)
