#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設計ツールシステム

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

統一された設計ツールシステムのメインパッケージ。
データベース、API、画面設計ツールを統合し、一貫したインターフェースを提供します。
"""

__version__ = "2.0.0"
__author__ = "Design Integration Team"
__description__ = "統一設計ツールシステム - 設計統合・品質保証・自動化"

# 統一設定管理
from .config.manager import UnifiedConfigManager
from .config.schema import ConfigSchema, ToolConfig

# コア機能
from .core.validation import UnifiedValidator
from .core.generation import UnifiedGenerator
from .core.integration import ToolIntegrator
from .core.analysis import DesignAnalyzer

# 主要クラスのエクスポート
__all__ = [
    # 設定管理
    "UnifiedConfigManager",
    "ConfigSchema", 
    "ToolConfig",
    
    # コア機能
    "UnifiedValidator",
    "UnifiedGenerator", 
    "ToolIntegrator",
    "DesignAnalyzer",
    
    # バージョン情報
    "__version__",
    "__author__",
    "__description__"
]

# グローバル設定インスタンス
_global_config_manager = None

def get_config_manager(project_name: str = "skill-report-web") -> UnifiedConfigManager:
    """
    グローバル設定管理インスタンスを取得
    
    Args:
        project_name: プロジェクト名
        
    Returns:
        統一設定管理インスタンス
    """
    global _global_config_manager
    if _global_config_manager is None:
        _global_config_manager = UnifiedConfigManager(project_name)
    return _global_config_manager

def reset_config_manager():
    """グローバル設定管理インスタンスをリセット"""
    global _global_config_manager
    _global_config_manager = None

# 便利関数
def get_tool_config(tool_name: str, project_name: str = "skill-report-web") -> ToolConfig:
    """
    指定ツールの設定を取得
    
    Args:
        tool_name: ツール名（database, api, screens, testing）
        project_name: プロジェクト名
        
    Returns:
        ツール設定オブジェクト
    """
    config_manager = get_config_manager(project_name)
    return config_manager.get_tool_config(tool_name)

def validate_project_config(project_name: str = "skill-report-web") -> dict:
    """
    プロジェクト設定の検証
    
    Args:
        project_name: プロジェクト名
        
    Returns:
        検証結果辞書
    """
    config_manager = get_config_manager(project_name)
    return config_manager.validate_config()
