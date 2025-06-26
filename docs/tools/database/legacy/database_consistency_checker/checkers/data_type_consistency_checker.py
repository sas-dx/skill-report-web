"""
データ型整合性チェッカー - DDLとYAML間のデータ型整合性検証
"""
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path

from core.models import (
    CheckResult, CheckSeverity, ColumnDefinition, 
    DDLTable, TableDefinition
)
from parsers.ddl_parser import EnhancedDDLParser
from parsers.yaml_parser import EnhancedYAMLParser


class DataTypeConsistencyChecker:
    """データ型整合性チェッカー"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
        self.ddl_parser = EnhancedDDLParser(self.logger)
        self.yaml_parser = EnhancedYAMLParser(self.logger)
        
        # データ型の互換性マッピング
        self.type_compatibility = self._init_type_compatibility()
    
    def _init_type_compatibility(self) -> Dict[str, List[str]]:
        """データ型の互換性マッピング"""
        return {
            'VARCHAR': ['VARCHAR', 'CHAR', 'TEXT'],
            'CHAR': ['CHAR', 'VARCHAR'],
            'TEXT': ['TEXT', 'LONGTEXT', 'MEDIUMTEXT', 'TINYTEXT'],
            'INT': ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT'],
            'INTEGER': ['INT', 'INTEGER', 'TINYINT', 'SMALLINT', 'MEDIUMINT', 'BIGINT'],
            'BIGINT': ['BIGINT', 'INT', 'INTEGER'],
            'TINYINT': ['TINYINT', 'INT', 'INTEGER'],
            'SMALLINT': ['SMALLINT', 'INT', 'INTEGER'],
            'MEDIUMINT': ['MEDIUMINT', 'INT', 'INTEGER'],
            'DECIMAL': ['DECIMAL', 'FLOAT', 'DOUBLE'],
            'FLOAT': ['FLOAT', 'DECIMAL', 'DOUBLE'],
            'DOUBLE': ['DOUBLE', 'FLOAT', 'DECIMAL'],
            'DATE': ['DATE'],
            'DATETIME': ['DATETIME', 'TIMESTAMP'],
            'TIMESTAMP': ['TIMESTAMP', 'DATETIME'],
            'TIME': ['TIME'],
            'YEAR': ['YEAR'],
            'BOOLEAN': ['BOOLEAN', 'BOOL', 'TINYINT'],
            'BOOL': ['BOOLEAN', 'BOOL', 'TINYINT'],
            'ENUM': ['ENUM'],
            'SET': ['SET'],
            'JSON': ['JSON', 'TEXT'],
            'BLOB': ['BLOB', 'LONGBLOB', 'MEDIUMBLOB', 'TINYBLOB'],
        }
    
    def check_data_type_consistency(self, table_name: str) -> List[CheckResult]:
        """指定テーブルのデータ型整合性チェック"""
        results = []
        
        try:
            # DDLファイルを解析
            ddl_file = self.base_dir / "ddl" / f"{table_name}.sql"
            if not ddl_file.exists():
                results.append(CheckResult(
                    check_name="data_type_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"DDLファイルが存在しません: {ddl_file}",
                    file_path=str(ddl_file)
                ))
                return results
            
            ddl_table = self.ddl_parser.parse_ddl_file_detailed(ddl_file)
            if not ddl_table:
                results.append(CheckResult(
                    check_name="data_type_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="DDLファイルの解析に失敗しました",
                    file_path=str(ddl_file)
                ))
                return results
            
            # YAMLファイルを解析
            yaml_file = self.base_dir / "table-details" / f"{table_name}_details.yaml"
            if not yaml_file.exists():
                results.append(CheckResult(
                    check_name="data_type_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"YAML詳細定義ファイルが存在しません: {yaml_file}",
                    file_path=str(yaml_file)
                ))
                return results
            
            yaml_table = self.yaml_parser.parse_table_definition(yaml_file)
            if not yaml_table:
                results.append(CheckResult(
                    check_name="data_type_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="YAML詳細定義ファイルの解析に失敗しました",
                    file_path=str(yaml_file)
                ))
                return results
            
            # カラム定義の整合性をチェック
            column_results = self._check_column_consistency(ddl_table, yaml_table)
            results.extend(column_results)
            
            # 成功時のメッセージ
            if not any(r.severity == CheckSeverity.ERROR for r in results):
                results.append(CheckResult(
                    check_name="data_type_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message="データ型整合性チェック完了",
                    details={
                        "ddl_columns": len(ddl_table.columns),
                        "yaml_columns": len(yaml_table.columns),
                        "checked_columns": len([r for r in results if r.severity != CheckSeverity.ERROR])
                    }
                ))
            
        except Exception as e:
            self.logger.error(f"データ型整合性チェックエラー: {table_name} - {e}")
            results.append(CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"チェック実行エラー: {str(e)}"
            ))
        
        return results
    
    def _check_column_consistency(self, ddl_table: DDLTable, yaml_table: TableDefinition) -> List[CheckResult]:
        """カラム定義の整合性チェック"""
        results = []
        
        # DDLとYAMLのカラムをマッピング
        ddl_columns = {col.name: col for col in ddl_table.columns}
        yaml_columns = {col.name: col for col in yaml_table.columns}
        
        # 全カラム名を取得
        all_columns = set(ddl_columns.keys()) | set(yaml_columns.keys())
        
        for column_name in all_columns:
            ddl_col = ddl_columns.get(column_name)
            yaml_col = yaml_columns.get(column_name)
            
            if not ddl_col:
                results.append(CheckResult(
                    check_name="data_type_consistency",
                    table_name=ddl_table.table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"カラム '{column_name}' がDDLに存在しません",
                    details={"column": column_name, "source": "yaml_only"}
                ))
                continue
            
            if not yaml_col:
                results.append(CheckResult(
                    check_name="data_type_consistency",
                    table_name=ddl_table.table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"カラム '{column_name}' がYAML定義に存在しません",
                    details={"column": column_name, "source": "ddl_only"}
                ))
                continue
            
            # カラム定義の詳細比較
            column_results = self._compare_column_definitions(ddl_col, yaml_col, ddl_table.table_name)
            results.extend(column_results)
        
        return results
    
    def _compare_column_definitions(self, ddl_col: ColumnDefinition, yaml_col: ColumnDefinition, table_name: str) -> List[CheckResult]:
        """カラム定義の詳細比較"""
        results = []
        column_name = ddl_col.name
        
        # データ型の比較
        type_result = self._compare_data_types(ddl_col, yaml_col, table_name)
        if type_result:
            results.append(type_result)
        
        # 長さ制約の比較
        length_result = self._compare_length_constraints(ddl_col, yaml_col, table_name)
        if length_result:
            results.append(length_result)
        
        # NULL制約の比較
        null_result = self._compare_null_constraints(ddl_col, yaml_col, table_name)
        if null_result:
            results.append(null_result)
        
        # デフォルト値の比較
        default_result = self._compare_default_values(ddl_col, yaml_col, table_name)
        if default_result:
            results.append(default_result)
        
        # ENUM値の比較
        enum_result = self._compare_enum_values(ddl_col, yaml_col, table_name)
        if enum_result:
            results.append(enum_result)
        
        # 成功時のメッセージ（エラーがない場合）
        if not results:
            results.append(CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message=f"カラム '{column_name}' のデータ型整合性OK",
                details={
                    "column": column_name,
                    "ddl_type": ddl_col.data_type,
                    "yaml_type": yaml_col.data_type
                }
            ))
        
        return results
    
    def _compare_data_types(self, ddl_col: ColumnDefinition, yaml_col: ColumnDefinition, table_name: str) -> Optional[CheckResult]:
        """データ型の比較"""
        ddl_type = ddl_col.data_type.upper() if ddl_col.data_type else ''
        yaml_type = yaml_col.data_type.upper() if yaml_col.data_type else ''
        
        if not ddl_type or not yaml_type:
            return CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"カラム '{ddl_col.name}' のデータ型が未定義",
                details={
                    "column": ddl_col.name,
                    "ddl_type": ddl_type,
                    "yaml_type": yaml_type
                }
            )
        
        # 完全一致チェック
        if ddl_type == yaml_type:
            return None
        
        # 互換性チェック
        compatible_types = self.type_compatibility.get(yaml_type, [])
        if ddl_type in compatible_types:
            return CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"カラム '{ddl_col.name}' のデータ型が互換性のある型で異なります",
                details={
                    "column": ddl_col.name,
                    "ddl_type": ddl_type,
                    "yaml_type": yaml_type,
                    "compatibility": "compatible"
                }
            )
        
        # 非互換
        return CheckResult(
            check_name="data_type_consistency",
            table_name=table_name,
            severity=CheckSeverity.ERROR,
            message=f"カラム '{ddl_col.name}' のデータ型が一致しません",
            details={
                "column": ddl_col.name,
                "ddl_type": ddl_type,
                "yaml_type": yaml_type,
                "compatibility": "incompatible"
            }
        )
    
    def _compare_length_constraints(self, ddl_col: ColumnDefinition, yaml_col: ColumnDefinition, table_name: str) -> Optional[CheckResult]:
        """長さ制約の比較"""
        ddl_length = ddl_col.length
        yaml_length = yaml_col.length
        
        # 両方ともNoneの場合は問題なし
        if ddl_length is None and yaml_length is None:
            return None
        
        # 片方だけNoneの場合
        if ddl_length is None or yaml_length is None:
            return CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"カラム '{ddl_col.name}' の長さ制約定義が片方のみ存在します",
                details={
                    "column": ddl_col.name,
                    "ddl_length": ddl_length,
                    "yaml_length": yaml_length
                }
            )
        
        # 長さが異なる場合
        if ddl_length != yaml_length:
            return CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"カラム '{ddl_col.name}' の長さ制約が一致しません",
                details={
                    "column": ddl_col.name,
                    "ddl_length": ddl_length,
                    "yaml_length": yaml_length
                }
            )
        
        return None
    
    def _compare_null_constraints(self, ddl_col: ColumnDefinition, yaml_col: ColumnDefinition, table_name: str) -> Optional[CheckResult]:
        """NULL制約の比較"""
        ddl_nullable = ddl_col.nullable
        yaml_nullable = yaml_col.nullable
        
        if ddl_nullable != yaml_nullable:
            severity = CheckSeverity.WARNING  # NULL制約の不一致は警告レベル
            return CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=severity,
                message=f"カラム '{ddl_col.name}' のNULL制約が一致しません",
                details={
                    "column": ddl_col.name,
                    "ddl_nullable": ddl_nullable,
                    "yaml_nullable": yaml_nullable
                }
            )
        
        return None
    
    def _compare_default_values(self, ddl_col: ColumnDefinition, yaml_col: ColumnDefinition, table_name: str) -> Optional[CheckResult]:
        """デフォルト値の比較"""
        ddl_default = ddl_col.default_value
        yaml_default = yaml_col.default_value
        
        # 両方ともNoneの場合は問題なし
        if ddl_default is None and yaml_default is None:
            return None
        
        # 値を正規化して比較
        ddl_normalized = self._normalize_default_value(ddl_default)
        yaml_normalized = self._normalize_default_value(yaml_default)
        
        if ddl_normalized != yaml_normalized:
            return CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"カラム '{ddl_col.name}' のデフォルト値が一致しません",
                details={
                    "column": ddl_col.name,
                    "ddl_default": ddl_default,
                    "yaml_default": yaml_default
                }
            )
        
        return None
    
    def _compare_enum_values(self, ddl_col: ColumnDefinition, yaml_col: ColumnDefinition, table_name: str) -> Optional[CheckResult]:
        """ENUM値の比較"""
        ddl_enum = set(ddl_col.enum_values) if ddl_col.enum_values else set()
        yaml_enum = set(yaml_col.enum_values) if yaml_col.enum_values else set()
        
        # 両方とも空の場合は問題なし
        if not ddl_enum and not yaml_enum:
            return None
        
        # ENUM値が異なる場合
        if ddl_enum != yaml_enum:
            missing_in_ddl = yaml_enum - ddl_enum
            missing_in_yaml = ddl_enum - yaml_enum
            
            return CheckResult(
                check_name="data_type_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"カラム '{ddl_col.name}' のENUM値が一致しません",
                details={
                    "column": ddl_col.name,
                    "ddl_enum": list(ddl_enum),
                    "yaml_enum": list(yaml_enum),
                    "missing_in_ddl": list(missing_in_ddl),
                    "missing_in_yaml": list(missing_in_yaml)
                }
            )
        
        return None
    
    def _normalize_default_value(self, value: Any) -> str:
        """デフォルト値の正規化"""
        if value is None:
            return ""
        
        # 文字列化
        str_value = str(value).strip()
        
        # 引用符を除去
        if str_value.startswith("'") and str_value.endswith("'"):
            str_value = str_value[1:-1]
        elif str_value.startswith('"') and str_value.endswith('"'):
            str_value = str_value[1:-1]
        
        # 大文字小文字を統一（特定のキーワードのみ）
        keywords = ['TRUE', 'FALSE', 'NULL', 'CURRENT_TIMESTAMP', 'NOW()']
        upper_value = str_value.upper()
        if upper_value in keywords:
            return upper_value
        
        return str_value
    
    def check_all_tables(self, table_names: List[str]) -> List[CheckResult]:
        """複数テーブルのデータ型整合性チェック"""
        all_results = []
        
        for table_name in table_names:
            self.logger.info(f"データ型整合性チェック開始: {table_name}")
            table_results = self.check_data_type_consistency(table_name)
            all_results.extend(table_results)
        
        return all_results
    
    def get_summary_statistics(self, results: List[CheckResult]) -> Dict[str, Any]:
        """チェック結果の統計情報を取得"""
        stats = {
            "total_checks": len(results),
            "success_count": 0,
            "warning_count": 0,
            "error_count": 0,
            "tables_checked": set(),
            "columns_checked": 0
        }
        
        for result in results:
            stats["tables_checked"].add(result.table_name)
            
            if result.severity == CheckSeverity.SUCCESS:
                stats["success_count"] += 1
            elif result.severity == CheckSeverity.WARNING:
                stats["warning_count"] += 1
            elif result.severity == CheckSeverity.ERROR:
                stats["error_count"] += 1
            
            # カラムレベルのチェックをカウント
            if result.details and "column" in result.details:
                stats["columns_checked"] += 1
        
        stats["tables_checked"] = len(stats["tables_checked"])
        
        return stats
