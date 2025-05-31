# テーブル定義書：MST_JobType（職種マスタ）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-009 |
| **テーブル名** | MST_JobType |
| **論理名** | 職種マスタ |
| **カテゴリ** | マスタ系 |
| **優先度** | 最高 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-29 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
職種マスタテーブル（MST_JobType）は、組織の職種情報を管理します。エンジニア、営業、管理職等の職種別にスキル要件、キャリアパス、評価基準を定義し、人材管理とスキル評価の基盤となります。

### 2.2 関連要求仕様ID
- **HR.1-JOB.1**: 職種管理機能
- **SKL.1-REQ.1**: 職種別スキル要件管理
- **CAR.1-PATH.1**: キャリアパス管理

### 2.3 関連API
- [API-007](../api/specs/API仕様書_API-007_職種管理API.md) - 職種管理API

### 2.4 関連バッチ
- [BATCH-701](../batch/specs/バッチ定義書_BATCH-701_組織・役職マスタ同期バッチ.md) - 組織・役職マスタ同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | tenant_id | テナントID | VARCHAR | 50 | × | ○ | MST_Tenant.tenant_id | - | 所属テナントのID |
| 2 | job_type_id | 職種ID | VARCHAR | 20 | × | ○ | - | - | 職種を一意に識別するID |
| 3 | job_type_code | 職種コード | VARCHAR | 10 | × | - | - | - | 人事システムの職種コード |
| 4 | job_type_name | 職種名 | VARCHAR | 100 | × | - | - | - | 職種の正式名称 |
| 5 | job_type_name_short | 職種名（略称） | VARCHAR | 50 | ○ | - | - | NULL | 職種の略称 |
| 6 | job_type_name_en | 職種名（英語） | VARCHAR | 100 | ○ | - | - | NULL | 職種名の英語表記 |
| 7 | category | 職種カテゴリ | VARCHAR | 50 | × | - | - | 'GENERAL' | 職種の分類（TECHNICAL/SALES/MANAGEMENT/GENERAL） |
| 8 | description | 職種説明 | TEXT | - | ○ | - | - | NULL | 職種の業務内容・説明 |
| 9 | required_skills | 必要スキル一覧 | JSON | - | ○ | - | - | NULL | 職種に必要なスキルのJSON配列 |
| 10 | career_path | キャリアパス情報 | JSON | - | ○ | - | - | NULL | キャリアパス情報のJSON |
| 11 | evaluation_criteria | 評価基準 | JSON | - | ○ | - | - | NULL | 評価基準の配分情報JSON |
| 12 | min_experience_years | 最低経験年数 | INTEGER | - | ○ | - | - | 0 | 職種に必要な最低経験年数 |
| 13 | max_experience_years | 最大経験年数 | INTEGER | - | ○ | - | - | NULL | 職種の最大想定経験年数 |
| 14 | salary_range_min | 給与レンジ下限 | DECIMAL | 10,0 | ○ | - | - | NULL | 給与レンジの下限額 |
| 15 | salary_range_max | 給与レンジ上限 | DECIMAL | 10,0 | ○ | - | - | NULL | 給与レンジの上限額 |
| 16 | sort_order | 表示順序 | INTEGER | - | × | - | - | 0 | 職種一覧での表示順序 |
| 17 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 職種が有効かどうか |
| 18 | effective_date | 有効開始日 | DATE | - | × | - | - | - | 職種の有効開始日 |
| 19 | expiry_date | 有効終了日 | DATE | - | ○ | - | - | NULL | 職種の有効終了日 |
| 20 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 21 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 22 | created_by | 作成者ID | VARCHAR | 50 | × | - | - | - | レコード作成者のユーザーID |
| 23 | updated_by | 更新者ID | VARCHAR | 50 | × | - | - | - | レコード更新者のユーザーID |
| 24 | version | バージョン | INTEGER | - | × | - | - | 1 | 楽観的排他制御用バージョン |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | tenant_id, job_type_id | 主キー（複合キー） |
| idx_job_type_code | UNIQUE | tenant_id, job_type_code | 職種コードの一意性を保証（テナント内） |
| idx_job_type_name | UNIQUE | tenant_id, job_type_name | 職種名の一意性を保証（テナント内） |
| idx_category | INDEX | tenant_id, category | 職種カテゴリ検索用 |
| idx_active | INDEX | tenant_id, is_active | 有効職種検索用 |
| idx_sort_order | INDEX | tenant_id, sort_order | 表示順序検索用 |
| idx_effective | INDEX | effective_date, expiry_date | 有効期間検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_job_type | PRIMARY KEY | tenant_id, job_type_id | 主キー制約（複合キー） |
| uq_job_type_code | UNIQUE | tenant_id, job_type_code | 職種コードの一意性を保証（テナント内） |
| uq_job_type_name | UNIQUE | tenant_id, job_type_name | 職種名の一意性を保証（テナント内） |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | tenant_id, created_by | MST_UserAuth(tenant_id, user_id) |
| fk_updated_by | FOREIGN KEY | tenant_id, updated_by | MST_UserAuth(tenant_id, user_id) |
| chk_category | CHECK | category | category IN ('TECHNICAL', 'SALES', 'MANAGEMENT', 'GENERAL') |
| chk_experience_years | CHECK | min_experience_years, max_experience_years | min_experience_years >= 0 AND (max_experience_years IS NULL OR max_experience_years >= min_experience_years) |
| chk_salary_range | CHECK | salary_range_min, salary_range_max | (salary_range_min IS NULL OR salary_range_min >= 0) AND (salary_range_max IS NULL OR salary_range_max >= salary_range_min) |
| chk_sort_order | CHECK | sort_order | sort_order >= 0 |
| chk_expiry_date | CHECK | expiry_date | expiry_date IS NULL OR expiry_date >= effective_date |
| chk_version | CHECK | version | version >= 1 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | tenant_id, created_by / tenant_id, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Employee | tenant_id, job_type_id | 1:N | 職種を持つ社員 |
| MST_EmployeeJobType | tenant_id, job_type_id | 1:N | 社員職種関連 |
| MST_JobTypeSkillGrade | tenant_id, job_type_id | 1:N | 職種スキルグレード関連 |
| MST_JobTypeSkill | tenant_id, job_type_id | 1:N | 職種スキル関連 |
| MST_CertificationRequirement | tenant_id, job_type_id | 1:N | 資格要件マスタ |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO MST_JobType (
    tenant_id, job_type_id, job_type_code, job_type_name,
    job_type_name_short, category, description,
    required_skills, career_path, evaluation_criteria,
    min_experience_years, max_experience_years,
    salary_range_min, salary_range_max, effective_date,
    created_by, updated_by
) VALUES (
    'tenant001',
    'JOB_001',
    'SE',
    'システムエンジニア',
    'SE',
    'TECHNICAL',
    'システム開発・保守を担当する技術職',
    '["Java", "SQL", "設計", "テスト"]',
    '{"junior": "JG001", "senior": "JG002", "expert": "JG003"}',
    '{"technical": 70, "communication": 20, "management": 10}',
    0,
    10,
    4000000,
    8000000,
    '2023-04-01',
    'system',
    'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 30件 | 基本的な職種体系 |
| 年間増加件数 | 5件 | 新職種追加 |
| 5年後想定件数 | 55件 | 想定値 |

### 5.3 データ保持期間
| データ種別 | 保持期間 | 備考 |
|------------|----------|------|
| 現行職種 | 無期限 | 業務継続中は保持 |
| 廃止職種 | 10年 | 人事記録保持要件 |

## 6. 運用仕様

### 6.1 バックアップ
- **日次バックアップ**: 毎日2:00実行
- **週次バックアップ**: 毎週日曜日3:00実行
- **月次バックアップ**: 毎月1日4:00実行

### 6.2 パーティション
- **パーティション種別**: なし
- **パーティション条件**: -

### 6.3 アーカイブ
- **アーカイブ条件**: 廃止から10年経過
- **アーカイブ先**: アーカイブDB
- **アーカイブ方法**: 年次バッチで実行

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | tenant_id, is_active | 有効職種一覧取得 |
| SELECT | 高 | tenant_id, category | カテゴリ別職種取得 |
| SELECT | 中 | tenant_id, job_type_code | 職種コード検索 |
| SELECT | 中 | required_skills | JSON検索（スキル要件） |
| UPDATE | 低 | tenant_id, job_type_id | 職種情報更新 |
| INSERT | 低 | - | 新規職種作成 |

### 7.2 パフォーマンス要件
- **SELECT**: 10ms以内
- **INSERT**: 50ms以内
- **UPDATE**: 50ms以内
- **DELETE**: 50ms以内

### 7.3 同時接続数
- **想定同時接続数**: 50ユーザー
- **最大同時接続数**: 200ユーザー

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| hr_admin | ○ | ○ | ○ | × | 人事管理者 |
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員 |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- **個人情報**: 含まない
- **機密情報**: 含む（給与レンジ）
- **暗号化**: 不要
- **マスキング**: 本番環境以外では給与レンジをマスキング

### 8.3 監査要件
- **操作ログ**: 全ての更新操作を記録
- **アクセスログ**: 参照操作を記録
- **保持期間**: 90日間

## 9. 移行仕様

### 9.1 データ移行
- **移行元**: 人事システム
- **移行方法**: CSVインポート
- **移行タイミング**: システム移行時
- **移行検証**: JSON形式の妥当性チェック

### 9.2 DDL
```sql
CREATE TABLE MST_JobType (
    tenant_id VARCHAR(50) NOT NULL,
    job_type_id VARCHAR(20) NOT NULL,
    job_type_code VARCHAR(10) NOT NULL,
    job_type_name VARCHAR(100) NOT NULL,
    job_type_name_short VARCHAR(50) NULL,
    job_type_name_en VARCHAR(100) NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'GENERAL',
    description TEXT NULL,
    required_skills JSON NULL,
    career_path JSON NULL,
    evaluation_criteria JSON NULL,
    min_experience_years INTEGER NULL DEFAULT 0,
    max_experience_years INTEGER NULL,
    salary_range_min DECIMAL(10,0) NULL,
    salary_range_max DECIMAL(10,0) NULL,
    sort_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    effective_date DATE NOT NULL,
    expiry_date DATE NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (tenant_id, job_type_id),
    UNIQUE KEY idx_job_type_code (tenant_id, job_type_code),
    UNIQUE KEY idx_job_type_name (tenant_id, job_type_name),
    INDEX idx_category (tenant_id, category),
    INDEX idx_active (tenant_id, is_active),
    INDEX idx_sort_order (tenant_id, sort_order),
    INDEX idx_effective (effective_date, expiry_date),
    CONSTRAINT fk_job_type_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_job_type_created_by FOREIGN KEY (tenant_id, created_by) REFERENCES MST_UserAuth(tenant_id, user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_job_type_updated_by FOREIGN KEY (tenant_id, updated_by) REFERENCES MST_UserAuth(tenant_id, user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_job_type_category CHECK (category IN ('TECHNICAL', 'SALES', 'MANAGEMENT', 'GENERAL')),
    CONSTRAINT chk_job_type_experience_years CHECK (min_experience_years >= 0 AND (max_experience_years IS NULL OR max_experience_years >= min_experience_years)),
    CONSTRAINT chk_job_type_salary_range CHECK ((salary_range_min IS NULL OR salary_range_min >= 0) AND (salary_range_max IS NULL OR salary_range_max >= salary_range_min)),
    CONSTRAINT chk_job_type_sort_order CHECK (sort_order >= 0),
    CONSTRAINT chk_job_type_expiry_date CHECK (expiry_date IS NULL OR expiry_date >= effective_date),
    CONSTRAINT chk_job_type_version CHECK (version >= 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

### 10.1 設計要件
1. JSON型を使用してスキル要件、キャリアパス、評価基準を柔軟に管理
2. 有効期間により職種変更履歴を管理
3. 職種廃止時は論理削除（is_active=FALSE）を使用
4. 楽観的排他制御によりデータ整合性を保証
5. 人事システムとの定期同期により最新職種情報を維持

### 10.2 運用要件
1. 職種カテゴリにより職種の分類管理が可能
2. 給与レンジにより人事評価との連携が可能
3. 表示順序により職種一覧の表示制御が可能
4. テナント間でのデータ漏洩防止のため、必ずtenant_idを条件に含める
5. JSON検索時はMySQLのJSON関数を活用

### 10.3 障害対応
1. JSON形式の妥当性チェック機能を実装
2. 職種削除時の影響範囲確認機能を提供
3. 人事システム連携障害時のフォールバック処理を実装

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-29 | システムアーキテクト | 初版作成 |
| 1.1 | 2025-05-31 | システムアーキテクト | 新フォーマットに変更、マルチテナント対応追加 |
