"""
パフォーマンス影響分析チェック
"""
from pathlib import Path
from typing import List, Dict, Any
import re

from core.models import CheckResult, CheckSeverity
from core.logger import ConsistencyLogger
from parsers.ddl_parser import DDLParser
from parsers.yaml_parser import YAMLParser


class PerformanceImpactChecker:
    """
    パフォーマンス影響を分析するクラス。
    - インデックスカバレッジ分析
    - クエリパフォーマンス予測
    - データ量影響分析
    """

    def __init__(self, logger: ConsistencyLogger):
        self.logger = logger
        self.ddl_parser = DDLParser(logger)
        self.yaml_parser = YAMLParser(logger)

    def check_performance_impact(self, ddl_dir: Path, yaml_details_dir: Path, table_names: List[str]) -> List[CheckResult]:
        """
        指定されたテーブルのパフォーマンス影響をチェックする。

        Args:
            ddl_dir (Path): DDLファイルが格納されているディレクトリのパス。
            yaml_details_dir (Path): YAML詳細定義ファイルが格納されているディレクトリのパス。
            table_names (List[str]): チェック対象のテーブル名のリスト。

        Returns:
            List[CheckResult]: チェック結果のリスト。
        """
        results: List[CheckResult] = []
        self.logger.info("パフォーマンス影響分析チェックを開始します...")

        for table_name in table_names:
            ddl_path = ddl_dir / f"{table_name}.sql"
            yaml_path = yaml_details_dir / f"{table_name}_details.yaml"

            if not ddl_path.exists():
                results.append(CheckResult(
                    check_name="performance_impact",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"DDLファイルが見つかりません: {ddl_path}",
                    details={"file_path": str(ddl_path)}
                ))
                continue

            if not yaml_path.exists():
                results.append(CheckResult(
                    check_name="performance_impact",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"YAML詳細定義ファイルが見つかりません: {yaml_path}",
                    details={"file_path": str(yaml_path)}
                ))
                continue

            ddl_table_info = self.ddl_parser.parse_ddl_file(ddl_path)
            yaml_table_info = self.yaml_parser.parse_yaml_file(yaml_path)

            if not ddl_table_info or not yaml_table_info:
                results.append(CheckResult(
                    check_name="performance_impact",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="DDLまたはYAMLファイルのパースに失敗しました。",
                    details={"ddl_path": str(ddl_path), "yaml_path": str(yaml_path)}
                ))
                continue

            # 1. インデックスカバレッジ分析 (簡易版)
            results.extend(self._analyze_index_coverage(table_name, ddl_table_info, yaml_table_info))

            # 2. データ量影響分析 (YAMLの想定データ量とパフォーマンス要件から簡易予測)
            results.extend(self._analyze_data_volume_impact(table_name, yaml_table_info))

            # 3. クエリパフォーマンス予測 (簡易版 - 主キー/ユニークキーの利用を推奨)
            results.extend(self._predict_query_performance(table_name, ddl_table_info))

        self.logger.info("パフォーマンス影響分析チェックが完了しました。")
        return results

    def _analyze_index_coverage(self, table_name: str, ddl_table_info: Dict[str, Any], yaml_table_info: Dict[str, Any]) -> List[CheckResult]:
        """
        インデックスカバレッジを簡易的に分析する。
        - 主キー、ユニークキー、外部キーにインデックスがあるか
        - YAMLで定義されたインデックスがDDLに存在するか
        """
        results: List[CheckResult] = []
        
        ddl_indexes = ddl_table_info.get('indexes', [])
        yaml_indexes = yaml_table_info.get('indexes', [])
        ddl_columns = ddl_table_info.get('columns', [])

        # 主キーにインデックスがあるか (DDLから確認)
        pk_columns = [col['name'].lower() for col in ddl_columns if col.get('primary_key')]
        if pk_columns:
            has_pk_index = any(set(pk_columns).issubset([c.lower() for c in idx.get('columns', [])]) for idx in ddl_indexes)
            if not has_pk_index:
                results.append(CheckResult(
                    check_name="performance_impact",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"主キー '{', '.join(pk_columns)}' に対応するインデックスが見つかりません。通常、主キーには自動的にインデックスが作成されますが、確認が必要です。",
                    details={"check": "pk_index_coverage"}
                ))
            else:
                results.append(CheckResult(
                    check_name="performance_impact",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message=f"主キー '{', '.join(pk_columns)}' に対応するインデックスが見つかりました。",
                    details={"check": "pk_index_coverage"}
                ))

        # YAMLで定義されたインデックスがDDLに存在するか
        for yaml_idx in yaml_indexes:
            yaml_idx_name = yaml_idx.get('name')
            yaml_idx_cols = [c.lower() for c in yaml_idx.get('columns', [])]
            
            found_in_ddl = False
            for ddl_idx in ddl_indexes:
                ddl_idx_cols = [c.lower() for c in ddl_idx.get('columns', [])]
                if set(yaml_idx_cols) == set(ddl_idx_cols): # カラムが一致すればOKとする (名前は異なっても良い)
                    found_in_ddl = True
                    break
            
            if not found_in_ddl:
                results.append(CheckResult(
                    check_name="performance_impact",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message=f"YAMLで定義されたインデックス '{yaml_idx_name}' (カラム: {', '.join(yaml_idx_cols)}) がDDLに見つかりません。",
                    details={"check": "yaml_index_ddl_mismatch", "index_name": yaml_idx_name, "columns": yaml_idx_cols}
                ))
            else:
                results.append(CheckResult(
                    check_name="performance_impact",
                    table_name=table_name,
                    severity=CheckSeverity.SUCCESS,
                    message=f"YAMLで定義されたインデックス '{yaml_idx_name}' がDDLに存在します。",
                    details={"check": "yaml_index_ddl_match", "index_name": yaml_idx_name}
                ))
        
        return results

    def _analyze_data_volume_impact(self, table_name: str, yaml_table_info: Dict[str, Any]) -> List[CheckResult]:
        """
        データ量の影響を分析する。
        - YAMLの`data_volume`セクションから初期データ件数、月間増加件数、5年後想定件数を取得
        - `category`と`priority`からパフォーマンス要件を推測し、データ量が適切か簡易的に判断
        """
        results: List[CheckResult] = []
        
        data_volume = yaml_table_info.get('data_volume', {})
        initial_records = data_volume.get('initial_records')
        monthly_increase = data_volume.get('monthly_increase')
        five_year_estimate = data_volume.get('five_year_estimate')
        
        category = yaml_table_info.get('category')
        priority = yaml_table_info.get('priority')

        if not all([initial_records, monthly_increase, five_year_estimate]):
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.INFO,
                message="データ量見積もり情報がYAMLに不足しています。パフォーマンス分析の精度が低下します。",
                details={"check": "data_volume_missing"}
            ))
            return results

        # 簡易的なパフォーマンス要件の推測とデータ量評価
        # マスタ系: 高速参照重視（5-10ms以内）
        # トランザクション系: バランス重視（15-50ms以内）
        # システム系: 書き込み重視、参照は許容範囲
        # 履歴系: 書き込み重視、参照は低頻度
        # ワーク系: 処理効率重視

        # 5年後想定件数に基づく簡易的な警告
        if category == "マスタ系" and five_year_estimate > 100000:
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"マスタ系テーブル '{table_name}' の5年後想定件数 ({five_year_estimate}件) が多いです。パフォーマンス劣化の可能性があります。",
                details={"check": "data_volume_high", "category": category, "estimate": five_year_estimate}
            ))
        elif category == "トランザクション系" and five_year_estimate > 10000000:
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message=f"トランザクション系テーブル '{table_name}' の5年後想定件数 ({five_year_estimate}件) が非常に多いです。パーティショニング等の検討が必要です。",
                details={"check": "data_volume_very_high", "category": category, "estimate": five_year_estimate}
            ))
        else:
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message=f"データ量見積もりは適切に見えます (5年後想定: {five_year_estimate}件)。",
                details={"check": "data_volume_ok", "category": category, "estimate": five_year_estimate}
            ))
        
        return results

    def _predict_query_performance(self, table_name: str, ddl_table_info: Dict[str, Any]) -> List[CheckResult]:
        """
        クエリパフォーマンスを簡易的に予測する。
        - 主キー、ユニークキーが適切に定義されているか
        - 検索頻度の高いカラムにインデックスがあるか (YAMLの`indexes`セクションから推測)
        """
        results: List[CheckResult] = []
        
        ddl_columns = ddl_table_info.get('columns', [])
        ddl_indexes = ddl_table_info.get('indexes', [])

        # 主キーの存在確認
        pk_exists = any(col.get('primary_key') for col in ddl_columns)
        if not pk_exists:
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.WARNING,
                message="主キーが定義されていません。主キーは高速なレコードアクセスに不可欠です。",
                details={"check": "pk_missing"}
            ))
        else:
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message="主キーが適切に定義されています。",
                details={"check": "pk_exists"}
            ))

        # ユニークキーの存在確認 (DDLのユニーク制約から)
        unique_constraints = [idx for idx in ddl_indexes if idx.get('unique')]
        if not unique_constraints:
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.INFO,
                message="ユニーク制約が定義されていません。ユニークな値を持つカラムにはユニーク制約とインデックスを検討してください。",
                details={"check": "unique_constraint_missing"}
            ))
        else:
            results.append(CheckResult(
                check_name="performance_impact",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message=f"ユニーク制約が定義されています ({len(unique_constraints)}件)。",
                details={"check": "unique_constraint_exists", "count": len(unique_constraints)}
            ))
        
        return results
