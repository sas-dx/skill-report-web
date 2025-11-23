# テストスタイルガイド - 実装方針

このドキュメントは、[テストフレームワークアーキテクチャ](./TEST-FRAMEWORK-ARCHITECTURE.md)で定義された上位概念を、具体的な実装方針に落とし込んだものです。

---

## 📋 目次

1. [ファイル構成規則](#ファイル構成規則)
2. [命名規則](#命名規則)
3. [テストパターン](#テストパターン)
4. [実装例](#実装例)
5. [アンチパターン](#アンチパターン)

---

## 📂 ファイル構成規則

### 1. テストファイルの配置

#### パターンA: `__tests__` ディレクトリ（推奨）
```
src/
├── lib/
│   └── services/
│       ├── user.service.ts
│       └── __tests__/
│           └── user.service.test.ts    ← ここに配置
```

**利点**:
- テストファイルが明確に分離される
- ディレクトリ構造がクリーン
- カバレッジ集計が容易

#### パターンB: 並列配置
```
src/
├── components/
│   ├── CareerGoalForm.tsx
│   └── CareerGoalForm.test.tsx         ← 並列に配置
```

**利点**:
- ファイルが近接している
- インポートパスが短い

**使い分け**:
- **API Routes**: パターンA（`__tests__`）
- **Services**: パターンA（`__tests__`）
- **Components**: パターンB（並列配置）
- **Utils/Helpers**: パターンA（`__tests__`）

### 2. テストファイル名

**命名パターン**:
```
[対象ファイル名].test.[ts|tsx]
[対象ファイル名].spec.[ts|tsx]
```

**例**:
```
user.service.ts      → user.service.test.ts
CareerGoalForm.tsx   → CareerGoalForm.test.tsx
route.ts             → route.test.ts
```

---

## 🏷️ 命名規則

### 1. describe ブロック

**API Route テスト**:
```typescript
describe('API-[ID]: [API名称]', () => {
  describe('[HTTPメソッド] [エンドポイント]', () => {
    // ...
  });
});

// 例
describe('API-700: キャリア初期データ取得API', () => {
  describe('GET /api/career/init', () => {
    // ...
  });
});
```

**Service/Utils テスト**:
```typescript
describe('[機能名/クラス名]', () => {
  describe('[メソッド名]', () => {
    // ...
  });
});

// 例
describe('ユーザーサービス', () => {
  describe('getUserById', () => {
    // ...
  });
});
```

**Component テスト**:
```typescript
describe('<ComponentName />', () => {
  describe('[機能/振る舞い]', () => {
    // ...
  });
});

// 例
describe('<CareerGoalForm />', () => {
  describe('フォーム送信', () => {
    // ...
  });
});
```

### 2. test/it ブロック

**基本パターン**（英語）:
```typescript
test('should [期待する動作] when [条件]', () => {
  // ...
});

it('should [期待する動作] when [条件]', () => {
  // ...
});
```

**例**:
```typescript
test('should return user data when user exists', () => {});
test('should throw error when user not found', () => {});
test('should create user when valid data provided', () => {});
```

**日本語パターン**（プロジェクト標準）:
```typescript
test('[期待する結果]', () => {
  // ...
});
```

**例**:
```typescript
test('ユーザーが存在する場合、ユーザー情報を返す', () => {});
test('ユーザーが存在しない場合、nullを返す', () => {});
test('有効なデータで新しいユーザーを作成できる', () => {});
```

### 3. テストカテゴリ分け

```typescript
describe('GET /api/users', () => {
  describe('正常系', () => {
    test('ユーザー一覧を取得できること', () => {});
  });

  describe('異常系', () => {
    test('認証エラーの場合、401を返すこと', () => {});
  });

  describe('エッジケース', () => {
    test('ユーザーが0件の場合、空配列を返すこと', () => {});
  });

  describe('パフォーマンステスト', () => {
    test('レスポンス時間が1秒以内であること', () => {});
  });
});
```

---

## 🎯 テストパターン

### パターン1: API Route テスト

**標準テンプレート**:

```typescript
import { prismaMock } from '@/__mocks__/prisma';
import { createAuthenticatedRequest } from '@/__tests__/helpers/nextRequest.helper';
import { expectCompleteSuccessResponse } from '@/__tests__/helpers/apiResponse.helper';
import { createMockUser } from '@/__tests__/helpers/prismaFactories';

// 動的インポート
async function importGETFunction() {
  const module = await import('./route');
  return module.GET;
}

describe('API-XXX: [API名]', () => {
  describe('GET /api/xxx', () => {
    beforeEach(() => {
      // モックデータのセットアップ
      prismaMock.user.findMany.mockResolvedValue([
        createMockUser() as any,
      ]);
    });

    describe('正常系', () => {
      test('データを正常に取得できること', async () => {
        // Arrange
        const GET = await importGETFunction();
        const request = createAuthenticatedRequest('emp_001');

        // Act
        const response = await GET(request);

        // Assert
        const data = await expectCompleteSuccessResponse(response, ['users']);
        expect(data.data.users).toHaveLength(1);
      });
    });

    describe('異常系', () => {
      test('認証エラーの場合、401を返すこと', async () => {
        // Arrange
        const GET = await importGETFunction();
        const request = createAuthenticatedRequest(''); // 空のユーザーID

        // Act
        const response = await GET(request);

        // Assert
        const { status, data } = await getResponseData(response);
        expectUnauthorizedResponse(response, data);
      });
    });
  });
});
```

### パターン2: Service テスト

**標準テンプレート**:

```typescript
import { prismaMock } from '@/__mocks__/prisma';
import { createMockUser } from '@/__tests__/helpers/prismaFactories';
import { getUserById, createUser } from '../user.service';

describe('ユーザーサービス', () => {
  describe('getUserById', () => {
    test('ユーザーが存在する場合、ユーザー情報を返す', async () => {
      // Arrange
      const mockUser = createMockUser();
      prismaMock.mST_User.findUnique.mockResolvedValue(mockUser);

      // Act
      const result = await getUserById(1);

      // Assert
      expect(result).toEqual(mockUser);
      expect(prismaMock.mST_User.findUnique).toHaveBeenCalledWith({
        where: { user_id: 1 },
      });
    });

    test('ユーザーが存在しない場合、nullを返す', async () => {
      // Arrange
      prismaMock.mST_User.findUnique.mockResolvedValue(null);

      // Act
      const result = await getUserById(999);

      // Assert
      expect(result).toBeNull();
    });

    test('データベースエラーが発生した場合、エラーをスローする', async () => {
      // Arrange
      const dbError = new Error('Database connection failed');
      prismaMock.mST_User.findUnique.mockRejectedValue(dbError);

      // Act & Assert
      await expect(getUserById(1)).rejects.toThrow('Database connection failed');
    });
  });
});
```

### パターン3: Component テスト

**標準テンプレート**:

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { CareerGoalForm } from '../CareerGoalForm';

describe('<CareerGoalForm />', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  describe('レンダリング', () => {
    test('フォームが正しく表示されること', () => {
      // Arrange & Act
      render(<CareerGoalForm onSubmit={mockOnSubmit} />);

      // Assert
      expect(screen.getByLabelText('目標設定日')).toBeInTheDocument();
      expect(screen.getByLabelText('目標内容')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: '保存' })).toBeInTheDocument();
    });
  });

  describe('フォーム送信', () => {
    test('有効なデータで送信できること', async () => {
      // Arrange
      const user = userEvent.setup();
      render(<CareerGoalForm onSubmit={mockOnSubmit} />);

      // Act
      await user.type(screen.getByLabelText('目標内容'), 'テスト目標');
      await user.click(screen.getByRole('button', { name: '保存' }));

      // Assert
      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith({
          description: 'テスト目標',
        });
      });
    });

    test('バリデーションエラーが表示されること', async () => {
      // Arrange
      const user = userEvent.setup();
      render(<CareerGoalForm onSubmit={mockOnSubmit} />);

      // Act - 何も入力せずに送信
      await user.click(screen.getByRole('button', { name: '保存' }));

      // Assert
      expect(await screen.findByText('目標内容は必須です')).toBeInTheDocument();
      expect(mockOnSubmit).not.toHaveBeenCalled();
    });
  });
});
```

---

## 📐 実装例

### 例1: データ作成API（POST）のテスト

```typescript
import { createAuthenticatedRequest } from '@/__tests__/helpers/nextRequest.helper';
import { expectCreatedResponse } from '@/__tests__/helpers/apiResponse.helper';
import { createMockCareerPlan } from '@/__tests__/helpers/prismaFactories';

