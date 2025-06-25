#!/bin/bash

# YAML検証ツール Git pre-commitフック設定スクリプト
# 要求仕様ID: PLT.1-WEB.1
# 作成日: 2025-06-17
# 作成者: 開発チーム
# 統合日: 2025-06-20 (database_consistency_checkerに統合)

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# プロジェクトルートディレクトリの検出
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
GIT_HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
PRE_COMMIT_HOOK="$GIT_HOOKS_DIR/pre-commit"

echo -e "${BLUE}🔧 YAML検証ツール Git pre-commitフック設定${NC}"
echo "プロジェクトルート: $PROJECT_ROOT"
echo "Git hooksディレクトリ: $GIT_HOOKS_DIR"

# Gitリポジトリの確認
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${RED}❌ エラー: Gitリポジトリが見つかりません${NC}"
    echo "このスクリプトはGitリポジトリのルートで実行してください"
    exit 1
fi

# 検証レベルの選択
echo -e "\n${YELLOW}📋 検証レベルを選択してください:${NC}"
echo "1) 警告モード (エラーがあってもコミット可能)"
echo "2) 厳格モード (エラー時はコミット阻止)"
echo "3) カスタム設定"

read -p "選択 (1-3): " VALIDATION_LEVEL

case $VALIDATION_LEVEL in
    1)
        VALIDATION_MODE="warning"
        echo -e "${YELLOW}⚠️ 警告モードを選択しました${NC}"
        ;;
    2)
        VALIDATION_MODE="strict"
        echo -e "${RED}🔒 厳格モードを選択しました${NC}"
        ;;
    3)
        VALIDATION_MODE="custom"
        echo -e "${BLUE}⚙️ カスタム設定モードを選択しました${NC}"
        ;;
    *)
        echo -e "${RED}❌ 無効な選択です。警告モードを使用します${NC}"
        VALIDATION_MODE="warning"
        ;;
esac

# 既存のpre-commitフックのバックアップ
if [ -f "$PRE_COMMIT_HOOK" ]; then
    BACKUP_FILE="${PRE_COMMIT_HOOK}.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "\n${YELLOW}📦 既存のpre-commitフックをバックアップします${NC}"
    cp "$PRE_COMMIT_HOOK" "$BACKUP_FILE"
    echo "バックアップ先: $BACKUP_FILE"
fi

# pre-commitフックの作成
echo -e "\n${GREEN}📝 pre-commitフックを作成中...${NC}"

cat > "$PRE_COMMIT_HOOK" << 'EOF'
#!/bin/bash

# YAML検証ツール Git pre-commitフック
# 自動生成日: $(date +%Y-%m-%d %H:%M:%S)
# 検証モード: VALIDATION_MODE_PLACEHOLDER

set -e

# カラー定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 設定
VALIDATION_MODE="VALIDATION_MODE_PLACEHOLDER"
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
YAML_VALIDATOR_DIR="$PROJECT_ROOT/docs/design/database/tools/database_consistency_checker"

# 変更されたYAMLファイルを取得
changed_yaml_files=$(git diff --cached --name-only --diff-filter=ACM | grep "_details\.yaml$" || true)

if [ -z "$changed_yaml_files" ]; then
    # YAMLファイルの変更がない場合は正常終了
    exit 0
fi

echo -e "${BLUE}🔍 YAML検証を実行中...${NC}"

# テーブル名を抽出
tables=""
for file in $changed_yaml_files; do
    table_name=$(basename "$file" "_details.yaml")
    # テンプレートファイルは除外
    if [ "$table_name" != "MST_TEMPLATE" ]; then
        if [ -z "$tables" ]; then
            tables="$table_name"
        else
            tables="$tables,$table_name"
        fi
    fi
done

if [ -z "$tables" ]; then
    echo -e "${GREEN}✅ 検証対象のYAMLファイルがありません${NC}"
    exit 0
fi

echo "検証対象テーブル: $tables"

# YAML検証実行
validation_failed=false
validation_output=""

