# テーブル定義書：SYS_TenantUsage（テナント使用量）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-030 |
| **テーブル名** | SYS_TenantUsage |
| **論理名** | テナント使用量 |
| **カテゴリ** | システム系 |
| **機能カテゴリ** | マルチテナント管理 |
| **優先度** | 高 |
| **個人情報含有** | なし |
| **機密情報レベル** | 中 |
| **暗号化要否** | 不要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
SYS_TenantUsage（テナント使用量）は、システム運用に必要な情報を管理するテーブルです。検索インデックス、ログ、設定情報などを格納します。

### 2.2 関連API
API-025

### 2.3 関連バッチ
BATCH-018-01

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | VARCHAR | 50 | × | ○ | - | - | 主キー |
| 2 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 3 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 4 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 5 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_created_at | INDEX | created_at | 作成日時検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_sys_tenantusage | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |

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
INSERT INTO SYS_TenantUsage (
    id, created_by, updated_by
) VALUES (
    'sample_001', 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 100件 | 初期設定データ |
| 月間増加件数 | 3000件 | 想定値 |
| 年間増加件数 | 36000件 | 想定値 |
| 5年後想定件数 | 181,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から2年経過
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
- SELECT：20ms以内
- INSERT：30ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

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
CREATE TABLE SYS_TenantUsage (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_created_at (created_at),
    INDEX idx_active (is_active),
    CONSTRAINT fk_sys_tenantusage_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_sys_tenantusage_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='テナント使用量';
```

## 10. 特記事項

1. **設計方針**
   - システム系として設計
   - マルチテナント対応
   - 監査証跡の保持

2. **運用上の注意点**
   - 定期的なデータクリーンアップが必要
   - パフォーマンス監視を実施
   - データ量見積もりの定期見直し

3. **今後の拡張予定**
   - 必要に応じて機能拡張を検討

4. **関連画面**
   - SCR-TENANT-ADMIN

5. **データ量・パフォーマンス監視**
   - データ量が想定の150%を超えた場合はアラート
   - 応答時間が設定値の120%を超えた場合は調査
