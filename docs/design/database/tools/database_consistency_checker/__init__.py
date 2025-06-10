"""
データベース整合性チェックツール

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

データベース設計の整合性をチェックするツール
"""

from .checkers.consistency_checker import ConsistencyChecker

try:
    from shared.core.models import CheckResult, CheckSeverity, ConsistencyReport
    from shared.core.config import DatabaseToolsConfig
except ImportError:
    from docs.design.database.tools.shared.core.models import CheckResult, CheckSeverity, ConsistencyReport
    from docs.design.database.tools.shared.core.config import DatabaseToolsConfig

__version__ = "1.2.0"
__all__ = [
    "ConsistencyChecker",
    "CheckResult", 
    "CheckSeverity",
    "ConsistencyReport",
    "DatabaseToolsConfig"
]
