# テーブル定義書: MST_Permission

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Permission |
| 論理名 | 権限情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| action_type | アクション種別 | ENUM |  | ○ |  | アクション種別 |
| audit_required | 監査要求フラグ | BOOLEAN |  | ○ | False | 監査要求フラグ |
| condition_expression | 条件式 | TEXT |  | ○ |  | 条件式 |
| description | 権限説明 | TEXT |  | ○ |  | 権限説明 |
| effective_from | 有効開始日 | DATE |  | ○ |  | 有効開始日 |
| effective_to | 有効終了日 | DATE |  | ○ |  | 有効終了日 |
| is_system_permission | システム権限フラグ | BOOLEAN |  | ○ | False | システム権限フラグ |
| parent_permission_id | 親権限ID | VARCHAR | 50 | ○ |  | 親権限ID |
| permission_category | 権限カテゴリ | ENUM |  | ○ |  | 権限カテゴリ |
| permission_code | 権限コード | VARCHAR | 50 | ○ |  | 権限コード |
| permission_id | MST_Permissionの主キー | SERIAL |  | × |  | MST_Permissionの主キー |
| permission_name | 権限名 | VARCHAR | 100 | ○ |  | 権限名 |
| permission_name_short | 権限名略称 | VARCHAR | 50 | ○ |  | 権限名略称 |
| permission_status | 権限状態 | ENUM |  | ○ | ACTIVE | 権限状態 |
| requires_approval | 承認要求フラグ | BOOLEAN |  | ○ | False | 承認要求フラグ |
| requires_conditions | 条件要求フラグ | BOOLEAN |  | ○ | False | 条件要求フラグ |
| resource_type | リソース種別 | VARCHAR | 50 | ○ |  | リソース種別 |
| risk_level | リスクレベル | INT |  | ○ | 1 | リスクレベル |
| scope_level | スコープレベル | ENUM |  | ○ |  | スコープレベル |
| sort_order | 表示順序 | INT |  | ○ |  | 表示順序 |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_permission_code | permission_code | ○ |  |
| idx_permission_category | permission_category | × |  |
| idx_resource_action | resource_type, action_type | × |  |
| idx_scope_level | scope_level | × |  |
| idx_parent_permission | parent_permission_id | × |  |
| idx_system_permission | is_system_permission | × |  |
| idx_risk_level | risk_level | × |  |
| idx_permission_status | permission_status | × |  |
| idx_effective_period | effective_from, effective_to | × |  |
| idx_mst_permission_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_permission_parent | parent_permission_id | MST_Permission | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| uk_permission_code | UNIQUE |  | permission_code一意制約 |
| chk_action_type | CHECK | action_type IN (...) | action_type値チェック制約 |
| chk_permission_status | CHECK | permission_status IN (...) | permission_status値チェック制約 |
| chk_resource_type | CHECK | resource_type IN (...) | resource_type値チェック制約 |
| chk_risk_level | CHECK | risk_level > 0 | risk_level正値チェック制約 |

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
- 権限コードは PERM_ + リソース + アクション 形式
- システム権限は is_system_permission = true で保護
- リスクレベル3以上は承認要求を推奨
- 全ての権限行使は監査ログに記録
- 条件付き権限は condition_expression で制御
- 親権限が無効化される場合は子権限も無効化
- 有効期間外の権限は自動的に無効化

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - 権限マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215053 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223432 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |