# テーブル定義書: TRN_Notification

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_Notification |
| 論理名 | 通知履歴 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:02:17 |

## 概要

TRN_Notification（通知履歴）は、システムから送信された各種通知の履歴を管理するトランザクションテーブルです。
主な目的：
- 通知送信履歴の記録・管理
- 通知配信状況の追跡
- 通知効果の分析
- 未読通知の管理
- 通知設定の最適化支援
このテーブルにより、効果的な情報伝達を実現し、
重要な情報の確実な配信と適切なコミュニケーションを支援できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| batch_id | バッチID | VARCHAR | 50 | ○ |  | バッチID |
| notification_id | 通知ID | VARCHAR | 50 | ○ |  | 通知ID |
| title | タイトル | VARCHAR | 200 | ○ |  | タイトル |
| message | メッセージ | TEXT |  | ○ |  | メッセージ |
| action_label | アクションラベル | VARCHAR | 50 | ○ |  | アクションラベル |
| action_url | アクションURL | VARCHAR | 500 | ○ |  | アクションURL |
| archived_at | アーカイブ日時 | TIMESTAMP |  | ○ |  | アーカイブ日時 |
| delivered_at | 配信日時 | TIMESTAMP |  | ○ |  | 配信日時 |
| delivery_method | 配信方法 | ENUM |  | ○ |  | 配信方法 |
| delivery_status | 配信状況 | ENUM |  | ○ | PENDING | 配信状況 |
| device_type | デバイス種別 | ENUM |  | ○ |  | デバイス種別 |
| error_message | エラーメッセージ | TEXT |  | ○ |  | エラーメッセージ |
| expiry_date | 有効期限 | DATE |  | ○ |  | 有効期限 |
| external_message_id | 外部メッセージID | VARCHAR | 100 | ○ |  | 外部メッセージID |
| ip_address | IPアドレス | VARCHAR | 45 | ○ |  | IPアドレス |
| is_bulk_notification | 一括通知フラグ | BOOLEAN |  | ○ | False | 一括通知フラグ |
| last_retry_at | 最終再送日時 | TIMESTAMP |  | ○ |  | 最終再送日時 |
| max_retry_count | 最大再送回数 | INTEGER |  | ○ | 3 | 最大再送回数 |
| message_format | メッセージ形式 | ENUM |  | ○ | PLAIN | メッセージ形式 |
| notification_category | 通知カテゴリ | ENUM |  | ○ |  | 通知カテゴリ |
| notification_type | 通知種別 | ENUM |  | ○ |  | 通知種別 |
| personalization_data | パーソナライゼーションデータ | TEXT |  | ○ |  | パーソナライゼーションデータ |
| priority_level | 優先度 | ENUM |  | ○ | NORMAL | 優先度 |
| read_at | 既読日時 | TIMESTAMP |  | ○ |  | 既読日時 |
| read_status | 既読状況 | ENUM |  | ○ | UNREAD | 既読状況 |
| recipient_id | 受信者ID | VARCHAR | 50 | ○ |  | 受信者ID |
| related_entity_id | 関連エンティティID | VARCHAR | 50 | ○ |  | 関連エンティティID |
| related_entity_type | 関連エンティティ種別 | ENUM |  | ○ |  | 関連エンティティ種別 |
| retry_count | 再送回数 | INTEGER |  | ○ | 0 | 再送回数 |
| sender_id | 送信者ID | VARCHAR | 50 | ○ |  | 送信者ID |
| sent_at | 送信日時 | TIMESTAMP |  | ○ |  | 送信日時 |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | テンプレートID |
| template_variables | テンプレート変数 | TEXT |  | ○ |  | テンプレート変数 |
| user_agent | ユーザーエージェント | VARCHAR | 500 | ○ |  | ユーザーエージェント |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_id | notification_id | ○ |  |
| idx_recipient_id | recipient_id | × |  |
| idx_sender_id | sender_id | × |  |
| idx_notification_type | notification_type | × |  |
| idx_notification_category | notification_category | × |  |
| idx_priority_level | priority_level | × |  |
| idx_delivery_method | delivery_method | × |  |
| idx_delivery_status | delivery_status | × |  |
| idx_read_status | read_status | × |  |
| idx_sent_at | sent_at | × |  |
| idx_recipient_unread | recipient_id, read_status, expiry_date | × |  |
| idx_batch_id | batch_id | × |  |
| idx_related_entity | related_entity_type, related_entity_id | × |  |
| idx_trn_notification_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_notification_recipient | recipient_id | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_notification_sender | sender_id | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_notification_id | UNIQUE |  | notification_id一意制約 |
| chk_delivery_status | CHECK | delivery_status IN (...) | delivery_status値チェック制約 |
| chk_device_type | CHECK | device_type IN (...) | device_type値チェック制約 |
| chk_notification_type | CHECK | notification_type IN (...) | notification_type値チェック制約 |
| chk_read_status | CHECK | read_status IN (...) | read_status値チェック制約 |
| chk_related_entity_type | CHECK | related_entity_type IN (...) | related_entity_type値チェック制約 |

