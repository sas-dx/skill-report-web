/**
 * 統合テスト用セットアップヘルパー関数
 * テストの共通セットアップパターンを提供
 */

import { PrismaClient } from '@prisma/client'
import { createTestTenant, createTestEmployee } from './test-data-factory'

/**
 * 基本的なテストコンテキスト（テナント + 従業員）を作成
 * @param prisma PrismaClientインスタンス
 * @param overrides オーバーライド設定
 * @returns テナントと従業員の情報
 */
export async function setupBasicTestContext(
  prisma: PrismaClient,
  overrides: {
    tenantCode?: string
    employeeCode?: string
  } = {}
) {
  const tenant = await createTestTenant(prisma, {
    tenant_code: overrides.tenantCode || 'TEST_TENANT'
  })

  const employee = await createTestEmployee(prisma, {
    tenant_id: tenant.id,
    employee_code: overrides.employeeCode || 'EMP001'
  })

  return {
    tenant,
    employee
  }
}

/**
 * 複数従業員を含むテストコンテキストを作成
 * @param prisma PrismaClientインスタンス
 * @param employeeCount 作成する従業員数（デフォルト: 2）
 * @returns テナントと従業員配列
 */
export async function setupMultiEmployeeContext(
  prisma: PrismaClient,
  employeeCount: number = 2
) {
  const tenant = await createTestTenant(prisma)
  const employees = []

  for (let i = 0; i < employeeCount; i++) {
    const employee = await createTestEmployee(prisma, {
      tenant_id: tenant.id,
      employee_code: `EMP00${i + 1}`,
      full_name: `テスト太郎${i + 1}`
    })
    employees.push(employee)
  }

  return {
    tenant,
    employees
  }
}

/**
 * API統合テスト用の共通セットアップ
 * Route Handlerの動的インポートとDBセットアップを組み合わせ
 * @param apiPath APIのパス（例: '@/app/api/notifications/[userId]/route'）
 * @param methods インポートするHTTPメソッド（例: ['GET', 'PUT']）
 * @returns インポートされたRoute Handler関数
 */
export async function setupAPITest<T extends Record<string, any>>(
  apiPath: string,
  methods: string[] = ['GET']
): Promise<T> {
  const module = await import(apiPath)
  const handlers: any = {}

  methods.forEach(method => {
    if (module[method]) {
      handlers[method] = module[method]
    }
  })

  return handlers as T
}

/**
 * テストデータのバッチ作成ヘルパー
 * @param createFn データ作成関数
 * @param count 作成数
 * @param getOverrides インデックスに基づくオーバーライド取得関数
 * @returns 作成されたデータの配列
 */
export async function createTestDataBatch<T>(
  createFn: (overrides: any) => Promise<T>,
  count: number,
  getOverrides: (index: number) => any = (i) => ({})
): Promise<T[]> {
  const results: T[] = []

  for (let i = 0; i < count; i++) {
    const data = await createFn(getOverrides(i))
    results.push(data)
  }

  return results
}

/**
 * 日付範囲を生成するヘルパー
 * @param baseDate 基準日
 * @param offsetDays オフセット日数
 * @returns ISO8601形式の日付文字列
 */
export function generateDateOffset(
  baseDate: Date = new Date(),
  offsetDays: number = 0
): string {
  const date = new Date(baseDate)
  date.setDate(date.getDate() + offsetDays)
  return date.toISOString().split('T')[0]
}

/**
 * テストデータのクリーンアップ順序を定義
 * 外部キー制約を考慮した削除順序
 */
export const DATA_CLEANUP_ORDER = [
  'reportGeneration',
  'reportTemplate',
  'notification',
  'trainingHistory',
  'projectRecord',
  'skillRecord',
  'goalProgress',
  'careerPlan',
  'skillItem',
  'skillCategory',
  'skill',
  'userAuth',
  'employee',
  'department',
  'tenant'
] as const

/**
 * 順序を考慮したテストデータの一括削除
 * @param prisma PrismaClientインスタンス
 * @param tables 削除するテーブル配列（省略時は全テーブル）
 */
export async function cleanupTestDataOrdered(
  prisma: PrismaClient,
  tables: readonly string[] = DATA_CLEANUP_ORDER
) {
  for (const table of tables) {
    const modelName = table.charAt(0).toUpperCase() + table.slice(1)
    if ((prisma as any)[table]) {
      await (prisma as any)[table].deleteMany({})
    }
  }
}
