-- ============================================
-- テーブル: MST_RolePermission
-- 論理名: ロール権限紐付け
-- 説明: 
-- 作成日: 2025-06-06 19:43:49
-- ============================================

DROP TABLE IF EXISTS MST_RolePermission;

CREATE TABLE MST_RolePermission (
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
