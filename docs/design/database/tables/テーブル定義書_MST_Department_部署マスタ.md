# テーブル定義書：MST_Department（部署マスタ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-007 |
| **テーブル名** | MST_Department |
| **論理名** | 部署マスタ |
| **カテゴリ** | マスタ系 |
| **機能カテゴリ** | プロフィール管理 |
| **優先度** | 最高 |
| **個人情報含有** | なし |
| **機密情報レベル** | 低 |
| **暗号化要否** | 不要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
MST_Department（部署マスタ）は、組織の部署・組織単位の階層構造と基本情報を管理するマスタテーブルです。

主な目的：
- 組織階層の構造管理（部署、課、チーム等の階層関係）
- 部署基本情報の管理（部署名、部署コード、責任者等）
- 組織変更履歴の管理（統廃合、新設、移管等）
- 予算・コスト管理の組織単位設定
- 権限・アクセス制御の組織単位設定
- 人事異動・配置管理の基盤
- 組織図・レポート作成の基礎データ

このテーブルは、人事管理、権限管理、予算管理、レポート作成など、
組織運営の様々な業務プロセスの基盤となる重要なマスタデータです。


### 2.2 特記事項
- 組織階層は自己参照外部キーで表現
- 部署レベルは階層の深さを表す（1が最上位）
- 廃止された部署も履歴として保持（論理削除）
- コストセンターコードは予算管理システムと連携
- 部署長・副部署長は必須ではない（空席の場合もある）
- 表示順序は組織図作成時に使用

### 2.3 関連API
API-006

