# テーブル定義書: MST_Permission

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Permission |
| 論理名 | 権限情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-04 06:57:02 |

## 概要

MST_Permission（権限情報）は、システム内の権限（許可）を管理するマスタテーブルです。

主な目的：
- システム内の権限定義・管理（画面アクセス、機能実行、データ操作等）
- 権限の階層・グループ管理
- 細粒度アクセス制御の実現
- リソースベースアクセス制御（RBAC）の基盤
- 動的権限管理・条件付きアクセス制御
- 監査・コンプライアンス要件への対応
- 最小権限の原則実装

このテーブルは、ロールと組み合わせてシステムセキュリティを構成し、
適切なアクセス制御を実現する重要なマスタデータです。



## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| permission_code | 権限コード | VARCHAR | 50 | ○ |  | 権限を一意に識別するコード（例：PERM_USER_READ） |
| permission_name | 権限名 | VARCHAR | 100 | ○ |  | 権限の正式名称 |
| permission_name_short | 権限名略称 | VARCHAR | 50 | ○ |  | 権限の略称・短縮名 |
| permission_category | 権限カテゴリ | ENUM |  | ○ |  | 権限のカテゴリ（SYSTEM:システム、SCREEN:画面、API:API、DATA:データ、FUNCTION:機能） |
| resource_type | リソース種別 | VARCHAR | 50 | ○ |  | 権限対象のリソース種別（USER、SKILL、REPORT等） |
| action_type | アクション種別 | ENUM |  | ○ |  | 許可するアクション（CREATE:作成、READ:参照、UPDATE:更新、DELETE:削除、EXECUTE:実行） |
| scope_level | スコープレベル | ENUM |  | ○ |  | 権限のスコープ（GLOBAL:全体、TENANT:テナント、DEPARTMENT:部署、SELF:自分のみ） |
| parent_permission_id | 親権限ID | VARCHAR | 50 | ○ |  | 上位権限のID（MST_Permissionへの自己参照外部キー） |
| is_system_permission | システム権限フラグ | BOOLEAN |  | ○ | False | システム標準権限かどうか（削除・変更不可） |
| requires_conditions | 条件要求フラグ | BOOLEAN |  | ○ | False | 権限行使に条件が必要かどうか |
| condition_expression | 条件式 | TEXT |  | ○ |  | 権限行使の条件式（SQL WHERE句形式等） |
| risk_level | リスクレベル | INT |  | ○ | 1 | 権限のリスクレベル（1:低、2:中、3:高、4:最高） |
| requires_approval | 承認要求フラグ | BOOLEAN |  | ○ | False | 権限行使に承認が必要かどうか |
| audit_required | 監査要求フラグ | BOOLEAN |  | ○ | False | 権限行使時の監査ログ記録が必要かどうか |
| permission_status | 権限状態 | ENUM |  | ○ | ACTIVE | 権限の状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨） |
| effective_from | 有効開始日 | DATE |  | ○ |  | 権限の有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | 権限の有効終了日 |
| sort_order | 表示順序 | INT |  | ○ |  | 画面表示時の順序 |
| description | 権限説明 | TEXT |  | ○ |  | 権限の詳細説明・用途 |
| code | コード | VARCHAR | 20 | × |  | マスタコード |
| name | 名称 | VARCHAR | 100 | × |  | マスタ名称 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_permission_code | permission_code | ○ | 権限コード検索用（一意） |
| idx_permission_category | permission_category | × | 権限カテゴリ別検索用 |
| idx_resource_action | resource_type, action_type | × | リソース・アクション別検索用 |
| idx_scope_level | scope_level | × | スコープレベル別検索用 |
| idx_parent_permission | parent_permission_id | × | 親権限別検索用 |
| idx_system_permission | is_system_permission | × | システム権限検索用 |
| idx_risk_level | risk_level | × | リスクレベル別検索用 |
| idx_permission_status | permission_status | × | 権限状態別検索用 |
| idx_effective_period | effective_from, effective_to | × | 有効期間検索用 |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_permission_parent | parent_permission_id | MST_Permission | id | CASCADE | SET NULL | 親権限への自己参照外部キー |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_permission_code | UNIQUE |  | 権限コード一意制約 |
| chk_permission_category | CHECK | permission_category IN ('SYSTEM', 'SCREEN', 'API', 'DATA', 'FUNCTION') | 権限カテゴリ値チェック制約 |
| chk_action_type | CHECK | action_type IN ('CREATE', 'READ', 'UPDATE', 'DELETE', 'EXECUTE') | アクション種別値チェック制約 |
| chk_scope_level | CHECK | scope_level IN ('GLOBAL', 'TENANT', 'DEPARTMENT', 'SELF') | スコープレベル値チェック制約 |
| chk_permission_status | CHECK | permission_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED') | 権限状態値チェック制約 |
| chk_risk_level | CHECK | risk_level BETWEEN 1 AND 4 | リスクレベル範囲チェック制約 |
| chk_effective_period | CHECK | effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to | 有効期間整合性チェック制約 |
| chk_sort_order | CHECK | sort_order IS NULL OR sort_order >= 0 | 表示順序非負値チェック制約 |

## サンプルデータ

| permission_code | permission_name | permission_name_short | permission_category | resource_type | action_type | scope_level | parent_permission_id | is_system_permission | requires_conditions | condition_expression | risk_level | requires_approval | audit_required | permission_status | effective_from | effective_to | sort_order | description |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| PERM_USER_READ | ユーザー情報参照 | ユーザー参照 | DATA | USER | READ | TENANT | None | True | False | None | 1 | False | True | ACTIVE | 2025-01-01 | None | 1 | ユーザー情報の参照権限 |
| PERM_USER_UPDATE | ユーザー情報更新 | ユーザー更新 | DATA | USER | UPDATE | DEPARTMENT | None | True | True | department_id = :user_department_id | 2 | False | True | ACTIVE | 2025-01-01 | None | 2 | ユーザー情報の更新権限（同一部署のみ） |
| PERM_SYSTEM_ADMIN | システム管理 | システム管理 | SYSTEM | SYSTEM | EXECUTE | GLOBAL | None | True | False | None | 4 | True | True | ACTIVE | 2025-01-01 | None | 100 | システム全体の管理権限 |

## 特記事項

- 権限階層は自己参照外部キーで表現
- システム権限は削除・変更不可
- 条件式はSQL WHERE句形式で記述
- リスクレベルに応じた承認・監査要件
- スコープレベルによる権限範囲制限
- 有効期間による時限権限設定が可能

## 業務ルール

- 権限コードは PERM_ + リソース + アクション 形式
- システム権限は is_system_permission = true で保護
- リスクレベル3以上は承認要求を推奨
- 全ての権限行使は監査ログに記録
- 条件付き権限は condition_expression で制御
- 親権限が無効化される場合は子権限も無効化
- 有効期間外の権限は自動的に無効化

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 権限マスタテーブルの詳細定義 |
