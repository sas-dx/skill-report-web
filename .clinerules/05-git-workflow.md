# Git・バージョン管理ワークフロー

## 基本方針

### Gitflow戦略
- **main**: 本番リリース用ブランチ（プロダクション環境）
- **develop**: 開発統合ブランチ（開発環境）
- **feature/***: 機能開発ブランチ（要求仕様ID単位）
- **release/***: リリース準備ブランチ
- **hotfix/***: 緊急バグ修正ブランチ

### 要求仕様ID連携の強制
- **全ブランチ**: 要求仕様IDを含む命名必須
- **全コミット**: 要求仕様IDを含むメッセージ必須
- **全PR**: 要求仕様IDと対応する設計書の明記必須

## ブランチ命名規則

### feature ブランチ
```
feature/{要求仕様ID}-{機能名}
```

**例**:
```
feature/TNT.1-MGMT-tenant-management
feature/PLT.1-WEB.1-web-platform-base
feature/PRO.1-BASE.1-profile-management
feature/SKL.1-HIER.1-skill-hierarchy
feature/ACC.1-ROLE.1-role-management
```

### release ブランチ
```
release/v{メジャー}.{マイナー}.{パッチ}
```

**例**:
```
release/v1.0.0
release/v1.1.0
release/v2.0.0
```

### hotfix ブランチ
```
hotfix/{緊急度}-{修正内容}
```

**例**:
```
hotfix/critical-login-security-fix
hotfix/high-data-corruption-fix
hotfix/medium-ui-display-issue
```

## コミットメッセージ規約

### 基本フォーマット
```
[絵文字] [タイプ]: [要求仕様ID] [タイトル]

[本文]

[フッター]
```

### タイプ定義
- **feat**: 新機能（要求仕様ID必須）
- **fix**: バグ修正
- **docs**: ドキュメント変更
- **style**: コードスタイル変更（動作に影響しない）
- **refactor**: リファクタリング
- **perf**: パフォーマンス改善
- **test**: テスト追加・修正
- **chore**: ビルド・ツール変更

### 絵文字ガイドライン
- ✨ feat: 新機能
- 🐛 fix: バグ修正
- 📚 docs: ドキュメント
- 💎 style: スタイル
- ♻️ refactor: リファクタリング
- ⚡ perf: パフォーマンス
- 🧪 test: テスト
- 🔧 chore: ツール・設定

### コミットメッセージ例

#### 新機能実装
```
✨ feat: TNT.1-MGMT マルチテナント管理機能を実装

- テナント作成・編集・削除機能を追加
- テナント別設定管理を実装
- 管理者権限によるテナント操作制御を追加

Closes #123
Refs: docs/design/api/specs/API定義書_API-025_テナント管理API.md
```

#### バグ修正
```
🐛 fix: SKL.1-HIER.1 スキル階層表示の不具合を修正

- 3階層目のスキル項目が表示されない問題を解決
- カテゴリ選択時の子要素更新ロジックを修正

Fixes #456
```

#### ドキュメント更新
```
📚 docs: API定義書_API-021 スキル情報取得APIの仕様を更新

- レスポンス形式にテナントIDフィールドを追加
- エラーコード一覧を最新化

Refs: docs/design/api/specs/API定義書_API-021_スキル情報取得API.md
```

## Pull Request規約

### PRタイトル
```
[要求仕様ID] 機能名: 実装内容の概要
```

**例**:
```
[TNT.1-MGMT] テナント管理: マルチテナント基盤機能の実装
[SKL.1-HIER.1] スキル階層: 3階層スキル管理機能の実装
[PLT.1-WEB.1] Web基盤: Next.js 14 App Router基盤の構築
```

### PR説明テンプレート
```markdown
## 要求仕様ID
- 対象: {要求仕様ID}
- 関連設計書: docs/design/{設計書パス}

## 実装内容
- [ ] 機能1の実装
- [ ] 機能2の実装
- [ ] テスト実装

## 変更ファイル
- `src/app/{パス}`: 新規作成
- `src/components/{パス}`: 機能追加
- `docs/design/{パス}`: 仕様書更新

## テスト
- [ ] ユニットテスト実装済み
- [ ] 統合テスト実装済み
- [ ] E2Eテスト実装済み

## 非機能要件
- [ ] パフォーマンス: レスポンス1秒以内
- [ ] アクセシビリティ: WCAG 2.1 AA準拠
- [ ] セキュリティ: 脆弱性チェック済み
- [ ] マルチテナント: テナント分離確認済み

## 確認事項
- [ ] 要求仕様IDが全実装に記載されている
- [ ] 設計書との整合性を確認済み
- [ ] TypeScript型安全性を確保済み
- [ ] レスポンシブ対応を実装済み

## スクリーンショット
（UI変更がある場合）

## 備考
（追加の説明や注意事項）
```

## コードレビュープロセス

### レビュー観点

#### 1. 要求仕様準拠
- [ ] 要求仕様IDが明記されているか
- [ ] 設計書との整合性があるか
- [ ] 実装内容が仕様を満たしているか

#### 2. コード品質
- [ ] コーディング規約に準拠しているか
- [ ] TypeScript型安全性が確保されているか
- [ ] SOLID原則に従っているか
- [ ] DRY原則が守られているか

#### 3. セキュリティ
- [ ] 入力値検証が実装されているか
- [ ] 認証・認可が適切か
- [ ] マルチテナント分離が確保されているか
- [ ] 機密情報の適切な取り扱いがされているか

#### 4. パフォーマンス
- [ ] レスポンス時間1秒以内を満たすか
- [ ] 効率的なアルゴリズムが使用されているか
- [ ] 不要な処理がないか
- [ ] メモリリークの可能性がないか

#### 5. テスト
- [ ] 適切なテストが実装されているか
- [ ] テストカバレッジが80%以上か
- [ ] エッジケースが考慮されているか

### レビュー承認基準
- **必須承認者**: PL（笹尾）
- **推奨承認者**: 他の開発メンバー1名以上
- **自動チェック**: CI/CDパイプラインの全テスト通過

## ブランチ運用フロー

### 1. 機能開発フロー
```bash
# 1. developブランチから最新を取得
git checkout develop
git pull origin develop

# 2. featureブランチ作成
git checkout -b feature/SKL.1-HIER.1-skill-hierarchy

# 3. 実装・コミット
git add .
git commit -m "✨ feat: SKL.1-HIER.1 スキル階層構造を実装"

# 4. プッシュ・PR作成
git push origin feature/SKL.1-HIER.1-skill-hierarchy
# GitHub上でPR作成

# 5. レビュー・マージ後のクリーンアップ
git checkout develop
git pull origin develop
git branch -d feature/SKL.1-HIER.1-skill-hierarchy
```

### 2. リリースフロー
```bash
# 1. releaseブランチ作成
git checkout develop
git checkout -b release/v1.0.0

# 2. リリース準備（バージョン更新等）
git commit -m "🔧 chore: v1.0.0リリース準備"

# 3. mainブランチにマージ
git checkout main
git merge release/v1.0.0
git tag v1.0.0
git push origin main --tags

# 4. developブランチにもマージ
git checkout develop
git merge release/v1.0.0
git push origin develop

# 5. releaseブランチ削除
git branch -d release/v1.0.0
```

### 3. 緊急修正フロー
```bash
# 1. mainブランチからhotfixブランチ作成
git checkout main
git checkout -b hotfix/critical-login-security-fix

# 2. 修正・コミット
git commit -m "🐛 fix: ログイン認証の重大な脆弱性を修正"

# 3. mainとdevelopの両方にマージ
git checkout main
git merge hotfix/critical-login-security-fix
git tag v1.0.1
git push origin main --tags

git checkout develop
git merge hotfix/critical-login-security-fix
git push origin develop

# 4. hotfixブランチ削除
git branch -d hotfix/critical-login-security-fix
```

## CI/CD統合

### 自動チェック項目
- **静的解析**: ESLint、TypeScript型チェック
- **テスト実行**: ユニット・統合・E2Eテスト
- **セキュリティスキャン**: 脆弱性チェック
- **パフォーマンステスト**: レスポンス時間測定
- **要求仕様ID検証**: コミット・PRでの要求仕様ID存在チェック

### 自動デプロイ
- **develop → 開発環境**: 自動デプロイ
- **main → 本番環境**: 手動承認後デプロイ
- **feature → プレビュー環境**: Vercel Preview Deployment

## 禁止事項・注意事項

### 禁止事項
- 要求仕様IDなしのコミット・PR
- mainブランチへの直接コミット
- 設計書との不整合を含む実装
- レビューなしのマージ
- 破壊的変更の無承認実装

### 注意事項
- コミット前に必ず要求仕様IDを確認
- PR作成時は対応する設計書を明記
- マージ後は不要なブランチを削除
- 定期的なdevelopブランチの同期
- 緊急修正時も必ずレビューを実施

---

この Git・バージョン管理ワークフローに従って、要求仕様ID連携と品質保証を両立した開発を進めてください。
