#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設計ツールシステム - AI駆動機能モジュール

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

AI駆動による設計書生成、品質改善提案、整合性チェック機能を提供します。
既存の統一生成エンジンと統合し、高度な自動化を実現します。
"""

from .generators import (
    AIGenerationEngine,
    AIDesignDocGenerator,
    AIQualityImprover,
    AIConsistencyChecker
)

from .analyzers import (
    AIAnalysisEngine,
    AIQualityAnalyzer,
    AIComplexityAnalyzer,
    AIPatternAnalyzer
)

from .suggestions import (
    AISuggestionEngine,
    AINamingOptimizer,
    AIStructureOptimizer,
    AIPerformanceOptimizer
)

from .integrations import (
    AIIntegrationManager,
    OpenAIIntegration,
    ClaudeIntegration,
    LocalLLMIntegration
)

__version__ = "2.0.0"
__author__ = "統一設計ツールシステム開発チーム"

__all__ = [
    # AI生成エンジン
    "AIGenerationEngine",
    "AIDesignDocGenerator", 
    "AIQualityImprover",
    "AIConsistencyChecker",
    
    # AI分析エンジン
    "AIAnalysisEngine",
    "AIQualityAnalyzer",
    "AIComplexityAnalyzer",
    "AIPatternAnalyzer",
    
    # AI提案エンジン
    "AISuggestionEngine",
    "AINamingOptimizer",
    "AIStructureOptimizer",
    "AIPerformanceOptimizer",
    
    # AI統合管理
    "AIIntegrationManager",
    "OpenAIIntegration",
    "ClaudeIntegration",
    "LocalLLMIntegration"
]
