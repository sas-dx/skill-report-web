"""
DDL統一パーサー

DDL（SQL）ファイルの解析と検証を行う
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from .base_parser import BaseParser
from ..core import ValidationResult, ParseError


class DdlParser(BaseParser):
    """DDL専用パーサー"""
    
    def __init__(self):
        super().__init__("ddl")
        self.table_pattern = re.compile(
            r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([^\s(]+)\s*\(',
            re.IGNORECASE | re.MULTILINE
        )
        self.column_pattern = re.compile(
            r'^\s*([^\s]+)\s+([^\s,]+)(?:\s*\([^)]+\))?\s*(.*?)(?:,\s*$|$)',
            re.MULTILINE
        )
        self.constraint_pattern = re.compile(
            r'(?:CONSTRAINT\s+([^\s]+)\s+)?(PRIMARY\s+KEY|FOREIGN\s+KEY|UNIQUE|CHECK)\s*\([^)]+\)',
            re.IGNORECASE
        )
    
    def get_supported_extensions(self) -> List[str]:
        """サポートする拡張子"""
        return ['.sql', '.ddl']
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        DDLファイルを解析
        
        Args:
            file_path: DDLファイルパス
            
        Returns:
            解析されたデータ
            
        Raises:
            ParseError: 解析エラー
        """
        self._validate_file_exists(file_path)
        self._validate_file_readable(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not content.strip():
                raise ParseError(f"DDLファイルが空です: {file_path}", file_path)
            
            # テーブル定義を抽出
            tables = self._extract_tables(content)
            
            if not tables:
                raise ParseError(f"テーブル定義が見つかりません: {file_path}", file_path)
            
            result = {
                'file_path': file_path,
                'content': content,
                'tables': tables,
                'table_count': len(tables)
            }
            
            self.logger.debug(f"DDL解析完了: {file_path}, テーブル数: {len(tables)}")
            return result
            
        except Exception as e:
            if isinstance(e, ParseError):
                raise
            raise ParseError(f"DDL解析エラー: {str(e)}", file_path)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        DDLデータの妥当性を検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            検証結果
        """
        result = ValidationResult(is_valid=True)
        
        # 基本構造の検証
        if 'tables' not in data:
            result.add_error("テーブル定義が存在しません")
            return result
        
        tables = data['tables']
        if not isinstance(tables, list):
            result.add_error("テーブル定義はリスト形式である必要があります")
            return result
        
        if len(tables) == 0:
            result.add_error("最低1つのテーブル定義が必要です")
            return result
        
        # 各テーブルの検証
        for i, table in enumerate(tables):
            self._validate_table(table, i, result)
        
        return result
    
    def _extract_tables(self, content: str) -> List[Dict[str, Any]]:
        """DDLからテーブル定義を抽出"""
        tables = []
        
        # CREATE TABLE文を検索
        table_matches = self.table_pattern.finditer(content)
        
        for match in table_matches:
            table_name = match.group(1).strip('`"[]')
            start_pos = match.start()
            
            # テーブル定義の終了位置を検索
            paren_count = 0
            end_pos = start_pos
            in_table_def = False
            
            for i, char in enumerate(content[start_pos:], start_pos):
                if char == '(':
                    paren_count += 1
                    in_table_def = True
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0 and in_table_def:
                        end_pos = i + 1
                        break
            
            if end_pos > start_pos:
                table_def = content[start_pos:end_pos]
                table_info = self._parse_table_definition(table_name, table_def)
                tables.append(table_info)
        
        return tables
    
    def _parse_table_definition(self, table_name: str, table_def: str) -> Dict[str, Any]:
        """個別のテーブル定義を解析"""
        # カラム定義部分を抽出
        paren_start = table_def.find('(')
        paren_end = table_def.rfind(')')
        
        if paren_start == -1 or paren_end == -1:
            return {
                'name': table_name,
                'columns': [],
                'constraints': [],
                'definition': table_def
            }
        
        columns_section = table_def[paren_start + 1:paren_end]
        
        # カラムと制約を分離
        columns = []
        constraints = []
        
        lines = [line.strip() for line in columns_section.split('\n') if line.strip()]
        
        for line in lines:
            line = line.rstrip(',')
            
            # 制約かカラムかを判定
            if self._is_constraint_line(line):
                constraint_info = self._parse_constraint(line)
                if constraint_info:
                    constraints.append(constraint_info)
            else:
                column_info = self._parse_column(line)
                if column_info:
                    columns.append(column_info)
        
        return {
            'name': table_name,
            'columns': columns,
            'constraints': constraints,
            'definition': table_def
        }
    
    def _is_constraint_line(self, line: str) -> bool:
        """行が制約定義かどうかを判定"""
        constraint_keywords = [
            'PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'CHECK', 'CONSTRAINT'
        ]
        line_upper = line.upper()
        return any(keyword in line_upper for keyword in constraint_keywords)
    
    def _parse_column(self, line: str) -> Optional[Dict[str, Any]]:
        """カラム定義を解析"""
        # 基本的なカラム定義のパターンマッチング
        parts = line.split()
        if len(parts) < 2:
            return None
        
        column_name = parts[0].strip('`"[]')
        data_type = parts[1]
        
        # 属性を解析
        line_upper = line.upper()
        nullable = 'NOT NULL' not in line_upper
        primary_key = 'PRIMARY KEY' in line_upper
        unique = 'UNIQUE' in line_upper
        
        # デフォルト値を抽出
        default_match = re.search(r'DEFAULT\s+([^,\s]+)', line, re.IGNORECASE)
        default_value = default_match.group(1) if default_match else None
        
        return {
            'name': column_name,
            'type': data_type,
            'nullable': nullable,
            'primary_key': primary_key,
            'unique': unique,
            'default': default_value
        }
    
    def _parse_constraint(self, line: str) -> Optional[Dict[str, Any]]:
        """制約定義を解析"""
        line_upper = line.upper()
        
        constraint_type = None
        if 'PRIMARY KEY' in line_upper:
            constraint_type = 'PRIMARY_KEY'
        elif 'FOREIGN KEY' in line_upper:
            constraint_type = 'FOREIGN_KEY'
        elif 'UNIQUE' in line_upper:
            constraint_type = 'UNIQUE'
        elif 'CHECK' in line_upper:
            constraint_type = 'CHECK'
        
        if not constraint_type:
            return None
        
        # 制約名を抽出
        name_match = re.search(r'CONSTRAINT\s+([^\s]+)', line, re.IGNORECASE)
        constraint_name = name_match.group(1) if name_match else None
        
        return {
            'name': constraint_name,
            'type': constraint_type,
            'definition': line
        }
    
    def _validate_table(self, table: Dict[str, Any], index: int, result: ValidationResult) -> None:
        """個別テーブルの検証"""
        if not isinstance(table, dict):
            result.add_error(f"テーブル[{index}]は辞書形式である必要があります")
            return
        
        # テーブル名の検証
        if 'name' not in table:
            result.add_error(f"テーブル[{index}]にテーブル名がありません")
        elif not table['name']:
            result.add_error(f"テーブル[{index}]のテーブル名が空です")
        
        # カラムの検証
        if 'columns' not in table:
            result.add_error(f"テーブル[{index}]にカラム定義がありません")
        elif not isinstance(table['columns'], list):
            result.add_error(f"テーブル[{index}]のカラム定義はリスト形式である必要があります")
        elif len(table['columns']) == 0:
            result.add_error(f"テーブル[{index}]には最低1つのカラムが必要です")
    
    def extract_table_names(self, data: Dict[str, Any]) -> List[str]:
        """テーブル名のリストを抽出"""
        if 'tables' not in data:
            return []
        
        return [table.get('name', '') for table in data['tables'] if table.get('name')]
    
    def get_table_info(self, data: Dict[str, Any], table_name: str) -> Optional[Dict[str, Any]]:
        """特定のテーブル情報を取得"""
        if 'tables' not in data:
            return None
        
        for table in data['tables']:
            if table.get('name') == table_name:
                return table
        
        return None
    
    def compare_with_yaml(self, ddl_data: Dict[str, Any], yaml_data: Dict[str, Any]) -> ValidationResult:
        """DDLとYAMLの整合性をチェック"""
        result = ValidationResult(is_valid=True)
        
        # テーブル名の比較
        ddl_table_name = None
        if ddl_data.get('tables'):
            ddl_table_name = ddl_data['tables'][0].get('name')
        
        yaml_table_name = yaml_data.get('table_name')
        
        if ddl_table_name != yaml_table_name:
            result.add_error(f"テーブル名が一致しません: DDL={ddl_table_name}, YAML={yaml_table_name}")
        
        # カラム数の比較
        if ddl_data.get('tables'):
            ddl_columns = ddl_data['tables'][0].get('columns', [])
            yaml_columns = yaml_data.get('columns', [])
            
            if len(ddl_columns) != len(yaml_columns):
                result.add_warning(f"カラム数が異なります: DDL={len(ddl_columns)}, YAML={len(yaml_columns)}")
        
        return result
