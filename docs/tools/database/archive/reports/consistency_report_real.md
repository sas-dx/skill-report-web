# データベース整合性チェックレポート

**チェック日時:** 2025-06-21 23:53:01
**対象テーブル数:** 58
**総チェック数:** 275

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
| ✅ SUCCESS | 59 | 21.5% |
| ⚠️ WARNING | 117 | 42.5% |
| ❌ ERROR | 99 | 36.0% |

### 🎯 総合判定

❌ **修正が必要な問題があります**

重要な問題が検出されました。以下の詳細結果を確認して修正してください。

## 🔍 チェック別統計

| チェック名 | 成功 | 警告 | エラー | 情報 | 合計 |
|------------|------|------|--------|------|------|
| テーブル存在確認 | 0 | 58 | 0 | 0 | 58 |
| カラム整合性 | 0 | 52 | 0 | 0 | 52 |
| 外部キー整合性 | 7 | 0 | 99 | 0 | 106 |
| 命名規則チェック | 52 | 7 | 0 | 0 | 59 |

## 📋 詳細結果

### 🔍 テーブル存在確認 (58件)

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

#### 34. ⚠️ MST_TEMPLATE: 不足ファイル - テーブル定義書

---

#### 35. ⚠️ MST_JobType: 不足ファイル - テーブル定義書

---

#### 36. ⚠️ MST_UserRole: 不足ファイル - テーブル定義書

---

#### 37. ⚠️ TRN_GoalProgress: 不足ファイル - テーブル定義書

---

#### 38. ⚠️ MST_EmployeeDepartment: 不足ファイル - テーブル定義書

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

---

#### 53. ⚠️ ------------: 不足ファイル - YAML詳細定義

---

#### 54. ⚠️ MST: 不足ファイル - YAML詳細定義, DDL

---

#### 55. ⚠️ TRN: 不足ファイル - YAML詳細定義, DDL

---

#### 56. ⚠️ SYS: 不足ファイル - YAML詳細定義, DDL

---

#### 57. ⚠️ HIS: 不足ファイル - YAML詳細定義, DDL

---

#### 58. ⚠️ WRK: 不足ファイル - YAML詳細定義, DDL


### 🔍 カラム整合性 (52件)

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

#### 34. ⚠️ MST_TEMPLATE: カラム定義の不一致

---

#### 35. ⚠️ MST_JobType: カラム定義の不一致

---

#### 36. ⚠️ MST_UserRole: カラム定義の不一致

---

#### 37. ⚠️ TRN_GoalProgress: カラム定義の不一致

---

#### 38. ⚠️ MST_EmployeeDepartment: カラム定義の不一致

---

#### 39. ⚠️ MST_Skill: カラム定義の不一致

---

#### 40. ⚠️ MST_TrainingProgram: カラム定義の不一致

---

#### 41. ⚠️ MST_Permission: カラム定義の不一致

---

#### 42. ⚠️ HIS_NotificationLog: カラム定義の不一致

---

#### 43. ⚠️ SYS_SkillMatrix: カラム定義の不一致

---

#### 44. ⚠️ TRN_PDU: カラム定義の不一致

---

#### 45. ⚠️ MST_RolePermission: カラム定義の不一致

---

#### 46. ⚠️ MST_CareerPlan: カラム定義の不一致

---

#### 47. ⚠️ MST_EmployeeJobType: カラム定義の不一致

---

#### 48. ⚠️ SYS_IntegrationConfig: カラム定義の不一致

---

#### 49. ⚠️ SYS_BackupHistory: カラム定義の不一致

---

#### 50. ⚠️ MST_SystemConfig: カラム定義の不一致

---

#### 51. ⚠️ SYS_SkillIndex: カラム定義の不一致

---

#### 52. ⚠️ MST_UserAuth: カラム定義の不一致


### 🔍 外部キー整合性 (106件)

#### 1. ❌ MST_JobTypeSkillGrade: 参照先カラムが存在しません

---

#### 2. ❌ MST_JobTypeSkillGrade: 参照先カラムが存在しません

