-- ============================================
-- テーブル: MST_Department
-- 論理名: 部署マスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_Department;

CREATE TABLE MST_Department (
    department_code VARCHAR(20) COMMENT '部署を一意に識別するコード（例：DEPT001）',
    department_name VARCHAR(100) COMMENT '部署の正式名称',
    department_name_short VARCHAR(50) COMMENT '部署の略称・短縮名',
    parent_department_id VARCHAR(50) COMMENT '上位部署のID（MST_Departmentへの自己参照外部キー）',
    department_level INT COMMENT '組織階層のレベル（1:本部、2:部、3:課、4:チーム等）',
    department_type ENUM COMMENT '部署の種別（HEADQUARTERS:本部、DIVISION:事業部、DEPARTMENT:部、SECTION:課、TEAM:チーム）',
    manager_id VARCHAR(50) COMMENT '部署長の社員ID（MST_Employeeへの外部キー）',
    deputy_manager_id VARCHAR(50) COMMENT '副部署長の社員ID（MST_Employeeへの外部キー）',
    cost_center_code VARCHAR(20) COMMENT '予算管理用のコストセンターコード',
    budget_amount DECIMAL(15,2) COMMENT '年間予算額（円）',
    location VARCHAR(200) COMMENT '部署の物理的な所在地・フロア等',
    phone_number VARCHAR(20) COMMENT '部署の代表電話番号',
    email_address VARCHAR(255) COMMENT '部署の代表メールアドレス',
    establishment_date DATE COMMENT '部署の設立・新設日',
    abolition_date DATE COMMENT '部署の廃止・統合日',
    department_status ENUM DEFAULT 'ACTIVE' COMMENT '部署の状態（ACTIVE:有効、INACTIVE:無効、MERGED:統合、ABOLISHED:廃止）',
    sort_order INT COMMENT '組織図等での表示順序',
    description TEXT COMMENT '部署の役割・業務内容の説明',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_department_code ON MST_Department (department_code);
CREATE INDEX idx_parent_department ON MST_Department (parent_department_id);
CREATE INDEX idx_department_level ON MST_Department (department_level);
CREATE INDEX idx_department_type ON MST_Department (department_type);
CREATE INDEX idx_manager ON MST_Department (manager_id);
CREATE INDEX idx_status ON MST_Department (department_status);
CREATE INDEX idx_cost_center ON MST_Department (cost_center_code);
CREATE INDEX idx_sort_order ON MST_Department (sort_order);

-- 外部キー制約
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent FOREIGN KEY (parent_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy FOREIGN KEY (deputy_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_Department ADD CONSTRAINT uk_department_code UNIQUE ();
ALTER TABLE MST_Department ADD CONSTRAINT chk_department_level CHECK (department_level > 0);
ALTER TABLE MST_Department ADD CONSTRAINT chk_department_type CHECK (department_type IN ('HEADQUARTERS', 'DIVISION', 'DEPARTMENT', 'SECTION', 'TEAM'));
ALTER TABLE MST_Department ADD CONSTRAINT chk_department_status CHECK (department_status IN ('ACTIVE', 'INACTIVE', 'MERGED', 'ABOLISHED'));
ALTER TABLE MST_Department ADD CONSTRAINT chk_budget_amount CHECK (budget_amount IS NULL OR budget_amount >= 0);
ALTER TABLE MST_Department ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
