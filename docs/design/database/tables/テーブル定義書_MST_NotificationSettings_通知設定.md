# テーブル定義書: MST_NotificationSettings

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_NotificationSettings |
| 論理名 | 通知設定 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:17 |

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
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| channel_config | チャネル設定 | TEXT |  | ○ |  | チャネル設定 |
| frequency_type | 頻度タイプ | ENUM |  | ○ | IMMEDIATE | 頻度タイプ |
| frequency_value | 頻度値 | INTEGER |  | ○ |  | 頻度値 |
| is_enabled | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| notification_type | 通知タイプ | ENUM |  | ○ |  | 通知タイプ |
| notificationsettings_id | MST_NotificationSettingsの主キー | SERIAL |  | × |  | MST_NotificationSettingsの主キー |
| priority_level | 優先度レベル | ENUM |  | ○ | MEDIUM | 優先度レベル |
| setting_key | 設定キー | VARCHAR | 100 | ○ |  | 設定キー |
| setting_name | 設定名 | VARCHAR | 200 | ○ |  | 設定名 |
| target_audience | 対象者 | ENUM |  | ○ |  | 対象者 |
| template_id | テンプレートID | VARCHAR | 50 | ○ |  | テンプレートID |
| trigger_event | トリガーイベント | VARCHAR | 100 | ○ |  | トリガーイベント |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_notification_settings_tenant_key | tenant_id, setting_key | ○ |  |
| idx_notification_settings_type | notification_type | × |  |
| idx_notification_settings_event | trigger_event | × |  |
| idx_notification_settings_enabled | is_enabled | × |  |
| idx_notification_settings_template | template_id | × |  |
| idx_mst_notificationsettings_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_notification_settings_template | template_id | MST_NotificationTemplate | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_frequency_type | CHECK | frequency_type IN (...) | frequency_type値チェック制約 |
| chk_notification_type | CHECK | notification_type IN (...) | notification_type値チェック制約 |

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
- 同一テナント内で設定キーは重複不可
- 無効化された設定は通知処理から除外される
- テンプレートIDが指定されていない場合はデフォルトテンプレートを使用
- CUSTOM対象者の場合は別途対象者マスタで詳細設定が必要
- 頻度タイプがIMMEDIATEの場合、frequency_valueは不要
- 通知チャネル設定はJSON形式で各チャネルの仕様に準拠

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 通知設定マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |