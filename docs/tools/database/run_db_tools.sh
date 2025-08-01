#!/bin/bash
# データベースツール実行スクリプト

set -e

# 作業ディレクトリに移動
cd "$(dirname "$0")"

# Python仮想環境の確認・作成
if [ ! -d "venv_simple" ]; then
    echo "🔧 Python仮想環境を作成中..."
    python3 -m venv venv_simple
fi

# 仮想環境アクティベート
source venv_simple/bin/activate

# 依存関係インストール
echo "📦 依存関係をインストール中..."
pip install -r requirements_simple.txt

# ツール実行
echo "🚀 データベースツールを実行中..."

# 引数に応じてコマンド実行
if [ "$1" = "check" ]; then
    python db_tools.py check --all
elif [ "$1" = "validate" ]; then
    python db_tools.py validate --yaml-dir ../table-details
elif [ "$1" = "generate" ]; then
    if [ -n "$2" ]; then
        python db_tools.py generate --table "$2"
    else
        python db_tools.py generate --all
    fi
elif [ "$1" = "help" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    echo "使用方法:"
    echo "  ./run_db_tools.sh check          # 全体整合性チェック"
    echo "  ./run_db_tools.sh validate       # YAML検証"
    echo "  ./run_db_tools.sh generate       # 全テーブル生成"
    echo "  ./run_db_tools.sh generate TABLE # 特定テーブル生成"
    echo "  ./run_db_tools.sh help           # このヘルプ"
else
    echo "❓ 使用方法: ./run_db_tools.sh [check|validate|generate|help]"
    echo "詳細: ./run_db_tools.sh help"
fi

echo "✅ 完了"
