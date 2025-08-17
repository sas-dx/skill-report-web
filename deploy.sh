#!/bin/bash
# 要求仕様ID: PLT.1-DEPLOY.1 - デプロイスクリプト

set -e

echo "================================"
echo "年間スキル報告書WEB デプロイスクリプト"
echo "================================"

# 環境変数チェック
if [ ! -f .env ]; then
    echo "❌ エラー: .envファイルが見つかりません"
    echo "👉 .env.exampleをコピーして.envを作成してください"
    exit 1
fi

# デプロイ環境選択
echo ""
echo "デプロイ環境を選択してください:"
echo "1) 開発環境 (docker-compose.yml)"
echo "2) 本番環境 (docker-compose.prod.yml)"
read -p "選択 (1 or 2): " ENV_CHOICE

case $ENV_CHOICE in
    1)
        COMPOSE_FILE="docker-compose.yml"
        ENV_NAME="開発環境"
        ;;
    2)
        COMPOSE_FILE="docker-compose.prod.yml"
        ENV_NAME="本番環境"
        ;;
    *)
        echo "❌ 無効な選択です"
        exit 1
        ;;
esac

echo ""
echo "📦 $ENV_NAME にデプロイします..."
echo ""

# 既存のコンテナを停止
echo "🛑 既存のコンテナを停止中..."
docker-compose -f $COMPOSE_FILE down

# イメージをビルド
echo ""
echo "🔨 Dockerイメージをビルド中..."
docker-compose -f $COMPOSE_FILE build --no-cache

# コンテナを起動
echo ""
echo "🚀 コンテナを起動中..."
docker-compose -f $COMPOSE_FILE up -d

# 起動確認
echo ""
echo "⏳ サービスの起動を待機中..."
sleep 10

# データベースマイグレーション実行
echo ""
echo "🗄️ データベースマイグレーションを実行中..."
docker-compose -f $COMPOSE_FILE exec app npm run db:migrate || true

# Prismaクライアント生成
echo ""
echo "🔧 Prismaクライアントを生成中..."
docker-compose -f $COMPOSE_FILE exec app npm run db:generate || true

# データベースシード実行（開発環境のみ）
if [ "$ENV_CHOICE" = "1" ]; then
    read -p "📝 シードデータを投入しますか？ (y/n): " SEED_CHOICE
    if [ "$SEED_CHOICE" = "y" ]; then
        echo "🌱 シードデータを投入中..."
        docker-compose -f $COMPOSE_FILE exec app npm run db:seed
    fi
fi

# ヘルスチェック
echo ""
echo "🏥 ヘルスチェック中..."
for i in {1..5}; do
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ アプリケーションが正常に起動しました！"
        break
    fi
    echo "⏳ 待機中... ($i/5)"
    sleep 5
done

# デプロイ完了
echo ""
echo "================================"
echo "✅ デプロイが完了しました！"
echo "================================"
echo ""
echo "📌 アクセスURL:"
echo "   - アプリケーション: http://localhost:3000"
if [ "$ENV_CHOICE" = "1" ]; then
    echo "   - pgAdmin: http://localhost:8080"
    echo "     Email: admin@example.com"
    echo "     Password: admin123"
fi
echo ""
echo "📋 便利なコマンド:"
echo "   - ログ確認: docker-compose -f $COMPOSE_FILE logs -f"
echo "   - 停止: docker-compose -f $COMPOSE_FILE down"
echo "   - 再起動: docker-compose -f $COMPOSE_FILE restart"
echo ""