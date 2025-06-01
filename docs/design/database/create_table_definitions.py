#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト

改版履歴:
┌─────────┬────────────┬──────────┬─────────────────────────────────────────────────────┐
│ バージョン │    更新日    │  更新者  │                  主な変更内容                       │
├─────────┼────────────┼──────────┼─────────────────────────────────────────────────────┤
│  v1.0   │ 2024-11-XX │ 開発者   │ 初版作成・基本的なテーブル定義書生成機能            │
│  v2.0   │ 2024-11-XX │ 開発者   │ 基本構造の確立・共通カラム定義の実装                │
│  v3.0   │ 2024-12-XX │ 開発者   │ YAML詳細定義ファイル対応・設定駆動化                │
│  v4.0   │ 2024-12-XX │ 開発者   │ インデックス・制約定義対応・外部キー関係追加        │
│  v5.0   │ 2024-12-XX │ 開発者   │ 改版履歴機能追加・サンプルデータ対応                │
│  v6.0   │ 2025-01-XX │ 開発者   │ DDL生成機能追加・統合DDL対応・エラーハンドリング強化│
│  v7.0   │ 2025-05-XX │ 開発者   │ レイアウト改良・PK/FK表示・桁数情報追加             │
│  v8.0   │ 2025-06-01 │ システム │ 全テーブル定義書再生成・ファイル命名規則統一        │
└─────────┴────────────┴──────────┴─────────────────────────────────────────────────────┘

機能概要:
- テーブル一覧.mdからテーブル情報を自動読み込み
- YAML詳細定義ファイルとの連携
- テーブル定義書（Markdown）の自動生成
- DDLファイルの自動生成
- 統合DDLファイルの作成
- コマンドライン引数による柔軟な実行制御
"""

import os
import re
import sys
import yaml
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class TableDefinitionGenerator:
    """テーブル定義書生成クラス"""
    
    def __init__(self, base_dir: str = None):
        """初期化"""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.tables_dir = self.base_dir / "tables"
        self.ddl_dir = self.base_dir / "ddl"
        self.details_dir = self.base_dir / "table-details"
        self.table_list_file = self.base_dir / "テーブル一覧.md"
        
        # ディレクトリ作成
        self.tables_dir.mkdir(exist_ok=True)
        self.ddl_dir.mkdir(exist_ok=True)
        self.details_dir.mkdir(exist_ok=True)
        
        # テーブル情報
        self.tables_info = {}
        self.common_columns = self._get_common_columns()
        
    def _get_common_columns(self) -> Dict[str, Any]:
        """共通カラム定義を取得"""
        return {
            'audit_columns': [
                {
                    'name': 'created_at',
                    'logical': '作成日時',
                    'type': 'TIMESTAMP',
                    'length': None,
                    'null': False,
                    'default': 'CURRENT_TIMESTAMP',
                    'description': 'レコード作成日時'
                },
                {
                    'name': 'updated_at',
                    'logical': '更新日時',
                    'type': 'TIMESTAMP',
                    'length': None,
                    'null': False,
                    'default': 'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP',
                    'description': 'レコード更新日時'
                },
                {
                    'name': 'created_by',
                    'logical': '作成者',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'description': 'レコード作成者のユーザーID'
                },
                {
                    'name': 'updated_by',
                    'logical': '更新者',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'description': 'レコード更新者のユーザーID'
                }
            ],
            'tenant_columns': [
                {
                    'name': 'tenant_id',
                    'logical': 'テナントID',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'description': 'マルチテナント識別子'
                }
            ],
            'base_columns': [
                {
                    'name': 'id',
                    'logical': 'ID',
                    'type': 'VARCHAR',
                    'length': 50,
                    'null': False,
                    'primary': True,
                    'description': 'プライマリキー（UUID）'
                },
                {
                    'name': 'is_deleted',
                    'logical': '削除フラグ',
                    'type': 'BOOLEAN',
                    'length': None,
                    'null': False,
                    'default': False,
                    'description': '論理削除フラグ'
                }
            ]
        }
    
    def _get_column_length(self, column: Dict) -> str:
        """カラムの桁数を取得"""
        length = column.get('length')
        if length is None:
            return ""
        return str(length)
    
    def _is_primary_key(self, column_name: str, column: Dict) -> str:
        """プライマリキー判定"""
        if column.get('primary', False):
            return "●"
        return ""
    
    def _is_foreign_key(self, column_name: str, foreign_keys: List) -> str:
        """外部キー判定"""
        if not foreign_keys:
            return ""
        
        for fk in foreign_keys:
            if fk.get('column') == column_name:
                return "●"
        return ""
    
    def _format_column_row(self, column: Dict, foreign_keys: List = None) -> str:
        """カラム行をフォーマット"""
        name = column['name']
        logical = column['logical']
        col_type = column['type']
        length = self._get_column_length(column)
        null_str = "○" if column.get('null', True) else "×"
        pk_str = self._is_primary_key(name, column)
        fk_str = self._is_foreign_key(name, foreign_keys or [])
        default_str = str(column.get('default', '')) if column.get('default') else ''
        description = column['description']
        
        return f"| {name} | {logical} | {col_type} | {length} | {null_str} | {pk_str} | {fk_str} | {default_str} | {description} |"
    
    def load_table_list(self) -> Dict[str, Dict[str, Any]]:
        """テーブル一覧.mdからテーブル情報を読み込み"""
        if not self.table_list_file.exists():
            raise FileNotFoundError(f"テーブル一覧ファイルが見つかりません: {self.table_list_file}")
        
        with open(self.table_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # テーブル情報を抽出
        tables = {}
        table_pattern = r'\|\s*\[([^\]]+)\]\([^\)]+\)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
        
        for match in re.finditer(table_pattern, content):
            table_id = match.group(1).strip()
            category = match.group(2).strip()
            table_name = match.group(3).strip()
            logical_name = match.group(4).strip()
            
            tables[table_name] = {
                'table_id': table_id,
                'category': category,
                'logical_name': logical_name,
                'table_name': table_name
            }
        
        return tables
    
    def load_table_details(self, table_name: str) -> Optional[Dict[str, Any]]:
        """テーブル詳細定義YAMLを読み込み"""
        details_file = self.details_dir / f"{table_name}_details.yaml"
        
        if not details_file.exists():
            print(f"警告: {details_file} が見つかりません。基本定義のみで生成します。")
            return None
        
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"エラー: {details_file} の読み込みに失敗しました: {e}")
            return None
    
    def generate_table_definition(self, table_name: str, table_info: Dict[str, Any]) -> str:
        """テーブル定義書を生成"""
        details = self.load_table_details(table_name)
        logical_name = table_info['logical_name']
        category = table_info['category']
        
        # 外部キー情報を取得
        foreign_keys = details.get('foreign_keys', []) if details else []
        
        # 改版履歴の取得
        revision_history = ""
        if details and 'revision_history' in details:
            revision_history = self._format_revision_history(details['revision_history'])
        
        # 基本情報
        md_content = f"""# テーブル定義書: {table_name} ({logical_name})

## 📋 基本情報

| 項目 | 内容 |
|------|------|
| テーブル名 | {table_name} |
| 論理名 | {logical_name} |
| カテゴリ | {category} |
| 作成日 | {datetime.now().strftime('%Y-%m-%d')} |

> **注意**: 本テーブル定義書は自動生成されます。手動編集は行わないでください。
> 詳細定義の変更は `table-details/{table_name}_details.yaml` で行ってください。

{revision_history}

## 📝 テーブル概要

"""
        
        # 概要の追加
        if details and 'overview' in details:
            md_content += details['overview'] + "\n\n"
        else:
            md_content += f"{logical_name}テーブルの詳細定義です。\n\n"
        
        # カラム定義（v7レイアウト）
        md_content += "## 🗂️ カラム定義\n\n"
        md_content += "| カラム名 | 論理名 | データ型 | 桁数 | NULL | PK | FK | デフォルト | 説明 |\n"
        md_content += "|----------|--------|----------|------|------|----|----|------------|------|\n"
        
        # 基本カラム
        for col in self.common_columns['base_columns']:
            md_content += self._format_column_row(col, foreign_keys) + "\n"
        
        # テナントカラム（マルチテナント対応テーブルの場合）
        if not table_name.startswith('SYS_'):
            for col in self.common_columns['tenant_columns']:
                md_content += self._format_column_row(col, foreign_keys) + "\n"
        
        # 業務固有カラム
        if details and 'business_columns' in details:
            for col in details['business_columns']:
                md_content += self._format_column_row(col, foreign_keys) + "\n"
        
        # 監査カラム
        for col in self.common_columns['audit_columns']:
            md_content += self._format_column_row(col, foreign_keys) + "\n"
        
        # インデックス定義
        if details and 'business_indexes' in details:
            md_content += "\n## 🔍 インデックス定義\n\n"
            md_content += "| インデックス名 | カラム | ユニーク | 説明 |\n"
            md_content += "|----------------|--------|----------|------|\n"
            for idx in details['business_indexes']:
                unique_str = "○" if idx.get('unique', False) else "×"
                columns_str = ", ".join(idx['columns'])
                md_content += f"| {idx['name']} | {columns_str} | {unique_str} | {idx['description']} |\n"
        
        # 制約定義
        if details and 'business_constraints' in details:
            md_content += "\n## 🔒 制約定義\n\n"
            md_content += "| 制約名 | 制約タイプ | 対象カラム | 条件 | 説明 |\n"
            md_content += "|--------|------------|------------|------|------|\n"
            for constraint in details['business_constraints']:
                columns_str = ", ".join(constraint.get('columns', []))
                condition_str = constraint.get('condition', '')
                md_content += f"| {constraint['name']} | {constraint['type']} | {columns_str} | {condition_str} | {constraint['description']} |\n"
        
        # 外部キー関係
        if details and 'foreign_keys' in details:
            md_content += "\n## 🔗 外部キー関係\n\n"
            md_content += "| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |\n"
            md_content += "|------------|--------|--------------|------------|--------|--------|------|\n"
            for fk in details['foreign_keys']:
                md_content += f"| {fk['name']} | {fk['column']} | {fk['reference_table']} | {fk['reference_column']} | {fk['on_update']} | {fk['on_delete']} | {fk['description']} |\n"
        
        # サンプルデータ
        if details and 'sample_data' in details:
            md_content += "\n## 📊 サンプルデータ\n\n"
            md_content += "```json\n"
            md_content += json.dumps(details['sample_data'], ensure_ascii=False, indent=2)
            md_content += "\n```\n"
        
        # 特記事項
        if details and 'notes' in details:
            md_content += "\n## 📌 特記事項\n\n"
            for note in details['notes']:
                md_content += f"- {note}\n"
        
        # 業務ルール
        if details and 'business_rules' in details:
            md_content += "\n## 📋 業務ルール\n\n"
            for rule in details['business_rules']:
                md_content += f"- {rule}\n"
        
        return md_content
    
    def _format_revision_history(self, history: List[Dict[str, str]]) -> str:
        """改版履歴をフォーマット"""
        if not history:
            return ""
        
        content = "\n## 📝 改版履歴\n\n"
        content += "> **注意**: 改版履歴の詳細は以下のYAMLファイルで管理されています：\n"
        content += f"> `table-details/{history[0].get('table_name', 'TABLE_NAME')}_details.yaml`\n\n"
        content += "| バージョン | 更新日 | 更新者 | 主な変更内容 |\n"
        content += "|------------|--------|--------|-------------|\n"
        
        # 最新版から順に表示
        for item in sorted(history, key=lambda x: x.get('version', ''), reverse=True):
            content += f"| {item.get('version', '')} | {item.get('date', '')} | {item.get('author', '')} | {item.get('changes', '')} |\n"
        
        return content
    
    def generate_ddl(self, table_name: str, table_info: Dict[str, Any]) -> str:
        """DDLを生成"""
        details = self.load_table_details(table_name)
        
        ddl_content = f"-- {table_name} ({table_info['logical_name']}) DDL\n"
        ddl_content += f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # テーブル作成
        ddl_content += f"CREATE TABLE {table_name} (\n"
        
        columns = []
        
        # 基本カラム
        for col in self.common_columns['base_columns']:
            col_type = col['type']
            if col.get('length'):
                col_type += f"({col['length']})"
            
            col_def = f"    {col['name']} {col_type}"
            if not col.get('null', True):
                col_def += " NOT NULL"
            if col.get('default') is not None:
                if isinstance(col['default'], str):
                    col_def += f" DEFAULT '{col['default']}'"
                else:
                    col_def += f" DEFAULT {col['default']}"
            if col.get('primary'):
                col_def += " PRIMARY KEY"
            columns.append(col_def)
        
        # テナントカラム
        if not table_name.startswith('SYS_'):
            for col in self.common_columns['tenant_columns']:
                col_type = col['type']
                if col.get('length'):
                    col_type += f"({col['length']})"
                
                col_def = f"    {col['name']} {col_type}"
                if not col.get('null', True):
                    col_def += " NOT NULL"
                columns.append(col_def)
        
        # 業務固有カラム
        if details and 'business_columns' in details:
            for col in details['business_columns']:
                col_type = col['type']
                if col.get('length'):
                    col_type += f"({col['length']})"
                
                col_def = f"    {col['name']} {col_type}"
                if not col.get('null', True):
                    col_def += " NOT NULL"
                if col.get('default') is not None:
                    if isinstance(col['default'], str):
                        col_def += f" DEFAULT '{col['default']}'"
                    else:
                        col_def += f" DEFAULT {col['default']}"
                columns.append(col_def)
        
        # 監査カラム
        for col in self.common_columns['audit_columns']:
            col_type = col['type']
            if col.get('length'):
                col_type += f"({col['length']})"
            
            col_def = f"    {col['name']} {col_type}"
            if not col.get('null', True):
                col_def += " NOT NULL"
            if col.get('default'):
                col_def += f" DEFAULT {col['default']}"
            columns.append(col_def)
        
        ddl_content += ",\n".join(columns)
        ddl_content += "\n);\n\n"
        
        # インデックス作成
        if details and 'business_indexes' in details:
            for idx in details['business_indexes']:
                unique_str = "UNIQUE " if idx.get('unique', False) else ""
                columns_str = ", ".join(idx['columns'])
                ddl_content += f"CREATE {unique_str}INDEX {idx['name']} ON {table_name} ({columns_str});\n"
        
        # 外部キー制約
        if details and 'foreign_keys' in details:
            ddl_content += "\n-- 外部キー制約\n"
            for fk in details['foreign_keys']:
                ddl_content += f"ALTER TABLE {table_name} ADD CONSTRAINT {fk['name']} "
                ddl_content += f"FOREIGN KEY ({fk['column']}) REFERENCES {fk['reference_table']}({fk['reference_column']}) "
                ddl_content += f"ON UPDATE {fk['on_update']} ON DELETE {fk['on_delete']};\n"
        
        return ddl_content
    
    def generate_files(self, table_names: List[str] = None, output_dir: str = None):
        """ファイル生成メイン処理"""
        # テーブル一覧読み込み
        self.tables_info = self.load_table_list()
        
        # 出力先ディレクトリ設定
        if output_dir:
            output_path = Path(output_dir)
            tables_output = output_path / "tables"
            ddl_output = output_path / "ddl"
            tables_output.mkdir(parents=True, exist_ok=True)
            ddl_output.mkdir(parents=True, exist_ok=True)
        else:
            tables_output = self.tables_dir
            ddl_output = self.ddl_dir
        
        # 処理対象テーブル決定
        if table_names:
            target_tables = {name: info for name, info in self.tables_info.items() if name in table_names}
            missing_tables = set(table_names) - set(self.tables_info.keys())
            if missing_tables:
                print(f"警告: 以下のテーブルが見つかりません: {', '.join(missing_tables)}")
        else:
            target_tables = self.tables_info
        
        print(f"🚀 テーブル定義書生成スクリプト v8.0 (統一版)")
        print("=" * 80)
        print(f"{len(target_tables)}個のテーブルを処理します。")
        print()
        
        generated_ddls = []
        
        for table_name, table_info in target_tables.items():
            print(f"処理中: {table_name} ({table_info['logical_name']})")
            
            try:
                # テーブル定義書生成
                md_content = self.generate_table_definition(table_name, table_info)
                md_file = tables_output / f"テーブル定義書_{table_name}_{table_info['logical_name']}.md"
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                print(f"  ✓ {md_file}")
                
                # DDL生成
                ddl_content = self.generate_ddl(table_name, table_info)
                ddl_file = ddl_output / f"{table_name}.sql"
                
                with open(ddl_file, 'w', encoding='utf-8') as f:
                    f.write(ddl_content)
                print(f"  ✓ {ddl_file}")
                
                generated_ddls.append(ddl_content)
                
            except Exception as e:
                print(f"  ❌ エラー: {e}")
        
        # 統合DDL生成
        if generated_ddls:
            all_ddl_file = ddl_output / "all_tables.sql"
            with open(all_ddl_file, 'w', encoding='utf-8') as f:
                f.write("-- 全テーブル統合DDL\n")
                f.write(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("\n\n".join(generated_ddls))
            print(f"\n✅ 統合DDL: {all_ddl_file}")
        
        print(f"\n🎉 処理が完了しました！")
        print(f"📁 テーブル定義書出力先: {tables_output}")
        print(f"📁 DDL出力先: {ddl_output}")

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="テーブル定義書生成スクリプト v8.0 (統一版)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全テーブル生成
  python3 create_table_definitions.py
  
  # 個別テーブル生成
  python3 create_table_definitions.py --table MST_Employee
  python3 create_table_definitions.py --table MST_Role,MST_Permission
  
  # カテゴリ別生成
  python3 create_table_definitions.py --category マスタ系
  
  # 出力先指定
  python3 create_table_definitions.py --table MST_Employee --output-dir custom/
        """
    )
    
    parser.add_argument(
        '--table', '-t',
        help='生成対象テーブル名（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--category', '-c',
        help='生成対象カテゴリ（マスタ系、トランザクション系等）'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        help='出力先ディレクトリ'
    )
    
    parser.add_argument(
        '--base-dir', '-b',
        help='ベースディレクトリ（デフォルト: スクリプトのディレクトリ）'
    )
    
    args = parser.parse_args()
    
    try:
        generator = TableDefinitionGenerator(args.base_dir)
        
        # 対象テーブル決定
        target_tables = None
        
        if args.table:
            target_tables = [t.strip() for t in args.table.split(',')]
        elif args.category:
            # カテゴリ別フィルタリング（実装簡略化のため、今回は省略）
            print(f"カテゴリ別生成機能は今後実装予定です: {args.category}")
            return
        
        generator.generate_files(target_tables, args.output_dir)
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
