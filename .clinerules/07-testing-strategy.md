# テスト戦略・品質保証

## 基本方針

### 1. テストピラミッド戦略
- **ユニットテスト（70%）**: 個別コンポーネント・関数の動作検証
- **統合テスト（20%）**: コンポーネント間・API連携の検証
- **E2Eテスト（10%）**: ユーザーシナリオに基づく全体動作検証

### 2. 品質保証の原則
- **シフトレフト**: 開発初期段階での品質確保
- **自動化優先**: 手動テストの最小化と自動化の推進
- **継続的テスト**: CI/CDパイプラインでの自動テスト実行

## テストレベル別戦略

### 1. ユニットテスト

#### 対象・範囲
- **フロントエンド**: コンポーネント、ユーティリティ関数、状態管理
- **バックエンド**: API関数、ビジネスロジック、データアクセス層
- **共通**: バリデーション、計算ロジック、変換処理

#### テスト観点
- **機能性**: 正常系・異常系の動作確認
- **境界値**: 入力値の境界条件テスト
- **例外処理**: エラーハンドリングの検証

#### 実装方針
```javascript
// 良い例（包括的なユニットテスト）
describe('SkillValidation', () => {
  describe('validateSkillLevel', () => {
    it('should return true for valid skill levels (1-4)', () => {
      expect(validateSkillLevel(1)).toBe(true);
      expect(validateSkillLevel(4)).toBe(true);
    });

    it('should return false for invalid skill levels', () => {
      expect(validateSkillLevel(0)).toBe(false);
      expect(validateSkillLevel(5)).toBe(false);
      expect(validateSkillLevel(null)).toBe(false);
    });

    it('should handle edge cases', () => {
      expect(validateSkillLevel('1')).toBe(false); // 文字列
      expect(validateSkillLevel(1.5)).toBe(false); // 小数
    });
  });
});
```

### 2. 統合テスト

#### 対象・範囲
- **API統合**: フロントエンド ↔ バックエンドAPI
- **データベース統合**: API ↔ データベース
- **外部システム統合**: 人事システム、SSO等

#### テスト観点
- **データフロー**: 正しいデータの受け渡し
- **エラー伝播**: エラーの適切な処理・通知
- **パフォーマンス**: レスポンス時間の確認

#### 実装方針
```javascript
// API統合テストの例
describe('Skill API Integration', () => {
  beforeEach(async () => {
    await setupTestDatabase();
  });

  afterEach(async () => {
    await cleanupTestDatabase();
  });

  it('should create and retrieve skill record', async () => {
    // スキル作成
    const createResponse = await request(app)
      .post('/api/skills')
      .send({
        emp_no: 'EMP001',
        skill_id: 'SKL001',
        level: 3
      })
      .expect(201);

    // 作成されたスキルの取得
    const getResponse = await request(app)
      .get(`/api/skills/${createResponse.body.id}`)
      .expect(200);

    expect(getResponse.body.level).toBe(3);
  });
});
```

### 3. E2Eテスト

#### 対象・範囲
- **主要ユーザーシナリオ**: ログイン→スキル入力→保存→検索
- **クリティカルパス**: 認証、権限管理、データ保存
- **ブラウザ互換性**: Chrome、Edge、Safari

#### テスト観点
- **ユーザビリティ**: 実際の操作フローの確認
- **レスポンシブ**: 各デバイスサイズでの動作
- **アクセシビリティ**: キーボード操作、スクリーンリーダー

#### 実装方針
```javascript
// Playwright E2Eテストの例
test('スキル情報の登録・検索フロー', async ({ page }) => {
  // ログイン
  await page.goto('/login');
  await page.fill('[data-testid="user-id"]', 'test.user');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-button"]');

  // スキル情報画面へ遷移
  await page.click('[data-testid="skill-menu"]');
  await expect(page).toHaveURL('/skills');

  // スキル情報入力
  await page.selectOption('[data-testid="skill-category"]', 'JavaScript');
  await page.selectOption('[data-testid="skill-level"]', '3');
  await page.click('[data-testid="save-button"]');

  // 保存確認
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();

  // スキル検索で確認
  await page.goto('/skills/search');
  await page.fill('[data-testid="search-keyword"]', 'JavaScript');
  await page.click('[data-testid="search-button"]');
  
  await expect(page.locator('[data-testid="search-results"]')).toContainText('test.user');
});
```

## 要求仕様ID別テスト戦略

### 最高優先度（PLT.1-WEB.1, PRO.1-BASE.1, SKL.1-HIER.1）

#### テスト内容
- **認証・認可**: ログイン、権限チェック、セッション管理
- **基本情報管理**: CRUD操作、バリデーション、履歴管理
- **スキル階層**: 3階層構造、4段階評価、検索機能

#### テストケース例
```gherkin
Feature: スキル階層管理
  Scenario: 管理者がスキル項目を追加する
    Given 管理者としてログインしている
    When スキルマスタ管理画面を開く
    And 新規スキル項目「React.js」を「フロントエンド」カテゴリに追加する
    Then スキル項目が正常に保存される
    And スキル選択肢に「React.js」が表示される
```

### 高優先度（ACC.1-ROLE.1, SKL.1-EVAL.1, SKL.1-SRCH.1）

#### テスト内容
- **権限管理**: ロール作成・編集・削除、権限付与・変更
- **スキル評価**: 4段階評価の入力・表示・集計
- **スキル検索**: 条件指定、結果表示、パフォーマンス

### 中優先度（CAR.1-PLAN.1, WPM.1-DET.1, TRN.1-ATT.1）

#### テスト内容
- **目標管理**: 目標設定・進捗入力・評価
- **作業実績**: 案件情報入力・技術要素管理
- **研修管理**: 参加記録・PDU計算

### 低優先度（WPM.1-BULK.1, RPT.1-EXCEL.1, RPT.2-VIS.1）

#### テスト内容
- **一括処理**: CSV/Excelインポート・エラーハンドリング
- **帳票出力**: Excel/PDF生成・ダウンロード
- **可視化**: スキルマップ・ヒートマップ表示

## 非機能テスト

### 1. パフォーマンステスト

#### 目標値
- **レスポンス時間**: API〜UI まで1秒以内
- **同時接続数**: 100ユーザー同時利用可能
- **スループット**: 1000リクエスト/分

#### テスト方法
```javascript
// JMeterまたはk6を使用したパフォーマンステスト
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 10 }, // 10ユーザーまで増加
    { duration: '5m', target: 50 }, // 50ユーザーで維持
    { duration: '2m', target: 100 }, // 100ユーザーまで増加
    { duration: '5m', target: 100 }, // 100ユーザーで維持
    { duration: '2m', target: 0 }, // 0まで減少
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'], // 95%のリクエストが1秒以内
  },
};

export default function() {
  let response = http.get('https://api.example.com/skills');
  check(response, {
    'status is 200': (r) => r.status === 200,
    'response time < 1s': (r) => r.timings.duration < 1000,
  });
  sleep(1);
}
```

### 2. セキュリティテスト

#### テスト観点
- **認証・認可**: 不正アクセス、権限昇格
- **入力検証**: SQLインジェクション、XSS
- **データ保護**: 暗号化、機密情報漏洩

#### テスト方法
```javascript
// セキュリティテストの例
describe('Security Tests', () => {
  it('should prevent SQL injection', async () => {
    const maliciousInput = "'; DROP TABLE users; --";
    const response = await request(app)
      .get(`/api/skills/search?keyword=${maliciousInput}`)
      .expect(400); // バリデーションエラー
  });

  it('should prevent XSS attacks', async () => {
    const xssPayload = '<script>alert("XSS")</script>';
    const response = await request(app)
      .post('/api/skills')
      .send({ skill_name: xssPayload })
      .expect(400); // サニタイズエラー
  });

  it('should require authentication for protected endpoints', async () => {
    await request(app)
      .get('/api/admin/users')
      .expect(401); // 認証エラー
  });
});
```

### 3. アクセシビリティテスト

#### テスト観点
- **WCAG 2.1 AA準拠**: コントラスト、キーボード操作
- **スクリーンリーダー対応**: ARIAラベル、セマンティックHTML
- **操作性**: 3ステップ以内での目的画面到達

#### テスト方法
```javascript
// axe-coreを使用したアクセシビリティテスト
import { injectAxe, checkA11y } from 'axe-playwright';

test('アクセシビリティチェック', async ({ page }) => {
  await page.goto('/skills');
  await injectAxe(page);
  
  await checkA11y(page, null, {
    detailedReport: true,
    detailedReportOptions: { html: true },
  });
});

// キーボード操作テスト
test('キーボードナビゲーション', async ({ page }) => {
  await page.goto('/skills');
  
  // Tabキーでフォーカス移動
  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="skill-category"]')).toBeFocused();
  
  await page.keyboard.press('Tab');
  await expect(page.locator('[data-testid="skill-level"]')).toBeFocused();
  
  // Enterキーで保存
  await page.keyboard.press('Enter');
  await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
});
```

## テスト自動化・CI/CD統合

### 1. テスト実行環境

#### 開発環境
- **ローカル実行**: 開発者による個別テスト
- **プリコミット**: Git hooks による自動テスト
- **IDE統合**: VSCode拡張によるテスト実行

#### CI/CD環境
```yaml
# GitHub Actions ワークフロー例
name: Test Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  unit-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run test:unit
      - run: npm run test:coverage

  integration-test:
    runs-on: ubuntu-latest
    needs: unit-test
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: docker-compose up -d
      - run: npm run test:integration
      - run: docker-compose down

  e2e-test:
    runs-on: ubuntu-latest
    needs: integration-test
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npx playwright install
      - run: npm run test:e2e
```

### 2. テストデータ管理

#### テストデータ戦略
- **固定データ**: マスタデータ、基本設定
- **動的データ**: テスト実行時に生成
- **クリーンアップ**: テスト後の自動削除

#### 実装例
```javascript
// テストデータファクトリー
class TestDataFactory {
  static createUser(overrides = {}) {
    return {
      emp_no: 'TEST001',
      name: 'テスト太郎',
      dept_id: 'DEPT001',
      email: 'test@example.com',
      ...overrides
    };
  }

  static createSkillRecord(overrides = {}) {
    return {
      emp_no: 'TEST001',
      skill_id: 'SKL001',
      level: 3,
      acquired_date: new Date(),
      ...overrides
    };
  }
}

// テストデータセットアップ
beforeEach(async () => {
  await db.seed([
    TestDataFactory.createUser(),
    TestDataFactory.createSkillRecord()
  ]);
});

afterEach(async () => {
  await db.cleanup();
});
```

## 品質メトリクス・レポート

### 1. テストカバレッジ

#### 目標値
- **ユニットテスト**: 80%以上
- **統合テスト**: 主要APIの100%
- **E2Eテスト**: クリティカルパスの100%

#### 測定・レポート
```javascript
// Jest設定例
module.exports = {
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

### 2. 品質ダッシュボード

#### 監視項目
- **テスト実行結果**: 成功率、失敗原因
- **カバレッジ推移**: 時系列での変化
- **パフォーマンス**: レスポンス時間の推移
- **セキュリティ**: 脆弱性スキャン結果

### 3. 継続的改善

#### 改善サイクル
1. **メトリクス収集**: 自動化されたデータ収集
2. **分析・評価**: 週次での品質レビュー
3. **改善計画**: 問題点の特定と対策立案
4. **実装・検証**: 改善策の実装と効果測定

この包括的なテスト戦略により、高品質なシステムの継続的な提供を実現します。
