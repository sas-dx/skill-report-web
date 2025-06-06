-- ============================================
-- テーブル: TRN_TrainingHistory
-- 論理名: 研修参加履歴
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_TrainingHistory;

CREATE TABLE TRN_TrainingHistory (
    training_history_id VARCHAR(50) COMMENT '研修参加履歴を一意に識別するID',
    employee_id VARCHAR(50) COMMENT '参加した社員のID（MST_Employeeへの外部キー）',
    training_program_id VARCHAR(50) COMMENT '研修プログラムのID（MST_TrainingProgramへの外部キー）',
    training_name VARCHAR(200) COMMENT '研修・教育プログラムの名称',
    training_type ENUM COMMENT '研修の種別（INTERNAL:社内研修、EXTERNAL:社外研修、ONLINE:オンライン、CERTIFICATION:資格取得、CONFERENCE:カンファレンス）',
    training_category ENUM COMMENT '研修の分野（TECHNICAL:技術、BUSINESS:ビジネス、MANAGEMENT:マネジメント、SOFT_SKILL:ソフトスキル、COMPLIANCE:コンプライアンス）',
    provider_name VARCHAR(100) COMMENT '研修を提供する機関・会社名',
    instructor_name VARCHAR(100) COMMENT '研修講師の名前',
    start_date DATE COMMENT '研修開始日',
    end_date DATE COMMENT '研修終了日（単日の場合は開始日と同じ）',
    duration_hours DECIMAL(5,1) COMMENT '研修の総時間数',
    location VARCHAR(200) COMMENT '研修開催場所（オンラインの場合は「オンライン」）',
    cost DECIMAL(10,2) COMMENT '研修参加費用（円）',
    cost_covered_by ENUM COMMENT '費用の負担者（COMPANY:会社、EMPLOYEE:個人、SHARED:折半）',
    attendance_status ENUM DEFAULT 'COMPLETED' COMMENT '出席状況（COMPLETED:完了、PARTIAL:部分参加、ABSENT:欠席、CANCELLED:中止）',
    completion_rate DECIMAL(5,2) COMMENT '研修の完了率（%）',
    test_score DECIMAL(5,2) COMMENT '研修テストの点数',
    grade VARCHAR(10) COMMENT '研修の成績（A、B、C、合格、不合格等）',
    certificate_obtained BOOLEAN DEFAULT False COMMENT '修了証・認定証を取得したかどうか',
    certificate_number VARCHAR(100) COMMENT '修了証・認定証の番号',
    pdu_earned DECIMAL(5,1) COMMENT '研修で獲得した継続教育ポイント（PDU）',
    skills_acquired TEXT COMMENT '研修で習得したスキル（JSON形式）',
    learning_objectives TEXT COMMENT '研修の学習目標・目的',
    learning_outcomes TEXT COMMENT '実際の学習成果・習得内容',
    feedback TEXT COMMENT '研修に対するフィードバック・感想',
    satisfaction_score DECIMAL(3,1) COMMENT '研修に対する満足度（1.0-5.0）',
    recommendation_score DECIMAL(3,1) COMMENT '他者への推奨度（1.0-5.0）',
    follow_up_required BOOLEAN DEFAULT False COMMENT '追加のフォローアップが必要かどうか',
    follow_up_date DATE COMMENT 'フォローアップの予定日',
    manager_approval BOOLEAN DEFAULT False COMMENT '上司による参加承認があったかどうか',
    approved_by VARCHAR(50) COMMENT '研修参加を承認した上司のID',
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
CREATE UNIQUE INDEX idx_training_history_id ON TRN_TrainingHistory (training_history_id);
CREATE INDEX idx_employee_id ON TRN_TrainingHistory (employee_id);
CREATE INDEX idx_training_program_id ON TRN_TrainingHistory (training_program_id);
CREATE INDEX idx_training_type ON TRN_TrainingHistory (training_type);
CREATE INDEX idx_training_category ON TRN_TrainingHistory (training_category);
CREATE INDEX idx_date_range ON TRN_TrainingHistory (start_date, end_date);
CREATE INDEX idx_attendance_status ON TRN_TrainingHistory (attendance_status);
CREATE INDEX idx_employee_period ON TRN_TrainingHistory (employee_id, start_date, end_date);
CREATE INDEX idx_certificate ON TRN_TrainingHistory (certificate_obtained, certificate_number);

-- 外部キー制約
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program FOREIGN KEY (training_program_id) REFERENCES MST_TrainingProgram(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT uk_training_history_id UNIQUE ();
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_training_type CHECK (training_type IN ('INTERNAL', 'EXTERNAL', 'ONLINE', 'CERTIFICATION', 'CONFERENCE'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_training_category CHECK (training_category IN ('TECHNICAL', 'BUSINESS', 'MANAGEMENT', 'SOFT_SKILL', 'COMPLIANCE'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_cost_covered_by CHECK (cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_attendance_status CHECK (attendance_status IN ('COMPLETED', 'PARTIAL', 'ABSENT', 'CANCELLED'));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_date_range CHECK (end_date IS NULL OR start_date <= end_date);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_duration_hours CHECK (duration_hours IS NULL OR duration_hours > 0);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_completion_rate CHECK (completion_rate IS NULL OR (completion_rate >= 0 AND completion_rate <= 100));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_test_score CHECK (test_score IS NULL OR test_score >= 0);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_satisfaction_score CHECK (satisfaction_score IS NULL OR (satisfaction_score >= 1.0 AND satisfaction_score <= 5.0));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_recommendation_score CHECK (recommendation_score IS NULL OR (recommendation_score >= 1.0 AND recommendation_score <= 5.0));
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_cost CHECK (cost IS NULL OR cost >= 0);
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT chk_pdu_earned CHECK (pdu_earned IS NULL OR pdu_earned >= 0);
