# テーブル定義書: HIS_AuditLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_AuditLog |
| 論理名 | 監査ログ |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-21 22:02:17 |

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
| auditlog_id | HIS_AuditLogの主キー | SERIAL |  | × |  | HIS_AuditLogの主キー |
| tenant_id | テナントID | VARCHAR | 50 | × |  | テナントID（マルチテナント対応） |
| created_at | 作成日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | × | CURRENT_TIMESTAMP | 更新日時 |
| id | プライマリキー | VARCHAR | 50 | × |  | プライマリキー（UUID） |
| is_deleted | 論理削除フラグ | BOOLEAN |  | × | False | 論理削除フラグ |

## インデックス

| インデックス名 | カラム | ユニーク | 説明 |
|----------------|--------|----------|------|
| idx_his_auditlog_tenant_id | tenant_id | × | テナントID検索用インデックス |

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_his_auditlog_tenant | None | None | None | CASCADE | RESTRICT | 外部キー制約 |
| fk_his_auditlog_user | None | None | None | CASCADE | RESTRICT | 外部キー制約 |

## 制約

| 制約名 | 種別 | 条件 | 説明 |
|--------|------|------|------|
| pk_his_auditlog | PRIMARY KEY | auditlog_id, id | 主キー制約 |

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