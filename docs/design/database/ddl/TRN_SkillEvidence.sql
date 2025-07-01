-- ============================================
-- テーブル: TRN_SkillEvidence
-- 論理名: スキル証跡
-- 説明: TRN_SkillEvidence（スキル証跡）は、社員のスキル習得・向上を証明する具体的な証跡情報を管理するトランザクションテーブルです。

主な目的：
- スキル習得の客観的証拠の記録
- 成果物・実績による能力証明
- スキル評価の根拠データ提供
- ポートフォリオ作成支援
- 人事評価・昇進判定の材料提供

このテーブルにより、社員のスキルを定性的・定量的に証明し、
適切な人材配置や能力開発の判断を支援できます。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS TRN_SkillEvidence;

CREATE TABLE TRN_SkillEvidence (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    achievements TEXT COMMENT '成果・実績',
    certificate_number VARCHAR(100) COMMENT '証明書番号',
    complexity_level ENUM('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH') COMMENT '複雑度レベル',
    employee_id VARCHAR(50) COMMENT '社員ID',
    evidence_date DATE COMMENT '証跡日付',
    evidence_description TEXT COMMENT '証跡説明',
    evidence_id VARCHAR(50) COMMENT '証跡ID',
    evidence_title VARCHAR(200) COMMENT '証跡タイトル',
    evidence_type ENUM('CERTIFICATION', 'PROJECT', 'TRAINING', 'PORTFOLIO', 'PEER_REVIEW', 'SELF_ASSESSMENT', 'OTHER') COMMENT '証跡種別',
    external_url VARCHAR(500) COMMENT '外部URL',
    file_path VARCHAR(500) COMMENT 'ファイルパス',
    file_size_kb INTEGER COMMENT 'ファイルサイズ',
    file_type ENUM('PDF', 'IMAGE', 'VIDEO', 'DOCUMENT', 'URL', 'OTHER') COMMENT 'ファイル種別',
    impact_score DECIMAL(3,1) COMMENT '影響度スコア',
    is_portfolio_item BOOLEAN DEFAULT False COMMENT 'ポートフォリオ項目フラグ',
    is_public BOOLEAN DEFAULT False COMMENT '公開フラグ',
    issuer_name VARCHAR(100) COMMENT '発行者名',
    issuer_type ENUM('COMPANY', 'EDUCATIONAL', 'CERTIFICATION_BODY', 'GOVERNMENT', 'COMMUNITY', 'OTHER') COMMENT '発行者種別',
    lessons_learned TEXT COMMENT '学んだこと',
    related_certification_id VARCHAR(50) COMMENT '関連資格ID',
    related_project_id VARCHAR(50) COMMENT '関連案件ID',
    related_training_id VARCHAR(50) COMMENT '関連研修ID',
    role_in_activity VARCHAR(100) COMMENT '活動での役割',
    skill_id VARCHAR(50) COMMENT 'スキルID',
    skill_level_demonstrated ENUM('BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'EXPERT') COMMENT '実証スキルレベル',
    skillevidence_id INT AUTO_INCREMENT NOT NULL COMMENT 'TRN_SkillEvidenceの主キー',
    tags TEXT COMMENT 'タグ',
    team_size INTEGER COMMENT 'チーム規模',
    technologies_used TEXT COMMENT '使用技術',
    validity_end_date DATE COMMENT '有効終了日',
    validity_start_date DATE COMMENT '有効開始日',
    verification_comment TEXT COMMENT '検証コメント',
    verification_date DATE COMMENT '検証日',
    verification_method ENUM('AUTOMATIC', 'MANUAL', 'PEER', 'MANAGER', 'EXTERNAL') COMMENT '検証方法',
    verification_status ENUM('PENDING', 'VERIFIED', 'REJECTED', 'EXPIRED') DEFAULT 'PENDING' COMMENT '検証状況',
    verified_by VARCHAR(50) COMMENT '検証者',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_trn_skillevidence_tenant_id ON TRN_SkillEvidence (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier FOREIGN KEY (verified_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification FOREIGN KEY (related_certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_evidence_id
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
