# テーブル定義書：MST_SkillItem（スキル項目マスタ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-039 |
| **テーブル名** | MST_SkillItem |
| **論理名** | スキル項目マスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
スキル項目マスタテーブル（MST_SkillItem）は、システムで管理する個別のスキル項目を定義します。プログラミング言語、フレームワーク、ツール、ビジネススキル、資格など、あらゆるスキル項目を階層的に管理し、スキル評価の基盤となる重要なマスタデータです。

### 2.2 関連API
- [API-039](../../api/specs/API仕様書_API-039_スキル項目管理API.md) - スキル項目管理API

### 2.3 関連バッチ
- [BATCH-035](../../batch/specs/バッチ定義書_BATCH-035_スキル項目同期バッチ.md) - スキル項目同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | skill_item_id | スキル項目ID | VARCHAR | 20 | × | ○ | - | - | スキル項目を一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | skill_category_id | スキルカテゴリID | VARCHAR | 20 | × | - | ○ | - | 所属するスキルカテゴリID |
| 4 | parent_skill_id | 親スキルID | VARCHAR | 20 | ○ | - | ○ | NULL | 階層構造の親スキル項目ID |
| 5 | skill_code | スキルコード | VARCHAR | 50 | × | - | - | - | スキル項目の一意コード |
| 6 | skill_name | スキル名 | VARCHAR | 200 | × | - | - | - | スキル項目の名称 |
| 7 | skill_name_en | スキル名（英語） | VARCHAR | 200 | ○ | - | - | NULL | スキル項目の英語名称 |
| 8 | skill_description | スキル説明 | TEXT | - | ○ | - | - | NULL | スキル項目の詳細説明 |
| 9 | skill_type | スキル種別 | VARCHAR | 30 | × | - | - | 'TECHNICAL' | スキルの種別（TECHNICAL/BUSINESS/SOFT/CERTIFICATION等） |
| 10 | skill_level | スキルレベル | INTEGER | - | × | - | - | 1 | スキルの階層レベル（1:大分類、2:中分類、3:小分類等） |
| 11 | difficulty_level | 難易度レベル | INTEGER | - | ○ | - | - | 3 | スキルの習得難易度（1:易、5:難） |
| 12 | importance_level | 重要度レベル | INTEGER | - | ○ | - | - | 3 | スキルの重要度（1:低、5:高） |
| 13 | market_demand | 市場需要度 | INTEGER | - | ○ | - | - | 3 | 市場での需要度（1:低、5:高） |
| 14 | learning_time_hours | 学習時間目安 | INTEGER | - | ○ | - | - | NULL | 習得に必要な学習時間（時間） |
| 15 | prerequisite_skills | 前提スキル | TEXT | - | ○ | - | - | NULL | 習得に必要な前提スキル（JSON形式） |
| 16 | related_skills | 関連スキル | TEXT | - | ○ | - | - | NULL | 関連するスキル項目（JSON形式） |
| 17 | skill_keywords | スキルキーワード | TEXT | - | ○ | - | - | NULL | 検索用キーワード（JSON形式） |
| 18 | official_url | 公式URL | VARCHAR | 500 | ○ | - | - | NULL | 公式サイトのURL |
| 19 | documentation_url | ドキュメントURL | VARCHAR | 500 | ○ | - | - | NULL | 公式ドキュメントのURL |
| 20 | learning_resources | 学習リソース | TEXT | - | ○ | - | - | NULL | 推奨学習リソース（JSON形式） |
| 21 | certification_info | 資格情報 | TEXT | - | ○ | - | - | NULL | 関連資格情報（JSON形式） |
| 22 | version_info | バージョン情報 | VARCHAR | 100 | ○ | - | - | NULL | 技術のバージョン情報 |
| 23 | release_date | リリース日 | DATE | - | ○ | - | - | NULL | 技術のリリース日 |
| 24 | vendor_company | ベンダー企業 | VARCHAR | 200 | ○ | - | - | NULL | 開発・提供企業 |
| 25 | license_type | ライセンス種別 | VARCHAR | 50 | ○ | - | - | NULL | ライセンスの種別 |
| 26 | platform_support | プラットフォーム対応 | TEXT | - | ○ | - | - | NULL | 対応プラットフォーム（JSON形式） |
| 27 | industry_usage | 業界利用状況 | TEXT | - | ○ | - | - | NULL | 業界別利用状況（JSON形式） |
| 28 | skill_trend | スキルトレンド | VARCHAR | 20 | ○ | - | - | 'STABLE' | スキルのトレンド（EMERGING/GROWING/STABLE/DECLINING） |
| 29 | evaluation_criteria | 評価基準 | TEXT | - | ○ | - | - | NULL | スキル評価の基準（JSON形式） |
| 30 | assessment_method | 評価方法 | TEXT | - | ○ | - | - | NULL | 推奨評価方法（JSON形式） |
| 31 | icon_path | アイコンパス | VARCHAR | 500 | ○ | - | - | NULL | スキルアイコンのファイルパス |
| 32 | color_code | カラーコード | VARCHAR | 7 | ○ | - | - | NULL | 表示用カラーコード（#RRGGBB） |
| 33 | display_order | 表示順序 | INTEGER | - | × | - | - | 0 | カテゴリ内での表示順序 |
| 34 | is_featured | 注目スキルフラグ | BOOLEAN | - | × | - | - | FALSE | 注目すべきスキルかどうか |
| 35 | is_deprecated | 非推奨フラグ | BOOLEAN | - | × | - | - | FALSE | 非推奨スキルかどうか |
| 36 | deprecation_date | 非推奨日 | DATE | - | ○ | - | - | NULL | 非推奨となった日 |
| 37 | replacement_skill_id | 代替スキルID | VARCHAR | 20 | ○ | - | ○ | NULL | 代替となるスキル項目ID |
| 38 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | スキル項目が有効かどうか |
| 39 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 40 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 41 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 42 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | skill_item_id | 主キー |
| uq_skill_code | UNIQUE | tenant_id, skill_code | テナント内でのスキルコード一意性 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_skill_category | INDEX | skill_category_id | スキルカテゴリ検索用 |
| idx_parent_skill | INDEX | parent_skill_id | 親スキル検索用 |
| idx_skill_name | INDEX | skill_name | スキル名検索用 |
| idx_skill_type | INDEX | skill_type | スキル種別検索用 |
| idx_skill_level | INDEX | skill_level | スキルレベル検索用 |
| idx_difficulty | INDEX | difficulty_level | 難易度検索用 |
| idx_importance | INDEX | importance_level | 重要度検索用 |
| idx_market_demand | INDEX | market_demand | 市場需要度検索用 |
| idx_skill_trend | INDEX | skill_trend | スキルトレンド検索用 |
| idx_featured | INDEX | is_featured | 注目スキル検索用 |
| idx_deprecated | INDEX | is_deprecated | 非推奨スキル検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_display_order | INDEX | skill_category_id, display_order | 表示順序検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_item | PRIMARY KEY | skill_item_id | 主キー制約 |
| uq_skill_code | UNIQUE | tenant_id, skill_code | テナント内でのスキルコード一意性 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_skill_category | FOREIGN KEY | skill_category_id | MST_SkillCategory.skill_category_id |
| fk_parent_skill | FOREIGN KEY | parent_skill_id | MST_SkillItem.skill_item_id |
| fk_replacement_skill | FOREIGN KEY | replacement_skill_id | MST_SkillItem.skill_item_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_skill_type | CHECK | skill_type | skill_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'LANGUAGE', 'TOOL', 'FRAMEWORK', 'METHODOLOGY') |
| chk_skill_level | CHECK | skill_level | skill_level >= 1 AND skill_level <= 5 |
| chk_difficulty_level | CHECK | difficulty_level | difficulty_level IS NULL OR (difficulty_level >= 1 AND difficulty_level <= 5) |
| chk_importance_level | CHECK | importance_level | importance_level IS NULL OR (importance_level >= 1 AND importance_level <= 5) |
| chk_market_demand | CHECK | market_demand | market_demand IS NULL OR (market_demand >= 1 AND market_demand <= 5) |
| chk_learning_time | CHECK | learning_time_hours | learning_time_hours IS NULL OR learning_time_hours > 0 |
| chk_skill_trend | CHECK | skill_trend | skill_trend IS NULL OR skill_trend IN ('EMERGING', 'GROWING', 'STABLE', 'DECLINING') |
| chk_color_code | CHECK | color_code | color_code IS NULL OR color_code REGEXP '^#[0-9A-Fa-f]{6}$' |
| chk_display_order | CHECK | display_order | display_order >= 0 |
| chk_deprecation_logic | CHECK | is_deprecated, deprecation_date | (is_deprecated = FALSE AND deprecation_date IS NULL) OR (is_deprecated = TRUE AND deprecation_date IS NOT NULL) |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_SkillCategory | skill_category_id | 1:N | スキルカテゴリ |
| MST_SkillItem | parent_skill_id | 1:N | 親スキル項目（階層構造） |
| MST_SkillItem | replacement_skill_id | 1:N | 代替スキル項目 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_SkillItem | parent_skill_id | 1:N | 子スキル項目（階層構造） |
| MST_SkillItem | replacement_skill_id | 1:N | 代替対象スキル項目 |
| TRN_SkillRecord | skill_item_id | 1:N | スキル評価記録 |
| TRN_SkillEvidence | skill_item_id | 1:N | スキル証跡 |
| MST_JobTypeSkill | skill_item_id | 1:N | 職種スキル関連 |

## 5. データ仕様

### 5.1 データ例
```sql
-- プログラミング言語（大分類）
INSERT INTO MST_SkillItem (
    skill_item_id, tenant_id, skill_category_id, skill_code, skill_name, skill_name_en,
    skill_description, skill_type, skill_level, difficulty_level, importance_level, market_demand,
    learning_time_hours, official_url, skill_trend, is_featured, display_order,
    created_by, updated_by
) VALUES (
    'SKILL_JAVA', 'TENANT_001', 'CAT_PROGRAMMING', 'JAVA', 'Java', 'Java',
    'オブジェクト指向プログラミング言語。エンタープライズアプリケーション開発で広く使用される。',
    'TECHNICAL', 1, 3, 5, 5, 200,
    'https://www.oracle.com/java/', 'STABLE', TRUE, 1,
    'user_admin', 'user_admin'
);

-- フレームワーク（中分類）
INSERT INTO MST_SkillItem (
    skill_item_id, tenant_id, skill_category_id, parent_skill_id, skill_code, skill_name, skill_name_en,
    skill_description, skill_type, skill_level, difficulty_level, importance_level, market_demand,
    learning_time_hours, prerequisite_skills, official_url, documentation_url,
    version_info, vendor_company, skill_trend, display_order,
    created_by, updated_by
) VALUES (
    'SKILL_SPRING', 'TENANT_001', 'CAT_FRAMEWORK', 'SKILL_JAVA', 'SPRING_BOOT', 'Spring Boot', 'Spring Boot',
    'Javaベースのアプリケーション開発フレームワーク。マイクロサービス開発に最適。',
    'FRAMEWORK', 2, 3, 5, 5, 80,
    '["SKILL_JAVA"]', 'https://spring.io/projects/spring-boot', 'https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/',
    '3.2.x', 'VMware', 'GROWING', 1,
    'user_admin', 'user_admin'
);

-- ライブラリ（小分類）
INSERT INTO MST_SkillItem (
    skill_item_id, tenant_id, skill_category_id, parent_skill_id, skill_code, skill_name, skill_name_en,
    skill_description, skill_type, skill_level, difficulty_level, importance_level, market_demand,
    learning_time_hours, prerequisite_skills, related_skills, official_url,
    license_type, skill_trend, display_order,
    created_by, updated_by
) VALUES (
    'SKILL_HIBERNATE', 'TENANT_001', 'CAT_FRAMEWORK', 'SKILL_SPRING', 'HIBERNATE', 'Hibernate', 'Hibernate',
    'Java用のオブジェクト関係マッピング（ORM）フレームワーク。',
    'FRAMEWORK', 3, 4, 4, 4, 40,
    '["SKILL_JAVA", "SKILL_SQL"]', '["SKILL_JPA", "SKILL_MYBATIS"]', 'https://hibernate.org/',
    'LGPL', 'STABLE', 2,
    'user_admin', 'user_admin'
);

-- クラウドサービス
INSERT INTO MST_SkillItem (
    skill_item_id, tenant_id, skill_category_id, skill_code, skill_name, skill_name_en,
    skill_description, skill_type, skill_level, difficulty_level, importance_level, market_demand,
    learning_time_hours, learning_resources, certification_info, official_url,
    vendor_company, platform_support, skill_trend, is_featured, display_order,
    created_by, updated_by
) VALUES (
    'SKILL_AWS', 'TENANT_001', 'CAT_CLOUD', 'AWS', 'Amazon Web Services', 'Amazon Web Services',
    'Amazonが提供するクラウドコンピューティングプラットフォーム。',
    'TECHNICAL', 1, 4, 5, 5, 300,
    '["AWS公式トレーニング", "AWS認定試験対策"]', '["AWS認定ソリューションアーキテクト", "AWS認定デベロッパー"]',
    'https://aws.amazon.com/', 'Amazon', '["Web", "Mobile", "IoT"]',
    'GROWING', TRUE, 1,
    'user_admin', 'user_admin'
);

-- ビジネススキル
INSERT INTO MST_SkillItem (
    skill_item_id, tenant_id, skill_category_id, skill_code, skill_name, skill_name_en,
    skill_description, skill_type, skill_level, difficulty_level, importance_level, market_demand,
    learning_time_hours, evaluation_criteria, assessment_method, skill_trend, display_order,
    created_by, updated_by
) VALUES (
    'SKILL_PROJECT_MGMT', 'TENANT_001', 'CAT_BUSINESS', 'PROJECT_MANAGEMENT', 'プロジェクト管理', 'Project Management',
    'プロジェクトの計画、実行、監視、制御、終結を行うスキル。',
    'BUSINESS', 1, 3, 5, 4, 120,
    '["計画立案能力", "リスク管理", "チームマネジメント", "コミュニケーション"]',
    '["実績評価", "360度評価", "資格取得"]', 'STABLE', 1,
    'user_admin', 'user_admin'
);

-- 非推奨スキル
INSERT INTO MST_SkillItem (
    skill_item_id, tenant_id, skill_category_id, skill_code, skill_name, skill_name_en,
    skill_description, skill_type, skill_level, difficulty_level, importance_level, market_demand,
    learning_time_hours, official_url, skill_trend, is_deprecated, deprecation_date,
    replacement_skill_id, display_order, created_by, updated_by
) VALUES (
    'SKILL_FLASH', 'TENANT_001', 'CAT_WEB', 'ADOBE_FLASH', 'Adobe Flash', 'Adobe Flash',
    'Webブラウザ用のマルチメディアプラットフォーム。2020年にサポート終了。',
    'TECHNICAL', 1, 2, 1, 1, 60,
    'https://www.adobe.com/products/flashplayer/', 'DECLINING', TRUE, '2020-12-31',
    'SKILL_HTML5', 999, 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 基本的なスキル項目 |
| 月間増加件数 | 20件 | 新技術・新スキルの追加 |
| 年間増加件数 | 240件 | 想定値 |
| 5年後想定件数 | 1,700件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：非推奨から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 最高 | skill_category_id, is_active | カテゴリ別スキル一覧取得 |
| SELECT | 高 | skill_name, is_active | スキル名検索 |
| SELECT | 高 | skill_type, is_active | 種別別スキル取得 |
| SELECT | 中 | parent_skill_id | 階層構造検索 |
| SELECT | 中 | is_featured | 注目スキル取得 |
| INSERT | 低 | - | 新規スキル項目登録 |
| UPDATE | 低 | skill_item_id | スキル項目情報更新 |

### 7.2 パフォーマンス要件
- SELECT：20ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| skill_admin | ○ | ○ | ○ | × | スキル管理者 |
| manager | ○ | × | × | × | 管理職（参照のみ） |
| employee | ○ | × | × | × | 一般社員（参照のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含まない
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存スキル管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_SkillItem (
    skill_item_id VARCHAR(20) NOT NULL COMMENT 'スキル項目ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    skill_category_id VARCHAR(20) NOT NULL COMMENT 'スキルカテゴリID',
    parent_skill_id VARCHAR(20) NULL COMMENT '親スキルID',
    skill_code VARCHAR(50) NOT NULL COMMENT 'スキルコード',
    skill_name VARCHAR(200) NOT NULL COMMENT 'スキル名',
    skill_name_en VARCHAR(200) NULL COMMENT 'スキル名（英語）',
    skill_description TEXT NULL COMMENT 'スキル説明',
    skill_type VARCHAR(30) NOT NULL DEFAULT 'TECHNICAL' COMMENT 'スキル種別',
    skill_level INTEGER NOT NULL DEFAULT 1 COMMENT 'スキルレベル',
    difficulty_level INTEGER NULL DEFAULT 3 COMMENT '難易度レベル',
    importance_level INTEGER NULL DEFAULT 3 COMMENT '重要度レベル',
    market_demand INTEGER NULL DEFAULT 3 COMMENT '市場需要度',
    learning_time_hours INTEGER NULL COMMENT '学習時間目安',
    prerequisite_skills TEXT NULL COMMENT '前提スキル',
    related_skills TEXT NULL COMMENT '関連スキル',
    skill_keywords TEXT NULL COMMENT 'スキルキーワード',
    official_url VARCHAR(500) NULL COMMENT '公式URL',
    documentation_url VARCHAR(500) NULL COMMENT 'ドキュメントURL',
    learning_resources TEXT NULL COMMENT '学習リソース',
    certification_info TEXT NULL COMMENT '資格情報',
    version_info VARCHAR(100) NULL COMMENT 'バージョン情報',
    release_date DATE NULL COMMENT 'リリース日',
    vendor_company VARCHAR(200) NULL COMMENT 'ベンダー企業',
    license_type VARCHAR(50) NULL COMMENT 'ライセンス種別',
    platform_support TEXT NULL COMMENT 'プラットフォーム対応',
    industry_usage TEXT NULL COMMENT '業界利用状況',
    skill_trend VARCHAR(20) NULL DEFAULT 'STABLE' COMMENT 'スキルトレンド',
    evaluation_criteria TEXT NULL COMMENT '評価基準',
    assessment_method TEXT NULL COMMENT '評価方法',
    icon_path VARCHAR(500) NULL COMMENT 'アイコンパス',
    color_code VARCHAR(7) NULL COMMENT 'カラーコード',
    display_order INTEGER NOT NULL DEFAULT 0 COMMENT '表示順序',
    is_featured BOOLEAN NOT NULL DEFAULT FALSE COMMENT '注目スキルフラグ',
    is_deprecated BOOLEAN NOT NULL DEFAULT FALSE COMMENT '非推奨フラグ',
    deprecation_date DATE NULL COMMENT '非推奨日',
    replacement_skill_id VARCHAR(20) NULL COMMENT '代替スキルID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (skill_item_id),
    UNIQUE KEY uq_skill_code (tenant_id, skill_code),
    INDEX idx_tenant (tenant_id),
    INDEX idx_skill_category (skill_category_id),
    INDEX idx_parent_skill (parent_skill_id),
    INDEX idx_skill_name (skill_name),
    INDEX idx_skill_type (skill_type),
    INDEX idx_skill_level (skill_level),
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_importance (importance_level),
    INDEX idx_market_demand (market_demand),
    INDEX idx_skill_trend (skill_trend),
    INDEX idx_featured (is_featured),
    INDEX idx_deprecated (is_deprecated),
    INDEX idx_active (is_active),
    INDEX idx_display_order (skill_category_id, display_order),
    CONSTRAINT fk_skill_item_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_item_category FOREIGN KEY (skill_category_id) REFERENCES MST_SkillCategory(skill_category_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_item_parent FOREIGN KEY (parent_skill_id) REFERENCES MST_SkillItem(skill_item_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_item_replacement FOREIGN KEY (replacement_skill_id) REFERENCES MST_SkillItem(skill_item_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_item_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_item_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_item_type CHECK (skill_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'CERTIFICATION', 'LANGUAGE', 'TOOL', 'FRAMEWORK', 'METHODOLOGY')),
    CONSTRAINT chk_skill_item_level CHECK (skill_level >= 1 AND skill_level <= 5),
    CONSTRAINT chk_skill_item_difficulty CHECK (difficulty_level IS NULL OR (difficulty_level >= 1 AND difficulty_level <= 5)),
    CONSTRAINT chk_skill_item_importance CHECK (importance_level IS NULL OR (importance_level >= 1 AND importance_level <= 5)),
    CONSTRAINT chk_skill_item_market_demand CHECK (market_demand IS NULL OR (market_demand >= 1 AND market_demand <= 5)),
    CONSTRAINT chk_skill_item_learning_time CHECK (learning_time_hours IS NULL OR learning_time_hours > 0),
    CONSTRAINT chk_skill_item_trend CHECK (skill_trend IS NULL OR skill_trend IN ('EMERGING', 'GROWING', 'STABLE', 'DECLINING')),
    CONSTRAINT chk_skill_item_color_code CHECK (color_code IS NULL OR color_code REGEXP '^#[0-9A-Fa-f]{6}
),
    CONSTRAINT chk_skill_item_display_order CHECK (display_order >= 0),
    CONSTRAINT chk_skill_item_deprecation CHECK ((is_deprecated = FALSE AND deprecation_date IS NULL) OR (is_deprecated = TRUE AND deprecation_date IS NOT NULL))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキル項目マスタ';
```

## 10. 特記事項

1. **階層構造管理**
   - parent_skill_idによる階層構造をサポート
   - 大分類→中分類→小分類の3階層構造を想定
   - 自己参照外部キーによる柔軟な階層管理

2. **スキルトレンド管理**
   - EMERGING（新興）、GROWING（成長）、STABLE（安定）、DECLINING（衰退）
   - 市場動向に応じたスキル分類

3. **非推奨スキル管理**
   - 技術の陳腐化に対応した非推奨フラグ
   - 代替スキルへの移行パス管理

4. **多言語対応**
   - 日本語・英語でのスキル名管理
   - 国際的な技術名称への対応

5. **学習支援情報**
   - 学習時間目安、前提スキル、学習リソース
   - スキル習得の効率化支援

6. **評価基準管理**
   - スキル別の評価基準・評価方法定義
   - 客観的で一貫性のある評価の実現
