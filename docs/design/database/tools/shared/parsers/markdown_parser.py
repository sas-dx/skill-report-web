"""
Markdownテーブル定義書パーサー
Markdownファイルからテーブル定義を解析する機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import re
from typing import List, Dict, Any, Optional
from pathlib import Path

from .base_parser import BaseParser
from ..core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition
from ..core.exceptions import ParsingError


class MarkdownParser(BaseParser):
    """Markdownテーブル定義書パーサー"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self._setup_regex_patterns()
    
    def _setup_regex_patterns(self):
        """正規表現パターンの設定"""
        # テーブル名の抽出パターン
        self.table_name_patterns = [
            re.compile(r'#\s*テーブル定義書[_\s]*([A-Z_]+)[_\s]*(.+)', re.IGNORECASE),
            re.compile(r'#\s*([A-Z_]+)\s*テーブル', re.IGNORECASE),
            re.compile(r'テーブル名[:\s]*([A-Z_]+)', re.IGNORECASE),
            re.compile(r'物理名[:\s]*([A-Z_]+)', re.IGNORECASE)
        ]
        
        # 論理名の抽出パターン
        self.logical_name_patterns = [
            re.compile(r'論理名[:\s]*(.+)', re.IGNORECASE),
            re.compile(r'テーブル論理名[:\s]*(.+)', re.IGNORECASE)
        ]
        
        # カテゴリの抽出パターン
        self.category_patterns = [
            re.compile(r'カテゴリ[:\s]*(.+)', re.IGNORECASE),
            re.compile(r'分類[:\s]*(.+)', re.IGNORECASE)
        ]
        
        # 要求仕様IDの抽出パターン
        self.requirement_id_patterns = [
            re.compile(r'要求仕様ID[:\s]*([A-Z0-9\.\-]+)', re.IGNORECASE),
            re.compile(r'仕様ID[:\s]*([A-Z0-9\.\-]+)', re.IGNORECASE)
        ]
        
        # テーブルの抽出パターン
        self.table_pattern = re.compile(r'\|([^|]+)\|', re.MULTILINE)
        
        # セクションヘッダーのパターン
        self.section_patterns = {
            'columns': re.compile(r'#+\s*(?:カラム定義|列定義|フィールド定義)', re.IGNORECASE),
            'indexes': re.compile(r'#+\s*(?:インデックス定義|索引定義)', re.IGNORECASE),
            'foreign_keys': re.compile(r'#+\s*(?:外部キー|外部キー制約|参照制約)', re.IGNORECASE),
            'constraints': re.compile(r'#+\s*(?:制約|制約定義)', re.IGNORECASE)
        }
    
    def parse(self, source: Any) -> TableDefinition:
        """
        Markdownテーブル定義書を解析
        
        Args:
            source: Markdownファイルパス または Markdown文字列
            
        Returns:
            TableDefinition: テーブル定義オブジェクト
            
        Raises:
            ParsingError: 解析エラー
        """
        self._log_parsing_start(source)
        
        try:
            # Markdown内容の読み込み
            markdown_content = self._load_markdown_content(source)
            
            # 基本情報の抽出
            table_info = self._extract_table_info(markdown_content)
            
            # セクションの分割
            sections = self._split_into_sections(markdown_content)
            
            # TableDefinition オブジェクトの構築
            table_def = TableDefinition(
                name=table_info.get('name', ''),
                logical_name=table_info.get('logical_name', ''),
                category=table_info.get('category', ''),
                priority=table_info.get('priority', ''),
                requirement_id=table_info.get('requirement_id', ''),
                comment=table_info.get('comment', ''),
                columns=[],
                indexes=[],
                foreign_keys=[]
            )
            
            # カラム定義の解析
            if 'columns' in sections:
                table_def.columns = self._parse_columns_section(sections['columns'])
            
            # インデックス定義の解析
            if 'indexes' in sections:
                table_def.indexes = self._parse_indexes_section(sections['indexes'])
            
            # 外部キー定義の解析
            if 'foreign_keys' in sections:
                table_def.foreign_keys = self._parse_foreign_keys_section(sections['foreign_keys'])
            
            # 検証実行
            if self._validation_enabled:
                validation_results = self.validate(table_def)
                self._log_validation_results(validation_results)
            
            self._log_parsing_complete(source, 1)
            return table_def
            
        except Exception as e:
            raise self._handle_parsing_error(e, source, "Markdown解析エラー")
    
    def _load_markdown_content(self, source: Any) -> str:
        """Markdown内容の読み込み"""
        if isinstance(source, (str, Path)):
            # ファイルパスの場合
            file_path = Path(source)
            if not file_path.exists():
                raise ParsingError(f"Markdownファイルが見つかりません: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            # 文字列の場合
            return str(source)
    
    def _extract_table_info(self, content: str) -> Dict[str, str]:
        """テーブル基本情報の抽出"""
        info = {}
        
        # テーブル名の抽出
        for pattern in self.table_name_patterns:
            match = pattern.search(content)
            if match:
                info['name'] = match.group(1).strip()
                if len(match.groups()) > 1:
                    info['logical_name'] = match.group(2).strip()
                break
        
        # 論理名の抽出（テーブル名パターンで取得できなかった場合）
        if 'logical_name' not in info:
            for pattern in self.logical_name_patterns:
                match = pattern.search(content)
                if match:
                    info['logical_name'] = match.group(1).strip()
                    break
        
        # カテゴリの抽出
        for pattern in self.category_patterns:
            match = pattern.search(content)
            if match:
                info['category'] = match.group(1).strip()
                break
        
        # 要求仕様IDの抽出
        for pattern in self.requirement_id_patterns:
            match = pattern.search(content)
            if match:
                info['requirement_id'] = match.group(1).strip()
                break
        
        # コメント（概要）の抽出
        overview_match = re.search(r'#+\s*(?:概要|説明|目的)\s*\n\s*(.+)', content, re.IGNORECASE)
        if overview_match:
            info['comment'] = overview_match.group(1).strip()
        
        return info
    
    def _split_into_sections(self, content: str) -> Dict[str, str]:
        """セクションごとに内容を分割"""
        sections = {}
        lines = content.split('\n')
        current_section = None
        current_content = []
        
        for line in lines:
            # セクションヘッダーの検出
            section_found = False
            for section_name, pattern in self.section_patterns.items():
                if pattern.match(line):
                    # 前のセクションを保存
                    if current_section and current_content:
                        sections[current_section] = '\n'.join(current_content)
                    
                    current_section = section_name
                    current_content = []
                    section_found = True
                    break
            
            if not section_found and current_section:
                current_content.append(line)
        
        # 最後のセクションを保存
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def _parse_columns_section(self, section_content: str) -> List[ColumnDefinition]:
        """カラム定義セクションの解析"""
        columns = []
        
        # Markdownテーブルの抽出
        table_rows = self._extract_table_rows(section_content)
        if not table_rows:
            return columns
        
        # ヘッダー行の解析
        headers = table_rows[0] if table_rows else []
        header_map = self._create_column_header_map(headers)
        
        # データ行の解析
        for row in table_rows[2:]:  # ヘッダーと区切り行をスキップ
            if len(row) < len(headers):
                continue
            
            column = self._parse_column_row(row, header_map)
            if column:
                columns.append(column)
        
        return columns
    
    def _extract_table_rows(self, content: str) -> List[List[str]]:
        """Markdownテーブルの行を抽出"""
        rows = []
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('|') and line.endswith('|'):
                # パイプで区切られた行を分割
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                rows.append(cells)
        
        return rows
    
    def _create_column_header_map(self, headers: List[str]) -> Dict[str, int]:
        """カラムヘッダーのマッピングを作成"""
        header_map = {}
        
        # 標準的なヘッダー名のマッピング
        standard_headers = {
            'カラム名': 'name',
            '列名': 'name',
            'フィールド名': 'name',
            '物理名': 'name',
            'データ型': 'type',
            '型': 'type',
            'NULL': 'nullable',
            'NULL許可': 'nullable',
            'PK': 'primary_key',
            'プライマリキー': 'primary_key',
            '主キー': 'primary_key',
            'UK': 'unique',
            'ユニーク': 'unique',
            '一意': 'unique',
            'デフォルト': 'default',
            '初期値': 'default',
            'コメント': 'comment',
            '説明': 'comment',
            '備考': 'comment',
            '要求仕様ID': 'requirement_id',
            '仕様ID': 'requirement_id'
        }
        
        for i, header in enumerate(headers):
            header_clean = header.strip()
            for std_header, field_name in standard_headers.items():
                if std_header in header_clean:
                    header_map[field_name] = i
                    break
        
        return header_map
    
    def _parse_column_row(self, row: List[str], header_map: Dict[str, int]) -> Optional[ColumnDefinition]:
        """カラム行の解析"""
        if not row or not header_map:
            return None
        
        # 基本情報の取得
        name = self._get_cell_value(row, header_map, 'name', '')
        if not name:
            return None
        
        data_type = self._get_cell_value(row, header_map, 'type', '')
        nullable_text = self._get_cell_value(row, header_map, 'nullable', 'YES')
        pk_text = self._get_cell_value(row, header_map, 'primary_key', '')
        unique_text = self._get_cell_value(row, header_map, 'unique', '')
        default = self._get_cell_value(row, header_map, 'default', None)
        comment = self._get_cell_value(row, header_map, 'comment', '')
        requirement_id = self._get_cell_value(row, header_map, 'requirement_id', '')
        
        # ブール値の変換
        nullable = self._parse_boolean_value(nullable_text, default_true=True)
        primary_key = self._parse_boolean_value(pk_text, default_true=False)
        unique = self._parse_boolean_value(unique_text, default_true=False)
        
        return ColumnDefinition(
            name=name,
            type=data_type,
            nullable=nullable,
            primary_key=primary_key,
            unique=unique,
            default=default if default and default != '-' else None,
            comment=comment,
            requirement_id=requirement_id,
            auto_increment=False,  # Markdownからは判定困難
            check_constraint='',
            references=''
        )
    
    def _get_cell_value(self, row: List[str], header_map: Dict[str, int], field: str, default: Any) -> Any:
        """セルの値を取得"""
        if field in header_map and header_map[field] < len(row):
            value = row[header_map[field]].strip()
            return value if value and value != '-' else default
        return default
    
    def _parse_boolean_value(self, text: str, default_true: bool = False) -> bool:
        """ブール値の解析"""
        if not text or text == '-':
            return default_true
        
        text_upper = text.upper()
        
        # True値のパターン
        true_patterns = ['YES', 'Y', 'TRUE', 'T', '○', '◯', '✓', '1', 'PK', 'UK']
        if any(pattern in text_upper for pattern in true_patterns):
            return True
        
        # False値のパターン
        false_patterns = ['NO', 'N', 'FALSE', 'F', '×', '✗', '0']
        if any(pattern in text_upper for pattern in false_patterns):
            return False
        
        return default_true
    
    def _parse_indexes_section(self, section_content: str) -> List[IndexDefinition]:
        """インデックス定義セクションの解析"""
        indexes = []
        
        # Markdownテーブルの抽出
        table_rows = self._extract_table_rows(section_content)
        if not table_rows:
            return indexes
        
        # ヘッダー行の解析
        headers = table_rows[0] if table_rows else []
        header_map = self._create_index_header_map(headers)
        
        # データ行の解析
        for row in table_rows[2:]:  # ヘッダーと区切り行をスキップ
            if len(row) < len(headers):
                continue
            
            index = self._parse_index_row(row, header_map)
            if index:
                indexes.append(index)
        
        return indexes
    
    def _create_index_header_map(self, headers: List[str]) -> Dict[str, int]:
        """インデックスヘッダーのマッピングを作成"""
        header_map = {}
        
        standard_headers = {
            'インデックス名': 'name',
            '索引名': 'name',
            'カラム': 'columns',
            '列': 'columns',
            'ユニーク': 'unique',
            '一意': 'unique',
            'コメント': 'comment',
            '説明': 'comment'
        }
        
        for i, header in enumerate(headers):
            header_clean = header.strip()
            for std_header, field_name in standard_headers.items():
                if std_header in header_clean:
                    header_map[field_name] = i
                    break
        
        return header_map
    
    def _parse_index_row(self, row: List[str], header_map: Dict[str, int]) -> Optional[IndexDefinition]:
        """インデックス行の解析"""
        if not row or not header_map:
            return None
        
        name = self._get_cell_value(row, header_map, 'name', '')
        if not name:
            return None
        
        columns_text = self._get_cell_value(row, header_map, 'columns', '')
        unique_text = self._get_cell_value(row, header_map, 'unique', '')
        comment = self._get_cell_value(row, header_map, 'comment', '')
        
        # カラムリストの解析
        columns = [col.strip() for col in columns_text.split(',') if col.strip()]
        unique = self._parse_boolean_value(unique_text, default_true=False)
        
        return IndexDefinition(
            name=name,
            columns=columns,
            unique=unique,
            comment=comment,
            type='btree'
        )
    
    def _parse_foreign_keys_section(self, section_content: str) -> List[ForeignKeyDefinition]:
        """外部キー定義セクションの解析"""
        foreign_keys = []
        
        # Markdownテーブルの抽出
        table_rows = self._extract_table_rows(section_content)
        if not table_rows:
            return foreign_keys
        
        # ヘッダー行の解析
        headers = table_rows[0] if table_rows else []
        header_map = self._create_foreign_key_header_map(headers)
        
        # データ行の解析
        for row in table_rows[2:]:  # ヘッダーと区切り行をスキップ
            if len(row) < len(headers):
                continue
            
            foreign_key = self._parse_foreign_key_row(row, header_map)
            if foreign_key:
                foreign_keys.append(foreign_key)
        
        return foreign_keys
    
    def _create_foreign_key_header_map(self, headers: List[str]) -> Dict[str, int]:
        """外部キーヘッダーのマッピングを作成"""
        header_map = {}
        
        standard_headers = {
            '制約名': 'name',
            '外部キー名': 'name',
            'カラム': 'columns',
            '列': 'columns',
            '参照テーブル': 'references_table',
            '参照先テーブル': 'references_table',
            '参照カラム': 'references_columns',
            '参照先カラム': 'references_columns',
            'UPDATE': 'on_update',
            'DELETE': 'on_delete',
            'コメント': 'comment'
        }
        
        for i, header in enumerate(headers):
            header_clean = header.strip()
            for std_header, field_name in standard_headers.items():
                if std_header in header_clean:
                    header_map[field_name] = i
                    break
        
        return header_map
    
    def _parse_foreign_key_row(self, row: List[str], header_map: Dict[str, int]) -> Optional[ForeignKeyDefinition]:
        """外部キー行の解析"""
        if not row or not header_map:
            return None
        
        name = self._get_cell_value(row, header_map, 'name', '')
        columns_text = self._get_cell_value(row, header_map, 'columns', '')
        references_table = self._get_cell_value(row, header_map, 'references_table', '')
        references_columns_text = self._get_cell_value(row, header_map, 'references_columns', '')
        on_update = self._get_cell_value(row, header_map, 'on_update', 'RESTRICT')
        on_delete = self._get_cell_value(row, header_map, 'on_delete', 'RESTRICT')
        comment = self._get_cell_value(row, header_map, 'comment', '')
        
        if not columns_text or not references_table:
            return None
        
        # カラムリストの解析
        columns = [col.strip() for col in columns_text.split(',') if col.strip()]
        references_columns = [col.strip() for col in references_columns_text.split(',') if col.strip()]
        
        return ForeignKeyDefinition(
            name=name,
            columns=columns,
            references_table=references_table,
            references_columns=references_columns,
            on_update=on_update,
            on_delete=on_delete,
            comment=comment
        )


# パーサーファクトリーへの登録
from .base_parser import ParserFactory
ParserFactory.register_parser('.md', MarkdownParser)


# 便利関数
def parse_markdown_file(file_path: str, config=None, validate: bool = True) -> TableDefinition:
    """
    Markdownテーブル定義書を解析する便利関数
    
    Args:
        file_path: Markdownファイルパス
        config: 設定オブジェクト
        validate: 検証を実行するかどうか
        
    Returns:
        TableDefinition: テーブル定義オブジェクト
        
    Raises:
        ParsingError: 解析エラー
    """
    parser = MarkdownParser(config)
    parser.set_validation_enabled(validate)
    return parser.parse(file_path)
