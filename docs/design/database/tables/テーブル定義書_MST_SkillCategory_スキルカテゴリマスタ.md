# テーブル定義書: MST_SkillCategory (スキルカテゴリマスタ)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_SkillCategory |
| 論理名 | スキルカテゴリマスタ |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_SkillCategory_details.yaml` で行ってください。



## 📝 テーブル概要

MST_SkillCategory（スキルカテゴリマスタ）は、スキルの分類・カテゴリを管理するマスタテーブルです。

主な目的：
- スキルの体系的分類・階層管理
- スキル検索・絞り込みの基盤
- スキルマップ・スキル評価の構造化
- 業界標準・企業独自のスキル分類対応
- スキル統計・分析の軸設定
- キャリアパス・研修計画の基盤
- スキル可視化・レポート生成の支援

このテーブルは、スキル管理システムの基盤となり、
効率的なスキル管理と戦略的人材育成を支援します。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| category_code | カテゴリコード | VARCHAR | 20 | ○ |  |  |  | スキルカテゴリを一意に識別するコード（例：CAT001） |
| category_name | カテゴリ名 | VARCHAR | 100 | ○ |  |  |  | スキルカテゴリの正式名称 |
| category_name_short | カテゴリ名略称 | VARCHAR | 50 | ○ |  |  |  | スキルカテゴリの略称・短縮名 |
| category_name_en | カテゴリ名英語 | VARCHAR | 100 | ○ |  |  |  | スキルカテゴリの英語名称 |
| category_type | カテゴリ種別 | ENUM |  | ○ |  |  |  | カテゴリの種別（TECHNICAL:技術、BUSINESS:ビジネス、SOFT:ソフト、CERTIFICATION:資格、LANGUAGE:言語） |
| parent_category_id | 親カテゴリID | VARCHAR | 50 | ○ |  | ● |  | 上位カテゴリのID（MST_SkillCategoryへの自己参照外部キー） |
| category_level | カテゴリレベル | INT |  | ○ |  |  | 1 | カテゴリの階層レベル（1:最上位、数値が大きいほど下位） |
| category_path | カテゴリパス | VARCHAR | 500 | ○ |  |  |  | ルートからのカテゴリパス（例：/技術/プログラミング/Java） |
| is_system_category | システムカテゴリフラグ | BOOLEAN |  | ○ |  |  |  | システム標準カテゴリかどうか（削除・変更不可） |
| is_leaf_category | 末端カテゴリフラグ | BOOLEAN |  | ○ |  |  | True | 末端カテゴリ（子カテゴリを持たない）かどうか |
| skill_count | スキル数 | INT |  | ○ |  |  |  | このカテゴリに属するスキル数 |
| evaluation_method | 評価方法 | ENUM |  | ○ |  |  |  | このカテゴリのスキル評価方法（LEVEL:レベル、SCORE:スコア、BINARY:有無、CERTIFICATION:資格） |
| max_level | 最大レベル | INT |  | ○ |  |  |  | レベル評価時の最大レベル数 |
| icon_url | アイコンURL | VARCHAR | 255 | ○ |  |  |  | カテゴリ表示用アイコンのURL |
| color_code | カラーコード | VARCHAR | 7 | ○ |  |  |  | カテゴリ表示用カラーコード（#RRGGBB形式） |
| display_order | 表示順序 | INT |  | ○ |  |  | 999 | 同階層内での表示順序 |
| is_popular | 人気カテゴリフラグ | BOOLEAN |  | ○ |  |  |  | 人気・注目カテゴリかどうか |
| category_status | カテゴリ状態 | ENUM |  | ○ |  |  | ACTIVE | カテゴリの状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨） |
| effective_from | 有効開始日 | DATE |  | ○ |  |  |  | カテゴリの有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  |  |  | カテゴリの有効終了日 |
| description | カテゴリ説明 | TEXT |  | ○ |  |  |  | カテゴリの詳細説明・用途 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_category_code | category_code | ○ | カテゴリコード検索用（一意） |
| idx_category_type | category_type | × | カテゴリ種別検索用 |
| idx_parent_category | parent_category_id | × | 親カテゴリ別検索用 |
| idx_category_level | category_level | × | カテゴリレベル別検索用 |
| idx_category_path | category_path | × | カテゴリパス検索用 |
| idx_system_category | is_system_category | × | システムカテゴリ検索用 |
| idx_leaf_category | is_leaf_category | × | 末端カテゴリ検索用 |
| idx_category_status | category_status | × | カテゴリ状態別検索用 |
| idx_display_order | parent_category_id, display_order | × | 表示順序検索用 |
| idx_popular_category | is_popular | × | 人気カテゴリ検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_category_code | UNIQUE | category_code |  | カテゴリコード一意制約 |
| chk_category_type | CHECK |  | category_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'LANGUAGE') | カテゴリ種別値チェック制約 |
| chk_category_status | CHECK |  | category_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED') | カテゴリ状態値チェック制約 |
| chk_evaluation_method | CHECK |  | evaluation_method IS NULL OR evaluation_method IN ('LEVEL', 'SCORE', 'BINARY', 'CERTIFICATION') | 評価方法値チェック制約 |
| chk_category_level | CHECK |  | category_level > 0 | カテゴリレベル正値チェック制約 |
| chk_max_level | CHECK |  | max_level IS NULL OR max_level > 0 | 最大レベル正値チェック制約 |
| chk_skill_count | CHECK |  | skill_count >= 0 | スキル数非負値チェック制約 |
| chk_display_order | CHECK |  | display_order >= 0 | 表示順序非負値チェック制約 |
| chk_effective_period | CHECK |  | effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to | 有効期間整合性チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_skillcategory_parent | parent_category_id | MST_SkillCategory | id | CASCADE | SET NULL | 親カテゴリへの自己参照外部キー |

## 📊 サンプルデータ

```json
[
  {
    "category_code": "CAT001",
    "category_name": "プログラミング言語",
    "category_name_short": "プログラミング",
    "category_name_en": "Programming Languages",
    "category_type": "TECHNICAL",
    "parent_category_id": null,
    "category_level": 1,
    "category_path": "/プログラミング言語",
    "is_system_category": true,
    "is_leaf_category": false,
    "skill_count": 25,
    "evaluation_method": "LEVEL",
    "max_level": 5,
    "icon_url": "/icons/programming.svg",
    "color_code": "#007ACC",
    "display_order": 1,
    "is_popular": true,
    "category_status": "ACTIVE",
    "effective_from": "2025-01-01",
    "effective_to": null,
    "description": "各種プログラミング言語のスキル"
  },
  {
    "category_code": "CAT002",
    "category_name": "Java",
    "category_name_short": "Java",
    "category_name_en": "Java",
    "category_type": "TECHNICAL",
    "parent_category_id": "CAT001",
    "category_level": 2,
    "category_path": "/プログラミング言語/Java",
    "is_system_category": true,
    "is_leaf_category": true,
    "skill_count": 8,
    "evaluation_method": "LEVEL",
    "max_level": 5,
    "icon_url": "/icons/java.svg",
    "color_code": "#ED8B00",
    "display_order": 1,
    "is_popular": true,
    "category_status": "ACTIVE",
    "effective_from": "2025-01-01",
    "effective_to": null,
    "description": "Java言語に関するスキル"
  },
  {
    "category_code": "CAT003",
    "category_name": "コミュニケーション",
    "category_name_short": "コミュニケーション",
    "category_name_en": "Communication",
    "category_type": "SOFT",
    "parent_category_id": null,
    "category_level": 1,
    "category_path": "/コミュニケーション",
    "is_system_category": true,
    "is_leaf_category": true,
    "skill_count": 12,
    "evaluation_method": "LEVEL",
    "max_level": 4,
    "icon_url": "/icons/communication.svg",
    "color_code": "#28A745",
    "display_order": 10,
    "is_popular": true,
    "category_status": "ACTIVE",
    "effective_from": "2025-01-01",
    "effective_to": null,
    "description": "コミュニケーション能力に関するスキル"
  }
]
```

## 📌 特記事項

- カテゴリ階層は自己参照外部キーで表現
- システムカテゴリは削除・変更不可
- カテゴリパスで階層構造を可視化
- 評価方法はカテゴリ単位で設定可能
- アイコン・カラーコードで視覚的識別
- 人気カテゴリフラグで注目度管理

## 📋 業務ルール

- カテゴリコードは新設時に自動採番（CAT + 3桁連番）
- システムカテゴリは is_system_category = true で保護
- 親カテゴリが無効化される場合は子カテゴリも無効化
- 末端カテゴリのみにスキルを直接紐付け可能
- カテゴリパスは親カテゴリ変更時に自動更新
- スキル数は関連スキルの増減時に自動更新
- 有効期間外のカテゴリは自動的に無効化
