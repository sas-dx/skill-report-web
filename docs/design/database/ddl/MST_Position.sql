-- ============================================
-- テーブル: MST_Position
-- 論理名: 役職マスタ
-- 説明: MST_Position（役職マスタ）は、組織内の役職・職位の階層構造と基本情報を管理するマスタテーブルです。

主な目的：
- 役職階層の構造管理（社長、部長、課長、主任等の階層関係）
- 役職基本情報の管理（役職名、役職コード、権限レベル等）
- 人事評価・昇進管理の基盤
- 給与・手当計算の基礎データ
- 権限・アクセス制御の役職単位設定
- 組織図・名刺作成の基礎データ
- 人事制度・キャリアパス管理

このテーブルは、人事管理、権限管理、給与計算、組織運営など、
企業の階層的組織運営の基盤となる重要なマスタデータです。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS MST_Position;

CREATE TABLE MST_Position (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    position_code VARCHAR(20) COMMENT '役職コード',
    position_name VARCHAR(100) COMMENT '役職名',
    allowance_amount DECIMAL(10,2) COMMENT '役職手当額',
    approval_limit DECIMAL(15,2) COMMENT '承認限度額',
    authority_level INT COMMENT '権限レベル',
    can_evaluate BOOLEAN DEFAULT False COMMENT '評価権限フラグ',
    can_hire BOOLEAN DEFAULT False COMMENT '採用権限フラグ',
    description TEXT COMMENT '役職説明',
    is_executive BOOLEAN DEFAULT False COMMENT '役員フラグ',
    is_management BOOLEAN DEFAULT False COMMENT '管理職フラグ',
    position_category ENUM('EXECUTIVE', 'MANAGER', 'SUPERVISOR', 'STAFF') COMMENT '役職カテゴリ',
    position_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_Positionの主キー',
    position_level INT COMMENT '役職レベル',
    position_name_short VARCHAR(50) COMMENT '役職名略称',
    position_rank INT COMMENT '役職ランク',
    position_status ENUM('ACTIVE', 'INACTIVE', 'ABOLISHED') DEFAULT 'ACTIVE' COMMENT '役職状態',
    requires_approval BOOLEAN DEFAULT False COMMENT '承認権限フラグ',
    salary_grade VARCHAR(10) COMMENT '給与等級',
    sort_order INT COMMENT '表示順序',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_position_tenant_id ON MST_Position (tenant_id);

-- その他の制約
-- 制約DDL生成エラー: uk_position_code
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_level CHECK (position_level > 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_rank CHECK (position_rank > 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_authority_level CHECK (authority_level BETWEEN 1 AND 10);
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_category CHECK (position_category IN ('EXECUTIVE', 'MANAGER', 'SUPERVISOR', 'STAFF'));
ALTER TABLE MST_Position ADD CONSTRAINT chk_position_status CHECK (position_status IN ('ACTIVE', 'INACTIVE', 'ABOLISHED'));
ALTER TABLE MST_Position ADD CONSTRAINT chk_approval_limit CHECK (approval_limit IS NULL OR approval_limit >= 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_allowance_amount CHECK (allowance_amount IS NULL OR allowance_amount >= 0);
ALTER TABLE MST_Position ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
