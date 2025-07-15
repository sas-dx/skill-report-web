/**
 * Jest セットアップファイル
 * 要求仕様ID: TST.1-UNIT.1
 * 対応設計書: docs/testing/03_ユニットテスト実装ガイド.md
 */

// テスト環境の設定
process.env.NODE_ENV = 'test';
process.env.DATABASE_URL = 'postgresql://test:test@localhost:5432/test_db';
process.env.JWT_SECRET = 'test-jwt-secret-key';

// グローバルなテストセットアップ
beforeAll(async () => {
  // テスト開始前の初期化処理
  console.log('🧪 テスト環境を初期化中...');
});

afterAll(async () => {
  // テスト終了後のクリーンアップ処理
  console.log('🧹 テスト環境をクリーンアップ中...');
});

// モック関数の設定
global.fetch = jest.fn();

// コンソールログの制御（テスト実行時のノイズを減らす）
const originalConsoleError = console.error;
const originalConsoleWarn = console.warn;

beforeEach(() => {
  // 各テスト前にモックをリセット
  jest.clearAllMocks();
});

afterEach(() => {
  // 各テスト後のクリーンアップ
  jest.restoreAllMocks();
});

// テスト用のユーティリティ関数
global.testUtils = {
  // モックユーザーデータ
  mockUser: {
    id: 'test-user-001',
    loginId: 'testuser',
    name: 'テストユーザー',
    email: 'test@example.com',
    department: 'テスト部門'
  },
  
  // モックスキルデータ
  mockSkill: {
    skill_id: 'test-skill-001',
    category: 'technical',
    name: 'JavaScript',
    level: 3,
    experience_years: 2,
    description: 'テスト用スキル',
    projects: [],
    certifications: [],
    last_used_date: '2024-12-01'
  }
};
