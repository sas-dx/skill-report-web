"""
統一設計ツールシステム - 統一分析エンジン

全ての設計ツールで共通利用される横断分析機能を提供します。
品質分析、トレンド分析、パフォーマンス分析を統一実装します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import os
import yaml
import json
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod
import time
from datetime import datetime, timedelta
import statistics
import re
from collections import defaultdict, Counter

from ..config.manager import UnifiedConfigManager
from ..config.schema import UnifiedConfig
from .validation import UnifiedValidationEngine, ValidationReport


class AnalysisType(Enum):
    """分析タイプ"""
    QUALITY_METRICS = "quality_metrics"
    REQUIREMENT_COVERAGE = "requirement_coverage"
    DESIGN_CONSISTENCY = "design_consistency"
    TREND_ANALYSIS = "trend_analysis"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    COMPLEXITY_ANALYSIS = "complexity_analysis"


class MetricType(Enum):
    """メトリクスタイプ"""
    COUNT = "count"
    PERCENTAGE = "percentage"
    RATIO = "ratio"
    SCORE = "score"
    DURATION = "duration"
    SIZE = "size"


@dataclass
class AnalysisMetric:
    """分析メトリクス"""
    name: str
    value: Union[int, float, str]
    metric_type: MetricType
    unit: Optional[str] = None
    description: Optional[str] = None
    threshold: Optional[float] = None
    status: Optional[str] = None  # "good", "warning", "error"


@dataclass
class AnalysisResult:
    """分析結果"""
    analysis_type: AnalysisType
    metrics: List[AnalysisMetric] = field(default_factory=list)
    summary: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)
    execution_time: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrendData:
    """トレンドデータ"""
    timestamp: datetime
    value: Union[int, float]
    category: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAnalyzer(ABC):
    """分析器基底クラス"""
    
    def __init__(self, config: UnifiedConfig):
        self.config = config
        self.validation_engine = UnifiedValidationEngine(config.project_name)
    
    @abstractmethod
    def analyze(self, target_path: str, **kwargs) -> AnalysisResult:
        """分析実行（抽象メソッド）"""
        pass
    
    def _create_metric(
        self,
        name: str,
        value: Union[int, float, str],
        metric_type: MetricType,
        **kwargs
    ) -> AnalysisMetric:
        """メトリクスを作成"""
        metric = AnalysisMetric(
            name=name,
            value=value,
            metric_type=metric_type,
            **kwargs
        )
        
        # 閾値に基づいてステータスを設定
        if metric.threshold is not None and isinstance(value, (int, float)):
            if value >= metric.threshold:
                metric.status = "good"
            elif value >= metric.threshold * 0.7:
                metric.status = "warning"
            else:
                metric.status = "error"
        
        return metric


class QualityMetricsAnalyzer(BaseAnalyzer):
    """品質メトリクス分析器"""
    
    def analyze(self, target_path: str, **kwargs) -> AnalysisResult:
        """品質メトリクス分析"""
        start_time = time.time()
        result = AnalysisResult(analysis_type=AnalysisType.QUALITY_METRICS)
        
        try:
            # ディレクトリ全体のバリデーション実行
            validation_report = self.validation_engine.validate_directory(target_path, "*")
            
            # 基本メトリクスを計算
            total_files = validation_report.total_files
            total_checks = validation_report.total_checks
            error_count = validation_report.error_count
            warning_count = validation_report.warning_count
            
            # メトリクスを作成
            result.metrics = [
                self._create_metric(
                    "総ファイル数",
                    total_files,
                    MetricType.COUNT,
                    unit="files",
                    description="検証対象ファイルの総数"
                ),
                self._create_metric(
                    "総チェック数",
                    total_checks,
                    MetricType.COUNT,
                    unit="checks",
                    description="実行された検証項目の総数"
                ),
                self._create_metric(
                    "エラー数",
                    error_count,
                    MetricType.COUNT,
                    unit="errors",
                    description="検出されたエラーの数",
                    threshold=0
                ),
                self._create_metric(
                    "警告数",
                    warning_count,
                    MetricType.COUNT,
                    unit="warnings",
                    description="検出された警告の数",
                    threshold=total_checks * 0.1
                ),
                self._create_metric(
                    "品質スコア",
                    self._calculate_quality_score(validation_report),
                    MetricType.SCORE,
                    unit="score",
                    description="全体的な品質スコア（0-1）",
                    threshold=0.8
                ),
                self._create_metric(
                    "エラー率",
                    (error_count / max(total_checks, 1)) * 100,
                    MetricType.PERCENTAGE,
                    unit="%",
                    description="総チェック数に対するエラーの割合",
                    threshold=5.0
                )
            ]
            
            # サマリーを作成
            result.summary = {
                "overall_status": "good" if error_count == 0 else "error",
                "quality_score": self._calculate_quality_score(validation_report),
                "improvement_areas": self._identify_improvement_areas(validation_report)
            }
            
            # 推奨事項を生成
            result.recommendations = self._generate_quality_recommendations(validation_report)
            
        except Exception as e:
            result.metadata["error"] = str(e)
        
        result.execution_time = time.time() - start_time
        return result
    
    def _calculate_quality_score(self, report: ValidationReport) -> float:
        """品質スコアを計算"""
        if report.total_checks == 0:
            return 1.0
        
        error_penalty = report.error_count / report.total_checks
        warning_penalty = (report.warning_count / report.total_checks) * 0.5
        
        score = max(0.0, 1.0 - error_penalty - warning_penalty)
        return round(score, 3)
    
    def _identify_improvement_areas(self, report: ValidationReport) -> List[str]:
        """改善領域を特定"""
        areas = []
        
        # エラーカテゴリ別の集計
        error_categories = Counter()
        for error in report.errors:
            error_categories[error.category.value] += 1
        
        # 最も多いエラーカテゴリを特定
        if error_categories:
            most_common = error_categories.most_common(3)
            for category, count in most_common:
                areas.append(f"{category}: {count}件")
        
        return areas
    
    def _generate_quality_recommendations(self, report: ValidationReport) -> List[str]:
        """品質改善推奨事項を生成"""
        recommendations = []
        
        if report.error_count > 0:
            recommendations.append(f"{report.error_count}件のエラーを修正してください")
        
        if report.warning_count > report.total_checks * 0.2:
            recommendations.append("警告が多すぎます。コード品質の見直しを検討してください")
        
        if report.total_files > 0 and report.total_checks / report.total_files < 5:
            recommendations.append("ファイルあたりのチェック数が少ないです。検証項目を追加してください")
        
        return recommendations


class RequirementCoverageAnalyzer(BaseAnalyzer):
    """要求仕様カバレッジ分析器"""
    
    def analyze(self, target_path: str, **kwargs) -> AnalysisResult:
        """要求仕様カバレッジ分析"""
        start_time = time.time()
        result = AnalysisResult(analysis_type=AnalysisType.REQUIREMENT_COVERAGE)
        
        try:
            # 要求仕様IDを収集
            requirement_data = self._collect_requirement_ids(target_path)
            
            # カバレッジメトリクスを計算
            coverage_metrics = self._calculate_coverage_metrics(requirement_data)
            
            # メトリクスを作成
            result.metrics = [
                self._create_metric(
                    "総要求仕様ID数",
                    coverage_metrics["total_requirements"],
                    MetricType.COUNT,
                    unit="requirements",
                    description="プロジェクト内の総要求仕様ID数"
                ),
                self._create_metric(
                    "実装済み要求数",
                    coverage_metrics["implemented_requirements"],
                    MetricType.COUNT,
                    unit="requirements",
                    description="実装ファイルで参照されている要求仕様ID数"
                ),
                self._create_metric(
                    "カバレッジ率",
                    coverage_metrics["coverage_rate"] * 100,
                    MetricType.PERCENTAGE,
                    unit="%",
                    description="要求仕様IDの実装カバレッジ率",
                    threshold=80.0
                ),
                self._create_metric(
                    "孤立要求数",
                    coverage_metrics["orphaned_requirements"],
                    MetricType.COUNT,
                    unit="requirements",
                    description="実装で参照されていない要求仕様ID数",
                    threshold=0
                )
            ]
            
            # カテゴリ別分析
            category_analysis = self._analyze_by_category(requirement_data)
            
            result.summary = {
                "coverage_status": "good" if coverage_metrics["coverage_rate"] >= 0.8 else "warning",
                "category_breakdown": category_analysis,
                "top_categories": list(category_analysis.keys())[:5]
            }
            
            # 推奨事項を生成
            result.recommendations = self._generate_coverage_recommendations(coverage_metrics, category_analysis)
            
        except Exception as e:
            result.metadata["error"] = str(e)
        
        result.execution_time = time.time() - start_time
        return result
    
    def _collect_requirement_ids(self, target_path: str) -> Dict[str, Any]:
        """要求仕様IDを収集"""
        requirement_data = {
            "all_requirements": set(),
            "implemented_requirements": set(),
            "file_mapping": defaultdict(list),
            "category_mapping": defaultdict(list)
        }
        
        # 要求仕様IDパターン
        req_pattern = re.compile(r'([A-Z]{3}\.\d+-[A-Z]+\.\d+)')
        
        # ファイルを走査
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if file.endswith(('.md', '.yaml', '.ts', '.tsx', '.js', '.jsx')):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # 要求仕様IDを抽出
                        matches = req_pattern.findall(content)
                        for match in matches:
                            requirement_data["all_requirements"].add(match)
                            requirement_data["file_mapping"][match].append(file_path)
                            
                            # カテゴリを抽出
                            category = match.split('.')[0]
                            requirement_data["category_mapping"][category].append(match)
                            
                            # 実装ファイルかチェック
                            if any(impl_dir in file_path for impl_dir in ['src/', 'lib/', 'components/']):
                                requirement_data["implemented_requirements"].add(match)
                    
                    except Exception:
                        continue
        
        return requirement_data
    
    def _calculate_coverage_metrics(self, requirement_data: Dict[str, Any]) -> Dict[str, Any]:
        """カバレッジメトリクスを計算"""
        total_requirements = len(requirement_data["all_requirements"])
        implemented_requirements = len(requirement_data["implemented_requirements"])
        orphaned_requirements = total_requirements - implemented_requirements
        
        coverage_rate = implemented_requirements / max(total_requirements, 1)
        
        return {
            "total_requirements": total_requirements,
            "implemented_requirements": implemented_requirements,
            "orphaned_requirements": orphaned_requirements,
            "coverage_rate": coverage_rate
        }
    
    def _analyze_by_category(self, requirement_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """カテゴリ別分析"""
        category_analysis = {}
        
        for category, requirements in requirement_data["category_mapping"].items():
            unique_requirements = set(requirements)
            implemented = unique_requirements.intersection(requirement_data["implemented_requirements"])
            
            category_analysis[category] = {
                "total": len(unique_requirements),
                "implemented": len(implemented),
                "coverage_rate": len(implemented) / max(len(unique_requirements), 1)
            }
        
        # カバレッジ率でソート
        return dict(sorted(category_analysis.items(), key=lambda x: x[1]["coverage_rate"], reverse=True))
    
    def _generate_coverage_recommendations(self, metrics: Dict[str, Any], category_analysis: Dict[str, Any]) -> List[str]:
        """カバレッジ改善推奨事項を生成"""
        recommendations = []
        
        if metrics["coverage_rate"] < 0.8:
            recommendations.append(f"カバレッジ率が{metrics['coverage_rate']:.1%}と低いです。実装の追加を検討してください")
        
        if metrics["orphaned_requirements"] > 0:
            recommendations.append(f"{metrics['orphaned_requirements']}個の要求仕様IDが実装されていません")
        
        # 低カバレッジカテゴリを特定
        low_coverage_categories = [
            cat for cat, data in category_analysis.items()
            if data["coverage_rate"] < 0.5
        ]
        
        if low_coverage_categories:
            recommendations.append(f"以下のカテゴリのカバレッジが低いです: {', '.join(low_coverage_categories)}")
        
        return recommendations


class ComplexityAnalyzer(BaseAnalyzer):
    """複雑度分析器"""
    
    def analyze(self, target_path: str, **kwargs) -> AnalysisResult:
        """複雑度分析"""
        start_time = time.time()
        result = AnalysisResult(analysis_type=AnalysisType.COMPLEXITY_ANALYSIS)
        
        try:
            # ファイル複雑度を分析
            complexity_data = self._analyze_file_complexity(target_path)
            
            # 複雑度メトリクスを計算
            complexity_metrics = self._calculate_complexity_metrics(complexity_data)
            
            # メトリクスを作成
            result.metrics = [
                self._create_metric(
                    "平均ファイルサイズ",
                    complexity_metrics["avg_file_size"],
                    MetricType.SIZE,
                    unit="lines",
                    description="ファイルあたりの平均行数",
                    threshold=500
                ),
                self._create_metric(
                    "最大ファイルサイズ",
                    complexity_metrics["max_file_size"],
                    MetricType.SIZE,
                    unit="lines",
                    description="最大ファイル行数",
                    threshold=1000
                ),
                self._create_metric(
                    "複雑なファイル数",
                    complexity_metrics["complex_files"],
                    MetricType.COUNT,
                    unit="files",
                    description="閾値を超える複雑なファイル数",
                    threshold=0
                ),
                self._create_metric(
                    "平均ネスト深度",
                    complexity_metrics["avg_nesting_depth"],
                    MetricType.RATIO,
                    unit="levels",
                    description="平均的なネスト深度",
                    threshold=3.0
                )
            ]
            
            result.summary = {
                "complexity_status": "good" if complexity_metrics["complex_files"] == 0 else "warning",
                "hotspots": complexity_data["hotspots"][:5],
                "total_files_analyzed": len(complexity_data["files"])
            }
            
            # 推奨事項を生成
            result.recommendations = self._generate_complexity_recommendations(complexity_metrics, complexity_data)
            
        except Exception as e:
            result.metadata["error"] = str(e)
        
        result.execution_time = time.time() - start_time
        return result
    
    def _analyze_file_complexity(self, target_path: str) -> Dict[str, Any]:
        """ファイル複雑度を分析"""
        complexity_data = {
            "files": [],
            "hotspots": []
        }
        
        # 対象ファイル拡張子
        target_extensions = ['.ts', '.tsx', '.js', '.jsx', '.py', '.md', '.yaml']
        
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if any(file.endswith(ext) for ext in target_extensions):
                    file_path = os.path.join(root, file)
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # ファイル複雑度を計算
                        file_complexity = self._calculate_file_complexity(content, file_path)
                        complexity_data["files"].append(file_complexity)
                        
                        # ホットスポットを特定
                        if file_complexity["complexity_score"] > 0.7:
                            complexity_data["hotspots"].append(file_complexity)
                    
                    except Exception:
                        continue
        
        # ホットスポットを複雑度順にソート
        complexity_data["hotspots"].sort(key=lambda x: x["complexity_score"], reverse=True)
        
        return complexity_data
    
    def _calculate_file_complexity(self, content: str, file_path: str) -> Dict[str, Any]:
        """ファイル複雑度を計算"""
        lines = content.split('\n')
        line_count = len(lines)
        
        # 基本メトリクス
        non_empty_lines = len([line for line in lines if line.strip()])
        comment_lines = len([line for line in lines if line.strip().startswith(('#', '//', '/*', '*', '<!--'))])
        
        # ネスト深度を計算
        max_nesting = 0
        current_nesting = 0
        
        for line in lines:
            stripped = line.strip()
            
            # 開始ブロック
            if any(keyword in stripped for keyword in ['{', 'if ', 'for ', 'while ', 'function ', 'class ']):
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            
            # 終了ブロック
            if '}' in stripped:
                current_nesting = max(0, current_nesting - 1)
        
        # 複雑度スコアを計算（0-1）
        size_factor = min(1.0, line_count / 1000)  # 1000行で最大
        nesting_factor = min(1.0, max_nesting / 10)  # 10レベルで最大
        comment_ratio = comment_lines / max(non_empty_lines, 1)
        
        complexity_score = (size_factor * 0.4 + nesting_factor * 0.4 + (1 - comment_ratio) * 0.2)
        
        return {
            "file_path": file_path,
            "line_count": line_count,
            "non_empty_lines": non_empty_lines,
            "comment_lines": comment_lines,
            "max_nesting_depth": max_nesting,
            "complexity_score": round(complexity_score, 3)
        }
    
    def _calculate_complexity_metrics(self, complexity_data: Dict[str, Any]) -> Dict[str, Any]:
        """複雑度メトリクスを計算"""
        files = complexity_data["files"]
        
        if not files:
            return {
                "avg_file_size": 0,
                "max_file_size": 0,
                "complex_files": 0,
                "avg_nesting_depth": 0
            }
        
        line_counts = [f["line_count"] for f in files]
        nesting_depths = [f["max_nesting_depth"] for f in files]
        complex_files = len([f for f in files if f["complexity_score"] > 0.7])
        
        return {
            "avg_file_size": round(statistics.mean(line_counts), 1),
            "max_file_size": max(line_counts),
            "complex_files": complex_files,
            "avg_nesting_depth": round(statistics.mean(nesting_depths), 1)
        }
    
    def _generate_complexity_recommendations(self, metrics: Dict[str, Any], complexity_data: Dict[str, Any]) -> List[str]:
        """複雑度改善推奨事項を生成"""
        recommendations = []
        
        if metrics["complex_files"] > 0:
            recommendations.append(f"{metrics['complex_files']}個の複雑なファイルがあります。リファクタリングを検討してください")
        
        if metrics["avg_file_size"] > 500:
            recommendations.append(f"平均ファイルサイズが{metrics['avg_file_size']}行と大きいです。ファイル分割を検討してください")
        
        if metrics["avg_nesting_depth"] > 3:
            recommendations.append(f"平均ネスト深度が{metrics['avg_nesting_depth']}と深いです。コード構造の見直しを検討してください")
        
        # ホットスポットの推奨事項
        hotspots = complexity_data["hotspots"][:3]
        if hotspots:
            file_names = [os.path.basename(h["file_path"]) for h in hotspots]
            recommendations.append(f"以下のファイルの複雑度が高いです: {', '.join(file_names)}")
        
        return recommendations


class UnifiedAnalysisEngine:
    """統一分析エンジン"""
    
    def __init__(self, project_name: str = "default"):
        self.config_manager = UnifiedConfigManager(project_name)
        self.config = self.config_manager.load_config()
        
        # 分析器を初期化
        self.analyzers = {
            AnalysisType.QUALITY_METRICS: QualityMetricsAnalyzer(self.config),
            AnalysisType.REQUIREMENT_COVERAGE: RequirementCoverageAnalyzer(self.config),
            AnalysisType.COMPLEXITY_ANALYSIS: ComplexityAnalyzer(self.config)
        }
    
    def analyze(self, analysis_type: AnalysisType, target_path: str, **kwargs) -> AnalysisResult:
        """分析実行"""
        if analysis_type not in self.analyzers:
            return AnalysisResult(
                analysis_type=analysis_type,
                metadata={"error": f"サポートされていない分析タイプ: {analysis_type}"}
            )
        
        analyzer = self.analyzers[analysis_type]
        return analyzer.analyze(target_path, **kwargs)
    
    def comprehensive_analysis(self, target_path: str) -> Dict[AnalysisType, AnalysisResult]:
        """包括的分析"""
        results = {}
        
        for analysis_type in [
            AnalysisType.QUALITY_METRICS,
            AnalysisType.REQUIREMENT_COVERAGE,
            AnalysisType.COMPLEXITY_ANALYSIS
        ]:
            try:
                result = self.analyze(analysis_type, target_path)
                results[analysis_type] = result
            except Exception as e:
                results[analysis_type] = AnalysisResult(
                    analysis_type=analysis_type,
                    metadata={"error": str(e)}
                )
        
        return results
    
    def generate_dashboard_data(self, target_path: str) -> Dict[str, Any]:
        """ダッシュボード用データを生成"""
        comprehensive_results = self.comprehensive_analysis(target_path)
        
        dashboard_data = {
            "overview": {
                "timestamp": datetime.now().isoformat(),
                "target_path": target_path,
                "analysis_count": len(comprehensive_results)
            },
            "metrics": {},
            "status": {},
            "recommendations": []
        }
        
        # 各分析結果からデータを抽出
        for analysis_type, result in comprehensive_results.items():
            type_name = analysis_type.value
            
            # メトリクスを抽出
            dashboard_data["metrics"][type_name] = [
                {
                    "name": metric.name,
                    "value": metric.value,
                    "unit": metric.unit,
                    "status": metric.status
                }
                for metric in result.metrics
            ]
            
            # ステータスを抽出
            dashboard_data["status"][type_name] = result.summary.get("overall_status", "unknown")
            
            # 推奨事項を統合
            dashboard_data["recommendations"].extend(result.recommendations)
        
        return dashboard_data
    
    def export_analysis_report(self, results: Dict[AnalysisType, AnalysisResult], format: str = "json") -> str:
        """分析レポートをエクスポート"""
        if format == "json":
            return self._export_json_report(results)
        elif format == "markdown":
            return self._export_markdown_report(results)
        else:
            raise ValueError(f"サポートされていないフォーマット: {format}")
    
    def _export_json_report(self, results: Dict[AnalysisType, AnalysisResult]) -> str:
        """JSON形式レポート生成"""
        report_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "analysis_engine": "UnifiedAnalysisEngine",
                "version": "1.0.0"
            },
            "results": {}
        }
        
        for analysis_type, result in results.items():
            report_data["results"][analysis_type.value] = {
                "metrics": [
                    {
                        "name": metric.name,
                        "value": metric.value,
                        "type": metric.metric_type.value,
                        "unit": metric.unit,
                        "description": metric.description,
                        "status": metric.status
                    }
                    for metric in result.metrics
                ],
                "summary": result.summary,
                "recommendations": result.recommendations,
                "execution_time": result.execution_time
            }
        
        return json.dumps(report_data, ensure_ascii=False, indent=2)
    
    def _export_markdown_report(self, results: Dict[AnalysisType, AnalysisResult]) -> str:
        """Markdown形式レポート生成"""
        lines = []
        lines.append("# 統一設計ツールシステム 分析レポート")
        lines.append("")
        lines.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        for analysis_type, result in results.items():
            lines.append(f"## {analysis_type.value.replace('_', ' ').title()}")
            lines.append("")
            
            # メトリクス表
            lines.append("### メトリクス")
            lines.append("")
            lines.append("| 項目 | 値 | 単位 | ステータス | 説明 |")
            lines.append("|------|----|----|----------|------|")
            
            for metric in result.metrics:
                status_emoji = {"good": "✅", "warning": "⚠️", "error": "❌"}.get(metric.status, "")
                lines.append(f"| {metric.name} | {metric.value} | {metric.unit or ''} | {status_emoji} | {metric.description or ''} |")
            
            lines.append("")
            
            # 推奨事項
            if result.recommendations:
                lines.append("### 推奨事項")
                lines.append("")
                for rec in result.recommendations:
                    lines.append(f"- {rec}")
                lines.append("")
        
        return "\n".join(lines)
