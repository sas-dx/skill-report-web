# データベース整合性チェックレポート

**チェック日時:** 2025-06-22 11:43:45
**対象テーブル数:** 52
**総チェック数:** 262

## 🔍 チェック内容について

このレポートでは、データベース設計の整合性を以下の4つの観点からチェックしています。

### 1. テーブル存在確認

**目的:** すべてのテーブルが必要なファイルに定義されているか確認

**チェック内容:** テーブル一覧、エンティティ関連図、DDL、詳細YAMLの存在確認

**検出する問題:** 定義漏れ、ファイル不足、不整合

### 2. カラム整合性

**目的:** カラム定義の一貫性を確認

**チェック内容:** YAML、DDL、定義書間のカラム定義の一致確認

**検出する問題:** カラム名不一致、データ型不一致、制約不一致

### 3. 外部キー整合性

**目的:** 外部キー制約の妥当性を確認

**チェック内容:** 参照先テーブル・カラムの存在確認

**検出する問題:** 参照先不在、循環参照、制約違反

### 4. 命名規則チェック

**目的:** 命名規則の準拠を確認

**チェック内容:** テーブル名、カラム名の命名規則チェック

**検出する問題:** 命名規則違反、不適切な名前

## 📊 結果サマリー

| 重要度 | 件数 | 割合 |
|--------|------|------|
| ✅ SUCCESS | 156 | 59.5% |
| ⚠️ WARNING | 105 | 40.1% |
| ❌ ERROR | 1 | 0.4% |

### 🎯 総合判定

❌ **修正が必要な問題があります**

重要な問題が検出されました。以下の詳細結果を確認して修正してください。

## 🔍 チェック別統計

| チェック名 | 成功 | 警告 | エラー | 情報 | 合計 |
|------------|------|------|--------|------|------|
| テーブル存在確認 | 0 | 52 | 0 | 0 | 52 |
| カラム整合性 | 0 | 51 | 0 | 0 | 51 |
| 外部キー整合性 | 105 | 0 | 1 | 0 | 106 |
| 命名規則チェック | 51 | 2 | 0 | 0 | 53 |

## 📋 詳細結果

### 🔍 テーブル存在確認 (52件)

#### 1. ⚠️ MST_JobTypeSkillGrade: 不足ファイル - テーブル定義書

---

#### 2. ⚠️ MST_Tenant: 不足ファイル - テーブル定義書

---

#### 3. ⚠️ MST_NotificationTemplate: 不足ファイル - テーブル定義書

---

#### 4. ⚠️ SYS_SystemLog: 不足ファイル - テーブル定義書

---

#### 5. ⚠️ SYS_TenantUsage: 不足ファイル - テーブル定義書

---

#### 6. ⚠️ TRN_Notification: 不足ファイル - テーブル定義書

---

#### 7. ⚠️ TRN_SkillEvidence: 不足ファイル - テーブル定義書

---

#### 8. ⚠️ HIS_TenantBilling: 不足ファイル - テーブル定義書

---

#### 9. ⚠️ MST_SkillGrade: 不足ファイル - テーブル定義書

---

#### 10. ⚠️ MST_CertificationRequirement: 不足ファイル - テーブル定義書

---

#### 11. ⚠️ MST_TenantSettings: 不足ファイル - テーブル定義書

---

#### 12. ⚠️ TRN_EmployeeSkillGrade: 不足ファイル - テーブル定義書

---

#### 13. ⚠️ MST_ReportTemplate: 不足ファイル - テーブル定義書

---

#### 14. ⚠️ SYS_MasterData: 不足ファイル - テーブル定義書

---

#### 15. ⚠️ HIS_AuditLog: 不足ファイル - テーブル定義書

---

#### 16. ⚠️ MST_Certification: 不足ファイル - テーブル定義書

---

#### 17. ⚠️ MST_NotificationSettings: 不足ファイル - テーブル定義書

---

#### 18. ⚠️ MST_SkillCategory: 不足ファイル - テーブル定義書

---