describe('POST /api/career-goals', () => {
  test('キャリア目標を作成できること', async () => {
    // Arrange
    const newGoal = {
      target_position_id: 'pos_001',
      target_date: '2027-12-31',
      description: '新しい目標',
    };
    const createdGoal = createMockCareerPlan(newGoal);
    prismaMock.careerPlan.create.mockResolvedValue(createdGoal as any);

    const POST = await import('./route').then(m => m.POST);
    const request = createAuthenticatedRequest('emp_001', {
      'content-type': 'application/json',
    });

    // Request bodyのモック
    (request as any).json = jest.fn().mockResolvedValue(newGoal);

    // Act
    const response = await POST(request);

    // Assert
    const data = await expectCreatedResponse(response, [
      'plan_id',
      'target_position_id',
      'target_date',
    ]);

    expect(data.data.target_position_id).toBe('pos_001');
    expect(prismaMock.careerPlan.create).toHaveBeenCalledWith({
      data: expect.objectContaining({
        employee_id: 'emp_001',
        target_position_id: 'pos_001',
      }),
    });
  });
});
```

### 例2: データ更新API（PUT）のテスト

```typescript
describe('PUT /api/career-goals/[id]', () => {
  test('キャリア目標を更新できること', async () => {
    // Arrange
    const updateData = { progress_percentage: 75.0 };
    const updatedGoal = createMockCareerPlan({
      plan_id: 'plan_001',
      progress_percentage: 75.0,
    });
    prismaMock.careerPlan.update.mockResolvedValue(updatedGoal as any);

    const PUT = await import('./route').then(m => m.PUT);
    const request = createAuthenticatedRequest('emp_001');
    (request as any).json = jest.fn().mockResolvedValue(updateData);

    // Act
    const response = await PUT(request, { params: { id: 'plan_001' } });

    // Assert
    const data = await expectUpdatedResponse(response);
    expect(data.data.progress_percentage).toBe(75.0);
  });
});
```

### 例3: パラメータ化テスト（Data-Driven）

```typescript
describe('データ型バリデーション', () => {
  test.each([
    { input: 0, expected: true },
    { input: 50, expected: true },
    { input: 100, expected: true },
    { input: -1, expected: false },
    { input: 101, expected: false },
  ])('progress_percentage=$input の場合、valid=$expected', ({ input, expected }) => {
    // Arrange
    const result = validateProgressPercentage(input);

    // Assert
    expect(result).toBe(expected);
  });
});
```

### 例4: 非同期エラーハンドリング

```typescript
describe('エラーハンドリング', () => {
  test('データベースエラー時、500を返すこと', async () => {
    // Arrange
    prismaMock.careerPlan.findMany.mockRejectedValue(
      new Error('Database connection failed')
    );

    const GET = await importGETFunction();
    const request = createAuthenticatedRequest('emp_001');

    // Act
    const response = await GET(request);

    // Assert
    const { status, data } = await getResponseData(response);
    expectServerErrorResponse(response, data);
    expect(data.error).toContain('Database');
  });
});
```

---

## ❌ アンチパターン

### アンチパターン1: 重複したモックセットアップ

**❌ 悪い例**:
```typescript
test('test 1', () => {
  prismaMock.user.findMany.mockResolvedValue([
    {
      user_id: 1,
      employee_id: 'EMP001',
      name: 'テストユーザー',
      email: 'test@example.com',
      // ... 20行のフィールド
    }
  ]);
});

