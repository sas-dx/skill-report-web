#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト v5 (ハイブリッド方式)

このスクリプトは以下の機能を提供します：
1. テーブル一覧_拡張版.mdから基本情報・運用特性を読み込み
2. table-details/*.yamlから業務固有定義を読み込み
3. 両者をマージして完全なテーブル定義書を生成
4. 実行可能なDDLを生成

使用方法:
    python create_table_definitions_v5.py
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

class TableDefinitionGeneratorV5:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.table_list_file = self.base_dir / "テーブル一覧_拡張版.md"
        self.details_dir = self.base_dir / "table-details"
        self.output_dir = self.base_dir / "tables"
        self.ddl_output_dir = self.base_dir / "ddl"
        
        # 出力ディレクトリを作成
        self.output_dir.mkdir(exist_ok=True)
        self.ddl_output_dir.mkdir(exist_ok=True)
        
        # 共通カラム定義
        self.common_columns = [
            {
                'name': 'id',
                'logical': 'ID',
                'type': 'VARCHAR',
                'length': 50,
                'null': False,
                'pk': True,
                'description': '主キー'
            },
            {
                'name': 'tenant_id',
                'logical': 'テナントID',
                'type': 'VARCHAR',
                'length': 50,
                'null': False,
                'fk': True,
                'description': 'テナントID'
            },
            {
                'name': 'is_active',
                'logical': '有効フラグ',
                'type': 'BOOLEAN',
                'null': False,
                'default': 'TRUE',
                'description': 'レコードが有効かどうか'
            },
            {
                'name': 'created_at',
                'logical': '作成日時',
                'type': 'TIMESTAMP',
                'null': False,
                'default': 'CURRENT_TIMESTAMP',
                'description': 'レコード作成日時'
            },
            {
                'name': 'updated_at',
                'logical': '更新日時',
                'type': 'TIMESTAMP',
                'null': False,
                'default': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                'description': 'レコード更新日時'
            },
            {
                'name': 'created_by',
                'logical': '作成者ID',
                'type': 'VARCHAR',
                'length': 50,
                'null': False,
                'fk': True,
                'description': 'レコード作成者のユーザーID'
            },
            {
                'name': 'updated_by',
                'logical': '更新者ID',
                'type': 'VARCHAR',
                'length': 50,
                'null': False,
                'fk': True,
                'description': 'レコード更新者のユーザーID'
            }
        ]
        
        # 共通インデックス定義
        self.common_indexes = [
            {
                'name': 'PRIMARY',
                'type': 'PRIMARY KEY',
                'columns': ['id'],
                'description': '主キー'
            },
            {
                'name': 'idx_tenant',
                'type': 'INDEX',
                'columns': ['tenant_id'],
                'description': 'テナント検索用'
            },
            {
                'name': 'idx_active',
                'type': 'INDEX',
                'columns': ['is_active'],
                'description': '有効フラグ検索用'
            },
            {
                'name': 'idx_created_at',
                'type': 'INDEX',
                'columns': ['created_at'],
                'description': '作成日時検索用'
            }
        ]

    def load_table_list(self):
        """テーブル一覧_拡張版.mdを読み込み、基本情報を取得"""
        tables = {}
        
        if not self.table_list_file.exists():
            print(f"エラー: {self.table_list_file} が見つかりません")
            return tables
            
        with open(self.table_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # テーブル情報を抽出（拡張版フォーマット対応）
        table_pattern = r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|'
        
        matches = re.findall(table_pattern, content)
        
        for match in matches:
            if len(match) >= 21 and not match[0].strip().startswith('テーブルID'):
                table_id = match[0].strip()
                category = match[1].strip()
                table_name = match[2].strip()
                logical_name = match[3].strip()
                function_category = match[4].strip()
                related_api = match[5].strip()
                related_batch = match[6].strip()
                priority = match[7].strip()
                # データ量情報は8-11をスキップ
                # パフォーマンス情報は12-15をスキップ
                personal_info = match[16].strip()
                confidential_level = match[17].strip()
                encryption_required = match[18].strip()
                # アーカイブ条件は19をスキップ
                description = match[20].strip()
                status = "運用中"  # デフォルト値
                
                tables[table_name] = {
                    'table_id': table_id,
                    'table_name': table_name,
                    'logical_name': logical_name,
                    'category': category,
                    'function_category': function_category,
                    'priority': priority,
                    'personal_info': personal_info,
                    'confidential_level': confidential_level,
                    'encryption_required': encryption_required,
                    'status': status,
                    'related_api': related_api,
                    'related_batch': related_batch,
                    'description': description
                }
        
        return tables

    def load_table_details(self, table_name):
        """指定されたテーブルの詳細定義YAMLファイルを読み込み"""
        details_file = self.details_dir / f"{table_name}_details.yaml"
        
        if not details_file.exists():
            print(f"警告: {details_file} が見つかりません。基本定義のみで生成します。")
            return None
            
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                details = yaml.safe_load(f)
            return details
        except Exception as e:
            print(f"エラー: {details_file} の読み込みに失敗しました: {e}")
            return None

    def merge_column_definitions(self, table_details):
        """共通カラムと業務固有カラムをマージ"""
        merged_columns = []
        
        # 共通カラムを追加
        for i, common_col in enumerate(self.common_columns, 1):
            col_def = {
                'no': i,
                'name': common_col['name'],
                'logical': common_col['logical'],
                'type': common_col['type'],
                'length': common_col.get('length', '-'),
                'null': '×' if not common_col['null'] else '○',
                'pk': '○' if common_col.get('pk', False) else '-',
                'fk': '○' if common_col.get('fk', False) else '-',
                'default': common_col.get('default', '-'),
                'description': common_col['description']
            }
            merged_columns.append(col_def)
        
        # 業務固有カラムを追加
        if table_details and 'business_columns' in table_details:
            start_no = len(merged_columns) + 1
            for i, business_col in enumerate(table_details['business_columns'], start_no):
                col_def = {
                    'no': i,
                    'name': business_col['name'],
                    'logical': business_col['logical'],
                    'type': business_col['type'],
                    'length': business_col.get('length', '-'),
                    'null': '×' if not business_col.get('null', True) else '○',
                    'pk': '-',
                    'fk': '○' if business_col.get('name', '').endswith('_id') else '-',
                    'default': business_col.get('default', '-'),
                    'description': business_col['description']
                }
                merged_columns.append(col_def)
        
        return merged_columns

    def merge_index_definitions(self, table_details):
        """共通インデックスと業務固有インデックスをマージ"""
        merged_indexes = []
        
        # 共通インデックスを追加
        for common_idx in self.common_indexes:
            idx_def = {
                'name': common_idx['name'],
                'type': common_idx['type'],
                'columns': ', '.join(common_idx['columns']),
                'description': common_idx['description']
            }
            merged_indexes.append(idx_def)
        
        # 業務固有インデックスを追加
        if table_details and 'business_indexes' in table_details:
            for business_idx in table_details['business_indexes']:
                idx_def = {
                    'name': business_idx['name'],
                    'type': 'UNIQUE INDEX' if business_idx.get('unique', False) else 'INDEX',
                    'columns': ', '.join(business_idx['columns']),
                    'description': business_idx['description']
                }
                merged_indexes.append(idx_def)
        
        return merged_indexes

    def generate_ddl(self, table_info, columns, indexes, table_details):
        """DDLを生成"""
        table_name = table_info['table_name']
        logical_name = table_info['logical_name']
        
        ddl_lines = []
        ddl_lines.append(f"-- {logical_name}テーブル作成DDL")
        ddl_lines.append(f"CREATE TABLE {table_name} (")
        
        # カラム定義
        column_lines = []
        for col in columns:
            col_line = f"    {col['name']}"
            
            # データ型
            if col['length'] != '-' and col['length'] is not None:
                col_line += f" {col['type']}({col['length']})"
            else:
                col_line += f" {col['type']}"
            
            # NULL制約
            if col['null'] == '×':
                col_line += " NOT NULL"
            
            # デフォルト値
            if col['default'] != '-':
                col_line += f" DEFAULT {col['default']}"
            
            # コメント
            col_line += f" COMMENT '{col['logical']}'"
            
            column_lines.append(col_line)
        
        ddl_lines.extend([line + "," for line in column_lines[:-1]])
        ddl_lines.append(column_lines[-1] + ",")
        
        # 主キー
        ddl_lines.append("    PRIMARY KEY (id),")
        
        # インデックス
        for idx in indexes:
            if idx['name'] != 'PRIMARY':
                if idx['type'] == 'UNIQUE INDEX':
                    ddl_lines.append(f"    UNIQUE INDEX {idx['name']} ({idx['columns']}),")
                elif idx['type'] == 'INDEX':
                    ddl_lines.append(f"    INDEX {idx['name']} ({idx['columns']}),")
        
        # 外部キー制約
        if table_details and 'foreign_keys' in table_details:
            for fk in table_details['foreign_keys']:
                fk_line = f"    CONSTRAINT {fk['name']} FOREIGN KEY ({fk['column']}) "
                fk_line += f"REFERENCES {fk['reference_table']}({fk['reference_column']}) "
                fk_line += f"ON UPDATE {fk['on_update']} ON DELETE {fk['on_delete']},"
                ddl_lines.append(fk_line)
        
        # 最後のカンマを削除
        if ddl_lines[-1].endswith(','):
            ddl_lines[-1] = ddl_lines[-1][:-1]
        
        ddl_lines.append(f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='{logical_name}';")
        ddl_lines.append("")
        
        return '\n'.join(ddl_lines)

    def generate_table_definition(self, table_info, table_details):
        """テーブル定義書を生成"""
        table_name = table_info['table_name']
        logical_name = table_info['logical_name']
        
        # カラム定義をマージ
        columns = self.merge_column_definitions(table_details)
        
        # インデックス定義をマージ
        indexes = self.merge_index_definitions(table_details)
        
        # DDLを生成
        ddl = self.generate_ddl(table_info, columns, indexes, table_details)
        
        # テーブル定義書のマークダウンを生成
        md_content = f"""# テーブル定義書：{table_name}（{logical_name}）

## 1. 基本情報

| 項目 | 内容 |
|------|------|
| **テーブルID** | {table_info['table_id']} |
| **テーブル名** | {table_name} |
| **論理名** | {logical_name} |
| **カテゴリ** | {table_info['category']} |
| **機能カテゴリ** | {table_info['function_category']} |
| **優先度** | {table_info['priority']} |
| **個人情報含有** | {table_info['personal_info']} |
| **機密情報レベル** | {table_info['confidential_level']} |
| **暗号化要否** | {table_info['encryption_required']} |
| **ステータス** | {table_info['status']} |
| **作成日** | {datetime.now().strftime('%Y-%m-%d')} |
| **最終更新日** | {datetime.now().strftime('%Y-%m-%d')} |

## 2. テーブル概要

### 2.1 概要・目的
{table_details.get('overview', table_info['description']) if table_details else table_info['description']}
"""

        # 詳細定義がある場合は追加情報を含める
        if table_details:
            if 'notes' in table_details:
                md_content += f"""
### 2.2 特記事項
"""
                for note in table_details['notes']:
                    md_content += f"- {note}\n"

        md_content += f"""
### 2.3 関連API
{table_info['related_api']}

### 2.4 関連バッチ
{table_info['related_batch']}

## 3. テーブル構造

### 3.1 カラム定義

| No | カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト値 | 説明 |
|----|----------|--------|----------|------|------|----|----|--------------|------|
"""

        # カラム定義テーブル
        for col in columns:
            md_content += f"| {col['no']} | {col['name']} | {col['logical']} | {col['type']} | {col['length']} | {col['null']} | {col['pk']} | {col['fk']} | {col['default']} | {col['description']} |\n"

        md_content += f"""

### 3.2 インデックス定義

| インデックス名 | 種別 | カラム | 説明 |
|----------------|------|--------|------|
"""

        # インデックス定義テーブル
        for idx in indexes:
            md_content += f"| {idx['name']} | {idx['type']} | {idx['columns']} | {idx['description']} |\n"

        # 制約定義
        md_content += f"""

### 3.3 制約定義

| 制約名 | 制約種別 | カラム | 制約内容 |
|--------|----------|--------|----------|
| pk_{table_name.lower()} | PRIMARY KEY | id | 主キー制約 |
| fk_created_by | FOREIGN KEY | created_by | MST_UserAuth.user_id |
| fk_updated_by | FOREIGN KEY | updated_by | MST_UserAuth.user_id |
"""

        # 業務固有制約を追加
        if table_details and 'business_constraints' in table_details:
            for constraint in table_details['business_constraints']:
                columns_str = ', '.join(constraint.get('columns', [constraint.get('column', '')]))
                condition = constraint.get('condition', constraint.get('columns', ''))
                md_content += f"| {constraint['name']} | {constraint['type']} | {columns_str} | {condition} |\n"

        # リレーション情報
        md_content += f"""

## 4. リレーション

### 4.1 親テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| MST_UserAuth | created_by, updated_by | 1:N | ユーザー情報 |
"""

        # 業務固有の外部キーを追加
        if table_details and 'foreign_keys' in table_details:
            for fk in table_details['foreign_keys']:
                md_content += f"| {fk['reference_table']} | {fk['column']} | 1:N | {fk['description']} |\n"

        md_content += f"""

### 4.2 子テーブル
| テーブル名 | 関連カラム | カーディナリティ | 説明 |
|------------|------------|------------------|------|
| - | - | - | 必要に応じて追加 |

## 5. データ仕様

### 5.1 データ例
```sql
-- サンプルデータ
"""

        # サンプルデータを追加
        if table_details and 'sample_data' in table_details and table_details['sample_data']:
            sample = table_details['sample_data'][0]
            columns_list = ['id', 'tenant_id'] + list(sample.keys()) + ['created_by', 'updated_by']
            values_list = ["'sample_001'", "'tenant_001'"] + [f"'{v}'" if v is not None else 'NULL' for v in sample.values()] + ["'user_admin'", "'user_admin'"]
            
            md_content += f"""INSERT INTO {table_name} (
    {', '.join(columns_list)}
) VALUES (
    {', '.join(values_list)}
);
"""
        else:
            md_content += f"""INSERT INTO {table_name} (
    id, tenant_id, created_by, updated_by
) VALUES (
    'sample_001', 'tenant_001', 'user_admin', 'user_admin'
);
"""

        md_content += f"""```

### 5.2 データ量見積もり
| 項目 | 値 | 備考 |
|------|----|----- |
| 初期データ件数 | 500件 | 初期設定データ |
| 月間増加件数 | 100件 | 想定値 |
| 年間増加件数 | 1,200件 | 想定値 |
| 5年後想定件数 | 6,500件 | 想定値 |

## 6. 運用仕様

### 6.1 バックアップ
- 日次バックアップ：毎日2:00実行
- 週次バックアップ：毎週日曜日3:00実行

### 6.2 パーティション
- パーティション種別：なし
- パーティション条件：-

### 6.3 アーカイブ
- アーカイブ条件：作成から3年経過
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
- SELECT：15ms以内
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
{ddl}
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
   - 関連画面情報

5. **データ量・パフォーマンス監視**
   - データ量が想定の150%を超えた場合はアラート
   - 応答時間が設定値の120%を超えた場合は調査
"""

        # 業務ルールを追加
        if table_details and 'business_rules' in table_details:
            md_content += f"""

## 11. 業務ルール

"""
            for rule in table_details['business_rules']:
                md_content += f"- {rule}\n"

        return md_content, ddl

    def generate_all_definitions(self):
        """すべてのテーブル定義書を生成"""
        print("テーブル一覧を読み込み中...")
        tables = self.load_table_list()
        
        if not tables:
            print("テーブル情報が見つかりませんでした。")
            return
        
        print(f"{len(tables)}個のテーブルが見つかりました。")
        
        generated_count = 0
        ddl_all = []
        
        for table_name, table_info in tables.items():
            print(f"\n処理中: {table_name} ({table_info['logical_name']})")
            
            # 詳細定義を読み込み
            table_details = self.load_table_details(table_name)
            
            # テーブル定義書を生成
            md_content, ddl = self.generate_table_definition(table_info, table_details)
            
            # ファイルに保存
            output_file = self.output_dir / f"テーブル定義書_{table_name}_{table_info['logical_name']}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            # DDLを保存
            ddl_file = self.ddl_output_dir / f"{table_name}.sql"
            with open(ddl_file, 'w', encoding='utf-8') as f:
                f.write(ddl)
            
            ddl_all.append(ddl)
            generated_count += 1
            
            print(f"  ✓ {output_file}")
            print(f"  ✓ {ddl_file}")
        
        # 全DDLをまとめたファイルを作成
        all_ddl_file = self.ddl_output_dir / "all_tables.sql"
        with open(all_ddl_file, 'w', encoding='utf-8') as f:
            f.write("-- 全テーブル作成DDL\n")
            f.write(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write('\n'.join(ddl_all))
        
        print(f"\n✅ 生成完了: {generated_count}個のテーブル定義書を生成しました。")
        print(f"📁 出力先: {self.output_dir}")
        print(f"📁 DDL出力先: {self.ddl_output_dir}")
        print(f"📄 統合DDL: {all_ddl_file}")

def main():
    """メイン処理"""
    print("🚀 テーブル定義書生成スクリプト v5 (ハイブリッド方式)")
    print("=" * 60)
    
    generator = TableDefinitionGeneratorV5()
    generator.generate_all_definitions()
    
    print("\n🎉 処理が完了しました！")

if __name__ == "__main__":
    main()
