# テーブル定義書: MST_CertificationRequirement

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_CertificationRequirement |
| 論理名 | 資格要件マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:57 |

## 概要

MST_CertificationRequirement（資格要件マスタ）は、職種・役職・スキルレベルに応じた資格要件を管理するマスタテーブルです。
主な目的：
- 職種別必要資格の定義
- 昇進・昇格要件の管理
- スキルレベル認定基準の設定
- 人材配置判定の支援
- キャリア開発ガイドラインの提供
このテーブルにより、組織の人材要件を明確化し、
適切な人材配置と計画的な人材育成を実現できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| active_flag | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| alternative_certifications | 代替資格 | TEXT |  | ○ |  | 代替資格 |
| approval_date | 承認日 | DATE |  | ○ |  | 承認日 |
| approved_by | 承認者 | VARCHAR | 50 | ○ |  | 承認者 |
| assessment_criteria | 評価基準 | TEXT |  | ○ |  | 評価基準 |
| average_study_hours | 平均学習時間 | DECIMAL | 6,2 | ○ |  | 平均学習時間 |
| business_justification | 業務上の根拠 | TEXT |  | ○ |  | 業務上の根拠 |
| certification_id | 資格ID | VARCHAR | 50 | ○ |  | 資格ID |
| certificationrequirement_id | MST_CertificationRequirementの主キー | SERIAL |  | × |  | MST_CertificationRequirementの主キー |
| client_requirement | 顧客要件 | BOOLEAN |  | ○ | False | 顧客要件 |
| compliance_requirement | コンプライアンス要件 | BOOLEAN |  | ○ | False | コンプライアンス要件 |
| cost_support_amount | 支援金額 | DECIMAL | 10,2 | ○ |  | 支援金額 |
| cost_support_available | 費用支援有無 | BOOLEAN |  | ○ | False | 費用支援有無 |
| cost_support_conditions | 支援条件 | TEXT |  | ○ |  | 支援条件 |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | 作成者 |
| difficulty_rating | 難易度評価 | ENUM |  | ○ |  | 難易度評価 |
| effective_end_date | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| effective_start_date | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| escalation_timing | エスカレーション期限 | INTEGER |  | ○ |  | エスカレーション期限 |
| exemption_conditions | 免除条件 | TEXT |  | ○ |  | 免除条件 |
| grace_period_months | 猶予期間 | INTEGER |  | ○ |  | 猶予期間 |
| internal_policy | 社内方針 | BOOLEAN |  | ○ | False | 社内方針 |
| minimum_experience_years | 最低経験年数 | INTEGER |  | ○ |  | 最低経験年数 |
| minimum_skill_level | 最低スキルレベル | ENUM |  | ○ |  | 最低スキルレベル |
| notes | 備考 | TEXT |  | ○ |  | 備考 |
| notification_timing | 通知タイミング | INTEGER |  | ○ |  | 通知タイミング |
| priority_order | 優先順位 | INTEGER |  | ○ | 1 | 優先順位 |
| recommended_training_programs | 推奨研修プログラム | TEXT |  | ○ |  | 推奨研修プログラム |
| renewal_interval_months | 更新間隔 | INTEGER |  | ○ |  | 更新間隔 |
| renewal_required | 更新必要フラグ | BOOLEAN |  | ○ | False | 更新必要フラグ |
| requirement_description | 要件説明 | TEXT |  | ○ |  | 要件説明 |
| requirement_id | 要件ID | VARCHAR | 50 | ○ |  | 要件ID |
| requirement_level | 要件レベル | ENUM |  | ○ |  | 要件レベル |
| requirement_name | 要件名 | VARCHAR | 200 | ○ |  | 要件名 |
| requirement_type | 要件種別 | ENUM |  | ○ |  | 要件種別 |
| review_date | 見直し日 | DATE |  | ○ |  | 見直し日 |
| study_time_allocation | 学習時間配分 | DECIMAL | 5,2 | ○ |  | 学習時間配分 |
| success_rate | 合格率 | DECIMAL | 5,2 | ○ |  | 合格率 |
| target_department_id | 対象部署ID | VARCHAR | 50 | ○ |  | 対象部署ID |
| target_job_type_id | 対象職種ID | VARCHAR | 50 | ○ |  | 対象職種ID |
| target_position_id | 対象役職ID | VARCHAR | 50 | ○ |  | 対象役職ID |
| target_skill_grade_id | 対象スキルグレードID | VARCHAR | 50 | ○ |  | 対象スキルグレードID |
| training_support_available | 研修支援有無 | BOOLEAN |  | ○ | False | 研修支援有無 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_requirement_id | requirement_id | ○ |  |
| idx_requirement_type | requirement_type | × |  |
| idx_target_job_type | target_job_type_id | × |  |
| idx_target_position | target_position_id | × |  |
| idx_target_skill_grade | target_skill_grade_id | × |  |
| idx_certification_id | certification_id | × |  |
| idx_requirement_level | requirement_level | × |  |
| idx_active_flag | active_flag | × |  |
| idx_effective_period | effective_start_date, effective_end_date | × |  |
| idx_compliance_requirement | compliance_requirement | × |  |
| idx_priority_order | priority_order | × |  |
| idx_mst_certificationrequirement_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_cert_req_target_job_type | target_job_type_id | MST_JobType | id | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_target_position | target_position_id | MST_Position | id | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_target_skill_grade | target_skill_grade_id | MST_SkillGrade | id | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_target_department | target_department_id | MST_Department | id | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_certification | certification_id | MST_Certification | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_cert_req_created_by | created_by | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_cert_req_approved_by | approved_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_requirement_id | UNIQUE |  | requirement_id一意制約 |
| chk_requirement_type | CHECK | requirement_type IN (...) | requirement_type値チェック制約 |
| chk_target_job_type_id | CHECK | target_job_type_id IN (...) | target_job_type_id値チェック制約 |

