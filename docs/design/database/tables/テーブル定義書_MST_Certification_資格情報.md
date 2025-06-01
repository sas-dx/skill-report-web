# テーブル定義書：MST_Certification（資格情報）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-037 |
| **テーブル名** | MST_Certification |
| **論理名** | 資格情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 中 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
資格情報テーブル（MST_Certification）は、IT資格、業界資格、社内認定などの各種資格・認定情報を管理します。資格の詳細情報、取得要件、有効期限、更新条件などを保持し、スキル評価や人材育成計画の基盤となります。

### 2.2 関連API
- [API-033](../../api/specs/API仕様書_API-033_資格管理API.md) - 資格管理API

### 2.3 関連バッチ
- [BATCH-023](../../batch/specs/バッチ定義書_BATCH-023_資格情報同期バッチ.md) - 資格情報同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | certification_id | 資格ID | VARCHAR | 20 | × | ○ | - | - | 資格を一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | テナント固有資格の場合のテナントID |
| 3 | certification_code | 資格コード | VARCHAR | 20 | × | - | - | - | 資格のコード |
| 4 | certification_name | 資格名 | VARCHAR | 200 | × | - | - | - | 資格の正式名称 |
| 5 | certification_name_en | 資格名（英語） | VARCHAR | 200 | ○ | - | - | NULL | 資格名の英語表記 |
| 6 | certification_abbr | 資格略称 | VARCHAR | 50 | ○ | - | - | NULL | 資格の略称・通称 |
| 7 | certification_type | 資格種別 | VARCHAR | 20 | × | - | - | 'IT' | 資格の種別（IT/BUSINESS/LANGUAGE/INTERNAL等） |
| 8 | certification_category | 資格カテゴリ | VARCHAR | 50 | ○ | - | - | NULL | 資格の詳細カテゴリ |
| 9 | issuing_organization | 発行機関 | VARCHAR | 200 | × | - | - | - | 資格を発行する機関・団体 |
| 10 | issuing_country | 発行国 | VARCHAR | 10 | ○ | - | - | 'JP' | 資格の発行国（ISO 3166-1 alpha-2） |
| 11 | description | 説明 | TEXT | - | ○ | - | - | NULL | 資格の詳細説明 |
| 12 | difficulty_level | 難易度レベル | INTEGER | - | × | - | - | 1 | 資格の難易度（1:初級、2:中級、3:上級、4:エキスパート、5:マスター） |
| 13 | exam_format | 試験形式 | VARCHAR | 50 | ○ | - | - | NULL | 試験の形式（CBT/筆記/実技/論文等） |
| 14 | exam_duration | 試験時間 | INTEGER | - | ○ | - | - | NULL | 試験時間（分） |
| 15 | passing_score | 合格点 | INTEGER | - | ○ | - | - | NULL | 合格に必要な点数 |
| 16 | max_score | 満点 | INTEGER | - | ○ | - | - | NULL | 試験の満点 |
| 17 | prerequisites | 受験要件 | TEXT | - | ○ | - | - | NULL | 受験に必要な要件・条件 |
| 18 | study_hours | 学習時間目安 | INTEGER | - | ○ | - | - | NULL | 合格に必要な学習時間の目安（時間） |
| 19 | exam_fee | 受験料 | INTEGER | - | ○ | - | - | NULL | 受験料（円） |
| 20 | validity_period | 有効期間 | INTEGER | - | ○ | - | - | NULL | 資格の有効期間（月数） |
| 21 | renewal_required | 更新要否 | BOOLEAN | - | × | - | - | FALSE | 資格の更新が必要かどうか |
| 22 | renewal_conditions | 更新条件 | TEXT | - | ○ | - | - | NULL | 資格更新に必要な条件 |
| 23 | official_url | 公式URL | VARCHAR | 500 | ○ | - | - | NULL | 資格の公式サイトURL |
| 24 | study_resources | 学習リソース | TEXT | - | ○ | - | - | NULL | 推奨学習教材・リソース |
| 25 | related_skills | 関連スキル | TEXT | - | ○ | - | - | NULL | 資格に関連するスキル項目 |
| 26 | icon_url | アイコンURL | VARCHAR | 500 | ○ | - | - | NULL | 資格のアイコン画像URL |
| 27 | badge_url | バッジURL | VARCHAR | 500 | ○ | - | - | NULL | 資格バッジ画像URL |
| 28 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | 資格一覧での表示順序 |
| 29 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 資格が有効かどうか |
| 30 | effective_date | 有効開始日 | DATE | - | × | - | - | - | 資格の有効開始日 |
| 31 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | 資格の有効終了日 |
| 32 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 33 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 34 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 35 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | certification_id | 主キー |
| idx_certification_code | UNIQUE | certification_code | 資格コードの一意性を保証 |
| idx_tenant_cert | INDEX | tenant_id, certification_code | テナント内資格コード検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_cert_type | INDEX | certification_type | 資格種別検索用 |
| idx_cert_category | INDEX | certification_category | 資格カテゴリ検索用 |
| idx_issuing_org | INDEX | issuing_organization | 発行機関検索用 |
| idx_difficulty | INDEX | difficulty_level | 難易度検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_certification | PRIMARY KEY | certification_id | 主キー制約 |
| uq_certification_code | UNIQUE | certification_code | 資格コードの一意性を保証 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_cert_type | CHECK | certification_type | certification_type IN ('IT', 'BUSINESS', 'LANGUAGE', 'INTERNAL', 'PROFESSIONAL', 'ACADEMIC') |
| chk_difficulty_level | CHECK | difficulty_level | difficulty_level >= 1 AND difficulty_level <= 5 |
| chk_exam_duration | CHECK | exam_duration | exam_duration IS NULL OR exam_duration > 0 |
| chk_passing_score | CHECK | passing_score | passing_score IS NULL OR passing_score >= 0 |
| chk_max_score | CHECK | max_score | max_score IS NULL OR max_score > 0 |
| chk_score_relation | CHECK | passing_score, max_score | passing_score IS NULL OR max_score IS NULL OR passing_score <= max_score |
| chk_study_hours | CHECK | study_hours | study_hours IS NULL OR study_hours > 0 |
| chk_exam_fee | CHECK | exam_fee | exam_fee IS NULL OR exam_fee >= 0 |
| chk_validity_period | CHECK | validity_period | validity_period IS NULL OR validity_period > 0 |
| chk_expiry_date | CHECK | expiry_date | expiry_date IS NULL OR expiry_date >= effective_date |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_CertificationRequirement | certification_id | 1:N | 資格要件マスタ |
| TRN_EmployeeCertification | certification_id | 1:N | 社員資格取得履歴 |

