#!/bin/bash

# 改版履歴セクション欠落ファイルの一括修正スクリプト

# 対象ファイルリスト（改版履歴セクションが欠落している残り10ファイル）
files=(
    "MST_Permission_details.yaml"
    "MST_RolePermission_details.yaml"
    "MST_SkillCategory_details.yaml"
    "MST_SkillItem_details.yaml"
    "MST_UserAuth_details.yaml"
    "MST_UserRole_details.yaml"
    "SYS_SystemLog_details.yaml"
    "TRN_GoalProgress_details.yaml"
    "TRN_SkillRecord_details.yaml"
)

# 作業ディレクトリ
WORK_DIR="docs/design/database/table-details"

echo "改版履歴セクション追加開始..."

for file in "${files[@]}"; do
    filepath="$WORK_DIR/$file"
    
    if [ -f "$filepath" ]; then
        echo "処理中: $file"
        
        # テーブル名を抽出（ファイル名から）
        table_name=$(echo "$file" | sed 's/_details\.yaml$//')
        
        # 論理名を推定
        case "$table_name" in
            "MST_Permission") logical_name="権限マスタ" ;;
            "MST_RolePermission") logical_name="ロール権限関連マスタ" ;;
            "MST_SkillCategory") logical_name="スキルカテゴリマスタ" ;;
            "MST_SkillItem") logical_name="スキル項目マスタ" ;;
            "MST_UserAuth") logical_name="ユーザ認証マスタ" ;;
            "MST_UserRole") logical_name="ユーザロール関連マスタ" ;;
            "SYS_SystemLog") logical_name="システムログ" ;;
            "TRN_GoalProgress") logical_name="目標進捗トランザクション" ;;
            "TRN_SkillRecord") logical_name="スキル記録トランザクション" ;;
            *) logical_name="テーブル" ;;
        esac
        
        # 一時ファイル作成
        temp_file=$(mktemp)
        
        # ファイルの先頭部分を読み取り、改版履歴セクションを挿入
        awk -v table_name="$table_name" -v logical_name="$logical_name" '
        BEGIN { inserted = 0 }
        /^# テーブル概要・目的/ && !inserted {
            print "# 改版履歴"
            print "revision_history:"
            print "  - version: \"1.0.0\""
            print "    date: \"2025-06-01\""
            print "    author: \"開発チーム\""
            print "    changes: \"初版作成 - " logical_name "テーブルの詳細定義\""
            print ""
            inserted = 1
        }
        { print }
        ' "$filepath" > "$temp_file"
        
        # 元ファイルを置き換え
        mv "$temp_file" "$filepath"
        
        echo "完了: $file"
    else
        echo "ファイルが見つかりません: $filepath"
    fi
done

echo "改版履歴セクション追加完了！"
echo "処理されたファイル数: ${#files[@]}"
