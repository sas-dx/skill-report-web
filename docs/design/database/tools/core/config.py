"""
統一設定管理システム

全ツールで共通の設定を一元管理
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class DatabaseConfig:
    """データベース関連設定"""
    yaml_dir: str = "../table-details"
    ddl_dir: str = "../ddl"
    tables_dir: str = "../tables"
    backup_dir: str = "../backups"


@dataclass
class ValidationConfig:
    """バリデーション設定"""
    required_sections: list = None
    min_overview_length: int = 50
    min_notes_count: int = 3
    min_rules_count: int = 3
    
    def __post_init__(self):
        if self.required_sections is None:
            self.required_sections = [
                'revision_history', 'overview', 'notes', 'rules'
            ]


@dataclass
class LoggingConfig:
    """ログ設定"""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    console_enabled: bool = True
    log_dir: str = "./logs"


@dataclass
class Config:
    """統一設定クラス"""
    database: DatabaseConfig
    validation: ValidationConfig
    logging: LoggingConfig
    
    def __init__(self, config_file: Optional[str] = None):
        """設定初期化"""
        self.database = DatabaseConfig()
        self.validation = ValidationConfig()
        self.logging = LoggingConfig()
        
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str) -> None:
        """設定ファイルから読み込み"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if 'database' in data:
                self.database = DatabaseConfig(**data['database'])
            if 'validation' in data:
                self.validation = ValidationConfig(**data['validation'])
            if 'logging' in data:
                self.logging = LoggingConfig(**data['logging'])
                
        except Exception as e:
            print(f"設定ファイル読み込みエラー: {e}")
    
    def save_to_file(self, config_file: str) -> None:
        """設定ファイルに保存"""
        try:
            data = {
                'database': asdict(self.database),
                'validation': asdict(self.validation),
                'logging': asdict(self.logging)
            }
            
            os.makedirs(os.path.dirname(config_file), exist_ok=True)
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"設定ファイル保存エラー: {e}")
    
    def get_absolute_path(self, relative_path: str) -> str:
        """相対パスを絶対パスに変換"""
        if os.path.isabs(relative_path):
            return relative_path
        
        # tools/ ディレクトリからの相対パス
        tools_dir = Path(__file__).parent.parent
        return str(tools_dir / relative_path)
    
    def get_yaml_dir(self) -> str:
        """YAML ディレクトリの絶対パス"""
        return self.get_absolute_path(self.database.yaml_dir)
    
    def get_ddl_dir(self) -> str:
        """DDL ディレクトリの絶対パス"""
        return self.get_absolute_path(self.database.ddl_dir)
    
    def get_tables_dir(self) -> str:
        """テーブル定義書ディレクトリの絶対パス"""
        return self.get_absolute_path(self.database.tables_dir)
    
    def get_backup_dir(self) -> str:
        """バックアップディレクトリの絶対パス"""
        return self.get_absolute_path(self.database.backup_dir)


# グローバル設定インスタンス
_config: Optional[Config] = None


def get_config(config_file: Optional[str] = None) -> Config:
    """設定インスタンスを取得"""
    global _config
    
    if _config is None:
        # デフォルト設定ファイルパス
        if config_file is None:
            config_file = os.path.join(
                os.path.dirname(__file__), 
                '..', 
                'config.json'
            )
        
        _config = Config(config_file)
    
    return _config


def reset_config() -> None:
    """設定をリセット（テスト用）"""
    global _config
    _config = None
