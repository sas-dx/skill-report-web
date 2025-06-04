-- ============================================
-- テーブル: MST_JobType
-- 論理名: 職種マスタ
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS MST_JobType;

CREATE TABLE MST_JobType (
    job_type_code VARCHAR(20) COMMENT '職種を一意に識別するコード（例：SE、PM、QA、BA）',
    job_type_name VARCHAR(100) COMMENT '職種の正式名称',
    job_type_name_en VARCHAR(100) COMMENT '英語での職種名称',
    job_category ENUM COMMENT '職種の大分類（ENGINEERING:エンジニアリング、MANAGEMENT:マネジメント、SALES:営業、SUPPORT:サポート、OTHER:その他）',
    job_level ENUM COMMENT '職種の階層レベル（JUNIOR:ジュニア、SENIOR:シニア、LEAD:リード、MANAGER:マネージャー、DIRECTOR:ディレクター）',
    description TEXT COMMENT '職種の詳細説明・役割・責任範囲',
    required_experience_years INTEGER COMMENT '職種に就くために必要な経験年数（目安）',
    salary_grade_min INTEGER COMMENT '職種の給与グレード下限値',
    salary_grade_max INTEGER COMMENT '職種の給与グレード上限値',
    career_path TEXT COMMENT '職種からの一般的なキャリアパス・昇進ルート',
    required_certifications TEXT COMMENT '職種に必要または推奨される資格（JSON形式で複数格納）',
    required_skills TEXT COMMENT '職種に必要なスキル（JSON形式で複数格納）',
    department_affinity TEXT COMMENT '職種が配属されやすい部署（JSON形式で複数格納）',
    remote_work_eligible BOOLEAN DEFAULT False COMMENT 'リモートワークが可能な職種かどうか',
    travel_frequency ENUM COMMENT '出張の頻度（NONE:なし、LOW:低、MEDIUM:中、HIGH:高）',
    sort_order INTEGER DEFAULT 0 COMMENT '職種一覧での表示順序',
    is_active BOOLEAN DEFAULT True COMMENT '職種が有効かどうか',
    code VARCHAR(20) NOT NULL COMMENT 'マスタコード',
    name VARCHAR(100) NOT NULL COMMENT 'マスタ名称'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックス作成
CREATE UNIQUE INDEX idx_job_type_code ON MST_JobType (job_type_code);
CREATE INDEX idx_job_type_name ON MST_JobType (job_type_name);
CREATE INDEX idx_job_category ON MST_JobType (job_category);
CREATE INDEX idx_job_level ON MST_JobType (job_level);
CREATE INDEX idx_category_level ON MST_JobType (job_category, job_level);
CREATE INDEX idx_remote_eligible ON MST_JobType (remote_work_eligible, is_active);
CREATE INDEX idx_sort_order ON MST_JobType (sort_order);

-- その他の制約
ALTER TABLE MST_JobType ADD CONSTRAINT uk_job_type_code UNIQUE ();
ALTER TABLE MST_JobType ADD CONSTRAINT chk_job_category CHECK (job_category IN ('ENGINEERING', 'MANAGEMENT', 'SALES', 'SUPPORT', 'OTHER'));
ALTER TABLE MST_JobType ADD CONSTRAINT chk_job_level CHECK (job_level IN ('JUNIOR', 'SENIOR', 'LEAD', 'MANAGER', 'DIRECTOR'));
ALTER TABLE MST_JobType ADD CONSTRAINT chk_travel_frequency CHECK (travel_frequency IN ('NONE', 'LOW', 'MEDIUM', 'HIGH'));
ALTER TABLE MST_JobType ADD CONSTRAINT chk_experience_years CHECK (required_experience_years IS NULL OR required_experience_years >= 0);
ALTER TABLE MST_JobType ADD CONSTRAINT chk_salary_grade CHECK (salary_grade_min IS NULL OR salary_grade_max IS NULL OR salary_grade_min <= salary_grade_max);
