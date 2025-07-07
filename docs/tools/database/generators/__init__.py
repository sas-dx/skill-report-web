"""
統一ジェネレーターモジュール

各種出力形式のジェネレーターを提供
"""

from .base_generator import BaseGenerator
from .ddl_generator import DdlGenerator
from .markdown_generator import MarkdownGenerator

__all__ = [
    'BaseGenerator',
    'DdlGenerator',
    'MarkdownGenerator'
]

# ジェネレーターファクトリー
def create_generator(output_format: str) -> BaseGenerator:
    """
    出力形式に応じたジェネレーターを作成
    
    Args:
        output_format: 出力形式 ('sql', 'ddl', 'md', 'markdown')
        
    Returns:
        対応するジェネレーターインスタンス
        
    Raises:
        ValueError: サポートされていない出力形式
    """
    generators = {
        'sql': DdlGenerator,
        'ddl': DdlGenerator,
        'md': MarkdownGenerator,
        'markdown': MarkdownGenerator
    }
    
    if output_format.lower() not in generators:
        raise ValueError(f"サポートされていない出力形式: {output_format}")
    
    return generators[output_format.lower()]()

def get_generator_for_file(file_path: str) -> BaseGenerator:
    """
    ファイルパスから適切なジェネレーターを取得
    
    Args:
        file_path: 出力ファイルパス
        
    Returns:
        対応するジェネレーターインスタンス
        
    Raises:
        ValueError: サポートされていないファイル拡張子
    """
    from pathlib import Path
    
    suffix = Path(file_path).suffix.lower().lstrip('.')
    return create_generator(suffix)

def get_supported_formats() -> dict:
    """
    サポートされている出力形式の一覧を取得
    
    Returns:
        {拡張子: ジェネレータークラス名} の辞書
    """
    return {
        '.sql': 'DdlGenerator',
        '.ddl': 'DdlGenerator',
        '.md': 'MarkdownGenerator',
        '.markdown': 'MarkdownGenerator'
    }

def get_all_generators() -> dict:
    """
    利用可能な全ジェネレーターの情報を取得
    
    Returns:
        ジェネレーター情報の辞書
    """
    generators = {
        'ddl': DdlGenerator(),
        'markdown': MarkdownGenerator()
    }
    
    result = {}
    for name, generator in generators.items():
        result[name] = generator.get_generation_info()
    
    return result
