"""
統合ファイルシステムアダプター

全てのファイル操作を統一するアダプター
- YAML、DDL、Markdownファイルの読み書き
- ディレクトリ操作
- ファイル検索・フィルタリング
- バックアップ・復元機能
"""

import os
import shutil
import glob
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import logging

from ...core.exceptions import FileOperationError, ValidationError
from ...core.models import TableDefinition, FileMetadata
from ...parsers.yaml_parser import YamlParser
from ...parsers.ddl_parser import DDLParser
from ...parsers.markdown_parser import MarkdownParser

logger = logging.getLogger(__name__)


class UnifiedFileSystemAdapter:
    """統合ファイルシステムアダプター"""
    
    def __init__(self, base_path: str):
        """
        初期化
        
        Args:
            base_path: ベースディレクトリパス
        """
        self.base_path = Path(base_path)
        self.yaml_parser = YamlParser()
        self.ddl_parser = DDLParser()
        self.markdown_parser = MarkdownParser()
        
        # ディレクトリ構造の定義
        self.directories = {
            'table_details': self.base_path / 'table-details',
            'ddl': self.base_path / 'ddl',
            'tables': self.base_path / 'tables',
            'data': self.base_path / 'data',
            'backups': self.base_path / 'backups',
            'reports': self.base_path / 'reports'
        }
        
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """必要なディレクトリを作成"""
        for dir_path in self.directories.values():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    # ===== YAML操作 =====
    
    def read_yaml_definition(self, table_name: str) -> TableDefinition:
        """
        YAMLテーブル定義を読み込み
        
        Args:
            table_name: テーブル名
            
        Returns:
            TableDefinition: テーブル定義オブジェクト
            
        Raises:
            FileOperationError: ファイル読み込みエラー
        """
        try:
            yaml_path = self.directories['table_details'] / f"{table_name}_details.yaml"
            
            if not yaml_path.exists():
                raise FileOperationError(f"YAML定義ファイルが見つかりません: {yaml_path}")
            
            yaml_data = self.yaml_parser.parse_file(str(yaml_path))
            return TableDefinition.from_yaml_data(yaml_data)
            
        except Exception as e:
            logger.error(f"YAML定義読み込みエラー: {table_name}, {e}")
            raise FileOperationError(f"YAML定義読み込みに失敗しました: {e}")
    
    def write_yaml_definition(self, table_definition: TableDefinition) -> None:
        """
        YAMLテーブル定義を書き込み
        
        Args:
            table_definition: テーブル定義オブジェクト
            
        Raises:
            FileOperationError: ファイル書き込みエラー
        """
        try:
            yaml_path = self.directories['table_details'] / f"{table_definition.table_name}_details.yaml"
            yaml_data = table_definition.to_yaml_data()
            
            self.yaml_parser.write_file(str(yaml_path), yaml_data)
            logger.info(f"YAML定義を保存しました: {yaml_path}")
            
        except Exception as e:
            logger.error(f"YAML定義書き込みエラー: {table_definition.table_name}, {e}")
            raise FileOperationError(f"YAML定義書き込みに失敗しました: {e}")
    
    def list_yaml_definitions(self) -> List[str]:
        """
        全てのYAML定義ファイルのテーブル名を取得
        
        Returns:
            List[str]: テーブル名のリスト
        """
        try:
            yaml_files = glob.glob(str(self.directories['table_details'] / "*_details.yaml"))
            table_names = []
            
            for yaml_file in yaml_files:
                filename = Path(yaml_file).stem
                if filename.endswith('_details'):
                    table_name = filename[:-8]  # '_details'を除去
                    table_names.append(table_name)
            
            return sorted(table_names)
            
        except Exception as e:
            logger.error(f"YAML定義一覧取得エラー: {e}")
            raise FileOperationError(f"YAML定義一覧取得に失敗しました: {e}")
    
    # ===== DDL操作 =====
    
    def read_ddl_file(self, table_name: str) -> str:
        """
        DDLファイルを読み込み
        
        Args:
            table_name: テーブル名
            
        Returns:
            str: DDL内容
            
        Raises:
            FileOperationError: ファイル読み込みエラー
        """
        try:
            ddl_path = self.directories['ddl'] / f"{table_name}.sql"
            
            if not ddl_path.exists():
                raise FileOperationError(f"DDLファイルが見つかりません: {ddl_path}")
            
            return ddl_path.read_text(encoding='utf-8')
            
        except Exception as e:
            logger.error(f"DDLファイル読み込みエラー: {table_name}, {e}")
            raise FileOperationError(f"DDLファイル読み込みに失敗しました: {e}")
    
    def write_ddl_file(self, table_name: str, ddl_content: str) -> None:
        """
        DDLファイルを書き込み
        
        Args:
            table_name: テーブル名
            ddl_content: DDL内容
            
        Raises:
            FileOperationError: ファイル書き込みエラー
        """
        try:
            ddl_path = self.directories['ddl'] / f"{table_name}.sql"
            ddl_path.write_text(ddl_content, encoding='utf-8')
            logger.info(f"DDLファイルを保存しました: {ddl_path}")
            
        except Exception as e:
            logger.error(f"DDLファイル書き込みエラー: {table_name}, {e}")
            raise FileOperationError(f"DDLファイル書き込みに失敗しました: {e}")
    
    def list_ddl_files(self) -> List[str]:
        """
        全てのDDLファイルのテーブル名を取得
        
        Returns:
            List[str]: テーブル名のリスト
        """
        try:
            ddl_files = glob.glob(str(self.directories['ddl'] / "*.sql"))
            table_names = []
            
            for ddl_file in ddl_files:
                filename = Path(ddl_file).stem
                # テンプレートファイルを除外
                if not filename.startswith('---'):
                    table_names.append(filename)
            
            return sorted(table_names)
            
        except Exception as e:
            logger.error(f"DDLファイル一覧取得エラー: {e}")
            raise FileOperationError(f"DDLファイル一覧取得に失敗しました: {e}")
    
    # ===== Markdown操作 =====
    
    def read_markdown_definition(self, table_name: str) -> Dict[str, Any]:
        """
        Markdownテーブル定義を読み込み
        
        Args:
            table_name: テーブル名
            
        Returns:
            Dict[str, Any]: Markdown解析結果
            
        Raises:
            FileOperationError: ファイル読み込みエラー
        """
        try:
            # Markdownファイルを検索（論理名が含まれるため）
            markdown_files = glob.glob(str(self.directories['tables'] / f"テーブル定義書_{table_name}_*.md"))
            
            if not markdown_files:
                raise FileOperationError(f"Markdownファイルが見つかりません: {table_name}")
            
            markdown_path = markdown_files[0]  # 最初にマッチしたファイルを使用
            return self.markdown_parser.parse_file(markdown_path)
            
        except Exception as e:
            logger.error(f"Markdown定義読み込みエラー: {table_name}, {e}")
            raise FileOperationError(f"Markdown定義読み込みに失敗しました: {e}")
    
    def write_markdown_definition(self, table_definition: TableDefinition, content: str) -> None:
        """
        Markdownテーブル定義を書き込み
        
        Args:
            table_definition: テーブル定義オブジェクト
            content: Markdown内容
            
        Raises:
            FileOperationError: ファイル書き込みエラー
        """
        try:
            filename = f"テーブル定義書_{table_definition.table_name}_{table_definition.logical_name}.md"
            markdown_path = self.directories['tables'] / filename
            
            markdown_path.write_text(content, encoding='utf-8')
            logger.info(f"Markdown定義を保存しました: {markdown_path}")
            
        except Exception as e:
            logger.error(f"Markdown定義書き込みエラー: {table_definition.table_name}, {e}")
            raise FileOperationError(f"Markdown定義書き込みに失敗しました: {e}")
    
    def list_markdown_definitions(self) -> List[str]:
        """
        全てのMarkdown定義ファイルのテーブル名を取得
        
        Returns:
            List[str]: テーブル名のリスト
        """
        try:
            markdown_files = glob.glob(str(self.directories['tables'] / "テーブル定義書_*.md"))
            table_names = []
            
            for markdown_file in markdown_files:
                filename = Path(markdown_file).stem
                # ファイル名からテーブル名を抽出: テーブル定義書_{table_name}_{logical_name}
                parts = filename.split('_')
                if len(parts) >= 3 and parts[0] == 'テーブル定義書':
                    table_name = parts[1]
                    table_names.append(table_name)
            
            return sorted(list(set(table_names)))  # 重複除去
            
        except Exception as e:
            logger.error(f"Markdown定義一覧取得エラー: {e}")
            raise FileOperationError(f"Markdown定義一覧取得に失敗しました: {e}")
    
    # ===== サンプルデータ操作 =====
    
    def write_sample_data(self, table_name: str, sample_data: str) -> None:
        """
        サンプルデータファイルを書き込み
        
        Args:
            table_name: テーブル名
            sample_data: サンプルデータ内容
            
        Raises:
            FileOperationError: ファイル書き込みエラー
        """
        try:
            data_path = self.directories['data'] / f"{table_name}_sample_data.sql"
            data_path.write_text(sample_data, encoding='utf-8')
            logger.info(f"サンプルデータを保存しました: {data_path}")
            
        except Exception as e:
            logger.error(f"サンプルデータ書き込みエラー: {table_name}, {e}")
            raise FileOperationError(f"サンプルデータ書き込みに失敗しました: {e}")
    
    # ===== ファイル検索・フィルタリング =====
    
    def find_files_by_pattern(self, pattern: str, directory: str = None) -> List[Path]:
        """
        パターンマッチングでファイルを検索
        
        Args:
            pattern: 検索パターン
            directory: 検索対象ディレクトリ（None の場合は全ディレクトリ）
            
        Returns:
            List[Path]: マッチしたファイルのリスト
        """
        try:
            if directory and directory in self.directories:
                search_path = self.directories[directory]
                return list(search_path.glob(pattern))
            else:
                # 全ディレクトリを検索
                matched_files = []
                for dir_path in self.directories.values():
                    matched_files.extend(dir_path.glob(pattern))
                return matched_files
                
        except Exception as e:
            logger.error(f"ファイル検索エラー: {pattern}, {e}")
            raise FileOperationError(f"ファイル検索に失敗しました: {e}")
    
    def get_file_metadata(self, file_path: Union[str, Path]) -> FileMetadata:
        """
        ファイルメタデータを取得
        
        Args:
            file_path: ファイルパス
            
        Returns:
            FileMetadata: ファイルメタデータ
        """
        try:
            path = Path(file_path)
            stat = path.stat()
            
            return FileMetadata(
                path=str(path),
                name=path.name,
                size=stat.st_size,
                created_at=datetime.fromtimestamp(stat.st_ctime),
                modified_at=datetime.fromtimestamp(stat.st_mtime),
                exists=path.exists(),
                is_file=path.is_file(),
                is_directory=path.is_dir()
            )
            
        except Exception as e:
            logger.error(f"ファイルメタデータ取得エラー: {file_path}, {e}")
            raise FileOperationError(f"ファイルメタデータ取得に失敗しました: {e}")
    
    # ===== バックアップ・復元 =====
    
    def create_backup(self, table_name: str = None) -> str:
        """
        バックアップを作成
        
        Args:
            table_name: 特定テーブルのバックアップ（None の場合は全体）
            
        Returns:
            str: バックアップディレクトリパス
            
        Raises:
            FileOperationError: バックアップ作成エラー
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if table_name:
                backup_dir = self.directories['backups'] / f"{table_name}_{timestamp}"
            else:
                backup_dir = self.directories['backups'] / f"full_backup_{timestamp}"
            
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            if table_name:
                # 特定テーブルのファイルをバックアップ
                self._backup_table_files(table_name, backup_dir)
            else:
                # 全ファイルをバックアップ
                for dir_name, dir_path in self.directories.items():
                    if dir_name != 'backups' and dir_path.exists():
                        backup_subdir = backup_dir / dir_name
                        shutil.copytree(dir_path, backup_subdir, dirs_exist_ok=True)
            
            logger.info(f"バックアップを作成しました: {backup_dir}")
            return str(backup_dir)
            
        except Exception as e:
            logger.error(f"バックアップ作成エラー: {table_name}, {e}")
            raise FileOperationError(f"バックアップ作成に失敗しました: {e}")
    
    def _backup_table_files(self, table_name: str, backup_dir: Path) -> None:
        """特定テーブルのファイルをバックアップ"""
        # YAML定義
        yaml_file = self.directories['table_details'] / f"{table_name}_details.yaml"
        if yaml_file.exists():
            shutil.copy2(yaml_file, backup_dir / yaml_file.name)
        
        # DDLファイル
        ddl_file = self.directories['ddl'] / f"{table_name}.sql"
        if ddl_file.exists():
            shutil.copy2(ddl_file, backup_dir / ddl_file.name)
        
        # Markdownファイル
        markdown_files = glob.glob(str(self.directories['tables'] / f"テーブル定義書_{table_name}_*.md"))
        for markdown_file in markdown_files:
            shutil.copy2(markdown_file, backup_dir / Path(markdown_file).name)
        
        # サンプルデータ
        data_file = self.directories['data'] / f"{table_name}_sample_data.sql"
        if data_file.exists():
            shutil.copy2(data_file, backup_dir / data_file.name)
    
    def restore_backup(self, backup_path: str) -> None:
        """
        バックアップから復元
        
        Args:
            backup_path: バックアップディレクトリパス
            
        Raises:
            FileOperationError: 復元エラー
        """
        try:
            backup_dir = Path(backup_path)
            
            if not backup_dir.exists():
                raise FileOperationError(f"バックアップディレクトリが見つかりません: {backup_path}")
            
            # バックアップディレクトリの内容を復元
            for item in backup_dir.iterdir():
                if item.is_dir():
                    # ディレクトリの場合
                    target_dir = self.directories.get(item.name)
                    if target_dir:
                        shutil.copytree(item, target_dir, dirs_exist_ok=True)
                else:
                    # ファイルの場合（特定テーブルのバックアップ）
                    self._restore_table_file(item)
            
            logger.info(f"バックアップから復元しました: {backup_path}")
            
        except Exception as e:
            logger.error(f"バックアップ復元エラー: {backup_path}, {e}")
            raise FileOperationError(f"バックアップ復元に失敗しました: {e}")
    
    def _restore_table_file(self, file_path: Path) -> None:
        """特定テーブルファイルを復元"""
        filename = file_path.name
        
        if filename.endswith('_details.yaml'):
            target_dir = self.directories['table_details']
        elif filename.endswith('.sql') and not filename.endswith('_sample_data.sql'):
            target_dir = self.directories['ddl']
        elif filename.startswith('テーブル定義書_') and filename.endswith('.md'):
            target_dir = self.directories['tables']
        elif filename.endswith('_sample_data.sql'):
            target_dir = self.directories['data']
        else:
            logger.warning(f"復元対象外のファイル: {filename}")
            return
        
        shutil.copy2(file_path, target_dir / filename)
    
    # ===== ユーティリティ =====
    
    def cleanup_orphaned_files(self) -> List[str]:
        """
        孤立ファイルをクリーンアップ
        
        Returns:
            List[str]: 削除されたファイルのリスト
        """
        try:
            yaml_tables = set(self.list_yaml_definitions())
            ddl_tables = set(self.list_ddl_files())
            markdown_tables = set(self.list_markdown_definitions())
            
            all_tables = yaml_tables | ddl_tables | markdown_tables
            deleted_files = []
            
            # 孤立したDDLファイルを削除
            for table_name in ddl_tables - yaml_tables:
                ddl_file = self.directories['ddl'] / f"{table_name}.sql"
                if ddl_file.exists():
                    ddl_file.unlink()
                    deleted_files.append(str(ddl_file))
            
            # 孤立したMarkdownファイルを削除
            for table_name in markdown_tables - yaml_tables:
                markdown_files = glob.glob(str(self.directories['tables'] / f"テーブル定義書_{table_name}_*.md"))
                for markdown_file in markdown_files:
                    Path(markdown_file).unlink()
                    deleted_files.append(markdown_file)
            
            # 孤立したサンプルデータファイルを削除
            data_files = glob.glob(str(self.directories['data'] / "*_sample_data.sql"))
            for data_file in data_files:
                table_name = Path(data_file).stem.replace('_sample_data', '')
                if table_name not in yaml_tables:
                    Path(data_file).unlink()
                    deleted_files.append(data_file)
            
            logger.info(f"孤立ファイルを削除しました: {len(deleted_files)}件")
            return deleted_files
            
        except Exception as e:
            logger.error(f"孤立ファイルクリーンアップエラー: {e}")
            raise FileOperationError(f"孤立ファイルクリーンアップに失敗しました: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        ファイル統計情報を取得
        
        Returns:
            Dict[str, Any]: 統計情報
        """
        try:
            stats = {
                'yaml_files': len(self.list_yaml_definitions()),
                'ddl_files': len(self.list_ddl_files()),
                'markdown_files': len(self.list_markdown_definitions()),
                'directories': {}
            }
            
            for dir_name, dir_path in self.directories.items():
                if dir_path.exists():
                    files = list(dir_path.glob('*'))
                    total_size = sum(f.stat().st_size for f in files if f.is_file())
                    
                    stats['directories'][dir_name] = {
                        'file_count': len([f for f in files if f.is_file()]),
                        'total_size': total_size,
                        'path': str(dir_path)
                    }
            
            return stats
            
        except Exception as e:
            logger.error(f"統計情報取得エラー: {e}")
            raise FileOperationError(f"統計情報取得に失敗しました: {e}")
