"""
統合ファイルユーティリティ
全ツールで使用する共通ファイル操作機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-25
実装者: AI駆動開発チーム
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, Generator
from datetime import datetime
import hashlib
import tempfile
import json
import yaml

from ..core.exceptions import FileOperationError, ValidationError
from ..core.logger import get_logger

logger = get_logger(__name__)


class FileManager:
    """統合ファイル管理クラス"""
    
    def __init__(self, base_dir: Optional[Path] = None, backup_enabled: bool = True):
        """
        ファイルマネージャー初期化
        
        Args:
            base_dir: ベースディレクトリ
            backup_enabled: バックアップ機能の有効化
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.backup_enabled = backup_enabled
        self.backup_dir = self.base_dir / "backups"
        
        if backup_enabled:
            self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def read_file(self, file_path: Union[str, Path], encoding: str = 'utf-8') -> str:
        """
        ファイルを読み込み
        
        Args:
            file_path: ファイルパス
            encoding: エンコーディング
            
        Returns:
            str: ファイル内容
            
        Raises:
            FileOperationError: ファイル読み込みエラー
        """
        file_path = Path(file_path)
        
        try:
            if not file_path.exists():
                raise FileOperationError(
                    f"ファイルが存在しません: {file_path}",
                    file_path=file_path,
                    operation="read"
                )
            
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            logger.debug(f"ファイル読み込み完了: {file_path}")
            return content
            
        except Exception as e:
            if isinstance(e, FileOperationError):
                raise
            raise FileOperationError(
                f"ファイル読み込みエラー: {e}",
                file_path=file_path,
                operation="read"
            )
    
    def write_file(
        self, 
        file_path: Union[str, Path], 
        content: str, 
        encoding: str = 'utf-8',
        create_backup: bool = True
    ) -> bool:
        """
        ファイルを書き込み
        
        Args:
            file_path: ファイルパス
            content: 書き込み内容
            encoding: エンコーディング
            create_backup: バックアップ作成フラグ
            
        Returns:
            bool: 成功フラグ
            
        Raises:
            FileOperationError: ファイル書き込みエラー
        """
        file_path = Path(file_path)
        
        try:
            # バックアップ作成
            if create_backup and self.backup_enabled and file_path.exists():
                self.create_backup(file_path)
            
            # ディレクトリ作成
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ファイル書き込み
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            logger.debug(f"ファイル書き込み完了: {file_path}")
            return True
            
        except Exception as e:
            raise FileOperationError(
                f"ファイル書き込みエラー: {e}",
                file_path=file_path,
                operation="write"
            )
    
    def create_backup(self, file_path: Union[str, Path]) -> Path:
        """
        ファイルのバックアップを作成
        
        Args:
            file_path: バックアップ対象ファイル
            
        Returns:
            Path: バックアップファイルパス
            
        Raises:
            FileOperationError: バックアップ作成エラー
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileOperationError(
                f"バックアップ対象ファイルが存在しません: {file_path}",
                file_path=file_path,
                operation="backup"
            )
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{file_path.stem}.backup.{timestamp}{file_path.suffix}"
            backup_path = self.backup_dir / backup_name
            
            shutil.copy2(file_path, backup_path)
            
            logger.debug(f"バックアップ作成完了: {file_path} -> {backup_path}")
            return backup_path
            
        except Exception as e:
            raise FileOperationError(
                f"バックアップ作成エラー: {e}",
                file_path=file_path,
                operation="backup"
            )
    
    def delete_file(self, file_path: Union[str, Path], create_backup: bool = True) -> bool:
        """
        ファイルを削除
        
        Args:
            file_path: 削除対象ファイル
            create_backup: バックアップ作成フラグ
            
        Returns:
            bool: 成功フラグ
            
        Raises:
            FileOperationError: ファイル削除エラー
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.warning(f"削除対象ファイルが存在しません: {file_path}")
            return True
        
        try:
            # バックアップ作成
            if create_backup and self.backup_enabled:
                self.create_backup(file_path)
            
            # ファイル削除
            file_path.unlink()
            
            logger.debug(f"ファイル削除完了: {file_path}")
            return True
            
        except Exception as e:
            raise FileOperationError(
                f"ファイル削除エラー: {e}",
                file_path=file_path,
                operation="delete"
            )
    
    def copy_file(
        self, 
        source_path: Union[str, Path], 
        target_path: Union[str, Path]
    ) -> bool:
        """
        ファイルをコピー
        
        Args:
            source_path: コピー元ファイル
            target_path: コピー先ファイル
            
        Returns:
            bool: 成功フラグ
            
        Raises:
            FileOperationError: ファイルコピーエラー
        """
        source_path = Path(source_path)
        target_path = Path(target_path)
        
        if not source_path.exists():
            raise FileOperationError(
                f"コピー元ファイルが存在しません: {source_path}",
                file_path=source_path,
                operation="copy"
            )
        
        try:
            # ディレクトリ作成
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ファイルコピー
            shutil.copy2(source_path, target_path)
            
            logger.debug(f"ファイルコピー完了: {source_path} -> {target_path}")
            return True
            
        except Exception as e:
            raise FileOperationError(
                f"ファイルコピーエラー: {e}",
                file_path=source_path,
                operation="copy"
            )
    
    def move_file(
        self, 
        source_path: Union[str, Path], 
        target_path: Union[str, Path]
    ) -> bool:
        """
        ファイルを移動
        
        Args:
            source_path: 移動元ファイル
            target_path: 移動先ファイル
            
        Returns:
            bool: 成功フラグ
            
        Raises:
            FileOperationError: ファイル移動エラー
        """
        source_path = Path(source_path)
        target_path = Path(target_path)
        
        if not source_path.exists():
            raise FileOperationError(
                f"移動元ファイルが存在しません: {source_path}",
                file_path=source_path,
                operation="move"
            )
        
        try:
            # ディレクトリ作成
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # ファイル移動
            shutil.move(str(source_path), str(target_path))
            
            logger.debug(f"ファイル移動完了: {source_path} -> {target_path}")
            return True
            
        except Exception as e:
            raise FileOperationError(
                f"ファイル移動エラー: {e}",
                file_path=source_path,
                operation="move"
            )
    
    def get_file_hash(self, file_path: Union[str, Path], algorithm: str = 'md5') -> str:
        """
        ファイルのハッシュ値を取得
        
        Args:
            file_path: ファイルパス
            algorithm: ハッシュアルゴリズム
            
        Returns:
            str: ハッシュ値
            
        Raises:
            FileOperationError: ハッシュ計算エラー
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileOperationError(
                f"ファイルが存在しません: {file_path}",
                file_path=file_path,
                operation="hash"
            )
        
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
            
            return hash_obj.hexdigest()
            
        except Exception as e:
            raise FileOperationError(
                f"ハッシュ計算エラー: {e}",
                file_path=file_path,
                operation="hash"
            )
    
    def find_files(
        self, 
        directory: Union[str, Path], 
        pattern: str = "*",
        recursive: bool = True
    ) -> List[Path]:
        """
        ファイルを検索
        
        Args:
            directory: 検索ディレクトリ
            pattern: 検索パターン
            recursive: 再帰検索フラグ
            
        Returns:
            List[Path]: 見つかったファイルのリスト
        """
        directory = Path(directory)
        
        if not directory.exists():
            logger.warning(f"検索ディレクトリが存在しません: {directory}")
            return []
        
        try:
            if recursive:
                files = list(directory.rglob(pattern))
            else:
                files = list(directory.glob(pattern))
            
            # ファイルのみを返す
            return [f for f in files if f.is_file()]
            
        except Exception as e:
            logger.error(f"ファイル検索エラー: {e}")
            return []
    
    def cleanup_old_files(
        self, 
        directory: Union[str, Path], 
        days: int = 30,
        pattern: str = "*"
    ) -> int:
        """
        古いファイルをクリーンアップ
        
        Args:
            directory: クリーンアップ対象ディレクトリ
            days: 保持日数
            pattern: ファイルパターン
            
        Returns:
            int: 削除されたファイル数
        """
        directory = Path(directory)
        
        if not directory.exists():
            return 0
        
        try:
            cutoff_time = datetime.now().timestamp() - (days * 24 * 60 * 60)
            deleted_count = 0
            
            for file_path in directory.glob(pattern):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    file_path.unlink()
                    deleted_count += 1
                    logger.debug(f"古いファイルを削除: {file_path}")
            
            logger.info(f"クリーンアップ完了: {deleted_count}個のファイルを削除")
            return deleted_count
            
        except Exception as e:
            logger.error(f"クリーンアップエラー: {e}")
            return 0


class YamlFileManager(FileManager):
    """YAML専用ファイルマネージャー"""
    
    def read_yaml(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        YAMLファイルを読み込み
        
        Args:
            file_path: YAMLファイルパス
            
        Returns:
            Dict[str, Any]: YAML内容
            
        Raises:
            FileOperationError: YAML読み込みエラー
        """
        try:
            content = self.read_file(file_path)
            return yaml.safe_load(content)
            
        except yaml.YAMLError as e:
            raise FileOperationError(
                f"YAML解析エラー: {e}",
                file_path=Path(file_path),
                operation="yaml_read"
            )
    
    def write_yaml(
        self, 
        file_path: Union[str, Path], 
        data: Dict[str, Any],
        create_backup: bool = True
    ) -> bool:
        """
        YAMLファイルを書き込み
        
        Args:
            file_path: YAMLファイルパス
            data: YAML内容
            create_backup: バックアップ作成フラグ
            
        Returns:
            bool: 成功フラグ
            
        Raises:
            FileOperationError: YAML書き込みエラー
        """
        try:
            content = yaml.dump(
                data, 
                default_flow_style=False, 
                allow_unicode=True, 
                indent=2,
                sort_keys=False
            )
            return self.write_file(file_path, content, create_backup=create_backup)
            
        except yaml.YAMLError as e:
            raise FileOperationError(
                f"YAML生成エラー: {e}",
                file_path=Path(file_path),
                operation="yaml_write"
            )


