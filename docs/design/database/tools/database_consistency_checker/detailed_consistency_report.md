# データベース整合性チェックレポート

**チェック日時:** 2025-06-04 22:41:30
**対象テーブル数:** 51
**総チェック数:** 948

## 🔍 チェック内容について

このレポートでは、データベース設計の整合性を以下の4つの観点からチェックしています。

### 1. テーブル存在確認

**目的:** 設計ドキュメント間でのテーブル定義の一貫性を確認

**チェック内容:** テーブル一覧.md、entity_relationships.yaml、DDLファイル、詳細YAMLファイルの4つのソース間でテーブルが正しく定義されているかを確認

**検出する問題:** 定義漏れ、不整合、命名ミス

### 2. 孤立ファイル検出

**目的:** 不要なファイルや管理対象外ファイルの検出

**チェック内容:** テーブル一覧に記載されていないDDLファイルや詳細YAMLファイルを検出

**検出する問題:** 削除し忘れたファイル、テーブル一覧への追加漏れ

### 3. カラム定義整合性

**目的:** DDLとYAMLファイル間でのカラム定義の整合性確認

**チェック内容:** データ型、長さ、NULL制約、デフォルト値、ENUM値、インデックス、制約の一致確認

**検出する問題:** 型不一致、制約の相違、定義漏れ

### 4. 外部キー整合性

**目的:** エンティティ関連図とDDL間での外部キー定義の整合性確認

**チェック内容:** 外部キー名、参照先テーブル・カラム、ON DELETE/UPDATE設定の一致確認

**検出する問題:** 参照先不整合、制約設定の相違、定義漏れ

## 📊 結果サマリー

| 重要度 | 件数 | 割合 |
|--------|------|------|
| ✅ SUCCESS | 48 | 5.1% |
| ⚠️ WARNING | 564 | 59.5% |
| ❌ ERROR | 336 | 35.4% |

### 🎯 総合判定

❌ **修正が必要な問題があります**

重要な問題が検出されました。以下の詳細結果を確認して修正してください。

## 🔍 チェック別統計

| チェック名 | 成功 | 警告 | エラー | 情報 | 合計 |
|------------|------|------|--------|------|------|
| テーブル存在確認 | 48 | 0 | 3 | 0 | 51 |
| 孤立ファイル検出 | 0 | 3 | 0 | 0 | 3 |
| カラム定義整合性 | 0 | 374 | 156 | 0 | 530 |
| 外部キー整合性 | 0 | 187 | 177 | 0 | 364 |

## 📋 詳細結果

### 🔍 テーブル存在確認 (51件)

#### 1. ❌ テーブル定義の不整合 - 存在: テーブル詳細YAML | 不足: テーブル一覧.md, entity_relationships.yaml, DDLファイル

**テーブル:** HIS_ReportGeneration

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ✅ 存在
- **期待されるファイル:**
  - HIS_ReportGeneration.sql
- **修正提案:**
  - テーブル一覧.mdに'HIS_ReportGeneration'を追加してください
  - DDLファイル'HIS_ReportGeneration.sql'を作成してください
  - entity_relationships.yamlに'HIS_ReportGeneration'の関連定義を追加してください

---

#### 2. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, テーブル詳細YAML | 不足: テーブル一覧.md, DDLファイル

**テーブル:** MST_RolePermission

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ✅ 存在
- **期待されるファイル:**
  - MST_RolePermission.sql
- **修正提案:**
  - テーブル一覧.mdに'MST_RolePermission'を追加してください
  - DDLファイル'MST_RolePermission.sql'を作成してください

---

#### 3. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, テーブル詳細YAML | 不足: テーブル一覧.md, DDLファイル

**テーブル:** MST_Skill

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ✅ 存在
- **期待されるファイル:**
  - MST_Skill.sql
- **修正提案:**
  - テーブル一覧.mdに'MST_Skill'を追加してください
  - DDLファイル'MST_Skill.sql'を作成してください

---

#### 4. ✅ 全てのソースに存在します

**テーブル:** HIS_AuditLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 5. ✅ 全てのソースに存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 6. ✅ 全てのソースに存在します

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 7. ✅ 全てのソースに存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 8. ✅ 全てのソースに存在します

**テーブル:** MST_Certification

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 9. ✅ 全てのソースに存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 10. ✅ 全てのソースに存在します

**テーブル:** MST_Department

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 11. ✅ 全てのソースに存在します

**テーブル:** MST_Employee

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 12. ✅ 全てのソースに存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 13. ✅ 全てのソースに存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 14. ✅ 全てのソースに存在します

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 15. ✅ 全てのソースに存在します

**テーブル:** MST_JobType

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 16. ✅ 全てのソースに存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 17. ✅ 全てのソースに存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 18. ✅ 全てのソースに存在します

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 19. ✅ 全てのソースに存在します

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 20. ✅ 全てのソースに存在します

**テーブル:** MST_Permission

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 21. ✅ 全てのソースに存在します

**テーブル:** MST_Position

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 22. ✅ 全てのソースに存在します

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 23. ✅ 全てのソースに存在します

**テーブル:** MST_Role

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 24. ✅ 全てのソースに存在します

**テーブル:** MST_SkillCategory

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 25. ✅ 全てのソースに存在します

**テーブル:** MST_SkillGrade

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 26. ✅ 全てのソースに存在します

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 27. ✅ 全てのソースに存在します

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 28. ✅ 全てのソースに存在します

**テーブル:** MST_SkillItem

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 29. ✅ 全てのソースに存在します

**テーブル:** MST_SystemConfig

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 30. ✅ 全てのソースに存在します

**テーブル:** MST_Tenant

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 31. ✅ 全てのソースに存在します

**テーブル:** MST_TenantSettings

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 32. ✅ 全てのソースに存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 33. ✅ 全てのソースに存在します

**テーブル:** MST_UserAuth

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 34. ✅ 全てのソースに存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 35. ✅ 全てのソースに存在します

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 36. ✅ 全てのソースに存在します

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 37. ✅ 全てのソースに存在します

**テーブル:** SYS_MasterData

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 38. ✅ 全てのソースに存在します

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 39. ✅ 全てのソースに存在します

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 40. ✅ 全てのソースに存在します

**テーブル:** SYS_SystemLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 41. ✅ 全てのソースに存在します

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 42. ✅ 全てのソースに存在します

**テーブル:** SYS_TokenStore

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 43. ✅ 全てのソースに存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 44. ✅ 全てのソースに存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 45. ✅ 全てのソースに存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 46. ✅ 全てのソースに存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 47. ✅ 全てのソースに存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 48. ✅ 全てのソースに存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 49. ✅ 全てのソースに存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 50. ✅ 全てのソースに存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在

---

#### 51. ✅ 全てのソースに存在します

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在


### 🔍 孤立ファイル検出 (3件)

#### 1. ⚠️ 孤立ファイル: HIS_ReportGeneration_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** HIS_ReportGeneration_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 2. ⚠️ 孤立ファイル: MST_Skill_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Skill_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 3. ⚠️ 孤立ファイル: MST_RolePermission_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_RolePermission_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません


### 🔍 カラム定義整合性 (530件)

#### 1. ❌ カラム 'action_type' のENUM値が不一致

**テーブル:** HIS_AuditLog

**詳細情報:**
- **column_name:** action_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CREATE
  - READ
  - UPDATE
  - DELETE
  - LOGIN
  - LOGOUT

---

#### 2. ❌ カラム 'result_status' のENUM値が不一致

**テーブル:** HIS_AuditLog

**詳細情報:**
- **column_name:** result_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SUCCESS
  - FAILURE
  - ERROR

---

#### 3. ❌ カラム 'notification_type' のENUM値が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** notification_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - EMAIL
  - SLACK
  - TEAMS
  - WEBHOOK

---

#### 4. ❌ カラム 'priority_level' のENUM値が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** priority_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - HIGH
  - MEDIUM
  - LOW

---

#### 5. ❌ カラム 'send_status' のENUM値が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** send_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PENDING
  - SENDING
  - SUCCESS
  - FAILED
  - RETRY

---

#### 6. ❌ カラム 'recipient_type' のENUM値が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** recipient_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - USER
  - GROUP
  - CHANNEL
  - WEBHOOK

---

#### 7. ❌ カラム 'message_format' のENUM値が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** message_format
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PLAIN
  - HTML
  - MARKDOWN

---

#### 8. ❌ カラム 'payment_method' のENUM値が不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** payment_method
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CREDIT_CARD
  - BANK_TRANSFER
  - AUTO_DEBIT

---

#### 9. ❌ カラム 'billing_type' のENUM値が不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** billing_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - MONTHLY
  - USAGE
  - SETUP
  - ADDITIONAL

---

#### 10. ❌ カラム 'billing_status' のENUM値が不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** billing_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CALCULATED
  - INVOICED
  - PAID
  - CANCELLED

---

#### 11. ❌ カラム 'plan_type' のENUM値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** plan_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SHORT_TERM
  - MEDIUM_TERM
  - LONG_TERM
  - SPECIALIZED
  - MANAGEMENT
  - TECHNICAL

---

#### 12. ❌ カラム 'priority_level' のENUM値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** priority_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - LOW
  - NORMAL
  - HIGH
  - CRITICAL

---

#### 13. ❌ カラム 'target_level' のENUM値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** target_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ENTRY
  - JUNIOR
  - INTERMEDIATE
  - SENIOR
  - EXPERT
  - MANAGER
  - EXECUTIVE

---

#### 14. ❌ カラム 'visibility_level' のENUM値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** visibility_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PRIVATE
  - MANAGER
  - DEPARTMENT
  - COMPANY

---

#### 15. ❌ カラム 'current_level' のENUM値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** current_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ENTRY
  - JUNIOR
  - INTERMEDIATE
  - SENIOR
  - EXPERT
  - MANAGER
  - EXECUTIVE

---

#### 16. ❌ カラム 'review_frequency' のENUM値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** review_frequency
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - MONTHLY
  - QUARTERLY
  - SEMI_ANNUAL
  - ANNUAL

---

#### 17. ❌ カラム 'plan_status' のENUM値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** plan_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - DRAFT
  - ACTIVE
  - ON_HOLD
  - COMPLETED
  - CANCELLED
  - REVISED

---

#### 18. ❌ カラム 'exam_format' のENUM値が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** exam_format
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ONLINE
  - OFFLINE
  - BOTH

---

#### 19. ❌ カラム 'certification_level' のENUM値が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** certification_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - BASIC
  - INTERMEDIATE
  - ADVANCED
  - EXPERT

---

#### 20. ❌ カラム 'certification_category' のENUM値が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** certification_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - IT
  - BUSINESS
  - NATIONAL
  - LANGUAGE
  - OTHER

---

#### 21. ❌ カラム 'requirement_level' のENUM値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** requirement_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - MANDATORY
  - PREFERRED
  - OPTIONAL
  - DISQUALIFYING

---

#### 22. ❌ カラム 'minimum_skill_level' のENUM値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** minimum_skill_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - BEGINNER
  - INTERMEDIATE
  - ADVANCED
  - EXPERT

---

#### 23. ❌ カラム 'difficulty_rating' のENUM値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** difficulty_rating
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - EASY
  - MEDIUM
  - HARD
  - VERY_HARD

---

#### 24. ❌ カラム 'requirement_type' のENUM値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** requirement_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - JOB_TYPE
  - POSITION
  - SKILL_GRADE
  - PROJECT
  - PROMOTION

---

#### 25. ❌ カラム 'department_type' のENUM値が不一致

**テーブル:** MST_Department

**詳細情報:**
- **column_name:** department_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - HEADQUARTERS
  - DIVISION
  - DEPARTMENT
  - SECTION
  - TEAM

---

#### 26. ❌ カラム 'department_status' のENUM値が不一致

**テーブル:** MST_Department

**詳細情報:**
- **column_name:** department_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - MERGED
  - ABOLISHED

---

#### 27. ❌ カラム 'employee_status' のENUM値が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **column_name:** employee_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - RETIRED
  - SUSPENDED

---

#### 28. ❌ カラム 'gender' のENUM値が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **column_name:** gender
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - M
  - F
  - O

---

#### 29. ❌ カラム 'employment_status' のENUM値が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **column_name:** employment_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - FULL_TIME
  - PART_TIME
  - CONTRACT

---

#### 30. ❌ カラム 'approval_status' のENUM値が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **column_name:** approval_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - APPROVED
  - PENDING
  - REJECTED

---

#### 31. ❌ カラム 'assignment_status' のENUM値が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **column_name:** assignment_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - PENDING

---

#### 32. ❌ カラム 'assignment_type' のENUM値が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **column_name:** assignment_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PRIMARY
  - SECONDARY
  - TEMPORARY

---

#### 33. ❌ UNIQUE制約 ['assignment_type', 'department_id', 'employee_id', 'start_date'] がYAMLにのみ存在します（DDLに定義が必要）

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** yaml_only_unique_constraint
- **constraint_columns:**
  - assignment_type
  - department_id
  - employee_id
  - start_date

---

#### 34. ❌ カラム 'assignment_reason' のENUM値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** assignment_reason
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NEW_HIRE
  - PROMOTION
  - TRANSFER
  - SKILL_DEVELOPMENT
  - PROJECT_NEED
  - REORGANIZATION

---

#### 35. ❌ カラム 'evaluation_frequency' のENUM値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** evaluation_frequency
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - MONTHLY
  - QUARTERLY
  - SEMI_ANNUAL
  - ANNUAL

---

#### 36. ❌ カラム 'proficiency_level' のENUM値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** proficiency_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NOVICE
  - BEGINNER
  - INTERMEDIATE
  - ADVANCED
  - EXPERT

---

#### 37. ❌ カラム 'performance_rating' のENUM値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** performance_rating
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - EXCELLENT
  - GOOD
  - SATISFACTORY
  - NEEDS_IMPROVEMENT
  - UNSATISFACTORY

---

#### 38. ❌ カラム 'assignment_status' のENUM値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** assignment_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - PENDING
  - SUSPENDED

---

#### 39. ❌ カラム 'target_proficiency_level' のENUM値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** target_proficiency_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NOVICE
  - BEGINNER
  - INTERMEDIATE
  - ADVANCED
  - EXPERT

---

#### 40. ❌ カラム 'assignment_type' のENUM値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** assignment_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PRIMARY
  - SECONDARY
  - TEMPORARY
  - TRAINING
  - CANDIDATE

---

#### 41. ❌ カラム 'approval_status' のENUM値が不一致

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **column_name:** approval_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - APPROVED
  - PENDING
  - REJECTED

---

#### 42. ❌ カラム 'appointment_status' のENUM値が不一致

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **column_name:** appointment_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - SUSPENDED

---

#### 43. ❌ カラム 'appointment_type' のENUM値が不一致

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **column_name:** appointment_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PRIMARY
  - ACTING
  - CONCURRENT

---

#### 44. ❌ UNIQUE制約 ['appointment_type', 'employee_id', 'position_id', 'start_date'] がYAMLにのみ存在します（DDLに定義が必要）

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** yaml_only_unique_constraint
- **constraint_columns:**
  - appointment_type
  - employee_id
  - position_id
  - start_date

---

