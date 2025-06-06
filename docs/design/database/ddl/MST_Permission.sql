-- ============================================
-- テーブル: MST_Permission
-- 論理名: 権限情報
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_Permission;

CREATE TABLE MST_Permission (
    permission_code VARCHAR(50) COMMENT '権限を一意に識別するコード（例：PERM_USER_READ）',
    permission_name VARCHAR(100) COMMENT '権限の正式名称',
    permission_name_short VARCHAR(50) COMMENT '権限の略称・短縮名',
    permission_category ENUM COMMENT '権限のカテゴリ（SYSTEM:システム、SCREEN:画面、API:API、DATA:データ、FUNCTION:機能）',
    resource_type VARCHAR(50) COMMENT '権限対象のリソース種別（USER、SKILL、REPORT等）',
    action_type ENUM COMMENT '許可するアクション（CREATE:作成、READ:参照、UPDATE:更新、DELETE:削除、EXECUTE:実行）',
    scope_level ENUM COMMENT '権限のスコープ（GLOBAL:全体、TENANT:テナント、DEPARTMENT:部署、SELF:自分のみ）',
    parent_permission_id VARCHAR(50) COMMENT '上位権限のID（MST_Permissionへの自己参照外部キー）',
    is_system_permission BOOLEAN DEFAULT False COMMENT 'システム標準権限かどうか（削除・変更不可）',
    requires_conditions BOOLEAN DEFAULT False COMMENT '権限行使に条件が必要かどうか',
    condition_expression TEXT COMMENT '権限行使の条件式（SQL WHERE句形式等）',
    risk_level INT DEFAULT 1 COMMENT '権限のリスクレベル（1:低、2:中、3:高、4:最高）',
    requires_approval BOOLEAN DEFAULT False COMMENT '権限行使に承認が必要かどうか',
    audit_required BOOLEAN DEFAULT False COMMENT '権限行使時の監査ログ記録が必要かどうか',
    permission_status ENUM DEFAULT 'ACTIVE' COMMENT '権限の状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨）',
    effective_from DATE COMMENT '権限の有効開始日',
    effective_to DATE COMMENT '権限の有効終了日',
    sort_order INT COMMENT '画面表示時の順序',
    description TEXT COMMENT '権限の詳細説明・用途',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
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

-- 外部キー制約
ALTER TABLE MST_Permission ADD CONSTRAINT fk_permission_parent FOREIGN KEY (parent_permission_id) REFERENCES MST_Permission(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_Permission ADD CONSTRAINT uk_permission_code UNIQUE ();
ALTER TABLE MST_Permission ADD CONSTRAINT chk_permission_category CHECK (permission_category IN ('SYSTEM', 'SCREEN', 'API', 'DATA', 'FUNCTION'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_action_type CHECK (action_type IN ('CREATE', 'READ', 'UPDATE', 'DELETE', 'EXECUTE'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_scope_level CHECK (scope_level IN ('GLOBAL', 'TENANT', 'DEPARTMENT', 'SELF'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_permission_status CHECK (permission_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED'));
ALTER TABLE MST_Permission ADD CONSTRAINT chk_risk_level CHECK (risk_level BETWEEN 1 AND 4);
ALTER TABLE MST_Permission ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to);
ALTER TABLE MST_Permission ADD CONSTRAINT chk_sort_order CHECK (sort_order IS NULL OR sort_order >= 0);
