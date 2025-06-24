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

-- 作成日: 2025-06-24 23:02:18
-- ============================================

DROP TABLE IF EXISTS SYS_MasterData;

CREATE TABLE SYS_MasterData (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    data_type ENUM('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'DATE') DEFAULT 'STRING' COMMENT 'データ型',
    default_value TEXT COMMENT 'デフォルト値',
    description TEXT COMMENT '説明',
    display_order INTEGER DEFAULT 0 COMMENT '表示順序',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    is_editable BOOLEAN DEFAULT True COMMENT '編集可能フラグ',
    is_system_managed BOOLEAN DEFAULT False COMMENT 'システム管理フラグ',
    last_modified_at TIMESTAMP COMMENT '最終更新日時',
    last_modified_by VARCHAR(100) COMMENT '最終更新者',
    master_category VARCHAR(50) COMMENT 'マスターカテゴリ',
    master_key VARCHAR(100) COMMENT 'マスターキー',
    master_name VARCHAR(200) COMMENT 'マスター名',
    master_value TEXT COMMENT 'マスター値',
    masterdata_id INT AUTO_INCREMENT NOT NULL COMMENT 'SYS_MasterDataの主キー',
    validation_rule TEXT COMMENT 'バリデーションルール',
    version INTEGER DEFAULT 1 COMMENT 'バージョン',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_SYS_MasterData_master_key ON SYS_MasterData (master_key);
CREATE INDEX idx_SYS_MasterData_category ON SYS_MasterData (master_category);
CREATE INDEX idx_SYS_MasterData_category_order ON SYS_MasterData (master_category, display_order);
CREATE INDEX idx_SYS_MasterData_effective_period ON SYS_MasterData (effective_from, effective_to);
CREATE INDEX idx_SYS_MasterData_system_managed ON SYS_MasterData (is_system_managed);

-- その他の制約
-- 制約DDL生成エラー: uk_SYS_MasterData_master_key
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_data_type CHECK (data_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'DATE'));
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to >= effective_from);
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_display_order CHECK (display_order >= 0);
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_version CHECK (version > 0);
