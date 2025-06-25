"""
統合データモデル定義
両ツールで使用する共通データ構造

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from pathlib import Path
from datetime import datetime


class TableCategory(Enum):
    """テーブルカテゴリ"""
    MASTER = "マスタ系"
    TRANSACTION = "トランザクション系"
    HISTORY = "履歴系"
    SYSTEM = "システム系"
    WORK = "ワーク系"
    INTERFACE = "インターフェイス系"


class Priority(Enum):
    """優先度"""
    HIGHEST = "最高"
    HIGH = "高"
    MEDIUM = "中"
    LOW = "低"


class CheckStatus(Enum):
    """チェック結果ステータス"""
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SKIPPED = "SKIPPED"
    PENDING = "pending"
    RUNNING = "running"
    FAILED = "failed"


class CheckSeverity(Enum):
    """チェック重要度"""
    SUCCESS = "success"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class GenerationStatus(Enum):
    """生成結果ステータス"""
    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class FixType(Enum):
    """修正タイプ"""
    DDL = "ddl"
    YAML = "yaml"
    INSERT = "insert"
    DEFINITION = "definition"
    ALL = "all"


class DataType(Enum):
    """データ型"""
    VARCHAR = "VARCHAR"
    TEXT = "TEXT"
    INTEGER = "INTEGER"
    BIGINT = "BIGINT"
    DECIMAL = "DECIMAL"
    BOOLEAN = "BOOLEAN"
    DATE = "DATE"
    TIMESTAMP = "TIMESTAMP"
    JSON = "JSON"
    UUID = "UUID"


@dataclass
class ColumnDefinition:
    """カラム定義"""
    name: str
    type: str
    nullable: bool = True
    primary_key: bool = False
    unique: bool = False
    default: Optional[str] = None
    comment: Optional[str] = None
    requirement_id: Optional[str] = None
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    auto_increment: bool = False
    check_constraint: Optional[str] = None
    enum_values: Optional[List[str]] = None  # ENUM型の値リスト
    
    # 旧形式との互換性のため
    primary: Optional[bool] = None
    description: Optional[str] = None
    
    def __post_init__(self):
        """初期化後の処理"""
        # データ型の正規化
        self.type = self.type.upper()
        
        # プライマリキーの場合はNULL不可
        if self.primary_key:
            self.nullable = False
    
    def to_ddl_fragment(self) -> str:
        """DDL断片を生成"""
        ddl_parts = [self.name]
        
        # データ型
        if self.length:
            ddl_parts.append(f"{self.type}({self.length})")
        elif self.precision and self.scale:
            ddl_parts.append(f"{self.type}({self.precision},{self.scale})")
        else:
            ddl_parts.append(self.type)
        
        # NULL制約
        if not self.nullable:
            ddl_parts.append("NOT NULL")
        
        # デフォルト値
        if self.default:
            ddl_parts.append(f"DEFAULT {self.default}")
        
        return " ".join(ddl_parts)


@dataclass
class IndexDefinition:
    """インデックス定義"""
    name: str
    columns: List[str]
    unique: bool = False
    comment: Optional[str] = None
    type: str = "btree"  # インデックスタイプ（btree, hash, gin, gist等）
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_ddl(self, table_name: str) -> str:
        """DDL文を生成"""
        index_type = "UNIQUE INDEX" if self.unique else "INDEX"
        columns_str = ", ".join(self.columns)
        return f"CREATE {index_type} {self.name} ON {table_name} ({columns_str});"


@dataclass
class ForeignKeyDefinition:
    """外部キー定義"""
    name: str
    columns: List[str]
    references: Dict[str, Any] = field(default_factory=dict)  # table, columns
    on_update: str = "CASCADE"
    on_delete: str = "RESTRICT"
    comment: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # 旧形式との互換性のため
    column: Optional[str] = None
    reference_table: Optional[str] = None
    reference_column: Optional[str] = None
    # DDLParser互換性のため
    references_table: Optional[str] = None
    references_columns: Optional[List[str]] = None
    
    def __post_init__(self):
        """初期化後の処理 - 旧形式との互換性"""
        if self.column and not self.columns:
            self.columns = [self.column]
        
        # DDLParser形式からreferences辞書への変換
        if self.references_table and self.references_columns:
            if not self.references:
                self.references = {
                    "table": self.references_table,
                    "columns": self.references_columns
                }
        
        # 旧形式からreferences辞書への変換
        if self.reference_table and self.reference_column:
            if not self.references:
                self.references = {
                    "table": self.reference_table,
                    "columns": [self.reference_column]
                }
        
        # references辞書からDDLParser形式への逆変換
        if self.references and not self.references_table:
            self.references_table = self.references.get("table")
            self.references_columns = self.references.get("columns", [])
    
    def to_ddl(self) -> str:
        """DDL文を生成"""
        columns_str = ", ".join(self.columns)
        ref_table = self.references["table"]
        ref_columns_str = ", ".join(self.references["columns"])
        
        return (f"CONSTRAINT {self.name} FOREIGN KEY ({columns_str}) "
                f"REFERENCES {ref_table} ({ref_columns_str}) "
                f"ON UPDATE {self.on_update} ON DELETE {self.on_delete}")


@dataclass
class ConstraintDefinition:
    """制約定義（チェック制約など）"""
    name: str
    type: str  # CHECK, UNIQUE, etc.
    columns: List[str] = field(default_factory=list)
    condition: Optional[str] = None
    comment: Optional[str] = None
    
    def to_ddl(self) -> str:
        """DDL文を生成"""
        if self.type.upper() == "CHECK" and self.condition:
            return f"CONSTRAINT {self.name} CHECK ({self.condition})"
        elif self.type.upper() == "UNIQUE":
            columns_str = ", ".join(self.columns)
            return f"CONSTRAINT {self.name} UNIQUE ({columns_str})"
        else:
            return f"CONSTRAINT {self.name} {self.type}"


@dataclass
class BusinessColumnDefinition:
    """ビジネスカラム定義（旧形式との互換性）"""
    name: str
    data_type: str
    nullable: bool = True
    primary: bool = False
    unique: bool = False
    default: Optional[str] = None
    comment: Optional[str] = None
    description: Optional[str] = None  # DDLGenerator互換性のため追加
    requirement_id: Optional[str] = None
    length: Optional[int] = None
    precision: Optional[int] = None
    scale: Optional[int] = None
    enum_values: Optional[List[str]] = None  # ENUM型の値リスト
    
    def __post_init__(self):
        """初期化後の処理"""
        # descriptionがない場合はcommentを使用
        if self.description is None:
            self.description = self.comment
    
    @property
    def type(self) -> str:
        """data_typeのエイリアス（互換性のため）"""
        return self.data_type
    
    @property
    def primary_key(self) -> bool:
        """primaryのエイリアス（互換性のため）"""
        return self.primary
    
    def to_column_definition(self) -> ColumnDefinition:
        """ColumnDefinitionに変換"""
        col_def = ColumnDefinition(
            name=self.name,
            type=self.data_type,
            nullable=self.nullable,
            primary_key=self.primary,
            unique=self.unique,
            default=self.default,
            comment=self.comment,
            requirement_id=self.requirement_id,
            length=self.length,
            precision=self.precision,
            scale=self.scale
        )
        
        # ENUM値の引き継ぎ
        if self.enum_values:
            col_def.enum_values = self.enum_values
        
        return col_def


@dataclass
class BusinessIndexDefinition:
    """ビジネスインデックス定義（旧形式との互換性）"""
    name: str
    columns: List[str]
    unique: bool = False
    comment: Optional[str] = None
    
    def to_index_definition(self) -> IndexDefinition:
        """IndexDefinitionに変換"""
        return IndexDefinition(
            name=self.name,
            columns=self.columns,
            unique=self.unique,
            comment=self.comment
        )


@dataclass
class TableDefinition:
    """統合テーブル定義モデル - 両ツールで共通使用"""
    name: str
    logical_name: str
    category: str
    priority: str
    requirement_id: str
    columns: List[ColumnDefinition] = field(default_factory=list)
    indexes: List[IndexDefinition] = field(default_factory=list)
    foreign_keys: List[ForeignKeyDefinition] = field(default_factory=list)
    comment: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # 旧形式との互換性のため
    table_name: Optional[str] = None
    description: Optional[str] = None
    business_columns: List[BusinessColumnDefinition] = field(default_factory=list)
    business_indexes: List[BusinessIndexDefinition] = field(default_factory=list)
    constraints: List[ConstraintDefinition] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # .clinerules準拠のための追加属性
    overview: Optional[str] = None
    notes: List[str] = field(default_factory=list)
    business_rules: List[str] = field(default_factory=list)
    revision_history: List[Dict[str, str]] = field(default_factory=list)
    sample_data: List[Dict[str, Any]] = field(default_factory=list)
    initial_data: List[Dict[str, Any]] = field(default_factory=list)  # InsertGenerator互換性のため
    
    def __post_init__(self):
        """初期化後の処理"""
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        # 旧形式との互換性
        if self.table_name is None:
            self.table_name = self.name
        if self.description is None:
            self.description = self.comment
    
    def get_primary_key_columns(self) -> List[ColumnDefinition]:
        """プライマリキーカラムを取得"""
        return [col for col in self.columns if col.primary_key]
    
    def get_column_by_name(self, name: str) -> Optional[ColumnDefinition]:
        """名前でカラムを取得"""
        for col in self.columns:
            if col.name == name:
                return col
        return None
    
    def has_tenant_id(self) -> bool:
        """tenant_idカラムを持つかチェック"""
        return any(col.name == "tenant_id" for col in self.columns)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'name': self.name,
            'logical_name': self.logical_name,
            'category': self.category,
            'priority': self.priority,
            'requirement_id': self.requirement_id,
            'columns': [
                {
                    'name': col.name,
                    'type': col.type,
                    'nullable': col.nullable,
                    'primary_key': col.primary_key,
                    'unique': col.unique,
                    'default': col.default,
                    'comment': col.comment,
                    'requirement_id': col.requirement_id
                }
                for col in self.columns
            ],
            'indexes': [
                {
                    'name': idx.name,
                    'columns': idx.columns,
                    'unique': idx.unique,
                    'comment': idx.comment
                }
                for idx in self.indexes
            ],
            'foreign_keys': [
                {
                    'name': fk.name,
                    'columns': fk.columns,
                    'references': fk.references,
                    'on_update': fk.on_update,
                    'on_delete': fk.on_delete
                }
                for fk in self.foreign_keys
            ],
            'comment': self.comment,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


@dataclass
class TableInfo:
    """テーブル情報（database_consistency_checker互換性）"""
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
    """カラム情報（database_consistency_checker互換性）"""
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
    """インデックス情報（database_consistency_checker互換性）"""
    name: str
    columns: List[str] = field(default_factory=list)
    unique: bool = False
    comment: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ForeignKeyInfo:
    """外部キー情報（database_consistency_checker互換性）"""
    name: str
    columns: List[str] = field(default_factory=list)
    references_table: str = ""
    references_columns: List[str] = field(default_factory=list)
    on_update: str = "RESTRICT"
    on_delete: str = "RESTRICT"
    comment: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CheckResult:
    """統合チェック結果モデル - 整合性チェック結果の統一"""
    check_name: str
    table_name: Optional[str] = None
    status: CheckStatus = CheckStatus.SUCCESS
    severity: CheckSeverity = CheckSeverity.INFO
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
    
    # 統合モデル用の追加属性
    check_type: str = ""
    fix_suggestion: Optional[str] = None
    is_valid: Optional[bool] = None
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初期化後の処理"""
        if isinstance(self.severity, str):
            self.severity = CheckSeverity(self.severity)
        if isinstance(self.status, str):
            self.status = CheckStatus(self.status)
        
        # check_typeが空の場合はcheck_nameを使用
        if not self.check_type:
            self.check_type = self.check_name
        
        # is_validが設定されていない場合は自動判定
        if self.is_valid is None:
            self.is_valid = not self.is_error()
    
    def is_error(self) -> bool:
        """エラーかどうか判定"""
        return (self.status in [CheckStatus.ERROR, CheckStatus.FAILED] or 
                self.severity in [CheckSeverity.ERROR, CheckSeverity.CRITICAL])
    
    def is_warning(self) -> bool:
        """警告かどうか判定"""
        return self.status == CheckStatus.WARNING or self.severity == CheckSeverity.WARNING
    
    def is_success(self) -> bool:
        """成功かどうか判定"""
        return (self.status == CheckStatus.SUCCESS and 
                self.severity in [CheckSeverity.SUCCESS, CheckSeverity.INFO])
    
    def set_success(self):
        """成功状態に設定"""
        self.status = CheckStatus.SUCCESS
        self.severity = CheckSeverity.SUCCESS
    
    def set_failed(self):
        """失敗状態に設定"""
        self.status = CheckStatus.FAILED
        self.severity = CheckSeverity.ERROR
    
    def add_error(self, error: str):
        """エラーを追加"""
        self.errors.append(error)
        if self.status == CheckStatus.SUCCESS:
            self.status = CheckStatus.FAILED
            self.severity = CheckSeverity.ERROR
    
    def add_warning(self, warning: str):
        """警告を追加"""
        self.warnings.append(warning)
        if self.status == CheckStatus.SUCCESS:
            self.status = CheckStatus.WARNING
            self.severity = CheckSeverity.WARNING
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'check_name': self.check_name,
            'check_type': self.check_type,
            'table_name': self.table_name,
            'status': self.status.value,
            'severity': self.severity.value,
            'message': self.message,
            'details': self.details,
            'fix_suggestion': self.fix_suggestion,
            'is_valid': self.is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


