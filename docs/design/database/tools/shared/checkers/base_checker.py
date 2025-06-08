"""
ベースチェッカークラス

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/database/tools/REFACTORING_PLAN.md
実装日: 2025-06-08
実装者: AI Assistant
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import time

from ..core.models import TableDefinition
from ..core.config import DatabaseToolsConfig


@dataclass
class CheckResult:
    """チェック結果の基底クラス"""
    check_type: str
    table_name: str
    status: str  # 'pass', 'warning', 'error'
    message: str
    details: Optional[Dict[str, Any]] = None
    severity: str = 'info'  # 'info', 'warning', 'error', 'critical'


@dataclass
class CheckReport:
    """チェックレポートクラス"""
    checker_name: str
    total_checks: int
    passed_checks: int
    warning_checks: int
    error_checks: int
    results: List[CheckResult]
    execution_time: float
    
    @property
    def success_rate(self) -> float:
        """成功率を計算"""
        if self.total_checks == 0:
            return 100.0
        return (self.passed_checks / self.total_checks) * 100.0
    
    @property
    def has_errors(self) -> bool:
        """エラーが存在するかチェック"""
        return self.error_checks > 0
    
    @property
    def has_warnings(self) -> bool:
        """警告が存在するかチェック"""
        return self.warning_checks > 0


class BaseChecker(ABC):
    """チェッカーの基底クラス"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self._results: List[CheckResult] = []
        self._start_time: Optional[float] = None
    
    @abstractmethod
    def get_checker_name(self) -> str:
        """チェッカー名を取得"""
        pass
    
    @abstractmethod
    def check_table(self, table_def: TableDefinition) -> List[CheckResult]:
        """単一テーブルのチェック"""
        pass
    
    def check_tables(self, tables: List[TableDefinition]) -> CheckReport:
        """複数テーブルのチェック実行"""
        self._start_time = time.time()
        self._results = []
        
        self.logger.info(f"{self.get_checker_name()}チェック開始: {len(tables)}テーブル")
        
        for table_def in tables:
            try:
                table_results = self.check_table(table_def)
                self._results.extend(table_results)
                self.logger.debug(f"テーブル {table_def.name} チェック完了: {len(table_results)}件")
            except Exception as e:
                error_result = CheckResult(
                    check_type=self.get_checker_name(),
                    table_name=table_def.name,
                    status='error',
                    message=f"チェック実行エラー: {str(e)}",
                    severity='critical'
                )
                self._results.append(error_result)
                self.logger.error(f"テーブル {table_def.name} チェックエラー: {e}")
        
        execution_time = time.time() - self._start_time
        report = self._generate_report(execution_time)
        
        self.logger.info(f"{self.get_checker_name()}チェック完了: "
                        f"成功率 {report.success_rate:.1f}% "
                        f"({report.passed_checks}/{report.total_checks})")
        
        return report
    
    def _generate_report(self, execution_time: float) -> CheckReport:
        """チェックレポートを生成"""
        passed_checks = len([r for r in self._results if r.status == 'pass'])
        warning_checks = len([r for r in self._results if r.status == 'warning'])
        error_checks = len([r for r in self._results if r.status == 'error'])
        
        return CheckReport(
            checker_name=self.get_checker_name(),
            total_checks=len(self._results),
            passed_checks=passed_checks,
            warning_checks=warning_checks,
            error_checks=error_checks,
            results=self._results.copy(),
            execution_time=execution_time
        )
    
    def _create_result(self, table_name: str, status: str, message: str, 
                      details: Optional[Dict[str, Any]] = None, 
                      severity: str = 'info') -> CheckResult:
        """チェック結果を作成"""
        return CheckResult(
            check_type=self.get_checker_name(),
            table_name=table_name,
            status=status,
            message=message,
            details=details,
            severity=severity
        )
    
    def _validate_table_definition(self, table_def: TableDefinition) -> bool:
        """テーブル定義の基本検証"""
        if not table_def.name:
            self.logger.warning("テーブル名が空です")
            return False
        
        if not table_def.columns:
            self.logger.warning(f"テーブル {table_def.name} にカラムが定義されていません")
            return False
        
        return True
