"""
設計統合ツール - 設定管理モジュール
要求仕様ID: PLT.1-WEB.1

設計統合ツール全体の設定を管理します。
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class DatabaseConfig:
    """データベース設計設定"""
    yaml_dir: str = "docs/design/database/table-details"
    ddl_dir: str = "docs/design/database/ddl"
    tables_dir: str = "docs/design/database/tables"
    backup_dir: str = "docs/design/database/backups"
    
    # YAML検証設定
    required_sections: list = field(default_factory=lambda: [
        'revision_history', 'overview', 'notes', 'rules'
    ])
    min_overview_length: int = 50
    min_notes_count: int = 3
    min_rules_count: int = 3


@dataclass
class APIConfig:
    """API設計設定"""
    specs_dir: str = "docs/design/api/specs"
    yaml_dir: str = "docs/design/api/yaml-details"
    backup_dir: str = "docs/design/api/backups"
    
    # API検証設定
    required_sections: list = field(default_factory=lambda: [
        'endpoint', 'method', 'parameters', 'responses'
    ])
    supported_methods: list = field(default_factory=lambda: [
        'GET', 'POST', 'PUT', 'DELETE', 'PATCH'
    ])


@dataclass
class ScreenConfig:
    """画面設計設定"""
    specs_dir: str = "docs/design/screens/specs"
    yaml_dir: str = "docs/design/screens/screen-details"
    backup_dir: str = "docs/design/screens/backups"
    
    # 画面検証設定
    required_sections: list = field(default_factory=lambda: [
        'screen_id', 'screen_name', 'components', 'navigation'
    ])
    supported_devices: list = field(default_factory=lambda: [
        'desktop', 'tablet', 'mobile'
    ])


@dataclass
class IntegrationConfig:
    """設計統合設定"""
    requirements_dir: str = "docs/requirements"
    output_dir: str = "docs/design/integration"
    reports_dir: str = "docs/design/integration/reports"
    
    # 整合性チェック設定
    check_requirement_mapping: bool = True
    check_cross_references: bool = True
    check_naming_consistency: bool = True


@dataclass
class LoggingConfig:
    """ログ設定"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


