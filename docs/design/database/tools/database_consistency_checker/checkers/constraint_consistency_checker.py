"""
制約整合性チェッカー
PRIMARY KEY、UNIQUE、CHECK制約、インデックス定義の整合性をチェックする
"""
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass

from core.models import CheckResult, CheckSeverity, ConstraintDefinition, IndexDefinition
from core.logger import ConsistencyLogger
from parsers.column_parser import ColumnParser, TableSchema


@dataclass
class ConstraintMismatch:
    """制約の不一致情報"""
    constraint_name: str
    constraint_type: str
    ddl_definition: Optional[Dict] = None
    yaml_definition: Optional[Dict] = None
    issue_type: str = ""
    details: Dict = None


class ConstraintConsistencyChecker:
    """制約整合性チェッカー"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        self.logger = logger or ConsistencyLogger()
        self.column_parser = ColumnParser(logger)
    
    def check_constraint_consistency(
        self,
        ddl_dir: Path,
        yaml_details_dir: Path,
        table_names: List[str]
    ) -> List[CheckResult]:
        """制約整合性の包括的チェック"""
        results = []
        
        for table_name in table_names:
            table_results = self._check_table_constraints(
                table_name, ddl_dir, yaml_details_dir
            )
            results.extend(table_results)
        
        return results
    
    def _check_table_constraints(
        self,
        table_name: str,
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[CheckResult]:
        """単一テーブルの制約整合性をチェック"""
        results = []
        
        # DDLファイルとYAML詳細ファイルのパスを構築
        ddl_path = ddl_dir / f"{table_name}.sql"
        yaml_path = yaml_details_dir / f"{table_name}_details.yaml"
        
        if not ddl_path.exists():
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"DDLファイルが見つかりません: {ddl_path}",
                details={"file_path": str(ddl_path)}
            ))
            return results
        
        if not yaml_path.exists():
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"YAML詳細ファイルが見つかりません: {yaml_path}",
                details={"file_path": str(yaml_path)}
            ))
            return results
        
        # DDLとYAMLからスキーマ情報を解析
        ddl_schema = self.column_parser.parse_ddl_file(ddl_path)
        yaml_schema = self.column_parser.parse_yaml_file(yaml_path)
        
        if not ddl_schema or not yaml_schema:
            return results
        
        # 各種制約の整合性チェック
        pk_results = self._check_primary_key_consistency(table_name, ddl_schema, yaml_schema)
        results.extend(pk_results)
        
        unique_results = self._check_unique_constraint_consistency(table_name, ddl_schema, yaml_schema)
        results.extend(unique_results)
        
        check_results = self._check_check_constraint_consistency(table_name, ddl_schema, yaml_schema)
        results.extend(check_results)
        
        index_results = self._check_index_consistency(table_name, ddl_schema, yaml_schema)
        results.extend(index_results)
        
        fk_cascade_results = self._check_foreign_key_cascade_consistency(table_name, ddl_schema, yaml_schema)
        results.extend(fk_cascade_results)
        
        return results
    
    def _check_primary_key_consistency(
        self,
        table_name: str,
        ddl_schema: TableSchema,
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """PRIMARY KEY制約の整合性チェック"""
        results = []
        
        # DDLからPRIMARY KEYカラムを抽出
        ddl_pk_columns = set()
        for col_name, col_def in ddl_schema.columns.items():
            if getattr(col_def, 'primary_key', False):
                ddl_pk_columns.add(col_name)
        
        # YAMLからPRIMARY KEYカラムを抽出
        yaml_pk_columns = set()
        for col_name, col_def in yaml_schema.columns.items():
            if getattr(col_def, 'primary_key', False):
                yaml_pk_columns.add(col_name)
        
        # PRIMARY KEYの一致チェック
        if ddl_pk_columns != yaml_pk_columns:
            missing_in_ddl = yaml_pk_columns - ddl_pk_columns
            missing_in_yaml = ddl_pk_columns - yaml_pk_columns
            
            if missing_in_ddl:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"PRIMARY KEYカラムがDDLに不足: {', '.join(missing_in_ddl)}",
                    details={
                        "issue_type": "missing_primary_key_in_ddl",
                        "missing_columns": list(missing_in_ddl),
                        "yaml_pk_columns": list(yaml_pk_columns),
                        "ddl_pk_columns": list(ddl_pk_columns)
                    }
                ))
            
            if missing_in_yaml:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"PRIMARY KEYカラムがYAMLに不足: {', '.join(missing_in_yaml)}",
                    details={
                        "issue_type": "missing_primary_key_in_yaml",
                        "missing_columns": list(missing_in_yaml),
                        "yaml_pk_columns": list(yaml_pk_columns),
                        "ddl_pk_columns": list(ddl_pk_columns)
                    }
                ))
        else:
            if ddl_pk_columns:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message=f"PRIMARY KEY制約整合性OK: {', '.join(ddl_pk_columns)}",
                    details={
                        "issue_type": "primary_key_consistent",
                        "primary_key_columns": list(ddl_pk_columns)
                    }
                ))
        
        return results
    
    def _check_unique_constraint_consistency(
        self,
        table_name: str,
        ddl_schema: TableSchema,
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """UNIQUE制約の整合性チェック"""
        results = []
        
        # DDLからUNIQUE制約を抽出
        ddl_unique_constraints = set()
        for constraint in getattr(ddl_schema, 'constraints', []):
            if constraint.type.upper() == 'UNIQUE':
                ddl_unique_constraints.add(tuple(sorted(constraint.columns)))
        
        # カラムレベルのUNIQUE制約も追加
        for col_name, col_def in ddl_schema.columns.items():
            if getattr(col_def, 'unique', False):
                ddl_unique_constraints.add((col_name,))
        
        # YAMLからUNIQUE制約を抽出
        yaml_unique_constraints = set()
        for constraint in getattr(yaml_schema, 'constraints', []):
            if constraint.type.upper() == 'UNIQUE':
                yaml_unique_constraints.add(tuple(sorted(constraint.columns)))
        
        # カラムレベルのUNIQUE制約も追加
        for col_name, col_def in yaml_schema.columns.items():
            if getattr(col_def, 'unique', False):
                yaml_unique_constraints.add((col_name,))
        
        # UNIQUE制約の一致チェック
        missing_in_ddl = yaml_unique_constraints - ddl_unique_constraints
        missing_in_yaml = ddl_unique_constraints - yaml_unique_constraints
        
        for constraint_cols in missing_in_ddl:
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"UNIQUE制約がDDLに不足: {', '.join(constraint_cols)}",
                details={
                    "issue_type": "missing_unique_constraint_in_ddl",
                    "constraint_columns": list(constraint_cols)
                }
            ))
        
        for constraint_cols in missing_in_yaml:
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"UNIQUE制約がYAMLに不足: {', '.join(constraint_cols)}",
                details={
                    "issue_type": "missing_unique_constraint_in_yaml",
                    "constraint_columns": list(constraint_cols)
                }
            ))
        
        # 一致している制約の成功メッセージ
        common_constraints = ddl_unique_constraints & yaml_unique_constraints
        if common_constraints:
            for constraint_cols in common_constraints:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message=f"UNIQUE制約整合性OK: {', '.join(constraint_cols)}",
                    details={
                        "issue_type": "unique_constraint_consistent",
                        "constraint_columns": list(constraint_cols)
                    }
                ))
        
        return results
    
    def _check_check_constraint_consistency(
        self,
        table_name: str,
        ddl_schema: TableSchema,
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """CHECK制約の整合性チェック"""
        results = []
        
        # DDLからCHECK制約を抽出
        ddl_check_constraints = {}
        for constraint in getattr(ddl_schema, 'constraints', []):
            if constraint.type.upper() == 'CHECK':
                ddl_check_constraints[constraint.name] = constraint
        
        # YAMLからCHECK制約を抽出
        yaml_check_constraints = {}
        for constraint in getattr(yaml_schema, 'constraints', []):
            if constraint.type.upper() == 'CHECK':
                yaml_check_constraints[constraint.name] = constraint
        
        # CHECK制約の一致チェック
        ddl_names = set(ddl_check_constraints.keys())
        yaml_names = set(yaml_check_constraints.keys())
        
        missing_in_ddl = yaml_names - ddl_names
        missing_in_yaml = ddl_names - yaml_names
        common_names = ddl_names & yaml_names
        
        for constraint_name in missing_in_ddl:
            constraint = yaml_check_constraints[constraint_name]
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"CHECK制約がDDLに不足: {constraint_name}",
                details={
                    "issue_type": "missing_check_constraint_in_ddl",
                    "constraint_name": constraint_name,
                    "constraint_condition": constraint.condition
                }
            ))
        
        for constraint_name in missing_in_yaml:
            constraint = ddl_check_constraints[constraint_name]
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"CHECK制約がYAMLに不足: {constraint_name}",
                details={
                    "issue_type": "missing_check_constraint_in_yaml",
                    "constraint_name": constraint_name,
                    "constraint_condition": constraint.condition
                }
            ))
        
        # 共通制約の条件チェック
        for constraint_name in common_names:
            ddl_constraint = ddl_check_constraints[constraint_name]
            yaml_constraint = yaml_check_constraints[constraint_name]
            
            if ddl_constraint.condition != yaml_constraint.condition:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"CHECK制約の条件が不一致: {constraint_name}",
                    details={
                        "issue_type": "check_constraint_condition_mismatch",
                        "constraint_name": constraint_name,
                        "ddl_condition": ddl_constraint.condition,
                        "yaml_condition": yaml_constraint.condition
                    }
                ))
            else:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message=f"CHECK制約整合性OK: {constraint_name}",
                    details={
                        "issue_type": "check_constraint_consistent",
                        "constraint_name": constraint_name
                    }
                ))
        
        return results
    
    def _check_index_consistency(
        self,
        table_name: str,
        ddl_schema: TableSchema,
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """インデックス定義の整合性チェック"""
        results = []
        
        # DDLからインデックスを抽出
        ddl_indexes = {}
        for index in getattr(ddl_schema, 'indexes', []):
            # indexが辞書の場合とオブジェクトの場合を処理
            if isinstance(index, dict):
                columns = index.get('columns', [])
                unique = index.get('unique', False)
                name = index.get('name', '')
            else:
                columns = getattr(index, 'columns', [])
                unique = getattr(index, 'unique', False)
                name = getattr(index, 'name', '')
            
            key = (tuple(sorted(columns)), unique)
            ddl_indexes[key] = {'name': name, 'columns': columns, 'unique': unique}
        
        # YAMLからインデックスを抽出
        yaml_indexes = {}
        for index in getattr(yaml_schema, 'indexes', []):
            # indexが辞書の場合とオブジェクトの場合を処理
            if isinstance(index, dict):
                columns = index.get('columns', [])
                unique = index.get('unique', False)
                name = index.get('name', '')
            else:
                columns = getattr(index, 'columns', [])
                unique = getattr(index, 'unique', False)
                name = getattr(index, 'name', '')
            
            key = (tuple(sorted(columns)), unique)
            yaml_indexes[key] = {'name': name, 'columns': columns, 'unique': unique}
        
        # インデックスの一致チェック
        ddl_keys = set(ddl_indexes.keys())
        yaml_keys = set(yaml_indexes.keys())
        
        missing_in_ddl = yaml_keys - ddl_keys
        missing_in_yaml = ddl_keys - yaml_keys
        common_keys = ddl_keys & yaml_keys
        
        for index_key in missing_in_ddl:
            columns, unique = index_key
            index = yaml_indexes[index_key]
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"インデックスがDDLに不足: {index['name']} ({', '.join(columns)})",
                details={
                    "issue_type": "missing_index_in_ddl",
                    "index_name": index['name'],
                    "index_columns": list(columns),
                    "unique": unique
                }
            ))
        
        for index_key in missing_in_yaml:
            columns, unique = index_key
            index = ddl_indexes[index_key]
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"インデックスがYAMLに不足: {index['name']} ({', '.join(columns)})",
                details={
                    "issue_type": "missing_index_in_yaml",
                    "index_name": index['name'],
                    "index_columns": list(columns),
                    "unique": unique
                }
            ))
        
        # 一致しているインデックスの成功メッセージ
        for index_key in common_keys:
            columns, unique = index_key
            ddl_index = ddl_indexes[index_key]
            results.append(CheckResult(
                check_name="constraint_consistency",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message=f"インデックス整合性OK: {ddl_index['name']} ({', '.join(columns)})",
                details={
                    "issue_type": "index_consistent",
                    "index_name": ddl_index['name'],
                    "index_columns": list(columns),
                    "unique": unique
                }
            ))
        
        return results
    
    def _check_foreign_key_cascade_consistency(
        self,
        table_name: str,
        ddl_schema: TableSchema,
        yaml_schema: TableSchema
    ) -> List[CheckResult]:
        """外部キーのカスケード設定整合性チェック"""
        results = []
        
        # DDLから外部キーを抽出
        ddl_fks = {}
        for fk in getattr(ddl_schema, 'foreign_keys', []):
            key = (tuple(fk.get('columns', [])), fk.get('reference_table'), tuple(fk.get('reference_columns', [])))
            ddl_fks[key] = fk
        
        # YAMLから外部キーを抽出
        yaml_fks = {}
        for fk in getattr(yaml_schema, 'foreign_keys', []):
            key = (tuple(fk.get('columns', [])), fk.get('reference_table'), tuple(fk.get('reference_columns', [])))
            yaml_fks[key] = fk
        
        # 共通する外部キーのカスケード設定チェック
        common_keys = set(ddl_fks.keys()) & set(yaml_fks.keys())
        
        for fk_key in common_keys:
            ddl_fk = ddl_fks[fk_key]
            yaml_fk = yaml_fks[fk_key]
            
            # ON UPDATE設定の比較
            ddl_on_update = ddl_fk.get('on_update', 'RESTRICT').upper()
            yaml_on_update = yaml_fk.get('on_update', 'RESTRICT').upper()
            
            if ddl_on_update != yaml_on_update:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"外部キー {ddl_fk.get('name', 'unknown')} のON UPDATE設定が不一致",
                    details={
                        "issue_type": "foreign_key_on_update_mismatch",
                        "foreign_key_name": ddl_fk.get('name', 'unknown'),
                        "ddl_on_update": ddl_on_update,
                        "yaml_on_update": yaml_on_update,
                        "recommended_setting": "CASCADE"
                    }
                ))
            
            # ON DELETE設定の比較
            ddl_on_delete = ddl_fk.get('on_delete', 'RESTRICT').upper()
            yaml_on_delete = yaml_fk.get('on_delete', 'RESTRICT').upper()
            
            if ddl_on_delete != yaml_on_delete:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"外部キー {ddl_fk.get('name', 'unknown')} のON DELETE設定が不一致",
                    details={
                        "issue_type": "foreign_key_on_delete_mismatch",
                        "foreign_key_name": ddl_fk.get('name', 'unknown'),
                        "ddl_on_delete": ddl_on_delete,
                        "yaml_on_delete": yaml_on_delete,
                        "recommended_setting": "SET NULL"
                    }
                ))
            
            # 設定が一致している場合の成功メッセージ
            if ddl_on_update == yaml_on_update and ddl_on_delete == yaml_on_delete:
                results.append(CheckResult(
                    check_name="constraint_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message=f"外部キーカスケード設定整合性OK: {ddl_fk.get('name', 'unknown')}",
                    details={
                        "issue_type": "foreign_key_cascade_consistent",
                        "foreign_key_name": ddl_fk.get('name', 'unknown'),
                        "on_update": ddl_on_update,
                        "on_delete": ddl_on_delete
                    }
                ))
        
        return results
    
    def get_constraint_statistics(self, results: List[CheckResult]) -> Dict[str, Dict[str, int]]:
        """制約チェックの統計情報を取得"""
        stats = {
            'primary_key': {'success': 0, 'warning': 0, 'error': 0},
            'unique_constraint': {'success': 0, 'warning': 0, 'error': 0},
            'check_constraint': {'success': 0, 'warning': 0, 'error': 0},
            'index': {'success': 0, 'warning': 0, 'error': 0},
            'foreign_key_cascade': {'success': 0, 'warning': 0, 'error': 0}
        }
        
        for result in results:
            if result.check_name == "constraint_consistency":
                issue_type = result.details.get('issue_type', '')
                severity = result.severity.value
                
                if 'primary_key' in issue_type:
                    stats['primary_key'][severity] += 1
                elif 'unique_constraint' in issue_type:
                    stats['unique_constraint'][severity] += 1
                elif 'check_constraint' in issue_type:
                    stats['check_constraint'][severity] += 1
                elif 'index' in issue_type:
                    stats['index'][severity] += 1
                elif 'foreign_key' in issue_type:
                    stats['foreign_key_cascade'][severity] += 1
        
        return stats
