# データベース整合性チェックレポート

**チェック日時:** 2025-06-06 20:39:32
**対象テーブル数:** 1
**総チェック数:** 25

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

## 📊 結果サマリー

| 重要度 | 件数 | 割合 |
|--------|------|------|
| ⚠️ WARNING | 1 | 4.0% |
| ❌ ERROR | 24 | 96.0% |

### 🎯 総合判定

❌ **修正が必要な問題があります**

重要な問題が検出されました。以下の詳細結果を確認して修正してください。

## 🔍 チェック別統計

| チェック名 | 成功 | 警告 | エラー | 情報 | 合計 |
|------------|------|------|--------|------|------|
| データ型整合性 | 0 | 1 | 24 | 0 | 25 |

## 📋 詳細結果

### 🔍 データ型整合性 (25件)

#### 1. ❌ カラム 'difficulty_level' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** difficulty_level
- **source:** yaml_only

---

#### 2. ❌ カラム 'is_active' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_active
- **source:** yaml_only

---

#### 3. ❌ カラム 'certification_info' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** certification_info
- **source:** yaml_only

---

#### 4. ❌ カラム 'updated_at' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** updated_at
- **source:** yaml_only

---

#### 5. ❌ カラム 'id' のデータ型が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** id
- **ddl_type:** VARCHAR(50
- **yaml_type:** VARCHAR
- **compatibility:** incompatible

---

#### 6. ❌ カラム 'effective_from' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** effective_from
- **source:** yaml_only

---

#### 7. ❌ カラム 'technology_trend' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** technology_trend
- **source:** yaml_only

---

#### 8. ❌ カラム 'market_demand' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** market_demand
- **source:** yaml_only

---

#### 9. ❌ カラム 'evaluation_criteria' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** evaluation_criteria
- **source:** yaml_only

---

#### 10. ❌ カラム 'skill_name_en' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** skill_name_en
- **source:** yaml_only

---

#### 11. ❌ カラム 'skill_type' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** skill_type
- **source:** yaml_only

---

#### 12. ❌ カラム 'category_id' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** category_id
- **source:** yaml_only

---

#### 13. ❌ カラム 'is_core_skill' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_core_skill
- **source:** yaml_only

---

#### 14. ❌ カラム 'description' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** description
- **source:** yaml_only

---

#### 15. ❌ カラム 'created_at' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** created_at
- **source:** yaml_only

---

#### 16. ❌ カラム 'prerequisite_skills' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** prerequisite_skills
- **source:** yaml_only

---

#### 17. ❌ カラム 'learning_resources' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** learning_resources
- **source:** yaml_only

---

#### 18. ❌ カラム 'required_experience_months' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** required_experience_months
- **source:** yaml_only

---

#### 19. ❌ カラム 'is_deleted' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_deleted
- **source:** yaml_only

---

#### 20. ❌ カラム 'display_order' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** display_order
- **source:** yaml_only

---

#### 21. ❌ カラム 'effective_to' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** effective_to
- **source:** yaml_only

---

#### 22. ❌ カラム 'related_skills' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** related_skills
- **source:** yaml_only

---

#### 23. ❌ カラム 'skill_name' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** skill_name
- **source:** yaml_only

---

#### 24. ❌ カラム 'tenant_id' がDDLに存在しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** tenant_id
- **source:** yaml_only

---

#### 25. ⚠️ カラム 'id' の長さ制約定義が片方のみ存在します

**テーブル:** MST_Skill

**詳細情報:**
- **column:** id
- **ddl_length:** None
- **yaml_length:** 50