#### 45. ❌ カラム 'travel_frequency' のENUM値が不一致

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** travel_frequency
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NONE
  - LOW
  - MEDIUM
  - HIGH

---

#### 46. ❌ カラム 'job_level' のENUM値が不一致

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** job_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - JUNIOR
  - SENIOR
  - LEAD
  - MANAGER
  - DIRECTOR

---

#### 47. ❌ カラム 'job_category' のENUM値が不一致

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** job_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ENGINEERING
  - MANAGEMENT
  - SALES
  - SUPPORT
  - OTHER

---

#### 48. ❌ カラム 'skill_priority' のENUM値が不一致

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** skill_priority
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CRITICAL
  - HIGH
  - MEDIUM
  - LOW

---

#### 49. ❌ カラム 'skill_status' のENUM値が不一致

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** skill_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - DEPRECATED
  - OBSOLETE

---

#### 50. ❌ カラム 'skill_category' のENUM値が不一致

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** skill_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - BUSINESS
  - MANAGEMENT
  - COMMUNICATION

---

#### 51. ❌ カラム 'grade_requirement_type' のENUM値が不一致

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** grade_requirement_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - MINIMUM
  - STANDARD
  - ADVANCED

---

#### 52. ❌ カラム 'grade_status' のENUM値が不一致

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** grade_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - DEPRECATED
  - OBSOLETE

---

#### 53. ❌ カラム 'evaluation_frequency' のENUM値が不一致

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** evaluation_frequency
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ANNUAL
  - SEMI_ANNUAL
  - QUARTERLY

---

#### 54. ❌ カラム 'frequency_type' のENUM値が不一致

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** frequency_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - IMMEDIATE
  - DAILY
  - WEEKLY
  - MONTHLY

---

#### 55. ❌ カラム 'notification_type' のENUM値が不一致

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** notification_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - EMAIL
  - SLACK
  - TEAMS
  - WEBHOOK

---

#### 56. ❌ カラム 'target_audience' のENUM値が不一致

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** target_audience
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ALL
  - MANAGER
  - EMPLOYEE
  - CUSTOM

---

#### 57. ❌ カラム 'priority_level' のENUM値が不一致

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** priority_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - HIGH
  - MEDIUM
  - LOW

---

#### 58. ❌ カラム 'notification_type' のENUM値が不一致

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **column_name:** notification_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - EMAIL
  - SLACK
  - TEAMS
  - WEBHOOK

---

#### 59. ❌ カラム 'format_type' のENUM値が不一致

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **column_name:** format_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PLAIN
  - HTML
  - MARKDOWN

---

#### 60. ❌ カラム 'action_type' のENUM値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** action_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CREATE
  - READ
  - UPDATE
  - DELETE
  - EXECUTE

---

#### 61. ❌ カラム 'permission_category' のENUM値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** permission_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SYSTEM
  - SCREEN
  - API
  - DATA
  - FUNCTION

---

#### 62. ❌ カラム 'permission_status' のENUM値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** permission_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - DEPRECATED

---

#### 63. ❌ カラム 'scope_level' のENUM値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** scope_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - GLOBAL
  - TENANT
  - DEPARTMENT
  - SELF

---

#### 64. ❌ カラム 'position_category' のENUM値が不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** position_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - EXECUTIVE
  - MANAGER
  - SUPERVISOR
  - STAFF

---

#### 65. ❌ カラム 'position_status' のENUM値が不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** position_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - ABOLISHED

---

#### 66. ❌ カラム 'output_format' のENUM値が不一致

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **column_name:** output_format
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PDF
  - EXCEL
  - CSV
  - HTML

---

#### 67. ❌ カラム 'report_category' のENUM値が不一致

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **column_name:** report_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SKILL
  - GOAL
  - EVALUATION
  - SUMMARY
  - ANALYTICS

---

#### 68. ❌ カラム 'role_status' のENUM値が不一致

**テーブル:** MST_Role

**詳細情報:**
- **column_name:** role_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - DEPRECATED

---

#### 69. ❌ カラム 'role_category' のENUM値が不一致

**テーブル:** MST_Role

**詳細情報:**
- **column_name:** role_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SYSTEM
  - BUSINESS
  - TENANT
  - CUSTOM

---

#### 70. ❌ カラム 'evaluation_method' のENUM値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** evaluation_method
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - LEVEL
  - SCORE
  - BINARY
  - CERTIFICATION

---

#### 71. ❌ カラム 'category_type' のENUM値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** category_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - BUSINESS
  - SOFT
  - CERTIFICATION
  - LANGUAGE

---

#### 72. ❌ カラム 'category_status' のENUM値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** category_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - DEPRECATED

---

#### 73. ❌ カラム 'project_complexity' のENUM値が不一致

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** project_complexity
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SIMPLE
  - MODERATE
  - COMPLEX
  - CRITICAL

---

#### 74. ❌ カラム 'leadership_level' のENUM値が不一致

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** leadership_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NONE
  - TEAM
  - PROJECT
  - ORGANIZATION

---

#### 75. ❌ カラム 'assessment_frequency' のENUM値が不一致

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** assessment_frequency
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ANNUAL
  - SEMI_ANNUAL
  - QUARTERLY
  - ON_DEMAND

---

#### 76. ❌ カラム 'requirement_category' のENUM値が不一致

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** requirement_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - BUSINESS
  - LEADERSHIP
  - COMMUNICATION

---

#### 77. ❌ カラム 'assessment_method' のENUM値が不一致

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** assessment_method
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - EXAM
  - PORTFOLIO
  - INTERVIEW
  - PROJECT
  - PEER_REVIEW

---

#### 78. ❌ カラム 'requirement_status' のENUM値が不一致

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** requirement_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - DEPRECATED
  - OBSOLETE

---

#### 79. ❌ UNIQUE制約 ['requirement_name', 'skill_grade_id'] がYAMLにのみ存在します（DDLに定義が必要）

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** yaml_only_unique_constraint
- **constraint_columns:**
  - requirement_name
  - skill_grade_id

---

#### 80. ❌ カラム 'skill_category' のENUM値が不一致

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **column_name:** skill_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - BUSINESS
  - CERTIFICATION
  - SOFT

---

#### 81. ❌ UNIQUE制約 ['parent_skill_id', 'skill_id'] がYAMLにのみ存在します（DDLに定義が必要）

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** yaml_only_unique_constraint
- **constraint_columns:**
  - parent_skill_id
  - skill_id

---

#### 82. ❌ カラム 'skill_type' のENUM値が不一致

**テーブル:** MST_SkillItem

**詳細情報:**
- **column_name:** skill_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - BUSINESS
  - CERTIFICATION

---

#### 83. ❌ カラム 'config_type' のENUM値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** config_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - STRING
  - INTEGER
  - DECIMAL
  - BOOLEAN
  - JSON
  - ENCRYPTED

---

#### 84. ❌ カラム 'environment' のENUM値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** environment
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - DEV
  - TEST
  - PROD
  - ALL

---

#### 85. ❌ カラム 'config_category' のENUM値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** config_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SECURITY
  - SYSTEM
  - BUSINESS
  - UI
  - INTEGRATION

---

#### 86. ❌ カラム 'tenant_type' のENUM値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** tenant_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ENTERPRISE
  - DEPARTMENT
  - SUBSIDIARY
  - PARTNER
  - TRIAL

---

#### 87. ❌ カラム 'status' のENUM値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - SUSPENDED
  - TRIAL
  - EXPIRED

---

#### 88. ❌ カラム 'billing_cycle' のENUM値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** billing_cycle
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - MONTHLY
  - QUARTERLY
  - ANNUAL

---

#### 89. ❌ カラム 'subscription_plan' のENUM値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** subscription_plan
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - FREE
  - BASIC
  - STANDARD
  - PREMIUM
  - ENTERPRISE

---

#### 90. ❌ カラム 'backup_frequency' のENUM値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** backup_frequency
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - DAILY
  - WEEKLY
  - MONTHLY

---

#### 91. ❌ カラム 'setting_category' のENUM値が不一致

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** setting_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SYSTEM
  - UI
  - BUSINESS
  - SECURITY
  - INTEGRATION

---

#### 92. ❌ カラム 'data_type' のENUM値が不一致

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** data_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - STRING
  - INTEGER
  - BOOLEAN
  - JSON
  - DECIMAL

---

#### 93. ❌ カラム 'target_audience' のENUM値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** target_audience
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ALL
  - NEW_HIRE
  - JUNIOR
  - MIDDLE
  - SENIOR
  - MANAGER
  - EXECUTIVE
  - SPECIALIST

---

#### 94. ❌ カラム 'program_category' のENUM値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** program_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - BUSINESS
  - MANAGEMENT
  - COMPLIANCE
  - SOFT_SKILL
  - CERTIFICATION
  - ORIENTATION

---

#### 95. ❌ カラム 'difficulty_level' のENUM値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** difficulty_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - BEGINNER
  - INTERMEDIATE
  - ADVANCED
  - EXPERT

---

#### 96. ❌ カラム 'program_type' のENUM値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** program_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CLASSROOM
  - ONLINE
  - BLENDED
  - OJT
  - SELF_STUDY
  - EXTERNAL

---

#### 97. ❌ カラム 'venue_type' のENUM値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** venue_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - INTERNAL
  - EXTERNAL
  - ONLINE
  - HYBRID

---

#### 98. ❌ カラム 'assessment_method' のENUM値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** assessment_method
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NONE
  - TEST
  - ASSIGNMENT
  - PRESENTATION
  - PRACTICAL
  - COMPREHENSIVE

---

#### 99. ❌ カラム 'language' のENUM値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** language
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - JA
  - EN
  - BILINGUAL

---

#### 100. ❌ カラム 'account_status' のENUM値が不一致

**テーブル:** MST_UserAuth

**詳細情報:**
- **column_name:** account_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - LOCKED
  - SUSPENDED

---

#### 101. ❌ カラム 'approval_status' のENUM値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** approval_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PENDING
  - APPROVED
  - REJECTED

---

#### 102. ❌ カラム 'assignment_status' のENUM値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** assignment_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - INACTIVE
  - SUSPENDED
  - EXPIRED

---

#### 103. ❌ カラム 'assignment_type' のENUM値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** assignment_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - DIRECT
  - INHERITED
  - DELEGATED
  - TEMPORARY

---

#### 104. ❌ UNIQUE制約 ['assignment_status', 'role_id', 'user_id'] がYAMLにのみ存在します（DDLに定義が必要）

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** yaml_only_unique_constraint
- **constraint_columns:**
  - assignment_status
  - role_id
  - user_id

---

#### 105. ❌ カラム 'backup_trigger' のENUM値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** backup_trigger
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SCHEDULED
  - MANUAL
  - EMERGENCY

---

#### 106. ❌ カラム 'compression_type' のENUM値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** compression_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NONE
  - GZIP
  - ZIP

---

#### 107. ❌ カラム 'backup_type' のENUM値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** backup_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - FULL
  - INCREMENTAL
  - DIFFERENTIAL

---

#### 108. ❌ カラム 'backup_status' のENUM値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** backup_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - RUNNING
  - SUCCESS
  - FAILED
  - CANCELLED

---

#### 109. ❌ カラム 'backup_scope' のENUM値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** backup_scope
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - DATABASE
  - TABLE
  - SCHEMA

---

#### 110. ❌ カラム 'integration_type' のENUM値が不一致

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** integration_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - WEBHOOK
  - API
  - OAUTH
  - SMTP

---

#### 111. ❌ カラム 'auth_type' のENUM値が不一致

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** auth_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NONE
  - BASIC
  - BEARER
  - OAUTH2
  - API_KEY

---

#### 112. ❌ カラム 'health_status' のENUM値が不一致

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** health_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - HEALTHY
  - UNHEALTHY
  - UNKNOWN

---

#### 113. ❌ カラム 'data_type' のENUM値が不一致

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** data_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - STRING
  - INTEGER
  - DECIMAL
  - BOOLEAN
  - JSON
  - DATE

---

#### 114. ❌ カラム 'index_type' のENUM値が不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** index_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - FULLTEXT
  - KEYWORD
  - CATEGORY
  - SYNONYM

---

#### 115. ❌ カラム 'source_field' のENUM値が不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** source_field
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NAME
  - DESCRIPTION
  - KEYWORD
  - CATEGORY

---

#### 116. ❌ カラム 'log_level' のENUM値が不一致

**テーブル:** SYS_SystemLog

**詳細情報:**
- **column_name:** log_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ERROR
  - WARN
  - INFO
  - DEBUG

---

#### 117. ❌ カラム 'token_type' のENUM値が不一致

**テーブル:** SYS_TokenStore

**詳細情報:**
- **column_name:** token_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACCESS
  - REFRESH
  - SESSION

---

#### 118. ❌ カラム 'revoked_reason' のENUM値が不一致

**テーブル:** SYS_TokenStore

**詳細情報:**
- **column_name:** revoked_reason
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - LOGOUT
  - EXPIRED
  - SECURITY
  - ADMIN

---

#### 119. ❌ UNIQUE制約 ['effective_date', 'employee_id', 'job_type_id'] がYAMLにのみ存在します（DDLに定義が必要）

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** yaml_only_unique_constraint
- **constraint_columns:**
  - effective_date
  - employee_id
  - job_type_id

---

#### 120. ❌ カラム 'priority_level' のENUM値が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** priority_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - HIGH
  - MEDIUM
  - LOW

---

#### 121. ❌ カラム 'approval_status' のENUM値が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** approval_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - DRAFT
  - PENDING
  - APPROVED
  - REJECTED

---

#### 122. ❌ カラム 'goal_category' のENUM値が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** goal_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - BUSINESS
  - SKILL
  - CAREER
  - PERSONAL

---

#### 123. ❌ カラム 'achievement_status' のENUM値が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** achievement_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - NOT_STARTED
  - IN_PROGRESS
  - COMPLETED
  - OVERDUE
  - CANCELLED

---

#### 124. ❌ カラム 'goal_type' のENUM値が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** goal_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - QUANTITATIVE
  - QUALITATIVE
  - MILESTONE

---

#### 125. ❌ カラム 'device_type' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** device_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PC
  - MOBILE
  - TABLET

---

#### 126. ❌ カラム 'notification_type' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** notification_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SYSTEM
  - REMINDER
  - APPROVAL
  - ALERT
  - INFO
  - URGENT

---

#### 127. ❌ カラム 'priority_level' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** priority_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - LOW
  - NORMAL
  - HIGH
  - CRITICAL

---

#### 128. ❌ カラム 'notification_category' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** notification_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SKILL
  - TRAINING
  - PROJECT
  - CERTIFICATION
  - SYSTEM
  - HR

---

#### 129. ❌ カラム 'read_status' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** read_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - UNREAD
  - READ
  - ARCHIVED

---

#### 130. ❌ カラム 'related_entity_type' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** related_entity_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PROJECT
  - TRAINING
  - CERTIFICATION
  - SKILL
  - EMPLOYEE

---

#### 131. ❌ カラム 'message_format' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** message_format
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PLAIN
  - HTML
  - MARKDOWN

---

#### 132. ❌ カラム 'delivery_method' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** delivery_method
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - IN_APP
  - EMAIL
  - SLACK
  - TEAMS
  - LINE_WORKS
  - SMS

