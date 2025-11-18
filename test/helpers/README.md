# 統合テストヘルパー関数ガイド

## 📋 概要

このディレクトリには、統合テストの実装を効率化するためのヘルパー関数が含まれています。これらのヘルパーを使用することで、テストコードの重複を削減し、保守性と可読性を向上させることができます。

## 📂 ファイル構成

```
test/helpers/
├── index.ts                    # 統合エクスポート（すべてのヘルパーを一括インポート可能）
├── setup.ts                    # データベースセットアップ・ティアダウン
├── mock-request.ts             # NextRequestモック生成
├── test-data-factory.ts        # テストデータ生成ファクトリー
├── assertion-helpers.ts        # 共通アサーション関数
├── test-setup-helpers.ts       # テストセットアップパターン
└── README.md                   # このファイル
```

## 🚀 基本的な使用方法

### 1. ヘルパー関数のインポート

```typescript
// 個別インポート
import { setupTestDatabase, createTestTenant } from '@/test/helpers/setup'
import { assertSuccessResponse } from '@/test/helpers/assertion-helpers'

// 一括インポート（推奨）
import {
  setupTestDatabase,
  teardownTestDatabase,
  cleanupTestData,
  createTestTenant,
  createTestEmployee,
  assertSuccessResponse,
  assertErrorResponse
} from '@/test/helpers'
```

### 2. 基本的なテスト構造

```typescript
import { PrismaClient } from '@prisma/client'
import {
  setupTestDatabase,
  teardownTestDatabase,
  cleanupTestData,
  setupBasicTestContext,
  assertSuccessResponse
} from '@/test/helpers'

describe('API統合テスト: サンプルAPI', () => {
  let prisma: PrismaClient
  let GET: (request: Request) => Promise<Response>

  beforeAll(async () => {
    prisma = await setupTestDatabase()
    const module = await import('@/app/api/sample/route')
    GET = module.GET
  })

  afterAll(async () => {
    await teardownTestDatabase()
  })

  beforeEach(async () => {
    await cleanupTestData(prisma)
  })

  test('基本的なAPIテスト', async () => {
    // テストコンテキストの作成（テナント + 従業員）
    const { tenant, employee } = await setupBasicTestContext(prisma)

    // APIリクエスト実行
    const response = await GET(/* ... */)
    const responseData = await response.json()

    // アサーション
    assertSuccessResponse(response, responseData)
  })
})
```

## 📚 ヘルパー関数詳細

### データベースセットアップ (`setup.ts`)

#### `setupTestDatabase()`
テストデータベースの接続とマイグレーション実行

```typescript
const prisma = await setupTestDatabase()
```

#### `teardownTestDatabase()`
テスト終了後のデータベース切断

```typescript
await teardownTestDatabase()
```

#### `cleanupTestData(prisma)`
テストデータの一括削除

```typescript
await cleanupTestData(prisma)
```

---

### テストデータファクトリー (`test-data-factory.ts`)

#### テナント・組織データ

```typescript
// テナント作成
const tenant = await createTestTenant(prisma, {
  tenant_code: 'CUSTOM_CODE',
  tenant_name: 'カスタムテナント'
})

// 部署作成
const department = await createTestDepartment(prisma, {
  department_code: 'DEPT001',
  department_name: 'システム部'
})

// 従業員作成
const employee = await createTestEmployee(prisma, {
  tenant_id: tenant.id,
  employee_code: 'EMP001',
  full_name: '山田太郎'
})
```

#### スキル関連データ

```typescript
// スキルカテゴリ作成
const category = await createTestSkillCategory(prisma, {
  category_code: 'CAT_PROG',
  category_name: 'プログラミング'
})

// スキルアイテム作成
const skillItem = await createTestSkillItem(prisma, {
  skill_code: 'SKILL_JS',
  skill_name: 'JavaScript',
  skill_category_id: category.id
})

// スキル記録作成
const skillRecord = await createTestSkillRecord(
  prisma,
  employee.id,
  skillItem.id,
  tenant.id,
  'SYSTEM',
  { skill_level: 4, self_assessment: 4 }
)
```

#### プロジェクト・研修データ

```typescript
// プロジェクト記録作成
const project = await createTestProjectRecord(
  prisma,
  employee.id,
  tenant.id,
  'SYSTEM',
  {
    project_name: 'ECサイト構築',
    project_code: 'PRJ001'
  }
)

// 研修履歴作成
const training = await createTestTrainingHistory(
  prisma,
  employee.id,
  tenant.id,
  'SYSTEM',
  { training_name: 'React基礎講座' }
)
```

#### 通知・レポートデータ

```typescript
// 通知作成
const notification = await createTestNotification(
  prisma,
  employee.id,
  tenant.id,
  {
    notification_type: 'info',
    title: '新しい通知',
    message: 'テストメッセージ',
    read_status: 'unread',
    priority_level: 'high'
  }
)

// レポートテンプレート作成
const template = await createTestReportTemplate(
  prisma,
  tenant.id,
  {
    template_code: 'TPL_SKILL',
    template_name: 'スキルレポート',
    report_category: 'SKILL',
    output_format: 'PDF'
  }
)

// レポート生成レコード作成
const reportGen = await createTestReportGeneration(
  prisma,
  template.id,
  employee.id,
  tenant.id,
  {
    report_title: '2025年度スキルレポート',
    generation_status: 'COMPLETED',
    parameters: { year: 2025, department: 'IT' }
  }
)
```

---

