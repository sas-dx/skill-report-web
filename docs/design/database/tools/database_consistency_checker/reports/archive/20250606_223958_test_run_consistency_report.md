# データベース整合性チェックレポート

**チェック日時:** 2025-06-06 22:39:58
**対象テーブル数:** 100
**総チェック数:** 628

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

### 5. データ型整合性

**目的:** DDLとYAMLファイル間でのデータ型定義の詳細整合性確認

**チェック内容:** データ型の詳細比較、長さ・精度・スケールの一致確認、ENUM値の整合性確認

**検出する問題:** データ型不一致、長さ・精度の相違、ENUM値の不整合

### 6. 制約整合性

**目的:** CHECK制約、UNIQUE制約、PRIMARY KEY制約、インデックス制約の整合性確認

**チェック内容:** CHECK制約の条件一致、UNIQUE制約の対象カラム一致、PRIMARY KEY制約の整合性、インデックス制約の詳細比較

**検出する問題:** 制約条件不一致、制約対象カラム相違、制約定義漏れ、インデックス設定不整合

### 7. YAMLフォーマット整合性

**目的:** YAMLファイルが標準テンプレートに準拠しているかの確認

**チェック内容:** 必須セクション存在確認、セクション内構造確認、データ型妥当性確認、テンプレート準拠確認

**検出する問題:** 必須セクション不足、構造不整合、データ型不正、テンプレート非準拠

### 8. 修正提案

**目的:** 問題の自動修正提案と修正コマンド生成による開発効率向上

**チェック内容:** テーブル定義修正提案、カラム定義修正提案、制約修正提案、自動修正コマンド生成

**検出する問題:** 修正方法不明、手動修正の手間、修正漏れリスク

### 9. マルチテナント対応

**目的:** tenant_id必須確認、テナント用インデックス・制約確認

**チェック内容:** tenant_idカラム存在確認、テナント用インデックス確認、テナント制約確認、外部キーテナント整合性確認

**検出する問題:** tenant_id不足、テナントインデックス不足、テナント制約不備、テナント間参照問題

### 10. 要求仕様ID追跡

**目的:** 要求仕様IDとテーブル・カラムの対応関係確認によるトレーサビリティ確保

**チェック内容:** 要求仕様ID網羅性確認、要求仕様ID妥当性確認、要求仕様ID形式チェック、未割当項目検出

**検出する問題:** 要求仕様ID未割当、要求仕様ID不正、要求仕様ID重複、トレーサビリティ不備

### 11. パフォーマンス影響分析

**目的:** インデックスカバレッジ分析、クエリパフォーマンス予測、データ量影響分析

**チェック内容:** インデックスカバレッジ分析、クエリパフォーマンス予測、データ量影響分析、スロークエリ予測

**検出する問題:** インデックス不足、パフォーマンス劣化予測、データ量超過リスク、クエリ最適化不備

## 📊 結果サマリー

| 重要度 | 件数 | 割合 |
|--------|------|------|
| ⚠️ WARNING | 289 | 46.0% |
| ❌ ERROR | 339 | 54.0% |

### 🎯 総合判定

❌ **修正が必要な問題があります**

重要な問題が検出されました。以下の詳細結果を確認して修正してください。

## 🔍 チェック別統計

| チェック名 | 成功 | 警告 | エラー | 情報 | 合計 |
|------------|------|------|--------|------|------|
| テーブル存在確認 | 0 | 0 | 100 | 0 | 100 |
| 孤立ファイル検出 | 0 | 102 | 0 | 0 | 102 |
| 外部キー整合性 | 0 | 187 | 188 | 0 | 375 |
| データ型整合性 | 0 | 0 | 51 | 0 | 51 |

## 📋 詳細結果

### 🔍 テーブル存在確認 (100件)

#### 1. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** HIS_AuditLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'HIS_AuditLog'を追加してください

---

#### 2. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'HIS_NotificationLog'を追加してください

---

#### 3. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** HIS_ReportGeneration

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'HIS_ReportGeneration'を追加してください

---

#### 4. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** HIS_TenantBilling

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'HIS_TenantBilling'を追加してください

---

#### 5. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_CareerPlan

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_CareerPlan'を追加してください

---

#### 6. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Certification

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Certification'を追加してください

---

#### 7. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_CertificationRequirement'を追加してください

---

#### 8. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Department

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Department'を追加してください

---

#### 9. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Employee

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Employee'を追加してください

---

#### 10. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_EmployeeDepartment'を追加してください

---

#### 11. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_EmployeeJobType'を追加してください

---

#### 12. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_EmployeePosition'を追加してください

---

#### 13. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_JobType

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_JobType'を追加してください

---

#### 14. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_JobTypeSkill'を追加してください

---

#### 15. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_JobTypeSkillGrade'を追加してください

---

#### 16. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_NotificationSettings'を追加してください

---

#### 17. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_NotificationTemplate'を追加してください

---

#### 18. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Permission

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Permission'を追加してください

---

#### 19. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Position

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Position'を追加してください

---

#### 20. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_ReportTemplate'を追加してください

---

#### 21. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Role

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Role'を追加してください

---

#### 22. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_RolePermission

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_RolePermission'を追加してください

---

#### 23. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Skill

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Skill'を追加してください

---

#### 24. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_SkillCategory

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_SkillCategory'を追加してください

---

#### 25. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_SkillGrade

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_SkillGrade'を追加してください

---

#### 26. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_SkillGradeRequirement'を追加してください

---

#### 27. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_SkillHierarchy'を追加してください

---

#### 28. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_SkillItem

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_SkillItem'を追加してください

---

#### 29. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_SystemConfig

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_SystemConfig'を追加してください

---

#### 30. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_Tenant

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_Tenant'を追加してください

---

#### 31. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_TenantSettings

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_TenantSettings'を追加してください

---

#### 32. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_TrainingProgram'を追加してください

---

#### 33. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_UserAuth

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_UserAuth'を追加してください

---

#### 34. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** MST_UserRole

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'MST_UserRole'を追加してください

---

#### 35. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_BackupHistory'を追加してください

---

#### 36. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_IntegrationConfig'を追加してください

---

#### 37. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_MasterData

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_MasterData'を追加してください

---

#### 38. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_SkillIndex'を追加してください

---

#### 39. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_SkillMatrix'を追加してください

---

#### 40. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_SystemLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_SystemLog'を追加してください

---

#### 41. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_TenantUsage

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_TenantUsage'を追加してください

---

#### 42. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** SYS_TokenStore

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'SYS_TokenStore'を追加してください

---

#### 43. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-001

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-001.sql
  - TBL-001_details.yaml
- **修正提案:**
  - DDLファイル'TBL-001.sql'を作成してください
  - テーブル詳細YAML'TBL-001_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-001'の関連定義を追加してください

---

#### 44. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-002

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-002.sql
  - TBL-002_details.yaml
- **修正提案:**
  - DDLファイル'TBL-002.sql'を作成してください
  - テーブル詳細YAML'TBL-002_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-002'の関連定義を追加してください

---

#### 45. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-003

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-003.sql
  - TBL-003_details.yaml
- **修正提案:**
  - DDLファイル'TBL-003.sql'を作成してください
  - テーブル詳細YAML'TBL-003_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-003'の関連定義を追加してください

---

#### 46. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-004

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-004.sql
  - TBL-004_details.yaml
- **修正提案:**
  - DDLファイル'TBL-004.sql'を作成してください
  - テーブル詳細YAML'TBL-004_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-004'の関連定義を追加してください

---

#### 47. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-005

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-005.sql
  - TBL-005_details.yaml
- **修正提案:**
  - DDLファイル'TBL-005.sql'を作成してください
  - テーブル詳細YAML'TBL-005_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-005'の関連定義を追加してください

---

