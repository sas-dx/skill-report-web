# テーブル定義書_HIS_NotificationLog_通知送信履歴

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | HIS_NotificationLog |
| 論理名 | 通知送信履歴 |
| 用途 | 通知送信の履歴を記録・管理 |
| カテゴリ | 履歴系 |
| 作成日 | 2025-05-31 |
| 最終更新日 | 2025-05-31 |

## 概要

システムから送信された全ての通知（メール、Slack、Teams、LINE WORKS等）の送信履歴を記録し、送信状況の追跡、エラー分析、監査に活用するテーブル。

## カラム定義

| No | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト値 | 主キー | 外部キー | 説明 |
|----|----------|--------|----------|------|------|-------------|--------|----------|------|
| 1 | log_id | ログID | BIGINT | - | NOT NULL | AUTO_INCREMENT | ○ | - | 通知ログの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 50 | NOT NULL | - | - | MST_Tenant.tenant_id | 対象テナントID |
| 3 | notification_id | 通知ID | BIGINT | - | NULL | NULL | - | TRN_Notification.notification_id | 関連する通知ID |
| 4 | notification_type | 通知タイプ | VARCHAR | 50 | NOT NULL | - | - | - | 通知種別 |
| 5 | integration_type | 連携タイプ | VARCHAR | 50 | NOT NULL | - | - | - | 送信先システム種別 |
| 6 | integration_config_id | 連携設定ID | BIGINT | - | NULL | NULL | - | SYS_IntegrationConfig.config_id | 使用した連携設定ID |
| 7 | recipient_type | 受信者タイプ | VARCHAR | 20 | NOT NULL | - | - | - | 受信者種別 |
| 8 | recipient_id | 受信者ID | VARCHAR | 100 | NULL | NULL | - | - | 受信者の識別子 |
| 9 | recipient_address | 受信者アドレス | VARCHAR | 500 | NULL | NULL | - | - | 送信先アドレス（メール、チャンネル等） |
| 10 | sender_id | 送信者ID | VARCHAR | 50 | NULL | NULL | - | - | 送信者の識別子 |
| 11 | subject | 件名 | VARCHAR | 500 | NULL | NULL | - | - | 通知の件名・タイトル |
| 12 | message_body | メッセージ本文 | TEXT | - | NULL | NULL | - | - | 通知メッセージの本文 |
| 13 | message_format | メッセージ形式 | VARCHAR | 20 | NOT NULL | 'TEXT' | - | - | メッセージ形式 |
| 14 | priority | 優先度 | VARCHAR | 10 | NOT NULL | 'NORMAL' | - | - | 通知の優先度 |
| 15 | scheduled_at | 送信予定日時 | TIMESTAMP | - | NULL | NULL | - | - | 送信予定日時 |
| 16 | sent_at | 送信日時 | TIMESTAMP | - | NULL | NULL | - | - | 実際の送信日時 |
| 17 | delivery_status | 配信ステータス | VARCHAR | 20 | NOT NULL | 'PENDING' | - | - | 配信状況 |
| 18 | response_code | レスポンスコード | VARCHAR | 10 | NULL | NULL | - | - | 外部システムからのレスポンスコード |
| 19 | response_message | レスポンスメッセージ | TEXT | - | NULL | NULL | - | - | 外部システムからのレスポンスメッセージ |
| 20 | external_message_id | 外部メッセージID | VARCHAR | 200 | NULL | NULL | - | - | 外部システムでのメッセージID |
| 21 | retry_count | リトライ回数 | INT | - | NULL | 0 | - | - | 送信リトライ回数 |
| 22 | max_retry_count | 最大リトライ回数 | INT | - | NULL | 3 | - | - | 最大リトライ回数 |
| 23 | next_retry_at | 次回リトライ日時 | TIMESTAMP | - | NULL | NULL | - | - | 次回リトライ予定日時 |
| 24 | error_code | エラーコード | VARCHAR | 50 | NULL | NULL | - | - | エラーコード |
| 25 | error_message | エラーメッセージ | TEXT | - | NULL | NULL | - | - | エラーメッセージ詳細 |
| 26 | error_details_json | エラー詳細 | JSON | - | NULL | NULL | - | - | エラー詳細情報（JSON形式） |
| 27 | request_headers_json | リクエストヘッダー | JSON | - | NULL | NULL | - | - | 送信時のHTTPヘッダー |
| 28 | response_headers_json | レスポンスヘッダー | JSON | - | NULL | NULL | - | - | 受信したHTTPヘッダー |
| 29 | request_body | リクエストボディ | TEXT | - | NULL | NULL | - | - | 送信したリクエストボディ |
| 30 | response_body | レスポンスボディ | TEXT | - | NULL | NULL | - | - | 受信したレスポンスボディ |
| 31 | processing_time_ms | 処理時間(ms) | INT | - | NULL | NULL | - | - | 送信処理にかかった時間 |
| 32 | file_attachments_json | 添付ファイル情報 | JSON | - | NULL | NULL | - | - | 添付ファイル情報（JSON形式） |
| 33 | template_id | テンプレートID | BIGINT | - | NULL | NULL | - | MST_NotificationTemplate.template_id | 使用した通知テンプレートID |
| 34 | template_variables_json | テンプレート変数 | JSON | - | NULL | NULL | - | - | テンプレート置換変数 |
| 35 | batch_id | バッチID | VARCHAR | 100 | NULL | NULL | - | - | 一括送信時のバッチID |
| 36 | correlation_id | 相関ID | VARCHAR | 100 | NULL | NULL | - | - | 関連処理の追跡用ID |
| 37 | user_agent | ユーザーエージェント | VARCHAR | 500 | NULL | NULL | - | - | 送信時のユーザーエージェント |
| 38 | ip_address | IPアドレス | VARCHAR | 45 | NULL | NULL | - | - | 送信元IPアドレス |
| 39 | is_test | テスト送信フラグ | BOOLEAN | - | NOT NULL | FALSE | - | - | テスト送信かどうか |
| 40 | archived_at | アーカイブ日時 | TIMESTAMP | - | NULL | NULL | - | - | アーカイブされた日時 |
| 41 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | レコード作成日時 |
| 42 | updated_at | 更新日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | レコード更新日時 |
| 43 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | 'SYSTEM' | - | - | レコード作成者 |
| 44 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | 'SYSTEM' | - | - | レコード更新者 |

