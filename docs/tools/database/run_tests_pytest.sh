#!/bin/bash
# データベース設計ツール統合テストスイート実行スクリプト（pytest版）
# 要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
# 設計書: docs/design/database/08-database-design-guidelines.md

set -e  # エラー時に停止

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# カラー出力設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ヘルプ表示関数
show_help() {
    echo "データベース設計ツール統合テスト実行スクリプト（pytest版）"
    echo ""
    echo "使用方法:"
    echo "  ./run_tests_pytest.sh [オプション]"
    echo ""
    echo "オプション:"
    echo "  -u, --unit          ユニットテストのみ実行"
    echo "  -i, --integration   統合テストのみ実行"
    echo "  -p, --performance   パフォーマンステストのみ実行"
    echo "  -a, --all           全テスト実行（デフォルト）"
    echo "  -v, --verbose       詳細出力"
    echo "  -c, --coverage      カバレッジレポート生成"
    echo "  -h, --html          HTMLレポート生成"
    echo "  -j, --parallel      並列実行（自動CPU数検出）"
    echo "  --install-deps      依存関係を自動インストール"
    echo "  --help              ヘルプ表示"
    echo ""
    echo "例:"
    echo "  ./run_tests_pytest.sh --unit --verbose"
    echo "  ./run_tests_pytest.sh --all --coverage --html"
    echo "  ./run_tests_pytest.sh --parallel --install-deps"
}

# デフォルト設定
RUN_UNIT=false
RUN_INTEGRATION=false
RUN_PERFORMANCE=false
RUN_ALL=true
VERBOSE=false
COVERAGE=false
HTML_REPORT=false
PARALLEL=false
INSTALL_DEPS=false

# 引数解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--unit)
            RUN_UNIT=true
            RUN_ALL=false
            shift
            ;;
        -i|--integration)
            RUN_INTEGRATION=true
            RUN_ALL=false
            shift
            ;;
        -p|--performance)
            RUN_PERFORMANCE=true
            RUN_ALL=false
            shift
            ;;
        -a|--all)
            RUN_ALL=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -c|--coverage)
            COVERAGE=true
            shift
            ;;
        -h|--html)
            HTML_REPORT=true
            shift
            ;;
        -j|--parallel)
            PARALLEL=true
            shift
            ;;
        --install-deps)
            INSTALL_DEPS=true
            shift
            ;;
        --help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ 不明なオプション: $1${NC}"
            echo "ヘルプを表示するには --help を使用してください"
            exit 1
            ;;
    esac
done

# ヘッダー表示
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}🧪 データベース設計ツール統合テストスイート${NC}"
echo -e "${BLUE}============================================${NC}"

# Python環境チェック
echo -e "${YELLOW}🔍 Python環境をチェック中...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3が見つかりません。Python3をインストールしてください。${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✅ Python $PYTHON_VERSION を使用します${NC}"

# 仮想環境の推奨
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo -e "${YELLOW}⚠️  仮想環境が検出されませんでした。${NC}"
    echo -e "${YELLOW}   python3 -m venv venv && source venv/bin/activate${NC}"
    echo -e "${YELLOW}   での仮想環境使用を推奨します。${NC}"
fi

# 依存関係の自動インストール
if [ "$INSTALL_DEPS" = true ]; then
    echo -e "${YELLOW}📦 依存関係をインストール中...${NC}"
    if [ -f "requirements.txt" ]; then
        python3 -m pip install -r requirements.txt
        echo -e "${GREEN}✅ 依存関係のインストールが完了しました${NC}"
    else
        echo -e "${RED}❌ requirements.txt が見つかりません${NC}"
        exit 1
    fi
fi

# pytest の確認
echo -e "${YELLOW}🔧 pytest の確認中...${NC}"
if ! python3 -c "import pytest" 2>/dev/null; then
    echo -e "${RED}❌ pytest が見つかりません。${NC}"
    echo -e "${YELLOW}以下のコマンドでインストールしてください:${NC}"
    echo "pip install pytest pytest-html pytest-cov pytest-xdist"
    echo ""
    echo -e "${YELLOW}または --install-deps オプションを使用してください${NC}"
    exit 1
fi

PYTEST_VERSION=$(python3 -c "import pytest; print(pytest.__version__)")
echo -e "${GREEN}✅ pytest $PYTEST_VERSION を使用します${NC}"

# テストレポートディレクトリの作成
echo -e "${YELLOW}📁 テストレポートディレクトリを準備中...${NC}"
mkdir -p test_reports

# pytest オプション構築
PYTEST_ARGS=()

# 基本オプション
PYTEST_ARGS+=("--tb=short")

# 詳細出力
if [ "$VERBOSE" = true ]; then
    PYTEST_ARGS+=("-v")
else
    PYTEST_ARGS+=("-q")
fi

