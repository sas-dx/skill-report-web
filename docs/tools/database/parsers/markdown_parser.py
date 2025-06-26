"""
Markdown統一パーサー

Markdownファイルの解析と検証を行う
"""

import re
from typing import Dict, Any, List, Optional
from pathlib import Path

from .base_parser import BaseParser
from ..core import ValidationResult, ParseError


class MarkdownParser(BaseParser):
    """Markdown専用パーサー"""
    
    def __init__(self):
        super().__init__("markdown")
        self.header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        self.table_pattern = re.compile(r'^\|(.+)\|$', re.MULTILINE)
        self.code_block_pattern = re.compile(r'```(\w+)?\n(.*?)\n```', re.DOTALL)
    
    def get_supported_extensions(self) -> List[str]:
        """サポートする拡張子"""
        return ['.md', '.markdown']
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        Markdownファイルを解析
        
        Args:
            file_path: Markdownファイルパス
            
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
                raise ParseError(f"Markdownファイルが空です: {file_path}", file_path)
            
            # 構造を解析
            structure = self._parse_structure(content)
            
            result = {
                'file_path': file_path,
                'content': content,
                'structure': structure,
                'headers': structure.get('headers', []),
                'tables': structure.get('tables', []),
                'code_blocks': structure.get('code_blocks', [])
            }
            
            self.logger.debug(f"Markdown解析完了: {file_path}")
            return result
            
        except Exception as e:
            if isinstance(e, ParseError):
                raise
            raise ParseError(f"Markdown解析エラー: {str(e)}", file_path)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        Markdownデータの妥当性を検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            検証結果
        """
        result = ValidationResult(is_valid=True)
        
        # 基本構造の検証
        if 'content' not in data:
            result.add_error("コンテンツが存在しません")
            return result
        
        content = data['content']
        if not content.strip():
            result.add_error("コンテンツが空です")
            return result
        
        # ヘッダー構造の検証
        self._validate_headers(data, result)
        
        # テーブル定義書の場合の特別な検証
        if self._is_table_definition(data):
            self._validate_table_definition(data, result)
        
        return result
    
    def _parse_structure(self, content: str) -> Dict[str, Any]:
        """Markdownの構造を解析"""
        structure = {
            'headers': [],
            'tables': [],
            'code_blocks': []
        }
        
        # ヘッダーを抽出
        for match in self.header_pattern.finditer(content):
            level = len(match.group(1))
            title = match.group(2).strip()
            structure['headers'].append({
                'level': level,
                'title': title,
                'position': match.start()
            })
        
        # テーブルを抽出
        table_lines = []
        in_table = False
        
        for line in content.split('\n'):
            if self.table_pattern.match(line):
                if not in_table:
                    in_table = True
                    table_lines = []
                table_lines.append(line)
            else:
                if in_table and table_lines:
                    structure['tables'].append(self._parse_table(table_lines))
                    table_lines = []
                in_table = False
        
        # 最後のテーブルを処理
        if in_table and table_lines:
            structure['tables'].append(self._parse_table(table_lines))
        
        # コードブロックを抽出
        for match in self.code_block_pattern.finditer(content):
            language = match.group(1) or 'text'
            code = match.group(2)
            structure['code_blocks'].append({
                'language': language,
                'code': code,
                'position': match.start()
            })
        
        return structure
    
    def _parse_table(self, table_lines: List[str]) -> Dict[str, Any]:
        """テーブルを解析"""
        if len(table_lines) < 2:
            return {'headers': [], 'rows': []}
        
        # ヘッダー行を解析
        header_line = table_lines[0]
        headers = [cell.strip() for cell in header_line.split('|')[1:-1]]
        
        # データ行を解析（区切り行をスキップ）
        rows = []
        for line in table_lines[2:]:  # 最初の2行（ヘッダーと区切り）をスキップ
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
        
        return {
            'headers': headers,
            'rows': rows,
            'raw_lines': table_lines
        }
    
    def _is_table_definition(self, data: Dict[str, Any]) -> bool:
        """テーブル定義書かどうかを判定"""
        content = data.get('content', '')
        headers = data.get('headers', [])
        
        # ファイル名やヘッダーからテーブル定義書かどうかを判定
        file_path = data.get('file_path', '')
        if 'テーブル定義書' in file_path:
            return True
        
        for header in headers:
            if 'テーブル定義' in header.get('title', '') or 'カラム定義' in header.get('title', ''):
                return True
        
        return False
    
    def _validate_headers(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """ヘッダー構造の検証"""
        headers = data.get('headers', [])
        
        if not headers:
            result.add_warning("ヘッダーが見つかりません")
            return
        
        # H1ヘッダーの存在チェック
        h1_headers = [h for h in headers if h['level'] == 1]
        if not h1_headers:
            result.add_warning("H1ヘッダーが見つかりません")
        elif len(h1_headers) > 1:
            result.add_warning("H1ヘッダーが複数あります")
        
        # ヘッダーレベルの連続性チェック
        prev_level = 0
        for header in headers:
            level = header['level']
            if level > prev_level + 1:
                result.add_warning(f"ヘッダーレベルが飛んでいます: H{prev_level} -> H{level}")
            prev_level = level
    
    def _validate_table_definition(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """テーブル定義書の特別な検証"""
        content = data.get('content', '')
        tables = data.get('tables', [])
        
        # 必須セクションの存在チェック
        required_sections = ['概要', 'カラム定義', '制約', 'インデックス']
        for section in required_sections:
            if section not in content:
                result.add_warning(f"推奨セクション '{section}' が見つかりません")
        
        # カラム定義テーブルの検証
        column_tables = []
        for table in tables:
            headers = table.get('headers', [])
            if any('カラム名' in h or 'データ型' in h for h in headers):
                column_tables.append(table)
        
        if not column_tables:
            result.add_warning("カラム定義テーブルが見つかりません")
        else:
            for table in column_tables:
                self._validate_column_table(table, result)
    
    def _validate_column_table(self, table: Dict[str, Any], result: ValidationResult) -> None:
        """カラム定義テーブルの検証"""
        headers = table.get('headers', [])
        rows = table.get('rows', [])
        
        # 必須カラムの存在チェック
        required_columns = ['カラム名', 'データ型', 'NULL許可', '説明']
        for col in required_columns:
            if not any(col in h for h in headers):
                result.add_warning(f"推奨カラム '{col}' が見つかりません")
        
        # データ行の検証
        if not rows:
            result.add_warning("カラム定義テーブルにデータがありません")
        
        for i, row in enumerate(rows):
            # カラム名の検証
            column_name = row.get('カラム名', '')
            if not column_name:
                result.add_error(f"行{i+1}: カラム名が空です")
            
            # データ型の検証
            data_type = row.get('データ型', '')
            if not data_type:
                result.add_error(f"行{i+1}: データ型が空です")
    
    def extract_table_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """テーブル情報を抽出"""
        headers = data.get('headers', [])
        tables = data.get('tables', [])
        
        # テーブル名を抽出（H1ヘッダーから）
        table_name = ''
        if headers:
            h1_headers = [h for h in headers if h['level'] == 1]
            if h1_headers:
                table_name = h1_headers[0]['title']
        
        # カラム数を計算
        column_count = 0
        for table in tables:
            headers_list = table.get('headers', [])
            if any('カラム名' in h for h in headers_list):
                column_count = len(table.get('rows', []))
                break
        
        return {
            'table_name': table_name,
            'column_count': column_count,
            'table_count': len(tables),
            'header_count': len(headers)
        }
    
    def compare_with_yaml(self, md_data: Dict[str, Any], yaml_data: Dict[str, Any]) -> ValidationResult:
        """MarkdownとYAMLの整合性をチェック"""
        result = ValidationResult(is_valid=True)
        
        md_info = self.extract_table_info(md_data)
        
        # テーブル名の比較（部分一致）
        md_table_name = md_info.get('table_name', '')
        yaml_table_name = yaml_data.get('table_name', '')
        
        if yaml_table_name and yaml_table_name not in md_table_name:
            result.add_warning(f"テーブル名が一致しない可能性があります: MD={md_table_name}, YAML={yaml_table_name}")
        
        # カラム数の比較
        md_column_count = md_info.get('column_count', 0)
        yaml_column_count = len(yaml_data.get('columns', []))
        
        if md_column_count != yaml_column_count:
            result.add_warning(f"カラム数が異なります: MD={md_column_count}, YAML={yaml_column_count}")
        
        return result
    
    def get_toc(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """目次を生成"""
        headers = data.get('headers', [])
        toc = []
        
        for header in headers:
            toc.append({
                'level': header['level'],
                'title': header['title'],
                'anchor': self._generate_anchor(header['title'])
            })
        
        return toc
    
    def _generate_anchor(self, title: str) -> str:
        """アンカーリンクを生成"""
        # 簡単なアンカー生成（実際のMarkdownプロセッサに合わせて調整が必要）
        anchor = title.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor)
        anchor = re.sub(r'[-\s]+', '-', anchor)
        return anchor.strip('-')
