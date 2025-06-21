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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS TRN_SkillEvidence;

CREATE TABLE TRN_SkillEvidence (
    evidence_id VARCHAR,
    employee_id VARCHAR,
    skill_id VARCHAR,
    evidence_type ENUM,
    evidence_title VARCHAR,
    evidence_description TEXT,
    skill_level_demonstrated ENUM,
    evidence_date DATE,
    validity_start_date DATE,
    validity_end_date DATE,
    file_path VARCHAR,
    file_type ENUM,
    file_size_kb INTEGER,
    external_url VARCHAR,
    issuer_name VARCHAR,
    issuer_type ENUM,
    certificate_number VARCHAR,
    verification_method ENUM,
    verification_status ENUM DEFAULT 'PENDING',
    verified_by VARCHAR,
    verification_date DATE,
    verification_comment TEXT,
    related_project_id VARCHAR,
    related_training_id VARCHAR,
    related_certification_id VARCHAR,
    impact_score DECIMAL,
    complexity_level ENUM,
    team_size INTEGER,
    role_in_activity VARCHAR,
    technologies_used TEXT,
    achievements TEXT,
    lessons_learned TEXT,
    is_public BOOLEAN DEFAULT False,
    is_portfolio_item BOOLEAN DEFAULT False,
    tags TEXT,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時',
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
