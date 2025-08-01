from typing import List
from core.models import CheckResult, CheckConfig, ConsistencyReport, CheckSeverity
from core.logger import ConsistencyLogger
from core.config import Config
from checkers.check_executor import CheckExecutor
from core.report_builder import ReportBuilder

class CheckOrchestrator:
    """
    整合性チェックの実行順序を管理し、各チェックを実行するオーケストレーター
    """

    def __init__(self, config: Config, check_config: CheckConfig):
        self.config = config
        self.check_config = check_config
        self.logger = ConsistencyLogger(verbose=check_config.verbose)
        self.executor = CheckExecutor(self.logger, config, check_config)
        self.report_builder = ReportBuilder(config)

    def run_all_checks(self) -> ConsistencyReport:
        """
        全ての整合性チェックを実行
        """
        self.logger.header("データベース整合性チェック開始")
        
        # 設定の妥当性チェック
        missing_paths = self.config.validate_paths()
        if missing_paths:
            self.logger.error("必要なファイル/ディレクトリが見つかりません:")
            for path in missing_paths:
                self.logger.error(f"  - {path}")
            return self.report_builder.build_empty_report()
        
        # 出力ディレクトリの作成
        self.config.create_output_dirs()
        
        all_results = []

        # 1. テーブル存在確認
        all_results.extend(self.executor.execute_table_existence_check())
        
        # 2. 孤立ファイル検出
        all_results.extend(self.executor.execute_orphaned_files_check())
        
        # 3. YAMLフォーマット整合性
        all_results.extend(self.executor.execute_yaml_format_check())
        
        # 4. カラム定義整合性
        all_results.extend(self.executor.execute_column_consistency_check())
        
        # 5. 外部キー整合性
        all_results.extend(self.executor.execute_foreign_key_check())
        
        # 6. データ型整合性
        all_results.extend(self.executor.execute_data_type_check())
        
        # 7. 制約整合性
        all_results.extend(self.executor.execute_constraint_check())
        
        # 8. 修正提案 (他のチェック結果に依存するため、最後に実行)
        fix_suggestions_results = self._run_fix_suggestions_check(all_results)
        all_results.extend(fix_suggestions_results)
        
        # 9. マルチテナント対応
        all_results.extend(self.executor.execute_multitenant_compliance_check())
        
        # 10. 要求仕様ID追跡
        all_results.extend(self.executor.execute_requirement_traceability_check())
        
        # 11. パフォーマンス影響分析
        all_results.extend(self.executor.execute_performance_impact_check())
        
        # レポート作成
        report = self.report_builder.build_report(all_results)
        
        # サマリー表示
        self.logger.print_summary()
        
        self.logger.header("データベース整合性チェック完了")
        
        return report

    def run_specific_checks(self, check_names: List[str]) -> ConsistencyReport:
        """
        指定されたチェックのみを実行
        """
        self.logger.header(f"指定チェック実行: {', '.join(check_names)}")
        
        all_results = []
        
        # チェックの実行順序は固定し、指定されたチェックのみを実行
        if "table_existence" in check_names:
            all_results.extend(self.executor.execute_table_existence_check())
        
        if "orphaned_files" in check_names:
            all_results.extend(self.executor.execute_orphaned_files_check())
        
        if "yaml_format_consistency" in check_names:
            all_results.extend(self.executor.execute_yaml_format_check())
        
        if "column_consistency" in check_names:
            all_results.extend(self.executor.execute_column_consistency_check())
        
        if "foreign_key_consistency" in check_names:
            all_results.extend(self.executor.execute_foreign_key_check())
        
        if "data_type_consistency" in check_names:
            all_results.extend(self.executor.execute_data_type_check())
        
        if "constraint_consistency" in check_names:
            all_results.extend(self.executor.execute_constraint_check())
        
        if "fix_suggestions" in check_names:
            # 修正提案は他のチェック結果に依存するため、ここで生成
            fix_suggestions_results = self._run_fix_suggestions_check(all_results)
            all_results.extend(fix_suggestions_results)
        
        if "multitenant_compliance" in check_names:
            all_results.extend(self.executor.execute_multitenant_compliance_check())
        
        if "requirement_traceability" in check_names:
            all_results.extend(self.executor.execute_requirement_traceability_check())
        
        if "performance_impact" in check_names:
            all_results.extend(self.executor.execute_performance_impact_check())
        
        return self.report_builder.build_report(all_results)

    def _run_fix_suggestions_check(self, all_results: List[CheckResult]) -> List[CheckResult]:
        """修正提案チェックを実行"""
        results = []
        
        suggestions = self.report_builder._generate_fix_suggestions(all_results) # ReportBuilderから呼び出し
        
        if suggestions:
            for suggestion in suggestions:
                results.append(CheckResult(
                    check_name="fix_suggestions",
                    table_name=suggestion.table_name,
                    severity=CheckSeverity.INFO, # 修正提案は情報として扱う
                    message=f"修正提案: {suggestion.description}",
                    details={
                        "fix_type": suggestion.fix_type.value, # Enumのvalueを使用
                        "fix_content": suggestion.fix_content, # commandをfix_contentに変更
                        "critical": suggestion.critical,
                        "backup_required": suggestion.backup_required,
                        "details": suggestion.details
                    }
                ))
            self.logger.info(f"  修正提案: {len(suggestions)}件の提案が見つかりました")
        else:
            self.logger.success("  修正提案: 見つかりませんでした")
            results.append(CheckResult(
                check_name="fix_suggestions",
                table_name="",
                severity=CheckSeverity.SUCCESS,
                message="修正提案は見つかりませんでした",
                details={}
            ))
        return results

    def get_available_checks(self) -> List[str]:
        """利用可能なチェック名のリストを取得"""
        return [
            "table_existence",
            "orphaned_files",
            "yaml_format_consistency",
            "column_consistency",
            "foreign_key_consistency",
            "data_type_consistency",
            "constraint_consistency",
            "fix_suggestions",
            "multitenant_compliance",
            "requirement_traceability",
            "performance_impact"
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
