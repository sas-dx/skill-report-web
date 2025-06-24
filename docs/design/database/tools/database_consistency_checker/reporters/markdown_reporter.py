"""
データベース整合性チェックツール - Markdownレポーター
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
from database_consistency_checker.core.models import ConsistencyReport, CheckResult, CheckSeverity
from database_consistency_checker.core.check_definitions import get_japanese_check_name, get_all_check_definitions


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
        
        # チェック内容の解説
        lines.extend(self._generate_check_explanation_section())
        
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
    
    def _generate_check_explanation_section(self) -> List[str]:
        """チェック内容の解説セクションを生成"""
        lines = []
        
        lines.append("## 🔍 チェック内容について")
        lines.append("")
        lines.append("このレポートでは、データベース設計の整合性を以下の4つの観点からチェックしています。")
        lines.append("")
        
        # 各チェックの詳細説明
        check_definitions = get_all_check_definitions()
        
        for i, (check_key, definition) in enumerate(check_definitions.items(), 1):
            lines.append(f"### {i}. {definition.get('japanese_name', check_key)}")
            lines.append("")
            lines.append(f"**目的:** {definition.get('purpose', '詳細は実装を参照')}")
            lines.append("")
            lines.append(f"**チェック内容:** {definition.get('check_content', '詳細は実装を参照')}")
            lines.append("")
            lines.append(f"**検出する問題:** {definition.get('detected_issues', '詳細は実装を参照')}")
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
            
            # チェック名を日本語化
            japanese_name = get_japanese_check_name(check_name)
            lines.append(f"| {japanese_name} | {success} | {warning} | {error} | {info} | {total} |")
        
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
        
        # チェック種別ごとにグループ化
        results_by_check = {}
        for result in report.results:
            check_name = result.check_name
            if check_name not in results_by_check:
                results_by_check[check_name] = []
            results_by_check[check_name].append(result)
        
        # チェック種別順に出力（yaml_formatを追加）
        check_order = ['table_existence', 'yaml_format', 'column_consistency', 'foreign_key_consistency', 'data_type_consistency', 'naming_convention']
        
        for check_name in check_order:
            results = results_by_check.get(check_name, [])
            japanese_name = get_japanese_check_name(check_name)
            
            lines.append(f"### 🔍 {japanese_name} ({len(results)}件)")
            lines.append("")
            
            # YAMLフォーマットチェックの特別処理
            if check_name == 'yaml_format':
                if not results:
                    # YAMLファイルが存在しない場合の詳細説明
                    lines.extend(self._generate_yaml_format_no_files_section(report))
                else:
                    lines.extend(self._generate_yaml_format_details(results))
            else:
                if not results:
                    lines.append("該当する結果がありません。")
                    lines.append("")
                else:
                    # 重要度別にソート
                    severity_order = {
                        CheckSeverity.ERROR: 0,
                        CheckSeverity.WARNING: 1,
                        CheckSeverity.INFO: 2,
                        CheckSeverity.SUCCESS: 3
                    }
                    
                    sorted_results = sorted(results, key=lambda r: (severity_order.get(r.severity, 4), r.table_name or ""))
                    
                    for i, result in enumerate(sorted_results, 1):
                        icon = self.icons.get(result.severity, '')
                        
                        lines.append(f"#### {i}. {icon} {result.message}")
                        lines.append("")
                        
                        # テーブル名
                        if result.table_name:
                            lines.append(f"**テーブル:** {result.table_name}")
                            lines.append("")
                        
                        # ファイル情報
                        if result.file_path:
                            file_info = f"**ファイル:** `{result.file_path}`"
                            if result.line_number:
                                file_info += f" (行 {result.line_number})"
                            lines.append(file_info)
                            lines.append("")
                        
                        # 詳細情報
                        if result.details:
                            lines.append("**詳細情報:**")
                            lines.extend(self._format_detailed_info(result.details))
                            lines.append("")
                        
                        # 区切り線（最後の項目以外）
                        if i < len(sorted_results):
                            lines.append("---")
                            lines.append("")
            
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
        
        # 重要度別にグループ化
        suggestions_by_severity = {}
        for suggestion in report.fix_suggestions:
            # 辞書形式の場合の処理
            if isinstance(suggestion, dict):
                severity = suggestion.get('severity', 'info')
                if severity not in suggestions_by_severity:
                    suggestions_by_severity[severity] = []
                suggestions_by_severity[severity].append(suggestion)
            else:
                # FixSuggestionオブジェクトの場合
                fix_type = suggestion.fix_type.value
                if fix_type not in suggestions_by_severity:
                    suggestions_by_severity[fix_type] = []
                suggestions_by_severity[fix_type].append(suggestion)
        
        # 重要度順に出力
        severity_order = ['error', 'warning', 'info']
        
        for severity in severity_order:
            if severity not in suggestions_by_severity:
                continue
                
            suggestions = suggestions_by_severity[severity]
            severity_icon = '❌' if severity == 'error' else '⚠️' if severity == 'warning' else 'ℹ️'
            lines.append(f"### {severity_icon} {severity.upper()} ({len(suggestions)}件)")
            lines.append("")
            
            for i, suggestion in enumerate(suggestions, 1):
                if isinstance(suggestion, dict):
                    # 辞書形式の場合
                    table = suggestion.get('table', 'N/A')
                    issue = suggestion.get('issue', '')
                    fix_suggestion = suggestion.get('suggestion', '')
                    
                    lines.append(f"#### {i}. {table}")
                    lines.append("")
                    lines.append(f"**問題:** {issue}")
                    lines.append("")
                    lines.append(f"**修正方法:**")
                    lines.append("```bash")
                    lines.append(fix_suggestion)
                    lines.append("```")
                    lines.append("")
                else:
                    # FixSuggestionオブジェクトの場合
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
        
        # テーブル存在チェックの詳細情報を特別処理
        if 'existence_pattern' in details:
            return self._format_existence_details(details)
        
        # その他の詳細情報
        formatted_items = []
        for key, value in details.items():
            if isinstance(value, list):
                if value:  # リストが空でない場合
                    formatted_items.append(f"{key}: {', '.join(map(str, value))}")
                else:
                    formatted_items.append(f"{key}: なし")
            elif isinstance(value, dict):
                formatted_items.append(f"{key}: {len(value)}項目")
            else:
                formatted_items.append(f"{key}: {value}")
        
        result = " | ".join(formatted_items)
        return self._escape_markdown(result)
    
    def _format_existence_details(self, details: Dict) -> str:
        """テーブル存在チェックの詳細情報をフォーマット"""
        existence_pattern = details.get('existence_pattern', {})
        expected_files = details.get('expected_files', {})
        fix_suggestions = details.get('fix_suggestions', [])
        
        parts = []
        
        # 存在パターン
        pattern_parts = []
        source_names = {
            'table_list': 'テーブル一覧',
            'entity': 'エンティティ',
            'ddl': 'DDL',
            'details': '詳細YAML'
        }
        
        for source, exists in existence_pattern.items():
            status = "○" if exists else "×"
            name = source_names.get(source, source)
            pattern_parts.append(f"{name}:{status}")
        
        if pattern_parts:
            parts.append(" ".join(pattern_parts))
        
        # 期待ファイル
        if expected_files:
            file_list = [f"{key}:{filename}" for key, filename in expected_files.items()]
            parts.append(f"期待ファイル: {', '.join(file_list)}")
        
        result = " | ".join(parts)
        return self._escape_markdown(result)
    
    def _generate_yaml_format_details(self, results: List[CheckResult]) -> List[str]:
        """YAMLフォーマットチェックの詳細結果を生成"""
        lines = []
        
        # 成功・失敗でグループ化
        success_results = [r for r in results if r.severity == CheckSeverity.SUCCESS]
        error_results = [r for r in results if r.severity in [CheckSeverity.ERROR, CheckSeverity.WARNING]]
        
        # 成功したテーブル
        if success_results:
            lines.append("#### ✅ YAML形式検証成功")
            lines.append("")
            lines.append("以下のテーブルはYAML形式・必須セクション検証に合格しました：")
            lines.append("")
            
            for result in sorted(success_results, key=lambda r: r.table_name or ""):
                lines.append(f"- **{result.table_name}**: {result.message}")
            
            lines.append("")
            lines.append("---")
            lines.append("")
        
        # エラー・警告があるテーブル
        if error_results:
            lines.append("#### ❌ YAML形式検証エラー・警告")
            lines.append("")
            
            for i, result in enumerate(sorted(error_results, key=lambda r: r.table_name or ""), 1):
                icon = self.icons.get(result.severity, '')
                lines.append(f"##### {i}. {icon} {result.table_name}")
                lines.append("")
                lines.append(f"**メッセージ:** {result.message}")
                lines.append("")
                
                # YAMLチェック固有の詳細情報
                if result.metadata:
                    metadata = result.metadata
                    
                    # エラー詳細
                    if 'errors' in metadata and metadata['errors']:
                        lines.append("**🔴 検出されたエラー:**")
                        lines.append("")
                        for error in metadata['errors']:
                            lines.append(f"- {error}")
                        lines.append("")
                    
                    # 警告詳細
                    if 'warnings' in metadata and metadata['warnings']:
                        lines.append("**⚠️ 検出された警告:**")
                        lines.append("")
                        for warning in metadata['warnings']:
                            lines.append(f"- {warning}")
                        lines.append("")
                    
                    # テーブル情報
                    if 'table' in metadata:
                        lines.append(f"**対象テーブル:** {metadata['table']}")
                        lines.append("")
                
                # 区切り線（最後の項目以外）
                if i < len(error_results):
                    lines.append("---")
                    lines.append("")
        
        return lines
    
    def _generate_yaml_format_no_files_section(self, report: ConsistencyReport) -> List[str]:
        """YAMLファイルが存在しない場合の詳細セクションを生成"""
        lines = []
        
        lines.append("#### ⚠️ YAMLファイルが存在しません")
        lines.append("")
        lines.append("**検証対象ファイル**")
        lines.append("- **対象ディレクトリ**: `table-details/`")
        lines.append("- **検索パターン**: `*_details.yaml`")
        lines.append("- **発見ファイル数**: 0件")
        lines.append("")
        
        lines.append("#### 🔴 重要な問題")
        lines.append("**YAMLファイルが存在しません**")
        lines.append("")
        lines.append(f"- 全{report.total_tables}テーブルのYAML詳細定義ファイルが不足")
        lines.append("- 必須セクション検証が実行できない状態")
        lines.append("- データベース設計の品質保証に重大な影響")
        lines.append("")
        
        lines.append("#### 🔍 必須セクション検証（実行不可）")
        lines.append("")
        lines.append("以下の必須セクションの検証ができませんでした：")
        lines.append("")
        lines.append("- 🔴 **revision_history**: 改版履歴（検証対象なし）")
        lines.append("- 🔴 **overview**: テーブル概要・目的（検証対象なし）")
        lines.append("- 🔴 **notes**: 特記事項・考慮点（検証対象なし）")
        lines.append("- 🔴 **rules**: 業務ルール・制約（検証対象なし）")
        lines.append("")
        
        lines.append("#### 💡 対応方法")
        lines.append("")
        lines.append("以下のコマンドでYAML詳細定義ファイルを生成してください：")
        lines.append("")
        lines.append("```bash")
        lines.append("# 重要なテーブルから順次生成")
        lines.append("python3 -m table_generator --table MST_Employee --generate definition")
        lines.append("python3 -m table_generator --table MST_Department --generate definition")
        lines.append("python3 -m table_generator --table MST_SkillCategory --generate definition")
        lines.append("")
        lines.append("# 全テーブル一括生成（時間がかかる場合があります）")
        lines.append("python3 -m table_generator --all --generate definition")
        lines.append("```")
        lines.append("")
        
        lines.append("#### 📊 影響範囲")
        lines.append("")
        lines.append("YAMLファイル不足により以下の品質チェックが実行できません：")
        lines.append("")
        lines.append("- **必須セクション検証**: 設計書の品質基準チェック")
        lines.append("- **カラム定義整合性**: YAML ↔ DDL間の整合性確認")
        lines.append("- **業務ルール検証**: ビジネスロジックの妥当性チェック")
        lines.append("- **運用・保守情報**: 特記事項・注意点の確認")
        lines.append("")
        
        return lines
    
    def _format_detailed_info(self, details: Dict) -> List[str]:
        """詳細情報を複数行でフォーマット"""
        lines = []
        
        if not details:
            lines.append("詳細情報はありません。")
            return lines
        
        # テーブル存在チェックの詳細情報
        if 'existence_pattern' in details:
            lines.extend(self._format_existence_detailed_info(details))
        # YAMLフォーマットチェックの詳細情報
        elif 'errors' in details or 'warnings' in details:
            lines.extend(self._format_yaml_detailed_info(details))
        else:
            # その他の詳細情報
            for key, value in details.items():
                if isinstance(value, list):
                    if value:
                        lines.append(f"- **{key}:**")
                        for item in value:
                            lines.append(f"  - {item}")
                    else:
                        lines.append(f"- **{key}:** なし")
                elif isinstance(value, dict):
                    if value:
                        lines.append(f"- **{key}:**")
                        for sub_key, sub_value in value.items():
                            lines.append(f"  - {sub_key}: {sub_value}")
                    else:
                        lines.append(f"- **{key}:** なし")
                else:
                    lines.append(f"- **{key}:** {value}")
        
        return lines
    
    def _format_yaml_detailed_info(self, details: Dict) -> List[str]:
        """YAMLフォーマットチェックの詳細情報を複数行でフォーマット"""
        lines = []
        
        # エラー詳細
        if 'errors' in details and details['errors']:
            lines.append("- **🔴 エラー詳細:**")
            for error in details['errors']:
                lines.append(f"  - {error}")
            lines.append("")
        
        # 警告詳細
        if 'warnings' in details and details['warnings']:
            lines.append("- **⚠️ 警告詳細:**")
            for warning in details['warnings']:
                lines.append(f"  - {warning}")
            lines.append("")
        
        # テーブル情報
        if 'table' in details:
            lines.append(f"- **対象テーブル:** {details['table']}")
            lines.append("")
        
        return lines
    
    def _format_existence_detailed_info(self, details: Dict) -> List[str]:
        """テーブル存在チェックの詳細情報を複数行でフォーマット"""
        lines = []
        
        existence_pattern = details.get('existence_pattern', {})
        missing_sources = details.get('missing_sources', [])
        present_sources = details.get('present_sources', [])
        expected_files = details.get('expected_files', {})
        fix_suggestions = details.get('fix_suggestions', [])
        
        source_names = {
            'table_list': 'テーブル一覧.md',
            'entity': 'entity_relationships.yaml',
            'ddl': 'DDLファイル',
            'details': 'テーブル詳細YAML'
        }
        
        # 存在状況
        lines.append("- **存在状況:**")
        for source, exists in existence_pattern.items():
            status = "✅ 存在" if exists else "❌ 不足"
            name = source_names.get(source, source)
            lines.append(f"  - {name}: {status}")
        
        # 期待ファイル
        if expected_files:
            lines.append("- **期待されるファイル:**")
            for file_type, filename in expected_files.items():
                lines.append(f"  - {filename}")
        
        # 修正提案
        if fix_suggestions:
            lines.append("- **修正提案:**")
            for suggestion in fix_suggestions:
                lines.append(f"  - {suggestion}")
        
        return lines
    
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
