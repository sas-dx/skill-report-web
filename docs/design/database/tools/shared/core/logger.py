"""
統合ログ管理システム
データベースツール統合における統一ログ機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import json

from .config import get_config


class DatabaseToolsLogger:
    """統合ログ管理クラス"""
    
    def __init__(self, name: str = "database_tools"):
        self.config = get_config()
        self.name = name
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """ログ設定の初期化"""
        logger = logging.getLogger(self.name)
        
        # 既存のハンドラーをクリア
        logger.handlers.clear()
        
        # ログレベル設定
        log_level = getattr(logging, self.config.log_level.value.upper(), logging.INFO)
        logger.setLevel(log_level)
        
        # フォーマッター設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # ファイルハンドラー（設定されている場合）
        if hasattr(self.config, 'log_file') and self.config.log_file:
            log_file = Path(self.config.log_file)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        # 重複ログ防止
        logger.propagate = False
        
        return logger
    
    def debug(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """デバッグログ"""
        self._log_with_extra(logging.DEBUG, message, extra_data)
    
    def info(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """情報ログ"""
        self._log_with_extra(logging.INFO, message, extra_data)
    
    def warning(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """警告ログ"""
        self._log_with_extra(logging.WARNING, message, extra_data)
    
    def error(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """エラーログ"""
        self._log_with_extra(logging.ERROR, message, extra_data)
    
    def critical(self, message: str, extra_data: Optional[Dict[str, Any]] = None):
        """重大エラーログ"""
        self._log_with_extra(logging.CRITICAL, message, extra_data)
    
    def _log_with_extra(self, level: int, message: str, extra_data: Optional[Dict[str, Any]]):
        """追加データ付きログ出力"""
        if extra_data:
            # 追加データをJSON形式で付加
            extra_json = json.dumps(extra_data, ensure_ascii=False, default=str)
            full_message = f"{message} | Extra: {extra_json}"
        else:
            full_message = message
        
        self.logger.log(level, full_message)
    
    def log_file_operation(self, file_path: Path, operation: str, 
                          success: bool, **kwargs):
        """ファイル操作ログ"""
        log_data = {
            'file_path': str(file_path),
            'operation': operation,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if success:
            self.info(f"File operation successful: {operation} on {file_path}", log_data)
        else:
            self.error(f"File operation failed: {operation} on {file_path}", log_data)
    
    def log_validation_result(self, validation_type: str, result: bool, 
                             details: Optional[Dict[str, Any]] = None):
        """バリデーション結果ログ"""
        log_data = {
            'validation_type': validation_type,
            'result': result,
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            log_data.update(details)
        
        if result:
            self.info(f"Validation passed: {validation_type}", log_data)
        else:
            self.warning(f"Validation failed: {validation_type}", log_data)
    
    def log_generation_result(self, generator_type: str, target_file: Path, 
                             success: bool, **kwargs):
        """生成結果ログ"""
        log_data = {
            'generator_type': generator_type,
            'target_file': str(target_file),
            'success': success,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if success:
            self.info(f"Generation successful: {generator_type} -> {target_file}", log_data)
        else:
            self.error(f"Generation failed: {generator_type} -> {target_file}", log_data)
    
    def log_consistency_check(self, check_type: str, table_name: str, 
                             issues_found: int, **kwargs):
        """整合性チェックログ"""
        log_data = {
            'check_type': check_type,
            'table_name': table_name,
            'issues_found': issues_found,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if issues_found == 0:
            self.info(f"Consistency check passed: {check_type} for {table_name}", log_data)
        else:
            self.warning(f"Consistency check found {issues_found} issues: {check_type} for {table_name}", log_data)
    
    def log_performance_metric(self, operation: str, duration_ms: float, 
                              **kwargs):
        """パフォーマンスメトリクスログ"""
        log_data = {
            'operation': operation,
            'duration_ms': duration_ms,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        # パフォーマンス閾値チェック
        if duration_ms > 5000:  # 5秒以上
            self.warning(f"Slow operation detected: {operation} took {duration_ms}ms", log_data)
        else:
            self.debug(f"Operation completed: {operation} took {duration_ms}ms", log_data)
    
    def log_tool_execution(self, tool_name: str, command: str, 
                          success: bool, **kwargs):
        """ツール実行ログ"""
        log_data = {
            'tool_name': tool_name,
            'command': command,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if success:
            self.info(f"Tool execution successful: {tool_name} - {command}", log_data)
        else:
            self.error(f"Tool execution failed: {tool_name} - {command}", log_data)


class StructuredLogger:
    """構造化ログ出力クラス"""
    
    def __init__(self, base_logger: DatabaseToolsLogger):
        self.base_logger = base_logger
    
    def log_structured(self, level: str, event_type: str, 
                      data: Dict[str, Any]):
        """構造化ログ出力"""
        structured_data = {
            'event_type': event_type,
            'timestamp': datetime.now().isoformat(),
            **data
        }
        
        message = f"[{event_type}]"
        
        log_method = getattr(self.base_logger, level.lower(), self.base_logger.info)
        log_method(message, structured_data)
    
    def log_table_operation(self, table_name: str, operation: str, 
                           status: str, **kwargs):
        """テーブル操作ログ"""
        self.log_structured('info', 'table_operation', {
            'table_name': table_name,
            'operation': operation,
            'status': status,
            **kwargs
        })
    
    def log_consistency_result(self, check_name: str, result: Dict[str, Any]):
        """整合性チェック結果ログ"""
        self.log_structured('info', 'consistency_check', {
            'check_name': check_name,
            'result': result
        })
    
    def log_generation_stats(self, generator: str, stats: Dict[str, Any]):
        """生成統計ログ"""
        self.log_structured('info', 'generation_stats', {
            'generator': generator,
            'stats': stats
        })


# グローバルロガーインスタンス
_logger_instance: Optional[DatabaseToolsLogger] = None
_structured_logger_instance: Optional[StructuredLogger] = None


def get_logger(name: str = "database_tools") -> DatabaseToolsLogger:
    """グローバルロガーインスタンスを取得"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = DatabaseToolsLogger(name)
    return _logger_instance


