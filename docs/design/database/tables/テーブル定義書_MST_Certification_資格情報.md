# テーブル定義書: MST_Certification (資格情報)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_Certification |
| 論理名 | 資格情報 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_Certification_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 資格情報マスタテーブルの詳細定義 |


## 📝 テーブル概要

MST_Certification（資格情報）は、各種資格・認定・免許の基本情報を管理するマスタテーブルです。

主な目的：
- IT資格、業務資格、国家資格等の統一管理
- 資格の有効期限・更新要件の管理
- 資格とスキルの関連付け
- 資格取得推奨・必須要件の管理
- 資格取得状況の追跡・分析基盤

このテーブルにより、社員の資格取得状況を体系的に管理し、
キャリア開発や人材配置の判断材料として活用できます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| certification_code | 資格コード | VARCHAR | 50 | ○ |  |  |  | 資格を一意に識別するコード（例：CERT_AWS_SAA、CERT_PMP） |
| certification_name | 資格名 | VARCHAR | 200 | ○ |  |  |  | 正式な資格名称 |
| certification_name_en | 資格名（英語） | VARCHAR | 200 | ○ |  |  |  | 英語での資格名称 |
| issuer | 発行機関 | VARCHAR | 100 | ○ |  |  |  | 資格を発行する機関・団体名 |
| issuer_country | 発行国 | VARCHAR | 10 | ○ |  |  |  | 資格発行国（ISO 3166-1 alpha-2コード） |
| certification_category | 資格カテゴリ | ENUM |  | ○ |  |  |  | 資格の分類（IT:IT関連、BUSINESS:ビジネス、NATIONAL:国家資格、LANGUAGE:語学、OTHER:その他） |
| certification_level | 資格レベル | ENUM |  | ○ |  |  |  | 資格の難易度レベル（BASIC:基礎、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| validity_period_months | 有効期間（月） | INTEGER |  | ○ |  |  |  | 資格の有効期間（月数、NULLの場合は無期限） |
| renewal_required | 更新要否 | BOOLEAN |  | ○ |  |  |  | 定期的な更新が必要かどうか |
| renewal_requirements | 更新要件 | TEXT |  | ○ |  |  |  | 資格更新に必要な要件・条件 |
| exam_fee | 受験料 | DECIMAL | 10,2 | ○ |  |  |  | 受験料（円） |
| exam_language | 試験言語 | VARCHAR | 50 | ○ |  |  |  | 試験で使用される言語 |
| exam_format | 試験形式 | ENUM |  | ○ |  |  |  | 試験の実施形式（ONLINE:オンライン、OFFLINE:会場、BOTH:両方） |
| official_url | 公式URL | VARCHAR | 500 | ○ |  |  |  | 資格の公式サイトURL |
| description | 説明 | TEXT |  | ○ |  |  |  | 資格の詳細説明・概要 |
| skill_category_id | スキルカテゴリID | VARCHAR | 50 | ○ |  | ● |  | 関連するスキルカテゴリのID |
| is_recommended | 推奨資格フラグ | BOOLEAN |  | ○ |  |  |  | 会社として取得を推奨する資格かどうか |
| is_active | 有効フラグ | BOOLEAN |  | ○ |  |  | True | 資格が有効かどうか |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_certification_code | certification_code | ○ | 資格コード検索用（一意） |
| idx_certification_name | certification_name | × | 資格名検索用 |
| idx_issuer | issuer | × | 発行機関検索用 |
| idx_category_level | certification_category, certification_level | × | カテゴリ・レベル別検索用 |
| idx_recommended | is_recommended, is_active | × | 推奨資格検索用 |
| idx_skill_category | skill_category_id | × | スキルカテゴリ別検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_certification_code | UNIQUE | certification_code |  | 資格コード一意制約 |
| chk_certification_category | CHECK |  | certification_category IN ('IT', 'BUSINESS', 'NATIONAL', 'LANGUAGE', 'OTHER') | 資格カテゴリ値チェック制約 |
| chk_certification_level | CHECK |  | certification_level IN ('BASIC', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 資格レベル値チェック制約 |
| chk_exam_format | CHECK |  | exam_format IN ('ONLINE', 'OFFLINE', 'BOTH') | 試験形式値チェック制約 |
| chk_validity_period | CHECK |  | validity_period_months IS NULL OR validity_period_months > 0 | 有効期間正数チェック制約 |
| chk_exam_fee | CHECK |  | exam_fee IS NULL OR exam_fee >= 0 | 受験料非負数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_certification_skill_category | skill_category_id | MST_SkillCategory | id | CASCADE | SET NULL | スキルカテゴリへの外部キー |

## 📊 サンプルデータ

```json
[
  {
    "certification_code": "CERT_AWS_SAA",
    "certification_name": "AWS Certified Solutions Architect - Associate",
    "certification_name_en": "AWS Certified Solutions Architect - Associate",
    "issuer": "Amazon Web Services",
    "issuer_country": "US",
    "certification_category": "IT",
    "certification_level": "INTERMEDIATE",
    "validity_period_months": 36,
    "renewal_required": true,
    "renewal_requirements": "再認定試験の受験または上位資格の取得",
    "exam_fee": 15000,
    "exam_language": "日本語/英語",
    "exam_format": "ONLINE",
    "official_url": "https://aws.amazon.com/jp/certification/certified-solutions-architect-associate/",
    "description": "AWSクラウドでのソリューション設計・実装スキルを証明する資格",
    "skill_category_id": "SKILL_CAT_CLOUD",
    "is_recommended": true,
    "is_active": true
  },
  {
    "certification_code": "CERT_PMP",
    "certification_name": "Project Management Professional",
    "certification_name_en": "Project Management Professional",
    "issuer": "Project Management Institute",
    "issuer_country": "US",
    "certification_category": "BUSINESS",
    "certification_level": "ADVANCED",
    "validity_period_months": 36,
    "renewal_required": true,
    "renewal_requirements": "60 PDU（Professional Development Units）の取得",
    "exam_fee": 55500,
    "exam_language": "日本語/英語",
    "exam_format": "BOTH",
    "official_url": "https://www.pmi.org/certifications/project-management-pmp",
    "description": "プロジェクトマネジメントの国際的な資格",
    "skill_category_id": "SKILL_CAT_PM",
    "is_recommended": true,
    "is_active": true
  }
]
```

## 📌 特記事項

- 資格コードは「CERT_」プレフィックス + 発行機関略称 + 資格略称で構成
- 有効期間がNULLの場合は無期限有効
- 更新要件は資格ごとに異なるため、テキスト形式で柔軟に記録
- 受験料は円建てで統一（外貨の場合は取得時レートで換算）
- 推奨資格は人事評価・昇進要件との連携で使用
- 論理削除は is_active フラグで管理

## 📋 業務ルール

- 資格コードは一意である必要がある
- 推奨資格は定期的に見直しを行う
- 有効期限のある資格は更新要件を必須記載
- 受験料は税込み価格で記録
- 公式URLは資格詳細情報の参照先として使用
- スキルカテゴリとの関連付けにより、関連スキル推薦機能で活用
- 資格レベルは社内スキルグレードとの対応付けに使用
