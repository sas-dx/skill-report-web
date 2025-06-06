# データベース整合性チェックレポート

**チェック日時:** 2025-06-06 20:44:35
**対象テーブル数:** 1
**総チェック数:** 35

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
| ✅ SUCCESS | 10 | 28.6% |
| ⚠️ WARNING | 24 | 68.6% |
| ❌ ERROR | 1 | 2.9% |

### 🎯 総合判定

❌ **修正が必要な問題があります**

重要な問題が検出されました。以下の詳細結果を確認して修正してください。

## 🔍 チェック別統計

| チェック名 | 成功 | 警告 | エラー | 情報 | 合計 |
|------------|------|------|--------|------|------|
| データ型整合性 | 10 | 24 | 1 | 0 | 35 |

## 📋 詳細結果

### 🔍 データ型整合性 (35件)

#### 1. ❌ カラム 'updated_at' のデータ型が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** updated_at
- **ddl_type:** DATE
- **yaml_type:** TIMESTAMP
- **compatibility:** incompatible

---

#### 2. ⚠️ カラム 'skill_name' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** skill_name
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 3. ⚠️ カラム 'category_id' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** category_id
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 4. ⚠️ カラム 'technology_trend' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** technology_trend
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 5. ⚠️ カラム 'technology_trend' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** technology_trend
- **ddl_default:** STABLE' COMMENT '技術トレンド（EMERGING:新興、GROWING:成長中、STABLE:安定、DECLINING:衰退）
- **yaml_default:** STABLE

---

#### 6. ⚠️ カラム 'skill_type' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** skill_type
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 7. ⚠️ カラム 'skill_type' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** skill_type
- **ddl_default:** TECHNICAL' COMMENT 'スキルの種別（TECHNICAL:技術スキル、BUSINESS:ビジネススキル、SOFT:ソフトスキル、LANGUAGE:言語スキル）
- **yaml_default:** TECHNICAL

---

#### 8. ⚠️ カラム 'is_core_skill' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_core_skill
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 9. ⚠️ カラム 'is_core_skill' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_core_skill
- **ddl_default:** FALSE COMMENT '組織のコアスキルかどうか'
- **yaml_default:** False

---

#### 10. ⚠️ カラム 'created_at' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** created_at
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 11. ⚠️ カラム 'created_at' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** created_at
- **ddl_default:** CURRENT_TIMESTAMP COMMENT '作成日時'
- **yaml_default:** CURRENT_TIMESTAMP

---

#### 12. ⚠️ カラム 'is_deleted' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_deleted
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 13. ⚠️ カラム 'is_deleted' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_deleted
- **ddl_default:** FALSE COMMENT '論理削除フラグ'
- **yaml_default:** False

---

#### 14. ⚠️ カラム 'tenant_id' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** tenant_id
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 15. ⚠️ カラム 'display_order' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** display_order
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 16. ⚠️ カラム 'display_order' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** display_order
- **ddl_default:** 0 COMMENT '同一カテゴリ内での表示順序'
- **yaml_default:** 0

---

#### 17. ⚠️ カラム 'id' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** id
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 18. ⚠️ カラム 'difficulty_level' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** difficulty_level
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 19. ⚠️ カラム 'difficulty_level' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** difficulty_level
- **ddl_default:** 3 COMMENT 'スキルの習得難易度（1:易、2:普通、3:難、4:非常に難、5:最高難度）'
- **yaml_default:** 3

---

#### 20. ⚠️ カラム 'market_demand' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** market_demand
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 21. ⚠️ カラム 'market_demand' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** market_demand
- **ddl_default:** MEDIUM' COMMENT '市場での需要レベル（LOW:低、MEDIUM:中、HIGH:高、VERY_HIGH:非常に高）
- **yaml_default:** MEDIUM

---

#### 22. ⚠️ カラム 'updated_at' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** updated_at
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 23. ⚠️ カラム 'updated_at' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** updated_at
- **ddl_default:** CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時'
- **yaml_default:** CURRENT_TIMESTAMP

---

#### 24. ⚠️ カラム 'is_active' のNULL制約が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_active
- **ddl_nullable:** False
- **yaml_nullable:** True

---

#### 25. ⚠️ カラム 'is_active' のデフォルト値が一致しません

**テーブル:** MST_Skill

**詳細情報:**
- **column:** is_active
- **ddl_default:** TRUE COMMENT 'スキルが有効かどうか'
- **yaml_default:** True

---

#### 26. ✅ カラム 'prerequisite_skills' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** prerequisite_skills
- **ddl_type:** TEXT
- **yaml_type:** TEXT

---

#### 27. ✅ カラム 'evaluation_criteria' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** evaluation_criteria
- **ddl_type:** TEXT
- **yaml_type:** TEXT

---

#### 28. ✅ カラム 'learning_resources' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** learning_resources
- **ddl_type:** TEXT
- **yaml_type:** TEXT

---

#### 29. ✅ カラム 'description' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** description
- **ddl_type:** TEXT
- **yaml_type:** TEXT

---

#### 30. ✅ カラム 'skill_name_en' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** skill_name_en
- **ddl_type:** VARCHAR
- **yaml_type:** VARCHAR

---

#### 31. ✅ カラム 'effective_to' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** effective_to
- **ddl_type:** DATE
- **yaml_type:** DATE

---

#### 32. ✅ カラム 'effective_from' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** effective_from
- **ddl_type:** DATE
- **yaml_type:** DATE

---

#### 33. ✅ カラム 'certification_info' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** certification_info
- **ddl_type:** TEXT
- **yaml_type:** TEXT

---

#### 34. ✅ カラム 'related_skills' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** related_skills
- **ddl_type:** TEXT
- **yaml_type:** TEXT

---

#### 35. ✅ カラム 'required_experience_months' のデータ型整合性OK

**テーブル:** MST_Skill

**詳細情報:**
- **column:** required_experience_months
- **ddl_type:** INT
- **yaml_type:** INT

