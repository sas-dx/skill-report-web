-- ============================================
-- テーブル: SYS_MasterData
-- 論理名: マスターデータ管理
-- 説明: マスターデータ管理テーブルは、システム全体で使用される各種マスターデータの管理を行うシステムテーブルです。

主な目的：
- システム設定値の一元管理
- 各種コードマスターの管理
- 動的な設定変更への対応
- マスターデータの変更履歴管理

このテーブルは、システムの柔軟性と保守性を向上させる重要なテーブルで、
ハードコーディングを避け、設定値の動的な変更を可能にします。

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS SYS_MasterData;

CREATE TABLE SYS_MasterData (
    master_key VARCHAR,
    master_category VARCHAR,
    master_name VARCHAR,
    master_value TEXT,
    data_type ENUM DEFAULT 'STRING',
    default_value TEXT,
    validation_rule TEXT,
    is_system_managed BOOLEAN DEFAULT False,
    is_editable BOOLEAN DEFAULT True,
    display_order INTEGER DEFAULT 0,
    description TEXT,
    effective_from DATE,
    effective_to DATE,
    last_modified_by VARCHAR,
    last_modified_at TIMESTAMP,
    version INTEGER DEFAULT 1,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_SYS_MasterData_master_key ON SYS_MasterData (master_key);
CREATE INDEX idx_SYS_MasterData_category ON SYS_MasterData (master_category);
CREATE INDEX idx_SYS_MasterData_category_order ON SYS_MasterData (master_category, display_order);
CREATE INDEX idx_SYS_MasterData_effective_period ON SYS_MasterData (effective_from, effective_to);
CREATE INDEX idx_SYS_MasterData_system_managed ON SYS_MasterData (is_system_managed);
