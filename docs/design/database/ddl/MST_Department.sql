-- ============================================
-- テーブル: MST_Department
-- 論理名: 部署マスタ
-- 説明: MST_Department（部署マスタ）は、組織の部署・組織単位の階層構造と基本情報を管理するマスタテーブルです。

主な目的：
- 組織階層の構造管理（部署、課、チーム等の階層関係）
- 部署基本情報の管理（部署名、部署コード、責任者等）
- 組織変更履歴の管理（統廃合、新設、移管等）
- 予算・コスト管理の組織単位設定
- 権限・アクセス制御の組織単位設定
- 人事異動・配置管理の基盤
- 組織図・レポート作成の基礎データ

このテーブルは、人事管理、権限管理、予算管理、レポート作成など、
組織運営の様々な業務プロセスの基盤となる重要なマスタデータです。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS MST_Department;

CREATE TABLE MST_Department (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    abolition_date DATE COMMENT '廃止日',
    budget_amount DECIMAL(15,2) COMMENT '予算額',
    cost_center_code VARCHAR(20) COMMENT 'コストセンターコード',
    department_code VARCHAR(20) COMMENT '部署コード',
    department_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_Departmentの主キー',
    department_level INT COMMENT '部署レベル',
    department_name VARCHAR(100) COMMENT '部署名',
    department_name_short VARCHAR(50) COMMENT '部署名略称',
    department_status ENUM('ACTIVE', 'INACTIVE', 'MERGED', 'ABOLISHED') DEFAULT 'ACTIVE' COMMENT '部署状態',
    department_type ENUM('HEADQUARTERS', 'DIVISION', 'DEPARTMENT', 'SECTION', 'TEAM') COMMENT '部署種別',
    deputy_manager_id VARCHAR(50) COMMENT '副部署長ID',
    description TEXT COMMENT '部署説明',
    email_address VARCHAR(255) COMMENT '代表メールアドレス',
    establishment_date DATE COMMENT '設立日',
    location VARCHAR(200) COMMENT '所在地',
    manager_id VARCHAR(50) COMMENT '部署長ID',
    parent_department_id VARCHAR(50) COMMENT '親部署ID',
    phone_number VARCHAR(20) COMMENT '代表電話番号',
    sort_order INT COMMENT '表示順序',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_department_tenant_id ON MST_Department (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent FOREIGN KEY (parent_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy FOREIGN KEY (deputy_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_department_code
ALTER TABLE MST_Department ADD CONSTRAINT chk_department_level CHECK (department_level > 0);
ALTER TABLE MST_Department ADD CONSTRAINT chk_department_type CHECK (department_type IN ('HEADQUARTERS', 'DIVISION', 'DEPARTMENT', 'SECTION', 'TEAM'));
ALTER TABLE MST_Department ADD CONSTRAINT chk_department_status CHECK (department_status IN ('ACTIVE', 'INACTIVE', 'MERGED', 'ABOLISHED'));
ALTER TABLE MST_Department ADD CONSTRAINT chk_budget_amount CHECK (budget_amount IS NULL OR budget_amount >= 0);
ALTER TABLE MST_Department ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
