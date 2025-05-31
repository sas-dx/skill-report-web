# テーブル定義書：資格情報 (MST_Certification)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-011 |
| **テーブル名** | MST_Certification |
| **論理名** | 資格情報 |
| **カテゴリ** | マスタ系 |
| **優先度** | 高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
資格情報テーブル（MST_Certification）は、システムで管理する資格の基本情報と、社員が取得した資格の詳細情報を管理するマスタテーブルです。資格名、発行機関、有効期限、取得日などの情報を保持し、社員のスキルプロファイルを補完する客観的な指標として活用されます。また、有効期限のある資格については、期限切れ前のアラート通知の基盤となります。

### 2.2 関連API
- [API-009](../api/specs/API仕様書_API-009.md) - 資格情報管理API
- [API-010](../api/specs/API仕様書_API-010.md) - 資格検索API

### 2.3 関連バッチ
- [BATCH-007](../batch/specs/バッチ定義書_BATCH-007.md) - 資格期限アラートバッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | cert_id | 資格ID | VARCHAR | 50 | × | ○ | - | - | 資格情報を一意に識別するID |
| 2 | employee_id | 社員ID | VARCHAR | 20 | × | - | ○ | - | 資格取得者の社員ID |
| 3 | cert_master_id | 資格マスタID | VARCHAR | 50 | ○ | - | - | NULL | 資格マスタの参照ID（NULL=自由入力資格） |
| 4 | cert_name | 資格名 | VARCHAR | 200 | × | - | - | - | 資格の正式名称 |
| 5 | cert_name_en | 資格英名 | VARCHAR | 200 | ○ | - | - | NULL | 資格の英語名称 |
| 6 | issuing_org | 発行機関 | VARCHAR | 100 | ○ | - | - | NULL | 資格の発行機関 |
| 7 | acquisition_date | 取得日 | DATE | - | × | - | - | - | 資格の取得日 |
| 8 | expiry_date | 有効期限 | DATE | - | ○ | - | - | NULL | 資格の有効期限（NULL=無期限） |
| 9 | certification_no | 認定番号 | VARCHAR | 50 | ○ | - | - | NULL | 資格の認定番号 |
| 10 | score | スコア・評価 | VARCHAR | 50 | ○ | - | - | NULL | 取得時のスコアや評価（点数・級など） |
| 11 | requires_renewal | 更新必要フラグ | BOOLEAN | - | × | - | - | FALSE | 定期的な更新が必要かどうか |
| 12 | renewal_interval | 更新間隔（月） | INTEGER | - | ○ | - | - | NULL | 更新が必要な場合の間隔（月数） |
| 13 | next_renewal_date | 次回更新日 | DATE | - | ○ | - | - | NULL | 次回の更新予定日 |
| 14 | related_skill_id | 関連スキルID | VARCHAR | 50 | ○ | - | ○ | NULL | 関連するスキルID |
| 15 | pdu_points | PDUポイント | INTEGER | - | ○ | - | - | NULL | 取得により付与されるPDUポイント |
| 16 | remarks | 備考 | TEXT | - | ○ | - | - | NULL | 備考欄 |
| 17 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 18 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 資格情報が有効かどうか |
| 19 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 20 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 21 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 22 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | cert_id | 主キー |
| idx_employee | INDEX | employee_id | 社員による検索用 |
| idx_cert_master | INDEX | cert_master_id | 資格マスタによる検索用 |
| idx_cert_name | INDEX | cert_name | 資格名による検索用 |
| idx_expiry_date | INDEX | expiry_date | 有効期限による検索用 |
| idx_next_renewal | INDEX | next_renewal_date | 次回更新日による検索用 |
| idx_related_skill | INDEX | related_skill_id | 関連スキルによる検索用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグによる検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_certification | PRIMARY KEY | cert_id | 主キー制約 |
| fk_employee | FOREIGN KEY | employee_id | MST_Employee.employee_id |
| fk_related_skill | FOREIGN KEY | related_skill_id | MST_SkillHierarchy.skill_id |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_dates | CHECK | acquisition_date, expiry_date | expiry_date IS NULL OR expiry_date >= acquisition_date |
| chk_renewal_interval | CHECK | renewal_interval | renewal_interval IS NULL OR renewal_interval >= 1 |
| chk_pdu_points | CHECK | pdu_points | pdu_points IS NULL OR pdu_points >= 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | employee_id | 1:N | 資格取得者の社員 |
| MST_SkillHierarchy | related_skill_id | 1:N | 関連するスキル項目 |
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_SkillRecord | cert_id | 1:N | 資格に関連するスキル評価 |
| TRN_PDU | cert_id | 1:N | 資格に関連するPDUポイント |

## 5. データ仕様

### 5.1 資格登録方法
| 方法 | cert_master_id | 説明 |
|------|----------------|------|
| マスタ選択 | 値あり | 事前定義された資格マスタから選択 |
| 自由入力 | NULL | 資格名等を直接入力 |

### 5.2 更新管理
| フラグ | 説明 | 関連カラム |
|--------|------|------------|
| requires_renewal=TRUE | 定期更新必要 | renewal_interval, next_renewal_date |
| requires_renewal=FALSE | 更新不要 | - |

### 5.3 データ例
```sql
-- IT系資格の例
INSERT INTO MST_Certification (
    cert_id, employee_id, cert_name, issuing_org,
    acquisition_date, expiry_date, certification_no,
    requires_renewal, renewal_interval, next_renewal_date,
    related_skill_id, pdu_points, tenant_id, created_by, updated_by
) VALUES (
    'CERT_001',
    'EMP_001',
    '情報処理安全確保支援士',
    'IPA（独立行政法人情報処理推進機構）',
    '2023-04-01',
    '2026-04-01',
    'RISS-2023-001234',
    TRUE,
    36,
    '2026-04-01',
    'SKILL_SEC_001',
    30,
    'TENANT_001',
    'system',
    'system'
);

-- 語学系資格の例
INSERT INTO MST_Certification (
    cert_id, employee_id, cert_name, issuing_org,
    acquisition_date, score, related_skill_id,
    tenant_id, created_by, updated_by
) VALUES (
    'CERT_002',
    'EMP_002',
    'TOEIC Listening & Reading Test',
    'ETS',
    '2023-06-15',
    '850',
    'SKILL_LANG_001',
    'TENANT_001',
    'system',
    'system'
);

-- プロジェクト管理系資格の例
INSERT INTO MST_Certification (
    cert_id, employee_id, cert_name, cert_name_en, issuing_org,
    acquisition_date, expiry_date, certification_no,
    requires_renewal, renewal_interval, next_renewal_date,
    related_skill_id, pdu_points, tenant_id, created_by, updated_by
) VALUES (
    'CERT_003',
    'EMP_003',
    'プロジェクトマネジメント・プロフェッショナル',
    'Project Management Professional (PMP)',
    'PMI',
    '2023-03-20',
    '2026-03-20',
    'PMP-2023-567890',
    TRUE,
    36,
    '2026-03-20',
    'SKILL_PM_001',
    60,
    'TENANT_001',
    'system',
    'system'
);
```

### 5.4 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 2,000件 | 既存社員の資格情報 |
| 年間増加件数 | 500件 | 新規取得・更新 |
| 5年後想定件数 | 4,500件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：RANGE
- パーティション条件：acquisition_date（年単位）

### 6.3 アーカイブ
- アーカイブ条件：論理削除から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | employee_id, is_active | 社員の資格一覧 |
| SELECT | 高 | expiry_date | 期限切れ近い資格 |
| SELECT | 中 | cert_name | 資格名検索 |
| SELECT | 中 | related_skill_id | スキル関連資格 |
| SELECT | 中 | tenant_id | テナント別資格 |
| INSERT | 中 | - | 新規資格登録 |
| UPDATE | 中 | cert_id | 資格情報更新 |

### 7.2 パフォーマンス要件
- SELECT：15ms以内
- INSERT：100ms以内
- UPDATE：100ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | × | × | × | 管理職（部下のみ） |
| employee | ○ | ○ | ○ | × | 一般社員（自分のみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含む（資格取得情報）
- 機密情報：含む（認定番号等）
- 暗号化：必要（認定番号、スコア）

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存資格管理システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存データの移行
INSERT INTO MST_Certification (
    cert_id, employee_id, cert_name, issuing_org,
    acquisition_date, expiry_date, certification_no,
    tenant_id, created_by, updated_by
)
SELECT 
    CONCAT('CERT_', LPAD(ROW_NUMBER() OVER (ORDER BY emp_no, cert_date), 6, '0')),
    emp_no,
    cert_name,
    issuer,
    cert_date,
    expire_date,
    cert_no,
    'TENANT_001',
    'migration',
    'migration'
FROM old_certification
WHERE is_valid = 1;
```

### 9.3 DDL
```sql
CREATE TABLE MST_Certification (
    cert_id VARCHAR(50) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    cert_master_id VARCHAR(50) NULL,
    cert_name VARCHAR(200) NOT NULL,
    cert_name_en VARCHAR(200) NULL,
    issuing_org VARCHAR(100) NULL,
    acquisition_date DATE NOT NULL,
    expiry_date DATE NULL,
    certification_no VARCHAR(50) NULL,
    score VARCHAR(50) NULL,
    requires_renewal BOOLEAN NOT NULL DEFAULT FALSE,
    renewal_interval INTEGER NULL,
    next_renewal_date DATE NULL,
    related_skill_id VARCHAR(50) NULL,
    pdu_points INTEGER NULL,
    remarks TEXT NULL,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (cert_id),
    INDEX idx_employee (employee_id),
    INDEX idx_cert_master (cert_master_id),
    INDEX idx_cert_name (cert_name),
    INDEX idx_expiry_date (expiry_date),
    INDEX idx_next_renewal (next_renewal_date),
    INDEX idx_related_skill (related_skill_id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    CONSTRAINT fk_cert_employee FOREIGN KEY (employee_id) REFERENCES MST_Employee(employee_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_cert_skill FOREIGN KEY (related_skill_id) REFERENCES MST_SkillHierarchy(skill_id) ON UPDATE CASCADE ON DELETE SET NULL,
    CONSTRAINT fk_cert_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_cert_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_cert_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_cert_dates CHECK (expiry_date IS NULL OR expiry_date >= acquisition_date),
    CONSTRAINT chk_cert_renewal_interval CHECK (renewal_interval IS NULL OR renewal_interval >= 1),
    CONSTRAINT chk_cert_pdu_points CHECK (pdu_points IS NULL OR pdu_points >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
PARTITION BY RANGE (YEAR(acquisition_date)) (
    PARTITION p2020 VALUES LESS THAN (2021),
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p2025 VALUES LESS THAN (2026),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);
```

## 10. 特記事項

1. **資格登録方式**: マスタ選択と自由入力の2方式をサポート
2. **有効期限管理**: 期限切れ前のアラート通知機能
3. **更新管理**: 定期更新が必要な資格の自動管理
4. **スキル連携**: 関連スキルとの紐付けによる総合評価
5. **PDU連携**: 継続教育ポイントとの連携
6. **多言語対応**: 英語名称の管理
7. **認定番号管理**: 資格の真正性確認
8. **スコア管理**: 点数・級等の評価情報
9. **テナント分離**: マルチテナント対応
10. **履歴管理**: 資格の取得・更新履歴を完全管理
11. **バッチ連携**: 期限アラート等の自動処理
12. **セキュリティ**: 個人情報保護と認定番号の暗号化

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（資格管理機能対応） |
