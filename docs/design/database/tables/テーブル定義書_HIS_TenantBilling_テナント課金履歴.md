# テーブル定義書: HIS_TenantBilling (テナント課金履歴)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | HIS_TenantBilling |
| 論理名 | テナント課金履歴 |
| カテゴリ | 履歴系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/HIS_TenantBilling_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - テナント課金履歴テーブルの詳細定義 |


## 📝 テーブル概要

HIS_TenantBilling（テナント課金履歴）は、マルチテナントシステムにおける各テナントの課金情報を履歴として管理するテーブルです。

主な目的：
- テナント別課金履歴の管理
- 使用量ベース課金の計算履歴
- 請求書発行のための基礎データ管理
- 課金監査のための証跡管理
- 収益分析のためのデータ蓄積

このテーブルは、マルチテナント管理機能において課金・請求業務を支える重要な履歴データです。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | ● |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | ● |  | 課金対象のテナントID（MST_Tenantへの参照） |
| billing_period_start | 課金期間開始日 | DATE |  | ○ |  |  |  | 課金期間の開始日 |
| billing_period_end | 課金期間終了日 | DATE |  | ○ |  |  |  | 課金期間の終了日 |
| billing_type | 課金タイプ | ENUM |  | ○ |  |  |  | 課金の種類（MONTHLY:月額、USAGE:従量、SETUP:初期費用、ADDITIONAL:追加費用） |
| plan_id | プランID | VARCHAR | 50 | ○ |  |  |  | 適用されたプランのID |
| plan_name | プラン名 | VARCHAR | 200 | ○ |  |  |  | 適用されたプランの名称 |
| base_amount | 基本料金 | DECIMAL | 12,2 | ○ |  |  |  | 基本料金（税抜） |
| usage_amount | 従量料金 | DECIMAL | 12,2 | ○ |  |  |  | 使用量に基づく従量料金（税抜） |
| additional_amount | 追加料金 | DECIMAL | 12,2 | ○ |  |  |  | 追加サービス等の料金（税抜） |
| discount_amount | 割引金額 | DECIMAL | 12,2 | ○ |  |  |  | 適用された割引金額（税抜） |
| subtotal_amount | 小計金額 | DECIMAL | 12,2 | ○ |  |  |  | 税抜小計金額 |
| tax_rate | 税率 | DECIMAL | 5,3 | ○ |  |  |  | 適用された税率（例：0.100 = 10%） |
| tax_amount | 税額 | DECIMAL | 12,2 | ○ |  |  |  | 消費税額 |
| total_amount | 合計金額 | DECIMAL | 12,2 | ○ |  |  |  | 税込合計金額 |
| currency_code | 通貨コード | VARCHAR | 3 | ○ |  |  | JPY | 通貨コード（ISO 4217準拠、例：JPY、USD） |
| usage_details | 使用量詳細 | TEXT |  | ○ |  |  |  | 使用量の詳細情報（JSON形式） |
| billing_status | 課金状態 | ENUM |  | ○ |  |  | CALCULATED | 課金の状態（CALCULATED:計算済み、INVOICED:請求済み、PAID:支払済み、CANCELLED:キャンセル） |
| invoice_number | 請求書番号 | VARCHAR | 50 | ○ |  |  |  | 発行された請求書の番号 |
| invoice_date | 請求日 | DATE |  | ○ |  |  |  | 請求書の発行日 |
| due_date | 支払期限 | DATE |  | ○ |  |  |  | 支払期限日 |
| paid_date | 支払日 | DATE |  | ○ |  |  |  | 実際の支払日 |
| payment_method | 支払方法 | ENUM |  | ○ |  |  |  | 支払方法（CREDIT_CARD:クレジットカード、BANK_TRANSFER:銀行振込、AUTO_DEBIT:自動引落） |
| notes | 備考 | TEXT |  | ○ |  |  |  | 課金に関する備考・特記事項 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_tenant_billing_tenant_period | tenant_id, billing_period_start, billing_period_end | × | テナント別課金期間検索用 |
| idx_tenant_billing_status | billing_status | × | 課金状態別検索用 |
| idx_tenant_billing_invoice | invoice_number | ○ | 請求書番号検索用（一意） |
| idx_tenant_billing_dates | invoice_date, due_date, paid_date | × | 日付別検索用 |
| idx_tenant_billing_type | billing_type | × | 課金タイプ別検索用 |
| idx_tenant_billing_amount | total_amount | × | 金額別検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_tenant_billing_invoice | UNIQUE | invoice_number |  | 請求書番号一意制約 |
| chk_tenant_billing_type | CHECK |  | billing_type IN ('MONTHLY', 'USAGE', 'SETUP', 'ADDITIONAL') | 課金タイプ値チェック制約 |
| chk_tenant_billing_status | CHECK |  | billing_status IN ('CALCULATED', 'INVOICED', 'PAID', 'CANCELLED') | 課金状態値チェック制約 |
| chk_tenant_billing_payment_method | CHECK |  | payment_method IS NULL OR payment_method IN ('CREDIT_CARD', 'BANK_TRANSFER', 'AUTO_DEBIT') | 支払方法値チェック制約 |
| chk_tenant_billing_period | CHECK |  | billing_period_end >= billing_period_start | 課金期間整合性チェック制約 |
| chk_tenant_billing_amounts_positive | CHECK |  | base_amount >= 0 AND usage_amount >= 0 AND additional_amount >= 0 AND discount_amount >= 0 AND tax_amount >= 0 AND total_amount >= 0 | 金額正数チェック制約 |
| chk_tenant_billing_tax_rate | CHECK |  | tax_rate >= 0 AND tax_rate <= 1 | 税率範囲チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_tenant_billing_tenant | tenant_id | MST_Tenant | id | CASCADE | RESTRICT | テナント管理への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "id": "TB001",
    "tenant_id": "TENANT001",
    "billing_period_start": "2025-05-01",
    "billing_period_end": "2025-05-31",
    "billing_type": "MONTHLY",
    "plan_id": "PLAN_STANDARD",
    "plan_name": "スタンダードプラン",
    "base_amount": 50000.0,
    "usage_amount": 15000.0,
    "additional_amount": 5000.0,
    "discount_amount": 3000.0,
    "subtotal_amount": 67000.0,
    "tax_rate": 0.1,
    "tax_amount": 6700.0,
    "total_amount": 73700.0,
    "currency_code": "JPY",
    "usage_details": "{\"users\": 25, \"storage_gb\": 150, \"api_calls\": 50000}",
    "billing_status": "PAID",
    "invoice_number": "INV-2025-05-001",
    "invoice_date": "2025-06-01",
    "due_date": "2025-06-30",
    "paid_date": "2025-06-15",
    "payment_method": "CREDIT_CARD",
    "notes": "5月分月額利用料金"
  },
  {
    "id": "TB002",
    "tenant_id": "TENANT002",
    "billing_period_start": "2025-05-01",
    "billing_period_end": "2025-05-31",
    "billing_type": "USAGE",
    "plan_id": "PLAN_ENTERPRISE",
    "plan_name": "エンタープライズプラン",
    "base_amount": 100000.0,
    "usage_amount": 45000.0,
    "additional_amount": 0.0,
    "discount_amount": 10000.0,
    "subtotal_amount": 135000.0,
    "tax_rate": 0.1,
    "tax_amount": 13500.0,
    "total_amount": 148500.0,
    "currency_code": "JPY",
    "usage_details": "{\"users\": 100, \"storage_gb\": 500, \"api_calls\": 200000, \"premium_features\": true}",
    "billing_status": "INVOICED",
    "invoice_number": "INV-2025-05-002",
    "invoice_date": "2025-06-01",
    "due_date": "2025-06-30",
    "paid_date": null,
    "payment_method": "BANK_TRANSFER",
    "notes": "5月分従量課金（大容量利用）"
  }
]
```

## 📌 特記事項

- 課金履歴は法的要件により7年間保持される
- 金額は全て税抜・税込を明確に分離して管理
- 使用量詳細はJSON形式で柔軟な情報を格納
- 請求書番号は全システムで一意である必要がある
- 支払状況は外部決済システムとの連携により更新
- 通貨コードはISO 4217準拠で国際化に対応
- 個人情報含有のため暗号化必須（テーブル一覧参照）

## 📋 業務ルール

- 課金期間は重複しない連続した期間である必要がある
- 請求書番号は発行後変更不可
- 支払済み状態の課金情報は変更不可
- キャンセルされた課金は金額を0に調整
- 税率は課金期間の法定税率を適用
- 使用量ベース課金は実際の使用量データに基づく
- 割引は契約条件に基づき自動適用
- 支払期限は請求日から30日後が標準
