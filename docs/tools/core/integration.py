"""
統合設計ツール - メイン統合エンジン

全ての設計ツールを統合し、統一されたインターフェースを提供します。
バリデーション、生成、解析機能を組み合わせた包括的な設計支援を実現します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import os
import sys
import json
import time
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from .config import IntegratedConfig, ToolType, QualityConfig
from .validation import ValidationEngine, ValidationCategory, ValidationReport
from .generation import GenerationEngine, GenerationType, GenerationContext, GenerationResult
from .analysis import AnalysisEngine, AnalysisType, AnalysisContext, AnalysisResult


class OperationType(Enum):
    """操作タイプ"""
    VALIDATE = "validate"
    GENERATE = "generate"
    ANALYZE = "analyze"
    SYNC = "sync"
    REPORT = "report"


class ExecutionMode(Enum):
    """実行モード"""
    SINGLE = "single"
    BATCH = "batch"
    INTERACTIVE = "interactive"
    AUTOMATED = "automated"


@dataclass
class IntegrationContext:
    """統合コンテキスト"""
    operation_type: OperationType
    execution_mode: ExecutionMode
    target_paths: List[str] = field(default_factory=list)
    requirement_ids: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    output_directory: Optional[str] = None
    force_overwrite: bool = False


@dataclass
class IntegrationResult:
    """統合結果"""
    success: bool
    operation_type: OperationType
    execution_time: float
    results: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)


class IntegratedDesignTools:
    """統合設計ツール"""
    
    def __init__(self, config_path: Optional[str] = None):
        """初期化"""
        self.config = self._load_config(config_path)
        self.validation_engine = ValidationEngine(self.config)
        self.generation_engine = GenerationEngine(self.config)
        self.analysis_engine = AnalysisEngine(self.config)
        
        # 実行履歴
        self.execution_history: List[IntegrationResult] = []
    
    def _load_config(self, config_path: Optional[str] = None) -> IntegratedConfig:
        """設定を読み込み"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            return IntegratedConfig.from_dict(config_data)
        else:
            # デフォルト設定
            return IntegratedConfig()
    
    def execute(self, context: IntegrationContext) -> IntegrationResult:
        """統合実行"""
        start_time = time.time()
        
        try:
            if context.operation_type == OperationType.VALIDATE:
                result = self._execute_validation(context)
            elif context.operation_type == OperationType.GENERATE:
                result = self._execute_generation(context)
            elif context.operation_type == OperationType.ANALYZE:
                result = self._execute_analysis(context)
            elif context.operation_type == OperationType.SYNC:
                result = self._execute_sync(context)
            elif context.operation_type == OperationType.REPORT:
                result = self._execute_report(context)
            else:
                raise ValueError(f"サポートされていない操作タイプ: {context.operation_type}")
            
            result.execution_time = time.time() - start_time
            self.execution_history.append(result)
            
            return result
            
        except Exception as e:
            error_result = IntegrationResult(
                success=False,
                operation_type=context.operation_type,
                execution_time=time.time() - start_time,
                errors=[str(e)]
            )
            self.execution_history.append(error_result)
            return error_result
    
    def _execute_validation(self, context: IntegrationContext) -> IntegrationResult:
        """バリデーション実行"""
        results = {}
        all_errors = []
        all_warnings = []
        
        # バリデーションカテゴリを決定
        categories = context.parameters.get('categories')
        if categories:
            categories = [ValidationCategory(cat) for cat in categories]
        
        if context.execution_mode == ExecutionMode.SINGLE:
            # 単一ファイル/ディレクトリのバリデーション
            for target_path in context.target_paths:
                if os.path.isfile(target_path):
                    report = self.validation_engine.validate_file(target_path, categories)
                elif os.path.isdir(target_path):
                    pattern = context.parameters.get('pattern', '*')
                    report = self.validation_engine.validate_directory(target_path, pattern, categories)
                else:
                    continue
                
                results[target_path] = {
                    'report': report,
                    'is_valid': report.is_valid,
                    'error_count': report.error_count,
                    'warning_count': report.warning_count
                }
                
                all_errors.extend([error.message for error in report.errors])
                all_warnings.extend([warning.message for warning in report.warnings])
        
        elif context.execution_mode == ExecutionMode.BATCH:
            # バッチバリデーション
            for target_path in context.target_paths:
                if os.path.isdir(target_path):
                    pattern = context.parameters.get('pattern', '**/*')
                    report = self.validation_engine.validate_directory(target_path, pattern, categories)
                    
                    results[target_path] = {
                        'report': report,
                        'is_valid': report.is_valid,
                        'error_count': report.error_count,
                        'warning_count': report.warning_count
                    }
                    
                    all_errors.extend([error.message for error in report.errors])
                    all_warnings.extend([warning.message for warning in report.warnings])
        
        # サマリーを作成
        total_files = sum(result['report'].total_files for result in results.values())
        total_errors = sum(result['error_count'] for result in results.values())
        total_warnings = sum(result['warning_count'] for result in results.values())
        
        summary = {
            'total_files': total_files,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'overall_valid': total_errors == 0
        }
        
        return IntegrationResult(
            success=total_errors == 0,
            operation_type=OperationType.VALIDATE,
            execution_time=0,  # 後で設定
            results=results,
            errors=all_errors,
            warnings=all_warnings,
            summary=summary
        )
    
    def _execute_generation(self, context: IntegrationContext) -> IntegrationResult:
        """生成実行"""
        results = {}
        all_errors = []
        all_warnings = []
        
        generation_type = GenerationType(context.parameters.get('generation_type', 'code'))
        
        for req_id in context.requirement_ids:
            # 生成コンテキストを作成
            gen_context = GenerationContext(
                requirement_id=req_id,
                design_doc_path=context.parameters.get('design_doc_path'),
                template_name=context.parameters.get('template_name'),
                output_path=context.parameters.get('output_path'),
                variables=context.parameters.get('variables', {}),
                metadata=context.parameters.get('metadata', {})
            )
            
            # 生成実行
            gen_result = self.generation_engine.generate(generation_type, gen_context)
            
            results[req_id] = {
                'result': gen_result,
                'success': gen_result.success,
                'output_path': gen_result.output_path
            }
            
            if not gen_result.success:
                all_errors.append(gen_result.error_message or f"生成失敗: {req_id}")
            
            all_warnings.extend(gen_result.warnings)
        
        # サマリーを作成
        successful_generations = sum(1 for result in results.values() if result['success'])
        total_generations = len(results)
        
        summary = {
            'total_generations': total_generations,
            'successful_generations': successful_generations,
            'failed_generations': total_generations - successful_generations,
            'success_rate': successful_generations / total_generations if total_generations > 0 else 0
        }
        
        return IntegrationResult(
            success=len(all_errors) == 0,
            operation_type=OperationType.GENERATE,
            execution_time=0,  # 後で設定
            results=results,
            errors=all_errors,
            warnings=all_warnings,
            summary=summary
        )
    
    def _execute_analysis(self, context: IntegrationContext) -> IntegrationResult:
        """解析実行"""
        results = {}
        all_errors = []
        all_warnings = []
        
        analysis_type = AnalysisType(context.parameters.get('analysis_type', 'dependency'))
        
        for target_path in context.target_paths:
            # 解析コンテキストを作成
            analysis_context = AnalysisContext(
                target_path=target_path,
                analysis_type=analysis_type,
                parameters=context.parameters.get('analysis_parameters', {}),
                output_format=context.parameters.get('output_format', 'json')
            )
            
            # 解析実行
            analysis_result = self.analysis_engine.analyze(analysis_context)
            
            results[target_path] = {
                'result': analysis_result,
                'success': analysis_result.success,
                'findings_count': len(analysis_result.findings)
            }
            
            if not analysis_result.success:
                all_errors.append(analysis_result.error_message or f"解析失敗: {target_path}")
            
            all_warnings.extend(analysis_result.warnings)
        
        # サマリーを作成
        successful_analyses = sum(1 for result in results.values() if result['success'])
        total_analyses = len(results)
        total_findings = sum(result['findings_count'] for result in results.values())
        
        summary = {
            'total_analyses': total_analyses,
            'successful_analyses': successful_analyses,
            'failed_analyses': total_analyses - successful_analyses,
            'total_findings': total_findings,
            'success_rate': successful_analyses / total_analyses if total_analyses > 0 else 0
        }
        
        return IntegrationResult(
            success=len(all_errors) == 0,
            operation_type=OperationType.ANALYZE,
            execution_time=0,  # 後で設定
            results=results,
            errors=all_errors,
            warnings=all_warnings,
            summary=summary
        )
    
    def _execute_sync(self, context: IntegrationContext) -> IntegrationResult:
        """同期実行"""
        results = {}
        all_errors = []
        all_warnings = []
        
        # 設計書とコードの同期チェック
        for target_path in context.target_paths:
            try:
                # バリデーションで設計書同期をチェック
                report = self.validation_engine.validate_file(
                    target_path, 
                    [ValidationCategory.DESIGN_SYNC, ValidationCategory.REQUIREMENT_ID]
                )
                
                sync_issues = []
                for error in report.errors:
                    if error.category == ValidationCategory.DESIGN_SYNC:
                        sync_issues.append({
                            'type': 'error',
                            'message': error.message,
                            'suggestion': error.suggestion
                        })
                
                for warning in report.warnings:
                    if warning.category == ValidationCategory.DESIGN_SYNC:
                        sync_issues.append({
                            'type': 'warning',
                            'message': warning.message,
                            'suggestion': warning.suggestion
                        })
                
                results[target_path] = {
                    'sync_issues': sync_issues,
                    'is_synced': len([issue for issue in sync_issues if issue['type'] == 'error']) == 0,
                    'issue_count': len(sync_issues)
                }
                
                if sync_issues:
                    for issue in sync_issues:
                        if issue['type'] == 'error':
                            all_errors.append(f"{target_path}: {issue['message']}")
                        else:
                            all_warnings.append(f"{target_path}: {issue['message']}")
                
            except Exception as e:
                all_errors.append(f"同期チェック失敗 {target_path}: {e}")
                results[target_path] = {
                    'sync_issues': [],
                    'is_synced': False,
                    'issue_count': 1,
                    'error': str(e)
                }
        
        # サマリーを作成
        synced_files = sum(1 for result in results.values() if result['is_synced'])
        total_files = len(results)
        total_issues = sum(result['issue_count'] for result in results.values())
        
        summary = {
            'total_files': total_files,
            'synced_files': synced_files,
            'unsynced_files': total_files - synced_files,
            'total_issues': total_issues,
            'sync_rate': synced_files / total_files if total_files > 0 else 0
        }
        
        return IntegrationResult(
            success=len(all_errors) == 0,
            operation_type=OperationType.SYNC,
            execution_time=0,  # 後で設定
            results=results,
            errors=all_errors,
            warnings=all_warnings,
            summary=summary
        )
    
    def _execute_report(self, context: IntegrationContext) -> IntegrationResult:
        """レポート実行"""
        results = {}
        all_errors = []
        all_warnings = []
        
        report_type = context.parameters.get('report_type', 'validation')
        output_format = context.parameters.get('output_format', 'html')
        
        try:
            if report_type == 'validation':
                # バリデーションレポート生成
                validation_results = []
                for target_path in context.target_paths:
                    if os.path.isdir(target_path):
                        report = self.validation_engine.validate_directory(target_path)
                        validation_results.append((target_path, report))
                
                # 統合レポートを生成
                combined_report = self._combine_validation_reports(validation_results)
                report_content = self.validation_engine.generate_report(combined_report, output_format)
                
                # レポートファイルを保存
                if context.output_directory:
                    output_path = os.path.join(
                        context.output_directory, 
                        f"validation_report.{output_format}"
                    )
                    os.makedirs(context.output_directory, exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(report_content)
                    
                    results['validation_report'] = {
                        'output_path': output_path,
                        'format': output_format,
                        'size': len(report_content)
                    }
                else:
                    results['validation_report'] = {
                        'content': report_content,
                        'format': output_format,
                        'size': len(report_content)
                    }
            
            elif report_type == 'summary':
                # サマリーレポート生成
                summary_data = self._generate_summary_report(context.target_paths)
                
                if output_format == 'json':
                    report_content = json.dumps(summary_data, ensure_ascii=False, indent=2)
                else:
                    report_content = self._format_summary_as_text(summary_data)
                
                if context.output_directory:
                    output_path = os.path.join(
                        context.output_directory, 
                        f"summary_report.{output_format}"
                    )
                    os.makedirs(context.output_directory, exist_ok=True)
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(report_content)
                    
                    results['summary_report'] = {
                        'output_path': output_path,
                        'format': output_format,
                        'size': len(report_content)
                    }
                else:
                    results['summary_report'] = {
                        'content': report_content,
                        'format': output_format,
                        'size': len(report_content)
                    }
            
            summary = {
                'report_type': report_type,
                'output_format': output_format,
                'reports_generated': len(results)
            }
            
        except Exception as e:
            all_errors.append(f"レポート生成失敗: {e}")
            summary = {
                'report_type': report_type,
                'output_format': output_format,
                'reports_generated': 0
            }
        
        return IntegrationResult(
            success=len(all_errors) == 0,
            operation_type=OperationType.REPORT,
            execution_time=0,  # 後で設定
            results=results,
            errors=all_errors,
            warnings=all_warnings,
            summary=summary
        )
    
    def _combine_validation_reports(self, validation_results: List[Tuple[str, ValidationReport]]) -> ValidationReport:
        """バリデーションレポートを統合"""
        combined = ValidationReport()
        
        for path, report in validation_results:
            combined.total_files += report.total_files
            combined.total_checks += report.total_checks
            combined.errors.extend(report.errors)
            combined.warnings.extend(report.warnings)
            combined.infos.extend(report.infos)
            combined.execution_time += report.execution_time
        
        return combined
    
    def _generate_summary_report(self, target_paths: List[str]) -> Dict[str, Any]:
        """サマリーレポートを生成"""
        summary = {
            'timestamp': time.time(),
            'target_paths': target_paths,
            'statistics': {},
            'quality_metrics': {},
            'recommendations': []
        }
        
        # 統計情報を収集
        total_files = 0
        file_types = {}
        
        for target_path in target_paths:
            if os.path.isdir(target_path):
                for root, dirs, files in os.walk(target_path):
                    for file in files:
                        total_files += 1
                        ext = os.path.splitext(file)[1]
                        file_types[ext] = file_types.get(ext, 0) + 1
        
        summary['statistics'] = {
            'total_files': total_files,
            'file_types': file_types
        }
        
        # 品質メトリクスを計算
        validation_report = ValidationReport()
        for target_path in target_paths:
            if os.path.isdir(target_path):
                report = self.validation_engine.validate_directory(target_path)
                validation_report.total_files += report.total_files
                validation_report.total_checks += report.total_checks
                validation_report.errors.extend(report.errors)
                validation_report.warnings.extend(report.warnings)
        
        summary['quality_metrics'] = {
            'total_checks': validation_report.total_checks,
            'error_count': len(validation_report.errors),
            'warning_count': len(validation_report.warnings),
            'quality_score': max(0, 100 - (len(validation_report.errors) * 10 + len(validation_report.warnings) * 2))
        }
        
        # 推奨事項を生成
        if validation_report.errors:
            summary['recommendations'].append("エラーの修正を優先してください")
        if validation_report.warnings:
            summary['recommendations'].append("警告の確認と対応を検討してください")
        if validation_report.total_checks == 0:
            summary['recommendations'].append("バリデーション対象ファイルを確認してください")
        
        return summary
    
    def _format_summary_as_text(self, summary_data: Dict[str, Any]) -> str:
        """サマリーデータをテキスト形式でフォーマット"""
        lines = []
        lines.append("=" * 60)
        lines.append("統合設計ツール サマリーレポート")
        lines.append("=" * 60)
        lines.append(f"生成日時: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(summary_data['timestamp']))}")
        lines.append("")
        
        # 統計情報
        stats = summary_data['statistics']
        lines.append("📊 統計情報")
        lines.append("-" * 20)
        lines.append(f"総ファイル数: {stats['total_files']}")
        lines.append("ファイルタイプ別:")
        for ext, count in sorted(stats['file_types'].items()):
            lines.append(f"  {ext or '(拡張子なし)'}: {count}")
        lines.append("")
        
        # 品質メトリクス
        metrics = summary_data['quality_metrics']
        lines.append("📈 品質メトリクス")
        lines.append("-" * 20)
        lines.append(f"総チェック数: {metrics['total_checks']}")
        lines.append(f"エラー数: {metrics['error_count']}")
        lines.append(f"警告数: {metrics['warning_count']}")
        lines.append(f"品質スコア: {metrics['quality_score']}/100")
        lines.append("")
        
        # 推奨事項
        if summary_data['recommendations']:
            lines.append("💡 推奨事項")
            lines.append("-" * 20)
            for i, rec in enumerate(summary_data['recommendations'], 1):
                lines.append(f"{i}. {rec}")
        
        return "\n".join(lines)
    
    def get_execution_history(self) -> List[IntegrationResult]:
        """実行履歴を取得"""
        return self.execution_history.copy()
    
    def clear_execution_history(self):
        """実行履歴をクリア"""
        self.execution_history.clear()
    
    def export_config(self, output_path: str):
        """設定をエクスポート"""
        config_dict = self.config.to_dict()
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(config_dict, f, ensure_ascii=False, indent=2)
    
    def get_status(self) -> Dict[str, Any]:
        """ツールの状態を取得"""
        return {
            'config': {
                'project_root': self.config.project_root,
                'tool_type': self.config.tool_type.value,
                'quality_enabled': self.config.quality.enabled
            },
            'engines': {
                'validation': 'ready',
                'generation': 'ready',
                'analysis': 'ready'
            },
            'execution_history': {
                'total_executions': len(self.execution_history),
                'successful_executions': sum(1 for result in self.execution_history if result.success),
                'last_execution': self.execution_history[-1].operation_type.value if self.execution_history else None
            }
        }


# CLI インターフェース用のヘルパー関数
def create_integration_context(
    operation: str,
    mode: str = "single",
    targets: List[str] = None,
    requirement_ids: List[str] = None,
    **kwargs
) -> IntegrationContext:
    """統合コンテキストを作成"""
    return IntegrationContext(
        operation_type=OperationType(operation),
        execution_mode=ExecutionMode(mode),
        target_paths=targets or [],
        requirement_ids=requirement_ids or [],
        parameters=kwargs
    )


def main():
    """メイン関数（CLI実行用）"""
    import argparse
    
    parser = argparse.ArgumentParser(description="統合設計ツール")
    parser.add_argument("operation", choices=["validate", "generate", "analyze", "sync", "report"])
    parser.add_argument("--mode", choices=["single", "batch", "interactive", "automated"], default="single")
    parser.add_argument("--targets", nargs="*", help="対象パス")
    parser.add_argument("--requirement-ids", nargs="*", help="要求仕様ID")
    parser.add_argument("--config", help="設定ファイルパス")
    parser.add_argument("--output", help="出力ディレクトリ")
    parser.add_argument("--format", choices=["text", "json", "html"], default="text")
    
    args = parser.parse_args()
    
    # ツールを初期化
    tools = IntegratedDesignTools(args.config)
    
    # コンテキストを作成
    context = create_integration_context(
        operation=args.operation,
        mode=args.mode,
        targets=args.targets or [],
        requirement_ids=args.requirement_ids or [],
        output_directory=args.output,
        output_format=args.format
    )
    
    # 実行
    result = tools.execute(context)
    
    # 結果を出力
    if result.success:
        print("✅ 実行成功")
        if result.summary:
            print("📊 サマリー:")
            for key, value in result.summary.items():
                print(f"  {key}: {value}")
    else:
        print("❌ 実行失敗")
        if result.errors:
            print("エラー:")
            for error in result.errors:
                print(f"  - {error}")
    
    if result.warnings:
        print("⚠️ 警告:")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(main())
