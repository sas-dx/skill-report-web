-- ============================================
-- テーブル: SYS_MasterData
-- 論理名: マスターデータ管理
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_MasterData;

CREATE TABLE SYS_MasterData (
    master_key VARCHAR(100) COMMENT 'マスターデータの一意識別キー',
    master_category VARCHAR(50) COMMENT 'マスターデータのカテゴリ（SYSTEM:システム設定、CODE:コードマスター、CONFIG:設定値）',
    master_name VARCHAR(200) COMMENT 'マスターデータの表示名',
    master_value TEXT COMMENT 'マスターデータの値（JSON形式も可）',
    data_type ENUM DEFAULT 'STRING' COMMENT 'マスター値のデータ型（STRING:文字列、INTEGER:整数、DECIMAL:小数、BOOLEAN:真偽値、JSON:JSON、DATE:日付）',
    default_value TEXT COMMENT 'マスターデータのデフォルト値',
    validation_rule TEXT COMMENT '値の妥当性チェック用の正規表現やルール',
    is_system_managed BOOLEAN DEFAULT False COMMENT 'システムが管理するマスターデータかどうか（true:システム管理、false:ユーザー管理）',
    is_editable BOOLEAN DEFAULT True COMMENT '管理画面から編集可能かどうか',
    display_order INTEGER DEFAULT 0 COMMENT '同一カテゴリ内での表示順序',
    description TEXT COMMENT 'マスターデータの詳細説明',
    effective_from DATE COMMENT 'マスターデータの有効開始日',
    effective_to DATE COMMENT 'マスターデータの有効終了日',
    last_modified_by VARCHAR(100) COMMENT '最後にマスターデータを更新したユーザー',
    last_modified_at TIMESTAMP COMMENT '最後にマスターデータを更新した日時',
    version INTEGER DEFAULT 1 COMMENT 'マスターデータのバージョン番号（楽観的排他制御用）',
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

-- その他の制約
ALTER TABLE SYS_MasterData ADD CONSTRAINT uk_SYS_MasterData_master_key UNIQUE ();
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_data_type CHECK (data_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'JSON', 'DATE'));
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_to >= effective_from);
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_display_order CHECK (display_order >= 0);
ALTER TABLE SYS_MasterData ADD CONSTRAINT chk_SYS_MasterData_version CHECK (version > 0);
