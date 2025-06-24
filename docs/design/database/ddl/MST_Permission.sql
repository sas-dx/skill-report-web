-- ============================================
-- テーブル: MST_Permission
-- 論理名: 権限情報
-- 説明: MST_Permission（権限情報）は、システム内の権限（許可）を管理するマスタテーブルです。

主な目的：
- システム内の権限定義・管理（画面アクセス、機能実行、データ操作等）
- 権限の階層・グループ管理
- 細粒度アクセス制御の実現
- リソースベースアクセス制御（RBAC）の基盤
- 動的権限管理・条件付きアクセス制御
- 監査・コンプライアンス要件への対応
- 最小権限の原則実装

このテーブルは、ロールと組み合わせてシステムセキュリティを構成し、
適切なアクセス制御を実現する重要なマスタデータです。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS MST_Permission;

CREATE TABLE MST_Permission (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    action_type ENUM('CREATE', 'READ', 'UPDATE', 'DELETE', 'EXECUTE') COMMENT 'アクション種別',
    audit_required BOOLEAN DEFAULT False COMMENT '監査要求フラグ',
    condition_expression TEXT COMMENT '条件式',
    description TEXT COMMENT '権限説明',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    is_system_permission BOOLEAN DEFAULT False COMMENT 'システム権限フラグ',
    parent_permission_id VARCHAR(50) COMMENT '親権限ID',
    permission_category ENUM('SYSTEM', 'SCREEN', 'API', 'DATA', 'FUNCTION') COMMENT '権限カテゴリ',
    permission_code VARCHAR(50) COMMENT '権限コード',
    permission_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_Permissionの主キー',
    permission_name VARCHAR(100) COMMENT '権限名',
    permission_name_short VARCHAR(50) COMMENT '権限名略称',
    permission_status ENUM('ACTIVE', 'INACTIVE', 'DEPRECATED') DEFAULT 'ACTIVE' COMMENT '権限状態',
    requires_approval BOOLEAN DEFAULT False COMMENT '承認要求フラグ',
    requires_conditions BOOLEAN DEFAULT False COMMENT '条件要求フラグ',
    resource_type VARCHAR(50) COMMENT 'リソース種別',
    risk_level INT DEFAULT 1 COMMENT 'リスクレベル',
    scope_level ENUM('GLOBAL', 'TENANT', 'DEPARTMENT', 'SELF') COMMENT 'スコープレベル',
    sort_order INT COMMENT '表示順序',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_permission_code ON MST_Permission (permission_code);
CREATE INDEX idx_permission_category ON MST_Permission (permission_category);
CREATE INDEX idx_resource_action ON MST_Permission (resource_type, action_type);
CREATE INDEX idx_scope_level ON MST_Permission (scope_level);
CREATE INDEX idx_parent_permission ON MST_Permission (parent_permission_id);
CREATE INDEX idx_system_permission ON MST_Permission (is_system_permission);
CREATE INDEX idx_risk_level ON MST_Permission (risk_level);
CREATE INDEX idx_permission_status ON MST_Permission (permission_status);
CREATE INDEX idx_effective_period ON MST_Permission (effective_from, effective_to);
CREATE INDEX idx_mst_permission_tenant_id ON MST_Permission (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Permission ADD CONSTRAINT fk_permission_parent FOREIGN KEY (parent_permission_id) REFERENCES MST_Permission(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_permission_code
ALTER TABLE MST_Permission ADD CONSTRAINT chk_permission_category CHECK (permission_category IN ('SYSTEM', 'SCREEN', 'API', 'DATA', 'FUNCTION'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_action_type CHECK (action_type IN ('CREATE', 'READ', 'UPDATE', 'DELETE', 'EXECUTE'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_scope_level CHECK (scope_level IN ('GLOBAL', 'TENANT', 'DEPARTMENT', 'SELF'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_permission_status CHECK (permission_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_risk_level CHECK (risk_level BETWEEN 1 AND 4);
ALTER TABLE MST_Permission ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to);
ALTER TABLE MST_Permission ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
