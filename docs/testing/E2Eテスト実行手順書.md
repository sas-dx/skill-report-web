# E2Eテスト実行手順書: 年間スキル報告書WEB化PJT

---

## 1. 文書情報

| 項目 | 内容 |
|------|------|
| 文書名 | E2Eテスト実行手順書 |
| プロジェクト名 | 年間スキル報告書WEB化プロジェクト |
| システム名 | スキル報告書管理システム（SRMS） |
| プロジェクトID | SAS-DX-AI-2025-001 |
| 作成者 | AI推進チーム |
| 作成日 | 2025年5月29日 |
| 最終更新日 | 2025年5月29日 |
| 版数 | 1.0 |

---

## 2. E2Eテスト環境構築

### 2.1 必要パッケージのインストール

```bash
# Playwright のインストール
npm install -D @playwright/test

# ブラウザのインストール
npx playwright install

# 追加の型定義
npm install -D @types/node
```

### 2.2 Playwright設定ファイル

#### playwright.config.ts
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/results.xml' }]
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    actionTimeout: 10000,
    navigationTimeout: 30000
  },
  projects: [
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
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] }
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] }
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

### 2.3 テストヘルパー・ユーティリティ

#### tests/e2e/helpers/auth.ts
```typescript
import { Page, expect } from '@playwright/test'

export class AuthHelper {
  constructor(private page: Page) {}

  async login(email: string = 'user@example.com', password: string = 'password') {
    await this.page.goto('/login')
    await this.page.fill('[data-testid="email-input"]', email)
    await this.page.fill('[data-testid="password-input"]', password)
    await this.page.click('[data-testid="login-button"]')
    
    // ログイン成功を確認
    await expect(this.page).toHaveURL('/dashboard')
    await expect(this.page.locator('[data-testid="user-menu"]')).toBeVisible()
  }

  async logout() {
    await this.page.click('[data-testid="user-menu"]')
    await this.page.click('[data-testid="logout-button"]')
    
    // ログアウト成功を確認
    await expect(this.page).toHaveURL('/login')
  }

  async isLoggedIn(): Promise<boolean> {
    try {
      await this.page.locator('[data-testid="user-menu"]').waitFor({ timeout: 5000 })
      return true
    } catch {
      return false
    }
  }
}
```

#### tests/e2e/helpers/skill.ts
```typescript
import { Page, expect } from '@playwright/test'

export class SkillHelper {
  constructor(private page: Page) {}

  async navigateToSkillManagement() {
    await this.page.click('[data-testid="nav-skills"]')
    await expect(this.page).toHaveURL('/skills')
    await expect(this.page.locator('h1')).toContainText('スキル管理')
  }

  async addSkill(skillData: {
    name: string
    category: string
    level: string
    experience?: string
  }) {
    await this.page.click('[data-testid="add-skill-button"]')
    
    // モーダルが開くのを待つ
    await expect(this.page.locator('[data-testid="skill-modal"]')).toBeVisible()
    
    // スキル情報を入力
    await this.page.fill('[data-testid="skill-name-input"]', skillData.name)
    await this.page.selectOption('[data-testid="skill-category-select"]', skillData.category)
    await this.page.selectOption('[data-testid="skill-level-select"]', skillData.level)
    
    if (skillData.experience) {
      await this.page.fill('[data-testid="skill-experience-input"]', skillData.experience)
    }
    
    // 保存
    await this.page.click('[data-testid="save-skill-button"]')
    
    // モーダルが閉じるのを待つ
    await expect(this.page.locator('[data-testid="skill-modal"]')).not.toBeVisible()
  }

  async editSkill(skillName: string, newData: Partial<{
    name: string
    category: string
    level: string
    experience: string
  }>) {
    // スキル行を見つけて編集ボタンをクリック
    const skillRow = this.page.locator(`[data-testid="skill-row"]:has-text("${skillName}")`)
    await skillRow.locator('[data-testid="edit-skill-button"]').click()
    
    // モーダルが開くのを待つ
    await expect(this.page.locator('[data-testid="skill-modal"]')).toBeVisible()
    
    // 新しいデータを入力
    if (newData.name) {
      await this.page.fill('[data-testid="skill-name-input"]', newData.name)
    }
    if (newData.category) {
      await this.page.selectOption('[data-testid="skill-category-select"]', newData.category)
    }
    if (newData.level) {
      await this.page.selectOption('[data-testid="skill-level-select"]', newData.level)
    }
    if (newData.experience) {
      await this.page.fill('[data-testid="skill-experience-input"]', newData.experience)
    }
    
    // 保存
    await this.page.click('[data-testid="save-skill-button"]')
    
    // モーダルが閉じるのを待つ
    await expect(this.page.locator('[data-testid="skill-modal"]')).not.toBeVisible()
  }

  async deleteSkill(skillName: string) {
    const skillRow = this.page.locator(`[data-testid="skill-row"]:has-text("${skillName}")`)
    await skillRow.locator('[data-testid="delete-skill-button"]').click()
    
    // 確認ダイアログが表示されるのを待つ
    await expect(this.page.locator('[data-testid="confirm-dialog"]')).toBeVisible()
    await this.page.click('[data-testid="confirm-delete-button"]')
    
    // ダイアログが閉じるのを待つ
    await expect(this.page.locator('[data-testid="confirm-dialog"]')).not.toBeVisible()
  }

  async searchSkill(searchTerm: string) {
    await this.page.fill('[data-testid="skill-search-input"]', searchTerm)
    await this.page.press('[data-testid="skill-search-input"]', 'Enter')
  }

  async filterByCategory(category: string) {
    await this.page.selectOption('[data-testid="category-filter-select"]', category)
  }

  async verifySkillExists(skillName: string) {
    await expect(this.page.locator(`[data-testid="skill-row"]:has-text("${skillName}")`)).toBeVisible()
  }

  async verifySkillNotExists(skillName: string) {
    await expect(this.page.locator(`[data-testid="skill-row"]:has-text("${skillName}")`)).not.toBeVisible()
  }
}
```

