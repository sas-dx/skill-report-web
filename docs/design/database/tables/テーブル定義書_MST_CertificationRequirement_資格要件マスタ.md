# テーブル定義書：MST_CertificationRequirement（資格要件マスタ）

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_CertificationRequirement |
| 論理名 | 資格要件マスタ |
| 用途 | 職種・グレード・スキル別の資格要件を管理 |
| カテゴリ | マスタ系 |
| 重要度 | 高 |

## テーブル概要

職種・スキルグレード・スキル別の資格要件（必須/推奨/任意）を管理するマスタテーブル。
動的な資格要件設定により、柔軟な人事・スキル管理システムを実現する。

## カラム定義

| # | カラム名 | データ型 | NULL | デフォルト | 主キー | 外部キー | インデックス | 説明 |
|---|----------|----------|------|------------|--------|----------|--------------|------|
| 1 | tenant_id | VARCHAR(50) | NOT NULL | - | ○ | MST_Tenant.tenant_id | ○ | テナントID |
| 2 | requirement_id | VARCHAR(20) | NOT NULL | - | ○ | - | ○ | 資格要件ID |
| 3 | job_type_id | VARCHAR(20) | NULL | - | - | MST_JobType.job_type_id | ○ | 職種ID |
| 4 | skill_grade_id | VARCHAR(20) | NULL | - | - | MST_SkillGrade.skill_grade_id | ○ | スキルグレードID |
| 5 | skill_item_id | VARCHAR(20) | NULL | - | - | MST_SkillItem.skill_item_id | ○ | スキル項目ID |
| 6 | certification_id | VARCHAR(20) | NOT NULL | - | - | MST_Certification.certification_id | ○ | 資格ID |
| 7 | requirement_type | VARCHAR(20) | NOT NULL | - | - | - | ○ | 要件種別（REQUIRED/RECOMMENDED/OPTIONAL） |
| 8 | priority | INT | NOT NULL | 1 | - | - | ○ | 優先度（1-10） |
| 9 | description | TEXT | NULL | - | - | - | - | 要件説明 |
| 10 | conditions | JSON | NULL | - | - | - | - | 取得条件 |
| 11 | deadline_months | INT | NULL | - | - | - | - | 取得期限（月数） |
| 12 | alternative_certifications | JSON | NULL | - | - | - | - | 代替資格一覧 |
| 13 | exemption_conditions | JSON | NULL | - | - | - | - | 免除条件 |
| 14 | evaluation_weight | DECIMAL(5,2) | NULL | 1.00 | - | - | - | 評価重み |
| 15 | effective_from | DATE | NOT NULL | - | - | - | ○ | 有効開始日 |
| 16 | effective_to | DATE | NULL | - | - | - | ○ | 有効終了日 |
| 17 | is_active | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 有効フラグ |
| 18 | created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | - | - | ○ | 作成日時 |
| 19 | created_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 作成者 |
| 20 | updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | ○ | 更新日時 |
| 21 | updated_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 更新者 |
| 22 | version | INT | NOT NULL | 1 | - | - | - | バージョン（楽観的排他制御） |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| PK_MST_CertificationRequirement | PRIMARY | tenant_id, requirement_id | 主キー |
| UK_MST_CertReq_Combination | UNIQUE | tenant_id, job_type_id, skill_grade_id, skill_item_id, certification_id | 組み合わせ一意制約 |
| IX_MST_CertReq_JobType | INDEX | tenant_id, job_type_id | 職種別検索用 |
| IX_MST_CertReq_SkillGrade | INDEX | tenant_id, skill_grade_id | スキルグレード別検索用 |
| IX_MST_CertReq_SkillItem | INDEX | tenant_id, skill_item_id | スキル項目別検索用 |
| IX_MST_CertReq_Certification | INDEX | tenant_id, certification_id | 資格別検索用 |
| IX_MST_CertReq_Type | INDEX | tenant_id, requirement_type | 要件種別検索用 |
| IX_MST_CertReq_Priority | INDEX | tenant_id, priority | 優先度検索用 |
| IX_MST_CertReq_Effective | INDEX | tenant_id, effective_from, effective_to | 有効期間検索用 |
| IX_MST_CertReq_Active | INDEX | tenant_id, is_active | 有効要件検索用 |
| IX_MST_CertReq_Created | INDEX | created_at | 作成日時検索用 |
| IX_MST_CertReq_Updated | INDEX | updated_at | 更新日時検索用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 条件 | 説明 |
|--------|------|------------|------|------|
| FK_MST_CertReq_Tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id | テナント参照制約 |
| FK_MST_CertReq_JobType | FOREIGN KEY | job_type_id | MST_JobType.job_type_id | 職種参照制約 |
| FK_MST_CertReq_SkillGrade | FOREIGN KEY | skill_grade_id | MST_SkillGrade.skill_grade_id | スキルグレード参照制約 |
| FK_MST_CertReq_SkillItem | FOREIGN KEY | skill_item_id | MST_SkillItem.skill_item_id | スキル項目参照制約 |
| FK_MST_CertReq_Certification | FOREIGN KEY | certification_id | MST_Certification.certification_id | 資格参照制約 |
| FK_MST_CertReq_CreatedBy | FOREIGN KEY | created_by | MST_UserAuth.user_id | 作成者参照制約 |
| FK_MST_CertReq_UpdatedBy | FOREIGN KEY | updated_by | MST_UserAuth.user_id | 更新者参照制約 |
| CK_MST_CertReq_Type | CHECK | requirement_type | requirement_type IN ('REQUIRED', 'RECOMMENDED', 'OPTIONAL') | 要件種別チェック |
| CK_MST_CertReq_Priority | CHECK | priority | priority >= 1 AND priority <= 10 | 優先度範囲チェック |
| CK_MST_CertReq_Weight | CHECK | evaluation_weight | evaluation_weight >= 0.0 AND evaluation_weight <= 10.0 | 評価重み範囲チェック |
| CK_MST_CertReq_Deadline | CHECK | deadline_months | deadline_months > 0 | 取得期限正数チェック |
| CK_MST_CertReq_Effective | CHECK | effective_from, effective_to | effective_to IS NULL OR effective_from <= effective_to | 有効期間チェック |
| CK_MST_CertReq_Scope | CHECK | job_type_id, skill_grade_id, skill_item_id | NOT (job_type_id IS NULL AND skill_grade_id IS NULL AND skill_item_id IS NULL) | 適用範囲必須チェック |

