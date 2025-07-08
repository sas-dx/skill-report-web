"""
サンプルデータジェネレーター（YAMLベース）

テーブル詳細定義YAMLファイルのsample_dataセクションを使用して、
PostgreSQL用のINSERT文を生成します。

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-21
実装者: AI駆動開発チーム

改良点：
- 外部キー依存関係を考慮した実行順序の自動決定
- より正確なデータ型変換
- 検証機能の統合強化
- 詳細なエラーハンドリング
- トランザクション対応のSQL生成
- BaseGeneratorインターフェース準拠
"""

import os
import sys
import yaml
import glob
import uuid
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime
from pathlib import Path
import logging

from .base_generator import BaseGenerator
from ..core.models import TableDefinition
from ..core.exceptions import GenerationError

# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../../.."))
TABLE_DETAILS_DIR = os.path.join(PROJECT_ROOT, "docs/design/database/table-details")


class TableDependencyResolver:
    """テーブル依存関係解決クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.dependencies = {}  # table_name -> [referenced_tables]
        self.tables_data = {}   # table_name -> yaml_data
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def load_table_dependencies(self, table_names: List[str]) -> bool:
        """テーブルの依存関係を読み込み"""
        for table_name in table_names:
            yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
            
            if not os.path.exists(yaml_file):
                if self.verbose:
                    self.logger.warning(f"ファイル {yaml_file} が存在しません")
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
                self.logger.info(f"テーブル {table_name}: 依存関係 {dependencies}")
        
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
                    self.logger.warning(f"循環依存を検出: {table}")
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
            self.logger.info(f"実行順序: {result}")
        
        return result
    
    def _load_yaml_file(self, file_path: str) -> Dict[str, Any]:
        """YAMLファイルを読み込む"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            if self.verbose:
                self.logger.error(f"{file_path} の読み込みに失敗しました: {e}")
            return {}


class EnhancedSQLGenerator:
    """改良版SQL生成クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
    
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
                    self.logger.warning(f"カラム {col_name}: 整数変換失敗 '{value}' -> NULL")
                return "NULL"
        
        # 小数点数型
        elif any(t in col_type_upper for t in ['DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE', 'REAL']):
            try:
                return str(float(value))
            except (ValueError, TypeError):
                if self.verbose:
                    self.logger.warning(f"カラム {col_name}: 数値変換失敗 '{value}' -> NULL")
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


class SampleDataGenerator(BaseGenerator):
    """YAMLベースサンプルデータ生成クラス（BaseGenerator準拠）"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.verbose = self.config.get('verbose', False)
        self.dependency_resolver = TableDependencyResolver(self.verbose)
        self.sql_generator = EnhancedSQLGenerator(self.verbose)
    
    def generate(self, table_def: TableDefinition, output_path: Optional[str] = None) -> str:
        """
        BaseGeneratorインターフェース準拠のgenerate実装
        
        Args:
            table_def: テーブル定義オブジェクト
            output_path: 出力ファイルパス（使用しない）
            
        Returns:
            str: 生成されたINSERT文
        """
        try:
            self._log_generation_start(table_def)
            
            # YAMLファイルからデータを読み込み
            yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_def.table_name}_details.yaml")
            
            if not os.path.exists(yaml_file):
                raise GenerationError(f"YAMLファイルが存在しません: {yaml_file}")
            
            yaml_data = self._load_yaml_file(yaml_file)
            if not yaml_data:
                raise GenerationError(f"YAMLファイルの読み込みに失敗しました: {yaml_file}")
            
            # INSERT文生成
            insert_statements, errors = self.sql_generator.generate_insert_statements(
                table_def.table_name, yaml_data
            )
            
            if errors:
                error_msg = f"INSERT文生成エラー: {'; '.join(errors)}"
                raise GenerationError(error_msg)
            
            if not insert_statements:
                self.logger.warning(f"テーブル {table_def.table_name}: INSERT文が生成されませんでした")
                return self._generate_empty_sql(table_def.table_name)
            
            # SQL文を組み立て
            sql_content = self._build_sql_content(table_def.table_name, insert_statements)
            
            self._log_generation_complete(table_def)
            return sql_content
            
        except Exception as e:
            raise self._handle_generation_error(e, table_def, "サンプルデータ生成")
    
    def get_file_extension(self) -> str:
        """ファイル拡張子を取得"""
        return '.sql'
    
    def generate_sample_data_sql(self, tables: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        複数テーブルのサンプルデータINSERT文を生成（従来互換）
        
        Args:
            tables: 対象テーブルリスト（Noneの場合は全テーブル）
            
        Returns:
            Dict[str, Any]: 生成結果
        """
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
        
        try:
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
                self.logger.info(f"実行順序決定完了: {len(execution_order)}テーブル")
            
            # 各テーブルの処理（依存関係順）
            for table_name in execution_order:
                if self.verbose:
                    self.logger.info(f"テーブル {table_name} のサンプルデータ処理を開始...")
                
                yaml_data = self.dependency_resolver.tables_data.get(table_name)
                if not yaml_data:
                    error_msg = f"テーブル {table_name}: YAMLデータが見つかりません"
                    results['errors'].append(error_msg)
                    continue
                
                # INSERT文生成
                insert_statements, errors = self.sql_generator.generate_insert_statements(table_name, yaml_data)
                
                if errors:
                    results['errors'].extend([f"{table_name}: {error}" for error in errors])
                    continue
                
                if insert_statements:
                    results['generated_tables'] += 1
                    results['total_records'] += len(insert_statements)
                    results['tables'][table_name] = {
                        'records': len(insert_statements),
                        'statements': insert_statements
                    }
                    
                    if self.verbose:
                        self.logger.info(f"テーブル {table_name}: {len(insert_statements)}件のINSERT文を生成")
            
            # 結果サマリー
            if results['errors']:
                results['success'] = False
            
            if self.verbose:
                self._print_summary(results)
            
        except Exception as e:
            results['success'] = False
            results['errors'].append(f"サンプルデータ生成エラー: {str(e)}")
            self.logger.error(f"サンプルデータ生成エラー: {e}")
        
        return results
    
    def _load_yaml_file(self, file_path: str) -> Dict[str, Any]:
        """YAMLファイルを読み込む"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"{file_path} の読み込みに失敗しました: {e}")
            return {}
    
    def _get_all_tables(self) -> List[str]:
        """全テーブル名を取得"""
        yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
        table_list = []
        for yaml_file in yaml_files:
            table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
            if table_name != "MST_TEMPLATE":
                table_list.append(table_name)
        return table_list
    
    def _build_sql_content(self, table_name: str, insert_statements: List[str]) -> str:
        """SQL内容を構築"""
        lines = []
        lines.append(f"-- サンプルデータ INSERT文: {table_name}")
        lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"-- レコード数: {len(insert_statements)}")
        lines.append("")
        lines.append("BEGIN;")
        lines.append("")
        
        for stmt in insert_statements:
            lines.append(stmt)
        
        lines.append("")
        lines.append("COMMIT;")
        lines.append("")
        lines.append(f"-- {table_name} サンプルデータ終了")
        
        return "\n".join(lines)
    
    def _generate_empty_sql(self, table_name: str) -> str:
        """空のSQL文を生成"""
        lines = []
        lines.append(f"-- サンプルデータ INSERT文: {table_name}")
        lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("-- 注意: sample_dataセクションが存在しないため、INSERT文は生成されませんでした")
        lines.append("")
        lines.append("-- BEGIN;")
        lines.append("-- INSERT文がここに生成される予定でした")
        lines.append("-- COMMIT;")
        
        return "\n".join(lines)
    
    def _print_summary(self, results: Dict[str, Any]):
        """結果サマリーを出力"""
        self.logger.info("=== サンプルデータINSERT文生成結果 ===")
        self.logger.info(f"対象テーブル数: {results['total_tables']}")
        self.logger.info(f"生成成功テーブル数: {results['generated_tables']}")
        self.logger.info(f"総レコード数: {results['total_records']}")
        self.logger.info(f"エラー数: {len(results['errors'])}")
        self.logger.info(f"実行順序: {', '.join(results['execution_order'])}")
        
        if results['errors']:
            self.logger.error("エラー詳細:")
            for error in results['errors']:
                self.logger.error(f"  - {error}")


# 従来互換性のための関数
def main():
    """メイン関数（従来互換）"""
    import argparse
    
    parser = argparse.ArgumentParser(description='サンプルデータINSERT文生成（YAMLベース）')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    parser.add_argument('--output-format', choices=['sql', 'json'], default='sql', help='出力形式')
    args = parser.parse_args()
    
    tables = args.tables.split(',') if args.tables else None
    config = {'verbose': args.verbose}
    
    generator = SampleDataGenerator(config)
    result = generator.generate_sample_data_sql(tables)
    
    if args.output_format == 'json':
        import json
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
