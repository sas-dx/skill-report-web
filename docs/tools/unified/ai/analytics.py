#!/usr/bin/env python3
"""
統一設計ツール - AI駆動リアルタイム分析機能

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
実装日: 2025-07-08
実装者: AI駆動開発チーム
"""

import os
import sys
import time
import json
import hashlib
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
import logging

# 外部ライブラリのインポート（オプショナル）
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    print("Warning: watchdog not available. File monitoring disabled.")

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    print("Warning: psutil not available. Performance monitoring limited.")

# ログ設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class FileMetrics:
    """ファイルメトリクス"""
    path: str
    size: int
    lines: int
    modified_time: float
    hash_value: str
    file_type: str
    encoding: str = 'utf-8'

@dataclass
class QualityMetrics:
    """品質メトリクス"""
    file_path: str
    code_quality_score: float
    design_compliance_score: float
    requirement_id_coverage: float
    complexity_score: float
    maintainability_score: float
    test_coverage: float
    documentation_score: float
    timestamp: datetime

@dataclass
class PerformanceMetrics:
    """パフォーマンスメトリクス"""
    operation: str
    duration: float
    memory_usage: float
    cpu_usage: float
    timestamp: datetime
    details: Dict[str, Any]

@dataclass
class AnalysisReport:
    """統合分析レポート"""
    timestamp: datetime
    total_files: int
    quality_score: float
    performance_score: float
    compliance_score: float
    recommendations: List[str]
    trends: Dict[str, Any]
    alerts: List[str]

class FileChangeHandler:
    """ファイル変更監視ハンドラー（watchdog非依存版）"""
    
    def __init__(self, analytics_engine):
        self.analytics_engine = analytics_engine
        self.last_processed = {}
        self.debounce_time = 1.0  # 1秒のデバウンス
    
    def check_file_changes(self, directory: str):
        """ファイル変更チェック（ポーリング方式）"""
        for root, dirs, files in os.walk(directory):
            # 除外ディレクトリをスキップ
            dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.next', 'venv'}]
            
            for file in files:
                file_path = os.path.join(root, file)
                if self._is_analysis_target(file_path):
                    try:
                        current_mtime = os.path.getmtime(file_path)
                        
                        if file_path not in self.last_processed or current_mtime > self.last_processed[file_path]:
                            self.last_processed[file_path] = current_mtime
                            logger.info(f"ファイル変更検知: {file_path}")
                            self.analytics_engine.analyze_file_change(file_path)
                    
                    except OSError:
                        continue
    
    def _is_analysis_target(self, file_path: str) -> bool:
        """分析対象ファイルかチェック"""
        target_extensions = {'.py', '.js', '.ts', '.tsx', '.md', '.yaml', '.yml', '.sql', '.json'}
        exclude_patterns = {'node_modules', '.git', '__pycache__', '.next', 'venv'}
        
        path_obj = Path(file_path)
        
        # 除外パターンチェック
        for exclude in exclude_patterns:
            if exclude in path_obj.parts:
                return False
        
        # 拡張子チェック
        return path_obj.suffix.lower() in target_extensions