#### 19. ⚠️ TRN_TrainingHistory: 不足ファイル - テーブル定義書

---

#### 20. ⚠️ WRK_BatchJobLog: 不足ファイル - テーブル定義書

---

#### 21. ⚠️ HIS_ReportGeneration: 不足ファイル - テーブル定義書

---

#### 22. ⚠️ MST_Role: 不足ファイル - テーブル定義書

---

#### 23. ⚠️ SYS_TokenStore: 不足ファイル - テーブル定義書

---

#### 24. ⚠️ MST_Position: 不足ファイル - テーブル定義書

---

#### 25. ⚠️ TRN_ProjectRecord: 不足ファイル - テーブル定義書

---

#### 26. ⚠️ MST_Employee: 不足ファイル - テーブル定義書

---

#### 27. ⚠️ TRN_SkillRecord: 不足ファイル - テーブル定義書

---

#### 28. ⚠️ MST_EmployeePosition: 不足ファイル - テーブル定義書

---

#### 29. ⚠️ MST_Department: 不足ファイル - テーブル定義書

---

#### 30. ⚠️ MST_SkillItem: 不足ファイル - テーブル定義書

---

#### 31. ⚠️ MST_SkillGradeRequirement: 不足ファイル - テーブル定義書

---

#### 32. ⚠️ MST_SkillHierarchy: 不足ファイル - テーブル定義書

---

#### 33. ⚠️ MST_JobTypeSkill: 不足ファイル - テーブル定義書

---

#### 34. ⚠️ MST_JobType: 不足ファイル - テーブル定義書

---

#### 35. ⚠️ MST_UserRole: 不足ファイル - テーブル定義書

---

#### 36. ⚠️ TRN_GoalProgress: 不足ファイル - テーブル定義書

---

#### 37. ⚠️ MST_EmployeeDepartment: 不足ファイル - テーブル定義書

---

#### 38. ⚠️ _TEMPLATE: 不足ファイル - DDL, テーブル定義書

---

#### 39. ⚠️ MST_Skill: 不足ファイル - テーブル定義書

---

#### 40. ⚠️ MST_TrainingProgram: 不足ファイル - テーブル定義書

---

#### 41. ⚠️ MST_Permission: 不足ファイル - テーブル定義書

---

#### 42. ⚠️ HIS_NotificationLog: 不足ファイル - テーブル定義書

---

#### 43. ⚠️ SYS_SkillMatrix: 不足ファイル - テーブル定義書

---

#### 44. ⚠️ TRN_PDU: 不足ファイル - テーブル定義書

---

#### 45. ⚠️ MST_RolePermission: 不足ファイル - テーブル定義書

---

#### 46. ⚠️ MST_CareerPlan: 不足ファイル - テーブル定義書

---

#### 47. ⚠️ MST_EmployeeJobType: 不足ファイル - テーブル定義書

---

#### 48. ⚠️ SYS_IntegrationConfig: 不足ファイル - テーブル定義書

---

#### 49. ⚠️ SYS_BackupHistory: 不足ファイル - テーブル定義書

---

#### 50. ⚠️ MST_SystemConfig: 不足ファイル - テーブル定義書

---

#### 51. ⚠️ SYS_SkillIndex: 不足ファイル - テーブル定義書

---

#### 52. ⚠️ MST_UserAuth: 不足ファイル - テーブル定義書


### 🔍 カラム整合性 (51件)

#### 1. ⚠️ MST_JobTypeSkillGrade: カラム定義の不一致

---

#### 2. ⚠️ MST_Tenant: カラム定義の不一致

---

#### 3. ⚠️ MST_NotificationTemplate: カラム定義の不一致

---

#### 4. ⚠️ SYS_SystemLog: カラム定義の不一致

---

#### 5. ⚠️ SYS_TenantUsage: カラム定義の不一致

---

#### 6. ⚠️ TRN_Notification: カラム定義の不一致

---

#### 7. ⚠️ TRN_SkillEvidence: カラム定義の不一致

---

