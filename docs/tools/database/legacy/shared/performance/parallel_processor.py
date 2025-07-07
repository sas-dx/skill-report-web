"""
並列処理エンジン
大量データ処理の高速化

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

import asyncio
import concurrent.futures
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional, Union, Tuple
from dataclasses import dataclass
import time
import threading
from queue import Queue, Empty
import multiprocessing as mp

from ..core.logger import get_logger
from ..core.exceptions import PerformanceError
from ..core.config import get_config

logger = get_logger(__name__)


@dataclass
class ProcessingResult:
    """処理結果"""
    success: bool
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    worker_id: Optional[str] = None


@dataclass
class ProcessingStats:
    """処理統計"""
    total_tasks: int = 0
    completed_tasks: int = 0
    failed_tasks: int = 0
    total_time: float = 0.0
    average_time: float = 0.0
    throughput: float = 0.0  # tasks per second


class ParallelProcessor:
    """並列処理エンジン"""
    
    def __init__(
        self, 
        max_workers: Optional[int] = None,
        use_async: bool = True,
        chunk_size: int = 100
    ):
        """
        並列処理エンジン初期化
        
        Args:
            max_workers: 最大ワーカー数
            use_async: 非同期処理使用フラグ
            chunk_size: チャンクサイズ
        """
        config = get_config()
        
        self.max_workers = max_workers or config.tool.max_workers
        self.use_async = use_async
        self.chunk_size = chunk_size
        self.stats = ProcessingStats()
        
        # CPUコア数の制限
        cpu_count = mp.cpu_count()
        if self.max_workers > cpu_count:
            logger.warning(f"ワーカー数をCPUコア数に制限: {self.max_workers} -> {cpu_count}")
            self.max_workers = cpu_count
        
        logger.info(f"並列処理エンジン初期化: workers={self.max_workers}, async={use_async}")
    
    async def process_async(
        self,
        tasks: List[Any],
        processor_func: Callable,
        progress_callback: Optional[Callable] = None
    ) -> List[ProcessingResult]:
        """
        非同期並列処理
        
        Args:
            tasks: 処理対象タスクリスト
            processor_func: 処理関数
            progress_callback: 進捗コールバック
            
        Returns:
            List[ProcessingResult]: 処理結果リスト
        """
        start_time = time.time()
        self.stats.total_tasks = len(tasks)
        
        logger.info(f"非同期並列処理開始: {len(tasks)}タスク")
        
        try:
            # セマフォで同時実行数を制限
            semaphore = asyncio.Semaphore(self.max_workers)
            
            async def process_task(task, task_id):
                async with semaphore:
                    task_start = time.time()
                    try:
                        # 同期関数を非同期で実行
                        loop = asyncio.get_event_loop()
                        result = await loop.run_in_executor(
                            None, processor_func, task
                        )
                        
                        execution_time = time.time() - task_start
                        
                        self.stats.completed_tasks += 1
                        
                        if progress_callback:
                            await asyncio.get_event_loop().run_in_executor(
                                None, progress_callback, self.stats.completed_tasks, self.stats.total_tasks
                            )
                        
                        return ProcessingResult(
                            success=True,
                            result=result,
                            execution_time=execution_time,
                            worker_id=f"async-{task_id}"
                        )
                        
                    except Exception as e:
                        execution_time = time.time() - task_start
                        self.stats.failed_tasks += 1
                        
                        logger.error(f"タスク処理エラー (ID: {task_id}): {e}")
                        
                        return ProcessingResult(
                            success=False,
                            error=str(e),
                            execution_time=execution_time,
                            worker_id=f"async-{task_id}"
                        )
            
            # 全タスクを並列実行
            results = await asyncio.gather(*[
                process_task(task, i) for i, task in enumerate(tasks)
            ])
            
            # 統計計算
            self.stats.total_time = time.time() - start_time
            self.stats.average_time = self.stats.total_time / len(tasks) if tasks else 0
            self.stats.throughput = len(tasks) / self.stats.total_time if self.stats.total_time > 0 else 0
            
            logger.info(f"非同期並列処理完了: {self.stats.completed_tasks}/{self.stats.total_tasks} 成功")
            return results
            
        except Exception as e:
            logger.error(f"非同期並列処理エラー: {e}")
            raise PerformanceError(f"並列処理失敗: {e}")
    
    def process_sync(
        self,
        tasks: List[Any],
        processor_func: Callable,
        progress_callback: Optional[Callable] = None
    ) -> List[ProcessingResult]:
        """
        同期並列処理
        
        Args:
            tasks: 処理対象タスクリスト
            processor_func: 処理関数
            progress_callback: 進捗コールバック
            
        Returns:
            List[ProcessingResult]: 処理結果リスト
        """
        start_time = time.time()
        self.stats.total_tasks = len(tasks)
        
        logger.info(f"同期並列処理開始: {len(tasks)}タスク")
        
        try:
            results = []
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # タスクを投入
                future_to_task = {
                    executor.submit(self._process_single_task, task, i, processor_func): (task, i)
                    for i, task in enumerate(tasks)
                }
                
                # 結果を収集
                for future in concurrent.futures.as_completed(future_to_task):
                    task, task_id = future_to_task[future]
                    
                    try:
                        result = future.result()
                        results.append(result)
                        
                        if result.success:
                            self.stats.completed_tasks += 1
                        else:
                            self.stats.failed_tasks += 1
                        
                        if progress_callback:
                            progress_callback(
                                self.stats.completed_tasks + self.stats.failed_tasks,
                                self.stats.total_tasks
                            )
                        
                    except Exception as e:
                        logger.error(f"Future取得エラー (タスクID: {task_id}): {e}")
                        results.append(ProcessingResult(
                            success=False,
                            error=str(e),
                            worker_id=f"sync-{task_id}"
                        ))
                        self.stats.failed_tasks += 1
            
            # 統計計算
            self.stats.total_time = time.time() - start_time
            self.stats.average_time = self.stats.total_time / len(tasks) if tasks else 0
            self.stats.throughput = len(tasks) / self.stats.total_time if self.stats.total_time > 0 else 0
            
            logger.info(f"同期並列処理完了: {self.stats.completed_tasks}/{self.stats.total_tasks} 成功")
            return results
            
        except Exception as e:
            logger.error(f"同期並列処理エラー: {e}")
            raise PerformanceError(f"並列処理失敗: {e}")
    
    def _process_single_task(
        self, 
        task: Any, 
        task_id: int, 
        processor_func: Callable
    ) -> ProcessingResult:
        """
        単一タスク処理
        
        Args:
            task: 処理対象タスク
            task_id: タスクID
            processor_func: 処理関数
            
        Returns:
            ProcessingResult: 処理結果
        """
        start_time = time.time()
        worker_id = f"sync-{threading.current_thread().ident}-{task_id}"
        
        try:
            result = processor_func(task)
            execution_time = time.time() - start_time
            
            return ProcessingResult(
                success=True,
                result=result,
                execution_time=execution_time,
                worker_id=worker_id
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"タスク処理エラー (ID: {task_id}, Worker: {worker_id}): {e}")
            
            return ProcessingResult(
                success=False,
                error=str(e),
                execution_time=execution_time,
                worker_id=worker_id
            )
    
    def process_chunked(
        self,
        tasks: List[Any],
        processor_func: Callable,
        progress_callback: Optional[Callable] = None
    ) -> List[ProcessingResult]:
        """
        チャンク分割並列処理
        
        Args:
            tasks: 処理対象タスクリスト
            processor_func: 処理関数
            progress_callback: 進捗コールバック
            
        Returns:
            List[ProcessingResult]: 処理結果リスト
        """
        if len(tasks) <= self.chunk_size:
            # チャンク分割不要
            if self.use_async:
                return asyncio.run(self.process_async(tasks, processor_func, progress_callback))
            else:
                return self.process_sync(tasks, processor_func, progress_callback)
        
        logger.info(f"チャンク分割処理開始: {len(tasks)}タスク -> {self.chunk_size}サイズのチャンク")
        
        all_results = []
        total_processed = 0
        
        # チャンクに分割
        for i in range(0, len(tasks), self.chunk_size):
            chunk = tasks[i:i + self.chunk_size]
            
            logger.debug(f"チャンク処理: {i+1}-{min(i+self.chunk_size, len(tasks))}/{len(tasks)}")
            
            # チャンク処理
            if self.use_async:
                chunk_results = asyncio.run(self.process_async(chunk, processor_func))
            else:
                chunk_results = self.process_sync(chunk, processor_func)
            
            all_results.extend(chunk_results)
            total_processed += len(chunk)
            
            # 進捗通知
            if progress_callback:
                progress_callback(total_processed, len(tasks))
        
        logger.info(f"チャンク分割処理完了: {len(all_results)}結果")
        return all_results
    
    def get_stats(self) -> ProcessingStats:
        """処理統計を取得"""
        return self.stats
    
    def reset_stats(self):
        """処理統計をリセット"""
        self.stats = ProcessingStats()


class FileProcessorPool:
    """ファイル処理専用プール"""
    
    def __init__(self, max_workers: Optional[int] = None):
        """
        ファイル処理プール初期化
        
        Args:
            max_workers: 最大ワーカー数
        """
        self.processor = ParallelProcessor(max_workers=max_workers, use_async=False)
    
    def process_files(
        self,
        file_paths: List[Path],
        processor_func: Callable[[Path], Any],
        progress_callback: Optional[Callable] = None
    ) -> List[ProcessingResult]:
        """
        ファイル並列処理
        
        Args:
            file_paths: ファイルパスリスト
            processor_func: ファイル処理関数
            progress_callback: 進捗コールバック
            
        Returns:
            List[ProcessingResult]: 処理結果リスト
        """
        logger.info(f"ファイル並列処理開始: {len(file_paths)}ファイル")
        
        # 存在するファイルのみ処理
        existing_files = [f for f in file_paths if f.exists()]
        
        if len(existing_files) != len(file_paths):
            missing_count = len(file_paths) - len(existing_files)
            logger.warning(f"{missing_count}個のファイルが存在しません")
        
        return self.processor.process_sync(
            existing_files,
            processor_func,
            progress_callback
        )
    
    def validate_yaml_files(
        self,
        yaml_files: List[Path],
        progress_callback: Optional[Callable] = None
    ) -> List[ProcessingResult]:
        """
        YAML ファイル並列バリデーション
        
        Args:
            yaml_files: YAMLファイルリスト
            progress_callback: 進捗コールバック
            
        Returns:
            List[ProcessingResult]: バリデーション結果リスト
        """
        from ..utils.validation import validate_yaml_file
        
        def validate_single_yaml(file_path: Path) -> Dict[str, Any]:
            """単一YAMLファイルバリデーション"""
            result = validate_yaml_file(file_path)
            return {
                'file_path': str(file_path),
                'is_valid': result.is_valid,
                'errors': result.errors,
                'warnings': result.warnings
            }
        
        return self.process_files(yaml_files, validate_single_yaml, progress_callback)


def create_progress_callback(description: str = "処理中") -> Callable:
    """
    進捗表示コールバックを作成
    
    Args:
        description: 処理説明
        
    Returns:
        Callable: 進捗コールバック関数
    """
    def progress_callback(completed: int, total: int):
        percentage = (completed / total) * 100 if total > 0 else 0
        logger.info(f"{description}: {completed}/{total} ({percentage:.1f}%)")
    
    return progress_callback


# 便利関数
async def process_files_async(
    file_paths: List[Path],
    processor_func: Callable,
    max_workers: Optional[int] = None,
    progress_callback: Optional[Callable] = None
) -> List[ProcessingResult]:
    """ファイル非同期並列処理"""
    processor = ParallelProcessor(max_workers=max_workers, use_async=True)
    return await processor.process_async(file_paths, processor_func, progress_callback)


def process_files_sync(
    file_paths: List[Path],
    processor_func: Callable,
    max_workers: Optional[int] = None,
    progress_callback: Optional[Callable] = None
) -> List[ProcessingResult]:
    """ファイル同期並列処理"""
    processor = ParallelProcessor(max_workers=max_workers, use_async=False)
    return processor.process_sync(file_paths, processor_func, progress_callback)
