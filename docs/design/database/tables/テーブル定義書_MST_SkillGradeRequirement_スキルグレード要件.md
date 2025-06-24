# テーブル定義書: MST_SkillGradeRequirement

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillGradeRequirement |
| 論理名 | スキルグレード要件 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| assessment_frequency | 評価頻度 | ENUM |  | ○ | ANNUAL | 評価頻度 |
| assessment_method | 評価方法 | ENUM |  | ○ |  | 評価方法 |
| certification_mapping | 資格マッピング | TEXT |  | ○ |  | 資格マッピング |
| effective_date | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  | 評価基準 |
| evidence_requirements | エビデンス要件 | TEXT |  | ○ |  | エビデンス要件 |
| expiry_date | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| learning_resources | 学習リソース | TEXT |  | ○ |  | 学習リソース |
| minimum_score | 最低スコア | DECIMAL | 5,2 | ○ |  | 最低スコア |
| prerequisite_requirements | 前提要件 | TEXT |  | ○ |  | 前提要件 |
| proficiency_level | 習熟度レベル | INTEGER |  | ○ |  | 習熟度レベル |
| requirement_category | 要件カテゴリ | ENUM |  | ○ |  | 要件カテゴリ |
| requirement_description | 要件説明 | TEXT |  | ○ |  | 要件説明 |
| requirement_name | 要件名 | VARCHAR | 200 | ○ |  | 要件名 |
| requirement_status | 要件状況 | ENUM |  | ○ | ACTIVE | 要件状況 |
| revision_notes | 改版備考 | TEXT |  | ○ |  | 改版備考 |
| skill_grade_id | スキルグレードID | VARCHAR | 50 | ○ |  | スキルグレードID |
| skillgraderequirement_id | MST_SkillGradeRequirementの主キー | SERIAL |  | × |  | MST_SkillGradeRequirementの主キー |
| validity_period | 有効期間 | INTEGER |  | ○ |  | 有効期間 |
| weight_percentage | 重み比率 | DECIMAL | 5,2 | ○ |  | 重み比率 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

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
| idx_mst_skillgraderequirement_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_SkillGradeRequirement_skill_grade | skill_grade_id | MST_SkillGrade | id | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
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

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキルグレード要件テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |