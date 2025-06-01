# テーブル定義書: MST_SkillGradeRequirement (スキルグレード要件)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_SkillGradeRequirement |
| 論理名 | スキルグレード要件 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_SkillGradeRequirement_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキルグレード要件テーブルの詳細定義 |


## 📝 テーブル概要

MST_SkillGradeRequirement（スキルグレード要件）は、スキルグレードごとの詳細要件を管理するマスタテーブルです。

主な目的：
- スキルグレード別の詳細要件定義
- 昇格基準の明確化
- 評価項目の標準化
- 学習目標の設定
- 能力開発計画の基礎データ
- 人材評価の客観化

このテーブルにより、各スキルグレードに求められる具体的な要件を明確に定義し、
公正で透明性の高い人材評価・育成システムを構築できます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| skill_grade_id | スキルグレードID | VARCHAR | 50 | ○ |  | ● |  | スキルグレードのID（MST_SkillGradeへの外部キー） |
| requirement_category | 要件カテゴリ | ENUM |  | ○ |  |  |  | 要件カテゴリ（TECHNICAL:技術、BUSINESS:業務、LEADERSHIP:リーダーシップ、COMMUNICATION:コミュニケーション） |
| requirement_name | 要件名 | VARCHAR | 200 | ○ |  |  |  | 要件の名称 |
| requirement_description | 要件説明 | TEXT |  | ○ |  |  |  | 要件の詳細説明 |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  |  |  | 具体的な評価基準・判定方法 |
| proficiency_level | 習熟度レベル | INTEGER |  | ○ |  |  |  | 要求される習熟度レベル（1-5、5が最高） |
| weight_percentage | 重み比率 | DECIMAL | 5,2 | ○ |  |  |  | グレード内での重み比率（%） |
| minimum_score | 最低スコア | DECIMAL | 5,2 | ○ |  |  |  | 合格に必要な最低スコア |
| evidence_requirements | エビデンス要件 | TEXT |  | ○ |  |  |  | 評価に必要なエビデンス・証拠 |
| learning_resources | 学習リソース | TEXT |  | ○ |  |  |  | 推奨学習リソース・教材（JSON形式） |
| prerequisite_requirements | 前提要件 | TEXT |  | ○ |  |  |  | 前提となる要件のリスト（JSON形式） |
| assessment_method | 評価方法 | ENUM |  | ○ |  |  |  | 評価方法（EXAM:試験、PORTFOLIO:ポートフォリオ、INTERVIEW:面接、PROJECT:プロジェクト、PEER_REVIEW:同僚評価） |
| assessment_frequency | 評価頻度 | ENUM |  | ○ |  |  | ANNUAL | 評価頻度（ANNUAL:年次、SEMI_ANNUAL:半年、QUARTERLY:四半期、ON_DEMAND:随時） |
| validity_period | 有効期間 | INTEGER |  | ○ |  |  |  | 評価結果の有効期間（月数） |
| certification_mapping | 資格マッピング | TEXT |  | ○ |  |  |  | 関連する外部資格・認定のマッピング（JSON形式） |
| requirement_status | 要件状況 | ENUM |  | ○ |  |  | ACTIVE | 要件状況（ACTIVE:有効、DEPRECATED:非推奨、OBSOLETE:廃止） |
| effective_date | 有効開始日 | DATE |  | ○ |  |  |  | 要件の有効開始日 |
| expiry_date | 有効終了日 | DATE |  | ○ |  |  |  | 要件の有効終了日（NULL:無期限） |
| revision_notes | 改版備考 | TEXT |  | ○ |  |  |  | 要件変更時の備考・理由 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_SkillGradeRequirement_skill_grade_id | skill_grade_id | × | スキルグレードID検索用 |
| idx_MST_SkillGradeRequirement_category | requirement_category | × | 要件カテゴリ別検索用 |
| idx_MST_SkillGradeRequirement_grade_category | skill_grade_id, requirement_category | × | グレード・カテゴリ複合検索用 |
| idx_MST_SkillGradeRequirement_proficiency_level | proficiency_level | × | 習熟度レベル別検索用 |
| idx_MST_SkillGradeRequirement_assessment_method | assessment_method | × | 評価方法別検索用 |
| idx_MST_SkillGradeRequirement_status | requirement_status | × | 要件状況別検索用 |
| idx_MST_SkillGradeRequirement_effective_date | effective_date | × | 有効開始日検索用 |
| idx_MST_SkillGradeRequirement_weight | weight_percentage | × | 重み比率別検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_MST_SkillGradeRequirement_grade_name | UNIQUE | skill_grade_id, requirement_name |  | グレード・要件名一意制約 |
| chk_MST_SkillGradeRequirement_category | CHECK |  | requirement_category IN ('TECHNICAL', 'BUSINESS', 'LEADERSHIP', 'COMMUNICATION') | 要件カテゴリ値チェック制約 |
| chk_MST_SkillGradeRequirement_proficiency_level | CHECK |  | proficiency_level >= 1 AND proficiency_level <= 5 | 習熟度レベル範囲チェック制約 |
| chk_MST_SkillGradeRequirement_weight_percentage | CHECK |  | weight_percentage >= 0 AND weight_percentage <= 100 | 重み比率範囲チェック制約 |
| chk_MST_SkillGradeRequirement_minimum_score | CHECK |  | minimum_score IS NULL OR (minimum_score >= 0 AND minimum_score <= 100) | 最低スコア範囲チェック制約 |
| chk_MST_SkillGradeRequirement_assessment_method | CHECK |  | assessment_method IN ('EXAM', 'PORTFOLIO', 'INTERVIEW', 'PROJECT', 'PEER_REVIEW') | 評価方法値チェック制約 |
| chk_MST_SkillGradeRequirement_assessment_frequency | CHECK |  | assessment_frequency IN ('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY', 'ON_DEMAND') | 評価頻度値チェック制約 |
| chk_MST_SkillGradeRequirement_status | CHECK |  | requirement_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE') | 要件状況値チェック制約 |
| chk_MST_SkillGradeRequirement_validity_period | CHECK |  | validity_period IS NULL OR validity_period > 0 | 有効期間正値チェック制約 |
| chk_MST_SkillGradeRequirement_date_range | CHECK |  | expiry_date IS NULL OR effective_date <= expiry_date | 日付範囲整合性チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_MST_SkillGradeRequirement_skill_grade | skill_grade_id | MST_SkillGrade | id | CASCADE | CASCADE | スキルグレードへの外部キー |

