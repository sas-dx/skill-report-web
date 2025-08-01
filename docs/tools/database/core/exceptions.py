"""
統一例外処理システム

全ツールで共通の例外クラスを提供
"""

from typing import Optional, Dict, Any


class DatabaseToolError(Exception):
    """データベースツール基底例外"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - 詳細: {self.details}"
        return self.message


class ValidationError(DatabaseToolError):
    """バリデーションエラー"""
    
    def __init__(self, message: str, field: Optional[str] = None, 
                 value: Optional[Any] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.field = field
        self.value = value
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.field:
            parts.append(f"フィールド: {self.field}")
        if self.value is not None:
            parts.append(f"値: {self.value}")
        if self.details:
            parts.append(f"詳細: {self.details}")
        return " - ".join(parts)


class FileNotFoundError(DatabaseToolError):
    """ファイル未発見エラー"""
    
    def __init__(self, file_path: str, details: Optional[Dict[str, Any]] = None):
        message = f"ファイルが見つかりません: {file_path}"
        super().__init__(message, details)
        self.file_path = file_path


class ParseError(DatabaseToolError):
    """パースエラー"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, 
                 line_number: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.file_path = file_path
        self.line_number = line_number
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.file_path:
            parts.append(f"ファイル: {self.file_path}")
        if self.line_number:
            parts.append(f"行: {self.line_number}")
        if self.details:
            parts.append(f"詳細: {self.details}")
        return " - ".join(parts)


class GenerationError(DatabaseToolError):
    """生成エラー"""
    
    def __init__(self, message: str, target_type: Optional[str] = None, 
                 target_name: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.target_type = target_type
        self.target_name = target_name
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.target_type:
            parts.append(f"対象タイプ: {self.target_type}")
        if self.target_name:
            parts.append(f"対象名: {self.target_name}")
        if self.details:
            parts.append(f"詳細: {self.details}")
        return " - ".join(parts)


class ConfigurationError(DatabaseToolError):
    """設定エラー"""
    
    def __init__(self, message: str, config_key: Optional[str] = None, 
                 details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.config_key = config_key
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.config_key:
            parts.append(f"設定キー: {self.config_key}")
        if self.details:
            parts.append(f"詳細: {self.details}")
        return " - ".join(parts)


class ConsistencyError(DatabaseToolError):
    """整合性エラー"""
    
    def __init__(self, message: str, source_file: Optional[str] = None, 
                 target_file: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.source_file = source_file
        self.target_file = target_file
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.source_file:
            parts.append(f"ソース: {self.source_file}")
        if self.target_file:
            parts.append(f"ターゲット: {self.target_file}")
        if self.details:
            parts.append(f"詳細: {self.details}")
        return " - ".join(parts)


def handle_exception(func):
    """例外ハンドリングデコレータ"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseToolError:
            # 既知の例外はそのまま再発生
            raise
        except FileNotFoundError as e:
            # 標準のFileNotFoundErrorを独自例外に変換
            raise FileNotFoundError(str(e))
        except Exception as e:
            # その他の例外は基底例外に変換
            raise DatabaseToolError(f"予期しないエラーが発生しました: {str(e)}")
    
    return wrapper