## サンプルデータ

```sql
INSERT INTO MST_CertificationRequirement VALUES
('tenant001', 'CR001', 'JOB001', 'SG002', NULL, 'CERT001', 'REQUIRED', 1, 
 'システムエンジニア中級には基本情報技術者が必須', 
 '{"experience_years": 2, "skill_level": "intermediate"}', 12, 
 '["CERT002", "CERT003"]', '{"experience_years": 5}', 2.00, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'CR002', 'JOB001', 'SG003', NULL, 'CERT002', 'REQUIRED', 1, 
 'システムエンジニア上級には応用情報技術者が必須', 
 '{"experience_years": 5, "skill_level": "advanced"}', 24, 
 '["CERT004", "CERT005"]', '{"experience_years": 10}', 3.00, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'CR003', 'JOB002', 'SG002', NULL, 'CERT006', 'RECOMMENDED', 2, 
 '営業中級には営業士検定が推奨', 
 '{"experience_years": 2, "sales_performance": "target_achievement"}', 18, 
 '["CERT007"]', '{"sales_years": 5}', 1.50, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'CR004', NULL, NULL, 'SKILL001', 'CERT008', 'OPTIONAL', 3, 
 'Javaスキルには Oracle Java認定が任意', 
 '{"skill_level": "intermediate"}', NULL, 
 '["CERT009", "CERT010"]', '{"experience_years": 3}', 1.00, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1);
```

## 業務ルール

### 基本ルール
1. **テナント分離**: 全ての操作はテナント単位で実行される
2. **組み合わせ一意性**: 同一テナント内で職種・スキルグレード・スキル項目・資格の組み合わせは一意である
3. **適用範囲必須**: 職種・スキルグレード・スキル項目のいずれかは必須指定
4. **有効性管理**: 無効化された資格要件は評価対象外

