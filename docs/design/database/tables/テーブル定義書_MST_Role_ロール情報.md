# テーブル定義書: MST_Role

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_Role |
| 論理名 | ロール情報 |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:21:58 |

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
| role_code |  | VARCHAR |  | ○ |  |  |
| role_name |  | VARCHAR |  | ○ |  |  |
| role_name_short |  | VARCHAR |  | ○ |  |  |
| role_category |  | ENUM |  | ○ |  |  |
| role_level |  | INT |  | ○ |  |  |
| parent_role_id |  | VARCHAR |  | ○ |  |  |
| is_system_role |  | BOOLEAN |  | ○ | False |  |
| is_tenant_specific |  | BOOLEAN |  | ○ | False |  |
| max_users |  | INT |  | ○ |  |  |
| role_priority |  | INT |  | ○ | 999 |  |
| auto_assign_conditions |  | JSON |  | ○ |  |  |
| role_status |  | ENUM |  | ○ | ACTIVE |  |
| effective_from |  | DATE |  | ○ |  |  |
| effective_to |  | DATE |  | ○ |  |  |
| sort_order |  | INT |  | ○ |  |  |
| description |  | TEXT |  | ○ |  |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

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

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
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