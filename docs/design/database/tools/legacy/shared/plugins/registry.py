"""
プラグインレジストリ - プラグイン登録・発見システム

要求仕様ID: PLT.1-WEB.1
対応設計書: docs/design/architecture/プラグインアーキテクチャ設計書.md
"""

from typing import Dict, List, Optional, Type, Set, Any
from dataclasses import dataclass, field
import json
import threading
from pathlib import Path
import logging

from .base_plugin import BasePlugin, PluginMetadata, PluginStatus
from ..core.logger import get_logger

logger = get_logger(__name__)

@dataclass
class PluginRegistryEntry:
    """プラグインレジストリエントリ"""
    name: str
    plugin_class: Optional[Type[BasePlugin]] = None
    plugin_instance: Optional[BasePlugin] = None
    metadata: Optional[PluginMetadata] = None
    registration_time: float = field(default_factory=lambda: __import__('time').time())
    last_accessed: float = field(default_factory=lambda: __import__('time').time())
    access_count: int = 0
    tags: Set[str] = field(default_factory=set)
    
    def update_access(self):
        """アクセス情報を更新"""
        import time
        self.last_accessed = time.time()
        self.access_count += 1

class PluginRegistry:
    """
    プラグインレジストリ
    
    プラグインの登録、発見、メタデータ管理を行います。
    """
    
    def __init__(self):
        self._entries: Dict[str, PluginRegistryEntry] = {}
        self._lock = threading.RLock()
        self._tags_index: Dict[str, Set[str]] = {}  # tag -> plugin_names
        self._dependency_graph: Dict[str, Set[str]] = {}  # plugin -> dependencies
        self._reverse_dependency_graph: Dict[str, Set[str]] = {}  # plugin -> dependents
        
    def register_plugin_class(self, name: str, plugin_class: Type[BasePlugin], tags: Optional[Set[str]] = None):
        """
        プラグインクラスを登録
        
        Args:
            name: プラグイン名
            plugin_class: プラグインクラス
            tags: プラグインタグ
        """
        with self._lock:
            if name in self._entries:
                entry = self._entries[name]
                entry.plugin_class = plugin_class
            else:
                entry = PluginRegistryEntry(
                    name=name,
                    plugin_class=plugin_class,
                    tags=tags or set()
                )
                self._entries[name] = entry
            
            # メタデータ取得（インスタンス化せずに）
            try:
                temp_instance = plugin_class()
                entry.metadata = temp_instance.metadata
                
                # 依存関係グラフ更新
                self._update_dependency_graph(name, entry.metadata.dependencies)
                
                # タグインデックス更新
                self._update_tags_index(name, entry.tags)
                
            except Exception as e:
                logger.warning(f"Failed to get metadata for plugin {name}: {e}")
            
            logger.debug(f"Registered plugin class: {name}")
    
    def register_plugin_instance(self, name: str, plugin_instance: BasePlugin):
        """
        プラグインインスタンスを登録
        
        Args:
            name: プラグイン名
            plugin_instance: プラグインインスタンス
        """
        with self._lock:
            if name in self._entries:
                entry = self._entries[name]
                entry.plugin_instance = plugin_instance
                entry.metadata = plugin_instance.metadata
            else:
                entry = PluginRegistryEntry(
                    name=name,
                    plugin_instance=plugin_instance,
                    metadata=plugin_instance.metadata
                )
                self._entries[name] = entry
            
            # 依存関係グラフ更新
            self._update_dependency_graph(name, entry.metadata.dependencies)
            
            logger.debug(f"Registered plugin instance: {name}")
    
    def unregister_plugin_class(self, name: str):
        """プラグインクラスの登録を解除"""
        with self._lock:
            if name in self._entries:
                entry = self._entries[name]
                entry.plugin_class = None
                
                # インスタンスも存在しない場合は完全削除
                if entry.plugin_instance is None:
                    self._remove_entry(name)
    
    def unregister_plugin_instance(self, name: str):
        """プラグインインスタンスの登録を解除"""
        with self._lock:
            if name in self._entries:
                entry = self._entries[name]
                entry.plugin_instance = None
                
                # クラスも存在しない場合は完全削除
                if entry.plugin_class is None:
                    self._remove_entry(name)
    
    def _remove_entry(self, name: str):
        """エントリを完全削除"""
        if name in self._entries:
            entry = self._entries[name]
            
            # タグインデックスから削除
            for tag in entry.tags:
                if tag in self._tags_index:
                    self._tags_index[tag].discard(name)
                    if not self._tags_index[tag]:
                        del self._tags_index[tag]
            
            # 依存関係グラフから削除
            self._remove_from_dependency_graph(name)
            
            del self._entries[name]
            logger.debug(f"Removed plugin entry: {name}")
    
    def get_plugin_class(self, name: str) -> Optional[Type[BasePlugin]]:
        """プラグインクラスを取得"""
        with self._lock:
            if name in self._entries:
                entry = self._entries[name]
                entry.update_access()
                return entry.plugin_class
            return None
    
    def get_plugin_instance(self, name: str) -> Optional[BasePlugin]:
        """プラグインインスタンスを取得"""
        with self._lock:
            if name in self._entries:
                entry = self._entries[name]
                entry.update_access()
                return entry.plugin_instance
            return None
    
    def get_plugin_metadata(self, name: str) -> Optional[PluginMetadata]:
        """プラグインメタデータを取得"""
        with self._lock:
            if name in self._entries:
                entry = self._entries[name]
                entry.update_access()
                return entry.metadata
            return None
    
    def list_plugins(self, status_filter: Optional[PluginStatus] = None, 
                    tag_filter: Optional[Set[str]] = None) -> List[str]:
        """
        プラグインリストを取得
        
        Args:
            status_filter: 状態フィルター
            tag_filter: タグフィルター
            
        Returns:
            List[str]: プラグイン名のリスト
        """
        with self._lock:
            result = []
            
            for name, entry in self._entries.items():
                # 状態フィルター
                if status_filter is not None:
                    if entry.plugin_instance is None:
                        continue
                    if entry.plugin_instance.status != status_filter:
                        continue
                
                # タグフィルター
                if tag_filter is not None:
                    if not tag_filter.intersection(entry.tags):
                        continue
                
                result.append(name)
            
            return sorted(result)
    
    def find_plugins_by_tag(self, tag: str) -> List[str]:
        """タグでプラグインを検索"""
        with self._lock:
            return list(self._tags_index.get(tag, set()))
    
    def find_plugins_by_dependency(self, dependency: str) -> List[str]:
        """依存関係でプラグインを検索"""
        with self._lock:
            result = []
            for name, entry in self._entries.items():
                if entry.metadata and dependency in entry.metadata.dependencies:
                    result.append(name)
            return result
    
    def get_dependency_order(self) -> List[str]:
        """
        依存関係を考慮したプラグインの読み込み順序を取得
        
        Returns:
            List[str]: 依存関係順のプラグイン名リスト
        """
        with self._lock:
            return self._topological_sort()
    
    def _update_dependency_graph(self, plugin_name: str, dependencies: List[str]):
        """依存関係グラフを更新"""
        # 既存の依存関係を削除
        if plugin_name in self._dependency_graph:
            for dep in self._dependency_graph[plugin_name]:
                if dep in self._reverse_dependency_graph:
                    self._reverse_dependency_graph[dep].discard(plugin_name)
        
        # 新しい依存関係を追加
        self._dependency_graph[plugin_name] = set(dependencies)
        
        for dep in dependencies:
            if dep not in self._reverse_dependency_graph:
                self._reverse_dependency_graph[dep] = set()
            self._reverse_dependency_graph[dep].add(plugin_name)
    
    def _remove_from_dependency_graph(self, plugin_name: str):
        """依存関係グラフから削除"""
        # 依存関係を削除
        if plugin_name in self._dependency_graph:
            for dep in self._dependency_graph[plugin_name]:
                if dep in self._reverse_dependency_graph:
                    self._reverse_dependency_graph[dep].discard(plugin_name)
            del self._dependency_graph[plugin_name]
        
        # 逆依存関係を削除
        if plugin_name in self._reverse_dependency_graph:
            for dependent in self._reverse_dependency_graph[plugin_name]:
                if dependent in self._dependency_graph:
                    self._dependency_graph[dependent].discard(plugin_name)
            del self._reverse_dependency_graph[plugin_name]
    
    def _update_tags_index(self, plugin_name: str, tags: Set[str]):
        """タグインデックスを更新"""
        for tag in tags:
            if tag not in self._tags_index:
                self._tags_index[tag] = set()
            self._tags_index[tag].add(plugin_name)
    
    def _topological_sort(self) -> List[str]:
        """トポロジカルソートで依存関係順を取得"""
        # Kahn's algorithm
        in_degree = {}
        all_plugins = set(self._entries.keys())
        
        # 入次数を計算
        for plugin in all_plugins:
            in_degree[plugin] = len(self._dependency_graph.get(plugin, set()))
        
        # 入次数0のノードをキューに追加
        queue = [plugin for plugin in all_plugins if in_degree[plugin] == 0]
        result = []
        
        while queue:
            # 優先度順でソート
            queue.sort(key=lambda p: self._get_plugin_priority(p), reverse=True)
            current = queue.pop(0)
            result.append(current)
            
            # 依存するプラグインの入次数を減らす
            for dependent in self._reverse_dependency_graph.get(current, set()):
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        # 循環依存チェック
        if len(result) != len(all_plugins):
            remaining = all_plugins - set(result)
            logger.warning(f"Circular dependency detected in plugins: {remaining}")
            result.extend(remaining)  # 循環依存があっても残りを追加
        
        return result
    
    def _get_plugin_priority(self, plugin_name: str) -> int:
        """プラグインの優先度を取得"""
        entry = self._entries.get(plugin_name)
        if entry and entry.metadata:
            return entry.metadata.priority
        return 100  # デフォルト優先度
    
    def get_statistics(self) -> Dict[str, Any]:
        """レジストリ統計情報を取得"""
        with self._lock:
            stats = {
                'total_plugins': len(self._entries),
                'loaded_classes': sum(1 for e in self._entries.values() if e.plugin_class is not None),
                'active_instances': sum(1 for e in self._entries.values() if e.plugin_instance is not None),
                'total_tags': len(self._tags_index),
                'dependency_relationships': sum(len(deps) for deps in self._dependency_graph.values()),
                'most_accessed': [],
                'least_accessed': []
            }
            
            # アクセス統計
            sorted_by_access = sorted(
                self._entries.values(),
                key=lambda e: e.access_count,
                reverse=True
            )
            
            stats['most_accessed'] = [
                {'name': e.name, 'access_count': e.access_count}
                for e in sorted_by_access[:5]
            ]
            
            stats['least_accessed'] = [
                {'name': e.name, 'access_count': e.access_count}
                for e in sorted_by_access[-5:]
            ]
            
            return stats
    
    def export_registry(self, file_path: Path):
        """レジストリ情報をファイルにエクスポート"""
        with self._lock:
            export_data = {
                'plugins': {},
                'tags_index': {tag: list(plugins) for tag, plugins in self._tags_index.items()},
                'dependency_graph': {plugin: list(deps) for plugin, deps in self._dependency_graph.items()}
            }
            
            for name, entry in self._entries.items():
                plugin_data = {
                    'name': entry.name,
                    'registration_time': entry.registration_time,
                    'last_accessed': entry.last_accessed,
                    'access_count': entry.access_count,
                    'tags': list(entry.tags)
                }
                
                if entry.metadata:
                    plugin_data['metadata'] = {
                        'name': entry.metadata.name,
                        'version': entry.metadata.version,
                        'description': entry.metadata.description,
                        'author': entry.metadata.author,
                        'dependencies': entry.metadata.dependencies,
                        'hooks': entry.metadata.hooks,
                        'priority': entry.metadata.priority,
                        'enabled': entry.metadata.enabled
                    }
                
                export_data['plugins'][name] = plugin_data
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Registry exported to: {file_path}")
    
    def clear(self):
        """レジストリをクリア"""
        with self._lock:
            self._entries.clear()
            self._tags_index.clear()
            self._dependency_graph.clear()
            self._reverse_dependency_graph.clear()
            logger.info("Plugin registry cleared")
