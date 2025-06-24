-- ============================================
-- テーブル: MST_UserRole
-- 論理名: ユーザーロール紐付け
-- 説明: MST_UserRole（ユーザーロール紐付け）は、ユーザーとロールの関連付けを管理するマスタテーブルです。

主な目的：
- ユーザーとロールの多対多関係管理
- 動的なロール割り当て・解除
- 時限ロール・条件付きロール割り当て
- ロール継承・委譲の管理
- 権限昇格・降格の履歴管理
- 職務分離・最小権限の原則実装
- 監査・コンプライアンス対応

このテーブルは、ユーザーの実際の権限を決定する重要な関連テーブルであり、
システムセキュリティの実装において中核的な役割を果たします。

-- 作成日: 2025-06-24 22:56:14
-- ============================================

DROP TABLE IF EXISTS MST_UserRole;

CREATE TABLE MST_UserRole (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    approval_status ENUM('PENDING', 'APPROVED', 'REJECTED') COMMENT '承認状態',
    approved_at TIMESTAMP COMMENT '承認日時',
    approved_by VARCHAR(50) COMMENT '承認者ID',
    assigned_by VARCHAR(50) COMMENT '割り当て者ID',
    assignment_reason TEXT COMMENT '割り当て理由',
    assignment_status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED', 'EXPIRED') DEFAULT 'ACTIVE' COMMENT '割り当て状態',
    assignment_type ENUM('DIRECT', 'INHERITED', 'DELEGATED', 'TEMPORARY') DEFAULT 'DIRECT' COMMENT '割り当て種別',
    auto_assigned BOOLEAN DEFAULT False COMMENT '自動割り当てフラグ',
    conditions JSON COMMENT '適用条件',
    delegation_expires_at TIMESTAMP COMMENT '委譲期限',
    delegation_source_user_id VARCHAR(50) COMMENT '委譲元ユーザーID',
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '有効開始日時',
    effective_to TIMESTAMP COMMENT '有効終了日時',
    is_primary_role BOOLEAN DEFAULT False COMMENT '主ロールフラグ',
    last_used_at TIMESTAMP COMMENT '最終使用日時',
    priority_order INT DEFAULT 999 COMMENT '優先順序',
    requires_approval BOOLEAN DEFAULT False COMMENT '承認要求フラグ',
    role_id VARCHAR(50) COMMENT 'ロールID',
    usage_count INT DEFAULT 0 COMMENT '使用回数',
    user_id VARCHAR(50) COMMENT 'ユーザーID',
    userrole_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_UserRoleの主キー',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_mst_userrole_tenant_id ON MST_UserRole (tenant_id);

-- 外部キー制約
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_role FOREIGN KEY (role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_assigned_by FOREIGN KEY (assigned_by) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_delegation_source FOREIGN KEY (delegation_source_user_id) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_approved_by FOREIGN KEY (approved_by) REFERENCES MST_UserAuth(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_user_role_active
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_assignment_type CHECK (assignment_type IN ('DIRECT', 'INHERITED', 'DELEGATED', 'TEMPORARY'));
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_assignment_status CHECK (assignment_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'EXPIRED'));
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_approval_status CHECK (approval_status IS NULL OR approval_status IN ('PENDING', 'APPROVED', 'REJECTED'));
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_effective_period CHECK (effective_to IS NULL OR effective_from <= effective_to);
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_delegation_period CHECK (delegation_expires_at IS NULL OR effective_from <= delegation_expires_at);
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_priority_order CHECK (priority_order > 0);
ALTER TABLE MST_UserRole ADD CONSTRAINT chk_usage_count CHECK (usage_count >= 0);
