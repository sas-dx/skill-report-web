# テーブル定義書: MST_SkillCategory

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_SkillCategory |
| 論理名 | スキルカテゴリマスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:19 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| category_code | カテゴリコード | VARCHAR | 20 | ○ |  | カテゴリコード |
| category_name | カテゴリ名 | VARCHAR | 100 | ○ |  | カテゴリ名 |
| category_level | カテゴリレベル | INT |  | ○ | 1 | カテゴリレベル |
| category_name_en | カテゴリ名英語 | VARCHAR | 100 | ○ |  | カテゴリ名英語 |
| category_name_short | カテゴリ名略称 | VARCHAR | 50 | ○ |  | カテゴリ名略称 |
| category_path | カテゴリパス | VARCHAR | 500 | ○ |  | カテゴリパス |
| category_status | カテゴリ状態 | ENUM |  | ○ | ACTIVE | カテゴリ状態 |
| category_type | カテゴリ種別 | ENUM |  | ○ |  | カテゴリ種別 |
| color_code | カラーコード | VARCHAR | 7 | ○ |  | カラーコード |
| description | カテゴリ説明 | TEXT |  | ○ |  | カテゴリ説明 |
| display_order | 表示順序 | INT |  | ○ | 999 | 表示順序 |
| effective_from | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| evaluation_method | 評価方法 | ENUM |  | ○ |  | 評価方法 |
| icon_url | アイコンURL | VARCHAR | 255 | ○ |  | アイコンURL |
| is_leaf_category | 末端カテゴリフラグ | BOOLEAN |  | ○ | True | 末端カテゴリフラグ |
| is_popular | 人気カテゴリフラグ | BOOLEAN |  | ○ | False | 人気カテゴリフラグ |
| is_system_category | システムカテゴリフラグ | BOOLEAN |  | ○ | False | システムカテゴリフラグ |
| max_level | 最大レベル | INT |  | ○ |  | 最大レベル |
| parent_category_id | 親カテゴリID | VARCHAR | 50 | ○ |  | 親カテゴリID |
| skill_count | スキル数 | INT |  | ○ | 0 | スキル数 |
| skillcategory_id | MST_SkillCategoryの主キー | SERIAL |  | × |  | MST_SkillCategoryの主キー |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

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
| idx_mst_skillcategory_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_skillcategory_parent | parent_category_id | MST_SkillCategory | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_category_code | UNIQUE |  | category_code一意制約 |
| chk_category_level | CHECK | category_level > 0 | category_level正値チェック制約 |
| chk_category_status | CHECK | category_status IN (...) | category_status値チェック制約 |
| chk_category_type | CHECK | category_type IN (...) | category_type値チェック制約 |
| chk_max_level | CHECK | max_level > 0 | max_level正値チェック制約 |

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
- カテゴリコードは新設時に自動採番（CAT + 3桁連番）
- システムカテゴリは is_system_category = true で保護
- 親カテゴリが無効化される場合は子カテゴリも無効化
- 末端カテゴリのみにスキルを直接紐付け可能
- カテゴリパスは親カテゴリ変更時に自動更新
- スキル数は関連スキルの増減時に自動更新
- 有効期間外のカテゴリは自動的に無効化

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキルカテゴリマスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |