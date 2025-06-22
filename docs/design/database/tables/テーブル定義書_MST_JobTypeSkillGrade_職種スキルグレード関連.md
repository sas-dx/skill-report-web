# テーブル定義書: MST_JobTypeSkillGrade

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_JobTypeSkillGrade |
| 論理名 | 職種スキルグレード関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:17 |

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
| jobtypeskillgrade_id | MST_JobTypeSkillGradeの主キー | SERIAL |  | × |  | MST_JobTypeSkillGradeの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_jobtypeskillgrade_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_JobTypeSkillGrade_job_type | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_MST_JobTypeSkillGrade_skill_grade | None | None | None | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_jobtypeskillgrade | PRIMARY KEY | jobtypeskillgrade_id | 主キー制約 |
| chk_jobtypeskillgrade_id | CHECK | jobtypeskillgrade_id IN (...) | jobtypeskillgrade_id値チェック制約 |

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