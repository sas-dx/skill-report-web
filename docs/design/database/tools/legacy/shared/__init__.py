"""
共有ライブラリ統合モジュール
データベースツール共通機能の統合エントリーポイント

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

# バージョン情報
__version__ = "2.0.0"
__author__ = "AI駆動開発チーム"
__description__ = "データベースツール共有ライブラリ"

# コアモジュール
from .core.config import get_config, Config
from .core.logger import get_logger, setup_logging
from .core.exceptions import (
    DatabaseToolsError,
    ValidationError,
    FileOperationError,
    ConfigurationError,
    ParsingError,
    GenerationError,
    YamlFormatError,
    TableDefinitionError,
    ConsistencyError,
    DatabaseConnectionError,
    ToolExecutionError
)
from .core.models import (
    TableInfo,
    ColumnInfo,
    IndexInfo,
    ForeignKeyInfo,
    ValidationResult,
    ProcessingResult,
    FileProcessingResult
)

# ユーティリティ
from .utils.file_utils import (
    ensure_directory,
    backup_file,
    safe_write_file,
    get_file_hash,
    find_files_by_pattern,
    copy_file_with_backup,
    FileManager
)
from .utils.validation import (
    validate_yaml_file,
    validate_file_exists,
    validate_directory_structure,
    ValidationEngine
)

# パフォーマンス
from .performance.parallel_processor import (
    ParallelProcessor,
    FileProcessorPool,
    ProcessingResult,
    ProcessingStats,
    create_progress_callback,
    process_files_async,
    process_files_sync
)
from .performance.cache_manager import (
    CacheManager,
    LRUCache,
    FileCache,
    ResultCache,
    get_cache_manager,
    cached_file_content,
    cached_result
)

# 監視・メトリクス
from .monitoring.metrics_collector import (
    MetricsCollector,
    PerformanceMonitor,
    SystemMonitor,
    MetricPoint,
    MetricSummary,
    get_metrics_collector,
    get_performance_monitor,
    get_system_monitor,
    record_metric,
    time_function,
    start_system_monitoring,
    export_metrics
)

# パーサー
from .parsers.base_parser import BaseParser
from .parsers.unified_parser import UnifiedParser

# ジェネレーター
from .generators.base_generator import BaseGenerator
from .generators.unified_generator import UnifiedGenerator

# 便利関数
def initialize_shared_library(
    log_level: str = "INFO",
    enable_caching: bool = True,
    enable_monitoring: bool = True,
    monitoring_interval: int = 60
):
    """
    共有ライブラリの初期化
    
    Args:
        log_level: ログレベル
        enable_caching: キャッシュ有効化
        enable_monitoring: 監視有効化
        monitoring_interval: 監視間隔（秒）
    """
    # ログ設定
    setup_logging(log_level)
    logger = get_logger(__name__)
    
    logger.info(f"共有ライブラリ初期化開始: v{__version__}")
    
    # キャッシュ初期化
    if enable_caching:
        cache_manager = get_cache_manager()
        logger.info("キャッシュシステム初期化完了")
    
    # 監視初期化
    if enable_monitoring:
        start_system_monitoring(monitoring_interval)
        logger.info(f"システム監視開始: interval={monitoring_interval}s")
    
    logger.info("共有ライブラリ初期化完了")


def get_library_info() -> dict:
    """ライブラリ情報取得"""
    return {
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'modules': {
            'core': ['config', 'logger', 'exceptions', 'models'],
            'utils': ['file_utils', 'validation'],
            'performance': ['parallel_processor', 'cache_manager'],
            'monitoring': ['metrics_collector']
        }
    }


def cleanup_shared_library():
    """共有ライブラリのクリーンアップ"""
    logger = get_logger(__name__)
    logger.info("共有ライブラリクリーンアップ開始")
    
    try:
        # システム監視停止
        system_monitor = get_system_monitor()
        system_monitor.stop_monitoring()
        
        # キャッシュクリア
        cache_manager = get_cache_manager()
        cache_manager.invalidate_all()
        
        logger.info("共有ライブラリクリーンアップ完了")
    except Exception as e:
        logger.error(f"クリーンアップエラー: {e}")


# エクスポート対象
__all__ = [
    # バージョン情報
    '__version__',
    '__author__',
    '__description__',
    
    # 初期化・クリーンアップ
    'initialize_shared_library',
    'get_library_info',
    'cleanup_shared_library',
    
    # コア
    'get_config',
    'Config',
    'get_logger',
    'setup_logging',
    'DatabaseToolsError',
    'ValidationError',
    'FileOperationError',
    'ConfigurationError',
    'ParsingError',
    'GenerationError',
    'YamlFormatError',
    'TableDefinitionError',
    'ConsistencyError',
    'DatabaseConnectionError',
    'ToolExecutionError',
    'TableInfo',
    'ColumnInfo',
    'IndexInfo',
    'ForeignKeyInfo',
    'ValidationResult',
    'ProcessingResult',
    'FileProcessingResult',
    
    # ユーティリティ
    'ensure_directory',
    'backup_file',
    'safe_write_file',
    'get_file_hash',
    'find_files_by_pattern',
    'copy_file_with_backup',
    'FileManager',
    'validate_yaml_file',
    'validate_file_exists',
    'validate_directory_structure',
    'ValidationEngine',
    
    # パフォーマンス
    'ParallelProcessor',
    'FileProcessorPool',
    'ProcessingStats',
    'create_progress_callback',
    'process_files_async',
    'process_files_sync',
    'CacheManager',
    'LRUCache',
    'FileCache',
    'ResultCache',
    'get_cache_manager',
    'cached_file_content',
    'cached_result',
    
    # 監視・メトリクス
    'MetricsCollector',
    'PerformanceMonitor',
    'SystemMonitor',
    'MetricPoint',
    'MetricSummary',
    'get_metrics_collector',
    'get_performance_monitor',
    'get_system_monitor',
    'record_metric',
    'time_function',
    'start_system_monitoring',
    'export_metrics',
    
    # パーサー・ジェネレーター
    'BaseParser',
    'UnifiedParser',
    'BaseGenerator',
    'UnifiedGenerator'
]
