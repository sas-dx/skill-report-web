#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設計統合ツール - 統合設定管理
汎用的な設定ファイル管理とプロジェクト固有設定の統合
"""

import os
import sys
import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field

# プロジェクトルートを取得
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.append(str(PROJECT_ROOT / "config"))

try:
    from config_manager import ConfigManager as BaseConfigManager
except ImportError:
    # フォールバック実装
    class BaseConfigManager:
        def __init__(self, project_name: str = None):
            self.project_name = project_name
        
        def get_config(self, key: str = None):
            return {}

@dataclass
class DesignIntegrationConfig:
    """設計統合ツール設定データクラス"""
    
    # 基本情報
    tool_name: str = "Design Integration Tools"
    version: str = "2.0.0"
    project_name: str = ""
    
    # パス設定
    design_root: str = "docs/design"
    database_specs: str = "docs/design/database/table-details"
    api_specs: str = "docs/design/api/specs"
    screen_specs: str = "docs/design/screens/specs"
    output_root: str = "docs/design"
    backup_root: str = "docs/design/backups"
    
    # 機能設定
    features: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    generation_settings: Dict[str, Any] = field(default_factory=dict)
    quality_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # 統合設定
    integration_settings: Dict[str, Any] = field(default_factory=dict)
    reporting: Dict[str, Any] = field(default_factory=dict)
    
    # ログ設定
    logging_config: Dict[str, Any] = field(default_factory=dict)

class DesignIntegrationConfigManager:
    """設計統合ツール専用設定管理クラス"""
    
    def __init__(self, project_name: str = "skill-report-web"):
        """
        初期化
        
        Args:
            project_name: プロジェクト名
        """
        self.project_name = project_name
        self.base_config_manager = BaseConfigManager(project_name)
        self.config_cache: Optional[DesignIntegrationConfig] = None
        self.logger = self._setup_logger()
        
        # 設定ファイルパス
        self.config_root = PROJECT_ROOT / "config"
        self.global_config_path = self.config_root / "global" / "design-integration.yaml"
        self.tool_config_path = self.config_root / "tools" / "design-integration.yaml"
        self.project_config_path = self.config_root / "projects" / f"{project_name}.yaml"
    
    def _setup_logger(self) -> logging.Logger:
        """ロガー設定"""
        logger = logging.getLogger(f"design_integration.{self.project_name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def load_config(self, force_reload: bool = False) -> DesignIntegrationConfig:
        """
        設定を読み込み・統合
        
        Args:
            force_reload: 強制再読み込みフラグ
            
        Returns:
            統合された設定オブジェクト
        """
        if self.config_cache and not force_reload:
            return self.config_cache
        
        try:
            # 1. グローバル設定読み込み
            global_config = self._load_yaml_file(self.global_config_path)
            self.logger.info(f"グローバル設定読み込み完了: {self.global_config_path}")
            
            # 2. ツール固有設定読み込み
            tool_config = self._load_yaml_file(self.tool_config_path)
            self.logger.info(f"ツール設定読み込み完了: {self.tool_config_path}")
            
            # 3. プロジェクト固有設定読み込み
            project_config = self._load_yaml_file(self.project_config_path)
            self.logger.info(f"プロジェクト設定読み込み完了: {self.project_config_path}")
            
            # 4. 設定統合
            merged_config = self._merge_configs(global_config, tool_config, project_config)
            
            # 5. 設定オブジェクト作成
            self.config_cache = self._create_config_object(merged_config)
            
            self.logger.info("設定統合完了")
            return self.config_cache
            
        except Exception as e:
            self.logger.error(f"設定読み込みエラー: {e}")
            # フォールバック設定を返す
            return self._create_fallback_config()
    
    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """YAMLファイル読み込み"""
        if not file_path.exists():
            self.logger.warning(f"設定ファイルが存在しません: {file_path}")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            self.logger.error(f"YAMLファイル読み込みエラー {file_path}: {e}")
            return {}
    
    def _merge_configs(self, global_config: Dict, tool_config: Dict, project_config: Dict) -> Dict[str, Any]:
        """設定統合（優先度: プロジェクト > ツール > グローバル）"""
        merged = {}
        
        # 1. グローバル設定をベースとする
        merged.update(global_config)
        
        # 2. ツール設定で上書き
        self._deep_merge(merged, tool_config)
        
        # 3. プロジェクト設定で最終上書き
        if 'design_integration' in project_config:
            self._deep_merge(merged, project_config['design_integration'])
        
        # 4. プロジェクト基本情報を追加
        if 'project_info' in project_config:
            merged['project_info'] = project_config['project_info']
        
        return merged
    
    def _deep_merge(self, base: Dict, update: Dict) -> None:
        """辞書の深いマージ"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def _create_config_object(self, merged_config: Dict[str, Any]) -> DesignIntegrationConfig:
        """設定オブジェクト作成"""
        config = DesignIntegrationConfig()
        
        # 基本情報
        if 'tool_info' in merged_config:
            tool_info = merged_config['tool_info']
            config.tool_name = tool_info.get('name', config.tool_name)
            config.version = tool_info.get('version', config.version)
        
        if 'project_info' in merged_config:
            config.project_name = merged_config['project_info'].get('name', self.project_name)
        
        # パス設定
        if 'paths' in merged_config:
            paths = merged_config['paths']
            config.design_root = paths.get('design_root', config.design_root)
            config.database_specs = paths.get('database_specs', config.database_specs)
            config.api_specs = paths.get('api_specs', config.api_specs)
            config.screen_specs = paths.get('screen_specs', config.screen_specs)
            config.output_root = paths.get('output_root', config.output_root)
            config.backup_root = paths.get('backup_root', config.backup_root)
        
        # 機能設定
        config.features = merged_config.get('features', {})
        config.validation_rules = merged_config.get('validation_rules', {})
        config.generation_settings = merged_config.get('generation_settings', {})
        config.quality_metrics = merged_config.get('quality_metrics', {})
        config.integration_settings = merged_config.get('integration_settings', {})
        config.reporting = merged_config.get('reporting', {})
        config.logging_config = merged_config.get('logging', {})
        
        return config
    
    def _create_fallback_config(self) -> DesignIntegrationConfig:
        """フォールバック設定作成"""
        self.logger.warning("フォールバック設定を使用します")
        return DesignIntegrationConfig(project_name=self.project_name)
    
    def get_database_config(self) -> Dict[str, Any]:
        """データベース関連設定取得"""
        config = self.load_config()
        return {
            'validation': config.validation_rules.get('database', {}),
            'generation': config.generation_settings.get('database', {}),
            'paths': {
                'specs_dir': config.database_specs,
                'output_dir': config.output_root + "/database"
            }
        }
    
    def get_api_config(self) -> Dict[str, Any]:
        """API関連設定取得"""
        config = self.load_config()
        return {
            'validation': config.validation_rules.get('api', {}),
            'generation': config.generation_settings.get('api', {}),
            'paths': {
                'specs_dir': config.api_specs,
                'output_dir': config.output_root + "/api"
            }
        }
    
    def get_screen_config(self) -> Dict[str, Any]:
        """画面関連設定取得"""
        config = self.load_config()
        return {
            'validation': config.validation_rules.get('screen', {}),
            'generation': config.generation_settings.get('screen', {}),
            'paths': {
                'specs_dir': config.screen_specs,
                'output_dir': config.output_root + "/screens"
            }
        }
    
    def get_quality_config(self) -> Dict[str, Any]:
        """品質基準設定取得"""
        config = self.load_config()
        return config.quality_metrics
    
    def get_integration_config(self) -> Dict[str, Any]:
        """統合設定取得"""
        config = self.load_config()
        return config.integration_settings
    
    def get_reporting_config(self) -> Dict[str, Any]:
        """レポート設定取得"""
        config = self.load_config()
        return config.reporting
    
    def is_feature_enabled(self, feature_path: str) -> bool:
        """
        機能有効性チェック
        
        Args:
            feature_path: 機能パス（例: "core.database_management"）
            
        Returns:
            機能が有効かどうか
        """
        config = self.load_config()
        features = config.features
        
        try:
            keys = feature_path.split('.')
            current = features
            for key in keys:
                current = current[key]
            return bool(current)
        except (KeyError, TypeError):
            return False
    
    def get_path(self, path_type: str) -> str:
        """
        パス取得
        
        Args:
            path_type: パスタイプ（design_root, database_specs等）
            
        Returns:
            絶対パス
        """
        config = self.load_config()
        
        path_mapping = {
            'design_root': config.design_root,
            'database_specs': config.database_specs,
            'api_specs': config.api_specs,
            'screen_specs': config.screen_specs,
            'output_root': config.output_root,
            'backup_root': config.backup_root
        }
        
        relative_path = path_mapping.get(path_type, config.design_root)
        return str(PROJECT_ROOT / relative_path)
    
    def validate_config(self) -> List[str]:
        """
        設定検証
        
        Returns:
            検証エラーリスト
        """
        errors = []
        config = self.load_config()
        
        # 必須パスの存在チェック
        required_paths = [
            ('design_root', config.design_root),
            ('database_specs', config.database_specs),
            ('api_specs', config.api_specs),
            ('screen_specs', config.screen_specs)
        ]
        
        for path_name, path_value in required_paths:
            full_path = PROJECT_ROOT / path_value
            if not full_path.exists():
                errors.append(f"必須ディレクトリが存在しません: {path_name} = {full_path}")
        
        # 設定値の妥当性チェック
        if not config.project_name:
            errors.append("プロジェクト名が設定されていません")
        
        if not config.tool_name:
            errors.append("ツール名が設定されていません")
        
        return errors
    
    def create_directories(self) -> None:
        """必要なディレクトリを作成"""
        config = self.load_config()
        
        directories = [
            config.design_root,
            config.database_specs,
            config.api_specs,
            config.screen_specs,
            config.output_root,
            config.backup_root,
            config.output_root + "/database",
            config.output_root + "/api",
            config.output_root + "/screens",
            config.output_root + "/reports"
        ]
        
        for directory in directories:
            full_path = PROJECT_ROOT / directory
            full_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"ディレクトリ作成: {full_path}")

def main():
    """テスト実行"""
    print("=== 設計統合ツール設定管理テスト ===")
    
    # 設定管理インスタンス作成
    config_manager = DesignIntegrationConfigManager("skill-report-web")
    
    # 設定読み込み
    config = config_manager.load_config()
    print(f"プロジェクト名: {config.project_name}")
    print(f"ツール名: {config.tool_name}")
    print(f"バージョン: {config.version}")
    
    # パス確認
    print(f"\n=== パス設定 ===")
    print(f"設計ルート: {config_manager.get_path('design_root')}")
    print(f"データベース仕様: {config_manager.get_path('database_specs')}")
    print(f"API仕様: {config_manager.get_path('api_specs')}")
    print(f"画面仕様: {config_manager.get_path('screen_specs')}")
    
    # 機能確認
    print(f"\n=== 機能設定 ===")
    print(f"データベース管理: {config_manager.is_feature_enabled('core.database_management')}")
    print(f"API管理: {config_manager.is_feature_enabled('core.api_management')}")
    print(f"画面管理: {config_manager.is_feature_enabled('core.screen_management')}")
    
    # 設定検証
    print(f"\n=== 設定検証 ===")
    errors = config_manager.validate_config()
    if errors:
        print("検証エラー:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("設定検証OK")
    
    # ディレクトリ作成
    print(f"\n=== ディレクトリ作成 ===")
    config_manager.create_directories()
    print("必要なディレクトリを作成しました")

if __name__ == "__main__":
    main()