#### 8. ⚠️ HIS_TenantBilling: カラム定義の不一致

---

#### 9. ⚠️ MST_SkillGrade: カラム定義の不一致

---

#### 10. ⚠️ MST_CertificationRequirement: カラム定義の不一致

---

#### 11. ⚠️ MST_TenantSettings: カラム定義の不一致

---

#### 12. ⚠️ TRN_EmployeeSkillGrade: カラム定義の不一致

---

#### 13. ⚠️ MST_ReportTemplate: カラム定義の不一致

---

#### 14. ⚠️ SYS_MasterData: カラム定義の不一致

---

#### 15. ⚠️ HIS_AuditLog: カラム定義の不一致

---

#### 16. ⚠️ MST_Certification: カラム定義の不一致

---

#### 17. ⚠️ MST_NotificationSettings: カラム定義の不一致

---

#### 18. ⚠️ MST_SkillCategory: カラム定義の不一致

---

#### 19. ⚠️ TRN_TrainingHistory: カラム定義の不一致

---

#### 20. ⚠️ WRK_BatchJobLog: カラム定義の不一致

---

#### 21. ⚠️ HIS_ReportGeneration: カラム定義の不一致

---

#### 22. ⚠️ MST_Role: カラム定義の不一致

---

#### 23. ⚠️ SYS_TokenStore: カラム定義の不一致

---

#### 24. ⚠️ MST_Position: カラム定義の不一致

---

#### 25. ⚠️ TRN_ProjectRecord: カラム定義の不一致

---

#### 26. ⚠️ MST_Employee: カラム定義の不一致

---

#### 27. ⚠️ TRN_SkillRecord: カラム定義の不一致

---

#### 28. ⚠️ MST_EmployeePosition: カラム定義の不一致

---

#### 29. ⚠️ MST_Department: カラム定義の不一致

---

#### 30. ⚠️ MST_SkillItem: カラム定義の不一致

---

#### 31. ⚠️ MST_SkillGradeRequirement: カラム定義の不一致

---

#### 32. ⚠️ MST_SkillHierarchy: カラム定義の不一致

---

#### 33. ⚠️ MST_JobTypeSkill: カラム定義の不一致

---

#### 34. ⚠️ MST_JobType: カラム定義の不一致

---

#### 35. ⚠️ MST_UserRole: カラム定義の不一致

---

#### 36. ⚠️ TRN_GoalProgress: カラム定義の不一致

---

#### 37. ⚠️ MST_EmployeeDepartment: カラム定義の不一致

---

#### 38. ⚠️ MST_Skill: カラム定義の不一致

---

#### 39. ⚠️ MST_TrainingProgram: カラム定義の不一致

---

#### 40. ⚠️ MST_Permission: カラム定義の不一致

---

#### 41. ⚠️ HIS_NotificationLog: カラム定義の不一致

---

#### 42. ⚠️ SYS_SkillMatrix: カラム定義の不一致

---

#### 43. ⚠️ TRN_PDU: カラム定義の不一致

---

#### 44. ⚠️ MST_RolePermission: カラム定義の不一致

---

#### 45. ⚠️ MST_CareerPlan: カラム定義の不一致

---

#### 46. ⚠️ MST_EmployeeJobType: カラム定義の不一致

---

#### 47. ⚠️ SYS_IntegrationConfig: カラム定義の不一致

---

#### 48. ⚠️ SYS_BackupHistory: カラム定義の不一致

---

#### 49. ⚠️ MST_SystemConfig: カラム定義の不一致

---

#### 50. ⚠️ SYS_SkillIndex: カラム定義の不一致

---

#### 51. ⚠️ MST_UserAuth: カラム定義の不一致


### 🔍 外部キー整合性 (106件)

#### 1. ❌ _TEMPLATE: 参照先テーブル '参照テーブル名' が存在しません

---

#### 2. ✅ MST_JobTypeSkillGrade: 外部キー 'fk_MST_JobTypeSkillGrade_job_type' OK

---

