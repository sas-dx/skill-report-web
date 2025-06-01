# テーブル定義書_HIS_AuditLog_監査ログ

## 基本情報

| 項目 | 内容 |
|------|------|
| テーブルID | TBL-005 |
| テーブル名 | HIS_AuditLog |
| 論理名 | 監査ログ |
| カテゴリ | 履歴系 |
| 優先度 | 高 |
| 作成日 | 2024-01-01 |
| 更新日 | 2024-01-01 |

## テーブル概要

### 概要・目的
システム内で発生するすべての重要な操作を記録し、セキュリティ監査とコンプライアンス要件を満たすための監査ログテーブル。

### 主な利用機能カテゴリ
- 認証・認可
- システム管理

### 関連API
- API-022: 監査ログ取得API

### 関連バッチ
- BATCH-003: セキュリティスキャンバッチ
- BATCH-014: ログクリーンアップバッチ

### 関連画面
- SCR-ACCESS: アクセス管理画面
- SCR-ADMIN: システム管理画面

## テーブル構造

### カラム定義

| # | カラム名 | 論理名 | データ型 | 桁数 | NULL | デフォルト | PK | FK | インデックス | 説明 |
|---|----------|--------|----------|------|------|------------|----|----|--------------|------|
| 1 | audit_log_id | 監査ログID | BIGINT | - | NOT NULL | AUTO_INCREMENT | ○ | - | PRIMARY | 監査ログの一意識別子 |
| 2 | tenant_id | テナントID | VARCHAR | 36 | NOT NULL | - | - | ○ | IDX_TENANT | テナント識別子 |
| 3 | user_id | ユーザーID | VARCHAR | 36 | NULL | - | - | ○ | IDX_USER | 操作実行ユーザー |
| 4 | session_id | セッションID | VARCHAR | 128 | NULL | - | - | - | IDX_SESSION | セッション識別子 |
| 5 | action_type | アクション種別 | VARCHAR | 50 | NOT NULL | - | - | - | IDX_ACTION | 操作種別（LOGIN, LOGOUT, CREATE, UPDATE, DELETE等） |
| 6 | resource_type | リソース種別 | VARCHAR | 100 | NOT NULL | - | - | - | IDX_RESOURCE | 操作対象リソース種別 |
| 7 | resource_id | リソースID | VARCHAR | 36 | NULL | - | - | - | IDX_RESOURCE_ID | 操作対象リソースID |
| 8 | ip_address | IPアドレス | VARCHAR | 45 | NULL | - | - | - | IDX_IP | 操作元IPアドレス（IPv6対応） |
| 9 | user_agent | ユーザーエージェント | TEXT | - | NULL | - | - | - | - | ブラウザ・アプリケーション情報 |
| 10 | request_method | リクエストメソッド | VARCHAR | 10 | NULL | - | - | - | - | HTTP メソッド（GET, POST等） |
| 11 | request_url | リクエストURL | VARCHAR | 2000 | NULL | - | - | - | - | アクセスURL |
| 12 | request_params | リクエストパラメータ | JSON | - | NULL | - | - | - | - | リクエストパラメータ（機密情報除く） |
| 13 | response_status | レスポンスステータス | INT | - | NULL | - | - | - | IDX_STATUS | HTTPステータスコード |
| 14 | execution_time | 実行時間 | INT | - | NULL | - | - | - | - | 処理実行時間（ミリ秒） |
| 15 | before_data | 変更前データ | JSON | - | NULL | - | - | - | - | 変更前のデータ（機密情報除く） |
| 16 | after_data | 変更後データ | JSON | - | NULL | - | - | - | - | 変更後のデータ（機密情報除く） |
| 17 | error_message | エラーメッセージ | TEXT | - | NULL | - | - | - | - | エラー発生時のメッセージ |
| 18 | risk_level | リスクレベル | ENUM | - | NOT NULL | 'LOW' | - | - | IDX_RISK | リスクレベル（LOW, MEDIUM, HIGH, CRITICAL） |
| 19 | compliance_flag | コンプライアンスフラグ | BOOLEAN | - | NOT NULL | FALSE | - | - | IDX_COMPLIANCE | コンプライアンス対象フラグ |
| 20 | retention_period | 保持期間 | INT | - | NOT NULL | 2555 | - | - | - | ログ保持期間（日数） |
| 21 | created_at | 作成日時 | TIMESTAMP | - | NOT NULL | CURRENT_TIMESTAMP | - | - | IDX_CREATED | レコード作成日時 |
| 22 | created_by | 作成者 | VARCHAR | 36 | NOT NULL | 'SYSTEM' | - | - | - | レコード作成者 |

### インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|---------------|------|--------|------|
| PRIMARY | PRIMARY KEY | audit_log_id | 主キー |
| IDX_TENANT_CREATED | COMPOSITE | tenant_id, created_at | テナント別時系列検索 |
| IDX_USER_ACTION | COMPOSITE | user_id, action_type, created_at | ユーザー別操作履歴 |
| IDX_RESOURCE_TYPE | INDEX | resource_type | リソース種別検索 |
| IDX_RISK_COMPLIANCE | COMPOSITE | risk_level, compliance_flag, created_at | リスク・コンプライアンス検索 |
| IDX_IP_SESSION | COMPOSITE | ip_address, session_id | セキュリティ分析用 |

### 制約定義

| 制約名 | 種別 | カラム | 説明 |
|--------|------|--------|------|
| FK_AUDIT_TENANT | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| FK_AUDIT_USER | FOREIGN KEY | user_id | MST_UserAuth.user_id |
| CHK_RISK_LEVEL | CHECK | risk_level | IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') |
| CHK_RETENTION_PERIOD | CHECK | retention_period | >= 1 AND <= 3650 |

## リレーション

