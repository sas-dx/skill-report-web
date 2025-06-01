# テーブル定義書：MST_Role（ロール情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-002 |
| **テーブル名** | MST_Role |
| **論理名** | ロール情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
ロール情報マスタテーブル（MST_Role）は、システム内で使用されるロール（役割）の定義を管理します。ユーザーに付与される権限の集合体として機能し、アクセス制御の基盤となります。

### 2.2 関連API
- [API-003](../../api/specs/API仕様書_API-003_ロール管理API.md) - ロール管理API

### 2.3 関連バッチ
- [BATCH-003](../../batch/specs/バッチ定義書_BATCH-003_セキュリティスキャンバッチ.md) - セキュリティスキャンバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | role_id | ロールID | VARCHAR | 50 | × | ○ | - | - | ロールを一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | role_name | ロール名 | VARCHAR | 100 | × | - | - | - | ロールの名称 |
| 4 | role_code | ロールコード | VARCHAR | 50 | × | - | - | - | ロールの識別コード |
| 5 | description | 説明 | TEXT | - | ○ | - | - | NULL | ロールの詳細説明 |
| 6 | role_type | ロール種別 | VARCHAR | 20 | × | - | - | 'CUSTOM' | ロールの種別（SYSTEM/TENANT/CUSTOM） |
| 7 | is_system_role | システムロールフラグ | BOOLEAN | - | × | - | - | FALSE | システム標準ロールかどうか |
| 8 | is_default | デフォルトロールフラグ | BOOLEAN | - | × | - | - | FALSE | 新規ユーザーのデフォルトロールかどうか |
| 9 | priority | 優先度 | INTEGER | - | × | - | - | 100 | ロールの優先度（数値が小さいほど高優先度） |
| 10 | max_users | 最大ユーザー数 | INTEGER | - | ○ | - | - | NULL | このロールを持てる最大ユーザー数 |
| 11 | permissions | 権限リスト | TEXT | - | ○ | - | - | NULL | 権限IDのJSON配列 |
| 12 | restrictions | 制限事項 | TEXT | - | ○ | - | - | NULL | ロールの制限事項（JSON形式） |
| 13 | valid_from | 有効開始日 | DATE | - | ○ | - | - | NULL | ロールの有効開始日 |
| 14 | valid_until | 有効終了日 | DATE | - | ○ | - | - | NULL | ロールの有効終了日 |
| 15 | approval_required | 承認必須フラグ | BOOLEAN | - | × | - | - | FALSE | ロール付与時に承認が必要かどうか |
| 16 | auto_assign_conditions | 自動付与条件 | TEXT | - | ○ | - | - | NULL | 自動付与の条件（JSON形式） |
| 17 | inheritance_roles | 継承ロール | TEXT | - | ○ | - | - | NULL | 継承するロールIDのJSON配列 |
| 18 | excluded_roles | 排他ロール | TEXT | - | ○ | - | - | NULL | 同時に持てないロールIDのJSON配列 |
| 19 | session_timeout | セッションタイムアウト | INTEGER | - | ○ | - | - | NULL | このロール固有のセッションタイムアウト（秒） |
| 20 | ip_restrictions | IP制限 | TEXT | - | ○ | - | - | NULL | アクセス可能なIPアドレス範囲（JSON形式） |
| 21 | time_restrictions | 時間制限 | TEXT | - | ○ | - | - | NULL | アクセス可能な時間帯（JSON形式） |
| 22 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | ロールが有効かどうか |
| 23 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 24 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 25 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 26 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | role_id | 主キー |
| uq_role_code | UNIQUE | tenant_id, role_code | テナント内でのロールコード一意性 |
| uq_role_name | UNIQUE | tenant_id, role_name | テナント内でのロール名一意性 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_role_type | INDEX | role_type | ロール種別検索用 |
| idx_system_role | INDEX | is_system_role | システムロール検索用 |
| idx_default_role | INDEX | is_default | デフォルトロール検索用 |
| idx_priority | INDEX | priority | 優先度検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_role | PRIMARY KEY | role_id | 主キー制約 |
| uq_role_code | UNIQUE | tenant_id, role_code | テナント内でのロールコード一意性 |
| uq_role_name | UNIQUE | tenant_id, role_name | テナント内でのロール名一意性 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_role_type | CHECK | role_type | role_type IN ('SYSTEM', 'TENANT', 'CUSTOM') |
| chk_priority | CHECK | priority | priority > 0 |
| chk_max_users | CHECK | max_users | max_users IS NULL OR max_users > 0 |
| chk_session_timeout | CHECK | session_timeout | session_timeout IS NULL OR session_timeout > 0 |
| chk_valid_period | CHECK | valid_from, valid_until | valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserRole | role_id | 1:N | ユーザーロール関連 |

## 5. データ仕様

