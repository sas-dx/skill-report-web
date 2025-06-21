# テーブル定義書: MST_SkillCategory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillCategory |
| 論理名 | スキルカテゴリマスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:21:58 |

## 概要

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


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| category_code |  | VARCHAR |  | ○ |  |  |
| category_name |  | VARCHAR |  | ○ |  |  |
| category_name_short |  | VARCHAR |  | ○ |  |  |
| category_name_en |  | VARCHAR |  | ○ |  |  |
| category_type |  | ENUM |  | ○ |  |  |
| parent_category_id |  | VARCHAR |  | ○ |  |  |
| category_level |  | INT |  | ○ | 1 |  |
| category_path |  | VARCHAR |  | ○ |  |  |
| is_system_category |  | BOOLEAN |  | ○ | False |  |
| is_leaf_category |  | BOOLEAN |  | ○ | True |  |
| skill_count |  | INT |  | ○ | 0 |  |
| evaluation_method |  | ENUM |  | ○ |  |  |
| max_level |  | INT |  | ○ |  |  |
| icon_url |  | VARCHAR |  | ○ |  |  |
| color_code |  | VARCHAR |  | ○ |  |  |
| display_order |  | INT |  | ○ | 999 |  |
| is_popular |  | BOOLEAN |  | ○ | False |  |
| category_status |  | ENUM |  | ○ | ACTIVE |  |
| effective_from |  | DATE |  | ○ |  |  |
| effective_to |  | DATE |  | ○ |  |  |
| description |  | TEXT |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_category_code | category_code | ○ |  |
| idx_category_type | category_type | × |  |
| idx_parent_category | parent_category_id | × |  |
| idx_category_level | category_level | × |  |
| idx_category_path | category_path | × |  |
| idx_system_category | is_system_category | × |  |
| idx_leaf_category | is_leaf_category | × |  |
| idx_category_status | category_status | × |  |
| idx_display_order | parent_category_id, display_order | × |  |
| idx_popular_category | is_popular | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_category_code | UNIQUE |  | category_code一意制約 |
| chk_category_type | CHECK | category_type IN (...) | category_type値チェック制約 |
| chk_category_level | CHECK | category_level > 0 | category_level正値チェック制約 |
| chk_max_level | CHECK | max_level > 0 | max_level正値チェック制約 |
| chk_category_status | CHECK | category_status IN (...) | category_status値チェック制約 |

## サンプルデータ

| category_code | category_name | category_name_short | category_name_en | category_type | parent_category_id | category_level | category_path | is_system_category | is_leaf_category | skill_count | evaluation_method | max_level | icon_url | color_code | display_order | is_popular | category_status | effective_from | effective_to | description |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| CAT001 | プログラミング言語 | プログラミング | Programming Languages | TECHNICAL | None | 1 | /プログラミング言語 | True | False | 25 | LEVEL | 5 | /icons/programming.svg | #007ACC | 1 | True | ACTIVE | 2025-01-01 | None | 各種プログラミング言語のスキル |
| CAT002 | Java | Java | Java | TECHNICAL | CAT001 | 2 | /プログラミング言語/Java | True | True | 8 | LEVEL | 5 | /icons/java.svg | #ED8B00 | 1 | True | ACTIVE | 2025-01-01 | None | Java言語に関するスキル |
| CAT003 | コミュニケーション | コミュニケーション | Communication | SOFT | None | 1 | /コミュニケーション | True | True | 12 | LEVEL | 4 | /icons/communication.svg | #28A745 | 10 | True | ACTIVE | 2025-01-01 | None | コミュニケーション能力に関するスキル |

## 特記事項

- カテゴリ階層は自己参照外部キーで表現
- システムカテゴリは削除・変更不可
- カテゴリパスで階層構造を可視化
- 評価方法はカテゴリ単位で設定可能
- アイコン・カラーコードで視覚的識別
- 人気カテゴリフラグで注目度管理

## 業務ルール

- カテゴリコードは新設時に自動採番（CAT + 3桁連番）
- システムカテゴリは is_system_category = true で保護
- 親カテゴリが無効化される場合は子カテゴリも無効化
- 末端カテゴリのみにスキルを直接紐付け可能
- カテゴリパスは親カテゴリ変更時に自動更新
- スキル数は関連スキルの増減時に自動更新
- 有効期間外のカテゴリは自動的に無効化

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキルカテゴリマスタテーブルの詳細定義 |