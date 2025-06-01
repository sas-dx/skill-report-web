# テーブル定義書: MST_CertificationRequirement (資格要件マスタ)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_CertificationRequirement |
| 論理名 | 資格要件マスタ |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_CertificationRequirement_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 資格要件マスタの詳細定義 |


## 📝 テーブル概要

MST_CertificationRequirement（資格要件マスタ）は、職種・役職・スキルレベルに応じた資格要件を管理するマスタテーブルです。

主な目的：
- 職種別必要資格の定義
- 昇進・昇格要件の管理
- スキルレベル認定基準の設定
- 人材配置判定の支援
- キャリア開発ガイドラインの提供

このテーブルにより、組織の人材要件を明確化し、
適切な人材配置と計画的な人材育成を実現できます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| requirement_id | 要件ID | VARCHAR | 50 | ○ |  |  |  | 資格要件を一意に識別するID |
| requirement_name | 要件名 | VARCHAR | 200 | ○ |  |  |  | 資格要件の名称 |
| requirement_description | 要件説明 | TEXT |  | ○ |  |  |  | 資格要件の詳細説明 |
| requirement_type | 要件種別 | ENUM |  | ○ |  |  |  | 要件の種別（JOB_TYPE:職種要件、POSITION:役職要件、SKILL_GRADE:スキルグレード要件、PROJECT:プロジェクト要件、PROMOTION:昇進要件） |
| target_job_type_id | 対象職種ID | VARCHAR | 50 | ○ |  | ● |  | 要件が適用される職種のID（MST_JobTypeへの外部キー） |
| target_position_id | 対象役職ID | VARCHAR | 50 | ○ |  | ● |  | 要件が適用される役職のID（MST_Positionへの外部キー） |
| target_skill_grade_id | 対象スキルグレードID | VARCHAR | 50 | ○ |  | ● |  | 要件が適用されるスキルグレードのID（MST_SkillGradeへの外部キー） |
| target_department_id | 対象部署ID | VARCHAR | 50 | ○ |  | ● |  | 要件が適用される部署のID（MST_Departmentへの外部キー） |
| certification_id | 資格ID | VARCHAR | 50 | ○ |  | ● |  | 必要な資格のID（MST_Certificationへの外部キー） |
| requirement_level | 要件レベル | ENUM |  | ○ |  |  |  | 要件の必要度（MANDATORY:必須、PREFERRED:推奨、OPTIONAL:任意、DISQUALIFYING:除外条件） |
| priority_order | 優先順位 | INTEGER |  | ○ |  |  | 1 | 複数資格がある場合の優先順位（1が最高） |
| alternative_certifications | 代替資格 | TEXT |  | ○ |  |  |  | 代替可能な資格のリスト（JSON形式） |
| minimum_experience_years | 最低経験年数 | INTEGER |  | ○ |  |  |  | 資格取得に加えて必要な実務経験年数 |
| minimum_skill_level | 最低スキルレベル | ENUM |  | ○ |  |  |  | 併せて必要な最低スキルレベル（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| grace_period_months | 猶予期間 | INTEGER |  | ○ |  |  |  | 資格取得までの猶予期間（月数） |
| renewal_required | 更新必要フラグ | BOOLEAN |  | ○ |  |  |  | 資格の定期更新が必要かどうか |
| renewal_interval_months | 更新間隔 | INTEGER |  | ○ |  |  |  | 資格更新の間隔（月数） |
| exemption_conditions | 免除条件 | TEXT |  | ○ |  |  |  | 資格要件の免除条件 |
| assessment_criteria | 評価基準 | TEXT |  | ○ |  |  |  | 要件充足の評価基準・判定方法 |
| business_justification | 業務上の根拠 | TEXT |  | ○ |  |  |  | 資格要件設定の業務上の根拠・理由 |
| compliance_requirement | コンプライアンス要件 | BOOLEAN |  | ○ |  |  |  | 法的・規制上の要件かどうか |
| client_requirement | 顧客要件 | BOOLEAN |  | ○ |  |  |  | 顧客要求による要件かどうか |
| internal_policy | 社内方針 | BOOLEAN |  | ○ |  |  |  | 社内方針による要件かどうか |
| effective_start_date | 有効開始日 | DATE |  | ○ |  |  |  | 要件の適用開始日 |
| effective_end_date | 有効終了日 | DATE |  | ○ |  |  |  | 要件の適用終了日 |
| notification_timing | 通知タイミング | INTEGER |  | ○ |  |  |  | 要件充足期限前の通知タイミング（日数） |
| escalation_timing | エスカレーション期限 | INTEGER |  | ○ |  |  |  | 未充足時のエスカレーション期限（日数） |
| cost_support_available | 費用支援有無 | BOOLEAN |  | ○ |  |  |  | 資格取得費用の支援があるかどうか |
| cost_support_amount | 支援金額 | DECIMAL | 10,2 | ○ |  |  |  | 資格取得費用の支援金額 |
| cost_support_conditions | 支援条件 | TEXT |  | ○ |  |  |  | 費用支援の条件・制約 |
| training_support_available | 研修支援有無 | BOOLEAN |  | ○ |  |  |  | 資格取得のための研修支援があるかどうか |
| recommended_training_programs | 推奨研修プログラム | TEXT |  | ○ |  |  |  | 資格取得に推奨される研修プログラム（JSON形式） |
| study_time_allocation | 学習時間配分 | DECIMAL | 5,2 | ○ |  |  |  | 業務時間内での学習時間配分（時間/週） |
| success_rate | 合格率 | DECIMAL | 5,2 | ○ |  |  |  | 社内での資格取得成功率（%） |
| average_study_hours | 平均学習時間 | DECIMAL | 6,2 | ○ |  |  |  | 資格取得に必要な平均学習時間 |
| difficulty_rating | 難易度評価 | ENUM |  | ○ |  |  |  | 社内での難易度評価（EASY:易、MEDIUM:中、HARD:難、VERY_HARD:非常に難） |
| active_flag | 有効フラグ | BOOLEAN |  | ○ |  |  | True | 現在有効な要件かどうか |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | ● |  | 要件を作成した担当者ID |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | ● |  | 要件を承認した責任者ID |
| approval_date | 承認日 | DATE |  | ○ |  |  |  | 要件が承認された日付 |
| review_date | 見直し日 | DATE |  | ○ |  |  |  | 次回要件見直し予定日 |
| notes | 備考 | TEXT |  | ○ |  |  |  | その他の備考・補足情報 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | ● |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_requirement_id | requirement_id | ○ | 要件ID検索用（一意） |
| idx_requirement_type | requirement_type | × | 要件種別検索用 |
| idx_target_job_type | target_job_type_id | × | 対象職種検索用 |
| idx_target_position | target_position_id | × | 対象役職検索用 |
| idx_target_skill_grade | target_skill_grade_id | × | 対象スキルグレード検索用 |
| idx_certification_id | certification_id | × | 資格ID検索用 |
| idx_requirement_level | requirement_level | × | 要件レベル検索用 |
| idx_active_flag | active_flag | × | 有効フラグ検索用 |
| idx_effective_period | effective_start_date, effective_end_date | × | 有効期間検索用 |
| idx_compliance_requirement | compliance_requirement | × | コンプライアンス要件検索用 |
| idx_priority_order | priority_order | × | 優先順位検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_requirement_id | UNIQUE | requirement_id |  | 要件ID一意制約 |
| chk_requirement_type | CHECK |  | requirement_type IN ('JOB_TYPE', 'POSITION', 'SKILL_GRADE', 'PROJECT', 'PROMOTION') | 要件種別値チェック制約 |
| chk_requirement_level | CHECK |  | requirement_level IN ('MANDATORY', 'PREFERRED', 'OPTIONAL', 'DISQUALIFYING') | 要件レベル値チェック制約 |
| chk_minimum_skill_level | CHECK |  | minimum_skill_level IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | 最低スキルレベル値チェック制約 |
| chk_difficulty_rating | CHECK |  | difficulty_rating IN ('EASY', 'MEDIUM', 'HARD', 'VERY_HARD') | 難易度評価値チェック制約 |
| chk_priority_order_positive | CHECK |  | priority_order > 0 | 優先順位正数チェック制約 |
| chk_experience_years_positive | CHECK |  | minimum_experience_years IS NULL OR minimum_experience_years >= 0 | 最低経験年数非負数チェック制約 |
| chk_grace_period_positive | CHECK |  | grace_period_months IS NULL OR grace_period_months > 0 | 猶予期間正数チェック制約 |
| chk_renewal_interval_positive | CHECK |  | renewal_interval_months IS NULL OR renewal_interval_months > 0 | 更新間隔正数チェック制約 |
| chk_effective_period | CHECK |  | effective_end_date IS NULL OR effective_start_date <= effective_end_date | 有効期間整合性チェック制約 |
| chk_success_rate_range | CHECK |  | success_rate IS NULL OR (success_rate >= 0 AND success_rate <= 100) | 合格率範囲チェック制約 |
| chk_cost_support_amount_positive | CHECK |  | cost_support_amount IS NULL OR cost_support_amount >= 0 | 支援金額非負数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_cert_req_target_job_type | target_job_type_id | MST_JobType | id | CASCADE | SET NULL | 対象職種への外部キー |
| fk_cert_req_target_position | target_position_id | MST_Position | id | CASCADE | SET NULL | 対象役職への外部キー |
| fk_cert_req_target_skill_grade | target_skill_grade_id | MST_SkillGrade | id | CASCADE | SET NULL | 対象スキルグレードへの外部キー |
| fk_cert_req_target_department | target_department_id | MST_Department | id | CASCADE | SET NULL | 対象部署への外部キー |
| fk_cert_req_certification | certification_id | MST_Certification | id | CASCADE | RESTRICT | 資格への外部キー |
| fk_cert_req_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 作成者への外部キー |
| fk_cert_req_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 承認者への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "requirement_id": "REQ_001",
    "requirement_name": "システムエンジニア必須資格要件",
    "requirement_description": "システムエンジニア職種における基本的な資格要件",
    "requirement_type": "JOB_TYPE",
    "target_job_type_id": "JOB_001",
    "target_position_id": null,
    "target_skill_grade_id": null,
    "target_department_id": null,
    "certification_id": "CERT_IPA_001",
    "requirement_level": "MANDATORY",
    "priority_order": 1,
    "alternative_certifications": "[\"基本情報技術者試験\", \"応用情報技術者試験\"]",
    "minimum_experience_years": 2,
    "minimum_skill_level": "INTERMEDIATE",
    "grace_period_months": 12,
    "renewal_required": false,
    "renewal_interval_months": null,
    "exemption_conditions": "同等の実務経験5年以上、または関連する上位資格保有",
    "assessment_criteria": "資格証明書の提出、実務経験の確認",
    "business_justification": "技術的基礎知識の担保、顧客への信頼性向上",
    "compliance_requirement": false,
    "client_requirement": true,
    "internal_policy": true,
    "effective_start_date": "2024-04-01",
    "effective_end_date": null,
    "notification_timing": 90,
    "escalation_timing": 30,
    "cost_support_available": true,
    "cost_support_amount": 50000.0,
    "cost_support_conditions": "初回受験のみ、合格時に全額支給",
    "training_support_available": true,
    "recommended_training_programs": "[\"TRN_PROG_003\", \"TRN_PROG_004\"]",
    "study_time_allocation": 2.0,
    "success_rate": 75.5,
    "average_study_hours": 150.0,
    "difficulty_rating": "MEDIUM",
    "active_flag": true,
    "created_by": "EMP000010",
    "approved_by": "EMP000005",
    "approval_date": "2024-03-15",
    "review_date": "2025-03-31",
    "notes": "新入社員は入社3年以内に取得必須"
  },
  {
    "requirement_id": "REQ_002",
    "requirement_name": "プロジェクトマネージャー昇進要件",
    "requirement_description": "プロジェクトマネージャー役職への昇進に必要な資格要件",
    "requirement_type": "PROMOTION",
    "target_job_type_id": null,
    "target_position_id": "POS_004",
    "target_skill_grade_id": null,
    "target_department_id": null,
    "certification_id": "CERT_PMP_001",
    "requirement_level": "MANDATORY",
    "priority_order": 1,
    "alternative_certifications": "[\"プロジェクトマネージャ試験\", \"P2M資格\"]",
    "minimum_experience_years": 5,
    "minimum_skill_level": "ADVANCED",
    "grace_period_months": 18,
    "renewal_required": true,
    "renewal_interval_months": 36,
    "exemption_conditions": "大規模プロジェクト成功実績3件以上",
    "assessment_criteria": "資格証明書、プロジェクト実績評価、360度評価",
    "business_justification": "プロジェクト管理能力の客観的証明、国際標準への準拠",
    "compliance_requirement": false,
    "client_requirement": true,
    "internal_policy": true,
    "effective_start_date": "2024-01-01",
    "effective_end_date": null,
    "notification_timing": 180,
    "escalation_timing": 60,
    "cost_support_available": true,
    "cost_support_amount": 100000.0,
    "cost_support_conditions": "受験料・研修費用全額支給、PDU維持費用も支援",
    "training_support_available": true,
    "recommended_training_programs": "[\"TRN_PROG_001\", \"TRN_PROG_005\"]",
    "study_time_allocation": 4.0,
    "success_rate": 65.0,
    "average_study_hours": 300.0,
    "difficulty_rating": "HARD",
    "active_flag": true,
    "created_by": "EMP000015",
    "approved_by": "EMP000008",
    "approval_date": "2023-12-01",
    "review_date": "2024-12-31",
    "notes": "PMO部門配属者は優先的に取得支援"
  }
]
```

## 📌 特記事項

- 代替資格はJSON形式で柔軟に管理
- 費用支援により資格取得を促進
- 研修プログラムとの連携で効率的な学習を支援
- 通知・エスカレーション機能で要件充足を管理
- 成功率・学習時間データで要件設定を最適化
- コンプライアンス・顧客要件を明確に区別

## 📋 業務ルール

- 要件IDは一意である必要がある
- 優先順位は正数である必要がある
- 有効開始日は有効終了日以前である必要がある
- 必須要件は猶予期間内に充足される必要がある
- 更新必要な資格は更新間隔が設定される必要がある
- 費用支援がある場合は支援条件が明記される必要がある
- コンプライアンス要件は除外・変更不可
- 承認済み要件のみ適用可能
