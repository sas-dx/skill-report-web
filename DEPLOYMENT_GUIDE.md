# Neon + Vercel デプロイガイド：年間スキル報告書WEB化PJT

## 📋 デプロイ準備チェックリスト

- [x] プロジェクト設定確認
- [x] Vercel設定ファイル作成
- [ ] Neon PostgreSQL設定
- [ ] 環境変数設定
- [ ] デプロイ実行
- [ ] 動作確認

## 🎯 必要なアカウント

1. **Neon**: PostgreSQLデータベース
   - URL: https://neon.tech/
   - プラン: Free Tier（開発用）または Pro（本番用）

2. **Vercel**: Next.jsホスティング
   - URL: https://vercel.com/
   - プラン: Hobby（無料）または Pro（本番用）

## 🗄️ STEP 1: Neon PostgreSQL設定

### 1-1. Neon アカウント作成・ログイン

1. **https://neon.tech/** にアクセス
2. **「Sign Up」** または **「Get Started for Free」** をクリック
3. GitHub/Google/Email でアカウント作成
4. ダッシュボードにログイン

### 1-2. データベースプロジェクト作成

1. **「Create Project」** をクリック
2. プロジェクト設定：
   ```
   Project Name: skill-report-web
   Database Name: skill_report_db
   Region: Asia Pacific (Singapore) または US East
   ```
3. **「Create Project」** をクリック

### 1-3. 接続情報の取得

1. プロジェクト作成後、**「Dashboard」** にアクセス
2. **「Connection Details」** セクションで接続文字列をコピー
3. 形式：
   ```
   postgresql://username:password@ep-xxx-xxx.region.aws.neon.tech/skill_report_db?sslmode=require
   ```

### 1-4. データベーススキーマ作成

1. **「SQL Editor」** タブを開く
2. 以下のSQLを実行してテーブル作成：

```sql
-- 主要テーブルの作成（簡略版）
CREATE TABLE IF NOT EXISTS "MST_Employee" (
    "emp_id" SERIAL PRIMARY KEY,
    "emp_no" VARCHAR(20) UNIQUE NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    "email" VARCHAR(255) UNIQUE NOT NULL,
    "department_id" INTEGER,
    "position_id" INTEGER,
    "hire_date" DATE,
    "status" VARCHAR(20) DEFAULT 'ACTIVE',
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "MST_Department" (
    "dept_id" SERIAL PRIMARY KEY,
    "dept_code" VARCHAR(20) UNIQUE NOT NULL,
    "dept_name" VARCHAR(100) NOT NULL,
    "parent_dept_id" INTEGER,
    "level" INTEGER DEFAULT 1,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 追加のテーブルは必要に応じてschema.prismaから生成
```

## 🚀 STEP 2: Vercel設定

### 2-1. Vercel アカウント作成・ログイン

1. **https://vercel.com/** にアクセス
2. **「Sign Up」** をクリック
3. GitHubアカウントでログイン（推奨）
4. ダッシュボードにアクセス

### 2-2. GitHubリポジトリとの連携

1. Vercelダッシュボードで **「New Project」** をクリック
2. **「Import Git Repository」** を選択
3. GitHubリポジトリ `skill-report-web` を選択
4. **「Import」** をクリック

### 2-3. プロジェクト設定

1. **Build and Output Settings:**
   ```
   Framework Preset: Next.js
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   ```

2. **Root Directory:** 
   ```
   . (ルートディレクトリ)
   ```

## ⚙️ STEP 3: 環境変数設定

### 3-1. Vercel環境変数設定

1. Vercelプロジェクトダッシュボードで **「Settings」** タブを開く
2. **「Environment Variables」** セクションに移動
3. 以下の環境変数を追加：

#### 必須環境変数

| 変数名 | 値 | 説明 |
|--------|-----|------|
| `DATABASE_URL` | `postgresql://username:password@ep-xxx.neon.tech/skill_report_db?sslmode=require` | Neonから取得した接続文字列 |
| `NEXTAUTH_URL` | `https://your-app-name.vercel.app` | デプロイ後のVercel URL |
| `NEXTAUTH_SECRET` | `your-nextauth-secret-32-chars-min` | ランダムな32文字以上の文字列 |
| `JWT_SECRET` | `your-jwt-secret-32-chars-min` | ランダムな32文字以上の文字列 |
| `ENCRYPTION_KEY` | `your-32-character-encryption-key` | 正確に32文字の暗号化キー |

#### 環境変数の設定手順

1. **「Add New」** をクリック
2. **Name:** `DATABASE_URL`
3. **Value:** Neonの接続文字列をペースト
4. **Environment:** `Production`, `Preview`, `Development` 全てにチェック
5. **「Save」** をクリック

**⚠️ セキュリティキーの生成方法：**
```bash
# Node.jsでランダムキー生成
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# または、オンラインツール使用
# https://www.random.org/strings/
```

### 3-2. 本番環境用追加設定

追加で設定推奨の環境変数：

| 変数名 | 値の例 | 説明 |
|--------|--------|------|
| `NODE_ENV` | `production` | 本番環境フラグ |
| `LOG_LEVEL` | `error` | ログレベル |
| `SMTP_HOST` | `smtp.gmail.com` | メール送信設定（オプション） |
| `SMTP_PORT` | `587` | メールポート |
| `SMTP_USER` | `your-email@gmail.com` | メールユーザー |
| `SMTP_PASS` | `your-app-password` | メールパスワード |

## 🛠️ STEP 4: ビルド設定最適化

### 4-1. Package.json最適化

プロジェクトの `package.json` に以下のスクリプトが含まれていることを確認：

