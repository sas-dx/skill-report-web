# テーブル定義書：テナント管理 (MST_Tenant)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-026 |
| **テーブル名** | MST_Tenant |
| **論理名** | テナント管理 |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 新規作成 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
テナント管理テーブル（MST_Tenant）は、マルチテナント環境における各テナント（組織・企業）の基本情報を管理します。テナントごとにデータを分離し、独立したサービス環境を提供するための基盤となるテーブルです。

### 2.2 関連API
- [API-025](../api/specs/API仕様書_API-025.md) - テナント管理API

### 2.3 関連バッチ
- [BATCH-018-01](../batch/specs/バッチ定義書_BATCH-018-01.md) - テナント使用量集計バッチ
- [BATCH-018-02](../batch/specs/バッチ定義書_BATCH-018-02.md) - テナント課金計算バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | tenant_id | テナントID | VARCHAR | 50 | × | ○ | - | - | テナントを一意に識別するID |
| 2 | tenant_name | テナント名 | VARCHAR | 200 | × | - | - | - | テナントの表示名 |
| 3 | company_name | 会社名 | VARCHAR | 200 | × | - | - | - | 正式な会社名 |
| 4 | domain | ドメイン | VARCHAR | 100 | ○ | - | - | NULL | テナント専用ドメイン |
| 5 | plan_type | プランタイプ | VARCHAR | 20 | × | - | - | 'BASIC' | 契約プラン（BASIC/STANDARD/PREMIUM/ENTERPRISE） |
| 6 | max_users | 最大ユーザー数 | INTEGER | - | × | - | - | 100 | 契約可能な最大ユーザー数 |
| 7 | max_storage_gb | 最大ストレージ容量 | INTEGER | - | × | - | - | 10 | 契約可能な最大ストレージ容量（GB） |
| 8 | contract_start_date | 契約開始日 | DATE | - | × | - | - | - | 契約開始日 |
| 9 | contract_end_date | 契約終了日 | DATE | - | ○ | - | - | NULL | 契約終了日（NULL=無期限） |
| 10 | status | ステータス | VARCHAR | 20 | × | - | - | 'ACTIVE' | テナントステータス（ACTIVE/SUSPENDED/TERMINATED） |
| 11 | timezone | タイムゾーン | VARCHAR | 50 | × | - | - | 'Asia/Tokyo' | テナントのタイムゾーン |
| 12 | locale | ロケール | VARCHAR | 10 | × | - | - | 'ja_JP' | テナントのロケール |
| 13 | admin_email | 管理者メール | VARCHAR | 256 | × | - | - | - | テナント管理者のメールアドレス |
| 14 | admin_phone | 管理者電話番号 | VARCHAR | 20 | ○ | - | - | NULL | テナント管理者の電話番号 |
| 15 | billing_email | 請求先メール | VARCHAR | 256 | ○ | - | - | NULL | 請求書送付先メールアドレス |
| 16 | is_trial | トライアルフラグ | BOOLEAN | - | × | - | - | FALSE | トライアル契約かどうか |
| 17 | trial_end_date | トライアル終了日 | DATE | - | ○ | - | - | NULL | トライアル終了日 |
| 18 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 19 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 20 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 21 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | tenant_id | 主キー |
| idx_tenant_name | UNIQUE | tenant_name | テナント名の一意性を保証 |
| idx_domain | UNIQUE | domain | ドメインの一意性を保証 |
| idx_status | INDEX | status | ステータスによる検索を高速化 |
| idx_plan_type | INDEX | plan_type | プランタイプによる検索を高速化 |
| idx_contract_dates | INDEX | contract_start_date, contract_end_date | 契約期間による検索を高速化 |
| idx_admin_email | INDEX | admin_email | 管理者メールによる検索を高速化 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_tenant | PRIMARY KEY | tenant_id | 主キー制約 |
| uq_tenant_name | UNIQUE | tenant_name | テナント名の一意性を保証 |
| uq_domain | UNIQUE | domain | ドメインの一意性を保証（NULL許可） |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_plan_type | CHECK | plan_type | plan_type IN ('BASIC', 'STANDARD', 'PREMIUM', 'ENTERPRISE') |
| chk_status | CHECK | status | status IN ('ACTIVE', 'SUSPENDED', 'TERMINATED') |
| chk_max_users | CHECK | max_users | max_users > 0 |
| chk_max_storage | CHECK | max_storage_gb | max_storage_gb > 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_TenantSettings | tenant_id | 1:1 | テナント設定 |
| SYS_TenantUsage | tenant_id | 1:N | テナント使用量 |
| HIS_TenantBilling | tenant_id | 1:N | テナント課金履歴 |
| MST_Employee | tenant_id | 1:N | 社員情報 |
| MST_SkillCategory | tenant_id | 1:N | スキルカテゴリ |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_Tenant (
    tenant_id, tenant_name, company_name, domain, plan_type, 
    max_users, max_storage_gb, contract_start_date, status,
    timezone, locale, admin_email, created_by, updated_by
) VALUES (
    'tenant001',
    'サンプル株式会社',
    'サンプル株式会社',
    'sample.skillreport.com',
    'STANDARD',
    500,
    100,
    '2025-01-01',
    'ACTIVE',
    'Asia/Tokyo',
    'ja_JP',
    'admin@sample.com',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 10件 | 初期契約テナント |
| 年間増加件数 | 100件 | 新規契約テナント |
| 5年後想定件数 | 510件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：契約終了から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id | テナント情報取得 |
| SELECT | 高 | status = 'ACTIVE' | アクティブテナント一覧 |
| SELECT | 中 | domain | ドメインによる検索 |
| UPDATE | 中 | tenant_id | テナント情報更新 |
| INSERT | 低 | - | 新規テナント作成 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | × | ○ | × | テナント管理者（自テナントのみ） |
| application | ○ | ○ | ○ | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（管理者メール、電話番号）
- 機密情報：含む（契約情報）
- 暗号化：メールアドレス、電話番号は暗号化推奨

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存契約管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_Tenant (
    tenant_id VARCHAR(50) NOT NULL,
    tenant_name VARCHAR(200) NOT NULL,
    company_name VARCHAR(200) NOT NULL,
    domain VARCHAR(100) NULL,
    plan_type VARCHAR(20) NOT NULL DEFAULT 'BASIC',
    max_users INTEGER NOT NULL DEFAULT 100,
    max_storage_gb INTEGER NOT NULL DEFAULT 10,
    contract_start_date DATE NOT NULL,
    contract_end_date DATE NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    timezone VARCHAR(50) NOT NULL DEFAULT 'Asia/Tokyo',
    locale VARCHAR(10) NOT NULL DEFAULT 'ja_JP',
    admin_email VARCHAR(256) NOT NULL,
    admin_phone VARCHAR(20) NULL,
    billing_email VARCHAR(256) NULL,
    is_trial BOOLEAN NOT NULL DEFAULT FALSE,
    trial_end_date DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (tenant_id),
    UNIQUE KEY idx_tenant_name (tenant_name),
    UNIQUE KEY idx_domain (domain),
    INDEX idx_status (status),
    INDEX idx_plan_type (plan_type),
    INDEX idx_contract_dates (contract_start_date, contract_end_date),
    INDEX idx_admin_email (admin_email),
    CONSTRAINT fk_tenant_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_tenant_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_tenant_plan_type CHECK (plan_type IN ('BASIC', 'STANDARD', 'PREMIUM', 'ENTERPRISE')),
    CONSTRAINT chk_tenant_status CHECK (status IN ('ACTIVE', 'SUSPENDED', 'TERMINATED')),
    CONSTRAINT chk_tenant_max_users CHECK (max_users > 0),
    CONSTRAINT chk_tenant_max_storage CHECK (max_storage_gb > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. テナントIDは一度設定すると変更不可（システム全体で参照されるため）
2. ドメインは任意設定だが、設定する場合は一意性を保証
3. 契約終了日がNULLの場合は無期限契約を表す
4. トライアル契約の場合、trial_end_dateを必ず設定
5. プラン変更時は履歴を別テーブルで管理することを推奨
6. テナント削除は論理削除（status='TERMINATED'）を基本とする

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成 |
