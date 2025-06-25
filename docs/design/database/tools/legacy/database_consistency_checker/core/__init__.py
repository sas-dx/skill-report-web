"""
データベース整合性チェックツール - コアモジュール
"""

from .config import Config, create_check_config

__all__ = [
    'Config',
    'create_check_config'
]
