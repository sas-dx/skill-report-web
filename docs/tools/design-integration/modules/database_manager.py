"""
設計統合ツール - データベース設計管理モジュール（完全統合版）
要求仕様ID: PLT.1-WEB.1

既存のデータベースツール機能を完全統合し、統合インターフェースを提供します。
最新のリファクタリング版データベースツールを統合し、強化された機能を提供します。
"""

import sys
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
import yaml
import json
from datetime import datetime

import sys
from pathlib import Path

# パスを追加してモジュールをインポート
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

try:
    from core.config import DesignIntegrationConfig
    from core.exceptions import DesignIntegrationError
    from core.logger import get_logger
except ImportError as e:
    print(f"インポートエラー: {e}")
    # フォールバック用の基本クラス
    class DesignIntegrationConfig:
        def __init__(self, config_path=None):
            self.project_root = Path.cwd()
        def get_database_yaml_dir(self):
            return self.project_root / "docs" / "design" / "database" / "table-details"
        def get_database_ddl_dir(self):
            return self.project_root / "docs" / "design" / "database" / "ddl"
        def get_database_tables_dir(self):
            return self.project_root / "docs" / "design" / "database" / "tables"
    
    class DesignIntegrationError(Exception):
        pass
    
    def get_logger(name):
        import logging
        return logging.getLogger(name)


