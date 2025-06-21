# テーブル定義書: HIS_AuditLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_AuditLog |
| 論理名 | 監査ログ |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-21 17:20:34 |

## 概要

システム内で発生する全ての重要な操作を記録する監査ログテーブルです。
主な目的：
- セキュリティ監査のための操作履歴記録
- システム不正利用の検知・追跡
- コンプライアンス要件への対応
- トラブルシューティング時の操作履歴確認
このテーブルは法的要件やセキュリティポリシーに基づき、
90日間のログ保持期間を設けています。


## カラム定義

| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |
|----------|--------|----------|------|------|------------|------|
| id |  | VARCHAR |  | ○ |  |  |
| user_id |  | VARCHAR |  | ○ |  |  |
| session_id |  | VARCHAR |  | ○ |  |  |
| action_type |  | ENUM |  | ○ |  |  |
| target_table |  | VARCHAR |  | ○ |  |  |
| target_id |  | VARCHAR |  | ○ |  |  |
| old_values |  | TEXT |  | ○ |  |  |
| new_values |  | TEXT |  | ○ |  |  |
| ip_address |  | VARCHAR |  | ○ |  |  |
| user_agent |  | VARCHAR |  | ○ |  |  |
| result_status |  | ENUM |  | ○ | SUCCESS |  |
| error_message |  | TEXT |  | ○ |  |  |
| execution_time_ms |  | INTEGER |  | ○ |  |  |
| is_deleted |  | BOOLEAN |  | ○ | False |  |
| tenant_id |  | VARCHAR |  | ○ |  |  |
| created_at |  | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP |  |
| updated_at |  | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP |  |
| created_by |  | VARCHAR |  | ○ |  |  |
| updated_by |  | VARCHAR |  | ○ |  |  |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_his_auditlog_id | id | ○ |  |
| idx_his_auditlog_user_id | user_id | × |  |
| idx_his_auditlog_tenant_id | tenant_id | × |  |
| idx_his_auditlog_action_type | action_type | × |  |
| idx_his_auditlog_target_table | target_table | × |  |
| idx_his_auditlog_created_at | created_at | × |  |
| idx_his_auditlog_user_created | user_id, created_at | × |  |
| idx_his_auditlog_tenant_created | tenant_id, created_at | × |  |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| uk_id | UNIQUE |  | id一意制約 |
| chk_action_type | CHECK | action_type IN (...) | action_type値チェック制約 |
| chk_result_status | CHECK | result_status IN (...) | result_status値チェック制約 |

## サンプルデータ

| id | user_id | session_id | action_type | target_table | target_id | old_values | new_values | ip_address | user_agent | result_status | error_message | execution_time_ms | is_deleted | tenant_id | created_by | updated_by |
|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|------|
| audit_001 | emp_001 | sess_abc123 | LOGIN | None | None | None | None | 192.168.1.100 | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 | SUCCESS | None | 150 | False | tenant_001 | system | system |
| audit_002 | emp_001 | sess_abc123 | UPDATE | MST_Employee | emp_001 | {"name": "田中太郎", "email": "tanaka@example.com"} | {"name": "田中太郎", "email": "tanaka.new@example.com"} | 192.168.1.100 | Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 | SUCCESS | None | 250 | False | tenant_001 | emp_001 | emp_001 |

## 特記事項

- 監査ログは法的要件により90日間保持が必要
- 機密情報（old_values, new_values）は暗号化して保存
- 物理削除は禁止、論理削除のみ許可
- 大量データ対応のため、パーティショニング検討が必要
- ログ検索性能向上のため、適切なインデックス設計が重要
- セキュリティ監査要件に基づく設計

## 業務ルール

- 全ての重要な操作（CRUD、認証）を記録する
- ログの改ざん防止のため、作成後の更新は原則禁止
- 個人情報を含む場合は暗号化して保存
- システム管理者のみがログを参照可能
- ログ保持期間は90日間、期間経過後は自動削除
- 異常なアクセスパターンの検知に活用

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - HIS_AuditLogの詳細定義 |