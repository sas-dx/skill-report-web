# テーブル定義書: MST_Certification

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Certification |
| 論理名 | 資格情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:17 |

## 概要

MST_Certification（資格情報）は、各種資格・認定・免許の基本情報を管理するマスタテーブルです。
主な目的：
- IT資格、業務資格、国家資格等の統一管理
- 資格の有効期限・更新要件の管理
- 資格とスキルの関連付け
- 資格取得推奨・必須要件の管理
- 資格取得状況の追跡・分析基盤
このテーブルにより、社員の資格取得状況を体系的に管理し、
キャリア開発や人材配置の判断材料として活用できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| certification_id | MST_Certificationの主キー | SERIAL |  | × |  | MST_Certificationの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_certification_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_certification_skill_category | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_certification | PRIMARY KEY | certification_id | 主キー制約 |

## サンプルデータ

| certification_code | certification_name | certification_name_en | issuer | issuer_country | certification_category | certification_level | validity_period_months | renewal_required | renewal_requirements | exam_fee | exam_language | exam_format | official_url | description | skill_category_id | is_recommended | is_active |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| CERT_AWS_SAA | AWS Certified Solutions Architect - Associate | AWS Certified Solutions Architect - Associate | Amazon Web Services | US | IT | INTERMEDIATE | 36 | True | 再認定試験の受験または上位資格の取得 | 15000 | 日本語/英語 | ONLINE | https://aws.amazon.com/jp/certification/certified-solutions-architect-associate/ | AWSクラウドでのソリューション設計・実装スキルを証明する資格 | SKILL_CAT_CLOUD | True | True |
| CERT_PMP | Project Management Professional | Project Management Professional | Project Management Institute | US | BUSINESS | ADVANCED | 36 | True | 60 PDU（Professional Development Units）の取得 | 55500 | 日本語/英語 | BOTH | https://www.pmi.org/certifications/project-management-pmp | プロジェクトマネジメントの国際的な資格 | SKILL_CAT_PM | True | True |

## 特記事項

- 資格コードは「CERT_」プレフィックス + 発行機関略称 + 資格略称で構成
- 有効期間がNULLの場合は無期限有効
- 更新要件は資格ごとに異なるため、テキスト形式で柔軟に記録
- 受験料は円建てで統一（外貨の場合は取得時レートで換算）
- 推奨資格は人事評価・昇進要件との連携で使用
- 論理削除は is_active フラグで管理

## 業務ルール

- 資格コードは一意である必要がある
- 推奨資格は定期的に見直しを行う
- 有効期限のある資格は更新要件を必須記載
- 受験料は税込み価格で記録
- 公式URLは資格詳細情報の参照先として使用
- スキルカテゴリとの関連付けにより、関連スキル推薦機能で活用
- 資格レベルは社内スキルグレードとの対応付けに使用

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 資格情報マスタテーブルの詳細定義 |