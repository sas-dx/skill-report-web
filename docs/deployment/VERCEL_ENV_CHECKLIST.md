# Vercel環境変数設定チェックリスト

## はじめに

このチェックリストに従って、Vercelに必要な環境変数を設定してください。
すべての環境変数を設定後、PR #36をmainブランチにマージすることでデプロイが成功します。

## 設定手順

### ステップ 1: Vercel Dashboardにアクセス

1. [Vercel Dashboard](https://vercel.com/dashboard)にログイン
2. `skill-report-web`プロジェクトを選択
3. **Settings** > **Environment Variables** に移動

---

## 必須環境変数の設定

### 📋 データベース設定（Neon推奨）

#### DATABASE_URL
```
Name: DATABASE_URL
Value: postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/skill_report_db?sslmode=require&pgbouncer=true
```
- [ ] 環境: Production ✓
- [ ] 環境: Preview ✓
- [ ] 環境: Development (オプション)

**取得方法:**
1. [Neon Console](https://console.neon.tech/)にログイン
2. プロジェクトを選択 → **Connection Details**
3. **Pooled connection**の文字列をコピー
4. 末尾に`&pgbouncer=true`が含まれていることを確認

#### DIRECT_URL
```
Name: DIRECT_URL
Value: postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/skill_report_db?sslmode=require
```
- [ ] 環境: Production ✓
- [ ] 環境: Preview ✓
- [ ] 環境: Development (オプション)

**取得方法:**
1. Neon Console → **Connection Details**
2. **Direct connection**の文字列をコピー
3. pgbouncer部分は**含めない**

---

### 🔐 認証・セキュリティ設定

#### NEXTAUTH_URL
```
Name: NEXTAUTH_URL
Value: https://your-project.vercel.app
```
- [ ] 環境: Production ✓
- [ ] 環境: Preview → `https://$VERCEL_URL` (動的URL)
- [ ] 環境: Development → `http://localhost:3000`

**注意:**
- Productionはカスタムドメインまたは`.vercel.app`ドメイン
- Previewは`https://$VERCEL_URL`を使用（Vercel変数）

#### NEXTAUTH_SECRET
```
Name: NEXTAUTH_SECRET
Value: <生成された32文字以上のランダム文字列>
```
- [ ] 環境: Production ✓
- [ ] 環境: Preview ✓
- [ ] 環境: Development ✓

**生成方法:**
```bash
openssl rand -base64 32
```
または
```bash
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

#### JWT_SECRET
```
Name: JWT_SECRET
Value: <生成された32文字以上のランダム文字列>
```
- [ ] 環境: Production ✓
- [ ] 環境: Preview ✓
- [ ] 環境: Development ✓

**生成方法:**
```bash
openssl rand -base64 32
```

**注意:** NEXTAUTH_SECRETとは**異なる値**を使用してください

#### ENCRYPTION_KEY
```
Name: ENCRYPTION_KEY
Value: <正確に32文字の16進数文字列>
```
- [ ] 環境: Production ✓
- [ ] 環境: Preview ✓
- [ ] 環境: Development ✓

**生成方法:**
```bash
openssl rand -hex 16
```

**注意:** 必ず32文字（16バイト × 2）である必要があります

---

## オプション環境変数（機能に応じて設定）

### 📧 メール設定（通知機能を使用する場合）

#### SMTP_HOST
```
Name: SMTP_HOST
Value: smtp.gmail.com
```
- [ ] 環境: Production
- [ ] 環境: Preview
- [ ] 環境: Development

#### SMTP_PORT
```
Name: SMTP_PORT
Value: 587
```
- [ ] 環境: Production
- [ ] 環境: Preview
- [ ] 環境: Development

#### SMTP_USER
```
Name: SMTP_USER
Value: your-email@gmail.com
```
- [ ] 環境: Production
- [ ] 環境: Preview
- [ ] 環境: Development

#### SMTP_PASS
```
Name: SMTP_PASS
Value: your-app-password
```
- [ ] 環境: Production
- [ ] 環境: Preview
- [ ] 環境: Development

**注意:** Gmailの場合はアプリパスワードを使用

#### SMTP_FROM
```
Name: SMTP_FROM
Value: noreply@your-domain.com
```
- [ ] 環境: Production
- [ ] 環境: Preview
- [ ] 環境: Development

---

### 🔧 アプリケーション設定

#### NODE_ENV
```
Name: NODE_ENV
Value: production
```
- [ ] 環境: Production ✓

**注意:** Vercelが自動設定するため、通常は不要

#### PORT
```
Name: PORT
Value: 3000
```

**注意:** Vercelが自動設定するため、通常は不要

---

### 📊 監視・分析（オプション）

#### SENTRY_DSN
```
Name: SENTRY_DSN
Value: https://xxx@xxx.ingest.sentry.io/xxx
```
- [ ] 環境: Production
- [ ] 環境: Preview
- [ ] 環境: Development

#### GOOGLE_ANALYTICS_ID
```
Name: GOOGLE_ANALYTICS_ID
Value: G-XXXXXXXXXX
```
- [ ] 環境: Production

---

## 設定確認チェックリスト

### ✅ 最小限の必須環境変数（これだけで動作）

- [ ] **DATABASE_URL** (Production, Preview)
- [ ] **DIRECT_URL** (Production, Preview)
- [ ] **NEXTAUTH_URL** (Production, Preview, Development)
- [ ] **NEXTAUTH_SECRET** (Production, Preview, Development)
- [ ] **JWT_SECRET** (Production, Preview, Development)
- [ ] **ENCRYPTION_KEY** (Production, Preview, Development)

### ✅ セキュリティチェック

- [ ] すべてのシークレットは一意のランダム文字列
- [ ] NEXTAUTH_SECRETとJWT_SECRETは異なる値
- [ ] ENCRYPTION_KEYは正確に32文字
- [ ] DATABASE_URLにはpgbouncer=trueが含まれる
- [ ] DIRECT_URLにはpgbouncer=trueが含まれない
- [ ] 本番環境とプレビュー環境で同じシークレットを使用

---

## 設定後の確認手順

### 1. 環境変数の保存確認

すべての環境変数を設定したら、Vercelで**Save**をクリックします。

### 2. PR #36をマージ

```bash
# GitHub PR #36のページにアクセス
# https://github.com/sas-dx/skill-report-web/pull/36

# "Merge pull request"をクリック
# または、ローカルで以下を実行:

git checkout main
git pull origin main
git merge claude/fix-cicd-deployment-01959KPkkF5dhKZ9bGz8h96x
git push origin main
```

### 3. Vercelデプロイの確認

1. [Vercel Dashboard](https://vercel.com/dashboard) > **Deployments**
2. デプロイステータスを確認
3. ビルドログでエラーがないか確認

### 4. ヘルスチェック

デプロイ完了後、以下のURLにアクセス：

```bash
curl https://your-project.vercel.app/api/health
```

**期待されるレスポンス:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "checks": {
    "application": "healthy",
    "database": "healthy"
  },
  "performance": {
    "database": "15ms",
    "total": "20ms"
  }
}
```

### 5. アプリケーションの動作確認

1. `https://your-project.vercel.app`にアクセス
2. ログイン機能を確認
3. 主要機能が動作することを確認

---

## トラブルシューティング

### ❌ ビルドが失敗する

**症状:** Vercelのビルドログに`Error: DATABASE_URL is not defined`

**解決策:**
1. Environment Variablesで`DATABASE_URL`が設定されているか確認
2. 設定後、Redeploy（再デプロイ）を実行

### ❌ データベース接続エラー

**症状:** `Can't reach database server`

**解決策:**
1. Neonデータベースが起動しているか確認
2. DATABASE_URLとDIRECT_URLが正しいか確認
3. `sslmode=require`が含まれているか確認

### ❌ 認証エラー

**症状:** NextAuthのログインが機能しない

**解決策:**
1. `NEXTAUTH_URL`がデプロイ先のURLと一致しているか確認
2. `NEXTAUTH_SECRET`が設定されているか確認
3. HTTPSを使用しているか確認（本番環境）

### ❌ 環境変数が反映されない

**解決策:**
環境変数を追加・変更した後は**必ず再デプロイ**が必要です：
1. Vercel Dashboard > Deployments
2. 最新のデプロイの右側の"..."メニュー
3. "Redeploy"をクリック

---

## クイックコピー用テンプレート

以下のテンプレートをコピーして、実際の値に置き換えてください：

```bash
# データベース（Neonから取得）
DATABASE_URL="postgresql://user:pass@ep-xxx.region.aws.neon.tech/skill_report_db?sslmode=require&pgbouncer=true"
DIRECT_URL="postgresql://user:pass@ep-xxx.region.aws.neon.tech/skill_report_db?sslmode=require"

# 認証（openssl rand -base64 32で生成）
NEXTAUTH_URL="https://your-project.vercel.app"
NEXTAUTH_SECRET="<32文字以上のランダム文字列>"
JWT_SECRET="<32文字以上のランダム文字列（NEXTAUTHとは別）>"

# 暗号化（openssl rand -hex 16で生成）
ENCRYPTION_KEY="<正確に32文字の16進数>"
```

---

## さらに詳しい情報

- [Vercelデプロイメントガイド](./VERCEL_DEPLOYMENT_GUIDE.md)
- [Docker本番デプロイメントガイド](./DEPLOYMENT_GUIDE.md)
- [Vercel公式ドキュメント](https://vercel.com/docs)
- [Neon公式ドキュメント](https://neon.tech/docs)

---

## サポート

問題が解決しない場合は、以下を確認してください：

1. Vercelのビルドログ（詳細なエラーメッセージ）
2. Neonデータベースの接続設定
3. 環境変数のスコープ（Production/Preview/Development）

最終更新: 2024-01-01
