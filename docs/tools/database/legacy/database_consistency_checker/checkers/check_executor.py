from typing import List, Dict
from pathlib import Path
from core.models import CheckResult, CheckSeverity
from core.logger import ConsistencyLogger
from checkers.table_existence_checker import TableExistenceChecker
from checkers.column_consistency_checker import ColumnConsistencyChecker
from checkers.foreign_key_checker import ForeignKeyChecker
from checkers.data_type_consistency_checker import DataTypeConsistencyChecker
from checkers.yaml_format_checker import YamlFormatChecker
from checkers.constraint_consistency_checker import ConstraintConsistencyChecker
from checkers.multitenant_compliance_checker import MultitenantComplianceChecker
from checkers.requirement_traceability_checker import RequirementTraceabilityChecker
from checkers.performance_impact_checker import PerformanceImpactChecker
from parsers.table_list_parser import TableListParser

class CheckExecutor:
    """
    個々の整合性チェックを実行するクラス
    """

    def __init__(self, logger: ConsistencyLogger, config, check_config):
        self.logger = logger
        self.config = config
        self.check_config = check_config

        self.table_existence_checker = TableExistenceChecker(self.logger)
        self.column_consistency_checker = ColumnConsistencyChecker(self.logger)
        self.foreign_key_checker = ForeignKeyChecker(self.logger)
        self.data_type_checker = DataTypeConsistencyChecker(Path(config.base_dir))
        self.yaml_format_checker = YamlFormatChecker(config.base_dir)
        self.constraint_checker = ConstraintConsistencyChecker(self.logger)
        self.multitenant_compliance_checker = MultitenantComplianceChecker(self.logger)
        self.requirement_traceability_checker = RequirementTraceabilityChecker(self.logger)
        self.performance_impact_checker = PerformanceImpactChecker(self.logger)
        self.table_list_parser = TableListParser(self.logger)

    def _get_target_table_names(self) -> List[str]:
        """対象テーブル名を取得するヘルパーメソッド"""
        tables = self.table_list_parser.parse_file(self.config.table_list_file)
        if not tables:
            self.logger.warning("テーブル一覧の解析に失敗しました")
            return []
        if self.check_config.target_tables:
            return self.check_config.target_tables
        return [t.table_name for t in tables]

    def execute_table_existence_check(self) -> List[CheckResult]:
        self.logger.section("1. テーブル存在確認")
        return self.table_existence_checker.check_table_existence(
            table_list_file=self.config.table_list_file,
            entity_file=self.config.entity_relationships_file,
            ddl_dir=self.config.ddl_dir,
            table_details_dir=self.config.table_details_dir,
            target_tables=self.check_config.target_tables
        )

    def execute_orphaned_files_check(self) -> List[CheckResult]:
        self.logger.section("2. 孤立ファイル検出")
        orphaned_files = self.table_existence_checker.get_orphaned_files(
            table_list_file=self.config.table_list_file,
            ddl_dir=self.config.ddl_dir,
            table_details_dir=self.config.table_details_dir
        )
        results = []
        for file_type, files in orphaned_files.items():
            if files:
                for file_name in files:
                    results.append(CheckResult(
                        check_name="orphaned_files",
                        table_name="",
                        severity=CheckSeverity.WARNING,
                        message=f"孤立ファイル: {file_name}",
                        details={
                            'file_type': file_type,
                            'file_name': file_name,
                            'reason': 'テーブル一覧.mdに対応するテーブルが見つかりません'
                        }
                    ))
        if not any(orphaned_files.values()):
            results.append(CheckResult(
                check_name="orphaned_files",
                table_name="",
                severity=CheckSeverity.SUCCESS,
                message="孤立ファイルは見つかりませんでした",
                details={}
            ))
        return results

    def execute_yaml_format_check(self) -> List[CheckResult]:
        self.logger.section("3. YAMLフォーマット整合性")
        table_names = self._get_target_table_names()
        yaml_format_results = self.yaml_format_checker.check_yaml_format_consistency(table_names)
        
        results = []
        for result in yaml_format_results:
            severity = CheckSeverity.SUCCESS
            if hasattr(result, 'status'):
                if result.status.name == 'ERROR':
                    severity = CheckSeverity.ERROR
                elif result.status.name == 'WARNING':
                    severity = CheckSeverity.WARNING
                elif result.status.name == 'INFO':
                    severity = CheckSeverity.INFO
            elif hasattr(result, 'severity'):
                severity = result.severity
            
            converted_result = CheckResult(
                check_name="yaml_format_consistency",
                table_name=getattr(result, 'table_name', ''),
                severity=severity,
                message=getattr(result, 'message', ''),
                details=getattr(result, 'details', {})
            )
            results.append(converted_result)
        return results

    def execute_column_consistency_check(self) -> List[CheckResult]:
        self.logger.section("4. カラム定義整合性")
        results = []
        tables = self.table_list_parser.parse_file(self.config.table_list_file)
        if not tables:
            self.logger.warning("テーブル一覧の解析に失敗しました")
            return results
        
        if self.check_config.target_tables:
            tables = [t for t in tables if t.table_name in self.check_config.target_tables]
        
        for table in tables:
            ddl_path = self.config.ddl_dir / f"{table.table_name}.sql"
            yaml_path = self.config.table_details_dir / f"{table.table_name}_details.yaml"
            
            if ddl_path.exists() and yaml_path.exists():
                table_results = self.column_consistency_checker.check_table_column_consistency(
                    ddl_path, yaml_path
                )
                results.extend(table_results)
            else:
                if not ddl_path.exists():
                    self.logger.warning(f"  {table.table_name}: DDLファイルが見つかりません")
                if not yaml_path.exists():
                    self.logger.warning(f"  {table.table_name}: YAML詳細ファイルが見つかりません")
        return results

    def execute_foreign_key_check(self) -> List[CheckResult]:
        self.logger.section("5. 外部キー整合性")
        if not self.config.entity_relationships_file.exists():
            self.logger.warning("entity_relationships.yamlが見つかりません")
            return []
        
        return self.foreign_key_checker.check_foreign_key_consistency(
            entity_yaml_path=self.config.entity_relationships_file,
            ddl_dir=self.config.ddl_dir,
            yaml_details_dir=self.config.table_details_dir
        )

    def execute_data_type_check(self) -> List[CheckResult]:
        self.logger.section("6. データ型整合性")
        table_names = self._get_target_table_names()
        return self.data_type_checker.check_all_tables(table_names)

    def execute_constraint_check(self) -> List[CheckResult]:
        self.logger.section("7. 制約整合性")
        table_names = self._get_target_table_names()
        return self.constraint_checker.check_constraint_consistency(
            ddl_dir=self.config.ddl_dir,
            yaml_details_dir=self.config.table_details_dir,
            table_names=table_names
        )

    def execute_multitenant_compliance_check(self) -> List[CheckResult]:
        self.logger.section("9. マルチテナント対応")
        table_names = self._get_target_table_names()
        return self.multitenant_compliance_checker.check_multitenant_compliance(
            ddl_dir=self.config.ddl_dir,
            yaml_details_dir=self.config.table_details_dir,
            table_names=table_names
        )

    def execute_requirement_traceability_check(self) -> List[CheckResult]:
        self.logger.section("10. 要求仕様ID追跡")
        table_names = self._get_target_table_names()
        return self.requirement_traceability_checker.check_requirement_traceability(
            yaml_details_dir=self.config.table_details_dir,
            table_names=table_names
        )

    def execute_performance_impact_check(self) -> List[CheckResult]:
        self.logger.section("11. パフォーマンス影響分析")
        table_names = self._get_target_table_names()
        return self.performance_impact_checker.check_performance_impact(
            ddl_dir=self.config.ddl_dir,
            yaml_details_dir=self.config.table_details_dir,
            table_names=table_names
        )
