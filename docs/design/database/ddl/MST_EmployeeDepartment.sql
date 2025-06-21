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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_EmployeeDepartment;

CREATE TABLE MST_EmployeeDepartment (
    employee_id VARCHAR,
    department_id VARCHAR,
    assignment_type ENUM DEFAULT 'PRIMARY',
    start_date DATE,
    end_date DATE,
    assignment_ratio DECIMAL,
    role_in_department VARCHAR,
    reporting_manager_id VARCHAR,
    assignment_reason VARCHAR,
    assignment_status ENUM DEFAULT 'ACTIVE',
    approval_status ENUM DEFAULT 'PENDING',
    approved_by VARCHAR,
    approved_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_MST_EmployeeDepartment_employee_id ON MST_EmployeeDepartment (employee_id);
CREATE INDEX idx_MST_EmployeeDepartment_department_id ON MST_EmployeeDepartment (department_id);
CREATE INDEX idx_MST_EmployeeDepartment_employee_department ON MST_EmployeeDepartment (employee_id, department_id);
CREATE INDEX idx_MST_EmployeeDepartment_assignment_type ON MST_EmployeeDepartment (assignment_type);
CREATE INDEX idx_MST_EmployeeDepartment_start_date ON MST_EmployeeDepartment (start_date);
CREATE INDEX idx_MST_EmployeeDepartment_end_date ON MST_EmployeeDepartment (end_date);
CREATE INDEX idx_MST_EmployeeDepartment_status ON MST_EmployeeDepartment (assignment_status);
