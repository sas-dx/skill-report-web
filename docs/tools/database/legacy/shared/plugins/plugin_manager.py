"""
プラグインマネージャー - プラグインライフサイクル管理

要求仕様ID: PLT.1-WEB.1
対応設計書: docs/design/architecture/プラグインアーキテクチャ設計書.md
"""

import os
import sys
import importlib
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Type, Set
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

from .base_plugin import BasePlugin, PluginMetadata, PluginStatus, PluginError, PluginDependencyError
from .registry import PluginRegistry
from ..core.config import get_config
from ..core.logger import get_logger

logger = get_logger(__name__)

class PluginManager:
    """
    プラグインマネージャー
    
    プラグインの発見、ロード、ライフサイクル管理を行います。
    """
    
    def __init__(self):
        self._plugins: Dict[str, BasePlugin] = {}
        self._plugin_classes: Dict[str, Type[BasePlugin]] = {}
        self._registry = PluginRegistry()
        self._lock = threading.RLock()
        self._plugin_paths: List[Path] = []
        self._hooks: Dict[str, List[BasePlugin]] = {}
        
        # 設定から初期化
        config = get_config()
        self._max_workers = config.get('plugins.max_workers', 4)
        self._plugin_timeout = config.get('plugins.timeout', 30)
        
        # デフォルトプラグインパス
        self._add_default_plugin_paths()
    
    def _add_default_plugin_paths(self):
        """デフォルトプラグインパスを追加"""
        # 現在のディレクトリからの相対パス
        current_dir = Path(__file__).parent.parent.parent
        
        # 標準プラグインディレクトリ
        plugin_dirs = [
            current_dir / "plugins" / "builtin",
            current_dir / "plugins" / "external",
            Path.cwd() / "plugins",
        ]
        
        for plugin_dir in plugin_dirs:
            if plugin_dir.exists():
                self._plugin_paths.append(plugin_dir)
    
    def add_plugin_path(self, path: Path):
        """プラグインパスを追加"""
        if path.exists() and path.is_dir():
            self._plugin_paths.append(path)
            logger.info(f"Added plugin path: {path}")
        else:
            logger.warning(f"Plugin path does not exist: {path}")
    
    def discover_plugins(self) -> List[str]:
        """
        プラグインを発見
        
        Returns:
            List[str]: 発見されたプラグイン名のリスト
        """
        discovered = []
        
        with self._lock:
            for plugin_path in self._plugin_paths:
                discovered.extend(self._discover_plugins_in_path(plugin_path))
        
        logger.info(f"Discovered {len(discovered)} plugins: {discovered}")
        return discovered
    
    def _discover_plugins_in_path(self, path: Path) -> List[str]:
        """指定パス内のプラグインを発見"""
        discovered = []
        
        try:
            for item in path.iterdir():
                if item.is_file() and item.suffix == '.py' and not item.name.startswith('_'):
                    # 単一ファイルプラグイン
                    plugin_name = item.stem
                    if self._load_plugin_module(item, plugin_name):
                        discovered.append(plugin_name)
                
                elif item.is_dir() and not item.name.startswith('_'):
                    # ディレクトリプラグイン
                    plugin_file = item / '__init__.py'
                    if plugin_file.exists():
                        plugin_name = item.name
                        if self._load_plugin_module(plugin_file, plugin_name):
                            discovered.append(plugin_name)
        
        except Exception as e:
            logger.error(f"Error discovering plugins in {path}: {e}")
        
        return discovered
    
    def _load_plugin_module(self, module_path: Path, plugin_name: str) -> bool:
        """プラグインモジュールをロード"""
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, module_path)
            if spec is None or spec.loader is None:
                return False
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # プラグインクラスを検索
            plugin_class = self._find_plugin_class(module)
            if plugin_class:
                self._plugin_classes[plugin_name] = plugin_class
                self._registry.register_plugin_class(plugin_name, plugin_class)
                logger.debug(f"Loaded plugin module: {plugin_name}")
                return True
        
        except Exception as e:
            logger.error(f"Failed to load plugin module {plugin_name}: {e}")
        
        return False
    
    def _find_plugin_class(self, module) -> Optional[Type[BasePlugin]]:
        """モジュール内のプラグインクラスを検索"""
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (isinstance(attr, type) and 
                issubclass(attr, BasePlugin) and 
                attr != BasePlugin):
                return attr
        return None
    
    def load_plugin(self, plugin_name: str, config: Optional[Dict] = None) -> bool:
        """
        プラグインをロード
        
        Args:
            plugin_name: プラグイン名
            config: プラグイン設定
            
        Returns:
            bool: ロード成功時True
        """
        with self._lock:
            if plugin_name in self._plugins:
                logger.warning(f"Plugin {plugin_name} is already loaded")
                return True
            
            if plugin_name not in self._plugin_classes:
                logger.error(f"Plugin class not found: {plugin_name}")
                return False
            
            try:
                # プラグインインスタンス作成
                plugin_class = self._plugin_classes[plugin_name]
                plugin = plugin_class()
                
                # 設定適用
                if config:
                    plugin.set_config(config)
                
                # 初期化
                if not plugin.initialize():
                    logger.error(f"Failed to initialize plugin: {plugin_name}")
                    return False
                
                # 登録
                self._plugins[plugin_name] = plugin
                self._registry.register_plugin_instance(plugin_name, plugin)
                
                logger.info(f"Plugin loaded successfully: {plugin_name}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_name}: {e}")
                return False
    
    def unload_plugin(self, plugin_name: str) -> bool:
        """
        プラグインをアンロード
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            bool: アンロード成功時True
        """
        with self._lock:
            if plugin_name not in self._plugins:
                logger.warning(f"Plugin {plugin_name} is not loaded")
                return True
            
            try:
                plugin = self._plugins[plugin_name]
                
                # 無効化・終了
                plugin.shutdown()
                
                # 登録解除
                del self._plugins[plugin_name]
                self._registry.unregister_plugin_instance(plugin_name)
                
                # フック解除
                self._unregister_plugin_hooks(plugin)
                
                logger.info(f"Plugin unloaded successfully: {plugin_name}")
                return True
                
            except Exception as e:
                logger.error(f"Failed to unload plugin {plugin_name}: {e}")
                return False
    
    def activate_plugin(self, plugin_name: str) -> bool:
        """
        プラグインを有効化
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            bool: 有効化成功時True
        """
        with self._lock:
            if plugin_name not in self._plugins:
                logger.error(f"Plugin {plugin_name} is not loaded")
                return False
            
            plugin = self._plugins[plugin_name]
            if plugin.activate():
                self._register_plugin_hooks(plugin)
                return True
            return False
    
    def deactivate_plugin(self, plugin_name: str) -> bool:
        """
        プラグインを無効化
        
        Args:
            plugin_name: プラグイン名
            
        Returns:
            bool: 無効化成功時True
        """
        with self._lock:
            if plugin_name not in self._plugins:
                logger.error(f"Plugin {plugin_name} is not loaded")
                return False
            
            plugin = self._plugins[plugin_name]
            if plugin.deactivate():
                self._unregister_plugin_hooks(plugin)
                return True
            return False
    
    def load_all_plugins(self, parallel: bool = True) -> Dict[str, bool]:
        """
        全プラグインをロード
        
        Args:
            parallel: 並列ロード有効時True
            
        Returns:
            Dict[str, bool]: プラグイン名と結果のマップ
        """
        results = {}
        plugin_names = list(self._plugin_classes.keys())
        
        if parallel and len(plugin_names) > 1:
            # 並列ロード
            with ThreadPoolExecutor(max_workers=self._max_workers) as executor:
                future_to_plugin = {
                    executor.submit(self.load_plugin, name): name 
                    for name in plugin_names
                }
                
                for future in as_completed(future_to_plugin, timeout=self._plugin_timeout):
                    plugin_name = future_to_plugin[future]
                    try:
                        results[plugin_name] = future.result()
                    except Exception as e:
                        logger.error(f"Failed to load plugin {plugin_name}: {e}")
                        results[plugin_name] = False
        else:
            # 順次ロード
            for plugin_name in plugin_names:
                results[plugin_name] = self.load_plugin(plugin_name)
        
        successful = sum(1 for success in results.values() if success)
        logger.info(f"Loaded {successful}/{len(plugin_names)} plugins successfully")
        
        return results
    
    def unload_all_plugins(self):
        """全プラグインをアンロード"""
        with self._lock:
            plugin_names = list(self._plugins.keys())
            for plugin_name in plugin_names:
                self.unload_plugin(plugin_name)
    
    def get_plugin(self, plugin_name: str) -> Optional[BasePlugin]:
        """プラグインインスタンスを取得"""
        return self._plugins.get(plugin_name)
    
    def get_active_plugins(self) -> List[BasePlugin]:
        """有効なプラグインのリストを取得"""
        return [
            plugin for plugin in self._plugins.values()
            if plugin.status == PluginStatus.ACTIVE
        ]
    
    def get_plugin_status(self, plugin_name: str) -> Optional[PluginStatus]:
        """プラグインの状態を取得"""
        plugin = self._plugins.get(plugin_name)
        return plugin.status if plugin else None
    
    def _register_plugin_hooks(self, plugin: BasePlugin):
        """プラグインのフックを登録"""
        for hook_name in plugin.metadata.hooks:
            if hook_name not in self._hooks:
                self._hooks[hook_name] = []
            if plugin not in self._hooks[hook_name]:
                self._hooks[hook_name].append(plugin)
    
    def _unregister_plugin_hooks(self, plugin: BasePlugin):
        """プラグインのフックを解除"""
        for hook_name in plugin.metadata.hooks:
            if hook_name in self._hooks and plugin in self._hooks[hook_name]:
                self._hooks[hook_name].remove(plugin)
    
    def execute_hook(self, hook_name: str, *args, **kwargs) -> List[any]:
        """
        フックを実行
        
        Args:
            hook_name: フック名
            *args: 位置引数
            **kwargs: キーワード引数
            
        Returns:
            List[any]: 各プラグインの実行結果
        """
        results = []
        
        if hook_name in self._hooks:
            # 優先度順でソート
            plugins = sorted(
                self._hooks[hook_name],
                key=lambda p: p.metadata.priority
            )
            
            for plugin in plugins:
                try:
                    method_name = f"on_{hook_name}"
                    if hasattr(plugin, method_name):
                        method = getattr(plugin, method_name)
                        result = method(*args, **kwargs)
                        results.append(result)
                except Exception as e:
                    logger.error(f"Error executing hook {hook_name} on plugin {plugin.metadata.name}: {e}")
        
        return results
    
    def get_plugin_info(self) -> Dict[str, Dict]:
        """プラグイン情報を取得"""
        info = {}
        
        with self._lock:
            for name, plugin in self._plugins.items():
                metadata = plugin.metadata
                info[name] = {
                    'name': metadata.name,
                    'version': metadata.version,
                    'description': metadata.description,
                    'author': metadata.author,
                    'status': plugin.status.value,
                    'dependencies': metadata.dependencies,
                    'hooks': metadata.hooks,
                    'priority': metadata.priority,
                    'enabled': metadata.enabled
                }
        
        return info
