# テーブル定義書: MST_Skill

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Skill |
| 論理名 | スキルマスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-06 19:50:10 |

## 概要

スキルマスタテーブルは、システムで管理するスキル項目の基本情報を管理するマスタテーブルです。

主な目的：
- スキル項目の一元管理
- スキルカテゴリとレベル定義の管理
- スキル評価基準の標準化
- スキル検索とフィルタリングの支援

このテーブルは、スキル管理システムの基盤となるマスタテーブルで、
統一されたスキル評価基準と効率的なスキル管理を実現します。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | スキルID | VARCHAR | 50 | ○ |  | スキルの一意識別子 |
| skill_name | スキル名 | VARCHAR | 200 | ○ |  | スキルの名称 |
| skill_name_en | スキル名英語 | VARCHAR | 200 | ○ |  | スキルの英語名称 |
| category_id | カテゴリID | VARCHAR | 50 | ○ |  | スキルカテゴリのID（MST_SkillCategoryへの外部キー） |
| skill_type | スキル種別 | ENUM |  | ○ | TECHNICAL | スキルの種別（TECHNICAL:技術スキル、BUSINESS:ビジネススキル、SOFT:ソフトスキル、LANGUAGE:言語スキル） |
| difficulty_level | 難易度レベル | INTEGER |  | ○ | 3 | スキルの習得難易度（1:易、2:普通、3:難、4:非常に難、5:最高難度） |
| description | 説明 | TEXT |  | ○ |  | スキルの詳細説明 |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  | スキル評価の基準や指標（JSON形式） |
| required_experience_months | 必要経験月数 | INTEGER |  | ○ |  | スキル習得に必要な経験期間（月数） |
| related_skills | 関連スキル | TEXT |  | ○ |  | 関連するスキルのID一覧（JSON配列形式） |
| prerequisite_skills | 前提スキル | TEXT |  | ○ |  | 習得前提となるスキルのID一覧（JSON配列形式） |
| certification_info | 資格情報 | TEXT |  | ○ |  | 関連する資格や認定情報（JSON形式） |
| learning_resources | 学習リソース | TEXT |  | ○ |  | 学習に役立つリソースのURL一覧（JSON配列形式） |
| market_demand | 市場需要 | ENUM |  | ○ | MEDIUM | 市場での需要レベル（LOW:低、MEDIUM:中、HIGH:高、VERY_HIGH:非常に高） |
| technology_trend | 技術トレンド | ENUM |  | ○ | STABLE | 技術トレンド（EMERGING:新興、GROWING:成長中、STABLE:安定、DECLINING:衰退） |
| is_core_skill | コアスキルフラグ | BOOLEAN |  | ○ | False | 組織のコアスキルかどうか |
| display_order | 表示順序 | INTEGER |  | ○ | 0 | 同一カテゴリ内での表示順序 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | スキルが有効かどうか |
| effective_from | 有効開始日 | DATE |  | ○ |  | スキルの有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | スキルの有効終了日 |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_Skill_id | id | ○ | スキルID検索用（一意） |
| idx_MST_Skill_skill_name | skill_name | × | スキル名検索用 |
| idx_MST_Skill_category_id | category_id | × | カテゴリID検索用 |
| idx_MST_Skill_skill_type | skill_type | × | スキル種別検索用 |
| idx_MST_Skill_category_order | category_id, display_order | × | カテゴリ別表示順序検索用 |
| idx_MST_Skill_market_demand | market_demand | × | 市場需要検索用 |
| idx_MST_Skill_is_active | is_active | × | 有効フラグ検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_Skill_category | category_id | MST_SkillCategory | id | CASCADE | RESTRICT | MST_SkillCategoryへの外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_MST_Skill_id | UNIQUE |  | スキルID一意制約 |
| chk_MST_Skill_skill_type | CHECK | skill_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'LANGUAGE') | スキル種別値チェック制約 |
| chk_MST_Skill_difficulty_level | CHECK | difficulty_level BETWEEN 1 AND 5 | 難易度レベル値チェック制約（1-5） |
| chk_MST_Skill_required_experience | CHECK | required_experience_months IS NULL OR required_experience_months >= 0 | 必要経験月数非負数チェック制約 |
| chk_MST_Skill_market_demand | CHECK | market_demand IN ('LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH') | 市場需要値チェック制約 |
| chk_MST_Skill_technology_trend | CHECK | technology_trend IN ('EMERGING', 'GROWING', 'STABLE', 'DECLINING') | 技術トレンド値チェック制約 |
| chk_MST_Skill_display_order | CHECK | display_order >= 0 | 表示順序非負数チェック制約 |
| chk_MST_Skill_effective_period | CHECK | effective_to IS NULL OR effective_from IS NULL OR effective_to >= effective_from | 有効期間整合性チェック制約 |

