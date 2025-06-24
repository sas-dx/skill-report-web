# テーブル定義書: MST_JobTypeSkill

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_JobTypeSkill |
| 論理名 | 職種スキル関連 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| alternative_skills | 代替スキル | TEXT |  | ○ |  | 代替スキル |
| certification_required | 資格必須 | BOOLEAN |  | ○ | False | 資格必須 |
| effective_date | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  | 評価基準 |
| experience_years | 必要経験年数 | DECIMAL | 4,1 | ○ |  | 必要経験年数 |
| expiry_date | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | 職種ID |
| jobtypeskill_id | MST_JobTypeSkillの主キー | SERIAL |  | × |  | MST_JobTypeSkillの主キー |
| learning_path | 学習パス | TEXT |  | ○ |  | 学習パス |
| prerequisite_skills | 前提スキル | TEXT |  | ○ |  | 前提スキル |
| required_level | 必要レベル | INTEGER |  | ○ |  | 必要レベル |
| skill_category | スキル分類 | ENUM |  | ○ |  | スキル分類 |
| skill_item_id | スキル項目ID | VARCHAR | 50 | ○ |  | スキル項目ID |
| skill_priority | スキル優先度 | ENUM |  | ○ | MEDIUM | スキル優先度 |
| skill_status | スキル状況 | ENUM |  | ○ | ACTIVE | スキル状況 |
| skill_weight | スキル重み | DECIMAL | 5,2 | ○ |  | スキル重み |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_JobTypeSkill_job_type_id | job_type_id | × |  |
| idx_MST_JobTypeSkill_skill_item_id | skill_item_id | × |  |
| idx_MST_JobTypeSkill_job_skill | job_type_id, skill_item_id | ○ |  |
| idx_MST_JobTypeSkill_required_level | required_level | × |  |
| idx_MST_JobTypeSkill_priority | skill_priority | × |  |
| idx_MST_JobTypeSkill_category | skill_category | × |  |
| idx_MST_JobTypeSkill_status | skill_status | × |  |
| idx_MST_JobTypeSkill_effective_date | effective_date | × |  |
| idx_mst_jobtypeskill_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_JobTypeSkill_job_type | job_type_id | MST_JobType | id | CASCADE | CASCADE | 外部キー制約 |
| fk_MST_JobTypeSkill_skill_item | skill_item_id | MST_SkillItem | id | CASCADE | CASCADE | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_job_type_id | CHECK | job_type_id IN (...) | job_type_id値チェック制約 |
| chk_jobtypeskill_id | CHECK | jobtypeskill_id IN (...) | jobtypeskill_id値チェック制約 |
| chk_required_level | CHECK | required_level > 0 | required_level正値チェック制約 |
| chk_skill_status | CHECK | skill_status IN (...) | skill_status値チェック制約 |

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

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 職種スキル関連テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214906 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |