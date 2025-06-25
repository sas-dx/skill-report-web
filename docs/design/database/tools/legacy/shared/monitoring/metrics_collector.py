"""
メトリクス収集システム
パフォーマンス監視とメトリクス収集

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict, deque
import json
import statistics

from ..core.logger import get_logger
from ..core.config import get_config

logger = get_logger(__name__)


@dataclass
class MetricPoint:
    """メトリクスポイント"""
    timestamp: datetime
    value: float
    tags: Dict[str, str] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            'timestamp': self.timestamp.isoformat(),
            'value': self.value,
            'tags': self.tags
        }


@dataclass
class MetricSummary:
    """メトリクス集計"""
    count: int = 0
    sum: float = 0.0
    min: float = float('inf')
    max: float = float('-inf')
    avg: float = 0.0
    p50: float = 0.0
    p95: float = 0.0
    p99: float = 0.0
    
    def update(self, value: float):
        """値を更新"""
        self.count += 1
        self.sum += value
        self.min = min(self.min, value)
        self.max = max(self.max, value)
        self.avg = self.sum / self.count
    
    def calculate_percentiles(self, values: List[float]):
        """パーセンタイル計算"""
        if not values:
            return
        
        sorted_values = sorted(values)
        self.p50 = statistics.median(sorted_values)
        
        if len(sorted_values) >= 20:  # 十分なデータがある場合のみ
            self.p95 = statistics.quantiles(sorted_values, n=20)[18]  # 95th percentile
            self.p99 = statistics.quantiles(sorted_values, n=100)[98]  # 99th percentile


class MetricsCollector:
    """メトリクス収集器"""
    
    def __init__(self, max_points: int = 10000, retention_hours: int = 24):
        """
        メトリクス収集器初期化
        
        Args:
            max_points: 最大保持ポイント数
            retention_hours: 保持時間（時間）
        """
        self.max_points = max_points
        self.retention_hours = retention_hours
        
        # メトリクスデータ
        self._metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_points))
        self._lock = threading.RLock()
        
        # 集計データ
        self._summaries: Dict[str, MetricSummary] = defaultdict(MetricSummary)
        
        # クリーンアップタイマー
        self._cleanup_timer = None
        self._start_cleanup_timer()
        
        logger.info(f"メトリクス収集器初期化: max_points={max_points}, retention={retention_hours}h")
    
    def record(
        self, 
        metric_name: str, 
        value: float, 
        tags: Optional[Dict[str, str]] = None
    ):
        """
        メトリクスを記録
        
        Args:
            metric_name: メトリクス名
            value: 値
            tags: タグ
        """
        with self._lock:
            point = MetricPoint(
                timestamp=datetime.now(),
                value=value,
                tags=tags or {}
            )
            
            self._metrics[metric_name].append(point)
            self._summaries[metric_name].update(value)
    
    def record_timing(self, metric_name: str, duration: float, tags: Optional[Dict[str, str]] = None):
        """タイミングメトリクスを記録"""
        self.record(f"{metric_name}.duration", duration, tags)
    
    def record_counter(self, metric_name: str, increment: int = 1, tags: Optional[Dict[str, str]] = None):
        """カウンターメトリクスを記録"""
        self.record(f"{metric_name}.count", increment, tags)
    
    def record_gauge(self, metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """ゲージメトリクスを記録"""
        self.record(f"{metric_name}.gauge", value, tags)
    
    def get_metrics(self, metric_name: str) -> List[MetricPoint]:
        """メトリクス取得"""
        with self._lock:
            return list(self._metrics.get(metric_name, []))
    
    def get_summary(self, metric_name: str) -> MetricSummary:
        """メトリクス集計取得"""
        with self._lock:
            summary = self._summaries.get(metric_name, MetricSummary())
            
            # パーセンタイル計算
            if metric_name in self._metrics:
                values = [point.value for point in self._metrics[metric_name]]
                summary.calculate_percentiles(values)
            
            return summary
    
    def get_all_metrics(self) -> Dict[str, List[MetricPoint]]:
        """全メトリクス取得"""
        with self._lock:
            return {name: list(points) for name, points in self._metrics.items()}
    
    def get_all_summaries(self) -> Dict[str, MetricSummary]:
        """全メトリクス集計取得"""
        with self._lock:
            summaries = {}
            for name in self._metrics.keys():
                summaries[name] = self.get_summary(name)
            return summaries
    
    def clear_metrics(self, metric_name: Optional[str] = None):
        """メトリクスクリア"""
        with self._lock:
            if metric_name:
                if metric_name in self._metrics:
                    self._metrics[metric_name].clear()
                if metric_name in self._summaries:
                    self._summaries[metric_name] = MetricSummary()
            else:
                self._metrics.clear()
                self._summaries.clear()
    
    def _cleanup_old_metrics(self):
        """古いメトリクスのクリーンアップ"""
        cutoff_time = datetime.now() - timedelta(hours=self.retention_hours)
        
        with self._lock:
            for metric_name, points in self._metrics.items():
                # 古いポイントを削除
                while points and points[0].timestamp < cutoff_time:
                    points.popleft()
                
                # 集計を再計算
                if points:
                    summary = MetricSummary()
                    values = []
                    for point in points:
                        summary.update(point.value)
                        values.append(point.value)
                    summary.calculate_percentiles(values)
                    self._summaries[metric_name] = summary
                else:
                    self._summaries[metric_name] = MetricSummary()
    
    def _start_cleanup_timer(self):
        """クリーンアップタイマー開始"""
        def cleanup():
            try:
                self._cleanup_old_metrics()
            except Exception as e:
                logger.error(f"メトリクスクリーンアップエラー: {e}")
            finally:
                # 次回タイマー設定
                self._cleanup_timer = threading.Timer(3600, cleanup)  # 1時間間隔
                self._cleanup_timer.daemon = True
                self._cleanup_timer.start()
        
        cleanup()
    
    def export_to_json(self, file_path: Path):
        """JSON形式でエクスポート"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'metrics': {},
            'summaries': {}
        }
        
        with self._lock:
            # メトリクスデータ
            for name, points in self._metrics.items():
                data['metrics'][name] = [point.to_dict() for point in points]
            
            # 集計データ
            for name, summary in self._summaries.items():
                data['summaries'][name] = {
                    'count': summary.count,
                    'sum': summary.sum,
                    'min': summary.min if summary.min != float('inf') else 0,
                    'max': summary.max if summary.max != float('-inf') else 0,
                    'avg': summary.avg,
                    'p50': summary.p50,
                    'p95': summary.p95,
                    'p99': summary.p99
                }
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"メトリクスをエクスポート: {file_path}")
        except Exception as e:
            logger.error(f"メトリクスエクスポートエラー: {e}")
    
    def __del__(self):
        """デストラクタ"""
        if self._cleanup_timer:
            self._cleanup_timer.cancel()


class PerformanceMonitor:
    """パフォーマンス監視"""
    
    def __init__(self, collector: Optional[MetricsCollector] = None):
        """
        パフォーマンス監視初期化
        
        Args:
            collector: メトリクス収集器
        """
        self.collector = collector or MetricsCollector()
        self._active_timers: Dict[str, float] = {}
        self._lock = threading.RLock()
    
    def start_timer(self, operation: str) -> str:
        """タイマー開始"""
        timer_id = f"{operation}_{threading.current_thread().ident}_{time.time()}"
        
        with self._lock:
            self._active_timers[timer_id] = time.time()
        
        return timer_id
    
    def end_timer(self, timer_id: str, tags: Optional[Dict[str, str]] = None):
        """タイマー終了"""
        end_time = time.time()
        
        with self._lock:
            if timer_id in self._active_timers:
                start_time = self._active_timers.pop(timer_id)
                duration = end_time - start_time
                
                # 操作名を抽出
                operation = timer_id.split('_')[0]
                self.collector.record_timing(operation, duration, tags)
                
                return duration
        
        return None
    
    def time_operation(self, operation: str, tags: Optional[Dict[str, str]] = None):
        """操作タイミング測定デコレータ"""
        def decorator(func):
            def wrapper(*args, **kwargs):
                timer_id = self.start_timer(operation)
                try:
                    result = func(*args, **kwargs)
                    self.end_timer(timer_id, tags)
                    return result
                except Exception as e:
                    self.end_timer(timer_id, {**(tags or {}), 'error': str(e)})
                    raise
            return wrapper
        return decorator
    
    def record_file_operation(
        self, 
        operation: str, 
        file_path: Path, 
        duration: float,
        success: bool = True
    ):
        """ファイル操作メトリクス記録"""
        tags = {
            'operation': operation,
            'file_type': file_path.suffix,
            'success': str(success)
        }
        
        self.collector.record_timing(f"file.{operation}", duration, tags)
        self.collector.record_counter(f"file.{operation}.total", 1, tags)
        
        if not success:
            self.collector.record_counter(f"file.{operation}.errors", 1, tags)
    
    def record_validation_result(
        self, 
        validator: str, 
        file_path: Path, 
        duration: float,
        errors: int,
        warnings: int
    ):
        """バリデーション結果メトリクス記録"""
        tags = {
            'validator': validator,
            'file_type': file_path.suffix
        }
        
        self.collector.record_timing(f"validation.{validator}", duration, tags)
        self.collector.record_gauge(f"validation.{validator}.errors", errors, tags)
        self.collector.record_gauge(f"validation.{validator}.warnings", warnings, tags)
    
    def record_processing_stats(
        self, 
        operation: str, 
        total_files: int,
        processed_files: int,
        failed_files: int,
        total_duration: float
    ):
        """処理統計メトリクス記録"""
        tags = {'operation': operation}
        
        self.collector.record_gauge(f"processing.{operation}.total_files", total_files, tags)
        self.collector.record_gauge(f"processing.{operation}.processed_files", processed_files, tags)
        self.collector.record_gauge(f"processing.{operation}.failed_files", failed_files, tags)
        self.collector.record_timing(f"processing.{operation}.total_duration", total_duration, tags)
        
        # 成功率
        success_rate = (processed_files / total_files) * 100 if total_files > 0 else 0
        self.collector.record_gauge(f"processing.{operation}.success_rate", success_rate, tags)
        
        # スループット
        throughput = processed_files / total_duration if total_duration > 0 else 0
        self.collector.record_gauge(f"processing.{operation}.throughput", throughput, tags)


class SystemMonitor:
    """システム監視"""
    
    def __init__(self, collector: Optional[MetricsCollector] = None):
        """
        システム監視初期化
        
        Args:
            collector: メトリクス収集器
        """
        self.collector = collector or MetricsCollector()
        self._monitoring = False
        self._monitor_thread = None
    
    def start_monitoring(self, interval: int = 60):
        """システム監視開始"""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self._monitor_thread.start()
        
        logger.info(f"システム監視開始: interval={interval}s")
    
    def stop_monitoring(self):
        """システム監視停止"""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join(timeout=5)
        
        logger.info("システム監視停止")
    
    def _monitor_loop(self, interval: int):
        """監視ループ"""
        while self._monitoring:
            try:
                self._collect_system_metrics()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"システム監視エラー: {e}")
                time.sleep(interval)
    
    def _collect_system_metrics(self):
        """システムメトリクス収集"""
        import psutil
        import os
        
        try:
            # CPU使用率
            cpu_percent = psutil.cpu_percent(interval=1)
            self.collector.record_gauge("system.cpu.usage", cpu_percent)
            
            # メモリ使用率
            memory = psutil.virtual_memory()
            self.collector.record_gauge("system.memory.usage", memory.percent)
            self.collector.record_gauge("system.memory.available", memory.available)
            
            # ディスク使用率
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            self.collector.record_gauge("system.disk.usage", disk_percent)
            
            # プロセス情報
            process = psutil.Process(os.getpid())
            self.collector.record_gauge("process.memory.rss", process.memory_info().rss)
            self.collector.record_gauge("process.cpu.percent", process.cpu_percent())
            
        except Exception as e:
            logger.error(f"システムメトリクス収集エラー: {e}")


# グローバルインスタンス
_metrics_collector: Optional[MetricsCollector] = None
_performance_monitor: Optional[PerformanceMonitor] = None
_system_monitor: Optional[SystemMonitor] = None


def get_metrics_collector() -> MetricsCollector:
    """グローバルメトリクス収集器取得"""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


def get_performance_monitor() -> PerformanceMonitor:
    """グローバルパフォーマンス監視取得"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor(get_metrics_collector())
    return _performance_monitor


def get_system_monitor() -> SystemMonitor:
    """グローバルシステム監視取得"""
    global _system_monitor
    if _system_monitor is None:
        _system_monitor = SystemMonitor(get_metrics_collector())
    return _system_monitor


# 便利関数
def record_metric(metric_name: str, value: float, tags: Optional[Dict[str, str]] = None):
    """メトリクス記録"""
    get_metrics_collector().record(metric_name, value, tags)


def time_function(operation: str, tags: Optional[Dict[str, str]] = None):
    """関数実行時間測定デコレータ"""
    return get_performance_monitor().time_operation(operation, tags)


def start_system_monitoring(interval: int = 60):
    """システム監視開始"""
    get_system_monitor().start_monitoring(interval)


def export_metrics(file_path: Path):
    """メトリクスエクスポート"""
    get_metrics_collector().export_to_json(file_path)
