#!/bin/bash
# 要求仕様ID: PLT.1-DB.1 - データベース初期データ投入自動化
# Prisma対応版のseed.tsファイル生成スクリプト

echo "========================================"
echo "Prisma seed.ts ファイル生成スクリプト"
echo "========================================"
echo

# Pythonの存在確認
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Pythonが見つかりません。Pythonをインストールしてください。"
    exit 1
fi

# Python実行コマンドの決定
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "✅ Python環境を確認しました ($PYTHON_CMD)"
echo

# 現在のディレクトリを確認
if [ ! -d "docs/design/database/data" ]; then
    echo "❌ SQLデータディレクトリが見つかりません: docs/design/database/data"
    echo "   正しいプロジェクトルートから実行してください。"
    exit 1
fi

echo "✅ SQLデータディレクトリを確認しました"
echo

# 出力ディレクトリの作成
if [ ! -d "src/database/prisma" ]; then
    echo "📁 出力ディレクトリを作成中: src/database/prisma"
    mkdir -p "src/database/prisma"
fi

echo "🚀 Prisma seed.tsファイルを生成中..."
echo

# Pythonスクリプトの実行
$PYTHON_CMD scripts/sql-to-seed-prisma-fixed.py --backup

if [ $? -ne 0 ]; then
    echo
    echo "❌ seed.tsファイルの生成に失敗しました"
    exit 1
fi

echo
echo "✅ seed.tsファイルの生成が完了しました！"
echo
echo "📋 次のステップ:"
echo "   1. npm run db:seed でデータベースに初期データを投入"
echo "   2. npm run dev でアプリケーションを起動"
echo
