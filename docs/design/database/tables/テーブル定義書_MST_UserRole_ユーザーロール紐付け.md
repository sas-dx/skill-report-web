# テーブル定義書: MST_UserRole

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_UserRole |
| 論理名 | ユーザーロール紐付け |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:02:18 |

## 概要

MST_UserRole（ユーザーロール紐付け）は、ユーザーとロールの関連付けを管理するマスタテーブルです。
主な目的：
- ユーザーとロールの多対多関係管理
- 動的なロール割り当て・解除
- 時限ロール・条件付きロール割り当て
- ロール継承・委譲の管理
- 権限昇格・降格の履歴管理
- 職務分離・最小権限の原則実装
- 監査・コンプライアンス対応
このテーブルは、ユーザーの実際の権限を決定する重要な関連テーブルであり、
システムセキュリティの実装において中核的な役割を果たします。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| userrole_id | MST_UserRoleの主キー | SERIAL |  | × |  | MST_UserRoleの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_userrole_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_userrole_user | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_userrole_role | None | None | None | CASCADE | CASCADE | 外部キー制約 |
| fk_userrole_assigned_by | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_userrole_delegation_source | None | None | None | CASCADE | SET NULL | 外部キー制約 |
| fk_userrole_approved_by | None | None | None | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_userrole | PRIMARY KEY | userrole_id | 主キー制約 |

## サンプルデータ

| user_id | role_id | assignment_type | assigned_by | assignment_reason | effective_from | effective_to | is_primary_role | priority_order | conditions | delegation_source_user_id | delegation_expires_at | auto_assigned | requires_approval | approval_status | approved_by | approved_at | assignment_status | last_used_at | usage_count |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| USER000001 | ROLE003 | DIRECT | USER000000 | 新規ユーザー登録時の標準ロール割り当て | 2025-01-01 00:00:00 | None | True | 1 | None | None | None | True | False | None | None | None | ACTIVE | 2025-06-01 09:00:00 | 150 |
| USER000002 | ROLE002 | DIRECT | USER000001 | テナント管理者権限付与 | 2025-02-01 00:00:00 | None | True | 1 | {"tenant_id": "TENANT001"} | None | None | False | True | APPROVED | USER000001 | 2025-01-31 15:30:00 | ACTIVE | 2025-06-01 10:30:00 | 75 |

## 特記事項

- ユーザーとロールの多対多関係を管理
- 時限ロール・条件付きロールに対応
- 委譲ロールによる一時的権限移譲が可能
- 承認フローによる権限昇格制御
- 使用状況の追跡・監査が可能
- 主ロールによる基本権限の明確化

## 業務ルール

- 1ユーザーにつき1つの主ロール（is_primary_role=true）のみ
- 有効期間外のロール割り当ては自動的に EXPIRED 状態に変更
- 委譲ロールは委譲期限で自動失効
- 承認要求ロールは承認完了まで使用不可
- ロール使用時は last_used_at と usage_count を更新
- 同一ユーザー・ロールの重複割り当ては不可
- 委譲元ユーザーが無効化された場合は委譲ロールも無効化

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - ユーザロール関連マスタテーブルの詳細定義 |