"""
統合設計ツール - 統一設定管理

全ての設計ツールで共通利用される設定管理機能を提供します。
環境別設定、プロジェクト固有設定、ツール間連携設定を統一管理します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum


class Environment(Enum):
    """実行環境の定義"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class ToolType(Enum):
    """設計ツールの種類"""
    DATABASE = "database"
    API = "api"
    SCREENS = "screens"
    TESTING = "testing"


@dataclass
class DatabaseConfig:
    """データベース設計ツール設定"""
    type: str = "postgresql"
    encoding: str = "utf-8"
    yaml_dir: str = "../table-details"
    ddl_dir: str = "../ddl"
    tables_dir: str = "../tables"
    strict_mode: bool = True
    required_sections: list = field(default_factory=lambda: [
        "revision_history", "overview", "notes", "rules"
    ])
    parallel_workers: int = 4
    cache_enabled: bool = True
    cache_ttl: int = 3600


@dataclass
class APIConfig:
    """API設計ツール設定"""
    openapi_version: str = "3.0.3"
    output_dir: str = "../api/specs"
    typescript_dir: str = "../../src/types/api"
    mock_server_port: int = 3001
    validation_strict: bool = True
    auto_generate_types: bool = True
    include_examples: bool = True


@dataclass
class ScreensConfig:
    """画面設計ツール設定"""
    framework: str = "react"
    typescript: bool = True
    components_dir: str = "../../src/components/generated"
    storybook_dir: str = "../../.storybook/generated"
    accessibility_level: str = "AA"
    responsive_breakpoints: list = field(default_factory=lambda: [
        "mobile", "tablet", "desktop"
    ])


@dataclass
class TestingConfig:
    """テスト設計ツール設定"""
    frameworks: list = field(default_factory=lambda: ["jest", "playwright"])
    unit_test_dir: str = "../../src/__tests__"
    e2e_test_dir: str = "../../tests/e2e"
    coverage_threshold: int = 80
    auto_generate_mocks: bool = True
    performance_budget: dict = field(default_factory=lambda: {
        "response_time": 1000,
        "memory_usage": "100MB"
    })


@dataclass
class QualityConfig:
    """品質保証設定"""
    requirement_id_mandatory: bool = True
    design_doc_sync: bool = True
    breaking_change_detection: bool = True
    auto_fix_suggestions: bool = True
    metrics_collection: bool = True
    ci_integration: bool = True


@dataclass
class IntegrationConfig:
    """ツール間連携設定"""
    enable_cross_tool_validation: bool = True
    auto_sync_changes: bool = True
    notification_channels: list = field(default_factory=lambda: ["console", "file"])
    webhook_urls: list = field(default_factory=list)
    real_time_monitoring: bool = False


class IntegratedConfig:
    """統合設計ツール設定管理クラス"""
    
    def __init__(self, config_file: Optional[str] = None, environment: Environment = Environment.DEVELOPMENT):
        """
        設定管理クラスの初期化
        
        Args:
            config_file: 設定ファイルパス（オプション）
            environment: 実行環境
        """
        self.environment = environment
        self.config_file = config_file or self._get_default_config_file()
        self.project_root = self._find_project_root()
        
        # デフォルト設定
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.screens = ScreensConfig()
        self.testing = TestingConfig()
        self.quality = QualityConfig()
        self.integration = IntegrationConfig()
        
        # 設定ファイルから読み込み
        self._load_config()
        
        # 環境変数による上書き
        self._load_environment_variables()
    
    def _get_default_config_file(self) -> str:
        """デフォルト設定ファイルパスを取得"""
        return os.path.join(
            os.path.dirname(__file__), 
            "..", 
            "config", 
            f"integrated_config_{self.environment.value}.yaml"
        )
    
    def _find_project_root(self) -> Path:
        """プロジェクトルートディレクトリを検索"""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / "package.json").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def _load_config(self):
        """設定ファイルから設定を読み込み"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
                
                if config_data:
                    self._update_config_from_dict(config_data)
            except Exception as e:
                print(f"設定ファイル読み込みエラー: {e}")
    
    def _update_config_from_dict(self, config_data: Dict[str, Any]):
        """辞書データから設定を更新"""
        if "database" in config_data:
            self._update_dataclass(self.database, config_data["database"])
        
        if "api" in config_data:
            self._update_dataclass(self.api, config_data["api"])
        
        if "screens" in config_data:
            self._update_dataclass(self.screens, config_data["screens"])
        
        if "testing" in config_data:
            self._update_dataclass(self.testing, config_data["testing"])
        
        if "quality" in config_data:
            self._update_dataclass(self.quality, config_data["quality"])
        
        if "integration" in config_data:
            self._update_dataclass(self.integration, config_data["integration"])
    
    def _update_dataclass(self, target_obj: Any, source_dict: Dict[str, Any]):
        """データクラスオブジェクトを辞書データで更新"""
        for key, value in source_dict.items():
            if hasattr(target_obj, key):
                setattr(target_obj, key, value)
    
    def _load_environment_variables(self):
        """環境変数から設定を読み込み"""
        # データベース設定
        if os.getenv("DB_TYPE"):
            self.database.type = os.getenv("DB_TYPE")
        
        if os.getenv("DB_STRICT_MODE"):
            self.database.strict_mode = os.getenv("DB_STRICT_MODE").lower() == "true"
        
        # API設定
        if os.getenv("API_MOCK_PORT"):
            self.api.mock_server_port = int(os.getenv("API_MOCK_PORT"))
        
        # 品質設定
        if os.getenv("QUALITY_REQUIREMENT_ID_MANDATORY"):
            self.quality.requirement_id_mandatory = os.getenv("QUALITY_REQUIREMENT_ID_MANDATORY").lower() == "true"
    
    def get_tool_config(self, tool_type: ToolType) -> Any:
        """指定されたツールの設定を取得"""
        config_map = {
            ToolType.DATABASE: self.database,
            ToolType.API: self.api,
            ToolType.SCREENS: self.screens,
            ToolType.TESTING: self.testing
        }
        return config_map.get(tool_type)
    
    def get_absolute_path(self, relative_path: str) -> Path:
        """相対パスを絶対パスに変換"""
        if os.path.isabs(relative_path):
            return Path(relative_path)
        return self.project_root / relative_path
    
    def save_config(self, output_file: Optional[str] = None):
        """現在の設定をファイルに保存"""
        output_file = output_file or self.config_file
        
        config_data = {
            "environment": self.environment.value,
            "database": self._dataclass_to_dict(self.database),
            "api": self._dataclass_to_dict(self.api),
            "screens": self._dataclass_to_dict(self.screens),
            "testing": self._dataclass_to_dict(self.testing),
            "quality": self._dataclass_to_dict(self.quality),
            "integration": self._dataclass_to_dict(self.integration)
        }
        
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
    
    def _dataclass_to_dict(self, obj: Any) -> Dict[str, Any]:
        """データクラスオブジェクトを辞書に変換"""
        if hasattr(obj, '__dataclass_fields__'):
            return {
                field_name: getattr(obj, field_name)
                for field_name in obj.__dataclass_fields__
            }
        return {}
    
    def validate_config(self) -> Dict[str, Any]:
        """設定の妥当性を検証"""
        validation_results = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # データベース設定の検証
        if not self.database.yaml_dir:
            validation_results["errors"].append("データベース設定: yaml_dirが設定されていません")
            validation_results["valid"] = False
        
        # API設定の検証
        if self.api.mock_server_port < 1024 or self.api.mock_server_port > 65535:
            validation_results["errors"].append("API設定: mock_server_portが無効な範囲です")
            validation_results["valid"] = False
        
        # テスト設定の検証
        if self.testing.coverage_threshold < 0 or self.testing.coverage_threshold > 100:
            validation_results["errors"].append("テスト設定: coverage_thresholdが無効な範囲です")
            validation_results["valid"] = False
        
        return validation_results
    
    def __str__(self) -> str:
        """設定の文字列表現"""
        return f"IntegratedConfig(environment={self.environment.value}, tools=4)"
    
    def __repr__(self) -> str:
        """設定の詳細表現"""
        return (
            f"IntegratedConfig("
            f"environment={self.environment.value}, "
            f"config_file={self.config_file}, "
            f"project_root={self.project_root}"
            f")"
        )


# グローバル設定インスタンス
_global_config: Optional[IntegratedConfig] = None


def get_config() -> IntegratedConfig:
    """グローバル設定インスタンスを取得"""
    global _global_config
    if _global_config is None:
        _global_config = IntegratedConfig()
    return _global_config


def set_config(config: IntegratedConfig):
    """グローバル設定インスタンスを設定"""
    global _global_config
    _global_config = config


def reset_config():
    """グローバル設定インスタンスをリセット"""
    global _global_config
    _global_config = None
