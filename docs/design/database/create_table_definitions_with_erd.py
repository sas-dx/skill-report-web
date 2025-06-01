#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト（ERD機能付き）

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
│  v9.0   │ 2025-06-01 │ システム │ 関連エンティティ図生成機能追加（2階層ERD対応）      │
└─────────┴────────────┴──────────┴─────────────────────────────────────────────────────┘

機能概要:
- テーブル一覧.mdからテーブル情報を自動読み込み
- YAML詳細定義ファイルとの連携
- テーブル定義書（Markdown）の自動生成
- DDLファイルの自動生成
- 統合DDLファイルの作成
- 関連エンティティ図（Mermaid ERD）の自動生成（2階層対応）
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

class ERDGenerator:
    """エンティティ関連図生成クラス"""
    
    def __init__(self, tables_info: Dict[str, Any], details_dir: Path):
        """初期化"""
        self.tables_info = tables_info
        self.details_dir = details_dir
        self.relationship_cache = {}
        
        # プロフィール管理テーブル定義
        self.profile_tables = {
            'MST_Employee': '社員基本情報',
            'MST_Department': '部署マスタ', 
            'MST_Position': '役職マスタ',
            'MST_JobType': '職種マスタ',
            'MST_EmployeeJobType': '社員職種関連',
            'MST_EmployeeDepartment': '社員部署関連',
            'MST_EmployeePosition': '社員役職関連'
        }
        
        # カラム表示優先順位
        self.column_priority = [
            'id', 'tenant_id', '*_code', '*_name', '*_id', 
            'status', 'created_at', 'updated_at'
        ]
    
    def load_table_details(self, table_name: str) -> Optional[Dict[str, Any]]:
        """テーブル詳細定義YAMLを読み込み"""
        details_file = self.details_dir / f"{table_name}_details.yaml"
        
        if not details_file.exists():
            return None
        
        try:
            with open(details_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"警告: {details_file} の読み込みに失敗: {e}")
            return None
    
    def get_foreign_key_relationships(self, table_name: str) -> List[Dict[str, str]]:
        """外部キー関係を取得"""
        details = self.load_table_details(table_name)
        if not details or 'foreign_keys' not in details:
            return []
        
        relationships = []
        for fk in details['foreign_keys']:
            relationships.append({
                'from_table': table_name,
                'from_column': fk['column'],
                'to_table': fk['reference_table'],
                'to_column': fk['reference_column'],
                'relationship_type': self._determine_relationship_type(fk),
                'description': fk.get('description', '')
            })
        
        return relationships
    
    def _determine_relationship_type(self, fk: Dict[str, str]) -> str:
        """関係タイプを判定"""
        # 自己参照の場合
        if fk['reference_table'] == fk.get('from_table'):
            return '||--o{'
        
        # 一般的な外部キー（多対一）
        return '}o--||'
    
    def find_related_tables(self, target_table: str, max_depth: int = 2) -> Dict[int, Set[str]]:
        """関連テーブルを階層別に取得"""
        related_tables = {0: {target_table}, 1: set(), 2: set()}
        processed_tables = set()
        
        # 1階層目: 直接関連テーブル
        for table_name in self.tables_info.keys():
            if table_name == target_table:
                continue
                
            # target_tableから参照するテーブル
            relationships = self.get_foreign_key_relationships(target_table)
            for rel in relationships:
                if rel['to_table'] in self.tables_info:
                    related_tables[1].add(rel['to_table'])
            
            # target_tableを参照するテーブル
            relationships = self.get_foreign_key_relationships(table_name)
            for rel in relationships:
                if rel['to_table'] == target_table:
                    related_tables[1].add(table_name)
        
        processed_tables.update(related_tables[1])
        
        # 2階層目: 1階層テーブルの関連テーブル
        if max_depth >= 2:
            for level1_table in related_tables[1]:
                # level1_tableから参照するテーブル
                relationships = self.get_foreign_key_relationships(level1_table)
                for rel in relationships:
                    if (rel['to_table'] in self.tables_info and 
                        rel['to_table'] not in related_tables[0] and 
                        rel['to_table'] not in related_tables[1]):
                        related_tables[2].add(rel['to_table'])
                
                # level1_tableを参照するテーブル
                for table_name in self.tables_info.keys():
                    if table_name in processed_tables or table_name == target_table:
                        continue
                    
                    relationships = self.get_foreign_key_relationships(table_name)
                    for rel in relationships:
                        if (rel['to_table'] == level1_table and 
                            table_name not in related_tables[0] and 
                            table_name not in related_tables[1]):
                            related_tables[2].add(table_name)
        
        # 表示制限（最大15テーブル）
        if len(related_tables[1]) + len(related_tables[2]) > 14:
            # 優先度順でフィルタリング（プロフィール管理テーブルを優先）
            all_related = list(related_tables[1]) + list(related_tables[2])
            priority_tables = [t for t in all_related if t in self.profile_tables]
            other_tables = [t for t in all_related if t not in self.profile_tables]
            
            limited_tables = priority_tables + other_tables[:14-len(priority_tables)]
            
            # 階層を再構築
            related_tables[1] = {t for t in limited_tables if t in related_tables[1]}
            related_tables[2] = {t for t in limited_tables if t in related_tables[2]}
        
        return related_tables
    
    def get_display_columns(self, table_name: str) -> List[Dict[str, str]]:
        """表示するカラムを取得"""
        details = self.load_table_details(table_name)
        display_columns = []
        
        # 基本カラム
        display_columns.append({'name': 'id', 'logical': 'ID', 'type': 'PK'})
        
        # テナントカラム
        if not table_name.startswith('SYS_'):
            display_columns.append({'name': 'tenant_id', 'logical': 'テナントID', 'type': 'FK'})
        
        # 業務固有カラム（優先度順）
        if details and 'business_columns' in details:
            business_cols = details['business_columns']
            
            # コードカラム
            code_cols = [col for col in business_cols if col['name'].endswith('_code')]
            for col in code_cols[:2]:  # 最大2つ
                col_type = 'UK' if col.get('unique') else ''
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': col_type
                })
            
            # 名前カラム
            name_cols = [col for col in business_cols if col['name'].endswith('_name')]
            for col in name_cols[:2]:  # 最大2つ
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': ''
                })
            
            # 外部キーカラム
            fk_cols = [col for col in business_cols if col['name'].endswith('_id')]
            for col in fk_cols[:3]:  # 最大3つ
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': 'FK'
                })
            
            # ステータスカラム
            status_cols = [col for col in business_cols if 'status' in col['name'].lower()]
            for col in status_cols[:1]:  # 最大1つ
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': ''
                })
        
        return display_columns[:8]  # 最大8カラム
    
    def generate_mermaid_erd(self, target_table: str, related_tables: Dict[int, Set[str]]) -> str:
        """Mermaid ERD形式を生成"""
        erd_content = "```mermaid\nerDiagram\n"
        
        # 全テーブルのカラム定義
        all_tables = {target_table} | related_tables[1] | related_tables[2]
        
        for table_name in all_tables:
            logical_name = self.tables_info.get(table_name, {}).get('logical_name', table_name)
            erd_content += f"    {table_name} {{\n"
            
            columns = self.get_display_columns(table_name)
            for col in columns:
                type_suffix = f" {col['type']}" if col['type'] else ""
                erd_content += f"        {col['name']}{type_suffix} \"{col['logical']}\"\n"
            
            erd_content += "    }\n\n"
        
        # 関係線の定義
        erd_content += "    %% 関係定義\n"
        
        # 1階層関係
        for table in related_tables[1]:
            relationships = self.get_foreign_key_relationships(target_table)
            for rel in relationships:
                if rel['to_table'] == table:
                    erd_content += f"    {target_table} {rel['relationship_type']} {table} : \"{rel['description']}\"\n"
            
            relationships = self.get_foreign_key_relationships(table)
            for rel in relationships:
                if rel['to_table'] == target_table:
                    erd_content += f"    {table} {rel['relationship_type']} {target_table} : \"{rel['description']}\"\n"
        
        # 2階層関係（主要なもののみ）
        for table in related_tables[2]:
            for level1_table in related_tables[1]:
                relationships = self.get_foreign_key_relationships(table)
                for rel in relationships:
                    if rel['to_table'] == level1_table:
                        erd_content += f"    {table} {rel['relationship_type']} {level1_table} : \"{rel['description']}\"\n"
                        break  # 1つの関係のみ表示
        
        erd_content += "```\n"
        return erd_content
    
    def generate_relationship_summary(self, target_table: str, related_tables: Dict[int, Set[str]]) -> str:
        """関連テーブル概要表を生成"""
        summary = "### 関連テーブル概要\n"
        summary += "| 階層 | テーブル名 | 論理名 | 関係 | カテゴリ | 説明 |\n"
        summary += "|------|------------|--------|------|----------|------|\n"
        
        # 対象テーブル
        target_info = self.tables_info.get(target_table, {})
        summary += f"| 0 | {target_table} | {target_info.get('logical_name', '')} | - | {target_info.get('category', '')} | 対象テーブル |\n"
        
        # 1階層テーブル
        for table in sorted(related_tables[1]):
            table_info = self.tables_info.get(table, {})
            relationship = self._get_relationship_description(target_table, table)
            summary += f"| 1 | {table} | {table_info.get('logical_name', '')} | {relationship} | {table_info.get('category', '')} | {self._get_table_description(target_table, table)} |\n"
        
        # 2階層テーブル
        for table in sorted(related_tables[2]):
            table_info = self.tables_info.get(table, {})
            relationship = self._get_relationship_description_level2(table, related_tables[1])
            summary += f"| 2 | {table} | {table_info.get('logical_name', '')} | {relationship} | {table_info.get('category', '')} | {self._get_table_description_level2(table, related_tables[1])} |\n"
        
        return summary
    
    def _get_relationship_description(self, target_table: str, related_table: str) -> str:
        """関係の説明を取得"""
        # target_tableからrelated_tableへの関係
        relationships = self.get_foreign_key_relationships(target_table)
        for rel in relationships:
            if rel['to_table'] == related_table:
                return "N:1"
        
        # related_tableからtarget_tableへの関係
        relationships = self.get_foreign_key_relationships(related_table)
        for rel in relationships:
            if rel['to_table'] == target_table:
                return "1:N"
        
        return "関連"
    
    def _get_relationship_description_level2(self, table: str, level1_tables: Set[str]) -> str:
        """2階層の関係説明を取得"""
        relationships = self.get_foreign_key_relationships(table)
        for rel in relationships:
            if rel['to_table'] in level1_tables:
                return "1:N"
        
        for level1_table in level1_tables:
            relationships = self.get_foreign_key_relationships(level1_table)
            for rel in relationships:
                if rel['to_table'] == table:
                    return "N:1"
        
        return "間接"
    
    def _get_table_description(self, target_table: str, related_table: str) -> str:
        """テーブルの説明を取得"""
        relationships = self.get_foreign_key_relationships(target_table)
        for rel in relationships:
            if rel['to_table'] == related_table:
                return rel['description'] or f"{related_table}への参照"
        
        relationships = self.get_foreign_key_relationships(related_table)
        for rel in relationships:
            if rel['to_table'] == target_table:
                return rel['description'] or f"{target_table}からの参照"
        
        return "関連テーブル"
    
    def _get_table_description_level2(self, table: str, level1_tables: Set[str]) -> str:
        """2階層テーブルの説明を取得"""
        for level1_table in level1_tables:
            relationships = self.get_foreign_key_relationships(table)
            for rel in relationships:
                if rel['to_table'] == level1_table:
                    return f"{level1_table}経由の関連"
        
        return "間接関連テーブル"
    
    def generate_business_flow_description(self, target_table: str, related_tables: Dict[int, Set[str]]) -> str:
        """主要業務フローの説明を生成"""
        if target_table not in self.profile_tables:
            return ""
        
        flow_desc = "### プロフィール管理の主要業務フロー\n"
        
        if target_table == 'MST_Employee':
            flow_desc += "1. **社員登録**: MST_Employee → MST_Department, MST_Position, MST_JobType\n"
            flow_desc += "2. **組織変更**: MST_Employee → MST_Department → MST_Department（階層移動）\n"
            flow_desc += "3. **スキル評価**: MST_Employee → TRN_EmployeeSkillGrade → MST_SkillGrade\n"
            flow_desc += "4. **権限管理**: MST_Employee → MST_UserAuth → MST_Role\n"
        elif target_table == 'MST_Department':
            flow_desc += "1. **部署管理**: MST_Department → MST_Department（階層構造）\n"
            flow_desc += "2. **社員配属**: MST_Employee → MST_Department\n"
            flow_desc += "3. **組織変更**: 部署間の社員移動管理\n"
        elif target_table == 'MST_Position':
            flow_desc += "1. **役職管理**: MST_Position → MST_Employee\n"
            flow_desc += "2. **昇進管理**: 役職変更の履歴管理\n"
        elif target_table == 'MST_JobType':
            flow_desc += "1. **職種管理**: MST_JobType → MST_Employee\n"
            flow_desc += "2. **スキル要件**: MST_JobType → MST_SkillGrade\n"
        
        return flow_desc

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
    
    def _generate_related_entity_section(self, table_name: str) -> str:
        """関連エンティティセクションを生成"""
        if not self.erd_generator:
            return ""
        
        # 関連テーブルを取得
        related_tables = self.erd_generator.find_related_tables(table_name, max_depth=2)
        
        if not related_tables[1] and not related_tables[2]:
            return ""
        
        section = "## 🔗 関連エンティティ図\n\n"
        
        # 関連テーブル概要
        section += self.erd_generator.generate_relationship_summary(table_name, related_tables)
        section += "\n"
        
        # ERD図
        section += "### エンティティ関連図（2階層）\n"
        section += self.erd_generator.generate_mermaid_erd(table_name, related_tables)
        section += "\n"
        
        # 業務フロー説明
        flow_desc = self.erd_generator.generate_business_flow_description(table_name, related_tables)
        if flow_desc:
            section += flow_desc
            section += "\n"
        
        return section
    
    def generate_table_definition(self, table_name: str, table_info: Dict[str, Any], include_erd: bool = False) -> str:
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
        
        # 関連エンティティ図の追加
        if include_erd an
