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

-- 作成日: 2025-06-21 17:20:34
-- ============================================

DROP TABLE IF EXISTS MST_UserRole;

CREATE TABLE MST_UserRole (
    user_id VARCHAR,
    role_id VARCHAR,
    assignment_type ENUM DEFAULT 'DIRECT',
    assigned_by VARCHAR,
    assignment_reason TEXT,
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_to TIMESTAMP,
    is_primary_role BOOLEAN DEFAULT False,
    priority_order INT DEFAULT 999,
    conditions JSON,
    delegation_source_user_id VARCHAR,
    delegation_expires_at TIMESTAMP,
    auto_assigned BOOLEAN DEFAULT False,
    requires_approval BOOLEAN DEFAULT False,
    approval_status ENUM,
    approved_by VARCHAR,
    approved_at TIMESTAMP,
    assignment_status ENUM DEFAULT 'ACTIVE',
    last_used_at TIMESTAMP,
    usage_count INT DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード更新日時'
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
