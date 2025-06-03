# テーブル定義書: SYS_SkillIndex

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SkillIndex |
| 論理名 | スキル検索インデックス |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

SYS_SkillIndex（スキル検索インデックス）は、スキル検索機能の高速化のための検索インデックス情報を管理するシステムテーブルです。

主な目的：
- 全文検索インデックスの管理
- スキル名・キーワードの検索最適化
- 検索パフォーマンスの向上
- 検索結果の関連度スコア管理
- 検索統計情報の蓄積

このテーブルは、スキル管理機能において高速で精度の高い検索を実現する重要なシステムデータです。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | ID | VARCHAR | 50 | ○ |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | マルチテナント識別子 |
| skill_id | スキルID | VARCHAR | 50 | ○ |  | インデックス対象のスキルID（MST_Skillへの参照） |
| index_type | インデックスタイプ | ENUM |  | ○ |  | インデックスの種類（FULLTEXT:全文検索、KEYWORD:キーワード、CATEGORY:カテゴリ、SYNONYM:同義語） |
| search_term | 検索語 | VARCHAR | 200 | ○ |  | 検索対象となる語句・キーワード |
| normalized_term | 正規化語 | VARCHAR | 200 | ○ |  | 検索最適化のため正規化された語句 |
| relevance_score | 関連度スコア | DECIMAL | 5,3 | ○ | 1.0 | 検索結果の関連度スコア（0.000-1.000） |
| frequency_weight | 頻度重み | DECIMAL | 5,3 | ○ | 1.0 | 語句の出現頻度による重み（0.000-1.000） |
| position_weight | 位置重み | DECIMAL | 5,3 | ○ | 1.0 | 語句の出現位置による重み（0.000-1.000） |
| language_code | 言語コード | VARCHAR | 10 | ○ | ja | 検索語の言語（ja:日本語、en:英語等） |
| source_field | ソースフィールド | ENUM |  | ○ |  | インデックス元のフィールド（NAME:スキル名、DESCRIPTION:説明、KEYWORD:キーワード、CATEGORY:カテゴリ） |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | インデックスが有効かどうか |
| search_count | 検索回数 | INTEGER |  | ○ | 0 | この語句での検索実行回数 |
| last_searched_at | 最終検索日時 | TIMESTAMP |  | ○ |  | この語句で最後に検索された日時 |
| index_updated_at | インデックス更新日時 | TIMESTAMP |  | ○ |  | インデックスが最後に更新された日時 |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_skill_index_skill | skill_id | × | スキルID別検索用 |
| idx_skill_index_search_term | normalized_term, language_code | × | 正規化語・言語別検索用 |
| idx_skill_index_type | index_type | × | インデックスタイプ別検索用 |
| idx_skill_index_tenant_term | tenant_id, normalized_term | × | テナント別検索語検索用 |
| idx_skill_index_relevance | relevance_score | × | 関連度スコア別検索用 |
| idx_skill_index_active | is_active | × | 有効フラグ検索用 |
| idx_skill_index_search_stats | search_count, last_searched_at | × | 検索統計検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_skill_index_skill | skill_id | MST_Skill | id | CASCADE | CASCADE | スキルマスタへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_skill_index_type | CHECK | index_type IN ('FULLTEXT', 'KEYWORD', 'CATEGORY', 'SYNONYM') | インデックスタイプ値チェック制約 |
| chk_skill_index_source_field | CHECK | source_field IN ('NAME', 'DESCRIPTION', 'KEYWORD', 'CATEGORY') | ソースフィールド値チェック制約 |
| chk_skill_index_relevance_range | CHECK | relevance_score >= 0.000 AND relevance_score <= 1.000 | 関連度スコア範囲チェック制約 |
| chk_skill_index_frequency_range | CHECK | frequency_weight >= 0.000 AND frequency_weight <= 1.000 | 頻度重み範囲チェック制約 |
| chk_skill_index_position_range | CHECK | position_weight >= 0.000 AND position_weight <= 1.000 | 位置重み範囲チェック制約 |
| chk_skill_index_search_count_positive | CHECK | search_count >= 0 | 検索回数正数チェック制約 |

## サンプルデータ

| id | tenant_id | skill_id | index_type | search_term | normalized_term | relevance_score | frequency_weight | position_weight | language_code | source_field | is_active | search_count | last_searched_at | index_updated_at |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| SI001 | TENANT001 | SKILL001 | FULLTEXT | Java | java | 1.0 | 1.0 | 1.0 | ja | NAME | True | 150 | 2025-06-01 18:30:00 | 2025-06-01 10:00:00 |
| SI002 | TENANT001 | SKILL001 | KEYWORD | プログラミング | プログラミング | 0.8 | 0.75 | 0.9 | ja | DESCRIPTION | True | 85 | 2025-06-01 17:45:00 | 2025-06-01 10:00:00 |
| SI003 | TENANT001 | SKILL001 | SYNONYM | ジャバ | ジャバ | 0.9 | 0.5 | 1.0 | ja | KEYWORD | True | 25 | 2025-06-01 16:20:00 | 2025-06-01 10:00:00 |

## 特記事項

- 検索インデックスは定期的なバッチ処理で更新される
- 正規化語は検索精度向上のため小文字・ひらがな統一等を実施
- 関連度スコアは複数の重み要素を組み合わせて算出
- 検索統計情報は検索機能の改善に活用
- 無効化されたインデックスは検索対象から除外
- 多言語対応により国際化に対応
- 同義語インデックスにより検索の網羅性を向上

## 業務ルール

- スキル削除時は関連インデックスも自動削除
- インデックス更新は元データ変更時に自動実行
- 検索実行時は統計情報を更新
- 関連度スコアは0.000-1.000の範囲で管理
- 無効インデックスは検索結果から除外
- 正規化語は検索時の表記ゆれ対応に使用
- 検索頻度の高い語句は優先的にインデックス化
- 定期的な統計分析によりインデックス最適化を実施

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - スキル検索インデックスシステムテーブルの詳細定義 |