## 制約

### 主キー制約
- PRIMARY KEY (log_id)

### 外部キー制約
- FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id)
- FOREIGN KEY (notification_id) REFERENCES TRN_Notification(notification_id)
- FOREIGN KEY (integration_config_id) REFERENCES SYS_IntegrationConfig(config_id)
- FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(template_id)

### チェック制約
- CHECK (notification_type IN ('SYSTEM_ALERT', 'USER_NOTIFICATION', 'BATCH_REPORT', 'ERROR_ALERT', 'REMINDER', 'ANNOUNCEMENT'))
- CHECK (integration_type IN ('EMAIL', 'SLACK', 'TEAMS', 'LINE_WORKS', 'WEBHOOK', 'SMS', 'PUSH'))
- CHECK (recipient_type IN ('USER', 'GROUP', 'CHANNEL', 'WEBHOOK', 'SYSTEM'))
- CHECK (message_format IN ('TEXT', 'HTML', 'MARKDOWN', 'JSON'))
- CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT'))
- CHECK (delivery_status IN ('PENDING', 'SENDING', 'SENT', 'DELIVERED', 'FAILED', 'CANCELLED', 'EXPIRED'))
- CHECK (retry_count >= 0)
- CHECK (max_retry_count >= 0)
- CHECK (processing_time_ms >= 0)

## インデックス

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| idx_tenant_created | BTREE | tenant_id, created_at | テナント・作成日時での検索用 |
| idx_notification_type | BTREE | notification_type | 通知タイプでの検索用 |
| idx_integration_type | BTREE | integration_type | 連携タイプでの検索用 |
| idx_delivery_status | BTREE | delivery_status | 配信ステータスでの検索用 |
| idx_sent_at | BTREE | sent_at | 送信日時での検索用 |
| idx_recipient | BTREE | recipient_type, recipient_id | 受信者での検索用 |
| idx_batch_id | BTREE | batch_id | バッチIDでの検索用 |
| idx_correlation_id | BTREE | correlation_id | 相関IDでの検索用 |
| idx_retry_schedule | BTREE | delivery_status, next_retry_at | リトライスケジュール用 |
| idx_archived_at | BTREE | archived_at | アーカイブ日時での検索用 |

## DDL

