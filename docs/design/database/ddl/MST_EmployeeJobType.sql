-- ============================================
-- テーブル: MST_EmployeeJobType
-- 論理名: 社員職種関連
-- 説明: MST_EmployeeJobType（社員職種関連）は、社員と職種の関連付けを管理するマスタテーブルです。

主な目的：
- 社員の職種履歴管理
- 複数職種対応（兼任・転職）
- 職種変更の追跡
- 人材配置の最適化
- スキル要件との連携

このテーブルにより、社員の職種変遷を正確に管理し、
適切な人材配置とキャリア開発を支援できます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeJobType;

CREATE TABLE MST_EmployeeJobType (
    employeejobtype_id SERIAL NOT NULL COMMENT 'MST_EmployeeJobTypeの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (employeejobtype_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_employeejobtype_tenant_id ON MST_EmployeeJobType (tenant_id);

-- 外部キー制約
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_job_type FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_created_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
