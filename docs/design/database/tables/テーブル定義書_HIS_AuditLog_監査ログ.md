# テーブル定義書: HIS_AuditLog (監査ログ)

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | HIS_AuditLog |
| 論理名 | 監査ログ |
| カテゴリ | 履歴系 |
| 作成日 | 2025-06-01 |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/HIS_AuditLog_details.yaml` で行ってください。


## 📝 改版履歴

> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：
> `table-details/TABLE_NAME_details.yaml`

| バージョン | 更新日 | 更新者 | 主な変更内容 |
|------------|--------|--------|-------------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - HIS_AuditLogの詳細定義 |


## 📝 テーブル概要

システム内で発生する全ての重要な操作を記録する監査ログテーブルです。

主な目的：
- セキュリティ監査のための操作履歴記録
- システム不正利用の検知・追跡
- コンプライアンス要件への対応
- トラブルシューティング時の操作履歴確認

このテーブルは法的要件やセキュリティポリシーに基づき、
90日間のログ保持期間を設けています。


## 🗂️ カラム定義

| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |
|----------|--------|----------|------|------|----|----|------------|------|
| id | ID | VARCHAR | 50 | × | ● |  |  | プライマリキー（UUID） |
| is_deleted | 削除フラグ | BOOLEAN |  | × |  |  |  | 論理削除フラグ |
| tenant_id | テナントID | VARCHAR | 50 | × |  | ● |  | マルチテナント識別子 |
| id | ID | VARCHAR | 50 | ○ |  |  |  | プライマリキー（UUID） |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | ● |  | 操作を実行したユーザーのID |
| session_id | セッションID | VARCHAR | 100 | ○ |  |  |  | 操作時のセッション識別子 |
| action_type | アクション種別 | ENUM |  | ○ |  |  |  | 実行されたアクションの種別（CREATE:作成、READ:参照、UPDATE:更新、DELETE:削除、LOGIN:ログイン、LOGOUT:ログアウト） |
| target_table | 対象テーブル | VARCHAR | 100 | ○ |  |  |  | 操作対象のテーブル名 |
| target_id | 対象レコードID | VARCHAR | 50 | ○ |  |  |  | 操作対象のレコードID |
| old_values | 変更前値 | TEXT |  | ○ |  |  |  | 更新・削除前のデータ（JSON形式） |
| new_values | 変更後値 | TEXT |  | ○ |  |  |  | 作成・更新後のデータ（JSON形式） |
| ip_address | IPアドレス | VARCHAR | 45 | ○ |  |  |  | 操作元のIPアドレス（IPv6対応） |
| user_agent | ユーザーエージェント | VARCHAR | 500 | ○ |  |  |  | 操作時のブラウザ・アプリケーション情報 |
| result_status | 実行結果 | ENUM |  | ○ |  |  | SUCCESS | 操作の実行結果（SUCCESS:成功、FAILURE:失敗、ERROR:エラー） |
| error_message | エラーメッセージ | TEXT |  | ○ |  |  |  | 操作失敗時のエラーメッセージ |
| execution_time_ms | 実行時間 | INTEGER |  | ○ |  |  |  | 操作の実行時間（ミリ秒） |
| is_deleted | 削除フラグ | BOOLEAN |  | ○ |  |  |  | 論理削除フラグ（監査ログは物理削除禁止） |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | ● |  | マルチテナント識別子 |
| created_at | 作成日時 | TIMESTAMP |  | ○ |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | ○ |  |  | CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | ○ |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | ○ |  |  |  | レコード更新者のユーザーID |
| created_at | 作成日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP | レコード作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × |  |  | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| created_by | 作成者 | VARCHAR | 50 | × |  |  |  | レコード作成者のユーザーID |
| updated_by | 更新者 | VARCHAR | 50 | × |  |  |  | レコード更新者のユーザーID |

## 🔍 インデックス定義

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_his_auditlog_id | id | ○ | プライマリキー検索用（一意） |
| idx_his_auditlog_user_id | user_id | × | ユーザーID検索用 |
| idx_his_auditlog_tenant_id | tenant_id | × | テナントID検索用 |
| idx_his_auditlog_action_type | action_type | × | アクション種別検索用 |
| idx_his_auditlog_target_table | target_table | × | 対象テーブル検索用 |
| idx_his_auditlog_created_at | created_at | × | 作成日時検索用（時系列検索） |
| idx_his_auditlog_user_created | user_id, created_at | × | ユーザー別時系列検索用 |
| idx_his_auditlog_tenant_created | tenant_id, created_at | × | テナント別時系列検索用 |

## 🔒 制約定義

| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |
|--------|------------|------------|------|------|
| chk_his_auditlog_action_type | CHECK |  | action_type IN ('CREATE', 'READ', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT') | アクション種別値チェック制約 |
| chk_his_auditlog_result_status | CHECK |  | result_status IN ('SUCCESS', 'FAILURE', 'ERROR') | 実行結果値チェック制約 |
| chk_his_auditlog_execution_time_positive | CHECK |  | execution_time_ms IS NULL OR execution_time_ms >= 0 | 実行時間非負数チェック制約 |

## 🔗 外部キー関係

| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|------------|--------|--------------|------------|--------|--------|------|
| fk_his_auditlog_tenant | tenant_id | MST_Tenant | id | CASCADE | RESTRICT | テナントマスタへの外部キー |
| fk_his_auditlog_user | user_id | MST_Employee | id | CASCADE | RESTRICT | 社員マスタへの外部キー |

## 📊 サンプルデータ

```json
[
  {
    "id": "audit_001",
    "user_id": "emp_001",
    "session_id": "sess_abc123",
    "action_type": "LOGIN",
    "target_table": null,
    "target_id": null,
    "old_values": null,
    "new_values": null,
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "result_status": "SUCCESS",
    "error_message": null,
    "execution_time_ms": 150,
    "is_deleted": false,
    "tenant_id": "tenant_001",
    "created_by": "system",
    "updated_by": "system"
  },
  {
    "id": "audit_002",
    "user_id": "emp_001",
    "session_id": "sess_abc123",
    "action_type": "UPDATE",
    "target_table": "MST_Employee",
    "target_id": "emp_001",
    "old_values": "{\"name\": \"田中太郎\", \"email\": \"tanaka@example.com\"}",
    "new_values": "{\"name\": \"田中太郎\", \"email\": \"tanaka.new@example.com\"}",
    "ip_address": "192.168.1.100",
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "result_status": "SUCCESS",
    "error_message": null,
    "execution_time_ms": 250,
    "is_deleted": false,
    "tenant_id": "tenant_001",
    "created_by": "emp_001",
    "updated_by": "emp_001"
  }
]
```

## 📌 特記事項

- 監査ログは法的要件により90日間保持が必要
- 機密情報（old_values, new_values）は暗号化して保存
- 物理削除は禁止、論理削除のみ許可
- 大量データ対応のため、パーティショニング検討が必要
- ログ検索性能向上のため、適切なインデックス設計が重要
- セキュリティ監査要件に基づく設計

## 📋 業務ルール

- 全ての重要な操作（CRUD、認証）を記録する
- ログの改ざん防止のため、作成後の更新は原則禁止
- 個人情報を含む場合は暗号化して保存
- システム管理者のみがログを参照可能
- ログ保持期間は90日間、期間経過後は自動削除
- 異常なアクセスパターンの検知に活用
