"""
テーブル生成ツール - コアモジュール
"""

import sys
from pathlib import Path

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .logger import Logger
from .adapters import Adapters
from shared.core.models import (
    TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition,
    BusinessColumnDefinition, BusinessIndexDefinition,
    GenerationResult, ProcessingResult, CheckResult, CheckSeverity
)

__all__ = [
    'Logger',
    'Adapters',
    'TableDefinition',
    'ColumnDefinition',
    'IndexDefinition',
    'ForeignKeyDefinition',
    'BusinessColumnDefinition',
    'BusinessIndexDefinition',
    'GenerationResult',
    'ProcessingResult',
    'CheckResult',
    'CheckSeverity'
]
