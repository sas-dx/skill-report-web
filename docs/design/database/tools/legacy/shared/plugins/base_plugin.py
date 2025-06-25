"""
プラグイン基底クラス - 全プラグインの基盤

要求仕様ID: PLT.1-WEB.1
対応設計書: docs/design/architecture/プラグインアーキテクチャ設計書.md
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Any, Optional, Set
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class PluginStatus(Enum):
    """プラグインの状態"""
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"
    ACTIVE = "active"
    ERROR = "error"
    DISABLED = "disabled"

@dataclass
class PluginMetadata:
    """プラグインメタデータ"""
    name: str
    version: str
    description: str
    author: str
    dependencies: List[str] = None
    hooks: List[str] = None
    priority: int = 100
    enabled: bool = True
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.hooks is None:
            self.hooks = []

class BasePlugin(ABC):
    """
    プラグイン基底クラス
    
    全てのプラグインはこのクラスを継承する必要があります。
    プラグインのライフサイクル管理とイベントハンドリングを提供します。
    """
    
    def __init__(self):
        self._status = PluginStatus.UNLOADED
        self._metadata: Optional[PluginMetadata] = None
        self._config: Dict[str, Any] = {}
        self._hooks: Dict[str, List[callable]] = {}
        self._logger = logging.getLogger(f"plugin.{self.__class__.__name__}")
    
    @property
    @abstractmethod
    def metadata(self) -> PluginMetadata:
        """プラグインメタデータを返す"""
        pass
    
    @property
    def status(self) -> PluginStatus:
        """現在のプラグイン状態を返す"""
        return self._status
    
    @property
    def config(self) -> Dict[str, Any]:
        """プラグイン設定を返す"""
        return self._config
    
    def set_config(self, config: Dict[str, Any]):
        """プラグイン設定を設定"""
        self._config = config
    
    def initialize(self) -> bool:
        """
        プラグインを初期化
        
        Returns:
            bool: 初期化成功時True
        """
        try:
            self._status = PluginStatus.LOADING
            self._logger.info(f"Initializing plugin: {self.metadata.name}")
            
            # 依存関係チェック
            if not self._check_dependencies():
                self._status = PluginStatus.ERROR
                return False
            
            # プラグイン固有の初期化
            if not self.on_initialize():
                self._status = PluginStatus.ERROR
                return False
            
            self._status = PluginStatus.LOADED
            self._logger.info(f"Plugin initialized successfully: {self.metadata.name}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to initialize plugin {self.metadata.name}: {e}")
            self._status = PluginStatus.ERROR
            return False
    
    def activate(self) -> bool:
        """
        プラグインを有効化
        
        Returns:
            bool: 有効化成功時True
        """
        try:
            if self._status != PluginStatus.LOADED:
                self._logger.warning(f"Cannot activate plugin {self.metadata.name}: not loaded")
                return False
            
            self._logger.info(f"Activating plugin: {self.metadata.name}")
            
            # フック登録
            self._register_hooks()
            
            # プラグイン固有の有効化処理
            if not self.on_activate():
                return False
            
            self._status = PluginStatus.ACTIVE
            self._logger.info(f"Plugin activated successfully: {self.metadata.name}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to activate plugin {self.metadata.name}: {e}")
            self._status = PluginStatus.ERROR
            return False
    
    def deactivate(self) -> bool:
        """
        プラグインを無効化
        
        Returns:
            bool: 無効化成功時True
        """
        try:
            if self._status != PluginStatus.ACTIVE:
                return True
            
            self._logger.info(f"Deactivating plugin: {self.metadata.name}")
            
            # プラグイン固有の無効化処理
            self.on_deactivate()
            
            # フック解除
            self._unregister_hooks()
            
            self._status = PluginStatus.LOADED
            self._logger.info(f"Plugin deactivated successfully: {self.metadata.name}")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to deactivate plugin {self.metadata.name}: {e}")
            return False
    
    def shutdown(self):
        """プラグインを終了"""
        try:
            self._logger.info(f"Shutting down plugin: {self.metadata.name}")
            
            # 無効化
            if self._status == PluginStatus.ACTIVE:
                self.deactivate()
            
            # プラグイン固有の終了処理
            self.on_shutdown()
            
            self._status = PluginStatus.UNLOADED
            self._logger.info(f"Plugin shut down successfully: {self.metadata.name}")
            
        except Exception as e:
            self._logger.error(f"Failed to shutdown plugin {self.metadata.name}: {e}")
    
    def _check_dependencies(self) -> bool:
        """依存関係をチェック"""
        # TODO: 依存関係チェックロジックを実装
        return True
    
    def _register_hooks(self):
        """フックを登録"""
        for hook_name in self.metadata.hooks:
            if hasattr(self, f"on_{hook_name}"):
                hook_method = getattr(self, f"on_{hook_name}")
                if hook_name not in self._hooks:
                    self._hooks[hook_name] = []
                self._hooks[hook_name].append(hook_method)
    
    def _unregister_hooks(self):
        """フックを解除"""
        self._hooks.clear()
    
    # プラグイン実装者がオーバーライドするメソッド
    
    def on_initialize(self) -> bool:
        """
        プラグイン固有の初期化処理
        
        Returns:
            bool: 初期化成功時True
        """
        return True
    
    def on_activate(self) -> bool:
        """
        プラグイン固有の有効化処理
        
        Returns:
            bool: 有効化成功時True
        """
        return True
    
    def on_deactivate(self):
        """プラグイン固有の無効化処理"""
        pass
    
    def on_shutdown(self):
        """プラグイン固有の終了処理"""
        pass
    
    # イベントハンドリング
    
    def emit_event(self, event_name: str, data: Any = None):
        """イベントを発行"""
        # TODO: イベントバスとの統合
        pass
    
    def handle_event(self, event_name: str, data: Any = None):
        """イベントを処理"""
        handler_name = f"on_{event_name}"
        if hasattr(self, handler_name):
            handler = getattr(self, handler_name)
            try:
                handler(data)
            except Exception as e:
                self._logger.error(f"Error handling event {event_name}: {e}")

class PluginError(Exception):
    """プラグイン関連のエラー"""
    pass

class PluginDependencyError(PluginError):
    """プラグイン依存関係エラー"""
    pass

class PluginLoadError(PluginError):
    """プラグインロードエラー"""
    pass
