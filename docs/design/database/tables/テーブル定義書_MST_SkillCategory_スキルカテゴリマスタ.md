# テーブル定義書：スキルカテゴリマスタ (MST_SkillCategory)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-009 |
| **テーブル名** | MST_SkillCategory |
| **論理名** | スキルカテゴリマスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
スキルカテゴリマスタテーブル（MST_SkillCategory）は、スキル管理システムの中核となるスキルの分類体系を管理します。3階層構造（大分類/中分類/小分類）によりスキルを体系的に分類し、スキル評価とレポート集計の基盤となります。

### 2.2 関連API
- [API-007](../api/specs/API仕様書_API-007.md) - スキル管理API
- [API-008](../api/specs/API仕様書_API-008.md) - スキルカテゴリ管理API

### 2.3 関連バッチ
- [BATCH-008](../batch/specs/バッチ定義書_BATCH-008.md) - スキルマスタ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | category_id | カテゴリID | VARCHAR | 20 | × | ○ | - | - | スキルカテゴリを一意に識別するID |
| 2 | category_code | カテゴリコード | VARCHAR | 20 | × | - | - | - | スキルカテゴリのコード |
| 3 | category_name | カテゴリ名 | VARCHAR | 100 | × | - | - | - | スキルカテゴリの名称 |
| 4 | category_name_en | カテゴリ名（英語） | VARCHAR | 100 | ○ | - | - | NULL | カテゴリ名の英語表記 |
| 5 | parent_category_id | 親カテゴリID | VARCHAR | 20 | ○ | - | ○ | NULL | 上位カテゴリのID |
| 6 | category_level | カテゴリレベル | INTEGER | - | × | - | - | 1 | 階層レベル（1:大分類、2:中分類、3:小分類） |
| 7 | category_path | カテゴリパス | VARCHAR | 500 | × | - | - | - | 階層構造を表すパス（/大分類/中分類/小分類） |
| 8 | icon_url | アイコンURL | VARCHAR | 500 | ○ | - | - | NULL | カテゴリのアイコン画像URL |
| 9 | color_code | カラーコード | VARCHAR | 7 | ○ | - | - | NULL | カテゴリの表示色（#RRGGBB形式） |
| 10 | description | 説明 | TEXT | - | ○ | - | - | NULL | カテゴリの詳細説明 |
| 11 | evaluation_criteria | 評価基準 | TEXT | - | ○ | - | - | NULL | スキル評価の基準・指針 |
| 12 | required_evidence | 必要な証跡 | TEXT | - | ○ | - | - | NULL | スキル証明に必要な証跡・資料 |
| 13 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | 同階層内での表示順序 |
| 14 | is_system_category | システムカテゴリフラグ | BOOLEAN | - | × | - | - | FALSE | システム標準カテゴリかどうか |
| 15 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | テナント固有カテゴリの場合のテナントID |
| 16 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | カテゴリが有効かどうか |
| 17 | effective_date | 有効開始日 | DATE | - | × | - | - | - | カテゴリの有効開始日 |
| 18 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | カテゴリの有効終了日 |
| 19 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 20 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 21 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 22 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | category_id | 主キー |
| idx_category_code | UNIQUE | category_code | カテゴリコードの一意性を保証 |
| idx_parent | INDEX | parent_category_id | 親カテゴリ検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_level | INDEX | category_level | カテゴリレベル検索用 |
| idx_path | INDEX | category_path | カテゴリパス検索用 |
| idx_system | INDEX | is_system_category | システムカテゴリ検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_category | PRIMARY KEY | category_id | 主キー制約 |
| uq_category_code | UNIQUE | category_code | カテゴリコードの一意性を保証 |
| fk_parent_category | FOREIGN KEY | parent_category_id | MST_SkillCategory.category_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_category_level | CHECK | category_level | category_level >= 1 AND category_level <= 3 |
| chk_color_code | CHECK | color_code | color_code IS NULL OR color_code REGEXP '^#[0-9A-Fa-f]{6}$' |
| chk_expiry_date | CHECK | expiry_date | expiry_date IS NULL OR expiry_date >= effective_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_SkillCategory | parent_category_id | 1:N | 親カテゴリ（自己参照） |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_SkillItem | category_id | 1:N | スキル項目 |
| MST_SkillCategory | parent_category_id | 1:N | 子カテゴリ（自己参照） |

