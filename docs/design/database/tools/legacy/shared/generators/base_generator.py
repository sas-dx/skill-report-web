"""
ベースジェネレータークラス
全ジェネレーターの共通基盤

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from pathlib import Path

from ..core.models import TableDefinition, GenerationResult
from ..core.config import Config
from ..core.logger import get_logger
from ..core.exceptions import GenerationError

logger = get_logger(__name__)


class BaseGenerator(ABC):
    """ジェネレーターベースクラス"""
    
    def __init__(self, config: Optional[Config] = None):
        """初期化"""
        self.config = config or Config()
        self.logger = get_logger(self.__class__.__name__)
    
    @abstractmethod
    def generate(self, table_def: TableDefinition, output_path: Path) -> GenerationResult:
        """生成実行（サブクラスで実装）"""
        pass
    
    @abstractmethod
    def get_output_extension(self) -> str:
        """出力ファイル拡張子を取得（サブクラスで実装）"""
        pass
    
    def _handle_generation_error(self, error: Exception, table_name: str) -> GenerationError:
        """生成エラーの統一処理"""
        error_msg = f"生成エラー: {table_name} - {str(error)}"
        self.logger.error(error_msg)
        return GenerationError(error_msg)
    
    def _ensure_output_directory(self, output_path: Path) -> None:
        """出力ディレクトリの確保"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _create_success_result(self, message: str, output_path: Path) -> GenerationResult:
        """成功結果を作成"""
        return GenerationResult(
            success=True,
            message=message,
            output_path=output_path,
            generator_name=self.__class__.__name__
        )
    
    def _create_error_result(self, message: str, error: str = "") -> GenerationResult:
        """エラー結果を作成"""
        return GenerationResult(
            success=False,
            message=message,
            error=error,
            generator_name=self.__class__.__name__
        )
    
    def can_generate(self, table_def: TableDefinition) -> bool:
        """生成可能かチェック"""
        return table_def is not None and table_def.table_name
    
    def get_output_filename(self, table_def: TableDefinition) -> str:
        """出力ファイル名を取得"""
        extension = self.get_output_extension()
        return f"{table_def.table_name}{extension}"