---

#### 133. ❌ カラム 'delivery_status' のENUM値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** delivery_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PENDING
  - SENT
  - DELIVERED
  - FAILED
  - BOUNCED

---

#### 134. ❌ カラム 'approval_status' のENUM値が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** approval_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PENDING
  - APPROVED
  - REJECTED
  - UNDER_REVIEW

---

#### 135. ❌ カラム 'pdu_category' のENUM値が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** pdu_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - LEADERSHIP
  - STRATEGIC
  - BUSINESS

---

#### 136. ❌ カラム 'evidence_type' のENUM値が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** evidence_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CERTIFICATE
  - ATTENDANCE
  - RECEIPT
  - REPORT
  - OTHER

---

#### 137. ❌ カラム 'activity_type' のENUM値が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** activity_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TRAINING
  - CONFERENCE
  - SEMINAR
  - SELF_STUDY
  - TEACHING
  - VOLUNTEER
  - OTHER

---

#### 138. ❌ カラム 'cost_covered_by' のENUM値が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** cost_covered_by
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - COMPANY
  - EMPLOYEE
  - SHARED

---

#### 139. ❌ カラム 'project_scale' のENUM値が不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** project_scale
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SMALL
  - MEDIUM
  - LARGE
  - ENTERPRISE

---

#### 140. ❌ カラム 'project_status' のENUM値が不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** project_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ONGOING
  - COMPLETED
  - SUSPENDED
  - CANCELLED

---

#### 141. ❌ カラム 'budget_range' のENUM値が不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** budget_range
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - UNDER_1M
  - UNDER_10M
  - UNDER_100M
  - OVER_100M

---

#### 142. ❌ カラム 'project_type' のENUM値が不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** project_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - DEVELOPMENT
  - MAINTENANCE
  - CONSULTING
  - RESEARCH
  - OTHER

---

#### 143. ❌ カラム 'complexity_level' のENUM値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** complexity_level
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - LOW
  - MEDIUM
  - HIGH
  - VERY_HIGH

---

#### 144. ❌ カラム 'skill_level_demonstrated' のENUM値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** skill_level_demonstrated
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - BEGINNER
  - INTERMEDIATE
  - ADVANCED
  - EXPERT

---

#### 145. ❌ カラム 'verification_status' のENUM値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** verification_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PENDING
  - VERIFIED
  - REJECTED
  - EXPIRED

---

#### 146. ❌ カラム 'evidence_type' のENUM値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** evidence_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - CERTIFICATION
  - PROJECT
  - TRAINING
  - PORTFOLIO
  - PEER_REVIEW
  - SELF_ASSESSMENT
  - OTHER

---

#### 147. ❌ カラム 'verification_method' のENUM値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** verification_method
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - AUTOMATIC
  - MANUAL
  - PEER
  - MANAGER
  - EXTERNAL

---

#### 148. ❌ カラム 'file_type' のENUM値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** file_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PDF
  - IMAGE
  - VIDEO
  - DOCUMENT
  - URL
  - OTHER

---

#### 149. ❌ カラム 'issuer_type' のENUM値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** issuer_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - COMPANY
  - EDUCATIONAL
  - CERTIFICATION_BODY
  - GOVERNMENT
  - COMMUNITY
  - OTHER

---

#### 150. ❌ カラム 'skill_status' のENUM値が不一致

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** skill_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - ACTIVE
  - EXPIRED
  - SUSPENDED

---

#### 151. ❌ カラム 'training_type' のENUM値が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** training_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - INTERNAL
  - EXTERNAL
  - ONLINE
  - CERTIFICATION
  - CONFERENCE

---

#### 152. ❌ カラム 'attendance_status' のENUM値が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** attendance_status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - COMPLETED
  - PARTIAL
  - ABSENT
  - CANCELLED

---

#### 153. ❌ カラム 'training_category' のENUM値が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** training_category
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - TECHNICAL
  - BUSINESS
  - MANAGEMENT
  - SOFT_SKILL
  - COMPLIANCE

---

#### 154. ❌ カラム 'cost_covered_by' のENUM値が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** cost_covered_by
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - COMPANY
  - EMPLOYEE
  - SHARED

---

#### 155. ❌ カラム 'status' のENUM値が不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** status
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - PENDING
  - RUNNING
  - COMPLETED
  - FAILED
  - CANCELLED

---

#### 156. ❌ カラム 'job_type' のENUM値が不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** job_type
- **issue_type:** enum_values_mismatch
- **ddl_enum_values:** なし
- **yaml_enum_values:**
  - SKILL_IMPORT
  - EMPLOYEE_IMPORT
  - BULK_UPDATE
  - BULK_DELETE
  - DATA_EXPORT

---

#### 157. ⚠️ カラム 'is_deleted' のデフォルト値が不一致

**テーブル:** HIS_AuditLog

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 158. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 159. ⚠️ カラム 'max_retry_count' のデフォルト値が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** max_retry_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 3
- **yaml_default:** 3

---

#### 160. ⚠️ カラム 'send_attempts' のデフォルト値が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **column_name:** send_attempts
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 161. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 162. ⚠️ カラム 'tax_rate' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** tax_rate
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,3

---

#### 163. ⚠️ カラム 'base_amount' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** base_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 12,2

---

#### 164. ⚠️ カラム 'base_amount' のデフォルト値が不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** base_amount
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 165. ⚠️ カラム 'total_amount' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** total_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 12,2

---

#### 166. ⚠️ カラム 'usage_amount' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** usage_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 12,2

---

#### 167. ⚠️ カラム 'usage_amount' のデフォルト値が不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** usage_amount
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 168. ⚠️ カラム 'discount_amount' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** discount_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 12,2

---

#### 169. ⚠️ カラム 'discount_amount' のデフォルト値が不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** discount_amount
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 170. ⚠️ カラム 'tax_amount' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** tax_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 12,2

---

#### 171. ⚠️ カラム 'additional_amount' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** additional_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 12,2

---

#### 172. ⚠️ カラム 'additional_amount' のデフォルト値が不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** additional_amount
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 173. ⚠️ カラム 'subtotal_amount' の長さが不一致

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **column_name:** subtotal_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 12,2

---

#### 174. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 175. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 176. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 177. ⚠️ カラム 'budget_allocated' の長さが不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** budget_allocated
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 178. ⚠️ カラム 'progress_percentage' の長さが不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** progress_percentage
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 179. ⚠️ カラム 'progress_percentage' のデフォルト値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** progress_percentage
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 180. ⚠️ カラム 'budget_used' の長さが不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** budget_used
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 181. ⚠️ カラム 'budget_used' のデフォルト値が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **column_name:** budget_used
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 182. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 183. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 184. ⚠️ カラム 'renewal_required' のデフォルト値が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** renewal_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 185. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 186. ⚠️ カラム 'exam_fee' の長さが不一致

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** exam_fee
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 187. ⚠️ カラム 'is_recommended' のデフォルト値が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **column_name:** is_recommended
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 188. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 189. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 190. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 191. ⚠️ カラム 'average_study_hours' の長さが不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** average_study_hours
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 6,2

---

#### 192. ⚠️ カラム 'priority_order' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** priority_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 1
- **yaml_default:** 1

---

#### 193. ⚠️ カラム 'client_requirement' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** client_requirement
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 194. ⚠️ カラム 'internal_policy' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** internal_policy
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 195. ⚠️ カラム 'study_time_allocation' の長さが不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** study_time_allocation
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 196. ⚠️ カラム 'success_rate' の長さが不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** success_rate
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 197. ⚠️ カラム 'renewal_required' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** renewal_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 198. ⚠️ カラム 'cost_support_available' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** cost_support_available
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 199. ⚠️ カラム 'active_flag' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** active_flag
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 200. ⚠️ カラム 'compliance_requirement' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** compliance_requirement
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 201. ⚠️ カラム 'cost_support_amount' の長さが不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** cost_support_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 202. ⚠️ カラム 'training_support_available' のデフォルト値が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **column_name:** training_support_available
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 203. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_Department

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 204. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_Department

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 205. ⚠️ カラム 'budget_amount' の長さが不一致

**テーブル:** MST_Department

**詳細情報:**
- **column_name:** budget_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 206. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_Employee

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 207. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_Employee

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 208. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_Employee

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 209. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 210. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 211. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 212. ⚠️ カラム 'assignment_ratio' の長さが不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **column_name:** assignment_ratio
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 213. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 214. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 215. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 216. ⚠️ カラム 'remote_work_eligible' のデフォルト値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** remote_work_eligible
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 217. ⚠️ カラム 'billable_flag' のデフォルト値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** billable_flag
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 218. ⚠️ カラム 'travel_required' のデフォルト値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** travel_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 219. ⚠️ カラム 'assignment_ratio' の長さが不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** assignment_ratio
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 220. ⚠️ カラム 'assignment_ratio' のデフォルト値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** assignment_ratio
- **issue_type:** default_value_mismatch
- **ddl_default:** 100.0
- **yaml_default:** 100.0

---

#### 221. ⚠️ カラム 'budget_allocation' の長さが不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** budget_allocation
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 222. ⚠️ カラム 'hourly_rate' の長さが不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** hourly_rate
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 8,2

---

#### 223. ⚠️ カラム 'overtime_eligible' のデフォルト値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** overtime_eligible
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 224. ⚠️ カラム 'security_clearance_required' のデフォルト値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** security_clearance_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 225. ⚠️ カラム 'workload_percentage' の長さが不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** workload_percentage
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 226. ⚠️ カラム 'workload_percentage' のデフォルト値が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **column_name:** workload_percentage
- **issue_type:** default_value_mismatch
- **ddl_default:** 100.0
- **yaml_default:** 100.0

---

#### 227. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 228. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 229. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 230. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 231. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 232. ⚠️ カラム 'remote_work_eligible' のデフォルト値が不一致

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** remote_work_eligible
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 233. ⚠️ カラム 'sort_order' のデフォルト値が不一致

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** sort_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 234. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** MST_JobType

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 235. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 236. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 237. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 238. ⚠️ カラム 'experience_years' の長さが不一致

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** experience_years
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 4,1

---

#### 239. ⚠️ カラム 'certification_required' のデフォルト値が不一致

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** certification_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 240. ⚠️ カラム 'skill_weight' の長さが不一致

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **column_name:** skill_weight
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 241. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 242. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 243. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 244. ⚠️ カラム 'salary_range_max' の長さが不一致

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** salary_range_max
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,0

---

#### 245. ⚠️ カラム 'salary_range_min' の長さが不一致

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** salary_range_min
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,0

---

#### 246. ⚠️ カラム 'required_experience_years' の長さが不一致

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **column_name:** required_experience_years
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 4,1

---

#### 247. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 248. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 249. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 250. ⚠️ カラム 'is_enabled' のデフォルト値が不一致

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **column_name:** is_enabled
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 251. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 252. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 253. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 254. ⚠️ カラム 'is_default' のデフォルト値が不一致

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **column_name:** is_default
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 255. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 256. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 257. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 258. ⚠️ カラム 'requires_approval' のデフォルト値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** requires_approval
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 259. ⚠️ カラム 'is_system_permission' のデフォルト値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** is_system_permission
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 260. ⚠️ カラム 'risk_level' のデフォルト値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** risk_level
- **issue_type:** default_value_mismatch
- **ddl_default:** 1
- **yaml_default:** 1

---

#### 261. ⚠️ カラム 'audit_required' のデフォルト値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** audit_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 262. ⚠️ カラム 'requires_conditions' のデフォルト値が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **column_name:** requires_conditions
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 263. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 264. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 265. ⚠️ カラム 'approval_limit' の長さが不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** approval_limit
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 266. ⚠️ カラム 'is_executive' のデフォルト値が不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** is_executive
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 267. ⚠️ カラム 'can_hire' のデフォルト値が不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** can_hire
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 268. ⚠️ カラム 'is_management' のデフォルト値が不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** is_management
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 269. ⚠️ カラム 'requires_approval' のデフォルト値が不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** requires_approval
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 270. ⚠️ カラム 'allowance_amount' の長さが不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** allowance_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 271. ⚠️ カラム 'can_evaluate' のデフォルト値が不一致

**テーブル:** MST_Position

**詳細情報:**
- **column_name:** can_evaluate
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 272. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 273. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 274. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 275. ⚠️ カラム 'is_default' のデフォルト値が不一致

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **column_name:** is_default
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 276. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 277. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_Role

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 278. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_Role

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 279. ⚠️ カラム 'is_system_role' のデフォルト値が不一致

**テーブル:** MST_Role

**詳細情報:**
- **column_name:** is_system_role
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 280. ⚠️ カラム 'is_tenant_specific' のデフォルト値が不一致

**テーブル:** MST_Role

**詳細情報:**
- **column_name:** is_tenant_specific
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 281. ⚠️ カラム 'role_priority' のデフォルト値が不一致

**テーブル:** MST_Role

**詳細情報:**
- **column_name:** role_priority
- **issue_type:** default_value_mismatch
- **ddl_default:** 999
- **yaml_default:** 999

---

#### 282. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 283. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 284. ⚠️ カラム 'is_leaf_category' のデフォルト値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** is_leaf_category
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 285. ⚠️ カラム 'is_system_category' のデフォルト値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** is_system_category
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 286. ⚠️ カラム 'category_level' のデフォルト値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** category_level
- **issue_type:** default_value_mismatch
- **ddl_default:** 1
- **yaml_default:** 1

---

#### 287. ⚠️ カラム 'skill_count' のデフォルト値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** skill_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 288. ⚠️ カラム 'display_order' のデフォルト値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** display_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 999
- **yaml_default:** 999

---

#### 289. ⚠️ カラム 'is_popular' のデフォルト値が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **column_name:** is_popular
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 290. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 291. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 292. ⚠️ カラム 'mentoring_capability' のデフォルト値が不一致

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** mentoring_capability
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 293. ⚠️ カラム 'promotion_eligibility' のデフォルト値が不一致

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** promotion_eligibility
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 294. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 295. ⚠️ カラム 'salary_impact_factor' の長さが不一致

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** salary_impact_factor
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 3,2

---

#### 296. ⚠️ カラム 'sort_order' のデフォルト値が不一致

**テーブル:** MST_SkillGrade

**詳細情報:**
- **column_name:** sort_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 297. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 298. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 299. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 300. ⚠️ カラム 'minimum_score' の長さが不一致

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** minimum_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 301. ⚠️ カラム 'weight_percentage' の長さが不一致

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **column_name:** weight_percentage
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 302. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 303. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 304. ⚠️ カラム 'is_leaf' のデフォルト値が不一致

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **column_name:** is_leaf
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 305. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 306. ⚠️ カラム 'sort_order' のデフォルト値が不一致

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **column_name:** sort_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 307. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_SkillItem

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 308. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_SkillItem

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 309. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_SkillItem

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 310. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 311. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 312. ⚠️ カラム 'tenant_specific' のデフォルト値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** tenant_specific
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 313. ⚠️ カラム 'is_user_configurable' のデフォルト値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** is_user_configurable
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 314. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 315. ⚠️ カラム 'sort_order' のデフォルト値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** sort_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 316. ⚠️ カラム 'is_encrypted' のデフォルト値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** is_encrypted
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 317. ⚠️ カラム 'requires_restart' のデフォルト値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** requires_restart
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 318. ⚠️ カラム 'is_system_only' のデフォルト値が不一致

