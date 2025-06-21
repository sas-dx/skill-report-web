# テーブル定義書: MST_UserRole

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_UserRole |
| 論理名 | ユーザーロール紐付け |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-21 17:20:34 |

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
| user_id |  | VARCHAR |  | ○ |  |  |
| role_id |  | VARCHAR |  | ○ |  |  |
| assignment_type |  | ENUM |  | ○ | DIRECT |  |
| assigned_by |  | VARCHAR |  | ○ |  |  |
| assignment_reason |  | TEXT |  | ○ |  |  |
| effective_from |  | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP |  |
| effective_to |  | TIMESTAMP |  | ○ |  |  |
| is_primary_role |  | BOOLEAN |  | ○ | False |  |
| priority_order |  | INT |  | ○ | 999 |  |
| conditions |  | JSON |  | ○ |  |  |
| delegation_source_user_id |  | VARCHAR |  | ○ |  |  |
| delegation_expires_at |  | TIMESTAMP |  | ○ |  |  |
| auto_assigned |  | BOOLEAN |  | ○ | False |  |
| requires_approval |  | BOOLEAN |  | ○ | False |  |
| approval_status |  | ENUM |  | ○ |  |  |
| approved_by |  | VARCHAR |  | ○ |  |  |
| approved_at |  | TIMESTAMP |  | ○ |  |  |
| assignment_status |  | ENUM |  | ○ | ACTIVE |  |
| last_used_at |  | TIMESTAMP |  | ○ |  |  |
| usage_count |  | INT |  | ○ | 0 |  |
| created_at | レコード作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | レコード更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | レコード更新日時 |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_user_role | user_id, role_id | ○ |  |
| idx_user_id | user_id | × |  |
| idx_role_id | role_id | × |  |
| idx_assignment_type | assignment_type | × |  |
| idx_assigned_by | assigned_by | × |  |
| idx_effective_period | effective_from, effective_to | × |  |
| idx_primary_role | user_id, is_primary_role | × |  |
| idx_assignment_status | assignment_status | × |  |
| idx_approval_status | approval_status | × |  |
| idx_delegation_source | delegation_source_user_id | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| chk_assignment_type | CHECK | assignment_type IN (...) | assignment_type値チェック制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |
| chk_assignment_status | CHECK | assignment_status IN (...) | assignment_status値チェック制約 |

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