-- ============================================
-- テーブル: TRN_SkillRecord
-- 論理名: スキル情報
-- 説明: TRN_SkillRecord（スキル情報）は、組織内の全社員が保有するスキル・技術・資格等の詳細情報を管理するトランザクションテーブルです。

主な目的：
- 社員個人のスキルポートフォリオ管理（技術スキル、ビジネススキル、資格等）
- スキルレベルの客観的評価・管理（5段階評価システム）
- 自己評価と上司評価による多面的スキル評価
- プロジェクトアサインメントのためのスキルマッチング
- 人材育成計画・キャリア開発支援
- 組織全体のスキル可視化・分析
- 資格取得状況・有効期限管理

このテーブルは、人材配置の最適化、教育研修計画の策定、組織のスキルギャップ分析など、
戦略的人材マネジメントの基盤となる重要なデータを提供します。

-- 作成日: 2025-06-24 23:05:57
-- ============================================

DROP TABLE IF EXISTS TRN_SkillRecord;

CREATE TABLE TRN_SkillRecord (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    acquisition_date DATE COMMENT '習得日',
    assessment_date DATE COMMENT '評価日',
    assessor_id VARCHAR(50) COMMENT '評価者ID',
    certification_id VARCHAR(50) COMMENT '関連資格ID',
    employee_id VARCHAR(50) COMMENT '社員ID',
    evidence_description TEXT COMMENT '証跡説明',
    expiry_date DATE COMMENT '有効期限',
    last_used_date DATE COMMENT '最終使用日',
    learning_hours INT COMMENT '学習時間',
    manager_assessment INT COMMENT '上司評価',
    project_experience_count INT COMMENT 'プロジェクト経験回数',
    self_assessment INT COMMENT '自己評価',
    skill_category_id VARCHAR(50) COMMENT 'スキルカテゴリID',
    skill_item_id VARCHAR(50) COMMENT 'スキル項目ID',
    skill_level INT COMMENT 'スキルレベル',
    skill_status ENUM('ACTIVE', 'EXPIRED', 'SUSPENDED') DEFAULT 'ACTIVE' COMMENT 'スキル状況',
    skillrecord_id INT AUTO_INCREMENT NOT NULL COMMENT 'TRN_SkillRecordの主キー',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_trn_skillrecord_tenant_id ON TRN_SkillRecord (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_item FOREIGN KEY (skill_item_id) REFERENCES MST_SkillItem(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor FOREIGN KEY (assessor_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_employee_skill
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_skill_level CHECK (skill_level BETWEEN 1 AND 5);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_self_assessment CHECK (self_assessment IS NULL OR self_assessment BETWEEN 1 AND 5);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_manager_assessment CHECK (manager_assessment IS NULL OR manager_assessment BETWEEN 1 AND 5);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_skill_status CHECK (skill_status IN ('ACTIVE', 'EXPIRED', 'SUSPENDED'));
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_learning_hours CHECK (learning_hours IS NULL OR learning_hours >= 0);
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT chk_project_count CHECK (project_experience_count IS NULL OR project_experience_count >= 0);
