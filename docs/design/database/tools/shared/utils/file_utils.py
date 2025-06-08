"""
統合ファイル操作ユーティリティ
両ツールで使用する共通ファイル操作機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
import yaml
import json

from ..core.config import get_config
from ..core.logger import get_logger
from ..core.exceptions import (
    FileOperationError, YamlParsingError, BackupError,
    ExceptionHandler
)


class FileManager:
    """統合ファイル操作クラス - 重複コードの統合"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
    
    @ExceptionHandler.handle_file_operation_error
    def read_file(self, file_path: Path, encoding: Optional[str] = None) -> str:
        """ファイル読み込み - 両ツールで使用"""
        encoding = encoding or self.config.encoding
        
        if not file_path.exists():
            raise FileOperationError(
                f"ファイルが存在しません: {file_path}",
                file_path=file_path,
                operation="read"
            )
        
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            self.logger.log_file_operation(file_path, "read", success=True)
            return content
            
        except Exception as e:
            self.logger.log_file_operation(file_path, "read", success=False, error=str(e))
            raise FileOperationError(
                f"ファイル読み込みエラー: {str(e)}",
                file_path=file_path,
                operation="read"
            ) from e
    
    @ExceptionHandler.handle_yaml_parsing_error
    def read_yaml_file(self, file_path: Path) -> Dict[str, Any]:
        """YAML読み込み - 両ツールで使用"""
        try:
            content = self.read_file(file_path)
            data = yaml.safe_load(content)
            
            if data is None:
                data = {}
            
            self.logger.log_file_operation(
                file_path, "yaml_read", success=True,
                data_keys=list(data.keys()) if isinstance(data, dict) else None
            )
            
            return data
            
        except yaml.YAMLError as e:
            self.logger.log_file_operation(file_path, "yaml_read", success=False, error=str(e))
            raise YamlParsingError(
                f"YAML解析エラー: {str(e)}",
                file_path=file_path
            ) from e
    
    def read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """JSON読み込み"""
        try:
            content = self.read_file(file_path)
            data = json.loads(content)
            
            self.logger.log_file_operation(
                file_path, "json_read", success=True,
                data_keys=list(data.keys()) if isinstance(data, dict) else None
            )
            
            return data
            
        except json.JSONDecodeError as e:
            self.logger.log_file_operation(file_path, "json_read", success=False, error=str(e))
            raise FileOperationError(
                f"JSON解析エラー: {str(e)}",
                file_path=file_path,
                operation="json_read"
            ) from e
    
    def write_file_safely(self, file_path: Path, content: str, 
                         encoding: Optional[str] = None, 
                         create_backup: bool = None) -> Optional[Path]:
        """安全なファイル書き込み - バックアップ付き"""
        encoding = encoding or self.config.encoding
        create_backup = create_backup if create_backup is not None else self.config.backup_enabled
        
        backup_path = None
        
        try:
            # ディレクトリ作成
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # バックアップ作成
            if create_backup and file_path.exists():
                backup_path = self.create_backup(file_path)
            
            # ファイル書き込み
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            self.logger.log_file_operation(
                file_path, "write", success=True,
                content_length=len(content),
                backup_created=backup_path is not None
            )
            
            return backup_path
            
        except Exception as e:
            self.logger.log_file_operation(file_path, "write", success=False, error=str(e))
            raise FileOperationError(
                f"ファイル書き込みエラー: {str(e)}",
                file_path=file_path,
                operation="write"
            ) from e
    
    def write_yaml_file(self, file_path: Path, data: Dict[str, Any], 
                       create_backup: bool = None) -> Optional[Path]:
        """YAML書き込み"""
        try:
            yaml_content = yaml.dump(
                data, 
                default_flow_style=False, 
                allow_unicode=True,
                sort_keys=False,
                indent=2
            )
            
            backup_path = self.write_file_safely(file_path, yaml_content, create_backup=create_backup)
            
            self.logger.log_file_operation(
                file_path, "yaml_write", success=True,
                data_keys=list(data.keys()) if isinstance(data, dict) else None
            )
            
            return backup_path
            
        except Exception as e:
            self.logger.log_file_operation(file_path, "yaml_write", success=False, error=str(e))
            raise FileOperationError(
                f"YAML書き込みエラー: {str(e)}",
                file_path=file_path,
                operation="yaml_write"
            ) from e
    
    def write_json_file(self, file_path: Path, data: Dict[str, Any], 
                       create_backup: bool = None) -> Optional[Path]:
        """JSON書き込み"""
        try:
            json_content = json.dumps(
                data, 
                ensure_ascii=False, 
                indent=2,
                default=str
            )
            
            backup_path = self.write_file_safely(file_path, json_content, create_backup=create_backup)
            
            self.logger.log_file_operation(
                file_path, "json_write", success=True,
                data_keys=list(data.keys()) if isinstance(data, dict) else None
            )
            
            return backup_path
            
        except Exception as e:
            self.logger.log_file_operation(file_path, "json_write", success=False, error=str(e))
            raise FileOperationError(
                f"JSON書き込みエラー: {str(e)}",
                file_path=file_path,
                operation="json_write"
            ) from e
    
    def create_backup(self, file_path: Path) -> Path:
        """バックアップ作成"""
        if not file_path.exists():
            raise FileOperationError(
                f"バックアップ対象ファイルが存在しません: {file_path}",
                file_path=file_path,
                operation="backup"
            )
        
        try:
            backup_path = self.config.get_backup_path(file_path)
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            shutil.copy2(file_path, backup_path)
            
            self.logger.log_file_operation(
                file_path, "backup", success=True,
                backup_path=str(backup_path)
            )
            
            return backup_path
            
        except Exception as e:
            self.logger.log_file_operation(file_path, "backup", success=False, error=str(e))
            raise BackupError(
                f"バックアップ作成エラー: {str(e)}",
                source_file=file_path
            ) from e
    
    def restore_from_backup(self, backup_path: Path, target_path: Path):
        """バックアップから復元"""
        if not backup_path.exists():
            raise BackupError(
                f"バックアップファイルが存在しません: {backup_path}",
                backup_file=backup_path
            )
        
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_path, target_path)
            
            self.logger.log_file_operation(
                target_path, "restore", success=True,
                backup_path=str(backup_path)
            )
            
        except Exception as e:
            self.logger.log_file_operation(target_path, "restore", success=False, error=str(e))
            raise BackupError(
                f"バックアップ復元エラー: {str(e)}",
                backup_file=backup_path,
                source_file=target_path
            ) from e
    
    def delete_file(self, file_path: Path, create_backup: bool = None):
        """ファイル削除"""
        create_backup = create_backup if create_backup is not None else self.config.backup_enabled
        
        if not file_path.exists():
            self.logger.warning(f"削除対象ファイルが存在しません: {file_path}")
            return
        
        try:
            backup_path = None
            if create_backup:
                backup_path = self.create_backup(file_path)
            
            file_path.unlink()
            
            self.logger.log_file_operation(
                file_path, "delete", success=True,
                backup_created=backup_path is not None
            )
            
        except Exception as e:
            self.logger.log_file_operation(file_path, "delete", success=False, error=str(e))
            raise FileOperationError(
                f"ファイル削除エラー: {str(e)}",
                file_path=file_path,
                operation="delete"
            ) from e
    
    def copy_file(self, source_path: Path, target_path: Path):
        """ファイルコピー"""
        if not source_path.exists():
            raise FileOperationError(
                f"コピー元ファイルが存在しません: {source_path}",
                file_path=source_path,
                operation="copy"
            )
        
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target_path)
            
            self.logger.log_file_operation(
                target_path, "copy", success=True,
                source_path=str(source_path)
            )
            
        except Exception as e:
            self.logger.log_file_operation(target_path, "copy", success=False, error=str(e))
            raise FileOperationError(
                f"ファイルコピーエラー: {str(e)}",
                file_path=target_path,
                operation="copy"
            ) from e
    
    def move_file(self, source_path: Path, target_path: Path):
        """ファイル移動"""
        if not source_path.exists():
            raise FileOperationError(
                f"移動元ファイルが存在しません: {source_path}",
                file_path=source_path,
                operation="move"
            )
        
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(target_path))
            
            self.logger.log_file_operation(
                target_path, "move", success=True,
                source_path=str(source_path)
            )
            
        except Exception as e:
            self.logger.log_file_operation(target_path, "move", success=False, error=str(e))
            raise FileOperationError(
                f"ファイル移動エラー: {str(e)}",
                file_path=target_path,
                operation="move"
            ) from e
    
    def list_files(self, directory: Path, pattern: str = "*", 
                  recursive: bool = False) -> List[Path]:
        """ファイル一覧取得"""
        if not directory.exists():
            raise FileOperationError(
                f"ディレクトリが存在しません: {directory}",
                file_path=directory,
                operation="list"
            )
        
        try:
            if recursive:
                files = list(directory.rglob(pattern))
            else:
                files = list(directory.glob(pattern))
            
            # ファイルのみを返す
            files = [f for f in files if f.is_file()]
            
            self.logger.debug(f"ファイル一覧取得: {directory}", {
                'directory': str(directory),
                'pattern': pattern,
                'recursive': recursive,
                'file_count': len(files)
            })
            
            return files
            
        except Exception as e:
            self.logger.log_file_operation(directory, "list", success=False, error=str(e))
            raise FileOperationError(
                f"ファイル一覧取得エラー: {str(e)}",
                file_path=directory,
                operation="list"
            ) from e
    
    def ensure_directory(self, directory: Path):
        """ディレクトリ作成（存在しない場合）"""
        try:
            directory.mkdir(parents=True, exist_ok=True)
            
            self.logger.debug(f"ディレクトリ確保: {directory}")
            
        except Exception as e:
            raise FileOperationError(
                f"ディレクトリ作成エラー: {str(e)}",
                file_path=directory,
                operation="mkdir"
            ) from e
    
    def get_file_info(self, file_path: Path) -> Dict[str, Any]:
        """ファイル情報取得"""
        if not file_path.exists():
            raise FileOperationError(
                f"ファイルが存在しません: {file_path}",
                file_path=file_path,
                operation="stat"
            )
        
        try:
            stat = file_path.stat()
            
            info = {
                'path': str(file_path),
                'name': file_path.name,
                'size': stat.st_size,
                'modified_time': datetime.fromtimestamp(stat.st_mtime),
                'created_time': datetime.fromtimestamp(stat.st_ctime),
                'is_file': file_path.is_file(),
                'is_directory': file_path.is_dir(),
                'suffix': file_path.suffix,
                'stem': file_path.stem
            }
            
            return info
            
        except Exception as e:
            raise FileOperationError(
                f"ファイル情報取得エラー: {str(e)}",
                file_path=file_path,
                operation="stat"
            ) from e


