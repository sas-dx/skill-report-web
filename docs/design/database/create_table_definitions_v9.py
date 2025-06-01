#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト v9.0 (関連ERD対応版)

改版履歴:
┌─────────┬────────────┬──────────┬─────────────────────────────────────────────────────┐
│ バージョン │    更新日    │  更新者  │                  主な変更内容                       │
├─────────┼────────────┼──────────┼─────────────────────────────────────────────────────┤
│  v9.0   │ 2025-06-01 │ システム │ 関連ERD自動生成機能追加・論理名物理名併記対応        │
│  v8.0   │ 2025-06-01 │ システム │ 全テーブル定義書再生成・ファイル命名規則統一        │
│  v7.0   │ 2025-05-XX │ 開発者   │ レイアウト改良・PK/FK表示・桁数情報追加             │
│  v6.0   │ 2025-01-XX │ 開発者   │ DDL生成機能追加・統合DDL対応・エラーハンドリング強化│
└─────────┴────────────┴──────────┴─────────────────────────────────────────────────────┘

機能概要:
- テーブル一覧.mdからテーブル情報を自動読み込み
- YAML詳細定義ファイルとの連携
- エンティティ関連定義(entity_relationships.yaml)との連携
- 関連エンティティERDの自動生成（論理名・物理名併記）
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
from typing import Dict, List, Optional, Any, Set, Tuple

class RelatedERDGenerator:
    """関連ERD生成クラス"""
    
    def __init__(self, entity_relationships: Dict[str, Any]):
        """初期化"""
        self.entities = entity_relationships.get('entities', {})
        self.relationships = entity_relationships.get('relationships', [])
        self.config = entity_relationships.get('related_entity_config', {})
        
        # 関連マップを構築
        self.relation_map = self._build_relation_map()
    
    def _build_relation_map(self) -> Dict[str, List[Dict[str, Any]]]:
        """関連マップを構築"""
        relation_map = {}
        
        for rel in self.relationships:
            source = rel['source']
            target = rel['target']
            
            if source not in relation_map:
                relation_map[source] = []
            if target not in relation_map:
                relation_map[target] = []
            
            # 双方向の関連を記録
            relation_map[source].append({
                'table': target,
                'type': rel['type'],
                'cardinality': rel['cardinality'],
                'foreign_key': rel.get('foreign_key'),
                'description': rel['description'],
                'direction': 'outgoing'
            })
            
            relation_map[target].append({
                'table': source,
                'type': rel['type'],
                'cardinality': self._reverse_cardinality(rel['cardinality']),
                'foreign_key': rel.get('foreign_key'),
                'description': rel['description'],
                'direction': 'incoming'
            })
        
        return relation_map
    
    def _reverse_cardinality(self, cardinality: str) -> str:
        """カーディナリティを逆転"""
        reverse_map = {
            "}o--||": "||--o{",
            "||--o{": "}o--||",
            "||--||": "||--||",
            "}o--o{": "}o--o{"
        }
        return reverse_map.get(cardinality, cardinality)
    
    def extract_related_entities(self, table_name: str) -> List[str]:
        """関連エンティティを抽出"""
        if table_name not in self.entities:
            return []
        
        # カスタム設定を取得
        custom_config = self.config.get('custom_settings', {}).get(table_name, {})
        depth = custom_config.get('depth', self.config.get('default_depth', 2))
        max_entities = custom_config.get('max_entities', self.config.get('max_entities', 8))
        priority_relations = custom_config.get('priority_relations', [])
        
        related_entities = set()
        visited = set()
        
        def _extract_recursive(current_table: str, current_depth: int):
            if current_depth > depth or current_table in visited:
                return
            
            visited.add(current_table)
            
            if current_table in self.relation_map:
                for rel in self.relation_map[current_table]:
                    related_table = rel['table']
                    if related_table != table_name and related_table in self.entities:
                        related_entities.add(related_table)
                        if current_depth < depth:
                            _extract_recursive(related_table, current_depth + 1)
        
        _extract_recursive(table_name, 0)
        
        # 優先関連を先頭に配置
        result = []
        for priority_table in priority_relations:
            if priority_table in related_entities:
                result.append(priority_table)
                related_entities.remove(priority_table)
        
        # 残りの関連エンティティを追加
        result.extend(list(related_entities))
        
        # 最大エンティティ数で制限
        return result[:max_entities-1]  # -1 は対象テーブル自身の分
    
    def generate_related_erd(self, table_name: str) -> Tuple[str, List[Dict[str, str]]]:
        """関連ERDを生成"""
        if table_name not in self.entities:
            return "", []
        
        related_entities = self.extract_related_entities(table_name)
        all_entities = [table_name] + related_entities
        
        # ERD生成
        erd_content = "```mermaid\nerDiagram\n"
        
        # エンティティ定義
        for entity_name in all_entities:
            if entity_name not in self.entities:
                continue
                
            entity = self.entities[entity_name]
            logical_name = entity['logical_name']
            
            erd_content += f'    {entity_name}["{entity_name}<br/>{logical_name}"] {{\n'
            
            # 主要カラムを表示
            key_columns = entity.get('key_columns', [])
            for col in key_columns[:6]:  # 最大6カラムまで表示
                col_type = col['type'].split('(')[0]  # 型名のみ抽出
                pk_mark = " PK" if col.get('is_pk') else ""
                fk_mark = " FK" if col.get('is_fk') else ""
                erd_content += f'        {col_type} {col["name"]}{pk_mark}{fk_mark} "{col["logical"]}"\n'
            
            erd_content += "    }\n\n"
        
        # 関連線
        processed_relations = set()
        for entity_name in all_entities:
            if entity_name not in self.relation_map:
                continue
                
            for rel in self.relation_map[entity_name]:
                related_table = rel['table']
                if related_table not in all_entities:
                    continue
                
                # 重複関連を避ける
                relation_key = tuple(sorted([entity_name, related_table]))
                if relation_key in processed_relations:
                    continue
                processed_relations.add(relation_key)
                
                # 関連線を描画
                cardinality = rel['cardinality']
                description = rel['description'].replace('（自己参照）', '').replace('は', '').replace('に', '').replace('を', '').replace('する', '')[:10]
                erd_content += f'    {entity_name} {cardinality} {related_table} : "{description}"\n'
        
        erd_content += "```"
        
        # 関連テーブル一覧
        related_table_list = []
        for entity_name in related_entities:
            if entity_name in self.entities:
                entity = self.entities[entity_name]
                
                # 関連タイプを判定
                relation_type = "参照"
                for rel in self.relation_map.get(table_name, []):
                    if rel['table'] == entity_name:
                        if rel['type'] == 'one_to_one':
                            relation_type = "1:1関連"
                        elif rel['type'] == 'one_to_many':
                            relation_type = "1:N関連"
                        elif rel['type'] == 'many_to_one':
                            relation_type = "参照"
                        elif rel['type'] == 'many_to_many':
                            relation_type = "N:N関連"
                        break
                
                related_table_list.append({
                    'table_name': entity_name,
                    'logical_name': entity['logical_name'],
                    'relation_type': relation_type,
                    'description': f"{entity['logical_name']}との関連"
                })
        
        return erd_content, related_table_list

class TableDefinitionGenerator:
    """テーブル定義書生成クラス"""
    
    def __init__(self, base_dir: str = None):
        """初期化"""
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.tables_dir = self.base_dir / "tables"
        self.ddl_dir = self.base_dir / "ddl"
        self.details_dir = self.base_dir / "table-details"
        self.table_list_file = self.base_dir / "テーブル一覧.md"
        self.entity_relationships_file = self.base_dir / "entity_relationships.yaml"
        
        # ディレクトリ作成
        self.tables_dir.mkdir(exist_ok=True)
        self.ddl_dir.mkdir(exist_ok=True)
        self.details_dir.mkdir(exist_ok=True)
        
        # テーブル情報
        self.tables_info = {}
        self.common_columns = self._get_common_columns()
        
        # 関連ERD生成器
        self.erd_generator = None
        self._load_entity_relationships()
        
    def _load_entity_relationships(self):
        """エンティティ関連定義を読み込み"""
        if self.entity_relationships_file.exists():
            try:
                with open(self.entity_relationships_file, 'r', encoding='utf-8') as f:
                    entity_relationships = yaml.safe_load(f)
                self.erd_generator = RelatedERDGenerator(entity_relationships)
                print(f"✓ エンティティ関連定義を読み込みました: {self.entity_relationships_file}")
            except Exception as e:
                print(f"警告: エンティティ関連定義の読み込みに失敗しました: {e}")
        else:
            print(f"警告: エンティティ関連定義ファイルが見つかりません: {self.entity_relationships_file}")
    
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
        
        # 関連エンティティセクション（新機能）
        if self.erd_generator:
            erd_content, related_tables = self.erd_generator.generate_related_erd(table_name)
            if erd_content:
                md_content += "## 🔗 関連エンティティ\n\n"
                md_content += "### 関連図\n\n"
                md_content += erd_content + "\n\n"
                
                if related_tables:
                    md_content += "### 関連テーブル一覧\n\n"
                    md_content += "| テーブル名 | 論理名 | 関連タイプ | 説明 |\n"
                    md_content += "|------------|--------|------------|------|\n"
                    for rel_table in related_tables:
                        md_content += f"| {rel_table['table_name']} | {rel_table['logical_name']} | {rel_table['relation_type']} | {rel_table['description']} |\n"
                    md_content += "\n"
        
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