class DesignIntegrationConfig:
    """設計統合ツール設定クラス"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        設定初期化
        
        Args:
            config_file: 設定ファイルパス（オプション）
        """
        self.project_root = self._find_project_root()
        
        # デフォルト設定
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.screen = ScreenConfig()
        self.integration = IntegrationConfig()
        self.logging = LoggingConfig()
        
        # 設定ファイルから読み込み
        if config_file:
            self.load_from_file(config_file)
        else:
            # デフォルト設定ファイルを探す
            default_config = self.project_root / "docs" / "tools" / "design-integration" / "config.yaml"
            if default_config.exists():
                self.load_from_file(str(default_config))
    
    def _find_project_root(self) -> Path:
        """プロジェクトルートディレクトリを探す"""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / "package.json").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def load_from_file(self, config_file: str):
        """設定ファイルから読み込み"""
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {config_file}")
        
        try:
            if config_path.suffix.lower() in ['.yaml', '.yml']:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = yaml.safe_load(f)
            elif config_path.suffix.lower() == '.json':
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_data = json.load(f)
            else:
                raise ValueError(f"サポートされていない設定ファイル形式: {config_path.suffix}")
            
            self._update_config(config_data)
            
        except Exception as e:
            raise RuntimeError(f"設定ファイルの読み込みに失敗しました: {e}")
    
    def _update_config(self, config_data: Dict[str, Any]):
        """設定データで更新"""
        if 'database' in config_data:
            self._update_dataclass(self.database, config_data['database'])
        
        if 'api' in config_data:
            self._update_dataclass(self.api, config_data['api'])
        
        if 'screen' in config_data:
            self._update_dataclass(self.screen, config_data['screen'])
        
        if 'integration' in config_data:
            self._update_dataclass(self.integration, config_data['integration'])
        
        if 'logging' in config_data:
            self._update_dataclass(self.logging, config_data['logging'])
    
    def _update_dataclass(self, target_obj: Any, update_data: Dict[str, Any]):
        """データクラスを更新"""
        for key, value in update_data.items():
            if hasattr(target_obj, key):
                setattr(target_obj, key, value)
    
    def get_absolute_path(self, relative_path: str) -> Path:
        """相対パスを絶対パスに変換"""
        return self.project_root / relative_path
    
    def get_database_yaml_dir(self) -> Path:
        """データベースYAMLディレクトリの絶対パス"""
        return self.get_absolute_path(self.database.yaml_dir)
    
    def get_database_ddl_dir(self) -> Path:
        """データベースDDLディレクトリの絶対パス"""
        return self.get_absolute_path(self.database.ddl_dir)
    
    def get_database_tables_dir(self) -> Path:
        """データベーステーブル定義書ディレクトリの絶対パス"""
        return self.get_absolute_path(self.database.tables_dir)
    
    def get_api_specs_dir(self) -> Path:
        """API仕様書ディレクトリの絶対パス"""
        return self.get_absolute_path(self.api.specs_dir)
    
    def get_screen_specs_dir(self) -> Path:
        """画面仕様書ディレクトリの絶対パス"""
        return self.get_absolute_path(self.screen.specs_dir)
    
    def get_integration_output_dir(self) -> Path:
        """統合出力ディレクトリの絶対パス"""
        return self.get_absolute_path(self.integration.output_dir)
    
    def ensure_directories(self):
        """必要なディレクトリを作成"""
        directories = [
            self.get_database_yaml_dir(),
            self.get_database_ddl_dir(),
            self.get_database_tables_dir(),
            self.get_absolute_path(self.database.backup_dir),
            self.get_api_specs_dir(),
            self.get_absolute_path(self.api.yaml_dir),
            self.get_absolute_path(self.api.backup_dir),
            self.get_screen_specs_dir(),
            self.get_absolute_path(self.screen.yaml_dir),
            self.get_absolute_path(self.screen.backup_dir),
            self.get_integration_output_dir(),
            self.get_absolute_path(self.integration.reports_dir),
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_to_file(self, config_file: str):
        """設定をファイルに保存"""
        config_data = {
            'database': {
                'yaml_dir': self.database.yaml_dir,
                'ddl_dir': self.database.ddl_dir,
                'tables_dir': self.database.tables_dir,
                'backup_dir': self.database.backup_dir,
                'required_sections': self.database.required_sections,
                'min_overview_length': self.database.min_overview_length,
                'min_notes_count': self.database.min_notes_count,
                'min_rules_count': self.database.min_rules_count,
            },
            'api': {
                'specs_dir': self.api.specs_dir,
                'yaml_dir': self.api.yaml_dir,
                'backup_dir': self.api.backup_dir,
                'required_sections': self.api.required_sections,
                'supported_methods': self.api.supported_methods,
            },
            'screen': {
                'specs_dir': self.screen.specs_dir,
                'yaml_dir': self.screen.yaml_dir,
                'backup_dir': self.screen.backup_dir,
                'required_sections': self.screen.required_sections,
                'supported_devices': self.screen.supported_devices,
            },
            'integration': {
                'requirements_dir': self.integration.requirements_dir,
                'output_dir': self.integration.output_dir,
                'reports_dir': self.integration.reports_dir,
                'check_requirement_mapping': self.integration.check_requirement_mapping,
                'check_cross_references': self.integration.check_cross_references,
                'check_naming_consistency': self.integration.check_naming_consistency,
            },
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'file_path': self.logging.file_path,
                'max_file_size': self.logging.max_file_size,
                'backup_count': self.logging.backup_count,
            }
        }
        
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        if config_path.suffix.lower() in ['.yaml', '.yml']:
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
        elif config_path.suffix.lower() == '.json':
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"サポートされていない設定ファイル形式: {config_path.suffix}")
    
    def validate(self) -> bool:
        """設定の妥当性をチェック"""
        errors = []
        
        # 必須ディレクトリの存在チェック
        required_dirs = [
            (self.database.yaml_dir, "データベースYAMLディレクトリ"),
            (self.api.specs_dir, "API仕様書ディレクトリ"),
            (self.screen.specs_dir, "画面仕様書ディレクトリ"),
        ]
        
        for dir_path, description in required_dirs:
            abs_path = self.get_absolute_path(dir_path)
            if not abs_path.exists():
                errors.append(f"{description}が存在しません: {abs_path}")
        
        # 設定値の妥当性チェック
        if self.database.min_overview_length < 10:
            errors.append("データベース概要の最小文字数は10文字以上である必要があります")
        
        if self.database.min_notes_count < 1:
            errors.append("データベース特記事項の最小項目数は1項目以上である必要があります")
        
        if self.logging.level not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
            errors.append(f"無効なログレベル: {self.logging.level}")
        
        if errors:
            for error in errors:
                print(f"設定エラー: {error}")
            return False
        
        return True
    
    def __str__(self) -> str:
        """設定の文字列表現"""
        return f"""設計統合ツール設定:
  プロジェクトルート: {self.project_root}
  データベース設定:
    YAMLディレクトリ: {self.database.yaml_dir}
    DDLディレクトリ: {self.database.ddl_dir}
    テーブル定義書ディレクトリ: {self.database.tables_dir}
  API設定:
    仕様書ディレクトリ: {self.api.specs_dir}
  画面設計設定:
    仕様書ディレクトリ: {self.screen.specs_dir}
  統合設定:
    出力ディレクトリ: {self.integration.output_dir}
  ログ設定:
    レベル: {self.logging.level}"""
