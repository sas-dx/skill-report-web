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

-- 作成日: 2025-06-24 23:05:58
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeDepartment;

CREATE TABLE MST_EmployeeDepartment (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    approval_status ENUM('APPROVED', 'PENDING', 'REJECTED') DEFAULT 'PENDING' COMMENT '承認状況',
    approved_at TIMESTAMP COMMENT '承認日時',
    approved_by VARCHAR(50) COMMENT '承認者ID',
    assignment_ratio DECIMAL(5,2) COMMENT '配属比率',
    assignment_reason VARCHAR(500) COMMENT '配属理由',
    assignment_status ENUM('ACTIVE', 'INACTIVE', 'PENDING') DEFAULT 'ACTIVE' COMMENT '配属状況',
    assignment_type ENUM('PRIMARY', 'SECONDARY', 'TEMPORARY') DEFAULT 'PRIMARY' COMMENT '配属区分',
    department_id VARCHAR(50) COMMENT '部署ID',
    employee_id VARCHAR(50) COMMENT '社員ID',
    employeedepartment_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_EmployeeDepartmentの主キー',
    end_date DATE COMMENT '配属終了日',
    reporting_manager_id VARCHAR(50) COMMENT '報告先上司ID',
    role_in_department VARCHAR(100) COMMENT '部署内役割',
    start_date DATE COMMENT '配属開始日',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_MST_EmployeeDepartment_employee_id ON MST_EmployeeDepartment (employee_id);
CREATE INDEX idx_MST_EmployeeDepartment_department_id ON MST_EmployeeDepartment (department_id);
CREATE INDEX idx_MST_EmployeeDepartment_employee_department ON MST_EmployeeDepartment (employee_id, department_id);
CREATE INDEX idx_MST_EmployeeDepartment_assignment_type ON MST_EmployeeDepartment (assignment_type);
CREATE INDEX idx_MST_EmployeeDepartment_start_date ON MST_EmployeeDepartment (start_date);
CREATE INDEX idx_MST_EmployeeDepartment_end_date ON MST_EmployeeDepartment (end_date);
CREATE INDEX idx_MST_EmployeeDepartment_status ON MST_EmployeeDepartment (assignment_status);
CREATE INDEX idx_mst_employeedepartment_tenant_id ON MST_EmployeeDepartment (tenant_id);

-- 外部キー制約
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_department FOREIGN KEY (department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager FOREIGN KEY (reporting_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_MST_EmployeeDepartment_employee_dept_primary
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_assignment_type CHECK (assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY'));
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_assignment_status CHECK (assignment_status IN ('ACTIVE', 'INACTIVE', 'PENDING'));
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_approval_status CHECK (approval_status IN ('APPROVED', 'PENDING', 'REJECTED'));
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT chk_MST_EmployeeDepartment_assignment_ratio CHECK (assignment_ratio IS NULL OR (assignment_ratio >= 0 AND assignment_ratio <= 100));
