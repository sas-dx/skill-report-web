#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト（最終版）

ERD機能を統合した完全版のテーブル定義書生成スクリプト
ファイル命名規則: テーブル定義書_テーブル名_論理名.md
"""

import os
import re
import sys
import yaml
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set

class ERDGenerator:
    """ERD生成クラス"""
    
    def __init__(self, tables_info: Dict[str, Any], details_dir: Path):
        """初期化"""
        self.tables_info = tables_info
        self.details_dir = details_dir
        
        # 重要テーブルカテゴリ定義
        self.important_categories = {
            'プロフィール管理': ['MST_Employee', 'MST_Department', 'MST_Position', 'MST_JobType'],
            'スキル管理': ['MST_SkillCategory', 'MST_SkillItem', 'MST_SkillGrade', 'TRN_EmployeeSkillGrade'],
            '認証・権限': ['MST_UserAuth', 'MST_Role', 'MST_Permission', 'MST_UserRole'],
            'システム': ['SYS_SystemLog', 'SYS_AuditLog', 'SYS_Configuration']
        }
    
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
                'relationship_type': '}o--||',
                'description': fk.get('description', '').replace('への外部キー', '').replace('への', '')
            })
        
        return relationships
    
    def find_related_tables(self, target_table: str, max_depth: int = 2) -> Dict[int, Set[str]]:
        """関連テーブルを階層別に取得"""
        related_tables = {0: {target_table}, 1: set(), 2: set()}
        
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
        
        # 2階層目: 1階層テーブルの関連テーブル
        if max_depth >= 2:
            for level1_table in list(related_tables[1]):
                relationships = self.get_foreign_key_relationships(level1_table)
                for rel in relationships:
                    if (rel['to_table'] in self.tables_info and 
                        rel['to_table'] not in related_tables[0] and 
                        rel['to_table'] not in related_tables[1]):
                        # 重要なテーブルのみ追加
                        if self._is_important_table(rel['to_table']):
                            related_tables[2].add(rel['to_table'])
        
        # 表示制限（最大8テーブル）
        if len(related_tables[2]) > 6:
            priority_tables = [t for t in related_tables[2] if self._is_high_priority_table(t)]
            other_tables = [t for t in related_tables[2] if not self._is_high_priority_table(t)]
            related_tables[2] = set(priority_tables + other_tables[:6-len(priority_tables)])
        
        return related_tables
    
    def _is_important_table(self, table_name: str) -> bool:
        """重要なテーブルかどうか判定"""
        for category_tables in self.important_categories.values():
            if table_name in category_tables:
                return True
        return table_name.startswith('MST_') or table_name.startswith('TRN_')
    
    def _is_high_priority_table(self, table_name: str) -> bool:
        """高優先度テーブルかどうか判定"""
        high_priority = ['MST_Employee', 'MST_Department', 'MST_Position', 'MST_SkillCategory', 'MST_SkillItem']
        return table_name in high_priority
    
    def get_display_columns(self, table_name: str) -> List[Dict[str, str]]:
        """表示するカラムを取得"""
        details = self.load_table_details(table_name)
        display_columns = []
        
        # 基本カラム
        display_columns.append({'name': 'id', 'logical': 'ID', 'type': 'PK'})
        
        # テナントカラム
        if not table_name.startswith('SYS_'):
            display_columns.append({'name': 'tenant_id', 'logical': 'テナントID', 'type': 'FK'})
        
        # 業務固有カラム（重要なもののみ）
        if details and 'business_columns' in details:
            business_cols = details['business_columns']
            
            # コードカラム（最大1つ）
            code_cols = [col for col in business_cols if col['name'].endswith('_code')]
            if code_cols:
                col = code_cols[0]
                col_type = 'UK' if col.get('unique') else ''
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': col_type
                })
            
            # 名前カラム（最大1つ）
            name_cols = [col for col in business_cols if col['name'].endswith('_name')]
            if name_cols:
                col = name_cols[0]
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': ''
                })
            
            # 外部キーカラム（最大2つ）
            fk_cols = [col for col in business_cols if col['name'].endswith('_id')]
            for col in fk_cols[:2]:
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': 'FK'
                })
            
            # ステータスカラム
            status_cols = [col for col in business_cols if 'status' in col['name'].lower()]
            if status_cols:
                col = status_cols[0]
                display_columns.append({
                    'name': col['name'], 
                    'logical': col['logical'], 
                    'type': ''
                })
        
        return display_columns[:6]  # 最大6カラム
    
    def generate_mermaid_erd(self, target_table: str, related_tables: Dict[int, Set[str]]) -> str:
        """Mermaid ERD形式を生成"""
        erd_content = "```mermaid\nerDiagram\n"
        
        # 全テーブルのカラム定義
        all_tables = {target_table} | related_tables[1] | related_tables[2]
        
        for table_name in sorted(all_tables):
            # テーブル定義開始
            erd_content += f"    {table_name} " + "{\n"
            
            columns = self.get_display_columns(table_name)
            for col in columns:
                type_suffix = f" {col['type']}" if col['type'] else ""
                erd_content += f"        {col['name']}{type_suffix} \"{col['logical']}\"\n"
            
            # テーブル定義終了
            erd_content += "    }\n\n"
        
        # 関係線の定義
        erd_content += "    %% 関係定義\n"
        
        # 1階層関係
        for table in sorted(related_tables[1]):
            relationships = self.get_foreign_key_relationships(target_table)
            for rel in relationships:
                if rel['to_table'] == table:
                    desc = rel['description'] or "参照"
                    erd_content += f"    {target_table} " + "}o--|| " + f"{table} : \"{desc}\"\n"
            
            relationships = self.get_foreign_key_relationships(table)
            for rel in relationships:
                if rel['to_table'] == target_table:
                    desc = rel['description'] or "参照"
                    erd_content += f"    {table} " + "}o--|| " + f"{target_table} : \"{desc}\"\n"
        
        # 2階層関係（主要なもののみ）
        for table in sorted(related_tables[2]):
            for level1_table in sorted(related_tables[1]):
                relationships = self.get_foreign_key_relationships(table)
                for rel in relationships:
                    if rel['to_table'] == level1_table:
                        desc = rel['description'] or "関連"
                        erd_content += f"    {table} " + "}o--|| " + f"{level1_table} : \"{desc}\"\n"
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
            description = self._get_table_description(target_table, table)
            summary += f"| 1 | {table} | {table_info.get('logical_name', '')} | {relationship} | {table_info.get('category', '')} | {description} |\n"
        
        # 2階層テーブル
        for table in sorted(related_tables[2]):
            table_info = self.tables_info.get(table, {})
            relationship = "間接"
            description = "間接関連テーブル"
            summary += f"| 2 | {table} | {table_info.get('logical_name', '')} | {relationship} | {table_info.get('category', '')} | {description} |\n"
        
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
    
    def generate_related_entity_section(self, table_name: str) -> str:
        """関連エンティティセクションを生成"""
        # 関連テーブルを取得
        related_tables = self.find_related_tables(table_name, max_depth=2)
        
        if not related_tables[1] and not related_tables[2]:
            return ""
        
        section = "## 🔗 関連エンティティ図\n\n"
        
        # 関連テーブル概要
        section += self.generate_relationship_summary(table_name, related_tables)
        section += "\n"
        
        # ERD図
        section += "### エンティティ関連図\n"
        section += self.generate_mermaid_erd(table_name, related_tables)
        section += "\n"
        
        return section

class TableDefinitionGenerator:
    """テーブル定義書生成クラス"""
    
    def __init__(self, base_dir: Path):
        """初期化"""
        self.base_dir = base_dir
        self.details_dir = base_dir / "table-details"
        self.output_dir = base_dir / "tables"
        self.table_list_file = base_dir / "テーブル一覧.md"
        
        # 出力ディレクトリ作成
        self.output_dir.mkdir(exist_ok=True)
        
        # テーブル情報を読み込み
        self.tables_info = self._load_tables_info()
        
        # ERD生成器初期化
        self.erd_generator = ERDGenerator(self.tables_info, self.details_dir)
    
    def _load_tables_info(self) -> Dict[str, Any]:
        """テーブル一覧からテーブル情報を読み込み"""
        if not self.table_list_file.exists():
            raise FileNotFoundError(f"テーブル一覧ファイルが見つかりません: {self.table_list_file}")
        
        with open(self.table_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tables_info = {}
        table_pattern = r'\|\s*\[([^\]]+)\]\([^\)]+\)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|'
        
        for match in re.finditer(table_pattern, content):
            table_id = match.group(1).strip()
            category = match.group(2).strip()
            table_name = match.group(3).strip()
            logical_name = match.group(4).strip()
            
            tables_info[table_name] = {
                'table_id': table_id,
                'category': category,
                'logical_name': logical_name,
                'table_name': table_name
            }
        
        return tables_info
    
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
    
    def generate_table_definition(self, table_name: str) -> str:
        """テーブル定義書を生成"""
        table_info = self.tables_info.get(table_name)
        if not table_info:
            raise ValueError(f"テーブル情報が見つかりません: {table_name}")
        
        details = self.load_table_details(table_name)
        if not details:
            raise ValueError(f"テーブル詳細定義が見つかりません: {table_name}")
        
        # ヘッダー生成
        content = self._generate_header(table_info, details)
        
        # 基本情報
        content += self._generate_basic_info(table_info, details)
        
        # カラム定義
        content += self._generate_column_definitions(details)
        
        # インデックス定義
        content += self._generate_index_definitions(details)
        
        # 制約定義
        content += self._generate_constraint_definitions(details)
        
        # 関連エンティティ図（ERD）
        erd_section = self.erd_generator.generate_related_entity_section(table_name)
        if erd_section:
            content += erd_section
        
        # 業務ルール
        content += self._generate_business_rules(details)
        
        # 備考
        content += self._generate_notes(details)
        
        return content
    
    def _generate_header(self, table_info: Dict[str, Any], details: Dict[str, Any]) -> str:
        """ヘッダー生成"""
        return f"""# テーブル定義書: {table_info['table_name']} ({table_info['logical_name']})

**テーブルID**: {table_info['table_id']}  
**カテゴリ**: {table_info['category']}  
**作成日**: {datetime.now().strftime('%Y年%m月%d日')}  
**更新日**: {datetime.now().strftime('%Y年%m月%d日')}

## 📋 概要

{details.get('description', 'テーブルの説明が設定されていません。')}

"""
    
    def _generate_basic_info(self, table_info: Dict[str, Any], details: Dict[str, Any]) -> str:
        """基本情報生成"""
        content = "## 📊 基本情報\n\n"
        content += "| 項目 | 値 |\n"
        content += "|------|----|\n"
        content += f"| テーブル名（物理） | {table_info['table_name']} |\n"
        content += f"| テーブル名（論理） | {table_info['logical_name']} |\n"
        content += f"| テーブルID | {table_info['table_id']} |\n"
        content += f"| カテゴリ | {table_info['category']} |\n"
        
        if 'engine' in details:
            content += f"| ストレージエンジン | {details['engine']} |\n"
        
        if 'charset' in details:
            content += f"| 文字セット | {details['charset']} |\n"
        
        if 'collation' in details:
            content += f"| 照合順序 | {details['collation']} |\n"
        
        content += "\n"
        return content
    
    def _generate_column_definitions(self, details: Dict[str, Any]) -> str:
        """カラム定義生成"""
        content = "## 📝 カラム定義\n\n"
        content += "| # | カラム名（物理） | カラム名（論理） | データ型 | NULL | デフォルト | 説明 |\n"
        content += "|---|------------------|------------------|----------|------|------------|------|\n"
        
        column_num = 1
        
        # 共通カラム
        if 'common_columns' in details:
            for col in details['common_columns']:
                null_str = "○" if col.get('nullable', False) else "×"
                default_str = col.get('default', '-')
                content += f"| {column_num} | {col['name']} | {col['logical']} | {col['type']} | {null_str} | {default_str} | {col.get('description', '')} |\n"
                column_num += 1
        
        # 業務カラム
        if 'business_columns' in details:
            for col in details['business_columns']:
                null_str = "○" if col.get('nullable', False) else "×"
                default_str = col.get('default', '-')
                content += f"| {column_num} | {col['name']} | {col['logical']} | {col['type']} | {null_str} | {default_str} | {col.get('description', '')} |\n"
                column_num += 1
        
        content += "\n"
        return content
    
    def _generate_index_definitions(self, details: Dict[str, Any]) -> str:
        """インデックス定義生成"""
        if 'indexes' not in details or not details['indexes']:
            return ""
        
        content = "## 🔍 インデックス定義\n\n"
        content += "| インデックス名 | 種類 | カラム | 説明 |\n"
        content += "|----------------|------|--------|------|\n"
        
        for idx in details['indexes']:
            columns_str = ', '.join(idx['columns'])
            content += f"| {idx['name']} | {idx['type']} | {columns_str} | {idx.get('description', '')} |\n"
        
        content += "\n"
        return content
    
    def _generate_constraint_definitions(self, details: Dict[str, Any]) -> str:
        """制約定義生成"""
        content = ""
        
        # 外部キー制約
        if 'foreign_keys' in details and details['foreign_keys']:
            content += "## 🔗 外部キー制約\n\n"
            content += "| 制約名 | カラム | 参照テーブル | 参照カラム | 説明 |\n"
            content += "|--------|--------|--------------|------------|------|\n"
            
            for fk in details['foreign_keys']:
                content += f"| {fk['name']} | {fk['column']} | {fk['reference_table']} | {fk['reference_column']} | {fk.get('description', '')} |\n"
            
            content += "\n"
        
        # チェック制約
        if 'check_constraints' in details and details['check_constraints']:
            content += "## ✅ チェック制約\n\n"
            content += "| 制約名 | 条件 | 説明 |\n"
            content += "|--------|------|------|\n"
            
            for check in details['check_constraints']:
                content += f"| {check['name']} | {check['condition']} | {check.get('description', '')} |\n"
            
            content += "\n"
        
        return content
    
    def _generate_business_rules(self, details: Dict[str, Any]) -> str:
        """業務ルール生成"""
        if 'business_rules' not in details or not details['business_rules']:
            return ""
        
        content = "## 📋 業務ルール\n\n"
        
        for i, rule in enumerate(details['business_rules'], 1):
            content += f"{i}. **{rule['title']}**\n"
            content += f"   {rule['description']}\n\n"
        
        return content
    
    def _generate_notes(self, details: Dict[str, Any]) -> str:
        """備考生成"""
        if 'notes' not in details or not details['notes']:
            return ""
        
        content = "## 📝 備考\n\n"
        
        for note in details['notes']:
            content += f"- {note}\n"
        
        content += "\n"
        return content
    
    def generate_all_table_definitions(self, target_tables: Optional[List[str]] = None) -> Dict[str, str]:
        """全テーブル定義書を生成"""
        results = {}
        
        tables_to_process = target_tables if target_tables else list(self.tables_info.keys())
        
        for table_name in tables_to_process:
            try:
                print(f"📋 {table_name} の定義書を生成中...")
                
                # テーブル定義書生成
                content = self.generate_table_definition(table_name)
                
                # ファイル名生成（命名規則: テーブル定義書_テーブル名_論理名.md）
                table_info = self.tables_info[table_name]
                logical_name = table_info['logical_name'].replace('/', '_').replace(' ', '_')
                filename = f"テーブル定義書_{table_name}_{logical_name}.md"
                
                # ファイル保存
                output_file = self.output_dir / filename
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                results[table_name] = str(output_file)
                print(f"✅ {filename} を生成しました")
                
            except Exception as e:
                print(f"❌ {table_name} の生成に失敗: {e}")
                results[table_name] = f"エラー: {e}"
        
        return results

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="テーブル定義書生成スクリプト（最終版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全テーブルの定義書を生成
  python3 create_table_definitions_final.py --all
  
  # 特定のテーブルの定義書を生成
  python3 create_table_definitions_final.py --tables MST_Employee MST_Department
  
  # プロフィール管理テーブルのみ生成
  python3 create_table_definitions_final.py --category profile
        """
    )
    
    parser.add_argument(
        '--all', '-a',
        action='store_true',
        help='全テーブルの定義書を生成'
    )
    
    parser.add_argument(
        '--tables', '-t',
        nargs='+',
        help='生成対象テーブル名（複数指定可能）'
    )
    
    parser.add_argument(
        '--category', '-c',
        choices=['profile', 'skill', 'auth', 'system'],
        help='カテゴリ別生成（profile: プロフィール管理, skill: スキル管理, auth: 認証・権限, system: システム）'
    )
    
    parser.add_argument(
        '--base-dir', '-b',
        help='ベースディレクトリ（デフォルト: スクリプトのディレクトリ）'
    )
    
    args = parser.parse_args()
    
    try:
        # ベースディレクトリ設定
        base_dir = Path(args.base_dir) if args.base_dir else Path(__file__).parent
        
        # 生成器初期化
        generator = TableDefinitionGenerator(base_dir)
        
        # 対象テーブル決定
        target_tables = None
        
        if args.tables:
            target_tables = args.tables
        elif args.category:
            category_map = {
                'profile': ['MST_Employee', 'MST_Department', 'MST_Position', 'MST_JobType'],
                'skill': ['MST_SkillCategory', 'MST_SkillItem', 'MST_SkillGrade', 'TRN_EmployeeSkillGrade'],
                'auth': ['MST_UserAuth', 'MST_Role', 'MST_Permission', 'MST_UserRole', 'MST_RolePermission'],
                'system': ['SYS_SystemLog', 'SYS_AuditLog', 'SYS_Configuration']
            }
            target_tables = category_map.get(args.category, [])
        
        # 生成実行
        print("🚀 テーブル定義書生成開始")
        print("=" * 60)
        
        results = generator.generate_all_table_definitions(target_tables)
        
        # 結果表示
        print("\n📊 生成結果")
        print("=" * 60)
        
        success_count = 0
        error_
