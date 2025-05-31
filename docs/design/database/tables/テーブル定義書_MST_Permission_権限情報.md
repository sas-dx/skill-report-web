# テーブル定義書：権限情報 (MST_Permission)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-003 |
| **テーブル名** | MST_Permission |
| **論理名** | 権限情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
権限情報テーブル（MST_Permission）は、システム内で利用可能な権限（パーミッション）を管理します。各権限は特定の機能やリソースへのアクセス制御に使用され、ロールベースアクセス制御（RBAC）の基盤となります。

### 2.2 関連API
- [API-003](../api/specs/API仕様書_API-003.md) - 権限管理API
- [API-004](../api/specs/API仕様書_API-004.md) - ユーザーロール管理API

### 2.3 関連バッチ
- [BATCH-003](../batch/specs/バッチ定義書_BATCH-003.md) - セキュリティスキャンバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | permission_id | 権限ID | VARCHAR | 50 | × | ○ | - | - | 権限を一意に識別するID |
| 2 | permission_name | 権限名 | VARCHAR | 100 | × | - | - | - | 権限の表示名 |
| 3 | permission_code | 権限コード | VARCHAR | 50 | × | - | - | - | システム内で使用する権限コード |
| 4 | category | カテゴリ | VARCHAR | 50 | × | - | - | - | 権限のカテゴリ（USER/SKILL/REPORT等） |
| 5 | resource_type | リソースタイプ | VARCHAR | 50 | × | - | - | - | 対象リソースの種類 |
| 6 | action_type | アクションタイプ | VARCHAR | 20 | × | - | - | - | 許可するアクション（READ/WRITE/DELETE等） |
| 7 | description | 説明 | TEXT | - | ○ | - | - | NULL | 権限の詳細説明 |
| 8 | is_system_permission | システム権限フラグ | BOOLEAN | - | × | - | - | FALSE | システム標準権限かどうか |
| 9 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | テナント固有権限の場合のテナントID |
| 10 | parent_permission_id | 親権限ID | VARCHAR | 50 | ○ | - | ○ | NULL | 階層構造の親権限ID |
| 11 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | 権限一覧での表示順序 |
| 12 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 権限が有効かどうか |
| 13 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 14 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 15 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 16 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | permission_id | 主キー |
| idx_permission_code | UNIQUE | permission_code | 権限コードの一意性を保証 |
| idx_category | INDEX | category | カテゴリ検索用 |
| idx_resource_action | INDEX | resource_type, action_type | リソース・アクション検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_parent | INDEX | parent_permission_id | 親権限検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_permission | PRIMARY KEY | permission_id | 主キー制約 |
| uq_permission_code | UNIQUE | permission_code | 権限コードの一意性を保証 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_parent_permission | FOREIGN KEY | parent_permission_id | MST_Permission.permission_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_action_type | CHECK | action_type | action_type IN ('READ', 'WRITE', 'DELETE', 'EXECUTE', 'ADMIN') |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_Permission | parent_permission_id | 1:N | 親権限（自己参照） |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_RolePermission | permission_id | 1:N | ロール権限関連 |
| MST_Permission | parent_permission_id | 1:N | 子権限（自己参照） |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_Permission (
    permission_id, permission_name, permission_code, category,
    resource_type, action_type, description, is_system_permission,
    created_by, updated_by
) VALUES (
    'PERM_USER_READ',
    'ユーザー情報参照',
    'USER_READ',
    'USER',
    'USER_PROFILE',
    'READ',
    'ユーザーの基本情報を参照する権限',
    TRUE,
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 50件 | システム標準権限 |
| 年間増加件数 | 20件 | カスタム権限追加 |
| 5年後想定件数 | 150件 | 想定値 |

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
| SELECT | 高 | category, is_active | カテゴリ別権限取得 |
| SELECT | 高 | permission_code | 権限コード検索 |
| SELECT | 中 | tenant_id | テナント固有権限取得 |
| UPDATE | 低 | permission_id | 権限情報更新 |
| INSERT | 低 | - | 新規権限作成 |

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
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| application | ○ | × | × | × | アプリケーション |
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
CREATE TABLE MST_Permission (
    permission_id VARCHAR(50) NOT NULL,
    permission_name VARCHAR(100) NOT NULL,
    permission_code VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50) NOT NULL,
    action_type VARCHAR(20) NOT NULL,
    description TEXT NULL,
    is_system_permission BOOLEAN NOT NULL DEFAULT FALSE,
    tenant_id VARCHAR(50) NULL,
    parent_permission_id VARCHAR(50) NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (permission_id),
    UNIQUE KEY idx_permission_code (permission_code),
    INDEX idx_category (category),
    INDEX idx_resource_action (resource_type, action_type),
    INDEX idx_tenant (tenant_id),
    INDEX idx_parent (parent_permission_id),
    INDEX idx_active (is_active),
    CONSTRAINT fk_permission_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_permission_parent FOREIGN KEY (parent_permission_id) REFERENCES MST_Permission(permission_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_permission_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_permission_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_permission_action_type CHECK (action_type IN ('READ', 'WRITE', 'DELETE', 'EXECUTE', 'ADMIN'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. システム標準権限（is_system_permission=TRUE）は削除不可
2. 権限コードは英数字とアンダースコアのみ使用可能
3. 階層構造により権限の継承関係を表現
4. テナント固有権限はtenant_idを設定
5. 権限の無効化は論理削除（is_active=FALSE）を使用
6. 親権限が削除された場合、子権限の親参照はNULLに設定

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
