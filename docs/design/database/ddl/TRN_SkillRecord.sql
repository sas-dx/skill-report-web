-- ============================================
-- テーブル: TRN_SkillRecord
-- 論理名: スキル情報
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_SkillRecord;

CREATE TABLE TRN_SkillRecord (
    employee_id VARCHAR(50) COMMENT 'スキルを保有する社員のID（MST_Employeeへの外部キー）',
    skill_item_id VARCHAR(50) COMMENT 'スキル項目のID（MST_SkillItemへの外部キー）',
    skill_level INT COMMENT 'スキルレベル（1:初級、2:中級、3:上級、4:エキスパート、5:マスター）',
    self_assessment INT COMMENT '自己評価（1-5段階）',
    manager_assessment INT COMMENT '上司による評価（1-5段階）',
    evidence_description TEXT COMMENT 'スキル習得の証跡や根拠の説明',
    acquisition_date DATE COMMENT 'スキルを習得した日付',
    last_used_date DATE COMMENT 'スキルを最後に使用した日付',
    expiry_date DATE COMMENT 'スキルの有効期限（資格等の場合）',
    certification_id VARCHAR(50) COMMENT '関連する資格のID（MST_Certificationへの外部キー）',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリのID（MST_SkillCategoryへの外部キー）',
    assessment_date DATE COMMENT '最後に評価を行った日付',
    assessor_id VARCHAR(50) COMMENT '評価を行った人のID（MST_Employeeへの外部キー）',
    skill_status ENUM DEFAULT 'ACTIVE' COMMENT 'スキルの状況（ACTIVE:有効、EXPIRED:期限切れ、SUSPENDED:一時停止）',
    learning_hours INT COMMENT 'スキル習得にかけた学習時間（時間）',
    project_experience_count INT COMMENT 'このスキルを使用したプロジェクトの回数',
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    is_deleted BOOLEAN NOT NULL DEFAULT False COMMENT '論理削除フラグ',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'マルチテナント識別子',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'レコード作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP' COMMENT 'レコード更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT 'レコード作成者のユーザーID',
    updated_by VARCHAR(50) NOT NULL COMMENT 'レコード更新者のユーザーID',
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_employee_skill ON TRN_SkillRecord (employee_id, skill_item_id);
CREATE INDEX idx_employee ON TRN_SkillRecord (employee_id);
CREATE INDEX idx_skill_item ON TRN_SkillRecord (skill_item_id);
CREATE INDEX idx_skill_level ON TRN_SkillRecord (skill_level);
CREATE INDEX idx_skill_category ON TRN_SkillRecord (skill_category_id);
CREATE INDEX idx_certification ON TRN_SkillRecord (certification_id);
CREATE INDEX idx_status ON TRN_SkillRecord (skill_status);
CREATE INDEX idx_expiry_date ON TRN_SkillRecord (expiry_date);
CREATE INDEX idx_assessment_date ON TRN_SkillRecord (assessment_date);

-- 外部キー制約
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor FOREIGN KEY (assessor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT uk_employee_skill UNIQUE ();
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_skill_level CHECK (skill_level BETWEEN 1 AND 5);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_self_assessment CHECK (self_assessment IS NULL OR self_assessment BETWEEN 1 AND 5);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_manager_assessment CHECK (manager_assessment IS NULL OR manager_assessment BETWEEN 1 AND 5);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_skill_status CHECK (skill_status IN ('ACTIVE', 'EXPIRED', 'SUSPENDED'));
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_learning_hours CHECK (learning_hours IS NULL OR learning_hours >= 0);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_project_count CHECK (project_experience_count IS NULL OR project_experience_count >= 0);
