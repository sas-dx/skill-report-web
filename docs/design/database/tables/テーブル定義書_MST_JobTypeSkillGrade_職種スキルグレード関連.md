# テーブル定義書：MST_JobTypeSkillGrade（職種スキルグレード関連）

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_JobTypeSkillGrade |
| 論理名 | 職種スキルグレード関連 |
| 用途 | 職種とスキルグレードの紐付けを管理 |
| カテゴリ | マスタ系 |
| 重要度 | 高 |

## テーブル概要

職種とスキルグレードの紐付け関係を管理するマスタテーブル。
職種別に適用可能なスキルグレード、昇格パス、評価基準の設定に使用される。

## カラム定義

| # | カラム名 | データ型 | NULL | デフォルト | 主キー | 外部キー | インデックス | 説明 |
|---|----------|----------|------|------------|--------|----------|--------------|------|
| 1 | tenant_id | VARCHAR(50) | NOT NULL | - | ○ | MST_Tenant.tenant_id | ○ | テナントID |
| 2 | job_type_skill_grade_id | VARCHAR(20) | NOT NULL | - | ○ | - | ○ | 職種スキルグレード関連ID |
| 3 | job_type_id | VARCHAR(20) | NOT NULL | - | - | MST_JobType.job_type_id | ○ | 職種ID |
| 4 | skill_grade_id | VARCHAR(20) | NOT NULL | - | - | MST_SkillGrade.skill_grade_id | ○ | スキルグレードID |
| 5 | is_applicable | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 適用可能フラグ |
| 6 | is_entry_grade | BOOLEAN | NOT NULL | FALSE | - | - | ○ | エントリーグレードフラグ |
| 7 | min_experience_years | INT | NULL | 0 | - | - | - | 最低経験年数 |
| 8 | max_experience_years | INT | NULL | - | - | - | - | 最大経験年数 |
| 9 | promotion_requirements | JSON | NULL | - | - | - | - | 昇格要件 |
| 10 | evaluation_criteria | JSON | NULL | - | - | - | - | 評価基準 |
| 11 | required_skills | JSON | NULL | - | - | - | - | 必要スキル一覧 |
| 12 | next_grade_id | VARCHAR(20) | NULL | - | - | MST_SkillGrade.skill_grade_id | ○ | 次のグレードID |
| 13 | promotion_period_months | INT | NULL | - | - | - | - | 昇格期間（月数） |
| 14 | salary_coefficient | DECIMAL(5,2) | NULL | 1.00 | - | - | - | 給与係数 |
| 15 | performance_weight | DECIMAL(5,2) | NULL | 1.00 | - | - | - | 成果重み |
| 16 | skill_weight | DECIMAL(5,2) | NULL | 1.00 | - | - | - | スキル重み |
| 17 | leadership_weight | DECIMAL(5,2) | NULL | 1.00 | - | - | - | リーダーシップ重み |
| 18 | effective_from | DATE | NOT NULL | - | - | - | ○ | 有効開始日 |
| 19 | effective_to | DATE | NULL | - | - | - | ○ | 有効終了日 |
| 20 | is_active | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 有効フラグ |
| 21 | created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | - | - | ○ | 作成日時 |
| 22 | created_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 作成者 |
| 23 | updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | ○ | 更新日時 |
| 24 | updated_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 更新者 |
| 25 | version | INT | NOT NULL | 1 | - | - | - | バージョン（楽観的排他制御） |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| PK_MST_JobTypeSkillGrade | PRIMARY | tenant_id, job_type_skill_grade_id | 主キー |
| UK_MST_JobTypeSkillGrade | UNIQUE | tenant_id, job_type_id, skill_grade_id | 職種・スキルグレード組み合わせ一意制約 |
| IX_MST_JTSG_JobType | INDEX | tenant_id, job_type_id | 職種別検索用 |
| IX_MST_JTSG_SkillGrade | INDEX | tenant_id, skill_grade_id | スキルグレード別検索用 |
| IX_MST_JTSG_Applicable | INDEX | tenant_id, is_applicable | 適用可能検索用 |
| IX_MST_JTSG_Entry | INDEX | tenant_id, is_entry_grade | エントリーグレード検索用 |
| IX_MST_JTSG_NextGrade | INDEX | tenant_id, next_grade_id | 次グレード検索用 |
| IX_MST_JTSG_Effective | INDEX | tenant_id, effective_from, effective_to | 有効期間検索用 |
| IX_MST_JTSG_Active | INDEX | tenant_id, is_active | 有効検索用 |
| IX_MST_JTSG_Created | INDEX | created_at | 作成日時検索用 |
| IX_MST_JTSG_Updated | INDEX | updated_at | 更新日時検索用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 条件 | 説明 |
|--------|------|------------|------|------|
| FK_MST_JTSG_Tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id | テナント参照制約 |
| FK_MST_JTSG_JobType | FOREIGN KEY | job_type_id | MST_JobType.job_type_id | 職種参照制約 |
| FK_MST_JTSG_SkillGrade | FOREIGN KEY | skill_grade_id | MST_SkillGrade.skill_grade_id | スキルグレード参照制約 |
| FK_MST_JTSG_NextGrade | FOREIGN KEY | next_grade_id | MST_SkillGrade.skill_grade_id | 次グレード参照制約 |
| FK_MST_JTSG_CreatedBy | FOREIGN KEY | created_by | MST_UserAuth.user_id | 作成者参照制約 |
| FK_MST_JTSG_UpdatedBy | FOREIGN KEY | updated_by | MST_UserAuth.user_id | 更新者参照制約 |
| CK_MST_JTSG_Experience | CHECK | min_experience_years, max_experience_years | min_experience_years <= max_experience_years | 経験年数範囲チェック |
| CK_MST_JTSG_Coefficient | CHECK | salary_coefficient | salary_coefficient >= 0.5 AND salary_coefficient <= 5.0 | 給与係数範囲チェック |
| CK_MST_JTSG_Weights | CHECK | performance_weight, skill_weight, leadership_weight | performance_weight >= 0.0 AND skill_weight >= 0.0 AND leadership_weight >= 0.0 | 重み正数チェック |
| CK_MST_JTSG_Effective | CHECK | effective_from, effective_to | effective_to IS NULL OR effective_from <= effective_to | 有効期間チェック |
| CK_MST_JTSG_Promotion | CHECK | promotion_period_months | promotion_period_months > 0 | 昇格期間正数チェック |

## サンプルデータ

```sql
INSERT INTO MST_JobTypeSkillGrade VALUES
('tenant001', 'JTSG001', 'JOB001', 'SG001', TRUE, TRUE, 0, 2, 
 '{"performance": "基本業務遂行", "skills": ["基本プログラミング"], "certifications": []}', 
 '{"technical": 40, "communication": 30, "management": 10}', 
 '["Java基礎", "SQL基礎", "コミュニケーション"]', 'SG002', 24, 1.00, 1.00, 1.00, 0.50, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'JTSG002', 'JOB001', 'SG002', TRUE, FALSE, 2, 5, 
 '{"performance": "独立業務遂行", "skills": ["応用プログラミング"], "certifications": ["基本情報技術者"]}', 
 '{"technical": 60, "communication": 40, "management": 20}', 
 '["Java応用", "設計スキル", "チームワーク"]', 'SG003', 36, 1.20, 1.20, 1.20, 0.80, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'JTSG003', 'JOB001', 'SG003', TRUE, FALSE, 5, 10, 
 '{"performance": "高度業務遂行", "skills": ["アーキテクチャ設計"], "certifications": ["応用情報技術者"]}', 
 '{"technical": 80, "communication": 60, "management": 40}', 
 '["アーキテクチャ", "リーダーシップ", "メンタリング"]', 'SG004', 48, 1.50, 1.50, 1.50, 1.20, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'JTSG004', 'JOB002', 'SG001', TRUE, TRUE, 0, 2, 
 '{"performance": "基本営業活動", "skills": ["営業基礎"], "certifications": []}', 
 '{"sales": 40, "communication": 50, "management": 10}', 
 '["営業基礎", "商品知識", "顧客対応"]', 'SG002', 18, 1.00, 1.00, 1.00, 0.50, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1);
```

## 業務ルール

### 基本ルール
1. **テナント分離**: 全ての操作はテナント単位で実行される
2. **組み合わせ一意性**: 同一テナント内で職種・スキルグレードの組み合わせは一意である
3. **エントリーグレード**: 各職種に1つのエントリーグレードを設定
4. **有効性管理**: 無効化された組み合わせは新規割り当て不可

