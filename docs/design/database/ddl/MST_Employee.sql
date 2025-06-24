-- ============================================
-- テーブル: MST_Employee
-- 論理名: 社員基本情報
-- 説明: 組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブル。

主な目的：
- 社員の基本情報（氏名、連絡先、入社日等）の管理
- 組織構造（部署、役職、上司関係）の管理
- 認証・権限管理のためのユーザー情報提供
- 人事システムとの連携データ基盤

このテーブルは年間スキル報告書システムの中核となるマスタデータであり、
スキル管理、目標管理、作業実績管理の全ての機能で参照される。

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS MST_Employee;

CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    employee_code VARCHAR(30) NOT NULL COMMENT '社員番号（例：EMP000001）',
    full_name VARCHAR(100) NOT NULL COMMENT '氏名（暗号化対象）',
    full_name_kana VARCHAR(100) NOT NULL COMMENT '氏名カナ（暗号化対象）',
    email VARCHAR(255) NOT NULL COMMENT 'メールアドレス（ログイン認証用）',
    phone VARCHAR(20) COMMENT '電話番号（暗号化対象）',
    birth_date DATE COMMENT '生年月日（暗号化対象）',
    gender VARCHAR(1) COMMENT '性別（M:男性、F:女性、O:その他）',
    hire_date DATE NOT NULL COMMENT '入社日',
    department_id VARCHAR(50) NOT NULL COMMENT '所属部署ID',
    position_id VARCHAR(50) COMMENT '役職ID',
    job_type_id VARCHAR(50) COMMENT '職種ID',
    manager_id VARCHAR(50) COMMENT '直属の上司ID（自己参照）',
    employment_status VARCHAR(20) NOT NULL DEFAULT 'FULL_TIME' COMMENT '雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員）',
    employee_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' COMMENT '在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_employee_code ON MST_Employee (employee_code);
CREATE UNIQUE INDEX idx_email ON MST_Employee (email);
CREATE INDEX idx_department ON MST_Employee (department_id);
CREATE INDEX idx_manager ON MST_Employee (manager_id);
CREATE INDEX idx_status ON MST_Employee (employee_status);
CREATE INDEX idx_hire_date ON MST_Employee (hire_date);

-- 外部キー制約
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position FOREIGN KEY (position_id) REFERENCES MST_Position(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