### 2.4 関連バッチ
BATCH-004, BATCH-015

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | VARCHAR | 50 | × | ○ | - | - | 主キー |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | レコードが有効かどうか |
| 4 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 5 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 6 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 7 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |
| 8 | department_code | 部署コード | VARCHAR | 20 | ○ | - | - | - | 部署を一意に識別するコード（例：DEPT001） |
| 9 | department_name | 部署名 | VARCHAR | 100 | ○ | - | - | - | 部署の正式名称 |
| 10 | department_name_short | 部署名略称 | VARCHAR | 50 | ○ | - | - | - | 部署の略称・短縮名 |
| 11 | parent_department_id | 親部署ID | VARCHAR | 50 | ○ | - | ○ | - | 上位部署のID（MST_Departmentへの自己参照外部キー） |
| 12 | department_level | 部署レベル | INT | None | ○ | - | - | - | 組織階層のレベル（1:本部、2:部、3:課、4:チーム等） |
| 13 | department_type | 部署種別 | ENUM | None | ○ | - | - | - | 部署の種別（HEADQUARTERS:本部、DIVISION:事業部、DEPARTMENT:部、SECTION:課、TEAM:チーム） |
| 14 | manager_id | 部署長ID | VARCHAR | 50 | ○ | - | ○ | - | 部署長の社員ID（MST_Employeeへの外部キー） |
| 15 | deputy_manager_id | 副部署長ID | VARCHAR | 50 | ○ | - | ○ | - | 副部署長の社員ID（MST_Employeeへの外部キー） |
| 16 | cost_center_code | コストセンターコード | VARCHAR | 20 | ○ | - | - | - | 予算管理用のコストセンターコード |
| 17 | budget_amount | 予算額 | DECIMAL | 15,2 | ○ | - | - | - | 年間予算額（円） |
| 18 | location | 所在地 | VARCHAR | 200 | ○ | - | - | - | 部署の物理的な所在地・フロア等 |
| 19 | phone_number | 代表電話番号 | VARCHAR | 20 | ○ | - | - | - | 部署の代表電話番号 |
| 20 | email_address | 代表メールアドレス | VARCHAR | 255 | ○ | - | - | - | 部署の代表メールアドレス |
| 21 | establishment_date | 設立日 | DATE | None | ○ | - | - | - | 部署の設立・新設日 |
| 22 | abolition_date | 廃止日 | DATE | None | ○ | - | - | - | 部署の廃止・統合日 |
| 23 | department_status | 部署状態 | ENUM | None | ○ | - | - | ACTIVE | 部署の状態（ACTIVE:有効、INACTIVE:無効、MERGED:統合、ABOLISHED:廃止） |
| 24 | sort_order | 表示順序 | INT | None | ○ | - | - | - | 組織図等での表示順序 |
| 25 | description | 部署説明 | TEXT | None | ○ | - | - | - | 部署の役割・業務内容の説明 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_department_code | UNIQUE INDEX | department_code | 部署コード検索用（一意） |
| idx_parent_department | INDEX | parent_department_id | 親部署別検索用 |
| idx_department_level | INDEX | department_level | 部署レベル別検索用 |
| idx_department_type | INDEX | department_type | 部署種別検索用 |
| idx_manager | INDEX | manager_id | 部署長別検索用 |
| idx_status | INDEX | department_status | 部署状態別検索用 |
| idx_cost_center | INDEX | cost_center_code | コストセンター別検索用 |
| idx_sort_order | INDEX | sort_order | 表示順序検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_department | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_department_code | UNIQUE | department_code | ['department_code'] |
| chk_department_level | CHECK |  | department_level > 0 |
| chk_department_type | CHECK |  | department_type IN ('HEADQUARTERS', 'DIVISION', 'DEPARTMENT', 'SECTION', 'TEAM') |
| chk_department_status | CHECK |  | department_status IN ('ACTIVE', 'INACTIVE', 'MERGED', 'ABOLISHED') |
| chk_budget_amount | CHECK |  | budget_amount IS NULL OR budget_amount >= 0 |
| chk_sort_order | CHECK |  | sort_order IS NULL OR sort_order >= 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_Department | parent_department_id | 1:N | 親部署への自己参照外部キー |
| MST_Employee | manager_id | 1:N | 部署長への外部キー |
| MST_Employee | deputy_manager_id | 1:N | 副部署長への外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_Department (
    id, tenant_id, department_code, department_name, department_name_short, parent_department_id, department_level, department_type, manager_id, deputy_manager_id, cost_center_code, budget_amount, location, phone_number, email_address, establishment_date, abolition_date, department_status, sort_order, description, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'DEPT001', '経営企画本部', '経営企画', NULL, '1', 'HEADQUARTERS', 'EMP000001', NULL, 'CC001', '50000000.0', '本社ビル 10F', '03-1234-5678', 'planning@company.com', '2020-04-01', NULL, 'ACTIVE', '1', '会社全体の経営戦略立案・推進を担当', 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 初期設定データ |
| 月間増加件数 | 100件 | 想定値 |
| 年間増加件数 | 1,200件 | 想定値 |
| 5年後想定件数 | 6,500件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | id, tenant_id | 基本検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新処理 |
| DELETE | 低 | id | 削除処理 |

### 7.2 パフォーマンス要件
- SELECT：15ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| user | ○ | × | × | × | 一般ユーザー（参照のみ） |

### 8.2 データ保護
- 個人情報：なし
- 機密情報：低レベル
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
-- 部署マスタテーブル作成DDL
CREATE TABLE MST_Department (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    department_code VARCHAR(20) COMMENT '部署コード',
    department_name VARCHAR(100) COMMENT '部署名',
    department_name_short VARCHAR(50) COMMENT '部署名略称',
    parent_department_id VARCHAR(50) COMMENT '親部署ID',
    department_level INT COMMENT '部署レベル',
    department_type ENUM COMMENT '部署種別',
    manager_id VARCHAR(50) COMMENT '部署長ID',
    deputy_manager_id VARCHAR(50) COMMENT '副部署長ID',
    cost_center_code VARCHAR(20) COMMENT 'コストセンターコード',
    budget_amount DECIMAL(15,2) COMMENT '予算額',
    location VARCHAR(200) COMMENT '所在地',
    phone_number VARCHAR(20) COMMENT '代表電話番号',
    email_address VARCHAR(255) COMMENT '代表メールアドレス',
    establishment_date DATE COMMENT '設立日',
    abolition_date DATE COMMENT '廃止日',
    department_status ENUM DEFAULT ACTIVE COMMENT '部署状態',
    sort_order INT COMMENT '表示順序',
    description TEXT COMMENT '部署説明',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_department_code (department_code),
    INDEX idx_parent_department (parent_department_id),
    INDEX idx_department_level (department_level),
    INDEX idx_department_type (department_type),
    INDEX idx_manager (manager_id),
    INDEX idx_status (department_status),
    INDEX idx_cost_center (cost_center_code),
    INDEX idx_sort_order (sort_order),
    CONSTRAINT fk_department_parent FOREIGN KEY (parent_department_id) REFERENCES MST_Department(id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_department_manager FOREIGN KEY (manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_department_deputy FOREIGN KEY (deputy_manager_id) REFERENCES MST_Employee(id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='部署マスタ';

```

## 10. 特記事項

1. **設計方針**
   - マスタ系として設計
   - マルチテナント対応
   - 監査証跡の保持

2. **運用上の注意点**
   - 定期的なデータクリーンアップが必要
   - パフォーマンス監視を実施
   - データ量見積もりの定期見直し

3. **今後の拡張予定**
   - 必要に応じて機能拡張を検討

4. **関連画面**
   - 関連画面情報

5. **データ量・パフォーマンス監視**
   - データ量が想定の150%を超えた場合はアラート
   - 応答時間が設定値の120%を超えた場合は調査


## 11. 業務ルール

- 部署コードは設立時に自動採番（DEPT + 3桁連番）
- 親部署が廃止される場合は子部署の再配置が必要
- 部署長は当該部署または上位部署の社員のみ設定可能
- 廃止時は department_status を ABOLISHED に変更
- 統合時は department_status を MERGED に変更
- 予算額は年度初めに設定・更新
- 組織変更は月初めに実施することを原則とする