### 5.1 データ例
```sql
-- システム管理者ロール
INSERT INTO MST_Role (
    role_id, tenant_id, role_name, role_code, description, role_type,
    is_system_role, priority, permissions, is_active,
    created_by, updated_by
) VALUES (
    'role_system_admin', 'SYSTEM', 'システム管理者', 'SYSTEM_ADMIN',
    'システム全体の管理権限を持つロール', 'SYSTEM',
    TRUE, 1, '["SYSTEM_ADMIN", "USER_MANAGE", "TENANT_MANAGE", "SECURITY_MANAGE"]', TRUE,
    'system', 'system'
);

-- テナント管理者ロール
INSERT INTO MST_Role (
    role_id, tenant_id, role_name, role_code, description, role_type,
    is_system_role, priority, permissions, is_active,
    created_by, updated_by
) VALUES (
    'role_tenant_admin', 'TENANT_001', 'テナント管理者', 'TENANT_ADMIN',
    'テナント内の管理権限を持つロール', 'TENANT',
    TRUE, 10, '["TENANT_ADMIN", "USER_MANAGE", "ROLE_MANAGE"]', TRUE,
    'system', 'system'
);

-- 一般ユーザーロール
INSERT INTO MST_Role (
    role_id, tenant_id, role_name, role_code, description, role_type,
    is_system_role, is_default, priority, permissions, is_active,
    created_by, updated_by
) VALUES (
    'role_user', 'TENANT_001', '一般ユーザー', 'USER',
    '基本的な機能を利用できるロール', 'CUSTOM',
    FALSE, TRUE, 100, '["PROFILE_VIEW", "SKILL_MANAGE", "REPORT_VIEW"]', TRUE,
    'role_tenant_admin', 'role_tenant_admin'
);

-- 閲覧専用ロール
INSERT INTO MST_Role (
    role_id, tenant_id, role_name, role_code, description, role_type,
    is_system_role, priority, permissions, restrictions, is_active,
    created_by, updated_by
) VALUES (
    'role_readonly', 'TENANT_001', '閲覧専用', 'READONLY',
    '閲覧のみ可能なロール', 'CUSTOM',
    FALSE, 200, '["PROFILE_VIEW", "REPORT_VIEW"]',
    '{"data_export": false, "bulk_operation": false}', TRUE,
    'role_tenant_admin', 'role_tenant_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 20件 | システム標準ロール、基本ロール |
| 月間増加件数 | 5件 | カスタムロール追加 |
| 年間増加件数 | 60件 | 想定値 |
| 5年後想定件数 | 320件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：無効化から1年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 最高 | role_id, tenant_id | 権限チェック |
| SELECT | 高 | tenant_id, is_default | デフォルトロール取得 |
| SELECT | 中 | tenant_id, role_type | ロール一覧取得 |
| UPDATE | 低 | role_id | ロール情報更新 |
| INSERT | 低 | - | 新規ロール作成 |

### 7.2 パフォーマンス要件
- SELECT：5ms以内
- INSERT：30ms以内
- UPDATE：30ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| role_admin | ○ | ○ | ○ | × | ロール管理者 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（権限情報、制限事項）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存権限管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_Role (
    role_id VARCHAR(50) NOT NULL COMMENT 'ロールID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    role_name VARCHAR(100) NOT NULL COMMENT 'ロール名',
    role_code VARCHAR(50) NOT NULL COMMENT 'ロールコード',
    description TEXT NULL COMMENT '説明',
    role_type VARCHAR(20) NOT NULL DEFAULT 'CUSTOM' COMMENT 'ロール種別',
    is_system_role BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'システムロールフラグ',
    is_default BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'デフォルトロールフラグ',
    priority INTEGER NOT NULL DEFAULT 100 COMMENT '優先度',
    max_users INTEGER NULL COMMENT '最大ユーザー数',
    permissions TEXT NULL COMMENT '権限リスト',
    restrictions TEXT NULL COMMENT '制限事項',
    valid_from DATE NULL COMMENT '有効開始日',
    valid_until DATE NULL COMMENT '有効終了日',
    approval_required BOOLEAN NOT NULL DEFAULT FALSE COMMENT '承認必須フラグ',
    auto_assign_conditions TEXT NULL COMMENT '自動付与条件',
    inheritance_roles TEXT NULL COMMENT '継承ロール',
    excluded_roles TEXT NULL COMMENT '排他ロール',
    session_timeout INTEGER NULL COMMENT 'セッションタイムアウト',
    ip_restrictions TEXT NULL COMMENT 'IP制限',
    time_restrictions TEXT NULL COMMENT '時間制限',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (role_id),
    UNIQUE KEY uq_role_code (tenant_id, role_code),
    UNIQUE KEY uq_role_name (tenant_id, role_name),
    INDEX idx_tenant (tenant_id),
    INDEX idx_role_type (role_type),
    INDEX idx_system_role (is_system_role),
    INDEX idx_default_role (is_default),
    INDEX idx_priority (priority),
    INDEX idx_active (is_active),
    CONSTRAINT fk_role_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_role_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_role_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_role_type CHECK (role_type IN ('SYSTEM', 'TENANT', 'CUSTOM')),
    CONSTRAINT chk_role_priority CHECK (priority > 0),
    CONSTRAINT chk_role_max_users CHECK (max_users IS NULL OR max_users > 0),
    CONSTRAINT chk_role_session_timeout CHECK (session_timeout IS NULL OR session_timeout > 0),
    CONSTRAINT chk_role_valid_period CHECK (valid_until IS NULL OR valid_from IS NULL OR valid_from <= valid_until)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ロール情報';
```

## 10. 特記事項

1. **ロール階層**
   - システムロール > テナントロール > カスタムロール
   - 継承関係により権限の集約が可能

2. **権限管理**
   - 権限はJSON配列で管理
   - 動的な権限チェックに対応

3. **制限事項**
   - IP制限、時間制限をサポート
   - セッションタイムアウトの個別設定が可能

4. **自動付与機能**
   - 条件に基づく自動ロール付与
   - 新規ユーザーのデフォルトロール設定

5. **排他制御**
   - 同時に持てないロールの定義
   - ロール付与時の整合性チェック
