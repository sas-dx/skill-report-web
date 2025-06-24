-- MST_Certification (資格情報) サンプルデータ
-- 生成日時: 2025-06-24 22:56:14

INSERT INTO MST_Certification (
    id, tenant_id, certification_code, certification_name,
    certification_category, certification_id, certification_level, certification_name_en,
    description, exam_fee, exam_format, exam_language,
    is_active, is_recommended, issuer, issuer_country,
    official_url, renewal_required, renewal_requirements, skill_category_id,
    validity_period_months, is_deleted, created_at, updated_at
) VALUES
    (NULL, NULL, 'CERT_AWS_SAA', 'AWS Certified Solutions Architect - Associate',
     'IT', NULL, 'INTERMEDIATE', 'AWS Certified Solutions Architect - Associate',
     'AWSクラウドでのソリューション設計・実装スキルを証明する資格', 15000, 'ONLINE', '日本語/英語',
     TRUE, TRUE, 'Amazon Web Services', 'US',
     'https://aws.amazon.com/jp/certification/certified-solutions-architect-associate/', TRUE, '再認定試験の受験または上位資格の取得', 'SKILL_CAT_CLOUD',
     36, NULL, NULL, NULL),
    (NULL, NULL, 'CERT_PMP', 'Project Management Professional',
     'BUSINESS', NULL, 'ADVANCED', 'Project Management Professional',
     'プロジェクトマネジメントの国際的な資格', 55500, 'BOTH', '日本語/英語',
     TRUE, TRUE, 'Project Management Institute', 'US',
     'https://www.pmi.org/certifications/project-management-pmp', TRUE, '60 PDU（Professional Development Units）の取得', 'SKILL_CAT_PM',
     36, NULL, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Certification ORDER BY created_at DESC;
