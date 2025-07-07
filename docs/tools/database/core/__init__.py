"""
統一コアシステム

全ツールで共通の基盤機能を提供するコアモジュール
"""

from .config import get_config, reset_config, Config
from .logger import get_logger, reset_loggers, Logger
from .exceptions import (
    DatabaseToolError,
    ValidationError,
    FileNotFoundError,
    ParseError,
    GenerationError,
    ConfigurationError,
    ConsistencyError,
    handle_exception
)
from .models import (
    RevisionHistory,
    ColumnDefinition,
    IndexDefinition,
    ForeignKeyDefinition,
    TableDefinition,
    ValidationResult,
    GenerationResult,
    ConsistencyCheckResult,
    ToolExecutionResult
)
from .utils import (
    FileUtils,
    YamlUtils,
    JsonUtils,
    TextUtils,
    ValidationUtils,
    DateTimeUtils,
    load_yaml,
    save_yaml,
    ensure_directory,
    get_current_timestamp
)

__version__ = "2.0.0"
__author__ = "Database Tools Team"

# 便利なエイリアス
Config = Config
Logger = Logger

# よく使用される関数をモジュールレベルで公開
__all__ = [
    # 設定
    'get_config',
    'reset_config',
    'Config',
    
    # ログ
    'get_logger',
    'reset_loggers',
    'Logger',
    
    # 例外
    'DatabaseToolError',
    'ValidationError',
    'FileNotFoundError',
    'ParseError',
    'GenerationError',
    'ConfigurationError',
    'ConsistencyError',
    'handle_exception',
    
    # データモデル
    'RevisionHistory',
    'ColumnDefinition',
    'IndexDefinition',
    'ForeignKeyDefinition',
    'TableDefinition',
    'ValidationResult',
    'GenerationResult',
    'ConsistencyCheckResult',
    'ToolExecutionResult',
    
    # ユーティリティクラス
    'FileUtils',
    'YamlUtils',
    'JsonUtils',
    'TextUtils',
    'ValidationUtils',
    'DateTimeUtils',
    
    # 便利関数
    'load_yaml',
    'save_yaml',
    'ensure_directory',
    'get_current_timestamp',
]


def initialize_core(config_file=None):
    """
    コアシステムを初期化
    
    Args:
        config_file: 設定ファイルパス（オプション）
    
    Returns:
        tuple: (config, logger) 設定とロガーのインスタンス
    """
    config = get_config(config_file)
    logger = get_logger('core')
    
    logger.info("データベースツール統一コアシステムを初期化しました")
    logger.info(f"バージョン: {__version__}")
    
    return config, logger


def get_version():
    """バージョン情報を取得"""
    return __version__


def get_system_info():
    """システム情報を取得"""
    import sys
    import platform
    
    return {
        'version': __version__,
        'author': __author__,
        'python_version': sys.version,
        'platform': platform.platform(),
        'architecture': platform.architecture()[0]
    }
