"""
統合設計ツール - 統一解析エンジン

全ての設計ツールで共通利用される解析機能を提供します。
依存関係解析、品質メトリクス、設計パターン検出を統一実装します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

import os
import re
import ast
import json
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

from .config import IntegratedConfig


class AnalysisType(Enum):
    """解析タイプ"""
    DEPENDENCY = "dependency"
    QUALITY = "quality"
    PATTERN = "pattern"
    COMPLEXITY = "complexity"
    SECURITY = "security"


class FindingLevel(Enum):
    """発見レベル"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AnalysisContext:
    """解析コンテキスト"""
    target_path: str
    analysis_type: AnalysisType
    parameters: Dict[str, Any] = field(default_factory=dict)
    output_format: str = "json"


@dataclass
class Finding:
    """解析結果の発見事項"""
    level: FindingLevel
    category: str
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    suggestion: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnalysisResult:
    """解析結果"""
    success: bool
    analysis_type: AnalysisType
    target_path: str
    findings: List[Finding] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    warnings: List[str] = field(default_factory=list)
    execution_time: float = 0.0


class BaseAnalyzer(ABC):
    """解析器基底クラス"""
    
    def __init__(self, config: IntegratedConfig):
        self.config = config
    
    @abstractmethod
    def analyze(self, context: AnalysisContext) -> AnalysisResult:
        """解析実行（抽象メソッド）"""
        pass
    
    def _create_finding(
        self,
        level: FindingLevel,
        category: str,
        message: str,
        **kwargs
    ) -> Finding:
        """発見事項を作成"""
        return Finding(
            level=level,
            category=category,
            message=message,
            **kwargs
        )


class DependencyAnalyzer(BaseAnalyzer):
    """依存関係解析器"""
    
    def analyze(self, context: AnalysisContext) -> AnalysisResult:
        """依存関係解析"""
        import time
        start_time = time.time()
        
        try:
            findings = []
            metrics = {}
            
            if os.path.isfile(context.target_path):
                # 単一ファイルの依存関係解析
                deps = self._analyze_file_dependencies(context.target_path)
                findings.extend(self._check_dependency_issues(deps, context.target_path))
                metrics['dependencies'] = deps
            
            elif os.path.isdir(context.target_path):
                # ディレクトリ全体の依存関係解析
                all_deps = {}
                for root, dirs, files in os.walk(context.target_path):
                    for file in files:
                        if self._is_analyzable_file(file):
                            file_path = os.path.join(root, file)
                            deps = self._analyze_file_dependencies(file_path)
                            all_deps[file_path] = deps
                            findings.extend(self._check_dependency_issues(deps, file_path))
                
                metrics['all_dependencies'] = all_deps
                metrics['dependency_graph'] = self._build_dependency_graph(all_deps)
                
                # 循環依存の検出
                cycles = self._detect_circular_dependencies(metrics['dependency_graph'])
                for cycle in cycles:
                    findings.append(self._create_finding(
                        level=FindingLevel.ERROR,
                        category="circular_dependency",
                        message=f"循環依存が検出されました: {' -> '.join(cycle)}",
                        suggestion="依存関係を見直して循環を解消してください"
                    ))
            
            # サマリーを作成
            summary = {
                'total_dependencies': len(metrics.get('dependencies', {})),
                'circular_dependencies': len([f for f in findings if f.category == 'circular_dependency']),
                'external_dependencies': len([d for d in metrics.get('dependencies', {}).get('external', [])]),
                'internal_dependencies': len([d for d in metrics.get('dependencies', {}).get('internal', [])])
            }
            
            return AnalysisResult(
                success=True,
                analysis_type=AnalysisType.DEPENDENCY,
                target_path=context.target_path,
                findings=findings,
                metrics=metrics,
                summary=summary,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                analysis_type=AnalysisType.DEPENDENCY,
                target_path=context.target_path,
                error_message=str(e),
                execution_time=time.time() - start_time
            )
    
    def _analyze_file_dependencies(self, file_path: str) -> Dict[str, List[str]]:
        """ファイルの依存関係を解析"""
        dependencies = {
            'imports': [],
            'external': [],
            'internal': []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # TypeScript/JavaScript のimport文を解析
            if file_path.endswith(('.ts', '.tsx', '.js', '.jsx')):
                dependencies.update(self._analyze_js_imports(content))
            
            # Python のimport文を解析
            elif file_path.endswith('.py'):
                dependencies.update(self._analyze_python_imports(content))
            
        except Exception:
            pass
        
        return dependencies
    
    def _analyze_js_imports(self, content: str) -> Dict[str, List[str]]:
        """JavaScript/TypeScript のimport文を解析"""
        imports = []
        external = []
        internal = []
        
        # import文のパターン
        import_patterns = [
            r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
            r"import\s+['\"]([^'\"]+)['\"]",
            r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                imports.append(match)
                
                # 外部依存か内部依存かを判定
                if match.startswith('.') or match.startswith('/'):
                    internal.append(match)
                else:
                    external.append(match)
        
        return {
            'imports': imports,
            'external': external,
            'internal': internal
        }
    
    def _analyze_python_imports(self, content: str) -> Dict[str, List[str]]:
        """Python のimport文を解析"""
        imports = []
        external = []
        internal = []
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                        if '.' in alias.name:
                            internal.append(alias.name)
                        else:
                            external.append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
                        if node.module.startswith('.'):
                            internal.append(node.module)
                        else:
                            external.append(node.module)
        
        except Exception:
            pass
        
        return {
            'imports': imports,
            'external': external,
            'internal': internal
        }
    
    def _check_dependency_issues(self, dependencies: Dict[str, List[str]], file_path: str) -> List[Finding]:
        """依存関係の問題をチェック"""
        findings = []
        
        # 外部依存が多すぎる場合
        external_count = len(dependencies.get('external', []))
        if external_count > 10:
            findings.append(self._create_finding(
                level=FindingLevel.WARNING,
                category="too_many_external_deps",
                message=f"外部依存が多すぎます: {external_count}個",
                file_path=file_path,
                suggestion="依存関係を整理し、必要最小限に抑えてください"
            ))
        
        # 未使用の可能性がある依存関係
        for dep in dependencies.get('imports', []):
            if dep.startswith('@types/'):
                continue  # 型定義は除外
            
            # 簡易的な使用チェック（実際のファイル内容を確認）
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # import文以外でモジュール名が使用されているかチェック
                module_name = dep.split('/')[-1]  # パッケージ名の最後の部分
                if module_name not in content.replace(f"from '{dep}'", "").replace(f'from "{dep}"', ""):
                    findings.append(self._create_finding(
                        level=FindingLevel.INFO,
                        category="potentially_unused_import",
                        message=f"未使用の可能性があるimport: {dep}",
                        file_path=file_path,
                        suggestion="使用されていない場合は削除を検討してください"
                    ))
            
            except Exception:
                pass
        
        return findings
    
    def _build_dependency_graph(self, all_deps: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
        """依存関係グラフを構築"""
        graph = {}
        
        for file_path, deps in all_deps.items():
            graph[file_path] = []
            
            for internal_dep in deps.get('internal', []):
                # 相対パスを絶対パスに変換
                if internal_dep.startswith('.'):
                    base_dir = os.path.dirname(file_path)
                    resolved_path = os.path.normpath(os.path.join(base_dir, internal_dep))
                    
                    # 実際のファイルパスを探す
                    for candidate in all_deps.keys():
                        if candidate.startswith(resolved_path):
                            graph[file_path].append(candidate)
                            break
        
        return graph
    
    def _detect_circular_dependencies(self, graph: Dict[str, List[str]]) -> List[List[str]]:
        """循環依存を検出"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(node: str, path: List[str]) -> bool:
            if node in rec_stack:
                # 循環を発見
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return True
            
            if node in visited:
                return False
            
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in graph.get(node, []):
                if dfs(neighbor, path + [neighbor]):
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in graph:
            if node not in visited:
                dfs(node, [node])
        
        return cycles
    
    def _is_analyzable_file(self, filename: str) -> bool:
        """解析対象ファイルかどうかを判定"""
        analyzable_extensions = {'.ts', '.tsx', '.js', '.jsx', '.py'}
        return any(filename.endswith(ext) for ext in analyzable_extensions)


class QualityAnalyzer(BaseAnalyzer):
    """品質解析器"""
    
    def analyze(self, context: AnalysisContext) -> AnalysisResult:
        """品質解析"""
        import time
        start_time = time.time()
        
        try:
            findings = []
            metrics = {}
            
            if os.path.isfile(context.target_path):
                file_metrics = self._analyze_file_quality(context.target_path)
                findings.extend(self._check_quality_issues(file_metrics, context.target_path))
                metrics[context.target_path] = file_metrics
            
            elif os.path.isdir(context.target_path):
                all_metrics = {}
                for root, dirs, files in os.walk(context.target_path):
                    for file in files:
                        if self._is_analyzable_file(file):
                            file_path = os.path.join(root, file)
                            file_metrics = self._analyze_file_quality(file_path)
                            findings.extend(self._check_quality_issues(file_metrics, file_path))
                            all_metrics[file_path] = file_metrics
                
                metrics = all_metrics
                
                # 全体的な品質メトリクスを計算
                overall_metrics = self._calculate_overall_metrics(all_metrics)
                metrics['overall'] = overall_metrics
            
            # サマリーを作成
            summary = self._create_quality_summary(metrics, findings)
            
            return AnalysisResult(
                success=True,
                analysis_type=AnalysisType.QUALITY,
                target_path=context.target_path,
                findings=findings,
                metrics=metrics,
                summary=summary,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return AnalysisResult(
                success=False,
                analysis_type=AnalysisType.QUALITY,
                target_path=context.target_path,
                error_message=str(e),
                execution_time=time.time() - start_time
            )
    
    def _analyze_file_quality(self, file_path: str) -> Dict[str, Any]:
        """ファイルの品質メトリクスを解析"""
        metrics = {
            'lines_of_code': 0,
            'comment_lines': 0,
            'blank_lines': 0,
            'function_count': 0,
            'class_count': 0,
            'complexity_score': 0,
            'comment_ratio': 0.0,
            'average_function_length': 0.0
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 基本的なメトリクスを計算
            metrics['lines_of_code'] = len([line for line in lines if line.strip()])
            metrics['blank_lines'] = len([line for line in lines if not line.strip()])
            
            # コメント行を計算
            comment_patterns = [r'^\s*//', r'^\s*#', r'^\s*/\*', r'^\s*\*']
            for line in lines:
                if any(re.match(pattern, line) for pattern in comment_patterns):
                    metrics['comment_lines'] += 1
            
            # コメント比率を計算
            if metrics['lines_of_code'] > 0:
                metrics['comment_ratio'] = metrics['comment_lines'] / metrics['lines_of_code']
            
            # 関数・クラス数を計算
            content = ''.join(lines)
            
            if file_path.endswith(('.ts', '.tsx', '.js', '.jsx')):
                metrics.update(self._analyze_js_quality(content))
            elif file_path.endswith('.py'):
                metrics.update(self._analyze_python_quality(content))
            
        except Exception:
            pass
        
        return metrics
    
    def _analyze_js_quality(self, content: str) -> Dict[str, Any]:
        """JavaScript/TypeScript の品質メトリクス"""
        metrics = {}
        
        # 関数数を計算
        function_patterns = [
            r'function\s+\w+',
            r'const\s+\w+\s*=\s*\([^)]*\)\s*=>',
            r'\w+\s*:\s*\([^)]*\)\s*=>'
        ]
        
        function_count = 0
        for pattern in function_patterns:
            function_count += len(re.findall(pattern, content))
        
        metrics['function_count'] = function_count
        
        # クラス数を計算
        class_count = len(re.findall(r'class\s+\w+', content))
        metrics['class_count'] = class_count
        
        # 複雑度スコアを計算（簡易版）
        complexity_keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'catch', '&&', '||']
        complexity_score = sum(content.count(keyword) for keyword in complexity_keywords)
        metrics['complexity_score'] = complexity_score
        
        return metrics
    
    def _analyze_python_quality(self, content: str) -> Dict[str, Any]:
        """Python の品質メトリクス"""
        metrics = {}
        
        try:
            tree = ast.parse(content)
            
            function_count = 0
            class_count = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    function_count += 1
                elif isinstance(node, ast.ClassDef):
                    class_count += 1
            
            metrics['function_count'] = function_count
            metrics['class_count'] = class_count
            
            # 複雑度スコア（簡易版）
            complexity_score = 0
            for node in ast.walk(tree):
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)):
                    complexity_score += 1
            
            metrics['complexity_score'] = complexity_score
            
        except Exception:
            pass
        
        return metrics
    
    def _check_quality_issues(self, metrics: Dict[str, Any], file_path: str) -> List[Finding]:
        """品質問題をチェック"""
        findings = []
        
        # コメント比率が低い
        if metrics.get('comment_ratio', 0) < 0.1:
            findings.append(self._create_finding(
                level=FindingLevel.WARNING,
                category="low_comment_ratio",
                message=f"コメント比率が低いです: {metrics.get('comment_ratio', 0):.1%}",
                file_path=file_path,
                suggestion="適切なコメントを追加してください"
            ))
        
        # ファイルが長すぎる
        if metrics.get('lines_of_code', 0) > 500:
            findings.append(self._create_finding(
                level=FindingLevel.WARNING,
                category="long_file",
                message=f"ファイルが長すぎます: {metrics.get('lines_of_code', 0)}行",
                file_path=file_path,
                suggestion="ファイルを分割することを検討してください"
            ))
        
        # 複雑度が高い
        if metrics.get('complexity_score', 0) > 20:
            findings.append(self._create_finding(
                level=FindingLevel.WARNING,
                category="high_complexity",
                message=f"複雑度が高いです: {metrics.get('complexity_score', 0)}",
                file_path=file_path,
                suggestion="コードの簡素化を検討してください"
            ))
        
        return findings
    
    def _calculate_overall_metrics(self, all_metrics: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """全体的な品質メトリクスを計算"""
        if not all_metrics:
            return {}
        
        total_loc = sum(metrics.get('lines_of_code', 0) for metrics in all_metrics.values())
        total_comments = sum(metrics.get('comment_lines', 0) for metrics in all_metrics.values())
        total_functions = sum(metrics.get('function_count', 0) for metrics in all_metrics.values())
        total_classes = sum(metrics.get('class_count', 0) for metrics in all_metrics.values())
        
        avg_complexity = sum(metrics.get('complexity_score', 0) for metrics in all_metrics.values()) / len(all_metrics)
        avg_comment_ratio = sum(metrics.get('comment_ratio', 0) for metrics in all_metrics.values()) / len(all_metrics)
        
        return {
            'total_files': len(all_metrics),
            'total_lines_of_code': total_loc,
            'total_comment_lines': total_comments,
            'total_functions': total_functions,
            'total_classes': total_classes,
            'average_complexity': avg_complexity,
            'average_comment_ratio': avg_comment_ratio,
            'overall_comment_ratio': total_comments / total_loc if total_loc > 0 else 0
        }
    
    def _create_quality_summary(self, metrics: Dict[str, Any], findings: List[Finding]) -> Dict[str, Any]:
        """品質サマリーを作成"""
        error_count = len([f for f in findings if f.level == FindingLevel.ERROR])
        warning_count = len([f for f in findings if f.level == FindingLevel.WARNING])
        
        # 品質スコアを計算（0-100）
        quality_score = max(0, 100 - (error_count * 20 + warning_count * 5))
        
        return {
            'quality_score': quality_score,
            'error_count': error_count,
            'warning_count': warning_count,
            'total_issues': len(findings),
            'metrics_summary': metrics.get('overall', {})
        }
    
    def _is_analyzable_file(self, filename: str) -> bool:
        """解析対象ファイルかどうかを判定"""
        analyzable_extensions = {'.ts', '.tsx', '.js', '.jsx', '.py'}
        return any(filename.endswith(ext) for ext in analyzable_extensions)


class AnalysisEngine:
    """統一解析エンジン"""
    
    def __init__(self, config: IntegratedConfig):
        self.config = config
        self.analyzers = {
            AnalysisType.DEPENDENCY: DependencyAnalyzer(config),
            AnalysisType.QUALITY: QualityAnalyzer(config)
        }
    
    def analyze(self, context: AnalysisContext) -> AnalysisResult:
        """解析実行"""
        if context.analysis_type not in self.analyzers:
            return AnalysisResult(
                success=False,
                analysis_type=context.analysis_type,
                target_path=context.target_path,
                error_message=f"サポートされていない解析タイプ: {context.analysis_type}"
            )
        
        analyzer = self.analyzers[context.analysis_type]
        return analyzer.analyze(context)
    
    def register_custom_analyzer(self, analysis_type: AnalysisType, analyzer: BaseAnalyzer):
        """カスタム解析器を登録"""
        self.analyzers[analysis_type] = analyzer
    
    def get_available_analyzers(self) -> List[AnalysisType]:
        """利用可能な解析器一覧を取得"""
        return list(self.analyzers.keys())
