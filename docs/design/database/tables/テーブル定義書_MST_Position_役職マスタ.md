# テーブル定義書：MST_Position（役職マスタ）

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
役職マスタテーブル（MST_Position）は、組織の役職情報を管理します。階層構造により役職の上下関係を表現し、人事システムとの連携により役職変更に対応します。社員の役職管理とレポート集計、権限管理の基盤となります。

### 2.2 関連要求仕様ID
- **ORG.1-POS.1**: 役職管理機能
- **ORG.2-HIER.1**: 組織階層管理
- **ACC.3-ROLE.1**: 役職ベース権限管理

### 2.3 関連API
- [API-006](../api/specs/API仕様書_API-006_組織情報管理API.md) - 組織情報管理API

### 2.4 関連バッチ
- [BATCH-004](../batch/specs/バッチ定義書_BATCH-004_パフォーマンス監視バッチ.md) - 社員情報同期バッチ
- [BATCH-701](../batch/specs/バッチ定義書_BATCH-701_組織・役職マスタ同期バッチ.md) - 組織・役職マスタ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | position_id | 役職ID | VARCHAR | 20 | × | ○ | - | - | 役職を一意に識別するID |
| 2 | position_code | 役職コード | VARCHAR | 10 | × | - | - | - | 人事システムの役職コード |
| 3 | position_name | 役職名 | VARCHAR | 100 | × | - | - | - | 役職の正式名称 |
| 4 | position_name_short | 役職名（略称） | VARCHAR | 50 | ○ | - | - | NULL | 役職の略称 |
| 5 | position_name_en | 役職名（英語） | VARCHAR | 100 | ○ | - | - | NULL | 役職名の英語表記 |
| 6 | parent_position_id | 上位役職ID | VARCHAR | 20 | ○ | - | ○ | NULL | 上位役職のID |
| 7 | position_level | 役職レベル | INTEGER | - | × | - | - | 1 | 役職階層のレベル（1:役員、2:部長、3:課長等） |
| 8 | position_rank | 役職ランク | INTEGER | - | × | - | - | 1 | 同レベル内での序列 |
| 9 | position_category | 役職カテゴリ | VARCHAR | 20 | × | - | - | 'GENERAL' | 役職の分類（EXECUTIVE/MANAGER/GENERAL） |
| 10 | management_flag | 管理職フラグ | BOOLEAN | - | × | - | - | FALSE | 管理職かどうか |
| 11 | approval_authority | 承認権限レベル | INTEGER | - | × | - | - | 0 | 承認可能な金額レベル |
| 12 | salary_grade | 給与グレード | VARCHAR | 10 | ○ | - | - | NULL | 給与体系のグレード |
| 13 | description | 説明 | TEXT | - | ○ | - | - | NULL | 役職の職務内容・説明 |
| 14 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | 同レベル内での表示順序 |
| 15 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 16 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 役職が有効かどうか |
| 17 | effective_date | 有効開始日 | DATE | - | × | - | - | - | 役職の有効開始日 |
| 18 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | 役職の有効終了日 |
| 19 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 20 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 21 | created_by | 作成者ID | VARCHAR | 50 | × | - | - | - | レコード作成者のユーザーID |
| 22 | updated_by | 更新者ID | VARCHAR | 50 | × | - | - | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | position_id | 主キー |
| idx_position_code | UNIQUE | position_code, tenant_id | 役職コードの一意性を保証（テナント内） |
| idx_parent | INDEX | parent_position_id | 上位役職検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_level | INDEX | position_level | 役職レベル検索用 |
| idx_category | INDEX | position_category | 役職カテゴリ検索用 |
| idx_management | INDEX | management_flag | 管理職フラグ検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_position | PRIMARY KEY | position_id | 主キー制約 |
| uq_position_code | UNIQUE | position_code, tenant_id | 役職コードの一意性を保証（テナント内） |
| fk_parent_position | FOREIGN KEY | parent_position_id | MST_Position.position_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | tenant_id, created_by | MST_UserAuth(tenant_id, user_id) |
| fk_updated_by | FOREIGN KEY | tenant_id, updated_by | MST_UserAuth(tenant_id, user_id) |
| chk_position_level | CHECK | position_level | position_level >= 1 AND position_level <= 10 |
| chk_position_rank | CHECK | position_rank | position_rank >= 1 |
| chk_position_category | CHECK | position_category | position_category IN ('EXECUTIVE', 'MANAGER', 'GENERAL') |
| chk_approval_authority | CHECK | approval_authority | approval_authority >= 0 |
| chk_expiry_date | CHECK | expiry_date | expiry_date IS NULL OR expiry_date >= effective_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Position | parent_position_id | 1:N | 上位役職（自己参照） |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | tenant_id, created_by / tenant_id, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | position_id | 1:N | 役職を持つ社員 |
| MST_Position | parent_position_id | 1:N | 下位役職（自己参照） |
| MST_EmployeePosition | position_id | 1:N | 社員役職関連 |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_Position (
    position_id, position_code, position_name,
    position_name_short, parent_position_id, position_level,
    position_rank, position_category, management_flag,
    approval_authority, salary_grade, effective_date,
    tenant_id, created_by, updated_by
) VALUES (
    'POS_001',
    'CEO',
    '代表取締役社長',
    '社長',
    NULL,
    1,
    1,
    'EXECUTIVE',
    TRUE,
    10,
    'E1',
    '2023-04-01',
    'tenant001',
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

### 5.3 データ保持期間
| データ種別 | 保持期間 | 備考 |
|------------|----------|------|
| 現行役職 | 無期限 | 業務継続中は保持 |
| 廃止役職 | 10年 | 人事記録保持要件 |

## 6. 運用仕様

### 6.1 バックアップ
- **日次バックアップ**: 毎日2:00実行
- **週次バックアップ**: 毎週日曜日3:00実行
- **月次バックアップ**: 毎月1日4:00実行

### 6.2 パーティション
- **パーティション種別**: なし
- **パーティション条件**: -

### 6.3 アーカイブ
- **アーカイブ条件**: 廃止から10年経過
- **アーカイブ先**: アーカイブDB
- **アーカイブ方法**: 年次バッチで実行

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id, is_active | 有効役職一覧取得 |
| SELECT | 高 | parent_position_id | 下位役職一覧取得 |
| SELECT | 中 | position_level | レベル別役職取得 |
| SELECT | 中 | position_category | カテゴリ別役職取得 |
| UPDATE | 低 | position_id | 役職情報更新 |
| INSERT | 低 | - | 新規役職作成 |

### 7.2 パフォーマンス要件
- **SELECT**: 10ms以内
- **INSERT**: 50ms以内
- **UPDATE**: 50ms以内
- **DELETE**: 50ms以内

### 7.3 同時接続数
- **想定同時接続数**: 50ユーザー
- **最大同時接続数**: 200ユーザー

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
- **個人情報**: 含まない
- **機密情報**: 含む（組織構造、給与グレード）
- **暗号化**: 不要
- **マスキング**: 本番環境以外では給与グレードをマスキング

### 8.3 監査要件
- **操作ログ**: 全ての更新操作を記録
- **アクセスログ**: 参照操作を記録
- **保持期間**: 90日間

## 9. 移行仕様

### 9.1 データ移行
- **移行元**: 人事システム
- **移行方法**: CSVインポート
- **移行タイミング**: システム移行時
- **移行検証**: 階層構造の整合性チェック

### 9.2 DDL
```sql
CREATE TABLE MST_Position (
    position_id VARCHAR(20) NOT NULL,
    position_code VARCHAR(10) NOT NULL,
    position_name VARCHAR(100) NOT NULL,
    position_name_short VARCHAR(50) NULL,
    position_name_en VARCHAR(100) NULL,
    parent_position_id VARCHAR(20) NULL,
    position_level INTEGER NOT NULL DEFAULT 1,
    position_rank INTEGER NOT NULL DEFAULT 1,
    position_category VARCHAR(20) NOT NULL DEFAULT 'GENERAL',
    management_flag BOOLEAN NOT NULL DEFAULT FALSE,
    approval_authority INTEGER NOT NULL DEFAULT 0,
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
    INDEX idx_category (position_category),
    INDEX idx_management (management_flag),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    CONSTRAINT fk_position_parent FOREIGN KEY (parent_position_id) REFERENCES MST_Position(position_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_position_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_position_created_by FOREIGN KEY (tenant_id, created_by) REFERENCES MST_UserAuth(tenant_id, user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_position_updated_by FOREIGN KEY (tenant_id, updated_by) REFERENCES MST_UserAuth(tenant_id, user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_position_level CHECK (position_level >= 1 AND position_level <= 10),
    CONSTRAINT chk_position_rank CHECK (position_rank >= 1),
    CONSTRAINT chk_position_category CHECK (position_category IN ('EXECUTIVE', 'MANAGER', 'GENERAL')),
    CONSTRAINT chk_approval_authority CHECK (approval_authority >= 0),
    CONSTRAINT chk_position_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

### 10.1 設計要件
1. 階層構造により役職の上下関係を表現
2. 役職レベルと役職ランクにより詳細な序列管理が可能
3. 有効期間により役職変更履歴を管理
4. 役職廃止時は論理削除（is_active=FALSE）を使用
5. 人事システムとの定期同期により最新役職情報を維持

### 10.2 運用要件
1. 管理職フラグにより管理職の識別が可能
2. 承認権限レベルにより決裁権限の管理が可能
3. 給与グレードにより給与体系との連携が可能
4. 同レベル内での表示順序はsort_orderで制御
5. テナント間でのデータ漏洩防止のため、必ずtenant_idを条件に含める

### 10.3 障害対応
1. 階層構造の循環参照チェック機能を実装
2. 役職削除時の影響範囲確認機能を提供
3. 人事システム連携障害時のフォールバック処理を実装

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、マルチテナント対応追加 |
