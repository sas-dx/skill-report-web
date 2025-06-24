# テーブル定義書: MST_UserRole

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | MST_UserRole |
| 論理名 | ユーザーロール紐付け |
| カテゴリ | マスタ系 |
| 生成日時 | 2025-06-24 23:02:18 |

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
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| approval_status | 承認状態 | ENUM |  | ○ |  | 承認状態 |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  | 承認日時 |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | 承認者ID |
| assigned_by | 割り当て者ID | VARCHAR | 50 | ○ |  | 割り当て者ID |
| assignment_reason | 割り当て理由 | TEXT |  | ○ |  | 割り当て理由 |
| assignment_status | 割り当て状態 | ENUM |  | ○ | ACTIVE | 割り当て状態 |
| assignment_type | 割り当て種別 | ENUM |  | ○ | DIRECT | 割り当て種別 |
| auto_assigned | 自動割り当てフラグ | BOOLEAN |  | ○ | False | 自動割り当てフラグ |
| conditions | 適用条件 | JSON |  | ○ |  | 適用条件 |
| delegation_expires_at | 委譲期限 | TIMESTAMP |  | ○ |  | 委譲期限 |
| delegation_source_user_id | 委譲元ユーザーID | VARCHAR | 50 | ○ |  | 委譲元ユーザーID |
| effective_from | 有効開始日時 | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP | 有効開始日時 |
| effective_to | 有効終了日時 | TIMESTAMP |  | ○ |  | 有効終了日時 |
| is_primary_role | 主ロールフラグ | BOOLEAN |  | ○ | False | 主ロールフラグ |
| last_used_at | 最終使用日時 | TIMESTAMP |  | ○ |  | 最終使用日時 |
| priority_order | 優先順序 | INT |  | ○ | 999 | 優先順序 |
| requires_approval | 承認要求フラグ | BOOLEAN |  | ○ | False | 承認要求フラグ |
| role_id | ロールID | VARCHAR | 50 | ○ |  | ロールID |
| usage_count | 使用回数 | INT |  | ○ | 0 | 使用回数 |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | ユーザーID |
| userrole_id | MST_UserRoleの主キー | SERIAL |  | × |  | MST_UserRoleの主キー |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |

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
| idx_mst_userrole_tenant_id | tenant_id | × |  |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_userrole_user | user_id | MST_UserAuth | user_id | CASCADE | CASCADE | 外部キー制約 |
| fk_userrole_role | role_id | MST_Role | id | CASCADE | CASCADE | 外部キー制約 |
| fk_userrole_assigned_by | assigned_by | MST_UserAuth | id | CASCADE | SET NULL | 外部キー制約 |
| fk_userrole_delegation_source | delegation_source_user_id | MST_UserAuth | id | CASCADE | SET NULL | 外部キー制約 |
| fk_userrole_approved_by | approved_by | MST_UserAuth | id | CASCADE | SET NULL | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_approval_status | CHECK | approval_status IN (...) | approval_status値チェック制約 |
| chk_assignment_status | CHECK | assignment_status IN (...) | assignment_status値チェック制約 |
| chk_assignment_type | CHECK | assignment_type IN (...) | assignment_type値チェック制約 |

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
- 1ユーザーにつき1つの主ロール（is_primary_role=true）のみ
- 有効期間外のロール割り当ては自動的に EXPIRED 状態に変更
- 委譲ロールは委譲期限で自動失効
- 承認要求ロールは承認完了まで使用不可
- ロール使用時は last_used_at と usage_count を更新
- 同一ユーザー・ロールの重複割り当ては不可
- 委譲元ユーザーが無効化された場合は委譲ロールも無効化

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - ユーザロール関連マスタテーブルの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214907 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_215000 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215054 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222631 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223433 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |