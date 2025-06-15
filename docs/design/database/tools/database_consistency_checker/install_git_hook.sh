#!/bin/bash

# Git pre-commitフックをインストールするスクリプト
# このスクリプトは、テーブル詳細YAML定義ファイルをコミットする前に
# 必須セクション（revision_history, overview, notes, business_rules）の
# 検証を自動的に実行するGit pre-commitフックをインストールします。

# 色付き出力用
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../" && pwd)"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
PRE_COMMIT_HOOK="$GIT_HOOKS_DIR/pre-commit"

# .gitディレクトリの存在確認
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${RED}エラー: $PROJECT_ROOT/.git ディレクトリが見つかりません。${NC}"
    echo -e "${YELLOW}このスクリプトはGitリポジトリのルートディレクトリで実行する必要があります。${NC}"
    exit 1
fi

# pre-commitフックの内容
PRE_COMMIT_CONTENT='#!/bin/bash

# テーブル詳細YAML定義ファイルの必須セクション検証を実行するGit pre-commitフック

# 色付き出力用
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
BLUE="\033[0;34m"
NC="\033[0m" # No Color

echo -e "${BLUE}テーブル詳細YAML定義ファイルの必須セクション検証を実行中...${NC}"

# ステージングされたYAMLファイルを取得
YAML_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep "docs/design/database/table-details/.*_details\.yaml$")

if [ -z "$YAML_FILES" ]; then
    echo -e "${GREEN}テーブル詳細YAML定義ファイルの変更はありません。検証をスキップします。${NC}"
    exit 0
fi

# 検証スクリプトのパス
CHECKER_SCRIPT="docs/design/database/tools/database_consistency_checker/run_check.py"

if [ ! -f "$CHECKER_SCRIPT" ]; then
    echo -e "${RED}エラー: 検証スクリプト $CHECKER_SCRIPT が見つかりません。${NC}"
    exit 1
fi

# 変更されたYAMLファイルごとに検証を実行
FAILED=0

for FILE in $YAML_FILES; do
    TABLE_NAME=$(basename "$FILE" | sed "s/_details\.yaml//")
    
    echo -e "${BLUE}テーブル $TABLE_NAME の検証を実行中...${NC}"
    
    python "$CHECKER_SCRIPT" --checks yaml_format --tables "$TABLE_NAME"
    
    if [ $? -ne 0 ]; then
        FAILED=1
    fi
done

if [ $FAILED -eq 1 ]; then
    echo -e "${RED}エラー: テーブル詳細YAML定義ファイルの必須セクション検証に失敗しました。${NC}"
    echo -e "${YELLOW}詳細なガイドラインは docs/design/database/tools/database_consistency_checker/required_sections_guide.md を参照してください。${NC}"
    echo -e "${YELLOW}コミットを中止します。問題を修正してから再度コミットしてください。${NC}"
    exit 1
fi

echo -e "${GREEN}テーブル詳細YAML定義ファイルの必須セクション検証に成功しました。${NC}"
exit 0
'

# pre-commitフックを作成
echo -e "${BLUE}Git pre-commitフックをインストールしています...${NC}"

# 既存のpre-commitフックがあるか確認
if [ -f "$PRE_COMMIT_HOOK" ]; then
    echo -e "${YELLOW}既存のpre-commitフックが見つかりました。バックアップを作成します。${NC}"
    cp "$PRE_COMMIT_HOOK" "$PRE_COMMIT_HOOK.bak"
fi

# 新しいpre-commitフックを作成
echo "$PRE_COMMIT_CONTENT" > "$PRE_COMMIT_HOOK"
chmod +x "$PRE_COMMIT_HOOK"

echo -e "${GREEN}Git pre-commitフックのインストールが完了しました。${NC}"
echo -e "${BLUE}テーブル詳細YAML定義ファイルをコミットする前に、必須セクションの検証が自動的に実行されます。${NC}"
echo -e "${YELLOW}詳細なガイドラインは docs/design/database/tools/database_consistency_checker/required_sections_guide.md を参照してください。${NC}"

exit 0
