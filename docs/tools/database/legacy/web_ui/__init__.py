"""
Web UIモジュール

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
"""

from .app import create_app
from .routes import register_routes
from .api import api_blueprint

__all__ = [
    'create_app',
    'register_routes',
    'api_blueprint'
]
