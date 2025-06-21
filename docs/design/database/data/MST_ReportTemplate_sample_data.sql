-- MST_ReportTemplate (帳票テンプレート) サンプルデータ
-- 生成日時: 2025-06-21 17:20:34

INSERT INTO MST_ReportTemplate (
    id, tenant_id, template_key, template_name,
    report_category, output_format, language_code, template_content,
    style_sheet, parameters_schema, data_source_config, page_settings,
    header_template, footer_template, is_default, is_active,
    version, preview_image_url, created_at, updated_at
) VALUES
    ('RT001', 'TENANT001', 'skill_summary_report', 'スキルサマリーレポート',
     'SKILL', 'PDF', 'ja', '<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{report_title}}</title>
</head>
<body>
    <h1>{{employee_name}}さんのスキルサマリー</h1>
    <div class="summary-section">
        <h2>保有スキル一覧</h2>
        {{#skills}}
        <div class="skill-item">
            <span class="skill-name">{{skill_name}}</span>
            <span class="skill-level">レベル: {{skill_level}}</span>
        </div>
        {{/skills}}
    </div>
</body>
</html>
',
     'body { font-family: ''Noto Sans JP'', sans-serif; }
.skill-item { margin: 10px 0; padding: 5px; border-bottom: 1px solid #ccc; }
.skill-name { font-weight: bold; }
.skill-level { color: #666; }
', '{"type": "object", "properties": {"employee_id": {"type": "string"}, "report_date": {"type": "string", "format": "date"}}}', '{"tables": ["MST_Employee", "TRN_EmployeeSkill", "MST_Skill"], "joins": ["employee_skills", "skill_details"]}', '{"size": "A4", "orientation": "portrait", "margin": {"top": "20mm", "bottom": "20mm", "left": "15mm", "right": "15mm"}}',
     '<div style="text-align: center; font-size: 12px;">{{company_name}} - スキル管理システム</div>', '<div style="text-align: center; font-size: 10px;">出力日時: {{generated_at}} - ページ {{page_number}}</div>', TRUE, TRUE,
     '1.0.0', '/assets/templates/skill_summary_preview.png', NULL, NULL),
    ('RT002', 'TENANT001', 'goal_progress_report', '目標進捗レポート',
     'GOAL', 'EXCEL', 'ja', '<workbook>
    <worksheet name="目標進捗">
        <row>
            <cell>社員名</cell>
            <cell>目標タイトル</cell>
            <cell>進捗率</cell>
            <cell>期限</cell>
            <cell>状態</cell>
        </row>
        {{#goals}}
        <row>
            <cell>{{employee_name}}</cell>
            <cell>{{goal_title}}</cell>
            <cell>{{progress_rate}}%</cell>
            <cell>{{deadline}}</cell>
            <cell>{{status}}</cell>
        </row>
        {{/goals}}
    </worksheet>
</workbook>
',
     NULL, '{"type": "object", "properties": {"department_id": {"type": "string"}, "period_start": {"type": "string", "format": "date"}, "period_end": {"type": "string", "format": "date"}}}', '{"tables": ["MST_Employee", "TRN_Goal"], "joins": ["employee_goals"]}', '{"orientation": "landscape"}',
     NULL, NULL, TRUE, TRUE,
     '1.0.0', '/assets/templates/goal_progress_preview.png', NULL, NULL)
;

-- 実行確認用クエリ
-- SELECT * FROM MST_ReportTemplate ORDER BY created_at DESC;
