"""
DDLファイルパーサー
CREATE TABLE文からテーブル定義を解析する機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import re
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

from .base_parser import BaseParser
from ..core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition
from ..core.exceptions import ParsingError


class DDLParser(BaseParser):
    """DDLファイルパーサー"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self._setup_regex_patterns()
    
    def _setup_regex_patterns(self):
        """正規表現パターンの設定"""
        # CREATE TABLE文のパターン
        self.create_table_pattern = re.compile(
            r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([`"]?)(\w+)\1\s*\(',
            re.IGNORECASE | re.MULTILINE
        )
        
        # カラム定義のパターン
        self.column_pattern = re.compile(
            r'^\s*([`"]?)(\w+)\1\s+([^,\s]+(?:\s*\([^)]+\))?)\s*(.*?)(?:,\s*$|$)',
            re.MULTILINE
        )
        
        # 制約のパターン
        self.constraint_patterns = {
            'primary_key': re.compile(r'PRIMARY\s+KEY', re.IGNORECASE),
            'not_null': re.compile(r'NOT\s+NULL', re.IGNORECASE),
            'unique': re.compile(r'UNIQUE', re.IGNORECASE),
            'auto_increment': re.compile(r'AUTO_INCREMENT|SERIAL', re.IGNORECASE),
            'default': re.compile(r'DEFAULT\s+([^,\s]+)', re.IGNORECASE),
            'check': re.compile(r'CHECK\s*\(([^)]+)\)', re.IGNORECASE),
            'references': re.compile(r'REFERENCES\s+(\w+)\s*\(([^)]+)\)', re.IGNORECASE)
        }
        
        # インデックス作成のパターン
        self.index_pattern = re.compile(
            r'CREATE\s+(?:(UNIQUE)\s+)?INDEX\s+([`"]?)(\w+)\2\s+ON\s+([`"]?)(\w+)\4\s*\(([^)]+)\)',
            re.IGNORECASE | re.MULTILINE
        )
        
        # 外部キー制約のパターン
        self.foreign_key_pattern = re.compile(
            r'(?:CONSTRAINT\s+([`"]?)(\w+)\1\s+)?FOREIGN\s+KEY\s*\(([^)]+)\)\s+REFERENCES\s+([`"]?)(\w+)\4\s*\(([^)]+)\)(?:\s+ON\s+UPDATE\s+(\w+))?(?:\s+ON\s+DELETE\s+(\w+))?',
            re.IGNORECASE | re.MULTILINE
        )
        
        # コメントのパターン
        self.comment_pattern = re.compile(r'COMMENT\s+[\'"]([^\'"]*)[\'"]', re.IGNORECASE)
    
    def parse(self, source: Any) -> List[TableDefinition]:
        """
        DDLファイルを解析
        
        Args:
            source: DDLファイルパス または DDL文字列
            
        Returns:
            List[TableDefinition]: テーブル定義オブジェクトのリスト
            
        Raises:
            ParsingError: 解析エラー
        """
        self._log_parsing_start(source)
        
        try:
            # DDL文字列の読み込み
            ddl_content = self._load_ddl_content(source)
            
            # CREATE TABLE文の抽出
            table_definitions = []
            table_matches = self.create_table_pattern.finditer(ddl_content)
            
            for match in table_matches:
                table_name = match.group(2)
                table_start = match.end()
                
                # テーブル定義の終了位置を検索
                table_end = self._find_table_end(ddl_content, table_start)
                table_ddl = ddl_content[match.start():table_end]
                
                # テーブル定義の解析
                table_def = self._parse_table_definition(table_name, table_ddl)
                table_definitions.append(table_def)
            
            # インデックス定義の解析
            self._parse_indexes(ddl_content, table_definitions)
            
            # 検証実行
            if self._validation_enabled:
                for table_def in table_definitions:
                    validation_results = self.validate(table_def)
                    self._log_validation_results(validation_results)
            
            self._log_parsing_complete(source, len(table_definitions))
            return table_definitions
            
        except Exception as e:
            raise self._handle_parsing_error(e, source, "DDL解析エラー")
    
    def _load_ddl_content(self, source: Any) -> str:
        """DDL内容の読み込み"""
        if isinstance(source, (str, Path)):
            # ファイルパスの場合
            file_path = Path(source)
            if not file_path.exists():
                raise ParsingError(f"DDLファイルが見つかりません: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # 文字列の場合
            return str(source)
    
    def _find_table_end(self, ddl_content: str, start_pos: int) -> int:
        """テーブル定義の終了位置を検索"""
        paren_count = 0
        in_string = False
        string_char = None
        i = start_pos
        
        while i < len(ddl_content):
            char = ddl_content[i]
            
            if not in_string:
                if char in ('"', "'", '`'):
                    in_string = True
                    string_char = char
                elif char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        # 閉じ括弧の後、セミコロンまたは次のCREATE文まで検索
                        j = i + 1
                        # セミコロンを探す
                        while j < len(ddl_content):
                            if ddl_content[j] == ';':
                                return j + 1
                            elif ddl_content[j:j+6].upper() == 'CREATE':
                                # 次のCREATE文が見つかった場合
                                return j
                            elif not ddl_content[j].isspace():
                                # セミコロンもCREATE文もない場合は、空白以外の文字まで
                                break
                            j += 1
                        # セミコロンが見つからない場合は、ファイル末尾まで
                        return len(ddl_content)
            else:
                if char == string_char and (i == 0 or ddl_content[i-1] != '\\'):
                    in_string = False
                    string_char = None
            
            i += 1
        
        return len(ddl_content)
    
    def _parse_table_definition(self, table_name: str, table_ddl: str) -> TableDefinition:
        """テーブル定義の解析"""
        # 基本情報
        table_def = TableDefinition(
            name=table_name,  # nameパラメータを追加
            table_name=table_name,
            logical_name=table_name,  # DDLからは論理名を取得できないため物理名を使用
            category=self._infer_category_from_name(table_name),
            priority='',
            requirement_id='',
            comment=self._extract_table_comment(table_ddl),
            columns=[],
            indexes=[],
            foreign_keys=[]
        )
        
        # カラム定義の解析
        columns = self._parse_columns(table_ddl)
        table_def.columns = columns
        
        # 外部キー制約の解析
        foreign_keys = self._parse_foreign_keys(table_ddl)
        table_def.foreign_keys = foreign_keys
        
        return table_def
    
    def _infer_category_from_name(self, table_name: str) -> str:
        """テーブル名からカテゴリを推測"""
        if table_name.startswith('MST_'):
            return 'マスタ系'
        elif table_name.startswith('TRN_'):
            return 'トランザクション系'
        elif table_name.startswith('HIS_'):
            return '履歴系'
        elif table_name.startswith('SYS_'):
            return 'システム系'
        elif table_name.startswith('WRK_'):
            return 'ワーク系'
        elif table_name.startswith('IF_'):
            return 'インターフェイス系'
        else:
            return '未分類'
    
    def _extract_table_comment(self, table_ddl: str) -> str:
        """テーブルコメントの抽出"""
        comment_match = self.comment_pattern.search(table_ddl)
        return comment_match.group(1) if comment_match else ''
    
    def _parse_columns(self, table_ddl: str) -> List[ColumnDefinition]:
        """カラム定義の解析"""
        columns = []
        
        # テーブル定義部分の抽出（括弧内）
        paren_start = table_ddl.find('(')
        paren_end = table_ddl.rfind(')')
        if paren_start == -1 or paren_end == -1:
            return columns
        
        columns_section = table_ddl[paren_start + 1:paren_end]
        
        # デバッグ: 抽出されたカラムセクションを出力
        if self.logger:
            self.logger.debug(f"カラムセクション全体: '{columns_section}'")
        
        # カンマで分割（ただし括弧内のカンマは除外）
        column_defs = []
        current_def = ''
        paren_count = 0
        in_string = False
        string_char = None
        
        for char in columns_section:
            if not in_string:
                if char in ('"', "'", '`'):
                    in_string = True
                    string_char = char
                elif char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                elif char == ',' and paren_count == 0:
                    # カンマで分割
                    if current_def.strip():
                        column_defs.append(current_def.strip())
                    current_def = ''
                    continue
            else:
                if char == string_char:
                    in_string = False
                    string_char = None
            
            current_def += char
        
        # 最後のカラム定義を追加
        if current_def.strip():
            column_defs.append(current_def.strip())
        
        # デバッグ: 分割されたカラム定義を出力
        if self.logger:
            self.logger.debug(f"分割されたカラム定義数: {len(column_defs)}")
            for i, def_text in enumerate(column_defs):
                self.logger.debug(f"カラム定義 {i+1}: '{def_text}'")
        
        # 各カラム定義を解析
        for i, column_def in enumerate(column_defs):
            column_def = column_def.strip()
            if not column_def or column_def.startswith('--'):
                continue
            
            # 制約定義の場合はスキップ（カラム定義ではない行）
            upper_def = column_def.upper()
            if (upper_def.startswith('CONSTRAINT') or 
                upper_def.startswith('PRIMARY KEY') or 
                upper_def.startswith('FOREIGN KEY') or 
                upper_def.startswith('INDEX') or 
                upper_def.startswith('KEY ') or
                upper_def.startswith('UNIQUE KEY')):
                if self.logger:
                    self.logger.debug(f"制約定義をスキップ: '{column_def}'")
                continue
            
            # デバッグログ
            if self.logger:
                self.logger.debug(f"カラム定義解析開始 {i+1}: '{column_def}'")
            
            column = self._parse_single_column(column_def)
            if column:
                columns.append(column)
                if self.logger:
                    self.logger.debug(f"カラム解析成功: {column.name} ({column.type})")
            else:
                if self.logger:
                    self.logger.debug(f"カラム解析失敗: '{column_def}'")
        
        return columns
    
    def _parse_single_column(self, column_def: str) -> Optional[ColumnDefinition]:
        """単一カラム定義の解析"""
        # カンマを除去
        column_def = column_def.rstrip(',').strip()
        
        # 空の定義や制約定義をスキップ
        if not column_def:
            return None
        
        # カラム名とデータ型の抽出
        parts = column_def.split()
        if len(parts) < 2:
            return None
        
        column_name = parts[0].strip('`"')
        data_type = parts[1]
        
        # 制約の解析
        constraints_text = ' '.join(parts[2:]) if len(parts) > 2 else ''
        
        # ColumnDefinitionオブジェクトの作成
        column = ColumnDefinition(
            name=column_name,
            type=data_type,
            nullable=not self.constraint_patterns['not_null'].search(constraints_text),
            primary_key=bool(self.constraint_patterns['primary_key'].search(constraints_text)),
            unique=bool(self.constraint_patterns['unique'].search(constraints_text)),
            comment=self._extract_column_comment(constraints_text),
            requirement_id='',  # DDLからは取得できない
        )
        
        # デフォルト値の抽出
        default_match = self.constraint_patterns['default'].search(constraints_text)
        if default_match:
            default_value = default_match.group(1).strip("'\"")
            # CURRENT_TIMESTAMPなどの関数は文字列として保存
            column.default = default_value
        
        # CHECK制約の抽出
        check_match = self.constraint_patterns['check'].search(constraints_text)
        if check_match:
            column.check_constraint = check_match.group(1)
        
        # 参照制約の抽出
        references_match = self.constraint_patterns['references'].search(constraints_text)
        if references_match:
            column.references = f"{references_match.group(1)}({references_match.group(2)})"
        
        return column
    
    def _extract_column_comment(self, constraints_text: str) -> str:
        """カラムコメントの抽出"""
        comment_match = self.comment_pattern.search(constraints_text)
        return comment_match.group(1) if comment_match else ''
    
    def _parse_foreign_keys(self, table_ddl: str) -> List[ForeignKeyDefinition]:
        """外部キー制約の解析"""
        foreign_keys = []
        
        for match in self.foreign_key_pattern.finditer(table_ddl):
            constraint_name = match.group(2) if match.group(2) else ''
            columns = [col.strip().strip('`"') for col in match.group(3).split(',')]
            references_table = match.group(5)
            references_columns = [col.strip().strip('`"') for col in match.group(6).split(',')]
            on_update = match.group(7) if match.group(7) else 'RESTRICT'
            on_delete = match.group(8) if match.group(8) else 'RESTRICT'
            
            foreign_key = ForeignKeyDefinition(
                name=constraint_name,
                columns=columns,
                references_table=references_table,
                references_columns=references_columns,
                on_update=on_update,
                on_delete=on_delete,
                comment=''
            )
            
            foreign_keys.append(foreign_key)
        
        return foreign_keys
    
    def _parse_indexes(self, ddl_content: str, table_definitions: List[TableDefinition]):
        """インデックス定義の解析"""
        table_dict = {table.table_name: table for table in table_definitions}
        
        for match in self.index_pattern.finditer(ddl_content):
            unique = bool(match.group(1))
            index_name = match.group(3)
            table_name = match.group(5)
            columns_text = match.group(6)
            
            if table_name in table_dict:
                columns = [col.strip().strip('`"') for col in columns_text.split(',')]
                
                index = IndexDefinition(
                    name=index_name,
                    columns=columns,
                    unique=unique,
                    comment='',
                    type='btree'
                )
                
                table_dict[table_name].indexes.append(index)
    
    def validate(self, result: TableDefinition) -> List:
        """DDL固有の検証を追加"""
        # 基底クラスの検証を実行
        validation_results = super().validate(result)
        
        # DDL固有の検証を追加
        ddl_specific_results = self._validate_ddl_specific(result)
        validation_results.extend(ddl_specific_results)
        
        return validation_results
    
    def _validate_ddl_specific(self, table: TableDefinition) -> List:
        """DDL固有の検証"""
        from ..core.models import CheckResult
        
        results = []
        
        # データ型の検証
        valid_types = ['VARCHAR', 'CHAR', 'TEXT', 'INT', 'INTEGER', 'BIGINT', 'DECIMAL', 'NUMERIC', 
                      'FLOAT', 'DOUBLE', 'BOOLEAN', 'DATE', 'TIME', 'TIMESTAMP', 'DATETIME']
        
        for column in table.columns:
            base_type = column.type.split('(')[0].upper()
            if base_type not in valid_types:
                results.append(CheckResult(
                    check_type="ddl_validation",
                    table_name=table.table_name,
                    status="warning",
                    message=f"未知のデータ型が使用されています: {column.type}",
                    details={"table": table.table_name, "column": column.name, "type": column.type}
                ))
        
        # 外部キー制約の検証
        for fk in table.foreign_keys:
            if not fk.references_table:
                results.append(CheckResult(
                    check_type="ddl_validation",
                    table_name=table.table_name,
                    status="error",
                    message="外部キー制約の参照先テーブルが指定されていません",
                    details={"table": table.table_name, "foreign_key": fk.name}
                ))
        
        return results


# パーサーファクトリーへの登録
from .base_parser import ParserFactory
ParserFactory.register_parser('.sql', DDLParser)


# 便利関数
def parse_ddl_file(file_path: str, config=None, validate: bool = True) -> List[TableDefinition]:
    """
    DDLファイルを解析する便利関数
    
    Args:
        file_path: DDLファイルパス
        config: 設定オブジェクト
        validate: 検証を実行するかどうか
        
    Returns:
        List[TableDefinition]: テーブル定義オブジェクトのリスト
        
    Raises:
        ParsingError: 解析エラー
    """
    parser = DDLParser(config)
    parser.set_validation_enabled(validate)
    return parser.parse(file_path)


def parse_ddl_string(ddl_string: str, config=None, validate: bool = True) -> List[TableDefinition]:
    """
    DDL文字列を解析する便利関数
    
    Args:
        ddl_string: DDL文字列
        config: 設定オブジェクト
        validate: 検証を実行するかどうか
        
    Returns:
        List[TableDefinition]: テーブル定義オブジェクトのリスト
        
    Raises:
        ParsingError: 解析エラー
    """
    parser = DDLParser(config)
    parser.set_validation_enabled(validate)
    return parser.parse(ddl_string)
