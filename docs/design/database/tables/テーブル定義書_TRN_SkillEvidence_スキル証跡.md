# テーブル定義書：TRN_SkillEvidence（スキル証跡）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-038 |
| **テーブル名** | TRN_SkillEvidence |
| **論理名** | スキル証跡 |
| **カテゴリ** | トランザクション系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
スキル証跡テーブル（TRN_SkillEvidence）は、スキル評価の根拠となる証跡情報を管理します。プロジェクト成果物、資格証明書、研修修了証、作品ポートフォリオなど、スキルレベルを裏付ける具体的な証拠を保持し、客観的で信頼性の高いスキル評価を支援します。

### 2.2 関連API
- [API-038](../../api/specs/API仕様書_API-038_スキル証跡管理API.md) - スキル証跡管理API

### 2.3 関連バッチ
- [BATCH-034](../../batch/specs/バッチ定義書_BATCH-034_証跡ファイル整理バッチ.md) - 証跡ファイル整理バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | evidence_id | 証跡ID | VARCHAR | 20 | × | ○ | - | - | スキル証跡を一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | skill_record_id | スキル記録ID | VARCHAR | 20 | × | - | ○ | - | 関連するスキル評価記録ID |
| 4 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 証跡の所有者である社員ID |
| 5 | skill_item_id | スキル項目ID | VARCHAR | 20 | × | - | ○ | - | 証跡が示すスキル項目ID |
| 6 | evidence_type | 証跡種別 | VARCHAR | 30 | × | - | - | 'DOCUMENT' | 証跡の種別（DOCUMENT/CERTIFICATION/PROJECT/PORTFOLIO/TRAINING等） |
| 7 | evidence_category | 証跡カテゴリ | VARCHAR | 50 | ○ | - | - | NULL | 証跡の詳細カテゴリ |
| 8 | evidence_title | 証跡タイトル | VARCHAR | 200 | × | - | - | - | 証跡の名称・タイトル |
| 9 | evidence_description | 証跡説明 | TEXT | - | ○ | - | - | NULL | 証跡の詳細説明 |
| 10 | file_path | ファイルパス | VARCHAR | 500 | ○ | - | - | NULL | 証跡ファイルの保存パス |
| 11 | file_name | ファイル名 | VARCHAR | 255 | ○ | - | - | NULL | 証跡ファイルの元ファイル名 |
| 12 | file_size | ファイルサイズ | BIGINT | - | ○ | - | - | NULL | ファイルサイズ（バイト） |
| 13 | file_type | ファイル種別 | VARCHAR | 50 | ○ | - | - | NULL | ファイルのMIMEタイプ |
| 14 | file_extension | ファイル拡張子 | VARCHAR | 10 | ○ | - | - | NULL | ファイルの拡張子 |
| 15 | external_url | 外部URL | VARCHAR | 500 | ○ | - | - | NULL | 外部サイトの証跡URL（GitHub、Qiita等） |
| 16 | project_name | プロジェクト名 | VARCHAR | 200 | ○ | - | - | NULL | 関連プロジェクト名 |
| 17 | project_period | プロジェクト期間 | VARCHAR | 50 | ○ | - | - | NULL | プロジェクト実施期間 |
| 18 | role_in_project | プロジェクト内役割 | VARCHAR | 100 | ○ | - | - | NULL | プロジェクトでの担当役割 |
| 19 | technologies_used | 使用技術 | TEXT | - | ○ | - | - | NULL | 使用した技術・ツール |
| 20 | achievement_description | 成果説明 | TEXT | - | ○ | - | - | NULL | 具体的な成果・実績の説明 |
| 21 | certification_name | 資格名 | VARCHAR | 200 | ○ | - | - | NULL | 取得資格名 |
| 22 | certification_id_ref | 資格ID参照 | VARCHAR | 20 | ○ | - | ○ | NULL | MST_Certificationへの参照 |
| 23 | certification_date | 資格取得日 | DATE | - | ○ | - | - | NULL | 資格取得日 |
| 24 | certification_score | 資格スコア | INTEGER | - | ○ | - | - | NULL | 資格試験のスコア |
| 25 | certification_expiry | 資格有効期限 | DATE | - | ○ | - | - | NULL | 資格の有効期限 |
| 26 | training_name | 研修名 | VARCHAR | 200 | ○ | - | - | NULL | 受講研修名 |
| 27 | training_provider | 研修提供者 | VARCHAR | 200 | ○ | - | - | NULL | 研修提供機関・会社 |
| 28 | training_completion_date | 研修修了日 | DATE | - | ○ | - | - | NULL | 研修修了日 |
| 29 | training_hours | 研修時間 | INTEGER | - | ○ | - | - | NULL | 研修受講時間 |
| 30 | skill_level_demonstrated | 実証スキルレベル | INTEGER | - | ○ | - | - | NULL | この証跡が示すスキルレベル（1-5） |
| 31 | verification_status | 検証ステータス | VARCHAR | 20 | × | - | - | 'PENDING' | 証跡の検証状況（PENDING/VERIFIED/REJECTED） |
| 32 | verified_by | 検証者ID | VARCHAR | 20 | ○ | - | ○ | NULL | 証跡を検証した人のID |
| 33 | verified_date | 検証日 | DATE | - | ○ | - | - | NULL | 証跡検証日 |
| 34 | verification_comment | 検証コメント | TEXT | - | ○ | - | - | NULL | 検証時のコメント |
| 35 | visibility | 公開範囲 | VARCHAR | 20 | × | - | - | 'PRIVATE' | 証跡の公開範囲（PRIVATE/TEAM/COMPANY/PUBLIC） |
| 36 | tags | タグ | TEXT | - | ○ | - | - | NULL | 証跡に付与するタグ（JSON形式） |
| 37 | is_featured | 注目証跡フラグ | BOOLEAN | - | × | - | - | FALSE | 注目すべき証跡かどうか |
| 38 | display_order | 表示順序 | INTEGER | - | × | - | - | 0 | 証跡一覧での表示順序 |
| 39 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 証跡が有効かどうか |
| 40 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 41 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 42 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 43 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | evidence_id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_skill_record | INDEX | skill_record_id | スキル記録検索用 |
| idx_employee | INDEX | employee_id | 社員検索用 |
| idx_skill_item | INDEX | skill_item_id | スキル項目検索用 |
| idx_evidence_type | INDEX | evidence_type | 証跡種別検索用 |
| idx_evidence_category | INDEX | evidence_category | 証跡カテゴリ検索用 |
| idx_verification_status | INDEX | verification_status | 検証ステータス検索用 |
| idx_verified_by | INDEX | verified_by | 検証者検索用 |
| idx_visibility | INDEX | visibility | 公開範囲検索用 |
| idx_featured | INDEX | is_featured | 注目証跡検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_certification_ref | INDEX | certification_id_ref | 資格参照検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_evidence | PRIMARY KEY | evidence_id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_skill_record | FOREIGN KEY | skill_record_id | TRN_SkillRecord.skill_record_id |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_skill_item | FOREIGN KEY | skill_item_id | MST_SkillItem.skill_item_id |
| fk_certification_ref | FOREIGN KEY | certification_id_ref | MST_Certification.certification_id |
| fk_verified_by | FOREIGN KEY | verified_by | MST_Employee.employee_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_evidence_type | CHECK | evidence_type | evidence_type IN ('DOCUMENT', 'CERTIFICATION', 'PROJECT', 'PORTFOLIO', 'TRAINING', 'AWARD', 'PUBLICATION', 'PRESENTATION') |
| chk_file_size | CHECK | file_size | file_size IS NULL OR file_size > 0 |
| chk_skill_level_demonstrated | CHECK | skill_level_demonstrated | skill_level_demonstrated IS NULL OR (skill_level_demonstrated >= 1 AND skill_level_demonstrated <= 5) |
| chk_verification_status | CHECK | verification_status | verification_status IN ('PENDING', 'VERIFIED', 'REJECTED') |
| chk_visibility | CHECK | visibility | visibility IN ('PRIVATE', 'TEAM', 'COMPANY', 'PUBLIC') |
| chk_certification_score | CHECK | certification_score | certification_score IS NULL OR certification_score >= 0 |
| chk_training_hours | CHECK | training_hours | training_hours IS NULL OR training_hours > 0 |
| chk_display_order | CHECK | display_order | display_order >= 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| TRN_SkillRecord | skill_record_id | 1:N | スキル評価記録 |
| MST_Employee | employee_id | 1:N | 証跡所有者 |
| MST_Employee | verified_by | 1:N | 検証者 |
| MST_SkillItem | skill_item_id | 1:N | スキル項目 |
| MST_Certification | certification_id_ref | 1:N | 資格情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 子テーブルなし |

