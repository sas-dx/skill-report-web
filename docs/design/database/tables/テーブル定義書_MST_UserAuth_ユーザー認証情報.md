# テーブル定義書：MST_UserAuth（ユーザー認証情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-001 |
| **テーブル名** | MST_UserAuth |
| **論理名** | ユーザー認証情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
ユーザー認証情報テーブル（MST_UserAuth）は、マルチテナント環境でのユーザー認証情報を管理します。ユーザーIDとパスワードによる標準認証と、SSOによるシングルサインオン認証の両方をサポートし、アカウントのステータス管理や連続ログイン失敗によるロック機能も提供します。

### 2.2 関連要求仕様ID
- **PLT.1-WEB.1**: ログイン・認証機能
- **ACC.1-AUTH.1**: ユーザー認証管理
- **ACC.2-SSO.1**: SSO連携機能

### 2.3 関連API
- [API-001](../api/specs/API仕様書_API-001_ログインAPI.md) - ログインAPI
- [API-002](../api/specs/API仕様書_API-002_ログアウトAPI.md) - ログアウトAPI

### 2.4 関連バッチ
- [BATCH-001](../batch/specs/バッチ定義書_BATCH-001_システムヘルスチェックバッチ.md) - システムヘルスチェックバッチ
- [BATCH-002](../batch/specs/バッチ定義書_BATCH-002_ログクリーンアップバッチ.md) - ログクリーンアップバッチ
- [BATCH-003](../batch/specs/バッチ定義書_BATCH-003_セキュリティスキャンバッチ.md) - セキュリティスキャンバッチ
- [BATCH-006](../batch/specs/バッチ定義書_BATCH-006_トークン無効化バッチ.md) - トークン無効化バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | tenant_id | テナントID | VARCHAR | 50 | × | ○ | MST_Tenant.tenant_id | - | テナントを識別するID |
| 2 | user_id | ユーザーID | VARCHAR | 50 | × | ○ | - | - | ユーザーを一意に識別するID |
| 3 | password_hash | パスワードハッシュ | VARCHAR | 256 | × | - | - | - | パスワードのハッシュ値（bcrypt等で暗号化） |
| 4 | email | メールアドレス | VARCHAR | 256 | × | - | - | - | ユーザーのメールアドレス |
| 5 | status | アカウント状態 | VARCHAR | 20 | × | - | - | 'ACTIVE' | アカウントの状態（ACTIVE/LOCKED/INACTIVE） |
| 6 | failed_attempts | 連続失敗回数 | INTEGER | 2 | × | - | - | 0 | 連続ログイン失敗回数 |
| 7 | locked_until | ロック解除予定日時 | TIMESTAMP | - | ○ | - | - | NULL | アカウントロック解除予定日時 |
| 8 | last_login | 最終ログイン日時 | TIMESTAMP | - | ○ | - | - | NULL | 最後にログインした日時 |
| 9 | sso_enabled | SSO有効フラグ | BOOLEAN | - | × | - | - | FALSE | SSOによる認証を有効にするかどうか |
| 10 | sso_provider | SSOプロバイダ名 | VARCHAR | 50 | ○ | - | - | NULL | 使用するSSOプロバイダの名称 |
| 11 | sso_subject | SSO識別子 | VARCHAR | 256 | ○ | - | - | NULL | SSOプロバイダから提供される一意の識別子 |
| 12 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 13 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | tenant_id, user_id | 主キー（複合キー） |
| idx_email | UNIQUE | tenant_id, email | テナント内でのメールアドレスの一意性を保証 |
| idx_status | INDEX | tenant_id, status | アカウント状態による検索を高速化 |
| idx_sso | INDEX | tenant_id, sso_provider, sso_subject | SSO認証情報による検索を高速化 |
| fk_tenant | FOREIGN KEY | tenant_id | テナントマスタへの外部キー |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_user_auth | PRIMARY KEY | tenant_id, user_id | 主キー制約（複合キー） |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenantテーブルへの外部キー制約 |
| uq_email | UNIQUE | tenant_id, email | テナント内でのメールアドレスの一意性を保証 |
| chk_status | CHECK | status | status列の値をACTIVE/LOCKED/INACTIVEに制限 |
| chk_failed_attempts | CHECK | failed_attempts | 0以上の値のみ許可 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | N:1 | テナント情報 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserRole | tenant_id, user_id | 1:N | ユーザーに割り当てられたロール |
| HIS_AuditLog | tenant_id, user_id | 1:N | ユーザーの操作履歴 |
| SYS_TokenStore | tenant_id, user_id | 1:N | ユーザーのアクセストークン |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_UserAuth (
    tenant_id, user_id, password_hash, email, status, failed_attempts, 
    sso_enabled, created_at, updated_at
) VALUES (
    'tenant001',
    'admin001', 
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/RK.s5uO9G',
    'admin@example.com',
    'ACTIVE',
    0,
    FALSE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 100件 | システム管理者・初期ユーザー |
| 年間増加件数 | 500件 | 新規ユーザー登録 |
| 5年後想定件数 | 2,600件 | 想定値 |

### 5.3 データ保持期間
| データ種別 | 保持期間 | 備考 |
|------------|----------|------|
| アクティブユーザー | 無期限 | 業務継続中は保持 |
| 非アクティブユーザー | 3年 | 最終ログインから3年後にアーカイブ |
| ログイン履歴 | 90日 | セキュリティ監査用 |

## 6. 運用仕様

### 6.1 バックアップ
- **日次バックアップ**: 毎日2:00実行
- **週次バックアップ**: 毎週日曜日3:00実行
- **月次バックアップ**: 毎月1日4:00実行

### 6.2 パーティション
- **パーティション種別**: なし
- **パーティション条件**: -

### 6.3 アーカイブ
- **アーカイブ条件**: 論理削除から3年経過
- **アーカイブ先**: アーカイブDB
- **アーカイブ方法**: 月次バッチで実行

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id, user_id | ログイン認証 |
| SELECT | 高 | tenant_id, email | メールアドレスによる検索 |
| UPDATE | 中 | tenant_id, user_id | ログイン失敗回数更新 |
| UPDATE | 中 | tenant_id, user_id | 最終ログイン日時更新 |
| INSERT | 低 | - | 新規ユーザー登録 |

### 7.2 パフォーマンス要件
- **SELECT**: 10ms以内
- **INSERT**: 50ms以内
- **UPDATE**: 50ms以内
- **DELETE**: 50ms以内

### 7.3 同時接続数
- **想定同時接続数**: 100ユーザー
- **最大同時接続数**: 500ユーザー

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| security_admin | ○ | × | ○ | × | セキュリティ管理者 |
| application | ○ | ○ | ○ | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- **個人情報**: 含む（メールアドレス）
- **機密情報**: 含む（パスワードハッシュ）
- **暗号化**: パスワードハッシュは必須（bcrypt推奨）
- **マスキング**: 本番環境以外ではパスワードハッシュをマスキング

### 8.3 監査要件
- **操作ログ**: 全ての更新操作を記録
- **アクセスログ**: 認証試行を記録
- **保持期間**: 90日間

## 9. 移行仕様

### 9.1 データ移行
- **移行元**: 既存認証システム
- **移行方法**: セキュアなデータ移行バッチ
- **移行タイミング**: システム移行時
- **移行検証**: パスワード認証テストで検証

### 9.2 DDL
```sql
CREATE TABLE MST_UserAuth (
    tenant_id VARCHAR(50) NOT NULL,
    user_id VARCHAR(50) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    email VARCHAR(256) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    failed_attempts INTEGER NOT NULL DEFAULT 0,
    locked_until TIMESTAMP NULL,
    last_login TIMESTAMP NULL,
    sso_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    sso_provider VARCHAR(50) NULL,
    sso_subject VARCHAR(256) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (tenant_id, user_id),
    UNIQUE KEY idx_email (tenant_id, email),
    INDEX idx_status (tenant_id, status),
    INDEX idx_sso (tenant_id, sso_provider, sso_subject),
    CONSTRAINT fk_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id),
    CONSTRAINT chk_status CHECK (status IN ('ACTIVE', 'LOCKED', 'INACTIVE')),
    CONSTRAINT chk_failed_attempts CHECK (failed_attempts >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

### 10.1 セキュリティ要件
1. パスワードは必ずハッシュ化して保存し、平文では保存しないこと
2. アカウントロックは連続5回のログイン失敗で発生し、30分後に自動解除
3. SSO連携時はsso_enabled=TRUE、sso_provider、sso_subjectに適切な値を設定
4. 個人情報保護の観点から、このテーブルへのアクセスは厳格に制限すること

### 10.2 運用要件
1. パスワードハッシュアルゴリズムはbcryptを使用（コスト12以上）
2. メールアドレスは小文字で正規化して保存
3. ユーザーIDは英数字のみ許可（特殊文字不可）
4. テナント間でのデータ漏洩防止のため、必ずtenant_idを条件に含める

### 10.3 障害対応
1. アカウントロック時は管理者による手動解除も可能
2. パスワードリセット機能との連携を考慮
3. SSO障害時のフォールバック認証を提供

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、マルチテナント対応追加 |
