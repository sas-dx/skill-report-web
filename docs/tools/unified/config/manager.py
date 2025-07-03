#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設定管理システム

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

統一設計ツールシステムの設定管理機能を提供します。
3層設定（グローバル・ツール・プロジェクト）の統合管理と動的設定更新を実装。
"""

import os
import sys
import yaml
import logging
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dataclasses import asdict

# プロジェクトルートを取得
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent
sys.path.append(str(PROJECT_ROOT / "config"))

from .schema import ConfigSchema, Environment, ToolType, DatabaseConfig, APIConfig, ScreenConfig, TestingConfig
from .validator import ConfigValidator, ValidationResult

try:
    from config_manager import ConfigManager as BaseConfigManager
except ImportError:
    # フォールバック実装
    class BaseConfigManager:
        def __init__(self, project_name: str = None):
            self.project_name = project_name
        
        def get_config(self, key: str = None):
            return {}


class UnifiedConfigManager:
    """統一設定管理クラス"""
    
    def __init__(self, project_name: str = "skill-report-web", environment: Environment = Environment.DEVELOPMENT):
        """
        初期化
        
        Args:
            project_name: プロジェクト名
            environment: 実行環境
        """
        self.project_name = project_name
        self.environment = environment
        self.project_root = self._find_project_root()
        
        # 設定ファイルパス
        self.config_root = self.project_root / "config"
        self.global_config_path = self.config_root / "global" / "design-integration.yaml"
        self.tool_config_path = self.config_root / "tools" / "design-integration.yaml"
        self.project_config_path = self.config_root / "projects" / f"{project_name}.yaml"
        
        # キャッシュとバリデーター
        self.config_cache: Optional[ConfigSchema] = None
        self.validator = ConfigValidator(self.project_root)
        self.base_config_manager = BaseConfigManager(project_name)
        
        # ロガー設定
        self.logger = self._setup_logger()
        
        # 設定変更監視
        self._config_watchers = []
    
    def _find_project_root(self) -> Path:
        """プロジェクトルートディレクトリを検索"""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / "package.json").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _setup_logger(self) -> logging.Logger:
        """ロガー設定"""
        logger = logging.getLogger(f"unified_config.{self.project_name}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def load_config(self, force_reload: bool = False) -> ConfigSchema:
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
            # 1. デフォルト設定作成
            config = ConfigSchema(
                project_name=self.project_name,
                environment=self.environment
            )
            
            # 2. グローバル設定読み込み・統合
            global_config = self._load_yaml_file(self.global_config_path)
            if global_config:
                self._merge_config_dict(config, global_config)
                self.logger.info(f"グローバル設定読み込み完了: {self.global_config_path}")
            
            # 3. ツール固有設定読み込み・統合
            tool_config = self._load_yaml_file(self.tool_config_path)
            if tool_config:
                self._merge_config_dict(config, tool_config)
                self.logger.info(f"ツール設定読み込み完了: {self.tool_config_path}")
            
            # 4. プロジェクト固有設定読み込み・統合
            project_config = self._load_yaml_file(self.project_config_path)
            if project_config:
                # プロジェクト設定の design_integration セクションを統合
                if 'design_integration' in project_config:
                    self._merge_config_dict(config, project_config['design_integration'])
                
                # プロジェクト基本情報を設定
                if 'project_info' in project_config:
                    project_info = project_config['project_info']
                    config.project_name = project_info.get('name', config.project_name)
                    if 'metadata' not in config.metadata:
                        config.metadata = {}
                    config.metadata.update(project_info)
                
                self.logger.info(f"プロジェクト設定読み込み完了: {self.project_config_path}")
            
            # 5. 環境変数による上書き
            self._apply_environment_overrides(config)
            
            # 6. 設定検証
            validation_result = self.validator.validate(config)
            if not validation_result.valid:
                self.logger.warning(f"設定検証でエラーが発生しました: {validation_result.errors}")
            
            if validation_result.warnings:
                self.logger.warning(f"設定検証で警告が発生しました: {validation_result.warnings}")
            
            # 7. キャッシュに保存
            self.config_cache = config
            
            self.logger.info("統一設定読み込み完了")
            return config
            
        except Exception as e:
            self.logger.error(f"設定読み込みエラー: {e}")
            # フォールバック設定を返す
            return self._create_fallback_config()
    
    def _load_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """YAMLファイル読み込み"""
        if not file_path.exists():
            self.logger.debug(f"設定ファイルが存在しません: {file_path}")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            self.logger.error(f"YAMLファイル読み込みエラー {file_path}: {e}")
            return {}
    
    def _merge_config_dict(self, config: ConfigSchema, config_dict: Dict[str, Any]):
        """辞書データを設定オブジェクトにマージ"""
        # ツール設定のマージ
        if 'database' in config_dict:
            self._update_dataclass(config.database, config_dict['database'])
        
        if 'api' in config_dict:
            self._update_dataclass(config.api, config_dict['api'])
        
        if 'screens' in config_dict:
            self._update_dataclass(config.screens, config_dict['screens'])
        
        if 'testing' in config_dict:
            self._update_dataclass(config.testing, config_dict['testing'])
        
        # 共通設定のマージ
        if 'paths' in config_dict:
            self._update_dataclass(config.paths, config_dict['paths'])
        
        if 'quality' in config_dict:
            self._update_dataclass(config.quality, config_dict['quality'])
        
        if 'integration' in config_dict:
            self._update_dataclass(config.integration, config_dict['integration'])
        
        if 'logging' in config_dict:
            self._update_dataclass(config.logging, config_dict['logging'])
        
        # 基本情報のマージ
        if 'tool_info' in config_dict:
            tool_info = config_dict['tool_info']
            if 'version' in tool_info:
                config.version = tool_info['version']
        
        # メタデータのマージ
        if 'metadata' in config_dict:
            config.metadata.update(config_dict['metadata'])
    
    def _update_dataclass(self, target_obj: Any, source_dict: Dict[str, Any]):
        """データクラスオブジェクトを辞書データで更新"""
        for key, value in source_dict.items():
            if hasattr(target_obj, key):
                current_value = getattr(target_obj, key)
                if isinstance(current_value, dict) and isinstance(value, dict):
                    # 辞書の場合は深いマージ
                    current_value.update(value)
                else:
                    setattr(target_obj, key, value)
    
    def _apply_environment_overrides(self, config: ConfigSchema):
        """環境変数による設定上書き"""
        # データベース設定
        if os.getenv("UNIFIED_DB_TYPE"):
            config.database.type = os.getenv("UNIFIED_DB_TYPE")
        
        if os.getenv("UNIFIED_DB_STRICT_MODE"):
            config.database.strict_mode = os.getenv("UNIFIED_DB_STRICT_MODE").lower() == "true"
        
        # API設定
        if os.getenv("UNIFIED_API_MOCK_PORT"):
            config.api.mock_server_port = int(os.getenv("UNIFIED_API_MOCK_PORT"))
        
        if os.getenv("UNIFIED_API_MOCK_ENABLED"):
            config.api.mock_server_enabled = os.getenv("UNIFIED_API_MOCK_ENABLED").lower() == "true"
        
        # 品質設定
        if os.getenv("UNIFIED_QUALITY_REQUIREMENT_ID_MANDATORY"):
            config.quality.requirement_id_mandatory = os.getenv("UNIFIED_QUALITY_REQUIREMENT_ID_MANDATORY").lower() == "true"
        
        # ログ設定
        if os.getenv("UNIFIED_LOG_LEVEL"):
            from .schema import LogLevel
            try:
                config.logging.level = LogLevel(os.getenv("UNIFIED_LOG_LEVEL"))
            except ValueError:
                self.logger.warning(f"無効なログレベル: {os.getenv('UNIFIED_LOG_LEVEL')}")
    
    def _create_fallback_config(self) -> ConfigSchema:
        """フォールバック設定作成"""
        self.logger.warning("フォールバック設定を使用します")
        return ConfigSchema(
            project_name=self.project_name,
            environment=self.environment
        )
    
    def get_tool_config(self, tool_name: str) -> Union[DatabaseConfig, APIConfig, ScreenConfig, TestingConfig]:
        """
        指定ツールの設定を取得
        
        Args:
            tool_name: ツール名（database, api, screens, testing）
            
        Returns:
            ツール設定オブジェクト
        """
        config = self.load_config()
        
        tool_mapping = {
            "database": config.database,
            "api": config.api,
            "screens": config.screens,
            "testing": config.testing
        }
        
        if tool_name not in tool_mapping:
            raise ValueError(f"サポートされていないツール名: {tool_name}")
        
        return tool_mapping[tool_name]
    
    def get_path(self, path_type: str) -> str:
        """
        パス取得
        
        Args:
            path_type: パスタイプ
            
        Returns:
            絶対パス
        """
        config = self.load_config()
        
        # 共通パス
        if hasattr(config.paths, path_type):
            relative_path = getattr(config.paths, path_type)
            return str(self.project_root / relative_path)
        
        # ツール固有パス
        for tool_config in [config.database, config.api, config.screens, config.testing]:
            if hasattr(tool_config, path_type):
                relative_path = getattr(tool_config, path_type)
                return str(self.project_root / relative_path)
        
        raise ValueError(f"サポートされていないパスタイプ: {path_type}")
    
    def is_feature_enabled(self, feature_path: str) -> bool:
        """
        機能有効性チェック
        
        Args:
            feature_path: 機能パス（例: "database.auto_generate_ddl"）
            
        Returns:
            機能が有効かどうか
        """
        config = self.load_config()
        
        try:
            keys = feature_path.split('.')
            current = config
            
            for key in keys:
                if hasattr(current, key):
                    current = getattr(current, key)
                else:
                    return False
            
            return bool(current)
        except (AttributeError, TypeError):
            return False
    
    def validate_config(self) -> ValidationResult:
        """
        設定検証
        
        Returns:
            検証結果
        """
        config = self.load_config()
        return self.validator.validate(config)
    
    def save_config(self, output_file: Optional[str] = None) -> bool:
        """
        現在の設定をファイルに保存
        
        Args:
            output_file: 出力ファイルパス（オプション）
            
        Returns:
            保存成功フラグ
        """
        try:
            config = self.load_config()
            output_file = output_file or str(self.project_config_path)
            
            # 設定を辞書形式に変換
            config_dict = config.to_dict()
            
            # ファイルに保存
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_dict, f, default_flow_style=False, allow_unicode=True)
            
            self.logger.info(f"設定を保存しました: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"設定保存エラー: {e}")
            return False
    
    def create_directories(self) -> List[str]:
        """
        必要なディレクトリを作成
        
        Returns:
            作成されたディレクトリのリスト
        """
        config = self.load_config()
        created_dirs = []
        
        # 作成対象ディレクトリ
        directories = [
            config.paths.design_root,
            config.paths.output_root,
            config.paths.backup_root,
            config.paths.temp_root,
            config.database.yaml_dir,
            config.database.ddl_dir,
            config.database.tables_dir,
            config.database.reports_dir,
            config.api.specs_dir,
            config.api.output_dir,
            config.screens.specs_dir,
            config.screens.output_dir,
            config.testing.specs_dir,
            config.testing.unit_test_dir,
            config.testing.e2e_test_dir,
            config.testing.reports_dir
        ]
        
        for directory in directories:
            full_path = self.project_root / directory
            if not full_path.exists():
                try:
                    full_path.mkdir(parents=True, exist_ok=True)
                    created_dirs.append(str(full_path))
                    self.logger.info(f"ディレクトリ作成: {full_path}")
                except Exception as e:
                    self.logger.error(f"ディレクトリ作成エラー {full_path}: {e}")
        
        return created_dirs
    
    def get_config_summary(self) -> Dict[str, Any]:
        """
        設定サマリーを取得
        
        Returns:
            設定サマリー辞書
        """
        config = self.load_config()
        validation_result = self.validator.validate(config)
        
        return {
            "project_name": config.project_name,
            "environment": config.environment.value,
            "version": config.version,
            "tools": {
                "database": {
                    "enabled": True,
                    "type": config.database.type,
                    "strict_mode": config.database.strict_mode
                },
                "api": {
                    "enabled": True,
                    "framework": config.api.framework,
                    "openapi_version": config.api.openapi_version
                },
                "screens": {
                    "enabled": True,
                    "framework": config.screens.framework,
                    "css_framework": config.screens.css_framework
                },
                "testing": {
                    "enabled": True,
                    "frameworks": config.testing.frameworks,
                    "coverage_threshold": config.testing.coverage_threshold
                }
            },
            "validation": {
                "valid": validation_result.valid,
                "error_count": len(validation_result.errors),
                "warning_count": len(validation_result.warnings)
            },
            "paths": {
                "design_root": self.get_path("design_root"),
                "output_root": self.get_path("output_root")
            }
        }
    
    def reload_config(self) -> ConfigSchema:
        """設定を強制再読み込み"""
        self.config_cache = None
        return self.load_config(force_reload=True)
    
    def __str__(self) -> str:
        """文字列表現"""
        return f"UnifiedConfigManager(project={self.project_name}, env={self.environment.value})"
    
    def __repr__(self) -> str:
        """詳細表現"""
        return (
            f"UnifiedConfigManager("
            f"project_name='{self.project_name}', "
            f"environment={self.environment.value}, "
            f"project_root='{self.project_root}'"
            f")"
        )


def main():
    """テスト実行"""
    print("=== 統一設定管理システムテスト ===")
    
    # 設定管理インスタンス作成
    config_manager = UnifiedConfigManager("skill-report-web")
    
    # 設定読み込み
    config = config_manager.load_config()
    print(f"プロジェクト名: {config.project_name}")
    print(f"環境: {config.environment.value}")
    print(f"バージョン: {config.version}")
    
    # ツール設定確認
    print(f"\n=== ツール設定 ===")
    db_config = config_manager.get_tool_config("database")
    print(f"データベースタイプ: {db_config.type}")
    print(f"厳密モード: {db_config.strict_mode}")
    
    api_config = config_manager.get_tool_config("api")
    print(f"APIフレームワーク: {api_config.framework}")
    print(f"OpenAPIバージョン: {api_config.openapi_version}")
    
    # パス確認
    print(f"\n=== パス設定 ===")
    print(f"設計ルート: {config_manager.get_path('design_root')}")
    print(f"出力ルート: {config_manager.get_path('output_root')}")
    
    # 機能確認
    print(f"\n=== 機能設定 ===")
    print(f"DDL自動生成: {config_manager.is_feature_enabled('database.auto_generate_ddl')}")
    print(f"API型自動生成: {config_manager.is_feature_enabled('api.auto_generate_types')}")
    
    # 設定検証
    print(f"\n=== 設定検証 ===")
    validation_result = config_manager.validate_config()
    print(f"検証結果: {'OK' if validation_result.valid else 'NG'}")
    if validation_result.errors:
        print("エラー:")
        for error in validation_result.errors:
            print(f"  - {error}")
    if validation_result.warnings:
        print("警告:")
        for warning in validation_result.warnings:
            print(f"  - {warning}")
    
    # ディレクトリ作成
    print(f"\n=== ディレクトリ作成 ===")
    created_dirs = config_manager.create_directories()
    print(f"作成されたディレクトリ数: {len(created_dirs)}")
    
    # 設定サマリー
    print(f"\n=== 設定サマリー ===")
    summary = config_manager.get_config_summary()
    print(f"プロジェクト: {summary['project_name']}")
    print(f"環境: {summary['environment']}")
    print(f"検証: {'OK' if summary['validation']['valid'] else 'NG'}")


if __name__ == "__main__":
    main()
