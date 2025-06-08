"""
統合データベースツール共通基盤
両ツールで使用する共通モジュールのエントリーポイント

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

# バージョン情報
__version__ = "1.0.0"
__author__ = "AI駆動開発チーム"

# 共通基盤モジュールのインポート
from .core.config import (
    DatabaseToolsConfig, 
    LogLevel, 
    ReportFormat, 
    CheckType,
    get_config, 
    set_config, 
    reset_config
)

from .core.logger import (
    DatabaseToolsLogger,
    StructuredLogger,
    get_logger,
    set_logger,
    reset_logger,
    log_function_call,
    log_execution_time
)

from .core.exceptions import (
    DatabaseToolsException,
    ConfigurationError,
    FileOperationError,
    ParsingError,
    ValidationError,
    GenerationError,
    ConsistencyCheckError,
    ModelConversionError,
    SystemError,
    YamlParsingError,
    BackupError,
    ConversionError,
    ExceptionHandler,
    validation_error,
    file_not_found_error,
    parsing_error,
    model_conversion_error
)

from .core.models import (
    TableCategory,
    Priority,
    CheckStatus,
    GenerationStatus,
    DataType,
    ColumnDefinition,
    IndexDefinition,
    ForeignKeyDefinition,
    TableDefinition,
    CheckResult,
    GenerationResult,
    FixResult,
    ReportSummary,
    create_table_definition_from_yaml
)

from .utils.file_utils import (
    FileManager,
    BackupManager,
    get_file_manager,
    get_backup_manager
)

# 便利な関数のエクスポート
__all__ = [
    # バージョン情報
    "__version__",
    "__author__",
    
    # 設定管理
    "DatabaseToolsConfig",
    "LogLevel",
    "ReportFormat", 
    "CheckType",
    "get_config",
    "set_config",
    "reset_config",
    
    # ログ機能
    "DatabaseToolsLogger",
    "StructuredLogger",
    "get_logger",
    "set_logger",
    "reset_logger",
    "log_function_call",
    "log_execution_time",
    
    # 例外処理
    "DatabaseToolsException",
    "ConfigurationError",
    "FileOperationError",
    "ParsingError",
    "ValidationError",
    "GenerationError",
    "ConsistencyCheckError",
    "ModelConversionError",
    "SystemError",
    "YamlParsingError",
    "BackupError",
    "ConversionError",
    "ExceptionHandler",
    "validation_error",
    "file_not_found_error",
    "parsing_error",
    "model_conversion_error",
    
    # データモデル
    "TableCategory",
    "Priority",
    "CheckStatus",
    "GenerationStatus",
    "DataType",
    "ColumnDefinition",
    "IndexDefinition",
    "ForeignKeyDefinition",
    "TableDefinition",
    "CheckResult",
    "GenerationResult",
    "FixResult",
    "ReportSummary",
    "create_table_definition_from_yaml",
    
    # ファイル操作
    "FileManager",
    "BackupManager",
    "get_file_manager",
    "get_backup_manager"
]


def initialize_shared_infrastructure(config: DatabaseToolsConfig = None):
    """共通基盤の初期化"""
    if config:
        set_config(config)
    
    # ログ初期化
    logger = get_logger()
    logger.info("統合データベースツール共通基盤を初期化しました", {
        "version": __version__,
        "config": get_config().to_dict()
    })
    
    return {
        "config": get_config(),
        "logger": logger,
        "file_manager": get_file_manager(),
        "backup_manager": get_backup_manager()
    }


def get_infrastructure_status():
    """共通基盤の状態取得"""
    try:
        config = get_config()
        logger = get_logger()
        
        status = {
            "version": __version__,
            "config_loaded": True,
            "logger_initialized": True,
            "directories": {
                "base_dir": str(config.base_dir),
                "tools_dir": str(config.tools_dir),
                "table_details_dir": str(config.table_details_dir),
                "ddl_dir": str(config.ddl_dir),
                "tables_dir": str(config.tables_dir),
                "data_dir": str(config.data_dir),
                "reports_dir": str(config.reports_dir),
                "backup_dir": str(config.backup_dir)
            },
            "settings": {
                "log_level": config.log_level.value,
                "backup_enabled": config.backup_enabled,
                "parallel_processing": config.parallel_processing,
                "cache_enabled": config.cache_enabled
            }
        }
        
        logger.debug("共通基盤状態を取得しました", status)
        return status
        
    except Exception as e:
        return {
            "version": __version__,
            "config_loaded": False,
            "logger_initialized": False,
            "error": str(e)
        }
