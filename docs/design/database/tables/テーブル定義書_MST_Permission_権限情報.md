# テーブル定義書：MST_Permission（権限情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-003 |
| **テーブル名** | MST_Permission |
| **論理名** | 権限情報 |
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
MST_Permission（権限情報）は、システム内の権限（許可）を管理するマスタテーブルです。

主な目的：
- システム内の権限定義・管理（画面アクセス、機能実行、データ操作等）
- 権限の階層・グループ管理
- 細粒度アクセス制御の実現
- リソースベースアクセス制御（RBAC）の基盤
- 動的権限管理・条件付きアクセス制御
- 監査・コンプライアンス要件への対応
- 最小権限の原則実装

このテーブルは、ロールと組み合わせてシステムセキュリティを構成し、
適切なアクセス制御を実現する重要なマスタデータです。


### 2.2 特記事項
- 権限階層は自己参照外部キーで表現
- システム権限は削除・変更不可
- 条件式はSQL WHERE句形式で記述
- リスクレベルに応じた承認・監査要件
- スコープレベルによる権限範囲制限
- 有効期間による時限権限設定が可能

### 2.3 関連API
API-003, API-004

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
| 8 | permission_code | 権限コード | VARCHAR | 50 | ○ | - | - | - | 権限を一意に識別するコード（例：PERM_USER_READ） |
| 9 | permission_name | 権限名 | VARCHAR | 100 | ○ | - | - | - | 権限の正式名称 |
| 10 | permission_name_short | 権限名略称 | VARCHAR | 50 | ○ | - | - | - | 権限の略称・短縮名 |
| 11 | permission_category | 権限カテゴリ | ENUM | None | ○ | - | - | - | 権限のカテゴリ（SYSTEM:システム、SCREEN:画面、API:API、DATA:データ、FUNCTION:機能） |
| 12 | resource_type | リソース種別 | VARCHAR | 50 | ○ | - | - | - | 権限対象のリソース種別（USER、SKILL、REPORT等） |
| 13 | action_type | アクション種別 | ENUM | None | ○ | - | - | - | 許可するアクション（CREATE:作成、READ:参照、UPDATE:更新、DELETE:削除、EXECUTE:実行） |
| 14 | scope_level | スコープレベル | ENUM | None | ○ | - | - | - | 権限のスコープ（GLOBAL:全体、TENANT:テナント、DEPARTMENT:部署、SELF:自分のみ） |
| 15 | parent_permission_id | 親権限ID | VARCHAR | 50 | ○ | - | ○ | - | 上位権限のID（MST_Permissionへの自己参照外部キー） |
| 16 | is_system_permission | システム権限フラグ | BOOLEAN | None | ○ | - | - | False | システム標準権限かどうか（削除・変更不可） |
| 17 | requires_conditions | 条件要求フラグ | BOOLEAN | None | ○ | - | - | False | 権限行使に条件が必要かどうか |
| 18 | condition_expression | 条件式 | TEXT | None | ○ | - | - | - | 権限行使の条件式（SQL WHERE句形式等） |
| 19 | risk_level | リスクレベル | INT | None | ○ | - | - | 1 | 権限のリスクレベル（1:低、2:中、3:高、4:最高） |
| 20 | requires_approval | 承認要求フラグ | BOOLEAN | None | ○ | - | - | False | 権限行使に承認が必要かどうか |
| 21 | audit_required | 監査要求フラグ | BOOLEAN | None | ○ | - | - | False | 権限行使時の監査ログ記録が必要かどうか |
| 22 | permission_status | 権限状態 | ENUM | None | ○ | - | - | ACTIVE | 権限の状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨） |
| 23 | effective_from | 有効開始日 | DATE | None | ○ | - | - | - | 権限の有効開始日 |
| 24 | effective_to | 有効終了日 | DATE | None | ○ | - | - | - | 権限の有効終了日 |
| 25 | sort_order | 表示順序 | INT | None | ○ | - | - | - | 画面表示時の順序 |
| 26 | description | 権限説明 | TEXT | None | ○ | - | - | - | 権限の詳細説明・用途 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_permission_code | UNIQUE INDEX | permission_code | 権限コード検索用（一意） |
| idx_permission_category | INDEX | permission_category | 権限カテゴリ別検索用 |
| idx_resource_action | INDEX | resource_type, action_type | リソース・アクション別検索用 |
| idx_scope_level | INDEX | scope_level | スコープレベル別検索用 |
| idx_parent_permission | INDEX | parent_permission_id | 親権限別検索用 |
| idx_system_permission | INDEX | is_system_permission | システム権限検索用 |
| idx_risk_level | INDEX | risk_level | リスクレベル別検索用 |
| idx_permission_status | INDEX | permission_status | 権限状態別検索用 |
| idx_effective_period | INDEX | effective_from, effective_to | 有効期間検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_permission | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_permission_code | UNIQUE | permission_code | ['permission_code'] |
| chk_permission_category | CHECK |  | permission_category IN ('SYSTEM', 'SCREEN', 'API', 'DATA', 'FUNCTION') |
| chk_action_type | CHECK |  | action_type IN ('CREATE', 'READ', 'UPDATE', 'DELETE', 'EXECUTE') |
| chk_scope_level | CHECK |  | scope_level IN ('GLOBAL', 'TENANT', 'DEPARTMENT', 'SELF') |
| chk_permission_status | CHECK |  | permission_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED') |
| chk_risk_level | CHECK |  | risk_level BETWEEN 1 AND 4 |
| chk_effective_period | CHECK |  | effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to |
| chk_sort_order | CHECK |  | sort_order IS NULL OR sort_order >= 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_Permission | parent_permission_id | 1:N | 親権限への自己参照外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_Permission (
    id, tenant_id, permission_code, permission_name, permission_name_short, permission_category, resource_type, action_type, scope_level, parent_permission_id, is_system_permission, requires_conditions, condition_expression, risk_level, requires_approval, audit_required, permission_status, effective_from, effective_to, sort_order, description, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'PERM_USER_READ', 'ユーザー情報参照', 'ユーザー参照', 'DATA', 'USER', 'READ', 'TENANT', NULL, 'True', 'False', NULL, '1', 'False', 'True', 'ACTIVE', '2025-01-01', NULL, '1', 'ユーザー情報の参照権限', 'user_admin', 'user_admin'
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
-- 権限情報テーブル作成DDL
CREATE TABLE MST_Permission (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    permission_code VARCHAR(50) COMMENT '権限コード',
    permission_name VARCHAR(100) COMMENT '権限名',
    permission_name_short VARCHAR(50) COMMENT '権限名略称',
    permission_category ENUM COMMENT '権限カテゴリ',
    resource_type VARCHAR(50) COMMENT 'リソース種別',
    action_type ENUM COMMENT 'アクション種別',
    scope_level ENUM COMMENT 'スコープレベル',
    parent_permission_id VARCHAR(50) COMMENT '親権限ID',
    is_system_permission BOOLEAN DEFAULT False COMMENT 'システム権限フラグ',
    requires_conditions BOOLEAN DEFAULT False COMMENT '条件要求フラグ',
    condition_expression TEXT COMMENT '条件式',
    risk_level INT DEFAULT 1 COMMENT 'リスクレベル',
    requires_approval BOOLEAN DEFAULT False COMMENT '承認要求フラグ',
    audit_required BOOLEAN DEFAULT False COMMENT '監査要求フラグ',
    permission_status ENUM DEFAULT ACTIVE COMMENT '権限状態',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    sort_order INT COMMENT '表示順序',
    description TEXT COMMENT '権限説明',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_permission_code (permission_code),
    INDEX idx_permission_category (permission_category),
    INDEX idx_resource_action (resource_type, action_type),
    INDEX idx_scope_level (scope_level),
    INDEX idx_parent_permission (parent_permission_id),
    INDEX idx_system_permission (is_system_permission),
    INDEX idx_risk_level (risk_level),
    INDEX idx_permission_status (permission_status),
    INDEX idx_effective_period (effective_from, effective_to),
    CONSTRAINT fk_permission_parent FOREIGN KEY (parent_permission_id) REFERENCES MST_Permission(id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='権限情報';

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

- 権限コードは PERM_ + リソース + アクション 形式
- システム権限は is_system_permission = true で保護
- リスクレベル3以上は承認要求を推奨
- 全ての権限行使は監査ログに記録
- 条件付き権限は condition_expression で制御
- 親権限が無効化される場合は子権限も無効化
- 有効期間外の権限は自動的に無効化