#### 3. ✅ MST_JobTypeSkillGrade: 外部キー 'fk_MST_JobTypeSkillGrade_skill_grade' OK

---

#### 4. ✅ MST_Tenant: 外部キー 'fk_tenant_parent' OK

---

#### 5. ✅ SYS_SystemLog: 外部キー 'fk_log_user' OK

---

#### 6. ✅ SYS_TenantUsage: 外部キー 'fk_SYS_TenantUsage_tenant' OK

---

#### 7. ✅ TRN_Notification: 外部キー 'fk_notification_recipient' OK

---

#### 8. ✅ TRN_Notification: 外部キー 'fk_notification_sender' OK

---

#### 9. ✅ TRN_SkillEvidence: 外部キー 'fk_evidence_employee' OK

---

#### 10. ✅ TRN_SkillEvidence: 外部キー 'fk_evidence_skill' OK

---

#### 11. ✅ TRN_SkillEvidence: 外部キー 'fk_evidence_verifier' OK

---

#### 12. ✅ TRN_SkillEvidence: 外部キー 'fk_evidence_project' OK

---

#### 13. ✅ TRN_SkillEvidence: 外部キー 'fk_evidence_training' OK

---

#### 14. ✅ TRN_SkillEvidence: 外部キー 'fk_evidence_certification' OK

---

#### 15. ✅ HIS_TenantBilling: 外部キー 'fk_tenant_billing_tenant' OK

---

#### 16. ✅ MST_CertificationRequirement: 外部キー 'fk_cert_req_target_job_type' OK

---

#### 17. ✅ MST_CertificationRequirement: 外部キー 'fk_cert_req_target_position' OK

---

#### 18. ✅ MST_CertificationRequirement: 外部キー 'fk_cert_req_target_skill_grade' OK

---

#### 19. ✅ MST_CertificationRequirement: 外部キー 'fk_cert_req_target_department' OK

---

#### 20. ✅ MST_CertificationRequirement: 外部キー 'fk_cert_req_certification' OK

---

#### 21. ✅ MST_CertificationRequirement: 外部キー 'fk_cert_req_created_by' OK

---

#### 22. ✅ MST_CertificationRequirement: 外部キー 'fk_cert_req_approved_by' OK

---

#### 23. ✅ MST_TenantSettings: 外部キー 'fk_tenant_settings_tenant' OK

---

#### 24. ✅ TRN_EmployeeSkillGrade: 外部キー 'fk_skill_grade_employee' OK

---

#### 25. ✅ TRN_EmployeeSkillGrade: 外部キー 'fk_skill_grade_job_type' OK

---

#### 26. ✅ TRN_EmployeeSkillGrade: 外部キー 'fk_skill_grade_evaluator' OK

---

#### 27. ✅ HIS_AuditLog: 外部キー 'fk_his_auditlog_tenant' OK

---

#### 28. ✅ HIS_AuditLog: 外部キー 'fk_his_auditlog_user' OK

---

#### 29. ✅ MST_Certification: 外部キー 'fk_certification_skill_category' OK

---

#### 30. ✅ MST_NotificationSettings: 外部キー 'fk_notification_settings_template' OK

---

#### 31. ✅ MST_SkillCategory: 外部キー 'fk_skillcategory_parent' OK

---

#### 32. ✅ TRN_TrainingHistory: 外部キー 'fk_training_history_employee' OK

---

#### 33. ✅ TRN_TrainingHistory: 外部キー 'fk_training_history_program' OK

---

#### 34. ✅ TRN_TrainingHistory: 外部キー 'fk_training_history_approver' OK

---

#### 35. ✅ WRK_BatchJobLog: 外部キー 'fk_WRK_BatchJobLog_executed_by' OK

---

#### 36. ✅ HIS_ReportGeneration: 外部キー 'fk_report_generation_template' OK

---

#### 37. ✅ MST_Role: 外部キー 'fk_role_parent' OK

---

#### 38. ✅ SYS_TokenStore: 外部キー 'fk_token_store_user' OK

---

#### 39. ✅ TRN_ProjectRecord: 外部キー 'fk_project_record_employee' OK

---

#### 40. ✅ MST_Employee: 外部キー 'fk_employee_department' OK

---

#### 41. ✅ MST_Employee: 外部キー 'fk_employee_position' OK

---

#### 42. ✅ MST_Employee: 外部キー 'fk_employee_job_type' OK

---

#### 43. ✅ MST_Employee: 外部キー 'fk_employee_manager' OK

---

#### 44. ✅ TRN_SkillRecord: 外部キー 'fk_skill_employee' OK

---

#### 45. ✅ TRN_SkillRecord: 外部キー 'fk_skill_item' OK

---

#### 46. ✅ TRN_SkillRecord: 外部キー 'fk_skill_certification' OK

---

#### 47. ✅ TRN_SkillRecord: 外部キー 'fk_skill_category' OK

---

#### 48. ✅ TRN_SkillRecord: 外部キー 'fk_skill_assessor' OK

---

#### 49. ✅ MST_EmployeePosition: 外部キー 'fk_MST_EmployeePosition_employee' OK

---

#### 50. ✅ MST_EmployeePosition: 外部キー 'fk_MST_EmployeePosition_position' OK

---

#### 51. ✅ MST_EmployeePosition: 外部キー 'fk_MST_EmployeePosition_approved_by' OK

---

#### 52. ✅ MST_Department: 外部キー 'fk_department_parent' OK

---

#### 53. ✅ MST_Department: 外部キー 'fk_department_manager' OK

---

#### 54. ✅ MST_Department: 外部キー 'fk_department_deputy' OK

---

#### 55. ✅ MST_SkillGradeRequirement: 外部キー 'fk_MST_SkillGradeRequirement_skill_grade' OK

---

#### 56. ✅ MST_SkillHierarchy: 外部キー 'fk_hierarchy_skill' OK

---

#### 57. ✅ MST_SkillHierarchy: 外部キー 'fk_hierarchy_parent' OK

---

#### 58. ✅ MST_JobTypeSkill: 外部キー 'fk_MST_JobTypeSkill_job_type' OK

---

#### 59. ✅ MST_JobTypeSkill: 外部キー 'fk_MST_JobTypeSkill_skill_item' OK

---

#### 60. ✅ MST_UserRole: 外部キー 'fk_userrole_user' OK

---

#### 61. ✅ MST_UserRole: 外部キー 'fk_userrole_role' OK

---

#### 62. ✅ MST_UserRole: 外部キー 'fk_userrole_assigned_by' OK

---

#### 63. ✅ MST_UserRole: 外部キー 'fk_userrole_delegation_source' OK

---

#### 64. ✅ MST_UserRole: 外部キー 'fk_userrole_approved_by' OK

---

#### 65. ✅ TRN_GoalProgress: 外部キー 'fk_TRN_GoalProgress_employee' OK

---

#### 66. ✅ TRN_GoalProgress: 外部キー 'fk_TRN_GoalProgress_supervisor' OK

---

#### 67. ✅ TRN_GoalProgress: 外部キー 'fk_TRN_GoalProgress_approved_by' OK

---

#### 68. ✅ TRN_GoalProgress: 外部キー 'fk_TRN_GoalProgress_career_plan' OK

---

#### 69. ✅ MST_EmployeeDepartment: 外部キー 'fk_MST_EmployeeDepartment_employee' OK

---

#### 70. ✅ MST_EmployeeDepartment: 外部キー 'fk_MST_EmployeeDepartment_department' OK

---

#### 71. ✅ MST_EmployeeDepartment: 外部キー 'fk_MST_EmployeeDepartment_reporting_manager' OK

---

#### 72. ✅ MST_EmployeeDepartment: 外部キー 'fk_MST_EmployeeDepartment_approved_by' OK

---

#### 73. ✅ MST_Skill: 外部キー 'fk_MST_Skill_tenant' OK

---

#### 74. ✅ MST_Skill: 外部キー 'fk_MST_Skill_category' OK

---