## 5. データ仕様

### 5.1 データ例
```sql
-- IT資格（基本情報技術者）
INSERT INTO MST_Certification (
    certification_id, certification_code, certification_name, certification_name_en,
    certification_abbr, certification_type, certification_category,
    issuing_organization, issuing_country, description, difficulty_level,
    exam_format, exam_duration, passing_score, max_score,
    study_hours, exam_fee, validity_period, renewal_required,
    official_url, is_active, effective_date, created_by, updated_by
) VALUES (
    'CERT_001', 'FE', '基本情報技術者試験', 'Fundamental Information Technology Engineer Examination',
    'FE', 'IT', 'IPA国家試験',
    '独立行政法人情報処理推進機構', 'JP',
    'ITエンジニアとしての基本的な知識・技能を問う国家試験',
    2, 'CBT', 150, 600, 1000,
    200, 7700, NULL, FALSE,
    'https://www.jitec.ipa.go.jp/1_11seido/fe.html',
    TRUE, '2025-04-01', 'system', 'system'
);

-- ビジネス資格（PMP）
INSERT INTO MST_Certification (
    certification_id, certification_code, certification_name, certification_name_en,
    certification_abbr, certification_type, certification_category,
    issuing_organization, issuing_country, description, difficulty_level,
    exam_format, exam_duration, prerequisites, study_hours, exam_fee,
    validity_period, renewal_required, renewal_conditions,
    official_url, is_active, effective_date, created_by, updated_by
) VALUES (
    'CERT_002', 'PMP', 'プロジェクトマネジメント・プロフェッショナル', 'Project Management Professional',
    'PMP', 'BUSINESS', 'プロジェクト管理',
    'Project Management Institute', 'US',
    'プロジェクトマネジメントの国際的な資格認定',
    4, 'CBT', 230, 'プロジェクトマネジメント経験4500時間以上',
    300, 55000, 36, TRUE, 'PDU 60単位の取得',
    'https://www.pmi.org/certifications/project-management-pmp',
    TRUE, '2025-04-01', 'system', 'system'
);

-- 語学資格（TOEIC）
INSERT INTO MST_Certification (
    certification_id, certification_code, certification_name, certification_name_en,
    certification_abbr, certification_type, certification_category,
    issuing_organization, issuing_country, description, difficulty_level,
    exam_format, exam_duration, max_score, study_hours, exam_fee,
    validity_period, renewal_required,
    official_url, is_active, effective_date, created_by, updated_by
) VALUES (
    'CERT_003', 'TOEIC', 'TOEIC Listening & Reading Test', 'Test of English for International Communication',
    'TOEIC L&R', 'LANGUAGE', '英語能力測定',
    '国際ビジネスコミュニケーション協会', 'JP',
    '英語によるコミュニケーション能力を測定するテスト',
    3, '筆記', 120, 990, 100, 7810,
    24, FALSE,
    'https://www.iibc-global.org/toeic.html',
    TRUE, '2025-04-01', 'system', 'system'
);

-- 社内認定資格
INSERT INTO MST_Certification (
    certification_id, tenant_id, certification_code, certification_name,
    certification_type, certification_category, issuing_organization,
    description, difficulty_level, validity_period, renewal_required,
    is_active, effective_date, created_by, updated_by
) VALUES (
    'CERT_T001', 'TENANT_001', 'INTERNAL_ARCH', '社内アーキテクト認定',
    'INTERNAL', '技術認定', '株式会社サンプル',
    '社内システムアーキテクトとしての技術認定',
    4, 24, TRUE,
    TRUE, '2025-04-01', 'admin_001', 'admin_001'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 主要IT資格・ビジネス資格 |
| 年間増加件数 | 50件 | 新規資格・社内認定追加 |
| 5年後想定件数 | 750件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：廃止から5年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | is_active, certification_type | 有効資格取得 |
| SELECT | 高 | certification_category | カテゴリ別検索 |
| SELECT | 中 | difficulty_level | 難易度別検索 |
| SELECT | 中 | issuing_organization | 発行機関別検索 |
| UPDATE | 低 | certification_id | 資格情報更新 |
| INSERT | 低 | - | 新規資格登録 |

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
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含まない
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存資格管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_Certification (
    certification_id VARCHAR(20) NOT NULL COMMENT '資格ID',
    tenant_id VARCHAR(50) NULL COMMENT 'テナントID',
    certification_code VARCHAR(20) NOT NULL COMMENT '資格コード',
    certification_name VARCHAR(200) NOT NULL COMMENT '資格名',
    certification_name_en VARCHAR(200) NULL COMMENT '資格名（英語）',
    certification_abbr VARCHAR(50) NULL COMMENT '資格略称',
    certification_type VARCHAR(20) NOT NULL DEFAULT 'IT' COMMENT '資格種別',
    certification_category VARCHAR(50) NULL COMMENT '資格カテゴリ',
    issuing_organization VARCHAR(200) NOT NULL COMMENT '発行機関',
    issuing_country VARCHAR(10) NULL DEFAULT 'JP' COMMENT '発行国',
    description TEXT NULL COMMENT '説明',
    difficulty_level INTEGER NOT NULL DEFAULT 1 COMMENT '難易度レベル',
    exam_format VARCHAR(50) NULL COMMENT '試験形式',
    exam_duration INTEGER NULL COMMENT '試験時間',
    passing_score INTEGER NULL COMMENT '合格点',
    max_score INTEGER NULL COMMENT '満点',
    prerequisites TEXT NULL COMMENT '受験要件',
    study_hours INTEGER NULL COMMENT '学習時間目安',
    exam_fee INTEGER NULL COMMENT '受験料',
    validity_period INTEGER NULL COMMENT '有効期間',
    renewal_required BOOLEAN NOT NULL DEFAULT FALSE COMMENT '更新要否',
    renewal_conditions TEXT NULL COMMENT '更新条件',
    official_url VARCHAR(500) NULL COMMENT '公式URL',
    study_resources TEXT NULL COMMENT '学習リソース',
    related_skills TEXT NULL COMMENT '関連スキル',
    icon_url VARCHAR(500) NULL COMMENT 'アイコンURL',
    badge_url VARCHAR(500) NULL COMMENT 'バッジURL',
    sort_order INTEGER NOT NULL DEFAULT 0 COMMENT '表示順序',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    effective_date DATE NOT NULL COMMENT '有効開始日',
    expiry_date DATE NULL COMMENT '有効終了日',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (certification_id),
    UNIQUE KEY idx_certification_code (certification_code),
    INDEX idx_tenant_cert (tenant_id, certification_code),
    INDEX idx_tenant (tenant_id),
    INDEX idx_cert_type (certification_type),
    INDEX idx_cert_category (certification_category),
    INDEX idx_issuing_org (issuing_organization),
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    CONSTRAINT fk_certification_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_certification_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_certification_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_certification_type CHECK (certification_type IN ('IT', 'BUSINESS', 'LANGUAGE', 'INTERNAL', 'PROFESSIONAL', 'ACADEMIC')),
    CONSTRAINT chk_certification_difficulty CHECK (difficulty_level >= 1 AND difficulty_level <= 5),
    CONSTRAINT chk_certification_exam_duration CHECK (exam_duration IS NULL OR exam_duration > 0),
    CONSTRAINT chk_certification_passing_score CHECK (passing_score IS NULL OR passing_score >= 0),
    CONSTRAINT chk_certification_max_score CHECK (max_score IS NULL OR max_score > 0),
    CONSTRAINT chk_certification_score_relation CHECK (passing_score IS NULL OR max_score IS NULL OR passing_score <= max_score),
    CONSTRAINT chk_certification_study_hours CHECK (study_hours IS NULL OR study_hours > 0),
    CONSTRAINT chk_certification_exam_fee CHECK (exam_fee IS NULL OR exam_fee >= 0),
    CONSTRAINT chk_certification_validity_period CHECK (validity_period IS NULL OR validity_period > 0),
    CONSTRAINT chk_certification_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='資格情報';
```

## 10. 特記事項

1. **多様な資格種別対応**
   - IT、BUSINESS、LANGUAGE、INTERNAL、PROFESSIONAL、ACADEMIC
   - 幅広い分野の資格を統一的に管理

2. **詳細な試験情報管理**
   - 試験形式、時間、合格点、受験料など詳細情報を保持
   - 受験計画立案を支援

3. **資格更新管理**
   - 有効期間と更新要否を管理
   - 更新条件の明確化により継続的な資格維持を支援

4. **学習支援情報**
   - 学習時間目安、推奨リソース、関連スキルを提供
   - 効率的な資格取得を支援

5. **国際対応**
   - 発行国情報により国際資格も管理可能
   - 英語名称対応でグローバル展開を支援

6. **視覚的表現**
   - アイコンとバッジによる視覚的な資格表現
   - モチベーション向上とわかりやすい表示

7. **マルチテナント対応**
   - システム標準資格とテナント固有資格（社内認定等）の混在管理
   - tenant_idがNULLの場合はシステム標準資格

8. **論理削除による履歴管理**
   - 資格廃止時は論理削除（is_active=FALSE）を使用
   - 有効期間により資格変更履歴を管理

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-06-01 | システムアーキテクト | 新フォーマットで初版作成 |