## サンプルデータ

| notification_id | recipient_id | sender_id | notification_type | notification_category | priority_level | title | message | message_format | action_url | action_label | delivery_method | delivery_status | sent_at | delivered_at | read_status | read_at | archived_at | expiry_date | retry_count | max_retry_count | last_retry_at | error_message | external_message_id | template_id | template_variables | related_entity_type | related_entity_id | batch_id | user_agent | ip_address | device_type | is_bulk_notification | personalization_data |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| NOTIF_001 | EMP000001 | None | REMINDER | CERTIFICATION | HIGH | AWS認定資格の更新期限が近づいています | お持ちのAWS認定ソリューションアーキテクト資格の有効期限が30日後に迫っています。更新手続きをお忘れなく。 | PLAIN | /certifications/renewal/CERT_AWS_001 | 更新手続きへ | EMAIL | DELIVERED | 2024-05-01 09:00:00 | 2024-05-01 09:01:23 | READ | 2024-05-01 10:30:45 | None | 2024-06-01 | 0 | 3 | None | None | email_12345 | TMPL_CERT_RENEWAL | {"certification_name": "AWS認定ソリューションアーキテクト", "days_until_expiry": 30} | CERTIFICATION | CERT_AWS_001 | None | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 | 192.168.1.100 | PC | False | {"preferred_language": "ja", "timezone": "Asia/Tokyo"} |
| NOTIF_002 | EMP000002 | EMP000010 | APPROVAL | TRAINING | NORMAL | 研修参加申請が承認されました | 申請いただいた「プロジェクトマネジメント基礎研修」への参加が承認されました。研修日程をご確認ください。 | HTML | /training/details/TRN_PROG_001 | 研修詳細を確認 | IN_APP | DELIVERED | 2024-04-15 14:30:00 | 2024-04-15 14:30:01 | READ | 2024-04-15 15:45:20 | 2024-04-20 10:00:00 | None | 0 | 3 | None | None | None | TMPL_TRAINING_APPROVAL | {"training_name": "プロジェクトマネジメント基礎研修", "approver_name": "田中部長"} | TRAINING | TRN_PROG_001 | None | Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) | 192.168.1.101 | MOBILE | False | {"preferred_language": "ja", "notification_sound": true} |

## 特記事項

- 配信方法により外部サービスとの連携が必要
- 再送機能により重要な通知の確実な配信を保証
- 既読状況の追跡により通知効果を測定
- テンプレート機能により一貫した通知フォーマットを維持
- バッチ送信により大量通知の効率的な配信が可能
- パーソナライゼーション機能により個人に最適化された通知を提供
- 通知IDは一意である必要がある
- 再送回数は最大再送回数以下である必要がある
- 既読日時は送信日時以降である必要がある
- アーカイブ日時は既読日時以降である必要がある
- 緊急通知は即座に配信される必要がある
- 有効期限切れの通知は自動的に非表示
- 配信失敗時は設定された回数まで自動再送
- 一括通知はバッチIDで管理

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知履歴テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222632 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |