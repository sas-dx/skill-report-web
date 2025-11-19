# デプロイメント設定ガイド

## CI/CDワークフローの設定

### 概要

このディレクトリには、GitHub Actionsを使用したCI/CDパイプラインの設定ファイルが含まれています。

### ワークフローファイルの配置

GitHub Appの権限制限により、ワークフローファイルは自動的にプッシュできません。
以下の手順で手動で配置してください：

#### 手順

1. **ワークフローファイルのコピー**
   ```bash
   cp docs/deployment/ci-cd-workflow.yml .github/workflows/ci-cd.yml
   ```

2. **ファイルの追加とコミット**
   ```bash
   git add .github/workflows/ci-cd.yml
   git commit -m "ci: GitHub Actions CI/CDワークフローを追加"
   ```

3. **プッシュ**
   ```bash
   git push
   ```

### ワークフローの機能

`ci-cd-workflow.yml` には以下の機能が含まれています：

#### 1. コード品質チェック (quality-check)
- ESLintによる静的解析
- TypeScriptの型チェック
- コードフォーマットチェック

#### 2. ビルドテスト (build)
- Next.jsアプリケーションのビルド
- Prismaクライアントの生成
- ビルド成果物のアップロード

#### 3. ユニットテスト (test)
- PostgreSQLサービスコンテナを使用
- データベースマイグレーション実行
- カバレッジレポート生成
- Codecovへのアップロード（オプション）

#### 4. Dockerイメージビルド (docker-build)
- マルチステージビルド
- GitHub Container Registryへのプッシュ
- タグ管理（ブランチ、PR、SHA、latest）
- ビルドキャッシュの活用

#### 5. デプロイ
- **本番環境** (deploy-production): mainブランチへのプッシュ時
- **ステージング環境** (deploy-staging): developブランチへのプッシュ時

### トリガー条件

#### プッシュイベント
- `main`, `master`, `develop`, `release/**` ブランチ

#### プルリクエスト
- `main`, `master`, `develop` ブランチへのPR

### 必要なシークレット設定

本番デプロイを有効にする場合、以下のGitHub Secretsを設定してください：

#### デプロイ用（SSH経由の場合）
```
DEPLOY_HOST         # デプロイ先サーバーのホスト名
DEPLOY_USER         # SSHユーザー名
DEPLOY_SSH_KEY      # SSH秘密鍵
```

#### その他（オプション）
```
CODECOV_TOKEN       # Codecovトークン（カバレッジレポート用）
```

### デプロイ方法のカスタマイズ

ワークフローファイルの `deploy-production` および `deploy-staging` ジョブには、
コメントアウトされたデプロイ手順の例が含まれています。

使用する環境に応じて、以下のいずれかの方法でカスタマイズしてください：

#### SSH経由でのデプロイ
```yaml
- name: Deploy to server
  uses: appleboy/ssh-action@v1.0.0
  with:
    host: ${{ secrets.DEPLOY_HOST }}
    username: ${{ secrets.DEPLOY_USER }}
    key: ${{ secrets.DEPLOY_SSH_KEY }}
    script: |
      cd /opt/skill-report-web
      docker-compose pull
      docker-compose up -d
      docker-compose exec app npx prisma migrate deploy
```

#### AWS ECS へのデプロイ
```yaml
- name: Deploy to ECS
  uses: aws-actions/amazon-ecs-deploy-task-definition@v1
  with:
    task-definition: task-definition.json
    service: skill-report-service
    cluster: skill-report-cluster
```

#### Kubernetes へのデプロイ
```yaml
- name: Deploy to Kubernetes
  uses: azure/k8s-deploy@v4
  with:
    manifests: |
      k8s/deployment.yml
      k8s/service.yml
    images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
```

### Dockerイメージの利用

ビルドされたDockerイメージは以下の形式で取得できます：

```bash
# 最新版
docker pull ghcr.io/sas-dx/skill-report-web:latest

# 特定のブランチ
docker pull ghcr.io/sas-dx/skill-report-web:develop

# 特定のコミット
docker pull ghcr.io/sas-dx/skill-report-web:main-abc1234
```

### トラブルシューティング

#### ワークフローが起動しない
- `.github/workflows/` ディレクトリにファイルが正しく配置されているか確認
- トリガー条件（ブランチ名）が正しいか確認

#### ビルドが失敗する
- ローカルで `npm run build` が成功するか確認
- 環境変数が正しく設定されているか確認

#### テストが失敗する
- ローカルで `npm run test` が成功するか確認
- データベース接続設定を確認

#### Dockerイメージのプッシュが失敗する
- GitHub Package の権限設定を確認
- `GITHUB_TOKEN` に適切な権限があるか確認

## 関連ファイル

- `Dockerfile` - Dockerイメージのビルド定義
- `docker-compose.prod.yml` - 本番環境のDocker Compose設定
- `nginx.conf` - Nginxリバースプロキシ設定
- `.dockerignore` - Dockerビルドコンテキストの除外設定

## 参考資料

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
