# テーブル定義書: MST_Skill

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Skill |
| 論理名 | スキルマスタ |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 23:19:39 |

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
| skill_id | MST_Skillの主キー | SERIAL |  | × |  | MST_Skillの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_skill_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_MST_Skill_tenant | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_MST_Skill_category | None | None | None | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_skill | PRIMARY KEY | skill_id | 主キー制約 |
| uk_id | UNIQUE |  | id一意制約 |

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