---

#### 3. ❌ SYS_SystemLog: 参照先カラムが存在しません

---

#### 4. ❌ SYS_TenantUsage: 参照先カラムが存在しません

---

#### 5. ❌ TRN_Notification: 参照先カラムが存在しません

---

#### 6. ❌ TRN_Notification: 参照先カラムが存在しません

---

#### 7. ❌ TRN_SkillEvidence: 参照先カラムが存在しません

---

#### 8. ❌ TRN_SkillEvidence: 参照先カラムが存在しません

---

#### 9. ❌ TRN_SkillEvidence: 参照先カラムが存在しません

---

#### 10. ❌ TRN_SkillEvidence: 参照先カラムが存在しません

---

#### 11. ❌ TRN_SkillEvidence: 参照先カラムが存在しません

---

#### 12. ❌ TRN_SkillEvidence: 参照先カラムが存在しません

---

#### 13. ❌ HIS_TenantBilling: 参照先カラムが存在しません

---

#### 14. ❌ MST_CertificationRequirement: 参照先カラムが存在しません

---

#### 15. ❌ MST_CertificationRequirement: 参照先カラムが存在しません

---

#### 16. ❌ MST_CertificationRequirement: 参照先カラムが存在しません

---

#### 17. ❌ MST_CertificationRequirement: 参照先カラムが存在しません

---

#### 18. ❌ MST_CertificationRequirement: 参照先カラムが存在しません

---

#### 19. ❌ MST_CertificationRequirement: 参照先カラムが存在しません

---

#### 20. ❌ MST_CertificationRequirement: 参照先カラムが存在しません

---

#### 21. ❌ MST_TenantSettings: 参照先カラムが存在しません

---

#### 22. ❌ TRN_EmployeeSkillGrade: 参照先カラムが存在しません

---

#### 23. ❌ TRN_EmployeeSkillGrade: 参照先カラムが存在しません

---

#### 24. ❌ TRN_EmployeeSkillGrade: 参照先カラムが存在しません

---

#### 25. ❌ HIS_AuditLog: 参照先カラムが存在しません

---

#### 26. ❌ HIS_AuditLog: 参照先カラムが存在しません

---

#### 27. ❌ MST_Certification: 参照先カラムが存在しません

---

#### 28. ❌ MST_NotificationSettings: 参照先カラムが存在しません

---

#### 29. ❌ MST_SkillCategory: 参照先カラムが存在しません

---

#### 30. ❌ TRN_TrainingHistory: 参照先カラムが存在しません

---

#### 31. ❌ TRN_TrainingHistory: 参照先カラムが存在しません

---

#### 32. ❌ TRN_TrainingHistory: 参照先カラムが存在しません

---

#### 33. ❌ WRK_BatchJobLog: 参照先カラムが存在しません

---

#### 34. ❌ HIS_ReportGeneration: 参照先カラムが存在しません

---

#### 35. ❌ MST_Role: 参照先カラムが存在しません

---

#### 36. ❌ SYS_TokenStore: 参照先カラムが存在しません

---

#### 37. ❌ TRN_ProjectRecord: 参照先カラムが存在しません

---

#### 38. ❌ TRN_SkillRecord: 参照先カラムが存在しません

---

#### 39. ❌ TRN_SkillRecord: 参照先カラムが存在しません

---

#### 40. ❌ TRN_SkillRecord: 参照先カラムが存在しません

---

#### 41. ❌ TRN_SkillRecord: 参照先カラムが存在しません

---

#### 42. ❌ TRN_SkillRecord: 参照先カラムが存在しません

---

#### 43. ❌ MST_EmployeePosition: 参照先カラムが存在しません

---

#### 44. ❌ MST_EmployeePosition: 参照先カラムが存在しません

---

#### 45. ❌ MST_EmployeePosition: 参照先カラムが存在しません

---

#### 46. ❌ MST_Department: 参照先カラムが存在しません

---

#### 47. ❌ MST_Department: 参照先カラムが存在しません

---

#### 48. ❌ MST_Department: 参照先カラムが存在しません

---

#### 49. ❌ MST_SkillGradeRequirement: 参照先カラムが存在しません

---

#### 50. ❌ MST_SkillHierarchy: 参照先カラムが存在しません

---

#### 51. ❌ MST_SkillHierarchy: 参照先カラムが存在しません

---

#### 52. ❌ MST_JobTypeSkill: 参照先カラムが存在しません

---

#### 53. ❌ MST_JobTypeSkill: 参照先カラムが存在しません

---

#### 54. ❌ MST_TEMPLATE: 参照先テーブル '参照テーブル名' が存在しません

---

#### 55. ❌ MST_UserRole: 参照先カラムが存在しません

---

#### 56. ❌ MST_UserRole: 参照先カラムが存在しません

---

#### 57. ❌ MST_UserRole: 参照先カラムが存在しません

---

#### 58. ❌ MST_UserRole: 参照先カラムが存在しません

---

#### 59. ❌ MST_UserRole: 参照先カラムが存在しません

---

#### 60. ❌ TRN_GoalProgress: 参照先カラムが存在しません

---

#### 61. ❌ TRN_GoalProgress: 参照先カラムが存在しません

---

#### 62. ❌ TRN_GoalProgress: 参照先カラムが存在しません

---

#### 63. ❌ TRN_GoalProgress: 参照先カラムが存在しません

---

#### 64. ❌ MST_EmployeeDepartment: 参照先カラムが存在しません

---

#### 65. ❌ MST_EmployeeDepartment: 参照先カラムが存在しません

---

#### 66. ❌ MST_EmployeeDepartment: 参照先カラムが存在しません

---

#### 67. ❌ MST_EmployeeDepartment: 参照先カラムが存在しません

---

#### 68. ❌ MST_Skill: 参照先カラムが存在しません

---

#### 69. ❌ MST_Skill: 参照先カラムが存在しません

---

#### 70. ❌ MST_TrainingProgram: 参照先カラムが存在しません

---

#### 71. ❌ MST_TrainingProgram: 参照先カラムが存在しません

---

#### 72. ❌ MST_Permission: 参照先カラムが存在しません

---

#### 73. ❌ HIS_NotificationLog: 参照先カラムが存在しません

---

#### 74. ❌ HIS_NotificationLog: 参照先カラムが存在しません

---

#### 75. ❌ HIS_NotificationLog: 参照先カラムが存在しません

---

#### 76. ❌ HIS_NotificationLog: 参照先カラムが存在しません

---

#### 77. ❌ SYS_SkillMatrix: 参照先カラムが存在しません

---

#### 78. ❌ SYS_SkillMatrix: 参照先カラムが存在しません

---

#### 79. ❌ TRN_PDU: 参照先カラムが存在しません

---

#### 80. ❌ TRN_PDU: 参照先カラムが存在しません

---

#### 81. ❌ TRN_PDU: 参照先カラムが存在しません

---

#### 82. ❌ TRN_PDU: 参照先カラムが存在しません

---

#### 83. ❌ TRN_PDU: 参照先カラムが存在しません

---

#### 84. ❌ MST_RolePermission: 参照先カラムが存在しません

---

#### 85. ❌ MST_RolePermission: 参照先カラムが存在しません

---

#### 86. ❌ MST_CareerPlan: 参照先カラムが存在しません

---

#### 87. ❌ MST_CareerPlan: 参照先カラムが存在しません

---

#### 88. ❌ MST_CareerPlan: 参照先カラムが存在しません

---

#### 89. ❌ MST_CareerPlan: 参照先カラムが存在しません

---

#### 90. ❌ MST_CareerPlan: 参照先カラムが存在しません

---

#### 91. ❌ MST_CareerPlan: 参照先カラムが存在しません

---

#### 92. ❌ MST_EmployeeJobType: 参照先カラムが存在しません

---

#### 93. ❌ MST_EmployeeJobType: 参照先カラムが存在しません

---

#### 94. ❌ MST_EmployeeJobType: 参照先カラムが存在しません

