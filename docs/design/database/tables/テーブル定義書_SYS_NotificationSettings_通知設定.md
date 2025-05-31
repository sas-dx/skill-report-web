# テーブル定義書：通知設定 (SYS_NotificationSettings)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-025 |
| **テーブル名** | SYS_NotificationSettings |
| **論理名** | 通知設定 |
| **カテゴリ** | システム系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
通知設定テーブル（SYS_NotificationSettings）は、システム全体およびテナント固有の通知設定を管理します。メール、Slack、Teams、LINE WORKSなどの各種通知チャネルの設定情報を格納し、通知の送信制御を行います。

### 2.2 関連API
- [API-201](../api/specs/API仕様書_API-201_通知一覧取得API.md) - 通知一覧取得API
- [API-202](../api/specs/API仕様書_API-202_通知詳細取得API.md) - 通知詳細取得API

### 2.3 関連バッチ
- [BATCH-401](../batch/specs/バッチ定義書_BATCH-401_定期通知送信バッチ.md) - 定期通知送信バッチ
- [BATCH-402](../batch/specs/バッチ定義書_BATCH-402_通知失敗リトライバッチ.md) - 通知失敗リトライバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | setting_id | 設定ID | VARCHAR | 50 | × | ○ | - | - | 通知設定を一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | テナントID（NULL=システム全体設定） |
| 3 | notification_type | 通知タイプ | VARCHAR | 50 | × | - | - | - | 通知の種類（SKILL_UPDATE/GOAL_REMINDER等） |
| 4 | channel_type | チャネルタイプ | VARCHAR | 20 | × | - | - | - | 通知チャネル（EMAIL/SLACK/TEAMS/LINEWORKS） |
| 5 | is_enabled | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 通知設定が有効かどうか |
| 6 | email_smtp_host | SMTPホスト | VARCHAR | 255 | ○ | - | - | NULL | メール送信用SMTPサーバーホスト |
| 7 | email_smtp_port | SMTPポート | INTEGER | - | ○ | - | - | NULL | メール送信用SMTPサーバーポート |
| 8 | email_smtp_user | SMTPユーザー | VARCHAR | 255 | ○ | - | - | NULL | SMTP認証用ユーザー名 |
| 9 | email_smtp_password | SMTPパスワード | VARCHAR | 255 | ○ | - | - | NULL | SMTP認証用パスワード（暗号化） |
| 10 | email_from_address | 送信者アドレス | VARCHAR | 255 | ○ | - | - | NULL | メール送信者アドレス |
| 11 | email_from_name | 送信者名 | VARCHAR | 100 | ○ | - | - | NULL | メール送信者名 |
| 12 | slack_webhook_url | Slack Webhook URL | VARCHAR | 500 | ○ | - | - | NULL | Slack通知用WebhookURL |
| 13 | slack_channel | Slackチャネル | VARCHAR | 100 | ○ | - | - | NULL | Slack通知先チャネル |
| 14 | slack_username | Slackユーザー名 | VARCHAR | 100 | ○ | - | - | NULL | Slack通知時の表示ユーザー名 |
| 15 | teams_webhook_url | Teams Webhook URL | VARCHAR | 500 | ○ | - | - | NULL | Teams通知用WebhookURL |
| 16 | lineworks_api_id | LINE WORKS API ID | VARCHAR | 100 | ○ | - | - | NULL | LINE WORKS API ID |
| 17 | lineworks_server_api_consumer_key | LINE WORKS Consumer Key | VARCHAR | 255 | ○ | - | - | NULL | LINE WORKS Consumer Key |
| 18 | lineworks_server_list_id | LINE WORKS Server List ID | VARCHAR | 100 | ○ | - | - | NULL | LINE WORKS Server List ID |
| 19 | lineworks_private_key | LINE WORKS Private Key | TEXT | - | ○ | - | - | NULL | LINE WORKS Private Key（暗号化） |
| 20 | template_subject | テンプレート件名 | VARCHAR | 200 | ○ | - | - | NULL | 通知テンプレートの件名 |
| 21 | template_body | テンプレート本文 | TEXT | - | ○ | - | - | NULL | 通知テンプレートの本文 |
| 22 | retry_count | リトライ回数 | INTEGER | - | × | - | - | 3 | 送信失敗時のリトライ回数 |
| 23 | retry_interval_minutes | リトライ間隔 | INTEGER | - | × | - | - | 5 | リトライ間隔（分） |
| 24 | is_active | アクティブフラグ | BOOLEAN | - | × | - | - | TRUE | 設定がアクティブかどうか |
| 25 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 26 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 27 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 28 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | setting_id | 主キー |
| idx_tenant_type_channel | UNIQUE | tenant_id, notification_type, channel_type | テナント・通知タイプ・チャネルの組み合わせ |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_notification_type | INDEX | notification_type | 通知タイプ検索用 |
| idx_channel_type | INDEX | channel_type | チャネルタイプ検索用 |
| idx_enabled | INDEX | is_enabled | 有効フラグ検索用 |
| idx_active | INDEX | is_active | アクティブフラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_notification_settings | PRIMARY KEY | setting_id | 主キー制約 |
| uq_tenant_type_channel | UNIQUE | tenant_id, notification_type, channel_type | テナント・通知タイプ・チャネルの一意性 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_channel_type | CHECK | channel_type | channel_type IN ('EMAIL', 'SLACK', 'TEAMS', 'LINEWORKS') |
| chk_retry_count | CHECK | retry_count | retry_count >= 0 AND retry_count <= 10 |
| chk_retry_interval | CHECK | retry_interval_minutes | retry_interval_minutes >= 1 AND retry_interval_minutes <= 1440 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| HIS_NotificationLog | setting_id | 1:N | 通知送信履歴 |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO SYS_NotificationSettings (
    setting_id, tenant_id, notification_type, channel_type,
    email_smtp_host, email_smtp_port, email_from_address,
    template_subject, template_body, created_by, updated_by
) VALUES (
    'notify_001',
    'tenant001',
    'SKILL_UPDATE',
    'EMAIL',
    'smtp.example.com',
    587,
    'noreply@example.com',
    'スキル情報が更新されました',
    'あなたのスキル情報が更新されました。詳細を確認してください。',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 100件 | 基本通知設定 |
| 年間増加件数 | 200件 | 新規テナント・カスタム設定 |
| 5年後想定件数 | 1,100件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：論理削除から1年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id, notification_type | 通知設定取得 |
| SELECT | 高 | channel_type, is_enabled | 有効な通知設定取得 |
| UPDATE | 中 | setting_id | 設定更新 |
| INSERT | 低 | - | 新規設定作成 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| application | ○ | × | × | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（API キー、パスワード）
- 暗号化：パスワード、APIキー、秘密鍵は必須

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存通知設定ファイル
- 移行方法：設定移行スクリプト
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE SYS_NotificationSettings (
    setting_id VARCHAR(50) NOT NULL,
    tenant_id VARCHAR(50) NULL,
    notification_type VARCHAR(50) NOT NULL,
    channel_type VARCHAR(20) NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT TRUE,
    email_smtp_host VARCHAR(255) NULL,
    email_smtp_port INTEGER NULL,
    email_smtp_user VARCHAR(255) NULL,
    email_smtp_password VARCHAR(255) NULL,
    email_from_address VARCHAR(255) NULL,
    email_from_name VARCHAR(100) NULL,
    slack_webhook_url VARCHAR(500) NULL,
    slack_channel VARCHAR(100) NULL,
    slack_username VARCHAR(100) NULL,
    teams_webhook_url VARCHAR(500) NULL,
    lineworks_api_id VARCHAR(100) NULL,
    lineworks_server_api_consumer_key VARCHAR(255) NULL,
    lineworks_server_list_id VARCHAR(100) NULL,
    lineworks_private_key TEXT NULL,
    template_subject VARCHAR(200) NULL,
    template_body TEXT NULL,
    retry_count INTEGER NOT NULL DEFAULT 3,
    retry_interval_minutes INTEGER NOT NULL DEFAULT 5,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (setting_id),
    UNIQUE KEY idx_tenant_type_channel (tenant_id, notification_type, channel_type),
    INDEX idx_tenant (tenant_id),
    INDEX idx_notification_type (notification_type),
    INDEX idx_channel_type (channel_type),
    INDEX idx_enabled (is_enabled),
    INDEX idx_active (is_active),
    CONSTRAINT fk_notification_settings_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_notification_settings_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_notification_settings_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_notification_settings_channel_type CHECK (channel_type IN ('EMAIL', 'SLACK', 'TEAMS', 'LINEWORKS')),
    CONSTRAINT chk_notification_settings_retry_count CHECK (retry_count >= 0 AND retry_count <= 10),
    CONSTRAINT chk_notification_settings_retry_interval CHECK (retry_interval_minutes >= 1 AND retry_interval_minutes <= 1440)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. tenant_idがNULLの場合はシステム全体のデフォルト設定
2. パスワードやAPIキーは暗号化して保存
3. 同一テナント・通知タイプ・チャネルの組み合わせは一意
4. 通知テンプレートには変数置換機能を提供
5. リトライ設定は通知チャネルごとに個別設定可能
6. 設定変更時は既存の通知キューには影響しない

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
