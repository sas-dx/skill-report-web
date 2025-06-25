#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
パス解決ヘルパー

モジュールパスの解決と設定を行うユーティリティ
"""
import sys
import os
from pathlib import Path
from typing import Optional


class PathResolver:
    """パス解決ユーティリティクラス"""
    
    @staticmethod
    def setup_module_path() -> Path:
        """
        モジュールパスを設定
        
        Returns:
            Path: tools ディレクトリのパス
        """
        # 現在のファイルから tools ディレクトリを特定
        current_file = Path(__file__)
        tools_dir = current_file.parent.parent
        
        # tools ディレクトリをパスに追加（最優先）
        if str(tools_dir) not in sys.path:
            sys.path.insert(0, str(tools_dir))
        
        # プロジェクトルートもパスに追加
        project_root = PathResolver.get_project_root()
        if project_root and str(project_root) not in sys.path:
            sys.path.insert(1, str(project_root))
        
        return tools_dir
    
    @staticmethod
    def get_project_root() -> Optional[Path]:
        """
        プロジェクトルートディレクトリを取得
        
        Returns:
            Optional[Path]: プロジェクトルートのパス（見つからない場合はNone）
        """
        # 環境変数から取得を試みる
        if env_root := os.getenv('SKILL_REPORT_PROJECT_ROOT'):
            return Path(env_root)
        
        # 現在のディレクトリから遡って検索
        current = Path(__file__).parent
        while current != current.parent:
            # package.json または .git の存在でプロジェクトルートを判定
            if (current / 'package.json').exists() or (current / '.git').exists():
                return current
            current = current.parent
        
        return None
    
    @staticmethod
    def get_database_dir() -> Path:
        """
        データベース設計ディレクトリを取得
        
        Returns:
            Path: データベース設計ディレクトリのパス
        """
        tools_dir = Path(__file__).parent.parent
        return tools_dir.parent  # docs/design/database
    
    @staticmethod
    def get_yaml_dir() -> Path:
        """
        YAML定義ファイルディレクトリを取得
        
        Returns:
            Path: YAML定義ファイルディレクトリのパス
        """
        database_dir = PathResolver.get_database_dir()
        return database_dir / "tables"
    
    @staticmethod
    def get_ddl_dir() -> Path:
        """
        DDLファイルディレクトリを取得
        
        Returns:
            Path: DDLファイルディレクトリのパス
        """
        database_dir = PathResolver.get_database_dir()
        return database_dir / "ddl"
    
    @staticmethod
    def get_table_details_dir() -> Path:
        """
        テーブル定義書ディレクトリを取得
        
        Returns:
            Path: テーブル定義書ディレクトリのパス
        """
        database_dir = PathResolver.get_database_dir()
        return database_dir / "table-details"
    
    @staticmethod
    def get_tables_dir() -> Path:
        """
        テーブル定義書ディレクトリを取得（tablesディレクトリ）
        
        Returns:
            Path: テーブル定義書ディレクトリのパス
        """
        database_dir = PathResolver.get_database_dir()
        return database_dir / "tables"
    
    @staticmethod
    def get_data_dir() -> Path:
        """
        サンプルデータディレクトリを取得
        
        Returns:
            Path: サンプルデータディレクトリのパス
        """
        database_dir = PathResolver.get_database_dir()
        return database_dir / "data"


def setup_import_paths():
    """
    インポートパスを設定する便利関数
    
    この関数を各モジュールの先頭で呼び出すことで、
    適切なインポートパスが設定される
    """
    resolver = PathResolver()
    return resolver.setup_module_path()
