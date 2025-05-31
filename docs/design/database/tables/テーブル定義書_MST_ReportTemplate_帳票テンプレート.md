# テーブル定義書：帳票テンプレート (MST_ReportTemplate)

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | TBL-019 |
| **テーブル名** | MST_ReportTemplate |
| **論理名** | 帳票テンプレート |
| **カテゴリ** | マスタ系 |
| **優先度** | 低 |
| **ステータス** | 運用中 |
| **作成日** | 2025-05-31 |
| **最終更新日** | 2025-05-31 |

## 2. テーブル概要

### 2.1 概要・目的
帳票テンプレートテーブル（MST_ReportTemplate）は、システムで出力される各種帳票のテンプレート情報を管理するマスタテーブルです。Excel形式やPDF形式の帳票テンプレートファイルの情報、レイアウト設定、出力パラメータなどを記録し、帳票出力機能の基盤となります。

### 2.2 関連API
- [API-018](../api/specs/API仕様書_API-018.md) - 帳票テンプレート管理API

### 2.3 関連バッチ
- [BATCH-012](../batch/specs/バッチ定義書_BATCH-012.md) - 帳票テンプレート同期バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | template_id | テンプレートID | VARCHAR | 50 | × | ○ | - | - | テンプレートを一意に識別するID |
| 2 | template_name | テンプレート名 | VARCHAR | 200 | × | - | - | - | テンプレートの名称 |
| 3 | template_type | テンプレート種別 | VARCHAR | 50 | × | - | - | - | テンプレートの種別 |
| 4 | output_format | 出力形式 | VARCHAR | 20 | × | - | - | - | 出力形式（Excel/PDF/CSV等） |
| 5 | file_name | ファイル名 | VARCHAR | 255 | × | - | - | - | テンプレートファイル名 |
| 6 | file_path | ファイルパス | VARCHAR | 500 | × | - | - | - | テンプレートファイルの保存パス |
| 7 | file_size | ファイルサイズ | BIGINT | - | ○ | - | - | NULL | テンプレートファイルのサイズ（バイト） |
| 8 | version | バージョン | VARCHAR | 20 | × | - | - | '1.0' | テンプレートのバージョン |
| 9 | description | 説明 | TEXT | - | ○ | - | - | NULL | テンプレートの説明 |
| 10 | layout_config | レイアウト設定 | TEXT | - | ○ | - | - | NULL | レイアウト設定（JSON形式） |
| 11 | output_params | 出力パラメータ | TEXT | - | ○ | - | - | NULL | 出力時のパラメータ設定（JSON形式） |
| 12 | target_roles | 対象ロール | VARCHAR | 500 | ○ | - | - | NULL | 利用可能なロール（カンマ区切り） |
| 13 | sort_order | ソート順 | INTEGER | - | ○ | - | - | 0 | 表示時のソート順 |
| 14 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | 所属テナントのID |
| 15 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | テンプレートが有効かどうか |
| 16 | is_public | 公開フラグ | BOOLEAN | - | × | - | - | TRUE | 一般ユーザーが利用可能かどうか |
| 17 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | レコード作成日時 |
| 18 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | レコード更新日時 |
| 19 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | レコード作成者のユーザーID |
| 20 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | レコード更新者のユーザーID |

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | template_id | 主キー |
| idx_template_name | INDEX | template_name | テンプレート名による検索用 |
| idx_template_type | INDEX | template_type | テンプレート種別による検索用 |
| idx_output_format | INDEX | output_format | 出力形式による検索用 |
| idx_sort_order | INDEX | sort_order | ソート順による並び替え用 |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_active | INDEX | is_active | 有効フラグによる検索用 |
| idx_public | INDEX | is_public | 公開フラグによる検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_report_template | PRIMARY KEY | template_id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
| chk_template_type | CHECK | template_type | template_type IN ('PERSONAL', 'DEPARTMENT', 'ANALYSIS', 'SUMMARY') |
| chk_output_format | CHECK | output_format | output_format IN ('Excel', 'PDF', 'CSV', 'Word') |
| chk_file_size | CHECK | file_size | file_size IS NULL OR file_size >= 0 |
| chk_sort_order | CHECK | sort_order | sort_order >= 0 |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | 作成者・更新者 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| TRN_ReportOutput | template_id | 1:N | 帳票出力履歴 |