@dataclass
class CheckResultSummary:
    """チェック結果サマリー - テストコードとの互換性のため"""
    results: List[CheckResult] = field(default_factory=list)
    table_name: str = ""
    
    @property
    def is_valid(self) -> bool:
        """全体的に有効かどうか判定"""
        return len(self.errors) == 0
    
    @property
    def errors(self) -> List[CheckResult]:
        """エラー結果のリスト"""
        return [r for r in self.results if r.is_error()]
    
    @property
    def warnings(self) -> List[CheckResult]:
        """警告結果のリスト"""
        return [r for r in self.results if r.is_warning()]
    
    @property
    def successes(self) -> List[CheckResult]:
        """成功結果のリスト"""
        return [r for r in self.results if r.is_success()]
    
    def add_result(self, result: CheckResult):
        """結果を追加"""
        self.results.append(result)
    
    def add_error(self, check_type: str, table_name: str, message: str, details: Dict[str, Any] = None):
        """エラーを追加"""
        result = CheckResult(
            check_name=check_type,
            check_type=check_type,
            table_name=table_name,
            status=CheckStatus.ERROR,
            severity=CheckSeverity.ERROR,
            message=message,
            details=str(details) if details else None
        )
        self.add_result(result)
    
    def add_warning(self, check_type: str, table_name: str, message: str, details: Dict[str, Any] = None):
        """警告を追加"""
        result = CheckResult(
            check_name=check_type,
            check_type=check_type,
            table_name=table_name,
            status=CheckStatus.WARNING,
            severity=CheckSeverity.WARNING,
            message=message,
            details=str(details) if details else None
        )
        self.add_result(result)
    
    def add_success(self, check_type: str, table_name: str, message: str, details: Dict[str, Any] = None):
        """成功を追加"""
        result = CheckResult(
            check_name=check_type,
            check_type=check_type,
            table_name=table_name,
            status=CheckStatus.SUCCESS,
            severity=CheckSeverity.SUCCESS,
            message=message,
            details=str(details) if details else None
        )
        self.add_result(result)
    
    def get_error_count(self) -> int:
        """エラー数を取得"""
        return len(self.errors)
    
    def get_warning_count(self) -> int:
        """警告数を取得"""
        return len(self.warnings)
    
    def get_success_count(self) -> int:
        """成功数を取得"""
        return len(self.successes)
    
    def has_errors(self) -> bool:
        """エラーがあるかチェック"""
        return len(self.errors) > 0
    
    def has_warnings(self) -> bool:
        """警告があるかチェック"""
        return len(self.warnings) > 0
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'is_valid': self.is_valid,
            'total_results': len(self.results),
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'success_count': len(self.successes),
            'results': [r.to_dict() for r in self.results]
        }


@dataclass
class CheckSummary:
    """チェック結果サマリー（database_consistency_checker互換性）"""
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
    """修正提案（database_consistency_checker互換性）"""
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
    """検証結果（database_consistency_checker互換性）"""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    suggestions: List[FixSuggestion] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReportData:
    """レポートデータ（database_consistency_checker互換性）"""
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
        return [r for r in self.results if r.status in [CheckStatus.FAILED, CheckStatus.ERROR]]


@dataclass
class GenerationResult:
    """生成結果モデル - テーブル生成結果の統一"""
    table_name: str
    generated_files: List[Path] = field(default_factory=list)
    status: GenerationStatus = GenerationStatus.SUCCESS
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time: Optional[float] = None
    timestamp: Optional[datetime] = None
    success: bool = True
    error_message: str = ""
    processed_files: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """初期化後の処理"""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def add_generated_file(self, file_path: Path):
        """生成ファイルを追加"""
        self.generated_files.append(file_path)
    
    def add_error(self, error: str):
        """エラーを追加"""
        self.errors.append(error)
        if self.status == GenerationStatus.SUCCESS:
            self.status = GenerationStatus.PARTIAL
    
    def add_warning(self, warning: str):
        """警告を追加"""
        self.warnings.append(warning)
    
    def set_failed(self):
        """失敗状態に設定"""
        self.status = GenerationStatus.FAILED
        self.success = False
    
    def set_success(self):
        """成功状態に設定"""
        self.status = GenerationStatus.SUCCESS
        self.success = True
    
    def is_success(self) -> bool:
        """成功かどうか判定"""
        return self.status == GenerationStatus.SUCCESS
    
    def is_failed(self) -> bool:
        """失敗かどうか判定"""
        return self.status == GenerationStatus.FAILED
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'table_name': self.table_name,
            'generated_files': [str(f) for f in self.generated_files],
            'status': self.status.value,
            'errors': self.errors,
            'warnings': self.warnings,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'success': self.success,
            'error_message': self.error_message,
            'processed_files': self.processed_files
        }


