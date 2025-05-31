# テーブル定義書：MST_SkillGradeRequirement（スキルグレード要件）

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_SkillGradeRequirement |
| 論理名 | スキルグレード要件 |
| 用途 | スキルグレード別の詳細要件を管理 |
| カテゴリ | マスタ系 |
| 重要度 | 高 |

## テーブル概要

スキルグレード別の詳細要件（スキル、経験、成果等）を管理するマスタテーブル。
スキルグレード昇格時の具体的な要件定義、評価基準の設定に使用される。

## カラム定義

| # | カラム名 | データ型 | NULL | デフォルト | 主キー | 外部キー | インデックス | 説明 |
|---|----------|----------|------|------------|--------|----------|--------------|------|
| 1 | tenant_id | VARCHAR(50) | NOT NULL | - | ○ | MST_Tenant.tenant_id | ○ | テナントID |
| 2 | skill_grade_requirement_id | VARCHAR(20) | NOT NULL | - | ○ | - | ○ | スキルグレード要件ID |
| 3 | skill_grade_id | VARCHAR(20) | NOT NULL | - | - | MST_SkillGrade.skill_grade_id | ○ | スキルグレードID |
| 4 | requirement_type | VARCHAR(20) | NOT NULL | - | - | - | ○ | 要件種別（SKILL/EXPERIENCE/PERFORMANCE/CERTIFICATION） |
| 5 | requirement_category | VARCHAR(50) | NOT NULL | - | - | - | ○ | 要件カテゴリ |
| 6 | requirement_name | VARCHAR(100) | NOT NULL | - | - | - | ○ | 要件名 |
| 7 | requirement_description | TEXT | NULL | - | - | - | - | 要件説明 |
| 8 | target_skill_id | VARCHAR(20) | NULL | - | - | MST_SkillItem.skill_item_id | ○ | 対象スキルID |
| 9 | target_certification_id | VARCHAR(20) | NULL | - | - | MST_Certification.certification_id | ○ | 対象資格ID |
| 10 | required_level | INT | NULL | - | - | - | ○ | 必要レベル（1-5） |
| 11 | required_score | DECIMAL(5,2) | NULL | - | - | - | - | 必要スコア |
| 12 | required_experience_months | INT | NULL | - | - | - | - | 必要経験月数 |
| 13 | required_project_count | INT | NULL | - | - | - | - | 必要プロジェクト数 |
| 14 | evaluation_criteria | JSON | NULL | - | - | - | - | 評価基準 |
| 15 | measurement_method | VARCHAR(100) | NULL | - | - | - | - | 測定方法 |
| 16 | evidence_requirements | JSON | NULL | - | - | - | - | 証跡要件 |
| 17 | weight | DECIMAL(5,2) | NOT NULL | 1.00 | - | - | - | 重み |
| 18 | is_mandatory | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 必須フラグ |
| 19 | priority | INT | NOT NULL | 1 | - | - | ○ | 優先度（1-10） |
| 20 | effective_from | DATE | NOT NULL | - | - | - | ○ | 有効開始日 |
| 21 | effective_to | DATE | NULL | - | - | - | ○ | 有効終了日 |
| 22 | is_active | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 有効フラグ |
| 23 | created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | - | - | ○ | 作成日時 |
| 24 | created_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 作成者 |
| 25 | updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | ○ | 更新日時 |
| 26 | updated_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 更新者 |
| 27 | version | INT | NOT NULL | 1 | - | - | - | バージョン（楽観的排他制御） |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| PK_MST_SkillGradeRequirement | PRIMARY | tenant_id, skill_grade_requirement_id | 主キー |
| UK_MST_SGR_Combination | UNIQUE | tenant_id, skill_grade_id, requirement_type, requirement_category, requirement_name | 組み合わせ一意制約 |
| IX_MST_SGR_SkillGrade | INDEX | tenant_id, skill_grade_id | スキルグレード別検索用 |
| IX_MST_SGR_Type | INDEX | tenant_id, requirement_type | 要件種別検索用 |
| IX_MST_SGR_Category | INDEX | tenant_id, requirement_category | 要件カテゴリ検索用 |
| IX_MST_SGR_Skill | INDEX | tenant_id, target_skill_id | 対象スキル検索用 |
| IX_MST_SGR_Certification | INDEX | tenant_id, target_certification_id | 対象資格検索用 |
| IX_MST_SGR_Level | INDEX | tenant_id, required_level | 必要レベル検索用 |
| IX_MST_SGR_Mandatory | INDEX | tenant_id, is_mandatory | 必須要件検索用 |
| IX_MST_SGR_Priority | INDEX | tenant_id, priority | 優先度検索用 |
| IX_MST_SGR_Effective | INDEX | tenant_id, effective_from, effective_to | 有効期間検索用 |
| IX_MST_SGR_Active | INDEX | tenant_id, is_active | 有効検索用 |
| IX_MST_SGR_Created | INDEX | created_at | 作成日時検索用 |
| IX_MST_SGR_Updated | INDEX | updated_at | 更新日時検索用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 条件 | 説明 |
|--------|------|------------|------|------|
| FK_MST_SGR_Tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id | テナント参照制約 |
| FK_MST_SGR_SkillGrade | FOREIGN KEY | skill_grade_id | MST_SkillGrade.skill_grade_id | スキルグレード参照制約 |
| FK_MST_SGR_Skill | FOREIGN KEY | target_skill_id | MST_SkillItem.skill_item_id | 対象スキル参照制約 |
| FK_MST_SGR_Certification | FOREIGN KEY | target_certification_id | MST_Certification.certification_id | 対象資格参照制約 |
| FK_MST_SGR_CreatedBy | FOREIGN KEY | created_by | MST_UserAuth.user_id | 作成者参照制約 |
| FK_MST_SGR_UpdatedBy | FOREIGN KEY | updated_by | MST_UserAuth.user_id | 更新者参照制約 |
| CK_MST_SGR_Type | CHECK | requirement_type | requirement_type IN ('SKILL', 'EXPERIENCE', 'PERFORMANCE', 'CERTIFICATION') | 要件種別チェック |
| CK_MST_SGR_Level | CHECK | required_level | required_level >= 1 AND required_level <= 5 | 必要レベル範囲チェック |
| CK_MST_SGR_Score | CHECK | required_score | required_score >= 0.0 AND required_score <= 100.0 | 必要スコア範囲チェック |
| CK_MST_SGR_Weight | CHECK | weight | weight >= 0.0 AND weight <= 10.0 | 重み範囲チェック |
| CK_MST_SGR_Priority | CHECK | priority | priority >= 1 AND priority <= 10 | 優先度範囲チェック |
| CK_MST_SGR_Experience | CHECK | required_experience_months | required_experience_months > 0 | 必要経験月数正数チェック |
| CK_MST_SGR_Project | CHECK | required_project_count | required_project_count > 0 | 必要プロジェクト数正数チェック |
| CK_MST_SGR_Effective | CHECK | effective_from, effective_to | effective_to IS NULL OR effective_from <= effective_to | 有効期間チェック |

