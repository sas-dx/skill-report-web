"""
カラム定義解析パーサー
DDLファイルとYAMLファイルからカラム定義を抽出・解析する
"""
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass

from core.logger import ConsistencyLogger


@dataclass
class ColumnDefinition:
    """カラム定義データクラス"""
    name: str
    logical_name: Optional[str] = None
    data_type: str = ""
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    nullable: bool = True
    unique: bool = False
    primary_key: bool = False
    default_value: Optional[str] = None
    comment: Optional[str] = None
    encrypted: bool = False
    enum_values: Optional[List[str]] = None
    validation: Optional[str] = None
    
    def __post_init__(self):
        """初期化後処理"""
        if self.enum_values is None:
            self.enum_values = []
    
    def get_full_type(self) -> str:
        """完全なデータ型文字列を取得"""
        if self.data_type.upper() == "ENUM":
            if self.enum_values:
                enum_str = ', '.join([f"'{v}'" for v in self.enum_values])
                return f"ENUM({enum_str})"
            return "ENUM"
        elif self.length is not None:
            if self.precision is not None and self.scale is not None:
                return f"{self.data_type}({self.precision},{self.scale})"
            else:
                return f"{self.data_type}({self.length})"
        return self.data_type
    
    def is_compatible_with(self, other: 'ColumnDefinition') -> bool:
        """他のカラム定義との互換性をチェック"""
        # 基本的なデータ型の互換性チェック
        if self.data_type.upper() != other.data_type.upper():
            return False
        
        # 長さの互換性チェック
        if self.length != other.length:
            return False
        
        # NULL制約の互換性チェック
        if self.nullable != other.nullable:
            return False
        
        return True


@dataclass
class TableSchema:
    """テーブルスキーマ定義"""
    table_name: str
    logical_name: Optional[str] = None
    columns: Dict[str, ColumnDefinition] = None
    primary_keys: List[str] = None
    unique_constraints: List[List[str]] = None
    indexes: List[Dict[str, Any]] = None
    foreign_keys: List[Dict[str, Any]] = None
    check_constraints: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        """初期化後処理"""
        if self.columns is None:
            self.columns = {}
        if self.primary_keys is None:
            self.primary_keys = []
        if self.unique_constraints is None:
            self.unique_constraints = []
        if self.indexes is None:
            self.indexes = []
        if self.foreign_keys is None:
            self.foreign_keys = []
        if self.check_constraints is None:
            self.check_constraints = []


class ColumnParser:
    """カラム定義解析パーサー"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        self.logger = logger or ConsistencyLogger()
    
    def parse_ddl_file(self, ddl_path: Path) -> Optional[TableSchema]:
        """DDLファイルからテーブルスキーマを解析"""
        try:
            with open(ddl_path, 'r', encoding='utf-8') as f:
                ddl_content = f.read()
            
            return self._parse_ddl_content(ddl_content, ddl_path.stem)
        
        except Exception as e:
            self.logger.error(f"DDLファイル解析エラー: {ddl_path}: {e}")
            return None
    
    def _parse_ddl_content(self, ddl_content: str, table_name: str) -> TableSchema:
        """DDL内容からテーブルスキーマを解析"""
        schema = TableSchema(table_name=table_name)
        
        # CREATE TABLE文を抽出
        create_table_match = re.search(
            r'CREATE\s+TABLE\s+(\w+)\s*\((.*?)\)\s*(?:ENGINE|;)',
            ddl_content,
            re.IGNORECASE | re.DOTALL
        )
        
        if not create_table_match:
            self.logger.warning(f"CREATE TABLE文が見つかりません: {table_name}")
            return schema
        
        table_def = create_table_match.group(2)
        
        # カラム定義を解析
        self._parse_ddl_columns(table_def, schema)
        
        # インデックスを解析
        self._parse_ddl_indexes(ddl_content, schema)
        
        # 外部キー制約を解析
        self._parse_ddl_foreign_keys(ddl_content, schema)
        
        # その他の制約を解析
        self._parse_ddl_constraints(ddl_content, schema)
        
        return schema
    
    def _parse_ddl_columns(self, table_def: str, schema: TableSchema):
        """DDLのカラム定義を解析"""
        # カラム定義の正規表現パターン
        column_pattern = r'(\w+)\s+([A-Z]+(?:\([^)]+\))?)\s*([^,]*?)(?:COMMENT\s+[\'"]([^\'"]*)[\'"]\s*)?(?:,|$)'
        
        for match in re.finditer(column_pattern, table_def, re.IGNORECASE):
            column_name = match.group(1).strip()
            data_type_full = match.group(2).strip()
            modifiers = match.group(3).strip() if match.group(3) else ""
            comment = match.group(4).strip() if match.group(4) else None
            
            # データ型と長さを解析
            data_type, length, precision, scale = self._parse_data_type(data_type_full)
            
            # カラム修飾子を解析
            nullable = "NOT NULL" not in modifiers.upper()
            unique = "UNIQUE" in modifiers.upper()
            primary_key = "PRIMARY KEY" in modifiers.upper()
            
            # デフォルト値を抽出
            default_match = re.search(r'DEFAULT\s+([\'"]?[^,\s]+[\'"]?)', modifiers, re.IGNORECASE)
            default_value = default_match.group(1).strip('\'"') if default_match else None
            
            # ENUM値を抽出
            enum_values = []
            if data_type.upper() == "ENUM":
                enum_match = re.search(r'ENUM\s*\(([^)]+)\)', data_type_full, re.IGNORECASE)
                if enum_match:
                    enum_str = enum_match.group(1)
                    enum_values = [v.strip('\'"') for v in enum_str.split(',')]
            
            column = ColumnDefinition(
                name=column_name,
                data_type=data_type,
                length=length,
                precision=precision,
                scale=scale,
                nullable=nullable,
                unique=unique,
                primary_key=primary_key,
                default_value=default_value,
                comment=comment,
                enum_values=enum_values
            )
            
            schema.columns[column_name] = column
            
            if primary_key:
                schema.primary_keys.append(column_name)
    
    def _parse_data_type(self, data_type_full: str) -> tuple:
        """データ型文字列を解析"""
        # ENUM型の場合
        if data_type_full.upper().startswith('ENUM'):
            return 'ENUM', None, None, None
        
        # 長さ指定がある場合
        type_match = re.match(r'([A-Z]+)\s*\(([^)]+)\)', data_type_full, re.IGNORECASE)
        if type_match:
            data_type = type_match.group(1).upper()
            params = type_match.group(2).strip()
            
            # DECIMAL(10,2)のような場合
            if ',' in params:
                parts = params.split(',')
                precision = int(parts[0].strip())
                scale = int(parts[1].strip())
                return data_type, None, precision, scale
            else:
                # VARCHAR(100)のような場合
                length = int(params)
                return data_type, length, None, None
        
        # 長さ指定がない場合
        return data_type_full.upper(), None, None, None
    
    def _parse_ddl_indexes(self, ddl_content: str, schema: TableSchema):
        """DDLのインデックス定義を解析"""
        index_pattern = r'CREATE\s+(UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+\w+\s*\(([^)]+)\)'
        
        for match in re.finditer(index_pattern, ddl_content, re.IGNORECASE):
            unique = bool(match.group(1))
            index_name = match.group(2)
            columns_str = match.group(3)
            columns = [col.strip() for col in columns_str.split(',')]
            
            index_def = {
                'name': index_name,
                'columns': columns,
                'unique': unique
            }
            
            schema.indexes.append(index_def)
            
            # UNIQUE制約として記録
            if unique:
                schema.unique_constraints.append(columns)
    
    def _parse_ddl_foreign_keys(self, ddl_content: str, schema: TableSchema):
        """DDLの外部キー制約を解析"""
        fk_pattern = r'ADD\s+CONSTRAINT\s+(\w+)\s+FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+(\w+)\s*\(([^)]+)\)(?:\s+ON\s+UPDATE\s+(\w+))?(?:\s+ON\s+DELETE\s+(\w+))?'
        
        for match in re.finditer(fk_pattern, ddl_content, re.IGNORECASE):
            constraint_name = match.group(1)
            source_columns = [col.strip() for col in match.group(2).split(',')]
            target_table = match.group(3)
            target_columns = [col.strip() for col in match.group(4).split(',')]
            on_update = match.group(5) if match.group(5) else 'RESTRICT'
            on_delete = match.group(6) if match.group(6) else 'RESTRICT'
            
            fk_def = {
                'name': constraint_name,
                'columns': source_columns,
                'reference_table': target_table,
                'reference_columns': target_columns,
                'on_update': on_update,
                'on_delete': on_delete
            }
            
            schema.foreign_keys.append(fk_def)
    
    def _parse_ddl_constraints(self, ddl_content: str, schema: TableSchema):
        """DDLのその他の制約を解析"""
        # CHECK制約
        check_pattern = r'ADD\s+CONSTRAINT\s+(\w+)\s+CHECK\s*\(([^)]+)\)'
        
        for match in re.finditer(check_pattern, ddl_content, re.IGNORECASE):
            constraint_name = match.group(1)
            condition = match.group(2)
            
            check_def = {
                'name': constraint_name,
                'condition': condition
            }
            
            schema.check_constraints.append(check_def)
        
        # UNIQUE制約
        unique_pattern = r'ADD\s+CONSTRAINT\s+(\w+)\s+UNIQUE\s*\(([^)]*)\)'
        
        for match in re.finditer(unique_pattern, ddl_content, re.IGNORECASE):
            constraint_name = match.group(1)
            columns_str = match.group(2)
            
            if columns_str.strip():  # 空でない場合のみ
                columns = [col.strip() for col in columns_str.split(',')]
                schema.unique_constraints.append(columns)
    
    def parse_yaml_file(self, yaml_path: Path) -> Optional[TableSchema]:
        """YAMLファイルからテーブルスキーマを解析"""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            
            return self._parse_yaml_content(yaml_data, yaml_path.stem)
        
        except Exception as e:
            self.logger.error(f"YAMLファイル解析エラー: {yaml_path}: {e}")
            return None
    
    def _parse_yaml_content(self, yaml_data: dict, table_name: str) -> TableSchema:
        """YAML内容からテーブルスキーマを解析"""
        schema = TableSchema(
            table_name=yaml_data.get('table_name', table_name),
            logical_name=yaml_data.get('logical_name')
        )
        
        # 業務固有カラム定義を解析
        business_columns = yaml_data.get('business_columns', [])
        for col_data in business_columns:
            column = self._parse_yaml_column(col_data)
            schema.columns[column.name] = column
            
            if col_data.get('primary_key', False):
                schema.primary_keys.append(column.name)
        
        # インデックス定義を解析
        business_indexes = yaml_data.get('business_indexes', [])
        for idx_data in business_indexes:
            index_def = {
                'name': idx_data.get('name'),
                'columns': idx_data.get('columns', []),
                'unique': idx_data.get('unique', False),
                'description': idx_data.get('description')
            }
            schema.indexes.append(index_def)
            
            if idx_data.get('unique', False):
                schema.unique_constraints.append(idx_data.get('columns', []))
        
        # 外部キー定義を解析
        foreign_keys = yaml_data.get('foreign_keys', [])
        for fk_data in foreign_keys:
            fk_def = {
                'name': fk_data.get('name'),
                'columns': [fk_data.get('column')],
                'reference_table': fk_data.get('reference_table'),
                'reference_columns': [fk_data.get('reference_column')],
                'on_update': fk_data.get('on_update', 'RESTRICT'),
                'on_delete': fk_data.get('on_delete', 'RESTRICT'),
                'description': fk_data.get('description')
            }
            schema.foreign_keys.append(fk_def)
        
        # 制約定義を解析
        business_constraints = yaml_data.get('business_constraints', [])
        for constraint_data in business_constraints:
            constraint_type = constraint_data.get('type', '').upper()
            
            if constraint_type == 'CHECK':
                check_def = {
                    'name': constraint_data.get('name'),
                    'condition': constraint_data.get('condition'),
                    'description': constraint_data.get('description')
                }
                schema.check_constraints.append(check_def)
            elif constraint_type == 'UNIQUE':
                columns = constraint_data.get('columns', [])
                if columns:
                    schema.unique_constraints.append(columns)
        
        return schema
    
    def _parse_yaml_column(self, col_data: dict) -> ColumnDefinition:
        """YAMLのカラムデータからColumnDefinitionを作成"""
        data_type = col_data.get('type', '').upper()
        length = col_data.get('length')
        
        return ColumnDefinition(
            name=col_data.get('name', ''),
            logical_name=col_data.get('logical'),
            data_type=data_type,
            length=length,
            nullable=col_data.get('null', True),
            unique=col_data.get('unique', False),
            default_value=col_data.get('default'),
            comment=col_data.get('description'),
            encrypted=col_data.get('encrypted', False),
            enum_values=col_data.get('enum_values', []),
            validation=col_data.get('validation')
        )
