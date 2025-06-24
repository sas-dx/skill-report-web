-- TRN_SkillEvidence (スキル証跡) サンプルデータ
-- 生成日時: 2025-06-24 23:05:57

INSERT INTO TRN_SkillEvidence (
    id, tenant_id, achievements, certificate_number,
    complexity_level, employee_id, evidence_date, evidence_description,
    evidence_id, evidence_title, evidence_type, external_url,
    file_path, file_size_kb, file_type, impact_score,
    is_portfolio_item, is_public, issuer_name, issuer_type,
    lessons_learned, related_certification_id, related_project_id, related_training_id,
    role_in_activity, skill_id, skill_level_demonstrated, skillevidence_id,
    tags, team_size, technologies_used, validity_end_date,
    validity_start_date, verification_comment, verification_date, verification_method,
    verification_status, verified_by, is_deleted, created_at,
    created_by, updated_by, updated_at
) VALUES
    (NULL, NULL, '予定より2週間早期リリース、性能要件120%達成、バグ発生率0.1%以下', NULL,
     'HIGH', 'EMP000001', '2024-03-31', '大規模ECサイトのバックエンドシステムをJavaで設計・開発',
     'EVD_001', 'ECサイト基盤システム開発', 'PROJECT', 'https://github.com/company/ecommerce-backend',
     '/evidence/EVD_001_project_summary.pdf', 2048, 'PDF', 4.5,
     TRUE, FALSE, '株式会社サンプル', 'COMPANY',
     '大規模システムでのマイクロサービス設計、チーム間連携の重要性', NULL, 'PRJ_REC_001', NULL,
     'テックリード', 'SKILL_JAVA_001', 'ADVANCED', NULL,
     '["Java", "Spring Boot", "システム設計", "チームリード"]', 8, '["Java", "Spring Boot", "PostgreSQL", "Redis", "Docker"]', NULL,
     '2024-03-31', '高品質なコードと優れた設計により、システムの安定性と拡張性を実現', '2024-04-05', 'MANAGER',
     'VERIFIED', 'EMP000010', NULL, NULL,
     NULL, NULL, NULL),
    (NULL, NULL, '一発合格、スコア850点（合格ライン720点）', 'AWS-SAA-2024-002',
     'MEDIUM', 'EMP000002', '2024-02-15', 'AWSクラウドサービスの設計・構築に関する認定資格',
     'EVD_002', 'AWS認定ソリューションアーキテクト - アソシエイト', 'CERTIFICATION', 'https://aws.amazon.com/verification',
     '/evidence/EVD_002_aws_certificate.pdf', 512, 'PDF', 4.0,
     TRUE, TRUE, 'Amazon Web Services', 'CERTIFICATION_BODY',
     'クラウドアーキテクチャの設計原則、AWSサービスの適切な選択方法', 'CERT_AWS_001', NULL, 'TRN_HIS_001',
     '受験者', 'SKILL_AWS_001', 'INTERMEDIATE', NULL,
     '["AWS", "クラウド", "認定資格", "アーキテクチャ"]', NULL, '["AWS", "EC2", "S3", "RDS", "Lambda"]', '2027-02-15',
     '2024-02-15', 'AWS公式認定により自動検証', '2024-02-15', 'AUTOMATIC',
     'VERIFIED', NULL, NULL, NULL,
     NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM TRN_SkillEvidence ORDER BY created_at DESC;
