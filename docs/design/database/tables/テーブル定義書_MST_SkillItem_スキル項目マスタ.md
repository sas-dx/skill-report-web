# テーブル定義書：MST_SkillItem（スキル項目マスタ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-035 |
| **テーブル名** | MST_SkillItem |
| **論理名** | スキル項目マスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
スキル項目マスタテーブル（MST_SkillItem）は、具体的なスキル項目を管理します。各スキル項目はスキルカテゴリに分類され、評価レベル、必要な証跡、関連資格などの詳細情報を保持します。マルチテナント対応により、テナント固有のスキル項目も管理可能です。

### 2.2 関連API
- [API-031](../../api/specs/API仕様書_API-031_スキル項目管理API.md) - スキル項目管理API

### 2.3 関連バッチ
- [BATCH-021](../../batch/specs/バッチ定義書_BATCH-021_スキル項目同期バッチ.md) - スキル項目同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | skill_item_id | スキル項目ID | VARCHAR | 20 | × | ○ | - | - | スキル項目を一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | テナント固有項目の場合のテナントID |
| 3 | category_id | カテゴリID | VARCHAR | 20 | × | - | ○ | - | 所属するスキルカテゴリのID |
| 4 | skill_code | スキルコード | VARCHAR | 20 | × | - | - | - | スキル項目のコード |
| 5 | skill_name | スキル名 | VARCHAR | 100 | × | - | - | - | スキル項目の名称 |
| 6 | skill_name_en | スキル名（英語） | VARCHAR | 100 | ○ | - | - | NULL | スキル名の英語表記 |
| 7 | skill_type | スキル種別 | VARCHAR | 20 | × | - | - | 'TECHNICAL' | スキルの種別（TECHNICAL/BUSINESS/SOFT等） |
| 8 | difficulty_level | 難易度レベル | INTEGER | - | × | - | - | 1 | スキルの難易度（1:初級、2:中級、3:上級、4:エキスパート、5:マスター） |
| 9 | description | 説明 | TEXT | - | ○ | - | - | NULL | スキル項目の詳細説明 |
| 10 | evaluation_criteria | 評価基準 | TEXT | - | ○ | - | - | NULL | スキル評価の具体的基準 |
| 11 | required_evidence | 必要な証跡 | TEXT | - | ○ | - | - | NULL | スキル証明に必要な証跡・資料 |
| 12 | learning_resources | 学習リソース | TEXT | - | ○ | - | - | NULL | 推奨学習リソース・教材 |
| 13 | related_certifications | 関連資格 | TEXT | - | ○ | - | - | NULL | 関連する資格・認定 |
| 14 | prerequisite_skills | 前提スキル | TEXT | - | ○ | - | - | NULL | 習得に必要な前提スキル |
| 15 | estimated_hours | 習得予想時間 | INTEGER | - | ○ | - | - | NULL | 習得に必要な予想時間（時間） |
| 16 | tags | タグ | VARCHAR | 500 | ○ | - | - | NULL | 検索用タグ（カンマ区切り） |
| 17 | icon_url | アイコンURL | VARCHAR | 500 | ○ | - | - | NULL | スキル項目のアイコン画像URL |
| 18 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | カテゴリ内での表示順序 |
| 19 | is_system_skill | システムスキルフラグ | BOOLEAN | - | × | - | - | FALSE | システム標準スキルかどうか |
| 20 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | スキル項目が有効かどうか |
| 21 | effective_date | 有効開始日 | DATE | - | × | - | - | - | スキル項目の有効開始日 |
| 22 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | スキル項目の有効終了日 |
| 23 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 24 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 25 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 26 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | skill_item_id | 主キー |
| idx_skill_code | UNIQUE | skill_code | スキルコードの一意性を保証 |
| idx_tenant_skill | INDEX | tenant_id, skill_code | テナント内スキルコード検索用 |
| idx_category | INDEX | category_id | カテゴリ検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_skill_type | INDEX | skill_type | スキル種別検索用 |
| idx_difficulty | INDEX | difficulty_level | 難易度検索用 |
| idx_system | INDEX | is_system_skill | システムスキル検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |
| idx_tags | INDEX | tags | タグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_item | PRIMARY KEY | skill_item_id | 主キー制約 |
| uq_skill_code | UNIQUE | skill_code | スキルコードの一意性を保証 |
| fk_category | FOREIGN KEY | category_id | MST_SkillCategory.category_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_skill_type | CHECK | skill_type | skill_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'LANGUAGE', 'CERTIFICATION') |
| chk_difficulty_level | CHECK | difficulty_level | difficulty_level >= 1 AND difficulty_level <= 5 |
| chk_estimated_hours | CHECK | estimated_hours | estimated_hours IS NULL OR estimated_hours > 0 |
| chk_expiry_date | CHECK | expiry_date | expiry_date IS NULL OR expiry_date >= effective_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_SkillCategory | category_id | 1:N | スキルカテゴリ |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_SkillRecord | skill_item_id | 1:N | スキル評価記録 |
| TRN_SkillEvidence | skill_item_id | 1:N | スキル証跡 |
| MST_JobTypeSkill | skill_item_id | 1:N | 職種スキル関連 |

