# テーブル定義書: HIS_TenantBilling

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_TenantBilling |
| 論理名 | テナント課金履歴 |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-24 22:56:15 |

## 概要

HIS_TenantBilling（テナント課金履歴）は、マルチテナントシステムにおける各テナントの課金情報を履歴として管理するテーブルです。
主な目的：
- テナント別課金履歴の管理
- 使用量ベース課金の計算履歴
- 請求書発行のための基礎データ管理
- 課金監査のための証跡管理
- 収益分析のためのデータ蓄積
このテーブルは、マルチテナント管理機能において課金・請求業務を支える重要な履歴データです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| plan_name | プラン名 | VARCHAR | 200 | ○ |  | プラン名 |
| additional_amount | 追加料金 | DECIMAL | 12,2 | ○ | 0.0 | 追加料金 |
| base_amount | 基本料金 | DECIMAL | 12,2 | ○ | 0.0 | 基本料金 |
| billing_period_end | 課金期間終了日 | DATE |  | ○ |  | 課金期間終了日 |
| billing_period_start | 課金期間開始日 | DATE |  | ○ |  | 課金期間開始日 |
| billing_status | 課金状態 | ENUM |  | ○ | CALCULATED | 課金状態 |
| billing_type | 課金タイプ | ENUM |  | ○ |  | 課金タイプ |
| currency_code | 通貨コード | VARCHAR | 3 | ○ | JPY | 通貨コード |
| discount_amount | 割引金額 | DECIMAL | 12,2 | ○ | 0.0 | 割引金額 |
| due_date | 支払期限 | DATE |  | ○ |  | 支払期限 |
| invoice_date | 請求日 | DATE |  | ○ |  | 請求日 |
| invoice_number | 請求書番号 | VARCHAR | 50 | ○ |  | 請求書番号 |
| notes | 備考 | TEXT |  | ○ |  | 備考 |
| paid_date | 支払日 | DATE |  | ○ |  | 支払日 |
| payment_method | 支払方法 | ENUM |  | ○ |  | 支払方法 |
| plan_id | プランID | VARCHAR | 50 | ○ |  | プランID |
| subtotal_amount | 小計金額 | DECIMAL | 12,2 | ○ |  | 小計金額 |
| tax_amount | 税額 | DECIMAL | 12,2 | ○ |  | 税額 |
| tax_rate | 税率 | DECIMAL | 5,3 | ○ |  | 税率 |
| tenantbilling_id | HIS_TenantBillingの主キー | SERIAL |  | × |  | HIS_TenantBillingの主キー |
| total_amount | 合計金額 | DECIMAL | 12,2 | ○ |  | 合計金額 |
| usage_amount | 従量料金 | DECIMAL | 12,2 | ○ | 0.0 | 従量料金 |
| usage_details | 使用量詳細 | TEXT |  | ○ |  | 使用量詳細 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_tenant_billing_tenant_period | tenant_id, billing_period_start, billing_period_end | × |  |
| idx_tenant_billing_status | billing_status | × |  |
| idx_tenant_billing_invoice | invoice_number | ○ |  |
| idx_tenant_billing_dates | invoice_date, due_date, paid_date | × |  |
| idx_tenant_billing_type | billing_type | × |  |
| idx_tenant_billing_amount | total_amount | × |  |
| idx_his_tenantbilling_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_tenant_billing_tenant | tenant_id | MST_Tenant | id | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_billing_status | CHECK | billing_status IN (...) | billing_status値チェック制約 |
| chk_billing_type | CHECK | billing_type IN (...) | billing_type値チェック制約 |

## サンプルデータ

| id | tenant_id | billing_period_start | billing_period_end | billing_type | plan_id | plan_name | base_amount | usage_amount | additional_amount | discount_amount | subtotal_amount | tax_rate | tax_amount | total_amount | currency_code | usage_details | billing_status | invoice_number | invoice_date | due_date | paid_date | payment_method | notes |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| TB001 | TENANT001 | 2025-05-01 | 2025-05-31 | MONTHLY | PLAN_STANDARD | スタンダードプラン | 50000.0 | 15000.0 | 5000.0 | 3000.0 | 67000.0 | 0.1 | 6700.0 | 73700.0 | JPY | {"users": 25, "storage_gb": 150, "api_calls": 50000} | PAID | INV-2025-05-001 | 2025-06-01 | 2025-06-30 | 2025-06-15 | CREDIT_CARD | 5月分月額利用料金 |
| TB002 | TENANT002 | 2025-05-01 | 2025-05-31 | USAGE | PLAN_ENTERPRISE | エンタープライズプラン | 100000.0 | 45000.0 | 0.0 | 10000.0 | 135000.0 | 0.1 | 13500.0 | 148500.0 | JPY | {"users": 100, "storage_gb": 500, "api_calls": 200000, "premium_features": true} | INVOICED | INV-2025-05-002 | 2025-06-01 | 2025-06-30 | None | BANK_TRANSFER | 5月分従量課金（大容量利用） |

## 特記事項

- 課金履歴は法的要件により7年間保持される
- 金額は全て税抜・税込を明確に分離して管理
- 使用量詳細はJSON形式で柔軟な情報を格納
- 請求書番号は全システムで一意である必要がある
- 支払状況は外部決済システムとの連携により更新
- 通貨コードはISO 4217準拠で国際化に対応
- 個人情報含有のため暗号化必須（テーブル一覧参照）
- 課金期間は重複しない連続した期間である必要がある
- 請求書番号は発行後変更不可
- 支払済み状態の課金情報は変更不可
- キャンセルされた課金は金額を0に調整
- 税率は課金期間の法定税率を適用
- 使用量ベース課金は実際の使用量データに基づく
- 割引は契約条件に基づき自動適用
- 支払期限は請求日から30日後が標準

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - テナント課金履歴テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223431 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |