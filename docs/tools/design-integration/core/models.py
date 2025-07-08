"""
設計統合ツール - データモデルモジュール
要求仕様ID: PLT.1-WEB.1

設計統合ツールで使用するデータモデルを定義します。
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum
from pathlib import Path


class DesignType(Enum):
    """設計タイプ"""
    DATABASE = "database"
    API = "api"
    SCREEN = "screen"
    ARCHITECTURE = "architecture"
    INTERFACE = "interface"


class ValidationStatus(Enum):
    """検証ステータス"""
    VALID = "valid"
    INVALID = "invalid"
    WARNING = "warning"
    NOT_CHECKED = "not_checked"


class GenerationStatus(Enum):
    """生成ステータス"""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    IN_PROGRESS = "in_progress"


@dataclass
class RequirementMapping:
    """要求仕様マッピング"""
    requirement_id: str
    design_type: DesignType
    design_id: str
    design_name: str
    file_path: Optional[str] = None
    status: ValidationStatus = ValidationStatus.NOT_CHECKED
    last_updated: Optional[datetime] = None
    
    def __post_init__(self):
        if self.last_updated is None:
            self.last_updated = datetime.now()


@dataclass
class ValidationResult:
    """検証結果"""
    target: str
    status: ValidationStatus
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_error(self, error: str):
        """エラーを追加"""
        self.errors.append(error)
        if self.status == ValidationStatus.VALID:
            self.status = ValidationStatus.INVALID
    
    def add_warning(self, warning: str):
        """警告を追加"""
        self.warnings.append(warning)
        if self.status == ValidationStatus.VALID:
            self.status = ValidationStatus.WARNING
    
    def is_valid(self) -> bool:
        """有効かどうか"""
        return self.status in [ValidationStatus.VALID, ValidationStatus.WARNING]
    
    def has_errors(self) -> bool:
        """エラーがあるかどうか"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """警告があるかどうか"""
        return len(self.warnings) > 0


@dataclass
class GenerationResult:
    """生成結果"""
    target: str
    status: GenerationStatus
    output_path: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_error(self, error: str):
        """エラーを追加"""
        self.errors.append(error)
        if self.status == GenerationStatus.SUCCESS:
            self.status = GenerationStatus.FAILED
    
    def add_warning(self, warning: str):
        """警告を追加"""
        self.warnings.append(warning)
    
    def is_success(self) -> bool:
        """成功かどうか"""
        return self.status == GenerationStatus.SUCCESS
    
    def has_errors(self) -> bool:
        """エラーがあるかどうか"""
        return len(self.errors) > 0


@dataclass
class DesignDocument:
    """設計書ドキュメント"""
    design_id: str
    design_type: DesignType
    name: str
    file_path: str
    requirement_id: Optional[str] = None
    content: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_result: Optional[ValidationResult] = None
    generation_result: Optional[GenerationResult] = None
    last_modified: Optional[datetime] = None
    
    def __post_init__(self):
        if self.last_modified is None and Path(self.file_path).exists():
            self.last_modified = datetime.fromtimestamp(Path(self.file_path).stat().st_mtime)
    
    def is_valid(self) -> bool:
        """有効かどうか"""
        return self.validation_result is not None and self.validation_result.is_valid()
    
    def needs_regeneration(self) -> bool:
        """再生成が必要かどうか"""
        return (self.generation_result is None or 
                self.generation_result.status == GenerationStatus.FAILED or
                (self.last_modified and self.generation_result.timestamp < self.last_modified))


@dataclass
class IntegrationResult:
    """統合結果"""
    operation: str
    total_items: int
    success_count: int = 0
    error_count: int = 0
    warning_count: int = 0
    validation_results: List[ValidationResult] = field(default_factory=list)
    generation_results: List[GenerationResult] = field(default_factory=list)
    requirement_mappings: List[RequirementMapping] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    duration: Optional[float] = None
    
    def add_validation_result(self, result: ValidationResult):
        """検証結果を追加"""
        self.validation_results.append(result)
        if result.has_errors():
            self.error_count += 1
        elif result.has_warnings():
            self.warning_count += 1
        else:
            self.success_count += 1
    
    def add_generation_result(self, result: GenerationResult):
        """生成結果を追加"""
        self.generation_results.append(result)
        if result.is_success():
            self.success_count += 1
        else:
            self.error_count += 1
    
    def add_error(self, error: str):
        """エラーを追加"""
        self.errors.append(error)
        self.error_count += 1
    
    def add_warning(self, warning: str):
        """警告を追加"""
        self.warnings.append(warning)
        self.warning_count += 1
    
    def is_success(self) -> bool:
        """成功かどうか"""
        return self.error_count == 0
    
    def get_success_rate(self) -> float:
        """成功率を取得"""
        if self.total_items == 0:
            return 0.0
        return self.success_count / self.total_items
    
    def get_summary(self) -> Dict[str, Any]:
        """サマリーを取得"""
        return {
            "operation": self.operation,
            "total_items": self.total_items,
            "success_count": self.success_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "success_rate": self.get_success_rate(),
            "duration": self.duration,
            "timestamp": self.timestamp.isoformat(),
            "is_success": self.is_success()
        }


@dataclass
class DatabaseTable:
    """データベーステーブル"""
    table_name: str
    logical_name: str
    category: str
    priority: str
    requirement_id: str
    yaml_path: str
    ddl_path: Optional[str] = None
    definition_path: Optional[str] = None
    columns: List[Dict[str, Any]] = field(default_factory=list)
    indexes: List[Dict[str, Any]] = field(default_factory=list)
    foreign_keys: List[Dict[str, Any]] = field(default_factory=list)
    validation_result: Optional[ValidationResult] = None
    
    def get_column_count(self) -> int:
        """カラム数を取得"""
        return len(self.columns)
    
    def has_primary_key(self) -> bool:
        """主キーがあるかどうか"""
        return any(col.get('primary_key', False) for col in self.columns)


@dataclass
class APIEndpoint:
    """APIエンドポイント"""
    api_id: str
    endpoint: str
    method: str
    name: str
    requirement_id: str
    spec_path: str
    yaml_path: Optional[str] = None
    parameters: List[Dict[str, Any]] = field(default_factory=list)
    responses: List[Dict[str, Any]] = field(default_factory=list)
    validation_result: Optional[ValidationResult] = None
    
    def get_parameter_count(self) -> int:
        """パラメータ数を取得"""
        return len(self.parameters)
    
    def get_response_count(self) -> int:
        """レスポンス数を取得"""
        return len(self.responses)


@dataclass
class ScreenDesign:
    """画面設計"""
    screen_id: str
    screen_name: str
    requirement_id: str
    spec_path: str
    yaml_path: Optional[str] = None
    components: List[Dict[str, Any]] = field(default_factory=list)
    navigation: List[Dict[str, Any]] = field(default_factory=list)
    validation_result: Optional[ValidationResult] = None
    
    def get_component_count(self) -> int:
        """コンポーネント数を取得"""
        return len(self.components)
    
    def get_navigation_count(self) -> int:
        """ナビゲーション数を取得"""
        return len(self.navigation)


@dataclass
class DesignIntegrationReport:
    """設計統合レポート"""
    title: str
    generated_at: datetime
    database_results: List[ValidationResult] = field(default_factory=list)
    api_results: List[ValidationResult] = field(default_factory=list)
    screen_results: List[ValidationResult] = field(default_factory=list)
    integration_results: List[IntegrationResult] = field(default_factory=list)
    requirement_mappings: List[RequirementMapping] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.summary:
            self.summary = self._generate_summary()
    
    def _generate_summary(self) -> Dict[str, Any]:
        """サマリーを生成"""
        total_database = len(self.database_results)
        valid_database = sum(1 for r in self.database_results if r.is_valid())
        
        total_api = len(self.api_results)
        valid_api = sum(1 for r in self.api_results if r.is_valid())
        
        total_screen = len(self.screen_results)
        valid_screen = sum(1 for r in self.screen_results if r.is_valid())
        
        total_mappings = len(self.requirement_mappings)
        valid_mappings = sum(1 for m in self.requirement_mappings if m.status == ValidationStatus.VALID)
        
        return {
            "database": {
                "total": total_database,
                "valid": valid_database,
                "success_rate": valid_database / total_database if total_database > 0 else 0
            },
            "api": {
                "total": total_api,
                "valid": valid_api,
                "success_rate": valid_api / total_api if total_api > 0 else 0
            },
            "screen": {
                "total": total_screen,
                "valid": valid_screen,
                "success_rate": valid_screen / total_screen if total_screen > 0 else 0
            },
            "requirement_mappings": {
                "total": total_mappings,
                "valid": valid_mappings,
                "success_rate": valid_mappings / total_mappings if total_mappings > 0 else 0
            },
            "overall": {
                "total_items": total_database + total_api + total_screen,
                "valid_items": valid_database + valid_api + valid_screen,
                "overall_success_rate": (valid_database + valid_api + valid_screen) / (total_database + total_api + total_screen) if (total_database + total_api + total_screen) > 0 else 0
            }
        }
