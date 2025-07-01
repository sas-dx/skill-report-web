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

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS SYS_SkillMatrix;

CREATE TABLE SYS_SkillMatrix (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    assessment_date DATE COMMENT '評価日',
    employee_id VARCHAR(50) COMMENT '社員ID',
    evidence_url VARCHAR(500) COMMENT '根拠URL',
    manager_assessment INTEGER COMMENT '上司評価',
    next_target_level INTEGER COMMENT '次回目標レベル',
    notes TEXT COMMENT '備考',
    peer_assessment INTEGER COMMENT '同僚評価',
    self_assessment INTEGER COMMENT '自己評価',
    skill_id VARCHAR(50) COMMENT 'スキルID',
    skill_level INTEGER DEFAULT 1 COMMENT 'スキルレベル',
    skillmatrix_id INT AUTO_INCREMENT NOT NULL COMMENT 'SYS_SkillMatrixの主キー',
    target_date DATE COMMENT '目標達成日',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_SYS_SkillMatrix_employee_skill ON SYS_SkillMatrix (employee_id, skill_id);
CREATE INDEX idx_SYS_SkillMatrix_employee_id ON SYS_SkillMatrix (employee_id);
CREATE INDEX idx_SYS_SkillMatrix_skill_id ON SYS_SkillMatrix (skill_id);
CREATE INDEX idx_SYS_SkillMatrix_assessment_date ON SYS_SkillMatrix (assessment_date);
CREATE INDEX idx_SYS_SkillMatrix_skill_level ON SYS_SkillMatrix (skill_level);

-- 外部キー制約
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_skill FOREIGN KEY (skill_id) REFERENCES MST_Skill(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
-- 制約DDL生成エラー: uk_SYS_SkillMatrix_employee_skill
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_skill_level CHECK (skill_level BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_self_assessment CHECK (self_assessment IS NULL OR self_assessment BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_manager_assessment CHECK (manager_assessment IS NULL OR manager_assessment BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_peer_assessment CHECK (peer_assessment IS NULL OR peer_assessment BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_next_target_level CHECK (next_target_level IS NULL OR next_target_level BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_target_date CHECK (target_date IS NULL OR target_date >= assessment_date);
