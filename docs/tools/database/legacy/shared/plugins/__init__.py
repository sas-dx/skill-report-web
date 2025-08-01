"""
プラグインシステム - 拡張可能なアーキテクチャ

このモジュールは、データベースツールの機能を動的に拡張するための
プラグインアーキテクチャを提供します。

主な機能:
- プラグインの動的ロード・アンロード
- プラグイン間の依存関係管理
- プラグインライフサイクル管理
- イベント駆動プラグイン通信
"""

from .plugin_manager import PluginManager
from .base_plugin import BasePlugin, PluginMetadata
from .registry import PluginRegistry
from .decorators import plugin, hook

__all__ = [
    'PluginManager',
    'BasePlugin', 
    'PluginMetadata',
    'PluginRegistry',
    'plugin',
    'hook'
]

# グローバルプラグインマネージャーインスタンス
_plugin_manager = None

def get_plugin_manager() -> PluginManager:
    """グローバルプラグインマネージャーを取得"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager

def initialize_plugins():
    """プラグインシステムを初期化"""
    manager = get_plugin_manager()
    manager.discover_plugins()
    manager.load_all_plugins()

def shutdown_plugins():
    """プラグインシステムを終了"""
    manager = get_plugin_manager()
    manager.unload_all_plugins()
