# テーブル定義書：MST_SkillGrade（スキルグレードマスタ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-036 |
| **テーブル名** | MST_SkillGrade |
| **論理名** | スキルグレードマスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
スキルグレードマスタテーブル（MST_SkillGrade）は、スキル評価の段階的なレベルを管理します。各グレードには明確な評価基準と要件が定義され、統一的なスキル評価体系を提供します。職種やテナントに応じたカスタマイズも可能です。

### 2.2 関連API
- [API-032](../../api/specs/API仕様書_API-032_スキルグレード管理API.md) - スキルグレード管理API

### 2.3 関連バッチ
- [BATCH-022](../../batch/specs/バッチ定義書_BATCH-022_スキルグレード同期バッチ.md) - スキルグレード同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | grade_id | グレードID | VARCHAR | 20 | × | ○ | - | - | スキルグレードを一意に識別するID |
| 2 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | テナント固有グレードの場合のテナントID |
| 3 | grade_code | グレードコード | VARCHAR | 20 | × | - | - | - | スキルグレードのコード |
| 4 | grade_name | グレード名 | VARCHAR | 100 | × | - | - | - | スキルグレードの名称 |
| 5 | grade_name_en | グレード名（英語） | VARCHAR | 100 | ○ | - | - | NULL | グレード名の英語表記 |
| 6 | grade_level | グレードレベル | INTEGER | - | × | - | - | 1 | グレードの数値レベル（1-10） |
| 7 | grade_type | グレード種別 | VARCHAR | 20 | × | - | - | 'STANDARD' | グレードの種別（STANDARD/TECHNICAL/BUSINESS等） |
| 8 | description | 説明 | TEXT | - | ○ | - | - | NULL | グレードの詳細説明 |
| 9 | evaluation_criteria | 評価基準 | TEXT | - | × | - | - | - | グレード判定の具体的基準 |
| 10 | required_skills | 必要スキル | TEXT | - | ○ | - | - | NULL | グレード達成に必要なスキル |
| 11 | required_experience | 必要経験 | TEXT | - | ○ | - | - | NULL | グレード達成に必要な経験 |
| 12 | required_certifications | 必要資格 | TEXT | - | ○ | - | - | NULL | グレード達成に必要な資格 |
| 13 | min_experience_years | 最小経験年数 | INTEGER | - | ○ | - | - | NULL | グレード達成に必要な最小経験年数 |
| 14 | min_project_count | 最小プロジェクト数 | INTEGER | - | ○ | - | - | NULL | グレード達成に必要な最小プロジェクト数 |
| 15 | assessment_method | 評価方法 | VARCHAR | 50 | × | - | - | 'SELF_ASSESSMENT' | 評価方法（SELF_ASSESSMENT/PEER_REVIEW/MANAGER_REVIEW等） |
| 16 | color_code | カラーコード | VARCHAR | 7 | ○ | - | - | NULL | グレードの表示色（#RRGGBB形式） |
| 17 | icon_url | アイコンURL | VARCHAR | 500 | ○ | - | - | NULL | グレードのアイコン画像URL |
| 18 | badge_url | バッジURL | VARCHAR | 500 | ○ | - | - | NULL | グレードバッジ画像URL |
| 19 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | グレード一覧での表示順序 |
| 20 | is_system_grade | システムグレードフラグ | BOOLEAN | - | × | - | - | FALSE | システム標準グレードかどうか |
| 21 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | グレードが有効かどうか |
| 22 | effective_date | 有効開始日 | DATE | - | × | - | - | - | グレードの有効開始日 |
| 23 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | グレードの有効終了日 |
| 24 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 25 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 26 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 27 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | grade_id | 主キー |
| idx_grade_code | UNIQUE | grade_code | グレードコードの一意性を保証 |
| idx_tenant_grade | INDEX | tenant_id, grade_code | テナント内グレードコード検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_grade_level | INDEX | grade_level | グレードレベル検索用 |
| idx_grade_type | INDEX | grade_type | グレード種別検索用 |
| idx_system | INDEX | is_system_grade | システムグレード検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |
| idx_assessment | INDEX | assessment_method | 評価方法検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_grade | PRIMARY KEY | grade_id | 主キー制約 |
| uq_grade_code | UNIQUE | grade_code | グレードコードの一意性を保証 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_grade_level | CHECK | grade_level | grade_level >= 1 AND grade_level <= 10 |
| chk_grade_type | CHECK | grade_type | grade_type IN ('STANDARD', 'TECHNICAL', 'BUSINESS', 'LEADERSHIP', 'SPECIALIST') |
| chk_assessment_method | CHECK | assessment_method | assessment_method IN ('SELF_ASSESSMENT', 'PEER_REVIEW', 'MANAGER_REVIEW', 'EXPERT_REVIEW', 'CERTIFICATION') |
| chk_color_code | CHECK | color_code | color_code IS NULL OR color_code REGEXP '^#[0-9A-Fa-f]{6}$' |
| chk_min_experience_years | CHECK | min_experience_years | min_experience_years IS NULL OR min_experience_years >= 0 |
| chk_min_project_count | CHECK | min_project_count | min_project_count IS NULL OR min_project_count >= 0 |
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
| TRN_SkillRecord | grade_id | 1:N | スキル評価記録 |
| MST_SkillGradeRequirement | grade_id | 1:N | スキルグレード要件 |
| MST_JobTypeSkillGrade | grade_id | 1:N | 職種スキルグレード関連 |

