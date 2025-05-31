# テーブル定義書：ユーザーロール関連 (MST_UserRole)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-003 |
| **テーブル名** | MST_UserRole |
| **論理名** | ユーザーロール関連 |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
ユーザーロール関連テーブル（MST_UserRole）は、ユーザーとロールの多対多の関係を管理します。一人のユーザーが複数のロールを持つことができ、一つのロールが複数のユーザーに割り当てられることを可能にします。

### 2.2 関連API
- [API-004](../api/specs/API仕様書_API-004.md) - ユーザーロール管理API

### 2.3 関連バッチ
- [BATCH-003](../batch/specs/バッチ定義書_BATCH-003.md) - セキュリティスキャンバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | user_id | ユーザーID | VARCHAR | 50 | × | ○ | ○ | - | ユーザーを一意に識別するID |
| 2 | role_id | ロールID | VARCHAR | 50 | × | ○ | ○ | - | ロールを一意に識別するID |
| 3 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントを一意に識別するID |
| 4 | assigned_at | 割り当て日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | ロール割り当て日時 |
| 5 | assigned_by | 割り当て者ID | VARCHAR | 50 | × | - | ○ | - | ロールを割り当てたユーザーID |
| 6 | expires_at | 有効期限 | TIMESTAMP | - | ○ | - | - | NULL | ロール有効期限（NULL=無期限） |
| 7 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | ロール割り当てが有効かどうか |
| 8 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 9 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | user_id, role_id, tenant_id | 複合主キー |
| idx_user_tenant | INDEX | user_id, tenant_id | ユーザー・テナント検索用 |
| idx_role_tenant | INDEX | role_id, tenant_id | ロール・テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_expires | INDEX | expires_at | 有効期限検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_user_role | PRIMARY KEY | user_id, role_id, tenant_id | 複合主キー制約 |
| fk_user | FOREIGN KEY | user_id | MST_UserAuth.user_id |
| fk_role | FOREIGN KEY | role_id | MST_Role.role_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_assigned_by | FOREIGN KEY | assigned_by | MST_UserAuth.user_id |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | user_id, assigned_by | 1:N | ユーザー認証情報 |
| MST_Role | role_id | 1:N | ロール情報 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |

### 4.2 子テーブル
なし

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_UserRole (
    user_id, role_id, tenant_id, assigned_by, is_active
) VALUES (
    'admin001', 'ADMIN', 'tenant001', 'system', TRUE
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 初期ユーザー×ロール |
| 年間増加件数 | 2,000件 | 新規ユーザー・ロール変更 |
| 5年後想定件数 | 10,500件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：論理削除から1年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | user_id, tenant_id | ユーザーロール取得 |
| SELECT | 高 | role_id, tenant_id | ロール所有者取得 |
| INSERT | 中 | - | ロール割り当て |
| UPDATE | 中 | user_id, role_id, tenant_id | ロール状態更新 |
| DELETE | 低 | - | ロール削除 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | ○ | テナント管理者（自テナントのみ） |
| application | ○ | ○ | ○ | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（権限情報）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存権限管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_UserRole (
    user_id VARCHAR(50) NOT NULL,
    role_id VARCHAR(50) NOT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    assigned_by VARCHAR(50) NOT NULL,
    expires_at TIMESTAMP NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, role_id, tenant_id),
    INDEX idx_user_tenant (user_id, tenant_id),
    INDEX idx_role_tenant (role_id, tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_expires (expires_at),
    CONSTRAINT fk_user_role_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_user_role_role FOREIGN KEY (role_id) REFERENCES MST_Role(role_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_user_role_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_user_role_assigned_by FOREIGN KEY (assigned_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. 同一ユーザー・ロール・テナントの組み合わせは一意
2. 有効期限が設定されている場合、期限切れ後は自動的に無効化
3. テナント管理者は自テナント内のユーザーロールのみ管理可能
4. ロール削除時は関連するユーザーロールも削除される
5. 論理削除（is_active=FALSE）を基本とし、物理削除は慎重に行う

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
