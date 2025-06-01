# テーブル定義書: TRN_SkillEvidence (スキル証跡)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | TRN_SkillEvidence |
| 論理名 | スキル証跡 |
| カテゴリ | トランザクション系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/TRN_SkillEvidence_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル証跡テーブルの詳細定義 |


## 📝 テーブル概要

TRN_SkillEvidence（スキル証跡）は、社員のスキル習得・向上を証明する具体的な証跡情報を管理するトランザクションテーブルです。

主な目的：
- スキル習得の客観的証拠の記録
- 成果物・実績による能力証明
- スキル評価の根拠データ提供
- ポートフォリオ作成支援
- 人事評価・昇進判定の材料提供

このテーブルにより、社員のスキルを定性的・定量的に証明し、
適切な人材配置や能力開発の判断を支援できます。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| evidence_id | 証跡ID | VARCHAR | 50 | ○ |  |  |  | スキル証跡を一意に識別するID |
| employee_id | 社員ID | VARCHAR | 50 | ○ |  | ● |  | 証跡の対象社員ID（MST_Employeeへの外部キー） |
| skill_id | スキルID | VARCHAR | 50 | ○ |  | ● |  | 証明対象のスキルID（MST_SkillItemへの外部キー） |
| evidence_type | 証跡種別 | ENUM |  | ○ |  |  |  | 証跡の種別（CERTIFICATION:資格、PROJECT:プロジェクト成果、TRAINING:研修修了、PORTFOLIO:ポートフォリオ、PEER_REVIEW:同僚評価、SELF_ASSESSMENT:自己評価、OTHER:その他） |
| evidence_title | 証跡タイトル | VARCHAR | 200 | ○ |  |  |  | 証跡の名称・タイトル |
| evidence_description | 証跡説明 | TEXT |  | ○ |  |  |  | 証跡の詳細説明・内容 |
| skill_level_demonstrated | 実証スキルレベル | ENUM |  | ○ |  |  |  | 証跡により実証されるスキルレベル（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート） |
| evidence_date | 証跡日付 | DATE |  | ○ |  |  |  | 証跡が作成・取得された日付 |
| validity_start_date | 有効開始日 | DATE |  | ○ |  |  |  | 証跡の有効期間開始日 |
| validity_end_date | 有効終了日 | DATE |  | ○ |  |  |  | 証跡の有効期間終了日（無期限の場合はNULL） |
| file_path | ファイルパス | VARCHAR | 500 | ○ |  |  |  | 証跡ファイルの保存パス |
| file_type | ファイル種別 | ENUM |  | ○ |  |  |  | 証跡ファイルの種別（PDF:PDF、IMAGE:画像、VIDEO:動画、DOCUMENT:文書、URL:URL、OTHER:その他） |
| file_size_kb | ファイルサイズ | INTEGER |  | ○ |  |  |  | ファイルサイズ（KB） |
| external_url | 外部URL | VARCHAR | 500 | ○ |  |  |  | 外部サイトの証跡URL（GitHub、Qiita等） |
| issuer_name | 発行者名 | VARCHAR | 100 | ○ |  |  |  | 証跡を発行した機関・組織名 |
| issuer_type | 発行者種別 | ENUM |  | ○ |  |  |  | 発行者の種別（COMPANY:会社、EDUCATIONAL:教育機関、CERTIFICATION_BODY:認定機関、GOVERNMENT:政府機関、COMMUNITY:コミュニティ、OTHER:その他） |
| certificate_number | 証明書番号 | VARCHAR | 100 | ○ |  |  |  | 資格証明書・修了証の番号 |
| verification_method | 検証方法 | ENUM |  | ○ |  |  |  | 証跡の検証方法（AUTOMATIC:自動、MANUAL:手動、PEER:同僚、MANAGER:上司、EXTERNAL:外部機関） |
| verification_status | 検証状況 | ENUM |  | ○ |  |  | PENDING | 証跡の検証状況（PENDING:検証待ち、VERIFIED:検証済み、REJECTED:却下、EXPIRED:期限切れ） |
| verified_by | 検証者 | VARCHAR | 50 | ○ |  | ● |  | 証跡を検証した担当者のID |
| verification_date | 検証日 | DATE |  | ○ |  |  |  | 証跡が検証された日付 |
| verification_comment | 検証コメント | TEXT |  | ○ |  |  |  | 検証時のコメント・備考 |
| related_project_id | 関連案件ID | VARCHAR | 50 | ○ |  | ● |  | 関連するプロジェクトのID（TRN_ProjectRecordへの外部キー） |
| related_training_id | 関連研修ID | VARCHAR | 50 | ○ |  | ● |  | 関連する研修のID（TRN_TrainingHistoryへの外部キー） |
| related_certification_id | 関連資格ID | VARCHAR | 50 | ○ |  | ● |  | 関連する資格のID（MST_Certificationへの外部キー） |
| impact_score | 影響度スコア | DECIMAL | 3,1 | ○ |  |  |  | 証跡の影響度・重要度スコア（1.0-5.0） |
| complexity_level | 複雑度レベル | ENUM |  | ○ |  |  |  | 証跡が示す作業の複雑度（LOW:低、MEDIUM:中、HIGH:高、VERY_HIGH:非常に高い） |
| team_size | チーム規模 | INTEGER |  | ○ |  |  |  | 関連プロジェクトのチーム規模 |
| role_in_activity | 活動での役割 | VARCHAR | 100 | ○ |  |  |  | 証跡となる活動での担当役割 |
| technologies_used | 使用技術 | TEXT |  | ○ |  |  |  | 証跡に関連する使用技術（JSON形式） |
| achievements | 成果・実績 | TEXT |  | ○ |  |  |  | 具体的な成果・実績 |
| lessons_learned | 学んだこと | TEXT |  | ○ |  |  |  | 活動から学んだ知識・経験 |
| is_public | 公開フラグ | BOOLEAN |  | ○ |  |  |  | 証跡を社外に公開可能かどうか |
| is_portfolio_item | ポートフォリオ項目フラグ | BOOLEAN |  | ○ |  |  |  | ポートフォリオに含める項目かどうか |
| tags | タグ | TEXT |  | ○ |  |  |  | 検索・分類用のタグ（JSON形式） |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_evidence_id | evidence_id | ○ | 証跡ID検索用（一意） |
| idx_employee_id | employee_id | × | 社員ID検索用 |
| idx_skill_id | skill_id | × | スキルID検索用 |
| idx_evidence_type | evidence_type | × | 証跡種別検索用 |
| idx_skill_level | skill_level_demonstrated | × | スキルレベル検索用 |
| idx_evidence_date | evidence_date | × | 証跡日付検索用 |
| idx_verification_status | verification_status | × | 検証状況検索用 |
| idx_validity_period | validity_start_date, validity_end_date | × | 有効期間検索用 |
| idx_employee_skill | employee_id, skill_id, verification_status | × | 社員別スキル証跡検索用 |
| idx_portfolio | is_portfolio_item, is_public | × | ポートフォリオ項目検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_evidence_id | UNIQUE | evidence_id |  | 証跡ID一意制約 |
| chk_evidence_type | CHECK |  | evidence_type IN ('CERTIFICATION', 'PROJECT', 'TRAINING', 'PORTFOLIO', 'PEER_REVIEW', 'SELF_ASSESSMENT', 'OTHER') | 証跡種別値チェック制約 |
| chk_skill_level | CHECK |  | skill_level_demonstrated IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') | スキルレベル値チェック制約 |
| chk_file_type | CHECK |  | file_type IN ('PDF', 'IMAGE', 'VIDEO', 'DOCUMENT', 'URL', 'OTHER') | ファイル種別値チェック制約 |
| chk_issuer_type | CHECK |  | issuer_type IN ('COMPANY', 'EDUCATIONAL', 'CERTIFICATION_BODY', 'GOVERNMENT', 'COMMUNITY', 'OTHER') | 発行者種別値チェック制約 |
| chk_verification_method | CHECK |  | verification_method IN ('AUTOMATIC', 'MANUAL', 'PEER', 'MANAGER', 'EXTERNAL') | 検証方法値チェック制約 |
| chk_verification_status | CHECK |  | verification_status IN ('PENDING', 'VERIFIED', 'REJECTED', 'EXPIRED') | 検証状況値チェック制約 |
| chk_complexity_level | CHECK |  | complexity_level IN ('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH') | 複雑度レベル値チェック制約 |
| chk_validity_period | CHECK |  | validity_end_date IS NULL OR validity_start_date <= validity_end_date | 有効期間の整合性チェック制約 |
| chk_impact_score | CHECK |  | impact_score IS NULL OR (impact_score >= 1.0 AND impact_score <= 5.0) | 影響度スコア範囲チェック制約 |
| chk_file_size | CHECK |  | file_size_kb IS NULL OR file_size_kb > 0 | ファイルサイズ正数チェック制約 |
| chk_team_size | CHECK |  | team_size IS NULL OR team_size > 0 | チーム規模正数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_evidence_employee | employee_id | MST_Employee | id | CASCADE | RESTRICT | 社員への外部キー |
| fk_evidence_skill | skill_id | MST_SkillItem | id | CASCADE | RESTRICT | スキル項目への外部キー |
| fk_evidence_verifier | verified_by | MST_Employee | id | CASCADE | SET NULL | 検証者への外部キー |
| fk_evidence_project | related_project_id | TRN_ProjectRecord | project_record_id | CASCADE | SET NULL | 関連案件への外部キー |
| fk_evidence_training | related_training_id | TRN_TrainingHistory | training_history_id | CASCADE | SET NULL | 関連研修への外部キー |
| fk_evidence_certification | related_certification_id | MST_Certification | id | CASCADE | SET NULL | 関連資格への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "evidence_id": "EVD_001",
    "employee_id": "EMP000001",
    "skill_id": "SKILL_JAVA_001",
    "evidence_type": "PROJECT",
    "evidence_title": "ECサイト基盤システム開発",
    "evidence_description": "大規模ECサイトのバックエンドシステムをJavaで設計・開発",
    "skill_level_demonstrated": "ADVANCED",
    "evidence_date": "2024-03-31",
    "validity_start_date": "2024-03-31",
    "validity_end_date": null,
    "file_path": "/evidence/EVD_001_project_summary.pdf",
    "file_type": "PDF",
    "file_size_kb": 2048,
    "external_url": "https://github.com/company/ecommerce-backend",
    "issuer_name": "株式会社サンプル",
    "issuer_type": "COMPANY",
    "certificate_number": null,
    "verification_method": "MANAGER",
    "verification_status": "VERIFIED",
    "verified_by": "EMP000010",
    "verification_date": "2024-04-05",
    "verification_comment": "高品質なコードと優れた設計により、システムの安定性と拡張性を実現",
    "related_project_id": "PRJ_REC_001",
    "related_training_id": null,
    "related_certification_id": null,
    "impact_score": 4.5,
    "complexity_level": "HIGH",
    "team_size": 8,
    "role_in_activity": "テックリード",
    "technologies_used": "[\"Java\", \"Spring Boot\", \"PostgreSQL\", \"Redis\", \"Docker\"]",
    "achievements": "予定より2週間早期リリース、性能要件120%達成、バグ発生率0.1%以下",
    "lessons_learned": "大規模システムでのマイクロサービス設計、チーム間連携の重要性",
    "is_public": false,
    "is_portfolio_item": true,
    "tags": "[\"Java\", \"Spring Boot\", \"システム設計\", \"チームリード\"]"
  },
  {
    "evidence_id": "EVD_002",
    "employee_id": "EMP000002",
    "skill_id": "SKILL_AWS_001",
    "evidence_type": "CERTIFICATION",
    "evidence_title": "AWS認定ソリューションアーキテクト - アソシエイト",
    "evidence_description": "AWSクラウドサービスの設計・構築に関する認定資格",
    "skill_level_demonstrated": "INTERMEDIATE",
    "evidence_date": "2024-02-15",
    "validity_start_date": "2024-02-15",
    "validity_end_date": "2027-02-15",
    "file_path": "/evidence/EVD_002_aws_certificate.pdf",
    "file_type": "PDF",
    "file_size_kb": 512,
    "external_url": "https://aws.amazon.com/verification",
    "issuer_name": "Amazon Web Services",
    "issuer_type": "CERTIFICATION_BODY",
    "certificate_number": "AWS-SAA-2024-002",
    "verification_method": "AUTOMATIC",
    "verification_status": "VERIFIED",
    "verified_by": null,
    "verification_date": "2024-02-15",
    "verification_comment": "AWS公式認定により自動検証",
    "related_project_id": null,
    "related_training_id": "TRN_HIS_001",
    "related_certification_id": "CERT_AWS_001",
    "impact_score": 4.0,
    "complexity_level": "MEDIUM",
    "team_size": null,
    "role_in_activity": "受験者",
    "technologies_used": "[\"AWS\", \"EC2\", \"S3\", \"RDS\", \"Lambda\"]",
    "achievements": "一発合格、スコア850点（合格ライン720点）",
    "lessons_learned": "クラウドアーキテクチャの設計原則、AWSサービスの適切な選択方法",
    "is_public": true,
    "is_portfolio_item": true,
    "tags": "[\"AWS\", \"クラウド\", \"認定資格\", \"アーキテクチャ\"]"
  }
]
```

## 📌 特記事項

- 証跡ファイルは機密性に応じて適切に管理
- 外部URLは定期的な有効性チェックが必要
- 検証プロセスは証跡の信頼性確保に重要
- ポートフォリオ項目は採用・評価活動に活用
- タグ機能により柔軟な検索・分類が可能
- 有効期限管理により証跡の鮮度を維持

## 📋 業務ルール

- 証跡IDは一意である必要がある
- 有効開始日は有効終了日以前である必要がある
- 検証済み証跡のみがスキル評価に使用可能
- 機密プロジェクトの証跡は公開不可
- ファイルサイズは10MB以下に制限
- 外部URLは定期的な有効性確認が必要
- ポートフォリオ項目は検証済みである必要がある
- 影響度スコアは1.0-5.0の範囲で設定
