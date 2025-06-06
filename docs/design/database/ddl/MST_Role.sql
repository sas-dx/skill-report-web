-- ============================================
-- テーブル: MST_Role
-- 論理名: ロール情報
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_Role;

CREATE TABLE MST_Role (
    role_code VARCHAR(20) COMMENT 'ロールを一意に識別するコード（例：ROLE001）',
    role_name VARCHAR(100) COMMENT 'ロールの正式名称',
    role_name_short VARCHAR(50) COMMENT 'ロールの略称・短縮名',
    role_category ENUM COMMENT 'ロールのカテゴリ（SYSTEM:システム、BUSINESS:業務、TENANT:テナント、CUSTOM:カスタム）',
    role_level INT COMMENT 'ロールの階層レベル（1:最上位、数値が大きいほど下位）',
    parent_role_id VARCHAR(50) COMMENT '上位ロールのID（MST_Roleへの自己参照外部キー）',
    is_system_role BOOLEAN DEFAULT False COMMENT 'システム標準ロールかどうか（削除・変更不可）',
    is_tenant_specific BOOLEAN DEFAULT False COMMENT 'テナント固有のロールかどうか',
    max_users INT COMMENT 'このロールに割り当て可能な最大ユーザー数',
    role_priority INT DEFAULT 999 COMMENT '複数ロール保持時の優先度（数値が小さいほど高優先）',
    auto_assign_conditions JSON COMMENT '自動ロール割り当ての条件（JSON形式）',
    role_status ENUM DEFAULT 'ACTIVE' COMMENT 'ロールの状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨）',
    effective_from DATE COMMENT 'ロールの有効開始日',
    effective_to DATE COMMENT 'ロールの有効終了日',
    sort_order INT COMMENT '画面表示時の順序',
    description TEXT COMMENT 'ロールの詳細説明・用途',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
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

-- 外部キー制約
ALTER TABLE MST_Role ADD CONSTRAINT fk_role_parent FOREIGN KEY (parent_role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_Role ADD CONSTRAINT uk_role_code UNIQUE ();
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_level CHECK (role_level > 0);
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_category CHECK (role_category IN ('SYSTEM', 'BUSINESS', 'TENANT', 'CUSTOM'));
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_status CHECK (role_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED'));
ALTER TABLE MST_Role ADD CONSTRAINT chk_max_users CHECK (max_users IS NULL OR max_users > 0);
ALTER TABLE MST_Role ADD CONSTRAINT chk_role_priority CHECK (role_priority > 0);
ALTER TABLE MST_Role ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to);
ALTER TABLE MST_Role ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