## サンプルデータ

```sql
INSERT INTO MST_SkillGradeRequirement VALUES
('tenant001', 'SGR001', 'SG002', 'SKILL', 'プログラミング', 'Java中級スキル', 
 'Javaでの業務アプリケーション開発が可能なレベル', 'SKILL001', NULL, 3, 75.0, NULL, NULL, 
 '{"evaluation": "実技テスト", "criteria": "設計から実装まで独立して実行"}', 
 '実技テスト・プロジェクト実績', '["プロジェクト成果物", "コードレビュー結果"]', 2.00, TRUE, 1, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'SGR002', 'SG002', 'CERTIFICATION', '技術資格', '基本情報技術者', 
 'IT基礎知識の証明として基本情報技術者の取得', NULL, 'CERT001', NULL, NULL, NULL, NULL, 
 '{"evaluation": "資格取得", "criteria": "合格証明書の提出"}', 
 '資格取得', '["合格証明書"]', 1.50, TRUE, 2, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'SGR003', 'SG002', 'EXPERIENCE', 'プロジェクト経験', '開発プロジェクト経験', 
 '開発プロジェクトでの実務経験', NULL, NULL, NULL, NULL, 24, 2, 
 '{"evaluation": "プロジェクト実績", "criteria": "2年以上かつ2プロジェクト以上"}', 
 'プロジェクト実績評価', '["プロジェクト完了報告書", "成果物"]', 1.80, TRUE, 3, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'SGR004', 'SG002', 'PERFORMANCE', 'コミュニケーション', 'チームワーク', 
 'チーム内での効果的なコミュニケーション能力', NULL, NULL, 3, 70.0, NULL, NULL, 
 '{"evaluation": "360度評価", "criteria": "チームメンバーからの評価"}', 
 '360度評価', '["評価シート", "フィードバック"]', 1.20, FALSE, 4, 
 '2024-01-01', NULL, TRUE, NOW(), 'admin', NOW(), 'admin', 1);
```

## 業務ルール

