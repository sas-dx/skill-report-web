# テーブル定義書: MST_Role

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Role |
| 論理名 | ロール情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:05:57 |

## 概要

MST_Role（ロール情報）は、システム内のロール（役割）を管理するマスタテーブルです。
主な目的：
- システム内のロール定義・管理（管理者、一般ユーザー、閲覧者等）
- ロール階層の管理（上位ロール、下位ロール）
- ロール別権限設定の基盤
- 職務分離・最小権限の原則実装
- 動的権限管理・ロールベースアクセス制御（RBAC）
- 組織変更に対応した柔軟な権限管理
- 監査・コンプライアンス対応
このテーブルは、システムセキュリティの基盤となり、
適切なアクセス制御と権限管理を実現する重要なマスタデータです。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| auto_assign_conditions | 自動割り当て条件 | JSON |  | ○ |  | 自動割り当て条件 |
| description | ロール説明 | TEXT |  | ○ |  | ロール説明 |
| effective_from | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| is_system_role | システムロールフラグ | BOOLEAN |  | ○ | False | システムロールフラグ |
| is_tenant_specific | テナント固有フラグ | BOOLEAN |  | ○ | False | テナント固有フラグ |
| max_users | 最大ユーザー数 | INT |  | ○ |  | 最大ユーザー数 |
| parent_role_id | 親ロールID | VARCHAR | 50 | ○ |  | 親ロールID |
| role_category | ロールカテゴリ | ENUM |  | ○ |  | ロールカテゴリ |
| role_code | ロールコード | VARCHAR | 20 | ○ |  | ロールコード |
| role_id | MST_Roleの主キー | SERIAL |  | × |  | MST_Roleの主キー |
| role_level | ロールレベル | INT |  | ○ |  | ロールレベル |
| role_name | ロール名 | VARCHAR | 100 | ○ |  | ロール名 |
| role_name_short | ロール名略称 | VARCHAR | 50 | ○ |  | ロール名略称 |
| role_priority | ロール優先度 | INT |  | ○ | 999 | ロール優先度 |
| role_status | ロール状態 | ENUM |  | ○ | ACTIVE | ロール状態 |
| sort_order | 表示順序 | INT |  | ○ |  | 表示順序 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_role_code | role_code | ○ |  |
| idx_role_category | role_category | × |  |
| idx_role_level | role_level | × |  |
| idx_parent_role | parent_role_id | × |  |
| idx_system_role | is_system_role | × |  |
| idx_tenant_specific | is_tenant_specific | × |  |
| idx_role_status | role_status | × |  |
| idx_effective_period | effective_from, effective_to | × |  |
| idx_sort_order | sort_order | × |  |
| idx_mst_role_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_role_parent | parent_role_id | MST_Role | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_role_code | UNIQUE |  | role_code一意制約 |
| chk_role_level | CHECK | role_level > 0 | role_level正値チェック制約 |
| chk_role_status | CHECK | role_status IN (...) | role_status値チェック制約 |

## サンプルデータ

| role_code | role_name | role_name_short | role_category | role_level | parent_role_id | is_system_role | is_tenant_specific | max_users | role_priority | auto_assign_conditions | role_status | effective_from | effective_to | sort_order | description |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| ROLE001 | システム管理者 | システム管理者 | SYSTEM | 1 | None | True | False | 5 | 1 | None | ACTIVE | 2025-01-01 | None | 1 | システム全体の管理権限を持つ最上位ロール |
| ROLE002 | テナント管理者 | テナント管理者 | TENANT | 2 | None | True | True | 10 | 2 | None | ACTIVE | 2025-01-01 | None | 2 | テナント内の管理権限を持つロール |
| ROLE003 | 一般ユーザー | 一般ユーザー | BUSINESS | 3 | None | True | False | None | 10 | {"default": true} | ACTIVE | 2025-01-01 | None | 10 | 基本的な業務機能を利用できるロール |

## 特記事項

- ロール階層は自己参照外部キーで表現
- システムロールは削除・変更不可
- テナント固有ロールはテナント内でのみ有効
- 複数ロール保持時は優先度で権限を決定
- 自動割り当て条件はJSON形式で柔軟に設定
- 有効期間による時限ロール設定が可能
- ロールコードは新設時に自動採番（ROLE + 3桁連番）
- システムロールは is_system_role = true で保護
- 親ロールが無効化される場合は子ロールも無効化
- 最大ユーザー数を超える割り当ては不可
- 有効期間外のロールは自動的に無効化
- ロール削除時は関連するユーザーロール紐付けも削除
- テナント固有ロールは該当テナント内でのみ使用可能

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - ロール情報テーブルの詳細定義 |
| 1.1.0 | 2025-06-01 | 開発チーム | 改版履歴管理機能追加、ロール階層・権限継承機能強化 |
| 3.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |