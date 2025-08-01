# テーブル定義書: MST_UserAuth

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_UserAuth |
| 論理名 | ユーザー認証情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:56 |

## 概要

MST_UserAuth（ユーザー認証情報）は、システムにアクセスする全ユーザーの認証・認可情報を管理するマスタテーブルです。
主な目的：
- ユーザーアカウントの一元管理（ログインID、パスワード等）
- 認証情報のセキュアな保存（パスワードハッシュ化、多要素認証対応）
- アカウント状態管理（有効/無効、ロック状態等）
- セッション管理・トークン管理
- パスワードポリシーの適用・管理
- ログイン履歴・セキュリティ監査
- 外部認証システム連携（SSO、LDAP等）
このテーブルは、システム全体のセキュリティの基盤となり、不正アクセス防止、
個人情報保護、コンプライアンス対応において重要な役割を果たします。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| account_status | アカウント状態 | ENUM |  | ○ | ACTIVE | アカウント状態 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| external_auth_id | 外部認証ID | VARCHAR | 255 | ○ |  | 外部認証ID |
| external_auth_provider | 外部認証プロバイダ | VARCHAR | 50 | ○ |  | 外部認証プロバイダ |
| failed_login_count | ログイン失敗回数 | INT |  | ○ | 0 | ログイン失敗回数 |
| last_failed_login_at | 最終ログイン失敗日時 | TIMESTAMP |  | ○ |  | 最終ログイン失敗日時 |
| last_login_at | 最終ログイン日時 | TIMESTAMP |  | ○ |  | 最終ログイン日時 |
| last_login_ip | 最終ログインIP | VARCHAR | 45 | ○ |  | 最終ログインIP |
| login_id | ログインID | VARCHAR | 100 | ○ |  | ログインID |
| mfa_enabled | 多要素認証有効 | BOOLEAN |  | ○ | False | 多要素認証有効 |
| mfa_secret | 多要素認証シークレット | VARCHAR | 255 | ○ |  | 多要素認証シークレット |
| password_changed_at | パスワード変更日時 | TIMESTAMP |  | ○ |  | パスワード変更日時 |
| password_expires_at | パスワード有効期限 | TIMESTAMP |  | ○ |  | パスワード有効期限 |
| password_hash | パスワードハッシュ | VARCHAR | 255 | ○ |  | パスワードハッシュ |
| password_salt | パスワードソルト | VARCHAR | 100 | ○ |  | パスワードソルト |
| recovery_token | 復旧トークン | VARCHAR | 255 | ○ |  | 復旧トークン |
| recovery_token_expires_at | 復旧トークン有効期限 | TIMESTAMP |  | ○ |  | 復旧トークン有効期限 |
| session_timeout | セッションタイムアウト | INT |  | ○ |  | セッションタイムアウト |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | ユーザーID |
| userauth_id | MST_UserAuthの主キー | SERIAL |  | × |  | MST_UserAuthの主キー |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_user_id | user_id | ○ |  |
| idx_login_id | login_id | ○ |  |
| idx_employee_id | employee_id | ○ |  |
| idx_account_status | account_status | × |  |
| idx_last_login | last_login_at | × |  |
| idx_password_expires | password_expires_at | × |  |
| idx_external_auth | external_auth_provider, external_auth_id | × |  |
| idx_mst_userauth_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_userauth_employee | employee_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_employee_id | UNIQUE |  | employee_id一意制約 |
| uk_login_id | UNIQUE |  | login_id一意制約 |
| uk_user_id | UNIQUE |  | user_id一意制約 |
| chk_account_status | CHECK | account_status IN (...) | account_status値チェック制約 |

## サンプルデータ

| user_id | login_id | password_hash | password_salt | employee_id | account_status | last_login_at | last_login_ip | failed_login_count | last_failed_login_at | password_changed_at | password_expires_at | mfa_enabled | mfa_secret | recovery_token | recovery_token_expires_at | session_timeout | external_auth_provider | external_auth_id |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| USER000001 | yamada.taro@company.com | $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoS | randomsalt123 | EMP000001 | ACTIVE | 2025-06-01 09:00:00 | 192.168.1.100 | 0 | None | 2025-01-01 00:00:00 | 2025-12-31 23:59:59 | True | JBSWY3DPEHPK3PXP | None | None | 480 | None | None |
| USER000002 | sato.hanako@company.com | $2b$12$XQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoX | randomsalt456 | EMP000002 | ACTIVE | 2025-05-31 17:30:00 | 192.168.1.101 | 0 | None | 2025-02-01 00:00:00 | 2026-01-31 23:59:59 | False | None | None | None | 240 | None | None |

## 特記事項

- パスワードは必ずハッシュ化して保存（平文保存禁止）
- 個人情報保護のため機密情報は暗号化
- ログイン失敗回数によるアカウントロック機能
- 多要素認証（MFA）対応
- 外部認証システム連携対応
- パスワード有効期限管理
- セッションタイムアウト個別設定可能
- ログイン失敗5回でアカウント自動ロック
- パスワードは90日で有効期限切れ
- パスワードは過去3回分と同じものは使用不可
- 管理者権限ユーザーは多要素認証必須
- 外部認証ユーザーはパスワード管理不要
- アカウントロック解除は管理者のみ可能
- 復旧トークンの有効期限は24時間
- セッションタイムアウトのデフォルトは8時間

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - ユーザ認証マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 8.0.20250624_214439 | 2025-06-24 | 最終カラム順序修正ツール | 主キー（id）を先頭に移動し、推奨カラム順序に最終修正 |
| 9.0.20250624_214522 | 2025-06-24 | 完全カラム順序修正ツール | 推奨カラム順序（1.UUID 2.tenant_id 3.主キー 4.その他）に完全修正 |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |