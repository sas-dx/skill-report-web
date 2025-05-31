# テーブル定義書：MST_SkillGrade（スキルグレードマスタ）

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_SkillGrade |
| 論理名 | スキルグレードマスタ |
| 用途 | 職種内での習熟度レベルを管理 |
| カテゴリ | マスタ系 |
| 重要度 | 高 |

## テーブル概要

職種内での習熟度レベル（初級、中級、上級、エキスパート等）を管理するマスタテーブル。
スキルグレード別の要件定義、昇格基準、評価基準の設定に使用される。

## カラム定義

| # | カラム名 | データ型 | NULL | デフォルト | 主キー | 外部キー | インデックス | 説明 |
|---|----------|----------|------|------------|--------|----------|--------------|------|
| 1 | tenant_id | VARCHAR(50) | NOT NULL | - | ○ | MST_Tenant.tenant_id | ○ | テナントID |
| 2 | skill_grade_id | VARCHAR(20) | NOT NULL | - | ○ | - | ○ | スキルグレードID |
| 3 | skill_grade_name | VARCHAR(100) | NOT NULL | - | - | - | ○ | スキルグレード名 |
| 4 | skill_grade_code | VARCHAR(10) | NOT NULL | - | - | - | ○ | スキルグレードコード |
| 5 | grade_level | INT | NOT NULL | - | - | - | ○ | グレードレベル（数値） |
| 6 | description | TEXT | NULL | - | - | - | - | グレード説明 |
| 7 | requirements | JSON | NULL | - | - | - | - | 昇格要件 |
| 8 | evaluation_criteria | JSON | NULL | - | - | - | - | 評価基準 |
| 9 | expected_skills | JSON | NULL | - | - | - | - | 期待スキル一覧 |
| 10 | min_experience_years | INT | NULL | 0 | - | - | - | 最低経験年数 |
| 11 | max_experience_years | INT | NULL | - | - | - | - | 最大経験年数 |
| 12 | promotion_criteria | JSON | NULL | - | - | - | - | 昇格基準 |
| 13 | salary_coefficient | DECIMAL(5,2) | NULL | 1.00 | - | - | - | 給与係数 |
| 14 | is_entry_level | BOOLEAN | NOT NULL | FALSE | - | - | ○ | エントリーレベルフラグ |
| 15 | is_active | BOOLEAN | NOT NULL | TRUE | - | - | ○ | 有効フラグ |
| 16 | display_order | INT | NOT NULL | 0 | - | - | ○ | 表示順序 |
| 17 | created_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP | - | - | ○ | 作成日時 |
| 18 | created_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 作成者 |
| 19 | updated_at | TIMESTAMP | NOT NULL | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | - | - | ○ | 更新日時 |
| 20 | updated_by | VARCHAR(50) | NOT NULL | - | - | MST_UserAuth.user_id | - | 更新者 |
| 21 | version | INT | NOT NULL | 1 | - | - | - | バージョン（楽観的排他制御） |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|---------------|------|------------|------|
| PK_MST_SkillGrade | PRIMARY | tenant_id, skill_grade_id | 主キー |
| UK_MST_SkillGrade_Code | UNIQUE | tenant_id, skill_grade_code | スキルグレードコード一意制約 |
| UK_MST_SkillGrade_Name | UNIQUE | tenant_id, skill_grade_name | スキルグレード名一意制約 |
| UK_MST_SkillGrade_Level | UNIQUE | tenant_id, grade_level | グレードレベル一意制約 |
| IX_MST_SkillGrade_Level | INDEX | tenant_id, grade_level | グレードレベル検索用 |
| IX_MST_SkillGrade_Entry | INDEX | tenant_id, is_entry_level | エントリーレベル検索用 |
| IX_MST_SkillGrade_Active | INDEX | tenant_id, is_active | 有効グレード検索用 |
| IX_MST_SkillGrade_Order | INDEX | tenant_id, display_order | 表示順序用 |
| IX_MST_SkillGrade_Created | INDEX | created_at | 作成日時検索用 |
| IX_MST_SkillGrade_Updated | INDEX | updated_at | 更新日時検索用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 条件 | 説明 |
|--------|------|------------|------|------|
| FK_MST_SkillGrade_Tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id | テナント参照制約 |
| FK_MST_SkillGrade_CreatedBy | FOREIGN KEY | created_by | MST_UserAuth.user_id | 作成者参照制約 |
| FK_MST_SkillGrade_UpdatedBy | FOREIGN KEY | updated_by | MST_UserAuth.user_id | 更新者参照制約 |
| CK_MST_SkillGrade_Level | CHECK | grade_level | grade_level >= 1 AND grade_level <= 10 | グレードレベル範囲チェック |
| CK_MST_SkillGrade_Experience | CHECK | min_experience_years, max_experience_years | min_experience_years <= max_experience_years | 経験年数範囲チェック |
| CK_MST_SkillGrade_Coefficient | CHECK | salary_coefficient | salary_coefficient >= 0.5 AND salary_coefficient <= 5.0 | 給与係数範囲チェック |
| CK_MST_SkillGrade_Order | CHECK | display_order | display_order >= 0 | 表示順序正数チェック |

## サンプルデータ