## 5. データ仕様

### 5.1 データ例
```sql
-- システム標準グレード（初級）
INSERT INTO MST_SkillGrade (
    grade_id, grade_code, grade_name, grade_name_en, grade_level,
    grade_type, description, evaluation_criteria, required_experience,
    min_experience_years, assessment_method, color_code,
    is_system_grade, effective_date, created_by, updated_by
) VALUES (
    'GRADE_001', 'BEGINNER', '初級', 'Beginner', 1,
    'STANDARD', '基本的なスキルレベル',
    '基本的な知識を有し、指導の下で業務を遂行できる',
    '基本的な業務経験、研修受講',
    0, 'SELF_ASSESSMENT', '#4CAF50',
    TRUE, '2025-04-01', 'system', 'system'
);

-- システム標準グレード（中級）
INSERT INTO MST_SkillGrade (
    grade_id, grade_code, grade_name, grade_name_en, grade_level,
    grade_type, description, evaluation_criteria, required_experience,
    min_experience_years, min_project_count, assessment_method, color_code,
    is_system_grade, effective_date, created_by, updated_by
) VALUES (
    'GRADE_002', 'INTERMEDIATE', '中級', 'Intermediate', 3,
    'STANDARD', '実務レベルのスキル',
    '独立して業務を遂行でき、他者への指導も可能',
    '実務経験、プロジェクト参加実績',
    2, 3, 'MANAGER_REVIEW', '#FF9800',
    TRUE, '2025-04-01', 'system', 'system'
);

-- 技術専門グレード
INSERT INTO MST_SkillGrade (
    grade_id, grade_code, grade_name, grade_name_en, grade_level,
    grade_type, description, evaluation_criteria, required_certifications,
    min_experience_years, assessment_method, color_code,
    is_system_grade, effective_date, created_by, updated_by
) VALUES (
    'GRADE_003', 'TECH_EXPERT', '技術エキスパート', 'Technical Expert', 7,
    'TECHNICAL', '技術分野の専門家レベル',
    '高度な技術知識を有し、技術的な課題解決をリードできる',
    '関連技術資格、専門認定',
    5, 'EXPERT_REVIEW', '#2196F3',
    TRUE, '2025-04-01', 'system', 'system'
);

-- テナント固有グレード
INSERT INTO MST_SkillGrade (
    grade_id, tenant_id, grade_code, grade_name, grade_level,
    grade_type, description, evaluation_criteria,
    is_system_grade, effective_date, created_by, updated_by
) VALUES (
    'GRADE_T001', 'TENANT_001', 'CUSTOM_SENIOR', 'カスタムシニア', 5,
    'BUSINESS', 'テナント固有のシニアレベル',
    '社内基準に基づくシニアレベルの評価',
    FALSE, '2025-04-01', 'admin_001', 'admin_001'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 50件 | システム標準グレード |
| 年間増加件数 | 10件 | カスタムグレード追加 |
| 5年後想定件数 | 100件 | 想定値 |

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
| SELECT | 高 | is_active, grade_type | 有効グレード取得 |
| SELECT | 高 | grade_level | グレードレベル検索 |
| SELECT | 中 | tenant_id | テナント固有グレード取得 |
| SELECT | 中 | assessment_method | 評価方法別検索 |
| UPDATE | 低 | grade_id | グレード情報更新 |
| INSERT | 低 | - | 新規グレード作成 |

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
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（評価体系）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存スキル管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_SkillGrade (
    grade_id VARCHAR(20) NOT NULL COMMENT 'グレードID',
    tenant_id VARCHAR(50) NULL COMMENT 'テナントID',
    grade_code VARCHAR(20) NOT NULL COMMENT 'グレードコード',
    grade_name VARCHAR(100) NOT NULL COMMENT 'グレード名',
    grade_name_en VARCHAR(100) NULL COMMENT 'グレード名（英語）',
    grade_level INTEGER NOT NULL DEFAULT 1 COMMENT 'グレードレベル',
    grade_type VARCHAR(20) NOT NULL DEFAULT 'STANDARD' COMMENT 'グレード種別',
    description TEXT NULL COMMENT '説明',
    evaluation_criteria TEXT NOT NULL COMMENT '評価基準',
    required_skills TEXT NULL COMMENT '必要スキル',
    required_experience TEXT NULL COMMENT '必要経験',
    required_certifications TEXT NULL COMMENT '必要資格',
    min_experience_years INTEGER NULL COMMENT '最小経験年数',
    min_project_count INTEGER NULL COMMENT '最小プロジェクト数',
    assessment_method VARCHAR(50) NOT NULL DEFAULT 'SELF_ASSESSMENT' COMMENT '評価方法',
    color_code VARCHAR(7) NULL COMMENT 'カラーコード',
    icon_url VARCHAR(500) NULL COMMENT 'アイコンURL',
    badge_url VARCHAR(500) NULL COMMENT 'バッジURL',
    sort_order INTEGER NOT NULL DEFAULT 0 COMMENT '表示順序',
    is_system_grade BOOLEAN NOT NULL DEFAULT FALSE COMMENT 'システムグレードフラグ',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    effective_date DATE NOT NULL COMMENT '有効開始日',
    expiry_date DATE NULL COMMENT '有効終了日',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (grade_id),
    UNIQUE KEY idx_grade_code (grade_code),
    INDEX idx_tenant_grade (tenant_id, grade_code),
    INDEX idx_tenant (tenant_id),
    INDEX idx_grade_level (grade_level),
    INDEX idx_grade_type (grade_type),
    INDEX idx_system (is_system_grade),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    INDEX idx_assessment (assessment_method),
    CONSTRAINT fk_skill_grade_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_grade_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_grade_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_grade_level CHECK (grade_level >= 1 AND grade_level <= 10),
    CONSTRAINT chk_skill_grade_type CHECK (grade_type IN ('STANDARD', 'TECHNICAL', 'BUSINESS', 'LEADERSHIP', 'SPECIALIST')),
    CONSTRAINT chk_skill_grade_assessment CHECK (assessment_method IN ('SELF_ASSESSMENT', 'PEER_REVIEW', 'MANAGER_REVIEW', 'EXPERT_REVIEW', 'CERTIFICATION')),
    CONSTRAINT chk_skill_grade_color_code CHECK (color_code IS NULL OR color_code REGEXP '^#[0-9A-Fa-f]{6}$'),
    CONSTRAINT chk_skill_grade_min_experience CHECK (min_experience_years IS NULL OR min_experience_years >= 0),
    CONSTRAINT chk_skill_grade_min_project CHECK (min_project_count IS NULL OR min_project_count >= 0),
    CONSTRAINT chk_skill_grade_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='スキルグレードマスタ';
```

