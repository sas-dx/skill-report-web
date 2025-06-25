"""
統合設定管理
全ツールで使用する共通設定機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-25
実装者: AI駆動開発チーム
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import yaml
import json


@dataclass
class DatabaseConfig:
    """データベース設定"""
    host: str = "localhost"
    port: int = 5432
    database: str = "skill_report"
    username: str = "postgres"
    password: str = ""
    schema: str = "public"
    connection_timeout: int = 30
    query_timeout: int = 300


@dataclass
class PathConfig:
    """パス設定"""
    base_dir: Path = field(default_factory=lambda: Path.cwd())
    table_details_dir: Path = field(default_factory=Path)
    ddl_dir: Path = field(default_factory=Path)
    tables_dir: Path = field(default_factory=Path)
    reports_dir: Path = field(default_factory=Path)
    backup_dir: Path = field(default_factory=Path)
    temp_dir: Path = field(default_factory=Path)
    
    def __post_init__(self):
        """パスの初期化"""
        if not self.table_details_dir:
            self.table_details_dir = self.base_dir / "docs/design/database/table-details"
        if not self.ddl_dir:
            self.ddl_dir = self.base_dir / "docs/design/database/ddl"
        if not self.tables_dir:
            self.tables_dir = self.base_dir / "docs/design/database/tables"
        if not self.reports_dir:
            self.reports_dir = self.base_dir / "docs/design/database/reports"
        if not self.backup_dir:
            self.backup_dir = self.base_dir / "docs/design/database/backups"
        if not self.temp_dir:
            self.temp_dir = self.base_dir / "temp"


@dataclass
class LogConfig:
    """ログ設定"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    console_enabled: bool = True
    log_dir: Path = field(default_factory=lambda: Path("logs"))
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    encoding: str = "utf-8"


@dataclass
class ToolConfig:
    """ツール設定"""
    encoding: str = "utf-8"
    backup_enabled: bool = True
    auto_cleanup: bool = True
    keep_reports: int = 30
    max_reports: int = 100
    parallel_processing: bool = False
    max_workers: int = 4
    timeout: int = 300
    retry_count: int = 3
    retry_delay: float = 1.0


@dataclass
class ValidationConfig:
    """検証設定"""
    strict_mode: bool = False
    required_sections: List[str] = field(default_factory=lambda: [
        "revision_history", "overview", "notes", "business_rules"
    ])
    min_overview_length: int = 50
    min_notes_count: int = 3
    min_rules_count: int = 3
    allow_empty_tables: bool = False
    validate_foreign_keys: bool = True
    validate_data_types: bool = True