## サンプルデータ

| requirement_id | requirement_name | requirement_description | requirement_type | target_job_type_id | target_position_id | target_skill_grade_id | target_department_id | certification_id | requirement_level | priority_order | alternative_certifications | minimum_experience_years | minimum_skill_level | grace_period_months | renewal_required | renewal_interval_months | exemption_conditions | assessment_criteria | business_justification | compliance_requirement | client_requirement | internal_policy | effective_start_date | effective_end_date | notification_timing | escalation_timing | cost_support_available | cost_support_amount | cost_support_conditions | training_support_available | recommended_training_programs | study_time_allocation | success_rate | average_study_hours | difficulty_rating | active_flag | created_by | approved_by | approval_date | review_date | notes |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| REQ_001 | システムエンジニア必須資格要件 | システムエンジニア職種における基本的な資格要件 | JOB_TYPE | JOB_001 | None | None | None | CERT_IPA_001 | MANDATORY | 1 | ["基本情報技術者試験", "応用情報技術者試験"] | 2 | INTERMEDIATE | 12 | False | None | 同等の実務経験5年以上、または関連する上位資格保有 | 資格証明書の提出、実務経験の確認 | 技術的基礎知識の担保、顧客への信頼性向上 | False | True | True | 2024-04-01 | None | 90 | 30 | True | 50000.0 | 初回受験のみ、合格時に全額支給 | True | ["TRN_PROG_003", "TRN_PROG_004"] | 2.0 | 75.5 | 150.0 | MEDIUM | True | EMP000010 | EMP000005 | 2024-03-15 | 2025-03-31 | 新入社員は入社3年以内に取得必須 |
| REQ_002 | プロジェクトマネージャー昇進要件 | プロジェクトマネージャー役職への昇進に必要な資格要件 | PROMOTION | None | POS_004 | None | None | CERT_PMP_001 | MANDATORY | 1 | ["プロジェクトマネージャ試験", "P2M資格"] | 5 | ADVANCED | 18 | True | 36 | 大規模プロジェクト成功実績3件以上 | 資格証明書、プロジェクト実績評価、360度評価 | プロジェクト管理能力の客観的証明、国際標準への準拠 | False | True | True | 2024-01-01 | None | 180 | 60 | True | 100000.0 | 受験料・研修費用全額支給、PDU維持費用も支援 | True | ["TRN_PROG_001", "TRN_PROG_005"] | 4.0 | 65.0 | 300.0 | HARD | True | EMP000015 | EMP000008 | 2023-12-01 | 2024-12-31 | PMO部門配属者は優先的に取得支援 |

## 特記事項

- 代替資格はJSON形式で柔軟に管理
- 費用支援により資格取得を促進
- 研修プログラムとの連携で効率的な学習を支援
- 通知・エスカレーション機能で要件充足を管理
- 成功率・学習時間データで要件設定を最適化
- コンプライアンス・顧客要件を明確に区別
- 要件IDは一意である必要がある
- 優先順位は正数である必要がある
- 有効開始日は有効終了日以前である必要がある
- 必須要件は猶予期間内に充足される必要がある
- 更新必要な資格は更新間隔が設定される必要がある
- 費用支援がある場合は支援条件が明記される必要がある
- コンプライアンス要件は除外・変更不可
- 承認済み要件のみ適用可能

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 資格要件マスタの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |