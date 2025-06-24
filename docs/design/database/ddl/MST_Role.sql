-- ============================================
-- テーブル: MST_Role
-- 論理名: ロール情報
-- 説明: MST_Role（ロール情報）は、システム内のロール（役割）を管理するマスタテーブルです。

主な目的：
- システム内のロール定義・管理（管理者、一般ユーザー、閲覧者等）
- ロール階層の管理（上位ロール、下位ロール）
- ロール別権限設定の基盤
- 職務分離・最小権限の原則実装
- 動的権限管理・ロールベースアクセス制御（RBAC）
- 組織変更に対応した柔軟な権限管理
- 監査・コンプライアンス対応

このテーブルは、システムセキュリティの基盤となり、
適切なアクセス制御と権限管理を実現する重要なマスタデータです。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS MST_Role;

CREATE TABLE MST_Role (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    auto_assign_conditions JSON COMMENT '自動割り当て条件',
    description TEXT COMMENT 'ロール説明',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    is_system_role BOOLEAN DEFAULT False COMMENT 'システムロールフラグ',
    is_tenant_specific BOOLEAN DEFAULT False COMMENT 'テナント固有フラグ',
    max_users INT COMMENT '最大ユーザー数',
    parent_role_id VARCHAR(50) COMMENT '親ロールID',
    role_category ENUM('SYSTEM', 'BUSINESS', 'TENANT', 'CUSTOM') COMMENT 'ロールカテゴリ',
    role_code VARCHAR(20) COMMENT 'ロールコード',
    role_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_Roleの主キー',
    role_level INT COMMENT 'ロールレベル',
    role_name VARCHAR(100) COMMENT 'ロール名',
    role_name_short VARCHAR(50) COMMENT 'ロール名略称',
    role_priority INT DEFAULT 999 COMMENT 'ロール優先度',
    role_status ENUM('ACTIVE', 'INACTIVE', 'DEPRECATED') DEFAULT 'ACTIVE' COMMENT 'ロール状態',
    sort_order INT COMMENT '表示順序',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_role_code ON MST_Role (role_code);
CREATE INDEX idx_role_category ON MST_Role (role_category);
CREATE INDEX idx_role_level ON MST_Role (role_level);
CREATE INDEX idx_parent_role ON MST_Role (parent_role_id);
CREATE INDEX idx_system_role ON MST_Role (is_system_role);
CREATE INDEX idx_tenant_specific ON MST_Role (is_tenant_specific);
CREATE INDEX idx_role_status ON MST_Role (role_status);
CREATE INDEX idx_effective_period ON MST_Role (effective_from, effective_to);
CREATE INDEX idx_sort_order ON MST_Role (sort_order);
CREATE INDEX idx_mst_role_tenant_id ON MST_Role (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Role ADD CONSTRAINT fk_role_parent FOREIGN KEY (parent_role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_role_code
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_level CHECK (role_level > 0);
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_category CHECK (role_category IN ('SYSTEM', 'BUSINESS', 'TENANT', 'CUSTOM'));
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_status CHECK (role_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED'));
ALTER TABLE MST_Role ADD CONSTRAINT chk_max_users CHECK (max_users IS NULL OR max_users > 0);
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_priority CHECK (role_priority > 0);
ALTER TABLE MST_Role ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to);
ALTER TABLE MST_Role ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