## 📊 サンプルデータ

```json
[
  {
    "skill_grade_id": "GRADE001",
    "requirement_category": "TECHNICAL",
    "requirement_name": "プログラミング基礎",
    "requirement_description": "基本的なプログラミング言語の理解と簡単なプログラムの作成能力",
    "evaluation_criteria": "指定された仕様に基づく簡単なプログラムの作成、基本的なアルゴリズムの理解",
    "proficiency_level": 2,
    "weight_percentage": 30.0,
    "minimum_score": 70.0,
    "evidence_requirements": "作成したプログラムのソースコード、動作確認結果",
    "learning_resources": "[\"プログラミング入門書\", \"オンライン学習サイト\", \"基礎研修\"]",
    "prerequisite_requirements": "[\"コンピュータ基礎知識\"]",
    "assessment_method": "PROJECT",
    "assessment_frequency": "SEMI_ANNUAL",
    "validity_period": 24,
    "certification_mapping": "[\"基本情報技術者試験\"]",
    "requirement_status": "ACTIVE",
    "effective_date": "2025-01-01",
    "expiry_date": null,
    "revision_notes": "初版作成"
  },
  {
    "skill_grade_id": "GRADE001",
    "requirement_category": "BUSINESS",
    "requirement_name": "業務理解",
    "requirement_description": "担当業務の基本的な理解と顧客要件の把握能力",
    "evaluation_criteria": "業務フローの説明、顧客要件の整理と文書化",
    "proficiency_level": 2,
    "weight_percentage": 25.0,
    "minimum_score": 75.0,
    "evidence_requirements": "業務分析レポート、要件定義書",
    "learning_resources": "[\"業務知識研修\", \"業界動向資料\", \"先輩社員からのOJT\"]",
    "prerequisite_requirements": null,
    "assessment_method": "PORTFOLIO",
    "assessment_frequency": "ANNUAL",
    "validity_period": 12,
    "certification_mapping": null,
    "requirement_status": "ACTIVE",
    "effective_date": "2025-01-01",
    "expiry_date": null,
    "revision_notes": "初版作成"
  },
  {
    "skill_grade_id": "GRADE003",
    "requirement_category": "LEADERSHIP",
    "requirement_name": "チームマネジメント",
    "requirement_description": "チームの運営管理と成果創出のためのリーダーシップ能力",
    "evaluation_criteria": "チーム運営実績、メンバー育成成果、プロジェクト成功率",
    "proficiency_level": 4,
    "weight_percentage": 35.0,
    "minimum_score": 80.0,
    "evidence_requirements": "チーム運営レポート、メンバー評価、プロジェクト成果物",
    "learning_resources": "[\"リーダーシップ研修\", \"マネジメント書籍\", \"外部セミナー\"]",
    "prerequisite_requirements": "[\"チームリーダー経験\", \"プロジェクト管理経験\"]",
    "assessment_method": "PEER_REVIEW",
    "assessment_frequency": "ANNUAL",
    "validity_period": 36,
    "certification_mapping": "[\"PMP\", \"プロジェクトマネージャ試験\"]",
    "requirement_status": "ACTIVE",
    "effective_date": "2025-01-01",
    "expiry_date": null,
    "revision_notes": "初版作成"
  }
]
```

## 📌 特記事項

- スキルグレード内での要件名は一意
- 重み比率の合計はグレード内で100%となるよう運用で管理
- 習熟度レベルは1-5の5段階評価
- 学習リソース・前提要件・資格マッピングはJSON形式で管理
- 有効期限により時期に応じた要件変更に対応
- 論理削除は is_deleted フラグで管理
- 評価結果の有効期間により再評価タイミングを管理

## 📋 業務ルール

- TECHNICAL要件は技術的能力を評価
- BUSINESS要件は業務遂行能力を評価
- LEADERSHIP要件は指導・管理能力を評価
- COMMUNICATION要件はコミュニケーション能力を評価
- 習熟度レベル4以上は上級者レベル
- 習熟度レベル3は中級者レベル
- 習熟度レベル1-2は初級者レベル
- 最低スコア未満は不合格
- 前提要件を満たさない場合は評価対象外
- 有効期限切れの要件は自動的に無効化
- 評価結果は有効期間内で有効