### データ整合性
1. **要件種別**: REQUIRED（必須）、RECOMMENDED（推奨）、OPTIONAL（任意）のいずれか
2. **優先度範囲**: 1-10の範囲内で設定
3. **評価重み範囲**: 0.0-10.0の範囲内で設定
4. **有効期間**: 有効開始日 ≤ 有効終了日
5. **JSON形式**: conditions、alternative_certifications、exemption_conditionsは有効なJSON形式

### 運用ルール
1. **論理削除**: 物理削除は行わず、is_activeフラグで管理
2. **履歴管理**: 更新時は監査ログに記録
3. **バージョン管理**: 楽観的排他制御でデータ整合性を保証
4. **有効期間管理**: 期間限定の資格要件設定が可能

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_JobType（職種マスタ）
- MST_SkillGrade（スキルグレードマスタ）
- MST_SkillItem（スキル項目マスタ）
- MST_Certification（資格情報）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- TRN_SkillRecord（スキル評価記録）- 資格要件チェック用

## パフォーマンス考慮事項

### 推奨事項
1. **インデックス活用**: 職種・スキルグレード・スキル項目・資格での検索が多いため適切なインデックスを設定
2. **JSON検索**: conditions等のJSON検索時はMySQLのJSON関数を活用
3. **キャッシュ戦略**: 資格要件マスタは更新頻度が低いためアプリケーションレベルでキャッシュ推奨
4. **有効期間フィルタ**: 現在有効な要件のみを取得するクエリ最適化

### 注意事項
1. **JSON型制限**: MySQLバージョンによるJSON型サポート確認が必要
2. **複合検索**: 複数条件での検索時のパフォーマンス監視
3. **インデックスサイズ**: 大量テナント環境では複合インデックスサイズに注意

## セキュリティ考慮事項

### アクセス制御
1. **テナント分離**: 必ずテナントIDでの絞り込みを実装
2. **権限チェック**: 資格要件管理権限を持つユーザーのみ更新可能
3. **監査ログ**: 全ての変更操作を監査ログに記録

### データ保護
1. **機密情報**: 評価重み等の機密情報は適切な権限管理
2. **暗号化**: 必要に応じてアプリケーションレベルでの暗号化
3. **バックアップ**: 定期的なバックアップとリストア手順の確立

## 運用上の注意

### メンテナンス
1. **定期見直し**: 資格要件の変更に応じた定期的な見直し
2. **有効期間管理**: 期限切れ要件の定期的なチェックと更新
3. **パフォーマンス監視**: JSON検索のパフォーマンス監視

### 障害対応
1. **整合性チェック**: 関連テーブルとの整合性定期チェック
2. **復旧手順**: データ破損時の復旧手順書整備
3. **ロールバック**: 更新失敗時のロールバック手順確立

### 要件管理
1. **動的設定**: 柔軟な資格要件設定と変更対応
2. **代替資格**: 代替資格の適切な管理と評価
3. **免除条件**: 免除条件の明確化と適用基準
4. **評価連携**: スキル評価システムとの連携強化

## 使用例

### 職種別必須資格の取得
```sql
SELECT cr.*, c.certification_name 
FROM MST_CertificationRequirement cr
JOIN MST_Certification c ON cr.certification_id = c.certification_id
WHERE cr.tenant_id = 'tenant001' 
  AND cr.job_type_id = 'JOB001'
  AND cr.requirement_type = 'REQUIRED'
  AND cr.is_active = TRUE
  AND (cr.effective_to IS NULL OR cr.effective_to >= CURDATE());
```

### スキルグレード別推奨資格の取得
```sql
SELECT cr.*, c.certification_name 
FROM MST_CertificationRequirement cr
JOIN MST_Certification c ON cr.certification_id = c.certification_id
WHERE cr.tenant_id = 'tenant001' 
  AND cr.skill_grade_id = 'SG002'
  AND cr.requirement_type = 'RECOMMENDED'
  AND cr.is_active = TRUE
ORDER BY cr.priority;
