# テーブル定義書：通知履歴 (TRN_Notification)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-013 |
| **テーブル名** | TRN_Notification |
| **論理名** | 通知履歴 |
| **カテゴリ** | トランザクション系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
通知履歴テーブル（TRN_Notification）は、システムから送信された全ての通知の履歴を管理します。メール、Slack、Teams等の多様な通知チャネルでの送信結果を記録し、通知の配信状況と効果測定を支援します。

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
| 1 | notification_id | 通知ID | VARCHAR | 20 | × | ○ | - | - | 通知を一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 通知対象のテナントID |
| 3 | recipient_id | 受信者ID | VARCHAR | 20 | × | - | ○ | - | 通知受信者の社員ID |
| 4 | notification_type | 通知タイプ | VARCHAR | 50 | × | - | - | - | 通知の種類（SKILL_EVALUATION/DEADLINE_REMINDER等） |
| 5 | notification_channel | 通知チャネル | VARCHAR | 20 | × | - | - | - | 通知手段（EMAIL/SLACK/TEAMS/LINE_WORKS/IN_APP） |
| 6 | priority | 優先度 | VARCHAR | 10 | × | - | - | 'NORMAL' | 通知の優先度（HIGH/NORMAL/LOW） |
| 7 | title | タイトル | VARCHAR | 200 | × | - | - | - | 通知のタイトル |
| 8 | message | メッセージ | TEXT | - | × | - | - | - | 通知の本文 |
| 9 | message_html | HTMLメッセージ | TEXT | - | ○ | - | - | NULL | HTML形式の通知本文 |
| 10 | template_id | テンプレートID | VARCHAR | 50 | ○ | - | - | NULL | 使用した通知テンプレートのID |
| 11 | template_variables | テンプレート変数 | JSON | - | ○ | - | - | NULL | テンプレートに渡した変数（JSON形式） |
| 12 | recipient_email | 受信者メールアドレス | VARCHAR | 255 | ○ | - | - | NULL | メール通知の宛先 |
| 13 | recipient_slack_id | SlackユーザーID | VARCHAR | 50 | ○ | - | - | NULL | Slack通知の宛先 |
| 14 | recipient_teams_id | TeamsユーザーID | VARCHAR | 50 | ○ | - | - | NULL | Teams通知の宛先 |
| 15 | recipient_line_id | LINE WORKSユーザーID | VARCHAR | 50 | ○ | - | - | NULL | LINE WORKS通知の宛先 |
| 16 | scheduled_at | 送信予定日時 | TIMESTAMP | - | × | - | - | - | 通知の送信予定日時 |
| 17 | sent_at | 送信日時 | TIMESTAMP | - | ○ | - | - | NULL | 実際の送信日時 |
| 18 | delivery_status | 配信ステータス | VARCHAR | 20 | × | - | - | 'PENDING' | 配信状況 |
| 19 | delivery_attempts | 配信試行回数 | INTEGER | - | × | - | - | 0 | 配信を試行した回数 |
| 20 | last_attempt_at | 最終試行日時 | TIMESTAMP | - | ○ | - | - | NULL | 最後に配信を試行した日時 |
| 21 | error_message | エラーメッセージ | TEXT | - | ○ | - | - | NULL | 配信失敗時のエラー内容 |
| 22 | external_message_id | 外部メッセージID | VARCHAR | 100 | ○ | - | - | NULL | 外部サービスでのメッセージID |
| 23 | read_at | 既読日時 | TIMESTAMP | - | ○ | - | - | NULL | 通知が既読された日時 |
| 24 | clicked_at | クリック日時 | TIMESTAMP | - | ○ | - | - | NULL | 通知内リンクがクリックされた日時 |
| 25 | action_taken | アクション実行フラグ | BOOLEAN | - | × | - | - | FALSE | 通知に対してアクションが実行されたか |
| 26 | action_taken_at | アクション実行日時 | TIMESTAMP | - | ○ | - | - | NULL | アクションが実行された日時 |
| 27 | related_record_type | 関連レコードタイプ | VARCHAR | 50 | ○ | - | - | NULL | 関連するレコードの種類 |
| 28 | related_record_id | 関連レコードID | VARCHAR | 20 | ○ | - | - | NULL | 関連するレコードのID |
| 29 | expires_at | 有効期限 | TIMESTAMP | - | ○ | - | - | NULL | 通知の有効期限 |
| 30 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 通知が有効かどうか |
| 31 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 32 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 33 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 34 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | notification_id | 主キー |
| idx_tenant_recipient | INDEX | tenant_id, recipient_id | テナント・受信者検索用 |
| idx_recipient | INDEX | recipient_id | 受信者検索用 |
| idx_type | INDEX | notification_type | 通知タイプ検索用 |
| idx_channel | INDEX | notification_channel | 通知チャネル検索用 |
| idx_status | INDEX | delivery_status | 配信ステータス検索用 |
| idx_scheduled | INDEX | scheduled_at | 送信予定日時検索用 |
| idx_sent | INDEX | sent_at | 送信日時検索用 |
| idx_priority | INDEX | priority | 優先度検索用 |
| idx_related | INDEX | related_record_type, related_record_id | 関連レコード検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_notification | PRIMARY KEY | notification_id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_recipient | FOREIGN KEY | recipient_id | MST_Employee.employee_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_notification_channel | CHECK | notification_channel | notification_channel IN ('EMAIL', 'SLACK', 'TEAMS', 'LINE_WORKS', 'IN_APP') |
| chk_priority | CHECK | priority | priority IN ('HIGH', 'NORMAL', 'LOW') |
| chk_delivery_status | CHECK | delivery_status | delivery_status IN ('PENDING', 'SENT', 'DELIVERED', 'FAILED', 'EXPIRED') |
| chk_delivery_attempts | CHECK | delivery_attempts | delivery_attempts >= 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_Employee | recipient_id | 1:N | 受信者 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | なし |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO TRN_Notification (
    notification_id, tenant_id, recipient_id,
    notification_type, notification_channel, priority,
    title, message, recipient_email,
    scheduled_at, delivery_status, related_record_type,
    related_record_id, created_by, updated_by
) VALUES (
    'NOTIF_001',
    'TENANT_001',
    'EMP_001',
    'SKILL_EVALUATION_REMINDER',
    'EMAIL',
    'NORMAL',
    'スキル評価期限のお知らせ',
    'スキル評価の期限が近づいています。期限：2024年3月31日までに評価を完了してください。',
    'employee001@company.com',
    '2024-03-25 09:00:00',
    'SENT',
    'SKILL_EVALUATION',
    'REC_001',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 新規システム |
| 日間増加件数 | 10,000件 | 通知送信数 |
| 月間増加件数 | 300,000件 | 想定値 |
| 年間増加件数 | 3,600,000件 | 想定値 |
| 5年後想定件数 | 18,000,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：created_at（月単位）

### 6.3 アーカイブ
- アーカイブ条件：作成日から1年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | recipient_id, is_active | 受信者別通知一覧取得 |
| SELECT | 高 | delivery_status | 配信状況別通知取得 |
| SELECT | 中 | notification_type | 通知タイプ別取得 |
| SELECT | 中 | scheduled_at | 送信予定日時別取得 |
| UPDATE | 高 | notification_id | 配信状況更新 |
| INSERT | 高 | - | 新規通知作成 |

### 7.2 パフォーマンス要件
- SELECT：20ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| notification_admin | ○ | ○ | ○ | × | 通知管理者 |
| manager | ○ | ○ | ○ | × | 管理職（部下のみ） |
| employee | ○ | × | ○ | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（受信者情報）
- 機密情報：含む（通知内容）
- 暗号化：必要（メッセージ内容）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存通知システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE TRN_Notification (
    notification_id VARCHAR(20) NOT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    recipient_id VARCHAR(20) NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    notification_channel VARCHAR(20) NOT NULL,
    priority VARCHAR(10) NOT NULL DEFAULT 'NORMAL',
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    message_html TEXT NULL,
    template_id VARCHAR(50) NULL,
    template_variables JSON NULL,
    recipient_email VARCHAR(255) NULL,
    recipient_slack_id VARCHAR(50) NULL,
    recipient_teams_id VARCHAR(50) NULL,
    recipient_line_id VARCHAR(50) NULL,
    scheduled_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP NULL,
    delivery_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    delivery_attempts INTEGER NOT NULL DEFAULT 0,
    last_attempt_at TIMESTAMP NULL,
    error_message TEXT NULL,
    external_message_id VARCHAR(100) NULL,
    read_at TIMESTAMP NULL,
    clicked_at TIMESTAMP NULL,
    action_taken BOOLEAN NOT NULL DEFAULT FALSE,
    action_taken_at TIMESTAMP NULL,
    related_record_type VARCHAR(50) NULL,
    related_record_id VARCHAR(20) NULL,
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (notification_id),
    INDEX idx_tenant_recipient (tenant_id, recipient_id),
    INDEX idx_recipient (recipient_id),
    INDEX idx_type (notification_type),
    INDEX idx_channel (notification_channel),
    INDEX idx_status (delivery_status),
    INDEX idx_scheduled (scheduled_at),
    INDEX idx_sent (sent_at),
    INDEX idx_priority (priority),
    INDEX idx_related (related_record_type, related_record_id),
    INDEX idx_active (is_active),
    CONSTRAINT fk_notification_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_notification_recipient FOREIGN KEY (recipient_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_notification_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_notification_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_notification_channel CHECK (notification_channel IN ('EMAIL', 'SLACK', 'TEAMS', 'LINE_WORKS', 'IN_APP')),
    CONSTRAINT chk_notification_priority CHECK (priority IN ('HIGH', 'NORMAL', 'LOW')),
    CONSTRAINT chk_notification_delivery_status CHECK (delivery_status IN ('PENDING', 'SENT', 'DELIVERED', 'FAILED', 'EXPIRED')),
    CONSTRAINT chk_notification_delivery_attempts CHECK (delivery_attempts >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. 多様な通知チャネル（メール/Slack/Teams/LINE WORKS/アプリ内）に対応
2. 通知テンプレート機能によるメッセージの標準化
3. 配信失敗時の自動リトライ機能
4. 通知の既読・クリック・アクション実行状況の追跡
5. 優先度による通知の重要度管理
6. 関連レコードとの紐付けによるコンテキスト管理
7. パーティション設計による大量データの効率的管理
8. 通知内容の暗号化による機密性保護
9. 有効期限による通知の自動無効化
10. 配信統計とKPI測定のためのメトリクス収集

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
