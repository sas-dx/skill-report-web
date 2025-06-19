-- MST_Employee (社員基本情報)
-- 生成日時: 2025-06-11 01:49:39
-- カテゴリ: マスタ系
-- 要求仕様ID: PRO.1-BASE.1

CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL,
    employee_code VARCHAR(30) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    full_name_kana VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    hire_date DATE NOT NULL,
    birth_date DATE,
    gender VARCHAR(1),
    department_id VARCHAR(50) NOT NULL,
    position_id VARCHAR(50),
    job_type_id VARCHAR(50),
    employment_status VARCHAR(20) NOT NULL DEFAULT 'FULL_TIME',
    manager_id VARCHAR(50),
    employee_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN NOT NULL,
    PRIMARY KEY (id)
);

-- インデックス作成
CREATE UNIQUE INDEX idx_employee_code ON MST_Employee (employee_code); -- 社員番号検索用（一意）
CREATE UNIQUE INDEX idx_email ON MST_Employee (email); -- メールアドレス検索用（一意）
CREATE INDEX idx_department ON MST_Employee (department_id); -- 部署別検索用
CREATE INDEX idx_manager ON MST_Employee (manager_id); -- 上司別検索用
CREATE INDEX idx_status ON MST_Employee (employee_status); -- 在籍状況別検索用
CREATE INDEX idx_hire_date ON MST_Employee (hire_date); -- 入社日検索用

-- 外部キー制約
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_department FOREIGN KEY (department_id) REFERENCES MST_Department (id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position FOREIGN KEY (position_id) REFERENCES MST_Position (id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type FOREIGN KEY (job_type_id) REFERENCES MST_JobType (id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee (id) ON UPDATE CASCADE ON DELETE SET NULL;

COMMENT ON TABLE MST_Employee IS '社員基本情報';

COMMENT ON COLUMN MST_Employee.id IS 'プライマリキー（UUID）';
COMMENT ON COLUMN MST_Employee.employee_code IS '社員番号（例：EMP000001）';
COMMENT ON COLUMN MST_Employee.full_name IS '氏名（暗号化対象）';
COMMENT ON COLUMN MST_Employee.full_name_kana IS '氏名カナ（暗号化対象）';
COMMENT ON COLUMN MST_Employee.email IS 'メールアドレス（ログイン認証用）';
COMMENT ON COLUMN MST_Employee.phone IS '電話番号（暗号化対象）';
COMMENT ON COLUMN MST_Employee.hire_date IS '入社日';
COMMENT ON COLUMN MST_Employee.birth_date IS '生年月日（暗号化対象）';
COMMENT ON COLUMN MST_Employee.gender IS '性別（M:男性、F:女性、O:その他）';
COMMENT ON COLUMN MST_Employee.department_id IS '所属部署ID';
COMMENT ON COLUMN MST_Employee.position_id IS '役職ID';
COMMENT ON COLUMN MST_Employee.job_type_id IS '職種ID';
COMMENT ON COLUMN MST_Employee.employment_status IS '雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員）';
COMMENT ON COLUMN MST_Employee.manager_id IS '直属の上司ID（自己参照）';
COMMENT ON COLUMN MST_Employee.employee_status IS '在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職）';
COMMENT ON COLUMN MST_Employee.created_at IS '作成日時';
COMMENT ON COLUMN MST_Employee.updated_at IS '更新日時';
COMMENT ON COLUMN MST_Employee.is_deleted IS '論理削除フラグ';
