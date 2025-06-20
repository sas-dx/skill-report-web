#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
サンプルデータINSERT文生成モジュール（改良版）

テーブル詳細YAMLファイルのsample_dataセクションを使用して、
PostgreSQL用のINSERT文を生成します。

改良点：
- 外部キー依存関係を考慮した実行順序の自動決定
- より正確なデータ型変換
- 検証機能の統合強化
- 詳細なエラーハンドリング
- トランザクション対応のSQL生成
"""

import os
import sys
import yaml
import glob
import uuid
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime
from colorama import Fore, Style, init

# colorama初期化
init()

# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
TABLE_DETAILS_DIR = os.path.join(PROJECT_ROOT, "docs/design/database/table-details")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs/design/database/data")


class TableDependencyResolver:
    """テーブル依存関係解決クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.dependencies = {}  # table_name -> [referenced_tables]
        self.tables_data = {}   # table_name -> yaml_data
    
    def load_table_dependencies(self, table_names: List[str]) -> bool:
        """テーブルの依存関係を読み込み"""
        for table_name in table_names:
            yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
            
            if not os.path.exists(yaml_file):
                if self.verbose:
                    print(f"{Fore.YELLOW}⚠️ ファイル {yaml_file} が存在しません{Style.RESET_ALL}")
                continue
            
            yaml_data = self._load_yaml_file(yaml_file)
            if not yaml_data:
                continue
            
            self.tables_data[table_name] = yaml_data
            
            # 外部キー依存関係を抽出
            dependencies = []
            foreign_keys = yaml_data.get('foreign_keys', [])
            
            for fk in foreign_keys:
                if isinstance(fk, dict) and 'references' in fk:
                    ref_table = fk['references'].get('table')
                    if ref_table and ref_table != table_name:  # 自己参照は除外
                        dependencies.append(ref_table)
            
            self.dependencies[table_name] = dependencies
            
            if self.verbose:
                print(f"{Fore.BLUE}テーブル {table_name}: 依存関係 {dependencies}{Style.RESET_ALL}")
        
        return True
    
    def resolve_execution_order(self, table_names: List[str]) -> List[str]:
        """実行順序を解決（トポロジカルソート）"""
        # 利用可能なテーブルのみを対象とする
        available_tables = [t for t in table_names if t in self.tables_data]
        
        if not available_tables:
            return []
        
        # トポロジカルソート実装
        visited = set()
        temp_visited = set()
        result = []
        
        def visit(table: str):
            if table in temp_visited:
                # 循環依存を検出
                if self.verbose:
                    print(f"{Fore.YELLOW}⚠️ 循環依存を検出: {table}{Style.RESET_ALL}")
                return
            
            if table in visited:
                return
            
            temp_visited.add(table)
            
            # 依存テーブルを先に処理
            for dep_table in self.dependencies.get(table, []):
                if dep_table in available_tables:
                    visit(dep_table)
            
            temp_visited.remove(table)
            visited.add(table)
            result.append(table)
        
        for table in available_tables:
            if table not in visited:
                visit(table)
        
        if self.verbose:
            print(f"{Fore.GREEN}✓ 実行順序: {result}{Style.RESET_ALL}")
        
        return result
    
    def _load_yaml_file(self, file_path: str) -> Dict[str, Any]:
        """YAMLファイルを読み込む"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            if self.verbose:
                print(f"{Fore.RED}エラー: {file_path} の読み込みに失敗しました: {e}{Style.RESET_ALL}")
            return {}


class EnhancedSQLGenerator:
    """改良版SQL生成クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
    
    def format_value_for_sql(self, value: Any, col_type: str, col_name: str = "") -> str:
        """値をSQL用にフォーマット（改良版）"""
        if value is None or value == "null":
            return "NULL"
        
        # データ型の正規化
        col_type_upper = col_type.upper()
        
        # 文字列型の詳細判定
        if any(t in col_type_upper for t in ['VARCHAR', 'TEXT', 'CHAR', 'STRING']):
            escaped_value = str(value).replace("'", "''")
            return f"'{escaped_value}'"
        
        # 数値型の詳細判定
        elif any(t in col_type_upper for t in ['INT', 'BIGINT', 'SMALLINT', 'SERIAL']):
            try:
                return str(int(value))
            except (ValueError, TypeError):
                if self.verbose:
                    print(f"{Fore.YELLOW}⚠️ カラム {col_name}: 整数変換失敗 '{value}' -> NULL{Style.RESET_ALL}")
                return "NULL"
        
        # 小数点数型
        elif any(t in col_type_upper for t in ['DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE', 'REAL']):
            try:
                return str(float(value))
            except (ValueError, TypeError):
                if self.verbose:
                    print(f"{Fore.YELLOW}⚠️ カラム {col_name}: 数値変換失敗 '{value}' -> NULL{Style.RESET_ALL}")
                return "NULL"
        
        # ブール型
        elif 'BOOLEAN' in col_type_upper or 'BOOL' in col_type_upper:
            if isinstance(value, bool):
                return 'TRUE' if value else 'FALSE'
            elif isinstance(value, str):
                return 'TRUE' if value.lower() in ['true', 't', '1', 'yes', 'y'] else 'FALSE'
            else:
                return 'TRUE' if value else 'FALSE'
        
        # 日付・時刻型
        elif any(t in col_type_upper for t in ['DATE', 'DATETIME', 'TIMESTAMP', 'TIME']):
            return f"'{value}'"
        
        # JSON型
        elif 'JSON' in col_type_upper:
            if isinstance(value, (dict, list)):
                import json
                escaped_json = json.dumps(value, ensure_ascii=False).replace("'", "''")
                return f"'{escaped_json}'"
            else:
                escaped_value = str(value).replace("'", "''")
                return f"'{escaped_value}'"
        
        # UUID型
        elif 'UUID' in col_type_upper:
            return f"'{value}'"
        
        # その他の場合は文字列として扱う
        else:
            escaped_value = str(value).replace("'", "''")
            return f"'{escaped_value}'"
    
    def generate_insert_statements(self, table_name: str, yaml_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """テーブルのINSERT文を生成（改良版）"""
        insert_statements = []
        errors = []
        
        # sample_dataの存在確認
        if 'sample_data' not in yaml_data:
            errors.append(f"sample_dataセクションが存在しません")
            return [], errors
        
        sample_data = yaml_data['sample_data']
        if not isinstance(sample_data, list) or len(sample_data) == 0:
            errors.append(f"sample_dataが空です")
            return [], errors
        
        # カラム定義の取得
        column_info = self._extract_column_info(yaml_data)
        if not column_info:
            errors.append(f"カラム定義が存在しません")
            return [], errors
        
        # 各レコードのINSERT文生成
        for i, record in enumerate(sample_data):
            if not isinstance(record, dict):
                errors.append(f"sample_data[{i}]が辞書形式ではありません")
                continue
            
            try:
                insert_sql = self._generate_single_insert(table_name, record, column_info)
                if insert_sql:
                    insert_statements.append(insert_sql)
            except Exception as e:
                errors.append(f"sample_data[{i}]のINSERT文生成に失敗: {str(e)}")
        
        return insert_statements, errors
    
    def _extract_column_info(self, yaml_data: Dict[str, Any]) -> Dict[str, str]:
        """カラム情報を抽出"""
        column_info = {}
        
        # columns形式の処理
        for col in yaml_data.get('columns', []):
            if isinstance(col, dict):
                col_name = col.get('name')
                col_type = col.get('type', '').upper()
                if col_name:
                    column_info[col_name] = col_type
        
        # business_columns形式の処理
        for col in yaml_data.get('business_columns', []):
            if isinstance(col, dict):
                col_name = col.get('name')
                col_type = col.get('type', '').upper()
                length = col.get('length')
                if length and col_type in ['VARCHAR', 'CHAR', 'DECIMAL']:
                    col_type = f"{col_type}({length})"
                if col_name:
                    column_info[col_name] = col_type
        
        # 共通カラムを追加（存在しない場合）
        default_columns = {
            'id': 'VARCHAR(50)',
            'created_at': 'TIMESTAMP',
            'updated_at': 'TIMESTAMP',
            'is_deleted': 'BOOLEAN'
        }
        
        for col_name, col_type in default_columns.items():
            if col_name not in column_info:
                column_info[col_name] = col_type
        
        return column_info
    
    def _generate_single_insert(self, table_name: str, record: Dict[str, Any], column_info: Dict[str, str]) -> str:
        """単一レコードのINSERT文を生成"""
        columns_list = []
        values_list = []
        
        # sample_dataの値を追加
        for col_name, value in record.items():
            if col_name in column_info:
                columns_list.append(col_name)
                col_type = column_info[col_name]
                formatted_value = self.format_value_for_sql(value, col_type, col_name)
                values_list.append(formatted_value)
        
        # 共通カラムのデフォルト値を追加（sample_dataに含まれていない場合）
        self._add_default_values(record, columns_list, values_list, column_info, table_name)
        
        if columns_list and values_list:
            columns_str = ', '.join(columns_list)
            values_str = ', '.join(values_list)
            return f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
        
        return ""
    
    def _add_default_values(self, record: Dict[str, Any], columns_list: List[str], 
                          values_list: List[str], column_info: Dict[str, str], table_name: str):
        """デフォルト値を追加"""
        # ID生成
        if 'id' not in record and 'id' in column_info:
            columns_list.append('id')
            table_prefix = table_name[:3].lower()
            short_uuid = str(uuid.uuid4())[:8]
            generated_id = f"{table_prefix}_{short_uuid}"
            values_list.append(f"'{generated_id}'")
        
        # タイムスタンプ
        if 'created_at' not in record and 'created_at' in column_info:
            columns_list.append('created_at')
            values_list.append('CURRENT_TIMESTAMP')
        
        if 'updated_at' not in record and 'updated_at' in column_info:
            columns_list.append('updated_at')
            values_list.append('CURRENT_TIMESTAMP')
        
        # 論理削除フラグ
        if 'is_deleted' not in record and 'is_deleted' in column_info:
            columns_list.append('is_deleted')
            values_list.append('FALSE')


class EnhancedSampleDataGenerator:
    """改良版サンプルデータ生成クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.dependency_resolver = TableDependencyResolver(verbose)
        self.sql_generator = EnhancedSQLGenerator(verbose)
    
    def generate_sample_data_sql(self, tables: Optional[List[str]] = None) -> Dict[str, Any]:
        """サンプルデータINSERT文を生成（改良版）"""
        results = {
            'success': True,
            'total_tables': 0,
            'generated_tables': 0,
            'total_records': 0,
            'execution_order': [],
            'tables': {},
            'errors': [],
            'warnings': []
        }
        
        # 出力ディレクトリの作成
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        # 対象テーブルの決定
        if tables:
            table_list = tables
        else:
            table_list = self._get_all_tables()
        
        results['total_tables'] = len(table_list)
        
        # 依存関係の解決
        if not self.dependency_resolver.load_table_dependencies(table_list):
            results['errors'].append("依存関係の読み込みに失敗しました")
            results['success'] = False
            return results
        
        # 実行順序の決定
        execution_order = self.dependency_resolver.resolve_execution_order(table_list)
        results['execution_order'] = execution_order
        
        if self.verbose:
            print(f"{Fore.CYAN}=== 実行順序決定完了 ==={Style.RESET_ALL}")
            print(f"対象テーブル数: {len(execution_order)}")
            print(f"実行順序: {execution_order}")
        
        # 各テーブルの処理（依存関係順）
        all_insert_statements = []
        
        for table_name in execution_order:
            if self.verbose:
                print(f"\n{Fore.BLUE}テーブル {table_name} のサンプルデータ処理を開始...{Style.RESET_ALL}")
            
            yaml_data = self.dependency_resolver.tables_data.get(table_name)
            if not yaml_data:
                error_msg = f"テーブル {table_name}: YAMLデータが見つかりません"
                results['errors'].append(error_msg)
                continue
            
            # INSERT文生成
            insert_statements, errors = self.sql_generator.generate_insert_statements(table_name, yaml_data)
            
            if errors:
                results['errors'].extend([f"{table_name}: {error}" for error in errors])
                if self.verbose:
                    for error in errors:
                        print(f"{Fore.RED}❌ {table_name}: {error}{Style.RESET_ALL}")
                continue
            
            if insert_statements:
                results['generated_tables'] += 1
                results['total_records'] += len(insert_statements)
                results['tables'][table_name] = {
                    'records': len(insert_statements),
                    'statements': insert_statements
                }
                
                # ファイル出力
                self._write_table_file(table_name, insert_statements)
                
                # 統合ファイル用
                all_insert_statements.extend([
                    f"-- {table_name} サンプルデータ",
                    f"-- レコード数: {len(insert_statements)}",
                    ""
                ] + insert_statements + [""])
                
                if self.verbose:
                    print(f"{Fore.GREEN}✓ テーブル {table_name}: {len(insert_statements)}件のINSERT文を生成しました{Style.RESET_ALL}")
        
        # 統合ファイルの出力
        self._write_combined_file(all_insert_statements, results)
        
        # 結果サマリー
        if results['errors']:
            results['success'] = False
        
        if self.verbose:
            self._print_summary(results)
        
        return results
    
    def _get_all_tables(self) -> List[str]:
        """全テーブル名を取得"""
        yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
        table_list = []
        for yaml_file in yaml_files:
            table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
            if table_name != "MST_TEMPLATE":
                table_list.append(table_name)
        return table_list
    
    def _write_table_file(self, table_name: str, insert_statements: List[str]):
        """個別テーブルファイルを出力"""
        output_file = os.path.join(OUTPUT_DIR, f"sample_data_{table_name}.sql")
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"-- サンプルデータ INSERT文: {table_name}\n")
                f.write(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- レコード数: {len(insert_statements)}\n\n")
                f.write("BEGIN;\n\n")
                
                for stmt in insert_statements:
                    f.write(stmt + "\n")
                
                f.write(f"\nCOMMIT;\n")
                f.write(f"\n-- {table_name} サンプルデータ終了\n")
            
            if self.verbose:
                print(f"{Fore.GREEN}✓ ファイル出力: {output_file}{Style.RESET_ALL}")
                
        except Exception as e:
            error_msg = f"テーブル {table_name}: ファイル出力に失敗しました: {str(e)}"
            if self.verbose:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
    
    def _write_combined_file(self, all_insert_statements: List[str], results: Dict[str, Any]):
        """統合ファイルを出力"""
        if not all_insert_statements:
            return
        
        combined_file = os.path.join(OUTPUT_DIR, "sample_data_all_enhanced.sql")
        try:
            with open(combined_file, 'w', encoding='utf-8') as f:
                f.write("-- 全テーブル サンプルデータ INSERT文（改良版）\n")
                f.write(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- 対象テーブル数: {results['generated_tables']}\n")
                f.write(f"-- 総レコード数: {results['total_records']}\n")
                f.write(f"-- 実行順序: {', '.join(results['execution_order'])}\n\n")
                f.write("-- トランザクション開始\n")
                f.write("BEGIN;\n\n")
                f.write("-- 外部キー制約を一時的に無効化（必要に応じて）\n")
                f.write("-- SET session_replication_role = replica;\n\n")
                
                for stmt in all_insert_statements:
                    f.write(stmt + "\n")
                
                f.write("\n-- 外部キー制約を再有効化\n")
                f.write("-- SET session_replication_role = DEFAULT;\n\n")
                f.write("-- トランザクション終了\n")
                f.write("COMMIT;\n\n")
                f.write("-- 全テーブル サンプルデータ終了\n")
            
            if self.verbose:
                print(f"\n{Fore.GREEN}✓ 統合ファイル出力: {combined_file}{Style.RESET_ALL}")
                
        except Exception as e:
            error_msg = f"統合ファイルの出力に失敗しました: {str(e)}"
            results['errors'].append(error_msg)
            if self.verbose:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
    
    def _print_summary(self, results: Dict[str, Any]):
        """結果サマリーを出力"""
        print(f"\n{Fore.CYAN}=== サンプルデータINSERT文生成結果（改良版） ==={Style.RESET_ALL}")
        print(f"対象テーブル数: {results['total_tables']}")
        print(f"生成成功テーブル数: {results['generated_tables']}")
        print(f"総レコード数: {results['total_records']}")
        print(f"エラー数: {len(results['errors'])}")
        print(f"警告数: {len(results['warnings'])}")
        print(f"実行順序: {', '.join(results['execution_order'])}")
        
        if results['errors']:
            print(f"\n{Fore.RED}エラー詳細:{Style.RESET_ALL}")
            for error in results['errors']:
                print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")
        
        if results['warnings']:
            print(f"\n{Fore.YELLOW}警告詳細:{Style.RESET_ALL}")
            for warning in results['warnings']:
                print(f"  {Fore.YELLOW}- {warning}{Style.RESET_ALL}")


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='サンプルデータINSERT文生成（改良版）')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    parser.add_argument('--output-format', choices=['sql', 'json'], default='sql', help='出力形式')
    args = parser.parse_args()
    
    tables = args.tables.split(',') if args.tables else None
    
    generator = EnhancedSampleDataGenerator(args.verbose)
    result = generator.generate_sample_data_sql(tables)
    
    if args.output_format == 'json':
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
