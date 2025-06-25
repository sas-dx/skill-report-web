"""
データベース整合性チェックツール - コアモジュール
"""

from .config import Config, create_check_config
from ...shared.core.models import (
    CheckResult, CheckSeverity, ConsistencyReport, CheckSummary,
    TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition,
    CheckStatus, CheckResultSummary, ValidationResult, FixSuggestion,
    ReportData, TableInfo, ColumnInfo, IndexInfo, ForeignKeyInfo
)

__all__ = [
    'Config',
    'create_check_config',
    'CheckResult',
    'CheckSeverity',
    'ConsistencyReport',
    'CheckSummary',
    'TableDefinition',
    'ColumnDefinition',
    'IndexDefinition',
    'ForeignKeyDefinition',
    'CheckStatus',
    'CheckResultSummary',
    'ValidationResult',
    'FixSuggestion',
    'ReportData',
    'TableInfo',
    'ColumnInfo',
    'IndexInfo',
    'ForeignKeyInfo'
]
