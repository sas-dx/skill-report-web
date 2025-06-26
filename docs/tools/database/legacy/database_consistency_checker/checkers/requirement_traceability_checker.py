"""
要求仕様ID追跡チェック
"""
from pathlib import Path
from typing import List, Dict, Any
import re

from core.models import CheckResult, CheckSeverity
from core.logger import ConsistencyLogger
from parsers.ddl_parser import DDLParser
from parsers.yaml_parser import YAMLParser


class RequirementTraceabilityChecker:
    """
    要求仕様IDの追跡と妥当性をチェックするクラス。
    - 要求仕様ID網羅性確認
    - 要求仕様ID妥当性確認
    - 要求仕様ID形式チェック
    - 未割当項目検出
    """

    def __init__(self, logger: ConsistencyLogger):
        self.logger = logger
        self.yaml_parser = YAMLParser(logger)
        # 要求仕様IDの正規表現パターン: {カテゴリ}.{番号}-{サブカテゴリ}.{番号}
        # 例: PRO.1-BASE.1, TNT.1-MGMT.1
        self.requirement_id_pattern = re.compile(r"^[A-Z]{3}\.\d+-[A-Z]{3}\.\d+$")

    def check_requirement_traceability(self, yaml_details_dir: Path, table_names: List[str]) -> List[CheckResult]:
        """
        指定されたテーブルの要求仕様ID追跡をチェックする。

        Args:
            yaml_details_dir (Path): YAML詳細定義ファイルが格納されているディレクトリのパス。
            table_names (List[str]): チェック対象のテーブル名のリスト。

        Returns:
            List[CheckResult]: チェック結果のリスト。
        """
        results: List[CheckResult] = []
        self.logger.info("要求仕様ID追跡チェックを開始します...")

        for table_name in table_names:
            yaml_path = yaml_details_dir / f"{table_name}_details.yaml"

            if not yaml_path.exists():
                results.append(CheckResult(
                    check_name="requirement_traceability",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"YAML詳細定義ファイルが見つかりません: {yaml_path}",
                    details={"file_path": str(yaml_path)}
                ))
                continue

            yaml_table_info = self.yaml_parser.parse_yaml_file(yaml_path)

            if not yaml_table_info:
                results.append(CheckResult(
                    check_name="requirement_traceability",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="YAMLファイルのパースに失敗しました。",
                    details={"yaml_path": str(yaml_path)}
                ))
                continue

            # テーブルレベルの要求仕様IDチェック
            results.extend(self._check_table_requirement_id(table_name, yaml_table_info))

            # カラムレベルの要求仕様IDチェック
            results.extend(self._check_column_requirement_ids(table_name, yaml_table_info))

        self.logger.info("要求仕様ID追跡チェックが完了しました。")
        return results

    def _check_table_requirement_id(self, table_name: str, yaml_table_info: Dict[str, Any]) -> List[CheckResult]:
        """テーブルレベルの要求仕様IDをチェックする。"""
        results: List[CheckResult] = []
        
        req_id = yaml_table_info.get('requirement_id')
        if not req_id:
            results.append(CheckResult(
                check_name="requirement_traceability",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message="テーブルレベルの'requirement_id'が見つかりません。",
                details={"check": "table_requirement_id_missing"}
            ))
        elif not self.requirement_id_pattern.match(req_id):
            results.append(CheckResult(
                check_name="requirement_traceability",
                table_name=table_name,
                severity=CheckSeverity.ERROR,
                message=f"テーブルレベルの'requirement_id'の形式が不正です: '{req_id}'",
                details={"check": "table_requirement_id_format_invalid", "requirement_id": req_id}
            ))
        else:
            results.append(CheckResult(
                check_name="requirement_traceability",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message=f"テーブルレベルの'requirement_id'が適切に定義されています: '{req_id}'",
                details={"check": "table_requirement_id_ok", "requirement_id": req_id}
            ))
        
        return results

    def _check_column_requirement_ids(self, table_name: str, yaml_table_info: Dict[str, Any]) -> List[CheckResult]:
        """カラムレベルの要求仕様IDをチェックする。"""
        results: List[CheckResult] = []
        
        columns = yaml_table_info.get('columns', [])
        for column in columns:
            col_name = column.get('name', 'Unnamed Column')
            req_id = column.get('requirement_id')

            if not req_id:
                results.append(CheckResult(
                    check_name="requirement_traceability",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"カラム '{col_name}' に'requirement_id'が見つかりません。",
                    details={"check": "column_requirement_id_missing", "column_name": col_name}
                ))
            elif not self.requirement_id_pattern.match(req_id):
                results.append(CheckResult(
                    check_name="requirement_traceability",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message=f"カラム '{col_name}' の'requirement_id'の形式が不正です: '{req_id}'",
                    details={"check": "column_requirement_id_format_invalid", "column_name": col_name, "requirement_id": req_id}
                ))
            else:
                results.append(CheckResult(
                    check_name="requirement_traceability",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message=f"カラム '{col_name}' の'requirement_id'が適切に定義されています: '{req_id}'",
                    details={"check": "column_requirement_id_ok", "column_name": col_name, "requirement_id": req_id}
                ))
        
        return results
