-- MST_TenantSettings (テナント設定) サンプルデータ
-- 生成日時: 2025-06-24 23:05:56

INSERT INTO MST_TenantSettings (
    id, tenant_id, data_type, default_value,
    display_order, effective_from, effective_until, is_encrypted,
    is_required, is_system_managed, is_user_configurable, last_modified_by,
    setting_category, setting_description, setting_key, setting_name,
    setting_value, tenantsettings_id, validation_rules, is_deleted,
    created_at, updated_at
) VALUES
    ('TS001', 'TENANT001', 'INTEGER', '50',
     1, '2025-01-01 00:00:00', NULL, FALSE,
     TRUE, FALSE, FALSE, 'SYSTEM',
     'SYSTEM', 'このテナントで作成可能な最大ユーザー数', 'max_users', '最大ユーザー数',
     '100', NULL, '{"min": 1, "max": 1000}', NULL,
     NULL, NULL),
    ('TS002', 'TENANT001', 'STRING', '#3b82f6',
     1, NULL, NULL, FALSE,
     FALSE, FALSE, TRUE, 'USER001',
     'UI', 'システムのメインテーマカラー', 'theme_color', 'テーマカラー',
     '#2563eb', NULL, '{"pattern": "^#[0-9a-fA-F]{6}$"}', NULL,
     NULL, NULL),
    ('TS003', 'TENANT001', 'BOOLEAN', 'false',
     1, NULL, NULL, FALSE,
     TRUE, FALSE, TRUE, 'USER001',
     'BUSINESS', 'スキル登録時に承認が必要かどうか', 'skill_approval_required', 'スキル承認必須',
     'true', NULL, NULL, NULL,
     NULL, NULL),
    ('TS004', 'TENANT001', 'JSON', '{"min_length": 6, "require_uppercase": false, "require_lowercase": false, "require_numbers": false, "require_symbols": false}',
     1, NULL, NULL, FALSE,
     TRUE, FALSE, TRUE, 'USER001',
     'SECURITY', 'パスワードの複雑性要件', 'password_policy', 'パスワードポリシー',
     '{"min_length": 8, "require_uppercase": true, "require_lowercase": true, "require_numbers": true, "require_symbols": false}', NULL, '{"type": "object", "properties": {"min_length": {"type": "integer", "minimum": 4, "maximum": 128}}}', NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_TenantSettings ORDER BY created_at DESC;
