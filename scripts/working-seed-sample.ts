// scripts/working-seed-sample.ts
// working-seed.tsでrun-seed.tsの設定を使用する方法のサンプル

import { runSeedWithConfig, PRODUCTION_DB_CONFIG, DEVELOPMENT_DB_CONFIG, DatabaseConfig } from './run-seed.js';

/**
 * working-seed.ts用のメイン実行関数
 * run-seed.tsの設定を使用してシードデータ投入を実行
 */
export async function executeWorkingSeed() {
  try {
    console.log('🔧 working-seed.ts からシードデータ投入を開始...');

    // 本番環境（Neon）でシード実行
    console.log('📍 Neon データベースに接続してシード実行...');
    await runSeedWithConfig(PRODUCTION_DB_CONFIG, 'production');

    console.log('✅ working-seed.ts からのシードデータ投入完了');
    
  } catch (error) {
    console.error('❌ working-seed.ts実行エラー:', error);
    process.exit(1);
  }
}

/**
 * 開発環境用の実行関数
 */
export async function executeWorkingSeedDev() {
  try {
    console.log('🛠️ working-seed.ts から開発環境でシード実行...');
    await runSeedWithConfig(DEVELOPMENT_DB_CONFIG, 'development');
    console.log('✅ 開発環境でのシードデータ投入完了');
  } catch (error) {
    console.error('❌ 開発環境シード実行エラー:', error);
    process.exit(1);
  }
}

/**
 * カスタム設定での実行関数
 */
export async function executeWithCustomConfig(config: DatabaseConfig) {
  try {
    console.log('⚙️ カスタム設定でシード実行...');
    await runSeedWithConfig(config, 'production');
    console.log('✅ カスタム設定でのシードデータ投入完了');
  } catch (error) {
    console.error('❌ カスタム設定シード実行エラー:', error);
    process.exit(1);
  }
}

// 使用例：直接実行
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.includes('--dev')) {
    executeWorkingSeedDev();
  } else {
    executeWorkingSeed();
  }
}

// エクスポート（他のファイルからインポート可能）
export { PRODUCTION_DB_CONFIG, DEVELOPMENT_DB_CONFIG, runSeedWithConfig } from './run-seed.js';
