# テストヘルパー関数

このディレクトリには、テストコードの重複を削減し、保守性を向上させるためのヘルパー関数が含まれています。

## 📁 ファイル構成

### `nextRequest.helper.ts`
Next.js の `NextRequest` オブジェクトをモックするためのヘルパー関数

### `prismaFactories.ts`
Prisma モデルのテストデータを生成するファクトリ関数

## 🔧 使用方法

### NextRequest モックの作成

#### 基本的な使い方

```typescript
import { createMockNextRequest, createAuthenticatedRequest } from '@/__tests__/helpers/nextRequest.helper';

// 基本的な NextRequest モック
const request = createMockNextRequest({
  url: 'http://localhost:3000/api/users',
  method: 'GET',
  headers: {
    'content-type': 'application/json',
  },
});

// 認証ヘッダー付きリクエスト（推奨）
const authRequest = createAuthenticatedRequest(
  'emp_001',  // ユーザーID
  { 'content-type': 'application/json' },  // 追加ヘッダー
  'http://localhost:3000/api/profile'  // URL
);
```

#### パラメータ

**`createMockNextRequest(options)`**
- `headers`: ヘッダーオブジェクト（省略可）
- `url`: リクエストURL（デフォルト: `http://localhost:3000`）
- `method`: HTTPメソッド（デフォルト: `GET`）
- `body`: リクエストボディ（省略可）

**`createAuthenticatedRequest(userId, additionalHeaders, url)`**
- `userId`: `x-user-id` ヘッダーに設定するユーザーID
- `additionalHeaders`: 追加のヘッダー（省略可）
- `url`: リクエストURL（省略可）

### Prisma ファクトリの使用

#### 単一のモックデータ作成

```typescript
import {
  createMockCareerPlan,
  createMockSkillCategory,
  createMockPosition,
  createMockUser,
} from '@/__tests__/helpers/prismaFactories';

// デフォルト値でキャリアプランを作成
const careerPlan = createMockCareerPlan();

// 一部のフィールドをオーバーライド
const customCareerPlan = createMockCareerPlan({
  employee_id: 'emp_999',
  target_level: 'EXPERT',
  progress_percentage: 75.0,
});

// スキルカテゴリの作成
const skillCategory = createMockSkillCategory({
  category_name: 'データベース設計',
  category_type: 'TECHNICAL',
});
```

#### 複数のモックデータ作成

```typescript
import {
  createMockCareerPlans,
  createMockSkillCategories,
  createMockPositions,
  createMockUsers,
} from '@/__tests__/helpers/prismaFactories';

// 5件のキャリアプランを作成（自動的にIDが連番になる）
const careerPlans = createMockCareerPlans(5);
// => plan_001, plan_002, plan_003, plan_004, plan_005

// 共通のオーバーライドを適用
const activeCareerPlans = createMockCareerPlans(3, {
  plan_status: 'ACTIVE',
  progress_percentage: 50.0,
});

// ユーザーデータを10件作成
const users = createMockUsers(10);
// => EMP001 ~ EMP010
```

## 📝 実装例

### API ルートテストでの使用

```typescript
import { createAuthenticatedRequest } from '@/__tests__/helpers/nextRequest.helper';
import { createMockCareerPlan } from '@/__tests__/helpers/prismaFactories';
import { prismaMock } from '@/__mocks__/prisma';

describe('GET /api/career/init', () => {
  beforeEach(() => {
    // ファクトリを使用してモックデータを設定
    prismaMock.careerPlan.findMany.mockResolvedValue([
      createMockCareerPlan() as any,
    ]);
  });

  test('キャリア初期データを取得できること', async () => {
    const GET = await import('./route').then(m => m.GET);
    const request = createAuthenticatedRequest('emp_001');

    const response = await GET(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.success).toBe(true);
  });
});
```

### サービステストでの使用

```typescript
import { createMockUser } from '@/__tests__/helpers/prismaFactories';
import { prismaMock } from '@/__mocks__/prisma';

describe('ユーザーサービス', () => {
  it('ユーザーを作成できる', async () => {
    const mockUser = createMockUser({
      employee_id: 'EMP999',
      name: '新規ユーザー',
    });

    prismaMock.mST_User.create.mockResolvedValue(mockUser);

    const result = await createUser({
      employee_id: 'EMP999',
      name: '新規ユーザー',
      email: 'new@example.com',
      role: 'user',
    });

    expect(result).toEqual(mockUser);
  });
});
```

## 🎯 ベストプラクティス

### 1. DRY原則の徹底
❌ **悪い例** - インラインでモックを作成
```typescript
const mockUser = {
  user_id: 1,
  employee_id: 'EMP001',
  name: 'テストユーザー',
  email: 'test@example.com',
  role: 'user',
  created_at: new Date('2024-01-01'),
  updated_at: new Date('2024-01-01'),
};
```

✅ **良い例** - ファクトリを使用
```typescript
const mockUser = createMockUser();
```

### 2. 必要なフィールドのみオーバーライド
✅ **推奨**
```typescript
const mockUser = createMockUser({
  employee_id: 'EMP999',  // テストに必要なフィールドのみ
});
```

### 3. テストの可読性を優先
✅ **推奨** - 明確な変数名を使用
```typescript
const activeCareerPlan = createMockCareerPlan({ plan_status: 'ACTIVE' });
const completedCareerPlan = createMockCareerPlan({ plan_status: 'COMPLETED' });
```

### 4. beforeEach での共通セットアップ
✅ **推奨**
```typescript
describe('API テスト', () => {
  beforeEach(() => {
    prismaMock.careerPlan.findMany.mockResolvedValue([
      createMockCareerPlan(),
    ]);
    prismaMock.skillCategory.findMany.mockResolvedValue([
      createMockSkillCategory(),
    ]);
  });

  // テストケース...
});
```

## 📦 利用可能なファクトリ一覧

### 単一データ作成
- `createMockCareerPlan(overrides?)`
- `createMockSkillCategory(overrides?)`
- `createMockPosition(overrides?)`
- `createMockUser(overrides?)`

### 複数データ作成
- `createMockCareerPlans(count, baseOverrides?)`
- `createMockSkillCategories(count, baseOverrides?)`
- `createMockPositions(count, baseOverrides?)`
- `createMockUsers(count, baseOverrides?)`

## 🔄 今後の拡張

新しいファクトリを追加する際は、以下のパターンに従ってください:

```typescript
/**
 * [モデル名]のテストデータを作成
 */
export function createMock[ModelName](overrides?: Partial<any>) {
  return {
    // すべてのフィールドにデフォルト値を設定
    id: 'default_id',
    name: 'デフォルト名',
    // ...
    ...overrides,  // オーバーライドは最後に適用
  }
}

/**
 * 複数の[モデル名]を作成
 */
export function createMock[ModelName]s(count: number, baseOverrides?: Partial<any>) {
  return Array.from({ length: count }, (_, index) =>
    createMock[ModelName]({
      id: `id_${String(index + 1).padStart(3, '0')}`,
      ...baseOverrides,
    })
  )
}
```

## 📚 関連ドキュメント

- [Jestモック設定ガイド](../../../docs/testing/JEST-SETUP.md)
- [Prismaモック使用例](../../../docs/testing/PRISMA-MOCKING.md)
- [テスト戦略](../../../docs/testing/README.md)

---

**更新日**: 2025-11-18
**メンテナー**: システム開発チーム
