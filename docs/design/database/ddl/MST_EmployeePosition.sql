-- ============================================
-- テーブル: MST_EmployeePosition
-- 論理名: 社員役職関連
-- 説明: MST_EmployeePosition（社員役職関連）は、社員と役職の関連付けを管理するマスタテーブルです。

主な目的：
- 社員の役職任命履歴の管理
- 複数役職兼任の管理
- 昇進・降格履歴の追跡
- 役職変更時の影響範囲把握
- 役職別権限管理
- 組織階層における権限委譲の管理

このテーブルにより、社員の役職変遷を詳細に管理し、
人事評価や昇進管理の履歴を正確に追跡できます。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS MST_EmployeePosition;

CREATE TABLE MST_EmployeePosition (
    employeeposition_id SERIAL NOT NULL COMMENT 'MST_EmployeePositionの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    PRIMARY KEY (employeeposition_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_mst_employeeposition_tenant_id ON MST_EmployeePosition (tenant_id);

-- 外部キー制約
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_position FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_approved_by FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