## 5. データ仕様

### 5.1 データ例
```sql
-- 大分類
INSERT INTO MST_SkillCategory (
    category_id, category_code, category_name,
    category_level, category_path, color_code,
    description, is_system_category, effective_date,
    created_by, updated_by
) VALUES (
    'CAT_001',
    'TECH',
    '技術スキル',
    1,
    '/技術スキル',
    '#2196F3',
    'プログラミング、インフラ、データベース等の技術的なスキル',
    TRUE,
    '2023-04-01',
    'system',
    'system'
);

-- 中分類
INSERT INTO MST_SkillCategory (
    category_id, category_code, category_name,
    parent_category_id, category_level, category_path,
    color_code, description, is_system_category,
    effective_date, created_by, updated_by
) VALUES (
    'CAT_002',
    'PROG',
    'プログラミング',
    'CAT_001',
    2,
    '/技術スキル/プログラミング',
    '#4CAF50',
    'プログラミング言語・フレームワークに関するスキル',
    TRUE,
    '2023-04-01',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 200件 | システム標準カテゴリ |
| 年間増加件数 | 50件 | カスタムカテゴリ追加 |
| 5年後想定件数 | 450件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：廃止から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | is_active, category_level | 有効カテゴリ階層取得 |
| SELECT | 高 | parent_category_id | 子カテゴリ一覧取得 |
| SELECT | 中 | category_path | パス検索 |
| SELECT | 中 | tenant_id | テナント固有カテゴリ取得 |
| UPDATE | 低 | category_id | カテゴリ情報更新 |
| INSERT | 低 | - | 新規カテゴリ作成 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：50ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| skill_admin | ○ | ○ | ○ | × | スキル管理者 |
| manager | ○ | ○ | ○ | × | 管理職（テナント内のみ） |
| employee | ○ | × | × | × | 一般社員 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（スキル体系）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存スキル管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_SkillCategory (
    category_id VARCHAR(20) NOT NULL,
    category_code VARCHAR(20) NOT NULL,
    category_name VARCHAR(100) NOT NULL,
    category_name_en VARCHAR(100) NULL,
    parent_category_id VARCHAR(20) NULL,
    category_level INTEGER NOT NULL DEFAULT 1,
    category_path VARCHAR(500) NOT NULL,
    icon_url VARCHAR(500) NULL,
    color_code VARCHAR(7) NULL,
    description TEXT NULL,
    evaluation_criteria TEXT NULL,
    required_evidence TEXT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_system_category BOOLEAN NOT NULL DEFAULT FALSE,
    tenant_id VARCHAR(50) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    effective_date DATE NOT NULL,
    expiry_date DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (category_id),
    UNIQUE KEY idx_category_code (category_code),
    INDEX idx_parent (parent_category_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_level (category_level),
    INDEX idx_path (category_path),
    INDEX idx_system (is_system_category),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    CONSTRAINT fk_skill_category_parent FOREIGN KEY (parent_category_id) REFERENCES MST_SkillCategory(category_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_category_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_category_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_category_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_category_level CHECK (category_level >= 1 AND category_level <= 3),
    CONSTRAINT chk_skill_category_color_code CHECK (color_code IS NULL OR color_code REGEXP '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT chk_skill_category_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. 3階層構造（大分類/中分類/小分類）によるスキル分類体系
2. システム標準カテゴリとテナント固有カテゴリの混在管理
3. カテゴリパスにより階層構造の可視化が可能
4. アイコンとカラーコードによる視覚的な分類表現
5. 評価基準と必要証跡により統一的なスキル評価を支援
6. カテゴリ廃止時は論理削除（is_active=FALSE）を使用
7. 有効期間によりカテゴリ変更履歴を管理
8. 同階層内での表示順序はsort_orderで制御
9. システム標準カテゴリは削除不可

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