```json
{
  "scripts": {
    "build": "next build",
    "start": "next start",
    "db:generate": "prisma generate --schema=src/database/prisma/schema.prisma",
    "db:deploy": "prisma db push --schema=src/database/prisma/schema.prisma"
  }
}
```

### 4-2. Vercel Build Settings

Vercelプロジェクト設定で：

1. **「Settings」** → **「General」**
2. **Build & Development Settings:**
   ```
   Build Command: npm run build
   Output Directory: .next
   Install Command: npm install
   Development Command: npm run dev
   ```

## 🎯 STEP 5: デプロイ実行

### 5-1. 手動デプロイ

1. Vercelダッシュボードの **「Deployments」** タブ
2. **「Deploy」** ボタンをクリック
3. デプロイ進行状況を監視

### 5-2. 自動デプロイ設定

1. **「Settings」** → **「Git」**
2. **Production Branch:** `master` または `main`
3. **「Auto-deploy commits to main branch」** を有効化

### 5-3. デプロイ状況確認

デプロイログで以下を確認：
- ✅ Dependencies installation
- ✅ TypeScript compilation  
- ✅ Next.js build
- ✅ Prisma client generation
- ✅ Function optimization

## 🔧 STEP 6: データベース初期化

### 6-1. Prisma Database Push

デプロイ後、Vercel Function内でデータベーススキーマを同期：

```bash
# ローカルで実行（Neonに接続）
npx prisma db push --schema=src/database/prisma/schema.prisma
npx prisma generate --schema=src/database/prisma/schema.prisma
```

### 6-2. サンプルデータ投入

```bash
# 必要に応じてサンプルデータ投入
npx prisma db seed
```

## ✅ STEP 7: 動作確認

### 7-1. 基本動作確認

1. **デプロイ完了通知確認**
   - Vercelからの完了メール
   - デプロイURL: `https://your-app-name.vercel.app`

2. **アプリケーション動作確認**
   ```
   ✅ ログイン画面表示
   ✅ ダッシュボード表示  
   ✅ プロフィール管理
   ✅ スキルマップ表示
   ✅ データベース接続
   ```

### 7-2. API エンドポイント確認

主要APIの動作確認：
```
✅ GET /api/auth/me - ユーザー情報取得
✅ GET /api/profiles/[userId] - プロフィール取得
✅ GET /api/skills/[userId] - スキル情報取得
✅ GET /api/dashboard/settings - 設定取得
```

### 7-3. パフォーマンス確認

- **ページ読み込み時間:** < 3秒
- **API応答時間:** < 1秒
- **データベース接続:** 正常
- **ビルドサイズ:** 最適化済み

## 🚨 トラブルシューティング

### よくある問題と解決方法

#### 1. データベース接続エラー
```
Error: P1001: Can't reach database server
```
**解決方法:**
- Neon接続文字列の確認
- SSL設定 `?sslmode=require` の確認
- IP制限設定の確認

#### 2. 環境変数エラー
```
Error: Missing environment variable
```
**解決方法:**
- Vercel環境変数設定の確認
- 変数名のタイポ確認
- すべての環境（Production/Preview/Development）での設定確認

#### 3. ビルドエラー
```
Type Error: Property does not exist
```
**解決方法:**
- TypeScript型定義の確認
- Prisma Client再生成: `npx prisma generate`
- 依存関係の確認: `npm install`

#### 4. 認証エラー
```
Error: NextAuth configuration error
```
**解決方法:**
- `NEXTAUTH_URL` の確認（正しいVercel URLに設定）
- `NEXTAUTH_SECRET` の設定確認
- JWT_SECRET の設定確認

### デバッグ手順

1. **Vercelログ確認**
   ```
   Vercel Dashboard → Functions → View Function Logs
   ```

2. **Neonログ確認**
   ```
   Neon Dashboard → Monitoring → Query Logs
   ```

3. **ローカルでの動作確認**
   ```bash
   # 本番環境変数を使用してローカル確認
   cp .env.example .env.local
   # .env.localに本番環境変数を設定
   npm run dev
   ```

## 🔐 セキュリティ設定

### 必須セキュリティ設定

1. **環境変数の暗号化**
   - Vercel環境変数は自動暗号化
   - 秘密鍵の定期ローテーション

2. **HTTPS強制**
   - Vercelは自動HTTPS
   - カスタムドメインでもSSL証明書自動発行

3. **セキュリティヘッダー**
   - CSPの設定
   - X-Frame-Options設定済み
   - XSS Protection有効

## 📊 監視・運用

### パフォーマンス監視

1. **Vercel Analytics**
   - ページ読み込み時間
   - Core Web Vitals
   - エラー率

2. **Neon Monitoring**  
   - データベース接続数
   - クエリ実行時間
   - ストレージ使用量

### アラート設定

1. **Vercel Notifications**
   - デプロイ失敗通知
   - 関数エラー通知

2. **Neon Alerts**
   - 接続上限アラート
   - ストレージ使用量アラート

## 🎉 デプロイ完了

以上の手順でNeon + Vercelを使用した年間スキル報告書WEB化アプリケーションのデプロイが完了します。

### 最終確認チェックリスト

- [ ] Neonデータベース作成・接続確認
- [ ] Vercelプロジェクト作成・デプロイ確認  
- [ ] 環境変数設定完了
- [ ] アプリケーション動作確認
- [ ] セキュリティ設定確認
- [ ] 監視設定確認

### サポート情報

- **プロジェクト管理者:** SAS Team
- **技術サポート:** GitHub Issues
- **緊急時連絡:** プロジェクト管理者まで

**🎯 デプロイURL:** `https://your-app-name.vercel.app`

---

*このガイドは年間スキル報告書WEB化プロジェクト専用に作成されています。*
