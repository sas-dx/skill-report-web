# テーブル定義書_MST_CertificationRequirement_資格要件マスタ

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_CertificationRequirement |
| 論理名 | 資格要件マスタ |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |
| 作成者 | 開発チーム |
| バージョン | 1.0.0 |

## テーブル概要

MST_CertificationRequirement（資格要件マスタ）は、職種・役職・スキルレベルに応じた資格要件を管理するマスタテーブルです。

### 主な目的
- 職種別必要資格の定義
- 昇進・昇格要件の管理
- スキルレベル認定基準の設定
- 人材配置判定の支援
- キャリア開発ガイドラインの提供

このテーブルにより、組織の人材要件を明確化し、適切な人材配置と計画的な人材育成を実現できます。

## カラム定義

| # | カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|---|----------|--------|----------|------|------|------------|------|
| 1 | id | ID | VARCHAR | 50 | NOT NULL | | 共通ID（主キー） |
| 2 | requirement_id | 要件ID | VARCHAR | 50 | NOT NULL | | 資格要件を一意に識別するID |
| 3 | requirement_name | 要件名 | VARCHAR | 200 | NOT NULL | | 資格要件の名称 |
| 4 | requirement_description | 要件説明 | TEXT | | NULL | | 資格要件の詳細説明 |
| 5 | requirement_type | 要件種別 | ENUM | | NOT NULL | | 要件の種別（JOB_TYPE:職種要件、POSITION:役職要件、SKILL_GRADE:スキルグレード要件、PROJECT:プロジェクト要件、PROMOTION:昇進要件） |
| 6 | target_job_type_id | 対象職種ID | VARCHAR | 50 | NULL | | 要件が適用される職種のID（MST_JobTypeへの外部キー） |
| 7 | target_position_id | 対象役職ID | VARCHAR | 50 | NULL | | 要件が適用される役職のID（MST_Positionへの外部キー） |
| 8 | target_skill_grade_id | 対象スキルグレードID | VARCHAR | 50 | NULL | | 要件が適用されるスキルグレードのID（MST_SkillGradeへの外部キー） |
| 9 | target_department_id | 対象部署ID | VARCHAR | 50 | NULL | | 要件が適用される部署のID（MST_Departmentへの外部キー） |
| 10 | certification_id | 資格ID | VARCHAR | 50 | NOT NULL | | 必要な資格のID（MST_Certificationへの外部キー） |
| 11 | requirement_level | 要件レベル | ENUM | | NOT NULL | | 要件の必要度（MANDATORY:必須、PREFERRED:推奨、OPTIONAL:任意、DISQUALIFYING:除外条件） |
| 12 | priority_order | 優先順位 | INTEGER | | NOT NULL | 1 | 複数資格がある場合の優先順位（1が最高） |
| 13 | alternative_certifications | 代替資格 | TEXT | | NULL | | 代替可能な資格のリスト（JSON形式） |
| 14 | minimum_experience_years | 最低経験年数 | INTEGER | | NULL | | 資格取得に加えて必要な実務経験年数 |
| 15 | minimum_skill_level | 最低スキルレベル | ENUM | | NULL | | 併せて必要な最低スキルレベル（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| 16 | grace_period_months | 猶予期間 | INTEGER | | NULL | | 資格取得までの猶予期間（月数） |
| 17 | renewal_required | 更新必要フラグ | BOOLEAN | | NOT NULL | FALSE | 資格の定期更新が必要かどうか |
| 18 | renewal_interval_months | 更新間隔 | INTEGER | | NULL | | 資格更新の間隔（月数） |
| 19 | exemption_conditions | 免除条件 | TEXT | | NULL | | 資格要件の免除条件 |
| 20 | assessment_criteria | 評価基準 | TEXT | | NULL | | 要件充足の評価基準・判定方法 |
| 21 | business_justification | 業務上の根拠 | TEXT | | NULL | | 資格要件設定の業務上の根拠・理由 |
| 22 | compliance_requirement | コンプライアンス要件 | BOOLEAN | | NOT NULL | FALSE | 法的・規制上の要件かどうか |
| 23 | client_requirement | 顧客要件 | BOOLEAN | | NOT NULL | FALSE | 顧客要求による要件かどうか |
| 24 | internal_policy | 社内方針 | BOOLEAN | | NOT NULL | FALSE | 社内方針による要件かどうか |
| 25 | effective_start_date | 有効開始日 | DATE | | NOT NULL | | 要件の適用開始日 |
| 26 | effective_end_date | 有効終了日 | DATE | | NULL | | 要件の適用終了日 |
| 27 | notification_timing | 通知タイミング | INTEGER | | NULL | | 要件充足期限前の通知タイミング（日数） |
| 28 | escalation_timing | エスカレーション期限 | INTEGER | | NULL | | 未充足時のエスカレーション期限（日数） |
| 29 | cost_support_available | 費用支援有無 | BOOLEAN | | NOT NULL | FALSE | 資格取得費用の支援があるかどうか |
| 30 | cost_support_amount | 支援金額 | DECIMAL | 10,2 | NULL | | 資格取得費用の支援金額 |
| 31 | cost_support_conditions | 支援条件 | TEXT | | NULL | | 費用支援の条件・制約 |
| 32 | training_support_available | 研修支援有無 | BOOLEAN | | NOT NULL | FALSE | 資格取得のための研修支援があるかどうか |
| 33 | recommended_training_programs | 推奨研修プログラム | TEXT | | NULL | | 資格取得に推奨される研修プログラム（JSON形式） |
| 34 | study_time_allocation | 学習時間配分 | DECIMAL | 5,2 | NULL | | 業務時間内での学習時間配分（時間/週） |
| 35 | success_rate | 合格率 | DECIMAL | 5,2 | NULL | | 社内での資格取得成功率（%） |
| 36 | average_study_hours | 平均学習時間 | DECIMAL | 6,2 | NULL | | 資格取得に必要な平均学習時間 |
| 37 | difficulty_rating | 難易度評価 | ENUM | | NULL | | 社内での難易度評価（EASY:易、MEDIUM:中、HARD:難、VERY_HARD:非常に難） |
| 38 | active_flag | 有効フラグ | BOOLEAN | | NOT NULL | TRUE | 現在有効な要件かどうか |
| 39 | created_by | 作成者 | VARCHAR | 50 | NOT NULL | | 要件を作成した担当者ID |
| 40 | approved_by | 承認者 | VARCHAR | 50 | NULL | | 要件を承認した責任者ID |
| 41 | approval_date | 承認日 | DATE | | NULL | | 要件が承認された日付 |
| 42 | review_date | 見直し日 | DATE | | NULL | | 次回要件見直し予定日 |
| 43 | notes | 備考 | TEXT | | NULL | | その他の備考・補足情報 |
| 44 | created_at | 作成日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード作成日時 |
| 45 | updated_at | 更新日時 | TIMESTAMP | | NOT NULL | CURRENT_TIMESTAMP | レコード更新日時 |
| 46 | updated_by | 更新者 | VARCHAR | 50 | NOT NULL | | レコード更新者 |
| 47 | version | バージョン | INTEGER | | NOT NULL | 1 | 楽観的排他制御用 |
| 48 | deleted_flag | 削除フラグ | BOOLEAN | | NOT NULL | FALSE | 論理削除フラグ |

## インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|---------------|------|--------|------|
| pk_mst_certification_requirement | PRIMARY KEY | id | 主キー |
| uk_requirement_id | UNIQUE | requirement_id | 要件ID一意制約 |
| idx_requirement_type | INDEX | requirement_type | 要件種別検索用 |
| idx_target_job_type | INDEX | target_job_type_id | 対象職種検索用 |
| idx_target_position | INDEX | target_position_id | 対象役職検索用 |
| idx_target_skill_grade | INDEX | target_skill_grade_id | 対象スキルグレード検索用 |
| idx_certification_id | INDEX | certification_id | 資格ID検索用 |
| idx_requirement_level | INDEX | requirement_level | 要件レベル検索用 |
| idx_active_flag | INDEX | active_flag | 有効フラグ検索用 |
| idx_effective_period | INDEX | effective_start_date, effective_end_date | 有効期間検索用 |
| idx_compliance_requirement | INDEX | compliance_requirement | コンプライアンス要件検索用 |
| idx_priority_order | INDEX | priority_order | 優先順位検索用 |

## 制約定義

| 制約名 | 種別 | 内容 | 説明 |
|--------|------|------|------|
| pk_mst_certification_requirement | PRIMARY KEY | id | 主キー制約 |
| uk_requirement_id | UNIQUE | requirement_id | 要件ID一意制約 |
| chk_requirement_type | CHECK | requirement_type IN ('JOB_TYPE', 'POSITION', 'SKILL_GRADE', 'PROJECT', 'PROMOTION') | 要件種別値チェック制約 |
| chk_requirement_level | CHECK | requirement_level IN ('MANDATORY', 'PREFERRED', 'OPTIONAL', 'DISQUALIFYING') | 要件レベル値チェック制約 |
| chk_minimum_skill_level | CHECK | minimum_skill_level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 最低スキルレベル値チェック制約 |
| chk_difficulty_rating | CHECK | difficulty_rating IN ('EASY', 'MEDIUM', 'HARD', 'VERY_HARD') | 難易度評価値チェック制約 |
| chk_priority_order_positive | CHECK | priority_order > 0 | 優先順位正数チェック制約 |
| chk_experience_years_positive | CHECK | minimum_experience_years IS NULL OR minimum_experience_years >= 0 | 最低経験年数非負数チェック制約 |
| chk_grace_period_positive | CHECK | grace_period_months IS NULL OR grace_period_months > 0 | 猶予期間正数チェック制約 |
| chk_renewal_interval_positive | CHECK | renewal_interval_months IS NULL OR renewal_interval_months > 0 | 更新間隔正数チェック制約 |
| chk_effective_period | CHECK | effective_end_date IS NULL OR effective_start_date <= effective_end_date | 有効期間整合性チェック制約 |
| chk_success_rate_range | CHECK | success_rate IS NULL OR (success_rate >= 0 AND success_rate <= 100) | 合格率範囲チェック制約 |
| chk_cost_support_amount_positive | CHECK | cost_support_amount IS NULL OR cost_support_amount >= 0 | 支援金額非負数チェック制約 |

