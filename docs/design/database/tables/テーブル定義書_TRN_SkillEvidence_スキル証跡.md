# テーブル定義書: TRN_SkillEvidence

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_SkillEvidence |
| 論理名 | スキル証跡 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-21 22:02:17 |

## 概要

TRN_SkillEvidence（スキル証跡）は、社員のスキル習得・向上を証明する具体的な証跡情報を管理するトランザクションテーブルです。
主な目的：
- スキル習得の客観的証拠の記録
- 成果物・実績による能力証明
- スキル評価の根拠データ提供
- ポートフォリオ作成支援
- 人事評価・昇進判定の材料提供
このテーブルにより、社員のスキルを定性的・定量的に証明し、
適切な人材配置や能力開発の判断を支援できます。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| skillevidence_id | TRN_SkillEvidenceの主キー | SERIAL |  | × |  | TRN_SkillEvidenceの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_by | レコード作成者のユーザーID | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | レコード更新者のユーザーID | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_trn_skillevidence_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_evidence_employee | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_evidence_skill | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_evidence_verifier | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_evidence_project | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_evidence_training | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_evidence_certification | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_trn_skillevidence | PRIMARY KEY | skillevidence_id, id | 主キー制約 |

## サンプルデータ

| evidence_id | employee_id | skill_id | evidence_type | evidence_title | evidence_description | skill_level_demonstrated | evidence_date | validity_start_date | validity_end_date | file_path | file_type | file_size_kb | external_url | issuer_name | issuer_type | certificate_number | verification_method | verification_status | verified_by | verification_date | verification_comment | related_project_id | related_training_id | related_certification_id | impact_score | complexity_level | team_size | role_in_activity | technologies_used | achievements | lessons_learned | is_public | is_portfolio_item | tags |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| EVD_001 | EMP000001 | SKILL_JAVA_001 | PROJECT | ECサイト基盤システム開発 | 大規模ECサイトのバックエンドシステムをJavaで設計・開発 | ADVANCED | 2024-03-31 | 2024-03-31 | None | /evidence/EVD_001_project_summary.pdf | PDF | 2048 | https://github.com/company/ecommerce-backend | 株式会社サンプル | COMPANY | None | MANAGER | VERIFIED | EMP000010 | 2024-04-05 | 高品質なコードと優れた設計により、システムの安定性と拡張性を実現 | PRJ_REC_001 | None | None | 4.5 | HIGH | 8 | テックリード | ["Java", "Spring Boot", "PostgreSQL", "Redis", "Docker"] | 予定より2週間早期リリース、性能要件120%達成、バグ発生率0.1%以下 | 大規模システムでのマイクロサービス設計、チーム間連携の重要性 | False | True | ["Java", "Spring Boot", "システム設計", "チームリード"] |
| EVD_002 | EMP000002 | SKILL_AWS_001 | CERTIFICATION | AWS認定ソリューションアーキテクト - アソシエイト | AWSクラウドサービスの設計・構築に関する認定資格 | INTERMEDIATE | 2024-02-15 | 2024-02-15 | 2027-02-15 | /evidence/EVD_002_aws_certificate.pdf | PDF | 512 | https://aws.amazon.com/verification | Amazon Web Services | CERTIFICATION_BODY | AWS-SAA-2024-002 | AUTOMATIC | VERIFIED | None | 2024-02-15 | AWS公式認定により自動検証 | None | TRN_HIS_001 | CERT_AWS_001 | 4.0 | MEDIUM | None | 受験者 | ["AWS", "EC2", "S3", "RDS", "Lambda"] | 一発合格、スコア850点（合格ライン720点） | クラウドアーキテクチャの設計原則、AWSサービスの適切な選択方法 | True | True | ["AWS", "クラウド", "認定資格", "アーキテクチャ"] |

## 特記事項

- 証跡ファイルは機密性に応じて適切に管理
- 外部URLは定期的な有効性チェックが必要
- 検証プロセスは証跡の信頼性確保に重要
- ポートフォリオ項目は採用・評価活動に活用
- タグ機能により柔軟な検索・分類が可能
- 有効期限管理により証跡の鮮度を維持

## 業務ルール

- 証跡IDは一意である必要がある
- 有効開始日は有効終了日以前である必要がある
- 検証済み証跡のみがスキル評価に使用可能
- 機密プロジェクトの証跡は公開不可
- ファイルサイズは10MB以下に制限
- 外部URLは定期的な有効性確認が必要
- ポートフォリオ項目は検証済みである必要がある
- 影響度スコアは1.0-5.0の範囲で設定

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル証跡テーブルの詳細定義 |