# テーブル定義書: SYS_TenantUsage

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_TenantUsage |
| 論理名 | テナント使用量 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-01 20:40:26 |

## 概要

テナント利用状況テーブルは、マルチテナント環境における各テナントのシステム利用状況を管理するシステムテーブルです。

主な目的：
- テナント別のリソース使用量監視
- 課金情報の基礎データ収集
- システム負荷分析とキャパシティプランニング
- SLA監視とパフォーマンス分析

このテーブルは、マルチテナントシステムの運用管理と課金処理を支える重要なテーブルで、
テナント毎の公平なリソース配分と適切な課金を実現します。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| usage_date | 利用日 | DATE |  | ○ |  | 利用状況を記録した日付 |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | 利用状況を記録するテナントのID |
| active_users | アクティブユーザー数 | INTEGER |  | ○ | 0 | 当日にログインしたユーザー数 |
| total_logins | 総ログイン回数 | INTEGER |  | ○ | 0 | 当日の総ログイン回数 |
| api_requests | API リクエスト数 | BIGINT |  | ○ | 0 | 当日のAPIリクエスト総数 |
| data_storage_mb | データ使用量MB | DECIMAL | 15,2 | ○ | 0.0 | 当日時点でのデータストレージ使用量（MB） |
| file_storage_mb | ファイル使用量MB | DECIMAL | 15,2 | ○ | 0.0 | 当日時点でのファイルストレージ使用量（MB） |
| backup_storage_mb | バックアップ使用量MB | DECIMAL | 15,2 | ○ | 0.0 | 当日時点でのバックアップストレージ使用量（MB） |
| cpu_usage_minutes | CPU使用時間分 | DECIMAL | 10,2 | ○ | 0.0 | 当日のCPU使用時間（分） |
| memory_usage_mb_hours | メモリ使用量MB時 | DECIMAL | 15,2 | ○ | 0.0 | 当日のメモリ使用量（MB×時間） |
| network_transfer_mb | ネットワーク転送量MB | DECIMAL | 15,2 | ○ | 0.0 | 当日のネットワーク転送量（MB） |
| report_generations | レポート生成回数 | INTEGER |  | ○ | 0 | 当日のレポート生成回数 |
| skill_assessments | スキル評価回数 | INTEGER |  | ○ | 0 | 当日のスキル評価実行回数 |
| notification_sent | 通知送信回数 | INTEGER |  | ○ | 0 | 当日の通知送信回数 |
| peak_concurrent_users | 最大同時接続ユーザー数 | INTEGER |  | ○ | 0 | 当日の最大同時接続ユーザー数 |
| peak_time | ピーク時刻 | TIME |  | ○ |  | 最大同時接続を記録した時刻 |
| error_count | エラー発生回数 | INTEGER |  | ○ | 0 | 当日のシステムエラー発生回数 |
| response_time_avg_ms | 平均応答時間ms | DECIMAL | 8,2 | ○ |  | 当日のAPI平均応答時間（ミリ秒） |
| uptime_percentage | 稼働率 | DECIMAL | 5,2 | ○ | 100.0 | 当日のシステム稼働率（%） |
| billing_amount | 課金額 | DECIMAL | 10,2 | ○ |  | 当日の利用に基づく課金額 |
| collection_timestamp | 収集日時 | TIMESTAMP |  | ○ |  | 利用状況データを収集した日時 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_TenantUsage_date_tenant | usage_date, tenant_id | ○ | 利用日とテナントIDの複合検索用（一意） |
| idx_SYS_TenantUsage_tenant_id | tenant_id | × | テナントID検索用 |
| idx_SYS_TenantUsage_usage_date | usage_date | × | 利用日検索用 |
| idx_SYS_TenantUsage_collection_timestamp | collection_timestamp | × | 収集日時検索用 |
| idx_SYS_TenantUsage_billing_amount | billing_amount | × | 課金額検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_SYS_TenantUsage_tenant | tenant_id | MST_Tenant | id | CASCADE | CASCADE | MST_Tenantへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_SYS_TenantUsage_date_tenant | UNIQUE |  | 利用日とテナントIDの組み合わせ一意制約 |
| chk_SYS_TenantUsage_active_users | CHECK | active_users >= 0 | アクティブユーザー数非負数チェック制約 |
| chk_SYS_TenantUsage_total_logins | CHECK | total_logins >= 0 | 総ログイン回数非負数チェック制約 |
| chk_SYS_TenantUsage_api_requests | CHECK | api_requests >= 0 | APIリクエスト数非負数チェック制約 |
| chk_SYS_TenantUsage_storage_usage | CHECK | data_storage_mb >= 0 AND file_storage_mb >= 0 AND backup_storage_mb >= 0 | ストレージ使用量非負数チェック制約 |
| chk_SYS_TenantUsage_resource_usage | CHECK | cpu_usage_minutes >= 0 AND memory_usage_mb_hours >= 0 AND network_transfer_mb >= 0 | リソース使用量非負数チェック制約 |
| chk_SYS_TenantUsage_counts | CHECK | report_generations >= 0 AND skill_assessments >= 0 AND notification_sent >= 0 | 各種実行回数非負数チェック制約 |
| chk_SYS_TenantUsage_peak_concurrent_users | CHECK | peak_concurrent_users >= 0 | 最大同時接続ユーザー数非負数チェック制約 |
| chk_SYS_TenantUsage_error_count | CHECK | error_count >= 0 | エラー発生回数非負数チェック制約 |
| chk_SYS_TenantUsage_response_time | CHECK | response_time_avg_ms IS NULL OR response_time_avg_ms >= 0 | 平均応答時間非負数チェック制約 |
| chk_SYS_TenantUsage_uptime_percentage | CHECK | uptime_percentage >= 0 AND uptime_percentage <= 100 | 稼働率範囲チェック制約（0-100%） |
| chk_SYS_TenantUsage_billing_amount | CHECK | billing_amount IS NULL OR billing_amount >= 0 | 課金額非負数チェック制約 |