```sql
INSERT INTO MST_SkillGrade VALUES
('tenant001', 'SG001', '初級', 'JUNIOR', 1, '基本的なスキルを習得したレベル', 
 '{"experience": "0-2年", "skills": ["基本知識"], "certifications": []}', 
 '{"technical": 40, "communication": 30, "management": 10}', 
 '["基本的なプログラミング", "基本的なコミュニケーション"]', 0, 2, 
 '{"performance": "基本業務を遂行", "evaluation": "指導の下で業務実行"}', 1.00, TRUE, TRUE, 1, 
 NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'SG002', '中級', 'MIDDLE', 2, '一人前のスキルを持つレベル', 
 '{"experience": "2-5年", "skills": ["応用知識"], "certifications": ["基本情報技術者"]}', 
 '{"technical": 60, "communication": 40, "management": 20}', 
 '["応用プログラミング", "チームワーク", "問題解決"]', 2, 5, 
 '{"performance": "独立して業務遂行", "evaluation": "自律的な業務実行"}', 1.20, FALSE, TRUE, 2, 
 NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'SG003', '上級', 'SENIOR', 3, '高度なスキルを持つレベル', 
 '{"experience": "5-10年", "skills": ["専門知識"], "certifications": ["応用情報技術者"]}', 
 '{"technical": 80, "communication": 60, "management": 40}', 
 '["アーキテクチャ設計", "リーダーシップ", "メンタリング"]', 5, 10, 
 '{"performance": "高度な業務遂行", "evaluation": "他者への指導・支援"}', 1.50, FALSE, TRUE, 3, 
 NOW(), 'admin', NOW(), 'admin', 1),
('tenant001', 'SG004', 'エキスパート', 'EXPERT', 4, '専門分野のエキスパートレベル', 
 '{"experience": "10年以上", "skills": ["エキスパート知識"], "certifications": ["高度情報技術者"]}', 
 '{"technical": 90, "communication": 80, "management": 60}', 
 '["技術戦略立案", "組織運営", "イノベーション創出"]', 10, 20, 
 '{"performance": "戦略的業務遂行", "evaluation": "組織全体への貢献"}', 2.00, FALSE, TRUE, 4, 
 NOW(), 'admin', NOW(), 'admin', 1);
```

## 業務ルール

### 基本ルール
1. **テナント分離**: 全ての操作はテナント単位で実行される
2. **グレードコード一意性**: 同一テナント内でスキルグレードコードは一意である
3. **グレード名一意性**: 同一テナント内でスキルグレード名は一意である
4. **グレードレベル一意性**: 同一テナント内でグレードレベルは一意である
5. **有効性管理**: 無効化されたスキルグレードは新規割り当て不可

### データ整合性
1. **グレードレベル範囲**: 1-10の範囲内で設定
2. **経験年数範囲**: 最低経験年数 ≤ 最大経験年数
3. **給与係数範囲**: 0.5-5.0の範囲内で設定
4. **表示順序**: 0以上の整数値
5. **JSON形式**: requirements、evaluation_criteria、expected_skills、promotion_criteriaは有効なJSON形式

### 運用ルール
1. **論理削除**: 物理削除は行わず、is_activeフラグで管理
2. **履歴管理**: 更新時は監査ログに記録
3. **バージョン管理**: 楽観的排他制御でデータ整合性を保証
4. **エントリーレベル**: テナント内で1つのエントリーレベルグレードを設定

## 関連テーブル

### 参照元テーブル
- MST_JobTypeSkillGrade（職種スキルグレード関連）
- MST_SkillGradeRequirement（スキルグレード要件）
- MST_CertificationRequirement（資格要件マスタ）
- TRN_SkillRecord（スキル評価記録）

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_UserAuth（ユーザー認証情報）

## パフォーマンス考慮事項

### 推奨事項
1. **インデックス活用**: グレードレベル、エントリーレベル、有効フラグでの検索が多いため適切なインデックスを設定
2. **JSON検索**: requirements等のJSON検索時はMySQLのJSON関数を活用
3. **キャッシュ戦略**: スキルグレードマスタは更新頻度が低いためアプリケーションレベルでキャッシュ推奨

### 注意事項
1. **JSON型制限**: MySQLバージョンによるJSON型サポート確認が必要
2. **文字エンコーディング**: UTF-8対応で多言語グレード名に対応
3. **インデックスサイズ**: 大量テナント環境では複合インデックスサイズに注意

## セキュリティ考慮事項

### アクセス制御
1. **テナント分離**: 必ずテナントIDでの絞り込みを実装
2. **権限チェック**: スキルグレード管理権限を持つユーザーのみ更新可能
3. **監査ログ**: 全ての変更操作を監査ログに記録

### データ保護
1. **機密情報**: 給与係数等の機密情報は適切な権限管理
2. **暗号化**: 必要に応じてアプリケーションレベルでの暗号化
3. **バックアップ**: 定期的なバックアップとリストア手順の確立

## 運用上の注意

### メンテナンス
1. **定期見直し**: スキルグレード体系の変更に応じた定期的な見直し
2. **データクリーンアップ**: 無効スキルグレードの定期的なアーカイブ
3. **パフォーマンス監視**: JSON検索のパフォーマンス監視

### 障害対応
1. **整合性チェック**: 関連テーブルとの整合性定期チェック
2. **復旧手順**: データ破損時の復旧手順書整備
3. **ロールバック**: 更新失敗時のロールバック手順確立

### 昇格管理
1. **昇格基準**: 明確な昇格基準の設定と運用
2. **評価プロセス**: 定期的な評価プロセスの実施
3. **フィードバック**: 昇格要件に対する進捗フィードバック
