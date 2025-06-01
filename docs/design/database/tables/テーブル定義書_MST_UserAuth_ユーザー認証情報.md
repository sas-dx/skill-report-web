# テーブル定義書：MST_UserAuth（ユーザー認証情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-001 |
| **テーブル名** | MST_UserAuth |
| **論理名** | ユーザー認証情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
ユーザー認証情報マスタテーブル（MST_UserAuth）は、システムにアクセスするユーザーの認証に必要な情報を管理します。ログイン認証、パスワード管理、セッション管理、多要素認証などの機能を支援し、システムのセキュリティを確保します。

### 2.2 関連API
- [API-001](../../api/specs/API仕様書_API-001_ユーザー認証API.md) - ユーザー認証API
- [API-002](../../api/specs/API仕様書_API-002_パスワード管理API.md) - パスワード管理API

### 2.3 関連バッチ
- [BATCH-001](../../batch/specs/バッチ定義書_BATCH-001_システムヘルスチェックバッチ.md) - システムヘルスチェックバッチ
- [BATCH-002](../../batch/specs/バッチ定義書_BATCH-002_ログクリーンアップバッチ.md) - ログクリーンアップバッチ
- [BATCH-003](../../batch/specs/バッチ定義書_BATCH-003_セキュリティスキャンバッチ.md) - セキュリティスキャンバッチ
- [BATCH-017](../../batch/specs/バッチ定義書_BATCH-017_トークン無効化バッチ.md) - トークン無効化バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | user_id | ユーザーID | VARCHAR | 50 | × | ○ | - | - | ユーザーを一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | login_id | ログインID | VARCHAR | 100 | × | - | - | - | ログイン時に使用するID |
| 4 | email | メールアドレス | VARCHAR | 255 | × | - | - | - | ユーザーのメールアドレス |
| 5 | password_hash | パスワードハッシュ | VARCHAR | 255 | × | - | - | - | ハッシュ化されたパスワード |
| 6 | salt | ソルト | VARCHAR | 100 | × | - | - | - | パスワードハッシュ化用のソルト |
| 7 | password_updated_at | パスワード更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | パスワード最終更新日時 |
| 8 | password_expires_at | パスワード有効期限 | TIMESTAMP | - | ○ | - | - | NULL | パスワードの有効期限 |
| 9 | failed_login_count | ログイン失敗回数 | INTEGER | - | × | - | - | 0 | 連続ログイン失敗回数 |
| 10 | last_failed_login_at | 最終ログイン失敗日時 | TIMESTAMP | - | ○ | - | - | NULL | 最後にログインに失敗した日時 |
| 11 | account_locked | アカウントロック状態 | BOOLEAN | - | × | - | - | FALSE | アカウントがロックされているかどうか |
| 12 | account_locked_at | アカウントロック日時 | TIMESTAMP | - | ○ | - | - | NULL | アカウントがロックされた日時 |
| 13 | account_locked_until | アカウントロック解除日時 | TIMESTAMP | - | ○ | - | - | NULL | アカウントロックが解除される日時 |
| 14 | last_login_at | 最終ログイン日時 | TIMESTAMP | - | ○ | - | - | NULL | 最後にログインした日時 |
| 15 | last_login_ip | 最終ログインIP | VARCHAR | 45 | ○ | - | - | NULL | 最後にログインしたIPアドレス |
| 16 | mfa_enabled | 多要素認証有効フラグ | BOOLEAN | - | × | - | - | FALSE | 多要素認証が有効かどうか |
| 17 | mfa_secret | 多要素認証シークレット | VARCHAR | 255 | ○ | - | - | NULL | TOTP用のシークレットキー |
| 18 | backup_codes | バックアップコード | TEXT | - | ○ | - | - | NULL | 多要素認証のバックアップコード（JSON形式） |
| 19 | session_timeout | セッションタイムアウト | INTEGER | - | × | - | - | 3600 | セッションタイムアウト時間（秒） |
| 20 | force_password_change | パスワード変更強制フラグ | BOOLEAN | - | × | - | - | FALSE | 次回ログイン時にパスワード変更を強制するかどうか |
| 21 | password_history | パスワード履歴 | TEXT | - | ○ | - | - | NULL | 過去のパスワードハッシュ（JSON形式） |
| 22 | security_questions | セキュリティ質問 | TEXT | - | ○ | - | - | NULL | セキュリティ質問と回答（JSON形式） |
| 23 | login_notification | ログイン通知設定 | BOOLEAN | - | × | - | - | TRUE | ログイン時の通知を送信するかどうか |
| 24 | suspicious_activity_detected | 不審なアクティビティ検知 | BOOLEAN | - | × | - | - | FALSE | 不審なアクティビティが検知されたかどうか |
| 25 | terms_accepted_at | 利用規約同意日時 | TIMESTAMP | - | ○ | - | - | NULL | 利用規約に同意した日時 |
| 26 | privacy_policy_accepted_at | プライバシーポリシー同意日時 | TIMESTAMP | - | ○ | - | - | NULL | プライバシーポリシーに同意した日時 |
| 27 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | ユーザーアカウントが有効かどうか |
| 28 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 29 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 30 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 31 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | user_id | 主キー |
| uq_login_id | UNIQUE | tenant_id, login_id | テナント内でのログインID一意性 |
| uq_email | UNIQUE | tenant_id, email | テナント内でのメールアドレス一意性 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_email | INDEX | email | メールアドレス検索用 |
| idx_last_login | INDEX | last_login_at | 最終ログイン日時検索用 |
| idx_account_locked | INDEX | account_locked | アカウントロック状態検索用 |
| idx_mfa_enabled | INDEX | mfa_enabled | 多要素認証有効フラグ検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_user_auth | PRIMARY KEY | user_id | 主キー制約 |
| uq_login_id | UNIQUE | tenant_id, login_id | テナント内でのログインID一意性 |
| uq_email | UNIQUE | tenant_id, email | テナント内でのメールアドレス一意性 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_email_format | CHECK | email | email LIKE '%@%.%' |
| chk_failed_login_count | CHECK | failed_login_count | failed_login_count >= 0 |
| chk_session_timeout | CHECK | session_timeout | session_timeout > 0 |
| chk_password_hash_length | CHECK | password_hash | LENGTH(password_hash) >= 60 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserRole | user_id | 1:N | ユーザーロール関連 |
| MST_Employee | user_id | 1:1 | 社員基本情報 |
| SYS_TokenStore | user_id | 1:N | トークン管理 |
| HIS_AuditLog | user_id | 1:N | 監査ログ |

## 5. データ仕様

### 5.1 データ例
```sql
-- システム管理者
INSERT INTO MST_UserAuth (
    user_id, tenant_id, login_id, email, password_hash, salt,
    password_updated_at, mfa_enabled, session_timeout, is_active,
    created_by, updated_by
) VALUES (
    'user_admin', 'TENANT_001', 'admin', 'admin@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RX.PleB8i', 'salt123',
    CURRENT_TIMESTAMP, TRUE, 7200, TRUE,
    'system', 'system'
);

-- 一般ユーザー
INSERT INTO MST_UserAuth (
    user_id, tenant_id, login_id, email, password_hash, salt,
    password_updated_at, mfa_enabled, session_timeout, is_active,
    created_by, updated_by
) VALUES (
    'user_001', 'TENANT_001', 'yamada.taro', 'yamada.taro@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RX.PleB8i', 'salt456',
    CURRENT_TIMESTAMP, FALSE, 3600, TRUE,
    'user_admin', 'user_admin'
);

-- アカウントロック状態のユーザー
INSERT INTO MST_UserAuth (
    user_id, tenant_id, login_id, email, password_hash, salt,
    password_updated_at, failed_login_count, account_locked, account_locked_at,
    account_locked_until, mfa_enabled, session_timeout, is_active,
    created_by, updated_by
) VALUES (
    'user_002', 'TENANT_001', 'suzuki.hanako', 'suzuki.hanako@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RX.PleB8i', 'salt789',
    CURRENT_TIMESTAMP, 5, TRUE, CURRENT_TIMESTAMP,
    DATE_ADD(CURRENT_TIMESTAMP, INTERVAL 30 MINUTE), FALSE, 3600, TRUE,
    'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 10件 | システム管理者、テスト用ユーザー |
| 月間増加件数 | 50件 | 新規ユーザー登録 |
| 年間増加件数 | 600件 | 想定値 |
| 5年後想定件数 | 3,010件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：無効化から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 最高 | login_id, email | ログイン認証 |
| UPDATE | 高 | user_id | パスワード更新、ログイン情報更新 |
| SELECT | 高 | user_id | ユーザー情報取得 |
| INSERT | 低 | - | 新規ユーザー登録 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| user_admin | ○ | ○ | ○ | × | ユーザー管理者 |
| user_self | ○ | × | ○ | × | 本人のみ（パスワード変更等） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（メールアドレス）
- 機密情報：含む（パスワードハッシュ、認証情報）
- 暗号化：パスワードハッシュ、多要素認証シークレット

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存認証システム
- 移行方法：暗号化CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_UserAuth (
    user_id VARCHAR(50) NOT NULL COMMENT 'ユーザーID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    login_id VARCHAR(100) NOT NULL COMMENT 'ログインID',
    email VARCHAR(255) NOT NULL COMMENT 'メールアドレス',
    password_hash VARCHAR(255) NOT NULL COMMENT 'パスワードハッシュ',
    salt VARCHAR(100) NOT NULL COMMENT 'ソルト',
    password_updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'パスワード更新日時',
    password_expires_at TIMESTAMP NULL COMMENT 'パスワード有効期限',
    failed_login_count INTEGER NOT NULL DEFAULT 0 COMMENT 'ログイン失敗回数',
    last_failed_login_at TIMESTAMP NULL COMMENT '最終ログイン失敗日時',
    account_locked BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'アカウントロック状態',
    account_locked_at TIMESTAMP NULL COMMENT 'アカウントロック日時',
    account_locked_until TIMESTAMP NULL COMMENT 'アカウントロック解除日時',
    last_login_at TIMESTAMP NULL COMMENT '最終ログイン日時',
    last_login_ip VARCHAR(45) NULL COMMENT '最終ログインIP',
    mfa_enabled BOOLEAN NOT NULL DEFAULT FALSE COMMENT '多要素認証有効フラグ',
    mfa_secret VARCHAR(255) NULL COMMENT '多要素認証シークレット',
    backup_codes TEXT NULL COMMENT 'バックアップコード',
    session_timeout INTEGER NOT NULL DEFAULT 3600 COMMENT 'セッションタイムアウト',
    force_password_change BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'パスワード変更強制フラグ',
    password_history TEXT NULL COMMENT 'パスワード履歴',
    security_questions TEXT NULL COMMENT 'セキュリティ質問',
    login_notification BOOLEAN NOT NULL DEFAULT TRUE COMMENT 'ログイン通知設定',
    suspicious_activity_detected BOOLEAN NOT NULL DEFAULT FALSE COMMENT '不審なアクティビティ検知',
    terms_accepted_at TIMESTAMP NULL COMMENT '利用規約同意日時',
    privacy_policy_accepted_at TIMESTAMP NULL COMMENT 'プライバシーポリシー同意日時',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (user_id),
    UNIQUE KEY uq_login_id (tenant_id, login_id),
    UNIQUE KEY uq_email (tenant_id, email),
    INDEX idx_tenant (tenant_id),
    INDEX idx_email (email),
    INDEX idx_last_login (last_login_at),
    INDEX idx_account_locked (account_locked),
    INDEX idx_mfa_enabled (mfa_enabled),
    INDEX idx_active (is_active),
    CONSTRAINT fk_user_auth_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_user_auth_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_user_auth_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_user_auth_email_format CHECK (email LIKE '%@%.%'),
    CONSTRAINT chk_user_auth_failed_login_count CHECK (failed_login_count >= 0),
    CONSTRAINT chk_user_auth_session_timeout CHECK (session_timeout > 0),
    CONSTRAINT chk_user_auth_password_hash_length CHECK (LENGTH(password_hash) >= 60)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ユーザー認証情報';
```

## 10. 特記事項

1. **セキュリティ要件**
   - パスワードはbcryptでハッシュ化（コスト12以上）
   - ソルトは各ユーザー固有の値を使用
   - 多要素認証（TOTP）をサポート

2. **アカウントロック機能**
   - 連続ログイン失敗回数が5回に達するとアカウントロック
   - ロック時間は設定可能（デフォルト30分）

3. **パスワードポリシー**
   - 最小8文字、英数字記号を含む
   - 過去5回分のパスワード履歴をチェック
   - 有効期限は90日（設定可能）

4. **監査要件**
   - すべてのログイン試行を記録
   - パスワード変更履歴を保持
   - 不審なアクティビティを検知・記録

5. **GDPR対応**
   - 個人データの削除要求に対応
   - データ処理の同意管理
   - データポータビリティをサポート