#### 75. ✅ MST_TrainingProgram: 外部キー 'fk_training_program_created_by' OK

---

#### 76. ✅ MST_TrainingProgram: 外部キー 'fk_training_program_approved_by' OK

---

#### 77. ✅ MST_Permission: 外部キー 'fk_permission_parent' OK

---

#### 78. ✅ HIS_NotificationLog: 外部キー 'fk_notification_log_notification' OK

---

#### 79. ✅ HIS_NotificationLog: 外部キー 'fk_notification_log_setting' OK

---

#### 80. ✅ HIS_NotificationLog: 外部キー 'fk_notification_log_template' OK

---

#### 81. ✅ HIS_NotificationLog: 外部キー 'fk_notification_log_integration' OK

---

#### 82. ✅ SYS_SkillMatrix: 外部キー 'fk_SYS_SkillMatrix_employee' OK

---

#### 83. ✅ SYS_SkillMatrix: 外部キー 'fk_SYS_SkillMatrix_skill' OK

---

#### 84. ✅ TRN_PDU: 外部キー 'fk_pdu_employee' OK

---

#### 85. ✅ TRN_PDU: 外部キー 'fk_pdu_certification' OK

---

#### 86. ✅ TRN_PDU: 外部キー 'fk_pdu_approver' OK

---

#### 87. ✅ TRN_PDU: 外部キー 'fk_pdu_training' OK

---

#### 88. ✅ TRN_PDU: 外部キー 'fk_pdu_project' OK

---

#### 89. ✅ MST_RolePermission: 外部キー 'fk_mst_rolepermission_role_id' OK

---

#### 90. ✅ MST_RolePermission: 外部キー 'fk_mst_rolepermission_permission_id' OK

---

#### 91. ✅ MST_RolePermission: 外部キー 'fk_mst_rolepermission_granted_by' OK

---

#### 92. ✅ MST_RolePermission: 外部キー 'fk_mst_rolepermission_revoked_by' OK

---

#### 93. ✅ MST_CareerPlan: 外部キー 'fk_career_plan_employee' OK

---

#### 94. ✅ MST_CareerPlan: 外部キー 'fk_career_plan_target_position' OK

---

#### 95. ✅ MST_CareerPlan: 外部キー 'fk_career_plan_target_job_type' OK

---

#### 96. ✅ MST_CareerPlan: 外部キー 'fk_career_plan_target_department' OK

---

#### 97. ✅ MST_CareerPlan: 外部キー 'fk_career_plan_mentor' OK

---

#### 98. ✅ MST_CareerPlan: 外部キー 'fk_career_plan_supervisor' OK

---

#### 99. ✅ MST_EmployeeJobType: 外部キー 'fk_emp_job_type_employee' OK

---

#### 100. ✅ MST_EmployeeJobType: 外部キー 'fk_emp_job_type_job_type' OK

---

#### 101. ✅ MST_EmployeeJobType: 外部キー 'fk_emp_job_type_mentor' OK

---

#### 102. ✅ MST_EmployeeJobType: 外部キー 'fk_emp_job_type_supervisor' OK

---

#### 103. ✅ MST_EmployeeJobType: 外部キー 'fk_emp_job_type_created_by' OK

---

#### 104. ✅ MST_EmployeeJobType: 外部キー 'fk_emp_job_type_approved_by' OK

---

#### 105. ✅ SYS_SkillIndex: 外部キー 'fk_skill_index_skill' OK

---

#### 106. ✅ MST_UserAuth: 外部キー 'fk_userauth_employee' OK


## 🔧 修正提案

### ❌ ERROR (1件)

#### 1. _TEMPLATE

**問題:** _TEMPLATE: 参照先テーブル '参照テーブル名' が存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

### ⚠️ WARNING (53件)

#### 1. MST_JobTypeSkillGrade

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_JobTypeSkillGrade --generate definition
```

#### 2. MST_Tenant

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Tenant --generate definition
```

#### 3. MST_NotificationTemplate

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_NotificationTemplate --generate definition
```

#### 4. SYS_SystemLog

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_SystemLog --generate definition
```

