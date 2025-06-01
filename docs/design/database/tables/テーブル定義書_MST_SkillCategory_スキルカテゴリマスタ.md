# テーブル定義書：MST_SkillCategory（スキルカテゴリマスタ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-034 |
| **テーブル名** | MST_SkillCategory |
| **論理名** | スキルカテゴリマスタ |
| **カテゴリ** | マスタ系 |
| **機能カテゴリ** | スキル管理 |
| **優先度** | 高 |
| **個人情報含有** | なし |
| **機密情報レベル** | 低 |
| **暗号化要否** | 不要 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
MST_SkillCategory（スキルカテゴリマスタ）は、スキルの分類・カテゴリを管理するマスタテーブルです。

主な目的：
- スキルの体系的分類・階層管理
- スキル検索・絞り込みの基盤
- スキルマップ・スキル評価の構造化
- 業界標準・企業独自のスキル分類対応
- スキル統計・分析の軸設定
- キャリアパス・研修計画の基盤
- スキル可視化・レポート生成の支援

このテーブルは、スキル管理システムの基盤となり、
効率的なスキル管理と戦略的人材育成を支援します。


### 2.2 特記事項
- カテゴリ階層は自己参照外部キーで表現
- システムカテゴリは削除・変更不可
- カテゴリパスで階層構造を可視化
- 評価方法はカテゴリ単位で設定可能
- アイコン・カラーコードで視覚的識別
- 人気カテゴリフラグで注目度管理

### 2.3 関連API
API-030

### 2.4 関連バッチ
BATCH-020

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
| 8 | category_code | カテゴリコード | VARCHAR | 20 | ○ | - | - | - | スキルカテゴリを一意に識別するコード（例：CAT001） |
| 9 | category_name | カテゴリ名 | VARCHAR | 100 | ○ | - | - | - | スキルカテゴリの正式名称 |
| 10 | category_name_short | カテゴリ名略称 | VARCHAR | 50 | ○ | - | - | - | スキルカテゴリの略称・短縮名 |
| 11 | category_name_en | カテゴリ名英語 | VARCHAR | 100 | ○ | - | - | - | スキルカテゴリの英語名称 |
| 12 | category_type | カテゴリ種別 | ENUM | None | ○ | - | - | - | カテゴリの種別（TECHNICAL:技術、BUSINESS:ビジネス、SOFT:ソフト、CERTIFICATION:資格、LANGUAGE:言語） |
| 13 | parent_category_id | 親カテゴリID | VARCHAR | 50 | ○ | - | ○ | - | 上位カテゴリのID（MST_SkillCategoryへの自己参照外部キー） |
| 14 | category_level | カテゴリレベル | INT | None | ○ | - | - | 1 | カテゴリの階層レベル（1:最上位、数値が大きいほど下位） |
| 15 | category_path | カテゴリパス | VARCHAR | 500 | ○ | - | - | - | ルートからのカテゴリパス（例：/技術/プログラミング/Java） |
| 16 | is_system_category | システムカテゴリフラグ | BOOLEAN | None | ○ | - | - | False | システム標準カテゴリかどうか（削除・変更不可） |
| 17 | is_leaf_category | 末端カテゴリフラグ | BOOLEAN | None | ○ | - | - | True | 末端カテゴリ（子カテゴリを持たない）かどうか |
| 18 | skill_count | スキル数 | INT | None | ○ | - | - | 0 | このカテゴリに属するスキル数 |
| 19 | evaluation_method | 評価方法 | ENUM | None | ○ | - | - | - | このカテゴリのスキル評価方法（LEVEL:レベル、SCORE:スコア、BINARY:有無、CERTIFICATION:資格） |
| 20 | max_level | 最大レベル | INT | None | ○ | - | - | - | レベル評価時の最大レベル数 |
| 21 | icon_url | アイコンURL | VARCHAR | 255 | ○ | - | - | - | カテゴリ表示用アイコンのURL |
| 22 | color_code | カラーコード | VARCHAR | 7 | ○ | - | - | - | カテゴリ表示用カラーコード（#RRGGBB形式） |
| 23 | display_order | 表示順序 | INT | None | ○ | - | - | 999 | 同階層内での表示順序 |
| 24 | is_popular | 人気カテゴリフラグ | BOOLEAN | None | ○ | - | - | False | 人気・注目カテゴリかどうか |
| 25 | category_status | カテゴリ状態 | ENUM | None | ○ | - | - | ACTIVE | カテゴリの状態（ACTIVE:有効、INACTIVE:無効、DEPRECATED:非推奨） |
| 26 | effective_from | 有効開始日 | DATE | None | ○ | - | - | - | カテゴリの有効開始日 |
| 27 | effective_to | 有効終了日 | DATE | None | ○ | - | - | - | カテゴリの有効終了日 |
| 28 | description | カテゴリ説明 | TEXT | None | ○ | - | - | - | カテゴリの詳細説明・用途 |


### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_category_code | UNIQUE INDEX | category_code | カテゴリコード検索用（一意） |
| idx_category_type | INDEX | category_type | カテゴリ種別検索用 |
| idx_parent_category | INDEX | parent_category_id | 親カテゴリ別検索用 |
| idx_category_level | INDEX | category_level | カテゴリレベル別検索用 |
| idx_category_path | INDEX | category_path | カテゴリパス検索用 |
| idx_system_category | INDEX | is_system_category | システムカテゴリ検索用 |
| idx_leaf_category | INDEX | is_leaf_category | 末端カテゴリ検索用 |
| idx_category_status | INDEX | category_status | カテゴリ状態別検索用 |
| idx_display_order | INDEX | parent_category_id, display_order | 表示順序検索用 |
| idx_popular_category | INDEX | is_popular | 人気カテゴリ検索用 |


### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_mst_skillcategory | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| uk_category_code | UNIQUE | category_code | ['category_code'] |
| chk_category_type | CHECK |  | category_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'LANGUAGE') |
| chk_category_status | CHECK |  | category_status IN ('ACTIVE', 'INACTIVE', 'DEPRECATED') |
| chk_evaluation_method | CHECK |  | evaluation_method IS NULL OR evaluation_method IN ('LEVEL', 'SCORE', 'BINARY', 'CERTIFICATION') |
| chk_category_level | CHECK |  | category_level > 0 |
| chk_max_level | CHECK |  | max_level IS NULL OR max_level > 0 |
| chk_skill_count | CHECK |  | skill_count >= 0 |
| chk_display_order | CHECK |  | display_order >= 0 |
| chk_effective_period | CHECK |  | effective_to IS NULL OR effective_from IS NULL OR effective_from <= effective_to |


## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
| MST_SkillCategory | parent_category_id | 1:N | 親カテゴリへの自己参照外部キー |


### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO MST_SkillCategory (
    id, tenant_id, category_code, category_name, category_name_short, category_name_en, category_type, parent_category_id, category_level, category_path, is_system_category, is_leaf_category, skill_count, evaluation_method, max_level, icon_url, color_code, display_order, is_popular, category_status, effective_from, effective_to, description, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'CAT001', 'プログラミング言語', 'プログラミング', 'Programming Languages', 'TECHNICAL', NULL, '1', '/プログラミング言語', 'True', 'False', '25', 'LEVEL', '5', '/icons/programming.svg', '#007ACC', '1', 'True', 'ACTIVE', '2025-01-01', NULL, '各種プログラミング言語のスキル', 'user_admin', 'user_admin'
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
-- スキルカテゴリマスタテーブル作成DDL
CREATE TABLE MST_SkillCategory (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    category_code VARCHAR(20) COMMENT 'カテゴリコード',
    category_name VARCHAR(100) COMMENT 'カテゴリ名',
    category_name_short VARCHAR(50) COMMENT 'カテゴリ名略称',
    category_name_en VARCHAR(100) COMMENT 'カテゴリ名英語',
    category_type ENUM COMMENT 'カテゴリ種別',
    parent_category_id VARCHAR(50) COMMENT '親カテゴリID',
    category_level INT DEFAULT 1 COMMENT 'カテゴリレベル',
    category_path VARCHAR(500) COMMENT 'カテゴリパス',
    is_system_category BOOLEAN DEFAULT False COMMENT 'システムカテゴリフラグ',
    is_leaf_category BOOLEAN DEFAULT True COMMENT '末端カテゴリフラグ',
    skill_count INT DEFAULT 0 COMMENT 'スキル数',
    evaluation_method ENUM COMMENT '評価方法',
    max_level INT COMMENT '最大レベル',
    icon_url VARCHAR(255) COMMENT 'アイコンURL',
    color_code VARCHAR(7) COMMENT 'カラーコード',
    display_order INT DEFAULT 999 COMMENT '表示順序',
    is_popular BOOLEAN DEFAULT False COMMENT '人気カテゴリフラグ',
    category_status ENUM DEFAULT ACTIVE COMMENT 'カテゴリ状態',
    effective_from DATE COMMENT '有効開始日',
    effective_to DATE COMMENT '有効終了日',
    description TEXT COMMENT 'カテゴリ説明',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_created_at (created_at),
    UNIQUE INDEX idx_category_code (category_code),
    INDEX idx_category_type (category_type),
    INDEX idx_parent_category (parent_category_id),
    INDEX idx_category_level (category_level),
    INDEX idx_category_path (category_path),
    INDEX idx_system_category (is_system_category),
    INDEX idx_leaf_category (is_leaf_category),
    INDEX idx_category_status (category_status),
    INDEX idx_display_order (parent_category_id, display_order),
    INDEX idx_popular_category (is_popular),
    CONSTRAINT fk_skillcategory_parent FOREIGN KEY (parent_category_id) REFERENCES MST_SkillCategory(id) ON UPDATE CASCADE ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキルカテゴリマスタ';

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

- カテゴリコードは新設時に自動採番（CAT + 3桁連番）
- システムカテゴリは is_system_category = true で保護
- 親カテゴリが無効化される場合は子カテゴリも無効化
- 末端カテゴリのみにスキルを直接紐付け可能
- カテゴリパスは親カテゴリ変更時に自動更新
- スキル数は関連スキルの増減時に自動更新
- 有効期間外のカテゴリは自動的に無効化
