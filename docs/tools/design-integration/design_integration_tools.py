#!/usr/bin/env python3
"""
設計統合ツール - 統合メインモジュール
要求仕様ID: PLT.1-WEB.1

データベース設計ツールを設計統合ツールに昇格させた統合ツールです：
1. データベース設計管理
2. API設計管理
3. 画面設計管理
4. 設計書整合性チェック
5. 設計書自動生成
"""

import sys
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Optional

# パスを追加してモジュールをインポート
sys.path.append(str(Path(__file__).parent))

from core.config import DesignIntegrationConfig
from core.logger import get_logger
from core.exceptions import DesignIntegrationError
from modules.database_manager import DatabaseDesignManager
from modules.api_manager import APIDesignManager
from modules.screen_manager import ScreenDesignManager
from modules.integration_checker import IntegrationChecker
from modules.design_generator import DesignGenerator


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="設計統合ツール - 統合メインモジュール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # データベース設計管理
  python design_integration_tools.py database validate --all --verbose
  python design_integration_tools.py database generate --table MST_Employee

  # API設計管理
  python design_integration_tools.py api validate --all --verbose
  python design_integration_tools.py api generate --api API-021

  # 画面設計管理
  python design_integration_tools.py screen validate --all --verbose
  python design_integration_tools.py screen generate --screen SCR-SKILL

  # 設計書整合性チェック
  python design_integration_tools.py check --all --verbose
  python design_integration_tools.py check --requirement SKL.1-HIER.1

  # 設計書自動生成
  python design_integration_tools.py generate --all --verbose
  python design_integration_tools.py generate --type database

  # 全処理実行
  python design_integration_tools.py all --verbose
        """
    )
    
    # サブコマンド
    subparsers = parser.add_subparsers(dest='command', help='実行するコマンド')
    
    # データベース設計管理コマンド
    db_parser = subparsers.add_parser('database', help='データベース設計管理')
    db_subparsers = db_parser.add_subparsers(dest='db_action', help='データベース操作')
    
    db_validate_parser = db_subparsers.add_parser('validate', help='データベース設計検証')
    db_validate_parser.add_argument('--all', action='store_true', help='全テーブルを検証')
    db_validate_parser.add_argument('--table', type=str, help='特定テーブルのみ検証')
    db_validate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    db_generate_parser = db_subparsers.add_parser('generate', help='データベース設計生成')
    db_generate_parser.add_argument('--all', action='store_true', help='全テーブルを生成')
    db_generate_parser.add_argument('--table', type=str, help='特定テーブルのみ生成')
    db_generate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # API設計管理コマンド
    api_parser = subparsers.add_parser('api', help='API設計管理')
    api_subparsers = api_parser.add_subparsers(dest='api_action', help='API操作')
    
    api_validate_parser = api_subparsers.add_parser('validate', help='API設計検証')
    api_validate_parser.add_argument('--all', action='store_true', help='全APIを検証')
    api_validate_parser.add_argument('--api', type=str, help='特定APIのみ検証')
    api_validate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    api_generate_parser = api_subparsers.add_parser('generate', help='API設計生成')
    api_generate_parser.add_argument('--all', action='store_true', help='全APIを生成')
    api_generate_parser.add_argument('--api', type=str, help='特定APIのみ生成')
    api_generate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 画面設計管理コマンド
    screen_parser = subparsers.add_parser('screen', help='画面設計管理')
    screen_subparsers = screen_parser.add_subparsers(dest='screen_action', help='画面操作')
    
    screen_validate_parser = screen_subparsers.add_parser('validate', help='画面設計検証')
    screen_validate_parser.add_argument('--all', action='store_true', help='全画面を検証')
    screen_validate_parser.add_argument('--screen', type=str, help='特定画面のみ検証')
    screen_validate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    screen_generate_parser = screen_subparsers.add_parser('generate', help='画面設計生成')
    screen_generate_parser.add_argument('--all', action='store_true', help='全画面を生成')
    screen_generate_parser.add_argument('--screen', type=str, help='特定画面のみ生成')
    screen_generate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 設計書整合性チェックコマンド
    check_parser = subparsers.add_parser('check', help='設計書整合性チェック')
    check_parser.add_argument('--all', action='store_true', help='全設計書をチェック')
    check_parser.add_argument('--requirement', type=str, help='特定要求仕様IDのみチェック')
    check_parser.add_argument('--type', choices=['database', 'api', 'screen'], help='特定設計タイプのみチェック')
    check_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 設計書自動生成コマンド
    generate_parser = subparsers.add_parser('generate', help='設計書自動生成')
    generate_parser.add_argument('--all', action='store_true', help='全設計書を生成')
    generate_parser.add_argument('--type', choices=['database', 'api', 'screen'], help='特定設計タイプのみ生成')
    generate_parser.add_argument('--requirement', type=str, help='特定要求仕様IDのみ生成')
    generate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 全処理実行コマンド
    all_parser = subparsers.add_parser('all', help='全処理実行（検証→生成→チェック）')
    all_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 共通オプション
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='ログレベル')
    parser.add_argument('--config', type=str, help='設定ファイルパス')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # 設定初期化
        config = DesignIntegrationConfig(args.config)
        logger = get_logger(__name__)
        
        logger.info(f"設計統合ツール開始: {args.command}")
        
        # コマンド実行
        success = execute_command(args, config)
        
        if success:
            logger.info("処理が正常に完了しました")
            return 0
        else:
            logger.error("処理中にエラーが発生しました")
            return 1
            
    except Exception as e:
        print(f"エラー: {e}")
        return 1


def execute_command(args, config: DesignIntegrationConfig) -> bool:
    """コマンド実行"""
    
    if args.command == 'database':
        return execute_database_command(args, config)
    elif args.command == 'api':
        return execute_api_command(args, config)
    elif args.command == 'screen':
        return execute_screen_command(args, config)
    elif args.command == 'check':
        return execute_check_command(args, config)
    elif args.command == 'generate':
        return execute_generate_command(args, config)
    elif args.command == 'all':
        return execute_all_command(args, config)
    else:
        print(f"不明なコマンド: {args.command}")
        return False


def execute_database_command(args, config: DesignIntegrationConfig) -> bool:
    """データベース設計管理実行"""
    print("=== データベース設計管理 ===")
    
    manager = DatabaseDesignManager(config)
    
    if args.db_action == 'validate':
        if args.all:
            return manager.validate_all(args.verbose)
        elif args.table:
            return manager.validate_table(args.table, args.verbose)
        else:
            print("--all または --table を指定してください")
            return False
    elif args.db_action == 'generate':
        if args.all:
            return manager.generate_all(args.verbose)
        elif args.table:
            return manager.generate_table(args.table, args.verbose)
        else:
            print("--all または --table を指定してください")
            return False
    else:
        print("validate または generate を指定してください")
        return False


def execute_api_command(args, config: DesignIntegrationConfig) -> bool:
    """API設計管理実行"""
    print("=== API設計管理 ===")
    
    manager = APIDesignManager(config)
    
    if args.api_action == 'validate':
        if args.all:
            return manager.validate_all(args.verbose)
        elif args.api:
            return manager.validate_api(args.api, args.verbose)
        else:
            print("--all または --api を指定してください")
            return False
    elif args.api_action == 'generate':
        if args.all:
            return manager.generate_all(args.verbose)
        elif args.api:
            return manager.generate_api(args.api, args.verbose)
        else:
            print("--all または --api を指定してください")
            return False
    else:
        print("validate または generate を指定してください")
        return False


def execute_screen_command(args, config: DesignIntegrationConfig) -> bool:
    """画面設計管理実行"""
    print("=== 画面設計管理 ===")
    
    manager = ScreenDesignManager(config)
    
    if args.screen_action == 'validate':
        if args.all:
            return manager.validate_all(args.verbose)
        elif args.screen:
            return manager.validate_screen(args.screen, args.verbose)
        else:
            print("--all または --screen を指定してください")
            return False
    elif args.screen_action == 'generate':
        if args.all:
            return manager.generate_all(args.verbose)
        elif args.screen:
            return manager.generate_screen(args.screen, args.verbose)
        else:
            print("--all または --screen を指定してください")
            return False
    else:
        print("validate または generate を指定してください")
        return False


def execute_check_command(args, config: DesignIntegrationConfig) -> bool:
    """設計書整合性チェック実行"""
    print("=== 設計書整合性チェック ===")
    
    checker = IntegrationChecker(config)
    
    if args.all:
        return checker.check_all_integration(args.verbose)
    elif args.requirement:
        return checker.check_requirement_integration(args.requirement, args.verbose)
    elif args.type:
        return checker.check_type_integration(args.type, args.verbose)
    else:
        print("--all, --requirement, または --type を指定してください")
        return False


def execute_generate_command(args, config: DesignIntegrationConfig) -> bool:
    """設計書自動生成実行"""
    print("=== 設計書自動生成 ===")
    
    generator = DesignGenerator(config)
    
    if args.all:
        return generator.generate_all_designs(args.verbose)
    elif args.type:
        return generator.generate_by_type(args.type, args.verbose)
    elif args.requirement:
        return generator.generate_by_requirement(args.requirement, args.verbose)
    else:
        print("--all, --type, または --requirement を指定してください")
        return False


def execute_all_command(args, config: DesignIntegrationConfig) -> bool:
    """全処理実行"""
    print("=== 設計統合ツール - 全処理実行 ===")
    
    success_count = 0
    total_count = 5
    
    # 1. データベース設計検証・生成
    print("\n1. データベース設計検証・生成を実行中...")
    db_manager = DatabaseDesignManager(config)
    if db_manager.validate_all(args.verbose) and db_manager.generate_all(args.verbose):
        print("✅ データベース設計完了")
        success_count += 1
    else:
        print("❌ データベース設計でエラーが発生しました")
    
    # 2. API設計検証・生成
    print("\n2. API設計検証・生成を実行中...")
    api_manager = APIDesignManager(config)
    if api_manager.validate_all(args.verbose) and api_manager.generate_all(args.verbose):
        print("✅ API設計完了")
        success_count += 1
    else:
        print("❌ API設計でエラーが発生しました")
    
    # 3. 画面設計検証・生成
    print("\n3. 画面設計検証・生成を実行中...")
    screen_manager = ScreenDesignManager(config)
    if screen_manager.validate_all(args.verbose) and screen_manager.generate_all(args.verbose):
        print("✅ 画面設計完了")
        success_count += 1
    else:
        print("❌ 画面設計でエラーが発生しました")
    
    # 4. 設計書整合性チェック
    print("\n4. 設計書整合性チェックを実行中...")
    checker = IntegrationChecker(config)
    if checker.check_all_integration(args.verbose):
        print("✅ 設計書整合性チェック完了")
        success_count += 1
    else:
        print("❌ 設計書整合性チェックでエラーが発見されました")
    
    # 5. 設計書自動生成
    print("\n5. 設計書自動生成を実行中...")
    generator = DesignGenerator(config)
    if generator.generate_all_designs(args.verbose):
        print("✅ 設計書自動生成完了")
        success_count += 1
    else:
        print("❌ 設計書自動生成でエラーが発生しました")
    
    # 結果サマリー
    print(f"\n📊 処理結果サマリー: {success_count}/{total_count} 成功")
    
    if success_count == total_count:
        print("\n🎉 全処理が正常に完了しました！")
        return True
    else:
        print(f"\n⚠️  {total_count - success_count} 個の処理でエラーが発生しました")
        return False


if __name__ == '__main__':
    sys.exit(main())
