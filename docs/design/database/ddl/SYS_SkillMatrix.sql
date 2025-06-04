-- ============================================
-- テーブル: SYS_SkillMatrix
-- 論理名: スキルマップ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS SYS_SkillMatrix;

CREATE TABLE SYS_SkillMatrix (
    employee_id VARCHAR(50) COMMENT '評価対象の社員ID（MST_Employeeへの外部キー）',
    skill_id VARCHAR(50) COMMENT 'スキル項目ID（MST_Skillへの外部キー）',
    skill_level INTEGER DEFAULT 1 COMMENT 'スキル評価レベル（1:初級、2:中級、3:上級、4:エキスパート、5:マスター）',
    self_assessment INTEGER COMMENT '本人による自己評価レベル（1-5）',
    manager_assessment INTEGER COMMENT '上司による評価レベル（1-5）',
    peer_assessment INTEGER COMMENT '同僚による評価レベル（1-5）',
    assessment_date DATE COMMENT 'スキル評価を実施した日付',
    evidence_url VARCHAR(500) COMMENT 'スキル評価の根拠となる資料やプロジェクトのURL',
    notes TEXT COMMENT 'スキル評価に関する詳細な備考やコメント',
    next_target_level INTEGER COMMENT '次回評価での目標レベル（1-5）',
    target_date DATE COMMENT '目標レベル達成予定日',
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

-- 外部キー制約
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_skill FOREIGN KEY (skill_id) REFERENCES MST_Skill(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- その他の制約
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT uk_SYS_SkillMatrix_employee_skill UNIQUE ();
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_skill_level CHECK (skill_level BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_self_assessment CHECK (self_assessment IS NULL OR self_assessment BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_manager_assessment CHECK (manager_assessment IS NULL OR manager_assessment BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_peer_assessment CHECK (peer_assessment IS NULL OR peer_assessment BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_next_target_level CHECK (next_target_level IS NULL OR next_target_level BETWEEN 1 AND 5);
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT chk_SYS_SkillMatrix_target_date CHECK (target_date IS NULL OR target_date >= assessment_date);
