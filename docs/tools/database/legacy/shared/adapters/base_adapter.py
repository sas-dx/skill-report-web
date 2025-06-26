"""
アダプター基底クラス

全てのアダプターが継承する基底クラスを定義します。
共通的な機能とインターフェースを提供します。
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from ..core.config import DatabaseToolsConfig
from ..core.exceptions import ValidationError, ConversionError


class BaseAdapter(ABC):
    """アダプター基底クラス"""
    
    def __init__(self, config: DatabaseToolsConfig):
        """
        アダプターを初期化
        
        Args:
            config: データベースツール設定
        """
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    def validate_input(self, data: Any) -> bool:
        """
        入力データの検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            bool: 検証結果
            
        Raises:
            ValidationError: 検証エラー時
        """
        pass
    
    @abstractmethod
    def transform_data(self, data: Any) -> Any:
        """
        データ変換処理
        
        Args:
            data: 変換対象データ
            
        Returns:
            Any: 変換後データ
            
        Raises:
            ConversionError: 変換エラー時
        """
        pass
    
    def log_operation(self, operation: str, details: Optional[Dict[str, Any]] = None):
        """
        操作ログの記録
        
        Args:
            operation: 操作名
            details: 詳細情報
        """
        log_message = f"Operation: {operation}"
        if details:
            log_message += f" - Details: {details}"
        self.logger.info(log_message)
    
    def handle_error(self, error: Exception, context: str) -> None:
        """
        エラーハンドリング
        
        Args:
            error: 発生したエラー
            context: エラー発生コンテキスト
        """
        error_message = f"Error in {context}: {str(error)}"
        self.logger.error(error_message)
        
        if isinstance(error, (ValidationError, ConversionError)):
            raise error
        else:
            raise ConversionError(f"Unexpected error in {context}: {str(error)}")
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        設定値の取得
        
        Args:
            key: 設定キー
            default: デフォルト値
            
        Returns:
            Any: 設定値
        """
        return getattr(self.config, key, default)
