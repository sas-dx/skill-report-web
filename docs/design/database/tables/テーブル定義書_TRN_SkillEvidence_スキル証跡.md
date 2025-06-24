# テーブル定義書: TRN_SkillEvidence

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | TRN_SkillEvidence |
| 論理名 | スキル証跡 |
| カテゴリ | トランザクション系 |
| 生成日時 | 2025-06-24 23:02:18 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| achievements | 成果・実績 | TEXT |  | ○ |  | 成果・実績 |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  | 証明書番号 |
| complexity_level | 複雑度レベル | ENUM |  | ○ |  | 複雑度レベル |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | 社員ID |
| evidence_date | 証跡日付 | DATE |  | ○ |  | 証跡日付 |
| evidence_description | 証跡説明 | TEXT |  | ○ |  | 証跡説明 |
| evidence_id | 証跡ID | VARCHAR | 50 | ○ |  | 証跡ID |
| evidence_title | 証跡タイトル | VARCHAR | 200 | ○ |  | 証跡タイトル |
| evidence_type | 証跡種別 | ENUM |  | ○ |  | 証跡種別 |
| external_url | 外部URL | VARCHAR | 500 | ○ |  | 外部URL |
| file_path | ファイルパス | VARCHAR | 500 | ○ |  | ファイルパス |
| file_size_kb | ファイルサイズ | INTEGER |  | ○ |  | ファイルサイズ |
| file_type | ファイル種別 | ENUM |  | ○ |  | ファイル種別 |
| impact_score | 影響度スコア | DECIMAL | 3,1 | ○ |  | 影響度スコア |
| is_portfolio_item | ポートフォリオ項目フラグ | BOOLEAN |  | ○ | False | ポートフォリオ項目フラグ |
| is_public | 公開フラグ | BOOLEAN |  | ○ | False | 公開フラグ |
| issuer_name | 発行者名 | VARCHAR | 100 | ○ |  | 発行者名 |
| issuer_type | 発行者種別 | ENUM |  | ○ |  | 発行者種別 |
| lessons_learned | 学んだこと | TEXT |  | ○ |  | 学んだこと |
| related_certification_id | 関連資格ID | VARCHAR | 50 | ○ |  | 関連資格ID |
| related_project_id | 関連案件ID | VARCHAR | 50 | ○ |  | 関連案件ID |
| related_training_id | 関連研修ID | VARCHAR | 50 | ○ |  | 関連研修ID |
| role_in_activity | 活動での役割 | VARCHAR | 100 | ○ |  | 活動での役割 |
| skill_id | スキルID | VARCHAR | 50 | ○ |  | スキルID |
| skill_level_demonstrated | 実証スキルレベル | ENUM |  | ○ |  | 実証スキルレベル |
| skillevidence_id | TRN_SkillEvidenceの主キー | SERIAL |  | × |  | TRN_SkillEvidenceの主キー |
| tags | タグ | TEXT |  | ○ |  | タグ |
| team_size | チーム規模 | INTEGER |  | ○ |  | チーム規模 |
| technologies_used | 使用技術 | TEXT |  | ○ |  | 使用技術 |
| validity_end_date | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| validity_start_date | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| verification_comment | 検証コメント | TEXT |  | ○ |  | 検証コメント |
| verification_date | 検証日 | DATE |  | ○ |  | 検証日 |
| verification_method | 検証方法 | ENUM |  | ○ |  | 検証方法 |
| verification_status | 検証状況 | ENUM |  | ○ | PENDING | 検証状況 |
| verified_by | 検証者 | VARCHAR | 50 | ○ |  | 検証者 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| created_by | 作成者ID | VARCHAR | 50 | ○ |  | 作成者ID |
| updated_by | 更新者ID | VARCHAR | 50 | ○ |  | 更新者ID |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_evidence_id | evidence_id | ○ |  |
| idx_employee_id | employee_id | × |  |
| idx_skill_id | skill_id | × |  |
| idx_evidence_type | evidence_type | × |  |
| idx_skill_level | skill_level_demonstrated | × |  |
| idx_evidence_date | evidence_date | × |  |
| idx_verification_status | verification_status | × |  |
| idx_validity_period | validity_start_date, validity_end_date | × |  |
| idx_employee_skill | employee_id, skill_id, verification_status | × |  |
| idx_portfolio | is_portfolio_item, is_public | × |  |
| idx_trn_skillevidence_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_evidence_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_evidence_skill | skill_id | MST_SkillItem | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_evidence_verifier | verified_by | MST_Employee | id | CASCADE | SET NULL | 外部キー制約 |
| fk_evidence_project | related_project_id | TRN_ProjectRecord | id | CASCADE | SET NULL | 外部キー制約 |
| fk_evidence_training | related_training_id | TRN_TrainingHistory | id | CASCADE | SET NULL | 外部キー制約 |
| fk_evidence_certification | related_certification_id | MST_Certification | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_evidence_id | UNIQUE |  | evidence_id一意制約 |
| chk_evidence_type | CHECK | evidence_type IN (...) | evidence_type値チェック制約 |
| chk_file_type | CHECK | file_type IN (...) | file_type値チェック制約 |
| chk_issuer_type | CHECK | issuer_type IN (...) | issuer_type値チェック制約 |
| chk_verification_status | CHECK | verification_status IN (...) | verification_status値チェック制約 |

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
- 証跡IDは一意である必要がある
- 有効開始日は有効終了日以前である必要がある
- 検証済み証跡のみがスキル評価に使用可能
- 機密プロジェクトの証跡は公開不可
- ファイルサイズは10MB以下に制限
- 外部URLは定期的な有効性確認が必要
- ポートフォリオ項目は検証済みである必要がある
- 影響度スコアは1.0-5.0の範囲で設定

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル証跡テーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214007 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214908 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215001 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222632 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |