# テーブル定義書：MST_Role（ロール情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-002 |
| **テーブル名** | MST_Role |
| **論理名** | ロール情報 |
| **カテゴリ** | マスタ系 |
| **機能カテゴリ** | 認証・認可 |
| **優先度** | 高 |
| **個人情報含有** | なし |
| **機密情報レベル** | 中 |
| **暗号化要否** | 不要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
MST_Role（ロール情報）は、システム内のロール（役割）を管理するマスタテーブルです。

主な目的：
- システム内のロール定義・管理（管理者、一般ユーザー、閲覧者等）
- ロール階層の管理（上位ロール、下位ロール）
- ロール別権限設定の基盤
- 職務分離・最小権限の原則実装
- 動的権限管理・ロールベースアクセス制御（RBAC）
- 組織変更に対応した柔軟な権限管理
- 監査・コンプライアンス対応

このテーブルは、システムセキュリティの基盤となり、
適切なアクセス制御と権限管理を実現する重要なマスタデータです。


### 2.2 特記事項
- ロール階層は自己参照外部キーで表現
- システムロールは削除・変更不可
- テナント固有ロールはテナント内でのみ有効
- 複数ロール保持時は優先度で権限を決定
- 自動割り当て条件はJSON形式で柔軟に設定
- 有効期間による時限ロール設定が可能

### 2.3 関連API
API-003

### 2.4 関連バッチ
BATCH-003

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
| 8 | role_code | ロールコード | VARCHAR | 20 | ○ | - | - | - | ロールを一意に識別するコード（例：ROLE001） |
| 9 | role_name | ロール名 | VARCHAR | 100 | ○ | - | - | - | ロールの正式名称 |
| 10 | role_name_short | ロール名略称 | VARCHAR | 50 | ○ | - | - | - | ロールの略称・短縮名 |
| 11 | role_category | ロールカテゴリ | ENUM | None | ○ | - | - | - | ロールのカテゴリ（SYSTEM:システム、BUSINESS:業務、TENANT:テナント、CUSTOM:カスタム） |
| 12 | role_level | ロールレベル | INT | None | ○ | - | - | - | ロールの階層レベル（1:最上位、数値が大きいほど下位） |
| 13 | parent_role_id | 親ロールID | VARCHAR | 50 | ○ | - | ○ | - | 上位ロールのID（MST_Roleへの自己参照外部キー） |
| 14 | is_system_role | システムロールフラグ | BOOLEAN | None | ○ | - | - | False | システム標準ロールかどうか（削除・変更不可） |
| 15 | is_tenant_specific | テナント固有フラグ | BOOLEAN | None | ○ | - | - | False | テナント固有のロールかどうか |
| 16 | max_users | 最大ユーザー数 | INT | None | ○ | - | - | - | このロールに割り当て可能な最大ユーザー数 |
| 17 | role_priority | ロール優先度 | INT | None | ○ | - | - | 999 | 複数ロール保持時の優先度（数値が小さいほど高優先） |
| 18 | auto_assign_conditions | 自動割り当て条件 | JSON | None | ○ | - | - | - | 自動ロール割り当ての条件（JSON形式） |
| 19 | role_status | ロール状態 | ENUM | None | ○ | - | - | ACTIVE | ロールの状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨） |
| 20 | effective_from | 有効開始日 | DATE | None | ○ | - | - | - | ロールの有効開始日 |
| 21 | effective_to | 有効終了日 | DATE | None | ○ | - | - | - | ロールの有効終了日 |
| 22 | sort_order | 表示順序 | INT | None | ○ | - | - | - | 画面表示時の順序 |
| 23 | description | ロール説明 | TEXT | None | ○ | - | - | - | ロールの詳細説明・用途 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_role_code | UNIQUE INDEX | role_code | ロールコード検索用（一意） |
| idx_role_category | INDEX | role_category | ロールカテゴリ別検索用 |
| idx_role_level | INDEX | role_level | ロールレベル別検索用 |
| idx_parent_role | INDEX | parent_role_id | 親ロール別検索用 |
| idx_system_role | INDEX | is_system_role | システムロール検索用 |
| idx_tenant_specific | INDEX | is_tenant_specific | テナント固有ロール検索用 |
| idx_role_status | INDEX | role_status | ロール状態別検索用 |
| idx_effective_period | INDEX | effective_from, effective_to | 有効期間検索用 |
| idx_sort_order | INDEX | sort_order | 表示順序検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_role | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_role_code | UNIQUE | role_code | ['role_code'] |
| chk_role_level | CHECK |  | role_level > 0 |
| chk_role_category | CHECK |  | role_category IN ('SYSTEM', 'BUSINESS', 'TENANT', 'CUSTOM') |
| chk_role_status | CHECK |  | role_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED') |
| chk_max_users | CHECK |  | max_users IS NULL OR max_users > 0 |
| chk_role_priority | CHECK |  | role_priority > 0 |
| chk_effective_period | CHECK |  | effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to |
| chk_sort_order | CHECK |  | sort_order IS NULL OR sort_order >= 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_Role | parent_role_id | 1:N | 親ロールへの自己参照外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_Role (
    id, tenant_id, role_code, role_name, role_name_short, role_category, role_level, parent_role_id, is_system_role, is_tenant_specific, max_users, role_priority, auto_assign_conditions, role_status, effective_from, effective_to, sort_order, description, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'ROLE001', 'システム管理者', 'システム管理者', 'SYSTEM', '1', NULL, 'True', 'False', '5', '1', NULL, 'ACTIVE', '2025-01-01', NULL, '1', 'システム全体の管理権限を持つ最上位ロール', 'user_admin', 'user_admin'
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
- 機密情報：中レベル
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
-- ロール情報テーブル作成DDL
CREATE TABLE MST_Role (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    role_code VARCHAR(20) COMMENT 'ロールコード',
    role_name VARCHAR(100) COMMENT 'ロール名',
    role_name_short VARCHAR(50) COMMENT 'ロール名略称',
    role_category ENUM COMMENT 'ロールカテゴリ',
    role_level INT COMMENT 'ロールレベル',
    parent_role_id VARCHAR(50) COMMENT '親ロールID',
    is_system_role BOOLEAN DEFAULT False COMMENT 'システムロールフラグ',
    is_tenant_specific BOOLEAN DEFAULT False COMMENT 'テナント固有フラグ',
    max_users INT COMMENT '最大ユーザー数',
    role_priority INT DEFAULT 999 COMMENT 'ロール優先度',
    auto_assign_conditions JSON COMMENT '自動割り当て条件',
    role_status ENUM DEFAULT ACTIVE COMMENT 'ロール状態',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    sort_order INT COMMENT '表示順序',
    description TEXT COMMENT 'ロール説明',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_role_code (role_code),
    INDEX idx_role_category (role_category),
    INDEX idx_role_level (role_level),
    INDEX idx_parent_role (parent_role_id),
    INDEX idx_system_role (is_system_role),
    INDEX idx_tenant_specific (is_tenant_specific),
    INDEX idx_role_status (role_status),
    INDEX idx_effective_period (effective_from, effective_to),
    INDEX idx_sort_order (sort_order),
    CONSTRAINT fk_role_parent FOREIGN KEY (parent_role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ロール情報';

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

- ロールコードは新設時に自動採番（ROLE + 3桁連番）
- システムロールは is_system_role = true で保護
- 親ロールが無効化される場合は子ロールも無効化
- 最大ユーザー数を超える割り当ては不可
- 有効期間外のロールは自動的に無効化
- ロール削除時は関連するユーザーロール紐付けも削除
- テナント固有ロールは該当テナント内でのみ使用可能
