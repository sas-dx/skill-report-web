# CI/CD セットアップガイド

## GitHub Actions 統合テストワークフロー設定

### 概要

統合テストを GitHub Actions で自動実行するためのワークフロー設定です。

### セットアップ手順

#### 1. ワークフローファイルの配置

テンプレートファイル `docs/testing/integration-test.yml.template` を以下の場所にコピーしてください：

```bash
cp docs/testing/integration-test.yml.template .github/workflows/integration-test.yml
```

#### 2. リポジトリへのコミット

```bash
git add .github/workflows/integration-test.yml
git commit -m "ci: GitHub Actions統合テストワークフロー追加"
git push
```

### ワークフロー内容

#### 自動実行トリガー

- `main`, `develop` ブランチへのプッシュ
- `main`, `develop` ブランチへのプルリクエスト
- `claude/**` ブランチへのプッシュ

#### 実行ジョブ

1. **Integration Test Job**
   - PostgreSQL 15 テストデータベースのセットアップ
   - Prisma マイグレーション実行
   - API統合テスト実行
   - カバレッジレポート生成
   - Codecov へのアップロード
   - PR へのカバレッジ結果コメント

2. **Database Test Job**
   - データベース専用テスト実行
   - テスト結果のアーティファクトアップロード

3. **Quality Gate Job**
   - 全テスト成功確認
   - 品質ゲート判定（80%カバレッジ以上）

### 品質ゲート基準

| 指標 | 目標値 |
|------|--------|
| 統合テストカバレッジ | 80%以上 |
| 全テストケース成功率 | 100% |
| データベーステスト成功率 | 100% |

### トラブルシューティング

#### PostgreSQL接続エラー

GitHub Actions のサービスコンテナが起動していることを確認：

```yaml
services:
  postgres:
    image: postgres:15-alpine
    options: >-
      --health-cmd "pg_isready -U test_user -d skill_report_test_db"
```

#### Prismaマイグレーションエラー

環境変数 `DATABASE_URL` が正しく設定されていることを確認：

```yaml
env:
  DATABASE_URL: postgresql://test_user:test_password@localhost:5434/skill_report_test_db
```

#### カバレッジアップロードエラー

Codecov トークンが設定されていない場合は `fail_ci_if_error: false` を確認。

### ローカルでのテスト実行

CI/CD環境と同等のテストをローカルで実行：

```bash
# テストDBセットアップ
npm run test:db:setup
npm run test:db:migrate

# 統合テスト実行
npm run test:integration

# データベーステスト実行
npm run test:integration:db

# クリーンアップ
npm run test:db:cleanup
```

---

**Note**: このワークフローは GitHub App の権限で直接プッシュできないため、手動で設定する必要があります。
