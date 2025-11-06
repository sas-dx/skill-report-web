import { defineConfig, devices } from '@playwright/test'
import dotenv from 'dotenv'

// 環境変数の読み込み
dotenv.config({ path: '.env.test' })
dotenv.config({ path: '.env.local' })

/**
 * Playwright設定 - ハイブリッドテストアーキテクチャ対応
 * 
 * Phase 1: Test Data Builder, Visual Regression, Versioned Data
 * Phase 2: AI Maintenance, Chaos Engineering
 * Phase 3: BDD/Cucumber, Distributed Testing, Multi-Tenancy
 */
export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  timeout: 60000,
  expect: {
    timeout: 10000,
    toHaveScreenshot: {
      maxDiffPixels: 100,
      animations: 'disabled'
    }
  },
  reporter: [
    ['html', { outputFolder: 'test-results/html-report' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/results.xml' }],
    ['line'],
    ['list']
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
    // Setup project
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/
    },
    // デスクトップブラウザ
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup']
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup']
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
      dependencies: ['setup']
    },
    // モバイルデバイス
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
      dependencies: ['setup']
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
      dependencies: ['setup']
    },
    // Visual Regression Testing
    {
      name: 'visual-regression',
      testMatch: /.*\.visual\.spec\.ts/,
      use: {
        ...devices['Desktop Chrome'],
        viewport: { width: 1920, height: 1080 }
      }
    },
    // Chaos Engineering Tests
    {
      name: 'chaos',
      testMatch: /chaos\/.*\.spec\.ts/,
      use: {
        ...devices['Desktop Chrome']
      }
    }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000
  }
})
