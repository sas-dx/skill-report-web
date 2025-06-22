# テーブル定義書: MST_UserAuth

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_UserAuth |
| 論理名 | ユーザー認証情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:18 |

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
| userauth_id | MST_UserAuthの主キー | SERIAL |  | × |  | MST_UserAuthの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_userauth_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_userauth_employee | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_userauth | PRIMARY KEY | userauth_id | 主キー制約 |

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