### データ整合性
1. **経験年数範囲**: 最低経験年数 ≤ 最大経験年数
2. **給与係数範囲**: 0.5-5.0の範囲内で設定
3. **重み**: 各重みは0.0以上の値
4. **有効期間**: 有効開始日 ≤ 有効終了日
5. **JSON形式**: promotion_requirements、evaluation_criteria、required_skillsは有効なJSON形式

### 運用ルール
1. **論理削除**: 物理削除は行わず、is_activeフラグで管理
2. **履歴管理**: 更新時は監査ログに記録
3. **バージョン管理**: 楽観的排他制御でデータ整合性を保証
4. **昇格パス**: 次グレードIDで昇格パスを定義

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_JobType（職種マスタ）
- MST_SkillGrade（スキルグレードマスタ）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- MST_EmployeeJobType（社員職種関連）
- TRN_SkillRecord（スキル評価記録）

## パフォーマンス考慮事項

### 推奨事項
1. **インデックス活用**: 職種・スキルグレード・適用可能での検索が多いため適切なインデックスを設定
2. **JSON検索**: promotion_requirements等のJSON検索時はMySQLのJSON関数を活用
3. **キャッシュ戦略**: 職種スキルグレード関連は更新頻度が低いためキャッシュ推奨

### 注意事項
1. **JSON型制限**: MySQLバージョンによるJSON型サポート確認が必要
2. **複合検索**: 複数条件での検索時のパフォーマンス監視
3. **インデックスサイズ**: 大量テナント環境では複合インデックスサイズに注意

## セキュリティ考慮事項

### アクセス制御
1. **テナント分離**: 必ずテナントIDでの絞り込みを実装
2. **権限チェック**: 職種スキルグレード管理権限を持つユーザーのみ更新可能
3. **監査ログ**: 全ての変更操作を監査ログに記録

### データ保護
1. **機密情報**: 給与係数等の機密情報は適切な権限管理
2. **暗号化**: 必要に応じてアプリケーションレベルでの暗号化
3. **バックアップ**: 定期的なバックアップとリストア手順の確立

## 運用上の注意

### メンテナンス
1. **定期見直し**: 職種スキルグレード体系の定期的な見直し
2. **昇格パス管理**: 昇格パスの適切な設定と管理
3. **パフォーマンス監視**: JSON検索のパフォーマンス監視

### 障害対応
1. **整合性チェック**: 関連テーブルとの整合性定期チェック
2. **復旧手順**: データ破損時の復旧手順書整備
3. **ロールバック**: 更新失敗時のロールバック手順確立

### 昇格管理
1. **昇格基準**: 明確な昇格基準の設定と運用
2. **評価プロセス**: 定期的な評価プロセスの実施
3. **キャリアパス**: 明確なキャリアパスの提示
4. **フィードバック**: 昇格要件に対する進捗フィードバック

## 使用例

### 職種別適用可能スキルグレード取得
```sql
SELECT jtsg.*, sg.skill_grade_name, sg.grade_level
FROM MST_JobTypeSkillGrade jtsg
JOIN MST_SkillGrade sg ON jtsg.skill_grade_id = sg.skill_grade_id
WHERE jtsg.tenant_id = 'tenant001' 
  AND jtsg.job_type_id = 'JOB001'
  AND jtsg.is_applicable = TRUE
  AND jtsg.is_active = TRUE
  AND (jtsg.effective_to IS NULL OR jtsg.effective_to >= CURDATE())
ORDER BY sg.grade_level;
```

### 昇格パス取得
```sql
SELECT jtsg.*, sg.skill_grade_name as current_grade, nsg.skill_grade_name as next_grade
FROM MST_JobTypeSkillGrade jtsg
JOIN MST_SkillGrade sg ON jtsg.skill_grade_id = sg.skill_grade_id
LEFT JOIN MST_SkillGrade nsg ON jtsg.next_grade_id = nsg.skill_grade_id
WHERE jtsg.tenant_id = 'tenant001' 
  AND jtsg.job_type_id = 'JOB001'
  AND jtsg.is_active = TRUE
ORDER BY sg.grade_level;
