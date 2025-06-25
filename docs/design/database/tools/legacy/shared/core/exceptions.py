"""
統合例外処理システム
全ツールで使用する共通例外クラス

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-25
実装者: AI駆動開発チーム
"""

from typing import Optional, Dict, Any, List
from pathlib import Path


class DatabaseToolsError(Exception):
    """データベースツール基底例外クラス"""
    
    def __init__(
        self, 
        message: str, 
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        suggestions: Optional[List[str]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.suggestions = suggestions or []
    
    def to_dict(self) -> Dict[str, Any]:
        """例外情報を辞書形式で取得"""
        return {
            'error_type': self.__class__.__name__,
            'error_code': self.error_code,
            'message': self.message,
            'details': self.details,
            'suggestions': self.suggestions
        }


class ConfigurationError(DatabaseToolsError):
    """設定関連エラー"""
    pass


class FileOperationError(DatabaseToolsError):
    """ファイル操作エラー"""
    
    def __init__(
        self, 
        message: str, 
        file_path: Optional[Path] = None,
        operation: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.file_path = file_path
        self.operation = operation
        if file_path:
            self.details['file_path'] = str(file_path)
        if operation:
            self.details['operation'] = operation


class ValidationError(DatabaseToolsError):
    """検証エラー"""
    
    def __init__(
        self, 
        message: str, 
        field: Optional[str] = None,
        value: Optional[Any] = None,
        expected: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.field = field
        self.value = value
        self.expected = expected
        
        if field:
            self.details['field'] = field
        if value is not None:
            self.details['value'] = str(value)
        if expected:
            self.details['expected'] = expected


class YamlFormatError(ValidationError):
    """YAML形式エラー"""
    
    def __init__(
        self, 
        message: str, 
        file_path: Optional[Path] = None,
        line_number: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.file_path = file_path
        self.line_number = line_number
        
        if file_path:
            self.details['file_path'] = str(file_path)
        if line_number:
            self.details['line_number'] = line_number


class TableDefinitionError(DatabaseToolsError):
    """テーブル定義エラー"""
    
    def __init__(
        self, 
        message: str, 
        table_name: Optional[str] = None,
        column_name: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.table_name = table_name
        self.column_name = column_name
        
        if table_name:
            self.details['table_name'] = table_name
        if column_name:
            self.details['column_name'] = column_name


class ConsistencyError(DatabaseToolsError):
    """整合性エラー"""
    
    def __init__(
        self, 
        message: str, 
        source_file: Optional[Path] = None,
        target_file: Optional[Path] = None,
        inconsistency_type: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.source_file = source_file
        self.target_file = target_file
        self.inconsistency_type = inconsistency_type
        
        if source_file:
            self.details['source_file'] = str(source_file)
        if target_file:
            self.details['target_file'] = str(target_file)
        if inconsistency_type:
            self.details['inconsistency_type'] = inconsistency_type


class DatabaseConnectionError(DatabaseToolsError):
    """データベース接続エラー"""
    
    def __init__(
        self, 
        message: str, 
        host: Optional[str] = None,
        port: Optional[int] = None,
        database: Optional[str] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.host = host
        self.port = port
        self.database = database
        
        if host:
            self.details['host'] = host
        if port:
            self.details['port'] = port
        if database:
            self.details['database'] = database


class GenerationError(DatabaseToolsError):
    """生成処理エラー"""
    
    def __init__(
        self, 
        message: str, 
        generation_type: Optional[str] = None,
        target_file: Optional[Path] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.generation_type = generation_type
        self.target_file = target_file
        
        if generation_type:
            self.details['generation_type'] = generation_type
        if target_file:
            self.details['target_file'] = str(target_file)


class ParsingError(DatabaseToolsError):
    """解析エラー"""
    
    def __init__(
        self, 
        message: str, 
        parser_type: Optional[str] = None,
        source_file: Optional[Path] = None,
        line_number: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.parser_type = parser_type
        self.source_file = source_file
        self.line_number = line_number
        
        if parser_type:
            self.details['parser_type'] = parser_type
        if source_file:
            self.details['source_file'] = str(source_file)
        if line_number:
            self.details['line_number'] = line_number


class ToolExecutionError(DatabaseToolsError):
    """ツール実行エラー"""
    
    def __init__(
        self, 
        message: str, 
        tool_name: Optional[str] = None,
        command: Optional[str] = None,
        exit_code: Optional[int] = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.tool_name = tool_name
        self.command = command
        self.exit_code = exit_code
        
        if tool_name:
            self.details['tool_name'] = tool_name
        if command:
            self.details['command'] = command
        if exit_code is not None:
            self.details['exit_code'] = exit_code


def handle_exception(
    exception: Exception, 
    logger=None, 
    context: Optional[Dict[str, Any]] = None
) -> DatabaseToolsError:
    """
    例外を統一形式で処理
    
    Args:
        exception: 発生した例外
        logger: ログ出力用ロガー
        context: 追加のコンテキスト情報
        
    Returns:
        DatabaseToolsError: 統一形式の例外
    """
    context = context or {}
    
    # 既にDatabaseToolsErrorの場合はそのまま返す
    if isinstance(exception, DatabaseToolsError):
        if logger:
            logger.error(f"ツールエラー: {exception.message}", extra=exception.details)
        return exception
    
    # 標準例外を統一形式に変換
    if isinstance(exception, FileNotFoundError):
        error = FileOperationError(
            message=f"ファイルが見つかりません: {exception}",
            operation="read",
            details=context
        )
    elif isinstance(exception, PermissionError):
        error = FileOperationError(
            message=f"ファイルアクセス権限がありません: {exception}",
            operation="access",
            details=context
        )
    elif isinstance(exception, ValueError):
        error = ValidationError(
            message=f"値が無効です: {exception}",
            details=context
        )
    elif isinstance(exception, KeyError):
        error = ValidationError(
            message=f"必須キーが見つかりません: {exception}",
            details=context
        )
    else:
        error = DatabaseToolsError(
            message=f"予期しないエラー: {exception}",
            error_code="UNEXPECTED_ERROR",
            details=context
        )
    
    if logger:
        logger.error(f"例外処理: {error.message}", extra=error.details)
    
    return error


def create_suggestion_list(error_type: str, details: Dict[str, Any]) -> List[str]:
    """
    エラータイプに基づいて修正提案を生成
    
    Args:
        error_type: エラータイプ
        details: エラー詳細情報
        
    Returns:
        List[str]: 修正提案リスト
    """
    suggestions = []
    
    if error_type == "FileNotFoundError":
        suggestions.extend([
            "ファイルパスが正しいか確認してください",
            "ファイルが存在するか確認してください",
            "相対パスではなく絶対パスを使用してみてください"
        ])
    
    elif error_type == "YamlFormatError":
        suggestions.extend([
            "YAML構文が正しいか確認してください",
            "インデントが正しいか確認してください",
            "必須セクションが存在するか確認してください"
        ])
    
    elif error_type == "ValidationError":
        suggestions.extend([
            "入力値の形式を確認してください",
            "必須項目が入力されているか確認してください",
            "データ型が正しいか確認してください"
        ])
    
    elif error_type == "ConsistencyError":
        suggestions.extend([
            "関連ファイル間の整合性を確認してください",
            "自動修正ツールの使用を検討してください",
            "手動で不整合箇所を修正してください"
        ])
    
    elif error_type == "DatabaseConnectionError":
        suggestions.extend([
            "データベースサーバーが起動しているか確認してください",
            "接続設定（ホスト、ポート、認証情報）を確認してください",
            "ネットワーク接続を確認してください"
        ])
    
    return suggestions
