"""
データベース整合性チェックツール - メインチェッカー
"""
from typing import List
from core.models import CheckResult, CheckConfig, ConsistencyReport
from core.logger import ConsistencyLogger
from core.config import Config
from checkers.check_orchestrator import CheckOrchestrator

class ConsistencyChecker:
    """データベース整合性チェックのメインエンジン"""
    
    def __init__(self, config: Config, check_config: CheckConfig):
        """
        チェッカー初期化
        
        Args:
            config: 設定
            check_config: チェック設定
        """
        self.config = config
        self.check_config = check_config
        self.logger = ConsistencyLogger(verbose=check_config.verbose)
        self.orchestrator = CheckOrchestrator(config, check_config)
    
    def run_all_checks(self) -> ConsistencyReport:
        """
        全ての整合性チェックを実行
        
        Returns:
            整合性チェックレポート
        """
        return self.orchestrator.run_all_checks()
    
    def run_specific_checks(self, check_names: List[str]) -> ConsistencyReport:
        """
        指定されたチェックのみを実行
        
        Args:
            check_names: 実行するチェック名のリスト
            
        Returns:
            整合性チェックレポート
        """
        return self.orchestrator.run_specific_checks(check_names)
    
    def get_available_checks(self) -> List[str]:
        """利用可能なチェック名のリストを取得"""
        return self.orchestrator.get_available_checks()
    
    def validate_check_names(self, check_names: List[str]) -> List[str]:
        """
        チェック名の妥当性を検証
        
        Args:
            check_names: チェック名のリスト
            
        Returns:
            無効なチェック名のリスト
        """
        return self.orchestrator.validate_check_names(check_names)
