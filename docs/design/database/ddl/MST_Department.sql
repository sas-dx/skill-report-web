-- ============================================
-- テーブル: MST_Department
-- 論理名: 部署マスタ
-- 説明: MST_Department（部署マスタ）は、組織の部署・組織単位の階層構造と基本情報を管理するマスタテーブルです。

主な目的：
- 組織階層の構造管理（部署、課、チーム等の階層関係）
- 部署基本情報の管理（部署名、部署コード、責任者等）
- 組織変更履歴の管理（統廃合、新設、移管等）
- 予算・コスト管理の組織単位設定
- 権限・アクセス制御の組織単位設定
- 人事異動・配置管理の基盤
- 組織図・レポート作成の基礎データ

このテーブルは、人事管理、権限管理、予算管理、レポート作成など、
組織運営の様々な業務プロセスの基盤となる重要なマスタデータです。

-- 作成日: 2025-06-21 23:07:48
-- ============================================

DROP TABLE IF EXISTS MST_Department;

CREATE TABLE MST_Department (
    department_id SERIAL NOT NULL COMMENT 'MST_Departmentの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT 'False' COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (department_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_department_tenant_id ON MST_Department (tenant_id);

-- 外部キー制約
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
