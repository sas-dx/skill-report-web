#!/bin/bash

# rules セクションを business_rules に統一するスクリプト
# 作成日: 2025-06-23
# 目的: YAMLファイルの rules セクションを business_rules に変更

echo "=== rules セクションを business_rules に統一開始 ==="

# 対象ディレクトリ
TARGET_DIR="docs/design/database/table-details"

# バックアップディレクトリ作成
BACKUP_DIR="${TARGET_DIR}/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

echo "バックアップディレクトリ: $BACKUP_DIR"

# 処理対象ファイル数をカウント
total_files=0
processed_files=0

# YAMLファイルを検索
for file in "$TARGET_DIR"/テーブル詳細定義YAML_*.yaml; do
    if [[ -f "$file" ]]; then
        total_files=$((total_files + 1))
    fi
done

echo "処理対象ファイル数: $total_files"

# 各YAMLファイルを処理
for file in "$TARGET_DIR"/テーブル詳細定義YAML_*.yaml; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file")
        echo "処理中: $filename"
        
        # バックアップ作成
        cp "$file" "$BACKUP_DIR/"
        
        # rules: を business_rules: に置換
        sed -i 's/^rules:/business_rules:/' "$file"
        
        processed_files=$((processed_files + 1))
        echo "  ✓ 完了 ($processed_files/$total_files)"
    fi
done

echo ""
echo "=== 処理完了 ==="
echo "処理済みファイル数: $processed_files"
echo "バックアップ場所: $BACKUP_DIR"

# 検証: business_rules セクションの存在確認
echo ""
echo "=== 検証: business_rules セクションの確認 ==="
missing_count=0

for file in "$TARGET_DIR"/テーブル詳細定義YAML_*.yaml; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file")
        if ! grep -q "^business_rules:" "$file"; then
            echo "❌ $filename: business_rules セクションが見つかりません"
            missing_count=$((missing_count + 1))
        fi
    fi
done

if [[ $missing_count -eq 0 ]]; then
    echo "✅ 全てのファイルで business_rules セクションを確認"
else
    echo "⚠️  $missing_count 個のファイルで business_rules セクションが不足"
fi

echo ""
echo "=== スクリプト完了 ==="