class BackupManager:
    """バックアップ管理クラス"""
    
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()
        self.file_manager = FileManager()
    
    def cleanup_old_backups(self, days: int = None):
        """古いバックアップファイルのクリーンアップ"""
        days = days or self.config.keep_reports
        cutoff_date = datetime.now() - datetime.timedelta(days=days)
        
        try:
            backup_files = self.file_manager.list_files(
                self.config.backup_dir, 
                "*.backup.*", 
                recursive=True
            )
            
            deleted_count = 0
            for backup_file in backup_files:
                file_info = self.file_manager.get_file_info(backup_file)
                if file_info['modified_time'] < cutoff_date:
                    self.file_manager.delete_file(backup_file, create_backup=False)
                    deleted_count += 1
            
            self.logger.info(f"バックアップクリーンアップ完了: {deleted_count}ファイル削除", {
                'deleted_count': deleted_count,
                'cutoff_days': days,
                'cutoff_date': cutoff_date.isoformat()
            })
            
        except Exception as e:
            self.logger.error(f"バックアップクリーンアップエラー: {str(e)}")
            raise
    
    def list_backups(self, original_file: Optional[Path] = None) -> List[Dict[str, Any]]:
        """バックアップファイル一覧取得"""
        try:
            backup_files = self.file_manager.list_files(
                self.config.backup_dir, 
                "*.backup.*", 
                recursive=True
            )
            
            backups = []
            for backup_file in backup_files:
                file_info = self.file_manager.get_file_info(backup_file)
                
                # 元ファイル名を推定
                name_parts = backup_file.name.split('.backup.')
                if len(name_parts) >= 2:
                    original_name = name_parts[0] + backup_file.suffix
                    
                    # 特定ファイルのフィルタリング
                    if original_file and original_name != original_file.name:
                        continue
                    
                    backups.append({
                        'backup_file': backup_file,
                        'original_name': original_name,
                        'size': file_info['size'],
                        'created_time': file_info['created_time'],
                        'modified_time': file_info['modified_time']
                    })
            
            # 作成日時でソート（新しい順）
            backups.sort(key=lambda x: x['created_time'], reverse=True)
            
            return backups
            
        except Exception as e:
            self.logger.error(f"バックアップ一覧取得エラー: {str(e)}")
            raise


# グローバルインスタンス
_file_manager_instance: Optional[FileManager] = None
_backup_manager_instance: Optional[BackupManager] = None


def get_file_manager() -> FileManager:
    """グローバルファイルマネージャーインスタンスを取得"""
    global _file_manager_instance
    if _file_manager_instance is None:
        _file_manager_instance = FileManager()
    return _file_manager_instance


def get_backup_manager() -> BackupManager:
    """グローバルバックアップマネージャーインスタンスを取得"""
    global _backup_manager_instance
    if _backup_manager_instance is None:
        _backup_manager_instance = BackupManager()
    return _backup_manager_instance
