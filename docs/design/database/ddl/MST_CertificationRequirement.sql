-- ============================================
-- テーブル: MST_CertificationRequirement
-- 論理名: 資格要件マスタ
-- 説明: MST_CertificationRequirement（資格要件マスタ）は、職種・役職・スキルレベルに応じた資格要件を管理するマスタテーブルです。

主な目的：
- 職種別必要資格の定義
- 昇進・昇格要件の管理
- スキルレベル認定基準の設定
- 人材配置判定の支援
- キャリア開発ガイドラインの提供

このテーブルにより、組織の人材要件を明確化し、
適切な人材配置と計画的な人材育成を実現できます。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_CertificationRequirement;

CREATE TABLE MST_CertificationRequirement (
    certificationrequirement_id SERIAL NOT NULL COMMENT 'MST_CertificationRequirementの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (certificationrequirement_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_certificationrequirement_tenant_id ON MST_CertificationRequirement (tenant_id);

-- 外部キー制約
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_certification FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_created_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