test('test 2', () => {
  prismaMock.user.findMany.mockResolvedValue([
    {
      user_id: 1,
      employee_id: 'EMP001',
      name: 'テストユーザー',
      email: 'test@example.com',
      // ... 同じ20行を繰り返し
    }
  ]);
});
```

**✅ 良い例**:
```typescript
beforeEach(() => {
  prismaMock.user.findMany.mockResolvedValue([
    createMockUser() as any,  // ファクトリを使用
  ]);
});

test('test 1', () => {
  // モックは既にセットアップ済み
});

test('test 2', () => {
  // モックは既にセットアップ済み
});
```

### アンチパターン2: 曖昧なアサーション

**❌ 悪い例**:
```typescript
test('データを取得できる', async () => {
  const result = await getUsers();
  expect(result).toBeTruthy();  // 何でもOKになってしまう
});
```

**✅ 良い例**:
```typescript
test('ユーザー一覧を取得できる', async () => {
  const result = await getUsers();

  expect(result).toHaveLength(1);
  expect(result[0]).toHaveProperty('user_id');
  expect(result[0]).toHaveProperty('name');
  expect(result[0].name).toBe('テストユーザー');
});
```

### アンチパターン3: テスト間の依存関係

**❌ 悪い例**:
```typescript
let userId: number;

