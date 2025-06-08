#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 設定管理（統合設定への移行）

統合設定システムを使用するためのラッパークラス。
後方互換性を保ちながら、統合設定に移行します。

対応要求仕様ID: PLT.2-TOOL.1
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# 統合設定をインポート
sys.path.append(str(Path(__file__).parent.parent.parent / "shared"))
from core.config import get_config as get_unified_config, DatabaseToolsConfig


class Config:
    """設定管理クラス（統合設定へのラッパー）
    
    既存のtable_generatorコードとの互換性を保ちながら、
    統合設定システムを使用します。
    """
    
    def __init__(self, base_dir: str = None, config_file: str = None):
        """初期化
        
        Args:
            base_dir (str, optional): ベースディレクトリ
            config_file (str, optional): 設定ファイルパス（未使用）
        """
        self._unified_config = get_unified_config()
        
        # ベースディレクトリが指定された場合は更新
        if base_dir:
            self._unified_config.base_dir = Path(base_dir)
            # ディレクトリパスを再計算
            self._unified_config.__post_init__()
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得（後方互換性のため）
        
        Args:
            key (str): 設定キー
            default (Any, optional): デフォルト値
            
        Returns:
            Any: 設定値
        """
        # 統合設定の属性にマッピング
        mapping = {
            'base_dir': self._unified_config.base_dir,
            'tables_dir': 'tables',
            'ddl_dir': 'ddl',
            'details_dir': 'table-details',
            'data_dir': 'data',
            'table_list_file': 'テーブル一覧.md',
            'all_ddl_file': 'all_tables.sql',
            'default_sample_count': self._unified_config.default_sample_count,
            'default_seed': self._unified_config.default_seed,
            'max_sample_count': self._unified_config.max_sample_count,
            'batch_insert_size': self._unified_config.batch_insert_size,
            'enable_color': True,  # 統合設定では未対応
            'log_level': self._unified_config.log_level.value,
            'faker_locale': self._unified_config.faker_locale,
            'faker_seed': self._unified_config.faker_seed,
            'default_charset': self._unified_config.default_charset,
            'default_collation': self._unified_config.default_collation,
            'output_encoding': self._unified_config.output_encoding,
            'line_ending': self._unified_config.line_ending,
            'company_domain': self._unified_config.company_domain,
            'default_department_prefix': self._unified_config.default_department_prefix,
            'default_employee_prefix': self._unified_config.default_employee_prefix,
            'default_skill_prefix': self._unified_config.default_skill_prefix,
            'skill_levels': self._unified_config.skill_levels,
            'skill_level_weights': self._unified_config.skill_level_weights,
            'department_distribution': self._unified_config.department_distribution,
        }
        
        return mapping.get(key, default)
    
    def set(self, key: str, value: Any):
        """設定値を設定（後方互換性のため）
        
        Args:
            key (str): 設定キー
            value (Any): 設定値
        """
        # 統合設定の属性に反映
        if key == 'default_sample_count':
            self._unified_config.default_sample_count = value
        elif key == 'default_seed':
            self._unified_config.default_seed = value
        elif key == 'faker_locale':
            self._unified_config.faker_locale = value
        elif key == 'company_domain':
            self._unified_config.company_domain = value
        # 他の設定も必要に応じて追加
    
    def get_base_dir(self) -> Path:
        """ベースディレクトリを取得"""
        return self._unified_config.base_dir
    
    def get_tables_dir(self) -> Path:
        """テーブル定義書出力ディレクトリを取得"""
        return self._unified_config.tables_dir
    
    def get_ddl_dir(self) -> Path:
        """DDL出力ディレクトリを取得"""
        return self._unified_config.ddl_dir
    
    def get_details_dir(self) -> Path:
        """テーブル詳細定義ディレクトリを取得"""
        return self._unified_config.table_details_dir
    
    def get_data_dir(self) -> Path:
        """データ出力ディレクトリを取得"""
        return self._unified_config.data_dir
    
    def get_table_list_file(self) -> Path:
        """テーブル一覧ファイルパスを取得"""
        return self._unified_config.base_dir / "テーブル一覧.md"
    
    def get_all_config(self) -> Dict[str, Any]:
        """全設定を取得"""
        return self._unified_config.to_dict()
    
    def update_config(self, config_dict: Dict[str, Any]):
        """設定を一括更新"""
        for key, value in config_dict.items():
            self.set(key, value)
    
    def ensure_directories(self):
        """必要なディレクトリを作成"""
        self._unified_config._ensure_directories()
    
    def validate_config(self) -> bool:
        """設定値の妥当性をチェック"""
        try:
            # 基本的な妥当性チェック
            if not self._unified_config.base_dir.exists():
                return False
            
            if self._unified_config.default_sample_count <= 0:
                return False
            
            if self._unified_config.max_sample_count <= 0:
                return False
            
            if self._unified_config.default_sample_count > self._unified_config.max_sample_count:
                return False
            
            return True
            
        except Exception:
            return False


# グローバル設定インスタンス
_global_config = None


def get_config(base_dir: str = None) -> Config:
    """グローバル設定インスタンスを取得
    
    Args:
        base_dir (str, optional): ベースディレクトリ
        
    Returns:
        Config: 設定インスタンス
    """
    global _global_config
    if _global_config is None:
        _global_config = Config(base_dir)
    return _global_config


def reset_config():
    """グローバル設定をリセット"""
    global _global_config
    _global_config = None
