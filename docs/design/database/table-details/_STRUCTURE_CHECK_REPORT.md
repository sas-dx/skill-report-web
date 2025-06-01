# テーブル詳細YAMLファイル構造一致性チェックレポート

## 実行日時
2025-06-01 17:16

## チェック結果概要

### ✅ 正常な項目
- **改版履歴コメント**: 全19ファイルで「# 改版履歴」コメントが正しく設定済み
- **基本構造**: 全ファイルで必須項目（table_name, logical_name, category）が存在

### ❌ 修正が必要な項目

#### 1. コメント行とtable_name不一致問題
以下のファイルでコメント行のテーブル名と実際のtable_nameが一致していません：

| ファイル名 | コメント行のテーブル名 | 実際のtable_name | 修正要否 |
|------------|----------------------|------------------|----------|
| MST_UserAuth_details.yaml | MST_SystemConfig | MST_UserAuth | ❌ 要修正 |
| MST_SystemConfig_details.yaml | MST_EmployeeJobType | MST_SystemConfig | ❌ 要修正 |
| MST_EmployeeJobType_details.yaml | MST_CareerPlan | MST_EmployeeJobType | ❌ 要修正 |
| MST_CareerPlan_details.yaml | MST_RolePermission | MST_CareerPlan | ❌ 要修正 |
| MST_RolePermission_details.yaml | TRN_PDU | MST_RolePermission | ❌ 要修正 |
| TRN_PDU_details.yaml | MST_Permission | TRN_PDU | ❌ 要修正 |
| MST_Permission_details.yaml | MST_TrainingProgram | MST_Permission | ❌ 要修正 |
| MST_TrainingProgram_details.yaml | TRN_GoalProgress | MST_TrainingProgram | ❌ 要修正 |
| TRN_GoalProgress_details.yaml | MST_UserRole | TRN_GoalProgress | ❌ 要修正 |
| MST_UserRole_details.yaml | MST_JobType | MST_UserRole | ❌ 要修正 |
| MST_JobType_details.yaml | MST_SkillHierarchy | MST_JobType | ❌ 要修正 |
| MST_SkillHierarchy_details.yaml | MST_SkillItem | MST_SkillHierarchy | ❌ 要修正 |
| MST_SkillItem_details.yaml | MST_Department | MST_SkillItem | ❌ 要修正 |
| MST_Department_details.yaml | TRN_SkillRecord | MST_Department | ❌ 要修正 |
| TRN_SkillRecord_details.yaml | MST_Employee | TRN_SkillRecord | ❌ 要修正 |
| MST_Employee_details.yaml | TRN_ProjectRecord | MST_Employee | ❌ 要修正 |
| TRN_ProjectRecord_details.yaml | MST_Position | TRN_ProjectRecord | ❌ 要修正 |
| MST_Position_details.yaml | MST_Role | MST_Position | ❌ 要修正 |
| MST_Role_details.yaml | TRN_TrainingHistory | MST_Role | ❌ 要修正 |
| TRN_TrainingHistory_details.yaml | MST_SkillCategory | TRN_TrainingHistory | ❌ 要修正 |
| MST_SkillCategory_details.yaml | MST_Certification | MST_SkillCategory | ❌ 要修正 |
| TRN_EmployeeSkillGrade_details.yaml | MST_CertificationRequirement | TRN_EmployeeSkillGrade | ❌ 要修正 |
| MST_CertificationRequirement_details.yaml | MST_SkillGrade | MST_CertificationRequirement | ❌ 要修正 |
| MST_SkillGrade_details.yaml | TRN_SkillEvidence | MST_SkillGrade | ❌ 要修正 |
| TRN_SkillEvidence_details.yaml | TRN_Notification | TRN_SkillEvidence | ❌ 要修正 |
| TRN_Notification_details.yaml | SYS_SystemLog | TRN_Notification | ❌ 要修正 |
| SYS_SystemLog_details.yaml | MST_Tenant | SYS_SystemLog | ❌ 要修正 |

#### 2. 正常なファイル
以下のファイルは正しく設定されています：

| ファイル名 | コメント行とtable_nameの一致 | 状態 |
|------------|----------------------------|------|
| MST_Certification_details.yaml | ✅ 一致 | 正常 |
| MST_Tenant_details.yaml | ✅ 一致 | 正常 |

## 推奨修正アクション

### 1. 緊急修正（優先度：高）
コメント行のテーブル名を実際のtable_nameと一致させる修正を実施

**修正パターン例:**
```yaml
# 修正前
# MST_SystemConfig テーブル詳細定義
table_name: "MST_UserAuth"

# 修正後  
# MST_UserAuth テーブル詳細定義
table_name: "MST_UserAuth"
```

### 2. 構造標準化（優先度：中）
作成したテンプレート（_TEMPLATE_table_details.yaml）に基づく構造統一

### 3. 継続的品質管理（優先度：中）
- 新規ファイル作成時のテンプレート使用徹底
- レビュー時の構造チェック項目追加

## テンプレート適用ガイド

### 必須セクション
1. ヘッダーコメント（テーブル名一致必須）
2. table_name, logical_name, category
3. revision_history（改版履歴）
4. overview（概要・目的）
5. business_columns（カラム定義）
6. business_indexes（インデックス）
7. business_constraints（制約）
8. foreign_keys（外部キー）
9. sample_data（サンプルデータ）
10. notes（特記事項）
11. business_rules（業務ルール）

### 推奨命名規則
- ファイル名: `[テーブル名]_details.yaml`
- インデックス名: `idx_[テーブル名]_[カラム名]`
- 制約名: `uk_*`, `chk_*`, `fk_*` プレフィックス

## 次のアクション
1. コメント行修正の一括実行
2. 修正後の再チェック実施
3. テンプレート使用ガイドラインの周知
