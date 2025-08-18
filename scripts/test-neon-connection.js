/**
 * Neon PostgreSQL 接続テストスクリプト
 * 要求仕様ID: PLT.1-DEPLOY.1
 */

require('dotenv').config();
const { PrismaClient } = require('@prisma/client');

async function testNeonConnection() {
  const prisma = new PrismaClient();
  
  try {
    console.log('🔌 Neon PostgreSQL 接続テスト開始...\n');
    
    // 1. 基本接続テスト
    console.log('📡 1. データベース接続確認...');
    await prisma.$connect();
    console.log('✅ データベース接続成功');
    
    // 2. クエリテスト
    console.log('\n📊 2. クエリ実行テスト...');
    const result = await prisma.$queryRaw`SELECT version()`;
    console.log('✅ クエリ実行成功');
    console.log('📋 PostgreSQL バージョン:', result[0]?.version?.substring(0, 50) + '...');
    
    // 3. 接続情報表示
    console.log('\n🔗 3. 接続情報:');
    console.log('DATABASE_URL:', process.env.DATABASE_URL ? '設定済み' : '未設定');
    console.log('DIRECT_URL:', process.env.DIRECT_URL ? '設定済み' : '未設定');
    
    // 4. 時刻テスト
    console.log('\n⏰ 4. 時刻同期テスト...');
    const timeResult = await prisma.$queryRaw`SELECT NOW() as current_time`;
    console.log('✅ サーバー時刻:', timeResult[0]?.current_time);
    
    // 5. パフォーマンステスト
    console.log('\n⚡ 5. パフォーマンステスト...');
    const startTime = Date.now();
    await prisma.$queryRaw`SELECT 1`;
    const endTime = Date.now();
    console.log(`✅ レスポンス時間: ${endTime - startTime}ms`);
    
    console.log('\n🎉 Neon データベース接続テスト完了！');
    console.log('✅ 本番環境での使用準備が整いました');
    
  } catch (error) {
    console.error('\n❌ 接続テストエラー:');
    console.error('Error:', error.message);
    
    if (error.message.includes('ENOTFOUND')) {
      console.error('💡 対処法: ネットワーク接続を確認してください');
    } else if (error.message.includes('authentication')) {
      console.error('💡 対処法: 認証情報を確認してください');
    } else if (error.message.includes('database')) {
      console.error('💡 対処法: データベース名を確認してください');
    }
    
    process.exit(1);
  } finally {
    await prisma.$disconnect();
  }
}

// メイン実行
if (require.main === module) {
  testNeonConnection();
}

module.exports = { testNeonConnection };
