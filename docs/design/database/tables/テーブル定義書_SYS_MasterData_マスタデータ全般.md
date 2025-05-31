# テーブル定義書：マスタデータ全般 (SYS_MasterData)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-025 |
| **テーブル名** | SYS_MasterData |
| **論理名** | マスタデータ全般 |
| **カテゴリ** | システム系 |
| **優先度** | 中 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
マスタデータ全般テーブル（SYS_MasterData）は、システム全体で使用される汎用的なマスタデータを管理するシステムテーブルです。コードマスタ、区分マスタ、設定値マスタなど、専用テーブルを作成するほどではない小規模なマスタデータを統合的に管理します。階層構造やグループ化にも対応し、柔軟なマスタデータ管理を実現します。

### 2.2 関連API
- [API-023](../api/specs/API仕様書_API-023.md) - マスタデータ管理API

### 2.3 関連バッチ
- [BATCH-015](../batch/specs/バッチ定義書_BATCH-015.md) - マスタデータ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | data_id | データID | VARCHAR | 50 | × | ○ | - | - | マスタデータを一意に識別するID |
| 2 | data_type | データ種別 | VARCHAR | 50 | × | - | - | - | データの種別（CODE/CATEGORY/CONFIG等） |
| 3 | data_group | データグループ | VARCHAR | 100 | × | - | - | - | データのグループ名 |
| 4 | data_key | データキー | VARCHAR | 100 | × | - | - | - | データのキー |
| 5 | data_value | データ値 | TEXT | - | × | - | - | - | データの値 |
| 6 | display_name | 表示名 | VARCHAR | 200 | × | - | - | - | 表示用の名称 |
| 7 | display_name_en | 表示名（英語） | VARCHAR | 200 | ○ | - | - | NULL | 英語表示名 |
| 8 | description | 説明 | TEXT | - | ○ | - | - | NULL | データの説明 |
| 9 | parent_data_id | 親データID | VARCHAR | 50 | ○ | - | SYS_MasterData.data_id | NULL | 親データのID（階層構造の場合） |
| 10 | level | レベル | INTEGER | - | × | - | - | 1 | 階層レベル |
| 11 | display_order | 表示順序 | INTEGER | - | × | - | - | 0 | 表示時の順序 |
| 12 | value_type | データ型 | VARCHAR | 20 | × | - | - | 'STRING' | 値のデータ型 |
| 13 | is_required | 必須フラグ | BOOLEAN | - | × | - | - | FALSE | 必須データかどうか |
| 14 | is_system | システム予約フラグ | BOOLEAN | - | × | - | - | FALSE | システム予約データかどうか |
| 15 | is_editable | 編集可能フラグ | BOOLEAN | - | × | - | - | TRUE | 編集可能かどうか |
| 16 | is_deletable | 削除可能フラグ | BOOLEAN | - | × | - | - | TRUE | 削除可能かどうか |
| 17 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | データが有効かどうか |
| 18 | valid_from | 有効開始日 | DATE | - | ○ | - | - | NULL | 有効開始日 |
| 19 | valid_to | 有効終了日 | DATE | - | ○ | - | - | NULL | 有効終了日 |
| 20 | attribute1 | 属性1 | VARCHAR | 255 | ○ | - | - | NULL | 拡張属性1 |
| 21 | attribute2 | 属性2 | VARCHAR | 255 | ○ | - | - | NULL | 拡張属性2 |
| 22 | attribute3 | 属性3 | VARCHAR | 255 | ○ | - | - | NULL | 拡張属性3 |
| 23 | attribute4 | 属性4 | TEXT | - | ○ | - | - | NULL | 拡張属性4（長文） |
| 24 | attribute5 | 属性5 | TEXT | - | ○ | - | - | NULL | 拡張属性5（JSON等） |
| 25 | remarks | 備考 | TEXT | - | ○ | - | - | NULL | 備考・コメント |
| 26 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 27 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード更新日時 |
| 28 | created_by | 作成者ID | VARCHAR | 50 | × | - | MST_UserAuth.user_id | - | レコード作成者のユーザーID |
| 29 | updated_by | 更新者ID | VARCHAR | 50 | × | - | MST_UserAuth.user_id | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | data_id | 主キー |
| uk_group_key | UNIQUE | data_group, data_key | グループ内でのキー一意制約 |
| idx_data_type | INDEX | data_type | データ種別での検索用 |
| idx_data_group | INDEX | data_group | データグループでの検索用 |
| idx_parent_data_id | INDEX | parent_data_id | 親データでの検索用 |
| idx_is_active | INDEX | is_active | 有効フラグでの検索用 |
| idx_display_order | INDEX | display_order | 表示順序での並び替え用 |
| idx_valid_period | INDEX | valid_from, valid_to | 有効期間での検索用 |
| idx_composite | INDEX | data_type, data_group, is_active, display_order | 複合検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_master_data | PRIMARY KEY | data_id | 主キー制約 |
| uk_group_key | UNIQUE | data_group, data_key | グループ内キー一意制約 |
| fk_master_parent | FOREIGN KEY | parent_data_id | SYS_MasterData(data_id) |
| fk_master_created | FOREIGN KEY | created_by | MST_UserAuth(user_id) |
| fk_master_updated | FOREIGN KEY | updated_by | MST_UserAuth(user_id) |
| chk_data_type | CHECK | data_type | data_type IN ('CODE', 'CATEGORY', 'CONFIG', 'ENUM', 'LOOKUP') |
| chk_value_type | CHECK | value_type | value_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 'JSON') |
| chk_level | CHECK | level | level >= 1 |
| chk_display_order | CHECK | display_order | display_order >= 0 |
| chk_valid_period | CHECK | valid_from, valid_to | valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | 関係 | 説明 |
|------------|------------|------|------|
| SYS_MasterData | parent_data_id | N:1 | 親データ（自己参照） |
| MST_UserAuth | created_by | N:1 | 作成者 |
| MST_UserAuth | updated_by | N:1 | 更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | 関係 | 説明 |
|------------|------------|------|------|
| SYS_MasterData | parent_data_id | 1:N | 子データ（自己参照） |