class Config:
    """統合設定クラス"""
    
    def __init__(self, base_dir: Optional[str] = None, config_file: Optional[str] = None):
        """設定初期化"""
        self.base_dir = Path(base_dir) if base_dir else self._detect_base_dir()
        
        # デフォルト設定
        self.database = DatabaseConfig()
        self.paths = PathConfig(base_dir=self.base_dir)
        self.logging = LogConfig()
        self.tool = ToolConfig()
        self.validation = ValidationConfig()
        
        # 設定ファイルから読み込み
        if config_file:
            self.load_from_file(config_file)
        else:
            self._load_default_config()
        
        # 環境変数から上書き
        self._load_from_env()
        
        # パスの確保
        self._ensure_directories()
    
    def _detect_base_dir(self) -> Path:
        """ベースディレクトリの自動検出"""
        current = Path.cwd()
        
        # skill-report-webディレクトリを探す
        for parent in [current] + list(current.parents):
            if (parent / "docs/design/database").exists():
                return parent
        
        # 見つからない場合は現在のディレクトリ
        return current
    
    def _load_default_config(self):
        """デフォルト設定ファイルの読み込み"""
        config_files = [
            self.base_dir / "config/database_tools.yaml",
            self.base_dir / "config/database_tools.yml",
            self.base_dir / ".database_tools.yaml",
            Path.home() / ".database_tools.yaml"
        ]
        
        for config_file in config_files:
            if config_file.exists():
                try:
                    self.load_from_file(config_file)
                    break
                except Exception:
                    continue
    
    def load_from_file(self, config_file: Path):
        """設定ファイルから読み込み"""
        config_file = Path(config_file)
        
        if not config_file.exists():
            raise FileNotFoundError(f"設定ファイルが見つかりません: {config_file}")
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.suffix.lower() in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                elif config_file.suffix.lower() == '.json':
                    data = json.load(f)
                else:
                    raise ValueError(f"サポートされていない設定ファイル形式: {config_file.suffix}")
            
            self._update_from_dict(data)
            
        except Exception as e:
            raise RuntimeError(f"設定ファイル読み込みエラー: {e}")
    
    def _update_from_dict(self, data: Dict[str, Any]):
        """辞書から設定を更新"""
        if 'database' in data:
            self._update_dataclass(self.database, data['database'])
        
        if 'paths' in data:
            paths_data = data['paths']
            # パスをPathオブジェクトに変換
            for key, value in paths_data.items():
                if hasattr(self.paths, key) and value:
                    setattr(self.paths, key, Path(value))
        
        if 'logging' in data:
            self._update_dataclass(self.logging, data['logging'])
        
        if 'tool' in data:
            self._update_dataclass(self.tool, data['tool'])
        
        if 'validation' in data:
            self._update_dataclass(self.validation, data['validation'])
    
    def _update_dataclass(self, obj, data: Dict[str, Any]):
        """データクラスを辞書で更新"""
        for key, value in data.items():
            if hasattr(obj, key):
                setattr(obj, key, value)
    
    def _load_from_env(self):
        """環境変数から設定を読み込み"""
        # データベース設定
        if os.getenv('DB_HOST'):
            self.database.host = os.getenv('DB_HOST')
        if os.getenv('DB_PORT'):
            self.database.port = int(os.getenv('DB_PORT'))
        if os.getenv('DB_NAME'):
            self.database.database = os.getenv('DB_NAME')
        if os.getenv('DB_USER'):
            self.database.username = os.getenv('DB_USER')
        if os.getenv('DB_PASSWORD'):
            self.database.password = os.getenv('DB_PASSWORD')
        
        # ログレベル
        if os.getenv('LOG_LEVEL'):
            self.logging.level = os.getenv('LOG_LEVEL')
        
        # ツール設定
        if os.getenv('TOOL_ENCODING'):
            self.tool.encoding = os.getenv('TOOL_ENCODING')
        if os.getenv('BACKUP_ENABLED'):
            self.tool.backup_enabled = os.getenv('BACKUP_ENABLED').lower() == 'true'
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        directories = [
            self.paths.reports_dir,
            self.paths.backup_dir,
            self.paths.temp_dir,
            self.logging.log_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_backup_path(self, original_file: Path) -> Path:
        """バックアップファイルパスを生成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{original_file.stem}.backup.{timestamp}{original_file.suffix}"
        return self.paths.backup_dir / backup_name
    
    def get_report_path(self, report_type: str, extension: str = "md") -> Path:
        """レポートファイルパスを生成"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"{report_type}_{timestamp}.{extension}"
        return self.paths.reports_dir / report_name
    
    def to_dict(self) -> Dict[str, Any]:
        """設定を辞書形式で取得"""
        return {
            'database': {
                'host': self.database.host,
                'port': self.database.port,
                'database': self.database.database,
                'username': self.database.username,
                'schema': self.database.schema,
                'connection_timeout': self.database.connection_timeout,
                'query_timeout': self.database.query_timeout
            },
            'paths': {
                'base_dir': str(self.paths.base_dir),
                'table_details_dir': str(self.paths.table_details_dir),
                'ddl_dir': str(self.paths.ddl_dir),
                'tables_dir': str(self.paths.tables_dir),
                'reports_dir': str(self.paths.reports_dir),
                'backup_dir': str(self.paths.backup_dir),
                'temp_dir': str(self.paths.temp_dir)
            },
            'logging': {
                'level': self.logging.level,
                'format': self.logging.format,
                'file_enabled': self.logging.file_enabled,
                'console_enabled': self.logging.console_enabled,
                'log_dir': str(self.logging.log_dir),
                'max_file_size': self.logging.max_file_size,
                'backup_count': self.logging.backup_count,
                'encoding': self.logging.encoding
            },
            'tool': {
                'encoding': self.tool.encoding,
                'backup_enabled': self.tool.backup_enabled,
                'auto_cleanup': self.tool.auto_cleanup,
                'keep_reports': self.tool.keep_reports,
                'max_reports': self.tool.max_reports,
                'parallel_processing': self.tool.parallel_processing,
                'max_workers': self.tool.max_workers,
                'timeout': self.tool.timeout,
                'retry_count': self.tool.retry_count,
                'retry_delay': self.tool.retry_delay
            },
            'validation': {
                'strict_mode': self.validation.strict_mode,
                'required_sections': self.validation.required_sections,
                'min_overview_length': self.validation.min_overview_length,
                'min_notes_count': self.validation.min_notes_count,
                'min_rules_count': self.validation.min_rules_count,
                'allow_empty_tables': self.validation.allow_empty_tables,
                'validate_foreign_keys': self.validation.validate_foreign_keys,
                'validate_data_types': self.validation.validate_data_types
            }
        }
    
    def save_to_file(self, config_file: Path):
        """設定をファイルに保存"""
        config_file = Path(config_file)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        data = self.to_dict()
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                if config_file.suffix.lower() in ['.yaml', '.yml']:
                    yaml.dump(data, f, default_flow_style=False, allow_unicode=True, indent=2)
                elif config_file.suffix.lower() == '.json':
                    json.dump(data, f, ensure_ascii=False, indent=2)
                else:
                    raise ValueError(f"サポートされていない設定ファイル形式: {config_file.suffix}")
        
        except Exception as e:
            raise RuntimeError(f"設定ファイル保存エラー: {e}")


# グローバルインスタンス
_config_instance: Optional[Config] = None


def get_config(base_dir: Optional[str] = None, config_file: Optional[str] = None) -> Config:
    """グローバル設定インスタンスを取得"""
    global _config_instance
    if _config_instance is None or base_dir or config_file:
        _config_instance = Config(base_dir, config_file)
    return _config_instance


def create_check_config(**kwargs) -> 'CheckConfig':
    """チェック設定を作成"""
    from .models import CheckConfig
    
    config = get_config()
    
    return CheckConfig(
        enabled_checks=kwargs.get('enabled_checks', []),
        disabled_checks=kwargs.get('disabled_checks', []),
        check_parameters=kwargs.get('check_parameters', {}),
        output_format=kwargs.get('output_format', 'console'),
        verbose=kwargs.get('verbose', False),
        fail_fast=kwargs.get('fail_fast', False)
    )
