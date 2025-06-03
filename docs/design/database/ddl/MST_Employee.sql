-- ============================================
-- テーブル: MST_Employee
-- 論理名: 社員基本情報
-- 説明: 
-- 作成日: 2025-06-04 06:46:06
-- ============================================

DROP TABLE IF EXISTS MST_Employee;

CREATE TABLE MST_Employee (
    employee_code VARCHAR(30) COMMENT '社員を一意に識別する番号（例：EMP000001、現行システムからの移行番号も対応）',
    full_name VARCHAR(100) COMMENT '社員の氏名（個人情報のため暗号化対象）',
    full_name_kana VARCHAR(100) COMMENT '社員の氏名カナ（個人情報のため暗号化対象）',
    email VARCHAR(255) COMMENT '社員のメールアドレス（ログイン認証に使用）',
    phone VARCHAR(20) COMMENT '社員の電話番号（個人情報のため暗号化対象）',
    hire_date DATE COMMENT '社員の入社日',
    birth_date DATE COMMENT '社員の生年月日（個人情報のため暗号化対象）',
    gender ENUM COMMENT '性別（M:男性、F:女性、O:その他）',
    department_id VARCHAR(50) COMMENT '所属部署のID（MST_Departmentへの外部キー）',
    position_id VARCHAR(50) COMMENT '役職のID（MST_Positionへの外部キー）',
    job_type_id VARCHAR(50) COMMENT '職種のID（MST_JobTypeへの外部キー）',
    employment_status ENUM DEFAULT 'FULL_TIME' COMMENT '雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員）',
    manager_id VARCHAR(50) COMMENT '直属の上司のID（MST_Employeeへの自己参照外部キー）',
    employee_status ENUM DEFAULT 'ACTIVE' COMMENT '在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職）',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
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

-- その他の制約
ALTER TABLE MST_Employee ADD CONSTRAINT uk_employee_code UNIQUE ();
ALTER TABLE MST_Employee ADD CONSTRAINT uk_email UNIQUE ();
ALTER TABLE MST_Employee ADD CONSTRAINT chk_gender CHECK (gender IN ('M', 'F', 'O'));
ALTER TABLE MST_Employee ADD CONSTRAINT chk_employment_status CHECK (employment_status IN ('FULL_TIME', 'PART_TIME', 'CONTRACT'));
ALTER TABLE MST_Employee ADD CONSTRAINT chk_employee_status CHECK (employee_status IN ('ACTIVE', 'RETIRED', 'SUSPENDED'));
