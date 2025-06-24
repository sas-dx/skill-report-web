# テーブル定義書: MST_Certification

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Certification |
| 論理名 | 資格情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 22:56:14 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| certification_code | 資格コード | VARCHAR | 50 | ○ |  | 資格コード |
| certification_name | 資格名 | VARCHAR | 200 | ○ |  | 資格名 |
| certification_category | 資格カテゴリ | ENUM |  | ○ |  | 資格カテゴリ |
| certification_id | 資格ID | INTEGER |  | × |  | 資格ID |
| certification_level | 資格レベル | ENUM |  | ○ |  | 資格レベル |
| certification_name_en | 資格名 | VARCHAR | 200 | ○ |  | 資格名（英語） |
| description | 説明 | TEXT |  | ○ |  | 説明 |
| exam_fee | 受験料 | DECIMAL | 10,2 | ○ |  | 受験料 |
| exam_format | 試験形式 | ENUM |  | ○ |  | 試験形式 |
| exam_language | 試験言語 | VARCHAR | 50 | ○ |  | 試験言語 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| is_recommended | 推奨資格フラグ | BOOLEAN |  | ○ | False | 推奨資格フラグ |
| issuer | 発行機関 | VARCHAR | 100 | ○ |  | 発行機関 |
| issuer_country | 発行国 | VARCHAR | 10 | ○ |  | 発行国 |
| official_url | 公式URL | VARCHAR | 500 | ○ |  | 公式URL |
| renewal_required | 更新要否 | BOOLEAN |  | ○ | False | 更新要否 |
| renewal_requirements | 更新要件 | TEXT |  | ○ |  | 更新要件 |
| skill_category_id | スキルカテゴリID | VARCHAR | 50 | ○ |  | スキルカテゴリID |
| validity_period_months | 有効期間 | INTEGER |  | ○ |  | 有効期間（月） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_certification_code | certification_code | ○ |  |
| idx_certification_name | certification_name | × |  |
| idx_issuer | issuer | × |  |
| idx_category_level | certification_category, certification_level | × |  |
| idx_recommended | is_recommended, is_active | × |  |
| idx_skill_category | skill_category_id | × |  |
| idx_mst_certification_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_certification_skill_category | skill_category_id | MST_SkillCategory | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_certification | PRIMARY KEY | certification_id | 主キー制約 |
| uk_id | UNIQUE |  | id一意制約 |
| uk_certification_code | UNIQUE |  | certification_code一意制約 |

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

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 資格情報マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 3.2.20250624 | 2025-06-24 | 主キー修正ツール | certification_id カラム削除、id を正しい主キーに設定 |
| 4.0.20250624 | 2025-06-24 | カラム順序統一ツール | certification_id を主キーとして復活、指定されたカラム順序に統一 |
| 4.1.20250624 | 2025-06-24 | 制約修正ツール | デフォルト値の型修正、制約処理の有効化 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223431 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |