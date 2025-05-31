# テーブル定義書_HIS_AuditLog_監査ログ

## テーブル概要

| 項目 | 内容 |
|------|------|
| テーブル名（物理） | HIS_AuditLog |
| テーブル名（論理） | 監査ログ |
| 用途 | システム操作の監査証跡を記録する履歴テーブル |
| カテゴリ | 履歴系 |
| 主な利用機能 | 認証・認可・システム管理 |
| 主な利用API | API-022 |
| 主な利用バッチ | BATCH-003, BATCH-014 |
| 優先度 | 高 |

## カラム定義

| No | カラム名（物理） | カラム名（論理） | データ型 | 桁数 | NULL許可 | デフォルト値 | 主キー | 外部キー | 説明 |
|----|------------------|------------------|----------|------|----------|--------------|--------|----------|------|
| 1 | audit_log_id | 監査ログID | VARCHAR | 20 | × | - | ○ | - | 監査ログの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 20 | × | - | - | MST_Tenant.tenant_id | テナント識別子 |
| 3 | user_id | ユーザーID | VARCHAR | 20 | ○ | NULL | - | MST_UserAuth.user_id | 操作実行ユーザー |
| 4 | session_id | セッションID | VARCHAR | 50 | ○ | NULL | - | - | セッション識別子 |
| 5 | operation_type | 操作種別 | VARCHAR | 20 | × | - | - | - | 操作の種別（LOGIN/LOGOUT/CREATE/UPDATE/DELETE/VIEW等） |
| 6 | operation_category | 操作カテゴリ | VARCHAR | 50 | × | - | - | - | 操作対象のカテゴリ（USER/SKILL/REPORT等） |
| 7 | target_table | 対象テーブル | VARCHAR | 50 | ○ | NULL | - | - | 操作対象のテーブル名 |
| 8 | target_id | 対象ID | VARCHAR | 50 | ○ | NULL | - | - | 操作対象のレコードID |
| 9 | operation_description | 操作説明 | VARCHAR | 200 | × | - | - | - | 操作内容の説明 |
| 10 | before_data | 変更前データ | TEXT | - | ○ | NULL | - | - | 変更前のデータ（JSON形式） |
| 11 | after_data | 変更後データ | TEXT | - | ○ | NULL | - | - | 変更後のデータ（JSON形式） |
| 12 | ip_address | IPアドレス | VARCHAR | 45 | ○ | NULL | - | - | 操作元のIPアドレス |
| 13 | user_agent | ユーザーエージェント | VARCHAR | 500 | ○ | NULL | - | - | 操作元のユーザーエージェント |
| 14 | request_url | リクエストURL | VARCHAR | 500 | ○ | NULL | - | - | 操作時のリクエストURL |
| 15 | request_method | リクエストメソッド | VARCHAR | 10 | ○ | NULL | - | - | HTTPメソッド（GET/POST/PUT/DELETE等） |
| 16 | response_status | レスポンスステータス | INT | - | ○ | NULL | - | - | HTTPレスポンスステータスコード |
| 17 | execution_time | 実行時間 | INT | - | ○ | NULL | - | - | 処理実行時間（ミリ秒） |
| 18 | error_message | エラーメッセージ | TEXT | - | ○ | NULL | - | - | エラー発生時のメッセージ |
| 19 | risk_level | リスクレベル | VARCHAR | 10 | × | 'LOW' | - | - | 操作のリスクレベル（LOW/MEDIUM/HIGH/CRITICAL） |
| 20 | is_suspicious | 疑わしい操作フラグ | BOOLEAN | - | × | FALSE | - | - | 疑わしい操作の判定フラグ |
| 21 | created_at | 作成日時 | TIMESTAMP | - | × | CURRENT_TIMESTAMP | - | - | レコード作成日時 |

## インデックス定義

| インデックス名 | 種別 | 対象カラム | 説明 |
|----------------|------|------------|------|
| PK_HIS_AuditLog | PRIMARY KEY | audit_log_id | 主キー |
| IDX_HIS_AuditLog_tenant | INDEX | tenant_id | テナント検索用 |
| IDX_HIS_AuditLog_user | INDEX | user_id | ユーザー検索用 |
| IDX_HIS_AuditLog_operation | INDEX | operation_type, operation_category | 操作種別検索用 |
| IDX_HIS_AuditLog_target | INDEX | target_table, target_id | 操作対象検索用 |
| IDX_HIS_AuditLog_created | INDEX | created_at | 作成日時検索用 |
| IDX_HIS_AuditLog_risk | INDEX | risk_level | リスクレベル検索用 |
| IDX_HIS_AuditLog_suspicious | INDEX | is_suspicious | 疑わしい操作検索用 |
| IDX_HIS_AuditLog_ip | INDEX | ip_address | IPアドレス検索用 |

## 制約定義

| 制約名 | 種別 | 対象カラム | 説明 |
|--------|------|------------|------|
| PK_HIS_AuditLog | PRIMARY KEY | audit_log_id | 主キー制約 |
| FK_HIS_AuditLog_tenant | FOREIGN KEY | tenant_id | テナントマスタ参照制約 |
| FK_HIS_AuditLog_user | FOREIGN KEY | user_id | ユーザー認証情報参照制約 |
| CHK_HIS_AuditLog_operation_type | CHECK | operation_type | operation_type IN ('LOGIN','LOGOUT','CREATE','UPDATE','DELETE','VIEW','EXPORT','IMPORT','ADMIN') |
| CHK_HIS_AuditLog_risk_level | CHECK | risk_level | risk_level IN ('LOW','MEDIUM','HIGH','CRITICAL') |
| CHK_HIS_AuditLog_response_status | CHECK | response_status | response_status >= 100 AND response_status <= 599 |
| CHK_HIS_AuditLog_execution_time | CHECK | execution_time | execution_time >= 0 |

## 関連テーブル

### 参照先テーブル
- MST_Tenant（テナント管理）
- MST_UserAuth（ユーザー認証情報）

### 参照元テーブル
- なし（履歴テーブルのため）

## 備考・注意事項

### 業務ルール
1. すべてのシステム操作は監査ログに記録される
2. 個人情報を含むデータの変更は必ず変更前後のデータを記録する
3. 高リスク操作（削除、管理者権限操作等）は詳細な情報を記録する
4. 疑わしい操作は自動的にフラグが設定される
5. ログの改ざんは禁止され、追記のみ許可される

### 運用上の注意
- 大量のログが生成されるため、定期的なアーカイブが必要
- パフォーマンスに影響しないよう非同期でログ記録を行う
- 機密情報がログに含まれないよう注意する
- 法的要件に応じた保存期間を設定する

### パフォーマンス考慮事項
- 作成日時での範囲検索が頻繁に行われるためインデックスを設定
- テナント、ユーザー、操作種別での検索が多いためインデックスを設定
- パーティショニングによる性能向上を検討する

### セキュリティ考慮事項
- テナント分離を確実に行い、他テナントのログにアクセスできないようにする
- ログの改ざんを防ぐため、適切なアクセス制御を行う
- 機密情報のマスキング処理を実装する
- 不正アクセスの検知機能を実装する

### データ保持ポリシー
- 監査ログは法的要件に応じて長期間保持する（例：7年間）
- 古いログは圧縮してアーカイブストレージに移動する
- 個人情報保護法に応じた削除要求への対応を考慮する

### 監査要件
- 金融業界等の規制要件に対応した監査証跡を提供する
- 改ざん検知機能を実装する
- 定期的な監査レポートの生成機能を提供する
