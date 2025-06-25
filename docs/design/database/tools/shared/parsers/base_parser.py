"""
ベースパーサークラス
全パーサーの共通基盤

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pathlib import Path

from ..core.models import TableDefinition, CheckResult
from ..core.config import Config
from ..core.logger import get_logger
from ..core.exceptions import ParsingError

logger = get_logger(__name__)


class BaseParser(ABC):
    """パーサーベースクラス"""
    
    def __init__(self, config: Optional[Config] = None):
        """初期化"""
        self.config = config or Config()
        self.logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    def parse(self, source: Path) -> TableDefinition:
        """解析実行（サブクラスで実装）"""
        pass
    
    @abstractmethod
    def validate(self, source: Path) -> List[CheckResult]:
        """バリデーション実行（サブクラスで実装）"""
        pass
    
    def _handle_parsing_error(self, error: Exception, source: Path) -> ParsingError:
        """解析エラーの統一処理"""
        error_msg = f"解析エラー: {source} - {str(error)}"
        self.logger.error(error_msg)
        return ParsingError(error_msg)
    
    def _validate_file_exists(self, file_path: Path) -> bool:
        """ファイル存在チェック"""
        if not file_path.exists():
            raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")
        return True
    
    def _validate_file_readable(self, file_path: Path) -> bool:
        """ファイル読み取り可能チェック"""
        try:
            with open(file_path, 'r', encoding=self.config.tool.encoding):
                pass
            return True
        except Exception as e:
            raise PermissionError(f"ファイルが読み取れません: {file_path} - {e}")
    
    def _create_success_result(self, message: str, table_name: str = "") -> CheckResult:
        """成功結果を作成"""
        from ..core.models import create_success_result
        return create_success_result(
            check_name=self.__class__.__name__,
            message=message,
            table_name=table_name
        )
    
    def _create_error_result(self, message: str, table_name: str = "", details: str = "") -> CheckResult:
        """エラー結果を作成"""
        from ..core.models import create_error_result
        return create_error_result(
            check_name=self.__class__.__name__,
            message=message,
            table_name=table_name,
            details=details
        )
    
    def _create_warning_result(self, message: str, table_name: str = "", details: str = "") -> CheckResult:
        """警告結果を作成"""
        from ..core.models import create_warning_result
        return create_warning_result(
            check_name=self.__class__.__name__,
            message=message,
            table_name=table_name,
            details=details
        )
    
    def get_supported_extensions(self) -> List[str]:
        """サポートするファイル拡張子を取得"""
        return []
    
    def can_parse(self, file_path: Path) -> bool:
        """ファイルを解析可能かチェック"""
        extensions = self.get_supported_extensions()
        if not extensions:
            return True
        return file_path.suffix.lower() in extensions
