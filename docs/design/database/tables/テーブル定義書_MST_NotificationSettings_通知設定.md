# テーブル定義書: MST_NotificationSettings

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_NotificationSettings |
| 論理名 | 通知設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:34 |

## 概要

MST_NotificationSettings（通知設定）は、システム全体の通知機能に関する設定情報を管理するマスタテーブルです。
主な目的：
- 通知チャネル（メール、Slack、Teams等）の設定管理
- 通知タイミング・頻度の制御設定
- 通知対象者・グループの設定管理
- 通知テンプレートとの紐付け設定
- テナント別通知設定の管理
このテーブルは、通知・連携管理機能の基盤となる重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id |  | VARCHAR |  | ○ |  |  |
| tenant_id |  | VARCHAR |  | ○ |  |  |
| setting_key |  | VARCHAR |  | ○ |  |  |
| setting_name |  | VARCHAR |  | ○ |  |  |
| notification_type |  | ENUM |  | ○ |  |  |
| target_audience |  | ENUM |  | ○ |  |  |
| trigger_event |  | VARCHAR |  | ○ |  |  |
| frequency_type |  | ENUM |  | ○ | IMMEDIATE |  |
| frequency_value |  | INTEGER |  | ○ |  |  |
| template_id |  | VARCHAR |  | ○ |  |  |
| channel_config |  | TEXT |  | ○ |  |  |
| is_enabled |  | BOOLEAN |  | ○ | True |  |
| priority_level |  | ENUM |  | ○ | MEDIUM |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_settings_tenant_key | tenant_id, setting_key | ○ |  |
| idx_notification_settings_type | notification_type | × |  |
| idx_notification_settings_event | trigger_event | × |  |
| idx_notification_settings_enabled | is_enabled | × |  |
| idx_notification_settings_template | template_id | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_notification_type | CHECK | notification_type IN (...) | notification_type値チェック制約 |
| chk_frequency_type | CHECK | frequency_type IN (...) | frequency_type値チェック制約 |

## サンプルデータ

| id | tenant_id | setting_key | setting_name | notification_type | target_audience | trigger_event | frequency_type | frequency_value | template_id | channel_config | is_enabled | priority_level |
|------|------|------|------|------|------|------|------|------|------|------|------|------|
| NS001 | TENANT001 | skill_update_notification | スキル更新通知 | EMAIL | MANAGER | skill_registered | IMMEDIATE | None | NT001 | {"smtp_server": "smtp.company.com", "from_address": "noreply@company.com"} | True | MEDIUM |
| NS002 | TENANT001 | goal_deadline_reminder | 目標期限リマインダー | SLACK | EMPLOYEE | goal_deadline_approaching | DAILY | 9 | NT002 | {"webhook_url": "https://hooks.slack.com/services/xxx", "channel": "#notifications"} | True | HIGH |

## 特記事項

- 通知設定はテナント別に管理され、同一テナント内で設定キーは一意
- channel_configはJSON形式で通知チャネル固有の設定を格納
- frequency_valueは頻度タイプに応じて異なる意味を持つ（時間、曜日等）
- 論理削除は is_enabled フラグで管理
- 通知テンプレートとの連携により柔軟な通知内容設定が可能
- 優先度レベルにより通知の重要度を制御

## 業務ルール

- 同一テナント内で設定キーは重複不可
- 無効化された設定は通知処理から除外される
- テンプレートIDが指定されていない場合はデフォルトテンプレートを使用
- CUSTOM対象者の場合は別途対象者マスタで詳細設定が必要
- 頻度タイプがIMMEDIATEの場合、frequency_valueは不要
- 通知チャネル設定はJSON形式で各チャネルの仕様に準拠

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知設定マスタテーブルの詳細定義 |