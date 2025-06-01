#!/bin/bash

# Phase 2: コメント行とtable_name不一致修正スクリプト
# 作成日: 2025-06-01
# 目的: 全YAMLファイルのコメント行をtable_nameに合わせて修正

echo "Phase 2: コメント行修正開始..."

# 対象ディレクトリ
TARGET_DIR="docs/design/database/table-details"

# テンプレートファイルとレポートファイルを除外
EXCLUDE_PATTERN="(_TEMPLATE_|_STRUCTURE_CHECK_|_PHASE1_)"

# 修正対象ファイルを取得
FILES=$(find "$TARGET_DIR" -name "*.yaml" | grep -v -E "$EXCLUDE_PATTERN")

# 修正カウンタ
FIXED_COUNT=0

for file in $FILES; do
    echo "処理中: $(basename "$file")"
    
    # table_nameの値を取得
    TABLE_NAME=$(grep '^table_name:' "$file" | sed 's/table_name: *"\([^"]*\)".*/\1/')
    
    if [ -n "$TABLE_NAME" ]; then
        # 現在のコメント行を確認
        CURRENT_COMMENT=$(head -1 "$file")
        EXPECTED_COMMENT="# $TABLE_NAME テーブル詳細定義"
        
        if [ "$CURRENT_COMMENT" != "$EXPECTED_COMMENT" ]; then
            echo "  修正前: $CURRENT_COMMENT"
            echo "  修正後: $EXPECTED_COMMENT"
            
            # 一時ファイルを作成して修正
            {
                echo "$EXPECTED_COMMENT"
                tail -n +2 "$file"
            } > "${file}.tmp"
            
            # 元ファイルを置換
            mv "${file}.tmp" "$file"
            
            FIXED_COUNT=$((FIXED_COUNT + 1))
            echo "  完了: $(basename "$file")"
        else
            echo "  スキップ: $(basename "$file") (既に正しい)"
        fi
    else
        echo "  エラー: $(basename "$file") - table_nameが見つかりません"
    fi
    echo ""
done

echo "Phase 2: コメント行修正完了！"
echo "修正されたファイル数: $FIXED_COUNT"
