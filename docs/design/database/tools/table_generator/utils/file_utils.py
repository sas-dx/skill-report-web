#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - ファイル操作ユーティリティ

ファイル・ディレクトリ操作の共通機能を提供します。

対応要求仕様ID: PLT.2-TOOL.1
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.core.logger import get_logger


class FileUtils:
    """ファイル操作ユーティリティクラス
    
    ファイル・ディレクトリの作成、削除、コピー、移動などの
    共通操作を提供します。
    """
    
    def __init__(self, logger=None):
        """初期化
        
        Args:
            logger (DatabaseToolsLogger, optional): ログ出力インスタンス
        """
        self.logger = logger or get_logger()
    
    def ensure_directory(self, directory_path: Path) -> bool:
        """ディレクトリの存在を確認し、存在しない場合は作成
        
        Args:
            directory_path (Path): ディレクトリパス
            
        Returns:
            bool: 作成成功フラグ
        """
        try:
            directory_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"ディレクトリ作成エラー ({directory_path}): {e}")
            return False
    
    def ensure_directories(self, directory_paths: List[Path]) -> bool:
        """複数ディレクトリの存在を確認し、存在しない場合は作成
        
        Args:
            directory_paths (List[Path]): ディレクトリパスのリスト
            
        Returns:
            bool: 全て作成成功フラグ
        """
        success = True
        for directory_path in directory_paths:
            if not self.ensure_directory(directory_path):
                success = False
        return success
    
    def write_file(self, file_path: Path, content: str, encoding: str = 'utf-8') -> bool:
        """ファイルに内容を書き込み
        
        Args:
            file_path (Path): ファイルパス
            content (str): 書き込み内容
            encoding (str): エンコーディング
            
        Returns:
            bool: 書き込み成功フラグ
        """
        try:
            # ディレクトリが存在しない場合は作成
            self.ensure_directory(file_path.parent)
            
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            self.logger.error(f"ファイル書き込みエラー ({file_path}): {e}")
            return False
    
    def read_file(self, file_path: Path, encoding: str = 'utf-8') -> Optional[str]:
        """ファイルの内容を読み込み
        
        Args:
            file_path (Path): ファイルパス
            encoding (str): エンコーディング
            
        Returns:
            Optional[str]: ファイル内容（失敗時はNone）
        """
        try:
            if not file_path.exists():
                self.logger.warning(f"ファイルが存在しません: {file_path}")
                return None
            
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
                
        except Exception as e:
            self.logger.error(f"ファイル読み込みエラー ({file_path}): {e}")
            return None
    
    def copy_file(self, src_path: Path, dst_path: Path) -> bool:
        """ファイルをコピー
        
        Args:
            src_path (Path): コピー元ファイルパス
            dst_path (Path): コピー先ファイルパス
            
        Returns:
            bool: コピー成功フラグ
        """
        try:
            if not src_path.exists():
                self.logger.error(f"コピー元ファイルが存在しません: {src_path}")
                return False
            
            # コピー先ディレクトリが存在しない場合は作成
            self.ensure_directory(dst_path.parent)
            
            shutil.copy2(src_path, dst_path)
            return True
            
        except Exception as e:
            self.logger.error(f"ファイルコピーエラー ({src_path} -> {dst_path}): {e}")
            return False
    
    def move_file(self, src_path: Path, dst_path: Path) -> bool:
        """ファイルを移動
        
        Args:
            src_path (Path): 移動元ファイルパス
            dst_path (Path): 移動先ファイルパス
            
        Returns:
            bool: 移動成功フラグ
        """
        try:
            if not src_path.exists():
                self.logger.error(f"移動元ファイルが存在しません: {src_path}")
                return False
            
            # 移動先ディレクトリが存在しない場合は作成
            self.ensure_directory(dst_path.parent)
            
            shutil.move(str(src_path), str(dst_path))
            return True
            
        except Exception as e:
            self.logger.error(f"ファイル移動エラー ({src_path} -> {dst_path}): {e}")
            return False
    
    def delete_file(self, file_path: Path) -> bool:
        """ファイルを削除
        
        Args:
            file_path (Path): 削除対象ファイルパス
            
        Returns:
            bool: 削除成功フラグ
        """
        try:
            if not file_path.exists():
                self.logger.warning(f"削除対象ファイルが存在しません: {file_path}")
                return True  # 存在しないので削除成功とみなす
            
            file_path.unlink()
            return True
            
        except Exception as e:
            self.logger.error(f"ファイル削除エラー ({file_path}): {e}")
            return False
    
    def delete_directory(self, directory_path: Path, recursive: bool = False) -> bool:
        """ディレクトリを削除
        
        Args:
            directory_path (Path): 削除対象ディレクトリパス
            recursive (bool): 再帰的削除フラグ
            
        Returns:
            bool: 削除成功フラグ
        """
        try:
            if not directory_path.exists():
                self.logger.warning(f"削除対象ディレクトリが存在しません: {directory_path}")
                return True  # 存在しないので削除成功とみなす
            
            if recursive:
                shutil.rmtree(directory_path)
            else:
                directory_path.rmdir()  # 空ディレクトリのみ削除
            
            return True
            
        except Exception as e:
            self.logger.error(f"ディレクトリ削除エラー ({directory_path}): {e}")
            return False
    
    def list_files(self, directory_path: Path, pattern: str = "*", recursive: bool = False) -> List[Path]:
        """ディレクトリ内のファイル一覧を取得
        
        Args:
            directory_path (Path): 対象ディレクトリパス
            pattern (str): ファイル名パターン
            recursive (bool): 再帰的検索フラグ
            
        Returns:
            List[Path]: ファイルパスのリスト
        """
        try:
            if not directory_path.exists():
                self.logger.warning(f"ディレクトリが存在しません: {directory_path}")
                return []
            
            if recursive:
                return list(directory_path.rglob(pattern))
            else:
                return list(directory_path.glob(pattern))
                
        except Exception as e:
            self.logger.error(f"ファイル一覧取得エラー ({directory_path}): {e}")
            return []
    
    def get_file_size(self, file_path: Path) -> Optional[int]:
        """ファイルサイズを取得
        
        Args:
            file_path (Path): ファイルパス
            
        Returns:
            Optional[int]: ファイルサイズ（バイト）
        """
        try:
            if not file_path.exists():
                return None
            
            return file_path.stat().st_size
            
        except Exception as e:
            self.logger.error(f"ファイルサイズ取得エラー ({file_path}): {e}")
            return None
    
    def get_file_info(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """ファイル情報を取得
        
        Args:
            file_path (Path): ファイルパス
            
        Returns:
            Optional[Dict[str, Any]]: ファイル情報辞書
        """
        try:
            if not file_path.exists():
                return None
            
            stat = file_path.stat()
            
            return {
                'name': file_path.name,
                'path': str(file_path),
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime,
                'accessed': stat.st_atime,
                'is_file': file_path.is_file(),
                'is_dir': file_path.is_dir(),
                'suffix': file_path.suffix,
                'stem': file_path.stem
            }
            
        except Exception as e:
            self.logger.error(f"ファイル情報取得エラー ({file_path}): {e}")
            return None
    
    def backup_file(self, file_path: Path, backup_suffix: str = '.bak') -> Optional[Path]:
        """ファイルをバックアップ
        
        Args:
            file_path (Path): バックアップ対象ファイルパス
            backup_suffix (str): バックアップファイルの接尾辞
            
        Returns:
            Optional[Path]: バックアップファイルパス（失敗時はNone）
        """
        try:
            if not file_path.exists():
                self.logger.error(f"バックアップ対象ファイルが存在しません: {file_path}")
                return None
            
            backup_path = file_path.with_suffix(file_path.suffix + backup_suffix)
            
            # 既存のバックアップファイルがある場合は削除
            if backup_path.exists():
                backup_path.unlink()
            
            if self.copy_file(file_path, backup_path):
                return backup_path
            else:
                return None
                
        except Exception as e:
            self.logger.error(f"ファイルバックアップエラー ({file_path}): {e}")
            return None
    
    def find_files_by_extension(self, directory_path: Path, extensions: List[str], recursive: bool = True) -> List[Path]:
        """指定した拡張子のファイルを検索
        
        Args:
            directory_path (Path): 検索対象ディレクトリパス
            extensions (List[str]): 拡張子のリスト（例: ['.md', '.yaml']）
            recursive (bool): 再帰的検索フラグ
            
        Returns:
            List[Path]: 見つかったファイルパスのリスト
        """
        try:
            if not directory_path.exists():
                self.logger.warning(f"検索対象ディレクトリが存在しません: {directory_path}")
                return []
            
            found_files = []
            
            for ext in extensions:
                pattern = f"*{ext}"
                if recursive:
                    files = list(directory_path.rglob(pattern))
                else:
                    files = list(directory_path.glob(pattern))
                found_files.extend(files)
            
            return found_files
            
        except Exception as e:
            self.logger.error(f"ファイル検索エラー ({directory_path}): {e}")
            return []
    
    def clean_directory(self, directory_path: Path, keep_patterns: List[str] = None) -> bool:
        """ディレクトリをクリーンアップ（指定パターン以外を削除）
        
        Args:
            directory_path (Path): クリーンアップ対象ディレクトリパス
            keep_patterns (List[str], optional): 保持するファイルパターンのリスト
            
        Returns:
            bool: クリーンアップ成功フラグ
        """
        try:
            if not directory_path.exists():
                self.logger.warning(f"クリーンアップ対象ディレクトリが存在しません: {directory_path}")
                return True
            
            keep_patterns = keep_patterns or []
            deleted_count = 0
            
            for item in directory_path.iterdir():
                should_keep = False
                
                # 保持パターンをチェック
                for pattern in keep_patterns:
                    if item.match(pattern):
                        should_keep = True
                        break
                
                if not should_keep:
                    if item.is_file():
                        if self.delete_file(item):
                            deleted_count += 1
                    elif item.is_dir():
                        if self.delete_directory(item, recursive=True):
                            deleted_count += 1
            
            self.logger.info(f"クリーンアップ完了: {deleted_count}個のアイテムを削除")
            return True
            
        except Exception as e:
            self.logger.error(f"ディレクトリクリーンアップエラー ({directory_path}): {e}")
            return False
