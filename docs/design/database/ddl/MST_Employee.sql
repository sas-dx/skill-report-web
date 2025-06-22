-- ============================================
-- テーブル: MST_Employee
-- 論理名: 社員基本情報
-- 説明: 組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブル
-- 作成日: 2025-06-21 23:07:48
-- ============================================

DROP TABLE IF EXISTS MST_Employee;

CREATE TABLE MST_Employee (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    employee_code VARCHAR(30) NOT NULL COMMENT '社員番号（例：EMP000001）',
    full_name VARCHAR(100) NOT NULL COMMENT '氏名（暗号化対象）',
    full_name_kana VARCHAR(100) NOT NULL COMMENT '氏名カナ（暗号化対象）',
    email VARCHAR(255) NOT NULL COMMENT 'メールアドレス（ログイン認証用）',
    phone VARCHAR(20) COMMENT '電話番号（暗号化対象）',
    hire_date DATE NOT NULL COMMENT '入社日',
    birth_date DATE COMMENT '生年月日（暗号化対象）',
    gender VARCHAR(1) COMMENT '性別（M:男性、F:女性、O:その他）',
    department_id VARCHAR(50) NOT NULL COMMENT '所属部署ID',
    position_id VARCHAR(50) COMMENT '役職ID',
    job_type_id VARCHAR(50) COMMENT '職種ID',
    employment_status VARCHAR(20) NOT NULL DEFAULT 'FULL_TIME' COMMENT '雇用形態（FULL_TIME:正社員、PART_TIME:パート、CONTRACT:契約社員）',
    manager_id VARCHAR(50) COMMENT '直属の上司ID（自己参照）',
    employee_status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE' COMMENT '在籍状況（ACTIVE:在籍、RETIRED:退職、SUSPENDED:休職）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_employee_code ON MST_Employee (employee_code);
CREATE UNIQUE INDEX idx_email ON MST_Employee (email);
CREATE INDEX idx_department ON MST_Employee (department_id);
CREATE INDEX idx_manager ON MST_Employee (manager_id);
CREATE INDEX idx_status ON MST_Employee (employee_status);
CREATE INDEX idx_hire_date ON MST_Employee (hire_date);

-- 外部キー制約
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_department FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