## 5. データ仕様

### 5.1 テンプレート種別定義
| 種別 | 説明 | 用途 |
|------|------|------|
| PERSONAL | 個人帳票 | 個人のスキル報告書、評価シート等 |
| DEPARTMENT | 部門帳票 | 部門別スキルマップ、組織図等 |
| ANALYSIS | 分析帳票 | スキル分析、統計レポート等 |
| SUMMARY | 集計帳票 | 月次・年次集計レポート等 |

### 5.2 出力形式定義
| 形式 | 説明 | 用途 |
|------|------|------|
| Excel | Excel形式 | データ編集可能な帳票 |
| PDF | PDF形式 | 印刷・配布用帳票 |
| CSV | CSV形式 | データ分析用 |
| Word | Word形式 | 文書形式の帳票 |

### 5.3 データ例
```sql
-- 個人スキル報告書テンプレート
INSERT INTO MST_ReportTemplate (
    template_id, template_name, template_type, output_format,
    file_name, file_path, version, description,
    layout_config, output_params, target_roles,
    tenant_id, created_by, updated_by
) VALUES (
    'TPL_001',
    '個人スキル報告書',
    'PERSONAL',
    'Excel',
    'personal_skill_report.xlsx',
    '/templates/personal/personal_skill_report.xlsx',
    '1.0',
    '社員個人のスキル評価結果を出力する帳票テンプレート',
    '{"orientation": "portrait", "margins": {"top": 20, "bottom": 20}}',
    '{"include_chart": true, "show_history": false}',
    'employee,manager',
    'TENANT_001',
    'system',
    'system'
);

-- 部門スキルマップテンプレート
INSERT INTO MST_ReportTemplate (
    template_id, template_name, template_type, output_format,
    file_name, file_path, version, description,
    layout_config, output_params, target_roles,
    is_public, tenant_id, created_by, updated_by
) VALUES (
    'TPL_002',
    '部門スキルマップ',
    'DEPARTMENT',
    'PDF',
    'department_skill_map.pdf',
    '/templates/department/department_skill_map.pdf',
    '1.0',
    '部門全体のスキル保有状況を可視化する帳票テンプレート',
    '{"orientation": "landscape", "page_size": "A3"}',
    '{"group_by": "skill_category", "show_level": true}',
    'manager,hr_admin',
    FALSE,
    'TENANT_001',
    'system',
    'system'
);

-- 年間作業報告書テンプレート
INSERT INTO MST_ReportTemplate (
    template_id, template_name, template_type, output_format,
    file_name, file_path, version, description,
    layout_config, output_params, target_roles,
    tenant_id, created_by, updated_by
) VALUES (
    'TPL_003',
    '年間作業報告書',
    'SUMMARY',
    'Excel',
    'annual_work_report.xlsx',
    '/templates/summary/annual_work_report.xlsx',
    '1.0',
    '年間の作業実績をまとめた報告書テンプレート',
    '{"orientation": "portrait", "include_summary": true}',
    '{"period": "yearly", "include_projects": true}',
    'employee,manager,hr_admin',
    'TENANT_001',
    'system',
    'system'
);
```

### 5.4 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 50件 | 基本的な帳票テンプレート |
| 年間増加件数 | 10件 | 新規帳票の追加 |
| 5年後想定件数 | 100件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行
- テンプレートファイルの別途バックアップ

### 6.2 パーティション
- パーティション種別：なし（データ量が少ないため）

### 6.3 アーカイブ
- アーカイブ条件：論理削除から2年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | template_type, is_active | テンプレート一覧 |
| SELECT | 高 | template_id | 特定テンプレート取得 |
| SELECT | 中 | target_roles | ロール別テンプレート |
| SELECT | 中 | tenant_id | テナント別テンプレート |
| INSERT | 低 | - | 新規テンプレート登録 |
| UPDATE | 低 | template_id | テンプレート更新 |

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
| report_admin | ○ | ○ | ○ | × | 帳票管理者 |
| manager | ○ | × | × | × | 管理職 |
| employee | ○ | × | × | × | 一般社員（公開テンプレートのみ） |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含まない（テンプレート情報）
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存帳票システム
- 移行方法：CSVインポート + ファイルコピー
- 移行タイミング：システム移行時

### 9.2 移行スクリプト例
```sql
-- 既存データの移行
INSERT INTO MST_ReportTemplate (
    template_id, template_name, template_type, output_format,
    file_name, file_path, version, description,
    tenant_id, created_by, updated_by
)
SELECT 
    CONCAT('TPL_', LPAD(ROW_NUMBER() OVER (ORDER BY template_name), 3, '0')),
    template_name,
    CASE 
        WHEN category = '個人' THEN 'PERSONAL'
        WHEN category = '部門' THEN 'DEPARTMENT'
        WHEN category = '分析' THEN 'ANALYSIS'
        ELSE 'SUMMARY'
    END,
    format_type,
    file_name,
    file_path,
    '1.0',
    description,
    'TENANT_001',
    'migration',
    'migration'
FROM old_report_template
WHERE is_valid = 1;
```

### 9.3 DDL
```sql
CREATE TABLE MST_ReportTemplate (
    template_id VARCHAR(50) NOT NULL,
    template_name VARCHAR(200) NOT NULL,
    template_type VARCHAR(50) NOT NULL,
    output_format VARCHAR(20) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT NULL,
    version VARCHAR(20) NOT NULL DEFAULT '1.0',
    description TEXT NULL,
    layout_config TEXT NULL,
    output_params TEXT NULL,
    target_roles VARCHAR(500) NULL,
    sort_order INTEGER NULL DEFAULT 0,
    tenant_id VARCHAR(50) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_public BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by VARCHAR(50) NOT NULL,
    updated_by VARCHAR(50) NOT NULL,
    PRIMARY KEY (template_id),
    INDEX idx_template_name (template_name),
    INDEX idx_template_type (template_type),
    INDEX idx_output_format (output_format),
    INDEX idx_sort_order (sort_order),
    INDEX idx_tenant (tenant_id),
    INDEX idx_active (is_active),
    INDEX idx_public (is_public),
    CONSTRAINT fk_template_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_template_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_template_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_template_type CHECK (template_type IN ('PERSONAL', 'DEPARTMENT', 'ANALYSIS', 'SUMMARY')),
    CONSTRAINT chk_output_format CHECK (output_format IN ('Excel', 'PDF', 'CSV', 'Word')),
    CONSTRAINT chk_file_size CHECK (file_size IS NULL OR file_size >= 0),
    CONSTRAINT chk_sort_order CHECK (sort_order >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 10. 特記事項

1. **ファイル管理**: テンプレートファイルは別途ファイルサーバーで管理
2. **バージョン管理**: テンプレート更新時のバージョン管理機能
3. **権限制御**: ロール別・公開フラグによる利用制限
4. **レイアウト設定**: JSON形式でのレイアウト設定保存
5. **出力パラメータ**: JSON形式での出力オプション管理
6. **ソート順制御**: 表示順序の制御機能
7. **テナント分離**: マルチテナント対応
8. **ファイルサイズ制限**: 100MB以下のファイルサイズ制限
9. **形式サポート**: Excel、PDF、CSV、Word形式をサポート
10. **セキュリティ**: ファイルアクセス権限の適切な設定
11. **バックアップ**: テンプレートファイルの定期バックアップ
12. **履歴管理**: テンプレート変更履歴の管理

---

**改訂履歴**

| バージョン | 日付 | 変更者 | 変更内容 |
|------------|------|--------|----------|
| 1.0 | 2025-05-31 | システムアーキテクト | 初版作成（帳票テンプレート管理対応） |