## 5. データ仕様

### 5.1 データ種別定義
| 種別 | 説明 | 用途 | 例 |
|------|------|------|-----|
| CODE | コードマスタ | 固定値リスト | 優先度、ステータス |
| CATEGORY | カテゴリマスタ | 分類情報 | スキル分類、業界分類 |
| CONFIG | 設定値マスタ | システム設定 | 制限値、閾値 |
| ENUM | 列挙型マスタ | 選択肢 | 性別、血液型 |
| LOOKUP | 参照マスタ | 検索用 | 地域、職種 |

### 5.2 値データ型定義
| 型 | 説明 | 用途 | 例 |
|----|------|------|-----|
| STRING | 文字列 | 一般的な文字データ | 名称、説明 |
| INTEGER | 整数 | 数値データ | 順序、カウント |
| DECIMAL | 小数 | 金額、比率 | 料金、割合 |
| BOOLEAN | 真偽値 | フラグ | 有効/無効 |
| DATE | 日付 | 日付データ | 開始日、終了日 |
| JSON | JSON形式 | 構造化データ | 設定情報、属性 |

### 5.3 データ例
```sql
-- 優先度マスタ
INSERT INTO SYS_MasterData (
    data_id, data_type, data_group, data_key, data_value,
    display_name, display_order, value_type, is_system,
    created_by, updated_by
) VALUES 
('MD_PRI_001', 'CODE', 'PRIORITY', 'HIGH', '1', '高', 1, 'INTEGER', TRUE, 'SYSTEM', 'SYSTEM'),
('MD_PRI_002', 'CODE', 'PRIORITY', 'MEDIUM', '2', '中', 2, 'INTEGER', TRUE, 'SYSTEM', 'SYSTEM'),
('MD_PRI_003', 'CODE', 'PRIORITY', 'LOW', '3', '低', 3, 'INTEGER', TRUE, 'SYSTEM', 'SYSTEM');

-- スキル分類マスタ（階層構造）
INSERT INTO SYS_MasterData (
    data_id, data_type, data_group, data_key, data_value,
    display_name, level, display_order, created_by, updated_by
) VALUES 
('MD_SKL_001', 'CATEGORY', 'SKILL_TYPE', 'TECH', 'TECHNICAL', '技術系', 1, 1, 'SYSTEM', 'SYSTEM'),
('MD_SKL_002', 'CATEGORY', 'SKILL_TYPE', 'PROG', 'PROGRAMMING', 'プログラミング', 2, 1, 'SYSTEM', 'SYSTEM'),
('MD_SKL_003', 'CATEGORY', 'SKILL_TYPE', 'INFRA', 'INFRASTRUCTURE', 'インフラ', 2, 2, 'SYSTEM', 'SYSTEM');

-- 親子関係の設定
UPDATE SYS_MasterData SET parent_data_id = 'MD_SKL_001' WHERE data_id IN ('MD_SKL_002', 'MD_SKL_003');

-- システム設定マスタ
INSERT INTO SYS_MasterData (
    data_id, data_type, data_group, data_key, data_value,
    display_name, value_type, is_system, description,
    created_by, updated_by
) VALUES 
('MD_CFG_001', 'CONFIG', 'SYSTEM', 'MAX_LOGIN_ATTEMPTS', '5', 'ログイン試行回数上限', 'INTEGER', TRUE, 'ログイン失敗の上限回数', 'SYSTEM', 'SYSTEM'),
('MD_CFG_002', 'CONFIG', 'SYSTEM', 'SESSION_TIMEOUT', '3600', 'セッションタイムアウト（秒）', 'INTEGER', TRUE, 'セッションの有効期限', 'SYSTEM', 'SYSTEM');

-- 地域マスタ（検索用）
INSERT INTO SYS_MasterData (
    data_id, data_type, data_group, data_key, data_value,
    display_name, display_name_en, attribute1, attribute2,
    created_by, updated_by
) VALUES 
('MD_REG_001', 'LOOKUP', 'REGION', 'TOKYO', '東京都', '東京都', 'Tokyo', '関東', 'JP'),
('MD_REG_002', 'LOOKUP', 'REGION', 'OSAKA', '大阪府', '大阪府', 'Osaka', '関西', 'JP');
```

