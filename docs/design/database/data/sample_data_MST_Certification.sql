-- サンプルデータ INSERT文: MST_Certification
-- 生成日時: 2025-06-21 07:31:30
-- レコード数: 2

BEGIN;

INSERT INTO MST_Certification (certification_code, certification_name, certification_name_en, issuer, issuer_country, certification_category, certification_level, validity_period_months, renewal_required, renewal_requirements, exam_fee, exam_language, exam_format, official_url, description, skill_category_id, is_recommended, is_active, id, created_at, updated_at, is_deleted) VALUES ('CERT_AWS_SAA', 'AWS Certified Solutions Architect - Associate', 'AWS Certified Solutions Architect - Associate', 'Amazon Web Services', 'US', 'IT', 'INTERMEDIATE', 36, TRUE, '再認定試験の受験または上位資格の取得', 15000.0, '日本語/英語', 'ONLINE', 'https://aws.amazon.com/jp/certification/certified-solutions-architect-associate/', 'AWSクラウドでのソリューション設計・実装スキルを証明する資格', 'SKILL_CAT_CLOUD', TRUE, TRUE, 'mst_ff634c59', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_Certification (certification_code, certification_name, certification_name_en, issuer, issuer_country, certification_category, certification_level, validity_period_months, renewal_required, renewal_requirements, exam_fee, exam_language, exam_format, official_url, description, skill_category_id, is_recommended, is_active, id, created_at, updated_at, is_deleted) VALUES ('CERT_PMP', 'Project Management Professional', 'Project Management Professional', 'Project Management Institute', 'US', 'BUSINESS', 'ADVANCED', 36, TRUE, '60 PDU（Professional Development Units）の取得', 55500.0, '日本語/英語', 'BOTH', 'https://www.pmi.org/certifications/project-management-pmp', 'プロジェクトマネジメントの国際的な資格', 'SKILL_CAT_PM', TRUE, TRUE, 'mst_6d24da0c', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

COMMIT;

-- MST_Certification サンプルデータ終了
