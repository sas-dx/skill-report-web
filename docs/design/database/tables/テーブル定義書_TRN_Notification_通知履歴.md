# テーブル定義書: TRN_Notification

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_Notification |
| 論理名 | 通知履歴 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| notification_id | 通知ID | VARCHAR | 50 | ○ |  | 通知を一意に識別するID |
| recipient_id | 受信者ID | VARCHAR | 50 | ○ |  | 通知受信者の社員ID（MST_Employeeへの外部キー） |
| sender_id | 送信者ID | VARCHAR | 50 | ○ |  | 通知送信者の社員ID（システム送信の場合はNULL） |
| notification_type | 通知種別 | ENUM |  | ○ |  | 通知の種別（SYSTEM:システム、REMINDER:リマインダー、APPROVAL:承認、ALERT:アラート、INFO:情報、URGENT:緊急） |
| notification_category | 通知カテゴリ | ENUM |  | ○ |  | 通知の分類（SKILL:スキル関連、TRAINING:研修関連、PROJECT:プロジェクト関連、CERTIFICATION:資格関連、SYSTEM:システム関連、HR:人事関連） |
| priority_level | 優先度 | ENUM |  | ○ | NORMAL | 通知の優先度（LOW:低、NORMAL:通常、HIGH:高、CRITICAL:緊急） |
| title | タイトル | VARCHAR | 200 | ○ |  | 通知のタイトル・件名 |
| message | メッセージ | TEXT |  | ○ |  | 通知の本文メッセージ |
| message_format | メッセージ形式 | ENUM |  | ○ | PLAIN | メッセージの形式（PLAIN:プレーンテキスト、HTML:HTML、MARKDOWN:Markdown） |
| action_url | アクションURL | VARCHAR | 500 | ○ |  | 通知に関連するアクションのURL |
| action_label | アクションラベル | VARCHAR | 50 | ○ |  | アクションボタンのラベル |
| delivery_method | 配信方法 | ENUM |  | ○ |  | 通知の配信方法（IN_APP:アプリ内、EMAIL:メール、SLACK:Slack、TEAMS:Teams、LINE_WORKS:LINE WORKS、SMS:SMS） |
| delivery_status | 配信状況 | ENUM |  | ○ | PENDING | 配信状況（PENDING:配信待ち、SENT:送信済み、DELIVERED:配信完了、FAILED:配信失敗、BOUNCED:バウンス） |
| sent_at | 送信日時 | TIMESTAMP |  | ○ |  | 通知が送信された日時 |
| delivered_at | 配信日時 | TIMESTAMP |  | ○ |  | 通知が配信された日時 |
| read_status | 既読状況 | ENUM |  | ○ | UNREAD | 既読状況（UNREAD:未読、READ:既読、ARCHIVED:アーカイブ済み） |
| read_at | 既読日時 | TIMESTAMP |  | ○ |  | 通知が既読になった日時 |
| archived_at | アーカイブ日時 | TIMESTAMP |  | ○ |  | 通知がアーカイブされた日時 |
| expiry_date | 有効期限 | DATE |  | ○ |  | 通知の有効期限 |
| retry_count | 再送回数 | INTEGER |  | ○ | 0 | 配信失敗時の再送回数 |
| max_retry_count | 最大再送回数 | INTEGER |  | ○ | 3 | 最大再送回数 |
| last_retry_at | 最終再送日時 | TIMESTAMP |  | ○ |  | 最後に再送を試行した日時 |
| error_message | エラーメッセージ | TEXT |  | ○ |  | 配信失敗時のエラーメッセージ |
| external_message_id | 外部メッセージID | VARCHAR | 100 | ○ |  | 外部サービス（メール、Slack等）のメッセージID |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | 使用した通知テンプレートのID |
| template_variables | テンプレート変数 | TEXT |  | ○ |  | テンプレートに渡した変数（JSON形式） |
| related_entity_type | 関連エンティティ種別 | ENUM |  | ○ |  | 関連するエンティティの種別（PROJECT:プロジェクト、TRAINING:研修、CERTIFICATION:資格、SKILL:スキル、EMPLOYEE:社員） |
| related_entity_id | 関連エンティティID | VARCHAR | 50 | ○ |  | 関連するエンティティのID |
| batch_id | バッチID | VARCHAR | 50 | ○ |  | 一括送信時のバッチID |
| user_agent | ユーザーエージェント | VARCHAR | 500 | ○ |  | 既読時のユーザーエージェント情報 |
| ip_address | IPアドレス | VARCHAR | 45 | ○ |  | 既読時のIPアドレス |
| device_type | デバイス種別 | ENUM |  | ○ |  | 既読時のデバイス種別（PC:PC、MOBILE:モバイル、TABLET:タブレット） |
| is_bulk_notification | 一括通知フラグ | BOOLEAN |  | ○ | False | 一括送信された通知かどうか |
| personalization_data | パーソナライゼーションデータ | TEXT |  | ○ |  | 個人向けカスタマイズデータ（JSON形式） |
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_id | notification_id | ○ | 通知ID検索用（一意） |
| idx_recipient_id | recipient_id | × | 受信者ID検索用 |
| idx_sender_id | sender_id | × | 送信者ID検索用 |
| idx_notification_type | notification_type | × | 通知種別検索用 |
| idx_notification_category | notification_category | × | 通知カテゴリ検索用 |
| idx_priority_level | priority_level | × | 優先度検索用 |
| idx_delivery_method | delivery_method | × | 配信方法検索用 |
| idx_delivery_status | delivery_status | × | 配信状況検索用 |
| idx_read_status | read_status | × | 既読状況検索用 |
| idx_sent_at | sent_at | × | 送信日時検索用 |
| idx_recipient_unread | recipient_id, read_status, expiry_date | × | 受信者別未読通知検索用 |
| idx_batch_id | batch_id | × | バッチID検索用 |
| idx_related_entity | related_entity_type, related_entity_id | × | 関連エンティティ検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_notification_recipient | recipient_id | MST_Employee | id | CASCADE | RESTRICT | 受信者への外部キー |
| fk_notification_sender | sender_id | MST_Employee | id | CASCADE | SET NULL | 送信者への外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_notification_id | UNIQUE |  | 通知ID一意制約 |
| chk_notification_type | CHECK | notification_type IN ('SYSTEM', 'REMINDER', 'APPROVAL', 'ALERT', 'INFO', 'URGENT') | 通知種別値チェック制約 |
| chk_notification_category | CHECK | notification_category IN ('SKILL', 'TRAINING', 'PROJECT', 'CERTIFICATION', 'SYSTEM', 'HR') | 通知カテゴリ値チェック制約 |
| chk_priority_level | CHECK | priority_level IN ('LOW', 'NORMAL', 'HIGH', 'CRITICAL') | 優先度値チェック制約 |
| chk_message_format | CHECK | message_format IN ('PLAIN', 'HTML', 'MARKDOWN') | メッセージ形式値チェック制約 |
| chk_delivery_method | CHECK | delivery_method IN ('IN_APP', 'EMAIL', 'SLACK', 'TEAMS', 'LINE_WORKS', 'SMS') | 配信方法値チェック制約 |
| chk_delivery_status | CHECK | delivery_status IN ('PENDING', 'SENT', 'DELIVERED', 'FAILED', 'BOUNCED') | 配信状況値チェック制約 |
| chk_read_status | CHECK | read_status IN ('UNREAD', 'READ', 'ARCHIVED') | 既読状況値チェック制約 |
| chk_related_entity_type | CHECK | related_entity_type IN ('PROJECT', 'TRAINING', 'CERTIFICATION', 'SKILL', 'EMPLOYEE') | 関連エンティティ種別値チェック制約 |
| chk_device_type | CHECK | device_type IN ('PC', 'MOBILE', 'TABLET') | デバイス種別値チェック制約 |
| chk_retry_count | CHECK | retry_count >= 0 AND retry_count <= max_retry_count | 再送回数範囲チェック制約 |
| chk_max_retry_count | CHECK | max_retry_count >= 0 | 最大再送回数非負数チェック制約 |

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

## 業務ルール

- 通知IDは一意である必要がある
- 再送回数は最大再送回数以下である必要がある
- 既読日時は送信日時以降である必要がある
- アーカイブ日時は既読日時以降である必要がある
- 緊急通知は即座に配信される必要がある
- 有効期限切れの通知は自動的に非表示
- 配信失敗時は設定された回数まで自動再送
- 一括通知はバッチIDで管理

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知履歴テーブルの詳細定義 |
