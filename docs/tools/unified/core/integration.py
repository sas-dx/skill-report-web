"""
統一設計ツールシステム - 統一統合エンジン

全ての設計ツールで共通利用される横断統合機能を提供します。
ツール間連携、データ同期、ワークフロー統合を統一実装します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import os
import yaml
import json
from typing import Dict, List, Any, Optional, Union, Callable, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import time
from datetime import datetime
import asyncio
import concurrent.futures

from ..config.manager import UnifiedConfigManager
from ..config.schema import UnifiedConfig
from .validation import UnifiedValidationEngine, ValidationReport
from .generation import UnifiedGenerationEngine, GenerationContext, GenerationResult, GenerationType, GenerationTemplate


class IntegrationType(Enum):
    """統合タイプ"""
    VALIDATION_GENERATION = "validation_generation"
    CROSS_REFERENCE = "cross_reference"
    WORKFLOW = "workflow"
    DATA_SYNC = "data_sync"
    QUALITY_ASSURANCE = "quality_assurance"


class WorkflowStage(Enum):
    """ワークフローステージ"""
    VALIDATION = "validation"
    GENERATION = "generation"
    CROSS_CHECK = "cross_check"
    QUALITY_CHECK = "quality_check"
    FINALIZATION = "finalization"


@dataclass
class IntegrationTask:
    """統合タスク"""
    task_id: str
    task_type: IntegrationType
    input_data: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    priority: int = 1
    timeout: float = 300.0


@dataclass
class IntegrationResult:
    """統合結果"""
    task_id: str
    success: bool
    stage: WorkflowStage
    results: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowContext:
    """ワークフローコンテキスト"""
    workflow_id: str
    project_name: str
    base_directory: str
    target_files: List[str] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)
    variables: Dict[str, Any] = field(default_factory=dict)


class BaseIntegrator(ABC):
    """統合器基底クラス"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.validation_engine = UnifiedValidationEngine(config.project_name)
        self.generation_engine = UnifiedGenerationEngine(config.project_name)
    
    @abstractmethod
    async def execute(self, task: IntegrationTask) -> IntegrationResult:
        """統合実行（抽象メソッド）"""
        pass
    
    def _create_result(self, task_id: str, success: bool, stage: WorkflowStage, **kwargs) -> IntegrationResult:
        """統合結果を作成"""
        return IntegrationResult(
            task_id=task_id,
            success=success,
            stage=stage,
            **kwargs
        )


class ValidationGenerationIntegrator(BaseIntegrator):
    """バリデーション・生成統合器"""
    
    async def execute(self, task: IntegrationTask) -> IntegrationResult:
        """バリデーション→生成の統合実行"""
        start_time = time.time()
        result = self._create_result(task.task_id, False, WorkflowStage.VALIDATION)
        
        try:
            input_data = task.input_data
            file_path = input_data.get("file_path")
            template_type = input_data.get("template_type")
            output_type = input_data.get("output_type", GenerationType.MARKDOWN)
            
            if not file_path or not template_type:
                result.errors.append("必須パラメータが不足しています: file_path, template_type")
                return result
            
            # Step 1: バリデーション実行
            validation_report = self.validation_engine.validate_file(file_path)
            result.results["validation"] = {
                "is_valid": validation_report.is_valid,
                "error_count": validation_report.error_count,
                "warning_count": validation_report.warning_count,
                "report": validation_report
            }
            
            # バリデーションエラーがある場合は生成をスキップ
            if not validation_report.is_valid:
                result.warnings.append("バリデーションエラーのため生成をスキップしました")
                result.stage = WorkflowStage.VALIDATION
                result.execution_time = time.time() - start_time
                return result
            
            # Step 2: 生成実行
            result.stage = WorkflowStage.GENERATION
            
            # ファイルからデータを読み込み
            file_data = await self._load_file_data(file_path)
            
            # 生成コンテキストを作成
            generation_context = GenerationContext(
                template_type=GenerationTemplate(template_type),
                output_type=GenerationType(output_type),
                data=file_data,
                metadata={"source_file": file_path, "validation_passed": True}
            )
            
            # 生成実行
            generation_result = self.generation_engine.generate(generation_context)
            result.results["generation"] = {
                "success": generation_result.success,
                "content_length": len(generation_result.content),
                "warnings": generation_result.warnings,
                "errors": generation_result.errors,
                "result": generation_result
            }
            
            if not generation_result.success:
                result.errors.extend(generation_result.errors)
                result.execution_time = time.time() - start_time
                return result
            
            # Step 3: 生成結果の保存（オプション）
            output_path = input_data.get("output_path")
            if output_path:
                save_success = self.generation_engine.save_result(generation_result, output_path)
                result.results["save"] = {"success": save_success, "path": output_path}
            
            result.success = True
            result.stage = WorkflowStage.FINALIZATION
            
        except Exception as e:
            result.errors.append(f"統合実行エラー: {e}")
        
        result.execution_time = time.time() - start_time
        return result
    
    async def _load_file_data(self, file_path: str) -> Dict[str, Any]:
        """ファイルからデータを読み込み"""
        file_ext = Path(file_path).suffix.lower()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_ext in ['.yaml', '.yml']:
                return yaml.safe_load(content)
            elif file_ext == '.json':
                return json.loads(content)
            else:
                # テキストファイルの場合は基本情報を抽出
                return {
                    "content": content,
                    "file_name": os.path.basename(file_path),
                    "file_type": file_ext,
                    "line_count": len(content.split('\n'))
                }
        except Exception as e:
            raise Exception(f"ファイル読み込みエラー: {e}")


class CrossReferenceIntegrator(BaseIntegrator):
    """横断参照統合器"""
    
    async def execute(self, task: IntegrationTask) -> IntegrationResult:
        """横断参照チェックの統合実行"""
        start_time = time.time()
        result = self._create_result(task.task_id, False, WorkflowStage.CROSS_CHECK)
        
        try:
            input_data = task.input_data
            base_directory = input_data.get("base_directory", self.config.project_root)
            
            # 横断参照検証を実行
            cross_ref_report = self.validation_engine.validate_cross_reference(base_directory)
            
            # 結果を分析
            analysis = self._analyze_cross_reference_results(cross_ref_report)
            
            result.results = {
                "cross_reference_report": cross_ref_report,
                "analysis": analysis,
                "recommendations": self._generate_recommendations(analysis)
            }
            
            result.success = True
            result.stage = WorkflowStage.FINALIZATION
            
        except Exception as e:
            result.errors.append(f"横断参照統合エラー: {e}")
        
        result.execution_time = time.time() - start_time
        return result
    
    def _analyze_cross_reference_results(self, report: ValidationReport) -> Dict[str, Any]:
        """横断参照結果を分析"""
        analysis = {
            "orphaned_requirements": [],
            "missing_implementations": [],
            "inconsistent_references": [],
            "coverage_stats": {}
        }
        
        # 孤立した要求仕様IDを特定
        for warning in report.warnings:
            if "参照されていません" in warning.message:
                analysis["orphaned_requirements"].append({
                    "requirement_id": warning.requirement_id,
                    "file_path": warning.file_path,
                    "message": warning.message
                })
        
        # カバレッジ統計を計算
        total_requirements = len(set(w.requirement_id for w in report.warnings if w.requirement_id))
        analysis["coverage_stats"] = {
            "total_requirements": total_requirements,
            "orphaned_count": len(analysis["orphaned_requirements"]),
            "coverage_rate": (total_requirements - len(analysis["orphaned_requirements"])) / max(total_requirements, 1)
        }
        
        return analysis
    
    def _generate_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """推奨事項を生成"""
        recommendations = []
        
        if analysis["orphaned_requirements"]:
            recommendations.append(
                f"{len(analysis['orphaned_requirements'])}個の孤立した要求仕様IDがあります。"
                "関連する設計書や実装ファイルで参照を追加してください。"
            )
        
        coverage_rate = analysis["coverage_stats"]["coverage_rate"]
        if coverage_rate < 0.8:
            recommendations.append(
                f"要求仕様IDのカバレッジ率が{coverage_rate:.1%}と低いです。"
                "トレーサビリティを向上させるため、参照を追加してください。"
            )
        
        return recommendations


