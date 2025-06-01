# テーブル定義書：MST_UserRole（ユーザーロール紐付け）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-004 |
| **テーブル名** | MST_UserRole |
| **論理名** | ユーザーロール紐付け |
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
MST_UserRole（ユーザーロール紐付け）は、ユーザーとロールの関連付けを管理するマスタテーブルです。

主な目的：
- ユーザーとロールの多対多関係管理
- 動的なロール割り当て・解除
- 時限ロール・条件付きロール割り当て
- ロール継承・委譲の管理
- 権限昇格・降格の履歴管理
- 職務分離・最小権限の原則実装
- 監査・コンプライアンス対応

このテーブルは、ユーザーの実際の権限を決定する重要な関連テーブルであり、
システムセキュリティの実装において中核的な役割を果たします。


### 2.2 特記事項
- ユーザーとロールの多対多関係を管理
- 時限ロール・条件付きロールに対応
- 委譲ロールによる一時的権限移譲が可能
- 承認フローによる権限昇格制御
- 使用状況の追跡・監査が可能
- 主ロールによる基本権限の明確化

### 2.3 関連API
API-004

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
| 8 | user_id | ユーザーID | VARCHAR | 50 | ○ | - | ○ | - | ユーザーのID（MST_UserAuthへの外部キー） |
| 9 | role_id | ロールID | VARCHAR | 50 | ○ | - | ○ | - | ロールのID（MST_Roleへの外部キー） |
| 10 | assignment_type | 割り当て種別 | ENUM | None | ○ | - | - | DIRECT | ロール割り当ての種別（DIRECT:直接、INHERITED:継承、DELEGATED:委譲、TEMPORARY:一時的） |
| 11 | assigned_by | 割り当て者ID | VARCHAR | 50 | ○ | - | - | - | ロールを割り当てた管理者のID（MST_UserAuthへの外部キー） |
| 12 | assignment_reason | 割り当て理由 | TEXT | None | ○ | - | - | - | ロール割り当ての理由・根拠 |
| 13 | effective_from | 有効開始日時 | TIMESTAMP | None | ○ | - | - | CURRENT_TIMESTAMP | ロール割り当ての有効開始日時 |
| 14 | effective_to | 有効終了日時 | TIMESTAMP | None | ○ | - | - | - | ロール割り当ての有効終了日時 |
| 15 | is_primary_role | 主ロールフラグ | BOOLEAN | None | ○ | - | - | False | ユーザーの主要ロールかどうか |
| 16 | priority_order | 優先順序 | INT | None | ○ | - | - | 999 | 複数ロール保持時の優先順序（数値が小さいほど高優先） |
| 17 | conditions | 適用条件 | JSON | None | ○ | - | - | - | ロール適用の条件（時間帯、場所、状況等をJSON形式） |
| 18 | delegation_source_user_id | 委譲元ユーザーID | VARCHAR | 50 | ○ | - | ○ | - | 委譲ロールの場合の委譲元ユーザーID |
| 19 | delegation_expires_at | 委譲期限 | TIMESTAMP | None | ○ | - | - | - | 委譲ロールの期限 |
| 20 | auto_assigned | 自動割り当てフラグ | BOOLEAN | None | ○ | - | - | False | システムによる自動割り当てかどうか |
| 21 | requires_approval | 承認要求フラグ | BOOLEAN | None | ○ | - | - | False | ロール行使に承認が必要かどうか |
| 22 | approval_status | 承認状態 | ENUM | None | ○ | - | - | - | 承認の状態（PENDING:承認待ち、APPROVED:承認済み、REJECTED:却下） |
| 23 | approved_by | 承認者ID | VARCHAR | 50 | ○ | - | - | - | ロール割り当てを承認した管理者のID |
| 24 | approved_at | 承認日時 | TIMESTAMP | None | ○ | - | - | - | ロール割り当てが承認された日時 |
| 25 | assignment_status | 割り当て状態 | ENUM | None | ○ | - | - | ACTIVE | 割り当ての状態（ACTIVE:有効、INACTIVE:無効、SUSPENDED:停止、EXPIRED:期限切れ） |
| 26 | last_used_at | 最終使用日時 | TIMESTAMP | None | ○ | - | - | - | このロールが最後に使用された日時 |
| 27 | usage_count | 使用回数 | INT | None | ○ | - | - | 0 | このロールが使用された回数 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_user_role | UNIQUE INDEX | user_id, role_id | ユーザー・ロール組み合わせ検索用（一意） |
| idx_user_id | INDEX | user_id | ユーザー別検索用 |
| idx_role_id | INDEX | role_id | ロール別検索用 |
| idx_assignment_type | INDEX | assignment_type | 割り当て種別検索用 |
| idx_assigned_by | INDEX | assigned_by | 割り当て者別検索用 |
| idx_effective_period | INDEX | effective_from, effective_to | 有効期間検索用 |
| idx_primary_role | INDEX | user_id, is_primary_role | 主ロール検索用 |
| idx_assignment_status | INDEX | assignment_status | 割り当て状態別検索用 |
| idx_approval_status | INDEX | approval_status | 承認状態別検索用 |
| idx_delegation_source | INDEX | delegation_source_user_id | 委譲元ユーザー検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_userrole | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_user_role_active | UNIQUE | user_id, role_id, assignment_status | ['user_id', 'role_id', 'assignment_status'] |
| chk_assignment_type | CHECK |  | assignment_type IN ('DIRECT', 'INHERITED', 'DELEGATED', 'TEMPORARY') |
| chk_assignment_status | CHECK |  | assignment_status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'EXPIRED') |
| chk_approval_status | CHECK |  | approval_status IS NULL OR approval_status IN ('PENDING', 'APPROVED', 'REJECTED') |
| chk_effective_period | CHECK |  | effective_to IS NULL OR effective_from <= effective_to |
| chk_delegation_period | CHECK |  | delegation_expires_at IS NULL OR effective_from <= delegation_expires_at |
| chk_priority_order | CHECK |  | priority_order > 0 |
| chk_usage_count | CHECK |  | usage_count >= 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_UserAuth | user_id | 1:N | ユーザーへの外部キー |
| MST_Role | role_id | 1:N | ロールへの外部キー |
| MST_UserAuth | assigned_by | 1:N | 割り当て者への外部キー |
| MST_UserAuth | delegation_source_user_id | 1:N | 委譲元ユーザーへの外部キー |
| MST_UserAuth | approved_by | 1:N | 承認者への外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_UserRole (
    id, tenant_id, user_id, role_id, assignment_type, assigned_by, assignment_reason, effective_from, effective_to, is_primary_role, priority_order, conditions, delegation_source_user_id, delegation_expires_at, auto_assigned, requires_approval, approval_status, approved_by, approved_at, assignment_status, last_used_at, usage_count, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'USER000001', 'ROLE003', 'DIRECT', 'USER000000', '新規ユーザー登録時の標準ロール割り当て', '2025-01-01 00:00:00', NULL, 'True', '1', NULL, NULL, NULL, 'True', 'False', NULL, NULL, NULL, 'ACTIVE', '2025-06-01 09:00:00', '150', 'user_admin', 'user_admin'
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
-- ユーザーロール紐付けテーブル作成DDL
CREATE TABLE MST_UserRole (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    user_id VARCHAR(50) COMMENT 'ユーザーID',
    role_id VARCHAR(50) COMMENT 'ロールID',
    assignment_type ENUM DEFAULT DIRECT COMMENT '割り当て種別',
    assigned_by VARCHAR(50) COMMENT '割り当て者ID',
    assignment_reason TEXT COMMENT '割り当て理由',
    effective_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '有効開始日時',
    effective_to TIMESTAMP COMMENT '有効終了日時',
    is_primary_role BOOLEAN DEFAULT False COMMENT '主ロールフラグ',
    priority_order INT DEFAULT 999 COMMENT '優先順序',
    conditions JSON COMMENT '適用条件',
    delegation_source_user_id VARCHAR(50) COMMENT '委譲元ユーザーID',
    delegation_expires_at TIMESTAMP COMMENT '委譲期限',
    auto_assigned BOOLEAN DEFAULT False COMMENT '自動割り当てフラグ',
    requires_approval BOOLEAN DEFAULT False COMMENT '承認要求フラグ',
    approval_status ENUM COMMENT '承認状態',
    approved_by VARCHAR(50) COMMENT '承認者ID',
    approved_at TIMESTAMP COMMENT '承認日時',
    assignment_status ENUM DEFAULT ACTIVE COMMENT '割り当て状態',
    last_used_at TIMESTAMP COMMENT '最終使用日時',
    usage_count INT DEFAULT 0 COMMENT '使用回数',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_user_role (user_id, role_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role_id (role_id),
    INDEX idx_assignment_type (assignment_type),
    INDEX idx_assigned_by (assigned_by),
    INDEX idx_effective_period (effective_from, effective_to),
    INDEX idx_primary_role (user_id, is_primary_role),
    INDEX idx_assignment_status (assignment_status),
    INDEX idx_approval_status (approval_status),
    INDEX idx_delegation_source (delegation_source_user_id),
    CONSTRAINT fk_userrole_user FOREIGN KEY (user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_userrole_role FOREIGN KEY (role_id) REFERENCES MST_Role(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_userrole_assigned_by FOREIGN KEY (assigned_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_userrole_delegation_source FOREIGN KEY (delegation_source_user_id) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_userrole_approved_by FOREIGN KEY (approved_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ユーザーロール紐付け';

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

- 1ユーザーにつき1つの主ロール（is_primary_role=true）のみ
- 有効期間外のロール割り当ては自動的に EXPIRED 状態に変更
- 委譲ロールは委譲期限で自動失効
- 承認要求ロールは承認完了まで使用不可
- ロール使用時は last_used_at と usage_count を更新
- 同一ユーザー・ロールの重複割り当ては不可
- 委譲元ユーザーが無効化された場合は委譲ロールも無効化
