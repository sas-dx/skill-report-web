#!/usr/bin/env python3
"""
設計統合ツール - メインインターフェース（データベースツール昇格版）
要求仕様ID: PLT.1-WEB.1

データベースツールを設計統合ツールに昇格させた統合インターフェースです：
1. 強化データベース設計管理
2. API設計管理
3. 画面設計管理
4. 統合レポート生成
5. 設計整合性チェック
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime

# パスを追加してモジュールをインポート
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from core.config import DesignIntegrationConfig
    from core.exceptions import DesignIntegrationError
    from core.logger import get_logger
    from modules.enhanced_database_manager import EnhancedDatabaseDesignManager
    from modules.database_manager import DatabaseDesignManager
    from modules.api_manager import APIDesignManager
    from modules.screen_manager import ScreenDesignManager
    from modules.report_generator import ReportGenerator
    from modules.integration_checker import IntegrationChecker
    from modules.design_generator import DesignGenerator
except ImportError as e:
    print(f"インポートエラー: {e}")
    print("フォールバックモードで動作します")
    
    # フォールバック用の基本クラス
    class DesignIntegrationConfig:
        def __init__(self, config_path=None):
            self.project_root = Path.cwd()
    
    class DesignIntegrationError(Exception):
        pass
    
    def get_logger(name):
        import logging
        return logging.getLogger(name)
    
    # フォールバック用のダミークラス
    class EnhancedDatabaseDesignManager:
        def __init__(self, config):
            self.config = config
            print("⚠️  強化データベース管理モジュールが利用できません")
        
        def execute_enhanced_workflow(self, verbose=False):
            print("❌ 強化ワークフローは利用できません")
            return {'overall_success': False, 'error': 'モジュール未利用'}


class DesignIntegrationTools:
    """設計統合ツール - メインクラス（データベースツール昇格版）"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初期化
        
        Args:
            config_path: 設定ファイルパス
        """
        self.config = DesignIntegrationConfig(config_path)
        self.logger = get_logger(__name__)
        
        # 各管理モジュールを初期化
        self._initialize_managers()
        
        self.logger.info("設計統合ツール（データベースツール昇格版）が初期化されました")
    
    def _initialize_managers(self):
        """管理モジュールを初期化"""
        try:
            # 強化データベース設計管理（メイン機能）
            self.enhanced_db_manager = EnhancedDatabaseDesignManager(self.config)
            
            # 基本データベース設計管理（フォールバック）
            self.db_manager = DatabaseDesignManager(self.config)
            
            # その他の設計管理モジュール
            self.api_manager = APIDesignManager(self.config)
            self.screen_manager = ScreenDesignManager(self.config)
            self.report_generator = ReportGenerator(self.config)
            self.integration_checker = IntegrationChecker(self.config)
            self.design_generator = DesignGenerator(self.config)
            
            self.logger.info("全管理モジュールの初期化が完了しました")
            
        except Exception as e:
            self.logger.error(f"管理モジュール初期化エラー: {e}")
            # フォールバックモードで継続
            self.enhanced_db_manager = None
            self.db_manager = None
    
    def execute_database_enhanced_workflow(self, verbose: bool = False) -> Dict[str, Any]:
        """
        強化データベース設計ワークフローを実行
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            実行結果辞書
        """
        print("\n" + "="*100)
        print("🚀 強化データベース設計ワークフロー実行")
        print("="*100)
        
        if not self.enhanced_db_manager:
            print("❌ 強化データベース管理モジュールが利用できません")
            return {'overall_success': False, 'error': 'モジュール未利用'}
        
        try:
            # 強化ワークフローを実行
            result = self.enhanced_db_manager.execute_enhanced_workflow(verbose)
            
            # 結果サマリーを表示
            if result.get('overall_success', False):
                print("\n🎉 強化データベース設計ワークフローが正常に完了しました！")
                print(f"成功率: {result.get('summary', {}).get('success_rate', 0):.1f}%")
                print(f"健全性スコア: {result.get('summary', {}).get('health_score', 0):.1f}/100.0")
            else:
                print("\n⚠️  強化ワークフローで問題が発生しました")
                if 'error' in result:
                    print(f"エラー: {result['error']}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"強化ワークフロー実行エラー: {e}")
            return {'overall_success': False, 'error': str(e)}
    
    def execute_database_basic_workflow(self, verbose: bool = False) -> Dict[str, Any]:
        """
        基本データベース設計ワークフローを実行
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            実行結果辞書
        """
        print("\n" + "="*80)
        print("🔧 基本データベース設計ワークフロー実行")
        print("="*80)
        
        if not self.db_manager:
            print("❌ データベース管理モジュールが利用できません")
            return {'overall_success': False, 'error': 'モジュール未利用'}
        
        try:
            # 基本ワークフローを実行
            result = self.db_manager.execute_full_workflow(verbose)
            
            print(f"\n📋 基本ワークフロー完了: {'成功' if result else '失敗'}")
            return {'overall_success': result}
            
        except Exception as e:
            self.logger.error(f"基本ワークフロー実行エラー: {e}")
            return {'overall_success': False, 'error': str(e)}
    
    def generate_comprehensive_database_report(self, verbose: bool = False) -> Dict[str, Any]:
        """
        包括的データベースレポートを生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            レポート辞書
        """
        print("\n📊 包括的データベースレポート生成")
        
        if not self.enhanced_db_manager:
            print("❌ 強化データベース管理モジュールが利用できません")
            return {}
        
        try:
            report = self.enhanced_db_manager.generate_comprehensive_report(verbose)
            
            if report:
                print("✅ 包括的レポート生成完了")
                if verbose:
                    self._print_report_summary(report)
            else:
                print("❌ レポート生成に失敗しました")
            
            return report
            
        except Exception as e:
            self.logger.error(f"包括的レポート生成エラー: {e}")
            return {}
    
    def optimize_database_design(self, verbose: bool = False) -> Dict[str, Any]:
        """
        データベース設計最適化を実行
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            最適化提案辞書
        """
        print("\n🔧 データベース設計最適化分析")
        
        if not self.enhanced_db_manager:
            print("❌ 強化データベース管理モジュールが利用できません")
            return {}
        
        try:
            optimization = self.enhanced_db_manager.optimize_database_design(verbose)
            
            if optimization:
                print("✅ 最適化分析完了")
                suggestions_count = len(optimization.get('suggestions', []))
                print(f"最適化提案数: {suggestions_count}")
            else:
                print("❌ 最適化分析に失敗しました")
            
            return optimization
            
        except Exception as e:
            self.logger.error(f"最適化分析エラー: {e}")
            return {}
    
    def validate_database_design(self, verbose: bool = False) -> Dict[str, Any]:
        """
        データベース設計検証を実行
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            検証結果辞書
        """
        print("\n🔍 データベース設計検証")
        
        if not self.enhanced_db_manager:
            print("❌ 強化データベース管理モジュールが利用できません")
            return {}
        
        try:
            health_report = self.enhanced_db_manager.validate_with_detailed_report(verbose)
            
            print(f"✅ 検証完了 - 健全性スコア: {health_report.overall_score:.1f}/100.0")
            print(f"有効テーブル: {health_report.valid_tables}/{health_report.total_tables}")
            
            if health_report.errors_count > 0:
                print(f"⚠️  エラー数: {health_report.errors_count}")
            
            return {
                'overall_score': health_report.overall_score,
                'total_tables': health_report.total_tables,
                'valid_tables': health_report.valid_tables,
                'errors_count': health_report.errors_count,
                'warnings_count': health_report.warnings_count,
                'recommendations': health_report.recommendations
            }
            
        except Exception as e:
            self.logger.error(f"データベース検証エラー: {e}")
            return {}
    
    def get_database_statistics(self, enhanced: bool = True) -> Dict[str, Any]:
        """
        データベース統計情報を取得
        
        Args:
            enhanced: 強化統計情報を使用するかどうか
            
        Returns:
            統計情報辞書
        """
        print("\n📈 データベース統計情報取得")
        
        try:
            if enhanced and self.enhanced_db_manager:
                stats = self.enhanced_db_manager.get_enhanced_statistics()
                print("✅ 強化統計情報を取得しました")
            elif self.db_manager:
                stats = self.db_manager.get_statistics()
                print("✅ 基本統計情報を取得しました")
            else:
                print("❌ 統計情報の取得に失敗しました")
                return {}
            
            # 統計サマリーを表示
            if stats:
                print(f"総テーブル数: {stats.get('total_tables', 0)}")
                print(f"総カラム数: {stats.get('total_columns', 0)}")
                
                if enhanced:
                    quality = stats.get('quality_metrics', {})
                    print(f"品質スコア: {quality.get('overall_quality_score', 0):.1f}/100.0")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"統計情報取得エラー: {e}")
            return {}
    
    def execute_integration_check(self, verbose: bool = False) -> Dict[str, Any]:
        """
        設計統合チェックを実行
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            統合チェック結果辞書
        """
        print("\n🔗 設計統合チェック実行")
        
        if not self.integration_checker:
            print("❌ 統合チェッカーが利用できません")
            return {}
        
        try:
            # 統合チェックを実行
            result = self.integration_checker.check_all_integrations(verbose)
            
            if result.get('overall_success', False):
                print("✅ 設計統合チェック完了")
            else:
                print("⚠️  設計統合で問題が発見されました")
            
            return result
            
        except Exception as e:
            self.logger.error(f"統合チェックエラー: {e}")
            return {'overall_success': False, 'error': str(e)}
    
    def generate_unified_report(self, verbose: bool = False) -> Dict[str, Any]:
        """
        統合レポートを生成
        
        Args:
            verbose: 詳細出力フラグ
            
        Returns:
            統合レポート辞書
        """
        print("\n📋 統合レポート生成")
        
        try:
            unified_report = {
                'generated_at': datetime.now().isoformat(),
                'database_report': {},
                'api_report': {},
                'screen_report': {},
                'integration_report': {},
                'summary': {}
            }
            
            # データベースレポート
            if self.enhanced_db_manager:
                print("📊 データベースレポート生成中...")
                unified_report['database_report'] = self.enhanced_db_manager.generate_comprehensive_report(verbose=False)
            
            # API設計レポート
            if self.api_manager:
                print("🔌 API設計レポート生成中...")
                unified_report['api_report'] = self.api_manager.generate_api_report(verbose=False)
            
            # 画面設計レポート
            if self.screen_manager:
                print("🖥️  画面設計レポート生成中...")
                unified_report['screen_report'] = self.screen_manager.generate_screen_report(verbose=False)
            
            # 統合チェックレポート
            if self.integration_checker:
                print("🔗 統合チェックレポート生成中...")
                unified_report['integration_report'] = self.integration_checker.check_all_integrations(verbose=False)
            
            # サマリー生成
            unified_report['summary'] = self._generate_unified_summary(unified_report)
            
            # レポート保存
            if self.report_generator:
                self.report_generator.save_unified_report(unified_report)
            
            print("✅ 統合レポート生成完了")
            
            if verbose:
                self._print_unified_report_summary(unified_report)
            
            return unified_report
            
        except Exception as e:
            self.logger.error(f"統合レポート生成エラー: {e}")
            return {}
    
    def _generate_unified_summary(self, unified_report: Dict[str, Any]) -> Dict[str, Any]:
        """
        統合サマリーを生成
        
        Args:
            unified_report: 統合レポート辞書
            
        Returns:
            サマリー辞書
        """
        summary = {
            'overall_health_score': 0.0,
            'total_components': 0,
            'healthy_components': 0,
            'issues_count': 0,
            'recommendations': []
        }
        
        try:
            # データベースサマリー
            db_report = unified_report.get('database_report', {})
            if db_report:
                db_summary = db_report.get('summary', {})
                summary['database_health'] = db_summary.get('overall_health_score', 0.0)
                summary['total_tables'] = db_summary.get('total_tables', 0)
                summary['total_components'] += summary['total_tables']
            
            # API設計サマリー
            api_report = unified_report.get('api_report', {})
            if api_report:
                summary['total_apis'] = api_report.get('total_apis', 0)
                summary['total_components'] += summary['total_apis']
            
            # 画面設計サマリー
            screen_report = unified_report.get('screen_report', {})
            if screen_report:
                summary['total_screens'] = screen_report.get('total_screens', 0)
                summary['total_components'] += summary['total_screens']
            
            # 全体健全性スコア計算
            scores = []
            if 'database_health' in summary:
                scores.append(summary['database_health'])
            
            if scores:
                summary['overall_health_score'] = sum(scores) / len(scores)
            
            # 推奨事項の統合
            for report_key in ['database_report', 'api_report', 'screen_report', 'integration_report']:
                report = unified_report.get(report_key, {})
                if isinstance(report, dict) and 'recommendations' in report:
                    summary['recommendations'].extend(report['recommendations'])
            
            return summary
            
        except Exception as e:
            self.logger.error(f"統合サマリー生成エラー: {e}")
            return summary
    
    def _print_report_summary(self, report: Dict[str, Any]):
        """
        レポートサマリーを出力
        
        Args:
            report: レポート辞書
        """
        print("\n📊 レポートサマリー:")
        summary = report.get('summary', {})
        print(f"  総テーブル数: {summary.get('total_tables', 0)}")
        print(f"  健全性スコア: {summary.get('overall_health_score', 0):.1f}/100.0")
        print(f"  有効テーブル: {summary.get('valid_tables', 0)}")
        print(f"  無効テーブル: {summary.get('invalid_tables', 0)}")
    
    def _print_unified_report_summary(self, unified_report: Dict[str, Any]):
        """
        統合レポートサマリーを出力
        
        Args:
            unified_report: 統合レポート辞書
        """
        print("\n📋 統合レポートサマリー:")
        summary = unified_report.get('summary', {})
        print(f"  全体健全性スコア: {summary.get('overall_health_score', 0):.1f}/100.0")
        print(f"  総コンポーネント数: {summary.get('total_components', 0)}")
        print(f"  データベーステーブル: {summary.get('total_tables', 0)}")
        print(f"  API数: {summary.get('total_apis', 0)}")
        print(f"  画面数: {summary.get('total_screens', 0)}")
        
        recommendations = summary.get('recommendations', [])
        if recommendations:
            print(f"  推奨事項数: {len(recommendations)}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="設計統合ツール（データベースツール昇格版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 強化データベースワークフロー実行
  python design_integration_tools.py database-enhanced --verbose
  
  # 基本データベースワークフロー実行
  python design_integration_tools.py database-basic --verbose
  
  # 包括的データベースレポート生成
  python design_integration_tools.py database-report --verbose
  
  # データベース設計最適化
  python design_integration_tools.py database-optimize --verbose
  
  # データベース設計検証
  python design_integration_tools.py database-validate --verbose
  
  # 統合レポート生成
  python design_integration_tools.py unified-report --verbose
  
  # 設計統合チェック
  python design_integration_tools.py integration-check --verbose
        """
    )
    
    # サブコマンド
    subparsers = parser.add_subparsers(dest='command', help='実行するコマンド')
    
    # 強化データベースワークフロー
    db_enhanced_parser = subparsers.add_parser('database-enhanced', help='強化データベースワークフロー実行')
    db_enhanced_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 基本データベースワークフロー
    db_basic_parser = subparsers.add_parser('database-basic', help='基本データベースワークフロー実行')
    db_basic_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # データベースレポート生成
    db_report_parser = subparsers.add_parser('database-report', help='包括的データベースレポート生成')
    db_report_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # データベース最適化
    db_optimize_parser = subparsers.add_parser('database-optimize', help='データベース設計最適化')
    db_optimize_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # データベース検証
    db_validate_parser = subparsers.add_parser('database-validate', help='データベース設計検証')
    db_validate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 統合レポート生成
    unified_report_parser = subparsers.add_parser('unified-report', help='統合レポート生成')
    unified_report_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 統合チェック
    integration_check_parser = subparsers.add_parser('integration-check', help='設計統合チェック')
    integration_check_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 統計情報取得
    stats_parser = subparsers.add_parser('stats', help='統計情報取得')
    stats_parser.add_argument('--enhanced', action='store_true', help='強化統計情報を使用')
    
    # 共通オプション
    parser.add_argument('--config', type=str, help='設定ファイルパス')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='ログレベル')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # ログレベル設定
        logging.basicConfig(level=getattr(logging, args.log_level))
        
        # 設計統合ツールを初期化
        tools = DesignIntegrationTools(args.config)
        
        # コマンド実行
        success = execute_command(tools, args)
        
        return 0 if success else 1
        
    except Exception as e:
        print(f"エラー: {e}")
        return 1


def execute_command(tools: DesignIntegrationTools, args) -> bool:
    """コマンド実行"""
    
    if args.command == 'database-enhanced':
        result = tools.execute_database_enhanced_workflow(args.verbose)
        return result.get('overall_success', False)
    
    elif args.command == 'database-basic':
        result = tools.execute_database_basic_workflow(args.verbose)
        return result.get('overall_success', False)
    
    elif args.command == 'database-report':
        result = tools.generate_comprehensive_database_report(args.verbose)
        return bool(result)
    
    elif args.command == 'database-optimize':
        result = tools.optimize_database_design(args.verbose)
        return bool(result)
    
    elif args.command == 'database-validate':
        result = tools.validate_database_design(args.verbose)
        return bool(result)
    
    elif args.command == 'unified-report':
        result = tools.generate_unified_report(args.verbose)
        return bool(result)
    
    elif args.command == 'integration-check':
        result = tools.execute_integration_check(args.verbose)
        return result.get('overall_success', False)
    
    elif args.command == 'stats':
        enhanced = getattr(args, 'enhanced', False)
        result = tools.get_database_statistics(enhanced)
        return bool(result)
    
    else:
        print(f"不明なコマンド: {args.command}")
        return False


if __name__ == '__main__':
    sys.exit(main())