**テーブル:** MST_SystemConfig

**詳細情報:**
- **column_name:** is_system_only
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 319. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 320. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 321. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 322. ⚠️ カラム 'tenant_level' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** tenant_level
- **issue_type:** default_value_mismatch
- **ddl_default:** 1
- **yaml_default:** 1

---

#### 323. ⚠️ カラム 'max_storage_gb' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** max_storage_gb
- **issue_type:** default_value_mismatch
- **ddl_default:** 10
- **yaml_default:** 10

---

#### 324. ⚠️ カラム 'current_users_count' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** current_users_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 325. ⚠️ カラム 'monthly_fee' の長さが不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** monthly_fee
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 326. ⚠️ カラム 'data_retention_days' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** data_retention_days
- **issue_type:** default_value_mismatch
- **ddl_default:** 2555
- **yaml_default:** 2555

---

#### 327. ⚠️ カラム 'sso_enabled' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** sso_enabled
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 328. ⚠️ カラム 'max_users' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** max_users
- **issue_type:** default_value_mismatch
- **ddl_default:** 100
- **yaml_default:** 100

---

#### 329. ⚠️ カラム 'api_rate_limit' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** api_rate_limit
- **issue_type:** default_value_mismatch
- **ddl_default:** 1000
- **yaml_default:** 1000

---

#### 330. ⚠️ カラム 'setup_fee' の長さが不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** setup_fee
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 331. ⚠️ カラム 'backup_enabled' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** backup_enabled
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 332. ⚠️ カラム 'storage_used_gb' の長さが不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** storage_used_gb
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,3

---

#### 333. ⚠️ カラム 'storage_used_gb' のデフォルト値が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **column_name:** storage_used_gb
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 334. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 335. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 336. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 337. ⚠️ カラム 'display_order' のデフォルト値が不一致

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** display_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 338. ⚠️ カラム 'is_system_managed' のデフォルト値が不一致

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** is_system_managed
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 339. ⚠️ カラム 'is_user_configurable' のデフォルト値が不一致

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** is_user_configurable
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 340. ⚠️ カラム 'is_required' のデフォルト値が不一致

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** is_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 341. ⚠️ カラム 'is_encrypted' のデフォルト値が不一致

**テーブル:** MST_TenantSettings

**詳細情報:**
- **column_name:** is_encrypted
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 342. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 343. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 344. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 345. ⚠️ カラム 'mandatory_flag' のデフォルト値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** mandatory_flag
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 346. ⚠️ カラム 'pdu_credits' の長さが不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** pdu_credits
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 347. ⚠️ カラム 'passing_score' の長さが不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** passing_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 348. ⚠️ カラム 'certification_provided' のデフォルト値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** certification_provided
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 349. ⚠️ カラム 'active_flag' のデフォルト値が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** active_flag
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 350. ⚠️ カラム 'cost_per_participant' の長さが不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** cost_per_participant
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 351. ⚠️ カラム 'duration_hours' の長さが不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **column_name:** duration_hours
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 352. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_UserAuth

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 353. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_UserAuth

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 354. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_UserAuth

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 355. ⚠️ カラム 'failed_login_count' のデフォルト値が不一致

**テーブル:** MST_UserAuth

**詳細情報:**
- **column_name:** failed_login_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 356. ⚠️ カラム 'mfa_enabled' のデフォルト値が不一致

**テーブル:** MST_UserAuth

**詳細情報:**
- **column_name:** mfa_enabled
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 357. ⚠️ カラム 'code' がDDLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** code
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(20) NOT NULL

---

#### 358. ⚠️ カラム 'description' がDDLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** description
- **issue_type:** ddl_only_column
- **ddl_definition:** TEXT

---

#### 359. ⚠️ カラム 'name' がDDLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** name
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(100) NOT NULL

---

#### 360. ⚠️ カラム 'priority_order' のデフォルト値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** priority_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 999
- **yaml_default:** 999

---

#### 361. ⚠️ カラム 'requires_approval' のデフォルト値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** requires_approval
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 362. ⚠️ カラム 'auto_assigned' のデフォルト値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** auto_assigned
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 363. ⚠️ カラム 'is_primary_role' のデフォルト値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** is_primary_role
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 364. ⚠️ カラム 'usage_count' のデフォルト値が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **column_name:** usage_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 365. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 366. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 367. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 368. ⚠️ カラム 'encryption_enabled' のデフォルト値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** encryption_enabled
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 369. ⚠️ カラム 'retention_period_days' のデフォルト値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** retention_period_days
- **issue_type:** default_value_mismatch
- **ddl_default:** 30
- **yaml_default:** 30

---

#### 370. ⚠️ カラム 'recovery_tested' のデフォルト値が不一致

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **column_name:** recovery_tested
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 371. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 372. ⚠️ カラム 'is_enabled' のデフォルト値が不一致

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** is_enabled
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 373. ⚠️ カラム 'timeout_seconds' のデフォルト値が不一致

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** timeout_seconds
- **issue_type:** default_value_mismatch
- **ddl_default:** 30
- **yaml_default:** 30

---

#### 374. ⚠️ カラム 'retry_interval' のデフォルト値が不一致

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** retry_interval
- **issue_type:** default_value_mismatch
- **ddl_default:** 5
- **yaml_default:** 5

---

#### 375. ⚠️ カラム 'retry_count' のデフォルト値が不一致

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **column_name:** retry_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 3
- **yaml_default:** 3

---

#### 376. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 377. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 378. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 379. ⚠️ カラム 'is_editable' のデフォルト値が不一致

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** is_editable
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 380. ⚠️ カラム 'display_order' のデフォルト値が不一致

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** display_order
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 381. ⚠️ カラム 'version' のデフォルト値が不一致

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** version
- **issue_type:** default_value_mismatch
- **ddl_default:** 1
- **yaml_default:** 1

---

#### 382. ⚠️ カラム 'is_system_managed' のデフォルト値が不一致

**テーブル:** SYS_MasterData

**詳細情報:**
- **column_name:** is_system_managed
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 383. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 384. ⚠️ カラム 'position_weight' の長さが不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** position_weight
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,3

---

#### 385. ⚠️ カラム 'position_weight' のデフォルト値が不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** position_weight
- **issue_type:** default_value_mismatch
- **ddl_default:** 1.0
- **yaml_default:** 1.0

---

#### 386. ⚠️ カラム 'is_active' のデフォルト値が不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** is_active
- **issue_type:** default_value_mismatch
- **ddl_default:** True
- **yaml_default:** True

---

#### 387. ⚠️ カラム 'search_count' のデフォルト値が不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** search_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 388. ⚠️ カラム 'frequency_weight' の長さが不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** frequency_weight
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,3

---

#### 389. ⚠️ カラム 'frequency_weight' のデフォルト値が不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** frequency_weight
- **issue_type:** default_value_mismatch
- **ddl_default:** 1.0
- **yaml_default:** 1.0

---

#### 390. ⚠️ カラム 'relevance_score' の長さが不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** relevance_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,3

---

#### 391. ⚠️ カラム 'relevance_score' のデフォルト値が不一致

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **column_name:** relevance_score
- **issue_type:** default_value_mismatch
- **ddl_default:** 1.0
- **yaml_default:** 1.0

---

#### 392. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 393. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 394. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 395. ⚠️ カラム 'skill_level' のデフォルト値が不一致

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **column_name:** skill_level
- **issue_type:** default_value_mismatch
- **ddl_default:** 1
- **yaml_default:** 1

---

#### 396. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** SYS_SystemLog

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 397. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_SystemLog

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 398. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** SYS_SystemLog

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 399. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 400. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 401. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 402. ⚠️ カラム 'error_count' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** error_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 403. ⚠️ カラム 'skill_assessments' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** skill_assessments
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 404. ⚠️ カラム 'uptime_percentage' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** uptime_percentage
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 405. ⚠️ カラム 'uptime_percentage' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** uptime_percentage
- **issue_type:** default_value_mismatch
- **ddl_default:** 100.0
- **yaml_default:** 100.0

---

#### 406. ⚠️ カラム 'active_users' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** active_users
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 407. ⚠️ カラム 'backup_storage_mb' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** backup_storage_mb
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 408. ⚠️ カラム 'backup_storage_mb' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** backup_storage_mb
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 409. ⚠️ カラム 'data_storage_mb' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** data_storage_mb
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 410. ⚠️ カラム 'data_storage_mb' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** data_storage_mb
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 411. ⚠️ カラム 'notification_sent' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** notification_sent
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 412. ⚠️ カラム 'cpu_usage_minutes' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** cpu_usage_minutes
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 413. ⚠️ カラム 'cpu_usage_minutes' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** cpu_usage_minutes
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 414. ⚠️ カラム 'peak_concurrent_users' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** peak_concurrent_users
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 415. ⚠️ カラム 'report_generations' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** report_generations
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 416. ⚠️ カラム 'file_storage_mb' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** file_storage_mb
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 417. ⚠️ カラム 'file_storage_mb' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** file_storage_mb
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 418. ⚠️ カラム 'billing_amount' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** billing_amount
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 419. ⚠️ カラム 'response_time_avg_ms' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** response_time_avg_ms
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 8,2

---

#### 420. ⚠️ カラム 'network_transfer_mb' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** network_transfer_mb
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 421. ⚠️ カラム 'network_transfer_mb' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** network_transfer_mb
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 422. ⚠️ カラム 'total_logins' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** total_logins
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 423. ⚠️ カラム 'memory_usage_mb_hours' の長さが不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** memory_usage_mb_hours
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 424. ⚠️ カラム 'memory_usage_mb_hours' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** memory_usage_mb_hours
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 425. ⚠️ カラム 'api_requests' のデフォルト値が不一致

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **column_name:** api_requests
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 426. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** SYS_TokenStore

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 427. ⚠️ カラム 'is_revoked' のデフォルト値が不一致

**テーブル:** SYS_TokenStore

**詳細情報:**
- **column_name:** is_revoked
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 428. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 429. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 430. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 431. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 432. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 433. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 434. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 435. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 436. ⚠️ カラム 'certification_flag' のデフォルト値が不一致

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **column_name:** certification_flag
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 437. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 438. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 439. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 440. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 441. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 442. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 443. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 444. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 445. ⚠️ カラム 'target_value' の長さが不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** target_value
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 446. ⚠️ カラム 'progress_rate' の長さが不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** progress_rate
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 447. ⚠️ カラム 'progress_rate' のデフォルト値が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** progress_rate
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 448. ⚠️ カラム 'achievement_rate' の長さが不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** achievement_rate
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 449. ⚠️ カラム 'current_value' の長さが不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **column_name:** current_value
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 15,2

---

#### 450. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 451. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 452. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 453. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 454. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 455. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 456. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 457. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 458. ⚠️ カラム 'max_retry_count' のデフォルト値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** max_retry_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 3
- **yaml_default:** 3

---

#### 459. ⚠️ カラム 'is_bulk_notification' のデフォルト値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** is_bulk_notification
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 460. ⚠️ カラム 'retry_count' のデフォルト値が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **column_name:** retry_count
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 461. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 462. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 463. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 464. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 465. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 466. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 467. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 468. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 469. ⚠️ カラム 'pdu_points' の長さが不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** pdu_points
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,1

---

#### 470. ⚠️ カラム 'cost' の長さが不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** cost
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 471. ⚠️ カラム 'duration_hours' の長さが不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** duration_hours
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,1

---

#### 472. ⚠️ カラム 'is_recurring' のデフォルト値が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **column_name:** is_recurring
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 473. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 474. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 475. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 476. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 477. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 478. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 479. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 480. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 481. ⚠️ カラム 'is_confidential' のデフォルト値が不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** is_confidential
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 482. ⚠️ カラム 'evaluation_score' の長さが不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** evaluation_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 3,1

---

#### 483. ⚠️ カラム 'is_public_reference' のデフォルト値が不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** is_public_reference
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 484. ⚠️ カラム 'participation_rate' の長さが不一致

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **column_name:** participation_rate
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 485. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 486. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 487. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 488. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 489. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 490. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 491. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 492. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 493. ⚠️ カラム 'is_public' のデフォルト値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** is_public
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 494. ⚠️ カラム 'is_portfolio_item' のデフォルト値が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** is_portfolio_item
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 495. ⚠️ カラム 'impact_score' の長さが不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **column_name:** impact_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 3,1

---

#### 496. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 497. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 498. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 499. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 500. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 501. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 502. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 503. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 504. ⚠️ カラム 'updated_at' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** updated_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 505. ⚠️ カラム 'updated_by' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** updated_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 506. ⚠️ カラム 'created_at' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** created_at
- **issue_type:** ddl_only_column
- **ddl_definition:** TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP

---

#### 507. ⚠️ カラム 'tenant_id' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** tenant_id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 508. ⚠️ カラム 'created_by' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** created_by
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 509. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 510. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 511. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 512. ⚠️ カラム 'manager_approval' のデフォルト値が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** manager_approval
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 513. ⚠️ カラム 'satisfaction_score' の長さが不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** satisfaction_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 3,1

---

#### 514. ⚠️ カラム 'certificate_obtained' のデフォルト値が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** certificate_obtained
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 515. ⚠️ カラム 'pdu_earned' の長さが不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** pdu_earned
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,1

---

#### 516. ⚠️ カラム 'recommendation_score' の長さが不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** recommendation_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 3,1

---

#### 517. ⚠️ カラム 'cost' の長さが不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** cost
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 10,2

---

#### 518. ⚠️ カラム 'completion_rate' の長さが不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** completion_rate
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 519. ⚠️ カラム 'follow_up_required' のデフォルト値が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** follow_up_required
- **issue_type:** default_value_mismatch
- **ddl_default:** False
- **yaml_default:** False

---

#### 520. ⚠️ カラム 'test_score' の長さが不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** test_score
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 521. ⚠️ カラム 'duration_hours' の長さが不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **column_name:** duration_hours
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,1

---

#### 522. ⚠️ カラム 'PRIMARY' がDDLにのみ存在します

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** PRIMARY
- **issue_type:** ddl_only_column
- **ddl_definition:** KEY

---

#### 523. ⚠️ カラム 'is_deleted' がDDLにのみ存在します

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** is_deleted
- **issue_type:** ddl_only_column
- **ddl_definition:** BOOLEAN NOT NULL DEFAULT False

---

#### 524. ⚠️ カラム 'id' がDDLにのみ存在します

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** id
- **issue_type:** ddl_only_column
- **ddl_definition:** VARCHAR(50) NOT NULL

---

#### 525. ⚠️ カラム 'success_records' のデフォルト値が不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** success_records
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 526. ⚠️ カラム 'progress_percentage' の長さが不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** progress_percentage
- **issue_type:** length_mismatch
- **ddl_length:** None
- **yaml_length:** 5,2

---

#### 527. ⚠️ カラム 'progress_percentage' のデフォルト値が不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** progress_percentage
- **issue_type:** default_value_mismatch
- **ddl_default:** 0.0
- **yaml_default:** 0.0

---

#### 528. ⚠️ カラム 'total_records' のデフォルト値が不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** total_records
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 529. ⚠️ カラム 'error_records' のデフォルト値が不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** error_records
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0

---

#### 530. ⚠️ カラム 'processed_records' のデフォルト値が不一致

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **column_name:** processed_records
- **issue_type:** default_value_mismatch
- **ddl_default:** 0
- **yaml_default:** 0


### 🔍 外部キー整合性 (364件)

#### 1. ❌ 外部キー fk_his_auditlog_tenant の参照先カラム MST_Tenant.id が存在しません

**テーブル:** HIS_AuditLog

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_his_auditlog_tenant
- **target_table:** MST_Tenant
- **target_column:** id
- **available_columns:**
  - tenant_id
  - tenant_code
  - tenant_name
  - tenant_name_en
  - tenant_short_name
  - tenant_type
  - parent_tenant_id
  - tenant_level
  - domain_name
  - subdomain
  - logo_url
  - primary_color
  - secondary_color
  - timezone
  - locale
  - currency_code
  - date_format
  - time_format
  - admin_email
  - contact_email
  - phone_number
  - address
  - postal_code
  - country_code
  - subscription_plan
  - max_users
  - max_storage_gb
  - features_enabled
  - custom_settings
  - security_policy
  - data_retention_days
  - backup_enabled
  - backup_frequency
  - contract_start_date
  - contract_end_date
  - trial_end_date
  - billing_cycle
  - monthly_fee
  - setup_fee
  - status
  - activation_date
  - suspension_date
  - suspension_reason
  - last_login_date
  - current_users_count
  - storage_used_gb
  - api_rate_limit
  - sso_enabled
  - sso_provider
  - sso_config
  - webhook_url
  - webhook_secret
  - created_by
  - notes
  - code
  - name
  - description

---

#### 2. ❌ 外部キー fk_his_auditlog_user の参照先カラム MST_Employee.id が存在しません

**テーブル:** HIS_AuditLog

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_his_auditlog_user
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 3. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 4. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 5. ❌ 外部キー fk_tenant_billing_tenant の参照先カラム MST_Tenant.id が存在しません

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_tenant_billing_tenant
- **target_table:** MST_Tenant
- **target_column:** id
- **available_columns:**
  - tenant_id
  - tenant_code
  - tenant_name
  - tenant_name_en
  - tenant_short_name
  - tenant_type
  - parent_tenant_id
  - tenant_level
  - domain_name
  - subdomain
  - logo_url
  - primary_color
  - secondary_color
  - timezone
  - locale
  - currency_code
  - date_format
  - time_format
  - admin_email
  - contact_email
  - phone_number
  - address
  - postal_code
  - country_code
  - subscription_plan
  - max_users
  - max_storage_gb
  - features_enabled
  - custom_settings
  - security_policy
  - data_retention_days
  - backup_enabled
  - backup_frequency
  - contract_start_date
  - contract_end_date
  - trial_end_date
  - billing_cycle
  - monthly_fee
  - setup_fee
  - status
  - activation_date
  - suspension_date
  - suspension_reason
  - last_login_date
  - current_users_count
  - storage_used_gb
  - api_rate_limit
  - sso_enabled
  - sso_provider
  - sso_config
  - webhook_url
  - webhook_secret
  - created_by
  - notes
  - code
  - name
  - description

---

#### 6. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 7. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 8. ❌ 外部キー fk_career_plan_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_career_plan_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 9. ❌ 外部キー fk_career_plan_target_position の参照先カラム MST_Position.id が存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_career_plan_target_position
- **target_table:** MST_Position
- **target_column:** id
- **available_columns:**
  - position_code
  - position_name
  - position_name_short
  - position_level
  - position_rank
  - position_category
  - authority_level
  - approval_limit
  - salary_grade
  - allowance_amount
  - is_management
  - is_executive
  - requires_approval
  - can_hire
  - can_evaluate
  - position_status
  - sort_order
  - description
  - code
  - name

---

#### 10. ❌ 外部キー fk_career_plan_target_job_type の参照先カラム MST_JobType.id が存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_career_plan_target_job_type
- **target_table:** MST_JobType
- **target_column:** id
- **available_columns:**
  - job_type_code
  - job_type_name
  - job_type_name_en
  - job_category
  - job_level
  - description
  - required_experience_years
  - salary_grade_min
  - salary_grade_max
  - career_path
  - required_certifications
  - required_skills
  - department_affinity
  - remote_work_eligible
  - travel_frequency
  - sort_order
  - is_active
  - code
  - name

---

#### 11. ❌ 外部キー fk_career_plan_target_department の参照先カラム MST_Department.id が存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_career_plan_target_department
- **target_table:** MST_Department
- **target_column:** id
- **available_columns:**
  - department_code
  - department_name
  - department_name_short
  - parent_department_id
  - department_level
  - department_type
  - manager_id
  - deputy_manager_id
  - cost_center_code
  - budget_amount
  - location
  - phone_number
  - email_address
  - establishment_date
  - abolition_date
  - department_status
  - sort_order
  - description
  - code
  - name

---

#### 12. ❌ 外部キー fk_career_plan_mentor の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_career_plan_mentor
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 13. ❌ 外部キー fk_career_plan_supervisor の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_career_plan_supervisor
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 14. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 15. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 16. ❌ 外部キー fk_certification_skill_category の参照先カラム MST_SkillCategory.id が存在しません

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_certification_skill_category
- **target_table:** MST_SkillCategory
- **target_column:** id
- **available_columns:**
  - category_code
  - category_name
  - category_name_short
  - category_name_en
  - category_type
  - parent_category_id
  - category_level
  - category_path
  - is_system_category
  - is_leaf_category
  - skill_count
  - evaluation_method
  - max_level
  - icon_url
  - color_code
  - display_order
  - is_popular
  - category_status
  - effective_from
  - effective_to
  - description
  - code
  - name

---

#### 17. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 18. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 19. ❌ 外部キー fk_cert_req_target_job_type の参照先カラム MST_JobType.id が存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_cert_req_target_job_type
- **target_table:** MST_JobType
- **target_column:** id
- **available_columns:**
  - job_type_code
  - job_type_name
  - job_type_name_en
  - job_category
  - job_level
  - description
  - required_experience_years
  - salary_grade_min
  - salary_grade_max
  - career_path
  - required_certifications
  - required_skills
  - department_affinity
  - remote_work_eligible
  - travel_frequency
  - sort_order
  - is_active
  - code
  - name

---

#### 20. ❌ 外部キー fk_cert_req_target_position の参照先カラム MST_Position.id が存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_cert_req_target_position
- **target_table:** MST_Position
- **target_column:** id
- **available_columns:**
  - position_code
  - position_name
  - position_name_short
  - position_level
  - position_rank
  - position_category
  - authority_level
  - approval_limit
  - salary_grade
  - allowance_amount
  - is_management
  - is_executive
  - requires_approval
  - can_hire
  - can_evaluate
  - position_status
  - sort_order
  - description
  - code
  - name

---

#### 21. ❌ 外部キー fk_cert_req_target_skill_grade の参照先カラム MST_SkillGrade.id が存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_cert_req_target_skill_grade
- **target_table:** MST_SkillGrade
- **target_column:** id
- **available_columns:**
  - grade_code
  - grade_name
  - grade_name_short
  - grade_level
  - description
  - evaluation_criteria
  - required_experience_months
  - skill_indicators
  - competency_requirements
  - certification_requirements
  - project_complexity
  - mentoring_capability
  - leadership_level
  - salary_impact_factor
  - promotion_eligibility
  - color_code
  - sort_order
  - is_active
  - code
  - name

---

#### 22. ❌ 外部キー fk_cert_req_target_department の参照先カラム MST_Department.id が存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_cert_req_target_department
- **target_table:** MST_Department
- **target_column:** id
- **available_columns:**
  - department_code
  - department_name
  - department_name_short
  - parent_department_id
  - department_level
  - department_type
  - manager_id
  - deputy_manager_id
  - cost_center_code
  - budget_amount
  - location
  - phone_number
  - email_address
  - establishment_date
  - abolition_date
  - department_status
  - sort_order
  - description
  - code
  - name

---

#### 23. ❌ 外部キー fk_cert_req_certification の参照先カラム MST_Certification.id が存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_cert_req_certification
- **target_table:** MST_Certification
- **target_column:** id
- **available_columns:**
  - certification_code
  - certification_name
  - certification_name_en
  - issuer
  - issuer_country
  - certification_category
  - certification_level
  - validity_period_months
  - renewal_required
  - renewal_requirements
  - exam_fee
  - exam_language
  - exam_format
  - official_url
  - description
  - skill_category_id
  - is_recommended
  - is_active
  - code
  - name

---

#### 24. ❌ 外部キー fk_cert_req_created_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_cert_req_created_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 25. ❌ 外部キー fk_cert_req_approved_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_cert_req_approved_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 26. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 27. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 28. ❌ 外部キー fk_department_parent の参照先カラム MST_Department.id が存在しません

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_department_parent
- **target_table:** MST_Department
- **target_column:** id
- **available_columns:**
  - department_code
  - department_name
  - department_name_short
  - parent_department_id
  - department_level
  - department_type
  - manager_id
  - deputy_manager_id
  - cost_center_code
  - budget_amount
  - location
  - phone_number
  - email_address
  - establishment_date
  - abolition_date
  - department_status
  - sort_order
  - description
  - code
  - name

---

#### 29. ❌ 外部キー fk_department_manager の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_department_manager
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 30. ❌ 外部キー fk_department_deputy の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_department_deputy
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 31. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 32. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 33. ❌ 外部キー fk_employee_department の参照先カラム MST_Department.id が存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_employee_department
- **target_table:** MST_Department
- **target_column:** id
- **available_columns:**
  - department_code
  - department_name
  - department_name_short
  - parent_department_id
  - department_level
  - department_type
  - manager_id
  - deputy_manager_id
  - cost_center_code
  - budget_amount
  - location
  - phone_number
  - email_address
  - establishment_date
  - abolition_date
  - department_status
  - sort_order
  - description
  - code
  - name

---

#### 34. ❌ 外部キー fk_employee_position の参照先カラム MST_Position.id が存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_employee_position
- **target_table:** MST_Position
- **target_column:** id
- **available_columns:**
  - position_code
  - position_name
  - position_name_short
  - position_level
  - position_rank
  - position_category
  - authority_level
  - approval_limit
  - salary_grade
  - allowance_amount
  - is_management
  - is_executive
  - requires_approval
  - can_hire
  - can_evaluate
  - position_status
  - sort_order
  - description
  - code
  - name

---

#### 35. ❌ 外部キー fk_employee_job_type の参照先カラム MST_JobType.id が存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_employee_job_type
- **target_table:** MST_JobType
- **target_column:** id
- **available_columns:**
  - job_type_code
  - job_type_name
  - job_type_name_en
  - job_category
  - job_level
  - description
  - required_experience_years
  - salary_grade_min
  - salary_grade_max
  - career_path
  - required_certifications
  - required_skills
  - department_affinity
  - remote_work_eligible
  - travel_frequency
  - sort_order
  - is_active
  - code
  - name

---

#### 36. ❌ 外部キー fk_employee_manager の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_employee_manager
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 37. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 38. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 39. ❌ 外部キー fk_MST_EmployeeDepartment_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_EmployeeDepartment_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 40. ❌ 外部キー fk_MST_EmployeeDepartment_department の参照先カラム MST_Department.id が存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_EmployeeDepartment_department
- **target_table:** MST_Department
- **target_column:** id
- **available_columns:**
  - department_code
  - department_name
  - department_name_short
  - parent_department_id
  - department_level
  - department_type
  - manager_id
  - deputy_manager_id
  - cost_center_code
  - budget_amount
  - location
  - phone_number
  - email_address
  - establishment_date
  - abolition_date
  - department_status
  - sort_order
  - description
  - code
  - name

---

#### 41. ❌ 外部キー fk_MST_EmployeeDepartment_reporting_manager の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_EmployeeDepartment_reporting_manager
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 42. ❌ 外部キー fk_MST_EmployeeDepartment_approved_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_EmployeeDepartment_approved_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 43. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 44. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 45. ❌ 外部キー fk_emp_job_type_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_emp_job_type_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 46. ❌ 外部キー fk_emp_job_type_job_type の参照先カラム MST_JobType.id が存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_emp_job_type_job_type
- **target_table:** MST_JobType
- **target_column:** id
- **available_columns:**
  - job_type_code
  - job_type_name
  - job_type_name_en
  - job_category
  - job_level
  - description
  - required_experience_years
  - salary_grade_min
  - salary_grade_max
  - career_path
  - required_certifications
  - required_skills
  - department_affinity
  - remote_work_eligible
  - travel_frequency
  - sort_order
  - is_active
  - code
  - name

---

#### 47. ❌ 外部キー fk_emp_job_type_mentor の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_emp_job_type_mentor
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 48. ❌ 外部キー fk_emp_job_type_supervisor の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_emp_job_type_supervisor
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 49. ❌ 外部キー fk_emp_job_type_created_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_emp_job_type_created_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 50. ❌ 外部キー fk_emp_job_type_approved_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_emp_job_type_approved_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 51. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 52. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 53. ❌ 外部キー fk_MST_EmployeePosition_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_EmployeePosition_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 54. ❌ 外部キー fk_MST_EmployeePosition_position の参照先カラム MST_Position.id が存在しません

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_EmployeePosition_position
- **target_table:** MST_Position
- **target_column:** id
- **available_columns:**
  - position_code
  - position_name
  - position_name_short
  - position_level
  - position_rank
  - position_category
  - authority_level
  - approval_limit
  - salary_grade
  - allowance_amount
  - is_management
  - is_executive
  - requires_approval
  - can_hire
  - can_evaluate
  - position_status
  - sort_order
  - description
  - code
  - name

---

#### 55. ❌ 外部キー fk_MST_EmployeePosition_approved_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_EmployeePosition_approved_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 56. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_JobType

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 57. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_JobType

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 58. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 59. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 60. ❌ 外部キー fk_MST_JobTypeSkill_job_type の参照先カラム MST_JobType.id が存在しません

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_JobTypeSkill_job_type
- **target_table:** MST_JobType
- **target_column:** id
- **available_columns:**
  - job_type_code
  - job_type_name
  - job_type_name_en
  - job_category
  - job_level
  - description
  - required_experience_years
  - salary_grade_min
  - salary_grade_max
  - career_path
  - required_certifications
  - required_skills
  - department_affinity
  - remote_work_eligible
  - travel_frequency
  - sort_order
  - is_active
  - code
  - name

---

#### 61. ❌ 外部キー fk_MST_JobTypeSkill_skill_item の参照先カラム MST_SkillItem.id が存在しません

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_JobTypeSkill_skill_item
- **target_table:** MST_SkillItem
- **target_column:** id
- **available_columns:**
  - skill_code
  - skill_name
  - skill_category_id
  - skill_type
  - difficulty_level
  - importance_level
  - code
  - name
  - description

---

