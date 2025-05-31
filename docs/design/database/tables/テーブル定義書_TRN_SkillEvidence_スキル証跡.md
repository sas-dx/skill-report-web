# テーブル定義書：スキル証跡 (TRN_SkillEvidence)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-012 |
| **テーブル名** | TRN_SkillEvidence |
| **論理名** | スキル証跡 |
| **カテゴリ** | トランザクション系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
スキル証跡テーブル（TRN_SkillEvidence）は、スキル評価の根拠となる証跡情報を管理します。ファイル、URL、テキスト等の多様な形式の証跡を保存し、スキル評価の客観性と透明性を確保します。

### 2.2 関連API
- [API-012](../api/specs/API仕様書_API-012.md) - スキル証跡管理API
- [API-013](../api/specs/API仕様書_API-013.md) - ファイルアップロードAPI

### 2.3 関連バッチ
- [BATCH-011](../batch/specs/バッチ定義書_BATCH-011.md) - 証跡ファイルクリーンアップバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | evidence_id | 証跡ID | VARCHAR | 20 | × | ○ | - | - | スキル証跡を一意に識別するID |
| 2 | record_id | 記録ID | VARCHAR | 20 | × | - | ○ | - | 関連するスキル評価記録のID |
| 3 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 証跡提出者の社員ID |
| 4 | skill_id | スキルID | VARCHAR | 20 | × | - | ○ | - | 証跡対象のスキル項目ID |
| 5 | evidence_type | 証跡タイプ | VARCHAR | 20 | × | - | - | - | 証跡の種類（FILE/URL/TEXT/CERTIFICATION） |
| 6 | evidence_title | 証跡タイトル | VARCHAR | 200 | × | - | - | - | 証跡の名称・タイトル |
| 7 | evidence_description | 証跡説明 | TEXT | - | ○ | - | - | NULL | 証跡の詳細説明 |
| 8 | file_path | ファイルパス | VARCHAR | 500 | ○ | - | - | NULL | ファイル証跡の保存パス |
| 9 | file_name | ファイル名 | VARCHAR | 255 | ○ | - | - | NULL | 元のファイル名 |
| 10 | file_size | ファイルサイズ | BIGINT | - | ○ | - | - | NULL | ファイルサイズ（バイト） |
| 11 | file_type | ファイルタイプ | VARCHAR | 100 | ○ | - | - | NULL | ファイルのMIMEタイプ |
| 12 | url | URL | VARCHAR | 1000 | ○ | - | - | NULL | URL証跡のリンク先 |
| 13 | text_content | テキスト内容 | TEXT | - | ○ | - | - | NULL | テキスト証跡の内容 |
| 14 | certification_name | 資格名 | VARCHAR | 200 | ○ | - | - | NULL | 資格証跡の資格名 |
| 15 | certification_number | 資格番号 | VARCHAR | 100 | ○ | - | - | NULL | 資格の認定番号 |
| 16 | certification_date | 取得日 | DATE | - | ○ | - | - | NULL | 資格取得日 |
| 17 | certification_expiry | 有効期限 | DATE | - | ○ | - | - | NULL | 資格の有効期限 |
| 18 | evaluation_level | 評価レベル | INTEGER | - | ○ | - | - | NULL | この証跡が示すスキルレベル（1-4） |
| 19 | submission_date | 提出日 | DATE | - | × | - | - | - | 証跡提出日 |
| 20 | verification_status | 検証ステータス | VARCHAR | 20 | × | - | - | 'PENDING' | 証跡の検証状況 |
| 21 | verified_by | 検証者ID | VARCHAR | 20 | ○ | - | ○ | NULL | 証跡を検証した社員ID |
| 22 | verification_date | 検証日 | DATE | - | ○ | - | - | NULL | 証跡検証日 |
| 23 | verification_comment | 検証コメント | TEXT | - | ○ | - | - | NULL | 検証者のコメント |
| 24 | access_count | アクセス回数 | INTEGER | - | × | - | - | 0 | 証跡の閲覧回数 |
| 25 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 26 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 証跡が有効かどうか |
| 27 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 28 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 29 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 30 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | evidence_id | 主キー |
| idx_record | INDEX | record_id | 評価記録検索用 |
| idx_employee | INDEX | employee_id | 社員検索用 |
| idx_skill | INDEX | skill_id | スキル検索用 |
| idx_type | INDEX | evidence_type | 証跡タイプ検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_status | INDEX | verification_status | 検証ステータス検索用 |
| idx_submission | INDEX | submission_date | 提出日検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_skill_evidence | PRIMARY KEY | evidence_id | 主キー制約 |
| fk_record | FOREIGN KEY | record_id | TRN_SkillRecord.record_id |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_skill | FOREIGN KEY | skill_id | MST_SkillItem.skill_id |
| fk_verified_by | FOREIGN KEY | verified_by | MST_Employee.employee_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_evidence_type | CHECK | evidence_type | evidence_type IN ('FILE', 'URL', 'TEXT', 'CERTIFICATION') |
| chk_evaluation_level | CHECK | evaluation_level | evaluation_level IS NULL OR (evaluation_level >= 1 AND evaluation_level <= 4) |
| chk_verification_status | CHECK | verification_status | verification_status IN ('PENDING', 'APPROVED', 'REJECTED', 'EXPIRED') |
| chk_file_size | CHECK | file_size | file_size IS NULL OR file_size > 0 |
| chk_access_count | CHECK | access_count | access_count >= 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_SkillRecord | record_id | 1:N | スキル評価記録 |
| MST_Employee | employee_id | 1:N | 証跡提出者 |
| MST_SkillItem | skill_id | 1:N | 対象スキル |
| MST_Employee | verified_by | 1:N | 検証者 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | なし |

