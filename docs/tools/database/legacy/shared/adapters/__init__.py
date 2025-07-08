"""
共通アダプターモジュール

このモジュールは、テーブル生成ツールと整合性チェックツール間で
共有されるアダプター機能を提供します。
"""

from .base_adapter import BaseAdapter
from .table_adapter import TableDefinitionAdapter
from .consistency_adapter import ConsistencyCheckAdapter

__all__ = [
    'BaseAdapter',
    'TableDefinitionAdapter', 
    'ConsistencyCheckAdapter'
]
