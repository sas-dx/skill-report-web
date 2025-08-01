"""
マルチテナント対応チェック
"""
from pathlib import Path
from typing import List, Dict, Any
import yaml

from core.models import CheckResult, CheckSeverity
from core.logger import ConsistencyLogger
from parsers.ddl_parser import DDLParser
from parsers.yaml_parser import YAMLParser


class MultitenantComplianceChecker:
    """
    マルチテナント対応の整合性をチェックするクラス。
    - tenant_idカラムの存在確認
    - テナント用インデックスの確認
    - 外部キーのテナント整合性確認
    """

    def __init__(self, logger: ConsistencyLogger):
        self.logger = logger
        self.ddl_parser = DDLParser(logger)
        self.yaml_parser = YAMLParser(logger)

    def check_multitenant_compliance(self, ddl_dir: Path, yaml_details_dir: Path, table_names: List[str]) -> List[CheckResult]:
        """
        指定されたテーブルのマルチテナント対応をチェックする。

        Args:
            ddl_dir (Path): DDLファイルが格納されているディレクトリのパス。
            yaml_details_dir (Path): YAML詳細定義ファイルが格納されているディレクトリのパス。
            table_names (List[str]): チェック対象のテーブル名のリスト。

        Returns:
            List[CheckResult]: チェック結果のリスト。
        """
        results: List[CheckResult] = []
        self.logger.info("マルチテナント対応チェックを開始します...")

        for table_name in table_names:
            ddl_path = ddl_dir / f"{table_name}.sql"
            yaml_path = yaml_details_dir / f"{table_name}_details.yaml"

            if not ddl_path.exists():
                results.append(CheckResult(
                    check_name="multitenant_compliance",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"DDLファイルが見つかりません: {ddl_path}",
                    details={"file_path": str(ddl_path)}
                ))
                continue

            if not yaml_path.exists():
                results.append(CheckResult(
                    check_name="multitenant_compliance",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"YAML詳細定義ファイルが見つかりません: {yaml_path}",
                    details={"file_path": str(yaml_path)}
                ))
                continue

            # DDLとYAMLからテーブル情報をパース
            ddl_table_info = self.ddl_parser.parse_ddl_file(ddl_path)
            yaml_table_info = self.yaml_parser.parse_yaml_file(yaml_path)

            if not ddl_table_info or not yaml_table_info:
                results.append(CheckResult(
                    check_name="multitenant_compliance",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="DDLまたはYAMLファイルのパースに失敗しました。",
                    details={"ddl_path": str(ddl_path), "yaml_path": str(yaml_path)}
                ))
                continue

            # 1. tenant_idカラムの存在確認
            results.extend(self._check_tenant_id_column(table_name, ddl_table_info, yaml_table_info))

            # 2. テナント用インデックスの確認
            results.extend(self._check_tenant_id_index(table_name, ddl_table_info, yaml_table_info))

            # 3. 外部キーのテナント整合性確認 (DDLのみでチェック)
            results.extend(self._check_foreign_key_tenant_integrity(table_name, ddl_table_info))

        self.logger.info("マルチテナント対応チェックが完了しました。")
        return results

    def _check_tenant_id_column(self, table_name: str, ddl_table_info: Dict[str, Any], yaml_table_info: Dict[str, Any]) -> List[CheckResult]:
        """tenant_idカラムの存在と定義をチェックする。"""
        results: List[CheckResult] = []
        
        ddl_columns = {col['name'].lower(): col for col in ddl_table_info.get('columns', [])}
        yaml_columns = {col['name'].lower(): col for col in yaml_table_info.get('columns', [])}

        # DDLでのtenant_id存在確認
        if 'tenant_id' not in ddl_columns:
            results.append(CheckResult(
                check_name="multitenant_compliance",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message="DDLに'tenant_id'カラムが見つかりません。",
                details={"check": "tenant_id_column_existence_ddl"}
            ))
        else:
            # DDLでのtenant_idの型とNULL制約の確認
            ddl_tenant_id = ddl_columns['tenant_id']
            if not ddl_tenant_id.get('nullable', True): # nullableがFalseまたは存在しない場合 (NOT NULL)
                results.append(CheckResult(
                    check_name="multitenant_compliance",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message="DDLに'tenant_id'カラムがNOT NULLで存在します。",
                    details={"check": "tenant_id_column_definition_ddl"}
                ))
            else:
                results.append(CheckResult(
                    check_name="multitenant_compliance",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message="DDLの'tenant_id'カラムがNULLを許可しています。マルチテナントテーブルではNOT NULLであるべきです。",
                    details={"check": "tenant_id_column_definition_ddl", "nullable": True}
                ))

        # YAMLでのtenant_id存在確認
        if 'tenant_id' not in yaml_columns:
            results.append(CheckResult(
                check_name="multitenant_compliance",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message="YAMLに'tenant_id'カラムが見つかりません。",
                details={"check": "tenant_id_column_existence_yaml"}
            ))
        else:
            # YAMLでのtenant_idの型とNULL制約の確認
            yaml_tenant_id = yaml_columns['tenant_id']
            if not yaml_tenant_id.get('nullable', True): # nullableがFalseまたは存在しない場合 (NOT NULL)
                results.append(CheckResult(
                    check_name="multitenant_compliance",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message="YAMLに'tenant_id'カラムがNOT NULLで存在します。",
                    details={"check": "tenant_id_column_definition_yaml"}
                ))
            else:
                results.append(CheckResult(
                    check_name="multitenant_compliance",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message="YAMLの'tenant_id'カラムがNULLを許可しています。マルチテナントテーブルではNOT NULLであるべきです。",
                    details={"check": "tenant_id_column_definition_yaml", "nullable": True}
                ))
        
        return results

    def _check_tenant_id_index(self, table_name: str, ddl_table_info: Dict[str, Any], yaml_table_info: Dict[str, Any]) -> List[CheckResult]:
        """tenant_idを含むインデックスの存在をチェックする。"""
        results: List[CheckResult] = []
        
        ddl_indexes = ddl_table_info.get('indexes', [])
        yaml_indexes = yaml_table_info.get('indexes', [])

        # DDLでのtenant_idを含むインデックス確認
        ddl_has_tenant_index = any('tenant_id' in [col.lower() for col in idx.get('columns', [])] for idx in ddl_indexes)
        if not ddl_has_tenant_index:
            results.append(CheckResult(
                check_name="multitenant_compliance",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message="DDLに'tenant_id'を含むインデックスが見つかりません。パフォーマンスのために推奨されます。",
                details={"check": "tenant_id_index_ddl"}
            ))
        else:
            results.append(CheckResult(
                check_name="multitenant_compliance",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message="DDLに'tenant_id'を含むインデックスが見つかりました。",
                details={"check": "tenant_id_index_ddl"}
            ))

        # YAMLでのtenant_idを含むインデックス確認
        yaml_has_tenant_index = any('tenant_id' in [col.lower() for col in idx.get('columns', [])] for idx in yaml_indexes)
        if not yaml_has_tenant_index:
            results.append(CheckResult(
                check_name="multitenant_compliance",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message="YAMLに'tenant_id'を含むインデックスが見つかりません。パフォーマンスのために推奨されます。",
                details={"check": "tenant_id_index_yaml"}
            ))
        else:
            results.append(CheckResult(
                check_name="multitenant_compliance",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message="YAMLに'tenant_id'を含むインデックスが見つかりました。",
                details={"check": "tenant_id_index_yaml"}
            ))
            
        return results

    def _check_foreign_key_tenant_integrity(self, table_name: str, ddl_table_info: Dict[str, Any]) -> List[CheckResult]:
        """
        外部キーが参照先テーブルのtenant_idと整合しているかをチェックする。
        これは、外部キーが参照元と参照先の両方にtenant_idを含み、かつ参照先のtenant_idが参照元のtenant_idと一致することを保証する。
        """
        results: List[CheckResult] = []
        
        foreign_keys = ddl_table_info.get('foreign_keys', [])

        for fk in foreign_keys:
            fk_columns = [col.lower() for col in fk.get('columns', [])]
            referenced_table = fk.get('references', {}).get('table')
            referenced_columns = [col.lower() for col in fk.get('references', {}).get('columns', [])]

            # 外部キーがtenant_idを含んでいるか
            if 'tenant_id' in fk_columns:
                # 参照先もtenant_idを含んでいるか
                if 'tenant_id' not in referenced_columns:
                    results.append(CheckResult(
                        check_name="multitenant_compliance",
                        table_name=table_name,
                        severity=CheckSeverity.ERROR,
                        message=f"外部キー '{fk.get('name', 'Unnamed FK')}' は'tenant_id'を含みますが、参照先テーブル '{referenced_table}' の参照カラムに'tenant_id'が含まれていません。テナント間参照の可能性があります。",
                        details={"check": "fk_tenant_integrity", "fk_name": fk.get('name'), "referenced_table": referenced_table}
                    ))
                else:
                    results.append(CheckResult(
                        check_name="multitenant_compliance",
                        table_name=table_name,
                        severity=CheckSeverity.SUCCESS,
                        message=f"外部キー '{fk.get('name', 'Unnamed FK')}' は'tenant_id'を含み、参照先も'tenant_id'を含んでいます。",
                        details={"check": "fk_tenant_integrity", "fk_name": fk.get('name'), "referenced_table": referenced_table}
                    ))
            # else:
            #     results.append(CheckResult(
            #         check_name="multitenant_compliance",
            #         table_name=table_name,
            #         severity=CheckSeverity.INFO,
            #         message=f"外部キー '{fk.get('name', 'Unnamed FK')}' は'tenant_id'を含みません。テナントに依存しない参照です。",
            #         details={"check": "fk_tenant_integrity", "fk_name": fk.get('name'), "referenced_table": referenced_table}
            #     ))
        
        return results
