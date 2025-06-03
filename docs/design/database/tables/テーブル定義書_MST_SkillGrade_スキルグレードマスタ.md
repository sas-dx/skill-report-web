# テーブル定義書: MST_SkillGrade

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillGrade |
| 論理名 | スキルグレードマスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

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
| grade_code | グレードコード | VARCHAR | 20 | ○ |  | スキルグレードを一意に識別するコード（例：BEGINNER、INTERMEDIATE、ADVANCED、EXPERT） |
| grade_name | グレード名 | VARCHAR | 50 | ○ |  | スキルグレードの名称 |
| grade_name_short | グレード名（短縮） | VARCHAR | 10 | ○ |  | 表示用の短縮名称（例：初級、中級、上級、専門） |
| grade_level | グレードレベル | INTEGER |  | ○ |  | グレードの数値レベル（1:初級、2:中級、3:上級、4:専門、5:エキスパート） |
| description | グレード説明 | TEXT |  | ○ |  | スキルグレードの詳細説明・到達基準 |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  | グレード判定のための具体的な評価基準 |
| required_experience_months | 必要経験期間（月） | INTEGER |  | ○ |  | グレード到達に必要な経験期間の目安（月数） |
| skill_indicators | スキル指標 | TEXT |  | ○ |  | グレード判定のためのスキル指標（JSON形式） |
| competency_requirements | 能力要件 | TEXT |  | ○ |  | グレードに求められる能力・知識要件（JSON形式） |
| certification_requirements | 資格要件 | TEXT |  | ○ |  | グレード認定に必要な資格（JSON形式） |
| project_complexity | プロジェクト複雑度 | ENUM |  | ○ |  | 担当可能なプロジェクトの複雑度（SIMPLE:単純、MODERATE:中程度、COMPLEX:複雑、CRITICAL:重要） |
| mentoring_capability | 指導能力 | BOOLEAN |  | ○ | False | 他者への指導・メンタリング能力があるか |
| leadership_level | リーダーシップレベル | ENUM |  | ○ |  | 発揮できるリーダーシップレベル（NONE:なし、TEAM:チーム、PROJECT:プロジェクト、ORGANIZATION:組織） |
| salary_impact_factor | 給与影響係数 | DECIMAL | 3,2 | ○ |  | 給与計算への影響係数（1.0を基準とした倍率） |
| promotion_eligibility | 昇進資格 | BOOLEAN |  | ○ | False | 昇進要件として考慮されるグレードか |
| color_code | 表示色コード | VARCHAR | 7 | ○ |  | UI表示用の色コード（例：#FF0000） |
| sort_order | 表示順序 | INTEGER |  | ○ | 0 | グレード一覧での表示順序 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | グレードが有効かどうか |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_grade_code | grade_code | ○ | グレードコード検索用（一意） |
| idx_grade_level | grade_level | ○ | グレードレベル検索用（一意） |
| idx_grade_name | grade_name | × | グレード名検索用 |
| idx_mentoring | mentoring_capability, is_active | × | 指導能力検索用 |
| idx_promotion | promotion_eligibility, is_active | × | 昇進資格検索用 |
| idx_sort_order | sort_order | × | 表示順序検索用 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_grade_code | UNIQUE |  | グレードコード一意制約 |
| uk_grade_level | UNIQUE |  | グレードレベル一意制約 |
| chk_grade_level | CHECK | grade_level >= 1 AND grade_level <= 5 | グレードレベル範囲チェック制約 |
| chk_project_complexity | CHECK | project_complexity IN ('SIMPLE', 'MODERATE', 'COMPLEX', 'CRITICAL') | プロジェクト複雑度値チェック制約 |
| chk_leadership_level | CHECK | leadership_level IN ('NONE', 'TEAM', 'PROJECT', 'ORGANIZATION') | リーダーシップレベル値チェック制約 |
| chk_experience_months | CHECK | required_experience_months IS NULL OR required_experience_months >= 0 | 必要経験期間非負数チェック制約 |
| chk_salary_factor | CHECK | salary_impact_factor IS NULL OR salary_impact_factor > 0 | 給与影響係数正数チェック制約 |

## サンプルデータ

| grade_code | grade_name | grade_name_short | grade_level | description | evaluation_criteria | required_experience_months | skill_indicators | competency_requirements | certification_requirements | project_complexity | mentoring_capability | leadership_level | salary_impact_factor | promotion_eligibility | color_code | sort_order | is_active |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| BEGINNER | 初級 | 初級 | 1 | 基本的な知識を持ち、指導の下で業務を遂行できるレベル | 基本概念の理解、簡単なタスクの実行、指導者のサポートが必要 | 6 | ["基本知識", "指導下での作業", "学習意欲"] | ["基礎理論の理解", "基本操作の習得"] | [] | SIMPLE | False | NONE | 1.0 | False | #90EE90 | 1 | True |
| INTERMEDIATE | 中級 | 中級 | 2 | 一般的な業務を独立して遂行でき、部分的に他者を指導できるレベル | 独立した作業遂行、問題解決能力、基本的な指導スキル | 18 | ["独立作業", "問題解決", "基本指導"] | ["実践的スキル", "問題分析能力", "コミュニケーション能力"] | ["基本情報技術者"] | MODERATE | True | TEAM | 1.2 | True | #FFD700 | 2 | True |
| ADVANCED | 上級 | 上級 | 3 | 複雑な業務をリードし、チーム全体の技術指導ができるレベル | 高度な技術力、リーダーシップ、戦略的思考 | 36 | ["高度技術", "リーダーシップ", "戦略思考"] | ["専門技術", "チーム管理", "技術戦略立案"] | ["応用情報技術者", "専門資格"] | COMPLEX | True | PROJECT | 1.5 | True | #FF8C00 | 3 | True |
| EXPERT | 専門家 | 専門 | 4 | 組織全体の技術方針に影響を与え、業界レベルでの専門性を持つレベル | 業界専門性、組織への影響力、イノベーション創出 | 60 | ["業界専門性", "組織影響力", "イノベーション"] | ["業界知識", "組織運営", "技術革新"] | ["高度情報技術者", "業界認定資格"] | CRITICAL | True | ORGANIZATION | 2.0 | True | #DC143C | 4 | True |

## 特記事項

- グレードレベルは1-5の範囲で一意である必要がある
- スキル指標・能力要件・資格要件はJSON形式で柔軟に管理
- 給与影響係数は人事制度との連携で使用
- 色コードはUI表示でのグレード識別に使用
- 昇進資格フラグは人事評価との連携で使用
- 論理削除は is_active フラグで管理

## 業務ルール

- グレードコードは英大文字・アンダースコアのみ使用可能
- グレードレベルは昇順で連続した値を設定
- 必要経験期間はグレードレベルに比例して設定
- 指導能力は中級以上で true に設定
- リーダーシップレベルはグレードレベルと整合性を保つ
- 給与影響係数はグレードレベルに応じて段階的に設定
- 昇進資格は中級以上で考慮対象とする

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキルグレードマスタテーブルの詳細定義 |
