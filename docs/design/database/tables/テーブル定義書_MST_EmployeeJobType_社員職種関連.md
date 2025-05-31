# テーブル定義書：MST_EmployeeJobType（社員職種関連）

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_EmployeeJobType |
| 論理名 | 社員職種関連 |
| 用途 | 社員と職種の紐付けを管理 |
| カテゴリ | マスタ系 |
| 重要度 | 最高 |

## テーブル概要

社員と職種の紐付け関係を管理するマスタテーブル。
社員の現在の職種、過去の職種履歴、職種変更の管理に使用される。

## カラム定義

| # | カラム名 | データ型 | NULL | デフォルト | 主キー | 外部キー | インデックス | 説明 |
|---|----------|----------|------|------------|--------|----------|--------------|------|
| 1 | tenant_id | VARCHAR(50) | NOT NULL | - | ○ | MST_Tenant.tenant_id | ○ | テナントID |
| 2 | employee_job_type_id | VARCHAR(20) | NOT NULL | - | ○ | - | ○ | 社員職種関連ID |
| 3 | employee_id | VARCHAR(20) | NOT NULL | - | - | MST_Employee.employee_id | ○ | 社員ID |
| 4 | job_type_id | VARCHAR(20) | NOT NULL | - | - | MST_JobType.job_type_id | ○ | 職種ID |
| 5 | skill_grade_id | VARCHAR(20) | NULL | - | - | MST_SkillGrade.skill_grade_id | ○ | 現在のスキルグレードID |
| 6 | assignment_type | VARCHAR(20) | NOT NULL | 'PRIMARY' | - | - | ○ | 割り当て種別（PRIMARY/SECONDARY/TEMPORARY） |
| 7 | start_date | DATE | NOT NULL | - | - | - | ○ | 開始日 |
| 8 | end_date | DATE | NULL | - | - | - | ○ | 終了日 |
| 9 | assignment_reason | VARCHAR(100) | NULL | - | - | - | - | 割り当て理由 |
| 10 | assignment_percentage | DECIMAL(5,2) | NULL | 100.00 | - | - | - | 割り当て比率（%） |
| 11 | reporting_manager_id | VARCHAR(20) | NULL | - | - | MST_Employee.employee_id | ○ | 報告先マネージャーID |
| 12 | target_grade_id | VARCHAR(20) | NULL | - | - | MST_SkillGrade.skill_grade_id | ○ | 目標スキルグレードID |
| 13 | promotion_target_date | DATE | NULL | - | - | - | ○ | 昇格目標日 |
| 14 | evaluation_cycle | VARCHAR(20) | NULL | 'ANNUAL' | - | - | - | 評価サイクル（MONTHLY/QUARTERLY/ANNUAL） |
| 15 | notes | TEXT | NULL | - | - | - | - | 備考 |
| 16 | is_current | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 現在有効フラグ |
| 17 | is_active | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 有効フラグ |
| 18 | created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | - | - | ○ | 作成日時 |
| 19 | created_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 作成者 |
| 20 | updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | ○ | 更新日時 |
| 21 | updated_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 更新者 |
| 22 | version | INT | NOT NULL | 1 | - | - | - | バージョン（楽観的排他制御） |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| PK_MST_EmployeeJobType | PRIMARY | tenant_id, employee_job_type_id | 主キー |
| UK_MST_EmpJobType_Current | UNIQUE | tenant_id, employee_id, assignment_type, is_current | 現在割り当て一意制約 |
| IX_MST_EmpJobType_Employee | INDEX | tenant_id, employee_id | 社員別検索用 |
| IX_MST_EmpJobType_JobType | INDEX | tenant_id, job_type_id | 職種別検索用 |
| IX_MST_EmpJobType_SkillGrade | INDEX | tenant_id, skill_grade_id | スキルグレード別検索用 |
| IX_MST_EmpJobType_Manager | INDEX | tenant_id, reporting_manager_id | マネージャー別検索用 |
| IX_MST_EmpJobType_Type | INDEX | tenant_id, assignment_type | 割り当て種別検索用 |
| IX_MST_EmpJobType_Period | INDEX | tenant_id, start_date, end_date | 期間検索用 |
| IX_MST_EmpJobType_Current | INDEX | tenant_id, is_current | 現在有効検索用 |
| IX_MST_EmpJobType_Active | INDEX | tenant_id, is_active | 有効検索用 |
| IX_MST_EmpJobType_Promotion | INDEX | tenant_id, promotion_target_date | 昇格目標日検索用 |
| IX_MST_EmpJobType_Created | INDEX | created_at | 作成日時検索用 |
| IX_MST_EmpJobType_Updated | INDEX | updated_at | 更新日時検索用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 条件 | 説明 |
|--------|------|------------|------|------|
| FK_MST_EmpJobType_Tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id | テナント参照制約 |
| FK_MST_EmpJobType_Employee | FOREIGN KEY | employee_id | MST_Employee.employee_id | 社員参照制約 |
| FK_MST_EmpJobType_JobType | FOREIGN KEY | job_type_id | MST_JobType.job_type_id | 職種参照制約 |
| FK_MST_EmpJobType_SkillGrade | FOREIGN KEY | skill_grade_id | MST_SkillGrade.skill_grade_id | スキルグレード参照制約 |
| FK_MST_EmpJobType_Manager | FOREIGN KEY | reporting_manager_id | MST_Employee.employee_id | マネージャー参照制約 |
| FK_MST_EmpJobType_TargetGrade | FOREIGN KEY | target_grade_id | MST_SkillGrade.skill_grade_id | 目標グレード参照制約 |
| FK_MST_EmpJobType_CreatedBy | FOREIGN KEY | created_by | MST_UserAuth.user_id | 作成者参照制約 |
| FK_MST_EmpJobType_UpdatedBy | FOREIGN KEY | updated_by | MST_UserAuth.user_id | 更新者参照制約 |
| CK_MST_EmpJobType_AssignType | CHECK | assignment_type | assignment_type IN ('PRIMARY', 'SECONDARY', 'TEMPORARY') | 割り当て種別チェック |
| CK_MST_EmpJobType_Percentage | CHECK | assignment_percentage | assignment_percentage >= 0.0 AND assignment_percentage <= 100.0 | 割り当て比率チェック |
| CK_MST_EmpJobType_Period | CHECK | start_date, end_date | end_date IS NULL OR start_date <= end_date | 期間チェック |
| CK_MST_EmpJobType_EvalCycle | CHECK | evaluation_cycle | evaluation_cycle IN ('MONTHLY', 'QUARTERLY', 'ANNUAL') | 評価サイクルチェック |
| CK_MST_EmpJobType_Current | CHECK | is_current, end_date | NOT (is_current = TRUE AND end_date IS NOT NULL AND end_date < CURDATE()) | 現在有効チェック |

