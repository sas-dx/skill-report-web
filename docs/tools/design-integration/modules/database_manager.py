"""
設計統合ツール - データベース設計管理モジュール
要求仕様ID: PLT.1-WEB.1

既存のデータベースツール機能をラップし、統合インターフェースを提供します。
"""

import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

from ..core.config import DesignIntegrationConfig
from ..core.exceptions import DesignIntegrationError
from ..core.logger import get_logger


class DatabaseDesignManager:
    """データベース設計管理クラス"""
    
    def __init__(self, config: DesignIntegrationConfig):
        """
        初期化
        
        Args:
            config: 設計統合ツール設定
        """
        self.config = config
        self.logger = get_logger(__name__)
        
        # 既存データベースツールのパス
        self.db_tools_path = config.project_root / "docs" / "design" / "database" / "tools"
        self.legacy_tool_path = self.db_tools_path / "db_tools_refactored.py"
        
        # 新しい統合ツールのパス
        self.integrated_tool_path = config.project_root / "docs" / "tools" / "database" / "db_tools_refactored.py"
        
        # 既存ツールが利用可能かチェック
        self._check_tool_availability()
    
    def _check_tool_availability(self):
        """既存ツールの利用可能性をチェック"""
        if not self.legacy_tool_path.exists() and not self.integrated_tool_path.exists():
            raise DesignIntegrationError(
                f"データベースツールが見つかりません: {self.legacy_tool_path} または {self.integrated_tool_path}"
            )
    
    def _get_available_tool_path(self) -> Path:
        """利用可能なツールパスを取得"""
        if self.integrated_tool_path.exists():
            return self.integrated_tool_path
        elif self.legacy_tool_path.exists():
            return self.legacy_tool_path
        else:
            raise DesignIntegrationError("利用可能なデータベースツールが見つかりません")
    
    def _execute_db_tool(self, args: List[str], verbose: bool = False) -> bool:
        """
        データベースツールを実行
        
        Args:
            args: 実行引数
            verbose: 詳細出力フラグ
            
        Returns:
            実行成功フラグ
        """
        try:
            tool_path = self._get_available_tool_path()
            cmd = [sys.executable, str(tool_path)] + args
            
            if verbose:
                self.logger.info(f"実行コマンド: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.config.project_root)
            )
            
            if verbose or result.returncode != 0:
                if result.stdout:
                    print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            
            return result.returncode == 0
            
        except Exception as e:
            self.logger.error(f"データベースツール実行エラー: {e}")
            return False
    
    def validate_all(self, verbose: bool = False) -> bool:
        """
        全データベース設計を検証
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info("全データベース設計の検証を開始")
        
        args = ['validate', '--all']
        if verbose:
            args.append('--verbose')
        
        success = self._execute_db_tool(args, verbose)
        
        if success:
            self.logger.info("全データベース設計の検証が完了しました")
        else:
            self.logger.error("データベース設計の検証でエラーが発生しました")
        
        return success
    
    def validate_table(self, table_name: str, verbose: bool = False) -> bool:
        """
        特定テーブルの設計を検証
        
        Args:
            table_name: テーブル名
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info(f"テーブル {table_name} の設計検証を開始")
        
        args = ['validate', '--table', table_name]
        if verbose:
            args.append('--verbose')
        
        success = self._execute_db_tool(args, verbose)
        
        if success:
            self.logger.info(f"テーブル {table_name} の設計検証が完了しました")
        else:
            self.logger.error(f"テーブル {table_name} の設計検証でエラーが発生しました")
        
        return success
    
    def generate_all(self, verbose: bool = False) -> bool:
        """
        全データベース設計書を生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info("全データベース設計書の生成を開始")
        
        args = ['generate', '--all']
        if verbose:
            args.append('--verbose')
        
        success = self._execute_db_tool(args, verbose)
        
        if success:
            self.logger.info("全データベース設計書の生成が完了しました")
        else:
            self.logger.error("データベース設計書の生成でエラーが発生しました")
        
        return success
    
    def generate_table(self, table_name: str, verbose: bool = False) -> bool:
        """
        特定テーブルの設計書を生成
        
        Args:
            table_name: テーブル名
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info(f"テーブル {table_name} の設計書生成を開始")
        
        args = ['generate', '--table', table_name]
        if verbose:
            args.append('--verbose')
        
        success = self._execute_db_tool(args, verbose)
        
        if success:
            self.logger.info(f"テーブル {table_name} の設計書生成が完了しました")
        else:
            self.logger.error(f"テーブル {table_name} の設計書生成でエラーが発生しました")
        
        return success
    
    def check_consistency(self, verbose: bool = False) -> bool:
        """
        データベース設計の整合性をチェック
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            チェック成功フラグ
        """
        self.logger.info("データベース設計の整合性チェックを開始")
        
        args = ['check', '--all']
        if verbose:
            args.append('--verbose')
        
        success = self._execute_db_tool(args, verbose)
        
        if success:
            self.logger.info("データベース設計の整合性チェックが完了しました")
        else:
            self.logger.error("データベース設計の整合性チェックでエラーが発生しました")
        
        return success
    
    def get_table_list(self) -> List[str]:
        """
        テーブル一覧を取得
        
        Returns:
            テーブル名のリスト
        """
        try:
            yaml_dir = self.config.get_database_yaml_dir()
            if not yaml_dir.exists():
                return []
            
            tables = []
            for yaml_file in yaml_dir.glob("*.yaml"):
                if yaml_file.name.startswith("テーブル詳細定義YAML_"):
                    # ファイル名からテーブル名を抽出
                    table_name = yaml_file.stem.replace("テーブル詳細定義YAML_", "")
                    tables.append(table_name)
            
            return sorted(tables)
            
        except Exception as e:
            self.logger.error(f"テーブル一覧取得エラー: {e}")
            return []
    
    def get_table_info(self, table_name: str) -> Optional[Dict[str, Any]]:
        """
        テーブル情報を取得
        
        Args:
            table_name: テーブル名
            
        Returns:
            テーブル情報辞書
        """
        try:
            yaml_file = self.config.get_database_yaml_dir() / f"テーブル詳細定義YAML_{table_name}.yaml"
            
            if not yaml_file.exists():
                return None
            
            import yaml
            with open(yaml_file, 'r', encoding='utf-8') as f:
                table_data = yaml.safe_load(f)
            
            return table_data
            
        except Exception as e:
            self.logger.error(f"テーブル情報取得エラー ({table_name}): {e}")
            return None
    
    def validate_yaml_format(self, verbose: bool = False) -> bool:
        """
        YAML形式の検証
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info("YAML形式の検証を開始")
        
        args = ['yaml-check', '--all']
        if verbose:
            args.append('--verbose')
        
        success = self._execute_db_tool(args, verbose)
        
        if success:
            self.logger.info("YAML形式の検証が完了しました")
        else:
            self.logger.error("YAML形式の検証でエラーが発生しました")
        
        return success
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        データベース設計の統計情報を取得
        
        Returns:
            統計情報辞書
        """
        try:
            tables = self.get_table_list()
            
            stats = {
                'total_tables': len(tables),
                'master_tables': 0,
                'transaction_tables': 0,
                'history_tables': 0,
                'system_tables': 0,
                'work_tables': 0,
                'tables_by_category': {},
                'total_columns': 0,
                'tables_with_issues': 0
            }
            
            for table_name in tables:
                table_info = self.get_table_info(table_name)
                if table_info:
                    # カテゴリ別集計
                    category = table_info.get('category', 'その他')
                    if category not in stats['tables_by_category']:
                        stats['tables_by_category'][category] = 0
                    stats['tables_by_category'][category] += 1
                    
                    # プレフィックス別集計
                    if table_name.startswith('MST_'):
                        stats['master_tables'] += 1
                    elif table_name.startswith('TRN_'):
                        stats['transaction_tables'] += 1
                    elif table_name.startswith('HIS_'):
                        stats['history_tables'] += 1
                    elif table_name.startswith('SYS_'):
                        stats['system_tables'] += 1
                    elif table_name.startswith('WRK_'):
                        stats['work_tables'] += 1
                    
                    # カラム数集計
                    columns = table_info.get('columns', [])
                    stats['total_columns'] += len(columns)
            
            return stats
            
        except Exception as e:
            self.logger.error(f"統計情報取得エラー: {e}")
            return {}
