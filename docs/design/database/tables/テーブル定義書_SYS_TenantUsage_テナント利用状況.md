# テーブル定義書: SYS_TenantUsage

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_TenantUsage |
| 論理名 | テナント利用状況 |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-24 22:56:15 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| active_users | アクティブユーザー数 | INTEGER |  | ○ | 0 | アクティブユーザー数 |
| api_requests | API リクエスト数 | BIGINT |  | ○ | 0 | API リクエスト数 |
| backup_storage_mb | バックアップ使用量MB | DECIMAL | 15,2 | ○ | 0.0 | バックアップ使用量MB |
| billing_amount | 課金額 | DECIMAL | 10,2 | ○ |  | 課金額 |
| collection_timestamp | 収集日時 | TIMESTAMP |  | ○ |  | 収集日時 |
| cpu_usage_minutes | CPU使用時間分 | DECIMAL | 10,2 | ○ | 0.0 | CPU使用時間分 |
| data_storage_mb | データ使用量MB | DECIMAL | 15,2 | ○ | 0.0 | データ使用量MB |
| error_count | エラー発生回数 | INTEGER |  | ○ | 0 | エラー発生回数 |
| file_storage_mb | ファイル使用量MB | DECIMAL | 15,2 | ○ | 0.0 | ファイル使用量MB |
| memory_usage_mb_hours | メモリ使用量MB時 | DECIMAL | 15,2 | ○ | 0.0 | メモリ使用量MB時 |
| network_transfer_mb | ネットワーク転送量MB | DECIMAL | 15,2 | ○ | 0.0 | ネットワーク転送量MB |
| notification_sent | 通知送信回数 | INTEGER |  | ○ | 0 | 通知送信回数 |
| peak_concurrent_users | 最大同時接続ユーザー数 | INTEGER |  | ○ | 0 | 最大同時接続ユーザー数 |
| peak_time | ピーク時刻 | TIME |  | ○ |  | ピーク時刻 |
| report_generations | レポート生成回数 | INTEGER |  | ○ | 0 | レポート生成回数 |
| response_time_avg_ms | 平均応答時間ms | DECIMAL | 8,2 | ○ |  | 平均応答時間ms |
| skill_assessments | スキル評価回数 | INTEGER |  | ○ | 0 | スキル評価回数 |
| tenantusage_id | SYS_TenantUsageの主キー | SERIAL |  | × |  | SYS_TenantUsageの主キー |
| total_logins | 総ログイン回数 | INTEGER |  | ○ | 0 | 総ログイン回数 |
| uptime_percentage | 稼働率 | DECIMAL | 5,2 | ○ | 100.0 | 稼働率 |
| usage_date | 利用日 | DATE |  | ○ |  | 利用日 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_SYS_TenantUsage_date_tenant | usage_date, tenant_id | ○ |  |
| idx_SYS_TenantUsage_tenant_id | tenant_id | × |  |
| idx_SYS_TenantUsage_usage_date | usage_date | × |  |
| idx_SYS_TenantUsage_collection_timestamp | collection_timestamp | × |  |
| idx_SYS_TenantUsage_billing_amount | billing_amount | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_SYS_TenantUsage_tenant | tenant_id | MST_Tenant | id | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |

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
- 利用状況データは毎日深夜2:00に自動収集する
- 同一テナント・同一日付のレコードは1つのみ
- 課金額は利用量とプラン料金に基づいて自動計算する
- ストレージ使用量は日次で最新値を記録する
- CPU・メモリ使用量は24時間の累積値を記録する
- エラー発生時は詳細ログを別途記録する
- 稼働率が95%を下回った場合はアラート通知を送信する
- データ保持期間は2年間とし、それ以降は月次集計データのみ保持する

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | システム | 初版作成 - SYS_TenantUsageの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |