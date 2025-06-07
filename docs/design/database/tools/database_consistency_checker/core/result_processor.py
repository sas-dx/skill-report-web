from typing import List, Dict
from core.models import CheckResult, CheckSeverity

class ResultProcessor:
    """
    チェック結果の処理、集計、フィルタリングを行うクラス
    """

    def __init__(self):
        pass

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

    def get_summary_statistics(self, results: List[CheckResult]) -> Dict[str, int]:
        """
        全体のサマリー統計情報を取得
        """
        summary = {
            'success': sum(1 for r in results if r.severity == CheckSeverity.SUCCESS),
            'warning': sum(1 for r in results if r.severity == CheckSeverity.WARNING),
            'error': sum(1 for r in results if r.severity == CheckSeverity.ERROR),
            'info': sum(1 for r in results if r.severity == CheckSeverity.INFO)
        }
        return summary