---

#### 95. ❌ MST_EmployeeJobType: 参照先カラムが存在しません

---

#### 96. ❌ MST_EmployeeJobType: 参照先カラムが存在しません

---

#### 97. ❌ MST_EmployeeJobType: 参照先カラムが存在しません

---

#### 98. ❌ SYS_SkillIndex: 参照先カラムが存在しません

---

#### 99. ❌ MST_UserAuth: 参照先カラムが存在しません

---

#### 100. ✅ MST_Tenant: 外部キー 'fk_tenant_parent' OK

---

#### 101. ✅ MST_Employee: 外部キー 'fk_employee_department' OK

---

#### 102. ✅ MST_Employee: 外部キー 'fk_employee_position' OK

---

#### 103. ✅ MST_Employee: 外部キー 'fk_employee_job_type' OK

---

#### 104. ✅ MST_Employee: 外部キー 'fk_employee_manager' OK

---

#### 105. ✅ MST_RolePermission: 外部キー 'fk_mst_rolepermission_role_id' OK

---

#### 106. ✅ MST_RolePermission: 外部キー 'fk_mst_rolepermission_permission_id' OK


## 🔧 修正提案

### ❌ ERROR (99件)

#### 1. MST_JobTypeSkillGrade

**問題:** MST_JobTypeSkillGrade: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 2. MST_JobTypeSkillGrade

**問題:** MST_JobTypeSkillGrade: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 3. SYS_SystemLog

**問題:** SYS_SystemLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 4. SYS_TenantUsage

**問題:** SYS_TenantUsage: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 5. TRN_Notification

**問題:** TRN_Notification: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 6. TRN_Notification

**問題:** TRN_Notification: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 7. TRN_SkillEvidence

**問題:** TRN_SkillEvidence: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 8. TRN_SkillEvidence

**問題:** TRN_SkillEvidence: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 9. TRN_SkillEvidence

**問題:** TRN_SkillEvidence: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 10. TRN_SkillEvidence

**問題:** TRN_SkillEvidence: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 11. TRN_SkillEvidence

**問題:** TRN_SkillEvidence: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 12. TRN_SkillEvidence

**問題:** TRN_SkillEvidence: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 13. HIS_TenantBilling

**問題:** HIS_TenantBilling: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 14. MST_CertificationRequirement

**問題:** MST_CertificationRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 15. MST_CertificationRequirement

**問題:** MST_CertificationRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 16. MST_CertificationRequirement

**問題:** MST_CertificationRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 17. MST_CertificationRequirement

**問題:** MST_CertificationRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 18. MST_CertificationRequirement

**問題:** MST_CertificationRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 19. MST_CertificationRequirement

**問題:** MST_CertificationRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 20. MST_CertificationRequirement

**問題:** MST_CertificationRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 21. MST_TenantSettings

**問題:** MST_TenantSettings: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 22. TRN_EmployeeSkillGrade

**問題:** TRN_EmployeeSkillGrade: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 23. TRN_EmployeeSkillGrade

**問題:** TRN_EmployeeSkillGrade: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 24. TRN_EmployeeSkillGrade

**問題:** TRN_EmployeeSkillGrade: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 25. HIS_AuditLog

**問題:** HIS_AuditLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 26. HIS_AuditLog

**問題:** HIS_AuditLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 27. MST_Certification

**問題:** MST_Certification: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 28. MST_NotificationSettings

**問題:** MST_NotificationSettings: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 29. MST_SkillCategory

**問題:** MST_SkillCategory: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 30. TRN_TrainingHistory

**問題:** TRN_TrainingHistory: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 31. TRN_TrainingHistory

**問題:** TRN_TrainingHistory: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 32. TRN_TrainingHistory

**問題:** TRN_TrainingHistory: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 33. WRK_BatchJobLog

**問題:** WRK_BatchJobLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 34. HIS_ReportGeneration

**問題:** HIS_ReportGeneration: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 35. MST_Role

**問題:** MST_Role: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 36. SYS_TokenStore

