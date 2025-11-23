# ユニットテスト統合フレームワーク - アーキテクチャ設計書

## 📐 上位概念定義

### 1. フレームワークのビジョン

**ビジョンステートメント**:
> 開発者が自信を持ってコードを変更でき、品質を保証しながら開発速度を最大化する、
> 保守可能で拡張可能な統合テストエコシステムを構築する

### 2. フレームワークの4大原則

#### 2.1 **一貫性（Consistency）**
- 全てのテストが同じパターンとベストプラクティスに従う
- 命名規則、ディレクトリ構造、テストスタイルの統一
- 学習曲線の最小化

#### 2.2 **再利用性（Reusability）**
- DRY原則の徹底（Don't Repeat Yourself）
- ヘルパー関数とファクトリパターンによるコードの共通化
- テストデータとモックの集中管理

#### 2.3 **保守性（Maintainability）**
- 変更に強いテストコード
- 明確な責任分離（Separation of Concerns）
- ドキュメント化された設計パターン

#### 2.4 **拡張性（Scalability）**
- 新機能追加時のテスト作成コストの最小化
- プロジェクト成長に対応できるアーキテクチャ
- 複数チームでの協調作業をサポート

---

## 🏗️ アーキテクチャレイヤー

### レイヤー構成図

```
┌─────────────────────────────────────────────────────────────┐
│                     L5: CI/CD & Reports                     │
│              (GitHub Actions, Coverage Reports)             │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                  L4: Test Orchestration                     │
│         (Test Suites, Describe Blocks, Lifecycle)           │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                  L3: Domain Test Logic                      │
│       (Business Logic Tests, Integration Tests)             │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                  L2: Test Utilities Layer                   │
│  ┌──────────────┬───────────────┬────────────────────────┐  │
│  │  Helpers     │   Factories   │  Assertion Helpers     │  │
│  │ (Request,    │  (Prisma,     │  (API Response,        │  │
│  │  Response)   │   Domain)     │   Data Validation)     │  │
│  └──────────────┴───────────────┴────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
┌─────────────────────────────────────────────────────────────┐
│                  L1: Test Foundation Layer                  │
│  ┌──────────────┬───────────────┬────────────────────────┐  │
│  │   Jest       │ Mock Systems  │  Test Config           │  │
│  │  (Runner,    │  (Prisma,     │  (jest.config.js,      │  │
│  │   Matchers)  │   MSW)        │   setupFiles)          │  │
│  └──────────────┴───────────────┴────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📦 レイヤー詳細定義

### L1: Test Foundation Layer（テスト基盤レイヤー）

**責務**: テストランナーとモックシステムの基盤を提供

**コンポーネント**:
- **Jest Core**: テストランナー、アサーション、ライフサイクル管理
- **Mock Systems**:
  - `jest-mock-extended`: Prisma型安全モック
  - `MSW`: HTTP/APIモック
  - `@testing-library`: React DOMモック
- **Configuration**: `jest.config.js`, `jest.setup.js`

**設計方針**:
```typescript
// jest.config.js の設計原則
{
  // 1. 明確なテスト対象の定義
  testMatch: ['**/__tests__/**/*.test.[jt]s?(x)', '**/?(*.)+(spec|test).[jt]s?(x)'],

  // 2. カバレッジ除外の明示
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/__tests__/**',      // テストコード自体は除外
    '!src/__mocks__/**',      // モックは除外
  ],

  // 3. 品質ゲートの設定
  coverageThreshold: {
    global: { statements: 80, branches: 80, functions: 80, lines: 80 }
  }
}
```

---

### L2: Test Utilities Layer（テストユーティリティレイヤー）

**責務**: 再利用可能なテストユーティリティの提供

**コンポーネント**:

#### 2.1 Request Helpers (`nextRequest.helper.ts`)
```typescript
// 設計パターン: Factory Pattern
// 目的: NextRequestの複雑な生成ロジックを隠蔽

createMockNextRequest()        // 汎用リクエスト生成
createAuthenticatedRequest()   // 認証付きリクエスト生成
createMultipartRequest()       // マルチパートリクエスト生成（将来実装）
```

#### 2.2 Response Helpers (`apiResponse.helper.ts`)
```typescript
// 設計パターン: Assertion Builder Pattern
// 目的: レスポンス検証の標準化と簡素化

// 成功系
expectCompleteSuccessResponse()  // 完全な成功レスポンス検証
expectCreatedResponse()          // 201 Created
expectUpdatedResponse()          // 200 OK (更新)

// エラー系
expectValidationErrorResponse()  // 400 Bad Request
expectUnauthorizedResponse()     // 401 Unauthorized
expectNotFoundResponse()         // 404 Not Found

// データ構造検証
expectArrayResponse()            // 配列レスポンス
expectPaginatedResponse()        // ページネーション
```

#### 2.3 Data Factories (`prismaFactories.ts`)
```typescript
// 設計パターン: Builder Pattern + Factory Pattern
// 目的: 一貫したテストデータの生成

// 単一データ生成
createMockCareerPlan(overrides?)
createMockEmployee(overrides?)
createMockSkill(overrides?)

// 複数データ生成（スケーラビリティ対応）
createMockCareerPlans(count, baseOverrides?)
createMockEmployees(count, baseOverrides?)
createMockSkills(count, baseOverrides?)
```

**設計原則**:
1. **Single Responsibility**: 各ヘルパーは1つの責務のみを持つ
2. **Composition over Inheritance**: 継承ではなく合成で機能を拡張
3. **Immutability**: ファクトリは常に新しいオブジェクトを返す
4. **Type Safety**: TypeScriptの型システムを最大限活用

---

### L3: Domain Test Logic（ドメインテストロジックレイヤー）

**責務**: ビジネスロジックとドメイン固有のテストを実装

**テストカテゴリ**:

#### 3.1 Unit Tests（単体テスト）
```
src/
├── lib/
│   └── services/
│       └── __tests__/
│           ├── user.service.test.ts          # サービス層テスト
│           └── careerGoal.service.test.ts
├── utils/
│   └── __tests__/
│       └── validation.test.ts                # ユーティリティテスト
```

**テストパターン**:
- **AAA Pattern**: Arrange → Act → Assert
- **Given-When-Then**: BDD スタイル
- **Data-Driven Tests**: パラメータ化テスト

#### 3.2 Integration Tests（統合テスト）
```
src/app/api/
└── career/
    └── init/
        └── route.test.ts                     # API Route統合テスト
```

**テストスコープ**:
- Route Handler + Prisma連携
- 認証・認可フロー
- エラーハンドリング
- データ変換ロジック

#### 3.3 Component Tests（コンポーネントテスト）
```
src/components/
└── __tests__/
    ├── CareerGoalForm.test.tsx               # フォームコンポーネント
    └── SkillMatrix.test.tsx                  # 表示コンポーネント
```

**テストアプローチ**:
- ユーザー視点のテスト（@testing-library/react）
- アクセシビリティテスト
- インタラクションテスト

---

### L4: Test Orchestration Layer（テストオーケストレーションレイヤー）

**責務**: テストの構造化と実行フローの制御

**テスト構造パターン**:

```typescript
describe('[Feature/Component Name]', () => {
  // Setup - ファクトリとヘルパーを活用
  beforeEach(() => {
    prismaMock.user.findMany.mockResolvedValue([createMockUser()]);
  });

  // 正常系テスト
  describe('正常系', () => {
    test('should ... when ...', async () => {
      // Arrange
      const request = createAuthenticatedRequest('emp_001');

      // Act
      const response = await GET(request);

      // Assert
      await expectCompleteSuccessResponse(response, ['data']);
    });
  });

  // 異常系テスト
  describe('異常系', () => {
    test('should return 400 when validation fails', async () => {
      // ...
    });
  });

  // エッジケーステスト
  describe('エッジケース', () => {
    test('should handle empty array', async () => {
      // ...
    });
  });
});
```

**命名規則**:
- **describe**: 日本語可（機能名/コンポーネント名）
- **test/it**: `should [期待する動作] when [条件]`
- **変数**: 意図を明確にする名前（`mockUser`, `validRequest`, `expectedResponse`）

---

### L5: CI/CD & Reports Layer（CI/CD & レポートレイヤー）

**責務**: 自動化されたテスト実行と品質レポート

**GitHub Actions ワークフロー**:

```yaml
# .github/workflows/test.yml
name: Test and Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run type check
        run: npm run type-check

      - name: Run tests with coverage
        run: npm test -- --coverage

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
```

**品質ゲート**:
1. **Type Safety**: TypeScript型チェック必須
2. **Test Success**: 全テストが合格
3. **Coverage Threshold**: 80%以上（段階的に引き上げ）
4. **No Regressions**: カバレッジ低下を検知

---

## 🎯 実装方針

### Phase 1: Foundation（基盤整備）✅ 完了

- [x] Jest 29.7.0 セットアップ
- [x] Prisma モックシステム構築（jest-mock-extended）
- [x] 基本的なヘルパー関数実装
- [x] 初期ファクトリ実装（4モデル）

### Phase 2: Expansion（拡張）✅ 完了

- [x] APIレスポンス検証ヘルパー実装
- [x] 追加ファクトリ実装（10モデル）
- [x] 既存テストのリファクタリング
- [x] ドキュメント整備

### Phase 3: Standardization（標準化）🔄 進行中

- [ ] テストスタイルガイドの作成
- [ ] テンプレートファイルの作成
  - [ ] API Route テストテンプレート
  - [ ] Service テストテンプレート
  - [ ] Component テストテンプレート
- [ ] ESLint/Prettier ルールの統一

### Phase 4: Automation（自動化）📋 計画中

- [ ] テストコード自動生成ツール
- [ ] カバレッジレポートの可視化
- [ ] パフォーマンステストの統合
- [ ] E2Eテストフレームワーク統合（Playwright）

---

## 📐 設計パターンカタログ

### 1. AAA Pattern（Arrange-Act-Assert）

**適用対象**: 全てのユニットテスト

```typescript
test('should create user with valid data', async () => {
  // Arrange - テストデータの準備
  const userData = createMockUser({ name: '新規ユーザー' });
  prismaMock.user.create.mockResolvedValue(userData);

  // Act - 対象関数の実行
  const result = await createUser(userData);

  // Assert - 結果の検証
  expect(result).toEqual(userData);
  expect(prismaMock.user.create).toHaveBeenCalledWith({
    data: userData,
  });
});
```

### 2. Builder Pattern（ビルダーパターン）

**適用対象**: 複雑なテストデータ生成

```typescript
// 将来的な拡張例
class CareerPlanBuilder {
  private data: Partial<CareerPlan> = {};

  withEmployee(employeeId: string) {
    this.data.employee_id = employeeId;
    return this;
  }

  withStatus(status: string) {
    this.data.plan_status = status;
    return this;
  }

  build(): CareerPlan {
    return createMockCareerPlan(this.data);
  }
}

// 使用例
const careerPlan = new CareerPlanBuilder()
  .withEmployee('emp_001')
  .withStatus('ACTIVE')
  .build();
```

### 3. Test Data Builders（テストデータビルダー）

**適用対象**: 関連データの一括生成

```typescript
// src/__tests__/builders/careerPlanScenario.builder.ts（将来実装）
export function createCareerPlanScenario() {
  const employee = createMockEmployee();
  const skills = createMockSkills(5);
  const careerPlan = createMockCareerPlan({
    employee_id: employee.employee_code,
  });

  return { employee, skills, careerPlan };
}
```

### 4. Object Mother Pattern（オブジェクトマザーパターン）

**適用対象**: よく使われる典型的なテストオブジェクト

```typescript
// src/__tests__/mothers/user.mother.ts（将来実装）
export class UserMother {
  static juniorEngineer() {
    return createMockEmployee({
      position_id: 'pos_junior',
      employment_type: 'FULL_TIME',
    });
  }

  static seniorEngineer() {
    return createMockEmployee({
      position_id: 'pos_senior',
      employment_type: 'FULL_TIME',
    });
  }

  static manager() {
    return createMockEmployee({
      position_id: 'pos_manager',
      employment_type: 'FULL_TIME',
    });
  }
}
```

---

## 🔄 テストライフサイクル管理

### セットアップとティアダウン

```typescript
describe('Test Suite', () => {
  // 全テスト実行前に1回だけ実行
  beforeAll(async () => {
    // 重い初期化処理（DBコネクション等）
  });

  // 各テスト実行前に毎回実行
  beforeEach(() => {
    // モックのリセット（jest.setup.jsで自動化済み）
    // テストデータの準備
  });

  // 各テスト実行後に毎回実行
  afterEach(() => {
    // クリーンアップ処理
  });

  // 全テスト実行後に1回だけ実行
  afterAll(async () => {
    // リソースの解放
  });
});
```

---

## 📊 品質メトリクス

### カバレッジ目標

| フェーズ | ステートメント | ブランチ | 関数 | 行 |
|---------|--------------|---------|------|-----|
| Phase 1 | 30% | 30% | 30% | 30% |
| Phase 2 | 50% | 50% | 50% | 50% |
| Phase 3 | 70% | 70% | 70% | 70% |
| **Phase 4（目標）** | **80%** | **80%** | **80%** | **80%** |

### テスト実行時間目標

- **Unit Tests**: < 10秒（全体）
- **Integration Tests**: < 30秒（全体）
- **E2E Tests**: < 5分（全体）

---

## 🛠️ 開発者ガイドライン

### 新規テスト作成時のチェックリスト

- [ ] 適切なレイヤーにテストファイルを配置
- [ ] ヘルパー関数を活用（Request/Response/Factory）
- [ ] AAA パターンに従う
- [ ] 明確なテスト名を付ける（`should ... when ...`）
- [ ] エッジケースを含める
- [ ] モックを適切にリセット（beforeEach）
- [ ] アサーションは具体的かつ明確に

### コードレビュー時の確認ポイント

- [ ] テストの意図が明確か
- [ ] 重複コードがないか（DRY原則）
- [ ] 適切なヘルパー/ファクトリを使用しているか
- [ ] カバレッジが維持または向上しているか
- [ ] テストが独立して実行可能か

---

## 📚 関連ドキュメント

- [Jest セットアップガイド](./JEST-SETUP.md)
- [Prisma モッキングガイド](./PRISMA-MOCKING.md)
- [MSW ハンドラーガイド](./MSW-HANDLERS.md)
- [ヘルパー関数使用ガイド](../../src/__tests__/helpers/README.md)
- [CI/CD セットアップ](./CI-CD-SETUP.md)

---

**最終更新**: 2025-11-23
**バージョン**: 1.0.0
**メンテナー**: システム開発チーム
