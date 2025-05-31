# テーブル定義書：トークン管理 (SYS_TokenStore)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-024 |
| **テーブル名** | SYS_TokenStore |
| **論理名** | トークン管理 |
| **カテゴリ** | システム系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
トークン管理テーブル（SYS_TokenStore）は、システムで使用される各種トークンを管理するシステムテーブルです。JWTトークン、リフレッシュトークン、APIトークン、パスワードリセットトークンなどを安全に保存し、トークンの有効性検証、期限管理、無効化処理を行います。セキュリティの要となるトークン管理機能の基盤を提供します。

### 2.2 関連API
- [API-001](../api/specs/API仕様書_API-001.md) - ユーザー認証API
- [API-002](../api/specs/API仕様書_API-002.md) - トークン管理API

### 2.3 関連バッチ
- [BATCH-017](../batch/specs/バッチ定義書_BATCH-017.md) - トークン無効化バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | token_id | トークンID | VARCHAR | 50 | × | ○ | - | - | トークンを一意に識別するID |
| 2 | token_type | トークン種別 | VARCHAR | 50 | × | - | - | - | トークンの種別（JWT/REFRESH/API/RESET等） |
| 3 | token_value | トークン値 | TEXT | - | × | - | - | - | トークンの値（ハッシュ化済み） |
| 4 | token_hash | トークンハッシュ | VARCHAR | 255 | × | - | - | - | トークンのハッシュ値（検索用） |
| 5 | user_id | ユーザーID | VARCHAR | 50 | × | - | MST_UserAuth.user_id | - | トークンの所有者 |
| 6 | client_id | クライアントID | VARCHAR | 100 | ○ | - | - | NULL | APIクライアントID |
| 7 | scope | スコープ | VARCHAR | 500 | ○ | - | - | NULL | トークンのスコープ（権限範囲） |
| 8 | issued_at | 発行日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | トークン発行日時 |
| 9 | expires_at | 有効期限 | TIMESTAMP | - | × | - | - | - | トークンの有効期限 |
| 10 | last_used_at | 最終使用日時 | TIMESTAMP | - | ○ | - | - | NULL | トークンの最終使用日時 |
| 11 | usage_count | 使用回数 | INTEGER | - | × | - | - | 0 | トークンの使用回数 |
| 12 | ip_address | IPアドレス | VARCHAR | 45 | ○ | - | - | NULL | トークン発行時のIPアドレス |
| 13 | user_agent | ユーザーエージェント | TEXT | - | ○ | - | - | NULL | トークン発行時のユーザーエージェント |
| 14 | device_info | デバイス情報 | TEXT | - | ○ | - | - | NULL | デバイス情報（JSON形式） |
| 15 | parent_token_id | 親トークンID | VARCHAR | 50 | ○ | - | SYS_TokenStore.token_id | NULL | 親トークンのID（リフレッシュトークンの場合） |
| 16 | child_token_count | 子トークン数 | INTEGER | - | × | - | - | 0 | 子トークンの数 |
| 17 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | トークンが有効かどうか |
| 18 | revocation_reason | 無効化理由 | VARCHAR | 100 | ○ | - | - | NULL | トークン無効化の理由 |
| 19 | revoked_at | 無効化日時 | TIMESTAMP | - | ○ | - | - | NULL | トークン無効化日時 |
| 20 | revoked_by | 無効化者 | VARCHAR | 50 | ○ | - | - | NULL | トークンを無効化したユーザーID |
| 21 | metadata | メタデータ | TEXT | - | ○ | - | - | NULL | 追加のメタデータ（JSON形式） |
| 22 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 23 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード更新日時 |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | token_id | 主キー |
| uk_token_hash | UNIQUE | token_hash | トークンハッシュの一意制約 |
| idx_token_type | INDEX | token_type | トークン種別での検索用 |
| idx_user_id | INDEX | user_id | ユーザーIDでの検索用 |
| idx_client_id | INDEX | client_id | クライアントIDでの検索用 |
| idx_expires_at | INDEX | expires_at | 有効期限での検索用 |
| idx_is_active | INDEX | is_active | 有効フラグでの検索用 |
| idx_parent_token_id | INDEX | parent_token_id | 親トークンでの検索用 |
| idx_issued_at | INDEX | issued_at | 発行日時での検索用 |
| idx_composite | INDEX | user_id, token_type, is_active | 複合検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_token_store | PRIMARY KEY | token_id | 主キー制約 |
| uk_token_hash | UNIQUE | token_hash | トークンハッシュ一意制約 |
| fk_token_user | FOREIGN KEY | user_id | MST_UserAuth(user_id) |
| fk_token_parent | FOREIGN KEY | parent_token_id | SYS_TokenStore(token_id) |
| chk_token_type | CHECK | token_type | token_type IN ('JWT', 'REFRESH', 'API', 'RESET', 'ACTIVATION', 'INVITATION') |
| chk_revocation_reason | CHECK | revocation_reason | revocation_reason IN ('EXPIRED', 'LOGOUT', 'SECURITY', 'ADMIN', 'USER_REQUEST') |
| chk_usage_count | CHECK | usage_count | usage_count >= 0 |
| chk_child_token_count | CHECK | child_token_count | child_token_count >= 0 |
| chk_expires_after_issued | CHECK | issued_at, expires_at | expires_at > issued_at |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | 関係 | 説明 |
|------------|------------|------|------|
| MST_UserAuth | user_id | N:1 | トークンの所有者 |
| SYS_TokenStore | parent_token_id | N:1 | 親トークン（自己参照） |

