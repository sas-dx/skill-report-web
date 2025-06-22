-- ============================================
-- テーブル: MST_EmployeeDepartment
-- 論理名: 社員部署関連
-- 説明: MST_EmployeeDepartment（社員部署関連）は、社員と部署の関連付けを管理するマスタテーブルです。

主な目的：
- 社員の部署所属履歴の管理
- 複数部署兼務の管理
- 部署異動履歴の追跡
- 組織変更時の影響範囲把握
- 部署別人員配置の管理
- 権限管理における部署ベースアクセス制御

このテーブルにより、社員の組織所属状況を詳細に管理し、
人事異動や組織変更の履歴を正確に追跡できます。

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeDepartment;

CREATE TABLE MST_EmployeeDepartment (
    employeedepartment_id SERIAL NOT NULL COMMENT 'MST_EmployeeDepartmentの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (employeedepartment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_employeedepartment_tenant_id ON MST_EmployeeDepartment (tenant_id);

-- 外部キー制約
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_department FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
