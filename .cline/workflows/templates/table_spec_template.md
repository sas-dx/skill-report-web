# テーブル定義書：{{logical_name}} ({{table_id}})

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | {{table_id}} |
| **テーブル名** | {{table_name}} |
| **論理名** | {{logical_name}} |
| **カテゴリ** | {{category}} |
| **優先度** | {{priority}} |
| **ステータス** | 未着手 |
| **作成日** | {{current_date}} |
| **最終更新日** | {{current_date}} |

## 2. テーブル概要

### 2.1 概要・目的
{{description}}

### 2.2 関連API
{{#each related_apis}}
- [{{this}}](../api/specs/API定義書_{{this}}.md)
{{/each}}

### 2.3 関連バッチ
{{#each related_batches}}
- [{{this}}](../batch/specs/バッチ仕様書_{{this}}.md)
{{/each}}

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | BIGINT | - | × | ○ | - | AUTO_INCREMENT | 主キー |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナント識別子 |
| 3 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 4 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant_id | INDEX | tenant_id | テナント検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| fk_tenant_id | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| chk_status | CHECK | status | status IN ('active', 'inactive') |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナントマスタ |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | なし |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO {{table_name}} (
    tenant_id,
    created_at,
    updated_at
) VALUES (
    'tenant001',
    '2025-05-31 00:00:00',
    '2025-05-31 00:00:00'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 運用開始時 |
| 年間増加件数 | 10,000件 | 想定値 |
| 5年後想定件数 | 50,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から5年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id | テナント別検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新処理 |
| DELETE | 低 | id | 論理削除 |

### 7.2 パフォーマンス要件
- SELECT：100ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| admin | ○ | ○ | ○ | ○ | 管理者 |
| user | ○ | ○ | ○ | × | 一般ユーザー |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含まない
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：なし
- 移行方法：-
- 移行タイミング：-

### 9.2 DDL
```sql
CREATE TABLE {{table_name}} (
    id BIGINT AUTO_INCREMENT,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    INDEX idx_tenant_id (tenant_id),
    INDEX idx_created_at (created_at),
    CONSTRAINT fk_tenant_id FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | {{current_date}} | システムアーキテクト | 初版作成 |