def get_structured_logger() -> StructuredLogger:
    """構造化ロガーインスタンスを取得"""
    global _structured_logger_instance
    if _structured_logger_instance is None:
        base_logger = get_logger()
        _structured_logger_instance = StructuredLogger(base_logger)
    return _structured_logger_instance


def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None):
    """ログ設定の初期化"""
    global _logger_instance, _structured_logger_instance
    
    # 既存インスタンスをクリア
    _logger_instance = None
    _structured_logger_instance = None
    
    # 新しいロガーを作成
    logger = get_logger()
    
    # ログレベル更新
    if log_level:
        level = getattr(logging, log_level.upper(), logging.INFO)
        logger.logger.setLevel(level)
        for handler in logger.logger.handlers:
            handler.setLevel(level)
    
    return logger


# 便利な関数
def log_exception(exception: Exception, context: str = ""):
    """例外ログ出力"""
    logger = get_logger()
    
    error_data = {
        'exception_type': type(exception).__name__,
        'exception_message': str(exception),
        'context': context
    }
    
    logger.error(f"Exception occurred: {type(exception).__name__}", error_data)


def log_timing(operation_name: str):
    """タイミング測定デコレータ"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger()
            start_time = datetime.now()
            
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds() * 1000
                logger.log_performance_metric(operation_name, duration, success=True)
                return result
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds() * 1000
                logger.log_performance_metric(operation_name, duration, success=False, error=str(e))
                raise
        
        return wrapper
    return decorator


def set_logger(logger: DatabaseToolsLogger):
    """グローバルロガーインスタンスを設定"""
    global _logger_instance
    _logger_instance = logger


def reset_logger():
    """グローバルロガーインスタンスをリセット"""
    global _logger_instance, _structured_logger_instance
    _logger_instance = None
    _structured_logger_instance = None


def log_function_call(func_name: str, args: tuple = None, kwargs: dict = None):
    """関数呼び出しログ"""
    logger = get_logger()
    log_data = {
        'function_name': func_name,
        'timestamp': datetime.now().isoformat()
    }
    
    if args:
        log_data['args_count'] = len(args)
    if kwargs:
        log_data['kwargs_keys'] = list(kwargs.keys())
    
    logger.debug(f"Function called: {func_name}", log_data)


def log_execution_time(func_name: str, duration_ms: float, success: bool = True):
    """実行時間ログ"""
    logger = get_logger()
    log_data = {
        'function_name': func_name,
        'duration_ms': duration_ms,
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if duration_ms > 1000:  # 1秒以上
        logger.warning(f"Slow function execution: {func_name} took {duration_ms}ms", log_data)
    else:
        logger.debug(f"Function execution: {func_name} took {duration_ms}ms", log_data)
