"""
データベース整合性チェックツール - 設定管理
"""
import os
from pathlib import Path
from typing import List, Optional
from .models import CheckConfig, FixType


class Config:
    """設定管理クラス"""
    
    def __init__(self, base_dir: str = ""):
        """
        設定初期化
        
        Args:
            base_dir: ベースディレクトリ（デフォルトは現在のディレクトリの親）
        """
        if not base_dir:
            # tools/database_consistency_checker から ../../ に移動
            current_dir = Path(__file__).parent.parent.parent.parent
            self.base_dir = current_dir.resolve()
        else:
            self.base_dir = Path(base_dir).resolve()
        
        # 各ディレクトリパス
        self.table_list_file = self.base_dir / "テーブル一覧.md"
        self.entity_relationships_file = self.base_dir / "entity_relationships.yaml"
        self.entity_diagram_file = self.base_dir / "エンティティ関連図.md"
        self.table_details_dir = self.base_dir / "table-details"
        self.tables_dir = self.base_dir / "tables"
        self.ddl_dir = self.base_dir / "ddl"
        self.data_dir = self.base_dir / "data"
        
        # 出力ディレクトリ
        self.output_dir = self.base_dir / "consistency_reports"
        self.fixes_dir = self.base_dir / "fixes"
    
    def validate_paths(self) -> List[str]:
        """
        必要なパスの存在確認
        
        Returns:
            存在しないパスのリスト
        """
        missing_paths = []
        
        required_files = [
            self.table_list_file,
            self.entity_relationships_file
        ]
        
        required_dirs = [
            self.table_details_dir,
            self.ddl_dir
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                missing_paths.append(str(file_path))
        
        for dir_path in required_dirs:
            if not dir_path.exists():
                missing_paths.append(str(dir_path))
        
        return missing_paths
    
    def create_output_dirs(self):
        """出力ディレクトリの作成"""
        self.output_dir.mkdir(exist_ok=True)
        self.fixes_dir.mkdir(exist_ok=True)
    
    def get_table_detail_files(self) -> List[Path]:
        """テーブル詳細YAMLファイルのリストを取得"""
        if not self.table_details_dir.exists():
            return []
        
        return list(self.table_details_dir.glob("*.yaml"))
    
    def get_ddl_files(self) -> List[Path]:
        """DDLファイルのリストを取得"""
        if not self.ddl_dir.exists():
            return []
        
        return list(self.ddl_dir.glob("*.sql"))
    
    def get_data_files(self) -> List[Path]:
        """データファイルのリストを取得"""
        if not self.data_dir.exists():
            return []
        
        return list(self.data_dir.glob("*_sample_data.sql"))
    
    def get_table_definition_files(self) -> List[Path]:
        """テーブル定義書ファイルのリストを取得"""
        if not self.tables_dir.exists():
            return []
        
        return list(self.tables_dir.glob("テーブル定義書_*.md"))


def parse_fix_types(fix_types_str: str) -> List[FixType]:
    """
    修正タイプ文字列をFixTypeリストに変換
    
    Args:
        fix_types_str: カンマ区切りの修正タイプ文字列
        
    Returns:
        FixTypeのリスト
    """
    if not fix_types_str or fix_types_str.lower() == "all":
        return [FixType.ALL]
    
    type_map = {
        "ddl": FixType.DDL,
        "yaml": FixType.YAML,
        "insert": FixType.INSERT,
        "all": FixType.ALL
    }
    
    types = []
    for type_str in fix_types_str.split(","):
        type_str = type_str.strip().lower()
        if type_str in type_map:
            types.append(type_map[type_str])
    
    return types if types else [FixType.ALL]


def create_check_config(
    suggest_fixes: bool = False,
    fix_types: str = "all",
    auto_apply: bool = False,
    output_fixes: Optional[str] = None,
    verbose: bool = False,
    target_tables: Optional[List[str]] = None,
    base_dir: str = "",
    output_format: str = "console",
    output_file: Optional[str] = None
) -> CheckConfig:
    """
    チェック設定を作成
    
    Args:
        suggest_fixes: 修正提案を生成するか
        fix_types: 修正タイプ（カンマ区切り）
        auto_apply: 自動適用するか
        output_fixes: 修正提案出力先
        verbose: 詳細ログ出力
        target_tables: 対象テーブルリスト
        base_dir: ベースディレクトリ
        output_format: 出力形式
        output_file: 出力ファイル
        
    Returns:
        CheckConfig
    """
    return CheckConfig(
        suggest_fixes=suggest_fixes,
        fix_types=parse_fix_types(fix_types),
        auto_apply=auto_apply,
        output_fixes=output_fixes,
        verbose=verbose,
        target_tables=target_tables or [],
        base_dir=base_dir,
        output_format=output_format,
        output_file=output_file
    )
