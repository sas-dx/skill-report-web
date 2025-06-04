"""
データベース整合性チェックツール - コンソールレポーター
"""
from typing import Dict, List
from ..core.models import ConsistencyReport, CheckResult, CheckSeverity


class ConsoleReporter:
    """コンソール出力用レポーター"""
    
    def __init__(self):
        """レポーター初期化"""
        # カラーコード
        self.colors = {
            CheckSeverity.SUCCESS: '\033[92m',  # 緑
            CheckSeverity.WARNING: '\033[93m',  # 黄
            CheckSeverity.ERROR: '\033[91m',    # 赤
            CheckSeverity.INFO: '\033[94m',     # 青
            'RESET': '\033[0m',
            'BOLD': '\033[1m',
            'HEADER': '\033[95m'  # マゼンタ
        }
        
        # 絵文字
        self.icons = {
            CheckSeverity.SUCCESS: '✅',
            CheckSeverity.WARNING: '⚠️',
            CheckSeverity.ERROR: '❌',
            CheckSeverity.INFO: 'ℹ️'
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
        
        lines.append(f"\n📅 チェック日時: {report.check_date}")
        lines.append(f"📊 対象テーブル数: {report.total_tables}")
        lines.append(f"🔍 総チェック数: {report.total_checks}")
        
        # 結果サマリー
        lines.append(f"\n📈 結果サマリー:")
        for severity, count in report.summary.items():
            if count > 0:
                icon = self.icons.get(CheckSeverity(severity), '')
                color = self.colors.get(CheckSeverity(severity), '')
                reset = self.colors['RESET']
                lines.append(f"  {color}{icon} {severity.upper()}: {count}件{reset}")
        
        # エラー率の計算
        if report.total_checks > 0:
            error_rate = (report.summary.get('error', 0) / report.total_checks) * 100
            warning_rate = (report.summary.get('warning', 0) / report.total_checks) * 100
            success_rate = (report.summary.get('success', 0) / report.total_checks) * 100
            
            lines.append(f"\n📊 統計:")
            lines.append(f"  成功率: {success_rate:.1f}%")
            lines.append(f"  警告率: {warning_rate:.1f}%")
            lines.append(f"  エラー率: {error_rate:.1f}%")
        
        # チェック別統計
        check_stats = self._get_check_statistics(report.results)
        if check_stats:
            lines.append(f"\n🔍 チェック別統計:")
            for check_name, stats in check_stats.items():
                lines.append(f"  {check_name}:")
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
        if report.fix_suggestions:
            lines.append(f"\n🔧 修正提案: {len(report.fix_suggestions)}件")
            lines.append("  詳細は --suggest-fixes オプションで確認してください")
        
        # 総合判定
        lines.append(f"\n🎯 総合判定:")
        if report.summary.get('error', 0) > 0:
            lines.append(f"  {self.colors[CheckSeverity.ERROR]}❌ 修正が必要な問題があります{self.colors['RESET']}")
        elif report.summary.get('warning', 0) > 0:
            lines.append(f"  {self.colors[CheckSeverity.WARNING]}⚠️ 注意が必要な項目があります{self.colors['RESET']}")
        else:
            lines.append(f"  {self.colors[CheckSeverity.SUCCESS]}✅ 整合性に問題はありません{self.colors['RESET']}")
        
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
            CheckSeverity.WARNING: 1,
            CheckSeverity.INFO: 2,
            CheckSeverity.SUCCESS: 3
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