## 外部キー定義

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_cert_req_target_job_type | target_job_type_id | MST_JobType | id | CASCADE | SET NULL | 対象職種への外部キー |
| fk_cert_req_target_position | target_position_id | MST_Position | id | CASCADE | SET NULL | 対象役職への外部キー |
| fk_cert_req_target_skill_grade | target_skill_grade_id | MST_SkillGrade | id | CASCADE | SET NULL | 対象スキルグレードへの外部キー |
| fk_cert_req_target_department | target_department_id | MST_Department | id | CASCADE | SET NULL | 対象部署への外部キー |
| fk_cert_req_certification | certification_id | MST_Certification | id | CASCADE | RESTRICT | 資格への外部キー |
| fk_cert_req_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 作成者への外部キー |
| fk_cert_req_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## サンプルデータ

| requirement_id | requirement_name | requirement_type | target_job_type_id | certification_id | requirement_level | priority_order |
|----------------|------------------|------------------|-------------------|------------------|-------------------|----------------|
| REQ_001 | システムエンジニア必須資格要件 | JOB_TYPE | JOB_001 | CERT_IPA_001 | MANDATORY | 1 |
| REQ_002 | プロジェクトマネージャー昇進要件 | PROMOTION | | CERT_PMP_001 | MANDATORY | 1 |

## 業務ルール

1. 要件IDは一意である必要がある
2. 優先順位は正数である必要がある
3. 有効開始日は有効終了日以前である必要がある
4. 必須要件は猶予期間内に充足される必要がある
5. 更新必要な資格は更新間隔が設定される必要がある
6. 費用支援がある場合は支援条件が明記される必要がある
7. コンプライアンス要件は除外・変更不可
8. 承認済み要件のみ適用可能

## 特記事項

- 代替資格はJSON形式で柔軟に管理
- 費用支援により資格取得を促進
- 研修プログラムとの連携で効率的な学習を支援
- 通知・エスカレーション機能で要件充足を管理
- 成功率・学習時間データで要件設定を最適化
- コンプライアンス・顧客要件を明確に区別

## 改版履歴

| バージョン | 日付 | 作成者 | 変更内容 |
|------------|------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 資格要件マスタの詳細定義 |
