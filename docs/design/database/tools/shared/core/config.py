"""
統合設定管理システム
両ツール（table_generator, database_consistency_checker）の設定を統合管理

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class LogLevel(Enum):
    """ログレベル定義"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ReportFormat(Enum):
    """レポート形式定義"""
    CONSOLE = "console"
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"


class CheckType(Enum):
    """チェック種別定義"""
    TABLE_EXISTENCE = "table_existence"
    COLUMN_CONSISTENCY = "column_consistency"
    FOREIGN_KEY_CONSISTENCY = "foreign_key_consistency"
    DATA_TYPE_CONSISTENCY = "data_type_consistency"
    YAML_FORMAT_CONSISTENCY = "yaml_format_consistency"
    CONSTRAINT_CONSISTENCY = "constraint_consistency"
    ORPHANED_FILES = "orphaned_files"
    NAMING_CONVENTION = "naming_convention"
    MULTITENANT_COMPLIANCE = "multitenant_compliance"


@dataclass
class DatabaseToolsConfig:
    """統合設定管理クラス - 両ツールの設定を統合"""
    
    # 基本設定
    base_dir: Path = field(default_factory=lambda: Path.cwd())
    encoding: str = "utf-8"
    line_ending: str = "\n"
    backup_enabled: bool = True
    log_level: LogLevel = LogLevel.INFO
    
    # ディレクトリ設定
    tools_dir: Path = field(init=False)
    table_details_dir: Path = field(init=False)
    ddl_dir: Path = field(init=False)
    tables_dir: Path = field(init=False)
    data_dir: Path = field(init=False)
    reports_dir: Path = field(init=False)
    backup_dir: Path = field(init=False)
    
    # テーブル生成ツール設定
    default_sample_count: int = 10
    max_sample_count: int = 10000
    default_seed: int = 12345
    faker_locale: str = "ja_JP"
    faker_seed: Optional[int] = None
    batch_insert_size: int = 1000
    ddl_template_dir: str = "templates/ddl"
    output_encoding: str = "utf-8"
    
    # データベース設定
    default_charset: str = "utf8mb4"
    default_collation: str = "utf8mb4_unicode_ci"
    
    # 業務固有設定
    company_domain: str = "company.com"
    default_department_prefix: str = "DEPT_"
    default_employee_prefix: str = "EMP"
    default_skill_prefix: str = "SKL_"
    
    # データ生成ルール
    skill_levels: List[int] = field(default_factory=lambda: [1, 2, 3, 4])
    skill_level_weights: List[int] = field(default_factory=lambda: [10, 30, 40, 20])
    department_distribution: Dict[str, int] = field(default_factory=lambda: {
        'DEPT_DEV': 40,    # 開発部40%
        'DEPT_SYS': 20,    # システム部20%
        'DEPT_BIZ': 30,    # 業務部30%
        'DEPT_MGT': 10     # 管理部10%
    })
    
    # 整合性チェックツール設定
    report_formats: List[ReportFormat] = field(default_factory=lambda: [
        ReportFormat.CONSOLE, ReportFormat.MARKDOWN
    ])
    keep_reports: int = 30
    max_reports: int = 100
    check_types: List[CheckType] = field(default_factory=lambda: [
        CheckType.TABLE_EXISTENCE,
        CheckType.COLUMN_CONSISTENCY,
        CheckType.FOREIGN_KEY_CONSISTENCY,
        CheckType.DATA_TYPE_CONSISTENCY,
        CheckType.YAML_FORMAT_CONSISTENCY,
        CheckType.CONSTRAINT_CONSISTENCY
    ])
    auto_fix_enabled: bool = False
    
    # 新機能設定
    parallel_processing: bool = True
    max_workers: int = 4
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1時間
    
    def __post_init__(self):
        """初期化後の設定"""
        # 実行時のディレクトリを考慮してパスを設定
        if self.base_dir.name == "tools" or (self.base_dir / "tools").exists():
            # toolsディレクトリから実行されている場合、またはdatabase/ディレクトリの場合
            if self.base_dir.name == "tools":
                db_dir = self.base_dir.parent
                self.tools_dir = self.base_dir
            else:
                # database/ディレクトリの場合
                db_dir = self.base_dir
                self.tools_dir = self.base_dir / "tools"
            
            self.table_details_dir = db_dir / "table-details"
            self.ddl_dir = db_dir / "ddl"
            self.tables_dir = db_dir / "tables"
            self.data_dir = db_dir / "data"
            self.reports_dir = db_dir / "reports"
            self.backup_dir = db_dir / "backups"
        else:
            # プロジェクトルートから実行されている場合
            self.tools_dir = self.base_dir / "docs" / "design" / "database" / "tools"
            self.table_details_dir = self.base_dir / "docs" / "design" / "database" / "table-details"
            self.ddl_dir = self.base_dir / "docs" / "design" / "database" / "ddl"
            self.tables_dir = self.base_dir / "docs" / "design" / "database" / "tables"
            self.data_dir = self.base_dir / "docs" / "design" / "database" / "data"
            self.reports_dir = self.base_dir / "docs" / "design" / "database" / "reports"
            self.backup_dir = self.base_dir / "docs" / "design" / "database" / "backups"
        
        # ディレクトリ作成
        self._ensure_directories()
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        directories = [
            self.table_details_dir,
            self.ddl_dir,
            self.tables_dir,
            self.data_dir,
            self.reports_dir,
            self.backup_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def from_env(cls) -> 'DatabaseToolsConfig':
        """環境変数から設定を読み込み"""
        config = cls()
        
        # 環境変数の読み込み
        if base_dir := os.getenv('DB_TOOLS_BASE_DIR'):
            config.base_dir = Path(base_dir)
        
        if log_level := os.getenv('DB_TOOLS_LOG_LEVEL'):
            try:
                config.log_level = LogLevel(log_level.upper())
            except ValueError:
                pass
        
        if sample_count := os.getenv('DB_TOOLS_SAMPLE_COUNT'):
            try:
                config.default_sample_count = int(sample_count)
            except ValueError:
                pass
        
        if backup_enabled := os.getenv('DB_TOOLS_BACKUP_ENABLED'):
            config.backup_enabled = backup_enabled.lower() in ('true', '1', 'yes')
        
        # table_generator固有の環境変数
        if seed := os.getenv('TABLE_GEN_SEED'):
            try:
                config.default_seed = int(seed)
            except ValueError:
                pass
        
        if faker_locale := os.getenv('TABLE_GEN_FAKER_LOCALE'):
            config.faker_locale = faker_locale
        
        if company_domain := os.getenv('TABLE_GEN_COMPANY_DOMAIN'):
            config.company_domain = company_domain
        
        return config
    
    def get_table_detail_path(self, table_name: str) -> Path:
        """テーブル詳細定義ファイルのパスを取得"""
        return self.table_details_dir / f"{table_name}_details.yaml"
    
    def get_ddl_path(self, table_name: str) -> Path:
        """DDLファイルのパスを取得"""
        return self.ddl_dir / f"{table_name}.sql"
    
    def get_table_definition_path(self, table_name: str, logical_name: str) -> Path:
        """テーブル定義書のパスを取得"""
        return self.tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
    
    def get_sample_data_path(self, table_name: str) -> Path:
        """サンプルデータファイルのパスを取得"""
        return self.data_dir / f"{table_name}_sample_data.sql"
    
    def get_table_list_file(self) -> Path:
        """テーブル一覧ファイルのパスを取得"""
        # データベース設計ディレクトリのテーブル一覧.mdファイル
        db_design_dir = self.base_dir / "docs" / "design" / "database" if self.base_dir.name != "tools" else self.base_dir.parent
        return db_design_dir / "テーブル一覧.md"
    
    def get_details_dir(self) -> Path:
        """テーブル詳細定義ディレクトリのパスを取得"""
        return self.table_details_dir
    
    def get_tables_dir(self) -> Path:
        """テーブル定義書ディレクトリのパスを取得"""
        return self.tables_dir
    
    def get_ddl_dir(self) -> Path:
        """DDLディレクトリのパスを取得"""
        return self.ddl_dir
    
    def get_backup_path(self, original_path: Path) -> Path:
        """バックアップファイルのパスを取得"""
        timestamp = self._get_timestamp()
        backup_name = f"{original_path.stem}.backup.{timestamp}{original_path.suffix}"
        return self.backup_dir / backup_name
    
    def _get_timestamp(self) -> str:
        """タイムスタンプ文字列を取得"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_timestamp(self) -> str:
        """タイムスタンプ文字列を取得（パブリックメソッド）"""
        return self._get_timestamp()
    
    def to_dict(self) -> Dict[str, Any]:
        """設定を辞書形式で取得"""
        return {
            'base_dir': str(self.base_dir),
            'encoding': self.encoding,
            'line_ending': repr(self.line_ending),
            'backup_enabled': self.backup_enabled,
            'log_level': self.log_level.value,
            'default_sample_count': self.default_sample_count,
            'faker_locale': self.faker_locale,
            'batch_insert_size': self.batch_insert_size,
            'report_formats': [fmt.value for fmt in self.report_formats],
            'keep_reports': self.keep_reports,
            'max_reports': self.max_reports,
            'check_types': [ct.value for ct in self.check_types],
            'auto_fix_enabled': self.auto_fix_enabled,
            'parallel_processing': self.parallel_processing,
            'max_workers': self.max_workers,
            'cache_enabled': self.cache_enabled,
            'cache_ttl': self.cache_ttl
        }


# グローバル設定インスタンス
_config_instance: Optional[DatabaseToolsConfig] = None


def get_config() -> DatabaseToolsConfig:
    """グローバル設定インスタンスを取得"""
    global _config_instance
    if _config_instance is None:
        _config_instance = DatabaseToolsConfig.from_env()
    return _config_instance


def set_config(config: DatabaseToolsConfig):
    """グローバル設定インスタンスを設定"""
    global _config_instance
    _config_instance = config


def reset_config():
    """グローバル設定インスタンスをリセット"""
    global _config_instance
    _config_instance = None
