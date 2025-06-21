-- ============================================
-- テーブル: SYS_SkillMatrix
-- 論理名: スキルマップ
-- 説明: スキルマップテーブルは、社員のスキル評価とスキル項目の関連を管理するシステムテーブルです。

主な目的：
- 社員とスキル項目の多対多関係を管理
- スキル評価レベルの記録
- スキル評価履歴の管理

このテーブルは、スキル管理システムの中核となるテーブルで、
社員のスキル可視化やスキル分析の基盤データを提供します。

-- 作成日: 2025-06-21 17:20:35
-- ============================================

DROP TABLE IF EXISTS SYS_SkillMatrix;

CREATE TABLE SYS_SkillMatrix (
    employee_id VARCHAR,
    skill_id VARCHAR,
    skill_level INTEGER DEFAULT 1,
    self_assessment INTEGER,
    manager_assessment INTEGER,
    peer_assessment INTEGER,
    assessment_date DATE,
    evidence_url VARCHAR,
    notes TEXT,
    next_target_level INTEGER,
    target_date DATE,
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_SYS_SkillMatrix_employee_skill ON SYS_SkillMatrix (employee_id, skill_id);
CREATE INDEX idx_SYS_SkillMatrix_employee_id ON SYS_SkillMatrix (employee_id);
CREATE INDEX idx_SYS_SkillMatrix_skill_id ON SYS_SkillMatrix (skill_id);
CREATE INDEX idx_SYS_SkillMatrix_assessment_date ON SYS_SkillMatrix (assessment_date);
CREATE INDEX idx_SYS_SkillMatrix_skill_level ON SYS_SkillMatrix (skill_level);
