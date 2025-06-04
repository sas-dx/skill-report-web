-- ============================================
-- テーブル: MST_Position
-- 論理名: 役職マスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_Position;

CREATE TABLE MST_Position (
    position_code VARCHAR(20) COMMENT '役職を一意に識別するコード（例：POS001）',
    position_name VARCHAR(100) COMMENT '役職の正式名称',
    position_name_short VARCHAR(50) COMMENT '役職の略称・短縮名',
    position_level INT COMMENT '役職の階層レベル（1:最上位、数値が大きいほど下位）',
    position_rank INT COMMENT '同レベル内での序列・ランク',
    position_category ENUM COMMENT '役職のカテゴリ（EXECUTIVE:役員、MANAGER:管理職、SUPERVISOR:監督職、STAFF:一般職）',
    authority_level INT COMMENT 'システム権限レベル（1-10、数値が大きいほど高権限）',
    approval_limit DECIMAL(15,2) COMMENT '承認可能な金額の上限（円）',
    salary_grade VARCHAR(10) COMMENT '給与計算用の等級コード',
    allowance_amount DECIMAL(10,2) COMMENT '月額役職手当（円）',
    is_management BOOLEAN DEFAULT False COMMENT '管理職かどうか（労働基準法上の管理監督者判定）',
    is_executive BOOLEAN DEFAULT False COMMENT '役員かどうか',
    requires_approval BOOLEAN DEFAULT False COMMENT '承認権限を持つかどうか',
    can_hire BOOLEAN DEFAULT False COMMENT '採用権限を持つかどうか',
    can_evaluate BOOLEAN DEFAULT False COMMENT '人事評価権限を持つかどうか',
    position_status ENUM DEFAULT 'ACTIVE' COMMENT '役職の状態（ACTIVE:有効、INACTIVE:無効、ABOLISHED:廃止）',
    sort_order INT COMMENT '組織図等での表示順序',
    description TEXT COMMENT '役職の責任・権限・業務内容の説明',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_position_code ON MST_Position (position_code);
CREATE INDEX idx_position_level ON MST_Position (position_level);
CREATE INDEX idx_position_rank ON MST_Position (position_rank);
CREATE INDEX idx_position_category ON MST_Position (position_category);
CREATE INDEX idx_authority_level ON MST_Position (authority_level);
CREATE INDEX idx_salary_grade ON MST_Position (salary_grade);
CREATE INDEX idx_status ON MST_Position (position_status);
CREATE INDEX idx_management_flags ON MST_Position (is_management, is_executive);
CREATE INDEX idx_sort_order ON MST_Position (sort_order);

-- その他の制約
ALTER TABLE MST_Position ADD CONSTRAINT uk_position_code UNIQUE ();
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_level CHECK (position_level > 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_rank CHECK (position_rank > 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_authority_level CHECK (authority_level BETWEEN 1 AND 10);
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_category CHECK (position_category IN ('EXECUTIVE', 'MANAGER', 'SUPERVISOR', 'STAFF'));
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_status CHECK (position_status IN ('ACTIVE', 'INACTIVE', 'ABOLISHED'));
ALTER TABLE MST_Position ADD CONSTRAINT chk_approval_limit CHECK (approval_limit IS NULL OR approval_limit >= 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_allowance_amount CHECK (allowance_amount IS NULL OR allowance_amount >= 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
