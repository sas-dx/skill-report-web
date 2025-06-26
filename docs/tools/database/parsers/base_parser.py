"""
統一パーサーベースクラス

全パーサーの基底クラスを定義
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..core import get_logger, ValidationResult, ParseError


class BaseParser(ABC):
    """パーサーの基底クラス"""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = get_logger(f"parser.{name}")
        self._cache = {}
    
    @abstractmethod
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        ファイルを解析してデータを返す
        
        Args:
            file_path: 解析対象ファイルパス
            
        Returns:
            解析結果データ
            
        Raises:
            ParseError: 解析エラー
        """
        pass
    
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        データの妥当性を検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            検証結果
        """
        pass
    
    @abstractmethod
    def get_supported_extensions(self) -> List[str]:
        """
        サポートするファイル拡張子を取得
        
        Returns:
            拡張子のリスト
        """
        pass
    
    def can_parse(self, file_path: str) -> bool:
        """
        ファイルを解析可能かチェック
        
        Args:
            file_path: ファイルパス
            
        Returns:
            解析可能な場合True
        """
        path = Path(file_path)
        return path.suffix.lower() in self.get_supported_extensions()
    
    def parse_with_validation(self, file_path: str) -> tuple[Dict[str, Any], ValidationResult]:
        """
        解析と検証を同時実行
        
        Args:
            file_path: ファイルパス
            
        Returns:
            (解析結果, 検証結果)のタプル
        """
        try:
            data = self.parse(file_path)
            validation_result = self.validate(data)
            return data, validation_result
        except Exception as e:
            validation_result = ValidationResult(
                is_valid=False,
                file_path=file_path
            )
            validation_result.add_error(f"解析エラー: {str(e)}")
            return {}, validation_result
    
    def parse_with_cache(self, file_path: str, use_cache: bool = True) -> Dict[str, Any]:
        """
        キャッシュ機能付きで解析
        
        Args:
            file_path: ファイルパス
            use_cache: キャッシュを使用するか
            
        Returns:
            解析結果
        """
        if use_cache and file_path in self._cache:
            self.logger.debug(f"キャッシュから取得: {file_path}")
            return self._cache[file_path]
        
        data = self.parse(file_path)
        
        if use_cache:
            self._cache[file_path] = data
            self.logger.debug(f"キャッシュに保存: {file_path}")
        
        return data
    
    def clear_cache(self) -> None:
        """キャッシュをクリア"""
        self._cache.clear()
        self.logger.debug("キャッシュをクリアしました")
    
    def get_cache_info(self) -> Dict[str, Any]:
        """キャッシュ情報を取得"""
        return {
            'cached_files': list(self._cache.keys()),
            'cache_size': len(self._cache)
        }
    
    def _validate_file_exists(self, file_path: str) -> None:
        """ファイル存在チェック"""
        if not Path(file_path).exists():
            raise ParseError(f"ファイルが存在しません: {file_path}", file_path)
    
    def _validate_file_readable(self, file_path: str) -> None:
        """ファイル読み取り可能チェック"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                f.read(1)
        except Exception as e:
            raise ParseError(f"ファイルが読み取れません: {str(e)}", file_path)
    
    def _get_file_info(self, file_path: str) -> Dict[str, Any]:
        """ファイル情報を取得"""
        path = Path(file_path)
        return {
            'name': path.name,
            'stem': path.stem,
            'suffix': path.suffix,
            'size': path.stat().st_size if path.exists() else 0,
            'exists': path.exists()
        }
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        return self.__str__()
