"""
統合ログ機能
両ツールで使用する統一されたログ機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import logging
import sys
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import json

from .config import get_config, LogLevel


class DatabaseToolsLogger:
    """統合ログ機能クラス"""
    
    def __init__(self, name: str = "database_tools", 
                 log_file: Optional[Path] = None,
                 console_output: bool = True):
        self.name = name
        self.logger = logging.getLogger(name)
        self.config = get_config()
        
        # ログレベル設定
        self.logger.setLevel(self._get_log_level())
        
        # ハンドラーをクリア（重複防止）
        self.logger.handlers.clear()
        
        # フォーマッター設定
        self.formatter = self._create_formatter()
        
        # コンソールハンドラー
        if console_output:
            self._add_console_handler()
        
        # ファイルハンドラー
        if log_file:
            self._add_file_handler(log_file)
        else:
            # デフォルトログファイル
            default_log_file = self.config.reports_dir / "database_tools.log"
            self._add_file_handler(default_log_file)
    
    def _get_log_level(self) -> int:
        """設定からログレベルを取得"""
        level_mapping = {
            LogLevel.DEBUG: logging.DEBUG,
            LogLevel.INFO: logging.INFO,
            LogLevel.WARNING: logging.WARNING,
            LogLevel.ERROR: logging.ERROR,
            LogLevel.CRITICAL: logging.CRITICAL
        }
        return level_mapping.get(self.config.log_level, logging.INFO)
    
    def _create_formatter(self) -> logging.Formatter:
        """フォーマッターを作成"""
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - "
            "%(filename)s:%(lineno)d - %(funcName)s - %(message)s"
        )
        return logging.Formatter(
            format_string,
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    
    def _add_console_handler(self):
        """コンソールハンドラーを追加"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(self, log_file: Path):
        """ファイルハンドラーを追加"""
        # ログディレクトリ作成
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(
            log_file, 
            encoding=self.config.encoding
        )
        file_handler.setFormatter(self.formatter)
        self.logger.addHandler(file_handler)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """デバッグログ"""
        self._log_with_context(logging.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """情報ログ"""
        self._log_with_context(logging.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """警告ログ"""
        self._log_with_context(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """エラーログ"""
        self._log_with_context(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """重大エラーログ"""
        self._log_with_context(logging.CRITICAL, message, extra)
    
    def _log_with_context(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None):
        """コンテキスト情報付きでログ出力"""
        if extra:
            # 追加情報をJSON形式で付加
            context_str = json.dumps(extra, ensure_ascii=False, default=str)
            full_message = f"{message} | Context: {context_str}"
        else:
            full_message = message
        
        self.logger.log(level, full_message)
    
    def log_operation_start(self, operation: str, **kwargs):
        """操作開始ログ"""
        context = {
            'operation': operation,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        self.info(f"操作開始: {operation}", context)
    
    def log_operation_end(self, operation: str, success: bool = True, 
                         execution_time: Optional[float] = None, **kwargs):
        """操作終了ログ"""
        status = "成功" if success else "失敗"
        context = {
            'operation': operation,
            'status': status,
            'execution_time': execution_time,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if success:
            self.info(f"操作完了: {operation} ({status})", context)
        else:
            self.error(f"操作失敗: {operation} ({status})", context)
    
    def log_table_operation(self, table_name: str, operation: str, 
                           status: str, **kwargs):
        """テーブル操作ログ"""
        context = {
            'table_name': table_name,
            'operation': operation,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if status.upper() in ['SUCCESS', 'COMPLETED']:
            self.info(f"テーブル操作: {table_name} - {operation}", context)
        elif status.upper() in ['WARNING']:
            self.warning(f"テーブル操作警告: {table_name} - {operation}", context)
        else:
            self.error(f"テーブル操作エラー: {table_name} - {operation}", context)
    
    def log_file_operation(self, file_path: Path, operation: str, 
                          success: bool = True, **kwargs):
        """ファイル操作ログ"""
        status = "成功" if success else "失敗"
        context = {
            'file_path': str(file_path),
            'operation': operation,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if success:
            self.info(f"ファイル操作: {operation} - {file_path.name}", context)
        else:
            self.error(f"ファイル操作失敗: {operation} - {file_path.name}", context)
    
    def log_check_result(self, check_type: str, table_name: str, 
                        status: str, message: str, **kwargs):
        """チェック結果ログ"""
        context = {
            'check_type': check_type,
            'table_name': table_name,
            'status': status,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if status.upper() == 'SUCCESS':
            self.debug(f"チェック成功: {check_type} - {table_name}", context)
        elif status.upper() == 'WARNING':
            self.warning(f"チェック警告: {check_type} - {table_name}: {message}", context)
        else:
            self.error(f"チェックエラー: {check_type} - {table_name}: {message}", context)
    
    def log_generation_result(self, table_name: str, status: str, 
                             generated_files: list, **kwargs):
        """生成結果ログ"""
        context = {
            'table_name': table_name,
            'status': status,
            'generated_files': [str(f) for f in generated_files],
            'file_count': len(generated_files),
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if status.upper() == 'SUCCESS':
            self.info(f"生成成功: {table_name} ({len(generated_files)}ファイル)", context)
        elif status.upper() == 'PARTIAL':
            self.warning(f"生成部分成功: {table_name} ({len(generated_files)}ファイル)", context)
        else:
            self.error(f"生成失敗: {table_name}", context)
    
    def log_exception(self, exception: Exception, operation: Optional[str] = None, **kwargs):
        """例外ログ"""
        import traceback
        
        context = {
            'exception_type': type(exception).__name__,
            'exception_message': str(exception),
            'operation': operation,
            'traceback': traceback.format_exc(),
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        self.error(f"例外発生: {type(exception).__name__}: {str(exception)}", context)


class StructuredLogger:
    """構造化ログ出力クラス"""
    
    def __init__(self, logger: DatabaseToolsLogger):
        self.logger = logger
    
    def log_structured(self, level: str, event: str, **fields):
        """構造化ログ出力"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'level': level.upper(),
            **fields
        }
        
        message = f"[{event}]"
        
        if level.upper() == 'DEBUG':
            self.logger.debug(message, log_entry)
        elif level.upper() == 'INFO':
            self.logger.info(message, log_entry)
        elif level.upper() == 'WARNING':
            self.logger.warning(message, log_entry)
        elif level.upper() == 'ERROR':
            self.logger.error(message, log_entry)
        elif level.upper() == 'CRITICAL':
            self.logger.critical(message, log_entry)
    
    def log_performance(self, operation: str, execution_time: float, **metrics):
        """パフォーマンスログ"""
        self.log_structured(
            'info',
            'performance_metric',
            operation=operation,
            execution_time=execution_time,
            **metrics
        )
    
    def log_audit(self, action: str, user: str, resource: str, **details):
        """監査ログ"""
        self.log_structured(
            'info',
            'audit_event',
            action=action,
            user=user,
            resource=resource,
            **details
        )


# グローバルロガーインスタンス
_logger_instance: Optional[DatabaseToolsLogger] = None


def get_logger(name: str = "database_tools") -> DatabaseToolsLogger:
    """グローバルロガーインスタンスを取得"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = DatabaseToolsLogger(name)
    return _logger_instance


def set_logger(logger: DatabaseToolsLogger):
    """グローバルロガーインスタンスを設定"""
    global _logger_instance
    _logger_instance = logger


def reset_logger():
    """グローバルロガーインスタンスをリセット"""
    global _logger_instance
    _logger_instance = None


# 便利関数
def log_function_call(func):
    """関数呼び出しログのデコレータ"""
    def wrapper(*args, **kwargs):
        logger = get_logger()
        func_name = func.__name__
        
        logger.debug(f"関数呼び出し開始: {func_name}", {
            'function': func_name,
            'args_count': len(args),
            'kwargs_keys': list(kwargs.keys())
        })
        
        try:
            result = func(*args, **kwargs)
            logger.debug(f"関数呼び出し成功: {func_name}")
            return result
        except Exception as e:
            logger.log_exception(e, operation=func_name)
            raise
    
    return wrapper


def log_execution_time(func):
    """実行時間ログのデコレータ"""
    def wrapper(*args, **kwargs):
        import time
        
        logger = get_logger()
        func_name = func.__name__
        
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            logger.info(f"実行完了: {func_name}", {
                'function': func_name,
                'execution_time': execution_time,
                'status': 'success'
            })
            
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            
            logger.error(f"実行失敗: {func_name}", {
                'function': func_name,
                'execution_time': execution_time,
                'status': 'failed',
                'error': str(e)
            })
            
            raise
    
    return wrapper