class JsonFileManager(FileManager):
    """JSON専用ファイルマネージャー"""
    
    def read_json(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        JSONファイルを読み込み
        
        Args:
            file_path: JSONファイルパス
            
        Returns:
            Dict[str, Any]: JSON内容
            
        Raises:
            FileOperationError: JSON読み込みエラー
        """
        try:
            content = self.read_file(file_path)
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            raise FileOperationError(
                f"JSON解析エラー: {e}",
                file_path=Path(file_path),
                operation="json_read"
            )
    
    def write_json(
        self, 
        file_path: Union[str, Path], 
        data: Dict[str, Any],
        create_backup: bool = True,
        indent: int = 2
    ) -> bool:
        """
        JSONファイルを書き込み
        
        Args:
            file_path: JSONファイルパス
            data: JSON内容
            create_backup: バックアップ作成フラグ
            indent: インデント数
            
        Returns:
            bool: 成功フラグ
            
        Raises:
            FileOperationError: JSON書き込みエラー
        """
        try:
            content = json.dumps(
                data, 
                ensure_ascii=False, 
                indent=indent,
                sort_keys=False
            )
            return self.write_file(file_path, content, create_backup=create_backup)
            
        except (TypeError, ValueError) as e:
            raise FileOperationError(
                f"JSON生成エラー: {e}",
                file_path=Path(file_path),
                operation="json_write"
            )


def create_temp_file(suffix: str = "", prefix: str = "db_tools_") -> Path:
    """
    一時ファイルを作成
    
    Args:
        suffix: ファイル拡張子
        prefix: ファイル名プレフィックス
        
    Returns:
        Path: 一時ファイルパス
    """
    fd, temp_path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(fd)
    return Path(temp_path)


def ensure_directory(directory: Union[str, Path]) -> Path:
    """
    ディレクトリの存在を確保
    
    Args:
        directory: ディレクトリパス
        
    Returns:
        Path: ディレクトリパス
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    ファイルサイズを取得
    
    Args:
        file_path: ファイルパス
        
    Returns:
        int: ファイルサイズ（バイト）
    """
    file_path = Path(file_path)
    return file_path.stat().st_size if file_path.exists() else 0


def is_binary_file(file_path: Union[str, Path]) -> bool:
    """
    バイナリファイルかどうかを判定
    
    Args:
        file_path: ファイルパス
        
    Returns:
        bool: バイナリファイルフラグ
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            return b'\0' in chunk
    except Exception:
        return True


# グローバルインスタンス
_file_manager: Optional[FileManager] = None
_yaml_manager: Optional[YamlFileManager] = None
_json_manager: Optional[JsonFileManager] = None


def get_file_manager(base_dir: Optional[Path] = None) -> FileManager:
    """グローバルファイルマネージャーを取得"""
    global _file_manager
    if _file_manager is None or base_dir:
        _file_manager = FileManager(base_dir)
    return _file_manager


def get_yaml_manager(base_dir: Optional[Path] = None) -> YamlFileManager:
    """グローバルYAMLマネージャーを取得"""
    global _yaml_manager
    if _yaml_manager is None or base_dir:
        _yaml_manager = YamlFileManager(base_dir)
    return _yaml_manager


def get_json_manager(base_dir: Optional[Path] = None) -> JsonFileManager:
    """グローバルJSONマネージャーを取得"""
    global _json_manager
    if _json_manager is None or base_dir:
        _json_manager = JsonFileManager(base_dir)
    return _json_manager
