# Vercelデプロイメントガイド

## 概要

このガイドでは、skill-report-webアプリケーションをVercelにデプロイする手順を説明します。

## 前提条件

- Vercelアカウントを持っていること
- PostgreSQLデータベース（Neon、Supabase、PlanetScale等）へのアクセス権限
- 必要なシークレット情報を準備していること

## セットアップ手順

### 1. Vercelプロジェクトの作成

#### 1.1 GitHubリポジトリと連携

1. [Vercel Dashboard](https://vercel.com/dashboard)にログイン
2. "Add New Project"をクリック
3. GitHubリポジトリ`sas-dx/skill-report-web`を選択
4. "Import"をクリック

#### 1.2 フレームワーク設定

Vercelは自動的にNext.jsプロジェクトを検出しますが、以下の設定を確認してください：

- **Framework Preset**: Next.js
- **Root Directory**: `./` (ルート)
- **Build Command**: `prisma generate --schema=src/database/prisma/schema.prisma && next build`
- **Output Directory**: `.next`
- **Install Command**: `npm install`

### 2. データベースのセットアップ（Neon推奨）

#### 2.1 Neonデータベースの作成

1. [Neon Console](https://console.neon.tech/)にログイン
2. 新しいプロジェクトを作成
3. データベース名: `skill_report_db`
4. リージョン: 日本に近いリージョン（Tokyo, Singapore等）を選択

#### 2.2 接続文字列の取得

Neonから以下の2つの接続文字列を取得します：

- **DATABASE_URL**: Pooled connection（推奨）
  ```
  postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/skill_report_db?sslmode=require&pgbouncer=true
  ```

- **DIRECT_URL**: Direct connection（マイグレーション用）
  ```
  postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/skill_report_db?sslmode=require
  ```

### 3. Vercel環境変数の設定

Vercelプロジェクトの設定画面（Settings > Environment Variables）で以下の環境変数を追加します：

#### 3.1 必須環境変数

```bash
# データベース接続（Neon）
DATABASE_URL="postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/skill_report_db?sslmode=require&pgbouncer=true"
DIRECT_URL="postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/skill_report_db?sslmode=require"

# NextAuth設定
NEXTAUTH_URL="https://your-project.vercel.app"
NEXTAUTH_SECRET="minimum-32-characters-long-random-string"

# JWT設定
JWT_SECRET="minimum-32-characters-long-random-string"

# 暗号化キー
ENCRYPTION_KEY="exactly-32-character-string-key"
```

#### 3.2 オプション環境変数

```bash
# メール設定（通知機能を使用する場合）
SMTP_HOST="smtp.example.com"
SMTP_PORT="587"
SMTP_USER="your-email@example.com"
SMTP_PASS="your-email-password"
SMTP_FROM="noreply@example.com"

# セキュリティ設定
BCRYPT_ROUNDS="12"
SESSION_TIMEOUT="3600"

# ファイルアップロード設定
UPLOAD_MAX_SIZE="10485760"
UPLOAD_ALLOWED_TYPES="image/jpeg,image/png,application/pdf"
```

#### 3.3 環境変数のスコープ設定

各環境変数に対して、適用する環境を選択します：

- ✅ Production
- ✅ Preview
- ✅ Development（ローカル開発で必要な場合）

### 4. シークレットの生成

強固なランダム文字列を生成するには：

```bash
# NEXTAUTH_SECRET と JWT_SECRET用（32文字以上）
openssl rand -base64 32

# ENCRYPTION_KEY用（正確に32文字）
openssl rand -hex 16
```

### 5. データベースマイグレーションの実行

#### 5.1 ローカルでのマイグレーション準備

```bash
# 環境変数を設定
export DATABASE_URL="your-neon-direct-url"

# Prismaクライアント生成
npm run db:generate

# マイグレーション実行
npx prisma migrate deploy --schema=src/database/prisma/schema.prisma

# 初期データ投入（オプション）
npm run db:seed
```

#### 5.2 Vercel経由でのマイグレーション実行

環境変数を設定した後、Vercelのビルドログで自動的にPrismaクライアントが生成されます。

### 6. デプロイの実行

#### 6.1 自動デプロイ

GitHubのmainブランチにプッシュすると、自動的にVercelにデプロイされます：

```bash
git push origin main
```

#### 6.2 手動デプロイ

Vercel Dashboardから手動でデプロイすることも可能です：

1. Vercel Dashboardでプロジェクトを選択
2. "Deployments"タブに移動
3. "Redeploy"をクリック

### 7. デプロイの確認

#### 7.1 ヘルスチェック

デプロイが完了したら、ヘルスチェックエンドポイントにアクセスして確認します：

```bash
curl https://your-project.vercel.app/api/health
```

期待されるレスポンス：
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "checks": {
    "application": "healthy",
    "database": "healthy"
  }
}
```

#### 7.2 ビルドログの確認

Vercel Dashboardの"Deployments"タブでビルドログを確認できます。エラーがある場合はここに表示されます。

## トラブルシューティング

### ビルドが失敗する

#### 問題: Prismaクライアント生成エラー

```
Error: @prisma/client did not initialize yet
```

**解決策**:
1. `vercel.json`のbuildCommandを確認
2. 環境変数`DATABASE_URL`が正しく設定されているか確認

#### 問題: 環境変数が見つからない

```
Error: DATABASE_URL is not defined
```

**解決策**:
1. Vercel Dashboard > Settings > Environment Variablesを確認
2. 環境変数のスコープ（Production/Preview/Development）を確認
3. デプロイを再実行

### データベース接続エラー

#### 問題: データベースに接続できない

```
Error: Can't reach database server
```

**解決策**:
1. Neonデータベースが起動しているか確認
2. IPアドレス制限がないか確認（Neonはデフォルトで全IPを許可）
3. 接続文字列が正しいか確認（特にSSLモード）

#### 問題: Connection pooling エラー

```
Error: prepared statement already exists
```

**解決策**:
DATABASE_URLに`&pgbouncer=true`が含まれているか確認：
```
postgresql://...?sslmode=require&pgbouncer=true
```

### パフォーマンスの問題

#### 問題: 初回アクセスが遅い

**原因**: Vercelのコールドスタート

**解決策**:
1. Vercel Proプランにアップグレード（常時実行）
2. キャッシュ戦略の最適化
3. ISRやSSGの活用

#### 問題: データベースクエリが遅い

**解決策**:
1. Neonの接続プーリングを使用（`pgbouncer=true`）
2. データベースインデックスを最適化
3. クエリの最適化

### 環境変数の問題

#### 問題: 環境変数がアプリケーションに反映されない

**解決策**:
1. 環境変数を追加/変更した後は必ず再デプロイ
2. ビルド時に必要な環境変数は`next.config.js`で明示的に参照

## カスタムドメインの設定

### 1. ドメインの追加

1. Vercel Dashboard > Settings > Domainsに移動
2. "Add Domain"をクリック
3. カスタムドメイン名を入力（例: `skill-report.example.com`）
4. DNSレコードの設定手順に従う

### 2. DNSレコードの設定

Vercelが提供するIPアドレスまたはCNAMEを、ドメインのDNS設定に追加します：

```
Type: A or CNAME
Name: skill-report
Value: 76.76.21.21 (Vercelが提供)
```

### 3. SSL証明書の自動発行

Vercelは自動的にLet's Encrypt SSL証明書を発行します。通常、数分以内に有効になります。

### 4. NEXTAUTH_URLの更新

カスタムドメインを設定したら、環境変数を更新します：

```bash
NEXTAUTH_URL="https://skill-report.example.com"
```

## モニタリングとログ

### デプロイメントログ

Vercel Dashboard > Deployments > ログを確認

### ランタイムログ

Vercel Dashboard > プロジェクト > Logsで確認可能
- リアルタイムログ
- エラーログ
- アクセスログ

### アナリティクス（Proプラン）

- ページビュー
- レスポンス時間
- エラー率

## セキュリティ設定

### 環境変数の保護

- 環境変数は暗号化されて保存されます
- `.env.local`ファイルは`.gitignore`に含まれています

### CORS設定

必要に応じて`next.config.js`でCORS設定を追加：

```javascript
async headers() {
  return [
    {
      source: '/api/:path*',
      headers: [
        { key: 'Access-Control-Allow-Origin', value: 'https://your-domain.com' },
      ],
    },
  ];
}
```

## CI/CDとの連携

### GitHub Actions

GitHub Actionsと連携する場合、Vercel CLIを使用します：

```yaml
- name: Deploy to Vercel
  env:
    VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
    VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
    VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}
  run: |
    npm i -g vercel
    vercel --prod --token=$VERCEL_TOKEN
```

## バックアップとロールバック

### 以前のデプロイへのロールバック

1. Vercel Dashboard > Deployments
2. ロールバックしたいデプロイメントを選択
3. "Promote to Production"をクリック

### データベースバックアップ

Neonは自動バックアップを提供しています（Proプラン）。
手動バックアップも可能：

```bash
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d).sql
```

## サポート

- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [Neon Documentation](https://neon.tech/docs)
- [Prisma Documentation](https://www.prisma.io/docs)

## よくある質問

### Q: Vercelの無料プランで使えますか？

A: はい、開発・テスト目的であれば無料プランで十分です。本番運用にはProプラン推奨。

### Q: データベースはどこでホストすべきですか？

A: Neon（PostgreSQL）を推奨します。Vercelとの統合が簡単で、接続プーリングをサポートしています。

### Q: 環境変数はどこで確認できますか？

A: Vercel Dashboard > Settings > Environment Variablesで確認・編集できます。

### Q: デプロイに失敗しました

A: ビルドログを確認してください。多くの場合、環境変数の設定ミスかデータベース接続の問題です。
