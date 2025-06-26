"""
統一ログシステム

全ツールで共通のログ機能を提供
"""

import logging
import os
from typing import Optional
from .config import get_config


class Logger:
    """統一ログクラス"""
    
    def __init__(self, name: str, config_file: Optional[str] = None):
        """ログ初期化"""
        self.config = get_config(config_file)
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """ログ設定"""
        # 既に設定済みの場合はスキップ
        if self.logger.handlers:
            return
        
        # ログレベル設定
        level = getattr(logging, self.config.logging.level.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        # フォーマッター作成
        formatter = logging.Formatter(self.config.logging.format)
        
        # コンソールハンドラー
        if self.config.logging.console_enabled:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # ファイルハンドラー
        if self.config.logging.file_enabled:
            log_dir = self.config.get_absolute_path(self.config.logging.log_dir)
            os.makedirs(log_dir, exist_ok=True)
            
            log_file = os.path.join(log_dir, f"{self.logger.name}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """デバッグログ"""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """情報ログ"""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """警告ログ"""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """エラーログ"""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """重大エラーログ"""
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs) -> None:
        """例外ログ（スタックトレース付き）"""
        self.logger.exception(message, *args, **kwargs)


# グローバルロガーインスタンス
_loggers: dict = {}


def get_logger(name: str, config_file: Optional[str] = None) -> Logger:
    """ログインスタンスを取得"""
    if name not in _loggers:
        _loggers[name] = Logger(name, config_file)
    return _loggers[name]


def reset_loggers() -> None:
    """ログをリセット（テスト用）"""
    global _loggers
    
    # 既存のハンドラーをクリア
    for logger_instance in _loggers.values():
        for handler in logger_instance.logger.handlers[:]:
            logger_instance.logger.removeHandler(handler)
    
    _loggers.clear()
    
    # ルートロガーもクリア
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