#### 48. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-006

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-006.sql
  - TBL-006_details.yaml
- **修正提案:**
  - DDLファイル'TBL-006.sql'を作成してください
  - テーブル詳細YAML'TBL-006_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-006'の関連定義を追加してください

---

#### 49. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-007

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-007.sql
  - TBL-007_details.yaml
- **修正提案:**
  - DDLファイル'TBL-007.sql'を作成してください
  - テーブル詳細YAML'TBL-007_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-007'の関連定義を追加してください

---

#### 50. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-008

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-008.sql
  - TBL-008_details.yaml
- **修正提案:**
  - DDLファイル'TBL-008.sql'を作成してください
  - テーブル詳細YAML'TBL-008_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-008'の関連定義を追加してください

---

#### 51. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-009

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-009.sql
  - TBL-009_details.yaml
- **修正提案:**
  - DDLファイル'TBL-009.sql'を作成してください
  - テーブル詳細YAML'TBL-009_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-009'の関連定義を追加してください

---

#### 52. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-010

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-010.sql
  - TBL-010_details.yaml
- **修正提案:**
  - DDLファイル'TBL-010.sql'を作成してください
  - テーブル詳細YAML'TBL-010_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-010'の関連定義を追加してください

---

#### 53. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-011

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-011.sql
  - TBL-011_details.yaml
- **修正提案:**
  - DDLファイル'TBL-011.sql'を作成してください
  - テーブル詳細YAML'TBL-011_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-011'の関連定義を追加してください

---

#### 54. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-012

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-012.sql
  - TBL-012_details.yaml
- **修正提案:**
  - DDLファイル'TBL-012.sql'を作成してください
  - テーブル詳細YAML'TBL-012_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-012'の関連定義を追加してください

---

#### 55. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-013

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-013.sql
  - TBL-013_details.yaml
- **修正提案:**
  - DDLファイル'TBL-013.sql'を作成してください
  - テーブル詳細YAML'TBL-013_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-013'の関連定義を追加してください

---

#### 56. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-014

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-014.sql
  - TBL-014_details.yaml
- **修正提案:**
  - DDLファイル'TBL-014.sql'を作成してください
  - テーブル詳細YAML'TBL-014_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-014'の関連定義を追加してください

---

#### 57. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-015

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-015.sql
  - TBL-015_details.yaml
- **修正提案:**
  - DDLファイル'TBL-015.sql'を作成してください
  - テーブル詳細YAML'TBL-015_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-015'の関連定義を追加してください

---

#### 58. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-016

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-016.sql
  - TBL-016_details.yaml
- **修正提案:**
  - DDLファイル'TBL-016.sql'を作成してください
  - テーブル詳細YAML'TBL-016_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-016'の関連定義を追加してください

---

#### 59. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-017

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-017.sql
  - TBL-017_details.yaml
- **修正提案:**
  - DDLファイル'TBL-017.sql'を作成してください
  - テーブル詳細YAML'TBL-017_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-017'の関連定義を追加してください

---

#### 60. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-018

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-018.sql
  - TBL-018_details.yaml
- **修正提案:**
  - DDLファイル'TBL-018.sql'を作成してください
  - テーブル詳細YAML'TBL-018_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-018'の関連定義を追加してください

---

#### 61. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-019

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-019.sql
  - TBL-019_details.yaml
- **修正提案:**
  - DDLファイル'TBL-019.sql'を作成してください
  - テーブル詳細YAML'TBL-019_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-019'の関連定義を追加してください

---

#### 62. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-020

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-020.sql
  - TBL-020_details.yaml
- **修正提案:**
  - DDLファイル'TBL-020.sql'を作成してください
  - テーブル詳細YAML'TBL-020_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-020'の関連定義を追加してください

---

#### 63. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-021

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-021.sql
  - TBL-021_details.yaml
- **修正提案:**
  - DDLファイル'TBL-021.sql'を作成してください
  - テーブル詳細YAML'TBL-021_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-021'の関連定義を追加してください

---

#### 64. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-022

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-022.sql
  - TBL-022_details.yaml
- **修正提案:**
  - DDLファイル'TBL-022.sql'を作成してください
  - テーブル詳細YAML'TBL-022_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-022'の関連定義を追加してください

---

#### 65. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-023

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-023.sql
  - TBL-023_details.yaml
- **修正提案:**
  - DDLファイル'TBL-023.sql'を作成してください
  - テーブル詳細YAML'TBL-023_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-023'の関連定義を追加してください

---

#### 66. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-024

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-024.sql
  - TBL-024_details.yaml
- **修正提案:**
  - DDLファイル'TBL-024.sql'を作成してください
  - テーブル詳細YAML'TBL-024_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-024'の関連定義を追加してください

---

#### 67. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-025

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-025.sql
  - TBL-025_details.yaml
- **修正提案:**
  - DDLファイル'TBL-025.sql'を作成してください
  - テーブル詳細YAML'TBL-025_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-025'の関連定義を追加してください

---

#### 68. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-026

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-026.sql
  - TBL-026_details.yaml
- **修正提案:**
  - DDLファイル'TBL-026.sql'を作成してください
  - テーブル詳細YAML'TBL-026_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-026'の関連定義を追加してください

---

#### 69. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-027

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-027.sql
  - TBL-027_details.yaml
- **修正提案:**
  - DDLファイル'TBL-027.sql'を作成してください
  - テーブル詳細YAML'TBL-027_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-027'の関連定義を追加してください

---

#### 70. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-028

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-028.sql
  - TBL-028_details.yaml
- **修正提案:**
  - DDLファイル'TBL-028.sql'を作成してください
  - テーブル詳細YAML'TBL-028_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-028'の関連定義を追加してください

---

#### 71. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-029

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-029.sql
  - TBL-029_details.yaml
- **修正提案:**
  - DDLファイル'TBL-029.sql'を作成してください
  - テーブル詳細YAML'TBL-029_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-029'の関連定義を追加してください

---

#### 72. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-030

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-030.sql
  - TBL-030_details.yaml
- **修正提案:**
  - DDLファイル'TBL-030.sql'を作成してください
  - テーブル詳細YAML'TBL-030_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-030'の関連定義を追加してください

---

#### 73. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-031

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-031.sql
  - TBL-031_details.yaml
- **修正提案:**
  - DDLファイル'TBL-031.sql'を作成してください
  - テーブル詳細YAML'TBL-031_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-031'の関連定義を追加してください

---

#### 74. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-032

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-032.sql
  - TBL-032_details.yaml
- **修正提案:**
  - DDLファイル'TBL-032.sql'を作成してください
  - テーブル詳細YAML'TBL-032_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-032'の関連定義を追加してください

---

#### 75. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-033

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-033.sql
  - TBL-033_details.yaml
- **修正提案:**
  - DDLファイル'TBL-033.sql'を作成してください
  - テーブル詳細YAML'TBL-033_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-033'の関連定義を追加してください

---

#### 76. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-034

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-034.sql
  - TBL-034_details.yaml
- **修正提案:**
  - DDLファイル'TBL-034.sql'を作成してください
  - テーブル詳細YAML'TBL-034_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-034'の関連定義を追加してください

---

#### 77. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-035

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-035.sql
  - TBL-035_details.yaml
- **修正提案:**
  - DDLファイル'TBL-035.sql'を作成してください
  - テーブル詳細YAML'TBL-035_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-035'の関連定義を追加してください

---

#### 78. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-036

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-036.sql
  - TBL-036_details.yaml
- **修正提案:**
  - DDLファイル'TBL-036.sql'を作成してください
  - テーブル詳細YAML'TBL-036_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-036'の関連定義を追加してください

---

#### 79. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-037

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-037.sql
  - TBL-037_details.yaml
- **修正提案:**
  - DDLファイル'TBL-037.sql'を作成してください
  - テーブル詳細YAML'TBL-037_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-037'の関連定義を追加してください

---

#### 80. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-038

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-038.sql
  - TBL-038_details.yaml
- **修正提案:**
  - DDLファイル'TBL-038.sql'を作成してください
  - テーブル詳細YAML'TBL-038_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-038'の関連定義を追加してください

---

#### 81. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-039

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-039.sql
  - TBL-039_details.yaml
- **修正提案:**
  - DDLファイル'TBL-039.sql'を作成してください
  - テーブル詳細YAML'TBL-039_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-039'の関連定義を追加してください

---

#### 82. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-040

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-040.sql
  - TBL-040_details.yaml
- **修正提案:**
  - DDLファイル'TBL-040.sql'を作成してください
  - テーブル詳細YAML'TBL-040_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-040'の関連定義を追加してください

---

#### 83. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-041

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-041.sql
  - TBL-041_details.yaml
- **修正提案:**
  - DDLファイル'TBL-041.sql'を作成してください
  - テーブル詳細YAML'TBL-041_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-041'の関連定義を追加してください

---

#### 84. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-042

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-042.sql
  - TBL-042_details.yaml
- **修正提案:**
  - DDLファイル'TBL-042.sql'を作成してください
  - テーブル詳細YAML'TBL-042_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-042'の関連定義を追加してください

---

#### 85. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-043

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-043.sql
  - TBL-043_details.yaml
- **修正提案:**
  - DDLファイル'TBL-043.sql'を作成してください
  - テーブル詳細YAML'TBL-043_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-043'の関連定義を追加してください

---

#### 86. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-044

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-044.sql
  - TBL-044_details.yaml
- **修正提案:**
  - DDLファイル'TBL-044.sql'を作成してください
  - テーブル詳細YAML'TBL-044_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-044'の関連定義を追加してください

---

#### 87. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-045

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-045.sql
  - TBL-045_details.yaml
- **修正提案:**
  - DDLファイル'TBL-045.sql'を作成してください
  - テーブル詳細YAML'TBL-045_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-045'の関連定義を追加してください

---

#### 88. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-046

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-046.sql
  - TBL-046_details.yaml
- **修正提案:**
  - DDLファイル'TBL-046.sql'を作成してください
  - テーブル詳細YAML'TBL-046_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-046'の関連定義を追加してください

---

#### 89. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-047

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-047.sql
  - TBL-047_details.yaml
- **修正提案:**
  - DDLファイル'TBL-047.sql'を作成してください
  - テーブル詳細YAML'TBL-047_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-047'の関連定義を追加してください

---

#### 90. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-048

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-048.sql
  - TBL-048_details.yaml
- **修正提案:**
  - DDLファイル'TBL-048.sql'を作成してください
  - テーブル詳細YAML'TBL-048_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-048'の関連定義を追加してください

---

#### 91. ❌ テーブル定義の不整合 - 存在: テーブル一覧.md | 不足: entity_relationships.yaml, DDLファイル, テーブル詳細YAML

**テーブル:** TBL-049

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ✅ 存在
  - entity_relationships.yaml: ❌ 不足
  - DDLファイル: ❌ 不足
  - テーブル詳細YAML: ❌ 不足
- **期待されるファイル:**
  - TBL-049.sql
  - TBL-049_details.yaml
- **修正提案:**
  - DDLファイル'TBL-049.sql'を作成してください
  - テーブル詳細YAML'TBL-049_details.yaml'を作成してください
  - entity_relationships.yamlに'TBL-049'の関連定義を追加してください

---

#### 92. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_EmployeeSkillGrade'を追加してください

---

#### 93. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_GoalProgress'を追加してください

---

#### 94. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_Notification

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_Notification'を追加してください

---

#### 95. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_PDU

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_PDU'を追加してください

---

#### 96. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_ProjectRecord'を追加してください

---

#### 97. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_SkillEvidence'を追加してください

---

#### 98. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_SkillRecord'を追加してください

---

#### 99. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'TRN_TrainingHistory'を追加してください

---

#### 100. ❌ テーブル定義の不整合 - 存在: entity_relationships.yaml, DDLファイル, テーブル詳細YAML | 不足: テーブル一覧.md

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **存在状況:**
  - テーブル一覧.md: ❌ 不足
  - entity_relationships.yaml: ✅ 存在
  - DDLファイル: ✅ 存在
  - テーブル詳細YAML: ✅ 存在
- **修正提案:**
  - テーブル一覧.mdに'WRK_BatchJobLog'を追加してください


### 🔍 孤立ファイル検出 (102件)

#### 1. ⚠️ 孤立ファイル: MST_Tenant.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Tenant.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 2. ⚠️ 孤立ファイル: MST_SkillGrade.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_SkillGrade.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 3. ⚠️ 孤立ファイル: MST_SkillHierarchy.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_SkillHierarchy.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 4. ⚠️ 孤立ファイル: SYS_BackupHistory.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_BackupHistory.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 5. ⚠️ 孤立ファイル: MST_EmployeePosition.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_EmployeePosition.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 6. ⚠️ 孤立ファイル: MST_TrainingProgram.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_TrainingProgram.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 7. ⚠️ 孤立ファイル: MST_SkillGradeRequirement.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_SkillGradeRequirement.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 8. ⚠️ 孤立ファイル: TRN_PDU.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_PDU.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 9. ⚠️ 孤立ファイル: MST_Certification.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Certification.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 10. ⚠️ 孤立ファイル: TRN_TrainingHistory.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_TrainingHistory.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 11. ⚠️ 孤立ファイル: MST_ReportTemplate.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_ReportTemplate.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 12. ⚠️ 孤立ファイル: MST_Position.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Position.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 13. ⚠️ 孤立ファイル: SYS_SkillMatrix.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_SkillMatrix.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 14. ⚠️ 孤立ファイル: TRN_EmployeeSkillGrade.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_EmployeeSkillGrade.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 15. ⚠️ 孤立ファイル: MST_CareerPlan.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_CareerPlan.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 16. ⚠️ 孤立ファイル: SYS_MasterData.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_MasterData.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 17. ⚠️ 孤立ファイル: SYS_SystemLog.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_SystemLog.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 18. ⚠️ 孤立ファイル: MST_TenantSettings.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_TenantSettings.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 19. ⚠️ 孤立ファイル: MST_SkillItem.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_SkillItem.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 20. ⚠️ 孤立ファイル: HIS_TenantBilling.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** HIS_TenantBilling.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 21. ⚠️ 孤立ファイル: MST_Role.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Role.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 22. ⚠️ 孤立ファイル: MST_UserRole.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_UserRole.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 23. ⚠️ 孤立ファイル: MST_UserAuth.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_UserAuth.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 24. ⚠️ 孤立ファイル: MST_Department.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Department.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 25. ⚠️ 孤立ファイル: MST_Permission.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Permission.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 26. ⚠️ 孤立ファイル: WRK_BatchJobLog.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** WRK_BatchJobLog.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 27. ⚠️ 孤立ファイル: HIS_NotificationLog.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** HIS_NotificationLog.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 28. ⚠️ 孤立ファイル: MST_JobTypeSkill.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_JobTypeSkill.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 29. ⚠️ 孤立ファイル: SYS_IntegrationConfig.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_IntegrationConfig.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 30. ⚠️ 孤立ファイル: SYS_TenantUsage.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_TenantUsage.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 31. ⚠️ 孤立ファイル: MST_NotificationTemplate.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_NotificationTemplate.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 32. ⚠️ 孤立ファイル: MST_EmployeeJobType.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_EmployeeJobType.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 33. ⚠️ 孤立ファイル: MST_NotificationSettings.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_NotificationSettings.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 34. ⚠️ 孤立ファイル: TRN_SkillRecord.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_SkillRecord.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 35. ⚠️ 孤立ファイル: TRN_SkillEvidence.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_SkillEvidence.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 36. ⚠️ 孤立ファイル: MST_JobTypeSkillGrade.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_JobTypeSkillGrade.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 37. ⚠️ 孤立ファイル: TRN_Notification.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_Notification.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 38. ⚠️ 孤立ファイル: MST_Employee.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Employee.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 39. ⚠️ 孤立ファイル: MST_SystemConfig.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_SystemConfig.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 40. ⚠️ 孤立ファイル: TRN_ProjectRecord.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_ProjectRecord.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 41. ⚠️ 孤立ファイル: TRN_GoalProgress.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** TRN_GoalProgress.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 42. ⚠️ 孤立ファイル: MST_SkillCategory.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_SkillCategory.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 43. ⚠️ 孤立ファイル: MST_EmployeeDepartment.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_EmployeeDepartment.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 44. ⚠️ 孤立ファイル: HIS_ReportGeneration.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** HIS_ReportGeneration.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 45. ⚠️ 孤立ファイル: MST_JobType.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_JobType.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 46. ⚠️ 孤立ファイル: SYS_TokenStore.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_TokenStore.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 47. ⚠️ 孤立ファイル: HIS_AuditLog.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** HIS_AuditLog.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 48. ⚠️ 孤立ファイル: MST_RolePermission.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_RolePermission.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 49. ⚠️ 孤立ファイル: SYS_SkillIndex.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** SYS_SkillIndex.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 50. ⚠️ 孤立ファイル: MST_CertificationRequirement.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_CertificationRequirement.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 51. ⚠️ 孤立ファイル: MST_Skill.sql

