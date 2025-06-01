#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成スクリプト（ERD機能付き修正版）

プロフィール管理テーブル専用のERD生成機能を追加した修正版
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

class ProfileERDGenerator:
    """プロフィール管理テーブル専用ERD生成クラス"""
    
    def __init__(self, tables_info: Dict[str, Any], details_dir: Path):
        """初期化"""
        self.tables_info = tables_info
        self.details_dir = details_dir
        
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
                'relationship_type': '}o--||',  # 多対一
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
        
        # 2階層目: 1階層テーブルの関連テーブル（プロフィール管理テーブル優先）
        if max_depth >= 2:
            for level1_table in list(related_tables[1]):
                relationships = self.get_foreign_key_relationships(level1_table)
                for rel in relationships:
                    if (rel['to_table'] in self.tables_info and 
                        rel['to_table'] not in related_tables[0] and 
                        rel['to_table'] not in related_tables[1]):
                        # プロフィール管理テーブルまたは重要なテーブルのみ追加
                        if (rel['to_table'] in self.profile_tables or 
                            rel['to_table'].startswith('TRN_') or
                            rel['to_table'].startswith('MST_')):
                            related_tables[2].add(rel['to_table'])
        
        # 表示制限（最大10テーブル）
        if len(related_tables[2]) > 6:
            priority_tables = [t for t in related_tables[2] if t in self.profile_tables]
            other_tables = [t for t in related_tables[2] if t not in self.profile_tables]
            related_tables[2] = set(priority_tables + other_tables[:6-len(priority_tables)])
        
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
                    # 関係線（f-stringを避ける）
                    erd_content += f"    {target_table} " + "}o--|| " + f"{table} : \"{desc}\"\n"
            
            relationships = self.get_foreign_key_relationships(table)
            for rel in relationships:
                if rel['to_table'] == target_table:
                    desc = rel['description'] or "参照"
                    # 関係線（f-stringを避ける）
                    erd_content += f"    {table} " + "}o--|| " + f"{target_table} : \"{desc}\"\n"
        
        # 2階層関係（主要なもののみ）
        for table in sorted(related_tables[2]):
            for level1_table in sorted(related_tables[1]):
                relationships = self.get_foreign_key_relationships(table)
                for rel in relationships:
                    if rel['to_table'] == level1_table:
                        desc = rel['description'] or "関連"
                        # 関係線（f-stringを避ける）
                        erd_content += f"    {table} " + "}o--|| " + f"{level1_table} : \"{desc}\"\n"
                        break  # 1つの関係のみ表示
        
        erd_content += "```\n"
        return erd_content
    
    def generate_relationship_summary(self, target_table: str, related_tables: Dict[int, Set[str]]) -> str:
        """関連テーブル概要表を生成"""
        summary = "### 関連テーブル概要（プロフィール管理）\n"
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
    
    def generate_business_flow_description(self, target_table: str) -> str:
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
        section += "### エンティティ関連図（2階層）\n"
        section += self.generate_mermaid_erd(table_name, related_tables)
        section += "\n"
        
        # 業務フロー説明
        flow_desc = self.generate_business_flow_description(table_name)
        if flow_desc:
            section += flow_desc
            section += "\n"
        
        return section

def main():
    """メイン関数（プロトタイプテスト用）"""
    parser = argparse.ArgumentParser(
        description="テーブル定義書ERD生成修正版",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # MST_EmployeeのERD生成テスト
  python3 create_table_definitions_erd_fixed.py --table MST_Employee
  
  # プロフィール管理テーブル全体のERD生成テスト
  python3 create_table_definitions_erd_fixed.py --profile-tables
        """
    )
    
    parser.add_argument(
        '--table', '-t',
        help='テスト対象テーブル名'
    )
    
    parser.add_argument(
        '--profile-tables', '-p',
        action='store_true',
        help='プロフィール管理テーブル全体をテスト'
    )
    
    parser.add_argument(
        '--base-dir', '-b',
        help='ベースディレクトリ（デフォルト: スクリプトのディレクトリ）'
    )
    
    args = parser.parse_args()
    
    try:
        # ベースディレクトリ設定
        base_dir = Path(args.base_dir) if args.base_dir else Path(__file__).parent
        details_dir = base_dir / "table-details"
        table_list_file = base_dir / "テーブル一覧.md"
        
        # テーブル一覧読み込み
        if not table_list_file.exists():
            raise FileNotFoundError(f"テーブル一覧ファイルが見つかりません: {table_list_file}")
        
        with open(table_list_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # テーブル情報を抽出
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
        
        # ERD生成器初期化
        erd_generator = ProfileERDGenerator(tables_info, details_dir)
        
        # テスト実行
        if args.table:
            test_tables = [args.table]
        elif args.profile_tables:
            test_tables = list(erd_generator.profile_tables.keys())
        else:
            test_tables = ['MST_Employee']  # デフォルト
        
        print("🚀 ERD生成修正版テスト")
        print("=" * 50)
        
        for table_name in test_tables:
            if table_name not in tables_info:
                print(f"❌ テーブルが見つかりません: {table_name}")
                continue
            
            print(f"\n📋 テーブル: {table_name} ({tables_info[table_name]['logical_name']})")
            print("-" * 50)
            
            # ERDセクション生成
            erd_section = erd_generator.generate_related_entity_section(table_name)
            
            if erd_section:
                print(erd_section)
            else:
                print("関連テーブルが見つかりませんでした。")
        
        print("\n🎉 修正版テスト完了！")
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