### 基本ルール
1. **テナント分離**: 全ての操作はテナント単位で実行される
2. **組み合わせ一意性**: 同一テナント内でスキルグレード・要件種別・カテゴリ・要件名の組み合わせは一意である
3. **必須要件**: 必須フラグがTRUEの要件は昇格時に必須チェック
4. **有効性管理**: 無効化された要件は評価対象外

### データ整合性
1. **要件種別**: SKILL（スキル）、EXPERIENCE（経験）、PERFORMANCE（成果）、CERTIFICATION（資格）のいずれか
2. **必要レベル**: 1-5の範囲内で設定
3. **必要スコア**: 0.0-100.0の範囲内で設定
4. **重み**: 0.0-10.0の範囲内で設定
5. **優先度**: 1-10の範囲内で設定
6. **有効期間**: 有効開始日 ≤ 有効終了日
7. **JSON形式**: evaluation_criteria、evidence_requirementsは有効なJSON形式

### 運用ルール
1. **論理削除**: 物理削除は行わず、is_activeフラグで管理
2. **履歴管理**: 更新時は監査ログに記録
3. **バージョン管理**: 楽観的排他制御でデータ整合性を保証
4. **要件評価**: 重みと優先度に基づく総合評価

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_SkillGrade（スキルグレードマスタ）
- MST_SkillItem（スキル項目マスタ）
- MST_Certification（資格情報）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- TRN_SkillRecord（スキル評価記録）- 要件チェック用

## パフォーマンス考慮事項

### 推奨事項
1. **インデックス活用**: スキルグレード・要件種別・必須フラグでの検索が多いため適切なインデックスを設定
2. **JSON検索**: evaluation_criteria等のJSON検索時はMySQLのJSON関数を活用
3. **キャッシュ戦略**: スキルグレード要件は更新頻度が低いためキャッシュ推奨

### 注意事項
1. **JSON型制限**: MySQLバージョンによるJSON型サポート確認が必要
2. **複合検索**: 複数条件での検索時のパフォーマンス監視
3. **インデックスサイズ**: 大量テナント環境では複合インデックスサイズに注意

## セキュリティ考慮事項

### アクセス制御
1. **テナント分離**: 必ずテナントIDでの絞り込みを実装
2. **権限チェック**: スキルグレード要件管理権限を持つユーザーのみ更新可能
3. **監査ログ**: 全ての変更操作を監査ログに記録

### データ保護
1. **機密情報**: 評価基準等の機密情報は適切な権限管理
2. **暗号化**: 必要に応じてアプリケーションレベルでの暗号化
3. **バックアップ**: 定期的なバックアップとリストア手順の確立

## 運用上の注意

### メンテナンス
1. **定期見直し**: スキルグレード要件の定期的な見直し
2. **要件更新**: 技術進歩に応じた要件の更新
3. **パフォーマンス監視**: JSON検索のパフォーマンス監視

### 障害対応
1. **整合性チェック**: 関連テーブルとの整合性定期チェック
2. **復旧手順**: データ破損時の復旧手順書整備
3. **ロールバック**: 更新失敗時のロールバック手順確立

### 要件管理
1. **明確化**: 要件の明確化と具体的な測定方法の定義
2. **証跡管理**: 要件達成の証跡管理
3. **評価基準**: 公平で客観的な評価基準の設定
4. **フィードバック**: 要件達成状況のフィードバック

## 使用例

### スキルグレード別必須要件取得
```sql
SELECT sgr.*, si.skill_item_name, c.certification_name
FROM MST_SkillGradeRequirement sgr
LEFT JOIN MST_SkillItem si ON sgr.target_skill_id = si.skill_item_id
LEFT JOIN MST_Certification c ON sgr.target_certification_id = c.certification_id
WHERE sgr.tenant_id = 'tenant001' 
  AND sgr.skill_grade_id = 'SG002'
  AND sgr.is_mandatory = TRUE
  AND sgr.is_active = TRUE
  AND (sgr.effective_to IS NULL OR sgr.effective_to >= CURDATE())
ORDER BY sgr.priority, sgr.requirement_type;
```

### 要件種別別要件取得
```sql
SELECT sgr.*, sg.skill_grade_name
FROM MST_SkillGradeRequirement sgr
JOIN MST_SkillGrade sg ON sgr.skill_grade_id = sg.skill_grade_id
WHERE sgr.tenant_id = 'tenant001' 
  AND sgr.requirement_type = 'SKILL'
  AND sgr.is_active = TRUE
ORDER BY sg.grade_level, sgr.priority;
