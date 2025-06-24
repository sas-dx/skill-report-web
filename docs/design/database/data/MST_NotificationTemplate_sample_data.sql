-- MST_NotificationTemplate (通知テンプレート) サンプルデータ
-- 生成日時: 2025-06-24 22:56:15

INSERT INTO MST_NotificationTemplate (
    id, tenant_id, body_template, format_type,
    is_active, is_default, language_code, notification_type,
    notificationtemplate_id, parameters, sample_data, subject_template,
    template_key, template_name, version, is_deleted,
    created_at, updated_at
) VALUES
    ('NT001', 'TENANT001', '{{employee_name}}さん

以下のスキル情報が更新されました。

スキル名: {{skill_name}}
更新日時: {{updated_at}}
更新者: {{updated_by}}

詳細は以下のリンクからご確認ください。
{{skill_detail_url}}

※このメールは自動送信されています。
', 'PLAIN',
     TRUE, TRUE, 'ja', 'EMAIL',
     NULL, '{"employee_name": "社員名", "skill_name": "スキル名", "updated_at": "更新日時", "updated_by": "更新者", "skill_detail_url": "詳細URL"}', '{"employee_name": "山田太郎", "skill_name": "Java", "updated_at": "2025-06-01 10:30:00", "updated_by": "佐藤花子", "skill_detail_url": "https://system.company.com/skills/123"}', '【スキル更新】{{employee_name}}さんのスキル情報が更新されました',
     'skill_update_notification', 'スキル更新通知テンプレート', '1.0.0', NULL,
     NULL, NULL),
    ('NT002', 'TENANT001', ':warning: *目標期限のお知らせ* :warning:

{{employee_name}}さんの目標「{{goal_title}}」の期限が近づいています。

• 期限: {{deadline_date}}
• 残り日数: {{remaining_days}}日
• 進捗率: {{progress_rate}}%

<{{goal_detail_url}}|詳細を確認する>
', 'MARKDOWN',
     TRUE, TRUE, 'ja', 'SLACK',
     NULL, '{"employee_name": "社員名", "goal_title": "目標タイトル", "deadline_date": "期限日", "remaining_days": "残り日数", "progress_rate": "進捗率", "goal_detail_url": "詳細URL"}', '{"employee_name": "山田太郎", "goal_title": "Java認定資格取得", "deadline_date": "2025-06-30", "remaining_days": "29", "progress_rate": "75", "goal_detail_url": "https://system.company.com/goals/456"}', NULL,
     'goal_deadline_reminder', '目標期限リマインダーテンプレート', '1.0.0', NULL,
     NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_NotificationTemplate ORDER BY created_at DESC;
