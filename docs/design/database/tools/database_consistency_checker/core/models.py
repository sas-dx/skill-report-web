"""
データベース整合性チェックツール - データモデル定義
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum


class CheckSeverity(Enum):
    """チェック結果の重要度"""
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    INFO = "info"


class FixType(Enum):
    """修正提案の種類"""
    DDL = "ddl"
    YAML = "yaml"
    INSERT = "insert"
    ALL = "all"


@dataclass
class ColumnDefinition:
    """カラム定義"""
    name: str
    logical_name: str = ""
    data_type: str = ""
    length: Optional[int] = None
    nullable: bool = True
    unique: bool = False
    primary_key: bool = False
    foreign_key: bool = False
    default_value: Optional[str] = None
    comment: str = ""
    encrypted: bool = False
    enum_values: List[str] = field(default_factory=list)
    validation: str = ""


@dataclass
class IndexDefinition:
    """インデックス定義"""
    name: str
    columns: List[str]
    unique: bool = False
    description: str = ""


@dataclass
class ForeignKeyDefinition:
    """外部キー定義"""
    name: str
    column: str
    reference_table: str
    reference_column: str
    on_update: str = "CASCADE"
    on_delete: str = "RESTRICT"
    description: str = ""


@dataclass
class ConstraintDefinition:
    """制約定義"""
    name: str
    type: str  # UNIQUE, CHECK, etc.
    columns: List[str] = field(default_factory=list)
    condition: str = ""
    description: str = ""


@dataclass
class TableDefinition:
    """テーブル定義"""
    table_name: str
    logical_name: str
    category: str
    overview: str = ""
    columns: List[ColumnDefinition] = field(default_factory=list)
    indexes: List[IndexDefinition] = field(default_factory=list)
    foreign_keys: List[ForeignKeyDefinition] = field(default_factory=list)
    constraints: List[ConstraintDefinition] = field(default_factory=list)
    sample_data: List[Dict[str, Any]] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)
    business_rules: List[str] = field(default_factory=list)


@dataclass
class EntityRelationship:
    """エンティティ関連定義"""
    source: str
    target: str
    type: str
    cardinality: str
    foreign_key: str
    description: str = ""


@dataclass
class CheckResult:
    """チェック結果"""
    check_name: str
    table_name: str
    severity: CheckSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    file_path: str = ""
    line_number: Optional[int] = None


@dataclass
class FixSuggestion:
    """修正提案"""
    fix_type: FixType
    table_name: str
    description: str
    fix_content: str
    file_path: str = ""
    backup_required: bool = True
    critical: bool = False


@dataclass
class ConsistencyReport:
    """整合性チェックレポート"""
    check_date: str
    total_tables: int
    total_checks: int
    results: List[CheckResult] = field(default_factory=list)
    fix_suggestions: List[FixSuggestion] = field(default_factory=list)
    summary: Dict[str, int] = field(default_factory=dict)


@dataclass
class TableListEntry:
    """テーブル一覧エントリ"""
    table_id: str
    category: str
    table_name: str
    logical_name: str
    priority: str
    personal_info: bool = False
    encryption_required: bool = False


@dataclass
class DDLTable:
    """DDL解析結果のテーブル定義"""
    table_name: str
    columns: List[ColumnDefinition] = field(default_factory=list)
    indexes: List[IndexDefinition] = field(default_factory=list)
    foreign_keys: List[ForeignKeyDefinition] = field(default_factory=list)
    constraints: List[ConstraintDefinition] = field(default_factory=list)
    engine: str = "InnoDB"
    charset: str = "utf8mb4"
    collation: str = "utf8mb4_unicode_ci"


@dataclass
class InsertStatement:
    """INSERT文解析結果"""
    table_name: str
    columns: List[str]
    values: List[List[Any]]
    file_path: str = ""


@dataclass
class CheckConfig:
    """チェック設定"""
    suggest_fixes: bool = False
    fix_types: List[FixType] = field(default_factory=lambda: [FixType.ALL])
    auto_apply: bool = False
    output_fixes: Optional[str] = None
    verbose: bool = False
    target_tables: List[str] = field(default_factory=list)
    base_dir: str = ""
    output_format: str = "console"  # console, markdown, json
    output_file: Optional[str] = None