### アサーションヘルパー (`assertion-helpers.ts`)

#### レスポンス検証

```typescript
// 成功レスポンス（200 OK）
assertSuccessResponse(response, responseData)

// 作成成功レスポンス（201 Created）
assertCreatedResponse(response, responseData)

// エラーレスポンス
assertErrorResponse(response, responseData, 'INVALID_PARAMETER', 400)

// 認証エラー
assertAuthenticationError(response, responseData)

// 認可エラー
assertAuthorizationError(response, responseData)

// Not Found
assertNotFoundError(response, responseData)
```

#### バリデーションエラー検証

```typescript
assertValidationError(response, responseData, [
  { field: 'email', message: 'メールアドレスが不正です' },
  { field: 'password', message: 'パスワードは8文字以上必要です' }
])
```

#### データ形式検証

```typescript
// ISO8601形式の日付チェック
assertDateFieldsISO8601(notification, ['created_at', 'updated_at', 'expires_at'])

// ページネーション情報検証
assertPaginationStructure(pagination, 20, 0)

// サマリー情報検証
assertSummaryStructure(summary, ['total', 'unread', 'read'])

// 必須フィールド検証
assertRequiredFields(employee, ['id', 'employee_code', 'full_name'])

// 配列要素のプロパティ検証
assertArrayItemsHaveProperties(notifications, ['id', 'title', 'message'])
```

#### ソート順検証

```typescript
// 降順チェック
assertDescendingOrder(notifications, (item) => item.created_at)

// 昇順チェック
assertAscendingOrder(employees, (item) => item.employee_code)
```

---

### テストセットアップヘルパー (`test-setup-helpers.ts`)

#### 基本テストコンテキスト作成

```typescript
// テナント + 従業員を一括作成
const { tenant, employee } = await setupBasicTestContext(prisma, {
  tenantCode: 'TEST_TENANT',
  employeeCode: 'EMP001'
})
```

#### 複数従業員のテストコンテキスト

```typescript
// 3人の従業員を含むコンテキスト
const { tenant, employees } = await setupMultiEmployeeContext(prisma, 3)

console.log(employees[0].employee_code) // EMP001
console.log(employees[1].employee_code) // EMP002
console.log(employees[2].employee_code) // EMP003
```

#### テストデータのバッチ作成

```typescript
// 10件の通知を一括作成
const notifications = await createTestDataBatch(
  (overrides) => createTestNotification(prisma, employee.id, tenant.id, overrides),
  10,
  (i) => ({
    title: `通知 ${i + 1}`,
    message: `メッセージ ${i + 1}`
  })
)
```

#### 日付生成ヘルパー

```typescript
// 今日
const today = generateDateOffset(new Date(), 0) // "2025-11-18"

// 7日前
const weekAgo = generateDateOffset(new Date(), -7) // "2025-11-11"

// 30日後
const nextMonth = generateDateOffset(new Date(), 30) // "2025-12-18"
```

---

## 💡 ベストプラクティス

### 1. ヘルパー関数の使用

❌ **悪い例：手動でテストデータを作成**

```typescript
const tenant = await prisma.tenant.create({
  data: {
    tenant_code: 'TEST001',
    tenant_name: 'テストテナント',
    tenant_name_en: 'Test Tenant',
    domain_name: 'test.com',
    status: 'active'
  }
})
```

✅ **良い例：ファクトリー関数を使用**

```typescript
const tenant = await createTestTenant(prisma, {
  tenant_code: 'TEST001'
})
```

### 2. アサーションの共通化

❌ **悪い例：繰り返しのアサーション**

```typescript
expect(response.status).toBe(200)
expect(responseData.success).toBe(true)
expect(responseData).toHaveProperty('data')
```

✅ **良い例：ヘルパー関数を使用**

```typescript
assertSuccessResponse(response, responseData)
```

### 3. テストセットアップの共通化

❌ **悪い例：毎回手動でセットアップ**

```typescript
const tenant = await createTestTenant(prisma)
const employee = await createTestEmployee(prisma, { tenant_id: tenant.id })
```

✅ **良い例：セットアップヘルパーを使用**

```typescript
const { tenant, employee } = await setupBasicTestContext(prisma)
```

---

## 🔧 カスタムヘルパーの追加

新しいヘルパー関数を追加する場合は、以下の手順に従ってください：

1. 適切なヘルパーファイルに関数を追加
2. `index.ts`にエクスポートを追加
3. このREADMEに使用例を追加

### 例：新しいファクトリー関数の追加

```typescript
// test-data-factory.ts に追加
export async function createTestCustomData(
  prisma: PrismaClient,
  overrides: Partial<{...}> = {}
) {
  // 実装
}

// index.ts に追加
export { createTestCustomData } from './test-data-factory'
```

---

## 📊 統計

**現在利用可能なヘルパー関数数**:
- データベース関連: 3関数
- リクエストモック: 5関数
- テストデータファクトリー: 17関数
- アサーション: 16関数
- セットアップパターン: 6関数

**合計**: 47関数

---

## 🤝 貢献

新しいヘルパー関数の追加や改善案がある場合は、以下のガイドラインに従ってください：

1. **単一責任の原則**: 各関数は1つの明確な目的を持つ
2. **再利用性**: 複数のテストで使える汎用的な実装
3. **型安全性**: TypeScriptの型システムを活用
4. **ドキュメント**: JSDocコメントと使用例を記載

---

*Last Updated: 2025-11-18 | Version: 1.0.0*