**詳細情報:**
- **file_type:** ddl_files
- **file_name:** MST_Skill.sql
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 52. ⚠️ 孤立ファイル: MST_JobTypeSkillGrade_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_JobTypeSkillGrade_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 53. ⚠️ 孤立ファイル: MST_Tenant_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Tenant_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 54. ⚠️ 孤立ファイル: MST_NotificationTemplate_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_NotificationTemplate_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 55. ⚠️ 孤立ファイル: SYS_SystemLog_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_SystemLog_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 56. ⚠️ 孤立ファイル: SYS_TenantUsage_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_TenantUsage_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 57. ⚠️ 孤立ファイル: TRN_Notification_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_Notification_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 58. ⚠️ 孤立ファイル: TRN_SkillEvidence_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_SkillEvidence_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 59. ⚠️ 孤立ファイル: HIS_TenantBilling_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** HIS_TenantBilling_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 60. ⚠️ 孤立ファイル: MST_SkillGrade_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_SkillGrade_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 61. ⚠️ 孤立ファイル: MST_CertificationRequirement_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_CertificationRequirement_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 62. ⚠️ 孤立ファイル: MST_TenantSettings_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_TenantSettings_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 63. ⚠️ 孤立ファイル: TRN_EmployeeSkillGrade_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_EmployeeSkillGrade_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 64. ⚠️ 孤立ファイル: MST_ReportTemplate_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_ReportTemplate_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 65. ⚠️ 孤立ファイル: SYS_MasterData_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_MasterData_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 66. ⚠️ 孤立ファイル: HIS_AuditLog_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** HIS_AuditLog_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 67. ⚠️ 孤立ファイル: MST_Certification_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Certification_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 68. ⚠️ 孤立ファイル: MST_NotificationSettings_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_NotificationSettings_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 69. ⚠️ 孤立ファイル: MST_SkillCategory_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_SkillCategory_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 70. ⚠️ 孤立ファイル: TRN_TrainingHistory_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_TrainingHistory_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 71. ⚠️ 孤立ファイル: WRK_BatchJobLog_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** WRK_BatchJobLog_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 72. ⚠️ 孤立ファイル: HIS_ReportGeneration_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** HIS_ReportGeneration_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 73. ⚠️ 孤立ファイル: MST_Role_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Role_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 74. ⚠️ 孤立ファイル: SYS_TokenStore_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_TokenStore_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 75. ⚠️ 孤立ファイル: MST_Position_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Position_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 76. ⚠️ 孤立ファイル: TRN_ProjectRecord_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_ProjectRecord_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 77. ⚠️ 孤立ファイル: MST_Employee_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Employee_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 78. ⚠️ 孤立ファイル: TRN_SkillRecord_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_SkillRecord_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 79. ⚠️ 孤立ファイル: MST_EmployeePosition_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_EmployeePosition_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 80. ⚠️ 孤立ファイル: MST_Department_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Department_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 81. ⚠️ 孤立ファイル: MST_SkillItem_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_SkillItem_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 82. ⚠️ 孤立ファイル: MST_SkillGradeRequirement_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_SkillGradeRequirement_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 83. ⚠️ 孤立ファイル: MST_SkillHierarchy_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_SkillHierarchy_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 84. ⚠️ 孤立ファイル: MST_JobTypeSkill_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_JobTypeSkill_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 85. ⚠️ 孤立ファイル: MST_JobType_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_JobType_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 86. ⚠️ 孤立ファイル: MST_UserRole_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_UserRole_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 87. ⚠️ 孤立ファイル: TRN_GoalProgress_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_GoalProgress_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 88. ⚠️ 孤立ファイル: MST_EmployeeDepartment_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_EmployeeDepartment_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 89. ⚠️ 孤立ファイル: MST_Skill_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Skill_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 90. ⚠️ 孤立ファイル: MST_TrainingProgram_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_TrainingProgram_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 91. ⚠️ 孤立ファイル: MST_Permission_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_Permission_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 92. ⚠️ 孤立ファイル: HIS_NotificationLog_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** HIS_NotificationLog_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 93. ⚠️ 孤立ファイル: SYS_SkillMatrix_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_SkillMatrix_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 94. ⚠️ 孤立ファイル: TRN_PDU_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** TRN_PDU_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 95. ⚠️ 孤立ファイル: MST_RolePermission_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_RolePermission_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 96. ⚠️ 孤立ファイル: MST_CareerPlan_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_CareerPlan_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 97. ⚠️ 孤立ファイル: MST_EmployeeJobType_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_EmployeeJobType_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 98. ⚠️ 孤立ファイル: SYS_IntegrationConfig_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_IntegrationConfig_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 99. ⚠️ 孤立ファイル: SYS_BackupHistory_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_BackupHistory_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 100. ⚠️ 孤立ファイル: MST_SystemConfig_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_SystemConfig_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 101. ⚠️ 孤立ファイル: SYS_SkillIndex_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** SYS_SkillIndex_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません

---

#### 102. ⚠️ 孤立ファイル: MST_UserAuth_details.yaml

**詳細情報:**
- **file_type:** detail_files
- **file_name:** MST_UserAuth_details.yaml
- **reason:** テーブル一覧.mdに対応するテーブルが見つかりません


### 🔍 外部キー整合性 (375件)

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

#### 5. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** HIS_ReportGeneration

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 6. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** HIS_ReportGeneration

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 7. ❌ 外部キー ['requested_by'] -> MST_UserAuth.['id'] がDDLに存在しません

**テーブル:** HIS_ReportGeneration

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - requested_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - id

---

#### 8. ❌ 外部キー ['requested_by'] -> MST_UserAuth.['id'] がYAMLに存在しません

**テーブル:** HIS_ReportGeneration

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - requested_by
- **target_table:** MST_UserAuth
- **target_columns:**
  - id

---

#### 9. ❌ 外部キー fk_tenant_billing_tenant の参照先カラム MST_Tenant.id が存在しません

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

#### 10. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 11. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 12. ❌ 外部キー fk_career_plan_employee の参照先カラム MST_Employee.id が存在しません

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

#### 13. ❌ 外部キー fk_career_plan_target_position の参照先カラム MST_Position.id が存在しません

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

#### 14. ❌ 外部キー fk_career_plan_target_job_type の参照先カラム MST_JobType.id が存在しません

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

#### 15. ❌ 外部キー fk_career_plan_target_department の参照先カラム MST_Department.id が存在しません

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

#### 16. ❌ 外部キー fk_career_plan_mentor の参照先カラム MST_Employee.id が存在しません

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

#### 17. ❌ 外部キー fk_career_plan_supervisor の参照先カラム MST_Employee.id が存在しません

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

#### 18. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 19. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 20. ❌ 外部キー fk_certification_skill_category の参照先カラム MST_SkillCategory.id が存在しません

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

#### 21. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 22. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 23. ❌ 外部キー fk_cert_req_target_job_type の参照先カラム MST_JobType.id が存在しません

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

#### 24. ❌ 外部キー fk_cert_req_target_position の参照先カラム MST_Position.id が存在しません

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

#### 25. ❌ 外部キー fk_cert_req_target_skill_grade の参照先カラム MST_SkillGrade.id が存在しません

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

#### 26. ❌ 外部キー fk_cert_req_target_department の参照先カラム MST_Department.id が存在しません

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

#### 27. ❌ 外部キー fk_cert_req_certification の参照先カラム MST_Certification.id が存在しません

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

#### 28. ❌ 外部キー fk_cert_req_created_by の参照先カラム MST_Employee.id が存在しません

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

#### 29. ❌ 外部キー fk_cert_req_approved_by の参照先カラム MST_Employee.id が存在しません

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

#### 30. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 31. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 32. ❌ 外部キー fk_department_parent の参照先カラム MST_Department.id が存在しません

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

#### 33. ❌ 外部キー fk_department_manager の参照先カラム MST_Employee.id が存在しません

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

#### 34. ❌ 外部キー fk_department_deputy の参照先カラム MST_Employee.id が存在しません

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

#### 35. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 36. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 37. ❌ 外部キー fk_employee_department の参照先カラム MST_Department.id が存在しません

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

#### 38. ❌ 外部キー fk_employee_position の参照先カラム MST_Position.id が存在しません

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

#### 39. ❌ 外部キー fk_employee_job_type の参照先カラム MST_JobType.id が存在しません

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

#### 40. ❌ 外部キー fk_employee_manager の参照先カラム MST_Employee.id が存在しません

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

#### 41. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 42. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 43. ❌ 外部キー fk_MST_EmployeeDepartment_employee の参照先カラム MST_Employee.id が存在しません

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

#### 44. ❌ 外部キー fk_MST_EmployeeDepartment_department の参照先カラム MST_Department.id が存在しません

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

#### 45. ❌ 外部キー fk_MST_EmployeeDepartment_reporting_manager の参照先カラム MST_Employee.id が存在しません

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

#### 46. ❌ 外部キー fk_MST_EmployeeDepartment_approved_by の参照先カラム MST_Employee.id が存在しません

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

#### 47. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 48. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 49. ❌ 外部キー fk_emp_job_type_employee の参照先カラム MST_Employee.id が存在しません

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

#### 50. ❌ 外部キー fk_emp_job_type_job_type の参照先カラム MST_JobType.id が存在しません

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

#### 51. ❌ 外部キー fk_emp_job_type_mentor の参照先カラム MST_Employee.id が存在しません

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

#### 52. ❌ 外部キー fk_emp_job_type_supervisor の参照先カラム MST_Employee.id が存在しません

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

#### 53. ❌ 外部キー fk_emp_job_type_created_by の参照先カラム MST_Employee.id が存在しません

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

#### 54. ❌ 外部キー fk_emp_job_type_approved_by の参照先カラム MST_Employee.id が存在しません

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

#### 55. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 56. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 57. ❌ 外部キー fk_MST_EmployeePosition_employee の参照先カラム MST_Employee.id が存在しません

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

#### 58. ❌ 外部キー fk_MST_EmployeePosition_position の参照先カラム MST_Position.id が存在しません

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

#### 59. ❌ 外部キー fk_MST_EmployeePosition_approved_by の参照先カラム MST_Employee.id が存在しません

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

#### 60. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_JobType

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 61. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_JobType

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 62. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 63. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_JobTypeSkill

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 64. ❌ 外部キー fk_MST_JobTypeSkill_job_type の参照先カラム MST_JobType.id が存在しません

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

#### 65. ❌ 外部キー fk_MST_JobTypeSkill_skill_item の参照先カラム MST_SkillItem.id が存在しません

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

#### 66. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 67. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_JobTypeSkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 68. ❌ 外部キー fk_MST_JobTypeSkillGrade_job_type の参照先カラム MST_JobType.id が存在しません

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

#### 69. ❌ 外部キー fk_MST_JobTypeSkillGrade_skill_grade の参照先カラム MST_SkillGrade.id が存在しません

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

#### 70. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 71. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 72. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 73. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_NotificationTemplate

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 74. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 75. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 76. ❌ 外部キー fk_permission_parent の参照先カラム MST_Permission.id が存在しません

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

#### 77. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Position

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 78. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Position

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 79. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 80. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_ReportTemplate

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 81. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 82. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 83. ❌ 外部キー fk_role_parent の参照先カラム MST_Role.id が存在しません

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

#### 84. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_RolePermission

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 85. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_RolePermission

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 86. ❌ 外部キー ['role_id'] -> MST_Role.['id'] がDDLに存在しません

**テーブル:** MST_RolePermission

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - role_id
- **target_table:** MST_Role
- **target_columns:**
  - id

---

#### 87. ❌ 外部キー ['role_id'] -> MST_Role.['id'] がYAMLに存在しません

**テーブル:** MST_RolePermission

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - role_id
- **target_table:** MST_Role
- **target_columns:**
  - id

---

#### 88. ❌ 外部キー ['permission_id'] -> MST_Permission.['id'] がDDLに存在しません

**テーブル:** MST_RolePermission

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - permission_id
- **target_table:** MST_Permission
- **target_columns:**
  - id

---

#### 89. ❌ 外部キー ['permission_id'] -> MST_Permission.['id'] がYAMLに存在しません

**テーブル:** MST_RolePermission

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - permission_id
- **target_table:** MST_Permission
- **target_columns:**
  - id

---

#### 90. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 91. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 92. ❌ 外部キー fk_MST_Skill_category の参照先カラム MST_SkillCategory.id が存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **issue_type:** missing_target_column
- **foreign_key_name:** fk_MST_Skill_category
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

#### 93. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillCategory

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 94. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillCategory

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 95. ❌ 外部キー fk_skillcategory_parent の参照先カラム MST_SkillCategory.id が存在しません

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

#### 96. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 97. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 98. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 99. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillGradeRequirement

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 100. ❌ 外部キー fk_MST_SkillGradeRequirement_skill_grade の参照先カラム MST_SkillGrade.id が存在しません

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

#### 101. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 102. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 103. ❌ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['id'] がDDLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - parent_skill_id
- **target_table:** MST_SkillHierarchy
- **target_columns:**
  - id

---

#### 104. ❌ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['id'] がYAMLに存在しません

**テーブル:** MST_SkillHierarchy

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - parent_skill_id
- **target_table:** MST_SkillHierarchy
- **target_columns:**
  - id

---

#### 105. ❌ 外部キー fk_hierarchy_skill の参照先カラム MST_SkillItem.id が存在しません

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

#### 106. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 107. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 108. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がDDLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 109. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がYAMLに存在しません

**テーブル:** MST_SkillItem

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 110. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_SystemConfig

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 111. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_SystemConfig

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 112. ❌ 外部キー fk_tenant_settings_tenant の参照先カラム MST_Tenant.id が存在しません

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

