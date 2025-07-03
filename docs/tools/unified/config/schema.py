#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設定スキーマ定義

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

統一設計ツールシステムの設定スキーマを定義します。
型安全性とバリデーション機能を提供し、設定の一貫性を保証します。
"""

import os
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Environment(Enum):
    """実行環境の定義"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class ToolType(Enum):
    """設計ツールの種類"""
    DATABASE = "database"
    API = "api"
    SCREENS = "screens"
    TESTING = "testing"


class LogLevel(Enum):
    """ログレベル"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class PathConfig:
    """パス設定"""
    design_root: str = "docs/design"
    output_root: str = "docs/design"
    backup_root: str = "docs/design/backups"
    temp_root: str = "temp"
    
    def get_absolute_path(self, relative_path: str, project_root: Path) -> Path:
        """相対パスを絶対パスに変換"""
        if os.path.isabs(relative_path):
            return Path(relative_path)
        return project_root / relative_path


@dataclass
class DatabaseConfig:
    """データベース設計ツール設定"""
    # 基本設定
    type: str = "postgresql"
    encoding: str = "utf-8"
    
    # パス設定
    yaml_dir: str = "docs/design/database/table-details"
    ddl_dir: str = "docs/design/database/ddl"
    tables_dir: str = "docs/design/database/tables"
    reports_dir: str = "docs/design/database/reports"
    
    # 品質設定
    strict_mode: bool = True
    required_sections: List[str] = field(default_factory=lambda: [
        "revision_history", "overview", "notes", "rules"
    ])
    
    # パフォーマンス設定
    parallel_workers: int = 4
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    # 検証設定
    validate_foreign_keys: bool = True
    validate_indexes: bool = True
    validate_constraints: bool = True
    
    # 生成設定
    auto_generate_ddl: bool = True
    auto_generate_docs: bool = True
    auto_generate_samples: bool = True


@dataclass
class APIConfig:
    """API設計ツール設定"""
    # 基本設定
    openapi_version: str = "3.0.3"
    framework: str = "nextjs"
    
    # パス設定
    specs_dir: str = "docs/design/api/specs"
    output_dir: str = "docs/design/api"
    typescript_dir: str = "src/types/api"
    
    # 開発設定
    mock_server_port: int = 3001
    mock_server_enabled: bool = True
    
    # 検証設定
    validation_strict: bool = True
    validate_examples: bool = True
    validate_schemas: bool = True
    
    # 生成設定
    auto_generate_types: bool = True
    auto_generate_mocks: bool = True
    auto_generate_tests: bool = True
    include_examples: bool = True


@dataclass
class ScreenConfig:
    """画面設計ツール設定"""
    # 基本設定
    framework: str = "react"
    typescript: bool = True
    css_framework: str = "tailwindcss"
    
    # パス設定
    specs_dir: str = "docs/design/screens/specs"
    output_dir: str = "docs/design/screens"
    components_dir: str = "src/components/generated"
    storybook_dir: str = ".storybook/generated"
    
    # アクセシビリティ設定
    accessibility_level: str = "AA"
    validate_contrast: bool = True
    validate_keyboard_nav: bool = True
    
    # レスポンシブ設定
    responsive_breakpoints: List[str] = field(default_factory=lambda: [
        "mobile", "tablet", "desktop"
    ])
    
    # 生成設定
    auto_generate_components: bool = True
    auto_generate_stories: bool = True
    auto_generate_tests: bool = True


@dataclass
class TestingConfig:
    """テスト設計ツール設定"""
    # 基本設定
    frameworks: List[str] = field(default_factory=lambda: ["jest", "playwright"])
    
    # パス設定
    specs_dir: str = "docs/testing"
    unit_test_dir: str = "src/__tests__"
    e2e_test_dir: str = "tests/e2e"
    reports_dir: str = "test-reports"
    
    # 品質設定
    coverage_threshold: int = 80
    performance_budget: Dict[str, Union[int, str]] = field(default_factory=lambda: {
        "response_time": 1000,
        "memory_usage": "100MB"
    })
    
    # 生成設定
    auto_generate_mocks: bool = True
    auto_generate_fixtures: bool = True
    auto_generate_scenarios: bool = True


@dataclass
class QualityConfig:
    """品質保証設定"""
    # 要求仕様管理
    requirement_id_mandatory: bool = True
    design_doc_sync: bool = True
    breaking_change_detection: bool = True
    
    # 自動化設定
    auto_fix_suggestions: bool = True
    auto_format_code: bool = True
    auto_update_docs: bool = True
    
    # メトリクス設定
    metrics_collection: bool = True
    performance_monitoring: bool = True
    quality_gates: Dict[str, Any] = field(default_factory=lambda: {
        "test_coverage": 80,
        "code_quality": "A",
        "security_score": 90
    })


@dataclass
class IntegrationConfig:
    """ツール間連携設定"""
    # 連携設定
    enable_cross_tool_validation: bool = True
    auto_sync_changes: bool = True
    real_time_monitoring: bool = False
    
    # 通知設定
    notification_channels: List[str] = field(default_factory=lambda: ["console", "file"])
    webhook_urls: List[str] = field(default_factory=list)
    
    # CI/CD設定
    ci_integration: bool = True
    auto_deploy_docs: bool = True
    pre_commit_hooks: bool = True


@dataclass
class LoggingConfig:
    """ログ設定"""
    level: LogLevel = LogLevel.INFO
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_enabled: bool = True
    file_path: str = "logs/design-tools.log"
    console_enabled: bool = True
    max_file_size: str = "10MB"
    backup_count: int = 5


@dataclass
class ToolConfig:
    """個別ツール設定の基底クラス"""
    tool_type: ToolType
    enabled: bool = True
    version: str = "1.0.0"
    
    # 共通パス設定
    paths: PathConfig = field(default_factory=PathConfig)
    
    # 共通品質設定
    quality: QualityConfig = field(default_factory=QualityConfig)
    
    # 共通ログ設定
    logging: LoggingConfig = field(default_factory=LoggingConfig)


@dataclass
class ConfigSchema:
    """統一設定スキーマのメインクラス"""
    # 基本情報
    project_name: str = "skill-report-web"
    environment: Environment = Environment.DEVELOPMENT
    version: str = "2.0.0"
    
    # ツール設定
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: APIConfig = field(default_factory=APIConfig)
    screens: ScreenConfig = field(default_factory=ScreenConfig)
    testing: TestingConfig = field(default_factory=TestingConfig)
    
    # 共通設定
    paths: PathConfig = field(default_factory=PathConfig)
    quality: QualityConfig = field(default_factory=QualityConfig)
    integration: IntegrationConfig = field(default_factory=IntegrationConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    
    # メタデータ
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def get_tool_config(self, tool_type: ToolType) -> Union[DatabaseConfig, APIConfig, ScreenConfig, TestingConfig]:
        """指定されたツールの設定を取得"""
        tool_mapping = {
            ToolType.DATABASE: self.database,
            ToolType.API: self.api,
            ToolType.SCREENS: self.screens,
            ToolType.TESTING: self.testing
        }
        return tool_mapping.get(tool_type)
    
    def is_tool_enabled(self, tool_type: ToolType) -> bool:
        """指定されたツールが有効かどうかを確認"""
        tool_config = self.get_tool_config(tool_type)
        return getattr(tool_config, 'enabled', True)
    
    def get_absolute_path(self, relative_path: str, project_root: Path) -> Path:
        """相対パスを絶対パスに変換"""
        return self.paths.get_absolute_path(relative_path, project_root)
    
    def to_dict(self) -> Dict[str, Any]:
        """設定を辞書形式に変換"""
        return {
            "project_name": self.project_name,
            "environment": self.environment.value,
            "version": self.version,
            "database": self._dataclass_to_dict(self.database),
            "api": self._dataclass_to_dict(self.api),
            "screens": self._dataclass_to_dict(self.screens),
            "testing": self._dataclass_to_dict(self.testing),
            "paths": self._dataclass_to_dict(self.paths),
            "quality": self._dataclass_to_dict(self.quality),
            "integration": self._dataclass_to_dict(self.integration),
            "logging": self._dataclass_to_dict(self.logging),
            "metadata": self.metadata
        }
    
    def _dataclass_to_dict(self, obj: Any) -> Dict[str, Any]:
        """データクラスオブジェクトを辞書に変換"""
        if hasattr(obj, '__dataclass_fields__'):
            result = {}
            for field_name in obj.__dataclass_fields__:
                value = getattr(obj, field_name)
                if isinstance(value, Enum):
                    result[field_name] = value.value
                elif hasattr(value, '__dataclass_fields__'):
                    result[field_name] = self._dataclass_to_dict(value)
                else:
                    result[field_name] = value
            return result
        return obj
    
    def __str__(self) -> str:
        """設定の文字列表現"""
        return f"ConfigSchema(project={self.project_name}, env={self.environment.value}, version={self.version})"
    
    def __repr__(self) -> str:
        """設定の詳細表現"""
        return (
            f"ConfigSchema("
            f"project_name='{self.project_name}', "
            f"environment={self.environment.value}, "
            f"version='{self.version}', "
            f"tools=[database, api, screens, testing]"
            f")"
        )