## サンプルデータ

| id | skill_name | skill_name_en | category_id | skill_type | difficulty_level | description | evaluation_criteria | required_experience_months | related_skills | prerequisite_skills | certification_info | learning_resources | market_demand | technology_trend | is_core_skill | display_order | is_active | effective_from | effective_to |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| SKILL001 | React | React | CAT_FRONTEND | TECHNICAL | 3 | Reactライブラリを使用したフロントエンド開発スキル。コンポーネント設計、状態管理、Hooksの理解が含まれます。 | {"level1":"基本的なコンポーネント作成","level2":"状態管理とイベント処理","level3":"Hooks活用とパフォーマンス最適化","level4":"複雑なアプリケーション設計","level5":"ライブラリ開発とベストプラクティス"} | 6 | ["SKILL002", "SKILL003", "SKILL004"] | ["SKILL_JS001", "SKILL_HTML001"] | {"name":"React Developer Certification","provider":"Meta","url":"https://developers.facebook.com/certification/"} | ["https://reactjs.org/docs/","https://react.dev/learn","https://egghead.io/courses/react"] | HIGH | GROWING | True | 1 | True | 2024-01-01 | None |
| SKILL002 | TypeScript | TypeScript | CAT_FRONTEND | TECHNICAL | 3 | TypeScriptを使用した型安全なJavaScript開発スキル。型定義、ジェネリクス、高度な型操作が含まれます。 | {"level1":"基本的な型定義","level2":"インターフェースとクラス","level3":"ジェネリクスと高度な型","level4":"型レベルプログラミング","level5":"ライブラリ型定義作成"} | 4 | ["SKILL001", "SKILL003"] | ["SKILL_JS001"] | None | ["https://www.typescriptlang.org/docs/","https://typescript-jp.gitbook.io/deep-dive/"] | VERY_HIGH | GROWING | True | 2 | True | 2024-01-01 | None |
| SKILL003 | Node.js | Node.js | CAT_BACKEND | TECHNICAL | 3 | Node.jsを使用したサーバーサイド開発スキル。非同期処理、API開発、パフォーマンス最適化が含まれます。 | {"level1":"基本的なサーバー構築","level2":"Express.jsでのAPI開発","level3":"非同期処理とストリーム","level4":"パフォーマンス最適化","level5":"スケーラブルアーキテクチャ設計"} | 8 | ["SKILL001", "SKILL002", "SKILL004"] | ["SKILL_JS001"] | None | ["https://nodejs.org/en/docs/","https://expressjs.com/","https://nodeschool.io/"] | HIGH | STABLE | True | 1 | True | 2024-01-01 | None |

## 特記事項

- スキルIDは一意である必要がある
- スキル名は重複可能（異なるカテゴリで同名スキルが存在する場合）
- 評価基準はJSON形式でレベル別に定義する
- 関連スキルと前提スキルはJSON配列形式で管理
- 学習リソースはURL一覧をJSON配列で管理
- 有効期間を設定することで、廃止予定スキルの管理が可能
- 論理削除は is_active フラグで管理

## 業務ルール

- スキルIDは「SKILL + 連番」形式で生成する
- 新しいスキル追加時は適切なカテゴリに分類する
- 評価基準は5段階で定義し、各レベルの説明を含める
- 前提スキルは循環参照しないよう注意する
- 市場需要と技術トレンドは定期的に見直しを行う
- コアスキルは組織戦略に基づいて設定する
- 廃止予定のスキルは有効終了日を設定し、段階的に無効化する
- 関連スキルの設定により、スキルマップの可視化を支援する

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - MST_Skillの詳細定義 |
