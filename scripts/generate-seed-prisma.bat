@echo off
REM 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入自動化
REM Prisma対応版のseed.tsファイル生成バッチ

echo ========================================
echo Prisma seed.ts ファイル生成スクリプト
echo ========================================
echo.

REM Pythonの存在確認
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonが見つかりません。Pythonをインストールしてください。
    pause
    exit /b 1
)

echo ✅ Python環境を確認しました
echo.

REM 現在のディレクトリを確認
if not exist "docs\design\database\data" (
    echo ❌ SQLデータディレクトリが見つかりません: docs\design\database\data
    echo    正しいプロジェクトルートから実行してください。
    pause
    exit /b 1
)

echo ✅ SQLデータディレクトリを確認しました
echo.

REM 出力ディレクトリの作成
if not exist "src\database\prisma" (
    echo 📁 出力ディレクトリを作成中: src\database\prisma
    mkdir "src\database\prisma"
)

echo 🚀 Prisma seed.tsファイルを生成中...
echo.

REM Pythonスクリプトの実行
python scripts\sql-to-seed-prisma-fixed.py --backup

if errorlevel 1 (
    echo.
    echo ❌ seed.tsファイルの生成に失敗しました
    pause
    exit /b 1
)

echo.
echo ✅ seed.tsファイルの生成が完了しました！
echo.
echo 📋 次のステップ:
echo    1. npm run db:seed でデータベースに初期データを投入
echo    2. npm run dev でアプリケーションを起動
echo.
pause
