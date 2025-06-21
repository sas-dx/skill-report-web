# テーブル定義書: SYS_TenantUsage

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_TenantUsage |
| 論理名 | テナント利用状況 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-21 17:20:34 |

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
| usage_date |  | DATE |  | ○ |  |  |
| tenant_id |  | VARCHAR |  | ○ |  |  |
| active_users |  | INTEGER |  | ○ | 0 |  |
| total_logins |  | INTEGER |  | ○ | 0 |  |
| api_requests |  | BIGINT |  | ○ | 0 |  |
| data_storage_mb |  | DECIMAL |  | ○ | 0.0 |  |
| file_storage_mb |  | DECIMAL |  | ○ | 0.0 |  |
| backup_storage_mb |  | DECIMAL |  | ○ | 0.0 |  |
| cpu_usage_minutes |  | DECIMAL |  | ○ | 0.0 |  |
| memory_usage_mb_hours |  | DECIMAL |  | ○ | 0.0 |  |
| network_transfer_mb |  | DECIMAL |  | ○ | 0.0 |  |
| report_generations |  | INTEGER |  | ○ | 0 |  |
| skill_assessments |  | INTEGER |  | ○ | 0 |  |
| notification_sent |  | INTEGER |  | ○ | 0 |  |
| peak_concurrent_users |  | INTEGER |  | ○ | 0 |  |
| peak_time |  | TIME |  | ○ |  |  |
| error_count |  | INTEGER |  | ○ | 0 |  |
| response_time_avg_ms |  | DECIMAL |  | ○ |  |  |
| uptime_percentage |  | DECIMAL |  | ○ | 100.0 |  |
| billing_amount |  | DECIMAL |  | ○ |  |  |
| collection_timestamp |  | TIMESTAMP |  | ○ |  |  |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_TenantUsage_date_tenant | usage_date, tenant_id | ○ |  |
| idx_SYS_TenantUsage_tenant_id | tenant_id | × |  |
| idx_SYS_TenantUsage_usage_date | usage_date | × |  |
| idx_SYS_TenantUsage_collection_timestamp | collection_timestamp | × |  |
| idx_SYS_TenantUsage_billing_amount | billing_amount | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_sys_tenantusage | PRIMARY KEY | id | 主キー制約 |

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