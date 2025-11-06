"""
統合設計ツール - コアライブラリ

このモジュールは統合設計ツールエコシステムの中核となるライブラリです。
全ての設計ツール（データベース、API、画面、テスト）で共通利用される
基盤機能を提供します。

主要機能:
- 統一設定管理
- 統一バリデーション
- 統一生成エンジン
- ツール間連携
- 品質保証
"""

from .config import IntegratedConfig
from .validation import ValidationEngine
from .generation import GenerationEngine
from .integration import IntegrationManager
from .quality import QualityAssurance

__version__ = "1.0.0"
__author__ = "年間スキル報告書WEB化PJT開発チーム"

__all__ = [
    "IntegratedConfig",
    "ValidationEngine", 
    "GenerationEngine",
    "IntegrationManager",
    "QualityAssurance"
]
