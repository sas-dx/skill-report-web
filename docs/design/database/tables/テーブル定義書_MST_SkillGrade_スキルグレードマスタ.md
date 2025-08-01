# テーブル定義書: MST_SkillGrade

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillGrade |
| 論理名 | スキルグレードマスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:57 |

## 概要

MST_SkillGrade（スキルグレードマスタ）は、スキルの習熟度レベルを定義・管理するマスタテーブルです。
主な目的：
- スキル習熟度の標準化・統一
- スキル評価基準の明確化
- 職種別スキル要件の定義基盤
- スキル成長パスの可視化
- 人材育成計画の策定支援
このテーブルにより、組織全体で統一されたスキル評価基準を確立し、
社員のスキル開発と適切な人材配置を効率的に行うことができます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| grade_code | グレードコード | VARCHAR | 20 | ○ |  | グレードコード |
| grade_name | グレード名 | VARCHAR | 50 | ○ |  | グレード名 |
| certification_requirements | 資格要件 | TEXT |  | ○ |  | 資格要件 |
| color_code | 表示色コード | VARCHAR | 7 | ○ |  | 表示色コード |
| competency_requirements | 能力要件 | TEXT |  | ○ |  | 能力要件 |
| description | グレード説明 | TEXT |  | ○ |  | グレード説明 |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  | 評価基準 |
| grade_level | グレードレベル | INTEGER |  | ○ |  | グレードレベル |
| grade_name_short | グレード名 | VARCHAR | 10 | ○ |  | グレード名（短縮） |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| leadership_level | リーダーシップレベル | ENUM |  | ○ |  | リーダーシップレベル |
| mentoring_capability | 指導能力 | BOOLEAN |  | ○ | False | 指導能力 |
| project_complexity | プロジェクト複雑度 | ENUM |  | ○ |  | プロジェクト複雑度 |
| promotion_eligibility | 昇進資格 | BOOLEAN |  | ○ | False | 昇進資格 |
| required_experience_months | 必要経験期間 | INTEGER |  | ○ |  | 必要経験期間（月） |
| salary_impact_factor | 給与影響係数 | DECIMAL | 3,2 | ○ |  | 給与影響係数 |
| skill_indicators | スキル指標 | TEXT |  | ○ |  | スキル指標 |
| skillgrade_id | MST_SkillGradeの主キー | SERIAL |  | × |  | MST_SkillGradeの主キー |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | 表示順序 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_grade_code | grade_code | ○ |  |
| idx_grade_level | grade_level | ○ |  |
| idx_grade_name | grade_name | × |  |
| idx_mentoring | mentoring_capability, is_active | × |  |
| idx_promotion | promotion_eligibility, is_active | × |  |
| idx_sort_order | sort_order | × |  |
| idx_mst_skillgrade_tenant_id | tenant_id | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_grade_code | UNIQUE |  | grade_code一意制約 |
| uk_grade_level | UNIQUE |  | grade_level一意制約 |
| chk_grade_level | CHECK | grade_level > 0 | grade_level正値チェック制約 |

## サンプルデータ

| grade_code | grade_name | grade_name_short | grade_level | description | evaluation_criteria | required_experience_months | skill_indicators | competency_requirements | certification_requirements | project_complexity | mentoring_capability | leadership_level | salary_impact_factor | promotion_eligibility | color_code | sort_order | is_active |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| BEGINNER | 初級 | 初級 | 1 | 基本的な知識を持ち、指導の下で業務を遂行できるレベル | 基本概念の理解、簡単なタスクの実行、指導者のサポートが必要 | 6 | ["基本知識", "指導下での作業", "学習意欲"] | ["基礎理論の理解", "基本操作の習得"] | [] | SIMPLE | False | NONE | 1.0 | False | #90EE90 | 1 | True |
| INTERMEDIATE | 中級 | 中級 | 2 | 一般的な業務を独立して遂行でき、部分的に他者を指導できるレベル | 独立した作業遂行、問題解決能力、基本的な指導スキル | 18 | ["独立作業", "問題解決", "基本指導"] | ["実践的スキル", "問題分析能力", "コミュニケーション能力"] | ["基本情報技術者"] | MODERATE | True | TEAM | 1.2 | True | #FFD700 | 2 | True |
| ADVANCED | 上級 | 上級 | 3 | 複雑な業務をリードし、チーム全体の技術指導ができるレベル | 高度な技術力、リーダーシップ、戦略的思考 | 36 | ["高度技術", "リーダーシップ", "戦略思考"] | ["専門技術", "チーム管理", "技術戦略立案"] | ["応用情報技術者", "専門資格"] | COMPLEX | True | PROJECT | 1.5 | True | #FF8C00 | 3 | True |

## 特記事項

- グレードレベルは1-5の範囲で一意である必要がある
- スキル指標・能力要件・資格要件はJSON形式で柔軟に管理
- 給与影響係数は人事制度との連携で使用
- 色コードはUI表示でのグレード識別に使用
- 昇進資格フラグは人事評価との連携で使用
- 論理削除は is_active フラグで管理
- グレードコードは英大文字・アンダースコアのみ使用可能
- グレードレベルは昇順で連続した値を設定
- 必要経験期間はグレードレベルに比例して設定
- 指導能力は中級以上で true に設定
- リーダーシップレベルはグレードレベルと整合性を保つ
- 給与影響係数はグレードレベルに応じて段階的に設定
- 昇進資格は中級以上で考慮対象とする

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキルグレードマスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |