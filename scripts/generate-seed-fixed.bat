@echo off
REM 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入自動化
REM SQLサンプルデータからPrisma seed.tsファイルを生成（修正版）

echo 🔧 SQLサンプルデータからPrisma seed.tsファイルを生成します...

REM スクリプトのディレクトリを取得
set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..

REM パスの設定
set PYTHON_SCRIPT=%SCRIPT_DIR%sql-to-seed-fixed.py
set SQL_DATA_DIR=%PROJECT_ROOT%\docs\design\database\data
set OUTPUT_FILE=%PROJECT_ROOT%\src\database\prisma\seed.ts

REM Pythonスクリプトが存在するかチェック
if not exist "%PYTHON_SCRIPT%" (
    echo ❌ エラー: Pythonスクリプトが見つかりません: %PYTHON_SCRIPT%
    exit /b 1
)

REM SQLデータディレクトリが存在するかチェック
if not exist "%SQL_DATA_DIR%" (
    echo ❌ エラー: SQLデータディレクトリが見つかりません: %SQL_DATA_DIR%
    exit /b 1
)

REM 既存のseed.tsファイルをバックアップ
if exist "%OUTPUT_FILE%" (
    for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set DATE=%%c%%a%%b
    for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIME=%%a%%b
    set BACKUP_FILE=%OUTPUT_FILE%.backup.%DATE%_%TIME%
    echo 📁 既存のseed.tsファイルをバックアップします: %BACKUP_FILE%
    copy "%OUTPUT_FILE%" "%BACKUP_FILE%" >nul
)

REM Pythonスクリプトを実行
echo 🐍 Pythonスクリプトを実行中...
python "%PYTHON_SCRIPT%" --sql-dir "%SQL_DATA_DIR%" --output "%OUTPUT_FILE%"

REM 実行結果をチェック
if %errorlevel% equ 0 (
    echo ✅ seed.tsファイルの生成が完了しました！
    echo 📁 出力ファイル: %OUTPUT_FILE%
    echo.
    echo 🚀 次のステップ:
    echo    1. 生成されたseed.tsファイルを確認
    echo    2. npm run db:seed でデータベースに初期データを投入
    echo.
    echo 💡 使用方法:
    echo    cd %PROJECT_ROOT%
    echo    npm run db:seed
) else (
    echo ❌ エラー: seed.tsファイルの生成に失敗しました
    exit /b 1
)

pause
