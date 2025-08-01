-- ============================================
-- テーブル: MST_JobType
-- 論理名: 職種マスタ
-- 説明: MST_JobType（職種マスタ）は、組織内の職種分類と各職種の基本情報を管理するマスタテーブルです。

主な目的：
- 職種の体系的な分類・管理
- 職種別スキル要件の定義基盤
- 人材配置・採用計画の基準
- キャリアパス・昇進要件の管理
- 職種別評価基準の設定

このテーブルにより、社員のキャリア開発や適材適所の人材配置、
職種別スキル要件の管理を効率的に行うことができます。

-- 作成日: 2025-06-24 23:05:58
-- ============================================

DROP TABLE IF EXISTS MST_JobType;

CREATE TABLE MST_JobType (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    career_path TEXT COMMENT 'キャリアパス',
    department_affinity TEXT COMMENT '部署親和性',
    description TEXT COMMENT '職種説明',
    is_active BOOLEAN DEFAULT True COMMENT '有効フラグ',
    job_category ENUM('ENGINEERING', 'MANAGEMENT', 'SALES', 'SUPPORT', 'OTHER') COMMENT '職種カテゴリ',
    job_level ENUM('JUNIOR', 'SENIOR', 'LEAD', 'MANAGER', 'DIRECTOR') COMMENT '職種レベル',
    job_type_code VARCHAR(20) COMMENT '職種コード',
    job_type_name VARCHAR(100) COMMENT '職種名',
    job_type_name_en VARCHAR(100) COMMENT '職種名（英語）',
    jobtype_id INT AUTO_INCREMENT NOT NULL COMMENT 'MST_JobTypeの主キー',
    remote_work_eligible BOOLEAN DEFAULT False COMMENT 'リモートワーク可否',
    required_certifications TEXT COMMENT '必要資格',
    required_experience_years INTEGER COMMENT '必要経験年数',
    required_skills TEXT COMMENT '必要スキル',
    salary_grade_max INTEGER COMMENT '給与グレード上限',
    salary_grade_min INTEGER COMMENT '給与グレード下限',
    sort_order INTEGER DEFAULT 0 COMMENT '表示順序',
    travel_frequency ENUM('NONE', 'LOW', 'MEDIUM', 'HIGH') COMMENT '出張頻度',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_job_type_code ON MST_JobType (job_type_code);
CREATE INDEX idx_job_type_name ON MST_JobType (job_type_name);
CREATE INDEX idx_job_category ON MST_JobType (job_category);
CREATE INDEX idx_job_level ON MST_JobType (job_level);
CREATE INDEX idx_category_level ON MST_JobType (job_category, job_level);
CREATE INDEX idx_remote_eligible ON MST_JobType (remote_work_eligible, is_active);
CREATE INDEX idx_sort_order ON MST_JobType (sort_order);
CREATE INDEX idx_mst_jobtype_tenant_id ON MST_JobType (tenant_id);

-- その他の制約
-- 制約DDL生成エラー: uk_job_type_code
ALTER TABLE MST_JobType ADD CONSTRAINT chk_job_category CHECK (job_category IN ('ENGINEERING', 'MANAGEMENT', 'SALES', 'SUPPORT', 'OTHER'));
ALTER TABLE MST_JobType ADD CONSTRAINT chk_job_level CHECK (job_level IN ('JUNIOR', 'SENIOR', 'LEAD', 'MANAGER', 'DIRECTOR'));
ALTER TABLE MST_JobType ADD CONSTRAINT chk_travel_frequency CHECK (travel_frequency IN ('NONE', 'LOW', 'MEDIUM', 'HIGH'));
ALTER TABLE MST_JobType ADD CONSTRAINT chk_experience_years CHECK (required_experience_years IS NULL OR required_experience_years >= 0);
ALTER TABLE MST_JobType ADD CONSTRAINT chk_salary_grade CHECK (salary_grade_min IS NULL OR salary_grade_max IS NULL OR salary_grade_min <= salary_grade_max);