## 5. データ仕様

### 5.1 データ例
```sql
-- システム標準技術スキル
INSERT INTO MST_SkillItem (
    skill_item_id, category_id, skill_code, skill_name, skill_name_en,
    skill_type, difficulty_level, description, evaluation_criteria,
    required_evidence, learning_resources, related_certifications,
    estimated_hours, tags, is_system_skill, effective_date,
    created_by, updated_by
) VALUES (
    'SKILL_001', 'CAT_002', 'JAVA', 'Java', 'Java Programming',
    'TECHNICAL', 3, 'Javaプログラミング言語の習得',
    '実務でJavaを使用したアプリケーション開発が可能',
    'ソースコード、開発実績、プロジェクト成果物',
    'Oracle Java認定資格、オンライン学習プラットフォーム',
    'Oracle Java SE認定資格',
    200, 'プログラミング,Java,オブジェクト指向',
    TRUE, '2025-04-01', 'system', 'system'
);

-- ビジネススキル
INSERT INTO MST_SkillItem (
    skill_item_id, category_id, skill_code, skill_name, skill_name_en,
    skill_type, difficulty_level, description, evaluation_criteria,
    required_evidence, estimated_hours, tags, is_system_skill,
    effective_date, created_by, updated_by
) VALUES (
    'SKILL_002', 'CAT_003', 'PROJECT_MGMT', 'プロジェクト管理', 'Project Management',
    'BUSINESS', 4, 'プロジェクトの計画・実行・管理スキル',
    'プロジェクトリーダーとして成功実績がある',
    'プロジェクト計画書、実績報告書、チーム評価',
    150, 'プロジェクト管理,リーダーシップ,計画',
    TRUE, '2025-04-01', 'system', 'system'
);

-- テナント固有スキル
INSERT INTO MST_SkillItem (
    skill_item_id, tenant_id, category_id, skill_code, skill_name,
    skill_type, difficulty_level, description, is_system_skill,
    effective_date, created_by, updated_by
) VALUES (
    'SKILL_T001', 'TENANT_001', 'CAT_T001', 'CUSTOM_TOOL', '社内ツール操作',
    'TECHNICAL', 2, '社内独自開発ツールの操作スキル',
    FALSE, '2025-04-01', 'admin_001', 'admin_001'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 1,000件 | システム標準スキル |
| 年間増加件数 | 200件 | カスタムスキル追加 |
| 5年後想定件数 | 2,000件 | 想定値 |

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
| SELECT | 高 | is_active, category_id | 有効スキル項目取得 |
| SELECT | 高 | skill_type, difficulty_level | スキル種別・難易度検索 |
| SELECT | 中 | tags | タグ検索 |
| SELECT | 中 | tenant_id | テナント固有スキル取得 |
| UPDATE | 低 | skill_item_id | スキル項目情報更新 |
| INSERT | 低 | - | 新規スキル項目作成 |

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
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
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
CREATE TABLE MST_SkillItem (
    skill_item_id VARCHAR(20) NOT NULL COMMENT 'スキル項目ID',
    tenant_id VARCHAR(50) NULL COMMENT 'テナントID',
    category_id VARCHAR(20) NOT NULL COMMENT 'カテゴリID',
    skill_code VARCHAR(20) NOT NULL COMMENT 'スキルコード',
    skill_name VARCHAR(100) NOT NULL COMMENT 'スキル名',
    skill_name_en VARCHAR(100) NULL COMMENT 'スキル名（英語）',
    skill_type VARCHAR(20) NOT NULL DEFAULT 'TECHNICAL' COMMENT 'スキル種別',
    difficulty_level INTEGER NOT NULL DEFAULT 1 COMMENT '難易度レベル',
    description TEXT NULL COMMENT '説明',
    evaluation_criteria TEXT NULL COMMENT '評価基準',
    required_evidence TEXT NULL COMMENT '必要な証跡',
    learning_resources TEXT NULL COMMENT '学習リソース',
    related_certifications TEXT NULL COMMENT '関連資格',
    prerequisite_skills TEXT NULL COMMENT '前提スキル',
    estimated_hours INTEGER NULL COMMENT '習得予想時間',
    tags VARCHAR(500) NULL COMMENT 'タグ',
    icon_url VARCHAR(500) NULL COMMENT 'アイコンURL',
    sort_order INTEGER NOT NULL DEFAULT 0 COMMENT '表示順序',
    is_system_skill BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'システムスキルフラグ',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    effective_date DATE NOT NULL COMMENT '有効開始日',
    expiry_date DATE NULL COMMENT '有効終了日',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (skill_item_id),
    UNIQUE KEY idx_skill_code (skill_code),
    INDEX idx_tenant_skill (tenant_id, skill_code),
    INDEX idx_category (category_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_skill_type (skill_type),
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_system (is_system_skill),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    INDEX idx_tags (tags),
    CONSTRAINT fk_skill_item_category FOREIGN KEY (category_id) REFERENCES MST_SkillCategory(category_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_item_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_item_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_item_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_item_type CHECK (skill_type IN ('TECHNICAL', 'BUSINESS', 'SOFT', 'LANGUAGE', 'CERTIFICATION')),
    CONSTRAINT chk_skill_item_difficulty CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
    CONSTRAINT chk_skill_item_hours CHECK (estimated_hours IS NULL OR estimated_hours > 0),
    CONSTRAINT chk_skill_item_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキル項目マスタ';
```

