#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト v8 (関連エンティティERD自動生成対応版)
- 関連エンティティのMermaid ERD自動生成機能
- 外部キー関係の自動解析
- テーブル定義書への関連エンティティ図統合
- v7の全機能を継承
"""

import os
import re
import sys
import yaml
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple

class ERDGenerator:
    """関連エンティティERD生成クラス"""
    
    def __init__(self, base_dir: Path, tables_info: Dict[str, Any]):
        self.base_dir = base_dir
        self.details_dir = base_dir / "table-details"
        self.tables_info = tables_info
        self.all_foreign_keys = {}
        self.reverse_foreign_keys = {}
        self._build_foreign_key_maps()
    
    def _build_foreign_key_maps(self):
        """全テーブルの外部キー関係マップを構築"""
        for table_name in self.tables_info.keys():
            details = self._load_table_details(table_name)
            if details and 'foreign_keys' in details:
                self.all_foreign_keys[table_name] = details['foreign_keys']
                
                # 逆参照マップも構築
                for fk in details['foreign_keys']:
                    ref_table = fk['reference_table']
                    if ref_table not in self.reverse_foreign_keys:
                        self.reverse_foreign_keys[ref_table] = []
                    self.reverse_foreign_keys[ref_table].append({
                        'from_table': table_name,
                        'from_column': fk['column'],
                        'to_column': fk['reference_column'],
                        'relationship_type': self._determine_relationship_type(fk)
                    })
    
    def _load_table_details(self, table_name: str) -> Optional[Dict[str, Any]]:
        """テーブル詳細定義YAMLを読み込み"""
        details_file = self.details_dir / f"{table_name}_details.yaml"
        if not details_file.exists():
            return None
        
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception:
            return None
    
    def _determine_relationship_type(self, fk: Dict[str, Any]) -> str:
        """外部キー関係のタイプを判定"""
        # 削除時の動作で判定
        on_delete = fk.get('on_delete', 'RESTRICT').upper()
        if on_delete == 'CASCADE':
            return 'composition'  # 強い関連（親が削除されると子も削除）
        elif on_delete == 'SET NULL':
            return 'aggregation'  # 弱い関連（親が削除されても子は残る）
        else:
            return 'association'  # 関連
    
    def analyze_related_tables(self, target_table: str) -> Dict[str, Any]:
        """関連テーブルを解析"""
        related = {
            'direct_references': [],      # 直接参照するテーブル
            'direct_referenced_by': [],   # 直接参照されるテーブル
            'all_related': set(),         # 全関連テーブル
            'relationships': []           # 関係性の詳細
        }
        
        # 直接参照するテーブル（外部キー先）
        if target_table in self.all_foreign_keys:
            for fk in self.all_foreign_keys[target_table]:
                ref_table = fk['reference_table']
                if ref_table != target_table and ref_table in self.tables_info:
                    related['direct_references'].append({
                        'table': ref_table,
                        'column': fk['column'],
                        'ref_column': fk['reference_column'],
                        'relationship_type': self._determine_relationship_type(fk)
                    })
                    related['all_related'].add(ref_table)
        
        # 直接参照されるテーブル（外部キー元）
        if target_table in self.reverse_foreign_keys:
            for ref in self.reverse_foreign_keys[target_table]:
                from_table = ref['from_table']
                if from_table != target_table and from_table in self.tables_info:
                    related['direct_referenced_by'].append({
                        'table': from_table,
                        'column': ref['from_column'],
                        'ref_column': ref['to_column'],
                        'relationship_type': ref['relationship_type']
                    })
                    related['all_related'].add(from_table)
        
        # 関係性の詳細を構築
        for ref in related['direct_references']:
            related['relationships'].append({
                'from': target_table,
                'to': ref['table'],
                'type': ref['relationship_type'],
                'direction': 'outgoing'
            })
        
        for ref in related['direct_referenced_by']:
            related['relationships'].append({
                'from': ref['table'],
                'to': target_table,
                'type': ref['relationship_type'],
                'direction': 'incoming'
            })
        
        return related
    
    def _get_key_columns(self, table_name: str) -> Dict[str, List[str]]:
        """テーブルの主要カラムを取得"""
        details = self._load_table_details(table_name)
        columns = {
            'primary_keys': ['id'],  # 基本的にidがPK
            'foreign_keys': [],
            'unique_keys': [],
            'business_keys': []
        }
        
        if not details:
            return columns
        
        # 業務固有カラムから主要なものを抽出
        if 'business_columns' in details:
            for col in details['business_columns']:
                col_name = col['name']
                
                # 外部キー
                if table_name in self.all_foreign_keys:
                    for fk in self.all_foreign_keys[table_name]:
                        if fk['column'] == col_name:
                            columns['foreign_keys'].append(f"{col_name} FK")
                
                # ユニークキー（コード系）
                if 'code' in col_name.lower() or 'email' in col_name.lower():
                    columns['unique_keys'].append(f"{col_name} UK")
                
                # 業務キー（名前系、重要な識別子）
                if any(keyword in col_name.lower() for keyword in ['name', 'title', 'status', 'type']):
                    columns['business_keys'].append(col_name)
        
        return columns
    
    def generate_mermaid_erd(self, target_table: str, related_tables: Dict[str, Any]) -> str:
        """Mermaid ERD形式で関連エンティティ図を生成"""
        mermaid_content = "```mermaid\nerDiagram\n"
        
        # 対象テーブルと関連テーブルのリスト
        all_tables = [target_table] + list(related_tables['all_related'])
        
        # エンティティ定義
        for table in all_tables:
            columns = self._get_key_columns(table)
            
            mermaid_content += f"    {table} {{\n"
            
            # 主キー
            for pk in columns['primary_keys']:
                mermaid_content += f"        string {pk} PK\n"
            
            # 外部キー
            for fk in columns['foreign_keys']:
                mermaid_content += f"        string {fk}\n"
            
            # ユニークキー
            for uk in columns['unique_keys']:
                mermaid_content += f"        string {uk}\n"
            
            # 主要な業務キー（最大3つまで）
            for bk in columns['business_keys'][:3]:
                if bk not in columns['primary_keys'] and not any(bk in fk for fk in columns['foreign_keys']):
                    mermaid_content += f"        string {bk}\n"
            
            mermaid_content += "    }\n\n"
        
        # リレーション定義
        for rel in related_tables['relationships']:
            from_table = rel['from']
            to_table = rel['to']
            rel_type = rel['type']
            
            # Mermaidの関係記号を決定
            if rel_type == 'composition':
                symbol = "||--o{"
                label = "強い関連"
            elif rel_type == 'aggregation':
                symbol = "||--o{"
                label = "弱い関連"
            else:
                symbol = "||--o{"
                label = "関連"
            
            mermaid_content += f"    {from_table} {symbol} {to_table} : \"{label}\"\n"
        
        mermaid_content += "```\n"
        return mermaid_content
    
    def generate_related_entities_section(self, target_table: str) -> str:
        """関連エンティティセクションを生成"""
        related_tables = self.analyze_related_tables(target_table)
        
        if not related_tables['all_related']:
            return "\n## 🔗 関連エンティティ\n\n関連するエンティティはありません。\n"
        
        content = "\n## 🔗 関連エンティティ\n\n"
        content += "以下は、このテーブルと直接的な関連を持つエンティティの関係図です。\n\n"
        
        # 関連エンティティ一覧
        content += "### 📊 関連テーブル一覧\n\n"
        content += "| テーブル名 | 論理名 | 関係性 | 説明 |\n"
        content += "|------------|--------|--------|------|\n"
        
        # 参照先テーブル
        for ref in related_tables['direct_references']:
            table_name = ref['table']
            logical_name = self.tables_info.get(table_name, {}).get('logical_name', table_name)
            rel_type = "参照先"
            description = f"{ref['column']} → {table_name}.{ref['ref_column']}"
            content += f"| {table_name} | {logical_name} | {rel_type} | {description} |\n"
        
        # 参照元テーブル
        for ref in related_tables['direct_referenced_by']:
            table_name = ref['table']
            logical_name = self.tables_info.get(table_name, {}).get('logical_name', table_name)
            rel_type = "参照元"
            description = f"{table_name}.{ref['column']} → {ref['ref_column']}"
            content += f"| {table_name} | {logical_name} | {rel_type} | {description} |\n"
        
        # ERD図
        content += "\n### 🎯 エンティティ関連図\n\n"
        content += self.generate_mermaid_erd(target_table, related_tables)
        
        # 関係性の説明
        if related_tables['relationships']:
            content += "\n### 📝 関係性の詳細\n\n"
            for rel in related_tables['relationships']:
                from_logical = self.tables_info.get(rel['from'], {}).get('logical_name', rel['from'])
                to_logical = self.tables_info.get(rel['to'], {}).get('logical_name', rel['to'])
                
                if rel['type'] == 'composition':
                    desc = "強い関連（親エンティティが削除されると子エンティティも削除される）"
                elif rel['type'] == 'aggregation':
                    desc = "弱い関連（親エンティティが削除されても子エンティティは残る）"
                else:
                    desc = "関連（参照整合性制約あり）"
                
                content += f"- **{from_logical} → {to_logical}**: {desc}\n"
        
        return content

class TableDefinitionGenerator:
    """テーブル定義書生成クラス（v8拡張版）"""
    
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
        self.erd_generator = None
        
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
        """テーブル定義書を生成（関連エンティティERD付き）"""
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
        
        # カラム定義
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
        
        # 関連エンティティERD（新機能）
        if self.erd_generator:
            md_content += self.erd_generator.generate_related_entities_section(table_name)
        
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
    
    def generate_files(self, table_names: List[str] = None, output_dir: str = None, enable_erd: bool = True):
        """ファイル生成メイン処理（ERD生成機能付き）"""
        # テーブル一覧読み込み
        self.tables_info = self.load_table_list()
        
        # ERDジェネレーター初期化
        if enable_erd:
            self.erd_generator = ERDGenerator(self.base_dir, self.tables_info)
        
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
        
        print(f"🚀 テーブル定義書生成スクリプト v8 (関連エンティティERD自動生成対応版)")
        print("=" * 80)
        print(f"{len(target_tables)}個のテーブルを処理します。")
        if enable_erd:
            print("✨ 関連エンティティERD自動生成機能: 有効")
        print()
        
        for table_name, table_info in target_tables.items():
            print(f"処理中: {table_name} ({table_info['logical_name']})")
            
            try:
                # テーブル定義書生成
                md_content = self.generate_table_definition(table_name, table_info)
                md_file = tables_output / f"テーブル定義書_{table_name}_{table_info['logical_name']}.md"
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(md_content)
                print(f"  ✓ {md_file}")
                
                # ERD生成状況表示
                if enable_erd and self.erd_generator:
                    related_tables = self.erd_generator.analyze_related_tables(table_name)
                    if related_tables['all_related']:
                        print(f"  🔗 関連エンティティ: {len(related_tables['all_related'])}個")
                    else:
                        print(f"  🔗 関連エンティティ: なし")
                
            except Exception as e:
