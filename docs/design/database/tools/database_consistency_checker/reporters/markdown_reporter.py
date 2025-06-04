"""
データベース整合性チェックツール - Markdownレポーター
"""
from typing import Dict, List
from ..core.models import ConsistencyReport, CheckResult, CheckSeverity


class MarkdownReporter:
    """Markdown出力用レポーター"""
    
    def __init__(self):
        """レポーター初期化"""
        # 絵文字マッピング
        self.icons = {
            CheckSeverity.SUCCESS: '✅',
            CheckSeverity.WARNING: '⚠️',
            CheckSeverity.ERROR: '❌',
            CheckSeverity.INFO: 'ℹ️'
        }
    
    def generate_report(self, report: ConsistencyReport) -> str:
        """
        Markdown形式のレポートを生成
        
        Args:
            report: 整合性チェックレポート
            
        Returns:
            Markdownレポート文字列
        """
        lines = []
        
        # ヘッダー
        lines.append("# データベース整合性チェックレポート")
        lines.append("")
        lines.append(f"**チェック日時:** {report.check_date}")
        lines.append(f"**対象テーブル数:** {report.total_tables}")
        lines.append(f"**総チェック数:** {report.total_checks}")
        lines.append("")
        
        # サマリー
        lines.extend(self._generate_summary_section(report))
        
        # チェック別統計
        lines.extend(self._generate_check_statistics_section(report))
        
        # 詳細結果
        lines.extend(self._generate_detailed_results_section(report))
        
        # 修正提案
        if report.fix_suggestions:
            lines.extend(self._generate_fix_suggestions_section(report))
        
        return '\n'.join(lines)
    
    def _generate_summary_section(self, report: ConsistencyReport) -> List[str]:
        """サマリーセクションを生成"""
        lines = []
        
        lines.append("## 📊 結果サマリー")
        lines.append("")
        
        # 結果テーブル
        lines.append("| 重要度 | 件数 | 割合 |")
        lines.append("|--------|------|------|")
        
        total = report.total_checks
        for severity_name, count in report.summary.items():
            if count > 0:
                severity = CheckSeverity(severity_name)
                icon = self.icons.get(severity, '')
                percentage = (count / total * 100) if total > 0 else 0
                lines.append(f"| {icon} {severity_name.upper()} | {count} | {percentage:.1f}% |")
        
        lines.append("")
        
        # 総合判定
        lines.append("### 🎯 総合判定")
        lines.append("")
        if report.summary.get('error', 0) > 0:
            lines.append("❌ **修正が必要な問題があります**")
            lines.append("")
            lines.append("重要な問題が検出されました。以下の詳細結果を確認して修正してください。")
        elif report.summary.get('warning', 0) > 0:
            lines.append("⚠️ **注意が必要な項目があります**")
            lines.append("")
            lines.append("警告項目が検出されました。必要に応じて対応を検討してください。")
        else:
            lines.append("✅ **整合性に問題はありません**")
            lines.append("")
            lines.append("すべてのチェックが正常に完了しました。")
        
        lines.append("")
        
        return lines
    
    def _generate_check_statistics_section(self, report: ConsistencyReport) -> List[str]:
        """チェック別統計セクションを生成"""
        lines = []
        
        lines.append("## 🔍 チェック別統計")
        lines.append("")
        
        check_stats = self._get_check_statistics(report.results)
        
        if not check_stats:
            lines.append("統計情報がありません。")
            lines.append("")
            return lines
        
        lines.append("| チェック名 | 成功 | 警告 | エラー | 情報 | 合計 |")
        lines.append("|------------|------|------|--------|------|------|")
        
        for check_name, stats in check_stats.items():
            success = stats.get('success', 0)
            warning = stats.get('warning', 0)
            error = stats.get('error', 0)
            info = stats.get('info', 0)
            total = stats.get('total', 0)
            
            lines.append(f"| {check_name} | {success} | {warning} | {error} | {info} | {total} |")
        
        lines.append("")
        
        return lines
    
    def _generate_detailed_results_section(self, report: ConsistencyReport) -> List[str]:
        """詳細結果セクションを生成"""
        lines = []
        
        lines.append("## 📋 詳細結果")
        lines.append("")
        
        if not report.results:
            lines.append("チェック結果がありません。")
            lines.append("")
            return lines
        
        # 重要度別にグループ化
        results_by_severity = {}
        for result in report.results:
            severity = result.severity
            if severity not in results_by_severity:
                results_by_severity[severity] = []
            results_by_severity[severity].append(result)
        
        # 重要度順に出力
        severity_order = [CheckSeverity.ERROR, CheckSeverity.WARNING, CheckSeverity.INFO, CheckSeverity.SUCCESS]
        
        for severity in severity_order:
            if severity not in results_by_severity:
                continue
            
            results = results_by_severity[severity]
            icon = self.icons.get(severity, '')
            
            lines.append(f"### {icon} {severity.value.upper()} ({len(results)}件)")
            lines.append("")
            
            # テーブル形式で出力
            lines.append("| テーブル名 | チェック | メッセージ | 詳細 |")
            lines.append("|------------|----------|------------|------|")
            
            for result in results:
                table_name = result.table_name or "-"
                check_name = result.check_name
                message = self._escape_markdown(result.message)
                details = self._format_details(result.details)
                
                lines.append(f"| {table_name} | {check_name} | {message} | {details} |")
            
            lines.append("")
        
        return lines
    
    def _generate_fix_suggestions_section(self, report: ConsistencyReport) -> List[str]:
        """修正提案セクションを生成"""
        lines = []
        
        lines.append("## 🔧 修正提案")
        lines.append("")
        
        if not report.fix_suggestions:
            lines.append("修正提案はありません。")
            lines.append("")
            return lines
        
        # 修正タイプ別にグループ化
        suggestions_by_type = {}
        for suggestion in report.fix_suggestions:
            fix_type = suggestion.fix_type.value
            if fix_type not in suggestions_by_type:
                suggestions_by_type[fix_type] = []
            suggestions_by_type[fix_type].append(suggestion)
        
        for fix_type, suggestions in suggestions_by_type.items():
            lines.append(f"### {fix_type.upper()} 修正 ({len(suggestions)}件)")
            lines.append("")
            
            for i, suggestion in enumerate(suggestions, 1):
                lines.append(f"#### {i}. {suggestion.table_name}")
                lines.append("")
                lines.append(f"**説明:** {suggestion.description}")
                lines.append("")
                
                if suggestion.critical:
                    lines.append("⚠️ **重要:** この修正は重要です。")
                    lines.append("")
                
                if suggestion.backup_required:
                    lines.append("💾 **注意:** 修正前にバックアップを取得してください。")
                    lines.append("")
                
                lines.append("**修正内容:**")
                lines.append("```sql")
                lines.append(suggestion.fix_content)
                lines.append("```")
                lines.append("")
        
        return lines
    
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
    
    def _escape_markdown(self, text: str) -> str:
        """Markdownエスケープ処理"""
        # 基本的なMarkdown文字をエスケープ
        escape_chars = ['|', '*', '_', '`', '[', ']', '(', ')', '#', '+', '-', '.', '!']
        for char in escape_chars:
            text = text.replace(char, f'\\{char}')
        return text
    
    def _format_details(self, details: Dict) -> str:
        """詳細情報をフォーマット"""
        if not details:
            return "-"
        
        # 簡潔な形式で詳細情報を表示
        formatted_items = []
        for key, value in details.items():
            if isinstance(value, (list, dict)):
                formatted_items.append(f"{key}: {len(value) if isinstance(value, list) else 'object'}")
            else:
                formatted_items.append(f"{key}: {value}")
        
        result = ", ".join(formatted_items)
        return self._escape_markdown(result)
    
    def generate_toc(self, report: ConsistencyReport) -> str:
        """目次を生成"""
        lines = []
        
        lines.append("## 目次")
        lines.append("")
        lines.append("- [結果サマリー](#-結果サマリー)")
        lines.append("- [チェック別統計](#-チェック別統計)")
        lines.append("- [詳細結果](#-詳細結果)")
        
        # 重要度別の目次
        results_by_severity = {}
        for result in report.results:
            severity = result.severity
            if severity not in results_by_severity:
                results_by_severity[severity] = []
            results_by_severity[severity].append(result)
        
        severity_order = [CheckSeverity.ERROR, CheckSeverity.WARNING, CheckSeverity.INFO, CheckSeverity.SUCCESS]
        
        for severity in severity_order:
            if severity in results_by_severity:
                icon = self.icons.get(severity, '')
                lines.append(f"  - [{icon} {severity.value.upper()}](#{icon}-{severity.value})")
        
        if report.fix_suggestions:
            lines.append("- [修正提案](#-修正提案)")
        
        lines.append("")
        
        return '\n'.join(lines)