#### 5. SYS_TenantUsage

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_TenantUsage --generate definition
```

#### 6. TRN_Notification

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_Notification --generate definition
```

#### 7. TRN_SkillEvidence

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_SkillEvidence --generate definition
```

#### 8. HIS_TenantBilling

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table HIS_TenantBilling --generate definition
```

#### 9. MST_SkillGrade

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_SkillGrade --generate definition
```

#### 10. MST_CertificationRequirement

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_CertificationRequirement --generate definition
```

#### 11. MST_TenantSettings

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_TenantSettings --generate definition
```

#### 12. TRN_EmployeeSkillGrade

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_EmployeeSkillGrade --generate definition
```

#### 13. MST_ReportTemplate

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_ReportTemplate --generate definition
```

#### 14. SYS_MasterData

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_MasterData --generate definition
```

#### 15. HIS_AuditLog

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table HIS_AuditLog --generate definition
```

#### 16. MST_Certification

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Certification --generate definition
```

#### 17. MST_NotificationSettings

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_NotificationSettings --generate definition
```

#### 18. MST_SkillCategory

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_SkillCategory --generate definition
```

#### 19. TRN_TrainingHistory

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_TrainingHistory --generate definition
```

#### 20. WRK_BatchJobLog

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table WRK_BatchJobLog --generate definition
```

#### 21. HIS_ReportGeneration

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table HIS_ReportGeneration --generate definition
```

#### 22. MST_Role

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Role --generate definition
```

#### 23. SYS_TokenStore

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_TokenStore --generate definition
```

#### 24. MST_Position

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Position --generate definition
```

#### 25. TRN_ProjectRecord

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_ProjectRecord --generate definition
```

#### 26. MST_Employee

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Employee --generate definition
```

#### 27. TRN_SkillRecord

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_SkillRecord --generate definition
```

#### 28. MST_EmployeePosition

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_EmployeePosition --generate definition
```

#### 29. MST_Department

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Department --generate definition
```

#### 30. MST_SkillItem

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_SkillItem --generate definition
```

#### 31. MST_SkillGradeRequirement

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_SkillGradeRequirement --generate definition
```

#### 32. MST_SkillHierarchy

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_SkillHierarchy --generate definition
```

#### 33. MST_JobTypeSkill

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_JobTypeSkill --generate definition
```

#### 34. MST_JobType

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_JobType --generate definition
```

#### 35. MST_UserRole

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_UserRole --generate definition
```

#### 36. TRN_GoalProgress

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_GoalProgress --generate definition
```

#### 37. MST_EmployeeDepartment

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_EmployeeDepartment --generate definition
```

#### 38. _TEMPLATE

**問題:** DDLが不足

**修正方法:**
```bash
python3 -m table_generator --table _TEMPLATE --generate ddl
```

#### 39. _TEMPLATE

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table _TEMPLATE --generate definition
```

#### 40. MST_Skill

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Skill --generate definition
```

#### 41. MST_TrainingProgram

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_TrainingProgram --generate definition
```

#### 42. MST_Permission

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Permission --generate definition
```

#### 43. HIS_NotificationLog

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table HIS_NotificationLog --generate definition
```

#### 44. SYS_SkillMatrix

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_SkillMatrix --generate definition
```

#### 45. TRN_PDU

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_PDU --generate definition
```

#### 46. MST_RolePermission

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_RolePermission --generate definition
```

#### 47. MST_CareerPlan

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_CareerPlan --generate definition
```

#### 48. MST_EmployeeJobType

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_EmployeeJobType --generate definition
```

#### 49. SYS_IntegrationConfig

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_IntegrationConfig --generate definition
```

#### 50. SYS_BackupHistory

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_BackupHistory --generate definition
```

#### 51. MST_SystemConfig

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_SystemConfig --generate definition
```

#### 52. SYS_SkillIndex

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_SkillIndex --generate definition
```

#### 53. MST_UserAuth

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_UserAuth --generate definition
```
