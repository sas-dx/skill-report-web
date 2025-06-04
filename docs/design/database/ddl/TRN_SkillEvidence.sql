-- ============================================
-- テーブル: TRN_SkillEvidence
-- 論理名: スキル証跡
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_SkillEvidence;

CREATE TABLE TRN_SkillEvidence (
    evidence_id VARCHAR(50) COMMENT 'スキル証跡を一意に識別するID',
    employee_id VARCHAR(50) COMMENT '証跡の対象社員ID（MST_Employeeへの外部キー）',
    skill_id VARCHAR(50) COMMENT '証明対象のスキルID（MST_SkillItemへの外部キー）',
    evidence_type ENUM COMMENT '証跡の種別（CERTIFICATION:資格、PROJECT:プロジェクト成果、TRAINING:研修修了、PORTFOLIO:ポートフォリオ、PEER_REVIEW:同僚評価、SELF_ASSESSMENT:自己評価、OTHER:その他）',
    evidence_title VARCHAR(200) COMMENT '証跡の名称・タイトル',
    evidence_description TEXT COMMENT '証跡の詳細説明・内容',
    skill_level_demonstrated ENUM COMMENT '証跡により実証されるスキルレベル（BEGINNER:初級、INTERMEDIATE:中級、ADVANCED:上級、EXPERT:エキスパート）',
    evidence_date DATE COMMENT '証跡が作成・取得された日付',
    validity_start_date DATE COMMENT '証跡の有効期間開始日',
    validity_end_date DATE COMMENT '証跡の有効期間終了日（無期限の場合はNULL）',
    file_path VARCHAR(500) COMMENT '証跡ファイルの保存パス',
    file_type ENUM COMMENT '証跡ファイルの種別（PDF:PDF、IMAGE:画像、VIDEO:動画、DOCUMENT:文書、URL:URL、OTHER:その他）',
    file_size_kb INTEGER COMMENT 'ファイルサイズ（KB）',
    external_url VARCHAR(500) COMMENT '外部サイトの証跡URL（GitHub、Qiita等）',
    issuer_name VARCHAR(100) COMMENT '証跡を発行した機関・組織名',
    issuer_type ENUM COMMENT '発行者の種別（COMPANY:会社、EDUCATIONAL:教育機関、CERTIFICATION_BODY:認定機関、GOVERNMENT:政府機関、COMMUNITY:コミュニティ、OTHER:その他）',
    certificate_number VARCHAR(100) COMMENT '資格証明書・修了証の番号',
    verification_method ENUM COMMENT '証跡の検証方法（AUTOMATIC:自動、MANUAL:手動、PEER:同僚、MANAGER:上司、EXTERNAL:外部機関）',
    verification_status ENUM DEFAULT 'PENDING' COMMENT '証跡の検証状況（PENDING:検証待ち、VERIFIED:検証済み、REJECTED:却下、EXPIRED:期限切れ）',
    verified_by VARCHAR(50) COMMENT '証跡を検証した担当者のID',
    verification_date DATE COMMENT '証跡が検証された日付',
    verification_comment TEXT COMMENT '検証時のコメント・備考',
    related_project_id VARCHAR(50) COMMENT '関連するプロジェクトのID（TRN_ProjectRecordへの外部キー）',
    related_training_id VARCHAR(50) COMMENT '関連する研修のID（TRN_TrainingHistoryへの外部キー）',
    related_certification_id VARCHAR(50) COMMENT '関連する資格のID（MST_Certificationへの外部キー）',
    impact_score DECIMAL(3,1) COMMENT '証跡の影響度・重要度スコア（1.0-5.0）',
    complexity_level ENUM COMMENT '証跡が示す作業の複雑度（LOW:低、MEDIUM:中、HIGH:高、VERY_HIGH:非常に高い）',
    team_size INTEGER COMMENT '関連プロジェクトのチーム規模',
    role_in_activity VARCHAR(100) COMMENT '証跡となる活動での担当役割',
    technologies_used TEXT COMMENT '証跡に関連する使用技術（JSON形式）',
    achievements TEXT COMMENT '具体的な成果・実績',
    lessons_learned TEXT COMMENT '活動から学んだ知識・経験',
    is_public BOOLEAN DEFAULT False COMMENT '証跡を社外に公開可能かどうか',
    is_portfolio_item BOOLEAN DEFAULT False COMMENT 'ポートフォリオに含める項目かどうか',
    tags TEXT COMMENT '検索・分類用のタグ（JSON形式）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'マルチテナント識別子',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP' COMMENT 'レコード更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_evidence_id ON TRN_SkillEvidence (evidence_id);
CREATE INDEX idx_employee_id ON TRN_SkillEvidence (employee_id);
CREATE INDEX idx_skill_id ON TRN_SkillEvidence (skill_id);
CREATE INDEX idx_evidence_type ON TRN_SkillEvidence (evidence_type);
CREATE INDEX idx_skill_level ON TRN_SkillEvidence (skill_level_demonstrated);
CREATE INDEX idx_evidence_date ON TRN_SkillEvidence (evidence_date);
CREATE INDEX idx_verification_status ON TRN_SkillEvidence (verification_status);
CREATE INDEX idx_validity_period ON TRN_SkillEvidence (validity_start_date, validity_end_date);
CREATE INDEX idx_employee_skill ON TRN_SkillEvidence (employee_id, skill_id, verification_status);
CREATE INDEX idx_portfolio ON TRN_SkillEvidence (is_portfolio_item, is_public);

-- 外部キー制約
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier FOREIGN KEY (verified_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(project_record_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(training_history_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification FOREIGN KEY (related_certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT uk_evidence_id UNIQUE ();
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_evidence_type CHECK (evidence_type IN ('CERTIFICATION', 'PROJECT', 'TRAINING', 'PORTFOLIO', 'PEER_REVIEW', 'SELF_ASSESSMENT', 'OTHER'));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_skill_level CHECK (skill_level_demonstrated IN ('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT'));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_file_type CHECK (file_type IN ('PDF', 'IMAGE', 'VIDEO', 'DOCUMENT', 'URL', 'OTHER'));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_issuer_type CHECK (issuer_type IN ('COMPANY', 'EDUCATIONAL', 'CERTIFICATION_BODY', 'GOVERNMENT', 'COMMUNITY', 'OTHER'));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_verification_method CHECK (verification_method IN ('AUTOMATIC', 'MANUAL', 'PEER', 'MANAGER', 'EXTERNAL'));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_verification_status CHECK (verification_status IN ('PENDING', 'VERIFIED', 'REJECTED', 'EXPIRED'));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_complexity_level CHECK (complexity_level IN ('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_validity_period CHECK (validity_end_date IS NULL OR validity_start_date <= validity_end_date);
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_impact_score CHECK (impact_score IS NULL OR (impact_score >= 1.0 AND impact_score <= 5.0));
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_file_size CHECK (file_size_kb IS NULL OR file_size_kb > 0);
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT chk_team_size CHECK (team_size IS NULL OR team_size > 0);
