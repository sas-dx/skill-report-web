"""
データベース整合性チェックツール - データモデル
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime


class CheckSeverity(Enum):
    """チェック結果の重要度"""
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class CheckStatus(Enum):
    """チェック実行状況"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


class FixType(Enum):
    """修正タイプ"""
    DDL = "ddl"
    YAML = "yaml"
    INSERT = "insert"
    DEFINITION = "definition"
    ALL = "all"


@dataclass
class CheckResult:
    """チェック結果"""
    check_name: str
    table_name: Optional[str] = None
    severity: CheckSeverity = CheckSeverity.INFO
    status: CheckStatus = CheckStatus.PENDING
    message: str = ""
    details: Optional[str] = None
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    column_name: Optional[str] = None
    expected_value: Optional[str] = None
    actual_value: Optional[str] = None
    suggestion: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """初期化後の処理"""
        if isinstance(self.severity, str):
            self.severity = CheckSeverity(self.severity)
        if isinstance(self.status, str):
            self.status = CheckStatus(self.status)


@dataclass
class TableInfo:
    """テーブル情報"""
    name: str
    logical_name: str = ""
    category: str = ""
    priority: str = ""
    requirement_id: str = ""
    comment: str = ""
    yaml_file: Optional[str] = None
    ddl_file: Optional[str] = None
    definition_file: Optional[str] = None
    columns: List[Dict[str, Any]] = field(default_factory=list)
    indexes: List[Dict[str, Any]] = field(default_factory=list)
    foreign_keys: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ColumnInfo:
    """カラム情報"""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Optional[str] = None
    comment: str = ""
    requirement_id: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IndexInfo:
    """インデックス情報"""
    name: str
    columns: List[str] = field(default_factory=list)
    unique: bool = False
    comment: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ForeignKeyInfo:
    """外部キー情報"""
    name: str
    columns: List[str] = field(default_factory=list)
    references_table: str = ""
    references_columns: List[str] = field(default_factory=list)
    on_update: str = "RESTRICT"
    on_delete: str = "RESTRICT"
    comment: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CheckSummary:
    """チェック結果サマリー"""
    total_checks: int = 0
    passed_checks: int = 0
    failed_checks: int = 0
    skipped_checks: int = 0
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0
    critical_count: int = 0
    execution_time: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        """成功率を計算"""
        if self.total_checks == 0:
            return 0.0
        return (self.passed_checks / self.total_checks) * 100
    
    @property
    def has_errors(self) -> bool:
        """エラーがあるかどうか"""
        return self.error_count > 0 or self.critical_count > 0


@dataclass
class FixSuggestion:
    """修正提案"""
    fix_type: str  # ddl, yaml, insert
    target_file: str
    description: str
    before_content: Optional[str] = None
    after_content: Optional[str] = None
    line_number: Optional[int] = None
    confidence: float = 1.0  # 0.0-1.0
    risk_level: str = "low"  # low, medium, high
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """検証結果"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[FixSuggestion] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReportData:
    """レポートデータ"""
    summary: CheckSummary
    results: List[CheckResult] = field(default_factory=list)
    tables: List[TableInfo] = field(default_factory=list)
    suggestions: List[FixSuggestion] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.now)
    
    def get_results_by_severity(self, severity: CheckSeverity) -> List[CheckResult]:
        """重要度別の結果を取得"""
        return [r for r in self.results if r.severity == severity]
    
    def get_results_by_table(self, table_name: str) -> List[CheckResult]:
        """テーブル別の結果を取得"""
        return [r for r in self.results if r.table_name == table_name]
    
    def get_failed_results(self) -> List[CheckResult]:
        """失敗した結果を取得"""
        return [r for r in self.results if r.status == CheckStatus.FAILED]


@dataclass
class ConsistencyReport:
    """整合性チェックレポート（ReportDataのエイリアス）"""
    summary: Dict[str, int] = field(default_factory=dict)
    results: List[CheckResult] = field(default_factory=list)
    tables: List[TableInfo] = field(default_factory=list)
    suggestions: List[FixSuggestion] = field(default_factory=list)
    fix_suggestions: List[FixSuggestion] = field(default_factory=list)  # エイリアス
    metadata: Dict[str, Any] = field(default_factory=dict)
    generated_at: datetime = field(default_factory=datetime.now)
    check_date: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    total_tables: int = 0
    total_checks: int = 0
    
    def get_results_by_severity(self, severity: CheckSeverity) -> List[CheckResult]:
        """重要度別の結果を取得"""
        return [r for r in self.results if r.severity == severity]
    
    def get_results_by_table(self, table_name: str) -> List[CheckResult]:
        """テーブル別の結果を取得"""
        return [r for r in self.results if r.table_name == table_name]
    
    def get_failed_results(self) -> List[CheckResult]:
        """失敗した結果を取得"""
        return [r for r in self.results if r.status == CheckStatus.FAILED]
    
    @classmethod
    def from_report_data(cls, report_data: ReportData) -> 'ConsistencyReport':
        """ReportDataから変換"""
        return cls(
            summary=report_data.summary,
            results=report_data.results,
            tables=report_data.tables,
            suggestions=report_data.suggestions,
            metadata=report_data.metadata,
            generated_at=report_data.generated_at
        )


# ユーティリティ関数
def create_check_result(
    check_name: str,
    table_name: Optional[str] = None,
    severity: Union[CheckSeverity, str] = CheckSeverity.INFO,
    status: Union[CheckStatus, str] = CheckStatus.SUCCESS,
    message: str = "",
    **kwargs
) -> CheckResult:
    """チェック結果を作成するヘルパー関数"""
    if isinstance(severity, str):
        severity = CheckSeverity(severity)
    if isinstance(status, str):
        status = CheckStatus(status)
    
    return CheckResult(
        check_name=check_name,
        table_name=table_name,
        severity=severity,
        status=status,
        message=message,
        **kwargs
    )


def create_error_result(
    check_name: str,
    message: str,
    table_name: Optional[str] = None,
    **kwargs
) -> CheckResult:
    """エラー結果を作成するヘルパー関数"""
    return create_check_result(
        check_name=check_name,
        table_name=table_name,
        severity=CheckSeverity.ERROR,
        status=CheckStatus.FAILED,
        message=message,
        **kwargs
    )


def create_warning_result(
    check_name: str,
    message: str,
    table_name: Optional[str] = None,
    **kwargs
) -> CheckResult:
    """警告結果を作成するヘルパー関数"""
    return create_check_result(
        check_name=check_name,
        table_name=table_name,
        severity=CheckSeverity.WARNING,
        status=CheckStatus.SUCCESS,
        message=message,
        **kwargs
    )


def create_info_result(
    check_name: str,
    message: str,
    table_name: Optional[str] = None,
    **kwargs
) -> CheckResult:
    """情報結果を作成するヘルパー関数"""
    return create_check_result(
        check_name=check_name,
        table_name=table_name,
        severity=CheckSeverity.INFO,
        status=CheckStatus.SUCCESS,
        message=message,
        **kwargs
    )


def create_success_result(
    check_name: str,
    message: str,
    table_name: Optional[str] = None,
    **kwargs
) -> CheckResult:
    """成功結果を作成するヘルパー関数"""
    return create_check_result(
        check_name=check_name,
        table_name=table_name,
        severity=CheckSeverity.SUCCESS,
        status=CheckStatus.SUCCESS,
        message=message,
        **kwargs
    )
