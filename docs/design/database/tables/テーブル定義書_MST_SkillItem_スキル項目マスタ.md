# テーブル定義書：スキル項目マスタ (MST_SkillItem)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-010 |
| **テーブル名** | MST_SkillItem |
| **論理名** | スキル項目マスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
スキル項目マスタテーブル（MST_SkillItem）は、具体的なスキル項目を管理します。スキルカテゴリの最下層に位置し、実際の評価対象となるスキル項目を定義します。4段階評価（×/△/○/◎）の基準と証跡要件を含み、統一的なスキル評価を支援します。

### 2.2 関連API
- [API-007](../api/specs/API仕様書_API-007.md) - スキル管理API
- [API-009](../api/specs/API仕様書_API-009.md) - スキル項目管理API

### 2.3 関連バッチ
- [BATCH-008](../batch/specs/バッチ定義書_BATCH-008.md) - スキルマスタ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | skill_id | スキルID | VARCHAR | 20 | × | ○ | - | - | スキル項目を一意に識別するID |
| 2 | skill_code | スキルコード | VARCHAR | 20 | × | - | - | - | スキル項目のコード |
| 3 | skill_name | スキル名 | VARCHAR | 100 | × | - | - | - | スキル項目の名称 |
| 4 | skill_name_en | スキル名（英語） | VARCHAR | 100 | ○ | - | - | NULL | スキル名の英語表記 |
| 5 | category_id | カテゴリID | VARCHAR | 20 | × | - | ○ | - | 所属するスキルカテゴリのID |
| 6 | skill_type | スキルタイプ | VARCHAR | 20 | × | - | - | 'TECHNICAL' | スキルの種類（技術/業務/ヒューマン等） |
| 7 | difficulty_level | 難易度レベル | INTEGER | - | × | - | - | 1 | スキルの難易度（1:初級、2:中級、3:上級、4:エキスパート） |
| 8 | description | 説明 | TEXT | - | ○ | - | - | NULL | スキル項目の詳細説明 |
| 9 | evaluation_level_1 | 評価レベル1基準 | TEXT | - | ○ | - | - | NULL | ×（未習得）の評価基準 |
| 10 | evaluation_level_2 | 評価レベル2基準 | TEXT | - | ○ | - | - | NULL | △（基礎）の評価基準 |
| 11 | evaluation_level_3 | 評価レベル3基準 | TEXT | - | ○ | - | - | NULL | ○（応用）の評価基準 |
| 12 | evaluation_level_4 | 評価レベル4基準 | TEXT | - | ○ | - | - | NULL | ◎（エキスパート）の評価基準 |
| 13 | required_evidence_1 | 必要証跡1 | TEXT | - | ○ | - | - | NULL | レベル1の必要証跡 |
| 14 | required_evidence_2 | 必要証跡2 | TEXT | - | ○ | - | - | NULL | レベル2の必要証跡 |
| 15 | required_evidence_3 | 必要証跡3 | TEXT | - | ○ | - | - | NULL | レベル3の必要証跡 |
| 16 | required_evidence_4 | 必要証跡4 | TEXT | - | ○ | - | - | NULL | レベル4の必要証跡 |
| 17 | related_skills | 関連スキル | TEXT | - | ○ | - | - | NULL | 関連するスキル項目のリスト |
| 18 | prerequisite_skills | 前提スキル | TEXT | - | ○ | - | - | NULL | 習得に必要な前提スキル |
| 19 | learning_resources | 学習リソース | TEXT | - | ○ | - | - | NULL | 推奨学習リソース・教材 |
| 20 | certification_info | 資格情報 | TEXT | - | ○ | - | - | NULL | 関連する資格・認定情報 |
| 21 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | カテゴリ内での表示順序 |
| 22 | is_system_skill | システムスキルフラグ | BOOLEAN | - | × | - | - | FALSE | システム標準スキルかどうか |
| 23 | tenant_id | テナントID | VARCHAR | 50 | ○ | - | ○ | NULL | テナント固有スキルの場合のテナントID |
| 24 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | スキル項目が有効かどうか |
| 25 | effective_date | 有効開始日 | DATE | - | × | - | - | - | スキル項目の有効開始日 |
| 26 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | スキル項目の有効終了日 |
| 27 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 28 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 29 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 30 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | skill_id | 主キー |
| idx_skill_code | UNIQUE | skill_code | スキルコードの一意性を保証 |
| idx_category | INDEX | category_id | カテゴリ検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_type | INDEX | skill_type | スキルタイプ検索用 |
| idx_difficulty | INDEX | difficulty_level | 難易度検索用 |
| idx_system | INDEX | is_system_skill | システムスキル検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_item | PRIMARY KEY | skill_id | 主キー制約 |
| uq_skill_code | UNIQUE | skill_code | スキルコードの一意性を保証 |
| fk_category | FOREIGN KEY | category_id | MST_SkillCategory.category_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_skill_type | CHECK | skill_type | skill_type IN ('TECHNICAL', 'BUSINESS', 'HUMAN', 'MANAGEMENT', 'LANGUAGE', 'CERTIFICATION') |
| chk_difficulty_level | CHECK | difficulty_level | difficulty_level >= 1 AND difficulty_level <= 4 |
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
| TRN_SkillRecord | skill_id | 1:N | スキル評価記録 |
| TRN_SkillEvidence | skill_id | 1:N | スキル証跡 |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_SkillItem (
    skill_id, skill_code, skill_name, category_id,
    skill_type, difficulty_level, description,
    evaluation_level_2, evaluation_level_3, evaluation_level_4,
    required_evidence_2, required_evidence_3, required_evidence_4,
    is_system_skill, effective_date, created_by, updated_by
) VALUES (
    'SKILL_001',
    'JAVA_BASIC',
    'Java基礎',
    'CAT_002',
    'TECHNICAL',
    2,
    'Javaプログラミングの基礎的なスキル',
    '基本的な文法を理解し、簡単なプログラムが作成できる',
    'オブジェクト指向を理解し、実用的なアプリケーションが開発できる',
    'フレームワークを活用し、大規模システムの設計・開発ができる',
    '基礎文法の理解を示すコード例',
    '実用的なアプリケーションのソースコード',
    '大規模システムでの設計書・実装例',
    TRUE,
    '2023-04-01',
    'system',
    'system'
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
| SELECT | 高 | category_id, is_active | カテゴリ別有効スキル取得 |
| SELECT | 高 | skill_type | スキルタイプ別取得 |
| SELECT | 中 | difficulty_level | 難易度別取得 |
| SELECT | 中 | tenant_id | テナント固有スキル取得 |
| UPDATE | 低 | skill_id | スキル項目更新 |
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
| skill_admin | ○ | ○ | ○ | × | スキル管理者 |
| manager | ○ | ○ | ○ | × | 管理職（テナント内のみ） |
| employee | ○ | × | × | × | 一般社員 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含む（スキル評価基準）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存スキル管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE MST_SkillItem (
    skill_id VARCHAR(20) NOT NULL,
    skill_code VARCHAR(20) NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    skill_name_en VARCHAR(100) NULL,
    category_id VARCHAR(20) NOT NULL,
    skill_type VARCHAR(20) NOT NULL DEFAULT 'TECHNICAL',
    difficulty_level INTEGER NOT NULL DEFAULT 1,
    description TEXT NULL,
    evaluation_level_1 TEXT NULL,
    evaluation_level_2 TEXT NULL,
    evaluation_level_3 TEXT NULL,
    evaluation_level_4 TEXT NULL,
    required_evidence_1 TEXT NULL,
    required_evidence_2 TEXT NULL,
    required_evidence_3 TEXT NULL,
    required_evidence_4 TEXT NULL,
    related_skills TEXT NULL,
    prerequisite_skills TEXT NULL,
    learning_resources TEXT NULL,
    certification_info TEXT NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_system_skill BOOLEAN NOT NULL DEFAULT FALSE,
    tenant_id VARCHAR(50) NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    effective_date DATE NOT NULL,
    expiry_date DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (skill_id),
    UNIQUE KEY idx_skill_code (skill_code),
    INDEX idx_category (category_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_type (skill_type),
    INDEX idx_difficulty (difficulty_level),
    INDEX idx_system (is_system_skill),
    INDEX idx_active (is_active),
    INDEX idx_effective (effective_date, expiry_date),
    CONSTRAINT fk_skill_item_category FOREIGN KEY (category_id) REFERENCES MST_SkillCategory(category_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_item_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_item_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_item_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_item_type CHECK (skill_type IN ('TECHNICAL', 'BUSINESS', 'HUMAN', 'MANAGEMENT', 'LANGUAGE', 'CERTIFICATION')),
    CONSTRAINT chk_skill_item_difficulty_level CHECK (difficulty_level >= 1 AND difficulty_level <= 4),
    CONSTRAINT chk_skill_item_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. 4段階評価（×/△/○/◎）の詳細な評価基準を定義
2. 各評価レベルに対応する必要証跡を明確化
3. スキルタイプにより技術・業務・ヒューマンスキル等を分類
4. 難易度レベルにより学習の段階的進行を支援
5. 関連スキル・前提スキルにより学習パスを提示
6. 学習リソース・資格情報により自己学習を支援
7. システム標準スキルとテナント固有スキルの混在管理
8. スキル廃止時は論理削除（is_active=FALSE）を使用
9. 有効期間によりスキル項目変更履歴を管理
10. システム標準スキルは削除不可

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
