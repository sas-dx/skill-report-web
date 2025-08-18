import { fileURLToPath, pathToFileURL } from 'url'
import { dirname, resolve } from 'path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const seedPath = resolve(__dirname, '../src/database/prisma/working-seed.ts')

/**
 * データベース接続用環境変数設定
 * working-seed.tsから読み込み可能な形式で定義
 */
export interface DatabaseConfig {
  DATABASE_URL: string;
  DIRECT_URL: string;
}

/**
 * 本番環境（Neon）のデータベース設定
 */
export const PRODUCTION_DB_CONFIG: DatabaseConfig = {
  DATABASE_URL: "postgresql://neondb_owner:npg_rTA8QuMhFGx0@ep-royal-fog-a1uzobb8-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require",
  DIRECT_URL: "postgresql://neondb_owner:npg_rTA8QuMhFGx0@ep-royal-fog-a1uzobb8-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
};

/**
 * 開発環境（ローカル）のデータベース設定
 */
export const DEVELOPMENT_DB_CONFIG: DatabaseConfig = {
  DATABASE_URL: "postgresql://postgres:password@localhost:5432/skill_report_dev",
  DIRECT_URL: "postgresql://postgres:password@localhost:5432/skill_report_dev"
};

/**
 * 環境変数を設定してシードを実行
 * @param config データベース設定
 * @param environment 実行環境 ('production' | 'development')
 */
export async function runSeedWithConfig(config: DatabaseConfig, environment: 'production' | 'development' = 'production') {
  try {
    console.log(`🌱 シードデータ投入開始 - ${environment} 環境`);
    console.log(`📍 接続先: ${config.DATABASE_URL.split('@')[1]?.split('/')[0] || 'Unknown'}`);

    // 環境変数を設定
    process.env.DATABASE_URL = config.DATABASE_URL;
    process.env.DIRECT_URL = config.DIRECT_URL;

    // working-seed.tsをインポートして実行
    const seedModule = await import(pathToFileURL(seedPath).href);
    if (seedModule.runSampleSeed) {
      await seedModule.runSampleSeed();
    } else {
      console.log('⚠️ runSampleSeed関数が見つかりません');
    }

    console.log('✅ シードデータ投入完了');
    
  } catch (error) {
    console.error('❌ シードデータ投入エラー:', error);
    process.exit(1);
  }
}

async function run() {
  const args = process.argv.slice(2);
  const environment = args.includes('--dev') ? 'development' : 'production';
  
  if (environment === 'development') {
    console.log('🛠️ 開発環境モードで実行');
    await runSeedWithConfig(DEVELOPMENT_DB_CONFIG, 'development');
  } else {
    console.log('🚀 本番環境（Neon）モードで実行');
    await runSeedWithConfig(PRODUCTION_DB_CONFIG, 'production');
  }
}

run()
