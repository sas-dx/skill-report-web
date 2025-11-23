# デプロイメントガイド

## 概要

このガイドでは、skill-report-webアプリケーションを本番環境にデプロイする手順を説明します。

## 前提条件

- Docker および Docker Compose がインストールされていること
- PostgreSQL データベースへのアクセス権限があること
- 必要なシークレット情報（NEXTAUTH_SECRET等）を準備していること

## デプロイ手順

### 1. 環境変数の設定

本番環境用の環境変数ファイルを作成します：

```bash
cp .env.production.example .env
```

`.env` ファイルを編集して、以下の必須項目を設定してください：

#### 必須項目

```bash
# データベース接続
DATABASE_URL="postgresql://username:password@postgres:5432/skill_report_db"
DB_NAME="skill_report_db"
DB_USER="skill_user"
DB_PASSWORD="your-secure-password"

# NextAuth設定
NEXTAUTH_URL="https://your-domain.com"
NEXTAUTH_SECRET="minimum-32-characters-long-random-string"

# JWT設定
JWT_SECRET="minimum-32-characters-long-random-string"

# 暗号化キー
ENCRYPTION_KEY="exactly-32-character-string-key"
```

### 2. シークレットの生成

強固なランダム文字列を生成するには、以下のコマンドを使用します：

```bash
# NEXTAUTH_SECRET と JWT_SECRET用（32文字以上）
openssl rand -base64 32

# ENCRYPTION_KEY用（正確に32文字）
openssl rand -hex 16
```

### 3. Docker Composeでのデプロイ

#### 3.1 イメージのビルド

```bash
docker-compose -f docker-compose.prod.yml build
```

#### 3.2 コンテナの起動

```bash
docker-compose -f docker-compose.prod.yml up -d
```

#### 3.3 データベースマイグレーションの実行

```bash
docker-compose -f docker-compose.prod.yml exec app npx prisma migrate deploy --schema=src/database/prisma/schema.prisma
```

#### 3.4 データベースシードの実行（初回のみ）

```bash
docker-compose -f docker-compose.prod.yml exec app npm run db:seed
```

### 4. 動作確認

#### 4.1 ヘルスチェック

```bash
curl http://localhost:3000/api/health
```

期待されるレスポンス：
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "checks": {
    "application": "healthy",
    "database": "healthy"
  },
  "performance": {
    "database": "10ms",
    "total": "15ms"
  }
}
```

#### 4.2 コンテナログの確認

```bash
# アプリケーションログ
docker-compose -f docker-compose.prod.yml logs -f app

# データベースログ
docker-compose -f docker-compose.prod.yml logs -f postgres

# すべてのログ
docker-compose -f docker-compose.prod.yml logs -f
```

#### 4.3 コンテナステータスの確認

```bash
docker-compose -f docker-compose.prod.yml ps
```

## トラブルシューティング

### コンテナが起動しない

#### 問題: アプリケーションコンテナが起動しない

1. ログを確認：
```bash
docker-compose -f docker-compose.prod.yml logs app
```

2. 環境変数が正しく設定されているか確認：
```bash
docker-compose -f docker-compose.prod.yml config
```

3. ビルドをクリーンアップして再実行：
```bash
docker-compose -f docker-compose.prod.yml down -v
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d
```

#### 問題: データベースコンテナが起動しない

1. ポート5432が使用されていないか確認：
```bash
lsof -i :5432
```

2. PostgreSQLデータボリュームをクリーンアップ（データが失われます）：
```bash
docker-compose -f docker-compose.prod.yml down -v
docker volume rm skill-report-web_postgres_data
```

### ヘルスチェックが失敗する

#### 問題: /api/health が 503 を返す

1. データベース接続を確認：
```bash
docker-compose -f docker-compose.prod.yml exec postgres psql -U $DB_USER -d $DB_NAME -c "SELECT 1"
```

2. DATABASE_URL が正しいか確認：
```bash
docker-compose -f docker-compose.prod.yml exec app printenv DATABASE_URL
```

3. Prismaクライアントが正しく生成されているか確認：
```bash
docker-compose -f docker-compose.prod.yml exec app ls -la node_modules/.prisma
```

### ビルドエラー

#### 問題: Dockerビルドが失敗する

1. ビルドログを確認：
```bash
docker-compose -f docker-compose.prod.yml build --no-cache --progress=plain
```

2. Node.jsのバージョンを確認（Dockerfile内）：
```dockerfile
FROM node:18-alpine AS builder
```

3. package.jsonの依存関係を確認：
```bash
npm install
npm run build
```

### パフォーマンスの問題

#### 問題: アプリケーションの起動が遅い

1. ヘルスチェックの start-period を延長（docker-compose.prod.yml）：
```yaml
healthcheck:
  start_period: 120s  # 60秒から120秒に延長
