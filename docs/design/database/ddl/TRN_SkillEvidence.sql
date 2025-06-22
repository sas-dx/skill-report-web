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

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS TRN_SkillEvidence;

CREATE TABLE TRN_SkillEvidence (
    skillevidence_id SERIAL NOT NULL COMMENT 'TRN_SkillEvidenceの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (skillevidence_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_skillevidence_tenant_id ON TRN_SkillEvidence (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_skill FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_project FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_training FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
