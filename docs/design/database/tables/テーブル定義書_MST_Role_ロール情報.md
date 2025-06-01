# テーブル定義書: MST_Role

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Role |
| 論理名 | ロール情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-01 20:40:25 |

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
| id | ID | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | マルチテナント識別子 |
| role_code | ロールコード | VARCHAR | 20 | ○ |  | ロールを一意に識別するコード（例：ROLE001） |
| role_name | ロール名 | VARCHAR | 100 | ○ |  | ロールの正式名称 |
| role_name_short | ロール名略称 | VARCHAR | 50 | ○ |  | ロールの略称・短縮名 |
| role_category | ロールカテゴリ | ENUM |  | ○ |  | ロールのカテゴリ（SYSTEM:システム、BUSINESS:業務、TENANT:テナント、CUSTOM:カスタム） |
| role_level | ロールレベル | INT |  | ○ |  | ロールの階層レベル（1:最上位、数値が大きいほど下位） |
| parent_role_id | 親ロールID | VARCHAR | 50 | ○ |  | 上位ロールのID（MST_Roleへの自己参照外部キー） |
| is_system_role | システムロールフラグ | BOOLEAN |  | ○ | False | システム標準ロールかどうか（削除・変更不可） |
| is_tenant_specific | テナント固有フラグ | BOOLEAN |  | ○ | False | テナント固有のロールかどうか |
| max_users | 最大ユーザー数 | INT |  | ○ |  | このロールに割り当て可能な最大ユーザー数 |
| role_priority | ロール優先度 | INT |  | ○ | 999 | 複数ロール保持時の優先度（数値が小さいほど高優先） |
| auto_assign_conditions | 自動割り当て条件 | JSON |  | ○ |  | 自動ロール割り当ての条件（JSON形式） |
| role_status | ロール状態 | ENUM |  | ○ | ACTIVE | ロールの状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨） |
| effective_from | 有効開始日 | DATE |  | ○ |  | ロールの有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | ロールの有効終了日 |
| sort_order | 表示順序 | INT |  | ○ |  | 画面表示時の順序 |
| description | ロール説明 | TEXT |  | ○ |  | ロールの詳細説明・用途 |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  | レコード更新者のユーザーID |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_role_code | role_code | ○ | ロールコード検索用（一意） |
| idx_role_category | role_category | × | ロールカテゴリ別検索用 |
| idx_role_level | role_level | × | ロールレベル別検索用 |
| idx_parent_role | parent_role_id | × | 親ロール別検索用 |
| idx_system_role | is_system_role | × | システムロール検索用 |
| idx_tenant_specific | is_tenant_specific | × | テナント固有ロール検索用 |
| idx_role_status | role_status | × | ロール状態別検索用 |
| idx_effective_period | effective_from, effective_to | × | 有効期間検索用 |
| idx_sort_order | sort_order | × | 表示順序検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_role_parent | parent_role_id | MST_Role | id | CASCADE | SET NULL | 親ロールへの自己参照外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_role_code | UNIQUE |  | ロールコード一意制約 |
| chk_role_level | CHECK | role_level > 0 | ロールレベル正値チェック制約 |
| chk_role_category | CHECK | role_category IN ('SYSTEM', 'BUSINESS', 'TENANT', 'CUSTOM') | ロールカテゴリ値チェック制約 |
| chk_role_status | CHECK | role_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED') | ロール状態値チェック制約 |
| chk_max_users | CHECK | max_users IS NULL OR max_users > 0 | 最大ユーザー数正値チェック制約 |
| chk_role_priority | CHECK | role_priority > 0 | ロール優先度正値チェック制約 |
| chk_effective_period | CHECK | effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to | 有効期間整合性チェック制約 |
| chk_sort_order | CHECK | sort_order IS NULL OR sort_order >= 0 | 表示順序非負値チェック制約 |

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

## 業務ルール

- ロールコードは新設時に自動採番（ROLE + 3桁連番）
- システムロールは is_system_role = true で保護
- 親ロールが無効化される場合は子ロールも無効化
- 最大ユーザー数を超える割り当ては不可
- 有効期間外のロールは自動的に無効化
- ロール削除時は関連するユーザーロール紐付けも削除
- テナント固有ロールは該当テナント内でのみ使用可能

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - ロール情報テーブルの詳細定義 |
| 1.1.0 | 2025-06-01 | 開発チーム | 改版履歴管理機能追加、ロール階層・権限継承機能強化 |