#### 62. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 63. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 64. ❌ 外部キー fk_MST_JobTypeSkillGrade_job_type の参照先カラム MST_JobType.id が存在しません

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_JobTypeSkillGrade_job_type
- **target_table:** MST_JobType
- **target_column:** id
- **available_columns:**
  - job_type_code
  - job_type_name
  - job_type_name_en
  - job_category
  - job_level
  - description
  - required_experience_years
  - salary_grade_min
  - salary_grade_max
  - career_path
  - required_certifications
  - required_skills
  - department_affinity
  - remote_work_eligible
  - travel_frequency
  - sort_order
  - is_active
  - code
  - name

---

#### 65. ❌ 外部キー fk_MST_JobTypeSkillGrade_skill_grade の参照先カラム MST_SkillGrade.id が存在しません

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_JobTypeSkillGrade_skill_grade
- **target_table:** MST_SkillGrade
- **target_column:** id
- **available_columns:**
  - grade_code
  - grade_name
  - grade_name_short
  - grade_level
  - description
  - evaluation_criteria
  - required_experience_months
  - skill_indicators
  - competency_requirements
  - certification_requirements
  - project_complexity
  - mentoring_capability
  - leadership_level
  - salary_impact_factor
  - promotion_eligibility
  - color_code
  - sort_order
  - is_active
  - code
  - name

---

#### 66. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 67. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 68. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 69. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 70. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 71. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 72. ❌ 外部キー fk_permission_parent の参照先カラム MST_Permission.id が存在しません

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_permission_parent
- **target_table:** MST_Permission
- **target_column:** id
- **available_columns:**
  - permission_code
  - permission_name
  - permission_name_short
  - permission_category
  - resource_type
  - action_type
  - scope_level
  - parent_permission_id
  - is_system_permission
  - requires_conditions
  - condition_expression
  - risk_level
  - requires_approval
  - audit_required
  - permission_status
  - effective_from
  - effective_to
  - sort_order
  - description
  - code
  - name

---

#### 73. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Position

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 74. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Position

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 75. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 76. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 77. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 78. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 79. ❌ 外部キー fk_role_parent の参照先カラム MST_Role.id が存在しません

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_role_parent
- **target_table:** MST_Role
- **target_column:** id
- **available_columns:**
  - role_code
  - role_name
  - role_name_short
  - role_category
  - role_level
  - parent_role_id
  - is_system_role
  - is_tenant_specific
  - max_users
  - role_priority
  - auto_assign_conditions
  - role_status
  - effective_from
  - effective_to
  - sort_order
  - description
  - code
  - name

---

#### 80. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillCategory

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 81. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillCategory

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 82. ❌ 外部キー fk_skillcategory_parent の参照先カラム MST_SkillCategory.id が存在しません

**テーブル:** MST_SkillCategory

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skillcategory_parent
- **target_table:** MST_SkillCategory
- **target_column:** id
- **available_columns:**
  - category_code
  - category_name
  - category_name_short
  - category_name_en
  - category_type
  - parent_category_id
  - category_level
  - category_path
  - is_system_category
  - is_leaf_category
  - skill_count
  - evaluation_method
  - max_level
  - icon_url
  - color_code
  - display_order
  - is_popular
  - category_status
  - effective_from
  - effective_to
  - description
  - code
  - name

---

#### 83. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 84. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 85. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 86. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 87. ❌ 外部キー fk_MST_SkillGradeRequirement_skill_grade の参照先カラム MST_SkillGrade.id が存在しません

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_SkillGradeRequirement_skill_grade
- **target_table:** MST_SkillGrade
- **target_column:** id
- **available_columns:**
  - grade_code
  - grade_name
  - grade_name_short
  - grade_level
  - description
  - evaluation_criteria
  - required_experience_months
  - skill_indicators
  - competency_requirements
  - certification_requirements
  - project_complexity
  - mentoring_capability
  - leadership_level
  - salary_impact_factor
  - promotion_eligibility
  - color_code
  - sort_order
  - is_active
  - code
  - name

---

#### 88. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 89. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 90. ❌ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['id'] がDDLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - parent_skill_id
- **target_table:** MST_SkillHierarchy
- **target_columns:**
  - id

---

#### 91. ❌ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['id'] がYAMLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - parent_skill_id
- **target_table:** MST_SkillHierarchy
- **target_columns:**
  - id

---

#### 92. ❌ 外部キー fk_hierarchy_skill の参照先カラム MST_SkillItem.id が存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_hierarchy_skill
- **target_table:** MST_SkillItem
- **target_column:** id
- **available_columns:**
  - skill_code
  - skill_name
  - skill_category_id
  - skill_type
  - difficulty_level
  - importance_level
  - code
  - name
  - description

---

#### 93. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 94. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 95. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がDDLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 96. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がYAMLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 97. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SystemConfig

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 98. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SystemConfig

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 99. ❌ 外部キー fk_tenant_settings_tenant の参照先カラム MST_Tenant.id が存在しません

**テーブル:** MST_TenantSettings

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_tenant_settings_tenant
- **target_table:** MST_Tenant
- **target_column:** id
- **available_columns:**
  - tenant_id
  - tenant_code
  - tenant_name
  - tenant_name_en
  - tenant_short_name
  - tenant_type
  - parent_tenant_id
  - tenant_level
  - domain_name
  - subdomain
  - logo_url
  - primary_color
  - secondary_color
  - timezone
  - locale
  - currency_code
  - date_format
  - time_format
  - admin_email
  - contact_email
  - phone_number
  - address
  - postal_code
  - country_code
  - subscription_plan
  - max_users
  - max_storage_gb
  - features_enabled
  - custom_settings
  - security_policy
  - data_retention_days
  - backup_enabled
  - backup_frequency
  - contract_start_date
  - contract_end_date
  - trial_end_date
  - billing_cycle
  - monthly_fee
  - setup_fee
  - status
  - activation_date
  - suspension_date
  - suspension_reason
  - last_login_date
  - current_users_count
  - storage_used_gb
  - api_rate_limit
  - sso_enabled
  - sso_provider
  - sso_config
  - webhook_url
  - webhook_secret
  - created_by
  - notes
  - code
  - name
  - description

---

#### 100. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 101. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 102. ❌ 外部キー fk_training_program_created_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_training_program_created_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 103. ❌ 外部キー fk_training_program_approved_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_training_program_approved_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 104. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 105. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 106. ❌ 外部キー fk_userauth_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_userauth_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 107. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 108. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 109. ❌ 外部キー ['user_id'] -> MST_UserAuth.['id'] がDDLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - id

---

#### 110. ❌ 外部キー ['user_id'] -> MST_UserAuth.['id'] がYAMLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - id

---

#### 111. ❌ 外部キー fk_userrole_role の参照先カラム MST_Role.id が存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_userrole_role
- **target_table:** MST_Role
- **target_column:** id
- **available_columns:**
  - role_code
  - role_name
  - role_name_short
  - role_category
  - role_level
  - parent_role_id
  - is_system_role
  - is_tenant_specific
  - max_users
  - role_priority
  - auto_assign_conditions
  - role_status
  - effective_from
  - effective_to
  - sort_order
  - description
  - code
  - name

---

#### 112. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 113. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 114. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 115. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 116. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_MasterData

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 117. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_MasterData

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 118. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 119. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 120. ❌ 外部キー fk_skill_index_skill の参照先テーブル MST_Skill のDDLファイルが存在しません

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **issue_type:** missing_target_table_ddl
- **foreign_key_name:** fk_skill_index_skill
- **target_table:** MST_Skill
- **target_ddl_path:** /home/kurosawa/skill-report-web/docs/design/database/ddl/MST_Skill.sql

---

#### 121. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 122. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 123. ❌ 外部キー fk_SYS_SkillMatrix_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_SYS_SkillMatrix_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 124. ❌ 外部キー fk_SYS_SkillMatrix_skill の参照先テーブル MST_Skill のDDLファイルが存在しません

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **issue_type:** missing_target_table_ddl
- **foreign_key_name:** fk_SYS_SkillMatrix_skill
- **target_table:** MST_Skill
- **target_ddl_path:** /home/kurosawa/skill-report-web/docs/design/database/ddl/MST_Skill.sql

---

#### 125. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 126. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 127. ❌ 外部キー fk_SYS_TenantUsage_tenant の参照先カラム MST_Tenant.id が存在しません

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_SYS_TenantUsage_tenant
- **target_table:** MST_Tenant
- **target_column:** id
- **available_columns:**
  - tenant_id
  - tenant_code
  - tenant_name
  - tenant_name_en
  - tenant_short_name
  - tenant_type
  - parent_tenant_id
  - tenant_level
  - domain_name
  - subdomain
  - logo_url
  - primary_color
  - secondary_color
  - timezone
  - locale
  - currency_code
  - date_format
  - time_format
  - admin_email
  - contact_email
  - phone_number
  - address
  - postal_code
  - country_code
  - subscription_plan
  - max_users
  - max_storage_gb
  - features_enabled
  - custom_settings
  - security_policy
  - data_retention_days
  - backup_enabled
  - backup_frequency
  - contract_start_date
  - contract_end_date
  - trial_end_date
  - billing_cycle
  - monthly_fee
  - setup_fee
  - status
  - activation_date
  - suspension_date
  - suspension_reason
  - last_login_date
  - current_users_count
  - storage_used_gb
  - api_rate_limit
  - sso_enabled
  - sso_provider
  - sso_config
  - webhook_url
  - webhook_secret
  - created_by
  - notes
  - code
  - name
  - description

---

#### 128. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_TokenStore

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 129. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_TokenStore

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 130. ❌ 外部キー fk_token_store_user の参照先カラム MST_UserAuth.id が存在しません

**テーブル:** SYS_TokenStore

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_token_store_user
- **target_table:** MST_UserAuth
- **target_column:** id
- **available_columns:**
  - user_id
  - login_id
  - password_hash
  - password_salt
  - employee_id
  - account_status
  - last_login_at
  - last_login_ip
  - failed_login_count
  - last_failed_login_at
  - password_changed_at
  - password_expires_at
  - mfa_enabled
  - mfa_secret
  - recovery_token
  - recovery_token_expires_at
  - session_timeout
  - external_auth_provider
  - external_auth_id
  - code
  - name
  - description

---

#### 131. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 132. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 133. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がDDLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 134. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がYAMLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 135. ❌ 外部キー fk_skill_grade_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_grade_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 136. ❌ 外部キー fk_skill_grade_job_type の参照先カラム MST_JobType.id が存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_grade_job_type
- **target_table:** MST_JobType
- **target_column:** id
- **available_columns:**
  - job_type_code
  - job_type_name
  - job_type_name_en
  - job_category
  - job_level
  - description
  - required_experience_years
  - salary_grade_min
  - salary_grade_max
  - career_path
  - required_certifications
  - required_skills
  - department_affinity
  - remote_work_eligible
  - travel_frequency
  - sort_order
  - is_active
  - code
  - name

---

#### 137. ❌ 外部キー fk_skill_grade_evaluator の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_grade_evaluator
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 138. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 139. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 140. ❌ 外部キー fk_TRN_GoalProgress_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_TRN_GoalProgress_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 141. ❌ 外部キー fk_TRN_GoalProgress_supervisor の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_TRN_GoalProgress_supervisor
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 142. ❌ 外部キー fk_TRN_GoalProgress_approved_by の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_TRN_GoalProgress_approved_by
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 143. ❌ 外部キー fk_TRN_GoalProgress_career_plan の参照先カラム MST_CareerPlan.id が存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_TRN_GoalProgress_career_plan
- **target_table:** MST_CareerPlan
- **target_column:** id
- **available_columns:**
  - career_plan_id
  - employee_id
  - plan_name
  - plan_description
  - plan_type
  - target_position_id
  - target_job_type_id
  - target_department_id
  - current_level
  - target_level
  - plan_start_date
  - plan_end_date
  - milestone_1_date
  - milestone_1_description
  - milestone_2_date
  - milestone_2_description
  - milestone_3_date
  - milestone_3_description
  - required_skills
  - required_certifications
  - required_experiences
  - development_actions
  - training_plan
  - mentor_id
  - supervisor_id
  - plan_status
  - progress_percentage
  - last_review_date
  - next_review_date
  - review_frequency
  - success_criteria
  - risk_factors
  - support_resources
  - budget_allocated
  - budget_used
  - priority_level
  - visibility_level
  - template_id
  - custom_fields
  - notes
  - code
  - name
  - description

---

#### 144. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 145. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 146. ❌ 外部キー fk_notification_recipient の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_notification_recipient
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 147. ❌ 外部キー fk_notification_sender の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_notification_sender
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 148. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 149. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 150. ❌ 外部キー fk_pdu_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_pdu_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 151. ❌ 外部キー fk_pdu_certification の参照先カラム MST_Certification.id が存在しません

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_pdu_certification
- **target_table:** MST_Certification
- **target_column:** id
- **available_columns:**
  - certification_code
  - certification_name
  - certification_name_en
  - issuer
  - issuer_country
  - certification_category
  - certification_level
  - validity_period_months
  - renewal_required
  - renewal_requirements
  - exam_fee
  - exam_language
  - exam_format
  - official_url
  - description
  - skill_category_id
  - is_recommended
  - is_active
  - code
  - name

---

#### 152. ❌ 外部キー fk_pdu_approver の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_pdu_approver
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 153. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 154. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 155. ❌ 外部キー fk_project_record_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_project_record_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 156. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 157. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 158. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がDDLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 159. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がYAMLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 160. ❌ 外部キー fk_evidence_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_evidence_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 161. ❌ 外部キー fk_evidence_skill の参照先カラム MST_SkillItem.id が存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_evidence_skill
- **target_table:** MST_SkillItem
- **target_column:** id
- **available_columns:**
  - skill_code
  - skill_name
  - skill_category_id
  - skill_type
  - difficulty_level
  - importance_level
  - code
  - name
  - description

---

#### 162. ❌ 外部キー fk_evidence_verifier の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_evidence_verifier
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 163. ❌ 外部キー fk_evidence_certification の参照先カラム MST_Certification.id が存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_evidence_certification
- **target_table:** MST_Certification
- **target_column:** id
- **available_columns:**
  - certification_code
  - certification_name
  - certification_name_en
  - issuer
  - issuer_country
  - certification_category
  - certification_level
  - validity_period_months
  - renewal_required
  - renewal_requirements
  - exam_fee
  - exam_language
  - exam_format
  - official_url
  - description
  - skill_category_id
  - is_recommended
  - is_active
  - code
  - name

---

#### 164. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 165. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 166. ❌ 外部キー fk_skill_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 167. ❌ 外部キー fk_skill_item の参照先カラム MST_SkillItem.id が存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_item
- **target_table:** MST_SkillItem
- **target_column:** id
- **available_columns:**
  - skill_code
  - skill_name
  - skill_category_id
  - skill_type
  - difficulty_level
  - importance_level
  - code
  - name
  - description

---

#### 168. ❌ 外部キー fk_skill_certification の参照先カラム MST_Certification.id が存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_certification
- **target_table:** MST_Certification
- **target_column:** id
- **available_columns:**
  - certification_code
  - certification_name
  - certification_name_en
  - issuer
  - issuer_country
  - certification_category
  - certification_level
  - validity_period_months
  - renewal_required
  - renewal_requirements
  - exam_fee
  - exam_language
  - exam_format
  - official_url
  - description
  - skill_category_id
  - is_recommended
  - is_active
  - code
  - name

