#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
データベース整合性チェックツール - 設定管理（統合設定への移行）

統合設定システムを使用するためのラッパークラス。
後方互換性を保ちながら、統合設定に移行します。

対応要求仕様ID: PLT.2-TOOL.2
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# 統合設定をインポート
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
from core.config import get_config as get_unified_config, DatabaseToolsConfig, ReportFormat, CheckType

# 既存のモデルをインポート（後方互換性のため）
from .models import CheckConfig, FixType


class Config:
    """設定管理クラス（統合設定へのラッパー）
    
    既存のdatabase_consistency_checkerコードとの互換性を保ちながら、
    統合設定システムを使用します。
    """
    
    def __init__(self, base_dir: str = ""):
        """設定初期化
        
        Args:
            base_dir: ベースディレクトリ（デフォルトは現在のディレクトリの親）
        """
        self._unified_config = get_unified_config()
        
        # ベースディレクトリが指定された場合は更新
        if base_dir:
            self._unified_config.base_dir = Path(base_dir)
            # ディレクトリパスを再計算
            self._unified_config.__post_init__()
        
        # 後方互換性のためのプロパティ設定
        self.base_dir = self._unified_config.base_dir
        self.table_list_file = self._unified_config.base_dir / "テーブル一覧.md"
        self.entity_relationships_file = self._unified_config.base_dir / "entity_relationships.yaml"
        self.entity_diagram_file = self._unified_config.base_dir / "エンティティ関連図.md"
        self.table_details_dir = self._unified_config.table_details_dir
        self.tables_dir = self._unified_config.tables_dir
        self.ddl_dir = self._unified_config.ddl_dir
        self.data_dir = self._unified_config.data_dir
        self.output_dir = self._unified_config.reports_dir
        self.fixes_dir = self._unified_config.base_dir / "fixes"
    
    def validate_paths(self) -> List[str]:
        """必要なパスの存在確認
        
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
    """修正タイプ文字列をFixTypeリストに変換
    
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
    output_file: Optional[str] = None,
    report_dir: str = "reports",
    keep_reports: int = 30,
    max_reports: int = 100,
    report_prefix: Optional[str] = None,
    auto_cleanup: bool = True
) -> CheckConfig:
    """チェック設定を作成
    
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
        report_dir: レポートディレクトリ
        keep_reports: レポート保持日数
        max_reports: 最大レポート数
        report_prefix: レポートファイルプレフィックス
        auto_cleanup: 自動クリーンアップ
        
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
        output_file=output_file,
        report_dir=report_dir,
        keep_reports=keep_reports,
        max_reports=max_reports,
        report_prefix=report_prefix,
        auto_cleanup=auto_cleanup
    )
