"""
データベース整合性チェックツール - JSONレポーター
"""
import json
import sys
from pathlib import Path
from typing import Dict, Any

# パス解決のセットアップ
_current_dir = Path(__file__).parent
_tools_dir = _current_dir.parent.parent
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

# 絶対インポートを使用
from database_consistency_checker.core.models import ConsistencyReport, CheckResult, CheckSeverity, FixSuggestion
from database_consistency_checker.core.check_definitions import get_japanese_check_name


class JsonReporter:
    """JSON出力用レポーター"""
    
    def __init__(self, indent: int = 2):
        """
        レポーター初期化
        
        Args:
            indent: JSON出力のインデント数
        """
        self.indent = indent
    
    def generate_report(self, report: ConsistencyReport) -> str:
        """
        JSON形式のレポートを生成
        
        Args:
            report: 整合性チェックレポート
            
        Returns:
            JSONレポート文字列
        """
        report_dict = self._convert_report_to_dict(report)
        return json.dumps(report_dict, ensure_ascii=False, indent=self.indent)
    
    def _convert_report_to_dict(self, report: ConsistencyReport) -> Dict[str, Any]:
        """レポートを辞書形式に変換"""
        return {
            "metadata": {
                "check_date": report.check_date,
                "total_tables": report.total_tables,
                "total_checks": report.total_checks,
                "tool_version": "1.0.0"
            },
            "summary": report.summary,
            "statistics": self._generate_statistics(report),
            "results": [self._convert_result_to_dict(result) for result in report.results],
            "fix_suggestions": [self._convert_fix_suggestion_to_dict(fix) for fix in report.fix_suggestions],
            "check_details": self._generate_check_details(report)
        }
    
    def _convert_result_to_dict(self, result: CheckResult) -> Dict[str, Any]:
        """チェック結果を辞書形式に変換"""
        return {
            "check_name": result.check_name,
            "check_name_japanese": get_japanese_check_name(result.check_name),
            "table_name": result.table_name,
            "severity": result.severity.value,
            "message": result.message,
            "details": result.details,
            "file_path": result.file_path,
            "line_number": result.line_number
        }
    
    def _convert_fix_suggestion_to_dict(self, fix: FixSuggestion) -> Dict[str, Any]:
        """修正提案を辞書形式に変換"""
        return {
            "fix_type": fix.fix_type.value,
            "table_name": fix.table_name,
            "description": fix.description,
            "fix_content": fix.fix_content,
            "file_path": fix.file_path,
            "backup_required": fix.backup_required,
            "critical": fix.critical
        }
    
    def _generate_statistics(self, report: ConsistencyReport) -> Dict[str, Any]:
        """統計情報を生成"""
        total_checks = report.total_checks
        
        # 基本統計
        stats = {
            "success_rate": (report.summary.get('success', 0) / total_checks * 100) if total_checks > 0 else 0,
            "warning_rate": (report.summary.get('warning', 0) / total_checks * 100) if total_checks > 0 else 0,
            "error_rate": (report.summary.get('error', 0) / total_checks * 100) if total_checks > 0 else 0,
            "info_rate": (report.summary.get('info', 0) / total_checks * 100) if total_checks > 0 else 0
        }
        
        # チェック別統計
        check_stats = {}
        for result in report.results:
            check_name = result.check_name
            if check_name not in check_stats:
                check_stats[check_name] = {
                    'success': 0,
                    'warning': 0,
                    'error': 0,
                    'info': 0,
                    'total': 0
                }
            
            check_stats[check_name][result.severity.value] += 1
            check_stats[check_name]['total'] += 1
        
        stats["by_check"] = check_stats
        
        # テーブル別統計
        table_stats = {}
        for result in report.results:
            if result.table_name:
                table_name = result.table_name
                if table_name not in table_stats:
                    table_stats[table_name] = {
                        'success': 0,
                        'warning': 0,
                        'error': 0,
                        'info': 0,
                        'total': 0
                    }
                
                table_stats[table_name][result.severity.value] += 1
                table_stats[table_name]['total'] += 1
        
        stats["by_table"] = table_stats
        
        return stats
    
    def _generate_check_details(self, report: ConsistencyReport) -> Dict[str, Any]:
        """チェック詳細情報を生成"""
        details = {}
        
        # 重要度別の結果数
        severity_counts = {}
        for result in report.results:
            severity = result.severity.value
            if severity not in severity_counts:
                severity_counts[severity] = 0
            severity_counts[severity] += 1
        
        details["severity_distribution"] = severity_counts
        
        # 問題のあるテーブル一覧
        problematic_tables = set()
        for result in report.results:
            if result.severity in [CheckSeverity.ERROR, CheckSeverity.WARNING] and result.table_name:
                problematic_tables.add(result.table_name)
        
        details["problematic_tables"] = sorted(list(problematic_tables))
        details["problematic_table_count"] = len(problematic_tables)
        
        # 成功したテーブル一覧
        successful_tables = set()
        for result in report.results:
            if result.severity == CheckSeverity.SUCCESS and result.table_name:
                successful_tables.add(result.table_name)
        
        # 問題のあるテーブルを除外
        successful_tables = successful_tables - problematic_tables
        
        details["successful_tables"] = sorted(list(successful_tables))
        details["successful_table_count"] = len(successful_tables)
        
        # チェック実行時間（将来的に追加予定）
        details["execution_info"] = {
            "start_time": None,
            "end_time": None,
            "duration_seconds": None
        }
        
        return details
    
    def generate_compact_report(self, report: ConsistencyReport) -> str:
        """
        コンパクトなJSON形式のレポートを生成
        
        Args:
            report: 整合性チェックレポート
            
        Returns:
            コンパクトなJSONレポート文字列
        """
        compact_dict = {
            "check_date": report.check_date,
            "total_tables": report.total_tables,
            "total_checks": report.total_checks,
            "summary": report.summary,
            "error_count": report.summary.get('error', 0),
            "warning_count": report.summary.get('warning', 0),
            "success_count": report.summary.get('success', 0),
            "has_errors": report.summary.get('error', 0) > 0,
            "has_warnings": report.summary.get('warning', 0) > 0,
            "fix_suggestion_count": len(report.fix_suggestions)
        }
        
        return json.dumps(compact_dict, ensure_ascii=False, separators=(',', ':'))
    
    def generate_errors_only_report(self, report: ConsistencyReport) -> str:
        """
        エラーのみのJSON形式レポートを生成
        
        Args:
            report: 整合性チェックレポート
            
        Returns:
            エラーのみのJSONレポート文字列
        """
        error_results = [
            self._convert_result_to_dict(result) 
            for result in report.results 
            if result.severity == CheckSeverity.ERROR
        ]
        
        error_fixes = [
            self._convert_fix_suggestion_to_dict(fix)
            for fix in report.fix_suggestions
            if fix.critical
        ]
        
        error_dict = {
            "check_date": report.check_date,
            "error_count": len(error_results),
            "errors": error_results,
            "critical_fixes": error_fixes
        }
        
        return json.dumps(error_dict, ensure_ascii=False, indent=self.indent)
    
    def save_report(self, report: ConsistencyReport, file_path: str):
        """
        レポートをファイルに保存
        
        Args:
            report: 整合性チェックレポート
            file_path: 保存先ファイルパス
        """
        report_json = self.generate_report(report)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(report_json)
    
    def load_report(self, file_path: str) -> Dict[str, Any]:
        """
        JSONレポートファイルを読み込み
        
        Args:
            file_path: レポートファイルパス
            
        Returns:
            レポート辞書
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
