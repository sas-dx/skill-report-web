"""
外部キー整合性チェッカー
entity_relationships.yamlとDDLファイル間の外部キー整合性をチェックする
"""
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass

from ..core.models import CheckResult, CheckSeverity
from ..core.logger import ConsistencyLogger
from ..parsers.column_parser import ColumnParser, TableSchema
from ..parsers.entity_yaml_parser import EntityYamlParser


@dataclass
class ForeignKeyDefinition:
    """外部キー定義"""
    name: str
    source_table: str
    source_columns: List[str]
    target_table: str
    target_columns: List[str]
    on_update: str = "RESTRICT"
    on_delete: str = "RESTRICT"
    description: Optional[str] = None


class ForeignKeyChecker:
    """外部キー整合性チェッカー"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        self.logger = logger or ConsistencyLogger()
        self.column_parser = ColumnParser(logger)
        self.entity_parser = EntityYamlParser(logger)
    
    def check_foreign_key_consistency(
        self,
        entity_yaml_path: Path,
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[CheckResult]:
        """外部キー整合性の包括的チェック"""
        results = []
        
        # entity_relationships.yamlから関連情報を取得
        entity_data = self.entity_parser.parse_file(entity_yaml_path)
        if not entity_data:
            results.append(CheckResult(
                check_type="foreign_key_consistency",
                table_name="",
                severity=CheckSeverity.ERROR,
                message=f"entity_relationships.yamlの解析に失敗: {entity_yaml_path}",
                details={"file_path": str(entity_yaml_path)}
            ))
            return results
        
        # 各テーブルの外部キー整合性をチェック
        for table_name in entity_data.get('entities', {}):
            table_results = self._check_table_foreign_keys(
                table_name, entity_data, ddl_dir, yaml_details_dir
            )
            results.extend(table_results)
        
        return results
    
    def _check_table_foreign_keys(
        self,
        table_name: str,
        entity_data: dict,
        ddl_dir: Path,
        yaml_details_dir: Path
    ) -> List[CheckResult]:
        """単一テーブルの外部キー整合性をチェック"""
        results = []
        
        # DDLファイルとYAML詳細ファイルのパスを構築
        ddl_path = ddl_dir / f"{table_name}.sql"
        yaml_path = yaml_details_dir / f"{table_name}_details.yaml"
        
        if not ddl_path.exists():
            results.append(CheckResult(
                check_type="foreign_key_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"DDLファイルが見つかりません: {ddl_path}",
                details={"file_path": str(ddl_path)}
            ))
            return results
        
        if not yaml_path.exists():
            results.append(CheckResult(
                check_type="foreign_key_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"YAML詳細ファイルが見つかりません: {yaml_path}",
                details={"file_path": str(yaml_path)}
            ))
            return results
        
        # DDLとYAMLから外部キー情報を解析
        ddl_schema = self.column_parser.parse_ddl_file(ddl_path)
        yaml_schema = self.column_parser.parse_yaml_file(yaml_path)
        
        if not ddl_schema or not yaml_schema:
            return results
        
        # entity_relationships.yamlから期待される外部キー関係を抽出
        expected_fks = self._extract_expected_foreign_keys(table_name, entity_data)
        
        # 外部キー整合性チェック
        fk_results = self._compare_foreign_keys(
            table_name, expected_fks, ddl_schema.foreign_keys, yaml_schema.foreign_keys
        )
        results.extend(fk_results)
        
        # 参照整合性チェック
        ref_results = self._check_reference_integrity(
            table_name, ddl_schema.foreign_keys, ddl_dir
        )
        results.extend(ref_results)
        
        return results
    
    def _extract_expected_foreign_keys(
        self, 
        table_name: str, 
        entity_data: dict
    ) -> List[ForeignKeyDefinition]:
        """entity_relationships.yamlから期待される外部キーを抽出"""
        expected_fks = []
        
        # エンティティ定義から外部キーカラムを特定
        entities = entity_data.get('entities', {})
        if table_name not in entities:
            return expected_fks
        
        entity = entities[table_name]
        key_columns = entity.get('key_columns', [])
        
        # 外部キーフラグが設定されているカラムを抽出
        for column in key_columns:
            if column.get('is_fk', False):
                # 関連定義から参照先を特定
                target_info = self._find_foreign_key_target(
                    table_name, column['name'], entity_data
                )
                
                if target_info:
                    fk_def = ForeignKeyDefinition(
                        name=f"fk_{table_name.lower()}_{column['name']}",
                        source_table=table_name,
                        source_columns=[column['name']],
                        target_table=target_info['table'],
                        target_columns=[target_info['column']]
                    )
                    expected_fks.append(fk_def)
        
        # 関連定義からも外部キーを抽出
        relationships = entity_data.get('relationships', [])
        for rel in relationships:
            if rel['source'] == table_name:
                fk_column = rel.get('foreign_key')
                if fk_column:
                    fk_def = ForeignKeyDefinition(
                        name=f"fk_{table_name.lower()}_{fk_column}",
                        source_table=table_name,
                        source_columns=[fk_column],
                        target_table=rel['target'],
                        target_columns=['id'],  # 通常はid
                        description=rel.get('description')
                    )
                    expected_fks.append(fk_def)
        
        return expected_fks
    
    def _find_foreign_key_target(
        self, 
        source_table: str, 
        fk_column: str, 
        entity_data: dict
    ) -> Optional[Dict[str, str]]:
        """外部キーの参照先を特定"""
        relationships = entity_data.get('relationships', [])
        
        for rel in relationships:
            if (rel['source'] == source_table and 
                rel.get('foreign_key') == fk_column):
                return {
                    'table': rel['target'],
                    'column': 'id'  # 通常はid、必要に応じて拡張
                }
        
        # 命名規則による推測（例：department_id -> MST_Department.id）
        if fk_column.endswith('_id'):
            base_name = fk_column[:-3]  # _idを除去
            
            # テーブル名の推測
            possible_tables = [
                f"MST_{base_name.title()}",
                f"MST_{base_name.upper()}",
                f"TRN_{base_name.title()}",
                f"SYS_{base_name.title()}"
            ]
            
            entities = entity_data.get('entities', {})
            for table_name in possible_tables:
                if table_name in entities:
                    return {
                        'table': table_name,
                        'column': 'id'
                    }
        
        return None
    
    def _compare_foreign_keys(
        self,
        table_name: str,
        expected_fks: List[ForeignKeyDefinition],
        ddl_fks: List[Dict],
        yaml_fks: List[Dict]
    ) -> List[CheckResult]:
        """外部キー定義の比較"""
        results = []
        
        # 期待される外部キーをキーでマッピング
        expected_fk_map = {}
        for fk in expected_fks:
            key = (tuple(fk.source_columns), fk.target_table, tuple(fk.target_columns))
            expected_fk_map[key] = fk
        
        # DDLの外部キーをキーでマッピング
        ddl_fk_map = {}
        for fk in ddl_fks:
            key = (tuple(fk['columns']), fk['reference_table'], tuple(fk['reference_columns']))
            ddl_fk_map[key] = fk
        
        # YAMLの外部キーをキーでマッピング
        yaml_fk_map = {}
        for fk in yaml_fks:
            key = (tuple(fk['columns']), fk['reference_table'], tuple(fk['reference_columns']))
            yaml_fk_map[key] = fk
        
        # 期待される外部キーがDDLとYAMLに存在するかチェック
        for fk_key, expected_fk in expected_fk_map.items():
            source_cols, target_table, target_cols = fk_key
            
            # DDLに存在するかチェック
            if fk_key not in ddl_fk_map:
                results.append(CheckResult(
                    check_type="foreign_key_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"外部キー {list(source_cols)} -> {target_table}.{list(target_cols)} がDDLに存在しません",
                    details={
                        "issue_type": "missing_ddl_foreign_key",
                        "source_columns": list(source_cols),
                        "target_table": target_table,
                        "target_columns": list(target_cols)
                    }
                ))
            
            # YAMLに存在するかチェック
            if fk_key not in yaml_fk_map:
                results.append(CheckResult(
                    check_type="foreign_key_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"外部キー {list(source_cols)} -> {target_table}.{list(target_cols)} がYAMLに存在しません",
                    details={
                        "issue_type": "missing_yaml_foreign_key",
                        "source_columns": list(source_cols),
                        "target_table": target_table,
                        "target_columns": list(target_cols)
                    }
                ))
        
        # DDLにのみ存在する外部キー
        ddl_only_keys = set(ddl_fk_map.keys()) - set(expected_fk_map.keys())
        for fk_key in ddl_only_keys:
            source_cols, target_table, target_cols = fk_key
            results.append(CheckResult(
                check_type="foreign_key_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"外部キー {list(source_cols)} -> {target_table}.{list(target_cols)} がDDLにのみ存在します",
                details={
                    "issue_type": "unexpected_ddl_foreign_key",
                    "source_columns": list(source_cols),
                    "target_table": target_table,
                    "target_columns": list(target_cols),
                    "ddl_definition": ddl_fk_map[fk_key]
                }
            ))
        
        # YAMLにのみ存在する外部キー
        yaml_only_keys = set(yaml_fk_map.keys()) - set(expected_fk_map.keys())
        for fk_key in yaml_only_keys:
            source_cols, target_table, target_cols = fk_key
            results.append(CheckResult(
                check_type="foreign_key_consistency",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"外部キー {list(source_cols)} -> {target_table}.{list(target_cols)} がYAMLにのみ存在します",
                details={
                    "issue_type": "unexpected_yaml_foreign_key",
                    "source_columns": list(source_cols),
                    "target_table": target_table,
                    "target_columns": list(target_cols),
                    "yaml_definition": yaml_fk_map[fk_key]
                }
            ))
        
        # 共通する外部キーのカスケード設定チェック
        common_keys = set(ddl_fk_map.keys()) & set(yaml_fk_map.keys())
        for fk_key in common_keys:
            ddl_fk = ddl_fk_map[fk_key]
            yaml_fk = yaml_fk_map[fk_key]
            
            # ON UPDATE設定の比較
            if ddl_fk.get('on_update', 'RESTRICT') != yaml_fk.get('on_update', 'RESTRICT'):
                results.append(CheckResult(
                    check_type="foreign_key_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"外部キー {ddl_fk['name']} のON UPDATE設定が不一致",
                    details={
                        "issue_type": "on_update_mismatch",
                        "foreign_key_name": ddl_fk['name'],
                        "ddl_on_update": ddl_fk.get('on_update', 'RESTRICT'),
                        "yaml_on_update": yaml_fk.get('on_update', 'RESTRICT')
                    }
                ))
            
            # ON DELETE設定の比較
            if ddl_fk.get('on_delete', 'RESTRICT') != yaml_fk.get('on_delete', 'RESTRICT'):
                results.append(CheckResult(
                    check_type="foreign_key_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"外部キー {ddl_fk['name']} のON DELETE設定が不一致",
                    details={
                        "issue_type": "on_delete_mismatch",
                        "foreign_key_name": ddl_fk['name'],
                        "ddl_on_delete": ddl_fk.get('on_delete', 'RESTRICT'),
                        "yaml_on_delete": yaml_fk.get('on_delete', 'RESTRICT')
                    }
                ))
        
        return results
    
    def _check_reference_integrity(
        self,
        table_name: str,
        foreign_keys: List[Dict],
        ddl_dir: Path
    ) -> List[CheckResult]:
        """参照整合性チェック（参照先テーブル・カラムの存在確認）"""
        results = []
        
        for fk in foreign_keys:
            target_table = fk['reference_table']
            target_columns = fk['reference_columns']
            
            # 参照先DDLファイルの存在確認
            target_ddl_path = ddl_dir / f"{target_table}.sql"
            if not target_ddl_path.exists():
                results.append(CheckResult(
                    check_type="foreign_key_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"外部キー {fk['name']} の参照先テーブル {target_table} のDDLファイルが存在しません",
                    details={
                        "issue_type": "missing_target_table_ddl",
                        "foreign_key_name": fk['name'],
                        "target_table": target_table,
                        "target_ddl_path": str(target_ddl_path)
                    }
                ))
                continue
            
            # 参照先テーブルのスキーマを解析
            target_schema = self.column_parser.parse_ddl_file(target_ddl_path)
            if not target_schema:
                results.append(CheckResult(
                    check_type="foreign_key_consistency",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"外部キー {fk['name']} の参照先テーブル {target_table} のDDL解析に失敗",
                    details={
                        "issue_type": "target_table_parse_error",
                        "foreign_key_name": fk['name'],
                        "target_table": target_table
                    }
                ))
                continue
            
            # 参照先カラムの存在確認
            for target_col in target_columns:
                if target_col not in target_schema.columns:
                    results.append(CheckResult(
                        check_type="foreign_key_consistency",
                        table_name=table_name,
                        severity=CheckSeverity.ERROR,
                        message=f"外部キー {fk['name']} の参照先カラム {target_table}.{target_col} が存在しません",
                        details={
                            "issue_type": "missing_target_column",
                            "foreign_key_name": fk['name'],
                            "target_table": target_table,
                            "target_column": target_col,
                            "available_columns": list(target_schema.columns.keys())
                        }
                    ))
        
        return results
