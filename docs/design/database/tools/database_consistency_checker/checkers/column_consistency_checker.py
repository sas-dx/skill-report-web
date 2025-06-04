"""
カラム定義整合性チェッカー
DDLとYAMLファイル間のカラム定義整合性をチェックする
"""
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass

from ..core.models import CheckResult, CheckSeverity
from ..core.logger import ConsistencyLogger
from ..parsers.column_parser import ColumnParser, TableSchema, ColumnDefinition


@dataclass
class ColumnInconsistency:
    """カラム不整合情報"""
    table_name: str
    column_name: str
    issue_type: str
    ddl_value: Optional[str] = None
    yaml_value: Optional[str] = None
    description: str = ""


class ColumnConsistencyChecker:
    """カラム定義整合性チェッカー"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        self.logger = logger or ConsistencyLogger()
        self.parser = ColumnParser(logger)
    
    def check_table_column_consistency(
        self, 
        ddl_path: Path, 
        yaml_path: Path
    ) -> List[CheckResult]:
        """単一テーブルのカラム整合性をチェック"""
        results = []
        
        # DDLとYAMLを解析
        ddl_schema = self.parser.parse_ddl_file(ddl_path)
        yaml_schema = self.parser.parse_yaml_file(yaml_path)
        
        if not ddl_schema:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=ddl_path.stem,
                severity=CheckSeverity.ERROR,
                message=f"DDLファイルの解析に失敗しました: {ddl_path}",
                details={"file_path": str(ddl_path)}
            ))
            return results
        
        if not yaml_schema:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=yaml_path.stem,
                severity=CheckSeverity.ERROR,
                message=f"YAMLファイルの解析に失敗しました: {yaml_path}",
                details={"file_path": str(yaml_path)}
            ))
            return results
        
        # カラム整合性チェック
        column_results = self._check_column_definitions(ddl_schema, yaml_schema)
        results.extend(column_results)
        
        # インデックス整合性チェック
        index_results = self._check_index_consistency(ddl_schema, yaml_schema)
        results.extend(index_results)
        
        # 制約整合性チェック
        constraint_results = self._check_constraint_consistency(ddl_schema, yaml_schema)
        results.extend(constraint_results)
        
        return results
    
    def _check_column_definitions(
        self, 
        ddl_schema: TableSchema, 
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """カラム定義の整合性をチェック"""
        results = []
        table_name = ddl_schema.table_name
        
        # DDLとYAMLのカラム名セットを取得
        ddl_columns = set(ddl_schema.columns.keys())
        yaml_columns = set(yaml_schema.columns.keys())
        
        # DDLにのみ存在するカラム
        ddl_only = ddl_columns - yaml_columns
        for column_name in ddl_only:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"カラム '{column_name}' がDDLにのみ存在します",
                details={
                    "column_name": column_name,
                    "issue_type": "ddl_only_column",
                    "ddl_definition": self._format_column_definition(ddl_schema.columns[column_name])
                }
            ))
        
        # YAMLにのみ存在するカラム
        yaml_only = yaml_columns - ddl_columns
        for column_name in yaml_only:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"カラム '{column_name}' がYAMLにのみ存在します（DDLに定義が必要）",
                details={
                    "column_name": column_name,
                    "issue_type": "yaml_only_column",
                    "yaml_definition": self._format_column_definition(yaml_schema.columns[column_name])
                }
            ))
        
        # 両方に存在するカラムの詳細比較
        common_columns = ddl_columns & yaml_columns
        for column_name in common_columns:
            ddl_col = ddl_schema.columns[column_name]
            yaml_col = yaml_schema.columns[column_name]
            
            column_results = self._compare_column_definitions(table_name, ddl_col, yaml_col)
            results.extend(column_results)
        
        return results
    
    def _compare_column_definitions(
        self, 
        table_name: str, 
        ddl_col: ColumnDefinition, 
        yaml_col: ColumnDefinition
    ) -> List[CheckResult]:
        """個別カラム定義の詳細比較"""
        results = []
        column_name = ddl_col.name
        
        # データ型の比較
        if ddl_col.data_type.upper() != yaml_col.data_type.upper():
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"カラム '{column_name}' のデータ型が不一致",
                details={
                    "column_name": column_name,
                    "issue_type": "data_type_mismatch",
                    "ddl_type": ddl_col.get_full_type(),
                    "yaml_type": yaml_col.get_full_type()
                }
            ))
        
        # 長さの比較（データ型が同じ場合のみ）
        elif ddl_col.data_type.upper() == yaml_col.data_type.upper():
            if ddl_col.length != yaml_col.length:
                results.append(CheckResult(
                    check_name="column_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"カラム '{column_name}' の長さが不一致",
                    details={
                        "column_name": column_name,
                        "issue_type": "length_mismatch",
                        "ddl_length": ddl_col.length,
                        "yaml_length": yaml_col.length
                    }
                ))
        
        # NULL制約の比較
        if ddl_col.nullable != yaml_col.nullable:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"カラム '{column_name}' のNULL制約が不一致",
                details={
                    "column_name": column_name,
                    "issue_type": "nullable_mismatch",
                    "ddl_nullable": ddl_col.nullable,
                    "yaml_nullable": yaml_col.nullable
                }
            ))
        
        # デフォルト値の比較
        if ddl_col.default_value != yaml_col.default_value:
            # 両方ともNoneでない場合のみチェック
            if ddl_col.default_value is not None or yaml_col.default_value is not None:
                results.append(CheckResult(
                    check_name="column_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"カラム '{column_name}' のデフォルト値が不一致",
                    details={
                        "column_name": column_name,
                        "issue_type": "default_value_mismatch",
                        "ddl_default": ddl_col.default_value,
                        "yaml_default": yaml_col.default_value
                    }
                ))
        
        # ENUM値の比較
        if ddl_col.data_type.upper() == "ENUM" and yaml_col.data_type.upper() == "ENUM":
            ddl_enum_set = set(ddl_col.enum_values or [])
            yaml_enum_set = set(yaml_col.enum_values or [])
            
            if ddl_enum_set != yaml_enum_set:
                results.append(CheckResult(
                    check_name="column_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"カラム '{column_name}' のENUM値が不一致",
                    details={
                        "column_name": column_name,
                        "issue_type": "enum_values_mismatch",
                        "ddl_enum_values": list(ddl_col.enum_values or []),
                        "yaml_enum_values": list(yaml_col.enum_values or [])
                    }
                ))
        
        return results
    
    def _check_index_consistency(
        self, 
        ddl_schema: TableSchema, 
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """インデックス定義の整合性をチェック"""
        results = []
        table_name = ddl_schema.table_name
        
        # インデックス名でマッピング
        ddl_indexes = {idx['name']: idx for idx in ddl_schema.indexes}
        yaml_indexes = {idx['name']: idx for idx in yaml_schema.indexes}
        
        ddl_index_names = set(ddl_indexes.keys())
        yaml_index_names = set(yaml_indexes.keys())
        
        # DDLにのみ存在するインデックス
        ddl_only = ddl_index_names - yaml_index_names
        for index_name in ddl_only:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"インデックス '{index_name}' がDDLにのみ存在します",
                details={
                    "index_name": index_name,
                    "issue_type": "ddl_only_index",
                    "ddl_index": ddl_indexes[index_name]
                }
            ))
        
        # YAMLにのみ存在するインデックス
        yaml_only = yaml_index_names - ddl_index_names
        for index_name in yaml_only:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"インデックス '{index_name}' がYAMLにのみ存在します（DDLに定義が必要）",
                details={
                    "index_name": index_name,
                    "issue_type": "yaml_only_index",
                    "yaml_index": yaml_indexes[index_name]
                }
            ))
        
        # 共通インデックスの詳細比較
        common_indexes = ddl_index_names & yaml_index_names
        for index_name in common_indexes:
            ddl_idx = ddl_indexes[index_name]
            yaml_idx = yaml_indexes[index_name]
            
            # カラム構成の比較
            if ddl_idx['columns'] != yaml_idx['columns']:
                results.append(CheckResult(
                    check_name="column_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"インデックス '{index_name}' のカラム構成が不一致",
                    details={
                        "index_name": index_name,
                        "issue_type": "index_columns_mismatch",
                        "ddl_columns": ddl_idx['columns'],
                        "yaml_columns": yaml_idx['columns']
                    }
                ))
            
            # UNIQUE属性の比較
            if ddl_idx.get('unique', False) != yaml_idx.get('unique', False):
                results.append(CheckResult(
                    check_name="column_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"インデックス '{index_name}' のUNIQUE属性が不一致",
                    details={
                        "index_name": index_name,
                        "issue_type": "index_unique_mismatch",
                        "ddl_unique": ddl_idx.get('unique', False),
                        "yaml_unique": yaml_idx.get('unique', False)
                    }
                ))
        
        return results
    
    def _check_constraint_consistency(
        self, 
        ddl_schema: TableSchema, 
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """制約定義の整合性をチェック"""
        results = []
        table_name = ddl_schema.table_name
        
        # PRIMARY KEY制約の比較
        ddl_pk = set(ddl_schema.primary_keys)
        yaml_pk = set(yaml_schema.primary_keys)
        
        if ddl_pk != yaml_pk:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message="PRIMARY KEY制約が不一致",
                details={
                    "issue_type": "primary_key_mismatch",
                    "ddl_primary_keys": list(ddl_pk),
                    "yaml_primary_keys": list(yaml_pk)
                }
            ))
        
        # UNIQUE制約の比較
        ddl_unique = {tuple(sorted(constraint)) for constraint in ddl_schema.unique_constraints}
        yaml_unique = {tuple(sorted(constraint)) for constraint in yaml_schema.unique_constraints}
        
        ddl_only_unique = ddl_unique - yaml_unique
        yaml_only_unique = yaml_unique - ddl_unique
        
        for constraint in ddl_only_unique:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"UNIQUE制約 {list(constraint)} がDDLにのみ存在します",
                details={
                    "issue_type": "ddl_only_unique_constraint",
                    "constraint_columns": list(constraint)
                }
            ))
        
        for constraint in yaml_only_unique:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"UNIQUE制約 {list(constraint)} がYAMLにのみ存在します（DDLに定義が必要）",
                details={
                    "issue_type": "yaml_only_unique_constraint",
                    "constraint_columns": list(constraint)
                }
            ))
        
        # CHECK制約の比較
        ddl_checks = {check['name']: check for check in ddl_schema.check_constraints}
        yaml_checks = {check['name']: check for check in yaml_schema.check_constraints}
        
        ddl_check_names = set(ddl_checks.keys())
        yaml_check_names = set(yaml_checks.keys())
        
        ddl_only_checks = ddl_check_names - yaml_check_names
        yaml_only_checks = yaml_check_names - ddl_check_names
        
        for check_name in ddl_only_checks:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"CHECK制約 '{check_name}' がDDLにのみ存在します",
                details={
                    "issue_type": "ddl_only_check_constraint",
                    "constraint_name": check_name,
                    "ddl_condition": ddl_checks[check_name].get('condition')
                }
            ))
        
        for check_name in yaml_only_checks:
            results.append(CheckResult(
                check_name="column_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"CHECK制約 '{check_name}' がYAMLにのみ存在します（DDLに定義が必要）",
                details={
                    "issue_type": "yaml_only_check_constraint",
                    "constraint_name": check_name,
                    "yaml_condition": yaml_checks[check_name].get('condition')
                }
            ))
        
        return results
    
    def _format_column_definition(self, column: ColumnDefinition) -> str:
        """カラム定義を文字列形式でフォーマット"""
        parts = [column.get_full_type()]
        
        if not column.nullable:
            parts.append("NOT NULL")
        
        if column.unique:
            parts.append("UNIQUE")
        
        if column.primary_key:
            parts.append("PRIMARY KEY")
        
        if column.default_value:
            parts.append(f"DEFAULT {column.default_value}")
        
        return " ".join(parts)