---

#### 169. ❌ 外部キー fk_skill_category の参照先カラム MST_SkillCategory.id が存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_category
- **target_table:** MST_SkillCategory
- **target_column:** id
- **available_columns:**
  - category_code
  - category_name
  - category_name_short
  - category_name_en
  - category_type
  - parent_category_id
  - category_level
  - category_path
  - is_system_category
  - is_leaf_category
  - skill_count
  - evaluation_method
  - max_level
  - icon_url
  - color_code
  - display_order
  - is_popular
  - category_status
  - effective_from
  - effective_to
  - description
  - code
  - name

---

#### 170. ❌ 外部キー fk_skill_assessor の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_skill_assessor
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 171. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 172. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 173. ❌ 外部キー fk_training_history_employee の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_training_history_employee
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 174. ❌ 外部キー fk_training_history_program の参照先カラム MST_TrainingProgram.id が存在しません

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_training_history_program
- **target_table:** MST_TrainingProgram
- **target_column:** id
- **available_columns:**
  - training_program_id
  - program_code
  - program_name
  - program_name_en
  - program_description
  - program_category
  - program_type
  - target_audience
  - difficulty_level
  - duration_hours
  - duration_days
  - max_participants
  - min_participants
  - prerequisites
  - learning_objectives
  - curriculum_outline
  - curriculum_details
  - materials_required
  - equipment_required
  - instructor_requirements
  - assessment_method
  - passing_score
  - certification_provided
  - pdu_credits
  - related_skills
  - related_certifications
  - cost_per_participant
  - external_provider
  - external_url
  - venue_type
  - venue_requirements
  - language
  - repeat_interval
  - mandatory_flag
  - active_flag
  - effective_start_date
  - effective_end_date
  - created_by
  - approved_by
  - approval_date
  - version_number
  - revision_notes
  - tags
  - code
  - name
  - description

---

#### 175. ❌ 外部キー fk_training_history_approver の参照先カラム MST_Employee.id が存在しません

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_training_history_approver
- **target_table:** MST_Employee
- **target_column:** id
- **available_columns:**
  - employee_code
  - full_name
  - full_name_kana
  - email
  - phone
  - hire_date
  - birth_date
  - gender
  - department_id
  - position_id
  - job_type_id
  - employment_status
  - manager_id
  - employee_status
  - code
  - name
  - description

---

