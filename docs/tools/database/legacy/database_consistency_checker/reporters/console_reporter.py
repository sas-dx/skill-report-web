"""
データベース整合性チェックツール - コンソールレポーター
"""
import sys
from pathlib import Path
from typing import Dict, List

# パス解決のセットアップ
_current_dir = Path(__file__).parent
_tools_dir = _current_dir.parent.parent
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

# 絶対インポートを使用
from shared.core.models import ConsistencyReport, CheckResult, CheckSeverity
from database_consistency_checker.core.check_definitions import get_japanese_check_name


class ConsoleReporter:
    """コンソール出力用レポーター"""
    
    def __init__(self):
        """レポーター初期化"""
        # カラーコード
        self.colors = {
            CheckSeverity.INFO: '\033[92m',     # 緑（成功の代わり）
            CheckSeverity.WARNING: '\033[93m',  # 黄
            CheckSeverity.ERROR: '\033[91m',    # 赤
            CheckSeverity.CRITICAL: '\033[95m', # マゼンタ
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'HEADER': '\033[95m'  # マゼンタ
        }
        
        # 絵文字
        self.icons = {
            CheckSeverity.INFO: '✅',
            CheckSeverity.WARNING: '⚠️',
            CheckSeverity.ERROR: '❌',
            CheckSeverity.CRITICAL: '🚨'
        }
    
    def generate_report(self, report: ConsistencyReport) -> str:
        """
        コンソール用レポートを生成
        
        Args:
            report: 整合性チェックレポート
            
        Returns:
            レポート文字列
        """
        # コンソール出力は既にloggerで行われているため、
        # ここでは簡潔なサマリーのみを返す
        return self._generate_summary(report)
    
    def _generate_summary(self, report: ConsistencyReport) -> str:
        """サマリー情報を生成"""
        lines = []
        
        lines.append(f"\n{self.colors['HEADER']}{self.colors['BOLD']}{'='*60}")
        lines.append("データベース整合性チェック結果サマリー")
        lines.append(f"{'='*60}{self.colors['RESET']}")
        
        # generated_atがない場合は現在時刻を使用
        from datetime import datetime
        generated_at = report.metadata.get('generated_at', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        lines.append(f"\n📅 チェック日時: {generated_at}")
        
        # report.tablesが存在するかチェック
        if hasattr(report, 'tables'):
            lines.append(f"📊 対象テーブル数: {len(report.tables)}")
        
        # report.summaryの型をチェック
        if hasattr(report, 'summary'):
            if hasattr(report.summary, 'total_checks'):
                lines.append(f"🔍 総チェック数: {report.summary.total_checks}")
            elif isinstance(report.summary, dict):
                total_checks = report.summary.get('total_checks', 0)
                lines.append(f"🔍 総チェック数: {total_checks}")
        
        # 結果サマリー
        lines.append(f"\n📈 結果サマリー:")
        
        # summaryの型に応じて処理を分岐
        if hasattr(report.summary, 'info_count'):
            # CheckSummaryオブジェクトの場合
            summary_items = [
                ('INFO', report.summary.info_count),
                ('WARNING', report.summary.warning_count),
                ('ERROR', report.summary.error_count),
                ('CRITICAL', report.summary.critical_count)
            ]
        elif isinstance(report.summary, dict):
            # dictの場合
            summary_items = [
                ('INFO', report.summary.get('info', 0)),
                ('WARNING', report.summary.get('warning', 0)),
                ('ERROR', report.summary.get('error', 0)),
                ('CRITICAL', report.summary.get('critical', 0))
            ]
        else:
            summary_items = []
        
        for severity_name, count in summary_items:
            if count > 0:
                try:
                    severity = CheckSeverity(severity_name.lower())
                    icon = self.icons.get(severity, '')
                    color = self.colors.get(severity, '')
                    reset = self.colors['RESET']
                    lines.append(f"  {color}{icon} {severity_name}: {count}件{reset}")
                except ValueError:
                    lines.append(f"  {severity_name}: {count}件")
        
        # エラー率の計算
        total_checks = 0
        error_count = 0
        warning_count = 0
        passed_checks = 0
        
        if hasattr(report.summary, 'total_checks'):
            total_checks = report.summary.total_checks
            error_count = report.summary.error_count
            warning_count = report.summary.warning_count
            passed_checks = report.summary.passed_checks
        elif isinstance(report.summary, dict):
            total_checks = report.summary.get('total_checks', 0)
            error_count = report.summary.get('error', 0)
            warning_count = report.summary.get('warning', 0)
            passed_checks = report.summary.get('passed_checks', 0)
        
        if total_checks > 0:
            error_rate = (error_count / total_checks) * 100
            warning_rate = (warning_count / total_checks) * 100
            success_rate = (passed_checks / total_checks) * 100
            
            lines.append(f"\n📊 統計:")
            lines.append(f"  成功率: {success_rate:.1f}%")
            lines.append(f"  警告率: {warning_rate:.1f}%")
            lines.append(f"  エラー率: {error_rate:.1f}%")
        
        # チェック別統計
        check_stats = self._get_check_statistics(report.results)
        if check_stats:
            lines.append(f"\n🔍 チェック別統計:")
            for check_name, stats in check_stats.items():
                # チェック名を日本語化
                japanese_name = get_japanese_check_name(check_name)
                lines.append(f"  {japanese_name}:")
                for severity, count in stats.items():
                    if severity != 'total' and count > 0:
                        icon = self.icons.get(CheckSeverity(severity), '')
                        lines.append(f"    {icon} {severity}: {count}件")
        
        # 重要な問題のハイライト
        critical_issues = [r for r in report.results if r.severity == CheckSeverity.ERROR]
        if critical_issues:
            lines.append(f"\n🚨 重要な問題 ({len(critical_issues)}件):")
            for issue in critical_issues[:5]:  # 最初の5件のみ表示
                table_info = f"[{issue.table_name}] " if issue.table_name else ""
                lines.append(f"  ❌ {table_info}{issue.message}")
            
            if len(critical_issues) > 5:
                lines.append(f"  ... 他 {len(critical_issues) - 5}件")
        
        # 修正提案がある場合
        if report.suggestions:
            lines.append(f"\n🔧 修正提案: {len(report.suggestions)}件")
            lines.append("  詳細は --suggest-fixes オプションで確認してください")
        
        # 総合判定
        lines.append(f"\n🎯 総合判定:")
        
        # error_countとcritical_countを取得
        if hasattr(report.summary, 'error_count'):
            error_count = report.summary.error_count
            critical_count = report.summary.critical_count
            warning_count = report.summary.warning_count
        elif isinstance(report.summary, dict):
            error_count = report.summary.get('error', 0)
            critical_count = report.summary.get('critical', 0)
            warning_count = report.summary.get('warning', 0)
        else:
            error_count = 0
            critical_count = 0
            warning_count = 0
        
        if error_count > 0 or critical_count > 0:
            lines.append(f"  {self.colors[CheckSeverity.ERROR]}❌ 修正が必要な問題があります{self.colors['RESET']}")
        elif warning_count > 0:
            lines.append(f"  {self.colors[CheckSeverity.WARNING]}⚠️ 注意が必要な項目があります{self.colors['RESET']}")
        else:
            lines.append(f"  {self.colors[CheckSeverity.INFO]}✅ 整合性に問題はありません{self.colors['RESET']}")
        
        lines.append("")
        
        return '\n'.join(lines)
    
    def _get_check_statistics(self, results: List[CheckResult]) -> Dict[str, Dict[str, int]]:
        """チェック別統計を取得"""
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
    
    def print_detailed_results(self, report: ConsistencyReport, max_results: int = 50):
        """
        詳細結果を出力
        
        Args:
            report: 整合性チェックレポート
            max_results: 最大表示件数
        """
        print(f"\n{self.colors['HEADER']}{self.colors['BOLD']}詳細結果{self.colors['RESET']}")
        print("-" * 60)
        
        # 重要度順にソート
        severity_order = {
            CheckSeverity.ERROR: 0,
            CheckSeverity.CRITICAL: 1,
            CheckSeverity.WARNING: 2,
            CheckSeverity.INFO: 3
        }
        
        sorted_results = sorted(
            report.results,
            key=lambda r: (severity_order.get(r.severity, 4), r.check_name, r.table_name)
        )
        
        displayed_count = 0
        for result in sorted_results:
            if displayed_count >= max_results:
                remaining = len(sorted_results) - displayed_count
                print(f"\n... 他 {remaining}件の結果があります")
                break
            
            self._print_single_result(result)
            displayed_count += 1
    
    def _print_single_result(self, result: CheckResult):
        """単一結果を出力"""
        icon = self.icons.get(result.severity, '')
        color = self.colors.get(result.severity, '')
        reset = self.colors['RESET']
        
        # ヘッダー
        table_info = f"[{result.table_name}] " if result.table_name else ""
        print(f"{color}{icon} {table_info}{result.message}{reset}")
        
        # 詳細情報
        if result.details:
            for key, value in result.details.items():
                if isinstance(value, (list, dict)):
                    print(f"  {key}: {value}")
                else:
                    print(f"  {key}: {value}")
        
        print()  # 空行
