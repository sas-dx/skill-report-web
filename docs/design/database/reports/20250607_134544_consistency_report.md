# データベース整合性チェックレポート

**チェック日時:** 2025-06-07 13:45:44
**対象テーブル数:** 100
**総チェック数:** 1180

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
| ⚠️ WARNING | 493 | 41.8% |
| ❌ ERROR | 339 | 28.7% |
| ℹ️ INFO | 348 | 29.5% |

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
| 制約整合性 | 0 | 51 | 0 | 0 | 51 |
| 修正提案 | 0 | 0 | 0 | 348 | 348 |
| マルチテナント対応 | 0 | 51 | 0 | 0 | 51 |
| 要求仕様ID追跡 | 0 | 51 | 0 | 0 | 51 |
| パフォーマンス影響分析 | 0 | 51 | 0 | 0 | 51 |

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

#### 191. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がDDLにのみ存在します

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

#### 193. ⚠️ 外部キー ['integration_config_id'] -> SYS_IntegrationConfig.['id'] がDDLにのみ存在します

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

#### 194. ⚠️ 外部キー ['template_id'] -> MST_NotificationTemplate.['id'] がYAMLにのみ存在します

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

#### 196. ⚠️ 外部キー ['integration_config_id'] -> SYS_IntegrationConfig.['id'] がYAMLにのみ存在します

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

#### 197. ⚠️ 外部キー fk_notification_log_template のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_template
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

#### 199. ⚠️ 外部キー fk_notification_log_integration のON DELETE設定が不一致

**テーブル:** HIS_NotificationLog

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_log_integration
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 200. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 201. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 202. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がDDLにのみ存在します

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

#### 203. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 204. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がDDLにのみ存在します

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

#### 206. ⚠️ 外部キー ['employee_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 207. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 208. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がYAMLにのみ存在します

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

#### 209. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 210. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がYAMLにのみ存在します

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

#### 212. ⚠️ 外部キー fk_career_plan_supervisor のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_supervisor
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 213. ⚠️ 外部キー fk_career_plan_target_department のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_department
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 214. ⚠️ 外部キー fk_career_plan_target_job_type のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 215. ⚠️ 外部キー fk_career_plan_target_position のON DELETE設定が不一致

**テーブル:** MST_CareerPlan

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_career_plan_target_position
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

#### 220. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 221. ⚠️ 外部キー ['target_skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

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

#### 222. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がDDLにのみ存在します

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

#### 223. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 224. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 225. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がDDLにのみ存在します

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

#### 226. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 227. ⚠️ 外部キー ['target_skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

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

#### 228. ⚠️ 外部キー ['target_department_id'] -> MST_Department.['id'] がYAMLにのみ存在します

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

#### 229. ⚠️ 外部キー ['target_job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 230. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 231. ⚠️ 外部キー ['target_position_id'] -> MST_Position.['id'] がYAMLにのみ存在します

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

#### 232. ⚠️ 外部キー fk_cert_req_approved_by のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 233. ⚠️ 外部キー fk_cert_req_target_skill_grade のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_skill_grade
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 234. ⚠️ 外部キー fk_cert_req_target_department のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_department
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 235. ⚠️ 外部キー fk_cert_req_target_job_type のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 236. ⚠️ 外部キー fk_cert_req_target_position のON DELETE設定が不一致

**テーブル:** MST_CertificationRequirement

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_cert_req_target_position
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

#### 241. ⚠️ 外部キー fk_department_manager のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 242. ⚠️ 外部キー fk_department_deputy のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_deputy
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 243. ⚠️ 外部キー fk_department_parent のON DELETE設定が不一致

**テーブル:** MST_Department

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_department_parent
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 244. ⚠️ 外部キー fk_employee_manager のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 245. ⚠️ 外部キー fk_employee_job_type のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_job_type
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 246. ⚠️ 外部キー fk_employee_position のON DELETE設定が不一致

**テーブル:** MST_Employee

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_employee_position
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

#### 251. ⚠️ 外部キー fk_MST_EmployeeDepartment_reporting_manager のON DELETE設定が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeeDepartment_reporting_manager
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 252. ⚠️ 外部キー fk_MST_EmployeeDepartment_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeeDepartment

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_MST_EmployeeDepartment_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 253. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 254. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 255. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 256. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 257. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 258. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 259. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 260. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 261. ⚠️ 外部キー ['mentor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 262. ⚠️ 外部キー ['created_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 263. ⚠️ 外部キー fk_emp_job_type_approved_by のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_approved_by
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 264. ⚠️ 外部キー fk_emp_job_type_supervisor のON DELETE設定が不一致

**テーブル:** MST_EmployeeJobType

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_emp_job_type_supervisor
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

#### 273. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 274. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がDDLにのみ存在します

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

#### 275. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 276. ⚠️ 外部キー ['skill_grade_id'] -> MST_SkillGrade.['id'] がYAMLにのみ存在します

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

#### 305. ⚠️ 外部キー ['assigned_by'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 307. ⚠️ 外部キー ['delegation_source_user_id'] -> MST_UserAuth.['user_id'] がDDLにのみ存在します

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

#### 309. ⚠️ 外部キー ['assigned_by'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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

#### 311. ⚠️ 外部キー ['delegation_source_user_id'] -> MST_UserAuth.['user_id'] がYAMLにのみ存在します

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

#### 312. ⚠️ 外部キー fk_userrole_delegation_source のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_delegation_source
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 313. ⚠️ 外部キー fk_userrole_assigned_by のON DELETE設定が不一致

**テーブル:** MST_UserRole

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_userrole_assigned_by
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

#### 320. ⚠️ 外部キー ['evaluator_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 321. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がDDLにのみ存在します

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

#### 322. ⚠️ 外部キー ['evaluator_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 323. ⚠️ 外部キー ['job_type_id'] -> MST_JobType.['id'] がYAMLにのみ存在します

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

#### 324. ⚠️ 外部キー fk_skill_grade_evaluator のON DELETE設定が不一致

**テーブル:** TRN_EmployeeSkillGrade

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_skill_grade_evaluator
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 325. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 327. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 328. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 330. ⚠️ 外部キー ['supervisor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 334. ⚠️ 外部キー ['recipient_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 335. ⚠️ 外部キー ['sender_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 336. ⚠️ 外部キー ['recipient_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 337. ⚠️ 外部キー ['sender_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 338. ⚠️ 外部キー fk_notification_sender のON DELETE設定が不一致

**テーブル:** TRN_Notification

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_notification_sender
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 339. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 340. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がDDLにのみ存在します

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

#### 341. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がDDLにのみ存在します

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

#### 342. ⚠️ 外部キー ['approved_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 343. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がYAMLにのみ存在します

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

#### 344. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がYAMLにのみ存在します

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

#### 345. ⚠️ 外部キー fk_pdu_approver のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_approver
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 346. ⚠️ 外部キー fk_pdu_certification のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 347. ⚠️ 外部キー fk_pdu_training のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_training
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 348. ⚠️ 外部キー fk_pdu_project のON DELETE設定が不一致

**テーブル:** TRN_PDU

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_pdu_project
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 349. ⚠️ 外部キー ['skill_id'] -> MST_SkillItem.['id'] がDDLにのみ存在します

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

#### 351. ⚠️ 外部キー ['verified_by'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 352. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がDDLにのみ存在します

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

#### 353. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がDDLにのみ存在します

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

#### 354. ⚠️ 外部キー ['skill_id'] -> MST_SkillItem.['id'] がYAMLにのみ存在します

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

#### 356. ⚠️ 外部キー ['verified_by'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 357. ⚠️ 外部キー ['related_training_id'] -> TRN_TrainingHistory.['training_history_id'] がYAMLにのみ存在します

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

#### 358. ⚠️ 外部キー ['related_project_id'] -> TRN_ProjectRecord.['project_record_id'] がYAMLにのみ存在します

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

#### 359. ⚠️ 外部キー fk_evidence_certification のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_certification
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 360. ⚠️ 外部キー fk_evidence_verifier のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_verifier
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 361. ⚠️ 外部キー fk_evidence_training のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_training
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 362. ⚠️ 外部キー fk_evidence_project のON DELETE設定が不一致

**テーブル:** TRN_SkillEvidence

**詳細情報:**
- **issue_type:** on_delete_mismatch
- **foreign_key_name:** fk_evidence_project
- **ddl_on_delete:** SET
- **yaml_on_delete:** SET NULL

---

#### 363. ⚠️ 外部キー ['assessor_id'] -> MST_Employee.['id'] がDDLにのみ存在します

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

#### 364. ⚠️ 外部キー ['certification_id'] -> MST_Certification.['id'] がDDLにのみ存在します

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

#### 365. ⚠️ 外部キー ['assessor_id'] -> MST_Employee.['id'] がYAMLにのみ存在します

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

#### 366. ⚠️ 外部キー ['certification_id'] -> MST_Certification.['id'] がYAMLにのみ存在します

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


## 🔧 修正提案

### ALL 修正 (240件)

#### 1. MST_TenantSettings

**説明:** 外部キーfk_tenant_settings_tenantの参照先カラムをtenant_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_tenant_settings_tenant

### 問題：
外部キー `fk_tenant_settings_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_TenantSettingsテーブルから外部キー制約を削除
ALTER TABLE MST_TenantSettings DROP FOREIGN KEY fk_tenant_settings_tenant;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_TenantSettings 
ADD CONSTRAINT fk_tenant_settings_tenant
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_TenantSettings_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_tenant_settings_tenant
    column: 参照元カラム名
    reference_table: MST_Tenant
    reference_column: tenant_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 2. MST_UserAuth

**説明:** 外部キーfk_userauth_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_userauth_employee

### 問題：
外部キー `fk_userauth_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_UserAuthテーブルから外部キー制約を削除
ALTER TABLE MST_UserAuth DROP FOREIGN KEY fk_userauth_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_UserAuth 
ADD CONSTRAINT fk_userauth_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_UserAuth_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_userauth_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 3. MST_Role

**説明:** 外部キーfk_role_parentの参照先カラムをparent_role_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_role_parent

### 問題：
外部キー `fk_role_parent` の参照先カラム `MST_Role.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_role_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Roleテーブルから外部キー制約を削除
ALTER TABLE MST_Role DROP FOREIGN KEY fk_role_parent;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Role 
ADD CONSTRAINT fk_role_parent
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Role(parent_role_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Role_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_role_parent
    column: 参照元カラム名
    reference_table: MST_Role
    reference_column: parent_role_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Roleへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 4. MST_Permission

**説明:** 外部キーfk_permission_parentの参照先カラムをparent_permission_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_permission_parent

### 問題：
外部キー `fk_permission_parent` の参照先カラム `MST_Permission.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_permission_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Permissionテーブルから外部キー制約を削除
ALTER TABLE MST_Permission DROP FOREIGN KEY fk_permission_parent;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Permission 
ADD CONSTRAINT fk_permission_parent
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Permission(parent_permission_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Permission_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_permission_parent
    column: 参照元カラム名
    reference_table: MST_Permission
    reference_column: parent_permission_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Permissionへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 5. MST_UserRole

**説明:** 外部キーfk_userrole_roleの参照先カラムをparent_role_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_userrole_role

### 問題：
外部キー `fk_userrole_role` の参照先カラム `MST_Role.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_role_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_UserRoleテーブルから外部キー制約を削除
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_role;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_UserRole 
ADD CONSTRAINT fk_userrole_role
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Role(parent_role_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_UserRole_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_userrole_role
    column: 参照元カラム名
    reference_table: MST_Role
    reference_column: parent_role_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Roleへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 6. MST_Employee

**説明:** 外部キーfk_employee_departmentの参照先カラムをparent_department_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_employee_department

### 問題：
外部キー `fk_employee_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Employeeテーブルから外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_department;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee 
ADD CONSTRAINT fk_employee_department
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Employee_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_employee_department
    column: 参照元カラム名
    reference_table: MST_Department
    reference_column: parent_department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Departmentへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 7. MST_Employee

**説明:** 外部キーfk_employee_positionの参照先カラムをposition_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_employee_position

### 問題：
外部キー `fk_employee_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Employeeテーブルから外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_position;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee 
ADD CONSTRAINT fk_employee_position
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Employee_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_employee_position
    column: 参照元カラム名
    reference_table: MST_Position
    reference_column: position_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Positionへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 8. MST_Employee

**説明:** 外部キーfk_employee_job_typeの参照先カラムをjob_type_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_employee_job_type

### 問題：
外部キー `fk_employee_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Employeeテーブルから外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_job_type;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee 
ADD CONSTRAINT fk_employee_job_type
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Employee_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_employee_job_type
    column: 参照元カラム名
    reference_table: MST_JobType
    reference_column: job_type_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_JobTypeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 9. MST_Employee

**説明:** 外部キーfk_employee_managerの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_employee_manager

### 問題：
外部キー `fk_employee_manager` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Employeeテーブルから外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_manager;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee 
ADD CONSTRAINT fk_employee_manager
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Employee_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_employee_manager
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 10. MST_Department

**説明:** 外部キーfk_department_parentの参照先カラムをparent_department_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_department_parent

### 問題：
外部キー `fk_department_parent` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Departmentテーブルから外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_parent;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Department 
ADD CONSTRAINT fk_department_parent
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Department_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_department_parent
    column: 参照元カラム名
    reference_table: MST_Department
    reference_column: parent_department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Departmentへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 11. MST_Department

**説明:** 外部キーfk_department_managerの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_department_manager

### 問題：
外部キー `fk_department_manager` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Departmentテーブルから外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_manager;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Department 
ADD CONSTRAINT fk_department_manager
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Department_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_department_manager
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 12. MST_Department

**説明:** 外部キーfk_department_deputyの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_department_deputy

### 問題：
外部キー `fk_department_deputy` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Departmentテーブルから外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_deputy;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Department 
ADD CONSTRAINT fk_department_deputy
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Department_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_department_deputy
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 13. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_EmployeeDepartment_employee

### 問題：
外部キー `fk_MST_EmployeeDepartment_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeDepartmentテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment 
ADD CONSTRAINT fk_MST_EmployeeDepartment_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeDepartment_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 14. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_departmentの参照先カラムをparent_department_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_EmployeeDepartment_department

### 問題：
外部キー `fk_MST_EmployeeDepartment_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeDepartmentテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_department;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment 
ADD CONSTRAINT fk_MST_EmployeeDepartment_department
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeDepartment_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_department
    column: 参照元カラム名
    reference_table: MST_Department
    reference_column: parent_department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Departmentへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 15. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_reporting_managerの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_EmployeeDepartment_reporting_manager

### 問題：
外部キー `fk_MST_EmployeeDepartment_reporting_manager` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeDepartmentテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_reporting_manager;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment 
ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeDepartment_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_reporting_manager
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 16. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_approved_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_EmployeeDepartment_approved_by

### 問題：
外部キー `fk_MST_EmployeeDepartment_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeDepartmentテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_approved_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment 
ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeDepartment_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_approved_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 17. MST_EmployeePosition

**説明:** 外部キーfk_MST_EmployeePosition_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_EmployeePosition_employee

### 問題：
外部キー `fk_MST_EmployeePosition_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeePositionテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeePosition 
ADD CONSTRAINT fk_MST_EmployeePosition_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeePosition_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 18. MST_EmployeePosition

**説明:** 外部キーfk_MST_EmployeePosition_positionの参照先カラムをposition_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_EmployeePosition_position

### 問題：
外部キー `fk_MST_EmployeePosition_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeePositionテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_position;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeePosition 
ADD CONSTRAINT fk_MST_EmployeePosition_position
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeePosition_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_position
    column: 参照元カラム名
    reference_table: MST_Position
    reference_column: position_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Positionへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 19. MST_EmployeePosition

**説明:** 外部キーfk_MST_EmployeePosition_approved_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_EmployeePosition_approved_by

### 問題：
外部キー `fk_MST_EmployeePosition_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeePositionテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_approved_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeePosition 
ADD CONSTRAINT fk_MST_EmployeePosition_approved_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeePosition_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_approved_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 20. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_emp_job_type_employee

### 問題：
外部キー `fk_emp_job_type_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeJobTypeテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType 
ADD CONSTRAINT fk_emp_job_type_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeJobType_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_emp_job_type_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 21. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_job_typeの参照先カラムをjob_type_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_emp_job_type_job_type

### 問題：
外部キー `fk_emp_job_type_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeJobTypeテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_job_type;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType 
ADD CONSTRAINT fk_emp_job_type_job_type
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeJobType_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_emp_job_type_job_type
    column: 参照元カラム名
    reference_table: MST_JobType
    reference_column: job_type_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_JobTypeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 22. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_mentorの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_emp_job_type_mentor

### 問題：
外部キー `fk_emp_job_type_mentor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeJobTypeテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_mentor;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType 
ADD CONSTRAINT fk_emp_job_type_mentor
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeJobType_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_emp_job_type_mentor
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 23. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_supervisorの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_emp_job_type_supervisor

### 問題：
外部キー `fk_emp_job_type_supervisor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeJobTypeテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_supervisor;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType 
ADD CONSTRAINT fk_emp_job_type_supervisor
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeJobType_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_emp_job_type_supervisor
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 24. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_created_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_emp_job_type_created_by

### 問題：
外部キー `fk_emp_job_type_created_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeJobTypeテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_created_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType 
ADD CONSTRAINT fk_emp_job_type_created_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeJobType_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_emp_job_type_created_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 25. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_approved_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_emp_job_type_approved_by

### 問題：
外部キー `fk_emp_job_type_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_EmployeeJobTypeテーブルから外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_approved_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType 
ADD CONSTRAINT fk_emp_job_type_approved_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_EmployeeJobType_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_emp_job_type_approved_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 26. MST_SkillCategory

**説明:** 外部キーfk_skillcategory_parentの参照先カラムをparent_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skillcategory_parent

### 問題：
外部キー `fk_skillcategory_parent` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_SkillCategoryテーブルから外部キー制約を削除
ALTER TABLE MST_SkillCategory DROP FOREIGN KEY fk_skillcategory_parent;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_SkillCategory 
ADD CONSTRAINT fk_skillcategory_parent
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_SkillCategory_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skillcategory_parent
    column: 参照元カラム名
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillCategoryへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 27. MST_Skill

**説明:** 外部キーfk_MST_Skill_categoryの参照先カラムをparent_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_Skill_category

### 問題：
外部キー `fk_MST_Skill_category` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Skillテーブルから外部キー制約を削除
ALTER TABLE MST_Skill DROP FOREIGN KEY fk_MST_Skill_category;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Skill 
ADD CONSTRAINT fk_MST_Skill_category
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Skill_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_Skill_category
    column: 参照元カラム名
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillCategoryへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 28. MST_SkillHierarchy

**説明:** 外部キーfk_hierarchy_skillの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_hierarchy_skill

### 問題：
外部キー `fk_hierarchy_skill` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_SkillHierarchyテーブルから外部キー制約を削除
ALTER TABLE MST_SkillHierarchy DROP FOREIGN KEY fk_hierarchy_skill;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_SkillHierarchy 
ADD CONSTRAINT fk_hierarchy_skill
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_SkillHierarchy_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_hierarchy_skill
    column: 参照元カラム名
    reference_table: MST_SkillItem
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillItemへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 29. MST_SkillGradeRequirement

**説明:** 外部キーfk_MST_SkillGradeRequirement_skill_gradeの参照先カラムをgrade_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_SkillGradeRequirement_skill_grade

### 問題：
外部キー `fk_MST_SkillGradeRequirement_skill_grade` の参照先カラム `MST_SkillGrade.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `grade_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_SkillGradeRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_SkillGradeRequirement DROP FOREIGN KEY fk_MST_SkillGradeRequirement_skill_grade;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_SkillGradeRequirement 
ADD CONSTRAINT fk_MST_SkillGradeRequirement_skill_grade
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillGrade(grade_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_SkillGradeRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_SkillGradeRequirement_skill_grade
    column: 参照元カラム名
    reference_table: MST_SkillGrade
    reference_column: grade_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillGradeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 30. MST_JobTypeSkill

**説明:** 外部キーfk_MST_JobTypeSkill_job_typeの参照先カラムをjob_type_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_JobTypeSkill_job_type

### 問題：
外部キー `fk_MST_JobTypeSkill_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_JobTypeSkillテーブルから外部キー制約を削除
ALTER TABLE MST_JobTypeSkill DROP FOREIGN KEY fk_MST_JobTypeSkill_job_type;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkill 
ADD CONSTRAINT fk_MST_JobTypeSkill_job_type
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_JobTypeSkill_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkill_job_type
    column: 参照元カラム名
    reference_table: MST_JobType
    reference_column: job_type_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_JobTypeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 31. MST_JobTypeSkill

**説明:** 外部キーfk_MST_JobTypeSkill_skill_itemの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_JobTypeSkill_skill_item

### 問題：
外部キー `fk_MST_JobTypeSkill_skill_item` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_JobTypeSkillテーブルから外部キー制約を削除
ALTER TABLE MST_JobTypeSkill DROP FOREIGN KEY fk_MST_JobTypeSkill_skill_item;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkill 
ADD CONSTRAINT fk_MST_JobTypeSkill_skill_item
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_JobTypeSkill_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkill_skill_item
    column: 参照元カラム名
    reference_table: MST_SkillItem
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillItemへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 32. MST_JobTypeSkillGrade

**説明:** 外部キーfk_MST_JobTypeSkillGrade_job_typeの参照先カラムをjob_type_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_JobTypeSkillGrade_job_type

### 問題：
外部キー `fk_MST_JobTypeSkillGrade_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_JobTypeSkillGradeテーブルから外部キー制約を削除
ALTER TABLE MST_JobTypeSkillGrade DROP FOREIGN KEY fk_MST_JobTypeSkillGrade_job_type;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkillGrade 
ADD CONSTRAINT fk_MST_JobTypeSkillGrade_job_type
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_JobTypeSkillGrade_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkillGrade_job_type
    column: 参照元カラム名
    reference_table: MST_JobType
    reference_column: job_type_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_JobTypeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 33. MST_JobTypeSkillGrade

**説明:** 外部キーfk_MST_JobTypeSkillGrade_skill_gradeの参照先カラムをgrade_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_MST_JobTypeSkillGrade_skill_grade

### 問題：
外部キー `fk_MST_JobTypeSkillGrade_skill_grade` の参照先カラム `MST_SkillGrade.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `grade_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_JobTypeSkillGradeテーブルから外部キー制約を削除
ALTER TABLE MST_JobTypeSkillGrade DROP FOREIGN KEY fk_MST_JobTypeSkillGrade_skill_grade;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkillGrade 
ADD CONSTRAINT fk_MST_JobTypeSkillGrade_skill_grade
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillGrade(grade_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_JobTypeSkillGrade_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkillGrade_skill_grade
    column: 参照元カラム名
    reference_table: MST_SkillGrade
    reference_column: grade_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillGradeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 34. MST_Certification

**説明:** 外部キーfk_certification_skill_categoryの参照先カラムをparent_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_certification_skill_category

### 問題：
外部キー `fk_certification_skill_category` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_Certificationテーブルから外部キー制約を削除
ALTER TABLE MST_Certification DROP FOREIGN KEY fk_certification_skill_category;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Certification 
ADD CONSTRAINT fk_certification_skill_category
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_Certification_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_certification_skill_category
    column: 参照元カラム名
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillCategoryへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 35. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_job_typeの参照先カラムをjob_type_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_cert_req_target_job_type

### 問題：
外部キー `fk_cert_req_target_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CertificationRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_job_type;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement 
ADD CONSTRAINT fk_cert_req_target_job_type
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_target_job_type
    column: 参照元カラム名
    reference_table: MST_JobType
    reference_column: job_type_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_JobTypeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 36. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_positionの参照先カラムをposition_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_cert_req_target_position

### 問題：
外部キー `fk_cert_req_target_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CertificationRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_position;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement 
ADD CONSTRAINT fk_cert_req_target_position
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_target_position
    column: 参照元カラム名
    reference_table: MST_Position
    reference_column: position_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Positionへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 37. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_skill_gradeの参照先カラムをgrade_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_cert_req_target_skill_grade

### 問題：
外部キー `fk_cert_req_target_skill_grade` の参照先カラム `MST_SkillGrade.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `grade_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CertificationRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_skill_grade;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement 
ADD CONSTRAINT fk_cert_req_target_skill_grade
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillGrade(grade_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_target_skill_grade
    column: 参照元カラム名
    reference_table: MST_SkillGrade
    reference_column: grade_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillGradeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 38. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_departmentの参照先カラムをparent_department_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_cert_req_target_department

### 問題：
外部キー `fk_cert_req_target_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CertificationRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_department;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement 
ADD CONSTRAINT fk_cert_req_target_department
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_target_department
    column: 参照元カラム名
    reference_table: MST_Department
    reference_column: parent_department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Departmentへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 39. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_certificationの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_cert_req_certification

### 問題：
外部キー `fk_cert_req_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CertificationRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_certification;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement 
ADD CONSTRAINT fk_cert_req_certification
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_certification
    column: 参照元カラム名
    reference_table: MST_Certification
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Certificationへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 40. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_created_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_cert_req_created_by

### 問題：
外部キー `fk_cert_req_created_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CertificationRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_created_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement 
ADD CONSTRAINT fk_cert_req_created_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_created_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 41. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_approved_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_cert_req_approved_by

### 問題：
外部キー `fk_cert_req_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CertificationRequirementテーブルから外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_approved_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement 
ADD CONSTRAINT fk_cert_req_approved_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_approved_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 42. MST_TrainingProgram

**説明:** 外部キーfk_training_program_created_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_training_program_created_by

### 問題：
外部キー `fk_training_program_created_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_TrainingProgramテーブルから外部キー制約を削除
ALTER TABLE MST_TrainingProgram DROP FOREIGN KEY fk_training_program_created_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_TrainingProgram 
ADD CONSTRAINT fk_training_program_created_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_TrainingProgram_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_training_program_created_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 43. MST_TrainingProgram

**説明:** 外部キーfk_training_program_approved_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_training_program_approved_by

### 問題：
外部キー `fk_training_program_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_TrainingProgramテーブルから外部キー制約を削除
ALTER TABLE MST_TrainingProgram DROP FOREIGN KEY fk_training_program_approved_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_TrainingProgram 
ADD CONSTRAINT fk_training_program_approved_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_TrainingProgram_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_training_program_approved_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 44. MST_CareerPlan

**説明:** 外部キーfk_career_plan_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_career_plan_employee

### 問題：
外部キー `fk_career_plan_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CareerPlanテーブルから外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan 
ADD CONSTRAINT fk_career_plan_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CareerPlan_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_career_plan_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 45. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_positionの参照先カラムをposition_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_career_plan_target_position

### 問題：
外部キー `fk_career_plan_target_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CareerPlanテーブルから外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_position;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan 
ADD CONSTRAINT fk_career_plan_target_position
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CareerPlan_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_career_plan_target_position
    column: 参照元カラム名
    reference_table: MST_Position
    reference_column: position_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Positionへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 46. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_job_typeの参照先カラムをjob_type_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_career_plan_target_job_type

### 問題：
外部キー `fk_career_plan_target_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CareerPlanテーブルから外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_job_type;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan 
ADD CONSTRAINT fk_career_plan_target_job_type
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CareerPlan_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_career_plan_target_job_type
    column: 参照元カラム名
    reference_table: MST_JobType
    reference_column: job_type_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_JobTypeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 47. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_departmentの参照先カラムをparent_department_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_career_plan_target_department

### 問題：
外部キー `fk_career_plan_target_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CareerPlanテーブルから外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_department;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan 
ADD CONSTRAINT fk_career_plan_target_department
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CareerPlan_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_career_plan_target_department
    column: 参照元カラム名
    reference_table: MST_Department
    reference_column: parent_department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Departmentへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 48. MST_CareerPlan

**説明:** 外部キーfk_career_plan_mentorの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_career_plan_mentor

### 問題：
外部キー `fk_career_plan_mentor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CareerPlanテーブルから外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_mentor;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan 
ADD CONSTRAINT fk_career_plan_mentor
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CareerPlan_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_career_plan_mentor
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 49. MST_CareerPlan

**説明:** 外部キーfk_career_plan_supervisorの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_career_plan_supervisor

### 問題：
外部キー `fk_career_plan_supervisor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- MST_CareerPlanテーブルから外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_supervisor;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan 
ADD CONSTRAINT fk_career_plan_supervisor
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### MST_CareerPlan_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_career_plan_supervisor
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 50. TRN_SkillRecord

**説明:** 外部キーfk_skill_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_employee

### 問題：
外部キー `fk_skill_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillRecordテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord 
ADD CONSTRAINT fk_skill_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillRecord_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 51. TRN_SkillRecord

**説明:** 外部キーfk_skill_itemの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_item

### 問題：
外部キー `fk_skill_item` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillRecordテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_item;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord 
ADD CONSTRAINT fk_skill_item
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillRecord_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_item
    column: 参照元カラム名
    reference_table: MST_SkillItem
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillItemへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 52. TRN_SkillRecord

**説明:** 外部キーfk_skill_certificationの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_certification

### 問題：
外部キー `fk_skill_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillRecordテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_certification;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord 
ADD CONSTRAINT fk_skill_certification
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillRecord_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_certification
    column: 参照元カラム名
    reference_table: MST_Certification
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Certificationへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 53. TRN_SkillRecord

**説明:** 外部キーfk_skill_categoryの参照先カラムをparent_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_category

### 問題：
外部キー `fk_skill_category` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillRecordテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_category;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord 
ADD CONSTRAINT fk_skill_category
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillRecord_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_category
    column: 参照元カラム名
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillCategoryへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 54. TRN_SkillRecord

**説明:** 外部キーfk_skill_assessorの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_assessor

### 問題：
外部キー `fk_skill_assessor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillRecordテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_assessor;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord 
ADD CONSTRAINT fk_skill_assessor
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillRecord_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_assessor
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 55. TRN_EmployeeSkillGrade

**説明:** 外部キーfk_skill_grade_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_grade_employee

### 問題：
外部キー `fk_skill_grade_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_EmployeeSkillGradeテーブルから外部キー制約を削除
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_EmployeeSkillGrade 
ADD CONSTRAINT fk_skill_grade_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_EmployeeSkillGrade_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_grade_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 56. TRN_EmployeeSkillGrade

**説明:** 外部キーfk_skill_grade_job_typeの参照先カラムをjob_type_codeに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_grade_job_type

### 問題：
外部キー `fk_skill_grade_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_EmployeeSkillGradeテーブルから外部キー制約を削除
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_job_type;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_EmployeeSkillGrade 
ADD CONSTRAINT fk_skill_grade_job_type
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_EmployeeSkillGrade_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_grade_job_type
    column: 参照元カラム名
    reference_table: MST_JobType
    reference_column: job_type_code
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_JobTypeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 57. TRN_EmployeeSkillGrade

**説明:** 外部キーfk_skill_grade_evaluatorの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_skill_grade_evaluator

### 問題：
外部キー `fk_skill_grade_evaluator` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_EmployeeSkillGradeテーブルから外部キー制約を削除
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_evaluator;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_EmployeeSkillGrade 
ADD CONSTRAINT fk_skill_grade_evaluator
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_EmployeeSkillGrade_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_grade_evaluator
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 58. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_TRN_GoalProgress_employee

### 問題：
外部キー `fk_TRN_GoalProgress_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_GoalProgressテーブルから外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress 
ADD CONSTRAINT fk_TRN_GoalProgress_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_GoalProgress_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 59. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_supervisorの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_TRN_GoalProgress_supervisor

### 問題：
外部キー `fk_TRN_GoalProgress_supervisor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_GoalProgressテーブルから外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_supervisor;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress 
ADD CONSTRAINT fk_TRN_GoalProgress_supervisor
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_GoalProgress_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_supervisor
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 60. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_approved_byの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_TRN_GoalProgress_approved_by

### 問題：
外部キー `fk_TRN_GoalProgress_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_GoalProgressテーブルから外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_approved_by;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress 
ADD CONSTRAINT fk_TRN_GoalProgress_approved_by
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_GoalProgress_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_approved_by
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 61. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_career_planの参照先カラムをcareer_plan_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_TRN_GoalProgress_career_plan

### 問題：
外部キー `fk_TRN_GoalProgress_career_plan` の参照先カラム `MST_CareerPlan.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `career_plan_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_GoalProgressテーブルから外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_career_plan;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress 
ADD CONSTRAINT fk_TRN_GoalProgress_career_plan
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_CareerPlan(career_plan_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_GoalProgress_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_career_plan
    column: 参照元カラム名
    reference_table: MST_CareerPlan
    reference_column: career_plan_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_CareerPlanへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 62. TRN_ProjectRecord

**説明:** 外部キーfk_project_record_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_project_record_employee

### 問題：
外部キー `fk_project_record_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_ProjectRecordテーブルから外部キー制約を削除
ALTER TABLE TRN_ProjectRecord DROP FOREIGN KEY fk_project_record_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_ProjectRecord 
ADD CONSTRAINT fk_project_record_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_ProjectRecord_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_project_record_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 63. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_training_history_employee

### 問題：
外部キー `fk_training_history_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_TrainingHistoryテーブルから外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_TrainingHistory 
ADD CONSTRAINT fk_training_history_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_TrainingHistory_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_training_history_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 64. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_programの参照先カラムをtraining_program_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_training_history_program

### 問題：
外部キー `fk_training_history_program` の参照先カラム `MST_TrainingProgram.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `training_program_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_TrainingHistoryテーブルから外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_program;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_TrainingHistory 
ADD CONSTRAINT fk_training_history_program
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_TrainingProgram(training_program_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_TrainingHistory_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_training_history_program
    column: 参照元カラム名
    reference_table: MST_TrainingProgram
    reference_column: training_program_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_TrainingProgramへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 65. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_approverの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_training_history_approver

### 問題：
外部キー `fk_training_history_approver` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_TrainingHistoryテーブルから外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_approver;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_TrainingHistory 
ADD CONSTRAINT fk_training_history_approver
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_TrainingHistory_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_training_history_approver
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 66. TRN_PDU

**説明:** 外部キーfk_pdu_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_pdu_employee

### 問題：
外部キー `fk_pdu_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_PDUテーブルから外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_PDU 
ADD CONSTRAINT fk_pdu_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_PDU_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_pdu_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 67. TRN_PDU

**説明:** 外部キーfk_pdu_certificationの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_pdu_certification

### 問題：
外部キー `fk_pdu_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_PDUテーブルから外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_certification;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_PDU 
ADD CONSTRAINT fk_pdu_certification
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_PDU_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_pdu_certification
    column: 参照元カラム名
    reference_table: MST_Certification
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Certificationへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 68. TRN_PDU

**説明:** 外部キーfk_pdu_approverの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_pdu_approver

### 問題：
外部キー `fk_pdu_approver` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_PDUテーブルから外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_approver;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_PDU 
ADD CONSTRAINT fk_pdu_approver
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_PDU_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_pdu_approver
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 69. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_evidence_employee

### 問題：
外部キー `fk_evidence_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillEvidenceテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence 
ADD CONSTRAINT fk_evidence_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillEvidence_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_evidence_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 70. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_skillの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_evidence_skill

### 問題：
外部キー `fk_evidence_skill` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillEvidenceテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_skill;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence 
ADD CONSTRAINT fk_evidence_skill
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillEvidence_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_evidence_skill
    column: 参照元カラム名
    reference_table: MST_SkillItem
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillItemへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 71. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_verifierの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_evidence_verifier

### 問題：
外部キー `fk_evidence_verifier` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillEvidenceテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_verifier;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence 
ADD CONSTRAINT fk_evidence_verifier
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillEvidence_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_evidence_verifier
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 72. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_certificationの参照先カラムをskill_category_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_evidence_certification

### 問題：
外部キー `fk_evidence_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_SkillEvidenceテーブルから外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_certification;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence 
ADD CONSTRAINT fk_evidence_certification
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_SkillEvidence_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_evidence_certification
    column: 参照元カラム名
    reference_table: MST_Certification
    reference_column: skill_category_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Certificationへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 73. TRN_Notification

**説明:** 外部キーfk_notification_recipientの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_notification_recipient

### 問題：
外部キー `fk_notification_recipient` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_Notificationテーブルから外部キー制約を削除
ALTER TABLE TRN_Notification DROP FOREIGN KEY fk_notification_recipient;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_Notification 
ADD CONSTRAINT fk_notification_recipient
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_Notification_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_notification_recipient
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 74. TRN_Notification

**説明:** 外部キーfk_notification_senderの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_notification_sender

### 問題：
外部キー `fk_notification_sender` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- TRN_Notificationテーブルから外部キー制約を削除
ALTER TABLE TRN_Notification DROP FOREIGN KEY fk_notification_sender;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_Notification 
ADD CONSTRAINT fk_notification_sender
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### TRN_Notification_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_notification_sender
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 75. SYS_SkillMatrix

**説明:** 外部キーfk_SYS_SkillMatrix_employeeの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_SYS_SkillMatrix_employee

### 問題：
外部キー `fk_SYS_SkillMatrix_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- SYS_SkillMatrixテーブルから外部キー制約を削除
ALTER TABLE SYS_SkillMatrix DROP FOREIGN KEY fk_SYS_SkillMatrix_employee;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE SYS_SkillMatrix 
ADD CONSTRAINT fk_SYS_SkillMatrix_employee
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### SYS_SkillMatrix_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_SYS_SkillMatrix_employee
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 76. SYS_TokenStore

**説明:** 外部キーfk_token_store_userの参照先カラムをuser_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_token_store_user

### 問題：
外部キー `fk_token_store_user` の参照先カラム `MST_UserAuth.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `user_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- SYS_TokenStoreテーブルから外部キー制約を削除
ALTER TABLE SYS_TokenStore DROP FOREIGN KEY fk_token_store_user;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE SYS_TokenStore 
ADD CONSTRAINT fk_token_store_user
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_UserAuth(user_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### SYS_TokenStore_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_token_store_user
    column: 参照元カラム名
    reference_table: MST_UserAuth
    reference_column: user_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_UserAuthへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 77. SYS_TenantUsage

**説明:** 外部キーfk_SYS_TenantUsage_tenantの参照先カラムをtenant_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_SYS_TenantUsage_tenant

### 問題：
外部キー `fk_SYS_TenantUsage_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- SYS_TenantUsageテーブルから外部キー制約を削除
ALTER TABLE SYS_TenantUsage DROP FOREIGN KEY fk_SYS_TenantUsage_tenant;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE SYS_TenantUsage 
ADD CONSTRAINT fk_SYS_TenantUsage_tenant
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### SYS_TenantUsage_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_SYS_TenantUsage_tenant
    column: 参照元カラム名
    reference_table: MST_Tenant
    reference_column: tenant_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 78. HIS_AuditLog

**説明:** 外部キーfk_his_auditlog_tenantの参照先カラムをtenant_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_his_auditlog_tenant

### 問題：
外部キー `fk_his_auditlog_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- HIS_AuditLogテーブルから外部キー制約を削除
ALTER TABLE HIS_AuditLog DROP FOREIGN KEY fk_his_auditlog_tenant;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE HIS_AuditLog 
ADD CONSTRAINT fk_his_auditlog_tenant
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### HIS_AuditLog_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_his_auditlog_tenant
    column: 参照元カラム名
    reference_table: MST_Tenant
    reference_column: tenant_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 79. HIS_AuditLog

**説明:** 外部キーfk_his_auditlog_userの参照先カラムをdepartment_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_his_auditlog_user

### 問題：
外部キー `fk_his_auditlog_user` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- HIS_AuditLogテーブルから外部キー制約を削除
ALTER TABLE HIS_AuditLog DROP FOREIGN KEY fk_his_auditlog_user;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE HIS_AuditLog 
ADD CONSTRAINT fk_his_auditlog_user
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### HIS_AuditLog_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_his_auditlog_user
    column: 参照元カラム名
    reference_table: MST_Employee
    reference_column: department_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Employeeへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 80. HIS_TenantBilling

**説明:** 外部キーfk_tenant_billing_tenantの参照先カラムをtenant_idに修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正: fk_tenant_billing_tenant

### 問題：
外部キー `fk_tenant_billing_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更

### DDL修正手順：

#### 1. 既存外部キー制約の削除
```sql
-- HIS_TenantBillingテーブルから外部キー制約を削除
ALTER TABLE HIS_TenantBilling DROP FOREIGN KEY fk_tenant_billing_tenant;
```

#### 2. 正しい外部キー制約の追加
```sql
-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE HIS_TenantBilling 
ADD CONSTRAINT fk_tenant_billing_tenant
    FOREIGN KEY (参照元カラム名) 
    REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### HIS_TenantBilling_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_tenant_billing_tenant
    column: 参照元カラム名
    reference_table: MST_Tenant
    reference_column: tenant_id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 参照元カラム名は実際のカラム名に置き換えてください
- データ型の互換性を確認してください
- 既存データの整合性を事前に確認してください

```

#### 81. HIS_AuditLog

**説明:** 外部キーfk_his_auditlog_tenantの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_his_auditlog_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE HIS_AuditLog DROP FOREIGN KEY fk_his_auditlog_tenant;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_tenant
    FOREIGN KEY (...) REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_his_auditlog_tenant
    # ... 他の設定 ...
    reference_table: MST_Tenant
    reference_column: tenant_id
```

```

#### 82. HIS_AuditLog

**説明:** 外部キーfk_his_auditlog_userの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_his_auditlog_user` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE HIS_AuditLog DROP FOREIGN KEY fk_his_auditlog_user;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE HIS_AuditLog ADD CONSTRAINT fk_his_auditlog_user
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_his_auditlog_user
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 83. HIS_TenantBilling

**説明:** 外部キーfk_tenant_billing_tenantの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_tenant_billing_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE HIS_TenantBilling DROP FOREIGN KEY fk_tenant_billing_tenant;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE HIS_TenantBilling ADD CONSTRAINT fk_tenant_billing_tenant
    FOREIGN KEY (...) REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_tenant_billing_tenant
    # ... 他の設定 ...
    reference_table: MST_Tenant
    reference_column: tenant_id
```

```

#### 84. MST_CareerPlan

**説明:** 外部キーfk_career_plan_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_career_plan_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 85. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_positionの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_career_plan_target_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_position;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position
    FOREIGN KEY (...) REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_target_position
    # ... 他の設定 ...
    reference_table: MST_Position
    reference_column: position_code
```

```

#### 86. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_job_typeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_career_plan_target_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_job_type;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type
    FOREIGN KEY (...) REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_target_job_type
    # ... 他の設定 ...
    reference_table: MST_JobType
    reference_column: job_type_code
```

```

#### 87. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_departmentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_career_plan_target_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_department;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department
    FOREIGN KEY (...) REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_target_department
    # ... 他の設定 ...
    reference_table: MST_Department
    reference_column: parent_department_id
```

```

#### 88. MST_CareerPlan

**説明:** 外部キーfk_career_plan_mentorの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_career_plan_mentor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_mentor;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_mentor
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 89. MST_CareerPlan

**説明:** 外部キーfk_career_plan_supervisorの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_career_plan_supervisor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_supervisor;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_supervisor
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 90. MST_Certification

**説明:** 外部キーfk_certification_skill_categoryの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_certification_skill_category` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Certification DROP FOREIGN KEY fk_certification_skill_category;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category
    FOREIGN KEY (...) REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_certification_skill_category
    # ... 他の設定 ...
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
```

```

#### 91. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_job_typeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_cert_req_target_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_job_type;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type
    FOREIGN KEY (...) REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_job_type
    # ... 他の設定 ...
    reference_table: MST_JobType
    reference_column: job_type_code
```

```

#### 92. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_positionの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_cert_req_target_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_position;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position
    FOREIGN KEY (...) REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_position
    # ... 他の設定 ...
    reference_table: MST_Position
    reference_column: position_code
```

```

#### 93. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_skill_gradeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_cert_req_target_skill_grade` の参照先カラム `MST_SkillGrade.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `grade_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_skill_grade;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade
    FOREIGN KEY (...) REFERENCES MST_SkillGrade(grade_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_skill_grade
    # ... 他の設定 ...
    reference_table: MST_SkillGrade
    reference_column: grade_code
```

```

#### 94. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_departmentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_cert_req_target_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_department;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department
    FOREIGN KEY (...) REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_department
    # ... 他の設定 ...
    reference_table: MST_Department
    reference_column: parent_department_id
```

```

#### 95. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_certificationの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_cert_req_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_certification;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_certification
    FOREIGN KEY (...) REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_certification
    # ... 他の設定 ...
    reference_table: MST_Certification
    reference_column: skill_category_id
```

```

#### 96. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_created_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_cert_req_created_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_created_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_created_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_created_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 97. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_approved_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_cert_req_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_approved_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_approved_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 98. MST_Department

**説明:** 外部キーfk_department_parentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_department_parent` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_parent;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent
    FOREIGN KEY (...) REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_department_parent
    # ... 他の設定 ...
    reference_table: MST_Department
    reference_column: parent_department_id
```

```

#### 99. MST_Department

**説明:** 外部キーfk_department_managerの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_department_manager` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_manager;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_department_manager
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 100. MST_Department

**説明:** 外部キーfk_department_deputyの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_department_deputy` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_deputy;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_department_deputy
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 101. MST_Employee

**説明:** 外部キーfk_employee_departmentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_employee_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_department;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_department
    FOREIGN KEY (...) REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_employee_department
    # ... 他の設定 ...
    reference_table: MST_Department
    reference_column: parent_department_id
```

```

#### 102. MST_Employee

**説明:** 外部キーfk_employee_positionの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_employee_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_position;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position
    FOREIGN KEY (...) REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_employee_position
    # ... 他の設定 ...
    reference_table: MST_Position
    reference_column: position_code
```

```

#### 103. MST_Employee

**説明:** 外部キーfk_employee_job_typeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_employee_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_job_type;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type
    FOREIGN KEY (...) REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_employee_job_type
    # ... 他の設定 ...
    reference_table: MST_JobType
    reference_column: job_type_code
```

```

#### 104. MST_Employee

**説明:** 外部キーfk_employee_managerの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_employee_manager` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_manager;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_employee_manager
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 105. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_EmployeeDepartment_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 106. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_departmentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_EmployeeDepartment_department` の参照先カラム `MST_Department.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_department;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_department
    FOREIGN KEY (...) REFERENCES MST_Department(parent_department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_department
    # ... 他の設定 ...
    reference_table: MST_Department
    reference_column: parent_department_id
```

```

#### 107. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_reporting_managerの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_EmployeeDepartment_reporting_manager` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_reporting_manager;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_reporting_manager
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 108. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_approved_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_EmployeeDepartment_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_approved_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_approved_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 109. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_emp_job_type_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 110. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_job_typeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_emp_job_type_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_job_type;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_job_type
    FOREIGN KEY (...) REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_job_type
    # ... 他の設定 ...
    reference_table: MST_JobType
    reference_column: job_type_code
```

```

#### 111. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_mentorの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_emp_job_type_mentor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_mentor;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_mentor
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 112. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_supervisorの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_emp_job_type_supervisor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_supervisor;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_supervisor
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 113. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_created_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_emp_job_type_created_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_created_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_created_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_created_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 114. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_approved_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_emp_job_type_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_approved_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_approved_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 115. MST_EmployeePosition

**説明:** 外部キーfk_MST_EmployeePosition_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_EmployeePosition_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 116. MST_EmployeePosition

**説明:** 外部キーfk_MST_EmployeePosition_positionの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_EmployeePosition_position` の参照先カラム `MST_Position.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `position_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_position;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_position
    FOREIGN KEY (...) REFERENCES MST_Position(position_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_position
    # ... 他の設定 ...
    reference_table: MST_Position
    reference_column: position_code
```

```

#### 117. MST_EmployeePosition

**説明:** 外部キーfk_MST_EmployeePosition_approved_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_EmployeePosition_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_approved_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_approved_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_approved_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 118. MST_JobTypeSkill

**説明:** 外部キーfk_MST_JobTypeSkill_job_typeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_JobTypeSkill_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_JobTypeSkill DROP FOREIGN KEY fk_MST_JobTypeSkill_job_type;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_job_type
    FOREIGN KEY (...) REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkill_job_type
    # ... 他の設定 ...
    reference_table: MST_JobType
    reference_column: job_type_code
```

```

#### 119. MST_JobTypeSkill

**説明:** 外部キーfk_MST_JobTypeSkill_skill_itemの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_JobTypeSkill_skill_item` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_JobTypeSkill DROP FOREIGN KEY fk_MST_JobTypeSkill_skill_item;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkill ADD CONSTRAINT fk_MST_JobTypeSkill_skill_item
    FOREIGN KEY (...) REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkill_skill_item
    # ... 他の設定 ...
    reference_table: MST_SkillItem
    reference_column: skill_category_id
```

```

#### 120. MST_JobTypeSkillGrade

**説明:** 外部キーfk_MST_JobTypeSkillGrade_job_typeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_JobTypeSkillGrade_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_JobTypeSkillGrade DROP FOREIGN KEY fk_MST_JobTypeSkillGrade_job_type;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_job_type
    FOREIGN KEY (...) REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkillGrade_job_type
    # ... 他の設定 ...
    reference_table: MST_JobType
    reference_column: job_type_code
```

```

#### 121. MST_JobTypeSkillGrade

**説明:** 外部キーfk_MST_JobTypeSkillGrade_skill_gradeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_JobTypeSkillGrade_skill_grade` の参照先カラム `MST_SkillGrade.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `grade_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_JobTypeSkillGrade DROP FOREIGN KEY fk_MST_JobTypeSkillGrade_skill_grade;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_JobTypeSkillGrade ADD CONSTRAINT fk_MST_JobTypeSkillGrade_skill_grade
    FOREIGN KEY (...) REFERENCES MST_SkillGrade(grade_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_JobTypeSkillGrade_skill_grade
    # ... 他の設定 ...
    reference_table: MST_SkillGrade
    reference_column: grade_code
```

```

#### 122. MST_Permission

**説明:** 外部キーfk_permission_parentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_permission_parent` の参照先カラム `MST_Permission.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_permission_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Permission DROP FOREIGN KEY fk_permission_parent;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Permission ADD CONSTRAINT fk_permission_parent
    FOREIGN KEY (...) REFERENCES MST_Permission(parent_permission_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_permission_parent
    # ... 他の設定 ...
    reference_table: MST_Permission
    reference_column: parent_permission_id
```

```

#### 123. MST_Role

**説明:** 外部キーfk_role_parentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_role_parent` の参照先カラム `MST_Role.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_role_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Role DROP FOREIGN KEY fk_role_parent;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Role ADD CONSTRAINT fk_role_parent
    FOREIGN KEY (...) REFERENCES MST_Role(parent_role_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_role_parent
    # ... 他の設定 ...
    reference_table: MST_Role
    reference_column: parent_role_id
```

```

#### 124. MST_Skill

**説明:** 外部キーfk_MST_Skill_categoryの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_Skill_category` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Skill DROP FOREIGN KEY fk_MST_Skill_category;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_Skill ADD CONSTRAINT fk_MST_Skill_category
    FOREIGN KEY (...) REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_Skill_category
    # ... 他の設定 ...
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
```

```

#### 125. MST_SkillCategory

**説明:** 外部キーfk_skillcategory_parentの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skillcategory_parent` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_SkillCategory DROP FOREIGN KEY fk_skillcategory_parent;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent
    FOREIGN KEY (...) REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skillcategory_parent
    # ... 他の設定 ...
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
```

```

#### 126. MST_SkillGradeRequirement

**説明:** 外部キーfk_MST_SkillGradeRequirement_skill_gradeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_MST_SkillGradeRequirement_skill_grade` の参照先カラム `MST_SkillGrade.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `grade_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_SkillGradeRequirement DROP FOREIGN KEY fk_MST_SkillGradeRequirement_skill_grade;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_SkillGradeRequirement ADD CONSTRAINT fk_MST_SkillGradeRequirement_skill_grade
    FOREIGN KEY (...) REFERENCES MST_SkillGrade(grade_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_SkillGradeRequirement_skill_grade
    # ... 他の設定 ...
    reference_table: MST_SkillGrade
    reference_column: grade_code
```

```

#### 127. MST_SkillHierarchy

**説明:** 外部キーfk_hierarchy_skillの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_hierarchy_skill` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_SkillHierarchy DROP FOREIGN KEY fk_hierarchy_skill;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_SkillHierarchy ADD CONSTRAINT fk_hierarchy_skill
    FOREIGN KEY (...) REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_hierarchy_skill
    # ... 他の設定 ...
    reference_table: MST_SkillItem
    reference_column: skill_category_id
```

```

#### 128. MST_TenantSettings

**説明:** 外部キーfk_tenant_settings_tenantの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_tenant_settings_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_TenantSettings DROP FOREIGN KEY fk_tenant_settings_tenant;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_TenantSettings ADD CONSTRAINT fk_tenant_settings_tenant
    FOREIGN KEY (...) REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_tenant_settings_tenant
    # ... 他の設定 ...
    reference_table: MST_Tenant
    reference_column: tenant_id
```

```

#### 129. MST_TrainingProgram

**説明:** 外部キーfk_training_program_created_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_training_program_created_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_TrainingProgram DROP FOREIGN KEY fk_training_program_created_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_created_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_program_created_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 130. MST_TrainingProgram

**説明:** 外部キーfk_training_program_approved_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_training_program_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_TrainingProgram DROP FOREIGN KEY fk_training_program_approved_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_program_approved_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 131. MST_UserAuth

**説明:** 外部キーfk_userauth_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_userauth_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_UserAuth DROP FOREIGN KEY fk_userauth_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_userauth_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 132. MST_UserRole

**説明:** 外部キーfk_userrole_roleの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_userrole_role` の参照先カラム `MST_Role.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_role_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_role;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_role
    FOREIGN KEY (...) REFERENCES MST_Role(parent_role_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_userrole_role
    # ... 他の設定 ...
    reference_table: MST_Role
    reference_column: parent_role_id
```

```

#### 133. SYS_SkillMatrix

**説明:** 外部キーfk_SYS_SkillMatrix_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_SYS_SkillMatrix_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE SYS_SkillMatrix DROP FOREIGN KEY fk_SYS_SkillMatrix_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE SYS_SkillMatrix ADD CONSTRAINT fk_SYS_SkillMatrix_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_SYS_SkillMatrix_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 134. SYS_TenantUsage

**説明:** 外部キーfk_SYS_TenantUsage_tenantの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_SYS_TenantUsage_tenant` の参照先カラム `MST_Tenant.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `tenant_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE SYS_TenantUsage DROP FOREIGN KEY fk_SYS_TenantUsage_tenant;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE SYS_TenantUsage ADD CONSTRAINT fk_SYS_TenantUsage_tenant
    FOREIGN KEY (...) REFERENCES MST_Tenant(tenant_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_SYS_TenantUsage_tenant
    # ... 他の設定 ...
    reference_table: MST_Tenant
    reference_column: tenant_id
```

```

#### 135. SYS_TokenStore

**説明:** 外部キーfk_token_store_userの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_token_store_user` の参照先カラム `MST_UserAuth.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `user_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE SYS_TokenStore DROP FOREIGN KEY fk_token_store_user;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE SYS_TokenStore ADD CONSTRAINT fk_token_store_user
    FOREIGN KEY (...) REFERENCES MST_UserAuth(user_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_token_store_user
    # ... 他の設定 ...
    reference_table: MST_UserAuth
    reference_column: user_id
```

```

#### 136. TRN_EmployeeSkillGrade

**説明:** 外部キーfk_skill_grade_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_grade_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_grade_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 137. TRN_EmployeeSkillGrade

**説明:** 外部キーfk_skill_grade_job_typeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_grade_job_type` の参照先カラム `MST_JobType.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `job_type_code` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_job_type;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_job_type
    FOREIGN KEY (...) REFERENCES MST_JobType(job_type_code)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_grade_job_type
    # ... 他の設定 ...
    reference_table: MST_JobType
    reference_column: job_type_code
```

```

#### 138. TRN_EmployeeSkillGrade

**説明:** 外部キーfk_skill_grade_evaluatorの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_grade_evaluator` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_evaluator;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_evaluator
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_grade_evaluator
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 139. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_TRN_GoalProgress_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 140. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_supervisorの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_TRN_GoalProgress_supervisor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_supervisor;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_supervisor
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 141. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_approved_byの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_TRN_GoalProgress_approved_by` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_approved_by;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_approved_by
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 142. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_career_planの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_TRN_GoalProgress_career_plan` の参照先カラム `MST_CareerPlan.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `career_plan_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_career_plan;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan
    FOREIGN KEY (...) REFERENCES MST_CareerPlan(career_plan_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_career_plan
    # ... 他の設定 ...
    reference_table: MST_CareerPlan
    reference_column: career_plan_id
```

```

#### 143. TRN_Notification

**説明:** 外部キーfk_notification_recipientの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_notification_recipient` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_Notification DROP FOREIGN KEY fk_notification_recipient;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_recipient
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_notification_recipient
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 144. TRN_Notification

**説明:** 外部キーfk_notification_senderの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_notification_sender` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_Notification DROP FOREIGN KEY fk_notification_sender;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_notification_sender
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 145. TRN_PDU

**説明:** 外部キーfk_pdu_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_pdu_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_pdu_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 146. TRN_PDU

**説明:** 外部キーfk_pdu_certificationの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_pdu_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_certification;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification
    FOREIGN KEY (...) REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_pdu_certification
    # ... 他の設定 ...
    reference_table: MST_Certification
    reference_column: skill_category_id
```

```

#### 147. TRN_PDU

**説明:** 外部キーfk_pdu_approverの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_pdu_approver` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_approver;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_pdu_approver
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 148. TRN_ProjectRecord

**説明:** 外部キーfk_project_record_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_project_record_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_ProjectRecord DROP FOREIGN KEY fk_project_record_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_ProjectRecord ADD CONSTRAINT fk_project_record_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_project_record_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 149. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_evidence_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 150. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_skillの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_evidence_skill` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_skill;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_skill
    FOREIGN KEY (...) REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_skill
    # ... 他の設定 ...
    reference_table: MST_SkillItem
    reference_column: skill_category_id
```

```

#### 151. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_verifierの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_evidence_verifier` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_verifier;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_verifier
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 152. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_certificationの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_evidence_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_certification;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification
    FOREIGN KEY (...) REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_certification
    # ... 他の設定 ...
    reference_table: MST_Certification
    reference_column: skill_category_id
```

```

#### 153. TRN_SkillRecord

**説明:** 外部キーfk_skill_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 154. TRN_SkillRecord

**説明:** 外部キーfk_skill_itemの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_item` の参照先カラム `MST_SkillItem.id` が存在しません。

### 利用可能なカラム：
- skill_code
- skill_name
- skill_category_id
- skill_type
- difficulty_level
- importance_level
- code
- name
- description

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_item;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_item
    FOREIGN KEY (...) REFERENCES MST_SkillItem(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_item
    # ... 他の設定 ...
    reference_table: MST_SkillItem
    reference_column: skill_category_id
```

```

#### 155. TRN_SkillRecord

**説明:** 外部キーfk_skill_certificationの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_certification` の参照先カラム `MST_Certification.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `skill_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_certification;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification
    FOREIGN KEY (...) REFERENCES MST_Certification(skill_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_certification
    # ... 他の設定 ...
    reference_table: MST_Certification
    reference_column: skill_category_id
```

```

#### 156. TRN_SkillRecord

**説明:** 外部キーfk_skill_categoryの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_category` の参照先カラム `MST_SkillCategory.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `parent_category_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_category;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category
    FOREIGN KEY (...) REFERENCES MST_SkillCategory(parent_category_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_category
    # ... 他の設定 ...
    reference_table: MST_SkillCategory
    reference_column: parent_category_id
```

```

#### 157. TRN_SkillRecord

**説明:** 外部キーfk_skill_assessorの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_skill_assessor` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_assessor;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_assessor
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 158. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_employeeの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_training_history_employee` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_employee;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_employee
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_history_employee
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 159. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_programの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_training_history_program` の参照先カラム `MST_TrainingProgram.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `training_program_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_program;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program
    FOREIGN KEY (...) REFERENCES MST_TrainingProgram(training_program_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_history_program
    # ... 他の設定 ...
    reference_table: MST_TrainingProgram
    reference_column: training_program_id
```

```

#### 160. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_approverの参照先カラムを修正

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キー参照先カラム修正提案

外部キー `fk_training_history_approver` の参照先カラム `MST_Employee.id` が存在しません。

### 利用可能なカラム：
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

### 推奨修正：
参照先カラムを `department_id` に変更してください。

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_approver;

-- 正しい参照先カラムで外部キー制約を再作成
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver
    FOREIGN KEY (...) REFERENCES MST_Employee(department_id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_history_approver
    # ... 他の設定 ...
    reference_table: MST_Employee
    reference_column: department_id
```

```

#### 161. MST_Tenant

**説明:** MST_Tenantの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_Tenant

### 不一致が検出された外部キー：

#### fk_tenant_parent - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_tenant_parentの修正
ALTER TABLE MST_Tenant DROP FOREIGN KEY fk_tenant_parent;
ALTER TABLE MST_Tenant ADD CONSTRAINT fk_tenant_parent
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_tenant_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 162. MST_UserAuth

**説明:** MST_UserAuthの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_UserAuth

### 不一致が検出された外部キー：

#### fk_userauth_employee - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_userauth_employeeの修正
ALTER TABLE MST_UserAuth DROP FOREIGN KEY fk_userauth_employee;
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_userauth_employee
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 163. MST_Role

**説明:** MST_Roleの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_Role

### 不一致が検出された外部キー：

#### fk_role_parent - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_role_parentの修正
ALTER TABLE MST_Role DROP FOREIGN KEY fk_role_parent;
ALTER TABLE MST_Role ADD CONSTRAINT fk_role_parent
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_role_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 164. MST_Permission

**説明:** MST_Permissionの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_Permission

### 不一致が検出された外部キー：

#### fk_permission_parent - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_permission_parentの修正
ALTER TABLE MST_Permission DROP FOREIGN KEY fk_permission_parent;
ALTER TABLE MST_Permission ADD CONSTRAINT fk_permission_parent
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_permission_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 165. MST_UserRole

**説明:** MST_UserRoleの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_UserRole

### 不一致が検出された外部キー：

#### fk_userrole_delegation_source - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_userrole_assigned_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_userrole_approved_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_userrole_delegation_sourceの修正
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_delegation_source;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_delegation_source
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_userrole_assigned_byの修正
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_assigned_by;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_assigned_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_userrole_approved_byの修正
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_approved_by;
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_approved_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_userrole_delegation_source
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_userrole_assigned_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_userrole_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 166. MST_Employee

**説明:** MST_Employeeの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_Employee

### 不一致が検出された外部キー：

#### fk_employee_manager - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_employee_job_type - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_employee_position - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_employee_managerの修正
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_manager;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_employee_job_typeの修正
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_job_type;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_employee_positionの修正
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_position;
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_employee_manager
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_employee_job_type
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_employee_position
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 167. MST_Department

**説明:** MST_Departmentの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_Department

### 不一致が検出された外部キー：

#### fk_department_manager - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_department_deputy - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_department_parent - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_department_managerの修正
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_manager;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_department_deputyの修正
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_deputy;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_department_parentの修正
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_parent;
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_department_manager
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_department_deputy
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_department_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 168. MST_EmployeeDepartment

**説明:** MST_EmployeeDepartmentの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_EmployeeDepartment

### 不一致が検出された外部キー：

#### fk_MST_EmployeeDepartment_reporting_manager - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_MST_EmployeeDepartment_approved_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_MST_EmployeeDepartment_reporting_managerの修正
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_reporting_manager;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_MST_EmployeeDepartment_approved_byの修正
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_approved_by;
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_reporting_manager
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_MST_EmployeeDepartment_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 169. MST_EmployeePosition

**説明:** MST_EmployeePositionの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_EmployeePosition

### 不一致が検出された外部キー：

#### fk_MST_EmployeePosition_approved_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_MST_EmployeePosition_approved_byの修正
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_approved_by;
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_approved_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 170. MST_EmployeeJobType

**説明:** MST_EmployeeJobTypeの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_EmployeeJobType

### 不一致が検出された外部キー：

#### fk_emp_job_type_approved_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_emp_job_type_supervisor - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_emp_job_type_mentor - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_emp_job_type_approved_byの修正
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_approved_by;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_emp_job_type_supervisorの修正
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_supervisor;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_emp_job_type_mentorの修正
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_mentor;
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_emp_job_type_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_emp_job_type_supervisor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_emp_job_type_mentor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 171. MST_SkillCategory

**説明:** MST_SkillCategoryの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_SkillCategory

### 不一致が検出された外部キー：

#### fk_skillcategory_parent - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_skillcategory_parentの修正
ALTER TABLE MST_SkillCategory DROP FOREIGN KEY fk_skillcategory_parent;
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skillcategory_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 172. MST_Certification

**説明:** MST_Certificationの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_Certification

### 不一致が検出された外部キー：

#### fk_certification_skill_category - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_certification_skill_categoryの修正
ALTER TABLE MST_Certification DROP FOREIGN KEY fk_certification_skill_category;
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_certification_skill_category
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 173. MST_CertificationRequirement

**説明:** MST_CertificationRequirementの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_CertificationRequirement

### 不一致が検出された外部キー：

#### fk_cert_req_approved_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_cert_req_target_skill_grade - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_cert_req_target_department - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_cert_req_target_job_type - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_cert_req_target_position - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_cert_req_approved_byの修正
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_approved_by;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_cert_req_target_skill_gradeの修正
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_skill_grade;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_cert_req_target_departmentの修正
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_department;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_cert_req_target_job_typeの修正
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_job_type;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_cert_req_target_positionの修正
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_position;
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_cert_req_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_cert_req_target_skill_grade
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_cert_req_target_department
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_cert_req_target_job_type
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_cert_req_target_position
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 174. MST_TrainingProgram

**説明:** MST_TrainingProgramの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_TrainingProgram

### 不一致が検出された外部キー：

#### fk_training_program_approved_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_training_program_approved_byの修正
ALTER TABLE MST_TrainingProgram DROP FOREIGN KEY fk_training_program_approved_by;
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_training_program_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 175. MST_CareerPlan

**説明:** MST_CareerPlanの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_CareerPlan

### 不一致が検出された外部キー：

#### fk_career_plan_supervisor - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_career_plan_target_department - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_career_plan_target_job_type - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_career_plan_target_position - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_career_plan_mentor - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_career_plan_supervisorの修正
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_supervisor;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_career_plan_target_departmentの修正
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_department;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_career_plan_target_job_typeの修正
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_job_type;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_career_plan_target_positionの修正
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_position;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_career_plan_mentorの修正
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_mentor;
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_career_plan_supervisor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_career_plan_target_department
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_career_plan_target_job_type
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_career_plan_target_position
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_career_plan_mentor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 176. MST_NotificationSettings

**説明:** MST_NotificationSettingsの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: MST_NotificationSettings

### 不一致が検出された外部キー：

#### fk_notification_settings_template - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_notification_settings_templateの修正
ALTER TABLE MST_NotificationSettings DROP FOREIGN KEY fk_notification_settings_template;
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT fk_notification_settings_template
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_notification_settings_template
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 177. TRN_SkillRecord

**説明:** TRN_SkillRecordの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: TRN_SkillRecord

### 不一致が検出された外部キー：

#### fk_skill_certification - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_skill_assessor - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_skill_category - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_skill_certificationの修正
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_certification;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_skill_assessorの修正
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_assessor;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_skill_categoryの修正
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_category;
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_certification
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_skill_assessor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_skill_category
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 178. TRN_EmployeeSkillGrade

**説明:** TRN_EmployeeSkillGradeの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: TRN_EmployeeSkillGrade

### 不一致が検出された外部キー：

#### fk_skill_grade_evaluator - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_skill_grade_evaluatorの修正
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_evaluator;
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_evaluator
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_skill_grade_evaluator
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 179. TRN_GoalProgress

**説明:** TRN_GoalProgressの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: TRN_GoalProgress

### 不一致が検出された外部キー：

#### fk_TRN_GoalProgress_supervisor - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_TRN_GoalProgress_career_plan - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_TRN_GoalProgress_approved_by - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_TRN_GoalProgress_supervisorの修正
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_supervisor;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_TRN_GoalProgress_career_planの修正
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_career_plan;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_TRN_GoalProgress_approved_byの修正
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_approved_by;
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_supervisor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_TRN_GoalProgress_career_plan
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_TRN_GoalProgress_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 180. TRN_TrainingHistory

**説明:** TRN_TrainingHistoryの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: TRN_TrainingHistory

### 不一致が検出された外部キー：

#### fk_training_history_program - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_training_history_approver - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_training_history_programの修正
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_program;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_training_history_approverの修正
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_approver;
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_training_history_program
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_training_history_approver
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 181. TRN_PDU

**説明:** TRN_PDUの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: TRN_PDU

### 不一致が検出された外部キー：

#### fk_pdu_approver - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_pdu_certification - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_pdu_training - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_pdu_project - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_pdu_approverの修正
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_approver;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_pdu_certificationの修正
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_certification;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_pdu_trainingの修正
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_training;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_training
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_pdu_projectの修正
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_project;
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_project
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_pdu_approver
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_pdu_certification
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_pdu_training
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_pdu_project
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 182. TRN_SkillEvidence

**説明:** TRN_SkillEvidenceの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: TRN_SkillEvidence

### 不一致が検出された外部キー：

#### fk_evidence_certification - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_evidence_verifier - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_evidence_training - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_evidence_project - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_evidence_certificationの修正
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_certification;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_evidence_verifierの修正
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_verifier;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_evidence_trainingの修正
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_training;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_training
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_evidence_projectの修正
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_project;
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_project
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_evidence_certification
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_evidence_verifier
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_evidence_training
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_evidence_project
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 183. TRN_Notification

**説明:** TRN_Notificationの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: TRN_Notification

### 不一致が検出された外部キー：

#### fk_notification_sender - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_notification_senderの修正
ALTER TABLE TRN_Notification DROP FOREIGN KEY fk_notification_sender;
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_notification_sender
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 184. SYS_SystemLog

**説明:** SYS_SystemLogの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: SYS_SystemLog

### 不一致が検出された外部キー：

#### fk_log_user - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_log_userの修正
ALTER TABLE SYS_SystemLog DROP FOREIGN KEY fk_log_user;
ALTER TABLE SYS_SystemLog ADD CONSTRAINT fk_log_user
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_log_user
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 185. HIS_NotificationLog

**説明:** HIS_NotificationLogの外部キーカスケード設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一: HIS_NotificationLog

### 不一致が検出された外部キー：

#### fk_notification_log_template - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_notification_log_setting - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

#### fk_notification_log_integration - ON DELETE設定
- **DDL**: SET
- **YAML**: SET NULL
- **推奨**: SET NULL

### DDL修正手順：

#### 1. 外部キー制約の再作成
```sql
-- 既存の外部キー制約を削除して再作成

-- fk_notification_log_templateの修正
ALTER TABLE HIS_NotificationLog DROP FOREIGN KEY fk_notification_log_template;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_template
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_notification_log_settingの修正
ALTER TABLE HIS_NotificationLog DROP FOREIGN KEY fk_notification_log_setting;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_setting
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;

-- fk_notification_log_integrationの修正
ALTER TABLE HIS_NotificationLog DROP FOREIGN KEY fk_notification_log_integration;
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_integration
    FOREIGN KEY (参照元カラム) REFERENCES 参照先テーブル(参照先カラム)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### YAML修正手順：

#### {table_name}_details.yaml の修正
```yaml
foreign_keys:
  - name: fk_notification_log_template
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_notification_log_setting
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
  - name: fk_notification_log_integration
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: SET NULL
```

### 推奨カスケード設定：
- **ON UPDATE**: CASCADE（参照先の更新を自動反映）
- **ON DELETE**: SET NULL（参照先削除時はNULLに設定）

### 注意事項：
- 実際のカラム名とテーブル名に置き換えてください
- 業務要件に応じてカスケード設定を調整してください
- 変更前にデータのバックアップを取得してください

```

#### 186. HIS_NotificationLog

**説明:** 外部キーfk_notification_log_templateのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_notification_log_template` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE HIS_NotificationLog DROP FOREIGN KEY fk_notification_log_template;

-- 新しい外部キー制約を追加
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_template
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_notification_log_template
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 187. HIS_NotificationLog

**説明:** 外部キーfk_notification_log_settingのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_notification_log_setting` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE HIS_NotificationLog DROP FOREIGN KEY fk_notification_log_setting;

-- 新しい外部キー制約を追加
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_setting
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_notification_log_setting
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 188. HIS_NotificationLog

**説明:** 外部キーfk_notification_log_integrationのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_notification_log_integration` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE HIS_NotificationLog DROP FOREIGN KEY fk_notification_log_integration;

-- 新しい外部キー制約を追加
ALTER TABLE HIS_NotificationLog ADD CONSTRAINT fk_notification_log_integration
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_notification_log_integration
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 189. MST_CareerPlan

**説明:** 外部キーfk_career_plan_supervisorのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_career_plan_supervisor` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_supervisor;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_supervisor
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_supervisor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 190. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_departmentのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_career_plan_target_department` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_department;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_department
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_target_department
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 191. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_job_typeのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_career_plan_target_job_type` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_job_type;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_job_type
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_target_job_type
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 192. MST_CareerPlan

**説明:** 外部キーfk_career_plan_target_positionのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_career_plan_target_position` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_target_position;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_target_position
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_target_position
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 193. MST_CareerPlan

**説明:** 外部キーfk_career_plan_mentorのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_career_plan_mentor` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CareerPlan DROP FOREIGN KEY fk_career_plan_mentor;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CareerPlan ADD CONSTRAINT fk_career_plan_mentor
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_career_plan_mentor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 194. MST_Certification

**説明:** 外部キーfk_certification_skill_categoryのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_certification_skill_category` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Certification DROP FOREIGN KEY fk_certification_skill_category;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Certification ADD CONSTRAINT fk_certification_skill_category
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_certification_skill_category
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 195. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_approved_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_cert_req_approved_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_approved_by;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_approved_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 196. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_skill_gradeのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_cert_req_target_skill_grade` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_skill_grade;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_skill_grade
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_skill_grade
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 197. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_departmentのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_cert_req_target_department` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_department;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_department
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_department
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 198. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_job_typeのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_cert_req_target_job_type` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_job_type;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_job_type
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_job_type
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 199. MST_CertificationRequirement

**説明:** 外部キーfk_cert_req_target_positionのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_cert_req_target_position` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_CertificationRequirement DROP FOREIGN KEY fk_cert_req_target_position;

-- 新しい外部キー制約を追加
ALTER TABLE MST_CertificationRequirement ADD CONSTRAINT fk_cert_req_target_position
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_cert_req_target_position
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 200. MST_Department

**説明:** 外部キーfk_department_managerのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_department_manager` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_manager;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_manager
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_department_manager
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 201. MST_Department

**説明:** 外部キーfk_department_deputyのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_department_deputy` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_deputy;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_deputy
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_department_deputy
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 202. MST_Department

**説明:** 外部キーfk_department_parentのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_department_parent` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Department DROP FOREIGN KEY fk_department_parent;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Department ADD CONSTRAINT fk_department_parent
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_department_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 203. MST_Employee

**説明:** 外部キーfk_employee_managerのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_employee_manager` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_manager;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_manager
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_employee_manager
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 204. MST_Employee

**説明:** 外部キーfk_employee_job_typeのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_employee_job_type` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_job_type;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_job_type
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_employee_job_type
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 205. MST_Employee

**説明:** 外部キーfk_employee_positionのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_employee_position` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Employee DROP FOREIGN KEY fk_employee_position;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Employee ADD CONSTRAINT fk_employee_position
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_employee_position
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 206. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_reporting_managerのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_MST_EmployeeDepartment_reporting_manager` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_reporting_manager;

-- 新しい外部キー制約を追加
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_reporting_manager
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_reporting_manager
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 207. MST_EmployeeDepartment

**説明:** 外部キーfk_MST_EmployeeDepartment_approved_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_MST_EmployeeDepartment_approved_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeDepartment DROP FOREIGN KEY fk_MST_EmployeeDepartment_approved_by;

-- 新しい外部キー制約を追加
ALTER TABLE MST_EmployeeDepartment ADD CONSTRAINT fk_MST_EmployeeDepartment_approved_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeeDepartment_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 208. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_approved_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_emp_job_type_approved_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_approved_by;

-- 新しい外部キー制約を追加
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_approved_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 209. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_supervisorのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_emp_job_type_supervisor` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_supervisor;

-- 新しい外部キー制約を追加
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_supervisor
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_supervisor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 210. MST_EmployeeJobType

**説明:** 外部キーfk_emp_job_type_mentorのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_emp_job_type_mentor` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeeJobType DROP FOREIGN KEY fk_emp_job_type_mentor;

-- 新しい外部キー制約を追加
ALTER TABLE MST_EmployeeJobType ADD CONSTRAINT fk_emp_job_type_mentor
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_emp_job_type_mentor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 211. MST_EmployeePosition

**説明:** 外部キーfk_MST_EmployeePosition_approved_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_MST_EmployeePosition_approved_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_EmployeePosition DROP FOREIGN KEY fk_MST_EmployeePosition_approved_by;

-- 新しい外部キー制約を追加
ALTER TABLE MST_EmployeePosition ADD CONSTRAINT fk_MST_EmployeePosition_approved_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_MST_EmployeePosition_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 212. MST_NotificationSettings

**説明:** 外部キーfk_notification_settings_templateのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_notification_settings_template` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_NotificationSettings DROP FOREIGN KEY fk_notification_settings_template;

-- 新しい外部キー制約を追加
ALTER TABLE MST_NotificationSettings ADD CONSTRAINT fk_notification_settings_template
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_notification_settings_template
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 213. MST_Permission

**説明:** 外部キーfk_permission_parentのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_permission_parent` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Permission DROP FOREIGN KEY fk_permission_parent;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Permission ADD CONSTRAINT fk_permission_parent
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_permission_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 214. MST_Role

**説明:** 外部キーfk_role_parentのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_role_parent` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Role DROP FOREIGN KEY fk_role_parent;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Role ADD CONSTRAINT fk_role_parent
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_role_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 215. MST_SkillCategory

**説明:** 外部キーfk_skillcategory_parentのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_skillcategory_parent` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_SkillCategory DROP FOREIGN KEY fk_skillcategory_parent;

-- 新しい外部キー制約を追加
ALTER TABLE MST_SkillCategory ADD CONSTRAINT fk_skillcategory_parent
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skillcategory_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 216. MST_Tenant

**説明:** 外部キーfk_tenant_parentのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_tenant_parent` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_Tenant DROP FOREIGN KEY fk_tenant_parent;

-- 新しい外部キー制約を追加
ALTER TABLE MST_Tenant ADD CONSTRAINT fk_tenant_parent
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_tenant_parent
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 217. MST_TrainingProgram

**説明:** 外部キーfk_training_program_approved_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_training_program_approved_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_TrainingProgram DROP FOREIGN KEY fk_training_program_approved_by;

-- 新しい外部キー制約を追加
ALTER TABLE MST_TrainingProgram ADD CONSTRAINT fk_training_program_approved_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_program_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 218. MST_UserAuth

**説明:** 外部キーfk_userauth_employeeのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_userauth_employee` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_UserAuth DROP FOREIGN KEY fk_userauth_employee;

-- 新しい外部キー制約を追加
ALTER TABLE MST_UserAuth ADD CONSTRAINT fk_userauth_employee
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_userauth_employee
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 219. MST_UserRole

**説明:** 外部キーfk_userrole_delegation_sourceのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_userrole_delegation_source` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_delegation_source;

-- 新しい外部キー制約を追加
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_delegation_source
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_userrole_delegation_source
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 220. MST_UserRole

**説明:** 外部キーfk_userrole_assigned_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_userrole_assigned_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_assigned_by;

-- 新しい外部キー制約を追加
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_assigned_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_userrole_assigned_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 221. MST_UserRole

**説明:** 外部キーfk_userrole_approved_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_userrole_approved_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE MST_UserRole DROP FOREIGN KEY fk_userrole_approved_by;

-- 新しい外部キー制約を追加
ALTER TABLE MST_UserRole ADD CONSTRAINT fk_userrole_approved_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_userrole_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 222. SYS_SystemLog

**説明:** 外部キーfk_log_userのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_log_user` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE SYS_SystemLog DROP FOREIGN KEY fk_log_user;

-- 新しい外部キー制約を追加
ALTER TABLE SYS_SystemLog ADD CONSTRAINT fk_log_user
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_log_user
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 223. TRN_EmployeeSkillGrade

**説明:** 外部キーfk_skill_grade_evaluatorのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_skill_grade_evaluator` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_EmployeeSkillGrade DROP FOREIGN KEY fk_skill_grade_evaluator;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_EmployeeSkillGrade ADD CONSTRAINT fk_skill_grade_evaluator
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_grade_evaluator
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 224. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_supervisorのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_TRN_GoalProgress_supervisor` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_supervisor;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_supervisor
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_supervisor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 225. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_career_planのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_TRN_GoalProgress_career_plan` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_career_plan;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_career_plan
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_career_plan
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 226. TRN_GoalProgress

**説明:** 外部キーfk_TRN_GoalProgress_approved_byのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_TRN_GoalProgress_approved_by` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_GoalProgress DROP FOREIGN KEY fk_TRN_GoalProgress_approved_by;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_GoalProgress ADD CONSTRAINT fk_TRN_GoalProgress_approved_by
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_TRN_GoalProgress_approved_by
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 227. TRN_Notification

**説明:** 外部キーfk_notification_senderのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_notification_sender` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_Notification DROP FOREIGN KEY fk_notification_sender;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_Notification ADD CONSTRAINT fk_notification_sender
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_notification_sender
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 228. TRN_PDU

**説明:** 外部キーfk_pdu_approverのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_pdu_approver` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_approver;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_approver
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_pdu_approver
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 229. TRN_PDU

**説明:** 外部キーfk_pdu_certificationのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_pdu_certification` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_certification;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_certification
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_pdu_certification
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 230. TRN_PDU

**説明:** 外部キーfk_pdu_trainingのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_pdu_training` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_training;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_training
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_pdu_training
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 231. TRN_PDU

**説明:** 外部キーfk_pdu_projectのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_pdu_project` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_PDU DROP FOREIGN KEY fk_pdu_project;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_PDU ADD CONSTRAINT fk_pdu_project
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_pdu_project
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 232. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_certificationのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_evidence_certification` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_certification;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_certification
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_certification
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 233. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_verifierのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_evidence_verifier` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_verifier;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_verifier
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_verifier
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 234. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_trainingのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_evidence_training` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_training;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_training
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_training
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 235. TRN_SkillEvidence

**説明:** 外部キーfk_evidence_projectのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_evidence_project` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillEvidence DROP FOREIGN KEY fk_evidence_project;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_SkillEvidence ADD CONSTRAINT fk_evidence_project
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_evidence_project
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 236. TRN_SkillRecord

**説明:** 外部キーfk_skill_certificationのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_skill_certification` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_certification;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_certification
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_certification
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 237. TRN_SkillRecord

**説明:** 外部キーfk_skill_assessorのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_skill_assessor` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_assessor;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_assessor
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_assessor
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 238. TRN_SkillRecord

**説明:** 外部キーfk_skill_categoryのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_skill_category` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_SkillRecord DROP FOREIGN KEY fk_skill_category;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_SkillRecord ADD CONSTRAINT fk_skill_category
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_skill_category
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 239. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_programのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_training_history_program` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_program;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_program
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_history_program
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

#### 240. TRN_TrainingHistory

**説明:** 外部キーfk_training_history_approverのON DELETE設定を統一

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## 外部キーカスケード設定統一提案

外部キー `fk_training_history_approver` のON DELETE設定を統一してください。

### 現在の設定：
- DDL: SET
- YAML: SET NULL

### 推奨設定：
- 統一設定: CASCADE

### 修正手順：

#### DDLファイルの修正：
```sql
-- 既存の外部キー制約を削除
ALTER TABLE TRN_TrainingHistory DROP FOREIGN KEY fk_training_history_approver;

-- 新しい外部キー制約を追加
ALTER TABLE TRN_TrainingHistory ADD CONSTRAINT fk_training_history_approver
    FOREIGN KEY (...) REFERENCES ...
    ON UPDATE CASCADE
    ON DELETE CASCADE;
```

#### YAMLファイルの修正：
```yaml
foreign_keys:
  - name: fk_training_history_approver
    # ... 他の設定 ...
    on_update: CASCADE
    on_delete: CASCADE
```

```

### DDL 修正 (54件)

#### 1. MST_UserAuth

**説明:** DDLに外部キーfk_mst_userauth_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_UserAuth

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_UserAuth.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_UserAuth
ADD CONSTRAINT fk_mst_userauth_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 2. MST_Role

**説明:** DDLに外部キーfk_mst_role_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_Role

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_Role.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_Role
ADD CONSTRAINT fk_mst_role_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 3. MST_Permission

**説明:** DDLに外部キーfk_mst_permission_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_Permission

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_Permission.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_Permission
ADD CONSTRAINT fk_mst_permission_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 4. MST_UserRole

**説明:** DDLに外部キーfk_mst_userrole_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_UserRole

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_UserRole.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_UserRole
ADD CONSTRAINT fk_mst_userrole_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 5. MST_UserRole

**説明:** DDLに外部キーfk_mst_userrole_user_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_UserRole

### 不足している外部キー：
- **参照元カラム**: user_id
- **参照先テーブル**: MST_UserAuth
- **参照先カラム**: id

### DDL修正手順：

#### MST_UserRole.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_UserRole
ADD CONSTRAINT fk_mst_userrole_user_id
    FOREIGN KEY (user_id)
    REFERENCES MST_UserAuth(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 6. MST_RolePermission

**説明:** DDLに外部キーfk_mst_rolepermission_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_RolePermission

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_RolePermission.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_RolePermission
ADD CONSTRAINT fk_mst_rolepermission_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 7. MST_RolePermission

**説明:** DDLに外部キーfk_mst_rolepermission_role_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_RolePermission

### 不足している外部キー：
- **参照元カラム**: role_id
- **参照先テーブル**: MST_Role
- **参照先カラム**: id

### DDL修正手順：

#### MST_RolePermission.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_RolePermission
ADD CONSTRAINT fk_mst_rolepermission_role_id
    FOREIGN KEY (role_id)
    REFERENCES MST_Role(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 8. MST_RolePermission

**説明:** DDLに外部キーfk_mst_rolepermission_permission_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_RolePermission

### 不足している外部キー：
- **参照元カラム**: permission_id
- **参照先テーブル**: MST_Permission
- **参照先カラム**: id

### DDL修正手順：

#### MST_RolePermission.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_RolePermission
ADD CONSTRAINT fk_mst_rolepermission_permission_id
    FOREIGN KEY (permission_id)
    REFERENCES MST_Permission(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 9. MST_Employee

**説明:** DDLに外部キーfk_mst_employee_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_Employee

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_Employee.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_Employee
ADD CONSTRAINT fk_mst_employee_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 10. MST_Department

**説明:** DDLに外部キーfk_mst_department_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_Department

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_Department.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_Department
ADD CONSTRAINT fk_mst_department_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 11. MST_Position

**説明:** DDLに外部キーfk_mst_position_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_Position

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_Position.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_Position
ADD CONSTRAINT fk_mst_position_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 12. MST_JobType

**説明:** DDLに外部キーfk_mst_jobtype_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_JobType

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_JobType.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_JobType
ADD CONSTRAINT fk_mst_jobtype_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 13. MST_EmployeeDepartment

**説明:** DDLに外部キーfk_mst_employeedepartment_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_EmployeeDepartment

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_EmployeeDepartment.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_EmployeeDepartment
ADD CONSTRAINT fk_mst_employeedepartment_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 14. MST_EmployeePosition

**説明:** DDLに外部キーfk_mst_employeeposition_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_EmployeePosition

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_EmployeePosition.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_EmployeePosition
ADD CONSTRAINT fk_mst_employeeposition_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 15. MST_EmployeeJobType

**説明:** DDLに外部キーfk_mst_employeejobtype_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_EmployeeJobType

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_EmployeeJobType.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_EmployeeJobType
ADD CONSTRAINT fk_mst_employeejobtype_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 16. MST_SkillCategory

**説明:** DDLに外部キーfk_mst_skillcategory_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SkillCategory

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_SkillCategory.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SkillCategory
ADD CONSTRAINT fk_mst_skillcategory_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 17. MST_Skill

**説明:** DDLに外部キーfk_mst_skill_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_Skill

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_Skill.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_Skill
ADD CONSTRAINT fk_mst_skill_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 18. MST_SkillHierarchy

**説明:** DDLに外部キーfk_mst_skillhierarchy_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SkillHierarchy

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_SkillHierarchy.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SkillHierarchy
ADD CONSTRAINT fk_mst_skillhierarchy_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 19. MST_SkillHierarchy

**説明:** DDLに外部キーfk_mst_skillhierarchy_parent_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SkillHierarchy

### 不足している外部キー：
- **参照元カラム**: parent_skill_id
- **参照先テーブル**: MST_SkillHierarchy
- **参照先カラム**: id

### DDL修正手順：

#### MST_SkillHierarchy.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SkillHierarchy
ADD CONSTRAINT fk_mst_skillhierarchy_parent_skill_id
    FOREIGN KEY (parent_skill_id)
    REFERENCES MST_SkillHierarchy(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 20. MST_SkillItem

**説明:** DDLに外部キーfk_mst_skillitem_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SkillItem

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_SkillItem.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SkillItem
ADD CONSTRAINT fk_mst_skillitem_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 21. MST_SkillItem

**説明:** DDLに外部キーfk_mst_skillitem_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SkillItem

### 不足している外部キー：
- **参照元カラム**: skill_id
- **参照先テーブル**: MST_Skill
- **参照先カラム**: id

### DDL修正手順：

#### MST_SkillItem.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SkillItem
ADD CONSTRAINT fk_mst_skillitem_skill_id
    FOREIGN KEY (skill_id)
    REFERENCES MST_Skill(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 22. MST_SkillGrade

**説明:** DDLに外部キーfk_mst_skillgrade_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SkillGrade

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_SkillGrade.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SkillGrade
ADD CONSTRAINT fk_mst_skillgrade_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 23. MST_SkillGradeRequirement

**説明:** DDLに外部キーfk_mst_skillgraderequirement_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SkillGradeRequirement

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_SkillGradeRequirement.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SkillGradeRequirement
ADD CONSTRAINT fk_mst_skillgraderequirement_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 24. MST_JobTypeSkill

**説明:** DDLに外部キーfk_mst_jobtypeskill_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_JobTypeSkill

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_JobTypeSkill.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_JobTypeSkill
ADD CONSTRAINT fk_mst_jobtypeskill_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 25. MST_JobTypeSkillGrade

**説明:** DDLに外部キーfk_mst_jobtypeskillgrade_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_JobTypeSkillGrade

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_JobTypeSkillGrade.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_JobTypeSkillGrade
ADD CONSTRAINT fk_mst_jobtypeskillgrade_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 26. MST_Certification

**説明:** DDLに外部キーfk_mst_certification_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_Certification

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_Certification.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_Certification
ADD CONSTRAINT fk_mst_certification_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 27. MST_CertificationRequirement

**説明:** DDLに外部キーfk_mst_certificationrequirement_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_CertificationRequirement

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_CertificationRequirement.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_CertificationRequirement
ADD CONSTRAINT fk_mst_certificationrequirement_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 28. MST_TrainingProgram

**説明:** DDLに外部キーfk_mst_trainingprogram_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_TrainingProgram

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_TrainingProgram.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_TrainingProgram
ADD CONSTRAINT fk_mst_trainingprogram_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 29. MST_CareerPlan

**説明:** DDLに外部キーfk_mst_careerplan_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_CareerPlan

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_CareerPlan.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_CareerPlan
ADD CONSTRAINT fk_mst_careerplan_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 30. MST_ReportTemplate

**説明:** DDLに外部キーfk_mst_reporttemplate_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_ReportTemplate

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_ReportTemplate.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_ReportTemplate
ADD CONSTRAINT fk_mst_reporttemplate_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 31. MST_SystemConfig

**説明:** DDLに外部キーfk_mst_systemconfig_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_SystemConfig

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_SystemConfig.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_SystemConfig
ADD CONSTRAINT fk_mst_systemconfig_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 32. MST_NotificationSettings

**説明:** DDLに外部キーfk_mst_notificationsettings_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_NotificationSettings

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_NotificationSettings.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_NotificationSettings
ADD CONSTRAINT fk_mst_notificationsettings_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 33. MST_NotificationTemplate

**説明:** DDLに外部キーfk_mst_notificationtemplate_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: MST_NotificationTemplate

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### MST_NotificationTemplate.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE MST_NotificationTemplate
ADD CONSTRAINT fk_mst_notificationtemplate_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 34. TRN_SkillRecord

**説明:** DDLに外部キーfk_trn_skillrecord_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_SkillRecord

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_SkillRecord.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_SkillRecord
ADD CONSTRAINT fk_trn_skillrecord_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 35. TRN_EmployeeSkillGrade

**説明:** DDLに外部キーfk_trn_employeeskillgrade_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_EmployeeSkillGrade

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_EmployeeSkillGrade.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_EmployeeSkillGrade
ADD CONSTRAINT fk_trn_employeeskillgrade_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 36. TRN_EmployeeSkillGrade

**説明:** DDLに外部キーfk_trn_employeeskillgrade_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_EmployeeSkillGrade

### 不足している外部キー：
- **参照元カラム**: skill_id
- **参照先テーブル**: MST_Skill
- **参照先カラム**: id

### DDL修正手順：

#### TRN_EmployeeSkillGrade.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_EmployeeSkillGrade
ADD CONSTRAINT fk_trn_employeeskillgrade_skill_id
    FOREIGN KEY (skill_id)
    REFERENCES MST_Skill(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 37. TRN_GoalProgress

**説明:** DDLに外部キーfk_trn_goalprogress_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_GoalProgress

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_GoalProgress.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_GoalProgress
ADD CONSTRAINT fk_trn_goalprogress_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 38. TRN_ProjectRecord

**説明:** DDLに外部キーfk_trn_projectrecord_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_ProjectRecord

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_ProjectRecord.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_ProjectRecord
ADD CONSTRAINT fk_trn_projectrecord_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 39. TRN_TrainingHistory

**説明:** DDLに外部キーfk_trn_traininghistory_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_TrainingHistory

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_TrainingHistory.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_TrainingHistory
ADD CONSTRAINT fk_trn_traininghistory_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 40. TRN_PDU

**説明:** DDLに外部キーfk_trn_pdu_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_PDU

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_PDU.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_PDU
ADD CONSTRAINT fk_trn_pdu_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 41. TRN_SkillEvidence

**説明:** DDLに外部キーfk_trn_skillevidence_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_SkillEvidence

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_SkillEvidence.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_SkillEvidence
ADD CONSTRAINT fk_trn_skillevidence_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 42. TRN_SkillEvidence

**説明:** DDLに外部キーfk_trn_skillevidence_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_SkillEvidence

### 不足している外部キー：
- **参照元カラム**: skill_id
- **参照先テーブル**: MST_Skill
- **参照先カラム**: id

### DDL修正手順：

#### TRN_SkillEvidence.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_SkillEvidence
ADD CONSTRAINT fk_trn_skillevidence_skill_id
    FOREIGN KEY (skill_id)
    REFERENCES MST_Skill(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 43. TRN_Notification

**説明:** DDLに外部キーfk_trn_notification_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: TRN_Notification

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### TRN_Notification.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE TRN_Notification
ADD CONSTRAINT fk_trn_notification_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 44. SYS_SkillIndex

**説明:** DDLに外部キーfk_sys_skillindex_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: SYS_SkillIndex

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### SYS_SkillIndex.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE SYS_SkillIndex
ADD CONSTRAINT fk_sys_skillindex_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 45. SYS_SkillMatrix

**説明:** DDLに外部キーfk_sys_skillmatrix_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: SYS_SkillMatrix

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### SYS_SkillMatrix.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE SYS_SkillMatrix
ADD CONSTRAINT fk_sys_skillmatrix_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 46. SYS_BackupHistory

**説明:** DDLに外部キーfk_sys_backuphistory_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: SYS_BackupHistory

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### SYS_BackupHistory.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE SYS_BackupHistory
ADD CONSTRAINT fk_sys_backuphistory_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 47. SYS_SystemLog

**説明:** DDLに外部キーfk_sys_systemlog_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: SYS_SystemLog

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### SYS_SystemLog.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE SYS_SystemLog
ADD CONSTRAINT fk_sys_systemlog_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 48. SYS_TokenStore

**説明:** DDLに外部キーfk_sys_tokenstore_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: SYS_TokenStore

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### SYS_TokenStore.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE SYS_TokenStore
ADD CONSTRAINT fk_sys_tokenstore_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 49. SYS_MasterData

**説明:** DDLに外部キーfk_sys_masterdata_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: SYS_MasterData

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### SYS_MasterData.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE SYS_MasterData
ADD CONSTRAINT fk_sys_masterdata_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 50. SYS_IntegrationConfig

**説明:** DDLに外部キーfk_sys_integrationconfig_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: SYS_IntegrationConfig

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### SYS_IntegrationConfig.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE SYS_IntegrationConfig
ADD CONSTRAINT fk_sys_integrationconfig_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 51. HIS_NotificationLog

**説明:** DDLに外部キーfk_his_notificationlog_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: HIS_NotificationLog

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### HIS_NotificationLog.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE HIS_NotificationLog
ADD CONSTRAINT fk_his_notificationlog_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 52. HIS_ReportGeneration

**説明:** DDLに外部キーfk_his_reportgeneration_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: HIS_ReportGeneration

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### HIS_ReportGeneration.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE HIS_ReportGeneration
ADD CONSTRAINT fk_his_reportgeneration_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 53. HIS_ReportGeneration

**説明:** DDLに外部キーfk_his_reportgeneration_requested_byを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: HIS_ReportGeneration

### 不足している外部キー：
- **参照元カラム**: requested_by
- **参照先テーブル**: MST_UserAuth
- **参照先カラム**: id

### DDL修正手順：

#### HIS_ReportGeneration.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE HIS_ReportGeneration
ADD CONSTRAINT fk_his_reportgeneration_requested_by
    FOREIGN KEY (requested_by)
    REFERENCES MST_UserAuth(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

#### 54. WRK_BatchJobLog

**説明:** DDLに外部キーfk_wrk_batchjoblog_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## DDL外部キー追加: WRK_BatchJobLog

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### DDL修正手順：

#### WRK_BatchJobLog.sql への外部キー追加
```sql
-- 外部キー制約を追加
ALTER TABLE WRK_BatchJobLog
ADD CONSTRAINT fk_wrk_batchjoblog_tenant_id
    FOREIGN KEY (tenant_id)
    REFERENCES MST_Tenant(id)
    ON UPDATE CASCADE
    ON DELETE SET NULL;
```

### 注意事項：
- 参照先テーブルとカラムが存在することを確認してください
- データ型の互換性を確認してください
- 既存データの整合性を事前にチェックしてください

```

### YAML 修正 (54件)

#### 1. MST_UserAuth

**説明:** YAMLに外部キーfk_mst_userauth_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_UserAuth

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_UserAuth_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_userauth_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 2. MST_Role

**説明:** YAMLに外部キーfk_mst_role_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_Role

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_Role_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_role_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 3. MST_Permission

**説明:** YAMLに外部キーfk_mst_permission_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_Permission

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_Permission_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_permission_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 4. MST_UserRole

**説明:** YAMLに外部キーfk_mst_userrole_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_UserRole

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_UserRole_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_userrole_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 5. MST_UserRole

**説明:** YAMLに外部キーfk_mst_userrole_user_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_UserRole

### 不足している外部キー：
- **参照元カラム**: user_id
- **参照先テーブル**: MST_UserAuth
- **参照先カラム**: id

### YAML修正手順：

#### MST_UserRole_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_userrole_user_id
    column: user_id
    reference_table: MST_UserAuth
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_UserAuthへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 6. MST_RolePermission

**説明:** YAMLに外部キーfk_mst_rolepermission_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_RolePermission

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_RolePermission_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_rolepermission_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 7. MST_RolePermission

**説明:** YAMLに外部キーfk_mst_rolepermission_role_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_RolePermission

### 不足している外部キー：
- **参照元カラム**: role_id
- **参照先テーブル**: MST_Role
- **参照先カラム**: id

### YAML修正手順：

#### MST_RolePermission_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_rolepermission_role_id
    column: role_id
    reference_table: MST_Role
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Roleへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 8. MST_RolePermission

**説明:** YAMLに外部キーfk_mst_rolepermission_permission_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_RolePermission

### 不足している外部キー：
- **参照元カラム**: permission_id
- **参照先テーブル**: MST_Permission
- **参照先カラム**: id

### YAML修正手順：

#### MST_RolePermission_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_rolepermission_permission_id
    column: permission_id
    reference_table: MST_Permission
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Permissionへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 9. MST_Employee

**説明:** YAMLに外部キーfk_mst_employee_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_Employee

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_Employee_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_employee_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 10. MST_Department

**説明:** YAMLに外部キーfk_mst_department_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_Department

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_Department_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_department_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 11. MST_Position

**説明:** YAMLに外部キーfk_mst_position_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_Position

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_Position_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_position_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 12. MST_JobType

**説明:** YAMLに外部キーfk_mst_jobtype_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_JobType

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_JobType_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_jobtype_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 13. MST_EmployeeDepartment

**説明:** YAMLに外部キーfk_mst_employeedepartment_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_EmployeeDepartment

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_EmployeeDepartment_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_employeedepartment_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 14. MST_EmployeePosition

**説明:** YAMLに外部キーfk_mst_employeeposition_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_EmployeePosition

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_EmployeePosition_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_employeeposition_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 15. MST_EmployeeJobType

**説明:** YAMLに外部キーfk_mst_employeejobtype_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_EmployeeJobType

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_EmployeeJobType_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_employeejobtype_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 16. MST_SkillCategory

**説明:** YAMLに外部キーfk_mst_skillcategory_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SkillCategory

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_SkillCategory_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skillcategory_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 17. MST_Skill

**説明:** YAMLに外部キーfk_mst_skill_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_Skill

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_Skill_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skill_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 18. MST_SkillHierarchy

**説明:** YAMLに外部キーfk_mst_skillhierarchy_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SkillHierarchy

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_SkillHierarchy_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skillhierarchy_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 19. MST_SkillHierarchy

**説明:** YAMLに外部キーfk_mst_skillhierarchy_parent_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SkillHierarchy

### 不足している外部キー：
- **参照元カラム**: parent_skill_id
- **参照先テーブル**: MST_SkillHierarchy
- **参照先カラム**: id

### YAML修正手順：

#### MST_SkillHierarchy_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skillhierarchy_parent_skill_id
    column: parent_skill_id
    reference_table: MST_SkillHierarchy
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_SkillHierarchyへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 20. MST_SkillItem

**説明:** YAMLに外部キーfk_mst_skillitem_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SkillItem

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_SkillItem_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skillitem_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 21. MST_SkillItem

**説明:** YAMLに外部キーfk_mst_skillitem_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SkillItem

### 不足している外部キー：
- **参照元カラム**: skill_id
- **参照先テーブル**: MST_Skill
- **参照先カラム**: id

### YAML修正手順：

#### MST_SkillItem_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skillitem_skill_id
    column: skill_id
    reference_table: MST_Skill
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Skillへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 22. MST_SkillGrade

**説明:** YAMLに外部キーfk_mst_skillgrade_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SkillGrade

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_SkillGrade_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skillgrade_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 23. MST_SkillGradeRequirement

**説明:** YAMLに外部キーfk_mst_skillgraderequirement_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SkillGradeRequirement

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_SkillGradeRequirement_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_skillgraderequirement_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 24. MST_JobTypeSkill

**説明:** YAMLに外部キーfk_mst_jobtypeskill_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_JobTypeSkill

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_JobTypeSkill_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_jobtypeskill_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 25. MST_JobTypeSkillGrade

**説明:** YAMLに外部キーfk_mst_jobtypeskillgrade_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_JobTypeSkillGrade

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_JobTypeSkillGrade_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_jobtypeskillgrade_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 26. MST_Certification

**説明:** YAMLに外部キーfk_mst_certification_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_Certification

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_Certification_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_certification_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 27. MST_CertificationRequirement

**説明:** YAMLに外部キーfk_mst_certificationrequirement_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_CertificationRequirement

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_CertificationRequirement_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_certificationrequirement_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 28. MST_TrainingProgram

**説明:** YAMLに外部キーfk_mst_trainingprogram_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_TrainingProgram

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_TrainingProgram_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_trainingprogram_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 29. MST_CareerPlan

**説明:** YAMLに外部キーfk_mst_careerplan_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_CareerPlan

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_CareerPlan_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_careerplan_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 30. MST_ReportTemplate

**説明:** YAMLに外部キーfk_mst_reporttemplate_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_ReportTemplate

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_ReportTemplate_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_reporttemplate_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 31. MST_SystemConfig

**説明:** YAMLに外部キーfk_mst_systemconfig_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_SystemConfig

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_SystemConfig_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_systemconfig_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 32. MST_NotificationSettings

**説明:** YAMLに外部キーfk_mst_notificationsettings_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_NotificationSettings

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_NotificationSettings_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_notificationsettings_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 33. MST_NotificationTemplate

**説明:** YAMLに外部キーfk_mst_notificationtemplate_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: MST_NotificationTemplate

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### MST_NotificationTemplate_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_mst_notificationtemplate_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 34. TRN_SkillRecord

**説明:** YAMLに外部キーfk_trn_skillrecord_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_SkillRecord

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_SkillRecord_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_skillrecord_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 35. TRN_EmployeeSkillGrade

**説明:** YAMLに外部キーfk_trn_employeeskillgrade_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_EmployeeSkillGrade

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_EmployeeSkillGrade_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_employeeskillgrade_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 36. TRN_EmployeeSkillGrade

**説明:** YAMLに外部キーfk_trn_employeeskillgrade_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_EmployeeSkillGrade

### 不足している外部キー：
- **参照元カラム**: skill_id
- **参照先テーブル**: MST_Skill
- **参照先カラム**: id

### YAML修正手順：

#### TRN_EmployeeSkillGrade_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_employeeskillgrade_skill_id
    column: skill_id
    reference_table: MST_Skill
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Skillへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 37. TRN_GoalProgress

**説明:** YAMLに外部キーfk_trn_goalprogress_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_GoalProgress

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_GoalProgress_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_goalprogress_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 38. TRN_ProjectRecord

**説明:** YAMLに外部キーfk_trn_projectrecord_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_ProjectRecord

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_ProjectRecord_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_projectrecord_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 39. TRN_TrainingHistory

**説明:** YAMLに外部キーfk_trn_traininghistory_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_TrainingHistory

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_TrainingHistory_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_traininghistory_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 40. TRN_PDU

**説明:** YAMLに外部キーfk_trn_pdu_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_PDU

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_PDU_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_pdu_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 41. TRN_SkillEvidence

**説明:** YAMLに外部キーfk_trn_skillevidence_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_SkillEvidence

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_SkillEvidence_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_skillevidence_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 42. TRN_SkillEvidence

**説明:** YAMLに外部キーfk_trn_skillevidence_skill_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_SkillEvidence

### 不足している外部キー：
- **参照元カラム**: skill_id
- **参照先テーブル**: MST_Skill
- **参照先カラム**: id

### YAML修正手順：

#### TRN_SkillEvidence_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_skillevidence_skill_id
    column: skill_id
    reference_table: MST_Skill
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Skillへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 43. TRN_Notification

**説明:** YAMLに外部キーfk_trn_notification_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: TRN_Notification

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### TRN_Notification_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_trn_notification_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 44. SYS_SkillIndex

**説明:** YAMLに外部キーfk_sys_skillindex_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: SYS_SkillIndex

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### SYS_SkillIndex_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_sys_skillindex_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 45. SYS_SkillMatrix

**説明:** YAMLに外部キーfk_sys_skillmatrix_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: SYS_SkillMatrix

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### SYS_SkillMatrix_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_sys_skillmatrix_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 46. SYS_BackupHistory

**説明:** YAMLに外部キーfk_sys_backuphistory_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: SYS_BackupHistory

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### SYS_BackupHistory_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_sys_backuphistory_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 47. SYS_SystemLog

**説明:** YAMLに外部キーfk_sys_systemlog_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: SYS_SystemLog

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### SYS_SystemLog_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_sys_systemlog_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 48. SYS_TokenStore

**説明:** YAMLに外部キーfk_sys_tokenstore_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: SYS_TokenStore

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### SYS_TokenStore_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_sys_tokenstore_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 49. SYS_MasterData

**説明:** YAMLに外部キーfk_sys_masterdata_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: SYS_MasterData

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### SYS_MasterData_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_sys_masterdata_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 50. SYS_IntegrationConfig

**説明:** YAMLに外部キーfk_sys_integrationconfig_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: SYS_IntegrationConfig

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### SYS_IntegrationConfig_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_sys_integrationconfig_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 51. HIS_NotificationLog

**説明:** YAMLに外部キーfk_his_notificationlog_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: HIS_NotificationLog

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### HIS_NotificationLog_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_his_notificationlog_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 52. HIS_ReportGeneration

**説明:** YAMLに外部キーfk_his_reportgeneration_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: HIS_ReportGeneration

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### HIS_ReportGeneration_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_his_reportgeneration_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 53. HIS_ReportGeneration

**説明:** YAMLに外部キーfk_his_reportgeneration_requested_byを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: HIS_ReportGeneration

### 不足している外部キー：
- **参照元カラム**: requested_by
- **参照先テーブル**: MST_UserAuth
- **参照先カラム**: id

### YAML修正手順：

#### HIS_ReportGeneration_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_his_reportgeneration_requested_by
    column: requested_by
    reference_table: MST_UserAuth
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_UserAuthへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```

#### 54. WRK_BatchJobLog

**説明:** YAMLに外部キーfk_wrk_batchjoblog_tenant_idを追加

⚠️ **重要:** この修正は重要です。

💾 **注意:** 修正前にバックアップを取得してください。

**修正内容:**
```sql

## YAML外部キー追加: WRK_BatchJobLog

### 不足している外部キー：
- **参照元カラム**: tenant_id
- **参照先テーブル**: MST_Tenant
- **参照先カラム**: id

### YAML修正手順：

#### WRK_BatchJobLog_details.yaml への外部キー追加
```yaml
foreign_keys:
  - name: fk_wrk_batchjoblog_tenant_id
    column: tenant_id
    reference_table: MST_Tenant
    reference_column: id
    on_update: CASCADE
    on_delete: SET NULL
    description: MST_Tenantへの参照
```

### 注意事項：
- 複数カラムの外部キーの場合は適切に調整してください
- 業務要件に応じてカスケード設定を調整してください

```
