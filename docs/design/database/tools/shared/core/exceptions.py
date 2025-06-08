"""
統合例外クラス定義
両ツールで使用する統一された例外処理

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

from typing import Optional, Dict, Any, List
from pathlib import Path


class DatabaseToolsException(Exception):
    """データベースツール基底例外クラス"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.details:
            return f"{self.message} (詳細: {self.details})"
        return self.message


class ConfigurationError(DatabaseToolsException):
    """設定エラー"""
    pass


class FileOperationError(DatabaseToolsException):
    """ファイル操作エラー"""
    
    def __init__(self, message: str, file_path: Optional[Path] = None, 
                 operation: Optional[str] = None, **kwargs):
        details = kwargs
        if file_path:
            details['file_path'] = str(file_path)
        if operation:
            details['operation'] = operation
        super().__init__(message, details)
        self.file_path = file_path
        self.operation = operation


class YamlParsingError(DatabaseToolsException):
    """YAML解析エラー"""
    
    def __init__(self, message: str, file_path: Optional[Path] = None, 
                 line_number: Optional[int] = None, **kwargs):
        details = kwargs
        if file_path:
            details['file_path'] = str(file_path)
        if line_number:
            details['line_number'] = line_number
        super().__init__(message, details)
        self.file_path = file_path
        self.line_number = line_number


class ValidationError(DatabaseToolsException):
    """バリデーションエラー"""
    
    def __init__(self, message: str, field: Optional[str] = None, 
                 value: Optional[Any] = None, **kwargs):
        details = kwargs
        if field:
            details['field'] = field
        if value is not None:
            details['value'] = str(value)
        super().__init__(message, details)
        self.field = field
        self.value = value


class TableGenerationError(DatabaseToolsException):
    """テーブル生成エラー"""
    
    def __init__(self, message: str, table_name: Optional[str] = None, 
                 generation_type: Optional[str] = None, **kwargs):
        details = kwargs
        if table_name:
            details['table_name'] = table_name
        if generation_type:
            details['generation_type'] = generation_type
        super().__init__(message, details)
        self.table_name = table_name
        self.generation_type = generation_type


class ConsistencyCheckError(DatabaseToolsException):
    """整合性チェックエラー"""
    
    def __init__(self, message: str, check_type: Optional[str] = None, 
                 table_name: Optional[str] = None, **kwargs):
        details = kwargs
        if check_type:
            details['check_type'] = check_type
        if table_name:
            details['table_name'] = table_name
        super().__init__(message, details)
        self.check_type = check_type
        self.table_name = table_name


class DDLParsingError(DatabaseToolsException):
    """DDL解析エラー"""
    
    def __init__(self, message: str, ddl_file: Optional[Path] = None, 
                 sql_statement: Optional[str] = None, **kwargs):
        details = kwargs
        if ddl_file:
            details['ddl_file'] = str(ddl_file)
        if sql_statement:
            details['sql_statement'] = sql_statement[:200] + "..." if len(sql_statement) > 200 else sql_statement
        super().__init__(message, details)
        self.ddl_file = ddl_file
        self.sql_statement = sql_statement


class DatabaseConnectionError(DatabaseToolsException):
    """データベース接続エラー"""
    
    def __init__(self, message: str, connection_string: Optional[str] = None, **kwargs):
        details = kwargs
        if connection_string:
            # セキュリティのため、パスワード部分をマスク
            masked_connection = self._mask_password(connection_string)
            details['connection_string'] = masked_connection
        super().__init__(message, details)
        self.connection_string = connection_string
    
    def _mask_password(self, connection_string: str) -> str:
        """接続文字列のパスワード部分をマスク"""
        import re
        # パスワード部分を***でマスク
        return re.sub(r'(password=)[^;]+', r'\1***', connection_string, flags=re.IGNORECASE)


class BackupError(DatabaseToolsException):
    """バックアップエラー"""
    
    def __init__(self, message: str, source_file: Optional[Path] = None, 
                 backup_file: Optional[Path] = None, **kwargs):
        details = kwargs
        if source_file:
            details['source_file'] = str(source_file)
        if backup_file:
            details['backup_file'] = str(backup_file)
        super().__init__(message, details)
        self.source_file = source_file
        self.backup_file = backup_file


class ReportGenerationError(DatabaseToolsException):
    """レポート生成エラー"""
    
    def __init__(self, message: str, report_format: Optional[str] = None, 
                 output_file: Optional[Path] = None, **kwargs):
        details = kwargs
        if report_format:
            details['report_format'] = report_format
        if output_file:
            details['output_file'] = str(output_file)
        super().__init__(message, details)
        self.report_format = report_format
        self.output_file = output_file


class FixApplicationError(DatabaseToolsException):
    """修正適用エラー"""
    
    def __init__(self, message: str, fix_type: Optional[str] = None, 
                 target_file: Optional[Path] = None, **kwargs):
        details = kwargs
        if fix_type:
            details['fix_type'] = fix_type
        if target_file:
            details['target_file'] = str(target_file)
        super().__init__(message, details)
        self.fix_type = fix_type
        self.target_file = target_file


# 例外ハンドリングユーティリティ
class ExceptionHandler:
    """例外ハンドリングユーティリティクラス"""
    
    @staticmethod
    def handle_file_operation_error(func):
        """ファイル操作エラーのデコレータ"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (IOError, OSError, PermissionError) as e:
                raise FileOperationError(
                    f"ファイル操作エラー: {str(e)}",
                    operation=func.__name__
                ) from e
        return wrapper
    
    @staticmethod
    def handle_yaml_parsing_error(func):
        """YAML解析エラーのデコレータ"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if 'yaml' in str(e).lower():
                    raise YamlParsingError(
                        f"YAML解析エラー: {str(e)}"
                    ) from e
                raise
        return wrapper
    
    @staticmethod
    def handle_validation_error(func):
        """バリデーションエラーのデコレータ"""
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (ValueError, TypeError) as e:
                raise ValidationError(
                    f"バリデーションエラー: {str(e)}"
                ) from e
        return wrapper


# 例外情報収集ユーティリティ
def collect_exception_info(exception: Exception) -> Dict[str, Any]:
    """例外情報を収集"""
    import traceback
    import sys
    
    info = {
        'exception_type': type(exception).__name__,
        'message': str(exception),
        'traceback': traceback.format_exc(),
        'python_version': sys.version,
    }
    
    # DatabaseToolsException固有の情報
    if isinstance(exception, DatabaseToolsException):
        info['details'] = exception.details
    
    return info


def format_exception_for_user(exception: Exception) -> str:
    """ユーザー向けの例外メッセージをフォーマット"""
    if isinstance(exception, DatabaseToolsException):
        return str(exception)
    
    # 一般的な例外の場合、ユーザーフレンドリーなメッセージに変換
    exception_type = type(exception).__name__
    
    user_friendly_messages = {
        'FileNotFoundError': 'ファイルが見つかりません',
        'PermissionError': 'ファイルへのアクセス権限がありません',
        'ValueError': '入力値が不正です',
        'TypeError': 'データ型が不正です',
        'KeyError': '必要なキーが見つかりません',
        'AttributeError': '属性が見つかりません'
    }
    
    base_message = user_friendly_messages.get(exception_type, '予期しないエラーが発生しました')
    return f"{base_message}: {str(exception)}"
