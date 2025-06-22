# テーブル定義書: MST_RolePermission

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_RolePermission |
| 論理名 | ロール権限紐付け |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 22:37:20 |

## 概要

MST_RolePermission（ロール権限紐付け）は、ロールと権限の多対多関係を管理するマスタテーブルです。
主な目的：
- ロールベースアクセス制御（RBAC）の実現
- 権限付与・取消の履歴管理と監査証跡の保持
- 細粒度な権限制御による情報セキュリティの確保
- 権限変更の追跡可能性とコンプライアンス対応
- システム機能へのアクセス制御の柔軟な管理
このテーブルは、システムのセキュリティ基盤として重要な役割を果たし、
適切な権限管理により情報漏洩や不正アクセスを防止します。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| role_permission_id | ロール権限紐付けの一意識別子 | BIGINT |  | × |  | ロール権限紐付けの一意識別子 |
| role_id | 権限を付与するロールのID | BIGINT |  | × |  | 権限を付与するロールのID |
| permission_id | ロールに付与する権限のID | BIGINT |  | × |  | ロールに付与する権限のID |
| is_active | この権限付与が有効かどうか | BOOLEAN |  | × | True | この権限付与が有効かどうか |
| granted_at | この権限がロールに付与された日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | この権限がロールに付与された日時 |
| granted_by | この権限を付与したユーザーのID | BIGINT |  | × |  | この権限を付与したユーザーのID |
| revoked_at | この権限が取り消された日時 | TIMESTAMP |  | ○ |  | この権限が取り消された日時（NULL=未取消） |
| revoked_by | この権限を取り消したユーザーのID | BIGINT |  | ○ |  | この権限を取り消したユーザーのID |
| notes | 権限付与・取消に関する備考 | TEXT |  | ○ |  | 権限付与・取消に関する備考 |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード最終更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード最終更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_mst_rolepermission_role_id | role_id | × |  |
| idx_mst_rolepermission_permission_id | permission_id | × |  |
| idx_mst_rolepermission_role_permission | role_id, permission_id | × |  |
| idx_mst_rolepermission_active | is_active, role_id | × |  |
| idx_mst_rolepermission_granted_at | granted_at | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_mst_rolepermission_role_id | None | None | None | CASCADE | CASCADE | ロールマスタへの外部キー制約 |
| fk_mst_rolepermission_permission_id | None | None | None | CASCADE | CASCADE | 権限マスタへの外部キー制約 |
| fk_mst_rolepermission_granted_by | None | None | None | CASCADE | RESTRICT | 権限付与者への外部キー制約 |
| fk_mst_rolepermission_revoked_by | None | None | None | CASCADE | RESTRICT | 権限取消者への外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_mst_rolepermission | PRIMARY KEY | role_permission_id | 主キー制約 |

## サンプルデータ

| role_permission_id | role_id | permission_id | is_active | granted_at | granted_by | revoked_at | revoked_by | notes | created_at | updated_at |
|------|------|------|------|------|------|------|------|------|------|------|
| 1 | 1 | 1 | True | 2024-01-01 00:00:00 | 1 | None | None | システム管理者の基本権限 | 2024-01-01 00:00:00 | 2024-01-01 00:00:00 |
| 2 | 1 | 2 | True | 2024-01-01 00:00:00 | 1 | None | None | システム管理者の基本権限 | 2024-01-01 00:00:00 | 2024-01-01 00:00:00 |
| 3 | 1 | 3 | True | 2024-01-01 00:00:00 | 1 | None | None | システム管理者の基本権限 | 2024-01-01 00:00:00 | 2024-01-01 00:00:00 |

## 特記事項

- ロールと権限の多対多関係を管理する中間テーブル
- 権限の付与・取消履歴を管理し、監査証跡を保持
- 有効フラグにより論理削除を実現
- 権限変更時は新しいレコードを作成し、古いレコードを無効化

## 業務ルール

- ロールと権限の組み合わせは一意である必要がある
- 権限の取消時は論理削除を行い、履歴を保持する
- 権限変更は必ず承認者の記録と共に実施する

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-21 | 開発チーム | 初版作成 - ロール権限紐付けテーブルの詳細定義 |