```sql
CREATE TABLE HIS_NotificationLog (
    log_id BIGINT NOT NULL AUTO_INCREMENT COMMENT 'ログID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    notification_id BIGINT COMMENT '通知ID',
    notification_type VARCHAR(50) NOT NULL COMMENT '通知タイプ',
    integration_type VARCHAR(50) NOT NULL COMMENT '連携タイプ',
    integration_config_id BIGINT COMMENT '連携設定ID',
    recipient_type VARCHAR(20) NOT NULL COMMENT '受信者タイプ',
    recipient_id VARCHAR(100) COMMENT '受信者ID',
    recipient_address VARCHAR(500) COMMENT '受信者アドレス',
    sender_id VARCHAR(50) COMMENT '送信者ID',
    subject VARCHAR(500) COMMENT '件名',
    message_body TEXT COMMENT 'メッセージ本文',
    message_format VARCHAR(20) NOT NULL DEFAULT 'TEXT' COMMENT 'メッセージ形式',
    priority VARCHAR(10) NOT NULL DEFAULT 'NORMAL' COMMENT '優先度',
    scheduled_at TIMESTAMP COMMENT '送信予定日時',
    sent_at TIMESTAMP COMMENT '送信日時',
    delivery_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '配信ステータス',
    response_code VARCHAR(10) COMMENT 'レスポンスコード',
    response_message TEXT COMMENT 'レスポンスメッセージ',
    external_message_id VARCHAR(200) COMMENT '外部メッセージID',
    retry_count INT DEFAULT 0 COMMENT 'リトライ回数',
    max_retry_count INT DEFAULT 3 COMMENT '最大リトライ回数',
    next_retry_at TIMESTAMP COMMENT '次回リトライ日時',
    error_code VARCHAR(50) COMMENT 'エラーコード',
    error_message TEXT COMMENT 'エラーメッセージ',
    error_details_json JSON COMMENT 'エラー詳細',
    request_headers_json JSON COMMENT 'リクエストヘッダー',
    response_headers_json JSON COMMENT 'レスポンスヘッダー',
    request_body TEXT COMMENT 'リクエストボディ',
    response_body TEXT COMMENT 'レスポンスボディ',
    processing_time_ms INT COMMENT '処理時間(ms)',
    file_attachments_json JSON COMMENT '添付ファイル情報',
    template_id BIGINT COMMENT 'テンプレートID',
    template_variables_json JSON COMMENT 'テンプレート変数',
    batch_id VARCHAR(100) COMMENT 'バッチID',
    correlation_id VARCHAR(100) COMMENT '相関ID',
    user_agent VARCHAR(500) COMMENT 'ユーザーエージェント',
    ip_address VARCHAR(45) COMMENT 'IPアドレス',
    is_test BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'テスト送信フラグ',
    archived_at TIMESTAMP COMMENT 'アーカイブ日時',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM' COMMENT '作成者',
    updated_by VARCHAR(50) NOT NULL DEFAULT 'SYSTEM' COMMENT '更新者',
    
    PRIMARY KEY (log_id),
    
    CONSTRAINT fk_notification_log_tenant 
        FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id),
    CONSTRAINT fk_notification_log_notification 
        FOREIGN KEY (notification_id) REFERENCES TRN_Notification(notification_id),
    CONSTRAINT fk_notification_log_integration 
        FOREIGN KEY (integration_config_id) REFERENCES SYS_IntegrationConfig(config_id),
    CONSTRAINT fk_notification_log_template 
        FOREIGN KEY (template_id) REFERENCES MST_NotificationTemplate(template_id),
    
    CONSTRAINT chk_notification_type 
        CHECK (notification_type IN ('SYSTEM_ALERT', 'USER_NOTIFICATION', 'BATCH_REPORT', 'ERROR_ALERT', 'REMINDER', 'ANNOUNCEMENT')),
    CONSTRAINT chk_integration_type 
        CHECK (integration_type IN ('EMAIL', 'SLACK', 'TEAMS', 'LINE_WORKS', 'WEBHOOK', 'SMS', 'PUSH')),
    CONSTRAINT chk_recipient_type 
        CHECK (recipient_type IN ('USER', 'GROUP', 'CHANNEL', 'WEBHOOK', 'SYSTEM')),
    CONSTRAINT chk_message_format 
        CHECK (message_format IN ('TEXT', 'HTML', 'MARKDOWN', 'JSON')),
    CONSTRAINT chk_priority 
        CHECK (priority IN ('LOW', 'NORMAL', 'HIGH', 'URGENT')),
    CONSTRAINT chk_delivery_status 
        CHECK (delivery_status IN ('PENDING', 'SENDING', 'SENT', 'DELIVERED', 'FAILED', 'CANCELLED', 'EXPIRED')),
    CONSTRAINT chk_retry_count 
        CHECK (retry_count >= 0),
    CONSTRAINT chk_max_retry_count 
        CHECK (max_retry_count >= 0),
    CONSTRAINT chk_processing_time 
        CHECK (processing_time_ms >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='通知送信履歴管理テーブル';

-- インデックス作成
CREATE INDEX idx_tenant_created ON HIS_NotificationLog(tenant_id, created_at);
CREATE INDEX idx_notification_type ON HIS_NotificationLog(notification_type);
CREATE INDEX idx_integration_type ON HIS_NotificationLog(integration_type);
CREATE INDEX idx_delivery_status ON HIS_NotificationLog(delivery_status);
CREATE INDEX idx_sent_at ON HIS_NotificationLog(sent_at);
CREATE INDEX idx_recipient ON HIS_NotificationLog(recipient_type, recipient_id);
CREATE INDEX idx_batch_id ON HIS_NotificationLog(batch_id);
CREATE INDEX idx_correlation_id ON HIS_NotificationLog(correlation_id);
CREATE INDEX idx_retry_schedule ON HIS_NotificationLog(delivery_status, next_retry_at);
CREATE INDEX idx_archived_at ON HIS_NotificationLog(archived_at);
```

