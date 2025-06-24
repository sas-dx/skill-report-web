# テーブル定義書: HIS_AuditLog

## 基本情報

| 項目 | 値 |
|------|-----|
| テーブル名 | HIS_AuditLog |
| 論理名 | 監査ログ |
| カテゴリ | 履歴系 |
| 生成日時 | 2025-06-24 23:05:57 |

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
| id | ID | VARCHAR | 50 | ○ |  | ID |
| tenant_id | テナントID | VARCHAR | 50 | ○ |  | テナントID |
| action_type | アクション種別 | ENUM |  | ○ |  | アクション種別 |
| auditlog_id | HIS_AuditLogの主キー | SERIAL |  | × |  | HIS_AuditLogの主キー |
| created_by | 作成者 | VARCHAR | 50 | ○ |  | 作成者 |
| error_message | エラーメッセージ | TEXT |  | ○ |  | エラーメッセージ |
| execution_time_ms | 実行時間 | INTEGER |  | ○ |  | 実行時間 |
| ip_address | IPアドレス | VARCHAR | 45 | ○ |  | IPアドレス |
| new_values | 変更後値 | TEXT |  | ○ |  | 変更後値 |
| old_values | 変更前値 | TEXT |  | ○ |  | 変更前値 |
| result_status | 実行結果 | ENUM |  | ○ | SUCCESS | 実行結果 |
| session_id | セッションID | VARCHAR | 100 | ○ |  | セッションID |
| target_id | 対象レコードID | VARCHAR | 50 | ○ |  | 対象レコードID |
| target_table | 対象テーブル | VARCHAR | 100 | ○ |  | 対象テーブル |
| updated_by | 更新者 | VARCHAR | 50 | ○ |  | 更新者 |
| user_agent | ユーザーエージェント | VARCHAR | 500 | ○ |  | ユーザーエージェント |
| user_id | ユーザーID | VARCHAR | 50 | ○ |  | ユーザーID |
| is_deleted | 削除フラグ | BOOLEAN |  | ○ | False | 削除フラグ |
| created_at | 作成日時 | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | 更新日時 | TIMESTAMP |  | ○ | CURRENT_TIMESTAMP | 更新日時 |

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

## 外部キー

| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |
|--------|--------|--------------|------------|--------|--------|------|
| fk_his_auditlog_tenant | tenant_id | MST_Tenant | id | CASCADE | RESTRICT | 外部キー制約 |
| fk_his_auditlog_user | user_id | MST_Employee | id | CASCADE | RESTRICT | 外部キー制約 |

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
- 全ての重要な操作（CRUD、認証）を記録する
- ログの改ざん防止のため、作成後の更新は原則禁止
- 個人情報を含む場合は暗号化して保存
- システム管理者のみがログを参照可能
- ログ保持期間は90日間、期間経過後は自動削除
- 異常なアクセスパターンの検知に活用

## 業務ルール

- 主キーの一意性は必須で変更不可
- 外部キー制約による参照整合性の保証
- 論理削除による履歴データの保持

## 改版履歴

| バージョン | 更新日 | 更新者 | 変更内容 |
|------------|--------|--------|----------|
| 1.0.0 | 2025-06-01 | 開発チーム | 初版作成 - HIS_AuditLogの詳細定義 |
| 2.0.0 | 2025-06-22 | 自動変換ツール | テンプレート形式への自動変換 |
| 3.1.20250624 | 2025-06-24 | 自動修正ツール | カラム順序を推奨順序に自動修正 |
| 4.0.20250624_213614 | 2025-06-24 | 自動修正ツール | カラム順序を統一テンプレートに従って自動修正 |
| 5.0.20250624_214006 | 2025-06-24 | 統一カラム順序修正ツール | カラム順序を統一テンプレート（Phase 1）に従って自動修正 |
| 10.0.20250624_214905 | 2025-06-24 | 最終カラム順序統一ツール | 要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正 |
| 11.0.20250624_214959 | 2025-06-24 | 最終カラム順序修正ツール（実構成対応版） | 実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正 |
| 12.0.20250624_215052 | 2025-06-24 | 現実的カラム順序修正ツール | 実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| 13.0.20250624_222630 | 2025-06-24 | ユーザー要求対応カラム順序修正ツール | ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分） |
| FINAL.20250624_223431 | 2025-06-24 | 最終カラム順序統一ツール | 推奨カラム順序テンプレートに従って最終統一 |