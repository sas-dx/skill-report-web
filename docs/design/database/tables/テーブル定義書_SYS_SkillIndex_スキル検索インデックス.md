# テーブル定義書: SYS_SkillIndex

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | SYS_SkillIndex |
| 論理名 | スキル検索インデックス |
| カテゴリ | システム系 |
| 生成日時 | 2025-06-21 17:20:35 |

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
| id |  | VARCHAR |  | ○ |  |  |
| tenant_id |  | VARCHAR |  | ○ |  |  |
| skill_id |  | VARCHAR |  | ○ |  |  |
| index_type |  | ENUM |  | ○ |  |  |
| search_term |  | VARCHAR |  | ○ |  |  |
| normalized_term |  | VARCHAR |  | ○ |  |  |
| relevance_score |  | DECIMAL |  | ○ | 1.0 |  |
| frequency_weight |  | DECIMAL |  | ○ | 1.0 |  |
| position_weight |  | DECIMAL |  | ○ | 1.0 |  |
| language_code |  | VARCHAR |  | ○ | ja |  |
| source_field |  | ENUM |  | ○ |  |  |
| is_active |  | BOOLEAN |  | ○ | True |  |
| search_count |  | INTEGER |  | ○ | 0 |  |
| last_searched_at |  | TIMESTAMP |  | ○ |  |  |
| index_updated_at |  | TIMESTAMP |  | ○ |  |  |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_skill_index_skill | skill_id | × |  |
| idx_skill_index_search_term | normalized_term, language_code | × |  |
| idx_skill_index_type | index_type | × |  |
| idx_skill_index_tenant_term | tenant_id, normalized_term | × |  |
| idx_skill_index_relevance | relevance_score | × |  |
| idx_skill_index_active | is_active | × |  |
| idx_skill_index_search_stats | search_count, last_searched_at | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_index_type | CHECK | index_type IN (...) | index_type値チェック制約 |

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