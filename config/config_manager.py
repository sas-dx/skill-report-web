#!/usr/bin/env python3
"""
統合設定マネージャー
グローバル設定、ツール設定、プロジェクト設定を統合管理
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import logging

@dataclass
class ConfigPaths:
    """設定ファイルパス管理"""
    global_config: str = "config/global/default.yaml"
    tools_dir: str = "config/tools"
    projects_dir: str = "config/projects"
    
class ConfigManager:
    """統合設定マネージャー"""
    
    def __init__(self, project_name: Optional[str] = None, tool_name: Optional[str] = None):
        """
        初期化
        
        Args:
            project_name: プロジェクト名（例: "skill-report-web"）
            tool_name: ツール名（例: "ui-generator"）
        """
        self.project_name = project_name
        self.tool_name = tool_name
        self.paths = ConfigPaths()
        self.logger = self._setup_logger()
        
        # 設定キャッシュ
        self._global_config = None
        self._tool_config = None
        self._project_config = None
        self._merged_config = None
        
    def _setup_logger(self) -> logging.Logger:
        """ログ設定"""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
        
    def load_yaml_file(self, file_path: str) -> Dict[str, Any]:
        """YAMLファイル読み込み"""
        try:
            path = Path(file_path)
            if not path.exists():
                self.logger.warning(f"設定ファイルが見つかりません: {file_path}")
                return {}
                
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
                
        except Exception as e:
            self.logger.error(f"設定ファイル読み込みエラー: {file_path} - {e}")
            return {}
            
    def get_global_config(self) -> Dict[str, Any]:
        """グローバル設定取得"""
        if self._global_config is None:
            self._global_config = self.load_yaml_file(self.paths.global_config)
        return self._global_config
        
    def get_tool_config(self, tool_name: Optional[str] = None) -> Dict[str, Any]:
        """ツール設定取得"""
        tool = tool_name or self.tool_name
        if not tool:
            return {}
            
        if self._tool_config is None:
            tool_config_path = f"{self.paths.tools_dir}/{tool}.yaml"
            self._tool_config = self.load_yaml_file(tool_config_path)
        return self._tool_config
        
    def get_project_config(self, project_name: Optional[str] = None) -> Dict[str, Any]:
        """プロジェクト設定取得"""
        project = project_name or self.project_name
        if not project:
            return {}
            
        if self._project_config is None:
            project_config_path = f"{self.paths.projects_dir}/{project}.yaml"
            self._project_config = self.load_yaml_file(project_config_path)
        return self._project_config
        
    def merge_configs(self) -> Dict[str, Any]:
        """設定統合（優先度: プロジェクト > ツール > グローバル）"""
        if self._merged_config is not None:
            return self._merged_config
            
        # 基本設定から開始
        merged = self.get_global_config().copy()
        
        # ツール設定をマージ
        tool_config = self.get_tool_config()
        if tool_config:
            merged = self._deep_merge(merged, tool_config)
            
        # プロジェクト設定をマージ（最高優先度）
        project_config = self.get_project_config()
        if project_config:
            merged = self._deep_merge(merged, project_config)
            
        self._merged_config = merged
        return merged
        
    def _deep_merge(self, base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """辞書の深いマージ"""
        result = base.copy()
        
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result
        
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        ドット記法でのキー取得
        
        Args:
            key_path: "system.name" のようなドット区切りのキーパス
            default: デフォルト値
            
        Returns:
            設定値
        """
        config = self.merge_configs()
        keys = key_path.split('.')
        
        current = config
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
                
        return current
        
    def get_screen_config(self, screen_type: str) -> Dict[str, Any]:
        """画面タイプ別設定取得"""
        # プロジェクト固有の画面設定
        project_screens = self.get("screens", {})
        if screen_type in project_screens:
            screen_config = project_screens[screen_type].copy()
        else:
            screen_config = {}
            
        # ツール設定の画面タイプ設定をマージ
        tool_screen_types = self.get("screen_types", {})
        if screen_type in tool_screen_types:
            screen_config = self._deep_merge(screen_config, tool_screen_types[screen_type])
            
        return screen_config
        
    def get_color_palette(self) -> Dict[str, str]:
        """カラーパレット取得（プロジェクトブランディング優先）"""
        # ツールのデフォルトカラーパレット
        colors = self.get("color_palette", {}).copy()
        
        # プロジェクトブランディング設定で上書き
        branding = self.get("branding", {})
        if branding:
            if "primary_color" in branding:
                colors["primary"] = branding["primary_color"]
            if "secondary_color" in branding:
                colors["secondary"] = branding["secondary_color"]
            if "accent_color" in branding:
                colors["accent"] = branding["accent_color"]
                
        return colors
        
    def get_navigation_items(self) -> list:
        """ナビゲーション項目取得"""
        return self.get("navigation.sidebar_items", [])
        
    def get_form_fields(self, form_type: str) -> Dict[str, Any]:
        """フォーム項目設定取得"""
        return self.get(f"form_fields.{form_type}", {})
        
    def get_output_config(self) -> Dict[str, Any]:
        """出力設定取得"""
        output_config = self.get("output", {}).copy()
        
        # プロジェクト固有のディレクトリ設定を適用
        directories = self.get("directories", {})
        if "design" in directories and "base_directory" in output_config:
            # 相対パスの場合は、プロジェクトのdesignディレクトリを基準にする
            if not os.path.isabs(output_config["base_directory"]):
                output_config["base_directory"] = os.path.join(
                    directories["design"], "screens"
                )
                
        return output_config
        
    def validate_config(self) -> Dict[str, list]:
        """設定検証"""
        errors = []
        warnings = []
        
        # 必須設定の確認
        required_keys = [
            "system.name",
            "directories.docs",
            "encoding.default"
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                errors.append(f"必須設定が不足: {key}")
                
        # ツール固有の検証
        if self.tool_name == "ui-generator":
            if not self.get("image_generation.default_size"):
                errors.append("UI生成ツール: 画像サイズ設定が不足")
                
        # プロジェクト固有の検証
        if self.project_name:
            if not self.get("project_info.name"):
                warnings.append("プロジェクト名が設定されていません")
                
        return {
            "errors": errors,
            "warnings": warnings
        }
        
    def save_config(self, config: Dict[str, Any], config_type: str, name: str):
        """設定保存"""
        if config_type == "tool":
            file_path = f"{self.paths.tools_dir}/{name}.yaml"
        elif config_type == "project":
            file_path = f"{self.paths.projects_dir}/{name}.yaml"
        else:
            raise ValueError(f"不正な設定タイプ: {config_type}")
            
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            self.logger.info(f"設定保存完了: {file_path}")
        except Exception as e:
            self.logger.error(f"設定保存エラー: {file_path} - {e}")
            raise
            
    def export_merged_config(self, output_path: str, format: str = "yaml"):
        """統合設定のエクスポート"""
        merged = self.merge_configs()
        
        try:
            if format.lower() == "json":
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(merged, f, indent=2, ensure_ascii=False)
            else:  # yaml
                with open(output_path, 'w', encoding='utf-8') as f:
                    yaml.dump(merged, f, default_flow_style=False, allow_unicode=True)
                    
            self.logger.info(f"統合設定エクスポート完了: {output_path}")
        except Exception as e:
            self.logger.error(f"エクスポートエラー: {output_path} - {e}")
            raise
            
    def clear_cache(self):
        """設定キャッシュクリア"""
        self._global_config = None
        self._tool_config = None
        self._project_config = None
        self._merged_config = None
        
    def reload(self):
        """設定再読み込み"""
        self.clear_cache()
        return self.merge_configs()

# 便利関数
def create_config_manager(project_name: str = "skill-report-web", 
                         tool_name: str = "ui-generator") -> ConfigManager:
    """設定マネージャー作成"""
    return ConfigManager(project_name=project_name, tool_name=tool_name)

def get_config(key_path: str, project_name: str = "skill-report-web", 
               tool_name: str = "ui-generator", default: Any = None) -> Any:
    """設定値取得（簡易版）"""
    manager = create_config_manager(project_name, tool_name)
    return manager.get(key_path, default)

if __name__ == "__main__":
    # テスト実行
    manager = create_config_manager()
    
    print("=== 設定検証 ===")
    validation = manager.validate_config()
    if validation["errors"]:
        print("エラー:")
        for error in validation["errors"]:
            print(f"  - {error}")
    if validation["warnings"]:
        print("警告:")
        for warning in validation["warnings"]:
            print(f"  - {warning}")
            
    print("\n=== 主要設定値 ===")
    print(f"システム名: {manager.get('system.name')}")
    print(f"プロジェクト名: {manager.get('project_info.name')}")
    print(f"ツール名: {manager.get('tool_info.name')}")
    print(f"プライマリカラー: {manager.get_color_palette().get('primary')}")
    
    print("\n=== 画面設定例 ===")
    profile_config = manager.get_screen_config("profile")
    print(f"プロフィール画面: {profile_config}")
