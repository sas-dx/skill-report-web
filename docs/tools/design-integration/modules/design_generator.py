"""
設計統合ツール - 設計書自動生成モジュール
要求仕様ID: PLT.1-WEB.1

データベース、API、画面設計書の自動生成を統合管理します。
"""

import sys
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

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
    
    class DesignIntegrationError(Exception):
        pass
    
    def get_logger(name):
        import logging
        return logging.getLogger(name)
from .database_manager import DatabaseDesignManager
from .api_manager import APIDesignManager
from .screen_manager import ScreenDesignManager


class DesignGenerator:
    """設計書自動生成クラス"""
    
    def __init__(self, config: DesignIntegrationConfig):
        """
        初期化
        
        Args:
            config: 設計統合ツール設定
        """
        self.config = config
        self.logger = get_logger(__name__)
        
        # 各設計管理マネージャーを初期化
        self.database_manager = DatabaseDesignManager(config)
        self.api_manager = APIDesignManager(config)
        self.screen_manager = ScreenDesignManager(config)
        
        # 生成結果
        self.generation_results = {
            'database': {},
            'api': {},
            'screen': {},
            'summary': {}
        }
    
    def generate_all_designs(self, verbose: bool = False) -> bool:
        """
        全設計書を自動生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info("全設計書の自動生成を開始")
        
        success_count = 0
        total_count = 3
        
        try:
            # 1. データベース設計生成
            print("\n1. データベース設計書生成...")
            if self.database_manager.generate_all(verbose):
                print("✅ データベース設計書生成完了")
                self.generation_results['database']['status'] = 'success'
                success_count += 1
            else:
                print("❌ データベース設計書生成でエラーが発生しました")
                self.generation_results['database']['status'] = 'error'
            
            # 2. API設計生成
            print("\n2. API設計書生成...")
            if self.api_manager.generate_all(verbose):
                print("✅ API設計書生成完了")
                self.generation_results['api']['status'] = 'success'
                success_count += 1
            else:
                print("❌ API設計書生成でエラーが発生しました")
                self.generation_results['api']['status'] = 'error'
            
            # 3. 画面設計生成
            print("\n3. 画面設計書生成...")
            if self.screen_manager.generate_all(verbose):
                print("✅ 画面設計書生成完了")
                self.generation_results['screen']['status'] = 'success'
                success_count += 1
            else:
                print("❌ 画面設計書生成でエラーが発生しました")
                self.generation_results['screen']['status'] = 'error'
            
            # 結果サマリー
            self._generate_summary(success_count, total_count)
            print(f"\n📊 設計書生成結果: {success_count}/{total_count} 成功")
            
            if verbose:
                self._print_detailed_results()
            
            if success_count == total_count:
                print("\n🎉 全設計書の自動生成が正常に完了しました！")
                self.logger.info("全設計書の自動生成が完了しました")
                return True
            else:
                print(f"\n⚠️  {total_count - success_count} 個の生成でエラーが発生しました")
                self.logger.warning(f"設計書生成で {total_count - success_count} 個のエラーが発生しました")
                return False
                
        except Exception as e:
            self.logger.error(f"設計書生成実行エラー: {e}")
            return False
    
    def generate_by_type(self, design_type: str, verbose: bool = False) -> bool:
        """
        特定設計タイプの設計書を生成
        
        Args:
            design_type: 設計タイプ（database, api, screen）
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info(f"{design_type} 設計書の生成を開始")
        
        try:
            if design_type == 'database':
                success = self.database_manager.generate_all(verbose)
                self.generation_results['database']['status'] = 'success' if success else 'error'
            elif design_type == 'api':
                success = self.api_manager.generate_all(verbose)
                self.generation_results['api']['status'] = 'success' if success else 'error'
            elif design_type == 'screen':
                success = self.screen_manager.generate_all(verbose)
                self.generation_results['screen']['status'] = 'success' if success else 'error'
            else:
                self.logger.error(f"不明な設計タイプ: {design_type}")
                return False
            
            if success:
                self.logger.info(f"{design_type} 設計書の生成が完了しました")
            else:
                self.logger.error(f"{design_type} 設計書の生成でエラーが発生しました")
            
            return success
                
        except Exception as e:
            self.logger.error(f"{design_type} 設計書生成実行エラー: {e}")
            return False
    
    def generate_by_requirement(self, requirement_id: str, verbose: bool = False) -> bool:
        """
        特定要求仕様IDに関連する設計書を生成
        
        Args:
            requirement_id: 要求仕様ID
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        self.logger.info(f"要求仕様ID {requirement_id} に関連する設計書の生成を開始")
        
        try:
            success_count = 0
            total_count = 0
            
            # 要求仕様IDに関連するテーブルを検索・生成
            related_tables = self._find_related_tables(requirement_id)
            if related_tables:
                total_count += 1
                print(f"\n関連テーブル生成: {', '.join(related_tables)}")
                table_success = True
                for table_name in related_tables:
                    if not self.database_manager.generate_table(table_name, verbose):
                        table_success = False
                
                if table_success:
                    print("✅ 関連テーブル生成完了")
                    success_count += 1
                else:
                    print("❌ 関連テーブル生成でエラーが発生しました")
            
            # 要求仕様IDに関連するAPIを検索・生成
            related_apis = self._find_related_apis(requirement_id)
            if related_apis:
                total_count += 1
                print(f"\n関連API生成: {', '.join(related_apis)}")
                api_success = True
                for api_id in related_apis:
                    if not self.api_manager.generate_api(api_id, verbose):
                        api_success = False
                
                if api_success:
                    print("✅ 関連API生成完了")
                    success_count += 1
                else:
                    print("❌ 関連API生成でエラーが発生しました")
            
            # 要求仕様IDに関連する画面を検索・生成
            related_screens = self._find_related_screens(requirement_id)
            if related_screens:
                total_count += 1
                print(f"\n関連画面生成: {', '.join(related_screens)}")
                screen_success = True
                for screen_id in related_screens:
                    if not self.screen_manager.generate_screen(screen_id, verbose):
                        screen_success = False
                
                if screen_success:
                    print("✅ 関連画面生成完了")
                    success_count += 1
                else:
                    print("❌ 関連画面生成でエラーが発生しました")
            
            if total_count == 0:
                print(f"⚠️  要求仕様ID {requirement_id} に関連する設計書が見つかりませんでした")
                return False
            
            print(f"\n📊 要求仕様ID {requirement_id} 関連生成結果: {success_count}/{total_count} 成功")
            
            if success_count == total_count:
                print(f"\n🎉 要求仕様ID {requirement_id} に関連する設計書の生成が完了しました！")
                self.logger.info(f"要求仕様ID {requirement_id} 関連設計書の生成が完了しました")
                return True
            else:
                print(f"\n⚠️  {total_count - success_count} 個の生成でエラーが発生しました")
                self.logger.warning(f"要求仕様ID {requirement_id} 関連設計書生成で {total_count - success_count} 個のエラーが発生しました")
                return False
                
        except Exception as e:
            self.logger.error(f"要求仕様ID関連設計書生成実行エラー ({requirement_id}): {e}")
            return False
    
    def generate_database_designs(self, verbose: bool = False) -> bool:
        """
        データベース設計書を生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        return self.database_manager.generate_all(verbose)
    
    def generate_api_designs(self, verbose: bool = False) -> bool:
        """
        API設計書を生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        return self.api_manager.generate_all(verbose)
    
    def generate_screen_designs(self, verbose: bool = False) -> bool:
        """
        画面設計書を生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            生成成功フラグ
        """
        return self.screen_manager.generate_all(verbose)
    
    def _find_related_tables(self, requirement_id: str) -> List[str]:
        """要求仕様IDに関連するテーブルを検索"""
        related_tables = []
        
        try:
            yaml_dir = self.config.get_database_yaml_dir()
            if yaml_dir.exists():
                for yaml_file in yaml_dir.glob("*.yaml"):
                    if yaml_file.name.startswith("テーブル詳細定義YAML_"):
                        try:
                            with open(yaml_file, 'r', encoding='utf-8') as f:
                                content = f.read()
                            if requirement_id in content:
                                table_name = yaml_file.stem.replace("テーブル詳細定義YAML_", "")
                                related_tables.append(table_name)
                        except:
                            pass
        except Exception as e:
            self.logger.warning(f"関連テーブル検索エラー: {e}")
        
        return related_tables
    
    def _find_related_apis(self, requirement_id: str) -> List[str]:
        """要求仕様IDに関連するAPIを検索"""
        related_apis = []
        
        try:
            api_specs_dir = self.config.project_root / "docs" / "design" / "api" / "specs"
            if api_specs_dir.exists():
                for api_file in api_specs_dir.glob("API定義書_*.md"):
                    try:
                        with open(api_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if requirement_id in content:
                            # API IDを抽出
                            import re
                            api_match = re.search(r'API定義書_API-(\d+)_', api_file.name)
                            if api_match:
                                api_id = f"API-{api_match.group(1)}"
                                related_apis.append(api_id)
                    except:
                        pass
        except Exception as e:
            self.logger.warning(f"関連API検索エラー: {e}")
        
        return related_apis
    
    def _find_related_screens(self, requirement_id: str) -> List[str]:
        """要求仕様IDに関連する画面を検索"""
        related_screens = []
        
        try:
            screen_specs_dir = self.config.project_root / "docs" / "design" / "screens" / "specs"
            if screen_specs_dir.exists():
                for screen_file in screen_specs_dir.glob("画面設計書_*.md"):
                    try:
                        with open(screen_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if requirement_id in content:
                            # 画面IDを抽出
                            import re
                            screen_match = re.search(r'画面設計書_SCR-([A-Z]+)_', screen_file.name)
                            if screen_match:
                                screen_id = f"SCR-{screen_match.group(1)}"
                                related_screens.append(screen_id)
                    except:
                        pass
        except Exception as e:
            self.logger.warning(f"関連画面検索エラー: {e}")
        
        return related_screens
    
    def _generate_summary(self, success_count: int, total_count: int):
        """結果サマリーを生成"""
        self.generation_results['summary'] = {
            'total_success': success_count,
            'total_count': total_count,
            'success_rate': (success_count / total_count * 100) if total_count > 0 else 0,
            'overall_status': 'success' if success_count == total_count else 'partial' if success_count > 0 else 'error'
        }
    
    def _print_detailed_results(self):
        """詳細結果を出力"""
        print("\n📋 詳細結果:")
        
        # データベース設計結果
        db_status = self.generation_results['database'].get('status', 'unknown')
        print(f"  - データベース設計: {self._get_status_emoji(db_status)} {db_status}")
        
        # API設計結果
        api_status = self.generation_results['api'].get('status', 'unknown')
        print(f"  - API設計: {self._get_status_emoji(api_status)} {api_status}")
        
        # 画面設計結果
        screen_status = self.generation_results['screen'].get('status', 'unknown')
        print(f"  - 画面設計: {self._get_status_emoji(screen_status)} {screen_status}")
        
        # サマリー情報
        summary = self.generation_results.get('summary', {})
        if summary:
            print(f"\n📊 サマリー:")
            print(f"  - 成功率: {summary.get('success_rate', 0):.1f}%")
            print(f"  - 全体ステータス: {self._get_status_emoji(summary.get('overall_status', 'unknown'))} {summary.get('overall_status', 'unknown')}")
    
    def _get_status_emoji(self, status: str) -> str:
        """ステータスに対応する絵文字を取得"""
        status_emojis = {
            'success': '✅',
            'error': '❌',
            'partial': '⚠️',
            'unknown': '❓'
        }
        return status_emojis.get(status, '❓')
    
    def get_generation_results(self) -> Dict[str, Any]:
        """生成結果を取得"""
        return self.generation_results
    
    def export_results(self, output_path: Path) -> bool:
        """結果をファイルに出力"""
        try:
            import json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.generation_results, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"生成結果を出力しました: {output_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"結果出力エラー: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """生成統計情報を取得"""
        try:
            stats = {
                'database': {
                    'total_tables': len(self.database_manager.get_table_list()),
                    'status': self.generation_results['database'].get('status', 'unknown')
                },
                'api': {
                    'total_apis': len(self.api_manager.get_api_list()),
                    'status': self.generation_results['api'].get('status', 'unknown')
                },
                'screen': {
                    'total_screens': len(self.screen_manager.get_screen_list()),
                    'status': self.generation_results['screen'].get('status', 'unknown')
                },
                'summary': self.generation_results.get('summary', {})
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"統計情報取得エラー: {e}")
            return {}
    
    def validate_before_generation(self, verbose: bool = False) -> bool:
        """
        生成前の検証を実行
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            検証成功フラグ
        """
        self.logger.info("生成前検証を開始")
        
        try:
            success_count = 0
            total_count = 3
            
            # データベース設計検証
            if self.database_manager.validate_all(verbose):
                success_count += 1
            
            # API設計検証
            if self.api_manager.validate_all(verbose):
                success_count += 1
            
            # 画面設計検証
            if self.screen_manager.validate_all(verbose):
                success_count += 1
            
            if success_count == total_count:
                self.logger.info("生成前検証が完了しました")
                return True
            else:
                self.logger.warning(f"生成前検証で {total_count - success_count} 個のエラーが発生しました")
                return False
                
        except Exception as e:
            self.logger.error(f"生成前検証エラー: {e}")
            return False
