# テーブル定義書: MST_JobTypeSkill

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_JobTypeSkill |
| 論理名 | 職種スキル関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:18 |

## 概要

MST_JobTypeSkill（職種スキル関連）は、職種と必要スキルの関連付けを管理するマスタテーブルです。
主な目的：
- 職種ごとの必要スキルの定義
- スキル要求レベルの管理
- 職種別スキル要件の標準化
- 人材配置時のスキルマッチング
- 教育計画立案の基礎データ
- 採用要件定義の支援
このテーブルにより、各職種に求められるスキルセットを明確に定義し、
人材育成や配置転換の判断基準として活用できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| jobtypeskill_id | MST_JobTypeSkillの主キー | SERIAL |  | × |  | MST_JobTypeSkillの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_jobtypeskill_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_JobTypeSkill_job_type | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_MST_JobTypeSkill_skill_item | None | None | None | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_jobtypeskill | PRIMARY KEY | jobtypeskill_id | 主キー制約 |
| chk_jobtypeskill_id | CHECK | jobtypeskill_id IN (...) | jobtypeskill_id値チェック制約 |

## サンプルデータ

| job_type_id | skill_item_id | required_level | skill_priority | skill_category | experience_years | certification_required | skill_weight | evaluation_criteria | learning_path | skill_status | effective_date | expiry_date | alternative_skills | prerequisite_skills |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| JOB001 | SKILL001 | 4 | CRITICAL | TECHNICAL | 3.0 | True | 25.0 | 実務プロジェクトでの設計・実装経験、コードレビュー能力 | 基礎研修→実践プロジェクト→上級研修→資格取得 | ACTIVE | 2025-01-01 | None | ["SKILL002", "SKILL003"] | ["SKILL010", "SKILL011"] |
| JOB001 | SKILL002 | 3 | HIGH | BUSINESS | 2.0 | False | 20.0 | 業務要件の理解度、顧客とのコミュニケーション能力 | 業務知識研修→OJT→実践経験 | ACTIVE | 2025-01-01 | None | ["SKILL004"] | ["SKILL012"] |
| JOB002 | SKILL003 | 5 | CRITICAL | MANAGEMENT | 5.0 | True | 30.0 | チーム運営実績、プロジェクト成功率、メンバー育成実績 | リーダーシップ研修→実践経験→管理職研修→資格取得 | ACTIVE | 2025-01-01 | None | None | ["SKILL001", "SKILL002"] |

## 特記事項

- 職種とスキル項目の組み合わせは一意
- 必要レベルは1-5の5段階評価
- スキル重みの合計は職種内で100%となるよう運用で管理
- 代替スキル・前提スキルはJSON形式で管理
- 有効期限により時期に応じたスキル要件変更に対応
- 論理削除は is_deleted フラグで管理
- 資格必須フラグにより採用・昇進要件を明確化

## 業務ルール

- CRITICAL優先度のスキルは必須要件
- HIGH優先度のスキルは重要要件（推奨）
- MEDIUM/LOW優先度のスキルは付加価値要件
- 必要レベル4以上は上級者レベル
- 必要レベル3は中級者レベル
- 必要レベル1-2は初級者レベル
- 資格必須スキルは昇進・配置転換の条件
- 前提スキルを満たさない場合は当該スキルの習得不可
- 代替スキルは同等の価値を持つスキルとして扱う
- 有効期限切れのスキル要件は自動的に無効化

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 職種スキル関連テーブルの詳細定義 |