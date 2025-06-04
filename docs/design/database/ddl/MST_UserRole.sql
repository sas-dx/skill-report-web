-- ============================================
-- テーブル: MST_UserRole
-- 論理名: ユーザーロール紐付け
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_UserRole;

CREATE TABLE MST_UserRole (
    user_id VARCHAR(50) COMMENT 'ユーザーのID（MST_UserAuthへの外部キー）',
    role_id VARCHAR(50) COMMENT 'ロールのID（MST_Roleへの外部キー）',
    assignment_type ENUM DEFAULT 'DIRECT' COMMENT 'ロール割り当ての種別（DIRECT:直接、INHERITED:継承、DELEGATED:委譲、TEMPORARY:一時的）',
    assigned_by VARCHAR(50) COMMENT 'ロールを割り当てた管理者のID（MST_UserAuthへの外部キー）',
    assignment_reason TEXT COMMENT 'ロール割り当ての理由・根拠',
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'ロール割り当ての有効開始日時',
    effective_to TIMESTAMP COMMENT 'ロール割り当ての有効終了日時',
    is_primary_role BOOLEAN DEFAULT False COMMENT 'ユーザーの主要ロールかどうか',
    priority_order INT DEFAULT 999 COMMENT '複数ロール保持時の優先順序（数値が小さいほど高優先）',
    conditions JSON COMMENT 'ロール適用の条件（時間帯、場所、状況等をJSON形式）',
    delegation_source_user_id VARCHAR(50) COMMENT '委譲ロールの場合の委譲元ユーザーID',
    delegation_expires_at TIMESTAMP COMMENT '委譲ロールの期限',
    auto_assigned BOOLEAN DEFAULT False COMMENT 'システムによる自動割り当てかどうか',
    requires_approval BOOLEAN DEFAULT False COMMENT 'ロール行使に承認が必要かどうか',
    approval_status ENUM COMMENT '承認の状態（PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下）',
    approved_by VARCHAR(50) COMMENT 'ロール割り当てを承認した管理者のID',
    approved_at TIMESTAMP COMMENT 'ロール割り当てが承認された日時',
    assignment_status ENUM DEFAULT 'ACTIVE' COMMENT '割り当ての状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、EXPIRED:期限切れ）',
    last_used_at TIMESTAMP COMMENT 'このロールが最後に使用された日時',
    usage_count INT DEFAULT 0 COMMENT 'このロールが使用された回数',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称',
    description TEXT COMMENT 'マスタ説明'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_user_role ON MST_UserRole (user_id, role_id);
CREATE INDEX idx_user_id ON MST_UserRole (user_id);
CREATE INDEX idx_role_id ON MST_UserRole (role_id);
CREATE INDEX idx_assignment_type ON MST_UserRole (assignment_type);
CREATE INDEX idx_assigned_by ON MST_UserRole (assigned_by);
CREATE INDEX idx_effective_period ON MST_UserRole (effective_from, effective_to);
CREATE INDEX idx_primary_role ON MST_UserRole (user_id, is_primary_role);
CREATE INDEX idx_assignment_status ON MST_UserRole (assignment_status);
CREATE INDEX idx_approval_status ON MST_UserRole (approval_status);
CREATE INDEX idx_delegation_source ON MST_UserRole (delegation_source_user_id);

-- 外部キー制約
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_role FOREIGN KEY (role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_assigned_by FOREIGN KEY (assigned_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_delegation_source FOREIGN KEY (delegation_source_user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_approved_by FOREIGN KEY (approved_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE MST_UserRole ADD CONSTRAINT uk_user_role_active UNIQUE ();
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_assignment_type CHECK (assignment_type IN ('DIRECT', 'INHERITED', 'DELEGATED', 'TEMPORARY'));
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_assignment_status CHECK (assignment_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'EXPIRED'));
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_approval_status CHECK (approval_status IS NULL OR approval_status IN ('PENDING', 'APPROVED', 'REJECTED'));
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from <= effective_to);
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_delegation_period CHECK (delegation_expires_at IS NULL OR effective_from <= delegation_expires_at);
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_priority_order CHECK (priority_order > 0);
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_usage_count CHECK (usage_count >= 0);