### 5.4 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 基本マスタデータ |
| 年間増加件数 | 100件 | 新規マスタ追加 |
| 最大想定件数 | 5,000件 | 5年後想定 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 データメンテナンス
- 無効データの定期確認：月次
- 重複データのチェック：週次
- 参照整合性の確認：日次

### 6.3 キャッシュ戦略
- 頻繁にアクセスされるマスタデータはアプリケーションレベルでキャッシュ
- キャッシュ更新：データ変更時に即座に更新
- キャッシュ有効期限：24時間

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 極高 | data_group, is_active | マスタデータ取得 |
| SELECT | 高 | data_type, data_group | 種別別取得 |
| SELECT | 中 | parent_data_id | 階層データ取得 |
| INSERT | 低 | - | 新規マスタ追加 |
| UPDATE | 低 | - | マスタデータ更新 |
| DELETE | 極低 | - | 論理削除のみ |

### 7.2 パフォーマンス要件
- SELECT（通常検索）：50ms以内
- SELECT（階層検索）：100ms以内
- INSERT/UPDATE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| master_admin | ○ | ○ | ○ | × | マスタ管理者 |
| application | ○ | × | × | × | アプリケーション |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む可能性（システム設定値）
- 暗号化：設定値の一部で必要
- 変更履歴：全変更を記録

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存マスタテーブル群
- 移行方法：データ変換・統合
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存優先度マスタからの移行
INSERT INTO SYS_MasterData (
    data_id, data_type, data_group, data_key, data_value,
    display_name, display_order, value_type, is_system,
    created_by, updated_by
)
SELECT 
    CONCAT('MD_PRI_', LPAD(priority_id, 3, '0')),
    'CODE',
    'PRIORITY',
    priority_code,
    CAST(priority_value AS CHAR),
    priority_name,
    sort_order,
    'INTEGER',
    TRUE,
    'MIGRATION',
    'MIGRATION'
