-- サンプルデータ INSERT文: MST_NotificationTemplate
-- 生成日時: 2025-06-21 22:54:40
-- レコード数: 2

INSERT INTO MST_NotificationTemplate (id, tenant_id, template_key, template_name, notification_type, language_code, subject_template, body_template, format_type, parameters, sample_data, is_default, is_active, version, created_at, updated_at, is_deleted) VALUES ('NT001', 'TENANT001', 'skill_update_notification', 'スキル更新通知テンプレート', 'EMAIL', 'ja', '【スキル更新】{{employee_name}}さんのスキル情報が更新されました', '{{employee_name}}さん

以下のスキル情報が更新されました。

スキル名: {{skill_name}}
更新日時: {{updated_at}}
更新者: {{updated_by}}

詳細は以下のリンクからご確認ください。
{{skill_detail_url}}

※このメールは自動送信されています。
', 'PLAIN', '{"employee_name": "社員名", "skill_name": "スキル名", "updated_at": "更新日時", "updated_by": "更新者", "skill_detail_url": "詳細URL"}', '{"employee_name": "山田太郎", "skill_name": "Java", "updated_at": "2025-06-01 10:30:00", "updated_by": "佐藤花子", "skill_detail_url": "https://system.company.com/skills/123"}', TRUE, TRUE, '1.0.0', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);
INSERT INTO MST_NotificationTemplate (id, tenant_id, template_key, template_name, notification_type, language_code, subject_template, body_template, format_type, parameters, sample_data, is_default, is_active, version, created_at, updated_at, is_deleted) VALUES ('NT002', 'TENANT001', 'goal_deadline_reminder', '目標期限リマインダーテンプレート', 'SLACK', 'ja', NULL, ':warning: *目標期限のお知らせ* :warning:

{{employee_name}}さんの目標「{{goal_title}}」の期限が近づいています。

• 期限: {{deadline_date}}
• 残り日数: {{remaining_days}}日
• 進捗率: {{progress_rate}}%

<{{goal_detail_url}}|詳細を確認する>
', 'MARKDOWN', '{"employee_name": "社員名", "goal_title": "目標タイトル", "deadline_date": "期限日", "remaining_days": "残り日数", "progress_rate": "進捗率", "goal_detail_url": "詳細URL"}', '{"employee_name": "山田太郎", "goal_title": "Java認定資格取得", "deadline_date": "2025-06-30", "remaining_days": "29", "progress_rate": "75", "goal_detail_url": "https://system.company.com/goals/456"}', TRUE, TRUE, '1.0.0', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, FALSE);

-- MST_NotificationTemplate サンプルデータ終了