## 10. 特記事項

1. **多様なスキル種別対応**
   - TECHNICAL（技術）、BUSINESS（ビジネス）、SOFT（ソフト）、LANGUAGE（言語）、CERTIFICATION（資格）
   - 幅広いスキル分野をカバー

2. **5段階難易度レベル**
   - 1:初級、2:中級、3:上級、4:エキスパート、5:マスター
   - 明確な習得レベルの定義

3. **学習支援情報**
   - 学習リソース、関連資格、前提スキル、習得予想時間
   - 効率的なスキル習得を支援

4. **柔軟な検索機能**
   - タグによる横断的検索
   - スキル種別、難易度による絞り込み

5. **マルチテナント対応**
   - システム標準スキルとテナント固有スキルの混在管理
   - tenant_idがNULLの場合はシステム標準スキル

6. **評価基準の明確化**
   - 具体的な評価基準と必要証跡を定義
   - 客観的なスキル評価を支援

7. **論理削除による履歴管理**
   - スキル項目廃止時は論理削除（is_active=FALSE）を使用
   - 有効期間によりスキル項目変更履歴を管理

8. **システム標準スキルの保護**
   - システム標準スキル（is_system_skill=TRUE）は削除不可
   - テナント管理者による誤削除を防止

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-06-01 | システムアーキテクト | 新フォーマットで初版作成 |