**問題:** SYS_TokenStore: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 37. TRN_ProjectRecord

**問題:** TRN_ProjectRecord: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 38. TRN_SkillRecord

**問題:** TRN_SkillRecord: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 39. TRN_SkillRecord

**問題:** TRN_SkillRecord: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 40. TRN_SkillRecord

**問題:** TRN_SkillRecord: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 41. TRN_SkillRecord

**問題:** TRN_SkillRecord: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 42. TRN_SkillRecord

**問題:** TRN_SkillRecord: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 43. MST_EmployeePosition

**問題:** MST_EmployeePosition: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 44. MST_EmployeePosition

**問題:** MST_EmployeePosition: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 45. MST_EmployeePosition

**問題:** MST_EmployeePosition: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 46. MST_Department

**問題:** MST_Department: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 47. MST_Department

**問題:** MST_Department: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 48. MST_Department

**問題:** MST_Department: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 49. MST_SkillGradeRequirement

**問題:** MST_SkillGradeRequirement: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 50. MST_SkillHierarchy

**問題:** MST_SkillHierarchy: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 51. MST_SkillHierarchy

**問題:** MST_SkillHierarchy: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 52. MST_JobTypeSkill

**問題:** MST_JobTypeSkill: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 53. MST_JobTypeSkill

**問題:** MST_JobTypeSkill: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 54. MST_TEMPLATE

**問題:** MST_TEMPLATE: 参照先テーブル '参照テーブル名' が存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 55. MST_UserRole

**問題:** MST_UserRole: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 56. MST_UserRole

**問題:** MST_UserRole: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 57. MST_UserRole

**問題:** MST_UserRole: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 58. MST_UserRole

**問題:** MST_UserRole: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 59. MST_UserRole

**問題:** MST_UserRole: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 60. TRN_GoalProgress

**問題:** TRN_GoalProgress: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 61. TRN_GoalProgress

**問題:** TRN_GoalProgress: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 62. TRN_GoalProgress

**問題:** TRN_GoalProgress: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 63. TRN_GoalProgress

**問題:** TRN_GoalProgress: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 64. MST_EmployeeDepartment

**問題:** MST_EmployeeDepartment: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 65. MST_EmployeeDepartment

**問題:** MST_EmployeeDepartment: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 66. MST_EmployeeDepartment

**問題:** MST_EmployeeDepartment: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 67. MST_EmployeeDepartment

**問題:** MST_EmployeeDepartment: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 68. MST_Skill

**問題:** MST_Skill: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 69. MST_Skill

**問題:** MST_Skill: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 70. MST_TrainingProgram

**問題:** MST_TrainingProgram: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 71. MST_TrainingProgram

**問題:** MST_TrainingProgram: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 72. MST_Permission

**問題:** MST_Permission: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 73. HIS_NotificationLog

**問題:** HIS_NotificationLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 74. HIS_NotificationLog

**問題:** HIS_NotificationLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 75. HIS_NotificationLog

**問題:** HIS_NotificationLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 76. HIS_NotificationLog

**問題:** HIS_NotificationLog: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 77. SYS_SkillMatrix

**問題:** SYS_SkillMatrix: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 78. SYS_SkillMatrix

**問題:** SYS_SkillMatrix: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 79. TRN_PDU

**問題:** TRN_PDU: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 80. TRN_PDU

**問題:** TRN_PDU: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 81. TRN_PDU

**問題:** TRN_PDU: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 82. TRN_PDU

**問題:** TRN_PDU: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 83. TRN_PDU

**問題:** TRN_PDU: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 84. MST_RolePermission

**問題:** MST_RolePermission: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 85. MST_RolePermission

**問題:** MST_RolePermission: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 86. MST_CareerPlan

**問題:** MST_CareerPlan: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 87. MST_CareerPlan

**問題:** MST_CareerPlan: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 88. MST_CareerPlan

**問題:** MST_CareerPlan: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 89. MST_CareerPlan

**問題:** MST_CareerPlan: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 90. MST_CareerPlan

**問題:** MST_CareerPlan: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 91. MST_CareerPlan

