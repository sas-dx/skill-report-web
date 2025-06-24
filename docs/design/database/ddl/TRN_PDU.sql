-- ============================================
-- テーブル: TRN_PDU
-- 論理名: 継続教育ポイント
-- 説明: TRN_PDU（継続教育ポイント）は、社員が取得した継続教育ポイント（Professional Development Units）を管理するトランザクションテーブルです。

主な目的：
- PDU取得履歴の記録・管理
- 資格維持要件の追跡
- 学習活動の定量化
- 継続教育計画の進捗管理
- 資格更新の支援

このテーブルにより、社員の継続的な学習活動を体系的に記録し、
資格維持や専門性向上の支援を効率的に行うことができます。

-- 作成日: 2025-06-24 22:56:15
-- ============================================

DROP TABLE IF EXISTS TRN_PDU;

CREATE TABLE TRN_PDU (
    id VARCHAR(50) NOT NULL COMMENT 'プライマリキー（UUID）',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID（マルチテナント対応）',
    activity_date DATE COMMENT '活動日',
    activity_description TEXT COMMENT '活動説明',
    activity_name VARCHAR(200) COMMENT '活動名',
    activity_type ENUM('TRAINING', 'CONFERENCE', 'SEMINAR', 'SELF_STUDY', 'TEACHING', 'VOLUNTEER', 'OTHER') COMMENT '活動種別',
    approval_comment TEXT COMMENT '承認コメント',
    approval_date DATE COMMENT '承認日',
    approval_status ENUM('PENDING', 'APPROVED', 'REJECTED', 'UNDER_REVIEW') DEFAULT 'PENDING' COMMENT '承認状況',
    approved_by VARCHAR(50) COMMENT '承認者',
    certificate_number VARCHAR(100) COMMENT '証明書番号',
    certification_id VARCHAR(50) COMMENT '資格ID',
    cost DECIMAL(10,2) COMMENT '費用',
    cost_covered_by ENUM('COMPANY', 'EMPLOYEE', 'SHARED') COMMENT '費用負担者',
    duration_hours DECIMAL(5,1) COMMENT '活動時間',
    employee_id VARCHAR(50) COMMENT '社員ID',
    end_time TIME COMMENT '終了時刻',
    evidence_file_path VARCHAR(500) COMMENT '証跡ファイルパス',
    evidence_type ENUM('CERTIFICATE', 'ATTENDANCE', 'RECEIPT', 'REPORT', 'OTHER') COMMENT '証跡種別',
    expiry_date DATE COMMENT '有効期限',
    instructor_name VARCHAR(100) COMMENT '講師名',
    is_recurring BOOLEAN DEFAULT False COMMENT '定期活動フラグ',
    learning_objectives TEXT COMMENT '学習目標',
    learning_outcomes TEXT COMMENT '学習成果',
    location VARCHAR(200) COMMENT '開催場所',
    pdu_category ENUM('TECHNICAL', 'LEADERSHIP', 'STRATEGIC', 'BUSINESS') COMMENT 'PDUカテゴリ',
    pdu_id VARCHAR(50) COMMENT 'PDU ID',
    pdu_points DECIMAL(5,1) COMMENT 'PDUポイント',
    pdu_subcategory VARCHAR(50) COMMENT 'PDUサブカテゴリ',
    provider_name VARCHAR(100) COMMENT '提供機関名',
    recurrence_pattern VARCHAR(50) COMMENT '繰り返しパターン',
    related_project_id VARCHAR(50) COMMENT '関連案件ID',
    related_training_id VARCHAR(50) COMMENT '関連研修ID',
    skills_developed TEXT COMMENT '向上スキル',
    start_time TIME COMMENT '開始時刻',
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE COMMENT '論理削除フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    created_by VARCHAR(50) COMMENT '作成者ID',
    updated_by VARCHAR(50) COMMENT '更新者ID',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新日時'
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
CREATE INDEX idx_trn_pdu_tenant_id ON TRN_PDU (tenant_id);

-- 外部キー制約
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE RESTRICT;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification FOREIGN KEY (certification_id) REFERENCES MST_Certification(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver FOREIGN KEY (approved_by) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_training FOREIGN KEY (related_training_id) REFERENCES TRN_TrainingHistory(id) ON UPDATE CASCADE ON DELETE SET NULL;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_project FOREIGN KEY (related_project_id) REFERENCES TRN_ProjectRecord(id) ON UPDATE CASCADE ON DELETE SET NULL;

-- その他の制約
-- 制約DDL生成エラー: uk_pdu_id
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_activity_type CHECK (activity_type IN ('TRAINING', 'CONFERENCE', 'SEMINAR', 'SELF_STUDY', 'TEACHING', 'VOLUNTEER', 'OTHER'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_pdu_category CHECK (pdu_category IN ('TECHNICAL', 'LEADERSHIP', 'STRATEGIC', 'BUSINESS'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_cost_covered_by CHECK (cost_covered_by IN ('COMPANY', 'EMPLOYEE', 'SHARED'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_evidence_type CHECK (evidence_type IN ('CERTIFICATE', 'ATTENDANCE', 'RECEIPT', 'REPORT', 'OTHER'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_approval_status CHECK (approval_status IN ('PENDING', 'APPROVED', 'REJECTED', 'UNDER_REVIEW'));
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_duration_hours CHECK (duration_hours > 0);
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_pdu_points CHECK (pdu_points > 0);
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_cost CHECK (cost IS NULL OR cost >= 0);
ALTER TABLE TRN_PDU ADD CONSTRAINT chk_time_range CHECK (start_time IS NULL OR end_time IS NULL OR start_time <= end_time);