## 10. 特記事項

1. **10段階グレードレベル**
   - 1-10の数値レベルで細かな段階評価を実現
   - 柔軟なグレード体系の構築が可能

2. **多様なグレード種別**
   - STANDARD（標準）、TECHNICAL（技術）、BUSINESS（ビジネス）、LEADERSHIP（リーダーシップ）、SPECIALIST（専門）
   - 分野別の専門的なグレード体系を支援

3. **多様な評価方法**
   - 自己評価、ピアレビュー、上司評価、専門家評価、資格認定
   - 評価の客観性と信頼性を確保

4. **視覚的なグレード表現**
   - カラーコード、アイコン、バッジによる視覚的表現
   - モチベーション向上とわかりやすい表示

5. **定量的な要件定義**
   - 最小経験年数、最小プロジェクト数による明確な基準
   - 客観的なグレード判定を支援

6. **マルチテナント対応**
   - システム標準グレードとテナント固有グレードの混在管理
   - tenant_idがNULLの場合はシステム標準グレード

7. **論理削除による履歴管理**
   - グレード廃止時は論理削除（is_active=FALSE）を使用
   - 有効期間によりグレード変更履歴を管理

8. **システム標準グレードの保護**
   - システム標準グレード（is_system_grade=TRUE）は削除不可
   - テナント管理者による誤削除を防止

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-06-01 | システムアーキテクト | 新フォーマットで初版作成 |
