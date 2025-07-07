"""
設計統合ツール - ログ管理モジュール
要求仕様ID: PLT.1-WEB.1

設計統合ツール用のログ機能を提供します。
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional
from .config import LoggingConfig


def setup_logging(config: LoggingConfig) -> None:
    """ログ設定のセットアップ"""
    
    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.level.upper()))
    
    # 既存のハンドラーをクリア
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # フォーマッターの作成
    formatter = logging.Formatter(config.format)
    
    # コンソールハンドラー
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # ファイルハンドラー（設定されている場合）
    if config.file_path:
        file_path = Path(config.file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=config.max_file_size,
            backupCount=config.backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """ロガーの取得"""
    return logging.getLogger(name)


class DesignIntegrationLogger:
    """設計統合ツール専用ロガー"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(f"design_integration.{name}")
    
    def debug(self, message: str, **kwargs):
        """デバッグログ"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs):
        """情報ログ"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """警告ログ"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """エラーログ"""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs):
        """重大エラーログ"""
        self.logger.critical(message, extra=kwargs)
    
    def log_operation_start(self, operation: str, target: Optional[str] = None):
        """操作開始ログ"""
        if target:
            self.info(f"操作開始: {operation} (対象: {target})")
        else:
            self.info(f"操作開始: {operation}")
    
    def log_operation_success(self, operation: str, target: Optional[str] = None):
        """操作成功ログ"""
        if target:
            self.info(f"操作成功: {operation} (対象: {target})")
        else:
            self.info(f"操作成功: {operation}")
    
    def log_operation_error(self, operation: str, error: Exception, target: Optional[str] = None):
        """操作エラーログ"""
        if target:
            self.error(f"操作エラー: {operation} (対象: {target}) - {error}")
        else:
            self.error(f"操作エラー: {operation} - {error}")
    
    def log_validation_result(self, target: str, is_valid: bool, errors: Optional[list] = None):
        """検証結果ログ"""
        if is_valid:
            self.info(f"検証成功: {target}")
        else:
            error_count = len(errors) if errors else 0
            self.warning(f"検証失敗: {target} ({error_count}個のエラー)")
            if errors:
                for error in errors:
                    self.warning(f"  - {error}")
    
    def log_generation_result(self, target: str, output_path: str, success: bool):
        """生成結果ログ"""
        if success:
            self.info(f"生成成功: {target} -> {output_path}")
        else:
            self.error(f"生成失敗: {target}")
    
    def log_file_operation(self, operation: str, file_path: str, success: bool):
        """ファイル操作ログ"""
        if success:
            self.debug(f"ファイル{operation}成功: {file_path}")
        else:
            self.error(f"ファイル{operation}失敗: {file_path}")
