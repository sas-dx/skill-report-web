-- ============================================
-- テーブル: TRN_EmployeeSkillGrade
-- 論理名: 社員スキルグレード
-- 説明: TRN_EmployeeSkillGrade（社員スキルグレード）は、社員が職種ごとに持つスキルグレード情報を管理するトランザクションテーブルです。

主な目的：
- 社員の職種別スキルグレードの管理
- スキルグレードの履歴管理（昇格・降格の記録）
- 有効期間による時系列管理
- 人事評価・昇進判定の基礎データ提供
- スキル分析・レポート作成の基盤
- 組織のスキル可視化・最適化支援

このテーブルは、人事評価、キャリア開発、組織分析など、スキル管理の中核となる重要なデータです。

-- 作成日: 2025-06-21 22:02:17
-- ============================================

DROP TABLE IF EXISTS TRN_EmployeeSkillGrade;

CREATE TABLE TRN_EmployeeSkillGrade (
    employeeskillgrade_id SERIAL NOT NULL COMMENT 'TRN_EmployeeSkillGradeの主キー',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (employeeskillgrade_id, id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE INDEX idx_trn_employeeskillgrade_tenant_id ON TRN_EmployeeSkillGrade (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_employee FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_job_type FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_evaluator FOREIGN KEY (None) REFERENCES None(None) ON UPDATE CASCADE ON DELETE SET NULL;
