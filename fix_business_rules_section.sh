#!/bin/bash

# 🚨 feat: notesセクション内の「=== 業務ルール ===」記述を削除
# 要求仕様ID: 統一化修正
# 対応設計書: .clinerules/08-database-design-guidelines.md

echo "=== notesセクション内の「=== 業務ルール ===」記述削除開始 ==="

# 対象ディレクトリ
TARGET_DIR="docs/design/database/table-details"

# バックアップディレクトリ作成
BACKUP_DIR="${TARGET_DIR}/backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 修正対象ファイル数をカウント
total_files=0
modified_files=0

echo "バックアップディレクトリ: $BACKUP_DIR"

# 全YAMLファイルを処理（TEMPLATEとbackupディレクトリは除外）
for file in "${TARGET_DIR}"/テーブル詳細定義YAML_*.yaml; do
    # ファイル名にTEMPLATEが含まれている場合はスキップ
    if [[ "$file" == *"TEMPLATE"* ]]; then
        echo "スキップ: $(basename "$file") (テンプレートファイル)"
        continue
    fi
    
    # ファイルが存在するかチェック
    if [[ ! -f "$file" ]]; then
        continue
    fi
    
    total_files=$((total_files + 1))
    filename=$(basename "$file")
    
    echo "処理中: $filename"
    
    # バックアップ作成
    cp "$file" "$BACKUP_DIR/"
    
    # 「=== 業務ルール ===」を含む行とその直後の「-」で始まる行を削除
    # sedを使用してnotesセクション内の該当記述を削除
    sed -i.tmp '
        /^[[:space:]]*- === 業務ルール ===/d
        /^[[:space:]]*- === 業務ルール ===/,/^[[:space:]]*- [^=]/ {
            /^[[:space:]]*- === 業務ルール ===/d
        }
    ' "$file"
    
    # 一時ファイル削除
    rm -f "${file}.tmp"
    
    # 修正されたかチェック
    if ! diff -q "$file" "$BACKUP_DIR/$filename" > /dev/null 2>&1; then
        modified_files=$((modified_files + 1))
        echo "✅ 修正完了: $filename"
    else
        echo "ℹ️  変更なし: $filename"
    fi
done

echo ""
echo "=== 修正結果サマリー ==="
echo "処理対象ファイル数: $total_files"
echo "修正されたファイル数: $modified_files"
echo "バックアップ場所: $BACKUP_DIR"
echo ""

if [[ $modified_files -gt 0 ]]; then
    echo "✨ notesセクション内の「=== 業務ルール ===」記述削除が完了しました！"
    echo ""
    echo "次のステップ:"
    echo "1. 修正内容を確認してください"
    echo "2. YAML検証ツールで整合性をチェックしてください"
    echo "3. 問題なければGitコミットしてください"
else
    echo "ℹ️  修正対象となるファイルはありませんでした"
fi

echo ""
echo "=== 修正完了 ==="