class DatabaseDesignManager:
    """データベース設計管理クラス（完全統合版）"""
    
    def __init__(self, config: DesignIntegrationConfig):
        """
        初期化
        
        Args:
            config: 設計統合ツール設定
        """
        self.config = config
        self.logger = get_logger(__name__)
        
        # 統合されたデータベースツールのパス
        self.db_tools_root = config.project_root / "docs" / "tools" / "database"
        self.main_tool_path = self.db_tools_root / "db_tools_refactored.py"
        
        # 統合ツールモジュールのパス
        self.modules_path = self.db_tools_root / "modules"
        self.core_path = self.db_tools_root / "core"
        
        # パスをsys.pathに追加
        sys.path.insert(0, str(self.db_tools_root))
        sys.path.insert(0, str(self.modules_path))
        sys.path.insert(0, str(self.core_path))
        
        # 統合ツールが利用可能かチェック
        self._check_tool_availability()
        
        # 統合モジュールを初期化
        self._initialize_integrated_modules()
    
    def _check_tool_availability(self):
        """統合ツールの利用可能性をチェック"""
        if not self.main_tool_path.exists():
            raise DesignIntegrationError(
                f"統合データベースツールが見つかりません: {self.main_tool_path}"
            )
        
        required_modules = [
            self.modules_path / "yaml_validator.py",
            self.modules_path / "table_generator.py",
            self.modules_path / "consistency_checker.py"
        ]
        
        for module_path in required_modules:
            if not module_path.exists():
                raise DesignIntegrationError(
                    f"必須モジュールが見つかりません: {module_path}"
                )
    
    def _initialize_integrated_modules(self):
        """統合モジュールを初期化"""
        try:
            # 設定モジュールをインポート
            config_spec = importlib.util.spec_from_file_location(
                "db_config", self.core_path / "config.py"
            )
            config_module = importlib.util.module_from_spec(config_spec)
            config_spec.loader.exec_module(config_module)
            
            # データベースツール設定を初期化
            self.db_config = config_module.Config()
            
            # 各モジュールをインポート
            validator_spec = importlib.util.spec_from_file_location(
                "yaml_validator", self.modules_path / "yaml_validator.py"
            )
            validator_module = importlib.util.module_from_spec(validator_spec)
            validator_spec.loader.exec_module(validator_module)
            self.yaml_validator = validator_module.YAMLValidator(self.db_config)
            
            generator_spec = importlib.util.spec_from_file_location(
                "table_generator", self.modules_path / "table_generator.py"
            )
            generator_module = importlib.util.module_from_spec(generator_spec)
            generator_spec.loader.exec_module(generator_module)
            self.table_generator = generator_module.TableGenerator(self.db_config)
            
            checker_spec = importlib.util.spec_from_file_location(
                "consistency_checker", self.modules_path / "consistency_checker.py"
            )
            checker_module = importlib.util.module_from_spec(checker_spec)
            checker_spec.loader.exec_module(checker_module)
            self.consistency_checker = checker_module.ConsistencyChecker(self.db_config)
            
            self.logger.info("統合データベースモジュールの初期化が完了しました")
            
        except Exception as e:
            self.logger.warning(f"統合モジュール初期化に失敗: {e}")
            self.logger.info("フォールバックモードで動作します")
            self.yaml_validator = None
            self.table_generator = None
            self.consistency_checker = None
    
    def _execute_db_tool(self, args: List[str], verbose: bool = False) -> bool:
        """
        データベースツールを実行（フォールバック用）
        
        Args:
            args: 実行引数
            verbose: 詳細出力フラグ
            
        Returns:
            実行成功フラグ
        """
        try:
            cmd = [sys.executable, str(self.main_tool_path)] + args
            
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
        
        try:
            if self.yaml_validator:
                # 統合モジュールを使用
                success = self.yaml_validator.validate_all(verbose)
            else:
                # フォールバックモード
                args = ['validate', '--all']
                if verbose:
                    args.append('--verbose')
                success = self._execute_db_tool(args, verbose)
            
            if success:
                self.logger.info("全データベース設計の検証が完了しました")
            else:
                self.logger.error("データベース設計の検証でエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"検証実行エラー: {e}")
            return False
    
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
        
        try:
            if self.yaml_validator:
                # 統合モジュールを使用
                success = self.yaml_validator.validate_single(table_name, verbose)
            else:
                # フォールバックモード
                args = ['validate', '--table', table_name]
                if verbose:
                    args.append('--verbose')
                success = self._execute_db_tool(args, verbose)
            
            if success:
                self.logger.info(f"テーブル {table_name} の設計検証が完了しました")
            else:
                self.logger.error(f"テーブル {table_name} の設計検証でエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"テーブル検証実行エラー ({table_name}): {e}")
            return False
    
    def generate_all(self, verbose: bool = False) -> bool:
        """
        全データベース設計書を生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info("全データベース設計書の生成を開始")
        
        try:
            if self.table_generator:
                # 統合モジュールを使用
                success = self.table_generator.generate_all(verbose)
            else:
                # フォールバックモード
                args = ['generate', '--all']
                if verbose:
                    args.append('--verbose')
                success = self._execute_db_tool(args, verbose)
            
            if success:
                self.logger.info("全データベース設計書の生成が完了しました")
            else:
                self.logger.error("データベース設計書の生成でエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"生成実行エラー: {e}")
            return False
    
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
        
        try:
            if self.table_generator:
                # 統合モジュールを使用
                success = self.table_generator.generate(table_name, verbose)
            else:
                # フォールバックモード
                args = ['generate', '--table', table_name]
                if verbose:
                    args.append('--verbose')
                success = self._execute_db_tool(args, verbose)
            
            if success:
                self.logger.info(f"テーブル {table_name} の設計書生成が完了しました")
            else:
                self.logger.error(f"テーブル {table_name} の設計書生成でエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"テーブル生成実行エラー ({table_name}): {e}")
            return False
    
    def check_consistency(self, verbose: bool = False) -> bool:
        """
        データベース設計の整合性をチェック
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            チェック成功フラグ
        """
        self.logger.info("データベース設計の整合性チェックを開始")
        
        try:
            if self.consistency_checker:
                # 統合モジュールを使用
                success = self.consistency_checker.check_all(verbose)
            else:
                # フォールバックモード
                args = ['check', '--all']
                if verbose:
                    args.append('--verbose')
                success = self._execute_db_tool(args, verbose)
            
            if success:
                self.logger.info("データベース設計の整合性チェックが完了しました")
            else:
                self.logger.error("データベース設計の整合性チェックでエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"整合性チェック実行エラー: {e}")
            return False
    
    def check_table_consistency(self, table_name: str, verbose: bool = False) -> bool:
        """
        特定テーブルの整合性をチェック
        
        Args:
            table_name: テーブル名
            verbose: 詳細出力フラグ
            
        Returns:
            チェック成功フラグ
        """
        self.logger.info(f"テーブル {table_name} の整合性チェックを開始")
        
        try:
            if self.consistency_checker:
                # 統合モジュールを使用
                success = self.consistency_checker.check_single(table_name, verbose)
            else:
                # フォールバックモード
                args = ['check', '--table', table_name]
                if verbose:
                    args.append('--verbose')
                success = self._execute_db_tool(args, verbose)
            
            if success:
                self.logger.info(f"テーブル {table_name} の整合性チェックが完了しました")
            else:
                self.logger.error(f"テーブル {table_name} の整合性チェックでエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"テーブル整合性チェック実行エラー ({table_name}): {e}")
            return False
    
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
        
        try:
            if self.yaml_validator:
                # 統合モジュールを使用
                success = self.yaml_validator.validate_all(verbose)
            else:
                # フォールバックモード
                args = ['validate', '--all']
                if verbose:
                    args.append('--verbose')
                success = self._execute_db_tool(args, verbose)
            
            if success:
                self.logger.info("YAML形式の検証が完了しました")
            else:
                self.logger.error("YAML形式の検証でエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"YAML検証実行エラー: {e}")
            return False
    
    def execute_full_workflow(self, verbose: bool = False) -> bool:
        """
        完全ワークフローを実行（検証→生成→整合性チェック）
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            実行成功フラグ
        """
        self.logger.info("データベース設計の完全ワークフローを開始")
        
        success_count = 0
        total_count = 3
        
        # 1. YAML検証
        print("\n1. YAML検証を実行中...")
        if self.validate_all(verbose):
            print("✅ YAML検証完了")
            success_count += 1
        else:
            print("❌ YAML検証でエラーが発生しました")
        
        # 2. テーブル生成
        print("\n2. テーブル生成を実行中...")
        if self.generate_all(verbose):
            print("✅ テーブル生成完了")
            success_count += 1
        else:
            print("❌ テーブル生成でエラーが発生しました")
        
        # 3. 整合性チェック
        print("\n3. 整合性チェックを実行中...")
        if self.check_consistency(verbose):
            print("✅ 整合性チェック完了")
            success_count += 1
        else:
            print("❌ 整合性チェックでエラーが発生しました")
        
        # 結果サマリー
        print(f"\n📊 データベース設計ワークフロー結果: {success_count}/{total_count} 成功")
        
        if success_count == total_count:
            print("\n🎉 データベース設計の完全ワークフローが正常に完了しました！")
            self.logger.info("データベース設計の完全ワークフローが完了しました")
            return True
        else:
            print(f"\n⚠️  {total_count - success_count} 個の処理でエラーが発生しました")
            self.logger.warning(f"データベース設計ワークフローで {total_count - success_count} 個のエラーが発生しました")
            return False
    
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
                'tables_with_issues': 0,
                'validation_status': 'unknown',
                'generation_status': 'unknown',
                'consistency_status': 'unknown'
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
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        データベース設計の健全性ステータスを取得
        
        Returns:
            健全性ステータス辞書
        """
        try:
            health = {
                'overall_status': 'unknown',
                'yaml_validation': 'unknown',
                'table_generation': 'unknown',
                'consistency_check': 'unknown',
                'issues': [],
                'recommendations': [],
                'last_check': None
            }
            
            # 簡易チェックを実行
            tables = self.get_table_list()
            if not tables:
                health['issues'].append("テーブル定義が見つかりません")
                health['overall_status'] = 'error'
                return health
            
            # YAMLファイルの存在チェック
            yaml_dir = self.config.get_database_yaml_dir()
            ddl_dir = self.config.get_database_ddl_dir()
            tables_dir = self.config.get_database_tables_dir()
            
            missing_files = 0
            for table_name in tables:
                yaml_file = yaml_dir / f"テーブル詳細定義YAML_{table_name}.yaml"
                ddl_file = ddl_dir / f"{table_name}.sql"
                table_file = tables_dir / f"テーブル定義書_{table_name}_*.md"
                
                if not yaml_file.exists():
                    missing_files += 1
                    health['issues'].append(f"YAMLファイルが見つかりません: {table_name}")
            
            if missing_files == 0:
                health['yaml_validation'] = 'ok'
            elif missing_files < len(tables) * 0.1:  # 10%未満
                health['yaml_validation'] = 'warning'
            else:
                health['yaml_validation'] = 'error'
            
            # 全体ステータスを決定
            if health['yaml_validation'] == 'ok':
                health['overall_status'] = 'ok'
            elif health['yaml_validation'] == 'warning':
                health['overall_status'] = 'warning'
            else:
                health['overall_status'] = 'error'
            
            # 推奨事項を追加
            if missing_files > 0:
                health['recommendations'].append("不足しているファイルを生成してください")
            
            health['recommendations'].append("定期的な整合性チェックを実行してください")
            
            return health
            
        except Exception as e:
            self.logger.error(f"健全性ステータス取得エラー: {e}")
            return {
                'overall_status': 'error',
                'issues': [f"ステータス取得エラー: {str(e)}"],
                'recommendations': ["システム管理者に連絡してください"]
            }
