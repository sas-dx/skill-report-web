"""
データベース整合性チェックツール

データベース設計ドキュメント間の整合性をチェックするツール
"""

__version__ = "1.0.0"
__author__ = "Database Design Team"
__description__ = "データベース整合性チェックツール"

from .core.models import CheckResult, CheckSeverity, ConsistencyReport
from .core.config import Config
from .checkers.consistency_checker import ConsistencyChecker

__all__ = [
    "CheckResult",
    "CheckSeverity", 
    "ConsistencyReport",
    "Config",
    "ConsistencyChecker"
]