```

2. コンテナリソースを増やす：
```yaml
app:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 2G
```

## メンテナンス

### コンテナの再起動

```bash
# アプリケーションコンテナのみ
docker-compose -f docker-compose.prod.yml restart app

# すべてのコンテナ
docker-compose -f docker-compose.prod.yml restart
```

### ログのローテーション

ログは自動的にローテーションされます（設定: max-size: 10m, max-file: 3）

手動でクリアする場合：
```bash
docker-compose -f docker-compose.prod.yml down
docker system prune -a
```

### データベースバックアップ

```bash
# バックアップ作成
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U $DB_USER $DB_NAME > backup_$(date +%Y%m%d_%H%M%S).sql

# バックアップからリストア
docker-compose -f docker-compose.prod.yml exec -T postgres psql -U $DB_USER $DB_NAME < backup_20240101_120000.sql
```

### アプリケーションの更新

```bash
# 1. 最新のコードを取得
git pull origin main

# 2. イメージを再ビルド
docker-compose -f docker-compose.prod.yml build

# 3. コンテナを再起動（ダウンタイムあり）
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# 4. マイグレーションを実行
docker-compose -f docker-compose.prod.yml exec app npx prisma migrate deploy --schema=src/database/prisma/schema.prisma
```

## セキュリティ

### SSL/TLS証明書の設定

Nginxを使用してHTTPSを有効にする場合：

1. SSL証明書を配置：
```bash
mkdir -p ssl
# 証明書ファイルをssl/ディレクトリに配置
cp /path/to/certificate.crt ssl/
cp /path/to/private.key ssl/
```

2. nginx.confのHTTPSセクションのコメントを外す

3. Nginxコンテナを再起動：
```bash
docker-compose -f docker-compose.prod.yml restart nginx
```

### ファイアウォール設定

必要なポートのみを開放してください：

```bash
# HTTP/HTTPS（Nginx使用時）
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# 直接アクセスする場合（Nginxなし）
sudo ufw allow 3000/tcp

# PostgreSQL（外部アクセスが必要な場合のみ）
# sudo ufw allow 5432/tcp  # 注意: 本番環境では推奨されません
```

## モニタリング

### コンテナリソース使用状況

```bash
docker stats
```

### ディスク使用状況

```bash
docker system df
```

### データベース接続数

```bash
docker-compose -f docker-compose.prod.yml exec postgres psql -U $DB_USER -d $DB_NAME -c "SELECT count(*) FROM pg_stat_activity;"
```

## 関連ファイル

- `Dockerfile` - Dockerイメージのビルド定義
- `docker-compose.prod.yml` - 本番環境のDocker Compose設定
- `nginx.conf` - Nginxリバースプロキシ設定
- `.dockerignore` - Dockerビルドコンテキストの除外設定
- `.env.production.example` - 本番環境変数のテンプレート

## サポート

問題が解決しない場合は、以下を確認してください：

1. [GitHub Issues](https://github.com/sas-dx/skill-report-web/issues)
2. ログファイル（`docker-compose logs`）
3. システムリソース（CPU、メモリ、ディスク容量）
