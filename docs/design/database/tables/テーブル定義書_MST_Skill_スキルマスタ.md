# テーブル定義書: MST_Skill

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Skill |
| 論理名 | スキルマスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:57 |

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
| id | スキルID | VARCHAR | 50 | ○ |  | スキルID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| skill_name | スキル名 | VARCHAR | 200 | ○ |  | スキル名 |
| category_id | カテゴリID | VARCHAR | 50 | ○ |  | カテゴリID |
| certification_info | 資格情報 | TEXT |  | ○ |  | 資格情報 |
| description | 説明 | TEXT |  | ○ |  | 説明 |
| difficulty_level | 難易度レベル | INTEGER |  | ○ | 3 | 難易度レベル |
| display_order | 表示順序 | INTEGER |  | ○ | 0 | 表示順序 |
| effective_from | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| evaluation_criteria | 評価基準 | TEXT |  | ○ |  | 評価基準 |
| is_active | 有効フラグ | BOOLEAN |  | ○ | True | 有効フラグ |
| is_core_skill | コアスキルフラグ | BOOLEAN |  | ○ | False | コアスキルフラグ |
| learning_resources | 学習リソース | TEXT |  | ○ |  | 学習リソース |
| market_demand | 市場需要 | ENUM |  | ○ | MEDIUM | 市場需要 |
| prerequisite_skills | 前提スキル | TEXT |  | ○ |  | 前提スキル |
| related_skills | 関連スキル | TEXT |  | ○ |  | 関連スキル |
| required_experience_months | 必要経験月数 | INTEGER |  | ○ |  | 必要経験月数 |
| skill_id | MST_Skillの主キー | SERIAL |  | × |  | MST_Skillの主キー |
| skill_name_en | スキル名英語 | VARCHAR | 200 | ○ |  | スキル名英語 |
| skill_type | スキル種別 | ENUM |  | ○ | TECHNICAL | スキル種別 |
| technology_trend | 技術トレンド | ENUM |  | ○ | STABLE | 技術トレンド |
| is_deleted | 削除フラグ | BOOLEAN |  | ○ | False | 削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_MST_Skill_id | id | ○ |  |
| idx_MST_Skill_skill_name | skill_name | × |  |
| idx_MST_Skill_category_id | category_id | × |  |
| idx_MST_Skill_skill_type | skill_type | × |  |
| idx_MST_Skill_category_order | category_id, display_order | × |  |
| idx_MST_Skill_market_demand | market_demand | × |  |
| idx_MST_Skill_is_active | is_active | × |  |
| idx_mst_skill_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_Skill_tenant | tenant_id | MST_Tenant | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_MST_Skill_category | category_id | MST_SkillCategory | id | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_difficulty_level | CHECK | difficulty_level > 0 | difficulty_level正値チェック制約 |
| chk_skill_type | CHECK | skill_type IN (...) | skill_type値チェック制約 |

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
- スキルIDは「SKILL + 連番」形式で生成する
- 新しいスキル追加時は適切なカテゴリに分類する
- 評価基準は5段階で定義し、各レベルの説明を含める
- 前提スキルは循環参照しないよう注意する
- 市場需要と技術トレンドは定期的に見直しを行う
- コアスキルは組織戦略に基づいて設定する
- 廃止予定のスキルは有効終了日を設定し、段階的に無効化する
- 関連スキルの設定により、スキルマップの可視化を支援する

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - MST_Skillの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |