#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統一設定検証システム

要求仕様ID: PLT.1-WEB.1
設計書: docs/design/architecture/技術スタック設計書.md

統一設計ツールシステムの設定検証機能を提供します。
設定の妥当性、整合性、セキュリティを包括的に検証します。
"""

import os
import re
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass
from .schema import ConfigSchema, Environment, ToolType, LogLevel


@dataclass
class ValidationResult:
    """検証結果"""
    valid: bool
    errors: List[str] = None
    warnings: List[str] = None
    suggestions: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []
        if self.suggestions is None:
            self.suggestions = []
    
    def add_error(self, message: str):
        """エラーを追加"""
        self.errors.append(message)
        self.valid = False
    
    def add_warning(self, message: str):
        """警告を追加"""
        self.warnings.append(message)
    
    def add_suggestion(self, message: str):
        """提案を追加"""
        self.suggestions.append(message)
    
    def merge(self, other: 'ValidationResult'):
        """他の検証結果をマージ"""
        if not other.valid:
            self.valid = False
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.suggestions.extend(other.suggestions)
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "summary": {
                "error_count": len(self.errors),
                "warning_count": len(self.warnings),
                "suggestion_count": len(self.suggestions)
            }
        }


class ConfigValidator:
    """統一設定検証クラス"""
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        初期化
        
        Args:
            project_root: プロジェクトルートパス
        """
        self.project_root = project_root or self._find_project_root()
        
        # 検証ルール
        self.validation_rules = {
            "project_name": self._validate_project_name,
            "paths": self._validate_paths,
            "database": self._validate_database_config,
            "api": self._validate_api_config,
            "screens": self._validate_screen_config,
            "testing": self._validate_testing_config,
            "quality": self._validate_quality_config,
            "integration": self._validate_integration_config,
            "logging": self._validate_logging_config
        }
    
    def _find_project_root(self) -> Path:
        """プロジェクトルートディレクトリを検索"""
        current = Path(__file__).parent
        while current.parent != current:
            if (current / "package.json").exists() or (current / ".git").exists():
                return current
            current = current.parent
        return Path.cwd()
    
    def validate(self, config: ConfigSchema) -> ValidationResult:
        """
        設定の包括的検証
        
        Args:
            config: 検証対象の設定
            
        Returns:
            検証結果
        """
        result = ValidationResult(valid=True)
        
        # 基本検証
        result.merge(self._validate_basic_config(config))
        
        # 個別検証
        for rule_name, rule_func in self.validation_rules.items():
            try:
                rule_result = rule_func(config)
                result.merge(rule_result)
            except Exception as e:
                result.add_error(f"検証ルール '{rule_name}' でエラー: {str(e)}")
        
        # 整合性検証
        result.merge(self._validate_consistency(config))
        
        # セキュリティ検証
        result.merge(self._validate_security(config))
        
        return result
    
    def _validate_basic_config(self, config: ConfigSchema) -> ValidationResult:
        """基本設定の検証"""
        result = ValidationResult(valid=True)
        
        # プロジェクト名検証
        if not config.project_name:
            result.add_error("プロジェクト名が設定されていません")
        elif not re.match(r'^[a-zA-Z0-9_-]+$', config.project_name):
            result.add_error("プロジェクト名に無効な文字が含まれています")
        
        # 環境検証
        if not isinstance(config.environment, Environment):
            result.add_error("無効な環境設定です")
        
        # バージョン検証
        if not config.version:
            result.add_warning("バージョンが設定されていません")
        elif not re.match(r'^\d+\.\d+\.\d+$', config.version):
            result.add_warning("バージョン形式が推奨形式（x.y.z）ではありません")
        
        return result
    
    def _validate_project_name(self, config: ConfigSchema) -> ValidationResult:
        """プロジェクト名の詳細検証"""
        result = ValidationResult(valid=True)
        
        project_name = config.project_name
        
        # 長さ検証
        if len(project_name) < 3:
            result.add_error("プロジェクト名は3文字以上である必要があります")
        elif len(project_name) > 50:
            result.add_error("プロジェクト名は50文字以下である必要があります")
        
        # 命名規則検証
        if project_name.startswith('-') or project_name.endswith('-'):
            result.add_error("プロジェクト名の先頭・末尾にハイフンは使用できません")
        
        if '__' in project_name:
            result.add_warning("プロジェクト名に連続するアンダースコアは推奨されません")
        
        return result
    
    def _validate_paths(self, config: ConfigSchema) -> ValidationResult:
        """パス設定の検証"""
        result = ValidationResult(valid=True)
        
        paths = config.paths
        
        # 必須パスの存在確認
        required_paths = [
            ("design_root", paths.design_root),
            ("output_root", paths.output_root)
        ]
        
        for path_name, path_value in required_paths:
            if not path_value:
                result.add_error(f"必須パス '{path_name}' が設定されていません")
                continue
            
            full_path = self.project_root / path_value
            if not full_path.exists():
                result.add_warning(f"パス '{path_name}' が存在しません: {full_path}")
        
        # パスの重複確認
        path_values = [paths.design_root, paths.output_root, paths.backup_root, paths.temp_root]
        if len(set(path_values)) != len(path_values):
            result.add_warning("パス設定に重複があります")
        
        return result
    
    def _validate_database_config(self, config: ConfigSchema) -> ValidationResult:
        """データベース設定の検証"""
        result = ValidationResult(valid=True)
        
        db_config = config.database
        
        # 基本設定検証
        if db_config.type not in ["postgresql", "mysql", "sqlite", "oracle"]:
            result.add_warning(f"サポートされていないデータベースタイプ: {db_config.type}")
        
        if db_config.encoding not in ["utf-8", "utf8", "latin1"]:
            result.add_warning(f"推奨されないエンコーディング: {db_config.encoding}")
        
        # パフォーマンス設定検証
        if db_config.parallel_workers < 1 or db_config.parallel_workers > 16:
            result.add_warning("parallel_workersは1-16の範囲で設定することを推奨します")
        
        if db_config.cache_ttl < 60 or db_config.cache_ttl > 86400:
            result.add_warning("cache_ttlは60-86400秒の範囲で設定することを推奨します")
        
        # 必須セクション検証
        required_sections = ["revision_history", "overview", "notes", "rules"]
        missing_sections = [s for s in required_sections if s not in db_config.required_sections]
        if missing_sections:
            result.add_error(f"必須セクションが不足しています: {missing_sections}")
        
        return result
    
    def _validate_api_config(self, config: ConfigSchema) -> ValidationResult:
        """API設定の検証"""
        result = ValidationResult(valid=True)
        
        api_config = config.api
        
        # OpenAPI バージョン検証
        if not re.match(r'^\d+\.\d+\.\d+$', api_config.openapi_version):
            result.add_error("OpenAPIバージョンが無効な形式です")
        
        # ポート番号検証
        if api_config.mock_server_port < 1024 or api_config.mock_server_port > 65535:
            result.add_error("mock_server_portが無効な範囲です（1024-65535）")
        
        # フレームワーク検証
        if api_config.framework not in ["nextjs", "express", "fastapi", "spring"]:
            result.add_warning(f"サポートされていないフレームワーク: {api_config.framework}")
        
        return result
    
    def _validate_screen_config(self, config: ConfigSchema) -> ValidationResult:
        """画面設定の検証"""
        result = ValidationResult(valid=True)
        
        screen_config = config.screens
        
        # フレームワーク検証
        if screen_config.framework not in ["react", "vue", "angular", "svelte"]:
            result.add_warning(f"サポートされていないフレームワーク: {screen_config.framework}")
        
        # CSSフレームワーク検証
        if screen_config.css_framework not in ["tailwindcss", "bootstrap", "material-ui", "chakra-ui"]:
            result.add_warning(f"サポートされていないCSSフレームワーク: {screen_config.css_framework}")
        
        # アクセシビリティレベル検証
        if screen_config.accessibility_level not in ["A", "AA", "AAA"]:
            result.add_error("accessibility_levelは A, AA, AAA のいずれかである必要があります")
        
        # ブレークポイント検証
        required_breakpoints = ["mobile", "tablet", "desktop"]
        missing_breakpoints = [bp for bp in required_breakpoints if bp not in screen_config.responsive_breakpoints]
        if missing_breakpoints:
            result.add_warning(f"推奨ブレークポイントが不足しています: {missing_breakpoints}")
        
        return result
    
    def _validate_testing_config(self, config: ConfigSchema) -> ValidationResult:
        """テスト設定の検証"""
        result = ValidationResult(valid=True)
        
        testing_config = config.testing
        
        # カバレッジ閾値検証
        if testing_config.coverage_threshold < 0 or testing_config.coverage_threshold > 100:
            result.add_error("coverage_thresholdは0-100の範囲である必要があります")
        elif testing_config.coverage_threshold < 70:
            result.add_warning("coverage_thresholdが70%未満です。品質向上のため80%以上を推奨します")
        
        # フレームワーク検証
        supported_frameworks = ["jest", "mocha", "playwright", "cypress", "selenium"]
        unsupported = [f for f in testing_config.frameworks if f not in supported_frameworks]
        if unsupported:
            result.add_warning(f"サポートされていないテストフレームワーク: {unsupported}")
        
        # パフォーマンス予算検証
        if "response_time" in testing_config.performance_budget:
            response_time = testing_config.performance_budget["response_time"]
            if response_time > 3000:
                result.add_warning("レスポンス時間の予算が3秒を超えています")
        
        return result
    
    def _validate_quality_config(self, config: ConfigSchema) -> ValidationResult:
        """品質設定の検証"""
        result = ValidationResult(valid=True)
        
        quality_config = config.quality
        
        # 品質ゲート検証
        if "test_coverage" in quality_config.quality_gates:
            coverage = quality_config.quality_gates["test_coverage"]
            if coverage < 50:
                result.add_warning("テストカバレッジの品質ゲートが50%未満です")
        
        if "security_score" in quality_config.quality_gates:
            security_score = quality_config.quality_gates["security_score"]
            if security_score < 80:
                result.add_warning("セキュリティスコアの品質ゲートが80未満です")
        
        return result
    
    def _validate_integration_config(self, config: ConfigSchema) -> ValidationResult:
        """統合設定の検証"""
        result = ValidationResult(valid=True)
        
        integration_config = config.integration
        
        # 通知チャンネル検証
        supported_channels = ["console", "file", "email", "slack", "teams"]
        unsupported = [ch for ch in integration_config.notification_channels if ch not in supported_channels]
        if unsupported:
            result.add_warning(f"サポートされていない通知チャンネル: {unsupported}")
        
        # Webhook URL検証
        for url in integration_config.webhook_urls:
            if not url.startswith(("http://", "https://")):
                result.add_error(f"無効なWebhook URL: {url}")
        
        return result
    
    def _validate_logging_config(self, config: ConfigSchema) -> ValidationResult:
        """ログ設定の検証"""
        result = ValidationResult(valid=True)
        
        logging_config = config.logging
        
        # ログレベル検証
        if not isinstance(logging_config.level, LogLevel):
            result.add_error("無効なログレベルです")
        
        # ファイルサイズ検証
        if logging_config.file_enabled:
            if not re.match(r'^\d+[KMGT]?B$', logging_config.max_file_size):
                result.add_error("max_file_sizeの形式が無効です（例: 10MB）")
        
        # バックアップ数検証
        if logging_config.backup_count < 1 or logging_config.backup_count > 100:
            result.add_warning("backup_countは1-100の範囲で設定することを推奨します")
        
        return result
    
    def _validate_consistency(self, config: ConfigSchema) -> ValidationResult:
        """設定間の整合性検証"""
        result = ValidationResult(valid=True)
        
        # パス整合性
        if config.database.yaml_dir.startswith(config.paths.design_root):
            pass  # 正常
        else:
            result.add_warning("データベース設定のパスが設計ルートと整合していません")
        
        # 環境別設定整合性
        if config.environment == Environment.PRODUCTION:
            if config.logging.level == LogLevel.DEBUG:
                result.add_warning("本番環境でDEBUGログレベルが設定されています")
            
            if config.api.mock_server_enabled:
                result.add_error("本番環境でモックサーバーが有効になっています")
        
        return result
    
    def _validate_security(self, config: ConfigSchema) -> ValidationResult:
        """セキュリティ検証"""
        result = ValidationResult(valid=True)
        
        # 本番環境でのセキュリティチェック
        if config.environment == Environment.PRODUCTION:
            if not config.quality.breaking_change_detection:
                result.add_warning("本番環境で破壊的変更検出が無効になっています")
            
            if not config.integration.ci_integration:
                result.add_warning("本番環境でCI統合が無効になっています")
        
        # ログファイルのセキュリティ
        if config.logging.file_enabled:
            log_path = Path(config.logging.file_path)
            if log_path.is_absolute() and str(log_path).startswith('/tmp'):
                result.add_warning("ログファイルが一時ディレクトリに設定されています")
        
        return result
    
    def validate_file_permissions(self, config: ConfigSchema) -> ValidationResult:
        """ファイル権限の検証"""
        result = ValidationResult(valid=True)
        
        # 重要なディレクトリの権限確認
        important_paths = [
            config.paths.design_root,
            config.paths.output_root,
            config.database.yaml_dir,
            config.api.specs_dir
        ]
        
        for path_str in important_paths:
            path = self.project_root / path_str
            if path.exists():
                # 読み取り権限確認
                if not os.access(path, os.R_OK):
                    result.add_error(f"読み取り権限がありません: {path}")
                
                # 書き込み権限確認
                if not os.access(path, os.W_OK):
                    result.add_warning(f"書き込み権限がありません: {path}")
        
        return result
    
    def suggest_improvements(self, config: ConfigSchema) -> List[str]:
        """設定改善提案"""
        suggestions = []
        
        # パフォーマンス改善提案
        if config.database.parallel_workers == 1:
            suggestions.append("データベース処理の並列度を上げることでパフォーマンスが向上する可能性があります")
        
        if not config.database.cache_enabled:
            suggestions.append("データベースキャッシュを有効にすることで処理速度が向上します")
        
        # 品質改善提案
        if config.testing.coverage_threshold < 80:
            suggestions.append("テストカバレッジを80%以上に設定することを推奨します")
        
        if not config.quality.auto_fix_suggestions:
            suggestions.append("自動修正提案を有効にすることで開発効率が向上します")
        
        # セキュリティ改善提案
        if not config.quality.breaking_change_detection:
            suggestions.append("破壊的変更検出を有効にすることでシステムの安定性が向上します")
        
        return suggestions