# 拡張YAML検証を実行
if [ -f "$YAML_VALIDATOR_DIR/yaml_format_check.py" ]; then
    echo -e "${BLUE}📋 拡張YAML検証を実行中...${NC}"
    
    # Python環境の確認
    if command -v python3 >/dev/null 2>&1; then
        PYTHON_CMD="python3"
    elif command -v python >/dev/null 2>&1; then
        PYTHON_CMD="python"
    else
        echo -e "${RED}❌ Pythonが見つかりません${NC}"
        exit 1
    fi
    
    # 検証実行
    cd "$PROJECT_ROOT"
    validation_output=$($PYTHON_CMD -c "
import sys
sys.path.append('docs/design/database/tools/database_consistency_checker')
from yaml_format_check import check_yaml_format_enhanced
import json

tables_list = '$tables'.split(',')
result = check_yaml_format_enhanced(tables=tables_list, verbose=True)

if not result['success']:
    print('VALIDATION_FAILED')
    for table_result in result['results']:
        if not table_result['valid']:
            print(f'❌ {table_result[\"table\"]}:')
            for error in table_result['errors']:
                print(f'  - {error}')
            if 'warnings' in table_result and table_result['warnings']:
                for warning in table_result['warnings']:
                    print(f'  ⚠️ {warning}')
else:
    print('VALIDATION_SUCCESS')
    print(f'✅ 全{result[\"valid\"]}テーブルの検証に成功しました')
" 2>&1)
    
    if echo "$validation_output" | grep -q "VALIDATION_FAILED"; then
        validation_failed=true
    fi
else
    echo -e "${YELLOW}⚠️ YAML検証ツールが見つかりません${NC}"
    echo "パス: $YAML_VALIDATOR_DIR/yaml_format_check.py"
fi

# 結果の表示と処理
echo -e "\n${BLUE}📊 検証結果:${NC}"
echo "$validation_output" | grep -v "VALIDATION_"

if [ "$validation_failed" = true ]; then
    echo -e "\n${RED}❌ YAML検証に失敗しました${NC}"
    
    if [ "$VALIDATION_MODE" = "strict" ]; then
        echo -e "${RED}🔒 厳格モードのため、コミットを中止します${NC}"
        echo -e "\n${YELLOW}💡 修正方法:${NC}"
        echo "1. docs/design/database/tools/database_consistency_checker/README.md を参照"
        echo "2. 必須セクション（revision_history, overview, notes, business_rules）を確認"
        echo "3. 要求仕様ID形式（例: PRO.1-BASE.1）を確認"
        echo "4. 修正後に再度コミットを実行"
        exit 1
    else
        echo -e "${YELLOW}⚠️ 警告モードのため、コミットを続行します${NC}"
        echo -e "${YELLOW}💡 後で修正することを推奨します${NC}"
    fi
else
    echo -e "\n${GREEN}✅ YAML検証に成功しました${NC}"
fi

exit 0
EOF

# プレースホルダーを実際の値に置換
sed -i "s/VALIDATION_MODE_PLACEHOLDER/$VALIDATION_MODE/g" "$PRE_COMMIT_HOOK"
sed -i "s/\$(date +%Y-%m-%d %H:%M:%S)/$(date +%Y-%m-%d\ %H:%M:%S)/g" "$PRE_COMMIT_HOOK"

# 実行権限を付与
chmod +x "$PRE_COMMIT_HOOK"

echo -e "${GREEN}✅ pre-commitフックの設定が完了しました${NC}"

# 設定ファイルの作成（カスタムモードの場合）
if [ "$VALIDATION_MODE" = "custom" ]; then
    CONFIG_FILE="$SCRIPT_DIR/.yaml_validator_config"
    echo -e "\n${BLUE}⚙️ 設定ファイルを作成中...${NC}"
    
    cat > "$CONFIG_FILE" << EOF
# YAML検証ツール設定ファイル
# 作成日: $(date +%Y-%m-%d %H:%M:%S)

# 検証レベル: warning, strict
validation_mode=custom

# 検証対象ファイルパターン
include_patterns=*_details.yaml

# 除外ファイルパターン
exclude_patterns=MST_TEMPLATE_details.yaml

# 必須セクション検証
check_required_sections=true

# 要求仕様ID検証
check_requirement_ids=true

# 詳細ログ出力
verbose=true

# エラー時の動作: abort, warn
on_error=warn
EOF
    
    echo "設定ファイル: $CONFIG_FILE"
    echo -e "${YELLOW}💡 設定ファイルを編集してカスタマイズできます${NC}"
fi

# テスト実行の提案
echo -e "\n${BLUE}🧪 テスト実行:${NC}"
echo "以下のコマンドでテストできます:"
echo "1. YAMLファイルを編集"
echo "2. git add <編集したYAMLファイル>"
echo "3. git commit -m \"テストコミット\""

# 使用方法の表示
echo -e "\n${GREEN}📖 使用方法:${NC}"
echo "• YAMLファイルを編集してコミットすると自動的に検証が実行されます"
echo "• 検証に失敗した場合は詳細なエラーメッセージが表示されます"
echo "• 設定を変更したい場合は、このスクリプトを再実行してください"

# アンインストール方法
echo -e "\n${YELLOW}🗑️ アンインストール:${NC}"
echo "フックを無効にするには: rm $PRE_COMMIT_HOOK"
if [ -f "${PRE_COMMIT_HOOK}.backup."* ]; then
    echo "バックアップから復元するには: cp ${PRE_COMMIT_HOOK}.backup.* $PRE_COMMIT_HOOK"
fi

echo -e "\n${GREEN}🎉 Git pre-commitフックの設定が完了しました！${NC}"
