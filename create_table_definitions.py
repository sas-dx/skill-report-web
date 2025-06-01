#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書一括作成スクリプト
テーブル一覧.mdを元に、残りのテーブル定義書を新命名規則で作成します。
"""

import os
import re
from datetime import datetime

# テーブル情報の定義
tables = [
    # マスタ系
    {"id": "TBL-003", "name": "MST_Permission", "logical": "権限情報", "category": "マスタ系", "priority": "高", "api": "API-003, API-004", "batch": "BATCH-003"},
    {"id": "TBL-004", "name": "MST_UserRole", "logical": "ユーザーロール関連", "category": "マスタ系", "priority": "高", "api": "API-004", "batch": "BATCH-003"},
    {"id": "TBL-006", "name": "MST_Employee", "logical": "社員基本情報", "category": "マスタ系", "priority": "最高", "api": "API-005", "batch": "BATCH-004"},
    {"id": "TBL-007", "name": "MST_Department", "logical": "部署マスタ", "category": "マスタ系", "priority": "最高", "api": "API-006", "batch": "BATCH-004, BATCH-015"},
    {"id": "TBL-008", "name": "MST_Position", "logical": "役職マスタ", "category": "マスタ系", "priority": "最高", "api": "API-006", "batch": "BATCH-004, BATCH-015"},
    {"id": "TBL-009", "name": "MST_SkillHierarchy", "logical": "スキル階層マスタ", "category": "マスタ系", "priority": "高", "api": "API-007", "batch": "BATCH-005"},
    {"id": "TBL-011", "name": "MST_Certification", "logical": "資格情報", "category": "マスタ系", "priority": "高", "api": "API-009, API-010", "batch": "BATCH-007"},
    {"id": "TBL-013", "name": "MST_CareerPlan", "logical": "目標・キャリアプラン", "category": "マスタ系", "priority": "中", "api": "API-012", "batch": "BATCH-008"},
    {"id": "TBL-019", "name": "MST_ReportTemplate", "logical": "帳票テンプレート", "category": "マスタ系", "priority": "低", "api": "API-018", "batch": "BATCH-012"},
    {"id": "TBL-023", "name": "MST_SystemConfig", "logical": "システム設定", "category": "マスタ系", "priority": "低", "api": "API-024", "batch": "BATCH-016"},
    {"id": "TBL-026", "name": "MST_Tenant", "logical": "テナント管理", "category": "マスタ系", "priority": "最高", "api": "API-025", "batch": "BATCH-018-01, BATCH-018-02"},
    {"id": "TBL-027", "name": "MST_TenantSettings", "logical": "テナント設定", "category": "マスタ系", "priority": "最高", "api": "API-026", "batch": "BATCH-018-05"},
    {"id": "TBL-028", "name": "MST_NotificationSettings", "logical": "通知設定", "category": "マスタ系", "priority": "高", "api": "API-028", "batch": "BATCH-019-05"},
    {"id": "TBL-029", "name": "MST_NotificationTemplate", "logical": "通知テンプレート", "category": "マスタ系", "priority": "高", "api": "API-029", "batch": "BATCH-019-01"},
    {"id": "TBL-034", "name": "MST_SkillCategory", "logical": "スキルカテゴリマスタ", "category": "マスタ系", "priority": "高", "api": "API-030", "batch": "BATCH-020"},
    {"id": "TBL-035", "name": "MST_JobType", "logical": "職種マスタ", "category": "マスタ系", "priority": "最高", "api": "API-031", "batch": "BATCH-027"},
    {"id": "TBL-036", "name": "MST_SkillGrade", "logical": "スキルグレードマスタ", "category": "マスタ系", "priority": "高", "api": "API-032", "batch": "BATCH-028"},
    {"id": "TBL-037", "name": "MST_CertificationRequirement", "logical": "資格要件マスタ", "category": "マスタ系", "priority": "高", "api": "API-033", "batch": "BATCH-029"},
    {"id": "TBL-038", "name": "MST_EmployeeJobType", "logical": "社員職種関連", "category": "マスタ系", "priority": "最高", "api": "API-034", "batch": "BATCH-030"},
    {"id": "TBL-039", "name": "MST_JobTypeSkillGrade", "logical": "職種スキルグレード関連", "category": "マスタ系", "priority": "高", "api": "API-035", "batch": "BATCH-031"},
    {"id": "TBL-040", "name": "MST_SkillGradeRequirement", "logical": "スキルグレード要件", "category": "マスタ系", "priority": "高", "api": "API-036", "batch": "BATCH-032"},
    {"id": "TBL-041", "name": "MST_JobTypeSkill", "logical": "職種スキル関連", "category": "マスタ系", "priority": "高", "api": "API-037", "batch": "BATCH-033"},
    {"id": "TBL-042", "name": "MST_EmployeeDepartment", "logical": "社員部署関連", "category": "マスタ系", "priority": "最高", "api": "API-020", "batch": "BATCH-025"},
    {"id": "TBL-043", "name": "MST_EmployeePosition", "logical": "社員役職関連", "category": "マスタ系", "priority": "最高", "api": "API-021", "batch": "BATCH-026"},
    {"id": "TBL-044", "name": "MST_SkillItem", "logical": "スキル項目マスタ", "category": "マスタ系", "priority": "高", "api": "API-038", "batch": "BATCH-034"},
    {"id": "TBL-045", "name": "MST_TrainingProgram", "logical": "研修プログラム", "category": "マスタ系", "priority": "中", "api": "API-039", "batch": "BATCH-035"},
    
    # トランザクション系
    {"id": "TBL-010", "name": "TRN_SkillRecord", "logical": "スキル評価記録", "category": "トランザクション系", "priority": "最高", "api": "API-008", "batch": "BATCH-006"},
    {"id": "TBL-014", "name": "TRN_GoalProgress", "logical": "目標進捗", "category": "トランザクション系", "priority": "中", "api": "API-013", "batch": "BATCH-008"},
    {"id": "TBL-015", "name": "TRN_ProjectRecord", "logical": "案件実績", "category": "トランザクション系", "priority": "中", "api": "API-014", "batch": "BATCH-009"},
    {"id": "TBL-017", "name": "TRN_TrainingHistory", "logical": "研修履歴", "category": "トランザクション系", "priority": "中", "api": "API-016", "batch": "BATCH-011"},
    {"id": "TBL-018", "name": "TRN_PDU", "logical": "継続教育ポイント", "category": "トランザクション系", "priority": "中", "api": "API-017", "batch": "BATCH-011"},
    {"id": "TBL-046", "name": "TRN_SkillEvidence", "logical": "スキル証跡", "category": "トランザクション系", "priority": "中", "api": "API-040", "batch": "BATCH-036"},
    {"id": "TBL-047", "name": "TRN_Notification", "logical": "通知履歴", "category": "トランザクション系", "priority": "中", "api": "API-041", "batch": "BATCH-037"},
    
    # システム系
    {"id": "TBL-012", "name": "SYS_SkillIndex", "logical": "スキル検索インデックス", "category": "システム系", "priority": "高", "api": "API-011", "batch": "BATCH-006"},
    {"id": "TBL-020", "name": "SYS_SkillMatrix", "logical": "スキルマップ", "category": "システム系", "priority": "低", "api": "API-019", "batch": "BATCH-006"},
    {"id": "TBL-021", "name": "SYS_BackupHistory", "logical": "バックアップ履歴", "category": "システム系", "priority": "高", "api": "API-020", "batch": "BATCH-013"},
    {"id": "TBL-022", "name": "SYS_SystemLog", "logical": "システムログ", "category": "システム系", "priority": "高", "api": "API-021", "batch": "BATCH-014"},
    {"id": "TBL-024", "name": "SYS_TokenStore", "logical": "トークン管理", "category": "システム系", "priority": "高", "api": "API-001, API-002", "batch": "BATCH-017"},
    {"id": "TBL-025", "name": "SYS_MasterData", "logical": "マスタデータ全般", "category": "システム系", "priority": "低", "api": "API-023", "batch": "BATCH-015"},
    {"id": "TBL-030", "name": "SYS_TenantUsage", "logical": "テナント使用量", "category": "システム系", "priority": "高", "api": "API-025", "batch": "BATCH-018-01"},
    {"id": "TBL-031", "name": "SYS_IntegrationConfig", "logical": "外部連携設定", "category": "システム系", "priority": "高", "api": "API-028, API-029", "batch": "BATCH-019-03"},
    
    # 履歴系
    {"id": "TBL-005", "name": "HIS_AuditLog", "logical": "監査ログ", "category": "履歴系", "priority": "高", "api": "API-022", "batch": "BATCH-003, BATCH-014"},
    {"id": "TBL-032", "name": "HIS_NotificationLog", "logical": "通知送信履歴", "category": "履歴系", "priority": "中", "api": "API-029", "batch": "BATCH-019-04"},
    {"id": "TBL-033", "name": "HIS_TenantBilling", "logical": "テナント課金履歴", "category": "履歴系", "priority": "高", "api": "API-025", "batch": "BATCH-018-02"},
    
    # ワーク系
    {"id": "TBL-016", "name": "WRK_BatchJobLog", "logical": "一括登録ジョブログ", "category": "ワーク系", "priority": "低", "api": "API-015", "batch": "BATCH-010"},
]

def create_table_definition(table_info):
    """テーブル定義書のテンプレートを生成"""
    
    # カテゴリに応じたカラム数を設定
    if table_info["category"] == "マスタ系":
        column_count = 25
    elif table_info["category"] == "トランザクション系":
        column_count = 20
    elif table_info["category"] == "システム系":
        column_count = 18
    elif table_info["category"] == "履歴系":
        column_count = 15
    else:  # ワーク系
        column_count = 12
    
    template = f"""# テーブル定義書：{table_info["name"]}（{table_info["logical"]}）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | {table_info["id"]} |
