# テーブル定義書：テナント設定 (MST_TenantSettings)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-027 |
| **テーブル名** | MST_TenantSettings |
| **論理名** | テナント設定 |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 新規作成 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
テナント設定テーブル（MST_TenantSettings）は、各テナントの個別設定情報を管理します。UI設定、機能有効化フラグ、セキュリティ設定など、テナントごとにカスタマイズ可能な設定項目を格納します。

### 2.2 関連API
- [API-026](../api/specs/API仕様書_API-026.md) - テナント設定管理API

### 2.3 関連バッチ
- [BATCH-018-05](../batch/specs/バッチ定義書_BATCH-018-05.md) - テナント設定同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | tenant_id | テナントID | VARCHAR | 50 | × | ○ | ○ | - | テナントを一意に識別するID |
| 2 | theme_color | テーマカラー | VARCHAR | 7 | × | - | - | '#1976d2' | UIテーマカラー（HEX形式） |
| 3 | logo_url | ロゴURL | VARCHAR | 500 | ○ | - | - | NULL | テナントロゴのURL |
| 4 | company_logo_url | 会社ロゴURL | VARCHAR | 500 | ○ | - | - | NULL | 会社ロゴのURL |
| 5 | favicon_url | ファビコンURL | VARCHAR | 500 | ○ | - | - | NULL | ファビコンのURL |
| 6 | enable_skill_management | スキル管理有効 | BOOLEAN | - | × | - | - | TRUE | スキル管理機能の有効化 |
| 7 | enable_goal_management | 目標管理有効 | BOOLEAN | - | × | - | - | TRUE | 目標管理機能の有効化 |
| 8 | enable_training_management | 研修管理有効 | BOOLEAN | - | × | - | - | TRUE | 研修管理機能の有効化 |
| 9 | enable_report_generation | レポート生成有効 | BOOLEAN | - | × | - | - | TRUE | レポート生成機能の有効化 |
| 10 | enable_api_access | API アクセス有効 | BOOLEAN | - | × | - | - | FALSE | API アクセスの有効化 |
| 11 | password_policy_min_length | パスワード最小長 | INTEGER | - | × | - | - | 8 | パスワードの最小文字数 |
| 12 | password_policy_require_uppercase | 大文字必須 | BOOLEAN | - | × | - | - | TRUE | パスワードに大文字を必須とするか |
| 13 | password_policy_require_lowercase | 小文字必須 | BOOLEAN | - | × | - | - | TRUE | パスワードに小文字を必須とするか |
| 14 | password_policy_require_numbers | 数字必須 | BOOLEAN | - | × | - | - | TRUE | パスワードに数字を必須とするか |
| 15 | password_policy_require_symbols | 記号必須 | BOOLEAN | - | × | - | - | FALSE | パスワードに記号を必須とするか |
| 16 | session_timeout_minutes | セッションタイムアウト | INTEGER | - | × | - | - | 480 | セッションタイムアウト時間（分） |
| 17 | max_login_attempts | 最大ログイン試行回数 | INTEGER | - | × | - | - | 5 | 最大ログイン失敗回数 |
| 18 | account_lock_duration_minutes | アカウントロック時間 | INTEGER | - | × | - | - | 30 | アカウントロック時間（分） |
| 19 | enable_two_factor_auth | 二要素認証有効 | BOOLEAN | - | × | - | - | FALSE | 二要素認証の有効化 |
| 20 | backup_retention_days | バックアップ保持日数 | INTEGER | - | × | - | - | 30 | バックアップデータの保持日数 |
| 21 | data_export_format | データエクスポート形式 | VARCHAR | 20 | × | - | - | 'CSV' | データエクスポートのデフォルト形式 |
| 22 | notification_email_enabled | メール通知有効 | BOOLEAN | - | × | - | - | TRUE | メール通知の有効化 |
| 23 | notification_slack_enabled | Slack通知有効 | BOOLEAN | - | × | - | - | FALSE | Slack通知の有効化 |
| 24 | notification_teams_enabled | Teams通知有効 | BOOLEAN | - | × | - | - | FALSE | Teams通知の有効化 |
| 25 | custom_css | カスタムCSS | TEXT | - | ○ | - | - | NULL | テナント固有のCSS設定 |
| 26 | custom_javascript | カスタムJavaScript | TEXT | - | ○ | - | - | NULL | テナント固有のJavaScript設定 |
| 27 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 28 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 29 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 30 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | tenant_id | 主キー |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_tenant_settings | PRIMARY KEY | tenant_id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_theme_color | CHECK | theme_color | theme_color REGEXP '^#[0-9A-Fa-f]{6}$' |
| chk_password_min_length | CHECK | password_policy_min_length | password_policy_min_length >= 4 AND password_policy_min_length <= 128 |
| chk_session_timeout | CHECK | session_timeout_minutes | session_timeout_minutes >= 5 AND session_timeout_minutes <= 1440 |
| chk_max_login_attempts | CHECK | max_login_attempts | max_login_attempts >= 1 AND max_login_attempts <= 20 |
| chk_lock_duration | CHECK | account_lock_duration_minutes | account_lock_duration_minutes >= 1 AND account_lock_duration_minutes <= 1440 |
| chk_backup_retention | CHECK | backup_retention_days | backup_retention_days >= 1 AND backup_retention_days <= 365 |
| chk_export_format | CHECK | data_export_format | data_export_format IN ('CSV', 'EXCEL', 'JSON', 'PDF') |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:1 | テナントマスタ |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
なし

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_TenantSettings (
    tenant_id, theme_color, enable_skill_management, enable_goal_management,
    password_policy_min_length, session_timeout_minutes, max_login_attempts,
    account_lock_duration_minutes, notification_email_enabled,
    created_by, updated_by
) VALUES (
    'tenant001',
    '#1976d2',
    TRUE,
    TRUE,
    8,
    480,
    5,
    30,
    TRUE,
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 10件 | 初期契約テナント分 |
| 年間増加件数 | 100件 | 新規契約テナント分 |
| 5年後想定件数 | 510件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：テナント削除から1年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id | テナント設定取得 |
| UPDATE | 中 | tenant_id | 設定変更 |
| INSERT | 低 | - | 新規テナント設定作成 |

### 7.2 パフォーマンス要件
- SELECT：5ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | × | ○ | × | テナント管理者（自テナントのみ） |
| application | ○ | ○ | ○ | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（セキュリティ設定）
- 暗号化：カスタムスクリプトは暗号化推奨

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存設定ファイル
- 移行方法：設定移行スクリプト
- 移行タイミング：テナント作成時

### 9.2 DDL
```sql
CREATE TABLE MST_TenantSettings (
    tenant_id VARCHAR(50) NOT NULL,
    theme_color VARCHAR(7) NOT NULL DEFAULT '#1976d2',
    logo_url VARCHAR(500) NULL,
    company_logo_url VARCHAR(500) NULL,
    favicon_url VARCHAR(500) NULL,
    enable_skill_management BOOLEAN NOT NULL DEFAULT TRUE,
    enable_goal_management BOOLEAN NOT NULL DEFAULT TRUE,
    enable_training_management BOOLEAN NOT NULL DEFAULT TRUE,
    enable_report_generation BOOLEAN NOT NULL DEFAULT TRUE,
    enable_api_access BOOLEAN NOT NULL DEFAULT FALSE,
    password_policy_min_length INTEGER NOT NULL DEFAULT 8,
    password_policy_require_uppercase BOOLEAN NOT NULL DEFAULT TRUE,
    password_policy_require_lowercase BOOLEAN NOT NULL DEFAULT TRUE,
    password_policy_require_numbers BOOLEAN NOT NULL DEFAULT TRUE,
    password_policy_require_symbols BOOLEAN NOT NULL DEFAULT FALSE,
    session_timeout_minutes INTEGER NOT NULL DEFAULT 480,
    max_login_attempts INTEGER NOT NULL DEFAULT 5,
    account_lock_duration_minutes INTEGER NOT NULL DEFAULT 30,
    enable_two_factor_auth BOOLEAN NOT NULL DEFAULT FALSE,
    backup_retention_days INTEGER NOT NULL DEFAULT 30,
    data_export_format VARCHAR(20) NOT NULL DEFAULT 'CSV',
    notification_email_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    notification_slack_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    notification_teams_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    custom_css TEXT NULL,
    custom_javascript TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (tenant_id),
    CONSTRAINT fk_tenant_settings_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_tenant_settings_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_tenant_settings_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_tenant_settings_theme_color CHECK (theme_color REGEXP '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT chk_tenant_settings_password_min_length CHECK (password_policy_min_length >= 4 AND password_policy_min_length <= 128),
    CONSTRAINT chk_tenant_settings_session_timeout CHECK (session_timeout_minutes >= 5 AND session_timeout_minutes <= 1440),
    CONSTRAINT chk_tenant_settings_max_login_attempts CHECK (max_login_attempts >= 1 AND max_login_attempts <= 20),
    CONSTRAINT chk_tenant_settings_lock_duration CHECK (account_lock_duration_minutes >= 1 AND account_lock_duration_minutes <= 1440),
    CONSTRAINT chk_tenant_settings_backup_retention CHECK (backup_retention_days >= 1 AND backup_retention_days <= 365),
    CONSTRAINT chk_tenant_settings_export_format CHECK (data_export_format IN ('CSV', 'EXCEL', 'JSON', 'PDF'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. テナント作成時に自動的にデフォルト設定でレコードを作成
2. カスタムCSS/JavaScriptは実行前にセキュリティチェックを実施
3. パスワードポリシーの変更は既存ユーザーには適用されない（次回パスワード変更時から適用）
4. 機能有効化フラグの変更は即座に反映される
5. テーマカラーはHEX形式（#RRGGBB）で指定
6. セッションタイムアウトは5分〜24時間の範囲で設定可能

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成 |