### 親テーブル
- MST_Tenant (tenant_id)
- MST_UserAuth (user_id)

### 子テーブル
なし

## データ仕様

### データ例

```sql
INSERT INTO HIS_AuditLog VALUES
(1, 'tenant-001', 'user-001', 'sess-12345', 'LOGIN', 'USER_AUTH', 'user-001', '192.168.1.100', 'Mozilla/5.0...', 'POST', '/api/auth/login', '{"username":"***"}', 200, 150, NULL, '{"last_login":"2024-01-01 09:00:00"}', NULL, 'MEDIUM', TRUE, 2555, '2024-01-01 09:00:00', 'SYSTEM'),
(2, 'tenant-001', 'user-001', 'sess-12345', 'UPDATE', 'EMPLOYEE', 'emp-001', '192.168.1.100', 'Mozilla/5.0...', 'PUT', '/api/employees/emp-001', '{"department_id":"dept-002"}', 200, 85, '{"department_id":"dept-001"}', '{"department_id":"dept-002"}', NULL, 'LOW', FALSE, 2555, '2024-01-01 09:15:00', 'user-001');
```

### データ量見積もり
- 初期データ: 0件
- 月間増加: 約100,000件
- 年間増加: 約1,200,000件
- 3年後想定: 約3,600,000件

## 運用仕様

### バックアップ
- フルバックアップ: 日次
- 差分バックアップ: 4時間毎
- 保持期間: 3年

### パーティション
- パーティション種別: RANGE (created_at)
- パーティション単位: 月次
- 自動パーティション作成: 有効

### アーカイブ
- アーカイブ条件: 作成から2年経過
- アーカイブ先: 長期保存ストレージ
- アーカイブ形式: 圧縮JSON

## パフォーマンス

### アクセスパターン
1. **時系列検索**: created_at範囲指定での検索が最多
2. **ユーザー別検索**: 特定ユーザーの操作履歴検索
3. **リスク分析**: 高リスク操作の抽出
4. **コンプライアンス監査**: 特定期間の全操作ログ

### 性能要件
- 検索応答時間: 3秒以内
- 挿入性能: 1,000件/秒
- 同時接続数: 100セッション

### 最適化施策
- パーティション設計による検索性能向上
- 適切なインデックス設計
- 古いデータの自動アーカイブ

## セキュリティ

### アクセス制御
- 参照権限: システム管理者、監査担当者
- 更新権限: システムのみ（アプリケーション経由）
- 削除権限: なし（アーカイブのみ）

### データ保護
- 機密情報のマスキング
- 暗号化: 保存時暗号化
- 改ざん検知: チェックサム

### 監査要件
- すべての操作をログ記録
- ログの改ざん防止
- 法的要件への準拠

## 移行仕様

### データ移行
- 移行元: 既存ログファイル
- 移行方法: バッチ処理による段階的移行
- 移行期間: 1週間

### 移行後検証
- データ件数チェック
- 整合性チェック
- 性能テスト

## DDL

```sql
CREATE TABLE HIS_AuditLog (
    audit_log_id BIGINT AUTO_INCREMENT,
    tenant_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36),
    session_id VARCHAR(128),
    action_type VARCHAR(50) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id VARCHAR(36),
    ip_address VARCHAR(45),
    user_agent TEXT,
    request_method VARCHAR(10),
    request_url VARCHAR(2000),
    request_params JSON,
    response_status INT,
    execution_time INT,
    before_data JSON,
    after_data JSON,
    error_message TEXT,
    risk_level ENUM('LOW', 'MEDIUM', 'HIGH', 'CRITICAL') NOT NULL DEFAULT 'LOW',
    compliance_flag BOOLEAN NOT NULL DEFAULT FALSE,
    retention_period INT NOT NULL DEFAULT 2555,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(36) NOT NULL DEFAULT 'SYSTEM',
    
    PRIMARY KEY (audit_log_id),
    INDEX IDX_TENANT_CREATED (tenant_id, created_at),
    INDEX IDX_USER_ACTION (user_id, action_type, created_at),
    INDEX IDX_RESOURCE_TYPE (resource_type),
    INDEX IDX_RISK_COMPLIANCE (risk_level, compliance_flag, created_at),
    INDEX IDX_IP_SESSION (ip_address, session_id),
    
    CONSTRAINT FK_AUDIT_TENANT FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id),
    CONSTRAINT FK_AUDIT_USER FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id),
    CONSTRAINT CHK_RISK_LEVEL CHECK (risk_level IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')),
    CONSTRAINT CHK_RETENTION_PERIOD CHECK (retention_period >= 1 AND retention_period <= 3650)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(created_at) * 100 + MONTH(created_at)) (
    PARTITION p202401 VALUES LESS THAN (202402),
    PARTITION p202402 VALUES LESS THAN (202403),
    PARTITION p202403 VALUES LESS THAN (202404),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 特記事項

### 重要な設計上の考慮事項
1. **改ざん防止**: 一度作成されたログは更新・削除不可
2. **機密情報保護**: パスワード等の機密情報は記録しない
3. **法的要件**: 各国の法的要件に応じた保持期間設定
4. **性能考慮**: 大量データに対応したパーティション設計

### 運用上の注意点
1. **ディスク容量**: 大量のログデータによるディスク使用量増加
2. **アーカイブ**: 定期的な古いデータのアーカイブが必要
3. **監視**: ログ記録の失敗を監視する仕組みが必要
4. **コンプライアンス**: 定期的な監査ログの確認が必要

### 今後の拡張予定
1. **リアルタイム分析**: ストリーミング処理による即座の異常検知
2. **AI活用**: 機械学習による異常パターン検出
3. **外部連携**: SIEM等のセキュリティツールとの連携
4. **可視化**: ダッシュボードでの監査ログ可視化