## サンプルデータ

```sql
INSERT INTO MST_EmployeeJobType VALUES
('tenant001', 'EJT001', 'EMP001', 'JOB001', 'SG002', 'PRIMARY', '2024-01-01', NULL, 
 '新卒入社時の職種割り当て', 100.00, 'EMP010', 'SG003', '2025-01-01', 'ANNUAL', 
 'システムエンジニアとして配属', TRUE, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'EJT002', 'EMP002', 'JOB002', 'SG001', 'PRIMARY', '2024-01-01', NULL, 
 '営業部門への配属', 100.00, 'EMP011', 'SG002', '2024-12-01', 'QUARTERLY', 
 '営業職として配属', TRUE, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'EJT003', 'EMP003', 'JOB003', 'SG003', 'PRIMARY', '2024-01-01', NULL, 
 'プロジェクトマネージャーへの昇格', 100.00, 'EMP012', 'SG004', '2025-06-01', 'ANNUAL', 
 'PMとして昇格', TRUE, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'EJT004', 'EMP001', 'JOB002', 'SG001', 'SECONDARY', '2024-06-01', '2024-12-31', 
 '営業支援業務の兼務', 30.00, 'EMP011', NULL, NULL, 'MONTHLY', 
 '技術営業支援として兼務', FALSE, TRUE, NOW(), 'admin', NOW(), 'admin', 1);
```

## 業務ルール

