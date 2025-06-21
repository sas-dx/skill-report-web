# テーブル定義書: MST_SkillGradeRequirement

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillGradeRequirement |
| 論理名 | スキルグレード要件 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:34 |

## 概要

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


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| skill_grade_id |  | VARCHAR |  | ○ |  |  |
| requirement_category |  | ENUM |  | ○ |  |  |
| requirement_name |  | VARCHAR |  | ○ |  |  |
| requirement_description |  | TEXT |  | ○ |  |  |
| evaluation_criteria |  | TEXT |  | ○ |  |  |
| proficiency_level |  | INTEGER |  | ○ |  |  |
| weight_percentage |  | DECIMAL |  | ○ |  |  |
| minimum_score |  | DECIMAL |  | ○ |  |  |
| evidence_requirements |  | TEXT |  | ○ |  |  |
| learning_resources |  | TEXT |  | ○ |  |  |
| prerequisite_requirements |  | TEXT |  | ○ |  |  |
| assessment_method |  | ENUM |  | ○ |  |  |
| assessment_frequency |  | ENUM |  | ○ | ANNUAL |  |
| validity_period |  | INTEGER |  | ○ |  |  |
| certification_mapping |  | TEXT |  | ○ |  |  |
| requirement_status |  | ENUM |  | ○ | ACTIVE |  |
| effective_date |  | DATE |  | ○ |  |  |
| expiry_date |  | DATE |  | ○ |  |  |
| revision_notes |  | TEXT |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_SkillGradeRequirement_skill_grade_id | skill_grade_id | × |  |
| idx_MST_SkillGradeRequirement_category | requirement_category | × |  |
| idx_MST_SkillGradeRequirement_grade_category | skill_grade_id, requirement_category | × |  |
| idx_MST_SkillGradeRequirement_proficiency_level | proficiency_level | × |  |
| idx_MST_SkillGradeRequirement_assessment_method | assessment_method | × |  |
| idx_MST_SkillGradeRequirement_status | requirement_status | × |  |
| idx_MST_SkillGradeRequirement_effective_date | effective_date | × |  |
| idx_MST_SkillGradeRequirement_weight | weight_percentage | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_proficiency_level | CHECK | proficiency_level > 0 | proficiency_level正値チェック制約 |
| chk_requirement_status | CHECK | requirement_status IN (...) | requirement_status値チェック制約 |

## サンプルデータ

| skill_grade_id | requirement_category | requirement_name | requirement_description | evaluation_criteria | proficiency_level | weight_percentage | minimum_score | evidence_requirements | learning_resources | prerequisite_requirements | assessment_method | assessment_frequency | validity_period | certification_mapping | requirement_status | effective_date | expiry_date | revision_notes |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| GRADE001 | TECHNICAL | プログラミング基礎 | 基本的なプログラミング言語の理解と簡単なプログラムの作成能力 | 指定された仕様に基づく簡単なプログラムの作成、基本的なアルゴリズムの理解 | 2 | 30.0 | 70.0 | 作成したプログラムのソースコード、動作確認結果 | ["プログラミング入門書", "オンライン学習サイト", "基礎研修"] | ["コンピュータ基礎知識"] | PROJECT | SEMI_ANNUAL | 24 | ["基本情報技術者試験"] | ACTIVE | 2025-01-01 | None | 初版作成 |
| GRADE001 | BUSINESS | 業務理解 | 担当業務の基本的な理解と顧客要件の把握能力 | 業務フローの説明、顧客要件の整理と文書化 | 2 | 25.0 | 75.0 | 業務分析レポート、要件定義書 | ["業務知識研修", "業界動向資料", "先輩社員からのOJT"] | None | PORTFOLIO | ANNUAL | 12 | None | ACTIVE | 2025-01-01 | None | 初版作成 |
| GRADE003 | LEADERSHIP | チームマネジメント | チームの運営管理と成果創出のためのリーダーシップ能力 | チーム運営実績、メンバー育成成果、プロジェクト成功率 | 4 | 35.0 | 80.0 | チーム運営レポート、メンバー評価、プロジェクト成果物 | ["リーダーシップ研修", "マネジメント書籍", "外部セミナー"] | ["チームリーダー経験", "プロジェクト管理経験"] | PEER_REVIEW | ANNUAL | 36 | ["PMP", "プロジェクトマネージャ試験"] | ACTIVE | 2025-01-01 | None | 初版作成 |

## 特記事項

- スキルグレード内での要件名は一意
- 重み比率の合計はグレード内で100%となるよう運用で管理
- 習熟度レベルは1-5の5段階評価
- 学習リソース・前提要件・資格マッピングはJSON形式で管理
- 有効期限により時期に応じた要件変更に対応
- 論理削除は is_deleted フラグで管理
- 評価結果の有効期間により再評価タイミングを管理

## 業務ルール

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

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキルグレード要件テーブルの詳細定義 |