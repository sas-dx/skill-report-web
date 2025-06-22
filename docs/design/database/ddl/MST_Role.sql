-- ============================================
-- テーブル: MST_Role
-- 論理名: ロール情報
-- 説明: MST_Role（ロール情報）は、システム内のロール（役割）を管理するマスタテーブルです。

主な目的：
- システム内のロール定義・管理（管理者、一般ユーザー、閲覧者等）
- ロール階層の管理（上位ロール、下位ロール）
- ロール別権限設定の基盤
- 職務分離・最小権限の原則実装
- 動的権限管理・ロールベースアクセス制御（RBAC）
- 組織変更に対応した柔軟な権限管理
- 監査・コンプライアンス対応

このテーブルは、システムセキュリティの基盤となり、
適切なアクセス制御と権限管理を実現する重要なマスタデータです。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_Role;

CREATE TABLE MST_Role (
    role_id SERIAL NOT NULL COMMENT 'MST_Roleの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_role_tenant_id ON MST_Role (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Role ADD CONSTRAINT fk_role_parent FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
