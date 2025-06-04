-- MST_TenantSettings (テナント設定) サンプルデータ
-- 生成日時: 2025-06-04 06:57:02

INSERT INTO MST_TenantSettings (
    id, tenant_id, setting_category, setting_key,
    setting_name, setting_description, data_type, setting_value,
    default_value, validation_rules, is_required, is_encrypted,
    is_system_managed, is_user_configurable, display_order, effective_from,
    effective_until, last_modified_by, code, name,
    description
) VALUES
    ('TS001', 'TENANT001', 'SYSTEM', 'max_users',
     '最大ユーザー数', 'このテナントで作成可能な最大ユーザー数', 'INTEGER', '100',
     '50', '{"min": 1, "max": 1000}', TRUE, FALSE,
     FALSE, FALSE, 1, '2025-01-01 00:00:00',
     NULL, 'SYSTEM', NULL, NULL,
     NULL),
    ('TS002', 'TENANT001', 'UI', 'theme_color',
     'テーマカラー', 'システムのメインテーマカラー', 'STRING', '#2563eb',
     '#3b82f6', '{"pattern": "^#[0-9a-fA-F]{6}$"}', FALSE, FALSE,
     FALSE, TRUE, 1, NULL,
     NULL, 'USER001', NULL, NULL,
     NULL),
    ('TS003', 'TENANT001', 'BUSINESS', 'skill_approval_required',
     'スキル承認必須', 'スキル登録時に承認が必要かどうか', 'BOOLEAN', 'true',
     'false', NULL, TRUE, FALSE,
     FALSE, TRUE, 1, NULL,
     NULL, 'USER001', NULL, NULL,
     NULL),
    ('TS004', 'TENANT001', 'SECURITY', 'password_policy',
     'パスワードポリシー', 'パスワードの複雑性要件', 'JSON', '{"min_length": 8, "require_uppercase": true, "require_lowercase": true, "require_numbers": true, "require_symbols": false}',
     '{"min_length": 6, "require_uppercase": false, "require_lowercase": false, "require_numbers": false, "require_symbols": false}', '{"type": "object", "properties": {"min_length": {"type": "integer", "minimum": 4, "maximum": 128}}}', TRUE, FALSE,
     FALSE, TRUE, 1, NULL,
     NULL, 'USER001', NULL, NULL,
     NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_TenantSettings ORDER BY created_at DESC;
