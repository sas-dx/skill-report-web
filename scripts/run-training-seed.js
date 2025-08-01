/**
 * 要求仕様ID: TRN.1-ATT.1
 * 実装内容: 研修・資格情報のシードデータ実行スクリプト
 */
const { execSync } = require('child_process');
const path = require('path');

console.log('研修・資格情報のシードデータを実行します...');

try {
  // TypeScriptファイルをコンパイルして実行
  execSync('npx tsx src/database/prisma/seed-training.ts', {
    stdio: 'inherit',
    cwd: process.cwd()
  });
  
  console.log('研修・資格情報のシードデータ実行が完了しました');
} catch (error) {
  console.error('シードデータ実行中にエラーが発生しました:', error);
  process.exit(1);
}
