"""
設計統合ツール - コアモジュール
要求仕様ID: PLT.1-WEB.1

設計統合ツールのコア機能を提供します。
"""

from .config import DesignIntegrationConfig, DatabaseConfig, APIConfig, ScreenConfig
from .logger import get_logger, setup_logging
from .exceptions import DesignIntegrationError, ValidationError, GenerationError
from .models import DesignDocument, RequirementMapping, IntegrationResult

__all__ = [
    'DesignIntegrationConfig',
    'DatabaseConfig', 
    'APIConfig',
    'ScreenConfig',
    'get_logger',
    'setup_logging',
    'DesignIntegrationError',
    'ValidationError',
    'GenerationError',
    'DesignDocument',
    'RequirementMapping',
    'IntegrationResult',
]
