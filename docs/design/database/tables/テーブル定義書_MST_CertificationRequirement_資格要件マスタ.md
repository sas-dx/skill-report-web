# テーブル定義書: MST_CertificationRequirement

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_CertificationRequirement |
| 論理名 | 資格要件マスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:17 |

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
| certificationrequirement_id | MST_CertificationRequirementの主キー | SERIAL |  | × |  | MST_CertificationRequirementの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_certificationrequirement_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_cert_req_target_job_type | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_target_position | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_target_skill_grade | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_target_department | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_cert_req_certification | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_cert_req_created_by | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_cert_req_approved_by | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_certificationrequirement | PRIMARY KEY | certificationrequirement_id | 主キー制約 |

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

## 業務ルール

- 要件IDは一意である必要がある
- 優先順位は正数である必要がある
- 有効開始日は有効終了日以前である必要がある
- 必須要件は猶予期間内に充足される必要がある
- 更新必要な資格は更新間隔が設定される必要がある
- 費用支援がある場合は支援条件が明記される必要がある
- コンプライアンス要件は除外・変更不可
- 承認済み要件のみ適用可能

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 資格要件マスタの詳細定義 |