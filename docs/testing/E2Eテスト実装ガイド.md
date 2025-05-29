# E2Eテスト実装ガイド: 年間スキル報告書WEB化PJT

---

## 1. 文書情報

| 項目 | 内容 |
|------|------|
| 文書名 | E2Eテスト実装ガイド |
| プロジェクト名 | 年間スキル報告書WEB化プロジェクト |
| システム名 | スキル報告書管理システム（SRMS） |
| プロジェクトID | SAS-DX-AI-2025-001 |
| 作成者 | AI推進チーム |
| 作成日 | 2025年5月29日 |
| 最終更新日 | 2025年5月29日 |
| 版数 | 1.0 |

---

## 2. E2Eテストの概要

### 2.1 E2Eテストの目的

E2E（End-to-End）テストは、実際のユーザーの操作フローを模倣し、システム全体が期待通りに動作することを確認するテストです。

#### 主な検証項目
- **ユーザージャーニー**: ログインから各機能利用までの一連の流れ
- **UI/UX**: ユーザーインターフェースの動作と表示
- **データフロー**: フロントエンドからバックエンド、データベースまでの完全なデータ処理
- **ブラウザ互換性**: 複数ブラウザでの動作確認
- **レスポンシブ対応**: デスクトップ・モバイルでの表示確認

### 2.2 テスト対象ユーザーフロー

```mermaid
graph TD
    A[ログインページ] --> B[認証処理]
    B --> C[ダッシュボード]
    C --> D[スキル管理]
    C --> E[レポート作成]
    C --> F[レポート一覧]
    D --> G[スキル追加/編集/削除]
    E --> H[スキル選択・入力]
    H --> I[レポート生成]
    F --> J[レポート表示/ダウンロード]
    G --> K[ログアウト]
    I --> K
    J --> K
```

---

## 3. テスト環境セットアップ

### 3.1 必要パッケージのインストール

```bash
# Playwright のインストール
npm install -D @playwright/test

# ブラウザのインストール
npx playwright install

# 追加の型定義とユーティリティ
npm install -D @types/node
npm install -D dotenv
npm install -D cross-env
```

### 3.2 Playwright設定ファイル

#### playwright.config.ts
```typescript
import { defineConfig, devices } from '@playwright/test'
import dotenv from 'dotenv'

// 環境変数の読み込み
dotenv.config({ path: '.env.test' })

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  timeout: 60000,
  expect: {
    timeout: 10000
  },
  reporter: [
    ['html', { outputFolder: 'test-results/html-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/results.xml' }],
    ['allure-playwright', { outputFolder: 'test-results/allure-results' }]
  ],
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000,
    headless: process.env.CI ? true : false,
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,
    locale: 'ja-JP',
    timezoneId: 'Asia/Tokyo'
  },
  projects: [
    // デスクトップブラウザ
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] }
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] }
    },
    // モバイルデバイス
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] }
    },
    // タブレット
    {
      name: 'iPad',
      use: { ...devices['iPad Pro'] }
    }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000
  }
})
```

### 3.3 環境設定ファイル

#### .env.test
```bash
# テスト環境設定
BASE_URL=http://localhost:3000
API_BASE_URL=http://localhost:3001/api

# テストユーザー認証情報
TEST_USER_EMAIL=test@example.com
TEST_USER_PASSWORD=password123
TEST_ADMIN_EMAIL=admin@example.com
TEST_ADMIN_PASSWORD=admin123

# データベース設定
DATABASE_URL=postgresql://test_user:test_password@localhost:5433/srms_test

# Azure設定（テスト用）
AZURE_STORAGE_CONNECTION_STRING=UseDevelopmentStorage=true
AZURE_AD_CLIENT_ID=test-client-id
AZURE_AD_TENANT_ID=test-tenant-id
```

---

## 4. テストヘルパー・ページオブジェクト実装

### 4.1 ベースページクラス

#### tests/e2e/pages/BasePage.ts
```typescript
import { Page, Locator, expect } from '@playwright/test'

export abstract class BasePage {
  protected page: Page

  constructor(page: Page) {
    this.page = page
  }

  // 共通要素
  get header(): Locator {
    return this.page.locator('[data-testid="header"]')
  }

  get navigation(): Locator {
    return this.page.locator('[data-testid="navigation"]')
  }

  get footer(): Locator {
    return this.page.locator('[data-testid="footer"]')
  }

  get loadingSpinner(): Locator {
    return this.page.locator('[data-testid="loading-spinner"]')
  }

  get errorMessage(): Locator {
    return this.page.locator('[data-testid="error-message"]')
  }

  get successMessage(): Locator {
    return this.page.locator('[data-testid="success-message"]')
  }

  // 共通メソッド
  async waitForPageLoad(): Promise<void> {
    await this.page.waitForLoadState('networkidle')
    await expect(this.loadingSpinner).not.toBeVisible({ timeout: 10000 })
  }

  async waitForApiResponse(urlPattern: string | RegExp): Promise<void> {
    await this.page.waitForResponse(urlPattern)
  }

  async takeScreenshot(name: string): Promise<void> {
    await this.page.screenshot({ 
      path: `test-results/screenshots/${name}.png`,
      fullPage: true 
    })
  }

  async scrollToElement(locator: Locator): Promise<void> {
    await locator.scrollIntoViewIfNeeded()
  }

  async waitForElement(locator: Locator, timeout: number = 10000): Promise<void> {
    await locator.waitFor({ state: 'visible', timeout })
  }
}
```

