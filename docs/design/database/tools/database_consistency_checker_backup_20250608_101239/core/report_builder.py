from datetime import datetime
from typing import List, Dict
from core.models import CheckResult, ConsistencyReport, CheckSeverity
from fixers.fix_suggestion_generator import FixSuggestionGenerator, FixContext

class ReportBuilder:
    """
    整合性チェックレポートを構築するクラス
    """

    def __init__(self, config):
        self.config = config
        self.fix_generator = FixSuggestionGenerator(None) # Loggerは後で渡すか、FixSuggestionGeneratorを修正

    def _generate_fix_suggestions(self, results: List[CheckResult]) -> List:
        """チェック結果から修正提案を生成"""
        from core.models import FixSuggestion
        from fixers.table_list_fixer import TableListFixer
        from fixers.foreign_key_fixer import ForeignKeyFixer
        
        all_suggestions = []
        
        # 修正提案コンテキストの作成
        context = FixContext(
            base_dir=self.config.base_dir,
            ddl_dir=self.config.ddl_dir,
            yaml_details_dir=self.config.table_details_dir,
            table_list_file=self.config.table_list_file,
            entity_relationships_file=self.config.entity_relationships_file
        )
        
        # エラーと警告のみを対象とする
        error_warning_results = [
            r for r in results 
            if r.severity in [CheckSeverity.ERROR, CheckSeverity.WARNING]
        ]
        
        if not error_warning_results:
            return all_suggestions
        
        # 1. テーブル一覧関連の修正提案
        table_list_fixer = TableListFixer(None) # Loggerは後で渡す
        table_list_suggestions = table_list_fixer.generate_table_list_fixes(
            error_warning_results, 
            self.config.table_list_file,
            self.config.ddl_dir,
            self.config.table_details_dir
        )
        all_suggestions.extend(table_list_suggestions)
        
        # 2. 外部キー関連の修正提案
        foreign_key_fixer = ForeignKeyFixer(None) # Loggerは後で渡す
        fk_suggestions = foreign_key_fixer.generate_foreign_key_fixes(
            error_warning_results,
            self.config.ddl_dir,
            self.config.table_details_dir
        )
        all_suggestions.extend(fk_suggestions)
        
        # 3. 一般的な修正提案
        general_suggestions = self.fix_generator.generate_fix_suggestions(
            error_warning_results, 
            context
        )
        all_suggestions.extend(general_suggestions)
        
        # 修正提案の重複除去と優先度順ソート
        unique_suggestions = self._deduplicate_suggestions(all_suggestions)
        sorted_suggestions = self._sort_suggestions_by_priority(unique_suggestions)
        
        return sorted_suggestions

    def _deduplicate_suggestions(self, suggestions: List) -> List:
        """修正提案の重複を除去"""
        seen = set()
        unique_suggestions = []
        
        for suggestion in suggestions:
            # テーブル名と説明をキーとして重複チェック
            key = (suggestion.table_name, suggestion.description)
            if key not in seen:
                seen.add(key)
                unique_suggestions.append(suggestion)
        
        return unique_suggestions
    
    def _sort_suggestions_by_priority(self, suggestions: List) -> List:
        """修正提案を優先度順にソート"""
        def get_priority(suggestion):
            # クリティカルな修正を最優先
            if suggestion.critical:
                return 0
            # バックアップが必要な修正を次に
            elif suggestion.backup_required:
                return 1
            # その他
            else:
                return 2
        
        return sorted(suggestions, key=get_priority)

    def build_report(self, results: List[CheckResult]) -> ConsistencyReport:
        """
        整合性チェックレポートを作成
        """
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
        
        # 修正提案の生成
        fix_suggestions = self._generate_fix_suggestions(results)
        
        return ConsistencyReport(
            check_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tables=len(unique_tables),
            total_checks=len(results),
            results=results,
            fix_suggestions=fix_suggestions,
            summary=summary
        )

    def build_empty_report(self) -> ConsistencyReport:
        """空のレポートを作成"""
        return ConsistencyReport(
            check_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_tables=0,
            total_checks=0,
            results=[],
            fix_suggestions=[],
            summary={'success': 0, 'warning': 0, 'error': 0, 'info': 0}
        )