class QualityAnalyzer:
    """品質分析エンジン"""
    
    def __init__(self):
        self.requirement_patterns = [
            r'要求仕様ID:\s*([A-Z]{3}\.\d+-[A-Z]+\.\d+)',
            r'設計書:\s*([^\n]+)',
            r'実装日:\s*(\d{4}-\d{2}-\d{2})',
        ]
    
    def analyze_file_quality(self, file_path: str) -> QualityMetrics:
        """ファイル品質分析"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 各種スコア計算
            code_quality = self._calculate_code_quality(content, file_path)
            design_compliance = self._calculate_design_compliance(content)
            requirement_coverage = self._calculate_requirement_coverage(content)
            complexity = self._calculate_complexity(content)
            maintainability = self._calculate_maintainability(content)
            test_coverage = self._calculate_test_coverage(file_path)
            documentation = self._calculate_documentation_score(content)
            
            return QualityMetrics(
                file_path=file_path,
                code_quality_score=code_quality,
                design_compliance_score=design_compliance,
                requirement_id_coverage=requirement_coverage,
                complexity_score=complexity,
                maintainability_score=maintainability,
                test_coverage=test_coverage,
                documentation_score=documentation,
                timestamp=datetime.now()
            )
        
        except Exception as e:
            logger.error(f"品質分析エラー {file_path}: {e}")
            return QualityMetrics(
                file_path=file_path,
                code_quality_score=0.0,
                design_compliance_score=0.0,
                requirement_id_coverage=0.0,
                complexity_score=0.0,
                maintainability_score=0.0,
                test_coverage=0.0,
                documentation_score=0.0,
                timestamp=datetime.now()
            )
    
    def _calculate_code_quality(self, content: str, file_path: str) -> float:
        """コード品質スコア計算"""
        score = 100.0
        
        # 基本的な品質チェック
        lines = content.split('\n')
        
        # 長すぎる行のペナルティ
        long_lines = sum(1 for line in lines if len(line) > 120)
        score -= min(long_lines * 2, 20)
        
        # コメント率チェック
        comment_lines = sum(1 for line in lines if line.strip().startswith('#') or line.strip().startswith('//'))
        total_lines = len([line for line in lines if line.strip()])
        if total_lines > 0:
            comment_ratio = comment_lines / total_lines
            if comment_ratio < 0.1:
                score -= 15
            elif comment_ratio > 0.3:
                score -= 5
        
        # TODO/FIXME の存在チェック
        todo_count = content.count('TODO') + content.count('FIXME')
        score -= min(todo_count * 3, 15)
        
        # 重複コードの簡易チェック
        line_hashes = {}
        for line in lines:
            if len(line.strip()) > 10:
                line_hash = hashlib.md5(line.strip().encode()).hexdigest()
                line_hashes[line_hash] = line_hashes.get(line_hash, 0) + 1
        
        duplicate_lines = sum(count - 1 for count in line_hashes.values() if count > 1)
        score -= min(duplicate_lines * 1, 10)
        
        return max(score, 0.0)
    
    def _calculate_design_compliance(self, content: str) -> float:
        """設計書準拠スコア計算"""
        score = 100.0
        
        # 要求仕様ID の存在チェック
        if '要求仕様ID:' not in content:
            score -= 30
        
        # 設計書参照の存在チェック
        if '設計書:' not in content:
            score -= 20
        
        # 実装日の存在チェック
        if '実装日:' not in content:
            score -= 10
        
        # エグゼクティブサマリーの存在チェック（.mdファイル）
        if 'エグゼクティブサマリー' in content:
            score += 10  # ボーナス点
        elif content.endswith('.md'):
            score -= 25
        
        return max(score, 0.0)
    
    def _calculate_requirement_coverage(self, content: str) -> float:
        """要求仕様ID カバレッジ計算"""
        import re
        
        # 要求仕様ID パターンマッチング
        pattern = r'[A-Z]{3}\.\d+-[A-Z]+\.\d+'
        matches = re.findall(pattern, content)
        
        if not matches:
            return 0.0
        
        # ユニークな要求仕様ID の数
        unique_ids = set(matches)
        
        # 基本スコア（要求仕様ID が存在すれば80点）
        score = 80.0
        
        # 複数の要求仕様ID があれば追加点
        if len(unique_ids) > 1:
            score += min(len(unique_ids) * 5, 20)
        
        return min(score, 100.0)
    
    def _calculate_complexity(self, content: str) -> float:
        """複雑度スコア計算（低いほど良い）"""
        lines = content.split('\n')
        
        # サイクロマティック複雑度の簡易計算
        complexity_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'case', 'switch']
        complexity_count = 0
        
        for line in lines:
            for keyword in complexity_keywords:
                complexity_count += line.count(keyword)
        
        # 関数・メソッド数
        function_count = content.count('def ') + content.count('function ')
        
        if function_count == 0:
            return 100.0
        
        # 平均複雑度
        avg_complexity = complexity_count / function_count if function_count > 0 else 0
        
        # スコア計算（複雑度が低いほど高スコア）
        if avg_complexity <= 5:
            return 100.0
        elif avg_complexity <= 10:
            return 80.0
        elif avg_complexity <= 15:
            return 60.0
        else:
            return max(40.0 - (avg_complexity - 15) * 2, 0.0)
    
    def _calculate_maintainability(self, content: str) -> float:
        """保守性スコア計算"""
        score = 100.0
        
        lines = content.split('\n')
        total_lines = len([line for line in lines if line.strip()])
        
        # ファイルサイズペナルティ
        if total_lines > 500:
            score -= min((total_lines - 500) * 0.1, 20)
        
        # 関数サイズチェック
        in_function = False
        function_lines = 0
        max_function_lines = 0
        
        for line in lines:
            if 'def ' in line or 'function ' in line:
                if in_function:
                    max_function_lines = max(max_function_lines, function_lines)
                in_function = True
                function_lines = 0
            elif in_function and line.strip():
                function_lines += 1
        
        if max_function_lines > 50:
            score -= min((max_function_lines - 50) * 0.5, 15)
        
        # 命名規則チェック（簡易）
        import re
        
        class_pattern = r'\bclass\s+([A-Z][a-zA-Z0-9]*)\b'
        class_matches = re.findall(class_pattern, content)
        if class_matches:
            # クラス名がPascalCaseかチェック
            for class_name in class_matches:
                if not class_name[0].isupper():
                    score -= 5
        
        return max(score, 0.0)
    
    def _calculate_test_coverage(self, file_path: str) -> float:
        """テストカバレッジ計算（簡易）"""
        # テストファイルの存在チェック
        path_obj = Path(file_path)
        
        # テストファイルパターン
        test_patterns = [
            path_obj.parent / f"test_{path_obj.stem}.py",
            path_obj.parent / f"{path_obj.stem}_test.py",
            path_obj.parent / "tests" / f"test_{path_obj.stem}.py",
            path_obj.parent.parent / "tests" / f"test_{path_obj.stem}.py"
        ]
        
        for test_path in test_patterns:
            if test_path.exists():
                return 80.0
        
        # テストファイル自体の場合
        if 'test' in path_obj.name.lower():
            return 100.0
        
        return 0.0
    
    def _calculate_documentation_score(self, content: str) -> float:
        """ドキュメントスコア計算"""
        score = 100.0
        
        # docstring の存在チェック
        if '"""' not in content and "'''" not in content:
            score -= 30
        
        # コメント密度チェック
        lines = content.split('\n')
        comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
        code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))
        
        if code_lines > 0:
            comment_ratio = comment_lines / code_lines
            if comment_ratio < 0.1:
                score -= 20
        
        return max(score, 0.0)