class QualityAssuranceIntegrator(BaseIntegrator):
    """品質保証統合器"""
    
    async def execute(self, task: IntegrationTask) -> IntegrationResult:
        """品質保証チェックの統合実行"""
        start_time = time.time()
        result = self._create_result(task.task_id, False, WorkflowStage.QUALITY_CHECK)
        
        try:
            input_data = task.input_data
            target_directory = input_data.get("target_directory", self.config.project_root)
            quality_criteria = input_data.get("quality_criteria", {})
            
            # 品質チェックを実行
            quality_results = await self._run_quality_checks(target_directory, quality_criteria)
            
            # 品質スコアを計算
            quality_score = self._calculate_quality_score(quality_results)
            
            result.results = {
                "quality_checks": quality_results,
                "quality_score": quality_score,
                "passed": quality_score >= quality_criteria.get("minimum_score", 0.8),
                "recommendations": self._generate_quality_recommendations(quality_results)
            }
            
            result.success = True
            result.stage = WorkflowStage.FINALIZATION
            
        except Exception as e:
            result.errors.append(f"品質保証統合エラー: {e}")
        
        result.execution_time = time.time() - start_time
        return result
    
    async def _run_quality_checks(self, target_directory: str, criteria: Dict[str, Any]) -> Dict[str, Any]:
        """品質チェックを実行"""
        checks = {}
        
        # ファイル形式チェック
        checks["format_validation"] = self.validation_engine.validate_directory(
            target_directory, "*.md"
        )
        
        # 要求仕様ID整合性チェック
        checks["requirement_consistency"] = self.validation_engine.validate_cross_reference(
            target_directory
        )
        
        # ドキュメント完全性チェック
        checks["documentation_completeness"] = await self._check_documentation_completeness(
            target_directory
        )
        
        return checks
    
    async def _check_documentation_completeness(self, directory: str) -> Dict[str, Any]:
        """ドキュメント完全性をチェック"""
        completeness = {
            "required_sections": [],
            "missing_sections": [],
            "completeness_rate": 0.0
        }
        
        # 必須セクションの定義
        required_sections = [
            "エグゼクティブサマリー",
            "要求仕様ID",
            "設計書"
        ]
        
        # Markdownファイルをチェック
        md_files = list(Path(directory).rglob("*.md"))
        total_files = len(md_files)
        compliant_files = 0
        
        for md_file in md_files:
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                file_sections = []
                missing_sections = []
                
                for section in required_sections:
                    if section in content:
                        file_sections.append(section)
                    else:
                        missing_sections.append(section)
                
                if not missing_sections:
                    compliant_files += 1
                
            except Exception:
                continue
        
        completeness["completeness_rate"] = compliant_files / max(total_files, 1)
        return completeness
    
    def _calculate_quality_score(self, quality_results: Dict[str, Any]) -> float:
        """品質スコアを計算"""
        scores = []
        
        # フォーマット検証スコア
        format_report = quality_results.get("format_validation")
        if format_report:
            format_score = 1.0 if format_report.is_valid else 0.5
            scores.append(format_score)
        
        # 要求仕様ID整合性スコア
        req_report = quality_results.get("requirement_consistency")
        if req_report:
            req_score = max(0.0, 1.0 - (req_report.warning_count / max(req_report.total_checks, 1)))
            scores.append(req_score)
        
        # ドキュメント完全性スコア
        doc_completeness = quality_results.get("documentation_completeness")
        if doc_completeness:
            scores.append(doc_completeness["completeness_rate"])
        
        return sum(scores) / max(len(scores), 1)
    
    def _generate_quality_recommendations(self, quality_results: Dict[str, Any]) -> List[str]:
        """品質改善推奨事項を生成"""
        recommendations = []
        
        # フォーマット検証の推奨事項
        format_report = quality_results.get("format_validation")
        if format_report and not format_report.is_valid:
            recommendations.append("フォーマットエラーを修正してください")
        
        # ドキュメント完全性の推奨事項
        doc_completeness = quality_results.get("documentation_completeness")
        if doc_completeness and doc_completeness["completeness_rate"] < 0.8:
            recommendations.append("必須セクションが不足しているドキュメントがあります")
        
        return recommendations


class UnifiedIntegrationEngine:
    """統一統合エンジン"""
    
    def __init__(self, project_name: str = "default"):
        self.config_manager = UnifiedConfigManager(project_name)
        self.config = self.config_manager.load_config()
        
        # 統合器を初期化
        self.integrators = {
            IntegrationType.VALIDATION_GENERATION: ValidationGenerationIntegrator(self.config),
            IntegrationType.CROSS_REFERENCE: CrossReferenceIntegrator(self.config),
            IntegrationType.QUALITY_ASSURANCE: QualityAssuranceIntegrator(self.config)
        }
    
    async def execute_task(self, task: IntegrationTask) -> IntegrationResult:
        """統合タスクを実行"""
        if task.task_type not in self.integrators:
            return IntegrationResult(
                task_id=task.task_id,
                success=False,
                stage=WorkflowStage.VALIDATION,
                errors=[f"サポートされていない統合タイプ: {task.task_type}"]
            )
        
        integrator = self.integrators[task.task_type]
        
        try:
            # タイムアウト付きで実行
            result = await asyncio.wait_for(
                integrator.execute(task),
                timeout=task.timeout
            )
            return result
            
        except asyncio.TimeoutError:
            return IntegrationResult(
                task_id=task.task_id,
                success=False,
                stage=WorkflowStage.VALIDATION,
                errors=[f"タスク実行がタイムアウトしました: {task.timeout}秒"]
            )
        except Exception as e:
            return IntegrationResult(
                task_id=task.task_id,
                success=False,
                stage=WorkflowStage.VALIDATION,
                errors=[f"タスク実行エラー: {e}"]
            )
    
    async def execute_workflow(self, context: WorkflowContext, tasks: List[IntegrationTask]) -> Dict[str, IntegrationResult]:
        """ワークフローを実行"""
        results = {}
        
        # 依存関係を解決してタスクを順序付け
        ordered_tasks = self._resolve_dependencies(tasks)
        
        # タスクを順次実行
        for task in ordered_tasks:
            result = await self.execute_task(task)
            results[task.task_id] = result
            
            # エラーが発生した場合は後続タスクをスキップ
            if not result.success and task.metadata.get("critical", False):
                break
        
        return results
    
    async def execute_parallel_workflow(self, context: WorkflowContext, tasks: List[IntegrationTask]) -> Dict[str, IntegrationResult]:
        """並列ワークフローを実行"""
        # 依存関係のないタスクを並列実行
        independent_tasks = [task for task in tasks if not task.dependencies]
        dependent_tasks = [task for task in tasks if task.dependencies]
        
        results = {}
        
        # 独立タスクを並列実行
        if independent_tasks:
            parallel_results = await asyncio.gather(
                *[self.execute_task(task) for task in independent_tasks],
                return_exceptions=True
            )
            
            for task, result in zip(independent_tasks, parallel_results):
                if isinstance(result, Exception):
                    results[task.task_id] = IntegrationResult(
                        task_id=task.task_id,
                        success=False,
                        stage=WorkflowStage.VALIDATION,
                        errors=[f"並列実行エラー: {result}"]
                    )
                else:
                    results[task.task_id] = result
        
        # 依存タスクを順次実行
        for task in dependent_tasks:
            # 依存関係をチェック
            dependencies_met = all(
                dep_id in results and results[dep_id].success
                for dep_id in task.dependencies
            )
            
            if dependencies_met:
                result = await self.execute_task(task)
                results[task.task_id] = result
            else:
                results[task.task_id] = IntegrationResult(
                    task_id=task.task_id,
                    success=False,
                    stage=WorkflowStage.VALIDATION,
                    errors=["依存関係が満たされていません"]
                )
        
        return results
    
    def _resolve_dependencies(self, tasks: List[IntegrationTask]) -> List[IntegrationTask]:
        """依存関係を解決してタスクを順序付け"""
        ordered = []
        remaining = tasks.copy()
        
        while remaining:
            # 依存関係のないタスクを見つける
            ready_tasks = [
                task for task in remaining
                if all(dep_id in [t.task_id for t in ordered] for dep_id in task.dependencies)
            ]
            
            if not ready_tasks:
                # 循環依存または未解決の依存関係
                break
            
            # 優先度順にソート
            ready_tasks.sort(key=lambda t: t.priority, reverse=True)
            
            # 最初のタスクを追加
            task = ready_tasks[0]
            ordered.append(task)
            remaining.remove(task)
        
        # 残りのタスクも追加（依存関係エラーとして処理される）
        ordered.extend(remaining)
        
        return ordered
    
    def create_validation_generation_task(
        self,
        task_id: str,
        file_path: str,
        template_type: str,
        output_type: str = "markdown",
        output_path: Optional[str] = None
    ) -> IntegrationTask:
        """バリデーション・生成タスクを作成"""
        return IntegrationTask(
            task_id=task_id,
            task_type=IntegrationType.VALIDATION_GENERATION,
            input_data={
                "file_path": file_path,
                "template_type": template_type,
                "output_type": output_type,
                "output_path": output_path
            }
        )
    
    def create_quality_assurance_task(
        self,
        task_id: str,
        target_directory: str,
        quality_criteria: Optional[Dict[str, Any]] = None
    ) -> IntegrationTask:
        """品質保証タスクを作成"""
        return IntegrationTask(
            task_id=task_id,
            task_type=IntegrationType.QUALITY_ASSURANCE,
            input_data={
                "target_directory": target_directory,
                "quality_criteria": quality_criteria or {}
            }
        )
    
    def create_cross_reference_task(
        self,
        task_id: str,
        base_directory: Optional[str] = None
    ) -> IntegrationTask:
        """横断参照タスクを作成"""
        return IntegrationTask(
            task_id=task_id,
            task_type=IntegrationType.CROSS_REFERENCE,
            input_data={
                "base_directory": base_directory or self.config.project_root
            }
        )
