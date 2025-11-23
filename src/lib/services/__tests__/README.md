# テストサンプル - Prismaモックの使用例

このディレクトリには、`jest-mock-extended`を使用したPrismaモックの実践的な使用例が含まれています。

## 📁 ファイル構成

```
src/lib/services/
├── user.service.ts              # サンプルサービス（Prisma使用）
└── __tests__/
    ├── README.md                # このファイル
    └── user.service.test.ts     # Prismaモック使用例
```

## 🎯 このサンプルの目的

1. **Prismaモックの基本的な使い方を学ぶ**
   - モックのセットアップ方法
   - データの返却方法
   - エラーハンドリング

2. **テストのベストプラクティスを示す**
   - AAA パターン（Arrange-Act-Assert）
   - テストデータのファクトリ関数
   - エッジケースのテスト

3. **実際のプロジェクトで使える参考実装**
   - CRUD操作のテスト
   - 型安全なモック使用
   - モックの検証方法

## 🚀 実行方法

### 特定のテストファイルを実行

```bash
npm test -- src/lib/services/__tests__/user.service.test.ts
```

### すべてのテストを実行

```bash
npm test
```

### カバレッジ付きで実行

```bash
npm test -- --coverage
```

## 📝 テストの主要パターン

### 1. 基本的なモックの使い方

```typescript
import { prismaMock } from '@/__mocks__/prisma'

// モックデータを返す
prismaMock.mST_User.findUnique.mockResolvedValue(mockUser)

// 関数を実行
const result = await getUserById(1)

// 結果を検証
expect(result).toEqual(mockUser)
expect(prismaMock.mST_User.findUnique).toHaveBeenCalledWith({
  where: { user_id: 1 },
})
```

### 2. エラーケースのテスト

```typescript
// エラーを投げる
prismaMock.mST_User.findUnique.mockRejectedValue(
  new Error('Database connection failed')
)

// エラーが投げられることを検証
await expect(getUserById(1)).rejects.toThrow('Database connection failed')
```

### 3. 複数のデータを返す

```typescript
const mockUsers = [user1, user2, user3]
prismaMock.mST_User.findMany.mockResolvedValue(mockUsers)

const result = await getAllUsers()

expect(result).toHaveLength(3)
expect(result).toEqual(mockUsers)
```

### 4. テストデータのファクトリ

```typescript
function createMockUser(overrides?: Partial<MST_User>): MST_User {
  return {
    user_id: 1,
    employee_id: 'EMP001',
    name: 'テストユーザー',
    email: 'test@example.com',
    role: 'user',
    created_at: new Date('2024-01-01'),
    updated_at: new Date('2024-01-01'),
    ...overrides,  // 上書き可能
  }
}

// 使用例
const user1 = createMockUser()
const user2 = createMockUser({ user_id: 2, name: '別のユーザー' })
```

## 💡 テスト作成のヒント

### 1. AAA パターンを使う

```typescript
it('ユーザーを取得できる', async () => {
  // Arrange（準備）: テストデータとモックをセットアップ
  const mockUser = createMockUser()
  prismaMock.mST_User.findUnique.mockResolvedValue(mockUser)

  // Act（実行）: テスト対象の関数を実行
  const result = await getUserById(1)

  // Assert（検証）: 結果を検証
  expect(result).toEqual(mockUser)
})
```

### 2. モックの自動リセット

`jest.setup.js`で自動的にモックがリセットされるため、各テストは独立しています：

```typescript
beforeEach(() => {
  mockReset(prismaMock)  // 自動実行される
})
```

### 3. 型安全性を活用

`jest-mock-extended`により、Prismaの型が保持されます：

```typescript
// ✅ 型安全 - TypeScriptが補完してくれる
prismaMock.mST_User.findUnique.mockResolvedValue(mockUser)

// ❌ 型エラー - 存在しないメソッド
prismaMock.mST_User.nonExistentMethod.mockResolvedValue(...)
```

## 🔍 よくある質問

### Q: モックがリセットされない場合は？

A: `jest.setup.js`で`require('./src/__mocks__/prisma')`が実行されているか確認してください。これにより`beforeEach`でのリセットが有効になります。

### Q: 実際のデータベースに接続しているか確認するには？

A: テスト実行時にデータベース接続は発生しません。すべてモックで処理されます。

### Q: 複雑なクエリ（include, select等）はどうテストする？

A: 同じ方法で、モックの戻り値に必要なデータ構造を設定します：

```typescript
prismaMock.mST_User.findUnique.mockResolvedValue({
  ...mockUser,
  profile: { ... },  // include: { profile: true } の結果
})
```

## 📚 参考資料

- [Jest公式ドキュメント](https://jestjs.io/)
- [jest-mock-extended](https://github.com/marchaos/jest-mock-extended)
- [Prisma Testing Guide](https://www.prisma.io/docs/guides/testing/unit-testing)
- プロジェクト内: `docs/testing/03_ユニットテスト実装ガイド.md`

## 🎓 次のステップ

このサンプルを理解したら、以下を試してみてください：

1. **既存のサービスにテストを追加**
   - `careerGoalService.ts`のテストを作成
   - より複雑なビジネスロジックをテスト

2. **APIルートのテスト**
   - `src/app/api/`配下のRoute Handlersをテスト
   - NextRequestとNextResponseのモック

3. **カバレッジ目標の達成**
   - 80%以上のカバレッジを目指す
   - カバレッジレポートを確認: `npm test -- --coverage`

---

Happy Testing! 🚀