**問題:** MST_CareerPlan: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 92. MST_EmployeeJobType

**問題:** MST_EmployeeJobType: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 93. MST_EmployeeJobType

**問題:** MST_EmployeeJobType: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 94. MST_EmployeeJobType

**問題:** MST_EmployeeJobType: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 95. MST_EmployeeJobType

**問題:** MST_EmployeeJobType: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 96. MST_EmployeeJobType

**問題:** MST_EmployeeJobType: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 97. MST_EmployeeJobType

**問題:** MST_EmployeeJobType: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 98. SYS_SkillIndex

**問題:** SYS_SkillIndex: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

#### 99. MST_UserAuth

**問題:** MST_UserAuth: 参照先カラムが存在しません

**修正方法:**
```bash
参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください
```

### ⚠️ WARNING (63件)

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

#### 34. MST_TEMPLATE

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_TEMPLATE --generate definition
```

#### 35. MST_JobType

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_JobType --generate definition
```

#### 36. MST_UserRole

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_UserRole --generate definition
```

#### 37. TRN_GoalProgress

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_GoalProgress --generate definition
```

#### 38. MST_EmployeeDepartment

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_EmployeeDepartment --generate definition
```

#### 39. MST_Skill

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Skill --generate definition
```

#### 40. MST_TrainingProgram

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_TrainingProgram --generate definition
```

#### 41. MST_Permission

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_Permission --generate definition
```

#### 42. HIS_NotificationLog

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table HIS_NotificationLog --generate definition
```

#### 43. SYS_SkillMatrix

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_SkillMatrix --generate definition
```

#### 44. TRN_PDU

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN_PDU --generate definition
```

#### 45. MST_RolePermission

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_RolePermission --generate definition
```

#### 46. MST_CareerPlan

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_CareerPlan --generate definition
```

#### 47. MST_EmployeeJobType

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_EmployeeJobType --generate definition
```

#### 48. SYS_IntegrationConfig

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_IntegrationConfig --generate definition
```

#### 49. SYS_BackupHistory

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_BackupHistory --generate definition
```

#### 50. MST_SystemConfig

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_SystemConfig --generate definition
```

#### 51. SYS_SkillIndex

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS_SkillIndex --generate definition
```

#### 52. MST_UserAuth

**問題:** テーブル定義書が不足

**修正方法:**
```bash
python3 -m table_generator --table MST_UserAuth --generate definition
```

#### 53. ------------

**問題:** YAML詳細定義が不足

**修正方法:**
```bash
python3 -m table_generator --table ------------ --generate yaml
```

#### 54. MST

**問題:** YAML詳細定義が不足

**修正方法:**
```bash
python3 -m table_generator --table MST --generate yaml
```

#### 55. MST

**問題:** DDLが不足

**修正方法:**
```bash
python3 -m table_generator --table MST --generate ddl
```

#### 56. TRN

**問題:** YAML詳細定義が不足

**修正方法:**
```bash
python3 -m table_generator --table TRN --generate yaml
```

#### 57. TRN

**問題:** DDLが不足

**修正方法:**
```bash
python3 -m table_generator --table TRN --generate ddl
```

#### 58. SYS

**問題:** YAML詳細定義が不足

**修正方法:**
```bash
python3 -m table_generator --table SYS --generate yaml
```

#### 59. SYS

**問題:** DDLが不足

**修正方法:**
```bash
python3 -m table_generator --table SYS --generate ddl
```

#### 60. HIS

**問題:** YAML詳細定義が不足

**修正方法:**
```bash
python3 -m table_generator --table HIS --generate yaml
```

#### 61. HIS

**問題:** DDLが不足

**修正方法:**
```bash
python3 -m table_generator --table HIS --generate ddl
```

#### 62. WRK

**問題:** YAML詳細定義が不足

**修正方法:**
```bash
python3 -m table_generator --table WRK --generate yaml
```

#### 63. WRK

**問題:** DDLが不足

**修正方法:**
```bash
python3 -m table_generator --table WRK --generate ddl
```
