# テーブル定義書: TRN_Notification

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_Notification |
| 論理名 | 通知履歴 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-21 22:02:17 |

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
| notification_id | TRN_Notificationの主キー | SERIAL |  | × |  | TRN_Notificationの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_by | レコード作成者のユーザーID | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | レコード更新者のユーザーID | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_trn_notification_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_notification_recipient | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_notification_sender | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_trn_notification | PRIMARY KEY | notification_id, id | 主キー制約 |

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