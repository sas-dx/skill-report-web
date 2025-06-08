"""
修正提案機能パッケージ
データベース整合性チェックで検出された問題に対する修正提案を生成する
"""

from .fix_suggestion_generator import FixSuggestionGenerator
from .table_list_fixer import TableListFixer
from .foreign_key_fixer import ForeignKeyFixer

__all__ = [
    'FixSuggestionGenerator',
    'TableListFixer', 
    'ForeignKeyFixer'
]
