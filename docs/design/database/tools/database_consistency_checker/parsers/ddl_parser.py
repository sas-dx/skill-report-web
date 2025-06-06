"""
DDL解析機能 - CREATE TABLE文の詳細解析
"""
import re
import logging
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path

from ..core.models import (
    ColumnDefinition, IndexDefinition, ForeignKeyDefinition, 
    ConstraintDefinition, DDLTable
)


class DDLParser:
    """基本DDL解析クラス（既存機能との互換性維持）"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def parse_ddl_file(self, file_path: Path) -> Optional[str]:
        """DDLファイルからテーブル名を抽出（既存機能）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # CREATE TABLE文からテーブル名を抽出
            match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)', content, re.IGNORECASE)
            if match:
                return match.group(1)
            
            return None
        except Exception as e:
            self.logger.error(f"DDLファイル解析エラー: {file_path} - {e}")
            return None
    
    def get_table_name_from_file(self, file_path: Path) -> Optional[str]:
        """DDLファイルからテーブル名を抽出（既存機能との互換性）"""
        return self.parse_ddl_file(file_path)


class EnhancedDDLParser(DDLParser):
    """拡張DDL解析クラス - データ型整合性チェック用"""
    
    def __init__(self):
        super().__init__()
        self.data_type_patterns = self._init_data_type_patterns()
        self.constraint_patterns = self._init_constraint_patterns()
    
    def _init_data_type_patterns(self) -> Dict[str, str]:
        """データ型解析用の正規表現パターン"""
        return {
            'varchar': r'VARCHAR\s*\(\s*(\d+)\s*\)',
            'char': r'CHAR\s*\(\s*(\d+)\s*\)',
            'int': r'INT(?:EGER)?\s*(?:\(\s*(\d+)\s*\))?',
            'bigint': r'BIGINT\s*(?:\(\s*(\d+)\s*\))?',
            'decimal': r'DECIMAL\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)',
            'float': r'FLOAT\s*(?:\(\s*(\d+)\s*,\s*(\d+)\s*\))?',
            'double': r'DOUBLE\s*(?:\(\s*(\d+)\s*,\s*(\d+)\s*\))?',
            'text': r'TEXT',
            'longtext': r'LONGTEXT',
            'mediumtext': r'MEDIUMTEXT',
            'tinytext': r'TINYTEXT',
            'blob': r'BLOB',
            'longblob': r'LONGBLOB',
            'mediumblob': r'MEDIUMBLOB',
            'tinyblob': r'TINYBLOB',
            'date': r'DATE',
            'datetime': r'DATETIME\s*(?:\(\s*(\d+)\s*\))?',
            'timestamp': r'TIMESTAMP\s*(?:\(\s*(\d+)\s*\))?',
            'time': r'TIME\s*(?:\(\s*(\d+)\s*\))?',
            'year': r'YEAR\s*(?:\(\s*(\d+)\s*\))?',
            'boolean': r'BOOL(?:EAN)?',
            'tinyint': r'TINYINT\s*(?:\(\s*(\d+)\s*\))?',
            'smallint': r'SMALLINT\s*(?:\(\s*(\d+)\s*\))?',
            'mediumint': r'MEDIUMINT\s*(?:\(\s*(\d+)\s*\))?',
            'enum': r'ENUM\s*\(\s*([^)]+)\s*\)',
            'set': r'SET\s*\(\s*([^)]+)\s*\)',
            'json': r'JSON',
        }
    
    def _init_constraint_patterns(self) -> Dict[str, str]:
        """制約解析用の正規表現パターン"""
        return {
            'not_null': r'NOT\s+NULL',
            'null': r'NULL',
            'default': r'DEFAULT\s+([^,\s)]+(?:\s+[^,\s)]+)*)',
            'auto_increment': r'AUTO_INCREMENT',
            'unique': r'UNIQUE',
            'primary_key': r'PRIMARY\s+KEY',
            'comment': r'COMMENT\s+[\'"]([^\'"]*)[\'"]',
        }
    
    def parse_ddl_file_detailed(self, file_path: Path) -> Optional[DDLTable]:
        """DDLファイルの詳細解析"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # CREATE TABLE文を手動で抽出（正規表現では複雑すぎるため）
            table_name, columns_section, table_options = self._extract_create_table_parts(content)
            
            if not table_name:
                self.logger.warning(f"CREATE TABLE文が見つかりません: {file_path}")
                return None
            
            # DDLTableオブジェクトを作成
            ddl_table = DDLTable(table_name=table_name)
            
            # テーブルオプションを解析
            self._parse_table_options(table_options, ddl_table)
            
            # カラム定義を解析
            ddl_table.columns = self._parse_columns(columns_section)
            
            # インデックスを解析
            ddl_table.indexes = self._parse_indexes(content)
            
            # 外部キー制約を解析
            ddl_table.foreign_keys = self._parse_foreign_keys(content)
            
            # その他の制約を解析
            ddl_table.constraints = self._parse_constraints(content)
            
            return ddl_table
            
        except Exception as e:
            self.logger.error(f"DDLファイル詳細解析エラー: {file_path} - {e}")
            return None
    
    def _extract_create_table_parts(self, content: str) -> Tuple[Optional[str], str, str]:
        """CREATE TABLE文の各部分を手動で抽出"""
        # CREATE TABLE文の開始を見つける
        create_table_match = re.search(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)\s*\(', content, re.IGNORECASE)
        if not create_table_match:
            return None, "", ""
        
        table_name = create_table_match.group(1)
        start_pos = create_table_match.end() - 1  # '('の位置
        
        # 括弧の対応を取りながらCREATE TABLE文の終了を見つける
        paren_count = 0
        pos = start_pos
        in_quotes = False
        quote_char = None
        
        while pos < len(content):
            char = content[pos]
            
            # 引用符の処理
            if char in ["'", '"'] and (pos == 0 or content[pos-1] != '\\'):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
            
            if not in_quotes:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        # CREATE TABLE文の終了
                        columns_section = content[start_pos + 1:pos]
                        
                        # テーブルオプション部分を抽出（;まで）
                        options_start = pos + 1
                        semicolon_pos = content.find(';', options_start)
                        if semicolon_pos != -1:
                            table_options = content[options_start:semicolon_pos].strip()
                        else:
                            table_options = content[options_start:].strip()
                        
                        return table_name, columns_section, table_options
            
            pos += 1
        
        return None, "", ""
    
    def _parse_table_options(self, options_text: str, ddl_table: DDLTable) -> None:
        """テーブルオプションの解析"""
        if not options_text:
            return
        
        # ENGINE
        engine_match = re.search(r'ENGINE\s*=\s*(\w+)', options_text, re.IGNORECASE)
        if engine_match:
            ddl_table.engine = engine_match.group(1)
        
        # CHARSET
        charset_match = re.search(r'(?:DEFAULT\s+)?CHARSET\s*=\s*(\w+)', options_text, re.IGNORECASE)
        if charset_match:
            ddl_table.charset = charset_match.group(1)
        
        # COLLATE
        collate_match = re.search(r'COLLATE\s*=\s*(\w+)', options_text, re.IGNORECASE)
        if collate_match:
            ddl_table.collation = collate_match.group(1)
    
    def _parse_columns(self, columns_section: str) -> List[ColumnDefinition]:
        """カラム定義の解析"""
        columns = []
        
        # カラム定義を分割（制約定義は除外）
        column_lines = []
        current_line = ""
        paren_count = 0
        in_quotes = False
        quote_char = None
        
        for i, char in enumerate(columns_section):
            # 引用符の処理
            if char in ["'", '"'] and (i == 0 or columns_section[i-1] != '\\'):
                if not in_quotes:
                    in_quotes = True
                    quote_char = char
                elif char == quote_char:
                    in_quotes = False
                    quote_char = None
            
            current_line += char
            
            if not in_quotes:
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == ',' and paren_count == 0:
                    line = current_line.strip()[:-1]  # 末尾のカンマを除去
                    if line:
                        column_lines.append(line)
                    current_line = ""
        
        if current_line.strip():
            column_lines.append(current_line.strip())
        
        for line in column_lines:
            line = line.strip()
            if not line:
                continue
            
            # 制約定義をスキップ
            if self._is_constraint_definition(line):
                continue
            
            column = self._parse_single_column(line)
            if column:
                columns.append(column)
        
        return columns
    
    def _is_constraint_definition(self, line: str) -> bool:
        """制約定義かどうかを判定"""
        constraint_keywords = [
            'PRIMARY KEY', 'FOREIGN KEY', 'UNIQUE', 'CHECK', 'INDEX', 'KEY'
        ]
        
        line_upper = line.upper().strip()
        for keyword in constraint_keywords:
            if line_upper.startswith(keyword):
                return True
        
        return False
    
    def _parse_single_column(self, column_def: str) -> Optional[ColumnDefinition]:
        """単一カラム定義の解析"""
        try:
            # カラム名を抽出（最初の単語）
            parts = column_def.strip().split()
            if len(parts) < 2:
                return None
            
            column_name = parts[0].strip('`"\'')
            remaining = ' '.join(parts[1:])
            
            # ColumnDefinitionオブジェクトを作成
            column = ColumnDefinition(name=column_name)
            
            # データ型を解析
            data_type_info = self._extract_data_type(remaining)
            if data_type_info:
                column.data_type = data_type_info['type']
                column.length = data_type_info.get('length')
                if 'enum_values' in data_type_info:
                    column.enum_values = data_type_info['enum_values']
            
            # 制約を解析
            self._parse_column_constraints(remaining, column)
            
            return column
            
        except Exception as e:
            self.logger.error(f"カラム定義解析エラー: {column_def} - {e}")
            return None
    
    def _extract_data_type(self, type_section: str) -> Optional[Dict[str, Any]]:
        """データ型情報の抽出"""
        type_section_upper = type_section.upper()
        
        for type_name, pattern in self.data_type_patterns.items():
            match = re.search(pattern, type_section_upper)
            if match:
                result = {'type': type_name.upper()}
                
                # 長さ情報を抽出
                if match.groups():
                    if type_name in ['varchar', 'char', 'int', 'bigint', 'tinyint', 'smallint', 'mediumint']:
                        if match.group(1):
                            result['length'] = int(match.group(1))
                    elif type_name in ['decimal', 'float', 'double']:
                        if len(match.groups()) >= 2 and match.group(1) and match.group(2):
                            result['precision'] = int(match.group(1))
                            result['scale'] = int(match.group(2))
                    elif type_name in ['datetime', 'timestamp', 'time']:
                        if match.group(1):
                            result['precision'] = int(match.group(1))
                
                # ENUM値を抽出
                if type_name == 'enum':
                    enum_values_str = match.group(1)
                    enum_values = []
                    for value in re.findall(r"'([^']*)'", enum_values_str):
                        enum_values.append(value)
                    result['enum_values'] = enum_values
                
                return result
        
        # パターンにマッチしない場合は、最初の単語をデータ型として扱う
        first_word = type_section.split()[0].upper()
        return {'type': first_word}
    
    def _parse_column_constraints(self, constraint_section: str, column: ColumnDefinition) -> None:
        """カラム制約の解析"""
        constraint_section_upper = constraint_section.upper()
        
        # NOT NULL / NULL
        if re.search(self.constraint_patterns['not_null'], constraint_section_upper):
            column.nullable = False
        elif re.search(self.constraint_patterns['null'], constraint_section_upper):
            column.nullable = True
        
        # DEFAULT値
        default_match = re.search(self.constraint_patterns['default'], constraint_section_upper)
        if default_match:
            default_value = default_match.group(1).strip()
            # 引用符を除去
            if default_value.startswith("'") and default_value.endswith("'"):
                default_value = default_value[1:-1]
            elif default_value.startswith('"') and default_value.endswith('"'):
                default_value = default_value[1:-1]
            column.default_value = default_value
        
        # AUTO_INCREMENT
        if re.search(self.constraint_patterns['auto_increment'], constraint_section_upper):
            column.validation = "AUTO_INCREMENT"
        
        # UNIQUE
        if re.search(self.constraint_patterns['unique'], constraint_section_upper):
            column.unique = True
        
        # PRIMARY KEY
        if re.search(self.constraint_patterns['primary_key'], constraint_section_upper):
            column.primary_key = True
            column.nullable = False  # PRIMARY KEYは自動的にNOT NULL
        
        # COMMENT
        comment_match = re.search(self.constraint_patterns['comment'], constraint_section)
        if comment_match:
            column.comment = comment_match.group(1)
    
    def _parse_indexes(self, ddl_content: str) -> List[IndexDefinition]:
        """インデックス定義の解析"""
        indexes = []
        
        # CREATE INDEX文を検索
        index_patterns = [
            r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+\w+\s*\(\s*([^)]+)\s*\)',
            r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+\w+\s*\(\s*([^)]+)\s*\)\s*(?:COMMENT\s+[\'"]([^\'"]*)[\'"])?'
        ]
        
        for pattern in index_patterns:
            for match in re.finditer(pattern, ddl_content, re.IGNORECASE):
                index_name = match.group(1)
                columns_str = match.group(2)
                description = match.group(3) if len(match.groups()) >= 3 and match.group(3) else ""
                
                # カラム名を抽出
                columns = [col.strip().strip('`"\'') for col in columns_str.split(',')]
                
                # UNIQUE判定
                unique = 'UNIQUE' in match.group(0).upper()
                
                indexes.append(IndexDefinition(
                    name=index_name,
                    columns=columns,
                    unique=unique,
                    description=description
                ))
        
        return indexes
    
    def _parse_foreign_keys(self, ddl_content: str) -> List[ForeignKeyDefinition]:
        """外部キー制約の解析"""
        foreign_keys = []
        
        # ALTER TABLE ... ADD CONSTRAINT ... FOREIGN KEY文を検索
        fk_pattern = (
            r'ALTER\s+TABLE\s+\w+\s+ADD\s+CONSTRAINT\s+(\w+)\s+'
            r'FOREIGN\s+KEY\s*\(\s*(\w+)\s*\)\s+'
            r'REFERENCES\s+(\w+)\s*\(\s*(\w+)\s*\)'
            r'(?:\s+ON\s+UPDATE\s+(\w+))?'
            r'(?:\s+ON\s+DELETE\s+(\w+))?'
        )
        
        for match in re.finditer(fk_pattern, ddl_content, re.IGNORECASE):
            fk_name = match.group(1)
            column = match.group(2)
            ref_table = match.group(3)
            ref_column = match.group(4)
            on_update = match.group(5) or 'CASCADE'
            on_delete = match.group(6) or 'RESTRICT'
            
            foreign_keys.append(ForeignKeyDefinition(
                name=fk_name,
                column=column,
                reference_table=ref_table,
                reference_column=ref_column,
                on_update=on_update,
                on_delete=on_delete
            ))
        
        return foreign_keys
    
    def _parse_constraints(self, ddl_content: str) -> List[ConstraintDefinition]:
        """その他の制約の解析"""
        constraints = []
        
        # CHECK制約を検索
        check_pattern = r'ALTER\s+TABLE\s+\w+\s+ADD\s+CONSTRAINT\s+(\w+)\s+CHECK\s*\(\s*([^)]+)\s*\)'
        
        for match in re.finditer(check_pattern, ddl_content, re.IGNORECASE):
            constraint_name = match.group(1)
            condition = match.group(2)
            
            constraints.append(ConstraintDefinition(
                name=constraint_name,
                type='CHECK',
                condition=condition
            ))
        
        return constraints
