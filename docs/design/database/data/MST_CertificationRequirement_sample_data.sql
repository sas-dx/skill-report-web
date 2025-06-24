-- MST_CertificationRequirement (資格要件マスタ) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO MST_CertificationRequirement (
    id, tenant_id, active_flag, alternative_certifications,
    approval_date, approved_by, assessment_criteria, average_study_hours,
    business_justification, certification_id, certificationrequirement_id, client_requirement,
    compliance_requirement, cost_support_amount, cost_support_available, cost_support_conditions,
    created_by, difficulty_rating, effective_end_date, effective_start_date,
    escalation_timing, exemption_conditions, grace_period_months, internal_policy,
    minimum_experience_years, minimum_skill_level, notes, notification_timing,
    priority_order, recommended_training_programs, renewal_interval_months, renewal_required,
    requirement_description, requirement_id, requirement_level, requirement_name,
    requirement_type, review_date, study_time_allocation, success_rate,
    target_department_id, target_job_type_id, target_position_id, target_skill_grade_id,
    training_support_available, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, TRUE, '["基本情報技術者試験", "応用情報技術者試験"]',
     '2024-03-15', 'EMP000005', '資格証明書の提出、実務経験の確認', 150.0,
     '技術的基礎知識の担保、顧客への信頼性向上', 'CERT_IPA_001', NULL, TRUE,
     FALSE, 50000.0, TRUE, '初回受験のみ、合格時に全額支給',
     'EMP000010', 'MEDIUM', NULL, '2024-04-01',
     30, '同等の実務経験5年以上、または関連する上位資格保有', 12, TRUE,
     2, 'INTERMEDIATE', '新入社員は入社3年以内に取得必須', 90,
     1, '["TRN_PROG_003", "TRN_PROG_004"]', NULL, FALSE,
     'システムエンジニア職種における基本的な資格要件', 'REQ_001', 'MANDATORY', 'システムエンジニア必須資格要件',
     'JOB_TYPE', '2025-03-31', 2.0, 75.5,
     NULL, 'JOB_001', NULL, NULL,
     TRUE, NULL, NULL, NULL),
    (NULL, NULL, TRUE, '["プロジェクトマネージャ試験", "P2M資格"]',
     '2023-12-01', 'EMP000008', '資格証明書、プロジェクト実績評価、360度評価', 300.0,
     'プロジェクト管理能力の客観的証明、国際標準への準拠', 'CERT_PMP_001', NULL, TRUE,
     FALSE, 100000.0, TRUE, '受験料・研修費用全額支給、PDU維持費用も支援',
     'EMP000015', 'HARD', NULL, '2024-01-01',
     60, '大規模プロジェクト成功実績3件以上', 18, TRUE,
     5, 'ADVANCED', 'PMO部門配属者は優先的に取得支援', 180,
     1, '["TRN_PROG_001", "TRN_PROG_005"]', 36, TRUE,
     'プロジェクトマネージャー役職への昇進に必要な資格要件', 'REQ_002', 'MANDATORY', 'プロジェクトマネージャー昇進要件',
     'PROMOTION', '2024-12-31', 4.0, 65.0,
     NULL, NULL, 'POS_004', NULL,
     TRUE, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_CertificationRequirement ORDER BY created_at DESC;
