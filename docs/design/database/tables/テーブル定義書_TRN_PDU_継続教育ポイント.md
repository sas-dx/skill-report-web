# テーブル定義書：TRN_PDU（継続教育ポイント）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-018 |
| **テーブル名** | TRN_PDU |
| **論理名** | 継続教育ポイント |
| **カテゴリ** | トランザクション系 |
| **優先度** | 中 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
TRN_PDU（継続教育ポイント）は、継続教育ポイントに関する情報を管理するテーブルです。

### 2.2 関連API
- [API-017](../../api/specs/) - 関連API

### 2.3 関連バッチ
- [BATCH-011](../../batch/specs/) - 関連バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | VARCHAR | 50 | × | ○ | - | - | 主キー |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | name | 名称 | VARCHAR | 255 | × | - | - | - | 名称 |
| 4 | description | 説明 | TEXT | - | ○ | - | - | NULL | 説明 |
| 5 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 有効フラグ |
| 6 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | 作成日時 |
| 7 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新日時 |
| 8 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | 作成者ID |
| 9 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | 更新者ID |
| 10 | column_10 | カラム10 | VARCHAR | 100 | ○ | - | - | NULL | カラム10の説明 |
| 11 | column_11 | カラム11 | VARCHAR | 100 | ○ | - | - | NULL | カラム11の説明 |
| 12 | column_12 | カラム12 | VARCHAR | 100 | ○ | - | - | NULL | カラム12の説明 |
| 13 | column_13 | カラム13 | VARCHAR | 100 | ○ | - | - | NULL | カラム13の説明 |
| 14 | column_14 | カラム14 | VARCHAR | 100 | ○ | - | - | NULL | カラム14の説明 |
| 15 | column_15 | カラム15 | VARCHAR | 100 | ○ | - | - | NULL | カラム15の説明 |
| 16 | column_16 | カラム16 | VARCHAR | 100 | ○ | - | - | NULL | カラム16の説明 |
| 17 | column_17 | カラム17 | VARCHAR | 100 | ○ | - | - | NULL | カラム17の説明 |
| 18 | column_18 | カラム18 | VARCHAR | 100 | ○ | - | - | NULL | カラム18の説明 |
| 19 | column_19 | カラム19 | VARCHAR | 100 | ○ | - | - | NULL | カラム19の説明 |
| 20 | column_20 | カラム20 | VARCHAR | 100 | ○ | - | - | NULL | カラム20の説明 |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_name | INDEX | name | 名称検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_trn_pdu | PRIMARY KEY | id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | - |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO TRN_PDU (
    id, tenant_id, name, description, is_active,
    created_by, updated_by
) VALUES (
    'sample_001', 'TENANT_001', 'サンプル', 'サンプルデータ', TRUE,
    'system', 'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 10件 | 初期データ |
| 月間増加件数 | 50件 | 想定値 |
| 年間増加件数 | 600件 | 想定値 |
| 5年後想定件数 | 3,010件 | 想定値 |

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
| SELECT | 高 | id, tenant_id | 基本検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新 |
| DELETE | 低 | id | 削除 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者 |
| user | ○ | × | × | × | 一般ユーザー |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含まない
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE TRN_PDU (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    name VARCHAR(255) NOT NULL COMMENT '名称',
    description TEXT NULL COMMENT '説明',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_name (name),
    INDEX idx_active (is_active),
    CONSTRAINT fk_trn_pdu_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_trn_pdu_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_trn_pdu_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='継続教育ポイント';
```

## 10. 特記事項

1. **データ整合性**
   - 外部キー制約により関連テーブルとの整合性を保証

2. **パフォーマンス**
   - 適切なインデックスによる高速検索を実現

3. **セキュリティ**
   - ロールベースアクセス制御による適切な権限管理

4. **運用性**
   - 定期バックアップとアーカイブによるデータ保護

5. **拡張性**
   - 将来の機能拡張に対応可能な設計

