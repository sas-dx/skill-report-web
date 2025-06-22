"""
データベース整合性チェックツール - 設定管理
"""
from pathlib import Path
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, field


@dataclass
class CheckConfig:
    """チェック実行設定"""
    suggest_fixes: bool = False
    fix_types: str = "all"
    auto_apply: bool = False
    output_fixes: Optional[str] = None
    verbose: bool = False
    target_tables: Optional[List[str]] = None
    excluded_tables: Optional[List[str]] = field(default_factory=list)
    base_dir: Optional[str] = None
    output_format: str = "console"
    output_file: Optional[str] = None
    report_dir: str = "reports"
    keep_reports: int = 30
    max_reports: int = 100
    report_prefix: Optional[str] = None
    auto_cleanup: bool = True


class Config:
    """統合設定クラス"""
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        設定初期化
        
        Args:
            base_dir: ベースディレクトリ（指定しない場合は自動検出）
        """
        if base_dir:
            self.base_dir = Path(base_dir).resolve()
        else:
            self.base_dir = self._find_base_dir()
        
        # 各種ディレクトリパス
        self.tools_dir = self.base_dir / "docs" / "design" / "database" / "tools"
        self.yaml_dir = self.base_dir / "docs" / "design" / "database" / "table-details"
        self.ddl_dir = self.base_dir / "docs" / "design" / "database" / "ddl"
        self.tables_dir = self.base_dir / "docs" / "design" / "database" / "tables"
        self.data_dir = self.base_dir / "docs" / "design" / "database" / "data"
        self.reports_dir = self.base_dir / "docs" / "design" / "database" / "reports"
        
        # デフォルト除外テーブル（テンプレート・無効なテーブル名）
        self.default_excluded_tables = [
            "MST_TEMPLATE",  # テンプレートファイル
            "------------",  # 区切り線
            "MST", "TRN", "SYS", "HIS", "WRK"  # プレフィックスのみ
        ]
        
    def _find_base_dir(self) -> Path:
        """プロジェクトのベースディレクトリを自動検出"""
        current = Path.cwd()
        
        # 上位ディレクトリを探索
        while current != current.parent:
            # プロジェクトルートの特徴的なファイル/ディレクトリを確認
            if (current / "package.json").exists() or \
               (current / "docs" / "design" / "database").exists():
                return current
            current = current.parent
        
        # 見つからない場合は現在のディレクトリ
        return Path.cwd()
    
    def get_yaml_path(self, table_name: str) -> Path:
        """YAMLファイルパスを取得"""
        return self.yaml_dir / f"{table_name}_details.yaml"
    
    def get_ddl_path(self, table_name: str) -> Path:
        """DDLファイルパスを取得"""
        return self.ddl_dir / f"{table_name}.sql"
    
    def get_definition_path(self, table_name: str) -> Path:
        """定義書ファイルパスを取得"""
        # 定義書ファイル名のパターンを考慮
        for file in self.tables_dir.glob(f"テーブル定義書_{table_name}_*.md"):
            return file
        return self.tables_dir / f"テーブル定義書_{table_name}.md"
    
    def get_sample_data_path(self, table_name: str) -> Path:
        """サンプルデータファイルパスを取得"""
        return self.data_dir / f"{table_name}_sample.sql"


def create_check_config(**kwargs) -> CheckConfig:
    """
    チェック設定を作成
    
    Args:
        **kwargs: 設定パラメータ
        
    Returns:
        CheckConfig: チェック設定オブジェクト
    """
    return CheckConfig(**kwargs)