---

## 3. E2Eテストケース実装

### 3.1 認証機能テスト

#### tests/e2e/auth.spec.ts
```typescript
import { test, expect } from '@playwright/test'
import { AuthHelper } from './helpers/auth'

test.describe('認証機能', () => {
  test('正常系: ログイン・ログアウト', async ({ page }) => {
    const auth = new AuthHelper(page)
    
    // ログインページにアクセス
    await page.goto('/login')
    
    // ログインフォームの表示確認
    await expect(page.locator('h1')).toContainText('ログイン')
    await expect(page.locator('[data-testid="email-input"]')).toBeVisible()
    await expect(page.locator('[data-testid="password-input"]')).toBeVisible()
    await expect(page.locator('[data-testid="login-button"]')).toBeVisible()
    
    // ログイン実行
    await auth.login()
    
    // ダッシュボードの表示確認
    await expect(page.locator('h1')).toContainText('ダッシュボード')
    await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible()
    
    // ログアウト実行
    await auth.logout()
    
    // ログインページに戻ることを確認
    await expect(page.locator('h1')).toContainText('ログイン')
  })

  test('異常系: 無効な認証情報でログイン失敗', async ({ page }) => {
    await page.goto('/login')
    
    // 無効な認証情報を入力
    await page.fill('[data-testid="email-input"]', 'invalid@example.com')
    await page.fill('[data-testid="password-input"]', 'wrongpassword')
    await page.click('[data-testid="login-button"]')
    
    // エラーメッセージの表示確認
    await expect(page.locator('[data-testid="error-message"]')).toContainText('認証に失敗しました')
    
    // ログインページに留まることを確認
    await expect(page).toHaveURL('/login')
  })

  test('異常系: 必須項目未入力でのバリデーション', async ({ page }) => {
    await page.goto('/login')
    
    // 空のまま送信
    await page.click('[data-testid="login-button"]')
    
    // バリデーションエラーの表示確認
    await expect(page.locator('[data-testid="email-error"]')).toContainText('メールアドレスは必須です')
    await expect(page.locator('[data-testid="password-error"]')).toContainText('パスワードは必須です')
  })

  test('正常系: パスワード表示/非表示の切り替え', async ({ page }) => {
    await page.goto('/login')
    
    const passwordInput = page.locator('[data-testid="password-input"]')
    const toggleButton = page.locator('[data-testid="password-toggle"]')
    
    // 初期状態は非表示
    await expect(passwordInput).toHaveAttribute('type', 'password')
    
    // 表示に切り替え
    await toggleButton.click()
    await expect(passwordInput).toHaveAttribute('type', 'text')
    
    // 非表示に戻す
    await toggleButton.click()
    await expect(passwordInput).toHaveAttribute('type', 'password')
  })
})
```

### 3.2 スキル管理機能テスト

#### tests/e2e/skills.spec.ts
```typescript
import { test, expect } from '@playwright/test'
import { AuthHelper } from './helpers/auth'
import { SkillHelper } from './helpers/skill'

test.describe('スキル管理機能', () => {
  let auth: AuthHelper
  let skill: SkillHelper

  test.beforeEach(async ({ page }) => {
    auth = new AuthHelper(page)
    skill = new SkillHelper(page)
    
    // 事前にログイン
    await auth.login()
  })

  test('正常系: スキル一覧表示', async ({ page }) => {
    await skill.navigateToSkillManagement()
    
    // スキル一覧の表示確認
    await expect(page.locator('[data-testid="skills-table"]')).toBeVisible()
    await expect(page.locator('[data-testid="add-skill-button"]')).toBeVisible()
    await expect(page.locator('[data-testid="skill-search-input"]')).toBeVisible()
  })

  test('正常系: 新規スキル追加', async ({ page }) => {
    await skill.navigateToSkillManagement()
    
    const newSkill = {
      name: 'TypeScript',
      category: 'プログラミング言語',
      level: '◎',
      experience: '2年'
    }
    
    await skill.addSkill(newSkill)
    
    // 追加されたスキルの表示確認
    await skill.verifySkillExists(newSkill.name)
    
    // スキル詳細の確認
    const skillRow = page.locator(`[data-testid="skill-row"]:has-text("${newSkill.name}")`)
    await expect(skillRow).toContainText(newSkill.category)
    await expect(skillRow).toContainText(newSkill.level)
    await expect(skillRow).toContainText(newSkill.experience)
  })

  test('正常系: スキル編集', async ({ page }) => {
    await skill.navigateToSkillManagement()
    
    // 既存スキルがあることを前提
    const originalSkill = 'JavaScript'
    const updatedData = {
      level: '◎',
      experience: '4年'
    }
    
    await skill.editSkill(originalSkill, updatedData)
    
    // 更新されたスキルの確認
    const skillRow = page.locator(`[data-testid="skill-row"]:has-text("${originalSkill}")`)
    await expect(skillRow).toContainText(updatedData.level)
    await expect(skillRow).toContainText(updatedData.experience)
  })

  test('正常系: スキル削除', async ({ page }) => {
    await skill.navigateToSkillManagement()
    
    const skillToDelete = 'TestSkill'
    
    // 削除対象のスキルを追加
    await skill.addSkill({
      name: skillToDelete,
      category: 'テスト',
