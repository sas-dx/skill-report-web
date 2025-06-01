#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書一括再作成スクリプト v4.0 (修正版)
テーブル一覧_拡張版.mdから動的にデータを読み込み、
データ量見積もり、パフォーマンス要件、運用特性を反映
命名規則: テーブル定義書_テーブル名_論理名.md
"""

import os
import re
from datetime import datetime
from typing import List, Dict, Optional

def parse_extended_table_list_md(file_path: str) -> List[Dict[str, str]]:
    """
    テーブル一覧_拡張版.mdを解析してテーブル情報を抽出
    
    Args:
        file_path: テーブル一覧_拡張版.mdのファイルパス
        
    Returns:
        テーブル情報のリスト
    """
    tables = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 正規表現でテーブル行を直接抽出
        # TBL-で始まるテーブルIDを含む行を検索
        table_pattern = r'\|\s*(TBL-\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        
        matches = re.findall(table_pattern, content, re.MULTILINE)
        
        for match in matches:
            if len(match) >= 21:
                table_id = match[0].strip()
                category = match[1].strip()
                table_name = match[2].strip()
                logical_name = match[3].strip()
                
                # カテゴリの正規化
                if 'トランザクション' in category:
                    category = 'トランザクション系'
                elif 'マスタ' in category:
                    category = 'マスタ系'
                elif 'システム' in category:
                    category = 'システム系'
                elif '履歴' in category:
                    category = '履歴系'
                elif 'ワーク' in category:
                    category = 'ワーク系'
                
                table_info = {
                    'id': table_id,
                    'table_name': table_name,
                    'logical_name': logical_name,
                    'category': category,
                    'function_category': match[4].strip() if len(match) > 4 else '',
                    'api_ids': match[5].strip() if len(match) > 5 else '',
                    'batch_ids': match[6].strip() if len(match) > 6 else '',
                    'priority': match[7].strip() if len(match) > 7 else '中',
                    'initial_data_count': match[8].strip() if len(match) > 8 else '10件',
                    'monthly_increase': match[9].strip() if len(match) > 9 else '100件',
                    'yearly_increase': match[10].strip() if len(match) > 10 else '1,200件',
                    'five_year_estimate': match[11].strip() if len(match) > 11 else '6,010件',
                    'select_response_time': match[12].strip() if len(match) > 12 else '10ms以内',
                    'insert_response_time': match[13].strip() if len(match) > 13 else '50ms以内',
                    'update_response_time': match[14].strip() if len(match) > 14 else '50ms以内',
                    'delete_response_time': match[15].strip() if len(match) > 15 else '100ms以内',
                    'personal_info': match[16].strip() if len(match) > 16 else 'なし',
                    'confidential_level': match[17].strip() if len(match) > 17 else '低',
                    'encryption_required': match[18].strip() if len(match) > 18 else '不要',
                    'archive_condition': match[19].strip() if len(match) > 19 else '無効化から3年経過',
                    'screens': match[20].strip() if len(match) > 20 else ''
                }
                
                tables.append(table_info)
                print(f"   解析: {table_id} - {table_name} ({logical_name})")
    
    except FileNotFoundError:
        print(f"❌ エラー: ファイルが見つかりません: {file_path}")
        return []
    except Exception as e:
        print(f"❌ エラー: ファイル解析中にエラーが発生しました: {e}")
        return []
    
    return tables

def generate_enhanced_table_definition(table_info: Dict[str, str]) -> str:
    """拡張版テーブル定義書を生成"""
    
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
    
    # 暗号化設定
    encryption_note = ""
    if table_info['encryption_required'] == '要':
        encryption_note = "\n- **暗号化**: 個人情報・機密情報を含むため、カラムレベル暗号化を実施"
    
    # インデックス定義（テーブル特性に応じて調整）
    index_rows = """| PRIMARY | PRIMARY KEY | id | 主キー |
| idx_created_at | INDEX | created_at | 作成日時検索用 |"""
    
    if not table_info["table_name"].startswith("SYS_") and not table_info["table_name"].startswith("HIS_"):
        index_rows += "\n| idx_tenant | INDEX | tenant_id | テナント検索用 |"
    
    if table_info["category"] == "マスタ系":
        index_rows += "\n| idx_active | INDEX | is_active | 有効フラグ検索用 |"
    
    template = f"""# テーブル定義書：{table_info['table_name']}（{table_info['logical_name']}）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | {table_info['id']} |
| **テーブル名** | {table_info['table_name']} |
| **論理名** | {table_info['logical_name']} |
| **カテゴリ** | {table_info['category']} |
| **機能カテゴリ** | {table_info['function_category']} |
| **優先度** | {table_info['priority']} |
| **個人情報含有** | {table_info['personal_info']} |
| **機密情報レベル** | {table_info['confidential_level']} |
| **暗号化要否** | {table_info['encryption_required']} |
| **ステータス** | 運用中 |
| **作成日** | {current_date} |
| **最終更新日** | {current_date} |

## 2. テーブル概要

### 2.1 概要・目的
{table_info['table_name']}（{table_info['logical_name']}）は、{category_descriptions.get(table_info['category'], '業務データを管理するテーブルです。')}{encryption_note}

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
{index_rows}

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_{table_info['table_name'].lower()} | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
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
    id, created_by, updated_by
) VALUES (
    'sample_001', 'user_admin', 'user_admin'
);
```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | {table_info['initial_data_count']} | 初期設定データ |
| 月間増加件数 | {table_info['monthly_increase']} | 想定値 |
| 年間増加件数 | {table_info['yearly_increase']} | 想定値 |
| 5年後想定件数 | {table_info['five_year_estimate']} | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：{table_info['archive_condition']}
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
- SELECT：{table_info['select_response_time']}
- INSERT：{table_info['insert_response_time']}
- UPDATE：{table_info['update_response_time']}
- DELETE：{table_info['delete_response_time']}

## 8. セキュリティ

### 8.1 アクセス制御
| ロール | SELECT | INSERT | UPDATE | DELETE | 備考 |
|--------|--------|--------|--------|--------|------|
| system_admin | ○ | ○ | ○ | ○ | システム管理者 |
| tenant_admin | ○ | ○ | ○ | × | テナント管理者（自テナントのみ） |
| user | ○ | × | × | × | 一般ユーザー（参照のみ） |

### 8.2 データ保護
- 個人情報：{table_info['personal_info']}
- 機密情報：{table_info['confidential_level']}レベル
- 暗号化：{table_info['encryption_required']}

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
   - データ量見積もりの定期見直し

3. **今後の拡張予定**
   - 必要に応じて機能拡張を検討

4. **関連画面**
   - {table_info['screens']}

5. **データ量・パフォーマンス監視**
   - データ量が想定の150%を超えた場合はアラート
   - 応答時間が設定値の120%を超えた場合は調査
"""
    
    return template

def main():
    """メイン処理"""
    print("🚀 テーブル定義書一括再作成を開始します（v4.0 - 拡張版対応・修正版）...")
    
    # テーブル一覧_拡張版.mdのパス
    table_list_path = "テーブル一覧_拡張版.md"
    
    # テーブル一覧_拡張版.mdからデータを読み込み
    print("📖 テーブル一覧_拡張版.mdを読み込み中...")
    tables = parse_extended_table_list_md(table_list_path)
    
    if not tables:
        print("❌ エラー: テーブル情報を読み込めませんでした。")
        return
    
    print(f"✅ {len(tables)}個のテーブル情報を読み込みました。")
    
    # 出力ディレクトリの確認
    output_dir = "tables"
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
    for table in tables:
        filename = f"テーブル定義書_{table['table_name']}_{table['logical_name']}.md"
        file_path = os.path.join(output_dir, filename)
        
        # テーブル定義書の内容を生成
        content = generate_enhanced_table_definition(table)
        
        # ファイルに書き込み
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   作成: {filename}")
        created_count += 1
    
    print(f"\n✅ 完了！{created_count}個のテーブル定義書を作成しました。")
    print(f"📁 出力先: {output_dir}")
    
    # 統計情報を表示
    categories = {}
    total_initial = 0
    total_five_year = 0
    
    for table in tables:
        category = table['category']
        if category not in categories:
            categories[category] = 0
        categories[category] += 1
        
        # データ量統計
        try:
            initial = int(table['initial_data_count'].replace('件', '').replace(',', ''))
            five_year = int(table['five_year_estimate'].replace('件', '').replace(',', ''))
            total_initial += initial
            total_five_year += five_year
        except:
            pass
    
    print("\n📊 カテゴリ別統計:")
    for category, count in categories.items():
        print(f"   {category}: {count}個")
    
    print(f"\n📈 データ量統計:")
    print(f"   初期データ総計: {total_initial:,}件")
    print(f"   5年後想定総計: {total_five_year:,}件")
    print(f"   増加率: {((total_five_year - total_initial) / total_initial * 100):.1f}%")
    
    print("\n🎯 v4.0の改善点:")
    print("   ✅ テーブル特性に応じたデータ量見積もり")
    print("   ✅ カテゴリ別パフォーマンス要件")
    print("   ✅ セキュリティレベル別設定")
    print("   ✅ アーカイブ条件の個別設定")
    print("   ✅ 運用監視指標の明確化")

if __name__ == "__main__":
    main()