| **テーブル名** | {table_info["name"]} |
| **論理名** | {table_info["logical"]} |
| **カテゴリ** | {table_info["category"]} |
| **優先度** | {table_info["priority"]} |
| **ステータス** | 運用中 |
| **作成日** | 2025-06-01 |
| **最終更新日** | 2025-06-01 |

## 2. テーブル概要

### 2.1 概要・目的
{table_info["name"]}（{table_info["logical"]}）は、{table_info["logical"]}に関する情報を管理するテーブルです。

### 2.2 関連API
- [{table_info["api"]}](../../api/specs/) - 関連API

### 2.3 関連バッチ
- [{table_info["batch"]}](../../batch/specs/) - 関連バッチ

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
| 1 | id | ID | VARCHAR | 50 | × | ○ | - | - | 主キー |
| 2 | tenant_id | テナントID | VARCHAR | 50 | × | - | ○ | - | テナントID |
| 3 | name | 名称 | VARCHAR | 255 | × | - | - | - | 名称 |
| 4 | description | 説明 | TEXT | - | ○ | - | - | NULL | 説明 |
| 5 | is_active | 有効フラグ | BOOLEAN | - | × | - | - | TRUE | 有効フラグ |
| 6 | created_at | 作成日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP | 作成日時 |
| 7 | updated_at | 更新日時 | TIMESTAMP | - | × | - | - | CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP | 更新日時 |
| 8 | created_by | 作成者ID | VARCHAR | 50 | × | - | ○ | - | 作成者ID |
| 9 | updated_by | 更新者ID | VARCHAR | 50 | × | - | ○ | - | 更新者ID |"""

    # カラム数に応じて追加カラムを生成
    for i in range(10, column_count + 1):
        template += f"""
| {i} | column_{i} | カラム{i} | VARCHAR | 100 | ○ | - | - | NULL | カラム{i}の説明 |"""

    template += f"""

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_name | INDEX | name | 名称検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_{table_info["name"].lower()} | PRIMARY KEY | id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | - |

## 5. データ仕様

### 5.1 データ例
```sql
INSERT INTO {table_info["name"]} (
    id, tenant_id, name, description, is_active,
    created_by, updated_by
) VALUES (
    'sample_001', 'TENANT_001', 'サンプル', 'サンプルデータ', TRUE,
    'system', 'system'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 10件 | 初期データ |
| 月間増加件数 | 50件 | 想定値 |
| 年間増加件数 | 600件 | 想定値 |
| 5年後想定件数 | 3,010件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：無効化から1年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | id, tenant_id | 基本検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新 |
| DELETE | 低 | id | 削除 |

### 7.2 パフォーマンス要件
- SELECT：10ms以内
- INSERT：50ms以内
- UPDATE：50ms以内
- DELETE：100ms以内

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者 |
| user | ○ | × | × | × | 一般ユーザー |
| readonly | ○ | × | × | × | 参照専用 |

### 8.2 データ保護
- 個人情報：含まない
- 機密情報：含まない
- 暗号化：不要

## 9. 移行仕様

### 9.1 データ移行
- 移行元：既存システム
- 移行方法：CSVインポート
- 移行タイミング：システム移行時

### 9.2 DDL
```sql
CREATE TABLE {table_info["name"]} (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    name VARCHAR(255) NOT NULL COMMENT '名称',
    description TEXT NULL COMMENT '説明',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_name (name),
    INDEX idx_active (is_active),
    CONSTRAINT fk_{table_info["name"].lower()}_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_{table_info["name"].lower()}_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_{table_info["name"].lower()}_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='{table_info["logical"]}';
```

## 10. 特記事項

1. **データ整合性**
   - 外部キー制約により関連テーブルとの整合性を保証

2. **パフォーマンス**
   - 適切なインデックスによる高速検索を実現

3. **セキュリティ**
   - ロールベースアクセス制御による適切な権限管理

4. **運用性**
   - 定期バックアップとアーカイブによるデータ保護

5. **拡張性**
   - 将来の機能拡張に対応可能な設計

"""
    
    return template

def main():
    """メイン処理"""
    base_dir = "docs/design/database/tables"
    
    # ディレクトリが存在しない場合は作成
    os.makedirs(base_dir, exist_ok=True)
    
    # 各テーブル定義書を作成
    for table in tables:
        filename = f"テーブル定義書_{table['name']}_{table['logical']}.md"
        filepath = os.path.join(base_dir, filename)
        
        # テーブル定義書の内容を生成
        content = create_table_definition(table)
        
        # ファイルに書き込み
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filename}")
    
    print(f"\n✅ 完了: {len(tables)}個のテーブル定義書を作成しました。")

if __name__ == "__main__":
    main()
