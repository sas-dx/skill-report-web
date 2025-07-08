#!/bin/bash
"""
データベース設計ツール統合テスト実行スクリプト

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-21
実装者: AI Assistant

使用方法:
  ./run_tests.sh [オプション]

オプション:
  --unit          ユニットテストのみ実行
  --integration   統合テストのみ実行
  --performance   パフォーマンステストのみ実行
  --all           全テスト実行（デフォルト）
  --verbose       詳細出力
  --help          ヘルプ表示
"""

set -e  # エラー時に停止

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# デフォルト設定
RUN_UNIT=false
RUN_INTEGRATION=false
RUN_PERFORMANCE=false
RUN_ALL=true
VERBOSE=false

# 引数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --unit)
            RUN_UNIT=true
            RUN_ALL=false
            shift
            ;;
        --integration)
            RUN_INTEGRATION=true
            RUN_ALL=false
            shift
            ;;
        --performance)
            RUN_PERFORMANCE=true
            RUN_ALL=false
            shift
            ;;
        --all)
            RUN_ALL=true
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            echo "データベース設計ツール統合テスト実行スクリプト"
            echo ""
            echo "使用方法:"
            echo "  ./run_tests.sh [オプション]"
            echo ""
            echo "オプション:"
            echo "  --unit          ユニットテストのみ実行"
            echo "  --integration   統合テストのみ実行"
            echo "  --performance   パフォーマンステストのみ実行"
            echo "  --all           全テスト実行（デフォルト）"
            echo "  --verbose       詳細出力"
            echo "  --help          ヘルプ表示"
            exit 0
            ;;
        *)
            echo "不明なオプション: $1"
            echo "ヘルプを表示するには --help を使用してください"
            exit 1
            ;;
    esac
done

# Python環境チェック
echo "🔍 Python環境をチェック中..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 が見つかりません。Python3をインストールしてください。"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "✅ Python $PYTHON_VERSION を使用します"

# 必要なパッケージのチェック
echo "📦 必要なパッケージをチェック中..."
REQUIRED_PACKAGES=("yaml" "pathlib")
MISSING_PACKAGES=()

for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! python3 -c "import $package" 2>/dev/null; then
        MISSING_PACKAGES+=("$package")
    fi
done

if [ ${#MISSING_PACKAGES[@]} -gt 0 ]; then
    echo "⚠️  以下のパッケージが不足しています: ${MISSING_PACKAGES[*]}"
    echo "pip install ${MISSING_PACKAGES[*]} でインストールしてください"
fi

# オプションのパッケージチェック
echo "🔧 オプションパッケージをチェック中..."
if ! python3 -c "import psutil" 2>/dev/null; then
    echo "⚠️  psutil が見つかりません。パフォーマンステストは制限されます。"
    echo "   pip install psutil でインストールすることを推奨します。"
fi

# テスト実行
echo ""
echo "🚀 テスト実行を開始します..."
echo "============================================"

# 実行時間計測開始
START_TIME=$(date +%s)

# テスト実行関数
run_test_suite() {
    local test_type=$1
    local test_file=$2
    
    echo ""
    echo "📋 $test_type を実行中..."
    echo "--------------------------------------------"
    
    if [ "$VERBOSE" = true ]; then
        python3 -m unittest discover -s "tests/$test_file" -p "test_*.py" -v
    else
        python3 -m unittest discover -s "tests/$test_file" -p "test_*.py"
    fi
    
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "✅ $test_type: 成功"
    else
        echo "❌ $test_type: 失敗 (終了コード: $exit_code)"
        return $exit_code
    fi
}

# 個別テスト実行
OVERALL_SUCCESS=true

if [ "$RUN_ALL" = true ] || [ "$RUN_UNIT" = true ]; then
    if ! run_test_suite "ユニットテスト" "unit"; then
        OVERALL_SUCCESS=false
    fi
fi

if [ "$RUN_ALL" = true ] || [ "$RUN_INTEGRATION" = true ]; then
    if ! run_test_suite "統合テスト" "integration"; then
        OVERALL_SUCCESS=false
    fi
fi

if [ "$RUN_ALL" = true ] || [ "$RUN_PERFORMANCE" = true ]; then
    if ! run_test_suite "パフォーマンステスト" "performance"; then
        OVERALL_SUCCESS=false
    fi
fi

# 統合テスト実行（全テストスイート）
if [ "$RUN_ALL" = true ]; then
    echo ""
    echo "🔄 統合テストスイートを実行中..."
    echo "--------------------------------------------"
    
    if [ "$VERBOSE" = true ]; then
        python3 run_all_tests.py --verbose
    else
        python3 run_all_tests.py
    fi
    
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo "✅ 統合テストスイート: 成功"
    else
        echo "❌ 統合テストスイート: 失敗 (終了コード: $exit_code)"
        OVERALL_SUCCESS=false
    fi
fi

# 実行時間計測終了
END_TIME=$(date +%s)
EXECUTION_TIME=$((END_TIME - START_TIME))

# 結果サマリー
echo ""
echo "============================================"
echo "📊 テスト実行結果サマリー"
echo "============================================"
echo "実行時間: ${EXECUTION_TIME}秒"

if [ "$OVERALL_SUCCESS" = true ]; then
    echo "🎉 全テスト成功！"
    echo ""
    echo "✨ データベース設計ツールは正常に動作しています。"
    exit 0
else
    echo "⚠️  一部テストに問題があります。"
    echo ""
    echo "🔍 詳細なログを確認し、問題を修正してください。"
    echo "   - test_execution_report.json で詳細レポートを確認"
    echo "   - --verbose オプションで詳細出力を有効化"
    exit 1
fi
