#!/bin/bash
# 要求仕様ID: PLT.1-DOCKER.1 - 開発環境Docker化
# Docker環境でのseedファイル実行スクリプト

set -e

echo "🌱 Docker環境でのseedファイル実行を開始します..."

# PostgreSQLの準備完了を待機
echo "📡 PostgreSQLの準備完了を待機中..."
until docker-compose exec postgres pg_isready -U skill_user -d skill_report_db; do
  echo "⏳ PostgreSQLの準備を待機中..."
  sleep 2
done

echo "✅ PostgreSQLが準備完了しました"

# Prismaマイグレーションの実行
echo "🔄 Prismaマイグレーションを実行中..."
docker-compose exec app npx prisma migrate dev --schema=src/database/prisma/schema.prisma --name init

# Prismaクライアントの生成
echo "🔧 Prismaクライアントを生成中..."
docker-compose exec app npx prisma generate --schema=src/database/prisma/schema.prisma

# seedファイルの実行
echo "🌱 seedファイルを実行中..."
docker-compose exec app npx prisma db seed --schema=src/database/prisma/schema.prisma