## サンプルデータ

| usage_date | tenant_id | active_users | total_logins | api_requests | data_storage_mb | file_storage_mb | backup_storage_mb | cpu_usage_minutes | memory_usage_mb_hours | network_transfer_mb | report_generations | skill_assessments | notification_sent | peak_concurrent_users | peak_time | error_count | response_time_avg_ms | uptime_percentage | billing_amount | collection_timestamp |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| 2024-01-15 | TENANT001 | 25 | 47 | 15420 | 1024.5 | 512.25 | 256.75 | 180.5 | 2048.0 | 128.3 | 12 | 35 | 8 | 18 | 14:30:00 | 2 | 245.5 | 99.95 | 1250.0 | 2024-01-16 02:00:00 |
| 2024-01-15 | TENANT002 | 8 | 12 | 3240 | 256.25 | 128.5 | 64.25 | 45.25 | 512.0 | 32.1 | 3 | 8 | 2 | 6 | 10:15:00 | 0 | 198.25 | 100.0 | 320.0 | 2024-01-16 02:00:00 |

## 特記事項

- 利用日とテナントIDの組み合わせは一意である必要がある
- 利用状況データは日次で収集・集計される
- 課金額は利用量に基づいて自動計算される
- ストレージ使用量は日次スナップショットで記録
- CPU・メモリ使用量は累積値で記録
- 稼働率は0-100%の範囲で管理
- 論理削除は is_deleted フラグで管理

## 業務ルール

- 利用状況データは毎日深夜2:00に自動収集する
- 同一テナント・同一日付のレコードは1つのみ
- 課金額は利用量とプラン料金に基づいて自動計算する
- ストレージ使用量は日次で最新値を記録する
- CPU・メモリ使用量は24時間の累積値を記録する
- エラー発生時は詳細ログを別途記録する
- 稼働率が95%を下回った場合はアラート通知を送信する
- データ保持期間は2年間とし、それ以降は月次集計データのみ保持する

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_TenantUsageの詳細定義 |
