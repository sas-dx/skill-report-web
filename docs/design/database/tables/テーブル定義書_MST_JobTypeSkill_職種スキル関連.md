# テーブル定義書: MST_JobTypeSkill (職種スキル関連)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_JobTypeSkill |
| 論理名 | 職種スキル関連 |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_JobTypeSkill_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 職種スキル関連テーブルの詳細定義 |


## 📝 テーブル概要

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


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| job_type_id | 職種ID | VARCHAR | 50 | ○ |  | ● |  | 職種のID（MST_JobTypeへの外部キー） |
| skill_item_id | スキル項目ID | VARCHAR | 50 | ○ |  | ● |  | スキル項目のID（MST_SkillItemへの外部キー） |
| required_level | 必要レベル | INTEGER |  | ○ |  |  |  | 当該職種で必要なスキルレベル（1-5、5が最高レベル） |
| skill_priority | スキル優先度 | ENUM |  | ○ |  |  | MEDIUM | スキル優先度（CRITICAL:必須、HIGH:重要、MEDIUM:推奨、LOW:あれば良い） |
| skill_category | スキル分類 | ENUM |  | ○ |  |  |  | スキル分類（TECHNICAL:技術、BUSINESS:業務、MANAGEMENT:管理、COMMUNICATION:コミュニケーション） |
| experience_years | 必要経験年数 | DECIMAL | 4,1 | ○ |  |  |  | 当該スキルの必要経験年数 |
| certification_required | 資格必須 | BOOLEAN |  | ○ |  |  |  | 関連資格の取得が必須かどうか |
| skill_weight | スキル重み | DECIMAL | 5,2 | ○ |  |  |  | 職種内でのスキル重み（%、合計100%） |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  |  |  | スキルレベルの評価基準・判定方法 |
| learning_path | 学習パス | TEXT |  | ○ |  |  |  | スキル習得のための推奨学習パス |
| skill_status | スキル状況 | ENUM |  | ○ |  |  | ACTIVE | スキル状況（ACTIVE:有効、DEPRECATED:非推奨、OBSOLETE:廃止） |
| effective_date | 有効開始日 | DATE |  | ○ |  |  |  | スキル要件の有効開始日 |
| expiry_date | 有効終了日 | DATE |  | ○ |  |  |  | スキル要件の有効終了日（NULL:無期限） |
| alternative_skills | 代替スキル | TEXT |  | ○ |  |  |  | 代替可能なスキルのリスト（JSON形式） |
| prerequisite_skills | 前提スキル | TEXT |  | ○ |  |  |  | 前提となるスキルのリスト（JSON形式） |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_JobTypeSkill_job_type_id | job_type_id | × | 職種ID検索用 |
| idx_MST_JobTypeSkill_skill_item_id | skill_item_id | × | スキル項目ID検索用 |
| idx_MST_JobTypeSkill_job_skill | job_type_id, skill_item_id | ○ | 職種・スキル複合検索用（一意） |
| idx_MST_JobTypeSkill_required_level | required_level | × | 必要レベル別検索用 |
| idx_MST_JobTypeSkill_priority | skill_priority | × | 優先度別検索用 |
| idx_MST_JobTypeSkill_category | skill_category | × | スキル分類別検索用 |
| idx_MST_JobTypeSkill_status | skill_status | × | スキル状況別検索用 |
| idx_MST_JobTypeSkill_effective_date | effective_date | × | 有効開始日検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_MST_JobTypeSkill_job_skill | UNIQUE | job_type_id, skill_item_id |  | 職種・スキル項目一意制約 |
| chk_MST_JobTypeSkill_required_level | CHECK |  | required_level >= 1 AND required_level <= 5 | 必要レベル範囲チェック制約 |
| chk_MST_JobTypeSkill_priority | CHECK |  | skill_priority IN ('CRITICAL', 'HIGH', 'MEDIUM', 'LOW') | スキル優先度値チェック制約 |
| chk_MST_JobTypeSkill_category | CHECK |  | skill_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'COMMUNICATION') | スキル分類値チェック制約 |
| chk_MST_JobTypeSkill_status | CHECK |  | skill_status IN ('ACTIVE', 'DEPRECATED', 'OBSOLETE') | スキル状況値チェック制約 |
| chk_MST_JobTypeSkill_experience_years | CHECK |  | experience_years IS NULL OR experience_years >= 0 | 必要経験年数非負値チェック制約 |
| chk_MST_JobTypeSkill_skill_weight | CHECK |  | skill_weight IS NULL OR (skill_weight >= 0 AND skill_weight <= 100) | スキル重み範囲チェック制約 |
| chk_MST_JobTypeSkill_date_range | CHECK |  | expiry_date IS NULL OR effective_date <= expiry_date | 日付範囲整合性チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_MST_JobTypeSkill_job_type | job_type_id | MST_JobType | id | CASCADE | CASCADE | 職種への外部キー |
| fk_MST_JobTypeSkill_skill_item | skill_item_id | MST_SkillItem | id | CASCADE | CASCADE | スキル項目への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "job_type_id": "JOB001",
    "skill_item_id": "SKILL001",
    "required_level": 4,
    "skill_priority": "CRITICAL",
    "skill_category": "TECHNICAL",
    "experience_years": 3.0,
    "certification_required": true,
    "skill_weight": 25.0,
    "evaluation_criteria": "実務プロジェクトでの設計・実装経験、コードレビュー能力",
    "learning_path": "基礎研修→実践プロジェクト→上級研修→資格取得",
    "skill_status": "ACTIVE",
    "effective_date": "2025-01-01",
    "expiry_date": null,
    "alternative_skills": "[\"SKILL002\", \"SKILL003\"]",
    "prerequisite_skills": "[\"SKILL010\", \"SKILL011\"]"
  },
  {
    "job_type_id": "JOB001",
    "skill_item_id": "SKILL002",
    "required_level": 3,
    "skill_priority": "HIGH",
    "skill_category": "BUSINESS",
    "experience_years": 2.0,
    "certification_required": false,
    "skill_weight": 20.0,
    "evaluation_criteria": "業務要件の理解度、顧客とのコミュニケーション能力",
    "learning_path": "業務知識研修→OJT→実践経験",
    "skill_status": "ACTIVE",
    "effective_date": "2025-01-01",
    "expiry_date": null,
    "alternative_skills": "[\"SKILL004\"]",
    "prerequisite_skills": "[\"SKILL012\"]"
  },
  {
    "job_type_id": "JOB002",
    "skill_item_id": "SKILL003",
    "required_level": 5,
    "skill_priority": "CRITICAL",
    "skill_category": "MANAGEMENT",
    "experience_years": 5.0,
    "certification_required": true,
    "skill_weight": 30.0,
    "evaluation_criteria": "チーム運営実績、プロジェクト成功率、メンバー育成実績",
    "learning_path": "リーダーシップ研修→実践経験→管理職研修→資格取得",
    "skill_status": "ACTIVE",
    "effective_date": "2025-01-01",
    "expiry_date": null,
    "alternative_skills": null,
    "prerequisite_skills": "[\"SKILL001\", \"SKILL002\"]"
  }
]
```

## 📌 特記事項

- 職種とスキル項目の組み合わせは一意
- 必要レベルは1-5の5段階評価
- スキル重みの合計は職種内で100%となるよう運用で管理
- 代替スキル・前提スキルはJSON形式で管理
- 有効期限により時期に応じたスキル要件変更に対応
- 論理削除は is_deleted フラグで管理
- 資格必須フラグにより採用・昇進要件を明確化

## 📋 業務ルール

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
