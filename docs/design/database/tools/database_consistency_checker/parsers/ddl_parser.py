"""
データベース整合性チェックツール - DDL解析
"""
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from ..core.models import DDLTable, ColumnDefinition, IndexDefinition, ForeignKeyDefinition, ConstraintDefinition
from ..core.logger import ConsistencyLogger


class DDLParser:
    """DDLファイルの解析"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        """
        パーサー初期化
        
        Args:
            logger: ログ機能
        """
        self.logger = logger or ConsistencyLogger()
    
    def parse_file(self, file_path: Path) -> Optional[DDLTable]:
        """
        DDLファイルを解析
        
        Args:
            file_path: ファイルパス
            
        Returns:
            DDLテーブル定義
        """
        if not file_path.exists():
            self.logger.error(f"DDLファイルが見つかりません: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_ddl_content(content, file_path.stem)
            
        except Exception as e:
            self.logger.error(f"DDLファイルの読み込みエラー [{file_path}]: {e}")
            return None
    
    def _parse_ddl_content(self, content: str, table_name: str) -> Optional[DDLTable]:
        """
        DDL内容を解析
        
        Args:
            content: DDL内容
            table_name: テーブル名
            
        Returns:
            DDLテーブル定義
        """
        # CREATE TABLE文を抽出
        create_table_match = re.search(
            r'CREATE\s+TABLE\s+(\w+)\s*\((.*?)\)\s*ENGINE\s*=\s*(\w+).*?CHARSET\s*=\s*(\w+).*?COLLATE\s*=\s*(\w+)',
            content,
            re.DOTALL | re.IGNORECASE
        )
        
        if not create_table_match:
            self.logger.warning(f"CREATE TABLE文が見つかりません: {table_name}")
            return None
        
        actual_table_name = create_table_match.group(1)
        table_definition = create_table_match.group(2)
        engine = create_table_match.group(3)
        charset = create_table_match.group(4)
        collation = create_table_match.group(5)
        
        # カラム定義を解析
        columns = self._parse_columns(table_definition)
        
        # インデックス定義を解析
        indexes = self._parse_indexes(content)
        
        # 外部キー制約を解析
        foreign_keys = self._parse_foreign_keys(content)
        
        # その他の制約を解析
        constraints = self._parse_constraints(content)
        
        return DDLTable(
            table_name=actual_table_name,
            columns=columns,
            indexes=indexes,
            foreign_keys=foreign_keys,
            constraints=constraints,
            engine=engine,
            charset=charset,
            collation=collation
        )
    
    def _parse_columns(self, table_definition: str) -> List[ColumnDefinition]:
        """
        カラム定義を解析
        
        Args:
            table_definition: テーブル定義部分
            
        Returns:
            カラム定義のリスト
        """
        columns = []
        
        # カラム定義行を抽出（行の先頭が文字で始まる）
        lines = [line.strip() for line in table_definition.split('\n')]
        
        for line in lines:
            line = line.strip().rstrip(',')
            if not line or line.startswith('PRIMARY KEY') or line.startswith('KEY') or line.startswith('CONSTRAINT'):
                continue
            
            column = self._parse_column_line(line)
            if column:
                columns.append(column)
        
        return columns
    
    def _parse_column_line(self, line: str) -> Optional[ColumnDefinition]:
        """
        カラム定義行を解析
        
        Args:
            line: カラム定義行
            
        Returns:
            カラム定義
        """
        # カラム名とデータ型を抽出
        match = re.match(r'(\w+)\s+([A-Z]+(?:\([^)]+\))?)', line, re.IGNORECASE)
        if not match:
            return None
        
        name = match.group(1)
        data_type = match.group(2)
        
        # 属性を解析
        nullable = 'NOT NULL' not in line.upper()
        unique = 'UNIQUE' in line.upper()
        primary_key = 'PRIMARY KEY' in line.upper()
        
        # デフォルト値を抽出
        default_match = re.search(r'DEFAULT\s+([^,\s]+)', line, re.IGNORECASE)
        default_value = default_match.group(1) if default_match else None
        
        # コメントを抽出
        comment_match = re.search(r'COMMENT\s+[\'"]([^\'"]*)[\'"]', line, re.IGNORECASE)
        comment = comment_match.group(1) if comment_match else ""
        
        # データ型から長さを抽出
        length = None
        type_match = re.match(r'([A-Z]+)\((\d+)\)', data_type, re.IGNORECASE)
        if type_match:
            data_type = type_match.group(1)
            length = int(type_match.group(2))
        
        # ENUM値を抽出
        enum_values = []
        if data_type.upper() == 'ENUM':
            enum_match = re.search(r'ENUM\s*\(([^)]+)\)', line, re.IGNORECASE)
            if enum_match:
                enum_str = enum_match.group(1)
                enum_values = [val.strip().strip('\'"') for val in enum_str.split(',')]
        
        return ColumnDefinition(
            name=name,
            data_type=data_type,
            length=length,
            nullable=nullable,
            unique=unique,
            primary_key=primary_key,
            default_value=default_value,
            comment=comment,
            enum_values=enum_values
        )
    
    def _parse_indexes(self, content: str) -> List[IndexDefinition]:
        """
        インデックス定義を解析
        
        Args:
            content: DDL内容
            
        Returns:
            インデックス定義のリスト
        """
        indexes = []
        
        # CREATE INDEX文を抽出
        index_patterns = [
            r'CREATE\s+(UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+\w+\s*\(([^)]+)\)',
            r'CREATE\s+(UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+\w+\s*\(([^)]+)\)\s*;'
        ]
        
        for pattern in index_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                unique = bool(match.group(1))
                name = match.group(2)
                columns_str = match.group(3)
                columns = [col.strip() for col in columns_str.split(',')]
                
                indexes.append(IndexDefinition(
                    name=name,
                    columns=columns,
                    unique=unique
                ))
        
        return indexes
    
    def _parse_foreign_keys(self, content: str) -> List[ForeignKeyDefinition]:
        """
        外部キー制約を解析
        
        Args:
            content: DDL内容
            
        Returns:
            外部キー定義のリスト
        """
        foreign_keys = []
        
        # ALTER TABLE ADD CONSTRAINT文を抽出
        fk_pattern = r'ALTER\s+TABLE\s+\w+\s+ADD\s+CONSTRAINT\s+(\w+)\s+FOREIGN\s+KEY\s*\((\w+)\)\s+REFERENCES\s+(\w+)\s*\((\w+)\)(?:\s+ON\s+UPDATE\s+(\w+))?(?:\s+ON\s+DELETE\s+(\w+))?'
        
        matches = re.finditer(fk_pattern, content, re.IGNORECASE)
        for match in matches:
            name = match.group(1)
            column = match.group(2)
            reference_table = match.group(3)
            reference_column = match.group(4)
            on_update = match.group(5) or "CASCADE"
            on_delete = match.group(6) or "RESTRICT"
            
            foreign_keys.append(ForeignKeyDefinition(
                name=name,
                column=column,
                reference_table=reference_table,
                reference_column=reference_column,
                on_update=on_update,
                on_delete=on_delete
            ))
        
        return foreign_keys
    
    def _parse_constraints(self, content: str) -> List[ConstraintDefinition]:
        """
        制約定義を解析
        
        Args:
            content: DDL内容
            
        Returns:
            制約定義のリスト
        """
        constraints = []
        
        # ALTER TABLE ADD CONSTRAINT文を抽出（UNIQUE, CHECK制約）
        constraint_patterns = [
            (r'ALTER\s+TABLE\s+\w+\s+ADD\s+CONSTRAINT\s+(\w+)\s+UNIQUE\s*\(([^)]+)\)', 'UNIQUE'),
            (r'ALTER\s+TABLE\s+\w+\s+ADD\s+CONSTRAINT\s+(\w+)\s+CHECK\s*\(([^)]+)\)', 'CHECK')
        ]
        
        for pattern, constraint_type in constraint_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                name = match.group(1)
                definition = match.group(2)
                
                if constraint_type == 'UNIQUE':
                    columns = [col.strip() for col in definition.split(',')]
                    constraints.append(ConstraintDefinition(
                        name=name,
                        type=constraint_type,
                        columns=columns
                    ))
                elif constraint_type == 'CHECK':
                    constraints.append(ConstraintDefinition(
                        name=name,
                        type=constraint_type,
                        condition=definition
                    ))
        
        return constraints
    
    def get_table_name_from_file(self, file_path: Path) -> Optional[str]:
        """
        ファイルからテーブル名を抽出
        
        Args:
            file_path: ファイルパス
            
        Returns:
            テーブル名
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # CREATE TABLE文からテーブル名を抽出
            match = re.search(r'CREATE\s+TABLE\s+(\w+)', content, re.IGNORECASE)
            if match:
                return match.group(1)
            
            # ファイル名からテーブル名を推測
            return file_path.stem
            
        except Exception as e:
            self.logger.warning(f"テーブル名の抽出エラー [{file_path}]: {e}")
            return file_path.stem
    
    def validate_ddl_syntax(self, content: str) -> List[str]:
        """
        DDL構文の妥当性チェック
        
        Args:
            content: DDL内容
            
        Returns:
            エラーメッセージのリスト
        """
        errors = []
        
        # CREATE TABLE文の存在確認
        if not re.search(r'CREATE\s+TABLE', content, re.IGNORECASE):
            errors.append("CREATE TABLE文が見つかりません")
        
        # 基本的な構文チェック
        if content.count('(') != content.count(')'):
            errors.append("括弧の数が一致しません")
        
        # セミコロンの確認
        statements = content.split(';')
        for i, statement in enumerate(statements[:-1]):  # 最後の空文は除外
            statement = statement.strip()
            if statement and not statement.endswith(';') and i < len(statements) - 2:
                errors.append(f"文 {i+1} にセミコロンがありません")
        
        return errors
