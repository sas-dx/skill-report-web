"""
統一パーサーモジュール

各種ファイル形式のパーサーを提供
"""

from .base_parser import BaseParser
from .yaml_parser import YamlParser
from .ddl_parser import DdlParser
from .markdown_parser import MarkdownParser

__all__ = [
    'BaseParser',
    'YamlParser', 
    'DdlParser',
    'MarkdownParser'
]

# パーサーファクトリー
def create_parser(file_type: str) -> BaseParser:
    """
    ファイルタイプに応じたパーサーを作成
    
    Args:
        file_type: ファイルタイプ ('yaml', 'ddl', 'markdown')
        
    Returns:
        対応するパーサーインスタンス
        
    Raises:
        ValueError: サポートされていないファイルタイプ
    """
    parsers = {
        'yaml': YamlParser,
        'yml': YamlParser,
        'ddl': DdlParser,
        'sql': DdlParser,
        'markdown': MarkdownParser,
        'md': MarkdownParser
    }
    
    if file_type.lower() not in parsers:
        raise ValueError(f"サポートされていないファイルタイプ: {file_type}")
    
    return parsers[file_type.lower()]()

def get_parser_for_file(file_path: str) -> BaseParser:
    """
    ファイルパスから適切なパーサーを取得
    
    Args:
        file_path: ファイルパス
        
    Returns:
        対応するパーサーインスタンス
        
    Raises:
        ValueError: サポートされていないファイル拡張子
    """
    from pathlib import Path
    
    suffix = Path(file_path).suffix.lower().lstrip('.')
    return create_parser(suffix)

def get_supported_extensions() -> dict:
    """
    サポートされている拡張子の一覧を取得
    
    Returns:
        {拡張子: パーサークラス名} の辞書
    """
    return {
        '.yaml': 'YamlParser',
        '.yml': 'YamlParser', 
        '.sql': 'DdlParser',
        '.ddl': 'DdlParser',
        '.md': 'MarkdownParser',
        '.markdown': 'MarkdownParser'
    }
