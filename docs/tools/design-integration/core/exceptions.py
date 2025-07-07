"""
設計統合ツール - 例外処理モジュール
要求仕様ID: PLT.1-WEB.1

設計統合ツール固有の例外クラスを定義します。
"""

from typing import Optional, List, Dict, Any


class DesignIntegrationError(Exception):
    """設計統合ツールの基底例外クラス"""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.error_code:
            return f"[{self.error_code}] {super().__str__()}"
        return super().__str__()


class ValidationError(DesignIntegrationError):
    """検証エラー"""
    
    def __init__(self, message: str, field: Optional[str] = None, value: Optional[Any] = None, 
                 validation_errors: Optional[List[str]] = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field
        self.value = value
        self.validation_errors = validation_errors or []
    
    def add_error(self, error: str):
        """検証エラーを追加"""
        self.validation_errors.append(error)
    
    def has_errors(self) -> bool:
        """検証エラーがあるかチェック"""
        return len(self.validation_errors) > 0


class GenerationError(DesignIntegrationError):
    """生成エラー"""
    
    def __init__(self, message: str, target_type: Optional[str] = None, target_name: Optional[str] = None):
        super().__init__(message, "GENERATION_ERROR")
        self.target_type = target_type
        self.target_name = target_name


class ParseError(DesignIntegrationError):
    """解析エラー"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, line_number: Optional[int] = None):
        super().__init__(message, "PARSE_ERROR")
        self.file_path = file_path
        self.line_number = line_number


class FileOperationError(DesignIntegrationError):
    """ファイル操作エラー"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, operation: Optional[str] = None):
        super().__init__(message, "FILE_OPERATION_ERROR")
        self.file_path = file_path
        self.operation = operation


class ConfigurationError(DesignIntegrationError):
    """設定エラー"""
    
    def __init__(self, message: str, config_key: Optional[str] = None):
        super().__init__(message, "CONFIGURATION_ERROR")
        self.config_key = config_key


class IntegrationError(DesignIntegrationError):
    """統合エラー"""
    
    def __init__(self, message: str, source_type: Optional[str] = None, target_type: Optional[str] = None):
        super().__init__(message, "INTEGRATION_ERROR")
        self.source_type = source_type
        self.target_type = target_type


class RequirementMappingError(DesignIntegrationError):
    """要求仕様マッピングエラー"""
    
    def __init__(self, message: str, requirement_id: Optional[str] = None, design_type: Optional[str] = None):
        super().__init__(message, "REQUIREMENT_MAPPING_ERROR")
        self.requirement_id = requirement_id
        self.design_type = design_type


class ConsistencyError(DesignIntegrationError):
    """整合性エラー"""
    
    def __init__(self, message: str, inconsistent_items: Optional[List[str]] = None):
        super().__init__(message, "CONSISTENCY_ERROR")
        self.inconsistent_items = inconsistent_items or []


class TemplateError(DesignIntegrationError):
    """テンプレートエラー"""
    
    def __init__(self, message: str, template_name: Optional[str] = None, template_path: Optional[str] = None):
        super().__init__(message, "TEMPLATE_ERROR")
        self.template_name = template_name
        self.template_path = template_path


def handle_exception(func):
    """例外処理デコレータ"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DesignIntegrationError:
            # 既知の例外はそのまま再発生
            raise
        except FileNotFoundError as e:
            raise FileOperationError(f"ファイルが見つかりません: {e}", operation="read")
        except PermissionError as e:
            raise FileOperationError(f"ファイルアクセス権限がありません: {e}", operation="access")
        except Exception as e:
            raise DesignIntegrationError(f"予期しないエラーが発生しました: {e}")
    
    return wrapper


def format_validation_errors(errors: List[ValidationError]) -> str:
    """検証エラーのフォーマット"""
    if not errors:
        return "検証エラーはありません"
    
    formatted_errors = []
    for error in errors:
        error_msg = str(error)
        if error.field:
            error_msg = f"フィールド '{error.field}': {error_msg}"
        if error.validation_errors:
            error_msg += f" (詳細: {', '.join(error.validation_errors)})"
        formatted_errors.append(error_msg)
    
    return "\n".join(formatted_errors)


def create_error_report(errors: List[DesignIntegrationError]) -> Dict[str, Any]:
    """エラーレポートの作成"""
    report = {
        "total_errors": len(errors),
        "error_summary": {},
        "errors": []
    }
    
    # エラータイプ別の集計
    for error in errors:
        error_type = type(error).__name__
        if error_type not in report["error_summary"]:
            report["error_summary"][error_type] = 0
        report["error_summary"][error_type] += 1
        
        # エラー詳細
        error_detail = {
            "type": error_type,
            "message": str(error),
            "error_code": getattr(error, 'error_code', None),
            "details": getattr(error, 'details', {})
        }
        
        # 特定の例外タイプの追加情報
        if isinstance(error, ValidationError):
            error_detail.update({
                "field": error.field,
                "value": error.value,
                "validation_errors": error.validation_errors
            })
        elif isinstance(error, FileOperationError):
            error_detail.update({
                "file_path": error.file_path,
                "operation": error.operation
            })
        elif isinstance(error, ParseError):
            error_detail.update({
                "file_path": error.file_path,
                "line_number": error.line_number
            })
        
        report["errors"].append(error_detail)
    
    return report
