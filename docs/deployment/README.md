# デプロイメント設定ガイド

## 📋 概要

このディレクトリには、skill-report-webアプリケーションのデプロイに関するドキュメントが含まれています。

## 🚀 クイックスタート

### Vercelへのデプロイ（推奨）

最も簡単で高速なデプロイ方法です：

1. **[環境変数設定チェックリスト](./VERCEL_ENV_CHECKLIST.md)**に従って環境変数を設定
2. mainブランチにマージ
3. 自動的にVercelにデプロイされます

詳細: [Vercelデプロイメントガイド](./VERCEL_DEPLOYMENT_GUIDE.md)

### Dockerへのデプロイ（セルフホスト）

自前のサーバーでホストする場合：

1. `.env.production.example`をコピーして`.env`を作成
2. `docker-compose -f docker-compose.prod.yml up -d`

詳細: [Dockerデプロイメントガイド](./DEPLOYMENT_GUIDE.md)

## 📚 ドキュメント一覧

### 1. [VERCEL_ENV_CHECKLIST.md](./VERCEL_ENV_CHECKLIST.md) ⭐ 必読
**Vercelへのデプロイ前に必ず確認**

- ✅ 環境変数設定の完全なチェックリスト
- ✅ コピー&ペースト用のテンプレート
- ✅ シークレット生成方法
- ✅ 設定後の確認手順

**対象者:** すべての開発者、DevOps担当者

### 2. [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md)
**Vercelデプロイの詳細ガイド**

- Vercelプロジェクトのセットアップ
- Neonデータベースとの連携
- カスタムドメイン設定
- トラブルシューティング
- モニタリングとログ

**対象者:** DevOps担当者、インフラ担当者

### 3. [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)
**Dockerデプロイの詳細ガイド**

- Docker Composeでのデプロイ
- PostgreSQLコンテナ設定
- Nginxリバースプロキシ
- SSL/TLS証明書設定
- バックアップとロールバック

**対象者:** セルフホスト担当者、オンプレミス環境管理者

### 4. [ci-cd-workflow.yml](./ci-cd-workflow.yml)
**GitHub Actions CI/CDワークフロー定義**

- コード品質チェック
- ビルドテスト
- Dockerイメージビルド
- 自動デプロイ設定

**対象者:** DevOps担当者

**注意:** GitHub Appの権限制限により、このファイルは手動で`.github/workflows/`に配置する必要があります。

## 🎯 デプロイ方法の選択

### Vercelを選ぶべき場合

- ✅ 最も簡単で高速なデプロイ
- ✅ 自動スケーリング
- ✅ グローバルCDN
- ✅ SSL証明書の自動発行
- ✅ メンテナンスフリー

**推奨環境:** 開発、ステージング、本番（SaaS型）

### Dockerを選ぶべき場合

- ✅ 完全なコントロール
- ✅ オンプレミス要件
- ✅ カスタムインフラ
- ✅ コスト最適化（大規模）

**推奨環境:** 本番（セルフホスト）、エンタープライズ環境

## 🔧 必須環境変数（両環境共通）

| 環境変数 | 説明 | 生成方法 |
|---------|------|---------|
| `DATABASE_URL` | PostgreSQL接続文字列（Pooled） | Neonから取得 |
| `DIRECT_URL` | PostgreSQL接続文字列（Direct） | Neonから取得 |
| `NEXTAUTH_URL` | アプリケーションURL | デプロイ先のURL |
| `NEXTAUTH_SECRET` | NextAuth署名キー | `openssl rand -base64 32` |
| `JWT_SECRET` | JWT署名キー | `openssl rand -base64 32` |
| `ENCRYPTION_KEY` | 暗号化キー（32文字） | `openssl rand -hex 16` |

詳細: [VERCEL_ENV_CHECKLIST.md](./VERCEL_ENV_CHECKLIST.md)

## 🛠️ トラブルシューティング

### ビルドエラー

**Vercel:**
1. [Vercel Dashboard](https://vercel.com/dashboard) > Deployments > ビルドログ確認
2. 環境変数が正しく設定されているか確認
3. [VERCEL_ENV_CHECKLIST.md](./VERCEL_ENV_CHECKLIST.md)を再確認

**Docker:**
1. `docker-compose logs app`でログ確認
2. `.env`ファイルが正しく設定されているか確認
3. [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)のトラブルシューティング参照

### データベース接続エラー

**共通:**
1. DATABASE_URLが正しいか確認
2. データベースが起動しているか確認
3. ネットワーク接続を確認

詳細: [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md#トラブルシューティング)

## CI/CDワークフローの設定（オプション）

GitHub Actionsを使用したCI/CDパイプラインの設定方法：

### 手順

1. **ワークフローファイルのコピー**
   ```bash
   cp docs/deployment/ci-cd-workflow.yml .github/workflows/ci-cd.yml
   ```

2. **ファイルの追加とコミット**
   ```bash
   git add .github/workflows/ci-cd.yml
   git commit -m "ci: GitHub Actions CI/CDワークフローを追加"
   git push
   ```

### ワークフローの機能

- コード品質チェック（ESLint、TypeScript）
- ビルドテスト
- ユニットテスト（PostgreSQL統合）
- Dockerイメージビルド（GHCR）
- 自動デプロイ（本番・ステージング）

詳細は [ci-cd-workflow.yml](./ci-cd-workflow.yml) を参照してください。

## 📞 サポート

問題が解決しない場合：

1. 各ガイドのトラブルシューティングセクション確認
2. [GitHub Issues](https://github.com/sas-dx/skill-report-web/issues)で報告
3. ログファイルとエラーメッセージを添付

## 🔄 更新履歴

- 2024-01-01: Vercel環境変数チェックリスト追加
- 2024-01-01: Vercelデプロイメントガイド追加
- 2024-01-01: Dockerデプロイメントガイド追加
- 2024-01-01: CI/CDワークフロー追加

---

**最終更新:** 2024-01-01
**メンテナー:** SAS Team
