"""
統一例外クラス定義
データベースツール統合における統一エラーハンドリング

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum


class ErrorSeverity(Enum):
    """エラー重要度定義"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorCategory(Enum):
    """エラーカテゴリ定義"""
    VALIDATION = "validation"
    FILE_OPERATION = "file_operation"
    MODEL_CONVERSION = "model_conversion"
    PARSING = "parsing"
    GENERATION = "generation"
    CONSISTENCY_CHECK = "consistency_check"
    CONFIGURATION = "configuration"
    SYSTEM = "system"


class DatabaseToolsException(Exception):
    """統一例外基底クラス"""
    
    def __init__(
        self,
        message: str,
        error_code: str = None,
        category: ErrorCategory = ErrorCategory.SYSTEM,
        severity: ErrorSeverity = ErrorSeverity.MEDIUM,
        details: Optional[Dict[str, Any]] = None,
        suggestion: Optional[str] = None,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self._generate_error_code()
        self.category = category
        self.severity = severity
        self.details = details or {}
        self.suggestion = suggestion
        self.file_path = file_path
        self.line_number = line_number
        self.timestamp = datetime.now()
    
    def _generate_error_code(self) -> str:
        """エラーコード自動生成"""
        class_name = self.__class__.__name__
        timestamp = self.timestamp.strftime("%Y%m%d%H%M%S")
        return f"{class_name}_{timestamp}"
    
    def to_dict(self) -> Dict[str, Any]:
        """例外情報を辞書形式で取得"""
        return {
            'error_code': self.error_code,
            'message': self.message,
            'category': self.category.value,
            'severity': self.severity.value,
            'details': self.details,
            'suggestion': self.suggestion,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'timestamp': self.timestamp.isoformat(),
            'exception_type': self.__class__.__name__
        }
    
    def __str__(self) -> str:
        """文字列表現"""
        parts = [f"[{self.error_code}] {self.message}"]
        
        if self.file_path:
            location = self.file_path
            if self.line_number:
                location += f":{self.line_number}"
            parts.append(f"Location: {location}")
        
        if self.suggestion:
            parts.append(f"Suggestion: {self.suggestion}")
        
        return " | ".join(parts)


class ValidationError(DatabaseToolsException):
    """バリデーションエラー"""
    
    def __init__(
        self,
        message: str,
        field_name: Optional[str] = None,
        field_value: Any = None,
        validation_rule: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.VALIDATION,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        self.field_name = field_name
        self.field_value = field_value
        self.validation_rule = validation_rule
        
        # 詳細情報を追加
        if field_name:
            self.details['field_name'] = field_name
        if field_value is not None:
            self.details['field_value'] = str(field_value)
        if validation_rule:
            self.details['validation_rule'] = validation_rule


class FileOperationError(DatabaseToolsException):
    """ファイル操作エラー"""
    
    def __init__(
        self,
        message: str,
        operation: Optional[str] = None,
        file_path: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.FILE_OPERATION,
            severity=ErrorSeverity.HIGH,
            file_path=file_path,
            **kwargs
        )
        self.operation = operation
        
        if operation:
            self.details['operation'] = operation


class ModelConversionError(DatabaseToolsException):
    """モデル変換エラー"""
    
    def __init__(
        self,
        message: str,
        source_model: Optional[str] = None,
        target_model: Optional[str] = None,
        conversion_step: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.MODEL_CONVERSION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        self.source_model = source_model
        self.target_model = target_model
        self.conversion_step = conversion_step
        
        if source_model:
            self.details['source_model'] = source_model
        if target_model:
            self.details['target_model'] = target_model
        if conversion_step:
            self.details['conversion_step'] = conversion_step


class ParsingError(DatabaseToolsException):
    """解析エラー"""
    
    def __init__(
        self,
        message: str,
        parser_type: Optional[str] = None,
        source_format: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.PARSING,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        self.parser_type = parser_type
        self.source_format = source_format
        
        if parser_type:
            self.details['parser_type'] = parser_type
        if source_format:
            self.details['source_format'] = source_format


class GenerationError(DatabaseToolsException):
    """生成エラー"""
    
    def __init__(
        self,
        message: str,
        generator_type: Optional[str] = None,
        target_format: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.GENERATION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        self.generator_type = generator_type
        self.target_format = target_format
        
        if generator_type:
            self.details['generator_type'] = generator_type
        if target_format:
            self.details['target_format'] = target_format


class ConsistencyCheckError(DatabaseToolsException):
    """整合性チェックエラー"""
    
    def __init__(
        self,
        message: str,
        check_type: Optional[str] = None,
        inconsistency_details: Optional[List[Dict]] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.CONSISTENCY_CHECK,
            severity=ErrorSeverity.MEDIUM,
            **kwargs
        )
        self.check_type = check_type
        self.inconsistency_details = inconsistency_details or []
        
        if check_type:
            self.details['check_type'] = check_type
        if inconsistency_details:
            self.details['inconsistency_count'] = len(inconsistency_details)
            self.details['inconsistencies'] = inconsistency_details


class ConfigurationError(DatabaseToolsException):
    """設定エラー"""
    
    def __init__(
        self,
        message: str,
        config_key: Optional[str] = None,
        config_value: Any = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.CONFIGURATION,
            severity=ErrorSeverity.HIGH,
            **kwargs
        )
        self.config_key = config_key
        self.config_value = config_value
        
        if config_key:
            self.details['config_key'] = config_key
        if config_value is not None:
            self.details['config_value'] = str(config_value)


class SystemError(DatabaseToolsException):
    """システムエラー"""
    
    def __init__(
        self,
        message: str,
        system_component: Optional[str] = None,
        **kwargs
    ):
        super().__init__(
            message,
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            **kwargs
        )
        self.system_component = system_component
        
        if system_component:
            self.details['system_component'] = system_component


# 例外ハンドリングユーティリティ
class ExceptionHandler:
    """統一例外ハンドリングユーティリティ"""
    
    @staticmethod
    def handle_and_log(exception: DatabaseToolsException, logger=None):
        """例外をログに記録"""
        if logger:
            log_method = {
                ErrorSeverity.LOW: logger.debug,
                ErrorSeverity.MEDIUM: logger.warning,
                ErrorSeverity.HIGH: logger.error,
                ErrorSeverity.CRITICAL: logger.critical
            }.get(exception.severity, logger.error)
            
            log_method(f"Exception occurred: {exception}")
            if exception.details:
                logger.debug(f"Exception details: {exception.details}")
    
    @staticmethod
    def create_error_report(exceptions: List[DatabaseToolsException]) -> Dict[str, Any]:
        """例外リストからエラーレポートを生成"""
        if not exceptions:
            return {'total_errors': 0, 'errors': []}
        
        # カテゴリ別集計
        category_counts = {}
        severity_counts = {}
        
        error_list = []
        for exc in exceptions:
            error_list.append(exc.to_dict())
            
            # カテゴリ別カウント
            category = exc.category.value
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # 重要度別カウント
            severity = exc.severity.value
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        return {
            'total_errors': len(exceptions),
            'category_summary': category_counts,
            'severity_summary': severity_counts,
            'errors': error_list,
            'generated_at': datetime.now().isoformat()
        }


# 便利な例外生成関数
def validation_error(message: str, field_name: str = None, **kwargs) -> ValidationError:
    """バリデーションエラー生成"""
    return ValidationError(message, field_name=field_name, **kwargs)


def file_not_found_error(file_path: str, **kwargs) -> FileOperationError:
    """ファイル未発見エラー生成"""
    return FileOperationError(
        f"File not found: {file_path}",
        operation="read",
        file_path=file_path,
        suggestion="Check if the file path is correct and the file exists",
        **kwargs
    )


def parsing_error(message: str, file_path: str = None, **kwargs) -> ParsingError:
    """解析エラー生成"""
    return ParsingError(
        message,
        file_path=file_path,
        suggestion="Check the file format and syntax",
        **kwargs
    )


def model_conversion_error(source: str, target: str, **kwargs) -> ModelConversionError:
    """モデル変換エラー生成"""
    return ModelConversionError(
        f"Failed to convert from {source} to {target}",
        source_model=source,
        target_model=target,
        **kwargs
    )