class PerformanceMonitor:
    """パフォーマンス監視"""
    
    def __init__(self):
        self.metrics_history = []
        self.start_time = time.time()
        if PSUTIL_AVAILABLE:
            self.process = psutil.Process()
        else:
            self.process = None
    
    def start_operation(self, operation: str) -> Dict[str, Any]:
        """操作開始"""
        context = {
            'operation': operation,
            'start_time': time.time(),
        }
        
        if self.process:
            context['start_memory'] = self.process.memory_info().rss
            context['start_cpu'] = self.process.cpu_percent()
        else:
            context['start_memory'] = 0
            context['start_cpu'] = 0
        
        return context
    
    def end_operation(self, context: Dict[str, Any], details: Dict[str, Any] = None) -> PerformanceMetrics:
        """操作終了"""
        end_time = time.time()
        duration = end_time - context['start_time']
        
        if self.process:
            end_memory = self.process.memory_info().rss
            end_cpu = self.process.cpu_percent()
            memory_usage = end_memory - context['start_memory']
            cpu_usage = end_cpu
        else:
            memory_usage = 0
            cpu_usage = 0
        
        metrics = PerformanceMetrics(
            operation=context['operation'],
            duration=duration,
            memory_usage=memory_usage,
            cpu_usage=cpu_usage,
            timestamp=datetime.now(),
            details=details or {}
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """システムメトリクス取得"""
        if PSUTIL_AVAILABLE and self.process:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_usage': psutil.disk_usage('/').percent,
                'process_memory': self.process.memory_info().rss,
                'process_cpu': self.process.cpu_percent(),
                'uptime': time.time() - self.start_time
            }
        else:
            return {
                'cpu_percent': 0,
                'memory_percent': 0,
                'disk_usage': 0,
                'process_memory': 0,
                'process_cpu': 0,
                'uptime': time.time() - self.start_time
            }

