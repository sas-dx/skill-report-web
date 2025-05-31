# テーブル定義書：役職マスタ (MST_Position)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-008 |
| **テーブル名** | MST_Position |
| **論理名** | 役職マスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
役職マスタテーブル（MST_Position）は、組織内の役職情報を管理します。階層構造により役職の上下関係を表現し、人事システムとの連携により役職変更に対応します。社員の役職管理と権限制御の基盤となります。

### 2.2 関連API
- [API-006](../api/specs/API仕様書_API-006.md) - 組織情報管理API

### 2.3 関連バッチ
- [BATCH-004](../batch/specs/バッチ定義書_BATCH-004.md) - 社員情報同期バッチ
- [BATCH-015](../batch/specs/バッチ定義書_BATCH-015.md) - マスタデータ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | position_id | 役職ID | VARCHAR | 20 | × | ○ | - | - | 役職を一意に識別するID |
| 2 | position_code | 役職コード | VARCHAR | 10 | × | - | - | - | 人事システムの役職コード |
| 3 | position_name | 役職名 | VARCHAR | 100 | × | - | - | - | 役職の正式名称 |
| 4 | position_name_short | 役職名（略称） | VARCHAR | 50 | ○ | - | - | NULL | 役職の略称 |
| 5 | position_name_en | 役職名（英語） | VARCHAR | 100 | ○ | - | - | NULL | 役職名の英語表記 |
| 6 | position_level | 役職レベル | INTEGER | - | × | - | - | 1 | 役職の階層レベル（1:役員、2:部長、3:課長等） |
| 7 | position_rank | 役職ランク | INTEGER | - | × | - | - | 1 | 同レベル内での序列 |
| 8 | parent_position_id | 上位役職ID | VARCHAR | 20 | ○ | - | ○ | NULL | 上位役職のID |
| 9 | is_management | 管理職フラグ | BOOLEAN | - | × | - | - | FALSE | 管理職かどうか |
| 10 | is_executive | 役員フラグ | BOOLEAN | - | × | - | - | FALSE | 役員かどうか |
| 11 | authority_level | 権限レベル | INTEGER | - | × | - | - | 1 | システム内での権限レベル（1-10） |
| 12 | approval_limit | 承認限度額 | DECIMAL | 15,2 | ○ | - | - | NULL | 承認可能な金額上限 |
| 13 | salary_grade | 給与等級 | VARCHAR | 10 | ○ | - | - | NULL | 給与制度での等級 |
| 14 | description | 説明 | TEXT | - | ○ | - | - | NULL | 役職の職務内容・説明 |
| 15 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | 同レベル内での表示順序 |
| 16 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 17 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 役職が有効かどうか |
| 18 | effective_date | 有効開始日 | DATE | - | × | - | - | - | 役職の有効開始日 |
| 19 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | 役職の有効終了日 |
| 20 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 21 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 22 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 23 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | position_id | 主キー |
| idx_position_code | UNIQUE | position_code, tenant_id | 役職コードの一意性を保証（テナント内） |
| idx_parent | INDEX | parent_position_id | 上位役職検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_level | INDEX | position_level | 役職レベル検索用 |
| idx_rank | INDEX | position_rank | 役職ランク検索用 |
| idx_management | INDEX | is_management | 管理職検索用 |
| idx_executive | INDEX | is_executive | 役員検索用 |
| idx_authority | INDEX | authority_level | 権限レベル検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_position | PRIMARY KEY | position_id | 主キー制約 |
| uq_position_code | UNIQUE | position_code, tenant_id | 役職コードの一意性を保証（テナント内） |
| fk_parent_position | FOREIGN KEY | parent_position_id | MST_Position.position_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_position_level | CHECK | position_level | position_level >= 1 AND position_level <= 10 |
| chk_position_rank | CHECK | position_rank | position_rank >= 1 |
| chk_authority_level | CHECK | authority_level | authority_level >= 1 AND authority_level <= 10 |
| chk_approval_limit | CHECK | approval_limit | approval_limit IS NULL OR approval_limit >= 0 |
| chk_expiry_date | CHECK | expiry_date | expiry_date IS NULL OR expiry_date >= effective_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Position | parent_position_id | 1:N | 上位役職（自己参照） |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | position_id | 1:N | 所属社員 |
| MST_Position | parent_position_id | 1:N | 下位役職（自己参照） |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_Position (
    position_id, position_code, position_name,
    position_name_short, position_level, position_rank,
    parent_position_id, is_management, is_executive,
    authority_level, approval_limit, effective_date,
    tenant_id, created_by, updated_by
) VALUES (
    'POS_001',
    'MGR001',
    '部長',
    '部長',
    2,
    1,
    'POS_000',
    TRUE,
    FALSE,
    7,
    10000000.00,
    '2023-04-01',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 50件 | 既存役職体系 |
| 年間増加件数 | 5件 | 役職新設・変更 |
| 5年後想定件数 | 75件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：廃止から5年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id, is_active | 有効役職一覧取得 |
| SELECT | 高 | position_level | レベル別役職取得 |
| SELECT | 中 | is_management | 管理職一覧取得 |
| SELECT | 中 | authority_level | 権限レベル検索 |
| UPDATE | 低 | position_id | 役職情報更新 |
| INSERT | 低 | - | 新規役職作成 |

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
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（組織構造、権限情報）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：人事システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_Position (
    position_id VARCHAR(20) NOT NULL,
    position_code VARCHAR(10) NOT NULL,
    position_name VARCHAR(100) NOT NULL,
    position_name_short VARCHAR(50) NULL,
    position_name_en VARCHAR(100) NULL,
    position_level INTEGER NOT NULL DEFAULT 1,
    position_rank INTEGER NOT NULL DEFAULT 1,
    parent_position_id VARCHAR(20) NULL,
    is_management BOOLEAN NOT NULL DEFAULT FALSE,
    is_executive BOOLEAN NOT NULL DEFAULT FALSE,
    authority_level INTEGER NOT NULL DEFAULT 1,
    approval_limit DECIMAL(15,2) NULL,
    salary_grade VARCHAR(10) NULL,
    description TEXT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    effective_date DATE NOT NULL,
    expiry_date DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (position_id),
    UNIQUE KEY idx_position_code (position_code, tenant_id),
    INDEX idx_parent (parent_position_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_level (position_level),
    INDEX idx_rank (position_rank),
    INDEX idx_management (is_management),
    INDEX idx_executive (is_executive),
    INDEX idx_authority (authority_level),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    CONSTRAINT fk_position_parent FOREIGN KEY (parent_position_id) REFERENCES MST_Position(position_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_position_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_position_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_position_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_position_level CHECK (position_level >= 1 AND position_level <= 10),
    CONSTRAINT chk_position_rank CHECK (position_rank >= 1),
    CONSTRAINT chk_position_authority_level CHECK (authority_level >= 1 AND authority_level <= 10),
    CONSTRAINT chk_position_approval_limit CHECK (approval_limit IS NULL OR approval_limit >= 0),
    CONSTRAINT chk_position_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. 階層構造により役職の上下関係を表現
2. 役職レベルと役職ランクにより詳細な序列管理が可能
3. 管理職フラグと役員フラグにより権限制御を実装
4. 権限レベルによりシステム内での操作権限を制御
5. 承認限度額により承認ワークフローの制御が可能
6. 有効期間により役職変更履歴を管理
7. 役職廃止時は論理削除（is_active=FALSE）を使用
8. 人事システムとの定期同期により最新役職情報を維持
9. 給与等級により人事制度との連携が可能

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
