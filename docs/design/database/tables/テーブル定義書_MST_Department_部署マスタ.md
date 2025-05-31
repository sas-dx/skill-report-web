# テーブル定義書：部署マスタ (MST_Department)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-007 |
| **テーブル名** | MST_Department |
| **論理名** | 部署マスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
部署マスタテーブル（MST_Department）は、組織の部署情報を管理します。階層構造により部署の上下関係を表現し、人事システムとの連携により組織変更に対応します。社員の所属部署管理とレポート集計の基盤となります。

### 2.2 関連API
- [API-006](../api/specs/API仕様書_API-006.md) - 組織情報管理API

### 2.3 関連バッチ
- [BATCH-004](../batch/specs/バッチ定義書_BATCH-004.md) - 社員情報同期バッチ
- [BATCH-015](../batch/specs/バッチ定義書_BATCH-015.md) - マスタデータ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | department_id | 部署ID | VARCHAR | 20 | × | ○ | - | - | 部署を一意に識別するID |
| 2 | department_code | 部署コード | VARCHAR | 10 | × | - | - | - | 人事システムの部署コード |
| 3 | department_name | 部署名 | VARCHAR | 100 | × | - | - | - | 部署の正式名称 |
| 4 | department_name_short | 部署名（略称） | VARCHAR | 50 | ○ | - | - | NULL | 部署の略称 |
| 5 | department_name_en | 部署名（英語） | VARCHAR | 100 | ○ | - | - | NULL | 部署名の英語表記 |
| 6 | parent_department_id | 親部署ID | VARCHAR | 20 | ○ | - | ○ | NULL | 上位部署のID |
| 7 | department_level | 階層レベル | INTEGER | - | × | - | - | 1 | 組織階層のレベル（1:本部、2:部、3:課等） |
| 8 | department_path | 部署パス | VARCHAR | 500 | × | - | - | - | 階層構造を表すパス（/本部/部/課） |
| 9 | manager_id | 部署長ID | VARCHAR | 20 | ○ | - | ○ | NULL | 部署長の社員ID |
| 10 | cost_center_code | コストセンターコード | VARCHAR | 20 | ○ | - | - | NULL | 経理システムのコストセンター |
| 11 | location | 所在地 | VARCHAR | 100 | ○ | - | - | NULL | 部署の主な所在地 |
| 12 | phone_number | 代表電話番号 | VARCHAR | 20 | ○ | - | - | NULL | 部署の代表電話番号 |
| 13 | email | 代表メールアドレス | VARCHAR | 255 | ○ | - | - | NULL | 部署の代表メールアドレス |
| 14 | description | 説明 | TEXT | - | ○ | - | - | NULL | 部署の業務内容・説明 |
| 15 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | 同階層内での表示順序 |
| 16 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 17 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 部署が有効かどうか |
| 18 | effective_date | 有効開始日 | DATE | - | × | - | - | - | 部署の有効開始日 |
| 19 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | 部署の有効終了日 |
| 20 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 21 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 22 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 23 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | department_id | 主キー |
| idx_department_code | UNIQUE | department_code, tenant_id | 部署コードの一意性を保証（テナント内） |
| idx_parent | INDEX | parent_department_id | 親部署検索用 |
| idx_manager | INDEX | manager_id | 部署長検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_level | INDEX | department_level | 階層レベル検索用 |
| idx_path | INDEX | department_path | 部署パス検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_department | PRIMARY KEY | department_id | 主キー制約 |
| uq_department_code | UNIQUE | department_code, tenant_id | 部署コードの一意性を保証（テナント内） |
| fk_parent_department | FOREIGN KEY | parent_department_id | MST_Department.department_id |
| fk_manager | FOREIGN KEY | manager_id | MST_Employee.employee_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_department_level | CHECK | department_level | department_level >= 1 AND department_level <= 10 |
| chk_expiry_date | CHECK | expiry_date | expiry_date IS NULL OR expiry_date >= effective_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Department | parent_department_id | 1:N | 親部署（自己参照） |
| MST_Employee | manager_id | 1:N | 部署長 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | department_id | 1:N | 所属社員 |
| MST_Department | parent_department_id | 1:N | 子部署（自己参照） |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_Department (
    department_id, department_code, department_name,
    department_name_short, parent_department_id, department_level,
    department_path, manager_id, cost_center_code,
    location, effective_date, tenant_id,
    created_by, updated_by
) VALUES (
    'DEPT_001',
    'IT001',
    'システム開発部',
    'システム部',
    'DEPT_000',
    2,
    '/本社/システム開発部',
    'EMP_001',
    'CC001',
    '東京本社',
    '2023-04-01',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 100件 | 既存組織構造 |
| 年間増加件数 | 10件 | 組織変更・新設 |
| 5年後想定件数 | 150件 | 想定値 |

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
| SELECT | 高 | tenant_id, is_active | 有効部署一覧取得 |
| SELECT | 高 | parent_department_id | 子部署一覧取得 |
| SELECT | 中 | department_level | 階層別部署取得 |
| SELECT | 中 | department_path | パス検索 |
| UPDATE | 低 | department_id | 部署情報更新 |
| INSERT | 低 | - | 新規部署作成 |

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
- 機密情報：含む（組織構造）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：人事システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_Department (
    department_id VARCHAR(20) NOT NULL,
    department_code VARCHAR(10) NOT NULL,
    department_name VARCHAR(100) NOT NULL,
    department_name_short VARCHAR(50) NULL,
    department_name_en VARCHAR(100) NULL,
    parent_department_id VARCHAR(20) NULL,
    department_level INTEGER NOT NULL DEFAULT 1,
    department_path VARCHAR(500) NOT NULL,
    manager_id VARCHAR(20) NULL,
    cost_center_code VARCHAR(20) NULL,
    location VARCHAR(100) NULL,
    phone_number VARCHAR(20) NULL,
    email VARCHAR(255) NULL,
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
    PRIMARY KEY (department_id),
    UNIQUE KEY idx_department_code (department_code, tenant_id),
    INDEX idx_parent (parent_department_id),
    INDEX idx_manager (manager_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_level (department_level),
    INDEX idx_path (department_path),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    CONSTRAINT fk_department_parent FOREIGN KEY (parent_department_id) REFERENCES MST_Department(department_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_department_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_department_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_department_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_department_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_department_level CHECK (department_level >= 1 AND department_level <= 10),
    CONSTRAINT chk_department_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. 階層構造により組織の上下関係を表現
2. 部署パス（department_path）により階層の可視化が可能
3. 有効期間により組織変更履歴を管理
4. 部署廃止時は論理削除（is_active=FALSE）を使用
5. 人事システムとの定期同期により最新組織情報を維持
6. 部署長は必須ではないが、設定推奨
7. コストセンターコードにより経理システムとの連携が可能
8. 同階層内での表示順序はsort_orderで制御

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
