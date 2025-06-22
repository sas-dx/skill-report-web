# テーブル定義書: MST_NotificationSettings

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_NotificationSettings |
| 論理名 | 通知設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:17 |

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
| notificationsettings_id | MST_NotificationSettingsの主キー | SERIAL |  | × |  | MST_NotificationSettingsの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_notificationsettings_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_notification_settings_template | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_notificationsettings | PRIMARY KEY | notificationsettings_id | 主キー制約 |

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