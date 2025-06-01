# テーブル定義書：MST_Position（役職マスタ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-008 |
| **テーブル名** | MST_Position |
| **論理名** | 役職マスタ |
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
MST_Position（役職マスタ）は、組織内の役職・職位の階層構造と基本情報を管理するマスタテーブルです。

主な目的：
- 役職階層の構造管理（社長、部長、課長、主任等の階層関係）
- 役職基本情報の管理（役職名、役職コード、権限レベル等）
- 人事評価・昇進管理の基盤
- 給与・手当計算の基礎データ
- 権限・アクセス制御の役職単位設定
- 組織図・名刺作成の基礎データ
- 人事制度・キャリアパス管理

このテーブルは、人事管理、権限管理、給与計算、組織運営など、
企業の階層的組織運営の基盤となる重要なマスタデータです。


### 2.2 特記事項
- 役職レベルは階層の深さを表す（1が最上位）
- 同レベル内の序列は役職ランクで管理
- 権限レベルはシステムアクセス制御に使用
- 承認限度額は稟議・決裁システムと連携
- 管理職フラグは労働基準法上の管理監督者判定に使用
- 給与等級は給与計算システムと連携

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
| 8 | position_code | 役職コード | VARCHAR | 20 | ○ | - | - | - | 役職を一意に識別するコード（例：POS001） |
| 9 | position_name | 役職名 | VARCHAR | 100 | ○ | - | - | - | 役職の正式名称 |
| 10 | position_name_short | 役職名略称 | VARCHAR | 50 | ○ | - | - | - | 役職の略称・短縮名 |
| 11 | position_level | 役職レベル | INT | None | ○ | - | - | - | 役職の階層レベル（1:最上位、数値が大きいほど下位） |
| 12 | position_rank | 役職ランク | INT | None | ○ | - | - | - | 同レベル内での序列・ランク |
| 13 | position_category | 役職カテゴリ | ENUM | None | ○ | - | - | - | 役職のカテゴリ（EXECUTIVE:役員、MANAGER:管理職、SUPERVISOR:監督職、STAFF:一般職） |
| 14 | authority_level | 権限レベル | INT | None | ○ | - | - | - | システム権限レベル（1-10、数値が大きいほど高権限） |
| 15 | approval_limit | 承認限度額 | DECIMAL | 15,2 | ○ | - | - | - | 承認可能な金額の上限（円） |
| 16 | salary_grade | 給与等級 | VARCHAR | 10 | ○ | - | - | - | 給与計算用の等級コード |
| 17 | allowance_amount | 役職手当額 | DECIMAL | 10,2 | ○ | - | - | - | 月額役職手当（円） |
| 18 | is_management | 管理職フラグ | BOOLEAN | None | ○ | - | - | False | 管理職かどうか（労働基準法上の管理監督者判定） |
| 19 | is_executive | 役員フラグ | BOOLEAN | None | ○ | - | - | False | 役員かどうか |
| 20 | requires_approval | 承認権限フラグ | BOOLEAN | None | ○ | - | - | False | 承認権限を持つかどうか |
| 21 | can_hire | 採用権限フラグ | BOOLEAN | None | ○ | - | - | False | 採用権限を持つかどうか |
| 22 | can_evaluate | 評価権限フラグ | BOOLEAN | None | ○ | - | - | False | 人事評価権限を持つかどうか |
| 23 | position_status | 役職状態 | ENUM | None | ○ | - | - | ACTIVE | 役職の状態（ACTIVE:有効、INACTIVE:無効、ABOLISHED:廃止） |
| 24 | sort_order | 表示順序 | INT | None | ○ | - | - | - | 組織図等での表示順序 |
| 25 | description | 役職説明 | TEXT | None | ○ | - | - | - | 役職の責任・権限・業務内容の説明 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_position_code | UNIQUE INDEX | position_code | 役職コード検索用（一意） |
| idx_position_level | INDEX | position_level | 役職レベル別検索用 |
| idx_position_rank | INDEX | position_rank | 役職ランク別検索用 |
| idx_position_category | INDEX | position_category | 役職カテゴリ別検索用 |
| idx_authority_level | INDEX | authority_level | 権限レベル別検索用 |
| idx_salary_grade | INDEX | salary_grade | 給与等級別検索用 |
| idx_status | INDEX | position_status | 役職状態別検索用 |
| idx_management_flags | INDEX | is_management, is_executive | 管理職・役員フラグ検索用 |
| idx_sort_order | INDEX | sort_order | 表示順序検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_position | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_position_code | UNIQUE | position_code | ['position_code'] |
| chk_position_level | CHECK |  | position_level > 0 |
| chk_position_rank | CHECK |  | position_rank > 0 |
| chk_authority_level | CHECK |  | authority_level BETWEEN 1 AND 10 |
| chk_position_category | CHECK |  | position_category IN ('EXECUTIVE', 'MANAGER', 'SUPERVISOR', 'STAFF') |
| chk_position_status | CHECK |  | position_status IN ('ACTIVE', 'INACTIVE', 'ABOLISHED') |
| chk_approval_limit | CHECK |  | approval_limit IS NULL OR approval_limit >= 0 |
| chk_allowance_amount | CHECK |  | allowance_amount IS NULL OR allowance_amount >= 0 |
| chk_sort_order | CHECK |  | sort_order IS NULL OR sort_order >= 0 |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_Position (
    id, tenant_id, position_code, position_name, position_name_short, position_level, position_rank, position_category, authority_level, approval_limit, salary_grade, allowance_amount, is_management, is_executive, requires_approval, can_hire, can_evaluate, position_status, sort_order, description, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'POS001', '代表取締役社長', '社長', '1', '1', 'EXECUTIVE', '10', '999999999.99', 'E1', '500000.0', 'True', 'True', 'True', 'True', 'True', 'ACTIVE', '1', '会社の最高責任者として経営全般を統括', 'user_admin', 'user_admin'
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
-- 役職マスタテーブル作成DDL
CREATE TABLE MST_Position (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    position_code VARCHAR(20) COMMENT '役職コード',
    position_name VARCHAR(100) COMMENT '役職名',
    position_name_short VARCHAR(50) COMMENT '役職名略称',
    position_level INT COMMENT '役職レベル',
    position_rank INT COMMENT '役職ランク',
    position_category ENUM COMMENT '役職カテゴリ',
    authority_level INT COMMENT '権限レベル',
    approval_limit DECIMAL(15,2) COMMENT '承認限度額',
    salary_grade VARCHAR(10) COMMENT '給与等級',
    allowance_amount DECIMAL(10,2) COMMENT '役職手当額',
    is_management BOOLEAN DEFAULT False COMMENT '管理職フラグ',
    is_executive BOOLEAN DEFAULT False COMMENT '役員フラグ',
    requires_approval BOOLEAN DEFAULT False COMMENT '承認権限フラグ',
    can_hire BOOLEAN DEFAULT False COMMENT '採用権限フラグ',
    can_evaluate BOOLEAN DEFAULT False COMMENT '評価権限フラグ',
    position_status ENUM DEFAULT ACTIVE COMMENT '役職状態',
    sort_order INT COMMENT '表示順序',
    description TEXT COMMENT '役職説明',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_position_code (position_code),
    INDEX idx_position_level (position_level),
    INDEX idx_position_rank (position_rank),
    INDEX idx_position_category (position_category),
    INDEX idx_authority_level (authority_level),
    INDEX idx_salary_grade (salary_grade),
    INDEX idx_status (position_status),
    INDEX idx_management_flags (is_management, is_executive),
    INDEX idx_sort_order (sort_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='役職マスタ';

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

- 役職コードは新設時に自動採番（POS + 3桁連番）
- 役員は必ず管理職フラグがtrueである必要がある
- 承認権限を持つ役職は承認限度額の設定が必要
- 廃止時は position_status を ABOLISHED に変更
- 役職レベルと権限レベルは原則として対応関係にある
- 管理職は評価権限を持つことを原則とする
- 役職手当は月額で設定し、給与計算時に使用