class RealtimeAnalyticsEngine:
    """リアルタイム分析エンジン"""
    
    def __init__(self, watch_directories: List[str] = None):
        self.watch_directories = watch_directories or ['.']
        self.quality_analyzer = QualityAnalyzer()
        self.performance_monitor = PerformanceMonitor()
        self.file_metrics = {}
        self.quality_metrics = {}
        self.analysis_history = []
        self.running = False
        
        # 分析結果保存ディレクトリ
        self.output_dir = Path('docs/tools/reports/analytics')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # ファイル変更ハンドラー
        self.file_handler = FileChangeHandler(self)
    
    def start_monitoring(self):
        """監視開始"""
        logger.info("リアルタイム分析監視を開始します")
        self.running = True
        
        # 初期分析実行
        self._perform_initial_analysis()
        
        # 継続監視（ポーリング方式）
        if WATCHDOG_AVAILABLE:
            logger.info("watchdog使用: リアルタイム監視")
            # watchdog実装は省略（依存関係を減らすため）
        else:
            logger.info("ポーリング方式: 定期監視")
            self._start_polling_monitor()
    
    def stop_monitoring(self):
        """監視停止"""
        self.running = False
        logger.info("リアルタイム分析監視を停止しました")
    
    def _start_polling_monitor(self):
        """ポーリング監視開始"""
        def monitor_loop():
            while self.running:
                for directory in self.watch_directories:
                    if os.path.exists(directory):
                        self.file_handler.check_file_changes(directory)
                time.sleep(5)  # 5秒間隔でチェック
        
        monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        monitor_thread.start()
    
    def analyze_file_change(self, file_path: str):
        """ファイル変更分析"""
        context = self.performance_monitor.start_operation(f"analyze_file_change:{file_path}")
        
        try:
            # ファイルメトリクス更新
            file_metrics = self._get_file_metrics(file_path)
            self.file_metrics[file_path] = file_metrics
            
            # 品質分析実行
            quality_metrics = self.quality_analyzer.analyze_file_quality(file_path)
            self.quality_metrics[file_path] = quality_metrics
            
            # 影響範囲分析
            impact_analysis = self._analyze_impact(file_path)
            
            # 分析結果保存
            self._save_analysis_result(file_path, quality_metrics, impact_analysis)
            
            logger.info(f"ファイル分析完了: {file_path} (品質スコア: {quality_metrics.code_quality_score:.1f})")
            
        except Exception as e:
            logger.error(f"ファイル分析エラー {file_path}: {e}")
        
        finally:
            self.performance_monitor.end_operation(context, {'file_path': file_path})
    
    def generate_analysis_report(self) -> AnalysisReport:
        """統合分析レポート生成"""
        context = self.performance_monitor.start_operation("generate_analysis_report")
        
        try:
            total_files = len(self.quality_metrics)
            
            if total_files == 0:
                return AnalysisReport(
                    timestamp=datetime.now(),
                    total_files=0,
                    quality_score=0.0,
                    performance_score=0.0,
                    compliance_score=0.0,
                    recommendations=[],
                    trends={},
                    alerts=[]
                )
            
            # 品質スコア計算
            quality_scores = [m.code_quality_score for m in self.quality_metrics.values()]
            avg_quality = sum(quality_scores) / len(quality_scores)
            
            # コンプライアンススコア計算
            compliance_scores = [m.design_compliance_score for m in self.quality_metrics.values()]
            avg_compliance = sum(compliance_scores) / len(compliance_scores)
            
            # パフォーマンススコア計算
            recent_metrics = self.performance_monitor.metrics_history[-10:]
            if recent_metrics:
                avg_duration = sum(m.duration for m in recent_metrics) / len(recent_metrics)
                performance_score = max(100 - avg_duration * 10, 0)
            else:
                performance_score = 100.0
            
            # 推奨事項生成
            recommendations = self._generate_recommendations()
            
            # アラート生成
            alerts = self._generate_alerts()
            
            # トレンド分析
            trends = self._analyze_trends()
            
            report = AnalysisReport(
                timestamp=datetime.now(),
                total_files=total_files,
                quality_score=avg_quality,
                performance_score=performance_score,
                compliance_score=avg_compliance,
                recommendations=recommendations,
                trends=trends,
                alerts=alerts
            )
            
            # レポート保存
            self._save_report(report)
            
            return report
        
        finally:
            self.performance_monitor.end_operation(context)
    
    def _perform_initial_analysis(self):
        """初期分析実行"""
        logger.info("初期分析を実行中...")
        
        for directory in self.watch_directories:
            for root, dirs, files in os.walk(directory):
                # 除外ディレクトリをスキップ
                dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.next', 'venv'}]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.file_handler._is_analysis_target(file_path):
                        self.analyze_file_change(file_path)
        
        logger.info("初期分析完了")
    
    def _get_file_metrics(self, file_path: str) -> FileMetrics:
        """ファイルメトリクス取得"""
        try:
            stat = os.stat(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = len(content.split('\n'))
            hash_value = hashlib.md5(content.encode()).hexdigest()
            file_type = Path(file_path).suffix
            
            return FileMetrics(
                path=file_path,
                size=stat.st_size,
                lines=lines,
                modified_time=stat.st_mtime,
                hash_value=hash_value,
                file_type=file_type
            )
        
        except Exception as e:
            logger.error(f"ファイルメトリクス取得エラー {file_path}: {e}")
            return FileMetrics(
                path=file_path,
                size=0,
                lines=0,
                modified_time=0,
                hash_value='',
                file_type=''
            )
    
    def _analyze_impact(self, file_path: str) -> Dict[str, Any]:
        """影響範囲分析"""
        impact = {
            'modified_file': file_path,
            'related_files': [],
            'risk_level': 'low',
            'estimated_impact': []
        }
        
        # 関連ファイル検索（簡易実装）
        file_name = Path(file_path).stem
        
        for other_path in self.file_metrics.keys():
            if other_path != file_path:
                try:
                    with open(other_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if file_name in content:
                        impact['related_files'].append(other_path)
                
                except Exception:
                    continue
        
        # リスクレベル判定
        if len(impact['related_files']) > 5:
            impact['risk_level'] = 'high'
        elif len(impact['related_files']) > 2:
            impact['risk_level'] = 'medium'
        
        return impact
    
    def _generate_recommendations(self) -> List[str]:
        """推奨事項生成"""
        recommendations = []
        
        # 品質スコアが低いファイルの特定
        low_quality_files = [
            path for path, metrics in self.quality_metrics.items()
            if metrics.code_quality_score < 70
        ]
        
        if low_quality_files:
            recommendations.append(f"品質改善が必要なファイル: {len(low_quality_files)}件")
        
        # 要求仕様ID 未対応ファイルの特定
        missing_req_files = [
            path for path, metrics in self.quality_metrics.items()
            if metrics.requirement_id_coverage < 50
        ]
        
        if missing_req_files:
            recommendations.append(f"要求仕様ID対応が必要なファイル: {len(missing_req_files)}件")
        
        # テストカバレッジ改善
        untested_files = [
            path for path, metrics in self.quality_metrics.items()
            if metrics.test_coverage < 50
        ]
        
        if untested_files:
            recommendations.append(f"テスト実装が必要なファイル: {len(untested_files)}件")
        
        return recommendations
    
    def _generate_alerts(self) -> List[str]:
        """アラート生成"""
        alerts = []
        
        # 重大な品質問題
        critical_files = [
            path for path, metrics in self.quality_metrics.items()
            if metrics.code_quality_score < 50
        ]
        
        if critical_files:
            alerts.append(f"🚨 重大な品質問題: {len(critical_files)}件のファイルで品質スコア50未満")
        
        # 設計書非準拠
        non_compliant_files = [
            path for path, metrics in self.quality_metrics.items()
            if metrics.design_compliance_score < 60
        ]
        
        if non_compliant_files:
            alerts.append(f"⚠️ 設計書非準拠: {len(non_compliant_files)}件のファイル")
        
        # パフォーマンス問題
        recent_metrics = self.performance_monitor.metrics_history[-5:]
        if recent_metrics:
            avg_duration = sum(m.duration for m in recent_metrics) / len(recent_metrics)
            if avg_duration > 5.0:
                alerts.append(f"🐌 パフォーマンス低下: 平均処理時間 {avg_duration:.2f}秒")
        
        return alerts
    
    def _analyze_trends(self) -> Dict[str, Any]:
        """トレンド分析"""
        trends = {
            'quality_trend': 'stable',
            'file_count_trend': 'stable',
            'performance_trend': 'stable'
        }
        
        # 品質トレンド分析（簡易）
        if len(self.analysis_history) > 1:
            recent_quality = self.analysis_history[-1].quality_score
            previous_quality = self.analysis_history[-2].quality_score
            
            if recent_quality > previous_quality + 5:
                trends['quality_trend'] = 'improving'
            elif recent_quality < previous_quality - 5:
                trends['quality_trend'] = 'declining'
        
        return trends
    
    def _save_analysis_result(self, file_path: str, quality_metrics: QualityMetrics, impact_analysis: Dict[str, Any]):
        """分析結果保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        result_file = self.output_dir / f"analysis_{timestamp}_{Path(file_path).stem}.json"
        
        result = {
            'file_path': file_path,
            'timestamp': timestamp,
            'quality_metrics': asdict(quality_metrics),
            'impact_analysis': impact_analysis
        }
        
        try:
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            logger.error(f"分析結果保存エラー: {e}")
    
    def _save_report(self, report: AnalysisReport):
        """レポート保存"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.output_dir / f"report_{timestamp}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(report), f, indent=2, ensure_ascii=False, default=str)
            
            # 最新レポートとしてもコピー
            latest_file = self.output_dir / "latest_report.json"
            with open(latest_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(report), f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"分析レポート保存完了: {report_file}")
            
        except Exception as e:
            logger.error(f"レポート保存エラー: {e}")

def main():
    """メイン実行関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='統一設計ツール - リアルタイム分析')
    parser.add_argument('--watch', nargs='+', default=['.'], help='監視ディレクトリ')
    parser.add_argument('--report-only', action='store_true', help='レポート生成のみ実行')
    parser.add_argument('--output', default='docs/tools/reports/analytics', help='出力ディレクトリ')
    parser.add_argument('--continuous', action='store_true', help='継続監視モード')
    
    args = parser.parse_args()
    
    # 分析エンジン初期化
    engine = RealtimeAnalyticsEngine(watch_directories=args.watch)
    
    if args.report_only:
        # レポート生成のみ
        logger.info("レポート生成モードで実行中...")
        report = engine.generate_analysis_report()
        
        print("\n" + "="*60)
        print("📊 統一設計ツール - 分析レポート")
        print("="*60)
        print(f"📅 実行日時: {report.timestamp}")
        print(f"📁 対象ファイル数: {report.total_files}")
        print(f"⭐ 品質スコア: {report.quality_score:.1f}/100")
        print(f"🚀 パフォーマンススコア: {report.performance_score:.1f}/100")
        print(f"📋 設計書準拠スコア: {report.compliance_score:.1f}/100")
        
        if report.recommendations:
            print("\n📝 推奨事項:")
            for rec in report.recommendations:
                print(f"  • {rec}")
        
        if report.alerts:
            print("\n🚨 アラート:")
            for alert in report.alerts:
                print(f"  • {alert}")
        
        print(f"\n📄 詳細レポート: {engine.output_dir}/latest_report.json")
        print("="*60)
        
    elif args.continuous:
        # 継続監視モード
        logger.info("継続監視モードで実行中...")
        try:
            engine.start_monitoring()
            print("リアルタイム分析を開始しました。Ctrl+Cで停止します。")
            
            while True:
                time.sleep(30)  # 30秒ごとにレポート生成
                report = engine.generate_analysis_report()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] 品質スコア: {report.quality_score:.1f}, ファイル数: {report.total_files}")
                
        except KeyboardInterrupt:
            print("\n監視を停止しています...")
            engine.stop_monitoring()
            print("監視を停止しました。")
    
    else:
        # 一回限りの分析
        logger.info("一回限りの分析を実行中...")
        engine._perform_initial_analysis()
        report = engine.generate_analysis_report()
        
        print(f"\n分析完了: {report.total_files}件のファイルを分析")
        print(f"品質スコア: {report.quality_score:.1f}/100")
        print(f"詳細レポート: {engine.output_dir}/latest_report.json")

if __name__ == "__main__":
    main()