### 4.2 子テーブル
| テーブル名 | 関連カラム | 関係 | 説明 |
|------------|------------|------|------|
| SYS_TokenStore | parent_token_id | 1:N | 子トークン（自己参照） |

## 5. データ仕様

### 5.1 トークン種別定義
| 種別 | 説明 | 有効期限 | 用途 |
|------|------|----------|------|
| JWT | 認証用JWTトークン | 1時間 | API認証・セッション管理 |
| REFRESH | リフレッシュトークン | 30日間 | JWTトークンの更新 |
| API | API認証用トークン | 90日間 | 外部API連携 |
| RESET | パスワードリセット用 | 1時間 | パスワード再設定 |
| ACTIVATION | アカウント有効化用 | 24時間 | アカウント有効化 |
| INVITATION | 招待用トークン | 7日間 | ユーザー招待 |

### 5.2 無効化理由定義
| 理由 | 説明 | 対応 |
|------|------|------|
| EXPIRED | 期限切れ | 自動無効化 |
| LOGOUT | ログアウト | ユーザー操作 |
| SECURITY | セキュリティ上の理由 | 管理者判断 |
| ADMIN | 管理者による無効化 | 管理者操作 |
| USER_REQUEST | ユーザー要求 | ユーザー操作 |

### 5.3 データ例
```sql
-- JWTトークン
INSERT INTO SYS_TokenStore (
    token_id, token_type, token_hash, user_id, client_id,
    issued_at, expires_at, ip_address, is_active
) VALUES (
    'TKN_20250531_001',
    'JWT',
    'sha256_hash_value_1',
    'USR_001',
    'web-client',
    '2025-05-31 10:00:00',
    '2025-05-31 11:00:00',
    '192.168.1.100',
    TRUE
);

-- リフレッシュトークン
INSERT INTO SYS_TokenStore (
    token_id, token_type, token_hash, user_id, client_id,
    issued_at, expires_at, ip_address, is_active
) VALUES (
    'TKN_20250531_002',
    'REFRESH',
    'sha256_hash_value_2',
    'USR_001',
    'web-client',
    '2025-05-31 10:00:00',
    '2025-06-30 10:00:00',
    '192.168.1.100',
    TRUE
);

-- APIトークン
INSERT INTO SYS_TokenStore (
    token_id, token_type, token_hash, user_id, client_id,
    issued_at, expires_at, scope, is_active
) VALUES (
    'TKN_20250531_003',
    'API',
    'sha256_hash_value_3',
    'USR_002',
    'api-client',
    '2025-05-31 09:00:00',
    '2025-08-29 09:00:00',
    'read:skills,write:skills',
    TRUE
);

-- パスワードリセットトークン（使用済み）
INSERT INTO SYS_TokenStore (
    token_id, token_type, token_hash, user_id,
    issued_at, expires_at, is_active, revocation_reason, revoked_at
) VALUES (
    'TKN_20250531_004',
    'RESET',
    'sha256_hash_value_4',
    'USR_003',
    '2025-05-31 08:00:00',
    '2025-05-31 09:00:00',
    FALSE,
    'EXPIRED',
    '2025-05-31 09:00:01'
);
```

### 5.4 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 新規システム |
| 日次増加件数 | 1,000件 | ユーザー活動による |
| 年間想定件数 | 365,000件 | 365日分 |
| 保持期間 | 1年 | 監査要件 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：issued_at（月単位）

### 6.3 アーカイブ
- 期限切れトークン：1ヶ月後削除
- 無効化トークン：3ヶ月後削除
- 有効トークン：期限まで保持

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| INSERT | 高 | - | トークン発行 |
| SELECT | 極高 | token_hash | トークン検証 |
| SELECT | 高 | user_id, token_type | ユーザー別トークン取得 |
| UPDATE | 中 | last_used_at, usage_count | 使用履歴更新 |
| UPDATE | 中 | is_active, revoked_at | トークン無効化 |
| DELETE | 低 | expires_at < NOW() | 期限切れトークン削除 |

### 7.2 パフォーマンス要件
- SELECT（トークン検証）：10ms以内
- INSERT（トークン発行）：50ms以内
- UPDATE（無効化）：30ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| security_admin | ○ | × | ○ | ○ | セキュリティ管理者 |
| application | ○ | ○ | ○ | × | アプリケーション |
| auth_service | ○ | ○ | ○ | × | 認証サービス |

### 8.2 データ保護
- 個人情報：含む（ユーザーID、IPアドレス）
- 機密情報：含む（トークン値）
- 暗号化：必須（token_value、device_info）
- ハッシュ化：必須（token_hash）

### 8.3 セキュリティ対策
1. **トークン値の暗号化**：AES-256で暗号化
2. **ハッシュ値の生成**：SHA-256でハッシュ化
3. **アクセス監視**：異常なアクセスパターンの検知
4. **定期ローテーション**：長期間使用されないトークンの無効化

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存認証システム
- 移行方法：トークン再発行
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存トークンの無効化
UPDATE SYS_TokenStore 
SET is_active = FALSE, 
    revocation_reason = 'ADMIN',
    revoked_at = NOW(),
    revoked_by = 'SYSTEM_MIGRATION'
WHERE is_active = TRUE;

-- 新規トークンの発行（アプリケーション側で実行）
-- ユーザーには再ログインを要求
```

### 9.3 DDL
```sql
CREATE TABLE SYS_TokenStore (
    token_id VARCHAR(50) NOT NULL,
    token_type VARCHAR(50) NOT NULL,
    token_value TEXT NOT NULL,
    token_hash VARCHAR(255) NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    client_id VARCHAR(100) NULL,
    scope VARCHAR(500) NULL,
    issued_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL,
    last_used_at TIMESTAMP NULL,
    usage_count INTEGER NOT NULL DEFAULT 0,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    device_info TEXT NULL,
    parent_token_id VARCHAR(50) NULL,
    child_token_count INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    revocation_reason VARCHAR(100) NULL,
    revoked_at TIMESTAMP NULL,
    revoked_by VARCHAR(50) NULL,
    metadata TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (token_id),
    UNIQUE KEY uk_token_hash (token_hash),
    INDEX idx_token_type (token_type),
    INDEX idx_user_id (user_id),
    INDEX idx_client_id (client_id),
    INDEX idx_expires_at (expires_at),
    INDEX idx_is_active (is_active),
    INDEX idx_parent_token_id (parent_token_id),
    INDEX idx_issued_at (issued_at),
    INDEX idx_composite (user_id, token_type, is_active),
    CONSTRAINT fk_token_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_token_parent FOREIGN KEY (parent_token_id) REFERENCES SYS_TokenStore(token_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT chk_token_type CHECK (token_type IN ('JWT', 'REFRESH', 'API', 'RESET', 'ACTIVATION', 'INVITATION')),
    CONSTRAINT chk_revocation_reason CHECK (revocation_reason IS NULL OR revocation_reason IN ('EXPIRED', 'LOGOUT', 'SECURITY', 'ADMIN', 'USER_REQUEST')),
    CONSTRAINT chk_usage_count CHECK (usage_count >= 0),
    CONSTRAINT chk_child_token_count CHECK (child_token_count >= 0),
    CONSTRAINT chk_expires_after_issued CHECK (expires_at > issued_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(issued_at) * 100 + MONTH(issued_at)) (
    PARTITION p202501 VALUES LESS THAN (202502),
    PARTITION p202502 VALUES LESS THAN (202503),
    PARTITION p202503 VALUES LESS THAN (202504),
    PARTITION p202504 VALUES LESS THAN (202505),
    PARTITION p202505 VALUES LESS THAN (202506),
    PARTITION p202506 VALUES LESS THAN (202507),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. **高セキュリティ要件**：トークン値の暗号化とハッシュ化必須
2. **高頻度アクセス**：トークン検証の高速化が重要
3. **自動クリーンアップ**：期限切れトークンの定期削除
4. **監査対応**：トークン操作の完全な履歴管理
5. **親子関係**：リフレッシュトークンとJWTトークンの関連管理
6. **デバイス管理**：デバイス情報による不正アクセス検知
7. **スコープ管理**：APIトークンの権限制御
8. **使用統計**：トークン使用回数・最終使用日時の記録
9. **無効化管理**：様々な理由でのトークン無効化対応
10. **パフォーマンス最適化**：インデックス設計とパーティション分割
11. **セキュリティ監視**：異常なトークン使用パターンの検知
12. **災害対策**：トークン情報のバックアップと復旧手順

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（トークン管理システム対応） |