## 5. データ仕様

### 5.1 データ例
```sql
-- プロジェクト証跡
INSERT INTO TRN_SkillEvidence (
    evidence_id, tenant_id, skill_record_id, employee_id, skill_item_id,
    evidence_type, evidence_title, evidence_description,
    project_name, project_period, role_in_project, technologies_used,
    achievement_description, skill_level_demonstrated,
    verification_status, visibility, created_by, updated_by
) VALUES (
    'EVIDENCE_001', 'TENANT_001', 'SKILL_REC_001', 'EMP_001', 'SKILL_001',
    'PROJECT', 'ECサイト構築プロジェクト', 'Java Spring Bootを使用したECサイトのバックエンド開発',
    'ECサイト構築プロジェクト', '2025-01-01〜2025-03-31', 'バックエンドエンジニア',
    'Java, Spring Boot, MySQL, Docker, AWS',
    '決済機能とユーザー管理機能を担当。パフォーマンス要件を満たすAPIを設計・実装。',
    4, 'VERIFIED', 'COMPANY', 'user_001', 'user_001'
);

-- 資格証跡
INSERT INTO TRN_SkillEvidence (
    evidence_id, tenant_id, skill_record_id, employee_id, skill_item_id,
    evidence_type, evidence_title, evidence_description,
    certification_name, certification_id_ref, certification_date, certification_score,
    file_path, file_name, file_type, skill_level_demonstrated,
    verification_status, visibility, created_by, updated_by
) VALUES (
    'EVIDENCE_002', 'TENANT_001', 'SKILL_REC_002', 'EMP_002', 'SKILL_002',
    'CERTIFICATION', 'AWS認定ソリューションアーキテクト', 'AWS SAA資格取得証明',
    'AWS Certified Solutions Architect - Associate', 'CERT_AWS_SAA', '2025-05-15', 850,
    '/evidence/certificates/aws_saa_emp002.pdf', 'aws_saa_certificate.pdf', 'application/pdf',
    4, 'VERIFIED', 'COMPANY', 'user_002', 'user_002'
);

-- 研修証跡
INSERT INTO TRN_SkillEvidence (
    evidence_id, tenant_id, skill_record_id, employee_id, skill_item_id,
    evidence_type, evidence_title, evidence_description,
    training_name, training_provider, training_completion_date, training_hours,
    file_path, file_name, skill_level_demonstrated,
    verification_status, visibility, created_by, updated_by
) VALUES (
    'EVIDENCE_003', 'TENANT_001', 'SKILL_REC_003', 'EMP_003', 'SKILL_003',
    'TRAINING', 'Kubernetes実践研修', 'Kubernetesの基礎から実践まで学習',
    'Kubernetes実践研修', '株式会社テックアカデミー', '2025-04-30', 40,
    '/evidence/training/k8s_training_emp003.pdf', 'k8s_training_certificate.pdf',
    3, 'VERIFIED', 'TEAM', 'user_003', 'user_003'
);

-- ポートフォリオ証跡
INSERT INTO TRN_SkillEvidence (
    evidence_id, tenant_id, skill_record_id, employee_id, skill_item_id,
    evidence_type, evidence_title, evidence_description,
    external_url, technologies_used, achievement_description,
    skill_level_demonstrated, verification_status, visibility,
    tags, is_featured, created_by, updated_by
) VALUES (
    'EVIDENCE_004', 'TENANT_001', 'SKILL_REC_004', 'EMP_004', 'SKILL_004',
    'PORTFOLIO', 'オープンソースライブラリ開発', 'React用のUIコンポーネントライブラリを開発・公開',
    'https://github.com/emp004/react-ui-components', 'React, TypeScript, Storybook, Jest',
    'NPMで公開し、週間ダウンロード数1000回を達成。コミュニティからの貢献も受けている。',
    5, 'VERIFIED', 'PUBLIC',
    '["React", "TypeScript", "OSS", "UI/UX"]', TRUE, 'user_004', 'user_004'
);

-- 受賞証跡
INSERT INTO TRN_SkillEvidence (
    evidence_id, tenant_id, skill_record_id, employee_id, skill_item_id,
    evidence_type, evidence_title, evidence_description,
    achievement_description, file_path, file_name,
    skill_level_demonstrated, verification_status, visibility,
    is_featured, created_by, updated_by
) VALUES (
    'EVIDENCE_005', 'TENANT_001', 'SKILL_REC_005', 'EMP_005', 'SKILL_005',
    'AWARD', '社内ハッカソン最優秀賞', '社内ハッカソンでAIを活用したアプリケーションで最優秀賞を受賞',
    'チームリーダーとして機械学習モデルの設計・実装を担当。ビジネス価値の高いソリューションを提案。',
    '/evidence/awards/hackathon_award_emp005.jpg', 'hackathon_award.jpg',
    5, 'VERIFIED', 'COMPANY', TRUE, 'user_005', 'user_005'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 運用開始時 |
| 月間増加件数 | 1,000件 | 社員500名×月2件の証跡追加 |
| 年間増加件数 | 12,000件 | 想定値 |
| 5年後想定件数 | 60,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から5年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | employee_id, is_active | 個人証跡取得 |
| SELECT | 高 | skill_item_id, verification_status | スキル別証跡取得 |
| SELECT | 中 | evidence_type, visibility | 種別・公開範囲検索 |
| SELECT | 中 | is_featured | 注目証跡取得 |
| INSERT | 中 | - | 新規証跡登録 |
| UPDATE | 中 | evidence_id | 証跡情報更新 |

### 7.2 パフォーマンス要件
- SELECT：30ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| skill_admin | ○ | ○ | ○ | × | スキル管理者 |
| manager | ○ | ○ | ○ | × | 管理職（部下のみ） |
| employee | ○ | ○ | ○ | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（証跡情報）
- 機密情報：含む（プロジェクト情報）
- 暗号化：ファイルパス、外部URL

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存証跡管理システム
- 移行方法：CSVインポート + ファイル移行
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE TRN_SkillEvidence (
    evidence_id VARCHAR(20) NOT NULL COMMENT '証跡ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    skill_record_id VARCHAR(20) NOT NULL COMMENT 'スキル記録ID',
    employee_id VARCHAR(20) NOT NULL COMMENT '社員ID',
    skill_item_id VARCHAR(20) NOT NULL COMMENT 'スキル項目ID',
    evidence_type VARCHAR(30) NOT NULL DEFAULT 'DOCUMENT' COMMENT '証跡種別',
    evidence_category VARCHAR(50) NULL COMMENT '証跡カテゴリ',
    evidence_title VARCHAR(200) NOT NULL COMMENT '証跡タイトル',
    evidence_description TEXT NULL COMMENT '証跡説明',
    file_path VARCHAR(500) NULL COMMENT 'ファイルパス',
    file_name VARCHAR(255) NULL COMMENT 'ファイル名',
    file_size BIGINT NULL COMMENT 'ファイルサイズ',
    file_type VARCHAR(50) NULL COMMENT 'ファイル種別',
    file_extension VARCHAR(10) NULL COMMENT 'ファイル拡張子',
    external_url VARCHAR(500) NULL COMMENT '外部URL',
    project_name VARCHAR(200) NULL COMMENT 'プロジェクト名',
    project_period VARCHAR(50) NULL COMMENT 'プロジェクト期間',
    role_in_project VARCHAR(100) NULL COMMENT 'プロジェクト内役割',
    technologies_used TEXT NULL COMMENT '使用技術',
    achievement_description TEXT NULL COMMENT '成果説明',
    certification_name VARCHAR(200) NULL COMMENT '資格名',
    certification_id_ref VARCHAR(20) NULL COMMENT '資格ID参照',
    certification_date DATE NULL COMMENT '資格取得日',
    certification_score INTEGER NULL COMMENT '資格スコア',
    certification_expiry DATE NULL COMMENT '資格有効期限',
    training_name VARCHAR(200) NULL COMMENT '研修名',
    training_provider VARCHAR(200) NULL COMMENT '研修提供者',
    training_completion_date DATE NULL COMMENT '研修修了日',
    training_hours INTEGER NULL COMMENT '研修時間',
    skill_level_demonstrated INTEGER NULL COMMENT '実証スキルレベル',
    verification_status VARCHAR(20) NOT NULL DEFAULT 'PENDING' COMMENT '検証ステータス',
    verified_by VARCHAR(20) NULL COMMENT '検証者ID',
    verified_date DATE NULL COMMENT '検証日',
    verification_comment TEXT NULL COMMENT '検証コメント',
    visibility VARCHAR(20) NOT NULL DEFAULT 'PRIVATE' COMMENT '公開範囲',
    tags TEXT NULL COMMENT 'タグ',
    is_featured BOOLEAN NOT NULL DEFAULT FALSE COMMENT '注目証跡フラグ',
    display_order INTEGER NOT NULL DEFAULT 0 COMMENT '表示順序',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (evidence_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_skill_record (skill_record_id),
    INDEX idx_employee (employee_id),
    INDEX idx_skill_item (skill_item_id),
    INDEX idx_evidence_type (evidence_type),
    INDEX idx_evidence_category (evidence_category),
    INDEX idx_verification_status (verification_status),
    INDEX idx_verified_by (verified_by),
    INDEX idx_visibility (visibility),
    INDEX idx_featured (is_featured),
    INDEX idx_active (is_active),
    INDEX idx_certification_ref (certification_id_ref),
    CONSTRAINT fk_skill_evidence_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_evidence_skill_record FOREIGN KEY (skill_record_id) REFERENCES TRN_SkillRecord(skill_record_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_evidence_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_evidence_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(skill_item_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_evidence_certification FOREIGN KEY (certification_id_ref) REFERENCES MST_Certification(certification_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_evidence_verified_by FOREIGN KEY (verified_by) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_evidence_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_evidence_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_evidence_type CHECK (evidence_type IN ('DOCUMENT', 'CERTIFICATION', 'PROJECT', 'PORTFOLIO', 'TRAINING', 'AWARD', 'PUBLICATION', 'PRESENTATION')),
    CONSTRAINT chk_skill_evidence_file_size CHECK (file_size IS NULL OR file_size > 0),
    CONSTRAINT chk_skill_evidence_skill_level CHECK (skill_level_demonstrated IS NULL OR (skill_level_demonstrated >= 1 AND skill_level_demonstrated <= 5)),
    CONSTRAINT chk_skill_evidence_verification_status CHECK (verification_status IN ('PENDING', 'VERIFIED', 'REJECTED')),
    CONSTRAINT chk_skill_evidence_visibility CHECK (visibility IN ('PRIVATE', 'TEAM', 'COMPANY', 'PUBLIC')),
    CONSTRAINT chk_skill_evidence_certification_score CHECK (certification_score IS NULL OR certification_score >= 0),
    CONSTRAINT chk_skill_evidence_training_hours CHECK (training_hours IS NULL OR training_hours > 0),
    CONSTRAINT chk_skill_evidence_display_order CHECK (display_order >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキル証跡';
```

## 10. 特記事項

1. **多様な証跡種別対応**
   - DOCUMENT（文書）、CERTIFICATION（資格）、PROJECT（プロジェクト）、PORTFOLIO（ポートフォリオ）、TRAINING（研修）、AWARD（受賞）、PUBLICATION（出版）、PRESENTATION（発表）
   - 幅広い証跡タイプを統一的に管理

2. **ファイル管理機能**
   - ファイル
