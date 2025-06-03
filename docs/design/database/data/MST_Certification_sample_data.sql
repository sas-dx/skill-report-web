-- MST_Certification (資格情報) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_Certification (
    certification_code, certification_name, certification_name_en, issuer,
    issuer_country, certification_category, certification_level, validity_period_months,
    renewal_required, renewal_requirements, exam_fee, exam_language,
    exam_format, official_url, description, skill_category_id,
    is_recommended, is_active, code, name
) VALUES
    ('CERT_AWS_SAA', 'AWS Certified Solutions Architect - Associate', 'AWS Certified Solutions Architect - Associate', 'Amazon Web Services',
     'US', 'IT', 'INTERMEDIATE', 36,
     TRUE, '再認定試験の受験または上位資格の取得', 15000, '日本語/英語',
     'ONLINE', 'https://aws.amazon.com/jp/certification/certified-solutions-architect-associate/', 'AWSクラウドでのソリューション設計・実装スキルを証明する資格', 'SKILL_CAT_CLOUD',
     TRUE, TRUE, NULL, NULL),
    ('CERT_PMP', 'Project Management Professional', 'Project Management Professional', 'Project Management Institute',
     'US', 'BUSINESS', 'ADVANCED', 36,
     TRUE, '60 PDU（Professional Development Units）の取得', 55500, '日本語/英語',
     'BOTH', 'https://www.pmi.org/certifications/project-management-pmp', 'プロジェクトマネジメントの国際的な資格', 'SKILL_CAT_PM',
     TRUE, TRUE, NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_Certification ORDER BY created_at DESC;