## 5. データ仕様

### 5.1 データ例
```sql
-- ファイル証跡
INSERT INTO TRN_SkillEvidence (
    evidence_id, record_id, employee_id, skill_id,
    evidence_type, evidence_title, evidence_description,
    file_path, file_name, file_size, file_type,
    evaluation_level, submission_date, verification_status,
    tenant_id, created_by, updated_by
) VALUES (
    'EVD_001',
    'REC_001',
    'EMP_001',
    'SKILL_001',
    'FILE',
    'Javaアプリケーション開発プロジェクト',
    'Spring Bootを使用したWebアプリケーションの設計書と実装コード',
    '/evidence/2024/03/java_project_emp001.zip',
    'java_project.zip',
    2048576,
    'application/zip',
    3,
    '2024-03-25',
    'APPROVED',
    'TENANT_001',
    'system',
    'system'
);

-- 資格証跡
INSERT INTO TRN_SkillEvidence (
    evidence_id, record_id, employee_id, skill_id,
    evidence_type, evidence_title, certification_name,
    certification_number, certification_date,
    evaluation_level, submission_date, verification_status,
    tenant_id, created_by, updated_by
) VALUES (
    'EVD_002',
    'REC_001',
    'EMP_001',
    'SKILL_001',
    'CERTIFICATION',
    'Oracle Java SE 11 認定資格',
    'Oracle Certified Professional, Java SE 11 Developer',
    '1Z0-819-12345',
    '2024-02-15',
    4,
    '2024-03-20',
    'APPROVED',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 0件 | 新規システム |
| 月間増加件数 | 100,000件 | 評価記録×証跡数 |
| 年間増加件数 | 1,200,000件 | 想定値 |
| 5年後想定件数 | 6,000,000件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行
- ファイル証跡：別途ファイルシステムバックアップ

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：submission_date（月単位）

### 6.3 アーカイブ
- アーカイブ条件：提出日から5年経過
- アーカイブ先：アーカイブDB + ファイルストレージ

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | record_id | 評価記録別証跡取得 |
| SELECT | 高 | employee_id, skill_id | 社員・スキル別証跡取得 |
| SELECT | 中 | verification_status | 検証待ち証跡取得 |
| SELECT | 中 | evidence_type | タイプ別証跡取得 |
| UPDATE | 中 | evidence_id | 証跡更新・検証 |
| INSERT | 中 | - | 新規証跡登録 |

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
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | ○ | ○ | × | 管理職（部下のみ） |
| employee | ○ | ○ | ○ | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（証跡情報）
- 機密情報：含む（スキル証跡）
- 暗号化：必要（ファイル、テキスト内容）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存ファイルサーバー
- 移行方法：ファイル移行 + メタデータCSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE TRN_SkillEvidence (
    evidence_id VARCHAR(20) NOT NULL,
    record_id VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    skill_id VARCHAR(20) NOT NULL,
    evidence_type VARCHAR(20) NOT NULL,
    evidence_title VARCHAR(200) NOT NULL,
    evidence_description TEXT NULL,
    file_path VARCHAR(500) NULL,
    file_name VARCHAR(255) NULL,
    file_size BIGINT NULL,
    file_type VARCHAR(100) NULL,
    url VARCHAR(1000) NULL,
    text_content TEXT NULL,
    certification_name VARCHAR(200) NULL,
    certification_number VARCHAR(100) NULL,
    certification_date DATE NULL,
    certification_expiry DATE NULL,
    evaluation_level INTEGER NULL,
    submission_date DATE NOT NULL,
    verification_status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    verified_by VARCHAR(20) NULL,
    verification_date DATE NULL,
    verification_comment TEXT NULL,
    access_count INTEGER NOT NULL DEFAULT 0,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (evidence_id),
    INDEX idx_record (record_id),
    INDEX idx_employee (employee_id),
    INDEX idx_skill (skill_id),
    INDEX idx_type (evidence_type),
    INDEX idx_tenant (tenant_id),
    INDEX idx_status (verification_status),
    INDEX idx_submission (submission_date),
    INDEX idx_active (is_active),
    CONSTRAINT fk_skill_evidence_record FOREIGN KEY (record_id) REFERENCES TRN_SkillRecord(record_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_evidence_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_evidence_skill FOREIGN KEY (skill_id) REFERENCES MST_SkillItem(skill_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_evidence_verified_by FOREIGN KEY (verified_by) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_skill_evidence_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_skill_evidence_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_skill_evidence_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_skill_evidence_type CHECK (evidence_type IN ('FILE', 'URL', 'TEXT', 'CERTIFICATION')),
    CONSTRAINT chk_skill_evidence_evaluation_level CHECK (evaluation_level IS NULL OR (evaluation_level >= 1 AND evaluation_level <= 4)),
    CONSTRAINT chk_skill_evidence_verification_status CHECK (verification_status IN ('PENDING', 'APPROVED', 'REJECTED', 'EXPIRED')),
    CONSTRAINT chk_skill_evidence_file_size CHECK (file_size IS NULL OR file_size > 0),
    CONSTRAINT chk_skill_evidence_access_count CHECK (access_count >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(submission_date)) (
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p2026 VALUES LESS THAN (2027),
    PARTITION p2027 VALUES LESS THAN (2028),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. 多様な証跡タイプ（ファイル/URL/テキスト/資格）に対応
2. ファイル証跡は暗号化して保存し、アクセス制御を実装
3. 証跡検証ワークフローによる品質確保
4. 資格証跡は有効期限管理により最新性を保証
5. アクセス回数によりよく参照される証跡を把握
6. パーティション設計による大量データの効率的管理
7. 証跡廃止時は論理削除（is_active=FALSE）を使用
8. ファイルサイズ制限とウイルススキャンを実装
9. 証跡の改ざん防止のためハッシュ値管理を検討
10. 定期的な証跡ファイルクリーンアップバッチで容量管理

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、詳細情報追加 |
