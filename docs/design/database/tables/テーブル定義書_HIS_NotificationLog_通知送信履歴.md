# テーブル定義書: HIS_NotificationLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_NotificationLog |
| 論理名 | 通知送信履歴 |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-24 23:05:57 |

## 概要

HIS_NotificationLog（通知送信履歴）は、システムから送信された全ての通知の履歴を管理するテーブルです。
主な目的：
- 通知送信の履歴管理
- 送信成功・失敗の記録
- 通知配信の監査証跡
- 通知システムの分析・改善データ
- 再送処理のための情報管理
このテーブルは、通知・連携管理機能において送信状況の把握と品質向上を支える重要な履歴データです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| notification_id | 通知ID | VARCHAR | 50 | ○ |  | 通知ID |
| subject | 件名 | VARCHAR | 500 | ○ |  | 件名 |
| delivered_at | 配信確認日時 | TIMESTAMP |  | ○ |  | 配信確認日時 |
| error_details | エラー詳細 | TEXT |  | ○ |  | エラー詳細 |
| integration_config_id | 連携設定ID | VARCHAR | 50 | ○ |  | 連携設定ID |
| max_retry_count | 最大リトライ回数 | INTEGER |  | ○ | 3 | 最大リトライ回数 |
| message_body | メッセージ本文 | TEXT |  | ○ |  | メッセージ本文 |
| message_format | メッセージフォーマット | ENUM |  | ○ |  | メッセージフォーマット |
| notification_type | 通知タイプ | ENUM |  | ○ |  | 通知タイプ |
| notificationlog_id | HIS_NotificationLogの主キー | SERIAL |  | × |  | HIS_NotificationLogの主キー |
| opened_at | 開封日時 | TIMESTAMP |  | ○ |  | 開封日時 |
| priority_level | 優先度レベル | ENUM |  | ○ | MEDIUM | 優先度レベル |
| recipient_address | 受信者アドレス | VARCHAR | 500 | ○ |  | 受信者アドレス |
| recipient_type | 受信者タイプ | ENUM |  | ○ |  | 受信者タイプ |
| response_code | レスポンスコード | VARCHAR | 20 | ○ |  | レスポンスコード |
| response_message | レスポンスメッセージ | TEXT |  | ○ |  | レスポンスメッセージ |
| scheduled_at | 送信予定日時 | TIMESTAMP |  | ○ |  | 送信予定日時 |
| send_attempts | 送信試行回数 | INTEGER |  | ○ | 0 | 送信試行回数 |
| send_status | 送信状態 | ENUM |  | ○ |  | 送信状態 |
| sent_at | 送信日時 | TIMESTAMP |  | ○ |  | 送信日時 |
| setting_id | 設定ID | VARCHAR | 50 | ○ |  | 設定ID |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | テンプレートID |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_log_notification | notification_id | × |  |
| idx_notification_log_tenant_status | tenant_id, send_status | × |  |
| idx_notification_log_type | notification_type | × |  |
| idx_notification_log_scheduled | scheduled_at | × |  |
| idx_notification_log_sent | sent_at | × |  |
| idx_notification_log_status_attempts | send_status, send_attempts | × |  |
| idx_notification_log_priority | priority_level, scheduled_at | × |  |
| idx_his_notificationlog_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_notification_log_notification | notification_id | TRN_Notification | id | CASCADE | CASCADE | 外部キー制約 |
| fk_notification_log_setting | setting_id | MST_NotificationSettings | id | CASCADE | SET NULL | 外部キー制約 |
| fk_notification_log_template | template_id | MST_NotificationTemplate | id | CASCADE | SET NULL | 外部キー制約 |
| fk_notification_log_integration | integration_config_id | SYS_IntegrationConfig | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_notification_type | CHECK | notification_type IN (...) | notification_type値チェック制約 |
| chk_recipient_type | CHECK | recipient_type IN (...) | recipient_type値チェック制約 |
| chk_send_status | CHECK | send_status IN (...) | send_status値チェック制約 |

## サンプルデータ

| id | tenant_id | notification_id | setting_id | template_id | notification_type | recipient_type | recipient_address | subject | message_body | message_format | send_status | send_attempts | max_retry_count | scheduled_at | sent_at | delivered_at | opened_at | response_code | response_message | error_details | integration_config_id | priority_level |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| NL001 | TENANT001 | NOTIF001 | NS001 | NT001 | EMAIL | USER | yamada.taro@company.com | 【スキル更新】山田太郎さんのスキル情報が更新されました | 山田太郎さん

以下のスキル情報が更新されました。

スキル名: Java
更新日時: 2025-06-01 10:30:00
更新者: 佐藤花子

詳細は以下のリンクからご確認ください。
https://system.company.com/skills/123

※このメールは自動送信されています。 | PLAIN | SUCCESS | 1 | 3 | 2025-06-01 10:30:00 | 2025-06-01 10:30:15 | 2025-06-01 10:30:45 | 2025-06-01 11:15:30 | 250 | Message accepted for delivery | None | IC003 | MEDIUM |
| NL002 | TENANT001 | NOTIF002 | NS002 | NT002 | SLACK | CHANNEL | #notifications | None | :warning: *目標期限のお知らせ* :warning:

山田太郎さんの目標「Java認定資格取得」の期限が近づいています。

• 期限: 2025-06-30
• 残り日数: 29日
• 進捗率: 75%

<https://system.company.com/goals/456|詳細を確認する> | MARKDOWN | FAILED | 3 | 3 | 2025-06-01 09:00:00 | None | None | None | 404 | channel_not_found | {"error": "channel_not_found", "details": "The specified channel does not exist or the bot is not a member"} | IC001 | HIGH |

## 特記事項

- 通知送信履歴は2年間保持される
- 受信者アドレスは個人情報のため暗号化必須
- エラー詳細はJSON形式で構造化された情報を格納
- 配信確認・開封確認は対応している通知チャネルでのみ記録
- リトライ処理は最大試行回数まで自動実行
- 送信状態により後続処理を制御
- 優先度により送信順序を制御
- 送信試行回数は最大リトライ回数+1を超えない
- 成功した通知は再送不可
- 失敗した通知は設定された回数までリトライ
- 高優先度の通知は優先的に送信処理
- 送信予定日時を過ぎた通知は期限切れとして処理
- 受信者アドレスは送信時に暗号化して保存
- エラー詳細は障害分析のため詳細に記録
- 配信確認機能は通知チャネルの対応状況に依存

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知送信履歴テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223431 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |