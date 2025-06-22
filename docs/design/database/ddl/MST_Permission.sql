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

-- 作成日: 2025-06-21 22:02:18
-- ============================================

DROP TABLE IF EXISTS MST_Permission;

CREATE TABLE MST_Permission (
    permission_id SERIAL NOT NULL COMMENT 'MST_Permissionの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (permission_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_permission_tenant_id ON MST_Permission (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Permission ADD CONSTRAINT fk_permission_parent FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
