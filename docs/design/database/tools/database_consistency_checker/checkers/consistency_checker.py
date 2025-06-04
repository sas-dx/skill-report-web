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
            # 将来的に追加予定
            # "column_consistency",
            # "foreign_key_consistency",
            # "data_type_consistency",
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