test('ユーザーを作成', async () => {
  const user = await createUser({ name: 'Test' });
  userId = user.id;  // グローバル変数に保存
});

test('ユーザーを取得', async () => {
  const user = await getUser(userId);  // 前のテストに依存
  expect(user).toBeDefined();
});
```

**✅ 良い例**:
```typescript
test('ユーザーを作成', async () => {
  const user = await createUser({ name: 'Test' });
  expect(user.id).toBeDefined();
});

test('ユーザーを取得', async () => {
  // 独立したセットアップ
  const mockUser = createMockUser();
  prismaMock.user.findUnique.mockResolvedValue(mockUser);

  const user = await getUser(1);
  expect(user).toEqual(mockUser);
});
```

### アンチパターン4: 過度なモック

**❌ 悪い例**:
```typescript
test('ユーティリティ関数のテスト', () => {
  const mockDate = jest.fn();
  const mockMath = jest.fn();
  const mockString = jest.fn();
  // ... 全てをモック化
});
```

**✅ 良い例**:
```typescript
test('ユーティリティ関数のテスト', () => {
  // 外部依存のみモック化（DB、API等）
  // 純粋関数はそのままテスト
  const result = formatDate('2024-01-01');
  expect(result).toBe('2024年1月1日');
});
```

### アンチパターン5: 不適切なdescribeネスト

**❌ 悪い例**:
```typescript
describe('Users', () => {
  describe('GET', () => {
    describe('Success', () => {
      describe('With valid ID', () => {
        describe('When user exists', () => {
          test('returns user', () => {});  // ネストが深すぎる
        });
      });
    });
  });
});
```

**✅ 良い例**:
```typescript
describe('Users', () => {
  describe('GET /api/users/:id', () => {
    describe('正常系', () => {
      test('ユーザーが存在する場合、ユーザー情報を返す', () => {});
    });
  });
});
```

---

## 🔍 コードレビューチェックリスト

### 基本項目
- [ ] テストファイルが適切な場所に配置されている
- [ ] 命名規則に従っている
- [ ] AAA パターン（Arrange-Act-Assert）を使用している
- [ ] ヘルパー関数/ファクトリを活用している

### テスト品質
- [ ] テストの意図が明確
- [ ] エッジケースがカバーされている
- [ ] エラーケースがテストされている
- [ ] アサーションが具体的

### 保守性
- [ ] 重複コードがない（DRY原則）
- [ ] テストが独立している（他のテストに依存しない）
- [ ] モックが適切にリセットされている
- [ ] マジックナンバー/文字列を避けている

### パフォーマンス
- [ ] 不要な非同期待機がない
- [ ] 過度なモック化を避けている
- [ ] テスト実行時間が妥当

---

## 📚 参考資料

- [Jest 公式ドキュメント](https://jestjs.io/)
- [Testing Library ベストプラクティス](https://testing-library.com/docs/queries/about)
- [Effective Software Testing](https://www.effective-software-testing.com/)

---

**最終更新**: 2025-11-23
**バージョン**: 1.0.0
**メンテナー**: システム開発チーム
