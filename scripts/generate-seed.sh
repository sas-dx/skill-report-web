#!/bin/bash
# SQLサンプルデータからseed.tsファイルを生成するスクリプト
# 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入自動化

set -e

# スクリプトのディレクトリを取得
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# デフォルト設定
SQL_DIR="$PROJECT_ROOT/docs/design/database/data"
OUTPUT_FILE="$PROJECT_ROOT/src/database/prisma/seed.ts"
BACKUP=false

# ヘルプ表示
show_help() {
    cat << EOF
SQLサンプルデータからPrisma seed.tsファイルを生成

使用方法:
    $0 [オプション]

オプション:
    -s, --sql-dir DIR     SQLファイルのディレクトリ (default: docs/design/database/data)
    -o, --output FILE     出力ファイル (default: src/database/prisma/seed.ts)
    -b, --backup          既存のseed.tsファイルをバックアップ
    -h, --help            このヘルプを表示

例:
    $0                                    # デフォルト設定で実行
    $0 --backup                           # バックアップ付きで実行
    $0 --sql-dir ./data --output ./seed.ts # カスタムパスで実行
EOF
}

# オプション解析
while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--sql-dir)
            SQL_DIR="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -b|--backup)
            BACKUP=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "不明なオプション: $1"
            show_help
            exit 1
            ;;
    esac
done

# Pythonの存在確認
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3が見つかりません。Python3をインストールしてください。"
    exit 1
fi

# SQLディレクトリの存在確認
if [ ! -d "$SQL_DIR" ]; then
    echo "❌ SQLディレクトリが見つかりません: $SQL_DIR"
    exit 1
fi

# 出力ディレクトリの作成
OUTPUT_DIR="$(dirname "$OUTPUT_FILE")"
mkdir -p "$OUTPUT_DIR"

echo "🚀 SQLサンプルデータからseed.tsファイルを生成します..."
echo "📁 SQLディレクトリ: $SQL_DIR"
echo "📄 出力ファイル: $OUTPUT_FILE"

# Pythonスクリプトを実行
PYTHON_ARGS="--sql-dir '$SQL_DIR' --output '$OUTPUT_FILE'"
if [ "$BACKUP" = true ]; then
    PYTHON_ARGS="$PYTHON_ARGS --backup"
fi

python3 "$SCRIPT_DIR/sql-to-seed.py" $PYTHON_ARGS

echo ""
echo "✅ seed.tsファイルの生成が完了しました！"
echo "🚀 実行方法:"
echo "   cd $PROJECT_ROOT"
echo "   npm run db:seed"
