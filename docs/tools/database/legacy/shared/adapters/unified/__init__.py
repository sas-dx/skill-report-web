"""
統合アダプターパッケージ

全ての統合アダプターを提供するパッケージ
- UnifiedFileSystemAdapter: ファイルシステム操作の統一
- UnifiedDataTransformAdapter: データ変換処理の統一
"""

from .filesystem_adapter import UnifiedFileSystemAdapter
from .data_transform_adapter import (
    UnifiedDataTransformAdapter,
    TransformResult,
    ValidationResult
)

__all__ = [
    'UnifiedFileSystemAdapter',
    'UnifiedDataTransformAdapter',
    'TransformResult',
    'ValidationResult'
]