## 関連テーブル

| テーブル名 | 関係 | 説明 |
|------------|------|------|
| MST_Tenant | 親 | テナント基本情報 |
| TRN_Notification | 親 | 通知基本情報 |
| SYS_IntegrationConfig | 親 | 外部連携設定 |
| MST_NotificationTemplate | 親 | 通知テンプレート |
| SYS_SystemLog | 関連 | システムログ |
| SYS_AuditLog | 関連 | 監査ログ |

## 利用API

| API ID | API名 | 説明 |
|--------|-------|------|
| API-029 | 通知送信API | 通知送信とログ記録 |
| API-201 | 通知一覧取得API | 通知履歴取得 |
| API-202 | 通知詳細取得API | 通知詳細取得 |

## 利用バッチ

| バッチ ID | バッチ名 | 説明 |
|-----------|----------|------|
| BATCH-019-01 | 定期通知送信バッチ | 定期通知の送信とログ記録 |
| BATCH-019-02 | 通知失敗リトライバッチ | 失敗した通知の再送信 |
| BATCH-019-04 | 通知ログクリーンアップバッチ | 古いログの削除・アーカイブ |
| BATCH-406 | メール配信バッチ | メール送信とログ記録 |
| BATCH-407 | Slack連携同期バッチ | Slack通知とログ記録 |
| BATCH-408 | Teams連携同期バッチ | Teams通知とログ記録 |
| BATCH-409 | LINE WORKS連携同期バッチ | LINE WORKS通知とログ記録 |

## 運用考慮事項

### パフォーマンス
- 大量のログデータが蓄積されるため、パーティショニング（月別）を検討
- 古いデータの定期的なアーカイブが必要
- インデックスの最適化とメンテナンス

### ストレージ
- ログデータの圧縮保存を検討
- 長期保存要件に応じたアーカイブ戦略
- 不要なデータの定期削除

### セキュリティ
- 個人情報を含む可能性があるため、適切なアクセス制御
- ログデータの暗号化保存
- 監査要件への対応

### 監視
- 送信失敗率の監視
- 配信遅延の監視
- エラー傾向の分析

## データサンプル

```sql
-- メール送信成功ログ例
INSERT INTO HIS_NotificationLog (
    tenant_id, notification_type, integration_type,
    recipient_type, recipient_address, subject,
    message_body, delivery_status, sent_at,
    response_code, processing_time_ms, created_by, updated_by
) VALUES (
    'tenant001', 'USER_NOTIFICATION', 'EMAIL',
    'USER', 'user@example.com', 'スキル評価完了通知',
    'スキル評価が完了しました。', 'DELIVERED', NOW(),
    '200', 1250, 'SYSTEM', 'SYSTEM'
);

-- Slack送信失敗ログ例
INSERT INTO HIS_NotificationLog (
    tenant_id, notification_type, integration_type,
    recipient_type, recipient_address, subject,
    delivery_status, error_code, error_message,
    retry_count, next_retry_at, created_by, updated_by
) VALUES (
    'tenant001', 'SYSTEM_ALERT', 'SLACK',
    'CHANNEL', '#alerts', 'システムエラー通知',
    'FAILED', 'SLACK_API_ERROR', 'Channel not found',
    1, DATE_ADD(NOW(), INTERVAL 5 MINUTE), 'SYSTEM', 'SYSTEM'
);

-- 一括送信ログ例
INSERT INTO HIS_NotificationLog (
    tenant_id, notification_type, integration_type,
    recipient_type, batch_id, delivery_status,
    created_by, updated_by
) VALUES (
    'tenant001', 'BATCH_REPORT', 'EMAIL',
    'GROUP', 'BATCH_20250531_001', 'SENT',
    'SYSTEM', 'SYSTEM'
);
```

## 変更履歴

| 版数 | 変更日 | 変更者 | 変更内容 |
|------|--------|--------|----------|
| 1.0 | 2025-05-31 | システム管理者 | 初版作成 |
