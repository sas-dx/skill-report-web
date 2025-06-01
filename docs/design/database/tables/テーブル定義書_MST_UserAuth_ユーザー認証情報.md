# テーブル定義書: MST_UserAuth

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_UserAuth |
| 論理名 | ユーザー認証情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | ユーザーを一意に識別するID（例：USER000001） |
| login_id | ログインID | VARCHAR | 100 | ○ |  | ログイン時に使用するID（通常はメールアドレス） |
| password_hash | パスワードハッシュ | VARCHAR | 255 | ○ |  | ハッシュ化されたパスワード（bcrypt等） |
| password_salt | パスワードソルト | VARCHAR | 100 | ○ |  | パスワードハッシュ化用のソルト値 |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 関連する社員のID（MST_Employeeへの外部キー） |
| account_status | アカウント状態 | ENUM |  | ○ | ACTIVE | アカウントの状態（ACTIVE:有効、INACTIVE:無効、LOCKED:ロック、SUSPENDED:停止） |
| last_login_at | 最終ログイン日時 | TIMESTAMP |  | ○ |  | 最後にログインした日時 |
| last_login_ip | 最終ログインIP | VARCHAR | 45 | ○ |  | 最後にログインしたIPアドレス（IPv4/IPv6対応） |
| failed_login_count | ログイン失敗回数 | INT |  | ○ | 0 | 連続ログイン失敗回数（アカウントロック判定用） |
| last_failed_login_at | 最終ログイン失敗日時 | TIMESTAMP |  | ○ |  | 最後にログインに失敗した日時 |
| password_changed_at | パスワード変更日時 | TIMESTAMP |  | ○ |  | パスワードを最後に変更した日時 |
| password_expires_at | パスワード有効期限 | TIMESTAMP |  | ○ |  | パスワードの有効期限 |
| mfa_enabled | 多要素認証有効 | BOOLEAN |  | ○ | False | 多要素認証が有効かどうか |
| mfa_secret | 多要素認証シークレット | VARCHAR | 255 | ○ |  | TOTP等の多要素認証用シークレットキー |
| recovery_token | 復旧トークン | VARCHAR | 255 | ○ |  | パスワードリセット等の復旧用トークン |
| recovery_token_expires_at | 復旧トークン有効期限 | TIMESTAMP |  | ○ |  | 復旧トークンの有効期限 |
| session_timeout | セッションタイムアウト | INT |  | ○ |  | セッションタイムアウト時間（分） |
| external_auth_provider | 外部認証プロバイダ | VARCHAR | 50 | ○ |  | 外部認証プロバイダ（LDAP、SAML、OAuth等） |
| external_auth_id | 外部認証ID | VARCHAR | 255 | ○ |  | 外部認証システムでのユーザーID |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_user_id | user_id | ○ | ユーザーID検索用（一意） |
| idx_login_id | login_id | ○ | ログインID検索用（一意） |
| idx_employee_id | employee_id | ○ | 社員ID検索用（一意） |
| idx_account_status | account_status | × | アカウント状態別検索用 |
| idx_last_login | last_login_at | × | 最終ログイン日時検索用 |
| idx_password_expires | password_expires_at | × | パスワード有効期限検索用 |
| idx_external_auth | external_auth_provider, external_auth_id | × | 外部認証検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_userauth_employee | employee_id | MST_Employee | id | CASCADE | SET NULL | 社員への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_user_id | UNIQUE |  | ユーザーID一意制約 |
| uk_login_id | UNIQUE |  | ログインID一意制約 |
| uk_employee_id | UNIQUE |  | 社員ID一意制約 |
| chk_account_status | CHECK | account_status IN ('ACTIVE', 'INACTIVE', 'LOCKED', 'SUSPENDED') | アカウント状態値チェック制約 |
| chk_failed_login_count | CHECK | failed_login_count >= 0 | ログイン失敗回数非負値チェック制約 |
| chk_session_timeout | CHECK | session_timeout IS NULL OR session_timeout > 0 | セッションタイムアウト正値チェック制約 |

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

## 業務ルール

- ログイン失敗5回でアカウント自動ロック
- パスワードは90日で有効期限切れ
- パスワードは過去3回分と同じものは使用不可
- 管理者権限ユーザーは多要素認証必須
- 外部認証ユーザーはパスワード管理不要
- アカウントロック解除は管理者のみ可能
- 復旧トークンの有効期限は24時間
- セッションタイムアウトのデフォルトは8時間

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - ユーザ認証マスタテーブルの詳細定義 |