@dataclass
class ProcessingResult:
    """処理結果モデル - 個別テーブル処理結果"""
    table_name: str
    logical_name: str = ""
    success: bool = True
    has_yaml: bool = False
    error_message: str = ""
    generated_files: List[str] = field(default_factory=list)
    processed_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    execution_time: Optional[float] = None
    timestamp: Optional[datetime] = None
    
    def __post_init__(self):
        """初期化後の処理"""
        if self.timestamp is None:
            self.timestamp = datetime.now()
    
    def add_error(self, error: str):
        """エラーを追加"""
        self.errors.append(error)
        self.success = False
    
    def add_warning(self, warning: str):
        """警告を追加"""
        self.warnings.append(warning)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'table_name': self.table_name,
            'logical_name': self.logical_name,
            'success': self.success,
            'has_yaml': self.has_yaml,
            'error_message': self.error_message,
            'generated_files': self.generated_files,
            'processed_files': self.processed_files,
            'errors': self.errors,
            'warnings': self.warnings,
            'execution_time': self.execution_time,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }


@dataclass
class ConsistencyReport:
    """整合性チェックレポート（database_consistency_checker互換性）"""
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
        return [r for r in self.results if r.status in [CheckStatus.FAILED, CheckStatus.ERROR]]
    
    @classmethod
    def from_report_data(cls, report_data: ReportData) -> 'ConsistencyReport':
        """ReportDataから変換"""
        return cls(
            summary=report_data.summary.__dict__,
            results=report_data.results,
            tables=report_data.tables,
            suggestions=report_data.suggestions,
            metadata=report_data.metadata,
            generated_at=report_data.generated_at
        )


@dataclass
class CheckConfig:
    """チェック設定（database_consistency_checker互換性）"""
    enabled_checks: List[str] = field(default_factory=list)
    disabled_checks: List[str] = field(default_factory=list)
    check_parameters: Dict[str, Any] = field(default_factory=dict)
    output_format: str = "json"
    verbose: bool = False
    fail_fast: bool = False
    
    def is_check_enabled(self, check_name: str) -> bool:
        """チェックが有効かどうか判定"""
        if self.disabled_checks and check_name in self.disabled_checks:
            return False
        if self.enabled_checks:
            return check_name in self.enabled_checks
        return True


@dataclass
class TableListEntry:
    """テーブルリストエントリ（database_consistency_checker互換性）"""
    name: str
    logical_name: str = ""
    category: str = ""
    priority: str = ""
    requirement_id: str = ""
    yaml_file: Optional[str] = None
    ddl_file: Optional[str] = None
    definition_file: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'name': self.name,
            'logical_name': self.logical_name,
            'category': self.category,
            'priority': self.priority,
            'requirement_id': self.requirement_id,
            'yaml_file': self.yaml_file,
            'ddl_file': self.ddl_file,
            'definition_file': self.definition_file
        }


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
