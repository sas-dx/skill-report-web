"""
統一設計ツールシステム - コア機能モジュール

統一設計ツールシステムの中核機能を提供します。
- validation: 横断的な設計書検証
- generation: 設計書自動生成
- integration: ツール間連携
- analysis: 設計品質分析

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md
"""

from .validation import UnifiedValidationEngine, ValidationLevel, ValidationCategory
from .generation import UnifiedGenerationEngine, GenerationType, GenerationTemplate
from .integration import UnifiedIntegrationEngine, IntegrationType, IntegrationStatus
from .analysis import UnifiedAnalysisEngine, AnalysisType, QualityMetrics

__all__ = [
    # Validation
    'UnifiedValidationEngine',
    'ValidationLevel',
    'ValidationCategory',
    
    # Generation
    'UnifiedGenerationEngine',
    'GenerationType',
    'GenerationTemplate',
    
    # Integration
    'UnifiedIntegrationEngine',
    'IntegrationType',
    'IntegrationStatus',
    
    # Analysis
    'UnifiedAnalysisEngine',
    'AnalysisType',
    'QualityMetrics'
]

__version__ = "2.0.0"
__author__ = "統一設計ツール開発チーム"