FROM old_priority_master
WHERE is_active = 1;

-- 既存カテゴリマスタからの移行
INSERT INTO SYS_MasterData (
    data_id, data_type, data_group, data_key, data_value,
    display_name, parent_data_id, level, display_order,
    created_by, updated_by
)
SELECT 
    CONCAT('MD_CAT_', LPAD(category_id, 3, '0')),
    'CATEGORY',
    category_group,
    category_code,
    category_value,
    category_name,
    CASE WHEN parent_id IS NOT NULL THEN CONCAT('MD_CAT_', LPAD(parent_id, 3, '0')) END,
    category_level,
    sort_order,
    'MIGRATION',
    'MIGRATION'
FROM old_category_master
WHERE is_active = 1;
```

### 9.3 DDL
```sql
CREATE TABLE SYS_MasterData (
    data_id VARCHAR(50) NOT NULL,
    data_type VARCHAR(50) NOT NULL,
    data_group VARCHAR(100) NOT NULL,
    data_key VARCHAR(100) NOT NULL,
    data_value TEXT NOT NULL,
    display_name VARCHAR(200) NOT NULL,
    display_name_en VARCHAR(200) NULL,
    description TEXT NULL,
    parent_data_id VARCHAR(50) NULL,
    level INTEGER NOT NULL DEFAULT 1,
    display_order INTEGER NOT NULL DEFAULT 0,
    value_type VARCHAR(20) NOT NULL DEFAULT 'STRING',
    is_required BOOLEAN NOT NULL DEFAULT FALSE,
    is_system BOOLEAN NOT NULL DEFAULT FALSE,
    is_editable BOOLEAN NOT NULL DEFAULT TRUE,
    is_deletable BOOLEAN NOT NULL DEFAULT TRUE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    valid_from DATE NULL,
    valid_to DATE NULL,
    attribute1 VARCHAR(255) NULL,
    attribute2 VARCHAR(255) NULL,
    attribute3 VARCHAR(255) NULL,
    attribute4 TEXT NULL,
    attribute5 TEXT NULL,
    remarks TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (data_id),
    UNIQUE KEY uk_group_key (data_group, data_key),
    INDEX idx_data_type (data_type),
    INDEX idx_data_group (data_group),
    INDEX idx_parent_data_id (parent_data_id),
    INDEX idx_is_active (is_active),
    INDEX idx_display_order (display_order),
    INDEX idx_valid_period (valid_from, valid_to),
    INDEX idx_composite (data_type, data_group, is_active, display_order),
    CONSTRAINT fk_master_parent FOREIGN KEY (parent_data_id) REFERENCES SYS_MasterData(data_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_master_created FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_master_updated FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_data_type CHECK (data_type IN ('CODE', 'CATEGORY', 'CONFIG', 'ENUM', 'LOOKUP')),
    CONSTRAINT chk_value_type CHECK (value_type IN ('STRING', 'INTEGER', 'DECIMAL', 'BOOLEAN', 'DATE', 'JSON')),
    CONSTRAINT chk_level CHECK (level >= 1),
    CONSTRAINT chk_display_order CHECK (display_order >= 0),
    CONSTRAINT chk_valid_period CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. **汎用性重視**：様々な種類のマスタデータを統一的に管理
2. **階層構造対応**：親子関係による階層的なデータ構造
3. **多言語対応**：日本語・英語の表示名を管理
4. **拡張属性**：将来的な拡張に対応した属性フィールド
5. **有効期間管理**：時限的なマスタデータの管理
6. **システム保護**：重要なシステムデータの保護機能
7. **変更履歴**：作成者・更新者の記録による変更追跡
8. **柔軟な検索**：複数の検索条件に対応したインデックス設計
9. **キャッシュ対応**：高頻度アクセスに対応したキャッシュ戦略
10. **データ整合性**：外部キー制約による参照整合性の保証
11. **国際化対応**：多言語環境での利用を考慮
12. **運用効率**：管理画面での効率的なマスタデータ管理

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（汎用マスタデータ管理対応） |
