"""
データベース整合性チェックツール - メインチェッカー
"""
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from ..core.models import CheckResult, CheckConfig, ConsistencyReport, CheckSeverity
from ..core.config import Config
from ..core.logger import ConsistencyLogger
from .table_existence_checker import TableExistenceChecker
from .column_consistency_checker import ColumnConsistencyChecker
from .foreign_key_checker import ForeignKeyChecker
from .data_type_consistency_checker import DataTypeConsistencyChecker


class ConsistencyChecker:
    """データベース整合性チェックのメインエンジン"""
    
    def __init__(self, config: Config, check_config: CheckConfig):
        """
        チェッカー初期化
        
        Args:
            config: 設定
            check_config: チェック設定
        """
        self.config = config
        self.check_config = check_config
        self.logger = ConsistencyLogger(verbose=check_config.verbose)
        
        # 各チェッカーの初期化
        self.table_existence_checker = TableExistenceChecker(self.logger)
        self.column_consistency_checker = ColumnConsistencyChecker(self.logger)
        self.foreign_key_checker = ForeignKeyChecker(self.logger)
        self.data_type_checker = DataTypeConsistencyChecker(Path(config.base_dir))
    
    def run_all_checks(self) -> ConsistencyReport:
        """
        全ての整合性チェックを実行
        
        Returns:
            整合性チェックレポート
        """
        self.logger.header("データベース整合性チェック開始")
        
        # 設定の妥当性チェック
        missing_paths = self.config.validate_paths()
        if missing_paths:
            self.logger.error("必要なファイル/ディレクトリが見つかりません:")
            for path in missing_paths:
                self.logger.error(f"  - {path}")
            return self._create_empty_report()
        
        # 出力ディレクトリの作成
        self.config.create_output_dirs()
        
        all_results = []
        
        # 1. テーブル存在チェック
        self.logger.section("1. テーブル存在整合性チェック")
        existence_results = self.table_existence_checker.check_table_existence(
            table_list_file=self.config.table_list_file,
            entity_file=self.config.entity_relationships_file,
            ddl_dir=self.config.ddl_dir,
            table_details_dir=self.config.table_details_dir,
            target_tables=self.check_config.target_tables
        )
        all_results.extend(existence_results)
        
        # 2. 孤立ファイルチェック
        self.logger.section("2. 孤立ファイルチェック")
        orphaned_files = self.table_existence_checker.get_orphaned_files(
            table_list_file=self.config.table_list_file,
            ddl_dir=self.config.ddl_dir,
            table_details_dir=self.config.table_details_dir
        )
        
        orphan_results = self._create_orphan_results(orphaned_files)
        all_results.extend(orphan_results)
        
        # 3. カラム整合性チェック
        self.logger.section("3. カラム定義整合性チェック")
        column_results = self._run_column_consistency_checks()
        all_results.extend(column_results)
        
        # 4. 外部キー整合性チェック
        self.logger.section("4. 外部キー整合性チェック")
        fk_results = self._run_foreign_key_checks()
        all_results.extend(fk_results)
        
        # 5. データ型整合性チェック
        data_type_results = self._run_data_type_checks()
        all_results.extend(data_type_results)
        
        # レポート作成
        report = self._create_report(all_results)
        
        # サマリー表示
        self.logger.print_summary()
        
        self.logger.header("データベース整合性チェック完了")
        
        return report
    
    def run_specific_checks(self, check_names: List[str]) -> ConsistencyReport:
        """
        指定されたチェックのみを実行
        
        Args:
            check_names: 実行するチェック名のリスト
            
        Returns:
            整合性チェックレポート
        """
        self.logger.header(f"指定チェック実行: {', '.join(check_names)}")
        
        all_results = []
        
        if "table_existence" in check_names:
            existence_results = self.table_existence_checker.check_table_existence(
                table_list_file=self.config.table_list_file,
                entity_file=self.config.entity_relationships_file,
                ddl_dir=self.config.ddl_dir,
                table_details_dir=self.config.table_details_dir,
                target_tables=self.check_config.target_tables
            )
            all_results.extend(existence_results)
        
        if "orphaned_files" in check_names:
            orphaned_files = self.table_existence_checker.get_orphaned_files(
                table_list_file=self.config.table_list_file,
                ddl_dir=self.config.ddl_dir,
                table_details_dir=self.config.table_details_dir
            )
            orphan_results = self._create_orphan_results(orphaned_files)
            all_results.extend(orphan_results)
        
        if "column_consistency" in check_names:
            column_results = self._run_column_consistency_checks()
            all_results.extend(column_results)
        
        if "foreign_key_consistency" in check_names:
            fk_results = self._run_foreign_key_checks()
            all_results.extend(fk_results)
        
        if "data_type_consistency" in check_names:
            data_type_results = self._run_data_type_checks()
            all_results.extend(data_type_results)
        
        return self._create_report(all_results)
    
    def _create_orphan_results(self, orphaned_files: Dict[str, List[str]]) -> List[CheckResult]:
        """孤立ファイルの結果を作成"""
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
    
    def _run_data_type_checks(self) -> List[CheckResult]:
        """データ型整合性チェックを実行"""
        results = []
        
        # テーブル一覧から対象テーブルを取得
        from ..parsers.table_list_parser import TableListParser
        table_parser = TableListParser(self.logger)
        tables = table_parser.parse_file(self.config.table_list_file)
        
        if not tables:
            self.logger.warning("テーブル一覧の解析に失敗しました")
            return results
        
        # 対象テーブルのフィルタリング
        target_tables = self.check_config.target_tables
        if target_tables:
            table_names = target_tables
        else:
            table_names = [t.table_name for t in tables]
        
        # データ型整合性チェックを実行
        self.logger.section("5. データ型整合性チェック")
        data_type_results = self.data_type_checker.check_all_tables(table_names)
        results.extend(data_type_results)
        
        # 結果のサマリー表示
        if data_type_results:
            error_count = sum(1 for r in data_type_results if r.severity == CheckSeverity.ERROR)
            warning_count = sum(1 for r in data_type_results if r.severity == CheckSeverity.WARNING)
            success_count = sum(1 for r in data_type_results if r.severity == CheckSeverity.SUCCESS)
            
            if error_count > 0:
                self.logger.error(f"  データ型チェック: {error_count}個のエラー, {warning_count}個の警告, {success_count}個の成功")
            elif warning_count > 0:
                self.logger.warning(f"  データ型チェック: {warning_count}個の警告, {success_count}個の成功")
            else:
                self.logger.success(f"  データ型チェック: {success_count}個の成功")
            
            # 統計情報の表示
            if self.check_config.verbose:
                stats = self.data_type_checker.get_summary_statistics(data_type_results)
                self.logger.info(f"    チェック対象テーブル数: {stats['tables_checked']}")
                self.logger.info(f"    チェック対象カラム数: {stats['columns_checked']}")
        else:
            self.logger.success("  データ型チェック: OK")
        
        return results
    
    def _create_report(self, results: List[CheckResult]) -> ConsistencyReport:
        """整合性チェックレポートを作成"""
        # 統計情報の計算
        summary = {
            'success': sum(1 for r in results if r.severity == CheckSeverity.SUCCESS),
            'warning': sum(1 for r in results if r.severity == CheckSeverity.WARNING),
            'error': sum(1 for r in results if r.severity == CheckSeverity.ERROR),
            'info': sum(1 for r in results if r.severity == CheckSeverity.INFO)
        }
        
        # テーブル数の計算
        unique_tables = set()
        for result in results:
            if result.table_name:
                unique_tables.add(result.table_name)
        
        return ConsistencyReport(
            check_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tables=len(unique_tables),
            total_checks=len(results),
            results=results,
            fix_suggestions=[],  # 修正提案は後で実装
            summary=summary
        )
    
    def _create_empty_report(self) -> ConsistencyReport:
        """空のレポートを作成"""
        return ConsistencyReport(
            check_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tables=0,
            total_checks=0,
            results=[],
            fix_suggestions=[],
            summary={'success': 0, 'warning': 0, 'error': 0, 'info': 0}
        )
    
    def get_available_checks(self) -> List[str]:
        """利用可能なチェック名のリストを取得"""
        return [
            "table_existence",
            "orphaned_files",
            "column_consistency",
            "foreign_key_consistency",
            "data_type_consistency",
            # 将来的に追加予定
            # "constraint_consistency"
        ]
    
    def validate_check_names(self, check_names: List[str]) -> List[str]:
        """
        チェック名の妥当性を検証
        
        Args:
            check_names: チェック名のリスト
            
        Returns:
            無効なチェック名のリスト
        """
        available_checks = self.get_available_checks()
        return [name for name in check_names if name not in available_checks]
    
    def get_check_statistics(self, results: List[CheckResult]) -> Dict[str, Dict[str, int]]:
        """
        チェック別の統計情報を取得
        
        Args:
            results: チェック結果のリスト
            
        Returns:
            チェック別統計情報
        """
        stats = {}
        
        for result in results:
            check_name = result.check_name
            if check_name not in stats:
                stats[check_name] = {
                    'success': 0,
                    'warning': 0,
                    'error': 0,
                    'info': 0,
                    'total': 0
                }
            
            stats[check_name][result.severity.value] += 1
            stats[check_name]['total'] += 1
        
        return stats
    
    def filter_results_by_severity(
        self, 
        results: List[CheckResult], 
        severities: List[CheckSeverity]
    ) -> List[CheckResult]:
        """
        重要度でフィルタリング
        
        Args:
            results: チェック結果のリスト
            severities: フィルタする重要度のリスト
            
        Returns:
            フィルタされたチェック結果
        """
        return [r for r in results if r.severity in severities]
    
    def filter_results_by_table(
        self, 
        results: List[CheckResult], 
        table_names: List[str]
    ) -> List[CheckResult]:
        """
        テーブル名でフィルタリング
        
        Args:
            results: チェック結果のリスト
            table_names: フィルタするテーブル名のリスト
            
        Returns:
            フィルタされたチェック結果
        """
        return [r for r in results if r.table_name in table_names]
    
    def _run_column_consistency_checks(self) -> List[CheckResult]:
        """カラム整合性チェックを実行"""
        results = []
        
        # テーブル一覧から対象テーブルを取得
        from ..parsers.table_list_parser import TableListParser
        table_parser = TableListParser(self.logger)
        tables = table_parser.parse_file(self.config.table_list_file)
        
        if not tables:
            self.logger.warning("テーブル一覧の解析に失敗しました")
            return results
        
        # 対象テーブルのフィルタリング
        target_tables = self.check_config.target_tables
        if target_tables:
            tables = [t for t in tables if t.table_name in target_tables]
        
        # 各テーブルのカラム整合性をチェック
        for table in tables:
            ddl_path = self.config.ddl_dir / f"{table.table_name}.sql"
            yaml_path = self.config.table_details_dir / f"{table.table_name}_details.yaml"
            
            if ddl_path.exists() and yaml_path.exists():
                table_results = self.column_consistency_checker.check_table_column_consistency(
                    ddl_path, yaml_path
                )
                results.extend(table_results)
                
                # 進捗表示
                if table_results:
                    error_count = sum(1 for r in table_results if r.severity == CheckSeverity.ERROR)
                    warning_count = sum(1 for r in table_results if r.severity == CheckSeverity.WARNING)
                    
                    if error_count > 0:
                        self.logger.error(f"  {table.table_name}: {error_count}個のエラー, {warning_count}個の警告")
                    elif warning_count > 0:
                        self.logger.warning(f"  {table.table_name}: {warning_count}個の警告")
                    else:
                        self.logger.success(f"  {table.table_name}: OK")
                else:
                    self.logger.success(f"  {table.table_name}: OK")
            else:
                if not ddl_path.exists():
                    self.logger.warning(f"  {table.table_name}: DDLファイルが見つかりません")
                if not yaml_path.exists():
                    self.logger.warning(f"  {table.table_name}: YAML詳細ファイルが見つかりません")
        
        return results
    
    def _run_foreign_key_checks(self) -> List[CheckResult]:
        """外部キー整合性チェックを実行"""
        results = []
        
        # entity_relationships.yamlの存在確認
        if not self.config.entity_relationships_file.exists():
            self.logger.warning("entity_relationships.yamlが見つかりません")
            return results
        
        # 外部キー整合性チェックを実行
        fk_results = self.foreign_key_checker.check_foreign_key_consistency(
            entity_yaml_path=self.config.entity_relationships_file,
            ddl_dir=self.config.ddl_dir,
            yaml_details_dir=self.config.table_details_dir
        )
        
        results.extend(fk_results)
        
        # 結果のサマリー表示
        if fk_results:
            error_count = sum(1 for r in fk_results if r.severity == CheckSeverity.ERROR)
            warning_count = sum(1 for r in fk_results if r.severity == CheckSeverity.WARNING)
            
            if error_count > 0:
                self.logger.error(f"  外部キーチェック: {error_count}個のエラー, {warning_count}個の警告")
            elif warning_count > 0:
                self.logger.warning(f"  外部キーチェック: {warning_count}個の警告")
            else:
                self.logger.success("  外部キーチェック: OK")
        else:
            self.logger.success("  外部キーチェック: OK")
        
        return results