### 4.2 ログインページ

#### tests/e2e/pages/LoginPage.ts
```typescript
import { Page, Locator, expect } from '@playwright/test'
import { BasePage } from './BasePage'

export class LoginPage extends BasePage {
  readonly url = '/login'

  constructor(page: Page) {
    super(page)
  }

  // 要素の定義
  get emailInput(): Locator {
    return this.page.locator('[data-testid="email-input"]')
  }

  get passwordInput(): Locator {
    return this.page.locator('[data-testid="password-input"]')
  }

  get passwordToggle(): Locator {
    return this.page.locator('[data-testid="password-toggle"]')
  }

  get loginButton(): Locator {
    return this.page.locator('[data-testid="login-button"]')
  }

  get forgotPasswordLink(): Locator {
    return this.page.locator('[data-testid="forgot-password-link"]')
  }

  get emailError(): Locator {
    return this.page.locator('[data-testid="email-error"]')
  }

  get passwordError(): Locator {
    return this.page.locator('[data-testid="password-error"]')
  }

  get loginError(): Locator {
    return this.page.locator('[data-testid="login-error"]')
  }

  // アクションメソッド
  async goto(): Promise<void> {
    await this.page.goto(this.url)
    await this.waitForPageLoad()
  }

  async fillEmail(email: string): Promise<void> {
    await this.emailInput.fill(email)
  }

  async fillPassword(password: string): Promise<void> {
    await this.passwordInput.fill(password)
  }

  async togglePasswordVisibility(): Promise<void> {
    await this.passwordToggle.click()
  }

  async clickLogin(): Promise<void> {
    await this.loginButton.click()
  }

  async login(email: string, password: string): Promise<void> {
    await this.fillEmail(email)
    await this.fillPassword(password)
    await this.clickLogin()
  }

  async loginWithValidCredentials(): Promise<void> {
    const email = process.env.TEST_USER_EMAIL || 'test@example.com'
    const password = process.env.TEST_USER_PASSWORD || 'password123'
    await this.login(email, password)
    await this.waitForApiResponse(/\/api\/auth\/login/)
  }

  // 検証メソッド
  async verifyPageElements(): Promise<void> {
    await expect(this.page.locator('h1')).toContainText('ログイン')
    await expect(this.emailInput).toBeVisible()
    await expect(this.passwordInput).toBeVisible()
    await expect(this.loginButton).toBeVisible()
    await expect(this.forgotPasswordLink).toBeVisible()
  }

  async verifyEmailError(expectedMessage: string): Promise<void> {
    await expect(this.emailError).toContainText(expectedMessage)
  }

  async verifyPasswordError(expectedMessage: string): Promise<void> {
    await expect(this.passwordError).toContainText(expectedMessage)
  }

  async verifyLoginError(expectedMessage: string): Promise<void> {
    await expect(this.loginError).toContainText(expectedMessage)
  }

  async verifyPasswordVisibility(isVisible: boolean): Promise<void> {
    const expectedType = isVisible ? 'text' : 'password'
    await expect(this.passwordInput).toHaveAttribute('type', expectedType)
  }
}
```

---

## 5. E2Eテストケース実装

### 5.1 認証機能テスト