### 基本ルール
1. **テナント分離**: 全ての操作はテナント単位で実行される
2. **現在割り当て一意性**: 同一社員・同一割り当て種別で現在有効な職種は1つのみ
3. **主職種必須**: 全社員は必ずPRIMARY職種を持つ必要がある
4. **有効性管理**: 無効化された職種割り当ては評価対象外

### データ整合性
1. **割り当て種別**: PRIMARY（主職種）、SECONDARY（副職種）、TEMPORARY（一時的）のいずれか
2. **割り当て比率**: 0.0-100.0%の範囲内で設定
3. **期間**: 開始日 ≤ 終了日
4. **現在有効**: 現在有効フラグがTRUEの場合、終了日は未来日または未設定
5. **評価サイクル**: MONTHLY（月次）、QUARTERLY（四半期）、ANNUAL（年次）のいずれか

### 運用ルール
1. **論理削除**: 物理削除は行わず、is_activeフラグで管理
2. **履歴管理**: 更新時は監査ログに記録
3. **バージョン管理**: 楽観的排他制御でデータ整合性を保証
4. **職種変更**: 職種変更時は既存レコードを終了し、新規レコードを作成

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_Employee（社員基本情報）
- MST_JobType（職種マスタ）
- MST_SkillGrade（スキルグレードマスタ）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- TRN_SkillRecord（スキル評価記録）
- TRN_GoalProgress（目標進捗）

## パフォーマンス考慮事項

### 推奨事項
1. **インデックス活用**: 社員・職種・現在有効での検索が多いため適切なインデックスを設定
2. **期間検索最適化**: 有効期間での検索クエリを最適化
3. **キャッシュ戦略**: 現在の職種情報は頻繁にアクセスされるためキャッシュ推奨

### 注意事項
1. **履歴データ**: 職種変更履歴が蓄積されるため定期的なアーカイブ検討
2. **複合検索**: 複数条件での検索時のパフォーマンス監視
3. **インデックスサイズ**: 大量社員環境では複合インデックスサイズに注意

## セキュリティ考慮事項

### アクセス制御
1. **テナント分離**: 必ずテナントIDでの絞り込みを実装
2. **権限チェック**: 職種割り当て権限を持つユーザーのみ更新可能
3. **監査ログ**: 全ての変更操作を監査ログに記録

### データ保護
1. **個人情報**: 社員の職種情報は適切な権限管理
2. **暗号化**: 必要に応じてアプリケーションレベルでの暗号化
3. **バックアップ**: 定期的なバックアップとリストア手順の確立

## 運用上の注意

### メンテナンス
1. **定期見直し**: 職種割り当ての定期的な見直し
2. **履歴管理**: 職種変更履歴の適切な管理
3. **パフォーマンス監視**: 検索クエリのパフォーマンス監視

### 障害対応
1. **整合性チェック**: 関連テーブルとの整合性定期チェック
2. **復旧手順**: データ破損時の復旧手順書整備
3. **ロールバック**: 更新失敗時のロールバック手順確立

### 職種管理
1. **変更管理**: 職種変更時の適切な手順実行
2. **昇格管理**: スキルグレード昇格の管理
3. **兼務管理**: 複数職種兼務時の適切な管理
4. **評価連携**: 職種別評価システムとの連携

## 使用例

### 社員の現在職種取得
```sql
SELECT ejt.*, jt.job_type_name, sg.skill_grade_name
FROM MST_EmployeeJobType ejt
JOIN MST_JobType jt ON ejt.job_type_id = jt.job_type_id
LEFT JOIN MST_SkillGrade sg ON ejt.skill_grade_id = sg.skill_grade_id
WHERE ejt.tenant_id = 'tenant001' 
  AND ejt.employee_id = 'EMP001'
  AND ejt.assignment_type = 'PRIMARY'
  AND ejt.is_current = TRUE
  AND ejt.is_active = TRUE;
```

### 職種別社員一覧取得
```sql
SELECT ejt.*, e.employee_name
FROM MST_EmployeeJobType ejt
JOIN MST_Employee e ON ejt.employee_id = e.employee_id
WHERE ejt.tenant_id = 'tenant001' 
  AND ejt.job_type_id = 'JOB001'
  AND ejt.is_current = TRUE
  AND ejt.is_active = TRUE
ORDER BY ejt.skill_grade_id, e.employee_name;
