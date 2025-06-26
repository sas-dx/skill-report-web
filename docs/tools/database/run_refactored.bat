@echo off
REM データベースツール実行スクリプト（リファクタリング版）
REM 要求仕様ID: PLT.1-WEB.1

setlocal enabledelayedexpansion

REM スクリプトのディレクトリに移動
cd /d "%~dp0"

echo === データベースツール（リファクタリング版）===
echo 作業ディレクトリ: %cd%
echo.

REM Python環境チェック
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Pythonが見つかりません
    exit /b 1
)

echo ✅ Python: 
python --version

REM 必要なパッケージチェック
echo 📦 必要なパッケージをチェック中...
python -c "import yaml, pathlib" >nul 2>&1
if errorlevel 1 (
    echo ❌ 必要なパッケージが不足しています
    echo 以下のコマンドでインストールしてください:
    echo pip install pyyaml
    exit /b 1
)

echo ✅ 必要なパッケージが揃っています
echo.

REM 引数チェック
if "%1"=="" (
    echo 使用方法:
    echo   %0 validate [--all^|--table TABLE_NAME] [--verbose]
    echo   %0 generate [--all^|--table TABLE_NAME] [--verbose]
    echo   %0 check [--all^|--table TABLE_NAME] [--verbose]
    echo   %0 all [--verbose]
    echo.
    echo 例:
    echo   %0 validate --all --verbose
    echo   %0 generate --table MST_Employee --verbose
    echo   %0 check --all
    echo   %0 all --verbose
    exit /b 1
)

REM メインツール実行
echo 🚀 データベースツールを実行中...
python db_tools_refactored.py %*

echo.
echo ✅ 処理完了