# カバレッジレポート
if [ "$COVERAGE" = true ]; then
    PYTEST_ARGS+=("--cov=.")
    PYTEST_ARGS+=("--cov-report=term-missing")
    PYTEST_ARGS+=("--cov-report=html:test_reports/coverage")
    PYTEST_ARGS+=("--cov-report=xml:test_reports/coverage.xml")
fi

# HTMLレポート
if [ "$HTML_REPORT" = true ]; then
    PYTEST_ARGS+=("--html=test_reports/report.html")
    PYTEST_ARGS+=("--self-contained-html")
fi

# JUnit XMLレポート（CI/CD用）
PYTEST_ARGS+=("--junit-xml=test_reports/junit.xml")

# 並列実行
if [ "$PARALLEL" = true ]; then
    if python3 -c "import xdist" 2>/dev/null; then
        PYTEST_ARGS+=("-n" "auto")
        echo -e "${GREEN}✅ 並列実行を有効化しました（自動CPU数検出）${NC}"
    else
        echo -e "${YELLOW}⚠️  pytest-xdist が見つかりません。並列実行をスキップします。${NC}"
    fi
fi

# 実行時間計測開始
START_TIME=$(date +%s)

# テスト実行
echo ""
echo -e "${BLUE}🚀 テスト実行を開始します...${NC}"
echo -e "${BLUE}============================================${NC}"

# テスト対象の決定
TEST_TARGETS=()

if [ "$RUN_ALL" = true ]; then
    TEST_TARGETS+=("tests/")
elif [ "$RUN_UNIT" = true ]; then
    TEST_TARGETS+=("tests/unit/")
elif [ "$RUN_INTEGRATION" = true ]; then
    TEST_TARGETS+=("tests/integration/")
elif [ "$RUN_PERFORMANCE" = true ]; then
    TEST_TARGETS+=("tests/performance/")
fi

# マーカーによるフィルタリング
MARKER_ARGS=()
if [ "$RUN_UNIT" = true ]; then
    MARKER_ARGS+=("-m" "unit")
elif [ "$RUN_INTEGRATION" = true ]; then
    MARKER_ARGS+=("-m" "integration")
elif [ "$RUN_PERFORMANCE" = true ]; then
    MARKER_ARGS+=("-m" "performance")
fi

# pytest実行
echo -e "${YELLOW}実行コマンド: python3 -m pytest ${PYTEST_ARGS[*]} ${MARKER_ARGS[*]} ${TEST_TARGETS[*]}${NC}"
echo ""

if python3 -m pytest "${PYTEST_ARGS[@]}" "${MARKER_ARGS[@]}" "${TEST_TARGETS[@]}"; then
    TEST_SUCCESS=true
else
    TEST_SUCCESS=false
fi

# 実行時間計測終了
END_TIME=$(date +%s)
EXECUTION_TIME=$((END_TIME - START_TIME))

# 結果サマリー
echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}📊 テスト実行結果サマリー${NC}"
echo -e "${BLUE}============================================${NC}"
echo -e "${YELLOW}実行時間: ${EXECUTION_TIME}秒${NC}"

# レポートファイルの確認
echo ""
echo -e "${YELLOW}📄 生成されたレポート:${NC}"
if [ -f "test_reports/junit.xml" ]; then
    echo -e "${GREEN}  ✅ JUnit XML: test_reports/junit.xml${NC}"
fi
if [ -f "test_reports/report.html" ]; then
    echo -e "${GREEN}  ✅ HTML レポート: test_reports/report.html${NC}"
fi
if [ -d "test_reports/coverage" ]; then
    echo -e "${GREEN}  ✅ カバレッジレポート: test_reports/coverage/index.html${NC}"
fi

# 最終結果
echo ""
if [ "$TEST_SUCCESS" = true ]; then
    echo -e "${GREEN}🎉 全テスト成功！${NC}"
    echo ""
    echo -e "${GREEN}✨ データベース設計ツールは正常に動作しています。${NC}"
    
    # 追加情報
    if [ "$HTML_REPORT" = true ]; then
        echo -e "${YELLOW}🌐 HTMLレポートをブラウザで確認してください:${NC}"
        echo -e "${YELLOW}   file://$SCRIPT_DIR/test_reports/report.html${NC}"
    fi
    
    if [ "$COVERAGE" = true ]; then
        echo -e "${YELLOW}📈 カバレッジレポートをブラウザで確認してください:${NC}"
        echo -e "${YELLOW}   file://$SCRIPT_DIR/test_reports/coverage/index.html${NC}"
    fi
    
    exit 0
else
    echo -e "${RED}⚠️  一部テストに問題があります。${NC}"
    echo ""
    echo -e "${YELLOW}🔍 詳細なログを確認し、問題を修正してください:${NC}"
    echo -e "${YELLOW}   - test_reports/report.html で詳細レポートを確認${NC}"
    echo -e "${YELLOW}   - --verbose オプションで詳細出力を有効化${NC}"
    echo -e "${YELLOW}   - --coverage オプションでカバレッジを確認${NC}"
    exit 1
fi
