"""
高性能キャッシュシステム
処理結果の効率的なキャッシュ管理

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

import time
import hashlib
import pickle
import json
from pathlib import Path
from typing import Any, Optional, Dict, List, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
from collections import OrderedDict
import weakref

from ..core.logger import get_logger
from ..core.exceptions import CacheError
from ..core.config import get_config

logger = get_logger(__name__)


@dataclass
class CacheEntry:
    """キャッシュエントリ"""
    key: str
    value: Any
    created_at: datetime
    accessed_at: datetime
    access_count: int = 0
    ttl: Optional[float] = None  # seconds
    size: int = 0
    
    def is_expired(self) -> bool:
        """有効期限チェック"""
        if self.ttl is None:
            return False
        return (datetime.now() - self.created_at).total_seconds() > self.ttl
    
    def touch(self):
        """アクセス時刻更新"""
        self.accessed_at = datetime.now()
        self.access_count += 1


@dataclass
class CacheStats:
    """キャッシュ統計"""
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_size: int = 0
    entry_count: int = 0
    
    @property
    def hit_rate(self) -> float:
        """ヒット率"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0
    
    @property
    def miss_rate(self) -> float:
        """ミス率"""
        return 1.0 - self.hit_rate


class LRUCache:
    """LRU（Least Recently Used）キャッシュ"""
    
    def __init__(
        self, 
        max_size: int = 1000,
        max_memory: int = 100 * 1024 * 1024,  # 100MB
        default_ttl: Optional[float] = None
    ):
        """
        LRUキャッシュ初期化
        
        Args:
            max_size: 最大エントリ数
            max_memory: 最大メモリ使用量（バイト）
            default_ttl: デフォルトTTL（秒）
        """
        self.max_size = max_size
        self.max_memory = max_memory
        self.default_ttl = default_ttl
        
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.RLock()
        self._stats = CacheStats()
        
        logger.info(f"LRUキャッシュ初期化: max_size={max_size}, max_memory={max_memory}B")
    
    def get(self, key: str) -> Optional[Any]:
        """
        キャッシュから値を取得
        
        Args:
            key: キャッシュキー
            
        Returns:
            Optional[Any]: キャッシュされた値
        """
        with self._lock:
            if key not in self._cache:
                self._stats.misses += 1
                return None
            
            entry = self._cache[key]
            
            # 有効期限チェック
            if entry.is_expired():
                del self._cache[key]
                self._stats.misses += 1
                self._stats.evictions += 1
                self._update_stats()
                return None
            
            # LRU更新（最後に移動）
            self._cache.move_to_end(key)
            entry.touch()
            
            self._stats.hits += 1
            return entry.value
    
    def put(self, key: str, value: Any, ttl: Optional[float] = None) -> bool:
        """
        キャッシュに値を保存
        
        Args:
            key: キャッシュキー
            value: 保存する値
            ttl: TTL（秒）
            
        Returns:
            bool: 成功フラグ
        """
        try:
            # 値のサイズ計算
            size = self._calculate_size(value)
            
            with self._lock:
                now = datetime.now()
                
                # 既存エントリの更新
                if key in self._cache:
                    old_entry = self._cache[key]
                    self._stats.total_size -= old_entry.size
                
                # 新しいエントリ作成
                entry = CacheEntry(
                    key=key,
                    value=value,
                    created_at=now,
                    accessed_at=now,
                    ttl=ttl or self.default_ttl,
                    size=size
                )
                
                # メモリ制限チェック
                if self._stats.total_size + size > self.max_memory:
                    self._evict_by_memory(size)
                
                # サイズ制限チェック
                if len(self._cache) >= self.max_size:
                    self._evict_by_size()
                
                # エントリ追加
                self._cache[key] = entry
                self._cache.move_to_end(key)
                
                self._update_stats()
                return True
                
        except Exception as e:
            logger.error(f"キャッシュ保存エラー: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        キャッシュから削除
        
        Args:
            key: キャッシュキー
            
        Returns:
            bool: 削除成功フラグ
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._update_stats()
                return True
            return False
    
    def clear(self):
        """キャッシュをクリア"""
        with self._lock:
            self._cache.clear()
            self._stats = CacheStats()
    
    def _evict_by_size(self):
        """サイズ制限による退避"""
        while len(self._cache) >= self.max_size:
            # 最も古いエントリを削除
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
            self._stats.evictions += 1
    
    def _evict_by_memory(self, required_size: int):
        """メモリ制限による退避"""
        while (self._stats.total_size + required_size > self.max_memory and 
               len(self._cache) > 0):
            # 最も古いエントリを削除
            oldest_key = next(iter(self._cache))
            oldest_entry = self._cache[oldest_key]
            self._stats.total_size -= oldest_entry.size
            del self._cache[oldest_key]
            self._stats.evictions += 1
    
    def _calculate_size(self, value: Any) -> int:
        """値のサイズを計算"""
        try:
            return len(pickle.dumps(value))
        except Exception:
            # pickle化できない場合は推定サイズ
            if isinstance(value, str):
                return len(value.encode('utf-8'))
            elif isinstance(value, (list, tuple)):
                return sum(self._calculate_size(item) for item in value)
            elif isinstance(value, dict):
                return sum(self._calculate_size(k) + self._calculate_size(v) 
                          for k, v in value.items())
            else:
                return 1024  # デフォルト1KB
    
    def _update_stats(self):
        """統計更新"""
        self._stats.entry_count = len(self._cache)
        self._stats.total_size = sum(entry.size for entry in self._cache.values())
    
    def get_stats(self) -> CacheStats:
        """統計取得"""
        with self._lock:
            return self._stats
    
    def cleanup_expired(self) -> int:
        """期限切れエントリのクリーンアップ"""
        with self._lock:
            expired_keys = [
                key for key, entry in self._cache.items()
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                del self._cache[key]
            
            self._update_stats()
            
            if expired_keys:
                logger.debug(f"期限切れエントリを削除: {len(expired_keys)}個")
            
            return len(expired_keys)


class FileCache(LRUCache):
    """ファイル内容専用キャッシュ"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._file_mtimes: Dict[str, float] = {}
    
    def get_file_content(self, file_path: Path) -> Optional[str]:
        """
        ファイル内容をキャッシュから取得
        
        Args:
            file_path: ファイルパス
            
        Returns:
            Optional[str]: ファイル内容
        """
        if not file_path.exists():
            return None
        
        key = str(file_path)
        current_mtime = file_path.stat().st_mtime
        
        # ファイル更新チェック
        if key in self._file_mtimes:
            if self._file_mtimes[key] != current_mtime:
                # ファイルが更新されている
                self.delete(key)
                del self._file_mtimes[key]
        
        # キャッシュから取得
        content = self.get(key)
        if content is not None:
            return content
        
        # ファイル読み込み
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # キャッシュに保存
            self.put(key, content)
            self._file_mtimes[key] = current_mtime
            
            return content
            
        except Exception as e:
            logger.error(f"ファイル読み込みエラー: {e}")
            return None


class ResultCache:
    """処理結果専用キャッシュ"""
    
    def __init__(self, **kwargs):
        self._cache = LRUCache(**kwargs)
    
    def get_or_compute(
        self, 
        key: str, 
        compute_func: Callable[[], Any],
        ttl: Optional[float] = None
    ) -> Any:
        """
        キャッシュから取得、なければ計算して保存
        
        Args:
            key: キャッシュキー
            compute_func: 計算関数
            ttl: TTL（秒）
            
        Returns:
            Any: 結果
        """
        # キャッシュから取得
        result = self._cache.get(key)
        if result is not None:
            return result
        
        # 計算実行
        try:
            result = compute_func()
            self._cache.put(key, result, ttl)
            return result
        except Exception as e:
            logger.error(f"計算エラー (key: {key}): {e}")
            raise
    
    def invalidate_pattern(self, pattern: str):
        """パターンマッチでキャッシュ無効化"""
        import fnmatch
        
        with self._cache._lock:
            keys_to_delete = [
                key for key in self._cache._cache.keys()
                if fnmatch.fnmatch(key, pattern)
            ]
            
            for key in keys_to_delete:
                self._cache.delete(key)
            
            logger.debug(f"パターンマッチで削除: {pattern} -> {len(keys_to_delete)}個")


class CacheManager:
    """統合キャッシュマネージャー"""
    
    def __init__(self):
        """キャッシュマネージャー初期化"""
        config = get_config()
        
        # 各種キャッシュ初期化
        self.file_cache = FileCache(
            max_size=500,
            max_memory=50 * 1024 * 1024,  # 50MB
            default_ttl=3600  # 1時間
        )
        
        self.result_cache = ResultCache(
            max_size=1000,
            max_memory=100 * 1024 * 1024,  # 100MB
            default_ttl=1800  # 30分
        )
        
        self.validation_cache = ResultCache(
            max_size=200,
            max_memory=20 * 1024 * 1024,  # 20MB
            default_ttl=600  # 10分
        )
        
        # クリーンアップタイマー
        self._cleanup_timer = None
        self._start_cleanup_timer()
        
        logger.info("統合キャッシュマネージャー初期化完了")
    
    def _start_cleanup_timer(self):
        """クリーンアップタイマー開始"""
        def cleanup():
            try:
                total_cleaned = 0
                total_cleaned += self.file_cache.cleanup_expired()
                total_cleaned += self.result_cache._cache.cleanup_expired()
                total_cleaned += self.validation_cache._cache.cleanup_expired()
                
                if total_cleaned > 0:
                    logger.info(f"期限切れキャッシュクリーンアップ: {total_cleaned}個")
                
            except Exception as e:
                logger.error(f"キャッシュクリーンアップエラー: {e}")
            finally:
                # 次回タイマー設定
                self._cleanup_timer = threading.Timer(300, cleanup)  # 5分間隔
                self._cleanup_timer.daemon = True
                self._cleanup_timer.start()
        
        cleanup()
    
    def get_file_content(self, file_path: Path) -> Optional[str]:
        """ファイル内容取得（キャッシュ付き）"""
        return self.file_cache.get_file_content(file_path)
    
    def cache_validation_result(
        self, 
        file_path: Path, 
        result: Any,
        ttl: Optional[float] = None
    ):
        """バリデーション結果をキャッシュ"""
        key = f"validation:{file_path}:{file_path.stat().st_mtime}"
        self.validation_cache._cache.put(key, result, ttl)
    
    def get_validation_result(self, file_path: Path) -> Optional[Any]:
        """バリデーション結果をキャッシュから取得"""
        if not file_path.exists():
            return None
        
        key = f"validation:{file_path}:{file_path.stat().st_mtime}"
        return self.validation_cache._cache.get(key)
    
    def cache_processing_result(
        self, 
        operation: str, 
        params: Dict[str, Any], 
        result: Any,
        ttl: Optional[float] = None
    ):
        """処理結果をキャッシュ"""
        # パラメータからキーを生成
        params_str = json.dumps(params, sort_keys=True)
        key_data = f"{operation}:{params_str}"
        key = hashlib.md5(key_data.encode()).hexdigest()
        
        self.result_cache._cache.put(key, result, ttl)
    
    def get_processing_result(
        self, 
        operation: str, 
        params: Dict[str, Any]
    ) -> Optional[Any]:
        """処理結果をキャッシュから取得"""
        params_str = json.dumps(params, sort_keys=True)
        key_data = f"{operation}:{params_str}"
        key = hashlib.md5(key_data.encode()).hexdigest()
        
        return self.result_cache._cache.get(key)
    
    def invalidate_file_cache(self, file_path: Path):
        """ファイルキャッシュ無効化"""
        key = str(file_path)
        self.file_cache.delete(key)
        if key in self.file_cache._file_mtimes:
            del self.file_cache._file_mtimes[key]
    
    def invalidate_all(self):
        """全キャッシュ無効化"""
        self.file_cache.clear()
        self.result_cache._cache.clear()
        self.validation_cache._cache.clear()
        logger.info("全キャッシュを無効化しました")
    
    def get_stats(self) -> Dict[str, CacheStats]:
        """全キャッシュ統計取得"""
        return {
            'file_cache': self.file_cache.get_stats(),
            'result_cache': self.result_cache._cache.get_stats(),
            'validation_cache': self.validation_cache._cache.get_stats()
        }
    
    def __del__(self):
        """デストラクタ"""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()


# グローバルインスタンス
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """グローバルキャッシュマネージャー取得"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager


def cached_file_content(file_path: Path) -> Optional[str]:
    """ファイル内容取得（キャッシュ付き）"""
    return get_cache_manager().get_file_content(file_path)


def cached_result(
    operation: str, 
    params: Dict[str, Any], 
    compute_func: Callable[[], Any],
    ttl: Optional[float] = None
) -> Any:
    """処理結果取得（キャッシュ付き）"""
    cache_manager = get_cache_manager()
    
    # キャッシュから取得
    result = cache_manager.get_processing_result(operation, params)
    if result is not None:
        return result
    
    # 計算実行
    result = compute_func()
    cache_manager.cache_processing_result(operation, params, result, ttl)
    
    return result
