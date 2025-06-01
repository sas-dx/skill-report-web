# テーブル定義書: MST_UserRole (ユーザーロール紐付け)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | MST_UserRole |
| 論理名 | ユーザーロール紐付け |
| カテゴリ | マスタ系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/MST_UserRole_details.yaml` で行ってください。



## 📝 テーブル概要

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


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  |  |  | マルチテナント識別子 |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | ● |  | ユーザーのID（MST_UserAuthへの外部キー） |
| role_id | ロールID | VARCHAR | 50 | ○ |  | ● |  | ロールのID（MST_Roleへの外部キー） |
| assignment_type | 割り当て種別 | ENUM |  | ○ |  |  | DIRECT | ロール割り当ての種別（DIRECT:直接、INHERITED:継承、DELEGATED:委譲、TEMPORARY:一時的） |
| assigned_by | 割り当て者ID | VARCHAR | 50 | ○ |  | ● |  | ロールを割り当てた管理者のID（MST_UserAuthへの外部キー） |
| assignment_reason | 割り当て理由 | TEXT |  | ○ |  |  |  | ロール割り当ての理由・根拠 |
| effective_from | 有効開始日時 | TIMESTAMP |  | ○ |  |  | CURRENT_TIMESTAMP | ロール割り当ての有効開始日時 |
| effective_to | 有効終了日時 | TIMESTAMP |  | ○ |  |  |  | ロール割り当ての有効終了日時 |
| is_primary_role | 主ロールフラグ | BOOLEAN |  | ○ |  |  |  | ユーザーの主要ロールかどうか |
| priority_order | 優先順序 | INT |  | ○ |  |  | 999 | 複数ロール保持時の優先順序（数値が小さいほど高優先） |
| conditions | 適用条件 | JSON |  | ○ |  |  |  | ロール適用の条件（時間帯、場所、状況等をJSON形式） |
| delegation_source_user_id | 委譲元ユーザーID | VARCHAR | 50 | ○ |  | ● |  | 委譲ロールの場合の委譲元ユーザーID |
| delegation_expires_at | 委譲期限 | TIMESTAMP |  | ○ |  |  |  | 委譲ロールの期限 |
| auto_assigned | 自動割り当てフラグ | BOOLEAN |  | ○ |  |  |  | システムによる自動割り当てかどうか |
| requires_approval | 承認要求フラグ | BOOLEAN |  | ○ |  |  |  | ロール行使に承認が必要かどうか |
| approval_status | 承認状態 | ENUM |  | ○ |  |  |  | 承認の状態（PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下） |
| approved_by | 承認者ID | VARCHAR | 50 | ○ |  | ● |  | ロール割り当てを承認した管理者のID |
| approved_at | 承認日時 | TIMESTAMP |  | ○ |  |  |  | ロール割り当てが承認された日時 |
| assignment_status | 割り当て状態 | ENUM |  | ○ |  |  | ACTIVE | 割り当ての状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、EXPIRED:期限切れ） |
| last_used_at | 最終使用日時 | TIMESTAMP |  | ○ |  |  |  | このロールが最後に使用された日時 |
| usage_count | 使用回数 | INT |  | ○ |  |  |  | このロールが使用された回数 |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_user_role | user_id, role_id | ○ | ユーザー・ロール組み合わせ検索用（一意） |
| idx_user_id | user_id | × | ユーザー別検索用 |
| idx_role_id | role_id | × | ロール別検索用 |
| idx_assignment_type | assignment_type | × | 割り当て種別検索用 |
| idx_assigned_by | assigned_by | × | 割り当て者別検索用 |
| idx_effective_period | effective_from, effective_to | × | 有効期間検索用 |
| idx_primary_role | user_id, is_primary_role | × | 主ロール検索用 |
| idx_assignment_status | assignment_status | × | 割り当て状態別検索用 |
| idx_approval_status | approval_status | × | 承認状態別検索用 |
| idx_delegation_source | delegation_source_user_id | × | 委譲元ユーザー検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| uk_user_role_active | UNIQUE | user_id, role_id, assignment_status |  | アクティブなユーザー・ロール組み合わせ一意制約 |
| chk_assignment_type | CHECK |  | assignment_type IN ('DIRECT', 'INHERITED', 'DELEGATED', 'TEMPORARY') | 割り当て種別値チェック制約 |
| chk_assignment_status | CHECK |  | assignment_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'EXPIRED') | 割り当て状態値チェック制約 |
| chk_approval_status | CHECK |  | approval_status IS NULL OR approval_status IN ('PENDING', 'APPROVED', 'REJECTED') | 承認状態値チェック制約 |
| chk_effective_period | CHECK |  | effective_to IS NULL OR effective_from <= effective_to | 有効期間整合性チェック制約 |
| chk_delegation_period | CHECK |  | delegation_expires_at IS NULL OR effective_from <= delegation_expires_at | 委譲期間整合性チェック制約 |
| chk_priority_order | CHECK |  | priority_order > 0 | 優先順序正値チェック制約 |
| chk_usage_count | CHECK |  | usage_count >= 0 | 使用回数非負値チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_userrole_user | user_id | MST_UserAuth | user_id | CASCADE | CASCADE | ユーザーへの外部キー |
| fk_userrole_role | role_id | MST_Role | id | CASCADE | CASCADE | ロールへの外部キー |
| fk_userrole_assigned_by | assigned_by | MST_UserAuth | user_id | CASCADE | SET NULL | 割り当て者への外部キー |
| fk_userrole_delegation_source | delegation_source_user_id | MST_UserAuth | user_id | CASCADE | SET NULL | 委譲元ユーザーへの外部キー |
| fk_userrole_approved_by | approved_by | MST_UserAuth | user_id | CASCADE | SET NULL | 承認者への外部キー |

## 📊 サンプルデータ

```json
[
  {
    "user_id": "USER000001",
    "role_id": "ROLE003",
    "assignment_type": "DIRECT",
    "assigned_by": "USER000000",
    "assignment_reason": "新規ユーザー登録時の標準ロール割り当て",
    "effective_from": "2025-01-01 00:00:00",
    "effective_to": null,
    "is_primary_role": true,
    "priority_order": 1,
    "conditions": null,
    "delegation_source_user_id": null,
    "delegation_expires_at": null,
    "auto_assigned": true,
    "requires_approval": false,
    "approval_status": null,
    "approved_by": null,
    "approved_at": null,
    "assignment_status": "ACTIVE",
    "last_used_at": "2025-06-01 09:00:00",
    "usage_count": 150
  },
  {
    "user_id": "USER000002",
    "role_id": "ROLE002",
    "assignment_type": "DIRECT",
    "assigned_by": "USER000001",
    "assignment_reason": "テナント管理者権限付与",
    "effective_from": "2025-02-01 00:00:00",
    "effective_to": null,
    "is_primary_role": true,
    "priority_order": 1,
    "conditions": "{\"tenant_id\": \"TENANT001\"}",
    "delegation_source_user_id": null,
    "delegation_expires_at": null,
    "auto_assigned": false,
    "requires_approval": true,
    "approval_status": "APPROVED",
    "approved_by": "USER000001",
    "approved_at": "2025-01-31 15:30:00",
    "assignment_status": "ACTIVE",
    "last_used_at": "2025-06-01 10:30:00",
    "usage_count": 75
  }
]
```

## 📌 特記事項

- ユーザーとロールの多対多関係を管理
- 時限ロール・条件付きロールに対応
- 委譲ロールによる一時的権限移譲が可能
- 承認フローによる権限昇格制御
- 使用状況の追跡・監査が可能
- 主ロールによる基本権限の明確化

## 📋 業務ルール

- 1ユーザーにつき1つの主ロール（is_primary_role=true）のみ
- 有効期間外のロール割り当ては自動的に EXPIRED 状態に変更
- 委譲ロールは委譲期限で自動失効
- 承認要求ロールは承認完了まで使用不可
- ロール使用時は last_used_at と usage_count を更新
- 同一ユーザー・ロールの重複割り当ては不可
- 委譲元ユーザーが無効化された場合は委譲ロールも無効化