#### tests/e2e/auth.spec.ts
```typescript
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'

test.describe('認証機能', () => {
  let loginPage: LoginPage
  let dashboardPage: DashboardPage

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page)
    dashboardPage = new DashboardPage(page)
  })

  test('正常系: ログイン・ログアウトフロー', async ({ page }) => {
    // ログインページにアクセス
    await loginPage.goto()
    await loginPage.verifyPageElements()
    
    // ログイン実行
    await loginPage.loginWithValidCredentials()
    
    // ダッシュボードに遷移することを確認
    await expect(page).toHaveURL('/dashboard')
    await dashboardPage.verifyPageElements()
    
    // ログアウト実行
    await dashboardPage.logout()
    
    // ログインページに戻ることを確認
    await expect(page).toHaveURL('/login')
  })

  test('異常系: 無効な認証情報でログイン失敗', async ({ page }) => {
    await loginPage.goto()
    
    // 無効な認証情報でログイン試行
    await loginPage.login('invalid@example.com', 'wrongpassword')
    
    // エラーメッセージの表示確認
    await loginPage.verifyLoginError('認証に失敗しました')
    
    // ログインページに留まることを確認
    await expect(page).toHaveURL('/login')
  })

  test('異常系: 必須項目未入力でのバリデーション', async ({ page }) => {
    await loginPage.goto()
    
    // 空のまま送信
    await loginPage.clickLogin()
    
    // バリデーションエラーの表示確認
    await loginPage.verifyEmailError('メールアドレスは必須です')
    await loginPage.verifyPasswordError('パスワードは必須です')
  })

  test('正常系: パスワード表示/非表示の切り替え', async ({ page }) => {
    await loginPage.goto()
    
    // 初期状態は非表示
    await loginPage.verifyPasswordVisibility(false)
    
    // 表示に切り替え
    await loginPage.togglePasswordVisibility()
    await loginPage.verifyPasswordVisibility(true)
    
    // 非表示に戻す
    await loginPage.togglePasswordVisibility()
    await loginPage.verifyPasswordVisibility(false)
  })
})
```

### 5.2 スキル管理機能テスト

#### tests/e2e/skills.spec.ts
```typescript
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/LoginPage'
import { DashboardPage } from './pages/DashboardPage'
import { SkillsPage, SkillData } from './pages/SkillsPage'

test.describe('スキル管理機能', () => {
  let loginPage: LoginPage
  let dashboardPage: DashboardPage
  let skillsPage: SkillsPage

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page)
    dashboardPage = new DashboardPage(page)
    skillsPage = new SkillsPage(page)
    
    // 事前にログイン
    await loginPage.goto()
    await loginPage.loginWithValidCredentials()
    await dashboardPage.navigateToSkills()
  })

  test('正常系: 新規スキル追加', async ({ page }) => {
    const newSkill: SkillData = {
      name: 'TypeScript',
      category: 'プログラミング言語',
      level: '◎',
      experience: '2年',
      description: '型安全なJavaScript開発'
    }
    
    await skillsPage.addSkill(newSkill)
    
    // 追加されたスキルの確認
    await skillsPage.verifySkillExists(newSkill.name)
    await skillsPage.verifySkillDetails(newSkill.name, newSkill)
  })

  test('正常系: スキル編集', async ({ page }) => {
    // 既存スキルを追加
    const originalSkill: SkillData = {
      name: 'JavaScript',
      category: 'プログラミング言語',
      level: '○',
      experience: '3年'
    }
    await skillsPage.addSkill(originalSkill)
    
    // スキルを編集
    const updatedData = {
      level: '◎',
      experience: '4年',
      description: '更新された説明'
    }
    
    await skillsPage.editSkill(originalSkill.name, updatedData)
    
    // 更新されたスキルの確認
    await skillsPage.verifySkillDetails(originalSkill.name, updatedData)
  })

  test('正常系: スキル削除', async ({ page }) => {
    const skillToDelete: SkillData = {
      name: 'TestSkill',
      category: 'テスト',
      level: '△',
      experience: '1年'
    }
    
    // 削除対象のスキルを追加
    await skillsPage.addSkill(skillToDelete)
    await skillsPage.verifySkillExists(skillToDelete.name)
    
    // スキルを削除
    await skillsPage.deleteSkill(skillToDelete.name)
    
    // 削除されたことを確認
    await skillsPage.verifySkillNotExists(skillToDelete.name)
  })

  test('正常系: スキル検索機能', async ({ page }) => {
    // 複数のスキルを追加
    const skills: SkillData[] = [
      { name: 'JavaScript', category: 'プログラミング言語', level: '○' },
      { name: 'TypeScript', category: 'プログラミング言語', level: '◎' },
      { name: 'React', category: 'フレームワーク', level: '○' }
    ]
    
    for (const skill of skills) {
      await skillsPage.addSkill(skill)
    }
    
    // 検索実行
    await skillsPage.searchSkills('Script')
    
    // 検索結果の確認
    await skillsPage.verifySkillExists('JavaScript')
    await skillsPage.verifySkillExists('TypeScript')
    await skillsPage.verifySkillNotExists('React')
    
    // 検索をクリア
    await skillsPage.clearFilters()
    
    // 全てのスキルが表示されることを確認
    await skillsPage.verifySkillsCount(3)
  })
})
```

---

## 6. テスト実行・管理

### 6.1 テスト実行コマンド

