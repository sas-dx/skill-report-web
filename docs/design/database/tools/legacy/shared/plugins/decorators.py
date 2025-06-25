"""
プラグインデコレーター - プラグイン開発支援

要求仕様ID: PLT.1-WEB.1
対応設計書: docs/design/architecture/プラグインアーキテクチャ設計書.md
"""

from functools import wraps
from typing import Dict, List, Any, Optional, Callable, Set
import logging

from .base_plugin import BasePlugin, PluginMetadata
from ..core.logger import get_logger

logger = get_logger(__name__)

def plugin(name: str, version: str, description: str, author: str,
          dependencies: Optional[List[str]] = None,
          hooks: Optional[List[str]] = None,
          priority: int = 100,
          enabled: bool = True,
          tags: Optional[Set[str]] = None):
    """
    プラグインクラスデコレーター
    
    Args:
        name: プラグイン名
        version: バージョン
        description: 説明
        author: 作成者
        dependencies: 依存プラグイン
        hooks: フック名リスト
        priority: 優先度
        enabled: 有効フラグ
        tags: タグセット
    """
    def decorator(cls):
        if not issubclass(cls, BasePlugin):
            raise TypeError(f"@plugin decorator can only be applied to BasePlugin subclasses")
        
        # メタデータを設定
        metadata = PluginMetadata(
            name=name,
            version=version,
            description=description,
            author=author,
            dependencies=dependencies or [],
            hooks=hooks or [],
            priority=priority,
            enabled=enabled
        )
        
        # メタデータプロパティを動的に追加
        cls._plugin_metadata = metadata
        
        # metadata プロパティをオーバーライド
        @property
        def metadata_property(self):
            return cls._plugin_metadata
        
        cls.metadata = metadata_property
        
        # タグ情報を保存
        if tags:
            cls._plugin_tags = tags
        
        logger.debug(f"Plugin decorated: {name} v{version}")
        return cls
    
    return decorator

def hook(hook_name: str, priority: int = 100):
    """
    フックメソッドデコレーター
    
    Args:
        hook_name: フック名
        priority: 実行優先度
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in hook {hook_name}: {e}")
                raise
        
        # フック情報を関数に付与
        wrapper._hook_name = hook_name
        wrapper._hook_priority = priority
        wrapper._is_hook = True
        
        return wrapper
    
    return decorator

def event_handler(event_name: str):
    """
    イベントハンドラーデコレーター
    
    Args:
        event_name: イベント名
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error in event handler {event_name}: {e}")
                raise
        
        # イベントハンドラー情報を関数に付与
        wrapper._event_name = event_name
        wrapper._is_event_handler = True
        
        return wrapper
    
    return decorator

def requires_config(*config_keys: str):
    """
    設定必須デコレーター
    
    Args:
        *config_keys: 必須設定キー
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # 設定チェック
            missing_keys = []
            for key in config_keys:
                if key not in self.config:
                    missing_keys.append(key)
            
            if missing_keys:
                raise ValueError(f"Missing required config keys: {missing_keys}")
            
            return func(self, *args, **kwargs)
        
        wrapper._required_config = config_keys
        return wrapper
    
    return decorator

def cache_result(ttl: int = 300):
    """
    結果キャッシュデコレーター
    
    Args:
        ttl: キャッシュ有効期間（秒）
    """
    def decorator(func):
        cache = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            import hashlib
            import pickle
            
            # キャッシュキー生成
            key_data = (args, tuple(sorted(kwargs.items())))
            key_bytes = pickle.dumps(key_data)
            cache_key = hashlib.md5(key_bytes).hexdigest()
            
            # キャッシュチェック
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if time.time() - timestamp < ttl:
                    return result
                else:
                    del cache[cache_key]
            
            # 実行してキャッシュ
            result = func(*args, **kwargs)
            cache[cache_key] = (result, time.time())
            
            return result
        
        wrapper._is_cached = True
        wrapper._cache_ttl = ttl
        wrapper.clear_cache = lambda: cache.clear()
        
        return wrapper
    
    return decorator

def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    リトライデコレーター
    
    Args:
        max_attempts: 最大試行回数
        delay: 初期遅延時間（秒）
        backoff: 遅延時間の倍率
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                        time.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}")
            
            raise last_exception
        
        wrapper._max_attempts = max_attempts
        wrapper._retry_delay = delay
        wrapper._retry_backoff = backoff
        
        return wrapper
    
    return decorator

def validate_args(**validators):
    """
    引数検証デコレーター
    
    Args:
        **validators: 引数名と検証関数のマップ
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import inspect
            
            # 関数シグネチャ取得
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # 引数検証
            for arg_name, validator in validators.items():
                if arg_name in bound_args.arguments:
                    value = bound_args.arguments[arg_name]
                    if not validator(value):
                        raise ValueError(f"Validation failed for argument '{arg_name}': {value}")
            
            return func(*args, **kwargs)
        
        wrapper._validators = validators
        return wrapper
    
    return decorator

def measure_performance(log_level: int = logging.INFO):
    """
    パフォーマンス測定デコレーター
    
    Args:
        log_level: ログレベル
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                success = True
                return result
            except Exception as e:
                success = False
                raise
            finally:
                end_time = time.time()
                duration = end_time - start_time
                
                status = "SUCCESS" if success else "FAILED"
                logger.log(log_level, f"Performance: {func.__name__} {status} in {duration:.3f}s")
        
        return wrapper
    
    return decorator

def singleton_plugin(cls):
    """
    シングルトンプラグインデコレーター
    
    プラグインクラスをシングルトンにします。
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    # クラスの__new__メソッドをオーバーライド
    original_new = cls.__new__
    
    def new_method(cls_ref, *args, **kwargs):
        return get_instance(*args, **kwargs)
    
    cls.__new__ = staticmethod(new_method)
    cls._is_singleton = True
    
    return cls

def deprecated(reason: str = "", version: str = ""):
    """
    非推奨デコレーター
    
    Args:
        reason: 非推奨理由
        version: 非推奨になったバージョン
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import warnings
            
            message = f"{func.__name__} is deprecated"
            if version:
                message += f" since version {version}"
            if reason:
                message += f": {reason}"
            
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            logger.warning(message)
            
            return func(*args, **kwargs)
        
        wrapper._is_deprecated = True
        wrapper._deprecation_reason = reason
        wrapper._deprecation_version = version
        
        return wrapper
    
    return decorator

# 便利な検証関数
def is_string(value):
    """文字列検証"""
    return isinstance(value, str)

def is_positive_int(value):
    """正の整数検証"""
    return isinstance(value, int) and value > 0

def is_non_empty_string(value):
    """非空文字列検証"""
    return isinstance(value, str) and len(value.strip()) > 0

def is_valid_path(value):
    """有効パス検証"""
    from pathlib import Path
    try:
        Path(value)
        return True
    except:
        return False

def is_in_range(min_val, max_val):
    """範囲内検証関数ファクトリー"""
    def validator(value):
        return isinstance(value, (int, float)) and min_val <= value <= max_val
    return validator

def is_one_of(*valid_values):
    """選択肢検証関数ファクトリー"""
    def validator(value):
        return value in valid_values
    return validator
