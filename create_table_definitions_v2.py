#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書一括再作成スクリプト v2.0
命名規則: テーブル定義書_テーブル名_論理名.md
"""

import os
import re
from datetime import datetime

# テーブル一覧データ（テーブル一覧.mdから抽出）
TABLES = [
    # マスタ系
    {"id": "TBL-001", "table_name": "MST_UserAuth", "logical_name": "ユーザー認証情報", "category": "マスタ系", "priority": "最高", "api_ids": "API-001, API-002", "batch_ids": "BATCH-001, BATCH-002, BATCH-003, BATCH-017", "screens": "SCR-LOGIN, SCR-ACCESS"},
    {"id": "TBL-002", "table_name": "MST_Role", "logical_name": "ロール情報", "category": "マスタ系", "priority": "高", "api_ids": "API-003", "batch_ids": "BATCH-003", "screens": "SCR-ACCESS"},
    {"id": "TBL-003", "table_name": "MST_Permission", "logical_name": "権限情報", "category": "マスタ系", "priority": "高", "api_ids": "API-003, API-004", "batch_ids": "BATCH-003", "screens": "SCR-ACCESS"},
    {"id": "TBL-004", "table_name": "MST_UserRole", "logical_name": "ユーザーロール関連", "category": "マスタ系", "priority": "高", "api_ids": "API-004", "batch_ids": "BATCH-003", "screens": "SCR-ACCESS"},
    {"id": "TBL-006", "table_name": "MST_Employee", "logical_name": "社員基本情報", "category": "マスタ系", "priority": "最高", "api_ids": "API-005", "batch_ids": "BATCH-004", "screens": "SCR-PROFILE"},
    {"id": "TBL-007", "table_name": "MST_Department", "logical_name": "部署マスタ", "category": "マスタ系", "priority": "最高", "api_ids": "API-006", "batch_ids": "BATCH-004, BATCH-015", "screens": "SCR-PROFILE, SCR-ADMIN"},
    {"id": "TBL-008", "table_name": "MST_Position", "logical_name": "役職マスタ", "category": "マスタ系", "priority": "最高", "api_ids": "API-006", "batch_ids": "BATCH-004, BATCH-015", "screens": "SCR-PROFILE, SCR-ADMIN"},
    {"id": "TBL-009", "table_name": "MST_SkillHierarchy", "logical_name": "スキル階層マスタ", "category": "マスタ系", "priority": "高", "api_ids": "API-007", "batch_ids": "BATCH-005", "screens": "SCR-SKILL-M"},
    {"id": "TBL-011", "table_name": "MST_Certification", "logical_name": "資格情報", "category": "マスタ系", "priority": "高", "api_ids": "API-009, API-010", "batch_ids": "BATCH-007", "screens": "SCR-SKILL, SCR-SKILL-M"},
    {"id": "TBL-013", "table_name": "MST_CareerPlan", "logical_name": "目標・キャリアプラン", "category": "マスタ系", "priority": "中", "api_ids": "API-012", "batch_ids": "BATCH-008", "screens": "SCR-CAR-PLAN"},
    {"id": "TBL-019", "table_name": "MST_ReportTemplate", "logical_name": "帳票テンプレート", "category": "マスタ系", "priority": "低", "api_ids": "API-018", "batch_ids": "BATCH-012", "screens": "SCR-REPORT"},
    {"id": "TBL-023", "table_name": "MST_SystemConfig", "logical_name": "システム設定", "category": "マスタ系", "priority": "低", "api_ids": "API-024", "batch_ids": "BATCH-016", "screens": "SCR-ADMIN"},
    {"id": "TBL-026", "table_name": "MST_Tenant", "logical_name": "テナント管理", "category": "マスタ系", "priority": "最高", "api_ids": "API-025", "batch_ids": "BATCH-018-01, BATCH-018-02", "screens": "SCR-TENANT-ADMIN"},
    {"id": "TBL-027", "table_name": "MST_TenantSettings", "logical_name": "テナント設定", "category": "マスタ系", "priority": "最高", "api_ids": "API-026", "batch_ids": "BATCH-018-05", "screens": "SCR-TENANT-ADMIN"},
    {"id": "TBL-028", "table_name": "MST_NotificationSettings", "logical_name": "通知設定", "category": "マスタ系", "priority": "高", "api_ids": "API-028", "batch_ids": "BATCH-019-05", "screens": "SCR-NOTIFY-ADMIN"},
    {"id": "TBL-029", "table_name": "MST_NotificationTemplate", "logical_name": "通知テンプレート", "category": "マスタ系", "priority": "高", "api_ids": "API-029", "batch_ids": "BATCH-019-01", "screens": "SCR-NOTIFY-ADMIN"},
    {"id": "TBL-034", "table_name": "MST_SkillCategory", "logical_name": "スキルカテゴリマスタ", "category": "マスタ系", "priority": "高", "api_ids": "API-030", "batch_ids": "BATCH-020", "screens": "SCR-SKILL-M"},
    {"id": "TBL-035", "table_name": "MST_JobType", "logical_name": "職種マスタ", "category": "マスタ系", "priority": "最高", "api_ids": "API-031", "batch_ids": "BATCH-027", "screens": "SCR-PROFILE, SCR-ADMIN"},
    {"id": "TBL-036", "table_name": "MST_SkillGrade", "logical_name": "スキルグレードマスタ", "category": "マスタ系", "priority": "高", "api_ids": "API-032", "batch_ids": "BATCH-028", "screens": "SCR-SKILL-M"},
    {"id": "TBL-037", "table_name": "MST_CertificationRequirement", "logical_name": "資格要件マスタ", "category": "マスタ系", "priority": "高", "api_ids": "API-033", "batch_ids": "BATCH-029", "screens": "SCR-SKILL-M"},
    {"id": "TBL-038", "table_name": "MST_EmployeeJobType", "logical_name": "社員職種関連", "category": "マスタ系", "priority": "最高", "api_ids": "API-034", "batch_ids": "BATCH-030", "screens": "SCR-PROFILE, SCR-ADMIN"},
    {"id": "TBL-039", "table_name": "MST_JobTypeSkillGrade", "logical_name": "職種スキルグレード関連", "category": "マスタ系", "priority": "高", "api_ids": "API-035", "batch_ids": "BATCH-031", "screens": "SCR-SKILL-M"},
    {"id": "TBL-040", "table_name": "MST_SkillGradeRequirement", "logical_name": "スキルグレード要件", "category": "マスタ系", "priority": "高", "api_ids": "API-036", "batch_ids": "BATCH-032", "screens": "SCR-SKILL-M"},
    {"id": "TBL-041", "table_name": "MST_JobTypeSkill", "logical_name": "職種スキル関連", "category": "マスタ系", "priority": "高", "api_ids": "API-037", "batch_ids": "BATCH-033", "screens": "SCR-SKILL-M"},
    {"id": "TBL-042", "table_name": "MST_EmployeeDepartment", "logical_name": "社員部署関連", "category": "マスタ系", "priority": "最高", "api_ids": "API-020", "batch_ids": "BATCH-025", "screens": "SCR-PROFILE, SCR-ADMIN"},
    {"id": "TBL-043", "table_name": "MST_EmployeePosition", "logical_name": "社員役職関連", "category": "マスタ系", "priority": "最高", "api_ids": "API-021", "batch_ids": "BATCH-026", "screens": "SCR-PROFILE, SCR-ADMIN"},
    {"id": "TBL-044", "table_name": "MST_SkillItem", "logical_name": "スキル項目マスタ", "category": "マスタ系", "priority": "高", "api_ids": "API-038", "batch_ids": "BATCH-034", "screens": "SCR-SKILL-M"},
    {"id": "TBL-045", "table_name": "MST_TrainingProgram", "logical_name": "研修プログラム", "category": "マスタ系", "priority": "中", "api_ids": "API-039", "batch_ids": "BATCH-035", "screens": "SCR-TRAIN-M"},
    
    # トランザクション系
    {"id": "TBL-010", "table_name": "TRN_SkillRecord", "logical_name": "スキル評価記録", "category": "トランザクション系", "priority": "最高", "api_ids": "API-008", "batch_ids": "BATCH-006", "screens": "SCR-SKILL"},
    {"id": "TBL-014", "table_name": "TRN_GoalProgress", "logical_name": "目標進捗", "category": "トランザクション系", "priority": "中", "api_ids": "API-013", "batch_ids": "BATCH-008", "screens": "SCR-CAR-EVAL"},
    {"id": "TBL-015", "table_name": "TRN_ProjectRecord", "logical_name": "案件実績", "category": "トランザクション系", "priority": "中", "api_ids": "API-014", "batch_ids": "BATCH-009", "screens": "SCR-WORK"},
    {"id": "TBL-017", "table_name": "TRN_TrainingHistory", "logical_name": "研修履歴", "category": "トランザクション系", "priority": "中", "api_ids": "API-016", "batch_ids": "BATCH-011", "screens": "SCR-TRAIN"},
    {"id": "TBL-018", "table_name": "TRN_PDU", "logical_name": "継続教育ポイント", "category": "トランザクション系", "priority": "中", "api_ids": "API-017", "batch_ids": "BATCH-011", "screens": "SCR-TRAIN-M"},
    {"id": "TBL-046", "table_name": "TRN_SkillEvidence", "logical_name": "スキル証跡", "category": "トランザクション系", "priority": "中", "api_ids": "API-040", "batch_ids": "BATCH-036", "screens": "SCR-SKILL"},
    {"id": "TBL-047", "table_name": "TRN_Notification", "logical_name": "通知履歴", "category": "トランザクション系", "priority": "中", "api_ids": "API-041", "batch_ids": "BATCH-037", "screens": "SCR-NOTIFY"},
    
    # システム系
    {"id": "TBL-012", "table_name": "SYS_SkillIndex", "logical_name": "スキル検索インデックス", "category": "システム系", "priority": "高", "api_ids": "API-011", "batch_ids": "BATCH-006", "screens": "SCR-SKILL-SEARCH"},
    {"id": "TBL-020", "table_name": "SYS_SkillMatrix", "logical_name": "スキルマップ", "category": "システム系", "priority": "低", "api_ids": "API-019", "batch_ids": "BATCH-006", "screens": "SCR-SKILL-MAP"},
    {"id": "TBL-021", "table_name": "SYS_BackupHistory", "logical_name": "バックアップ履歴", "category": "システム系", "priority": "高", "api_ids": "API-020", "batch_ids": "BATCH-013", "screens": "SCR-ADMIN"},
    {"id": "TBL-022", "table_name": "SYS_SystemLog", "logical_name": "システムログ", "category": "システム系", "priority": "高", "api_ids": "API-021", "batch_ids": "BATCH-014", "screens": "SCR-ADMIN"},
    {"id": "TBL-024", "table_name": "SYS_TokenStore", "logical_name": "トークン管理", "category": "システム系", "priority": "高", "api_ids": "API-001, API-002", "batch_ids": "BATCH-017", "screens": "セッション管理"},
    {"id": "TBL-025", "table_name": "SYS_MasterData", "logical_name": "マスタデータ全般", "category": "システム系", "priority": "低", "api_ids": "API-023", "batch_ids": "BATCH-015", "screens": "SCR-ADMIN"},
    {"id": "TBL-030", "table_name": "SYS_TenantUsage", "logical_name": "テナント使用量", "category": "システム系", "priority": "高", "api_ids": "API-025", "batch_ids": "BATCH-018-01", "screens": "SCR-TENANT-ADMIN"},
    {"id": "TBL-031", "table_name": "SYS_IntegrationConfig", "logical_name": "外部連携設定", "category": "システム系", "priority": "高", "api_ids": "API-028, API-029", "batch_ids": "BATCH-019-03", "screens": "SCR-NOTIFY-ADMIN"},
    
    # 履歴系
    {"id": "TBL-005", "table_name": "HIS_AuditLog", "logical_name": "監査ログ", "category": "履歴系", "priority": "高", "api_ids": "API-022", "batch_ids": "BATCH-003, BATCH-014", "screens": "SCR-ACCESS, SCR-ADMIN"},
    {"id": "TBL-032", "table_name": "HIS_NotificationLog", "logical_name": "通知送信履歴", "category": "履歴系", "priority": "中", "api_ids": "API-029", "batch_ids": "BATCH-019-04", "screens": "SCR-NOTIFY-ADMIN"},
    {"id": "TBL-033", "table_name": "HIS_TenantBilling", "logical_name": "テナント課金履歴", "category": "履歴系", "priority": "高", "api_ids": "API-025", "batch_ids": "BATCH-018-02", "screens": "SCR-TENANT-ADMIN"},
    
    # ワーク系
    {"id": "TBL-016", "table_name": "WRK_BatchJobLog", "logical_name": "一括登録ジョブログ", "category": "ワーク系", "priority": "低", "api_ids": "API-015", "batch_ids": "BATCH-010", "screens": "SCR-WORK-BULK"},
]

def generate_table_definition(table_info):
    """テーブル定義書を生成"""
    
    # カテゴリに応じた説明を生成
    category_descriptions = {
        "マスタ系": "マスタデータを管理するテーブルです。システムの基本設定や参照データを格納し、他のテーブルから参照されます。",
        "トランザクション系": "業務トランザクションデータを管理するテーブルです。日々の業務処理で発生するデータを格納します。",
        "システム系": "システム運用に必要な情報を管理するテーブルです。検索インデックス、ログ、設定情報などを格納します。",
        "履歴系": "過去の操作や変更履歴を管理するテーブルです。監査証跡や履歴管理のためのデータを格納します。",
        "ワーク系": "一時的な作業データを管理するテーブルです。バッチ処理や一括処理の際に使用されます。"
    }
    
    # 基本的なカラム定義を生成（テーブルタイプに応じて）
    common_columns = [
        {"name": "id", "logical": "ID", "type": "VARCHAR", "length": "50", "null": "×", "pk": "○", "fk": "-", "default": "-", "desc": "主キー"},
        {"name": "created_at", "logical": "作成日時", "type": "TIMESTAMP", "length": "-", "null": "×", "pk": "-", "fk": "-", "default": "CURRENT_TIMESTAMP", "desc": "レコード作成日時"},
        {"name": "updated_at", "logical": "更新日時", "type": "TIMESTAMP", "length": "-", "null": "×", "pk": "-", "fk": "-", "default": "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP", "desc": "レコード更新日時"},
        {"name": "created_by", "logical": "作成者ID", "type": "VARCHAR", "length": "50", "null": "×", "pk": "-", "fk": "○", "default": "-", "desc": "レコード作成者のユーザーID"},
        {"name": "updated_by", "logical": "更新者ID", "type": "VARCHAR", "length": "50", "null": "×", "pk": "-", "fk": "○", "default": "-", "desc": "レコード更新者のユーザーID"},
    ]
    
    # テナント対応テーブルの場合はtenant_idを追加
    if not table_info["table_name"].startswith("SYS_") and not table_info["table_name"].startswith("HIS_"):
        tenant_column = {"name": "tenant_id", "logical": "テナントID", "type": "VARCHAR", "length": "50", "null": "×", "pk": "-", "fk": "○", "default": "-", "desc": "テナントID"}
        common_columns.insert(1, tenant_column)
    
    # 有効フラグを追加（マスタ系の場合）
    if table_info["category"] == "マスタ系":
        active_column = {"name": "is_active", "logical": "有効フラグ", "type": "BOOLEAN", "length": "-", "null": "×", "pk": "-", "fk": "-", "default": "TRUE", "desc": "レコードが有効かどうか"}
        common_columns.insert(-2, active_column)
    
    # カラム定義テーブルを生成
    column_rows = ""
    for i, col in enumerate(common_columns, 1):
        column_rows += f"| {i} | {col['name']} | {col['logical']} | {col['type']} | {col['length']} | {col['null']} | {col['pk']} | {col['fk']} | {col['default']} | {col['desc']} |\n"
    
    # 現在の日付を取得
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    template = f"""# テーブル定義書：{table_info['table_name']}（{table_info['logical_name']}）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | {table_info['id']} |
| **テーブル名** | {table_info['table_name']} |
| **論理名** | {table_info['logical_name']} |
| **カテゴリ** | {table_info['category']} |
| **優先度** | {table_info['priority']} |
| **ステータス** | 運用中 |
| **作成日** | {current_date} |
| **最終更新日** | {current_date} |

## 2. テーブル概要

### 2.1 概要・目的
{table_info['table_name']}（{table_info['logical_name']}）は、{category_descriptions.get(table_info['category'], '業務データを管理するテーブルです。')}

### 2.2 関連API
{table_info['api_ids']}

### 2.3 関連バッチ
{table_info['batch_ids']}

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
{column_rows}

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_tenant | INDEX | tenant_id | テナント検索用 |
| idx_created_at | INDEX | created_at | 作成日時検索用 |
| idx_active | INDEX | is_active | 有効フラグ検索用 |

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_{table_info['table_name'].lower()} | PRIMARY KEY | id | 主キー制約 |
| fk_tenant | FOREIGN KEY | tenant_id | MST_Tenant.tenant_id |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_Tenant | tenant_id | 1:N | テナント情報 |
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
INSERT INTO {table_info['table_name']} (
    id, tenant_id, created_by, updated_by
) VALUES (
    'sample_001', 'TENANT_001', 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 10件 | 初期設定データ |
| 月間増加件数 | 100件 | 想定値 |
| 年間増加件数 | 1,200件 | 想定値 |
| 5年後想定件数 | 6,010件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：無効化から3年経過
- アーカイブ先：アーカイブDB

## 7. パフォーマンス

### 7.1 想定アクセスパターン
| 操作 | 頻度 | 条件 | 備考 |
|------|------|------|------|
| SELECT | 高 | id, tenant_id | 基本検索 |
| INSERT | 中 | - | 新規登録 |
| UPDATE | 中 | id | 更新処理 |
| DELETE | 低 | id | 削除処理 |

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
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| user | ○ | × | × | × | 一般ユーザー（参照のみ） |

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
CREATE TABLE {table_info['table_name']} (
    id VARCHAR(50) NOT NULL COMMENT 'ID',
    tenant_id VARCHAR(50) NOT NULL COMMENT 'テナントID',
    is_active BOOLEAN NOT NULL DEFAULT TRUE COMMENT '有効フラグ',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '作成日時',
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新日時',
    created_by VARCHAR(50) NOT NULL COMMENT '作成者ID',
    updated_by VARCHAR(50) NOT NULL COMMENT '更新者ID',
    PRIMARY KEY (id),
    INDEX idx_tenant (tenant_id),
    INDEX idx_created_at (created_at),
    INDEX idx_active (is_active),
    CONSTRAINT fk_{table_info['table_name'].lower()}_tenant FOREIGN KEY (tenant_id) REFERENCES MST_Tenant(tenant_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_{table_info['table_name'].lower()}_created_by FOREIGN KEY (created_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_{table_info['table_name'].lower()}_updated_by FOREIGN KEY (updated_by) REFERENCES MST_UserAuth(user_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='{table_info['logical_name']}';
```

## 10. 特記事項

1. **設計方針**
   - {table_info['category']}として設計
   - マルチテナント対応
   - 監査証跡の保持

2. **運用上の注意点**
   - 定期的なデータクリーンアップが必要
   - パフォーマンス監視を実施

3. **今後の拡張予定**
   - 必要に応じて機能拡張を検討

4. **関連画面**
   - {table_info['screens']}
"""
    
    return template

def main():
    """メイン処理"""
    print("🚀 テーブル定義書一括再作成を開始します...")
    
    # 出力ディレクトリの確認
    output_dir = "docs/design/database/tables"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📁 ディレクトリを作成しました: {output_dir}")
    
    # 既存ファイルのバックアップ（削除）
    print("🗑️  既存ファイルを削除中...")
    for filename in os.listdir(output_dir):
        if filename.startswith("テーブル定義書_") and filename.endswith(".md"):
            file_path = os.path.join(output_dir, filename)
            os.remove(file_path)
            print(f"   削除: {filename}")
    
    # 各テーブルの定義書を生成
    print("📝 テーブル定義書を生成中...")
    
    created_count = 0
    for table in TABLES:
        filename = f"テーブル定義書_{table['table_name']}_{table['logical_name']}.md"
        file_path = os.path.join(output_dir, filename)
        
        # テーブル定義書の内容を生成
        content = generate_table_definition(table)
        
        # ファイルに書き込み
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   作成: {filename}")
        created_count += 1
    
    print(f"\n✅ 完了！{created_count}個のテーブル定義書を作成しました。")
    print(f"📁 出力先: {output_dir}")
    
    # 統計情報を表示
    categories = {}
    for table in TABLES:
        category = table['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
    
    print("\n📊 カテゴリ別統計:")
    for category, count in categories.items():
        print(f"   {category}: {count}個")

if __name__ == "__main__":
    main()
