# テーブル定義書: MST_JobTypeSkillGrade

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_JobTypeSkillGrade |
| 論理名 | 職種スキルグレード関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

MST_JobTypeSkillGrade（職種スキルグレード関連）は、職種とスキルグレードの関連付けを管理するマスタテーブルです。

主な目的：
- 職種ごとの必要スキルグレードの定義
- 昇進・昇格要件の明確化
- キャリアパス設計の基礎データ
- 人材評価基準の標準化
- 給与体系との連動管理
- 教育計画の目標設定

このテーブルにより、各職種に求められるスキルグレードを明確に定義し、
人材育成や昇進管理の判断基準として活用できます。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 職種のID（MST_JobTypeへの外部キー） |
| skill_grade_id | スキルグレードID | VARCHAR | 50 | ○ |  | スキルグレードのID（MST_SkillGradeへの外部キー） |
| grade_requirement_type | グレード要件区分 | ENUM |  | ○ | STANDARD | グレード要件区分（MINIMUM:最低要件、STANDARD:標準要件、ADVANCED:上級要件） |
| required_experience_years | 必要経験年数 | DECIMAL | 4,1 | ○ |  | 当該グレード到達に必要な経験年数 |
| promotion_criteria | 昇進基準 | TEXT |  | ○ |  | 当該グレードへの昇進基準・評価項目 |
| salary_range_min | 給与範囲下限 | DECIMAL | 10,0 | ○ |  | 当該グレードの給与範囲下限 |
| salary_range_max | 給与範囲上限 | DECIMAL | 10,0 | ○ |  | 当該グレードの給与範囲上限 |
| performance_expectations | 成果期待値 | TEXT |  | ○ |  | 当該グレードでの期待される成果・パフォーマンス |
| leadership_requirements | リーダーシップ要件 | TEXT |  | ○ |  | 当該グレードで求められるリーダーシップ能力 |
| technical_depth | 技術深度 | INTEGER |  | ○ |  | 技術的深度レベル（1-10、10が最高） |
| business_impact | 事業影響度 | INTEGER |  | ○ |  | 事業への影響度レベル（1-10、10が最高） |
| team_size_expectation | 期待チームサイズ | INTEGER |  | ○ |  | 管理が期待されるチームサイズ |
| certification_requirements | 資格要件 | TEXT |  | ○ |  | 必要な資格・認定のリスト（JSON形式） |
| grade_status | グレード状況 | ENUM |  | ○ | ACTIVE | グレード状況（ACTIVE:有効、DEPRECATED:非推奨、OBSOLETE:廃止） |
| effective_date | 有効開始日 | DATE |  | ○ |  | グレード要件の有効開始日 |
| expiry_date | 有効終了日 | DATE |  | ○ |  | グレード要件の有効終了日（NULL:無期限） |
| next_grade_path | 次グレードパス | TEXT |  | ○ |  | 次のグレードへの昇進パス（JSON形式） |
| evaluation_frequency | 評価頻度 | ENUM |  | ○ | ANNUAL | 評価頻度（ANNUAL:年次、SEMI_ANNUAL:半年、QUARTERLY:四半期） |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |
| description | 説明 | TEXT |  | ○ |  | マスタ説明 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_JobTypeSkillGrade_job_type_id | job_type_id | × | 職種ID検索用 |
| idx_MST_JobTypeSkillGrade_skill_grade_id | skill_grade_id | × | スキルグレードID検索用 |
| idx_MST_JobTypeSkillGrade_job_grade | job_type_id, skill_grade_id | ○ | 職種・スキルグレード複合検索用（一意） |
| idx_MST_JobTypeSkillGrade_requirement_type | grade_requirement_type | × | グレード要件区分別検索用 |
| idx_MST_JobTypeSkillGrade_experience_years | required_experience_years | × | 必要経験年数別検索用 |
| idx_MST_JobTypeSkillGrade_status | grade_status | × | グレード状況別検索用 |
| idx_MST_JobTypeSkillGrade_effective_date | effective_date | × | 有効開始日検索用 |
| idx_MST_JobTypeSkillGrade_technical_depth | technical_depth | × | 技術深度別検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_JobTypeSkillGrade_job_type | job_type_id | MST_JobType | id | CASCADE | CASCADE | 職種への外部キー |
| fk_MST_JobTypeSkillGrade_skill_grade | skill_grade_id | MST_SkillGrade | id | CASCADE | CASCADE | スキルグレードへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_MST_JobTypeSkillGrade_job_grade | UNIQUE |  | 職種・スキルグレード一意制約 |
| chk_MST_JobTypeSkillGrade_requirement_type | CHECK | grade_requirement_type IN ('MINIMUM', 'STANDARD', 'ADVANCED') | グレード要件区分値チェック制約 |
| chk_MST_JobTypeSkillGrade_status | CHECK | grade_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE') | グレード状況値チェック制約 |
| chk_MST_JobTypeSkillGrade_evaluation_frequency | CHECK | evaluation_frequency IN ('ANNUAL', 'SEMI_ANNUAL', 'QUARTERLY') | 評価頻度値チェック制約 |
| chk_MST_JobTypeSkillGrade_experience_years | CHECK | required_experience_years IS NULL OR required_experience_years >= 0 | 必要経験年数非負値チェック制約 |
| chk_MST_JobTypeSkillGrade_technical_depth | CHECK | technical_depth IS NULL OR (technical_depth >= 1 AND technical_depth <= 10) | 技術深度範囲チェック制約 |
| chk_MST_JobTypeSkillGrade_business_impact | CHECK | business_impact IS NULL OR (business_impact >= 1 AND business_impact <= 10) | 事業影響度範囲チェック制約 |
| chk_MST_JobTypeSkillGrade_team_size | CHECK | team_size_expectation IS NULL OR team_size_expectation >= 0 | 期待チームサイズ非負値チェック制約 |
| chk_MST_JobTypeSkillGrade_salary_range | CHECK | salary_range_min IS NULL OR salary_range_max IS NULL OR salary_range_min <= salary_range_max | 給与範囲整合性チェック制約 |
| chk_MST_JobTypeSkillGrade_date_range | CHECK | expiry_date IS NULL OR effective_date <= expiry_date | 日付範囲整合性チェック制約 |

