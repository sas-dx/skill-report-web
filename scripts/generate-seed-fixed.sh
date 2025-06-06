#!/bin/bash
# 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入自動化
# SQLサンプルデータからPrisma seed.tsファイルを生成（修正版）

set -e

echo "🔧 SQLサンプルデータからPrisma seed.tsファイルを生成します..."

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Pythonスクリプトのパス
PYTHON_SCRIPT="$SCRIPT_DIR/sql-to-seed-fixed.py"
SQL_DATA_DIR="$PROJECT_ROOT/docs/design/database/data"
OUTPUT_FILE="$PROJECT_ROOT/src/database/prisma/seed.ts"

# Pythonスクリプトが存在するかチェック
if [ ! -f "$PYTHON_SCRIPT" ]; then
    echo "❌ エラー: Pythonスクリプトが見つかりません: $PYTHON_SCRIPT"
    exit 1
fi

# SQLデータディレクトリが存在するかチェック
if [ ! -d "$SQL_DATA_DIR" ]; then
    echo "❌ エラー: SQLデータディレクトリが見つかりません: $SQL_DATA_DIR"
    exit 1
fi

# 既存のseed.tsファイルをバックアップ
if [ -f "$OUTPUT_FILE" ]; then
    BACKUP_FILE="${OUTPUT_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "📁 既存のseed.tsファイルをバックアップします: $BACKUP_FILE"
    cp "$OUTPUT_FILE" "$BACKUP_FILE"
fi

# Pythonスクリプトを実行
echo "🐍 Pythonスクリプトを実行中..."
python3 "$PYTHON_SCRIPT" \
    --sql-dir "$SQL_DATA_DIR" \
    --output "$OUTPUT_FILE"

# 実行結果をチェック
if [ $? -eq 0 ]; then
    echo "✅ seed.tsファイルの生成が完了しました！"
    echo "📁 出力ファイル: $OUTPUT_FILE"
    echo ""
    echo "🚀 次のステップ:"
    echo "   1. 生成されたseed.tsファイルを確認"
    echo "   2. npm run db:seed でデータベースに初期データを投入"
    echo ""
    echo "💡 使用方法:"
    echo "   cd $PROJECT_ROOT"
    echo "   npm run db:seed"
else
    echo "❌ エラー: seed.tsファイルの生成に失敗しました"
    exit 1
fi
