# テーブル定義書: MST_Permission

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Permission |
| 論理名 | 権限情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:18 |

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
| permission_id | MST_Permissionの主キー | SERIAL |  | × |  | MST_Permissionの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_permission_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_permission_parent | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_permission | PRIMARY KEY | permission_id | 主キー制約 |

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