#!/bin/bash
# データベースツール実行スクリプト（リファクタリング版）
# 要求仕様ID: PLT.1-WEB.1

set -e

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

echo "=== データベースツール（リファクタリング版）==="
echo "作業ディレクトリ: $(pwd)"
echo ""

# Python環境チェック
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3が見つかりません"
    exit 1
fi

echo "✅ Python3: $(python3 --version)"

# 必要なパッケージチェック
echo "📦 必要なパッケージをチェック中..."
python3 -c "import yaml, pathlib" 2>/dev/null || {
    echo "❌ 必要なパッケージが不足しています"
    echo "以下のコマンドでインストールしてください:"
    echo "pip install pyyaml"
    exit 1
}

echo "✅ 必要なパッケージが揃っています"
echo ""

# 引数チェック
if [ $# -eq 0 ]; then
    echo "使用方法:"
    echo "  $0 validate [--all|--table TABLE_NAME] [--verbose]"
    echo "  $0 generate [--all|--table TABLE_NAME] [--verbose]"
    echo "  $0 check [--all|--table TABLE_NAME] [--verbose]"
    echo "  $0 all [--verbose]"
    echo ""
    echo "例:"
    echo "  $0 validate --all --verbose"
    echo "  $0 generate --table MST_Employee --verbose"
    echo "  $0 check --all"
    echo "  $0 all --verbose"
    exit 1
fi

# メインツール実行
echo "🚀 データベースツールを実行中..."
python3 db_tools_refactored.py "$@"

echo ""
echo "✅ 処理完了"