#### 113. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 114. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 115. ❌ 外部キー fk_training_program_created_by の参照先カラム MST_Employee.id が存在しません

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

#### 116. ❌ 外部キー fk_training_program_approved_by の参照先カラム MST_Employee.id が存在しません

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

#### 117. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 118. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 119. ❌ 外部キー fk_userauth_employee の参照先カラム MST_Employee.id が存在しません

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

#### 120. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 121. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 122. ❌ 外部キー ['user_id'] -> MST_UserAuth.['id'] がDDLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - id

---

#### 123. ❌ 外部キー ['user_id'] -> MST_UserAuth.['id'] がYAMLに存在しません

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - user_id
- **target_table:** MST_UserAuth
- **target_columns:**
  - id

---

#### 124. ❌ 外部キー fk_userrole_role の参照先カラム MST_Role.id が存在しません

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

#### 125. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 126. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_BackupHistory

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 127. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 128. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_IntegrationConfig

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 129. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_MasterData

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 130. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_MasterData

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 131. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 132. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_SkillIndex

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 133. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 134. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_SkillMatrix

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 135. ❌ 外部キー fk_SYS_SkillMatrix_employee の参照先カラム MST_Employee.id が存在しません

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

#### 136. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 137. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 138. ❌ 外部キー fk_SYS_TenantUsage_tenant の参照先カラム MST_Tenant.id が存在しません

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

#### 139. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** SYS_TokenStore

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 140. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** SYS_TokenStore

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 141. ❌ 外部キー fk_token_store_user の参照先カラム MST_UserAuth.id が存在しません

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

#### 142. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 143. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 144. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がDDLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 145. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がYAMLに存在しません

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 146. ❌ 外部キー fk_skill_grade_employee の参照先カラム MST_Employee.id が存在しません

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

#### 147. ❌ 外部キー fk_skill_grade_job_type の参照先カラム MST_JobType.id が存在しません

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

#### 148. ❌ 外部キー fk_skill_grade_evaluator の参照先カラム MST_Employee.id が存在しません

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

#### 149. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 150. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 151. ❌ 外部キー fk_TRN_GoalProgress_employee の参照先カラム MST_Employee.id が存在しません

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

#### 152. ❌ 外部キー fk_TRN_GoalProgress_supervisor の参照先カラム MST_Employee.id が存在しません

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

#### 153. ❌ 外部キー fk_TRN_GoalProgress_approved_by の参照先カラム MST_Employee.id が存在しません

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

#### 154. ❌ 外部キー fk_TRN_GoalProgress_career_plan の参照先カラム MST_CareerPlan.id が存在しません

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

#### 155. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 156. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 157. ❌ 外部キー fk_notification_recipient の参照先カラム MST_Employee.id が存在しません

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

#### 158. ❌ 外部キー fk_notification_sender の参照先カラム MST_Employee.id が存在しません

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

#### 159. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 160. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 161. ❌ 外部キー fk_pdu_employee の参照先カラム MST_Employee.id が存在しません

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

#### 162. ❌ 外部キー fk_pdu_certification の参照先カラム MST_Certification.id が存在しません

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

#### 163. ❌ 外部キー fk_pdu_approver の参照先カラム MST_Employee.id が存在しません

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

#### 164. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 165. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_ProjectRecord

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 166. ❌ 外部キー fk_project_record_employee の参照先カラム MST_Employee.id が存在しません

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

#### 167. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 168. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 169. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がDDLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 170. ❌ 外部キー ['skill_id'] -> MST_Skill.['id'] がYAMLに存在しません

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - skill_id
- **target_table:** MST_Skill
- **target_columns:**
  - id

---

#### 171. ❌ 外部キー fk_evidence_employee の参照先カラム MST_Employee.id が存在しません

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

#### 172. ❌ 外部キー fk_evidence_skill の参照先カラム MST_SkillItem.id が存在しません

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

#### 173. ❌ 外部キー fk_evidence_verifier の参照先カラム MST_Employee.id が存在しません

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

#### 174. ❌ 外部キー fk_evidence_certification の参照先カラム MST_Certification.id が存在しません

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

#### 175. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 176. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 177. ❌ 外部キー fk_skill_employee の参照先カラム MST_Employee.id が存在しません

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

#### 178. ❌ 外部キー fk_skill_item の参照先カラム MST_SkillItem.id が存在しません

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

#### 179. ❌ 外部キー fk_skill_certification の参照先カラム MST_Certification.id が存在しません

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

#### 180. ❌ 外部キー fk_skill_category の参照先カラム MST_SkillCategory.id が存在しません

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

#### 181. ❌ 外部キー fk_skill_assessor の参照先カラム MST_Employee.id が存在しません

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

#### 182. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 183. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 184. ❌ 外部キー fk_training_history_employee の参照先カラム MST_Employee.id が存在しません

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

#### 185. ❌ 外部キー fk_training_history_program の参照先カラム MST_TrainingProgram.id が存在しません

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

#### 186. ❌ 外部キー fk_training_history_approver の参照先カラム MST_Employee.id が存在しません

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

#### 187. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がDDLに存在しません

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **issue_type:** missing_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 188. ❌ 外部キー ['tenant_id'] -> MST_Tenant.['id'] がYAMLに存在しません

**テーブル:** WRK_BatchJobLog

**詳細情報:**
- **issue_type:** missing_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - id

---

#### 189. ⚠️ 外部キー ['user_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 190. ⚠️ 外部キー ['user_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 191. ⚠️ 外部キー ['integration_config_id'] -> SYS_IntegrationConfig.['id'] がDDLにのみ存在します

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

#### 192. ⚠️ 外部キー ['setting_id'] -> MST_NotificationSettings.['id'] がDDLにのみ存在します

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

#### 193. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がDDLにのみ存在します

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

#### 194. ⚠️ 外部キー ['integration_config_id'] -> SYS_IntegrationConfig.['id'] がYAMLにのみ存在します

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

#### 195. ⚠️ 外部キー ['setting_id'] -> MST_NotificationSettings.['id'] がYAMLにのみ存在します

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

#### 196. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がYAMLにのみ存在します

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

#### 197. ⚠️ 外部キー fk_notification_log_integration のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_integration
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 198. ⚠️ 外部キー fk_notification_log_setting のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_setting
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 199. ⚠️ 外部キー fk_notification_log_template のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_template
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 200. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がDDLにのみ存在します

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

#### 201. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 202. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 203. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 204. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がDDLにのみ存在します

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

#### 205. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 206. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がYAMLにのみ存在します

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

#### 207. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 208. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 209. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 210. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がYAMLにのみ存在します

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

#### 211. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 212. ⚠️ 外部キー fk_career_plan_target_position のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_position
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 213. ⚠️ 外部キー fk_career_plan_target_job_type のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 214. ⚠️ 外部キー fk_career_plan_supervisor のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_supervisor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 215. ⚠️ 外部キー fk_career_plan_target_department のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_department
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 216. ⚠️ 外部キー fk_career_plan_mentor のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_mentor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 217. ⚠️ 外部キー ['skill_category_id'] -> MST_SkillCategory.['id'] がDDLにのみ存在します

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

#### 218. ⚠️ 外部キー ['skill_category_id'] -> MST_SkillCategory.['id'] がYAMLにのみ存在します

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

#### 219. ⚠️ 外部キー fk_certification_skill_category のON DELETE設定が不一致

**テーブル:** MST_Certification

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_certification_skill_category
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 220. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がDDLにのみ存在します

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

#### 221. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 222. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 223. ⚠️ 外部キー ['target_skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

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

#### 224. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がDDLにのみ存在します

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

#### 225. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 226. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がYAMLにのみ存在します

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

#### 227. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 228. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 229. ⚠️ 外部キー ['target_skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

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

