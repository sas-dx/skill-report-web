# テーブル定義書：MST_UserAuth（ユーザー認証情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-001 |
| **テーブル名** | MST_UserAuth |
| **論理名** | ユーザー認証情報 |
| **カテゴリ** | マスタ系 |
| **機能カテゴリ** | 認証・認可 |
| **優先度** | 最高 |
| **個人情報含有** | あり |
| **機密情報レベル** | 高 |
| **暗号化要否** | 要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
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


### 2.2 特記事項
- パスワードは必ずハッシュ化して保存（平文保存禁止）
- 個人情報保護のため機密情報は暗号化
- ログイン失敗回数によるアカウントロック機能
- 多要素認証（MFA）対応
- 外部認証システム連携対応
- パスワード有効期限管理
- セッションタイムアウト個別設定可能

### 2.3 関連API
API-001, API-002

### 2.4 関連バッチ
BATCH-001, BATCH-002, BATCH-003, BATCH-017

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | VARCHAR | 50 | × | ○ | - | - | 主キー |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | レコードが有効かどうか |
| 4 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 5 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 6 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 7 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |
| 8 | user_id | ユーザーID | VARCHAR | 50 | ○ | - | ○ | - | ユーザーを一意に識別するID（例：USER000001） |
| 9 | login_id | ログインID | VARCHAR | 100 | ○ | - | ○ | - | ログイン時に使用するID（通常はメールアドレス） |
| 10 | password_hash | パスワードハッシュ | VARCHAR | 255 | ○ | - | - | - | ハッシュ化されたパスワード（bcrypt等） |
| 11 | password_salt | パスワードソルト | VARCHAR | 100 | ○ | - | - | - | パスワードハッシュ化用のソルト値 |
| 12 | employee_id | 社員ID | VARCHAR | 50 | ○ | - | ○ | - | 関連する社員のID（MST_Employeeへの外部キー） |
| 13 | account_status | アカウント状態 | ENUM | None | ○ | - | - | ACTIVE | アカウントの状態（ACTIVE:有効、INACTIVE:無効、LOCKED:ロック、SUSPENDED:停止） |
| 14 | last_login_at | 最終ログイン日時 | TIMESTAMP | None | ○ | - | - | - | 最後にログインした日時 |
| 15 | last_login_ip | 最終ログインIP | VARCHAR | 45 | ○ | - | - | - | 最後にログインしたIPアドレス（IPv4/IPv6対応） |
| 16 | failed_login_count | ログイン失敗回数 | INT | None | ○ | - | - | 0 | 連続ログイン失敗回数（アカウントロック判定用） |
| 17 | last_failed_login_at | 最終ログイン失敗日時 | TIMESTAMP | None | ○ | - | - | - | 最後にログインに失敗した日時 |
| 18 | password_changed_at | パスワード変更日時 | TIMESTAMP | None | ○ | - | - | - | パスワードを最後に変更した日時 |
| 19 | password_expires_at | パスワード有効期限 | TIMESTAMP | None | ○ | - | - | - | パスワードの有効期限 |
| 20 | mfa_enabled | 多要素認証有効 | BOOLEAN | None | ○ | - | - | False | 多要素認証が有効かどうか |
| 21 | mfa_secret | 多要素認証シークレット | VARCHAR | 255 | ○ | - | - | - | TOTP等の多要素認証用シークレットキー |
| 22 | recovery_token | 復旧トークン | VARCHAR | 255 | ○ | - | - | - | パスワードリセット等の復旧用トークン |
| 23 | recovery_token_expires_at | 復旧トークン有効期限 | TIMESTAMP | None | ○ | - | - | - | 復旧トークンの有効期限 |
| 24 | session_timeout | セッションタイムアウト | INT | None | ○ | - | - | - | セッションタイムアウト時間（分） |
| 25 | external_auth_provider | 外部認証プロバイダ | VARCHAR | 50 | ○ | - | - | - | 外部認証プロバイダ（LDAP、SAML、OAuth等） |
| 26 | external_auth_id | 外部認証ID | VARCHAR | 255 | ○ | - | ○ | - | 外部認証システムでのユーザーID |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_user_id | UNIQUE INDEX | user_id | ユーザーID検索用（一意） |
| idx_login_id | UNIQUE INDEX | login_id | ログインID検索用（一意） |
| idx_employee_id | UNIQUE INDEX | employee_id | 社員ID検索用（一意） |
| idx_account_status | INDEX | account_status | アカウント状態別検索用 |
| idx_last_login | INDEX | last_login_at | 最終ログイン日時検索用 |
| idx_password_expires | INDEX | password_expires_at | パスワード有効期限検索用 |
| idx_external_auth | INDEX | external_auth_provider, external_auth_id | 外部認証検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_userauth | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_user_id | UNIQUE | user_id | ['user_id'] |
| uk_login_id | UNIQUE | login_id | ['login_id'] |
| uk_employee_id | UNIQUE | employee_id | ['employee_id'] |
| chk_account_status | CHECK |  | account_status IN ('ACTIVE', 'INACTIVE', 'LOCKED', 'SUSPENDED') |
| chk_failed_login_count | CHECK |  | failed_login_count >= 0 |
| chk_session_timeout | CHECK |  | session_timeout IS NULL OR session_timeout > 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_Employee | employee_id | 1:N | 社員への外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_UserAuth (
    id, tenant_id, user_id, login_id, password_hash, password_salt, employee_id, account_status, last_login_at, last_login_ip, failed_login_count, last_failed_login_at, password_changed_at, password_expires_at, mfa_enabled, mfa_secret, recovery_token, recovery_token_expires_at, session_timeout, external_auth_provider, external_auth_id, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'USER000001', 'yamada.taro@company.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uIoS', 'randomsalt123', 'EMP000001', 'ACTIVE', '2025-06-01 09:00:00', '192.168.1.100', '0', NULL, '2025-01-01 00:00:00', '2025-12-31 23:59:59', 'True', 'JBSWY3DPEHPK3PXP', NULL, NULL, '480', NULL, NULL, 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 初期設定データ |
| 月間増加件数 | 100件 | 想定値 |
| 年間増加件数 | 1,200件 | 想定値 |
| 5年後想定件数 | 6,500件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | id, tenant_id | 基本検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新処理 |
| DELETE | 低 | id | 削除処理 |

### 7.2 パフォーマンス要件
- SELECT：15ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| user | ○ | × | × | × | 一般ユーザー（参照のみ） |

### 8.2 データ保護
- 個人情報：あり
- 機密情報：高レベル
- 暗号化：要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
-- ユーザー認証情報テーブル作成DDL
CREATE TABLE MST_UserAuth (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    user_id VARCHAR(50) COMMENT 'ユーザーID',
    login_id VARCHAR(100) COMMENT 'ログインID',
    password_hash VARCHAR(255) COMMENT 'パスワードハッシュ',
    password_salt VARCHAR(100) COMMENT 'パスワードソルト',
    employee_id VARCHAR(50) COMMENT '社員ID',
    account_status ENUM DEFAULT ACTIVE COMMENT 'アカウント状態',
    last_login_at TIMESTAMP COMMENT '最終ログイン日時',
    last_login_ip VARCHAR(45) COMMENT '最終ログインIP',
    failed_login_count INT DEFAULT 0 COMMENT 'ログイン失敗回数',
    last_failed_login_at TIMESTAMP COMMENT '最終ログイン失敗日時',
    password_changed_at TIMESTAMP COMMENT 'パスワード変更日時',
    password_expires_at TIMESTAMP COMMENT 'パスワード有効期限',
    mfa_enabled BOOLEAN DEFAULT False COMMENT '多要素認証有効',
    mfa_secret VARCHAR(255) COMMENT '多要素認証シークレット',
    recovery_token VARCHAR(255) COMMENT '復旧トークン',
    recovery_token_expires_at TIMESTAMP COMMENT '復旧トークン有効期限',
    session_timeout INT COMMENT 'セッションタイムアウト',
    external_auth_provider VARCHAR(50) COMMENT '外部認証プロバイダ',
    external_auth_id VARCHAR(255) COMMENT '外部認証ID',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_user_id (user_id),
    UNIQUE INDEX idx_login_id (login_id),
    UNIQUE INDEX idx_employee_id (employee_id),
    INDEX idx_account_status (account_status),
    INDEX idx_last_login (last_login_at),
    INDEX idx_password_expires (password_expires_at),
    INDEX idx_external_auth (external_auth_provider, external_auth_id),
    CONSTRAINT fk_userauth_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ユーザー認証情報';

```

## 10. 特記事項

1. **設計方針**
   - マスタ系として設計
   - マルチテナント対応
   - 監査証跡の保持

2. **運用上の注意点**
   - 定期的なデータクリーンアップが必要
   - パフォーマンス監視を実施
   - データ量見積もりの定期見直し

3. **今後の拡張予定**
   - 必要に応じて機能拡張を検討

4. **関連画面**
   - 関連画面情報

5. **データ量・パフォーマンス監視**
   - データ量が想定の150%を超えた場合はアラート
   - 応答時間が設定値の120%を超えた場合は調査


## 11. 業務ルール

- ログイン失敗5回でアカウント自動ロック
- パスワードは90日で有効期限切れ
- パスワードは過去3回分と同じものは使用不可
- 管理者権限ユーザーは多要素認証必須
- 外部認証ユーザーはパスワード管理不要
- アカウントロック解除は管理者のみ可能
- 復旧トークンの有効期限は24時間
- セッションタイムアウトのデフォルトは8時間
