"""
統一設計ツールシステム

全ての設計ツールで共通利用される統一基盤システムです。
設定管理、バリデーション、生成、統合、分析の各エンジンを提供します。

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

from .config.manager import UnifiedConfigManager
from .config.schema import UnifiedConfig
from .config.validator import UnifiedConfigValidator

from .core.validation import (
    UnifiedValidationEngine,
    ValidationReport,
    ValidationIssue,
    ValidationCategory,
    ValidationSeverity
)

from .core.generation import (
    UnifiedGenerationEngine,
    GenerationContext,
    GenerationResult,
    GenerationType,
    GenerationTemplate
)

from .core.integration import (
    UnifiedIntegrationEngine,
    IntegrationTask,
    IntegrationResult,
    IntegrationType,
    WorkflowStage,
    WorkflowContext
)

from .core.analysis import (
    UnifiedAnalysisEngine,
    AnalysisResult,
    AnalysisMetric,
    AnalysisType,
    MetricType
)

__version__ = "1.0.0"
__author__ = "統一設計ツールシステム開発チーム"

# 統一エンジンのファクトリー関数
def create_unified_system(project_name: str = "default"):
    """統一設計ツールシステムを作成"""
    return UnifiedDesignToolSystem(project_name)


class UnifiedDesignToolSystem:
    """統一設計ツールシステム メインクラス"""
    
    def __init__(self, project_name: str = "default"):
        self.project_name = project_name
        
        # 各エンジンを初期化
        self.config_manager = UnifiedConfigManager(project_name)
        self.validation_engine = UnifiedValidationEngine(project_name)
        self.generation_engine = UnifiedGenerationEngine(project_name)
        self.integration_engine = UnifiedIntegrationEngine(project_name)
        self.analysis_engine = UnifiedAnalysisEngine(project_name)
    
    def get_config(self) -> UnifiedConfig:
        """設定を取得"""
        return self.config_manager.load_config()
    
    def validate_project(self, target_path: str = None) -> ValidationReport:
        """プロジェクト全体をバリデーション"""
        if target_path is None:
            target_path = self.get_config().project_root
        return self.validation_engine.validate_directory(target_path, "*")
    
    def analyze_project(self, target_path: str = None):
        """プロジェクト全体を分析"""
        if target_path is None:
            target_path = self.get_config().project_root
        return self.analysis_engine.comprehensive_analysis(target_path)
    
    def generate_dashboard_data(self, target_path: str = None):
        """ダッシュボード用データを生成"""
        if target_path is None:
            target_path = self.get_config().project_root
        return self.analysis_engine.generate_dashboard_data(target_path)


# 便利な関数をエクスポート
__all__ = [
    # メインクラス
    "UnifiedDesignToolSystem",
    "create_unified_system",
    
    # 設定管理
    "UnifiedConfigManager",
    "UnifiedConfig",
    "UnifiedConfigValidator",
    
    # バリデーション
    "UnifiedValidationEngine",
    "ValidationReport",
    "ValidationIssue",
    "ValidationCategory",
    "ValidationSeverity",
    
    # 生成
    "UnifiedGenerationEngine",
    "GenerationContext",
    "GenerationResult",
    "GenerationType",
    "GenerationTemplate",
    
    # 統合
    "UnifiedIntegrationEngine",
    "IntegrationTask",
    "IntegrationResult",
    "IntegrationType",
    "WorkflowStage",
    "WorkflowContext",
    
    # 分析
    "UnifiedAnalysisEngine",
    "AnalysisResult",
    "AnalysisMetric",
    "AnalysisType",
    "MetricType"
]