#### 176. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 177. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 178. ⚠️ 外部キー ['user_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** HIS_AuditLog

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_his_auditlog_user
  - columns: ['user_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 179. ⚠️ 外部キー ['user_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** HIS_AuditLog

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_his_auditlog_user
  - columns: ['user_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 社員マスタへの外部キー

---

#### 180. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がDDLにのみ存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - template_id
- **target_table:** MST_NotificationTemplate
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_notification_log_template
  - columns: ['template_id']
  - reference_table: MST_NotificationTemplate
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 181. ⚠️ 外部キー ['integration_config_id'] -> SYS_IntegrationConfig.['id'] がDDLにのみ存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - integration_config_id
- **target_table:** SYS_IntegrationConfig
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_notification_log_integration
  - columns: ['integration_config_id']
  - reference_table: SYS_IntegrationConfig
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 182. ⚠️ 外部キー ['setting_id'] -> MST_NotificationSettings.['id'] がDDLにのみ存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - setting_id
- **target_table:** MST_NotificationSettings
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_notification_log_setting
  - columns: ['setting_id']
  - reference_table: MST_NotificationSettings
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 183. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がYAMLにのみ存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - template_id
- **target_table:** MST_NotificationTemplate
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_notification_log_template
  - columns: ['template_id']
  - reference_table: MST_NotificationTemplate
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 通知テンプレートへの外部キー

---

#### 184. ⚠️ 外部キー ['integration_config_id'] -> SYS_IntegrationConfig.['id'] がYAMLにのみ存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - integration_config_id
- **target_table:** SYS_IntegrationConfig
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_notification_log_integration
  - columns: ['integration_config_id']
  - reference_table: SYS_IntegrationConfig
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 外部連携設定への外部キー

---

#### 185. ⚠️ 外部キー ['setting_id'] -> MST_NotificationSettings.['id'] がYAMLにのみ存在します

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - setting_id
- **target_table:** MST_NotificationSettings
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_notification_log_setting
  - columns: ['setting_id']
  - reference_table: MST_NotificationSettings
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 通知設定への外部キー

---

#### 186. ⚠️ 外部キー fk_notification_log_template のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_template
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 187. ⚠️ 外部キー fk_notification_log_setting のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_setting
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 188. ⚠️ 外部キー fk_notification_log_integration のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_integration
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 189. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - target_department_id
- **target_table:** MST_Department
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_career_plan_target_department
  - columns: ['target_department_id']
  - reference_table: MST_Department
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 190. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - target_position_id
- **target_table:** MST_Position
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_career_plan_target_position
  - columns: ['target_position_id']
  - reference_table: MST_Position
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 191. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - employee_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_career_plan_employee
  - columns: ['employee_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 192. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - mentor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_career_plan_mentor
  - columns: ['mentor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 193. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - supervisor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_career_plan_supervisor
  - columns: ['supervisor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 194. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - target_job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_career_plan_target_job_type
  - columns: ['target_job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 195. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がYAMLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - target_department_id
- **target_table:** MST_Department
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_career_plan_target_department
  - columns: ['target_department_id']
  - reference_table: MST_Department
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 目標部署への外部キー

---

#### 196. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がYAMLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - target_position_id
- **target_table:** MST_Position
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_career_plan_target_position
  - columns: ['target_position_id']
  - reference_table: MST_Position
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 目標役職への外部キー

---

#### 197. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - employee_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_career_plan_employee
  - columns: ['employee_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 社員への外部キー

---

#### 198. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - mentor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_career_plan_mentor
  - columns: ['mentor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: メンターへの外部キー

---

#### 199. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - supervisor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_career_plan_supervisor
  - columns: ['supervisor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 上司への外部キー

---

#### 200. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - target_job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_career_plan_target_job_type
  - columns: ['target_job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 目標職種への外部キー

---

#### 201. ⚠️ 外部キー fk_career_plan_target_department のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_department
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 202. ⚠️ 外部キー fk_career_plan_target_position のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_position
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 203. ⚠️ 外部キー fk_career_plan_mentor のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_mentor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 204. ⚠️ 外部キー fk_career_plan_supervisor のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_supervisor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 205. ⚠️ 外部キー fk_career_plan_target_job_type のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 206. ⚠️ 外部キー ['skill_category_id'] -> MST_SkillCategory.['id'] がDDLにのみ存在します

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - skill_category_id
- **target_table:** MST_SkillCategory
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_certification_skill_category
  - columns: ['skill_category_id']
  - reference_table: MST_SkillCategory
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 207. ⚠️ 外部キー ['skill_category_id'] -> MST_SkillCategory.['id'] がYAMLにのみ存在します

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - skill_category_id
- **target_table:** MST_SkillCategory
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_certification_skill_category
  - columns: ['skill_category_id']
  - reference_table: MST_SkillCategory
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: スキルカテゴリへの外部キー

---

#### 208. ⚠️ 外部キー fk_certification_skill_category のON DELETE設定が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_certification_skill_category
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 209. ⚠️ 外部キー ['target_skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - target_skill_grade_id
- **target_table:** MST_SkillGrade
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_cert_req_target_skill_grade
  - columns: ['target_skill_grade_id']
  - reference_table: MST_SkillGrade
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 210. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - target_department_id
- **target_table:** MST_Department
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_cert_req_target_department
  - columns: ['target_department_id']
  - reference_table: MST_Department
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 211. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - target_position_id
- **target_table:** MST_Position
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_cert_req_target_position
  - columns: ['target_position_id']
  - reference_table: MST_Position
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 212. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_cert_req_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 213. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - created_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_cert_req_created_by
  - columns: ['created_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 214. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - target_job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_cert_req_target_job_type
  - columns: ['target_job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 215. ⚠️ 外部キー ['target_skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - target_skill_grade_id
- **target_table:** MST_SkillGrade
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_cert_req_target_skill_grade
  - columns: ['target_skill_grade_id']
  - reference_table: MST_SkillGrade
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 対象スキルグレードへの外部キー

---

#### 216. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がYAMLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - target_department_id
- **target_table:** MST_Department
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_cert_req_target_department
  - columns: ['target_department_id']
  - reference_table: MST_Department
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 対象部署への外部キー

---

#### 217. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がYAMLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - target_position_id
- **target_table:** MST_Position
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_cert_req_target_position
  - columns: ['target_position_id']
  - reference_table: MST_Position
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 対象役職への外部キー

---

#### 218. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_cert_req_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 219. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - created_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_cert_req_created_by
  - columns: ['created_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 作成者への外部キー

---

#### 220. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - target_job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_cert_req_target_job_type
  - columns: ['target_job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 対象職種への外部キー

---

#### 221. ⚠️ 外部キー fk_cert_req_target_skill_grade のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_skill_grade
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 222. ⚠️ 外部キー fk_cert_req_target_department のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_department
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 223. ⚠️ 外部キー fk_cert_req_target_position のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_position
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 224. ⚠️ 外部キー fk_cert_req_approved_by のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 225. ⚠️ 外部キー fk_cert_req_target_job_type のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 226. ⚠️ 外部キー ['manager_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - manager_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_department_manager
  - columns: ['manager_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 227. ⚠️ 外部キー ['deputy_manager_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - deputy_manager_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_department_deputy
  - columns: ['deputy_manager_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 228. ⚠️ 外部キー ['manager_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - manager_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_department_manager
  - columns: ['manager_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 部署長への外部キー

---

#### 229. ⚠️ 外部キー ['deputy_manager_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - deputy_manager_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_department_deputy
  - columns: ['deputy_manager_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 副部署長への外部キー

---

#### 230. ⚠️ 外部キー fk_department_manager のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 231. ⚠️ 外部キー fk_department_deputy のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_deputy
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 232. ⚠️ 外部キー fk_department_parent のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 233. ⚠️ 外部キー fk_employee_manager のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 234. ⚠️ 外部キー fk_employee_job_type のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 235. ⚠️ 外部キー fk_employee_position のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_position
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 236. ⚠️ 外部キー ['reporting_manager_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - reporting_manager_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_EmployeeDepartment_reporting_manager
  - columns: ['reporting_manager_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 237. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_EmployeeDepartment_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 238. ⚠️ 外部キー ['reporting_manager_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - reporting_manager_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_EmployeeDepartment_reporting_manager
  - columns: ['reporting_manager_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 報告先上司への外部キー

---

#### 239. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_EmployeeDepartment_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 240. ⚠️ 外部キー fk_MST_EmployeeDepartment_reporting_manager のON DELETE設定が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeeDepartment_reporting_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 241. ⚠️ 外部キー fk_MST_EmployeeDepartment_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeeDepartment_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 242. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_emp_job_type_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 243. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_emp_job_type_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 244. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - mentor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_emp_job_type_mentor
  - columns: ['mentor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 245. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - created_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_emp_job_type_created_by
  - columns: ['created_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 246. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - supervisor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_emp_job_type_supervisor
  - columns: ['supervisor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 247. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_emp_job_type_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 248. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_emp_job_type_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 職種への外部キー

---

#### 249. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - mentor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_emp_job_type_mentor
  - columns: ['mentor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: メンターへの外部キー

---

#### 250. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - created_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_emp_job_type_created_by
  - columns: ['created_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 作成者への外部キー

---

#### 251. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - supervisor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_emp_job_type_supervisor
  - columns: ['supervisor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 上司への外部キー

---

#### 252. ⚠️ 外部キー fk_emp_job_type_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 253. ⚠️ 外部キー fk_emp_job_type_mentor のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_mentor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 254. ⚠️ 外部キー fk_emp_job_type_supervisor のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_supervisor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 255. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_EmployeePosition_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 256. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_EmployeePosition_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 257. ⚠️ 外部キー fk_MST_EmployeePosition_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeePosition_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 258. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_JobTypeSkill_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 259. ⚠️ 外部キー ['skill_item_id'] -> MST_SkillItem.['id'] がDDLにのみ存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - skill_item_id
- **target_table:** MST_SkillItem
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_JobTypeSkill_skill_item
  - columns: ['skill_item_id']
  - reference_table: MST_SkillItem
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 260. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_JobTypeSkill_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: 職種への外部キー

---

#### 261. ⚠️ 外部キー ['skill_item_id'] -> MST_SkillItem.['id'] がYAMLにのみ存在します

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - skill_item_id
- **target_table:** MST_SkillItem
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_JobTypeSkill_skill_item
  - columns: ['skill_item_id']
  - reference_table: MST_SkillItem
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: スキル項目への外部キー

---

#### 262. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_JobTypeSkillGrade_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 263. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - skill_grade_id
- **target_table:** MST_SkillGrade
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_JobTypeSkillGrade_skill_grade
  - columns: ['skill_grade_id']
  - reference_table: MST_SkillGrade
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 264. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_JobTypeSkillGrade_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: 職種への外部キー

---

#### 265. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - skill_grade_id
- **target_table:** MST_SkillGrade
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_JobTypeSkillGrade_skill_grade
  - columns: ['skill_grade_id']
  - reference_table: MST_SkillGrade
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: スキルグレードへの外部キー

---

#### 266. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がDDLにのみ存在します

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - template_id
- **target_table:** MST_NotificationTemplate
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_notification_settings_template
  - columns: ['template_id']
  - reference_table: MST_NotificationTemplate
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 267. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がYAMLにのみ存在します

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - template_id
- **target_table:** MST_NotificationTemplate
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_notification_settings_template
  - columns: ['template_id']
  - reference_table: MST_NotificationTemplate
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 通知テンプレートへの外部キー

---

#### 268. ⚠️ 外部キー fk_notification_settings_template のON DELETE設定が不一致

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_settings_template
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 269. ⚠️ 外部キー ['parent_permission_id'] -> MST_Permission.['id'] がDDLにのみ存在します

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - parent_permission_id
- **target_table:** MST_Permission
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_permission_parent
  - columns: ['parent_permission_id']
  - reference_table: MST_Permission
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 270. ⚠️ 外部キー ['parent_permission_id'] -> MST_Permission.['id'] がYAMLにのみ存在します

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - parent_permission_id
- **target_table:** MST_Permission
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_permission_parent
  - columns: ['parent_permission_id']
  - reference_table: MST_Permission
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 親権限への自己参照外部キー

---

#### 271. ⚠️ 外部キー fk_permission_parent のON DELETE設定が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_permission_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 272. ⚠️ 外部キー ['parent_role_id'] -> MST_Role.['id'] がDDLにのみ存在します

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - parent_role_id
- **target_table:** MST_Role
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_role_parent
  - columns: ['parent_role_id']
  - reference_table: MST_Role
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 273. ⚠️ 外部キー ['parent_role_id'] -> MST_Role.['id'] がYAMLにのみ存在します

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - parent_role_id
- **target_table:** MST_Role
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_role_parent
  - columns: ['parent_role_id']
  - reference_table: MST_Role
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 親ロールへの自己参照外部キー

---

#### 274. ⚠️ 外部キー fk_role_parent のON DELETE設定が不一致

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_role_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 275. ⚠️ DDLファイルが見つかりません: /home/kurosawa/skill-report-web/docs/design/database/ddl/MST_RolePermission.sql

**テーブル:** MST_RolePermission

**詳細情報:**
- **file_path:** /home/kurosawa/skill-report-web/docs/design/database/ddl/MST_RolePermission.sql

---

#### 276. ⚠️ DDLファイルが見つかりません: /home/kurosawa/skill-report-web/docs/design/database/ddl/MST_Skill.sql

**テーブル:** MST_Skill

**詳細情報:**
- **file_path:** /home/kurosawa/skill-report-web/docs/design/database/ddl/MST_Skill.sql

---

#### 277. ⚠️ 外部キー fk_skillcategory_parent のON DELETE設定が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skillcategory_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 278. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - skill_grade_id
- **target_table:** MST_SkillGrade
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_MST_SkillGradeRequirement_skill_grade
  - columns: ['skill_grade_id']
  - reference_table: MST_SkillGrade
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 279. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - skill_grade_id
- **target_table:** MST_SkillGrade
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_MST_SkillGradeRequirement_skill_grade
  - columns: ['skill_grade_id']
  - reference_table: MST_SkillGrade
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: スキルグレードへの外部キー

---

#### 280. ⚠️ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['skill_id'] がDDLにのみ存在します

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - parent_skill_id
- **target_table:** MST_SkillHierarchy
- **target_columns:**
  - skill_id
- **ddl_definition:**
  - name: fk_hierarchy_parent
  - columns: ['parent_skill_id']
  - reference_table: MST_SkillHierarchy
  - reference_columns: ['skill_id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 281. ⚠️ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['skill_id'] がYAMLにのみ存在します

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - parent_skill_id
- **target_table:** MST_SkillHierarchy
- **target_columns:**
  - skill_id
- **yaml_definition:**
  - name: fk_hierarchy_parent
  - columns: ['parent_skill_id']
  - reference_table: MST_SkillHierarchy
  - reference_columns: ['skill_id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: 親スキルへの自己参照外部キー

---

#### 282. ⚠️ 外部キー ['parent_tenant_id'] -> MST_Tenant.['tenant_id'] がDDLにのみ存在します

**テーブル:** MST_Tenant

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - parent_tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - tenant_id
- **ddl_definition:**
  - name: fk_tenant_parent
  - columns: ['parent_tenant_id']
  - reference_table: MST_Tenant
  - reference_columns: ['tenant_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 283. ⚠️ 外部キー ['parent_tenant_id'] -> MST_Tenant.['tenant_id'] がYAMLにのみ存在します

**テーブル:** MST_Tenant

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - parent_tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - tenant_id
- **yaml_definition:**
  - name: fk_tenant_parent
  - columns: ['parent_tenant_id']
  - reference_table: MST_Tenant
  - reference_columns: ['tenant_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 親テナントへの外部キー（自己参照）

---

#### 284. ⚠️ 外部キー fk_tenant_parent のON DELETE設定が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_tenant_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 285. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - created_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_training_program_created_by
  - columns: ['created_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 286. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_training_program_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 287. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - created_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_training_program_created_by
  - columns: ['created_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 作成者への外部キー

---

#### 288. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_training_program_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 289. ⚠️ 外部キー fk_training_program_approved_by のON DELETE設定が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_training_program_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 290. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - employee_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_userauth_employee
  - columns: ['employee_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 291. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - employee_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_userauth_employee
  - columns: ['employee_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 社員への外部キー

---

#### 292. ⚠️ 外部キー fk_userauth_employee のON DELETE設定が不一致

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userauth_employee
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 293. ⚠️ 外部キー ['delegation_source_user_id'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - delegation_source_user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **ddl_definition:**
  - name: fk_userrole_delegation_source
  - columns: ['delegation_source_user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 294. ⚠️ 外部キー ['assigned_by'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - assigned_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **ddl_definition:**
  - name: fk_userrole_assigned_by
  - columns: ['assigned_by']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 295. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **ddl_definition:**
  - name: fk_userrole_user
  - columns: ['user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 296. ⚠️ 外部キー ['approved_by'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **ddl_definition:**
  - name: fk_userrole_approved_by
  - columns: ['approved_by']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 297. ⚠️ 外部キー ['delegation_source_user_id'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - delegation_source_user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **yaml_definition:**
  - name: fk_userrole_delegation_source
  - columns: ['delegation_source_user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 委譲元ユーザーへの外部キー

---

#### 298. ⚠️ 外部キー ['assigned_by'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - assigned_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **yaml_definition:**
  - name: fk_userrole_assigned_by
  - columns: ['assigned_by']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 割り当て者への外部キー

---

#### 299. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **yaml_definition:**
  - name: fk_userrole_user
  - columns: ['user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: ユーザーへの外部キー

---

#### 300. ⚠️ 外部キー ['approved_by'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **yaml_definition:**
  - name: fk_userrole_approved_by
  - columns: ['approved_by']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 301. ⚠️ 外部キー fk_userrole_delegation_source のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_delegation_source
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 302. ⚠️ 外部キー fk_userrole_approved_by のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 303. ⚠️ 外部キー fk_userrole_assigned_by のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_assigned_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 304. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **ddl_definition:**
  - name: fk_log_user
  - columns: ['user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 305. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **yaml_definition:**
  - name: fk_log_user
  - columns: ['user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: ユーザーへの外部キー

---

#### 306. ⚠️ 外部キー fk_log_user のON DELETE設定が不一致

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_log_user
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 307. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['id'] がDDLにのみ存在します

**テーブル:** SYS_TokenStore

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_token_store_user
  - columns: ['user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE

---

#### 308. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['id'] がYAMLにのみ存在します

**テーブル:** SYS_TokenStore

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_token_store_user
  - columns: ['user_id']
  - reference_table: MST_UserAuth
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: CASCADE
  - description: ユーザー認証情報への外部キー

---

#### 309. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_skill_grade_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 310. ⚠️ 外部キー ['evaluator_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - evaluator_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_skill_grade_evaluator
  - columns: ['evaluator_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 311. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - job_type_id
- **target_table:** MST_JobType
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_skill_grade_job_type
  - columns: ['job_type_id']
  - reference_table: MST_JobType
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 職種への外部キー

---

#### 312. ⚠️ 外部キー ['evaluator_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - evaluator_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_skill_grade_evaluator
  - columns: ['evaluator_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 評価者への外部キー

---

#### 313. ⚠️ 外部キー fk_skill_grade_evaluator のON DELETE設定が不一致

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_grade_evaluator
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 314. ⚠️ 外部キー ['related_career_plan_id'] -> MST_CareerPlan.['id'] がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - related_career_plan_id
- **target_table:** MST_CareerPlan
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_TRN_GoalProgress_career_plan
  - columns: ['related_career_plan_id']
  - reference_table: MST_CareerPlan
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 315. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - supervisor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_TRN_GoalProgress_supervisor
  - columns: ['supervisor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 316. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_TRN_GoalProgress_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 317. ⚠️ 外部キー ['related_career_plan_id'] -> MST_CareerPlan.['id'] がYAMLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - related_career_plan_id
- **target_table:** MST_CareerPlan
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_TRN_GoalProgress_career_plan
  - columns: ['related_career_plan_id']
  - reference_table: MST_CareerPlan
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: キャリアプランへの外部キー

---

#### 318. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - supervisor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_TRN_GoalProgress_supervisor
  - columns: ['supervisor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 上司への外部キー

---

#### 319. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_TRN_GoalProgress_approved_by
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 320. ⚠️ 外部キー fk_TRN_GoalProgress_career_plan のON DELETE設定が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_TRN_GoalProgress_career_plan
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 321. ⚠️ 外部キー fk_TRN_GoalProgress_supervisor のON DELETE設定が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_TRN_GoalProgress_supervisor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 322. ⚠️ 外部キー fk_TRN_GoalProgress_approved_by のON DELETE設定が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_TRN_GoalProgress_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 323. ⚠️ 外部キー ['recipient_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - recipient_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_notification_recipient
  - columns: ['recipient_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 324. ⚠️ 外部キー ['sender_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - sender_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_notification_sender
  - columns: ['sender_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 325. ⚠️ 外部キー ['recipient_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - recipient_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_notification_recipient
  - columns: ['recipient_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 受信者への外部キー

---

#### 326. ⚠️ 外部キー ['sender_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - sender_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_notification_sender
  - columns: ['sender_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 送信者への外部キー

---

#### 327. ⚠️ 外部キー fk_notification_sender のON DELETE設定が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_sender
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 328. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - related_project_id
- **target_table:** TRN_ProjectRecord
- **target_columns:**
  - project_record_id
- **ddl_definition:**
  - name: fk_pdu_project
  - columns: ['related_project_id']
  - reference_table: TRN_ProjectRecord
  - reference_columns: ['project_record_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 329. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - related_training_id
- **target_table:** TRN_TrainingHistory
- **target_columns:**
  - training_history_id
- **ddl_definition:**
  - name: fk_pdu_training
  - columns: ['related_training_id']
  - reference_table: TRN_TrainingHistory
  - reference_columns: ['training_history_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 330. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_pdu_approver
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 331. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がYAMLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - related_project_id
- **target_table:** TRN_ProjectRecord
- **target_columns:**
  - project_record_id
- **yaml_definition:**
  - name: fk_pdu_project
  - columns: ['related_project_id']
  - reference_table: TRN_ProjectRecord
  - reference_columns: ['project_record_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 関連案件への外部キー

---

#### 332. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がYAMLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - related_training_id
- **target_table:** TRN_TrainingHistory
- **target_columns:**
  - training_history_id
- **yaml_definition:**
  - name: fk_pdu_training
  - columns: ['related_training_id']
  - reference_table: TRN_TrainingHistory
  - reference_columns: ['training_history_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 関連研修への外部キー

---

#### 333. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_pdu_approver
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 334. ⚠️ 外部キー fk_pdu_training のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_training
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 335. ⚠️ 外部キー fk_pdu_approver のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_approver
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 336. ⚠️ 外部キー fk_pdu_certification のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 337. ⚠️ 外部キー fk_pdu_project のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_project
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 338. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - related_training_id
- **target_table:** TRN_TrainingHistory
- **target_columns:**
  - training_history_id
- **ddl_definition:**
  - name: fk_evidence_training
  - columns: ['related_training_id']
  - reference_table: TRN_TrainingHistory
  - reference_columns: ['training_history_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 339. ⚠️ 外部キー ['related_certification_id'] -> MST_Certification.['id'] がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - related_certification_id
- **target_table:** MST_Certification
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_evidence_certification
  - columns: ['related_certification_id']
  - reference_table: MST_Certification
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 340. ⚠️ 外部キー ['skill_id'] -> MST_SkillItem.['id'] がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_SkillItem
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_evidence_skill
  - columns: ['skill_id']
  - reference_table: MST_SkillItem
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 341. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - related_project_id
- **target_table:** TRN_ProjectRecord
- **target_columns:**
  - project_record_id
- **ddl_definition:**
  - name: fk_evidence_project
  - columns: ['related_project_id']
  - reference_table: TRN_ProjectRecord
  - reference_columns: ['project_record_id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 342. ⚠️ 外部キー ['verified_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - verified_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_evidence_verifier
  - columns: ['verified_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 343. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がYAMLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - related_training_id
- **target_table:** TRN_TrainingHistory
- **target_columns:**
  - training_history_id
- **yaml_definition:**
  - name: fk_evidence_training
  - columns: ['related_training_id']
  - reference_table: TRN_TrainingHistory
  - reference_columns: ['training_history_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 関連研修への外部キー

---

#### 344. ⚠️ 外部キー ['related_certification_id'] -> MST_Certification.['id'] がYAMLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - related_certification_id
- **target_table:** MST_Certification
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_evidence_certification
  - columns: ['related_certification_id']
  - reference_table: MST_Certification
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 関連資格への外部キー

---

#### 345. ⚠️ 外部キー ['skill_id'] -> MST_SkillItem.['id'] がYAMLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_SkillItem
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_evidence_skill
  - columns: ['skill_id']
  - reference_table: MST_SkillItem
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: スキル項目への外部キー

---

#### 346. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がYAMLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - related_project_id
- **target_table:** TRN_ProjectRecord
- **target_columns:**
  - project_record_id
- **yaml_definition:**
  - name: fk_evidence_project
  - columns: ['related_project_id']
  - reference_table: TRN_ProjectRecord
  - reference_columns: ['project_record_id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 関連案件への外部キー

---

#### 347. ⚠️ 外部キー ['verified_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - verified_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_evidence_verifier
  - columns: ['verified_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 検証者への外部キー

---

#### 348. ⚠️ 外部キー fk_evidence_training のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_training
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 349. ⚠️ 外部キー fk_evidence_certification のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 350. ⚠️ 外部キー fk_evidence_project のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_project
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 351. ⚠️ 外部キー fk_evidence_verifier のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_verifier
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 352. ⚠️ 外部キー ['certification_id'] -> MST_Certification.['id'] がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - certification_id
- **target_table:** MST_Certification
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_skill_certification
  - columns: ['certification_id']
  - reference_table: MST_Certification
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 353. ⚠️ 外部キー ['assessor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - assessor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_skill_assessor
  - columns: ['assessor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 354. ⚠️ 外部キー ['certification_id'] -> MST_Certification.['id'] がYAMLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - certification_id
- **target_table:** MST_Certification
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_skill_certification
  - columns: ['certification_id']
  - reference_table: MST_Certification
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 資格への外部キー

---

#### 355. ⚠️ 外部キー ['assessor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - assessor_id
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_skill_assessor
  - columns: ['assessor_id']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 評価者への外部キー

---

#### 356. ⚠️ 外部キー fk_skill_category のON DELETE設定が不一致

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_category
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 357. ⚠️ 外部キー fk_skill_assessor のON DELETE設定が不一致

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_assessor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 358. ⚠️ 外部キー fk_skill_certification のON DELETE設定が不一致

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 359. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **ddl_definition:**
  - name: fk_training_history_approver
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET

---

#### 360. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - approved_by
- **target_table:** MST_Employee
- **target_columns:**
  - id
- **yaml_definition:**
  - name: fk_training_history_approver
  - columns: ['approved_by']
  - reference_table: MST_Employee
  - reference_columns: ['id']
  - on_update: CASCADE
  - on_delete: SET NULL
  - description: 承認者への外部キー

---

#### 361. ⚠️ 外部キー fk_training_history_approver のON DELETE設定が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_training_history_approver
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 362. ⚠️ 外部キー fk_training_history_program のON DELETE設定が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_training_history_program
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 363. ⚠️ 外部キー ['executed_by'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - executed_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **ddl_definition:**
  - name: fk_WRK_BatchJobLog_executed_by
  - columns: ['executed_by']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 364. ⚠️ 外部キー ['executed_by'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - executed_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - user_id
- **yaml_definition:**
  - name: fk_WRK_BatchJobLog_executed_by
  - columns: ['executed_by']
  - reference_table: MST_UserAuth
  - reference_columns: ['user_id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: 実行者（ユーザー認証情報）への外部キー

