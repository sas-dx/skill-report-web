-- ============================================
-- テーブル: TRN_PDU
-- 論理名: 継続教育ポイント
-- 説明: 
-- 作成日: 2025-06-04 06:57:02
-- ============================================

DROP TABLE IF EXISTS TRN_PDU;

CREATE TABLE TRN_PDU (
    pdu_id VARCHAR(50) COMMENT 'PDU記録を一意に識別するID',
    employee_id VARCHAR(50) COMMENT 'PDUを取得した社員のID（MST_Employeeへの外部キー）',
    certification_id VARCHAR(50) COMMENT '関連する資格のID（MST_Certificationへの外部キー）',
    activity_type ENUM COMMENT 'PDU取得活動の種別（TRAINING:研修、CONFERENCE:カンファレンス、SEMINAR:セミナー、SELF_STUDY:自己学習、TEACHING:指導、VOLUNTEER:ボランティア、OTHER:その他）',
    activity_name VARCHAR(200) COMMENT 'PDU取得活動の名称',
    activity_description TEXT COMMENT '活動の詳細説明・内容',
    provider_name VARCHAR(100) COMMENT '活動を提供する機関・組織名',
    activity_date DATE COMMENT 'PDU取得活動を実施した日',
    start_time TIME COMMENT '活動開始時刻',
    end_time TIME COMMENT '活動終了時刻',
    duration_hours DECIMAL(5,1) COMMENT '活動の総時間数',
    pdu_points DECIMAL(5,1) COMMENT '取得したPDUポイント数',
    pdu_category ENUM COMMENT 'PDUのカテゴリ（TECHNICAL:技術、LEADERSHIP:リーダーシップ、STRATEGIC:戦略、BUSINESS:ビジネス）',
    pdu_subcategory VARCHAR(50) COMMENT 'PDUの詳細カテゴリ',
    location VARCHAR(200) COMMENT '活動実施場所',
    cost DECIMAL(10,2) COMMENT '活動参加費用（円）',
    cost_covered_by ENUM COMMENT '費用の負担者（COMPANY:会社、EMPLOYEE:個人、SHARED:折半）',
    evidence_type ENUM COMMENT 'PDU取得の証跡種別（CERTIFICATE:修了証、ATTENDANCE:出席証明、RECEIPT:領収書、REPORT:レポート、OTHER:その他）',
    evidence_file_path VARCHAR(500) COMMENT '証跡ファイルの保存パス',
    certificate_number VARCHAR(100) COMMENT '修了証・認定証の番号',
    instructor_name VARCHAR(100) COMMENT '講師・指導者の名前',
    learning_objectives TEXT COMMENT '活動の学習目標・目的',
    learning_outcomes TEXT COMMENT '実際の学習成果・習得内容',
    skills_developed TEXT COMMENT '活動により向上したスキル（JSON形式）',
    approval_status ENUM DEFAULT 'PENDING' COMMENT 'PDU承認状況（PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下、UNDER_REVIEW:審査中）',
    approved_by VARCHAR(50) COMMENT 'PDUを承認した担当者のID',
    approval_date DATE COMMENT 'PDU承認日',
    approval_comment TEXT COMMENT '承認・却下時のコメント',
    expiry_date DATE COMMENT 'PDUの有効期限',
    is_recurring BOOLEAN DEFAULT False COMMENT '定期的に実施される活動かどうか',
    recurrence_pattern VARCHAR(50) COMMENT '定期活動の繰り返しパターン（WEEKLY、MONTHLY等）',
    related_training_id VARCHAR(50) COMMENT '関連する研修履歴のID（TRN_TrainingHistoryへの外部キー）',
    related_project_id VARCHAR(50) COMMENT '関連するプロジェクトのID（TRN_ProjectRecordへの外部キー）',
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
CREATE UNIQUE INDEX idx_pdu_id ON TRN_PDU (pdu_id);
CREATE INDEX idx_employee_id ON TRN_PDU (employee_id);
CREATE INDEX idx_certification_id ON TRN_PDU (certification_id);
CREATE INDEX idx_activity_type ON TRN_PDU (activity_type);
CREATE INDEX idx_activity_date ON TRN_PDU (activity_date);
CREATE INDEX idx_pdu_category ON TRN_PDU (pdu_category);
CREATE INDEX idx_approval_status ON TRN_PDU (approval_status);
CREATE INDEX idx_employee_period ON TRN_PDU (employee_id, activity_date);
CREATE INDEX idx_expiry_date ON TRN_PDU (expiry_date);
CREATE INDEX idx_certification_employee ON TRN_PDU (certification_id, employee_id, approval_status);

-- 外部キー制約
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(training_history_id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(project_record_id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
ALTER TABLE TRN_PDU ADD CONSTRAINT uk_pdu_id UNIQUE ();
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_activity_type CHECK (activity_type IN ('TRAINING', 'CONFERENCE', 'SEMINAR', 'SELF_STUDY', 'TEACHING', 'VOLUNTEER', 'OTHER'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_pdu_category CHECK (pdu_category IN ('TECHNICAL', 'LEADERSHIP', 'STRATEGIC', 'BUSINESS'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_cost_covered_by CHECK (cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_evidence_type CHECK (evidence_type IN ('CERTIFICATE', 'ATTENDANCE', 'RECEIPT', 'REPORT', 'OTHER'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_approval_status CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'UNDER_REVIEW'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_duration_hours CHECK (duration_hours > 0);
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_pdu_points CHECK (pdu_points > 0);
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_cost CHECK (cost IS NULL OR cost >= 0);
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_time_range CHECK (start_time IS NULL OR end_time IS NULL OR start_time <= end_time);
