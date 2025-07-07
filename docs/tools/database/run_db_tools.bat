@echo off
REM データベースツール実行スクリプト (Windows)

cd /d "%~dp0"

REM Python仮想環境の確認・作成
if not exist "venv_simple" (
    echo 🔧 Python仮想環境を作成中...
    python -m venv venv_simple
)

REM 仮想環境アクティベート
call venv_simple\Scripts\activate.bat

REM 依存関係インストール
echo 📦 依存関係をインストール中...
pip install -r requirements_simple.txt

REM ツール実行
echo 🚀 データベースツールを実行中...

REM 引数に応じてコマンド実行
if "%1"=="check" (
    python db_tools.py check --all
) else if "%1"=="validate" (
    python db_tools.py validate --yaml-dir ../table-details
) else if "%1"=="generate" (
    if "%2"=="" (
        python db_tools.py generate --all
    ) else (
        python db_tools.py generate --table %2
    )
) else if "%1"=="help" (
    goto :help
) else if "%1"=="-h" (
    goto :help
) else if "%1"=="--help" (
    goto :help
) else (
    echo ❓ 使用方法: run_db_tools.bat [check^|validate^|generate^|help]
    echo 詳細: run_db_tools.bat help
    goto :end
)

echo ✅ 完了
goto :end

:help
echo 使用方法:
echo   run_db_tools.bat check          # 全体整合性チェック
echo   run_db_tools.bat validate       # YAML検証
echo   run_db_tools.bat generate       # 全テーブル生成
echo   run_db_tools.bat generate TABLE # 特定テーブル生成
echo   run_db_tools.bat help           # このヘルプ

:end