```bash
# 全E2Eテスト実行
npx playwright test

# 特定のテストファイル実行
npx playwright test auth.spec.ts
npx playwright test skills.spec.ts

# 特定のブラウザでのみ実行
npx playwright test --project=chromium
npx playwright test --project=firefox
npx playwright test --project=webkit

# ヘッドレスモードを無効にして実行
npx playwright test --headed

# デバッグモードで実行
npx playwright test --debug

# 並列実行数を指定
npx playwright test --workers=2

# 失敗時のリトライ回数を指定
npx playwright test --retries=3

# 特定のタグでフィルタリング
npx playwright test --grep="正常系"
npx playwright test --grep-invert="異常系"

# レポート生成
npx playwright show-report
```

### 6.2 CI/CD統合

#### GitHub Actions設定
```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *' # 毎日午前2時に実行

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Install Playwright browsers
      run: npx playwright install --with-deps ${{ matrix.browser }}
    
    - name: Start application
      run: |
        npm run build
        npm run start &
        sleep 30
      env:
        NODE_ENV: test
    
    - name: Run E2E tests
      run: npx playwright test --project=${{ matrix.browser }}
      env:
        BASE_URL: http://localhost:3000
        TEST_USER_EMAIL: ${{ secrets.TEST_USER_EMAIL }}
        TEST_USER_PASSWORD: ${{ secrets.TEST_USER_PASSWORD }}
    
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: e2e-test-results-${{ matrix.browser }}
        path: |
          test-results/
          playwright-report/
    
    - name: Upload screenshots
      uses: actions/upload-artifact@v3
      if: failure()
      with:
        name: e2e-screenshots-${{ matrix.browser }}
        path: test-results/screenshots/
```

---

## 7. ベストプラクティス

### 7.1 テスト設計原則

#### Page Object Modelの活用
```typescript
// ✅ 良い例 - Page Object Model
const loginPage = new LoginPage(page)
await loginPage.login('user@example.com', 'password')

// ❌ 悪い例 - 直接的な要素操作
await page.fill('#email', 'user@example.com')
await page.fill('#password', 'password')
await page.click('#login-button')
```

#### 適切な待機処理
```typescript
// ✅ 良い例 - 明示的な待機
await page.waitForSelector('[data-testid="success-message"]')
await page.waitForResponse(/\/api\/login/)

// ❌ 悪い例 - 固定時間の待機
await page.waitForTimeout(3000)
```

#### データ属性の使用
```typescript
// ✅ 良い例 - data-testid属性
await page.click('[data-testid="submit-button"]')

// ❌ 悪い例 - CSSクラスやテキストに依存
await page.click('.btn-primary')
await page.click('text=送信')
```

### 7.2 テストの安定性向上

#### フレーキーテストの対策
```typescript
// リトライ機能の活用
test('不安定なテスト', async ({ page }) => {
  await test.step('操作実行', async () => {
    // 不安定な操作
  })
})

// 条件待ちの改善
await expect(async () => {
  const element = page.locator('[data-testid="dynamic-content"]')
  await expect(element).toBeVisible()
  await expect(element).toContainText('期待するテキスト')
}).toPass({ timeout: 10000 })
```

#### テストデータの管理
```typescript
// テストごとのクリーンアップ
test.beforeEach(async ({ page }) => {
  // テストデータのリセット
  await page.request.post('/api/test/reset')
})

test.afterEach(async ({ page }) => {
  // テスト後のクリーンアップ
  await page.request.delete('/api/test/cleanup')
})
```

---

## 8. まとめ

### 8.1 E2Eテスト実装の効果

- **品質向上**: ユーザー視点での動作確認により、実際の使用シーンでの不具合を早期発見
- **回帰テスト**: 機能追加・修正時の既存機能への影響を自動検証
- **ブラウザ互換性**: 複数ブラウザでの動作を自動確認
- **CI/CD統合**: 継続的な品質保証の実現

### 8.2 運用における注意点

- **実行時間**: E2Eテストは時間がかかるため、重要なシナリオに絞って実装
- **メンテナンス**: UIの変更に伴うテストコードの更新が必要
- **環境依存**: テスト環境の安定性がテスト結果に大きく影響
- **データ管理**: テストデータの準備・クリーンアップの自動化が重要

### 8.3 今後の拡張計画

- **視覚回帰テスト**: スクリーンショット比較による視覚的な変更検出
- **パフォーマンステスト**: ページロード時間やレスポンス時間の監視
- **アクセシビリティテスト**: WCAG準拠の自動チェック
- **モバイルテスト**: より多くのモバイルデバイスでのテスト拡充

このE2Eテスト実装ガイドにより、年間スキル報告書WEB化プロジェクトにおいて、エンドユーザーの視点から包括的な品質保証を実現し、安定したシステム運用を支援します。
