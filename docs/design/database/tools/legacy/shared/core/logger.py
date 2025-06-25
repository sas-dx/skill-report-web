"""
統合ログ機能
全ツールで使用する共通ログ機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-25
実装者: AI駆動開発チーム
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional, Dict, Any, Union
from datetime import datetime
import json
import sys
import traceback


class DatabaseToolsLogger:
    """データベースツール統合ログクラス"""
    
    def __init__(self, name: str, config: Optional['Config'] = None):
        """ログ初期化"""
        self.name = name
        self.config = config
        self.logger = logging.getLogger(name)
        
        # 重複ハンドラー防止
        if not self.logger.handlers:
            self._setup_logger()
    
    def _setup_logger(self):
        """ログ設定"""
        if self.config:
            log_config = self.config.logging
        else:
            # デフォルト設定
            from .config import LogConfig
            log_config = LogConfig()
        
        # ログレベル設定
        level = getattr(logging, log_config.level.upper(), logging.INFO)
        self.logger.setLevel(level)
        
        # フォーマッター作成
        formatter = logging.Formatter(
            log_config.format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # コンソールハンドラー
        if log_config.console_enabled:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # ファイルハンドラー
        if log_config.file_enabled:
            log_config.log_dir.mkdir(parents=True, exist_ok=True)
            log_file = log_config.log_dir / f"{self.name}.log"
            
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=log_config.max_file_size,
                backupCount=log_config.backup_count,
                encoding=log_config.encoding
            )
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """デバッグログ"""
        self._log(logging.DEBUG, message, extra)
    
    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """情報ログ"""
        self._log(logging.INFO, message, extra)
    
    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """警告ログ"""
        self._log(logging.WARNING, message, extra)
    
    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """エラーログ"""
        self._log(logging.ERROR, message, extra)
    
    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """重大エラーログ"""
        self._log(logging.CRITICAL, message, extra)
    
    def exception(self, message: str, extra: Optional[Dict[str, Any]] = None):
        """例外ログ（スタックトレース付き）"""
        extra = extra or {}
        extra['exception'] = traceback.format_exc()
        self._log(logging.ERROR, message, extra)
    
    def _log(self, level: int, message: str, extra: Optional[Dict[str, Any]] = None):
        """内部ログ処理"""
        if extra:
            # 構造化ログ情報を追加
            formatted_extra = self._format_extra(extra)
            full_message = f"{message} | {formatted_extra}"
        else:
            full_message = message
        
        self.logger.log(level, full_message)
    
    def _format_extra(self, extra: Dict[str, Any]) -> str:
        """追加情報のフォーマット"""
        try:
            return json.dumps(extra, ensure_ascii=False, default=str)
        except Exception:
            return str(extra)
    
    def log_file_operation(self, file_path: Path, operation: str, 
                          success: bool, **kwargs):
        """ファイル操作ログ"""
        extra = {
            'file_path': str(file_path),
            'operation': operation,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if success:
            self.info(f"ファイル操作成功: {operation} - {file_path}", extra)
        else:
            self.error(f"ファイル操作失敗: {operation} - {file_path}", extra)
    
    def log_check_result(self, check_name: str, table_name: Optional[str], 
                        result: str, **kwargs):
        """チェック結果ログ"""
        extra = {
            'check_name': check_name,
            'table_name': table_name,
            'result': result,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if result in ['SUCCESS', 'PASSED']:
            self.info(f"チェック成功: {check_name} - {table_name}", extra)
        elif result in ['WARNING']:
            self.warning(f"チェック警告: {check_name} - {table_name}", extra)
        else:
            self.error(f"チェック失敗: {check_name} - {table_name}", extra)
    
    def log_generation_result(self, table_name: str, file_type: str, 
                            success: bool, **kwargs):
        """生成結果ログ"""
        extra = {
            'table_name': table_name,
            'file_type': file_type,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if success:
            self.info(f"ファイル生成成功: {file_type} - {table_name}", extra)
        else:
            self.error(f"ファイル生成失敗: {file_type} - {table_name}", extra)
    
    def log_performance(self, operation: str, duration: float, **kwargs):
        """パフォーマンスログ"""
        extra = {
            'operation': operation,
            'duration_seconds': duration,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        if duration > 10.0:  # 10秒以上は警告
            self.warning(f"処理時間長: {operation} ({duration:.2f}秒)", extra)
        else:
            self.debug(f"処理時間: {operation} ({duration:.2f}秒)", extra)
    
    def log_tool_start(self, tool_name: str, **kwargs):
        """ツール開始ログ"""
        extra = {
            'tool_name': tool_name,
            'start_time': datetime.now().isoformat(),
            **kwargs
        }
        self.info(f"ツール開始: {tool_name}", extra)
    
    def log_tool_end(self, tool_name: str, success: bool, **kwargs):
        """ツール終了ログ"""
        extra = {
            'tool_name': tool_name,
            'end_time': datetime.now().isoformat(),
            'success': success,
            **kwargs
        }
        
        if success:
            self.info(f"ツール正常終了: {tool_name}", extra)
        else:
            self.error(f"ツール異常終了: {tool_name}", extra)


class PerformanceLogger:
    """パフォーマンス測定ログクラス"""
    
    def __init__(self, logger: DatabaseToolsLogger):
        self.logger = logger
        self.start_times: Dict[str, datetime] = {}
    
    def start(self, operation: str):
        """処理開始時刻を記録"""
        self.start_times[operation] = datetime.now()
        self.logger.debug(f"処理開始: {operation}")
    
    def end(self, operation: str, **kwargs):
        """処理終了時刻を記録し、実行時間をログ出力"""
        if operation in self.start_times:
            start_time = self.start_times[operation]
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.logger.log_performance(operation, duration, **kwargs)
            del self.start_times[operation]
        else:
            self.logger.warning(f"処理開始時刻が記録されていません: {operation}")
    
    def measure(self, operation: str):
        """コンテキストマネージャーとして使用"""
        return PerformanceMeasurer(self, operation)


class PerformanceMeasurer:
    """パフォーマンス測定コンテキストマネージャー"""
    
    def __init__(self, perf_logger: PerformanceLogger, operation: str):
        self.perf_logger = perf_logger
        self.operation = operation
    
    def __enter__(self):
        self.perf_logger.start(self.operation)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        success = exc_type is None
        self.perf_logger.end(self.operation, success=success)


class StructuredLogger:
    """構造化ログクラス"""
    
    def __init__(self, logger: DatabaseToolsLogger):
        self.logger = logger
    
    def log_table_processing(self, table_name: str, operation: str, 
                           status: str, **kwargs):
        """テーブル処理ログ"""
        data = {
            'table_name': table_name,
            'operation': operation,
            'status': status,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        message = f"テーブル処理: {operation} - {table_name} ({status})"
        
        if status in ['SUCCESS', 'COMPLETED']:
            self.logger.info(message, data)
        elif status in ['WARNING', 'PARTIAL']:
            self.logger.warning(message, data)
        else:
            self.logger.error(message, data)
    
    def log_validation_result(self, validator: str, target: str, 
                            result: bool, details: Optional[Dict] = None):
        """検証結果ログ"""
        data = {
            'validator': validator,
            'target': target,
            'result': 'PASS' if result else 'FAIL',
            'timestamp': datetime.now().isoformat()
        }
        
        if details:
            data['details'] = details
        
        message = f"検証結果: {validator} - {target} ({'PASS' if result else 'FAIL'})"
        
        if result:
            self.logger.info(message, data)
        else:
            self.logger.error(message, data)
    
    def log_file_statistics(self, file_type: str, count: int, 
                          total_size: int, **kwargs):
        """ファイル統計ログ"""
        data = {
            'file_type': file_type,
            'count': count,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        message = f"ファイル統計: {file_type} - {count}件 ({data['total_size_mb']}MB)"
        self.logger.info(message, data)


# グローバルインスタンス管理
_logger_instances: Dict[str, DatabaseToolsLogger] = {}


def get_logger(name: str = "database_tools", config: Optional['Config'] = None) -> DatabaseToolsLogger:
    """グローバルログインスタンスを取得"""
    if name not in _logger_instances:
        _logger_instances[name] = DatabaseToolsLogger(name, config)
    return _logger_instances[name]


def get_performance_logger(name: str = "database_tools") -> PerformanceLogger:
    """パフォーマンスログインスタンスを取得"""
    logger = get_logger(name)
    return PerformanceLogger(logger)


def get_structured_logger(name: str = "database_tools") -> StructuredLogger:
    """構造化ログインスタンスを取得"""
    logger = get_logger(name)
    return StructuredLogger(logger)


def setup_logging(config: Optional['Config'] = None):
    """ログ設定の初期化"""
    # ルートロガーの設定
    root_logger = logging.getLogger()
    
    # 既存のハンドラーをクリア
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # データベースツール用ログの初期化
    get_logger("database_tools", config)
    get_logger("consistency_checker", config)
    get_logger("table_generator", config)
    get_logger("sample_data_generator", config)


def cleanup_logging():
    """ログリソースのクリーンアップ"""
    global _logger_instances
    
    for logger_instance in _logger_instances.values():
        for handler in logger_instance.logger.handlers[:]:
            handler.close()
            logger_instance.logger.removeHandler(handler)
    
    _logger_instances.clear()


# ログデコレーター
def log_execution(logger_name: str = "database_tools"):
    """関数実行ログデコレーター"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            perf_logger = get_performance_logger(logger_name)
            
            func_name = f"{func.__module__}.{func.__name__}"
            
            try:
                with perf_logger.measure(func_name):
                    logger.debug(f"関数開始: {func_name}")
                    result = func(*args, **kwargs)
                    logger.debug(f"関数正常終了: {func_name}")
                    return result
            except Exception as e:
                logger.exception(f"関数異常終了: {func_name} - {str(e)}")
                raise
        
        return wrapper
    return decorator


def log_file_operation(operation: str, logger_name: str = "database_tools"):
    """ファイル操作ログデコレーター"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            
            # ファイルパスを引数から抽出
            file_path = None
            if args and hasattr(args[0], '__fspath__'):
                file_path = Path(args[0])
            elif 'file_path' in kwargs:
                file_path = Path(kwargs['file_path'])
            elif 'path' in kwargs:
                file_path = Path(kwargs['path'])
            
            try:
                result = func(*args, **kwargs)
                if file_path:
                    logger.log_file_operation(file_path, operation, True)
                return result
            except Exception as e:
                if file_path:
                    logger.log_file_operation(file_path, operation, False, error=str(e))
                raise
        
        return wrapper
    return decorator