## サンプルデータ

| job_type_id | skill_grade_id | grade_requirement_type | required_experience_years | promotion_criteria | salary_range_min | salary_range_max | performance_expectations | leadership_requirements | technical_depth | business_impact | team_size_expectation | certification_requirements | grade_status | effective_date | expiry_date | next_grade_path | evaluation_frequency |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| JOB001 | GRADE001 | MINIMUM | 0.0 | 基礎研修修了、OJT完了、基本業務遂行能力 | 3000000 | 4000000 | 指導の下での基本業務遂行、学習意欲の継続 | チームワーク、積極的な学習姿勢 | 2 | 2 | 0 | ["基本情報技術者試験"] | ACTIVE | 2025-01-01 | None | ["GRADE002"] | SEMI_ANNUAL |
| JOB001 | GRADE002 | STANDARD | 2.0 | 独立した業務遂行、技術スキル向上、プロジェクト貢献 | 4000000 | 5500000 | 独立した業務遂行、品質向上への貢献、後輩指導 | 後輩指導、技術的リーダーシップ | 4 | 4 | 2 | ["応用情報技術者試験", "専門資格1つ以上"] | ACTIVE | 2025-01-01 | None | ["GRADE003"] | ANNUAL |
| JOB002 | GRADE003 | ADVANCED | 5.0 | チーム運営実績、技術的専門性、事業貢献度 | 6000000 | 8000000 | チーム運営、技術戦略立案、事業成果創出 | チームマネジメント、技術戦略、人材育成 | 7 | 7 | 5 | ["高度情報技術者試験", "マネジメント資格", "専門資格2つ以上"] | ACTIVE | 2025-01-01 | None | ["GRADE004", "GRADE005"] | ANNUAL |

## 特記事項

- 職種とスキルグレードの組み合わせは一意
- 給与範囲は参考値として管理（実際の給与は別途決定）
- 技術深度・事業影響度は1-10の10段階評価
- 資格要件・次グレードパスはJSON形式で管理
- 有効期限により時期に応じたグレード要件変更に対応
- 論理削除は is_deleted フラグで管理
- 評価頻度により昇進評価のタイミングを管理

## 業務ルール

- MINIMUM要件は最低限の昇進条件
- STANDARD要件は一般的な昇進条件
- ADVANCED要件は優秀者向けの昇進条件
- 必要経験年数は最短期間を示す
- 技術深度7以上は技術エキスパートレベル
- 事業影響度7以上は事業リーダーレベル
- チームサイズ期待値は管理職適性の指標
- 資格要件は昇進の必要条件
- 次グレードパスは複数の昇進ルートを定義可能
- 有効期限切れのグレード要件は自動的に無効化

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 職種スキルグレード関連テーブルの詳細定義 |
