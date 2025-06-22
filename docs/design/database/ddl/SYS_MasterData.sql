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

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS SYS_MasterData;

CREATE TABLE SYS_MasterData (
    masterdata_id SERIAL NOT NULL COMMENT 'SYS_MasterDataの主キー',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (masterdata_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
