#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 設定管理

ツール全体で使用する設定値・定数を管理します。

対応要求仕様ID: PLT.2-TOOL.1
"""

import os
from pathlib import Path
from typing import Dict, Any


class Config:
    """設定管理クラス
    
    ツール全体で使用する設定値・定数を管理します。
    環境変数からの設定読み込みにも対応しています。
    """
    
    # デフォルト設定値
    DEFAULT_CONFIG = {
        # ディレクトリ設定
        'base_dir': None,  # 実行時に設定
        'tables_dir': 'tables',
        'ddl_dir': 'ddl',
        'details_dir': 'table-details',
        'data_dir': 'data',
        
        # ファイル名設定
        'table_list_file': 'テーブル一覧.md',
        'all_ddl_file': 'all_tables.sql',
        
        # データ生成設定
        'default_sample_count': 10,
        'default_seed': 12345,
        'max_sample_count': 10000,
        'batch_insert_size': 1000,
        
        # ログ設定
        'enable_color': True,
        'log_level': 'INFO',
        
        # Faker設定
        'faker_locale': 'ja_JP',
        'faker_seed': None,
        
        # データベース設定
        'default_charset': 'utf8mb4',
        'default_collation': 'utf8mb4_unicode_ci',
        
        # ファイル出力設定
        'output_encoding': 'utf-8',
        'line_ending': '\n',
        
        # テンプレート設定
        'table_definition_template': None,
        'ddl_template': None,
        
        # 業務固有設定
        'company_domain': 'company.com',
        'default_department_prefix': 'DEPT_',
        'default_employee_prefix': 'EMP',
        'default_skill_prefix': 'SKL_',
        
        # データ生成ルール
        'skill_levels': [1, 2, 3, 4],
        'skill_level_weights': [10, 30, 40, 20],
        'department_distribution': {
            'DEPT_DEV': 40,    # 開発部40%
            'DEPT_SYS': 20,    # システム部20%
            'DEPT_BIZ': 30,    # 業務部30%
            'DEPT_MGT': 10     # 管理部10%
        }
    }
    
    def __init__(self, base_dir: str = None, config_file: str = None):
        """初期化
        
        Args:
            base_dir (str, optional): ベースディレクトリ
            config_file (str, optional): 設定ファイルパス
        """
        self._config = self.DEFAULT_CONFIG.copy()
        
        # ベースディレクトリ設定
        if base_dir:
            self._config['base_dir'] = Path(base_dir)
        else:
            # スクリプトのディレクトリを基準とする
            self._config['base_dir'] = Path(__file__).parent.parent.parent.parent / 'docs' / 'design' / 'database'
        
        # 環境変数から設定を読み込み
        self._load_from_env()
        
        # 設定ファイルから読み込み（将来拡張用）
        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)
    
    def _load_from_env(self):
        """環境変数から設定を読み込み"""
        env_mappings = {
            'TABLE_GEN_BASE_DIR': 'base_dir',
            'TABLE_GEN_SAMPLE_COUNT': 'default_sample_count',
            'TABLE_GEN_SEED': 'default_seed',
            'TABLE_GEN_ENABLE_COLOR': 'enable_color',
            'TABLE_GEN_FAKER_LOCALE': 'faker_locale',
            'TABLE_GEN_COMPANY_DOMAIN': 'company_domain',
        }
        
        for env_key, config_key in env_mappings.items():
            env_value = os.getenv(env_key)
            if env_value:
                # 型変換
                if config_key in ['default_sample_count', 'default_seed']:
                    self._config[config_key] = int(env_value)
                elif config_key == 'enable_color':
                    self._config[config_key] = env_value.lower() in ('true', '1', 'yes')
                elif config_key == 'base_dir':
                    self._config[config_key] = Path(env_value)
                else:
                    self._config[config_key] = env_value
    
    def _load_from_file(self, config_file: str):
        """設定ファイルから読み込み（将来拡張用）
        
        Args:
            config_file (str): 設定ファイルパス
        """
        # TODO: YAML/JSON設定ファイル対応
        pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """設定値を取得
        
        Args:
            key (str): 設定キー
            default (Any, optional): デフォルト値
            
        Returns:
            Any: 設定値
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any):
        """設定値を設定
        
        Args:
            key (str): 設定キー
            value (Any): 設定値
        """
        self._config[key] = value
    
    def get_base_dir(self) -> Path:
        """ベースディレクトリを取得
        
        Returns:
            Path: ベースディレクトリパス
        """
        return self._config['base_dir']
    
    def get_tables_dir(self) -> Path:
        """テーブル定義書出力ディレクトリを取得
        
        Returns:
            Path: テーブル定義書出力ディレクトリパス
        """
        return self.get_base_dir() / self._config['tables_dir']
    
    def get_ddl_dir(self) -> Path:
        """DDL出力ディレクトリを取得
        
        Returns:
            Path: DDL出力ディレクトリパス
        """
        return self.get_base_dir() / self._config['ddl_dir']
    
    def get_details_dir(self) -> Path:
        """テーブル詳細定義ディレクトリを取得
        
        Returns:
            Path: テーブル詳細定義ディレクトリパス
        """
        return self.get_base_dir() / self._config['details_dir']
    
    def get_data_dir(self) -> Path:
        """データ出力ディレクトリを取得
        
        Returns:
            Path: データ出力ディレクトリパス
        """
        return self.get_base_dir() / self._config['data_dir']
    
    def get_table_list_file(self) -> Path:
        """テーブル一覧ファイルパスを取得
        
        Returns:
            Path: テーブル一覧ファイルパス
        """
        return self.get_base_dir() / self._config['table_list_file']
    
    def get_all_config(self) -> Dict[str, Any]:
        """全設定を取得
        
        Returns:
            Dict[str, Any]: 全設定の辞書
        """
        return self._config.copy()
    
    def update_config(self, config_dict: Dict[str, Any]):
        """設定を一括更新
        
        Args:
            config_dict (Dict[str, Any]): 更新する設定の辞書
        """
        self._config.update(config_dict)
    
    def ensure_directories(self):
        """必要なディレクトリを作成"""
        directories = [
            self.get_tables_dir(),
            self.get_ddl_dir(),
            self.get_details_dir(),
            self.get_data_dir()
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def validate_config(self) -> bool:
        """設定値の妥当性をチェック
        
        Returns:
            bool: 設定が妥当かどうか
        """
        try:
            # 必須ディレクトリの存在チェック
            base_dir = self.get_base_dir()
            if not base_dir.exists():
                return False
            
            # 数値設定の範囲チェック
            sample_count = self.get('default_sample_count')
            if not isinstance(sample_count, int) or sample_count <= 0:
                return False
            
            max_count = self.get('max_sample_count')
            if not isinstance(max_count, int) or max_count <= 0:
                return False
            
            if sample_count > max_count:
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