#### 230. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がYAMLにのみ存在します

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

#### 231. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 232. ⚠️ 外部キー fk_cert_req_target_position のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_position
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 233. ⚠️ 外部キー fk_cert_req_target_job_type のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 234. ⚠️ 外部キー fk_cert_req_target_skill_grade のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_skill_grade
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 235. ⚠️ 外部キー fk_cert_req_target_department のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_department
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 236. ⚠️ 外部キー fk_cert_req_approved_by のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 237. ⚠️ 外部キー ['manager_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 238. ⚠️ 外部キー ['deputy_manager_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 239. ⚠️ 外部キー ['manager_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 240. ⚠️ 外部キー ['deputy_manager_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 241. ⚠️ 外部キー fk_department_parent のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 242. ⚠️ 外部キー fk_department_manager のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 243. ⚠️ 外部キー fk_department_deputy のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_deputy
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 244. ⚠️ 外部キー fk_employee_job_type のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 245. ⚠️ 外部キー fk_employee_position のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_position
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 246. ⚠️ 外部キー fk_employee_manager のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 247. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 248. ⚠️ 外部キー ['reporting_manager_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 249. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 250. ⚠️ 外部キー ['reporting_manager_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 251. ⚠️ 外部キー fk_MST_EmployeeDepartment_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeeDepartment_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 252. ⚠️ 外部キー fk_MST_EmployeeDepartment_reporting_manager のON DELETE設定が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeeDepartment_reporting_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 253. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 254. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 255. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 256. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 257. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 258. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 259. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 260. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 261. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 262. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 263. ⚠️ 外部キー fk_emp_job_type_supervisor のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_supervisor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 264. ⚠️ 外部キー fk_emp_job_type_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 265. ⚠️ 外部キー fk_emp_job_type_mentor のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_mentor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 266. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 267. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 268. ⚠️ 外部キー fk_MST_EmployeePosition_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeePosition

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeePosition_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 269. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 270. ⚠️ 外部キー ['skill_item_id'] -> MST_SkillItem.['id'] がDDLにのみ存在します

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

#### 271. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 272. ⚠️ 外部キー ['skill_item_id'] -> MST_SkillItem.['id'] がYAMLにのみ存在します

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

#### 273. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

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

#### 274. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 275. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

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

#### 276. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 277. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がDDLにのみ存在します

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

#### 278. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がYAMLにのみ存在します

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

#### 279. ⚠️ 外部キー fk_notification_settings_template のON DELETE設定が不一致

**テーブル:** MST_NotificationSettings

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_settings_template
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 280. ⚠️ 外部キー ['parent_permission_id'] -> MST_Permission.['id'] がDDLにのみ存在します

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

#### 281. ⚠️ 外部キー ['parent_permission_id'] -> MST_Permission.['id'] がYAMLにのみ存在します

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

#### 282. ⚠️ 外部キー fk_permission_parent のON DELETE設定が不一致

**テーブル:** MST_Permission

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_permission_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 283. ⚠️ 外部キー ['parent_role_id'] -> MST_Role.['id'] がDDLにのみ存在します

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

#### 284. ⚠️ 外部キー ['parent_role_id'] -> MST_Role.['id'] がYAMLにのみ存在します

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

#### 285. ⚠️ 外部キー fk_role_parent のON DELETE設定が不一致

**テーブル:** MST_Role

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_role_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 286. ⚠️ 外部キー ['tenant_id'] -> MST_Tenant.['tenant_id'] がDDLにのみ存在します

**テーブル:** MST_Skill

**詳細情報:**
- **issue_type:** unexpected_ddl_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - tenant_id
- **ddl_definition:**
  - name: fk_MST_Skill_tenant
  - columns: ['tenant_id']
  - reference_table: MST_Tenant
  - reference_columns: ['tenant_id']
  - on_update: CASCADE
  - on_delete: RESTRICT

---

#### 287. ⚠️ 外部キー ['tenant_id'] -> MST_Tenant.['tenant_id'] がYAMLにのみ存在します

**テーブル:** MST_Skill

**詳細情報:**
- **issue_type:** unexpected_yaml_foreign_key
- **source_columns:**
  - tenant_id
- **target_table:** MST_Tenant
- **target_columns:**
  - tenant_id
- **yaml_definition:**
  - name: fk_MST_Skill_tenant
  - columns: ['tenant_id']
  - reference_table: MST_Tenant
  - reference_columns: ['tenant_id']
  - on_update: CASCADE
  - on_delete: RESTRICT
  - description: MST_Tenantへの外部キー

---

#### 288. ⚠️ 外部キー fk_skillcategory_parent のON DELETE設定が不一致

**テーブル:** MST_SkillCategory

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skillcategory_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 289. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

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

#### 290. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

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

#### 291. ⚠️ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['skill_id'] がDDLにのみ存在します

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

#### 292. ⚠️ 外部キー ['parent_skill_id'] -> MST_SkillHierarchy.['skill_id'] がYAMLにのみ存在します

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

#### 293. ⚠️ 外部キー ['parent_tenant_id'] -> MST_Tenant.['tenant_id'] がDDLにのみ存在します

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

#### 294. ⚠️ 外部キー ['parent_tenant_id'] -> MST_Tenant.['tenant_id'] がYAMLにのみ存在します

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

#### 295. ⚠️ 外部キー fk_tenant_parent のON DELETE設定が不一致

**テーブル:** MST_Tenant

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_tenant_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 296. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 297. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 298. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 299. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 300. ⚠️ 外部キー fk_training_program_approved_by のON DELETE設定が不一致

**テーブル:** MST_TrainingProgram

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_training_program_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 301. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 302. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 303. ⚠️ 外部キー fk_userauth_employee のON DELETE設定が不一致

**テーブル:** MST_UserAuth

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userauth_employee
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 304. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 305. ⚠️ 外部キー ['delegation_source_user_id'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 306. ⚠️ 外部キー ['approved_by'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 307. ⚠️ 外部キー ['assigned_by'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 308. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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

#### 309. ⚠️ 外部キー ['delegation_source_user_id'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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

#### 310. ⚠️ 外部キー ['approved_by'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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

#### 311. ⚠️ 外部キー ['assigned_by'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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

#### 312. ⚠️ 外部キー fk_userrole_assigned_by のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_assigned_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 313. ⚠️ 外部キー fk_userrole_delegation_source のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_delegation_source
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 314. ⚠️ 外部キー fk_userrole_approved_by のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 315. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 316. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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

#### 317. ⚠️ 外部キー fk_log_user のON DELETE設定が不一致

**テーブル:** SYS_SystemLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_log_user
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 318. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['id'] がDDLにのみ存在します

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

#### 319. ⚠️ 外部キー ['user_id'] -> MST_UserAuth.['id'] がYAMLにのみ存在します

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

#### 320. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 321. ⚠️ 外部キー ['evaluator_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 322. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 323. ⚠️ 外部キー ['evaluator_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 324. ⚠️ 外部キー fk_skill_grade_evaluator のON DELETE設定が不一致

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_grade_evaluator
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 325. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 326. ⚠️ 外部キー ['related_career_plan_id'] -> MST_CareerPlan.['id'] がDDLにのみ存在します

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

#### 327. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 328. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 329. ⚠️ 外部キー ['related_career_plan_id'] -> MST_CareerPlan.['id'] がYAMLにのみ存在します

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

#### 330. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 331. ⚠️ 外部キー fk_TRN_GoalProgress_supervisor のON DELETE設定が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_TRN_GoalProgress_supervisor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 332. ⚠️ 外部キー fk_TRN_GoalProgress_career_plan のON DELETE設定が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_TRN_GoalProgress_career_plan
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 333. ⚠️ 外部キー fk_TRN_GoalProgress_approved_by のON DELETE設定が不一致

**テーブル:** TRN_GoalProgress

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_TRN_GoalProgress_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 334. ⚠️ 外部キー ['sender_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 335. ⚠️ 外部キー ['recipient_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 336. ⚠️ 外部キー ['sender_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 337. ⚠️ 外部キー ['recipient_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 338. ⚠️ 外部キー fk_notification_sender のON DELETE設定が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_sender
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 339. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がDDLにのみ存在します

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

#### 340. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 341. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がDDLにのみ存在します

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

#### 342. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がYAMLにのみ存在します

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

#### 343. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 344. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がYAMLにのみ存在します

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

#### 345. ⚠️ 外部キー fk_pdu_certification のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 346. ⚠️ 外部キー fk_pdu_project のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_project
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 347. ⚠️ 外部キー fk_pdu_approver のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_approver
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 348. ⚠️ 外部キー fk_pdu_training のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_training
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 349. ⚠️ 外部キー ['verified_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 350. ⚠️ 外部キー ['related_certification_id'] -> MST_Certification.['id'] がDDLにのみ存在します

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

#### 351. ⚠️ 外部キー ['skill_id'] -> MST_SkillItem.['id'] がDDLにのみ存在します

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

#### 352. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がDDLにのみ存在します

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

#### 353. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がDDLにのみ存在します

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

#### 354. ⚠️ 外部キー ['verified_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 355. ⚠️ 外部キー ['related_certification_id'] -> MST_Certification.['id'] がYAMLにのみ存在します

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

#### 356. ⚠️ 外部キー ['skill_id'] -> MST_SkillItem.['id'] がYAMLにのみ存在します

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

#### 357. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がYAMLにのみ存在します

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

#### 358. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がYAMLにのみ存在します

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

#### 359. ⚠️ 外部キー fk_evidence_verifier のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_verifier
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 360. ⚠️ 外部キー fk_evidence_certification のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 361. ⚠️ 外部キー fk_evidence_project のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_project
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 362. ⚠️ 外部キー fk_evidence_training のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_training
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 363. ⚠️ 外部キー ['certification_id'] -> MST_Certification.['id'] がDDLにのみ存在します

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

#### 364. ⚠️ 外部キー ['assessor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 365. ⚠️ 外部キー ['certification_id'] -> MST_Certification.['id'] がYAMLにのみ存在します

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

#### 366. ⚠️ 外部キー ['assessor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 367. ⚠️ 外部キー fk_skill_certification のON DELETE設定が不一致

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 368. ⚠️ 外部キー fk_skill_assessor のON DELETE設定が不一致

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_assessor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 369. ⚠️ 外部キー fk_skill_category のON DELETE設定が不一致

**テーブル:** TRN_SkillRecord

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_category
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 370. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 371. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 372. ⚠️ 外部キー fk_training_history_program のON DELETE設定が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_training_history_program
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 373. ⚠️ 外部キー fk_training_history_approver のON DELETE設定が不一致

**テーブル:** TRN_TrainingHistory

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_training_history_approver
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 374. ⚠️ 外部キー ['executed_by'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 375. ⚠️ 外部キー ['executed_by'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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


### 🔍 データ型整合性 (51件)

#### 1. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-001.sql

**テーブル:** TBL-001

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-001.sql`

---

#### 2. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-002.sql

**テーブル:** TBL-002

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-002.sql`

---

#### 3. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-003.sql

**テーブル:** TBL-003

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-003.sql`

---

#### 4. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-004.sql

**テーブル:** TBL-004

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-004.sql`

---

#### 5. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-005.sql

**テーブル:** TBL-005

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-005.sql`

---

#### 6. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-005.sql

**テーブル:** TBL-005

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-005.sql`

---

#### 7. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-006.sql

**テーブル:** TBL-006

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-006.sql`

---

#### 8. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-007.sql

**テーブル:** TBL-007

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-007.sql`

---

#### 9. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-008.sql

**テーブル:** TBL-008

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-008.sql`

---

#### 10. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-009.sql

**テーブル:** TBL-009

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-009.sql`

---

#### 11. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-010.sql

**テーブル:** TBL-010

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-010.sql`

---

#### 12. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-010.sql

**テーブル:** TBL-010

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-010.sql`

---

#### 13. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-011.sql

**テーブル:** TBL-011

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-011.sql`

---

#### 14. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-012.sql

**テーブル:** TBL-012

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-012.sql`

---

#### 15. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-013.sql

**テーブル:** TBL-013

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-013.sql`

---

#### 16. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-014.sql

**テーブル:** TBL-014

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-014.sql`

---

#### 17. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-015.sql

**テーブル:** TBL-015

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-015.sql`

---

#### 18. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-016.sql

**テーブル:** TBL-016

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-016.sql`

---

#### 19. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-017.sql

**テーブル:** TBL-017

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-017.sql`

---

#### 20. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-018.sql

**テーブル:** TBL-018

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-018.sql`

---

#### 21. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-019.sql

**テーブル:** TBL-019

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-019.sql`

---

#### 22. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-020.sql

**テーブル:** TBL-020

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-020.sql`

---

#### 23. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-021.sql

**テーブル:** TBL-021

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-021.sql`

---

#### 24. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-022.sql

**テーブル:** TBL-022

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-022.sql`

---

#### 25. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-023.sql

**テーブル:** TBL-023

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-023.sql`

---

#### 26. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-024.sql

**テーブル:** TBL-024

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-024.sql`

---

#### 27. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-025.sql

**テーブル:** TBL-025

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-025.sql`

---

#### 28. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-026.sql

**テーブル:** TBL-026

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-026.sql`

---

#### 29. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-027.sql

**テーブル:** TBL-027

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-027.sql`

---

#### 30. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-028.sql

**テーブル:** TBL-028

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-028.sql`

---

#### 31. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-029.sql

**テーブル:** TBL-029

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-029.sql`

---

#### 32. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-030.sql

**テーブル:** TBL-030

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-030.sql`

---

#### 33. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-031.sql

**テーブル:** TBL-031

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-031.sql`

---

#### 34. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-032.sql

**テーブル:** TBL-032

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-032.sql`

---

#### 35. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-033.sql

**テーブル:** TBL-033

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-033.sql`

---

#### 36. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-034.sql

**テーブル:** TBL-034

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-034.sql`

---

#### 37. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-035.sql

**テーブル:** TBL-035

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-035.sql`

---

#### 38. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-036.sql

**テーブル:** TBL-036

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-036.sql`

---

#### 39. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-037.sql

**テーブル:** TBL-037

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-037.sql`

---

#### 40. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-038.sql

**テーブル:** TBL-038

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-038.sql`

---

#### 41. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-039.sql

**テーブル:** TBL-039

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-039.sql`

---

#### 42. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-040.sql

**テーブル:** TBL-040

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-040.sql`

---

#### 43. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-041.sql

**テーブル:** TBL-041

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-041.sql`

---

#### 44. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-042.sql

**テーブル:** TBL-042

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-042.sql`

---

#### 45. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-043.sql

**テーブル:** TBL-043

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-043.sql`

---

#### 46. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-044.sql

**テーブル:** TBL-044

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-044.sql`

---

#### 47. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-045.sql

**テーブル:** TBL-045

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-045.sql`

---

#### 48. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-046.sql

**テーブル:** TBL-046

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-046.sql`

---

#### 49. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-047.sql

**テーブル:** TBL-047

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-047.sql`

---

#### 50. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-048.sql

**テーブル:** TBL-048

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-048.sql`

---

#### 51. ❌ DDLファイルが存在しません: /home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-049.sql

**テーブル:** TBL-049

**ファイル:** `/home/kurosawa/skill-report-web/docs/design/database/ddl/TBL-049.sql`

