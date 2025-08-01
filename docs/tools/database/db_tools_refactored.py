#!/usr/bin/env python3
"""
データベースツール統合メインモジュール（リファクタリング版）
要求仕様ID: PLT.1-WEB.1

リファクタリングされたモジュールを使用した統合ツールです：
1. YAML検証
2. テーブル生成
3. 整合性チェック
"""

import sys
import argparse
import logging
from pathlib import Path

# パスを追加してモジュールをインポート
sys.path.append(str(Path(__file__).parent))

from core.config import Config
from core.logger import get_logger
from core.exceptions import DatabaseToolsError
from modules.yaml_validator import YAMLValidator
from modules.table_generator import TableGenerator
from modules.consistency_checker import ConsistencyChecker


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="データベースツール統合メインモジュール（リファクタリング版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # YAML検証
  python db_tools_refactored.py validate --all --verbose
  python db_tools_refactored.py validate --table MST_Employee

  # テーブル生成
  python db_tools_refactored.py generate --all --verbose
  python db_tools_refactored.py generate --table MST_Employee

  # 整合性チェック
  python db_tools_refactored.py check --all --verbose
  python db_tools_refactored.py check --table MST_Employee

  # 全処理実行
  python db_tools_refactored.py all --verbose
        """
    )
    
    # サブコマンド
    subparsers = parser.add_subparsers(dest='command', help='実行するコマンド')
    
    # YAML検証コマンド
    validate_parser = subparsers.add_parser('validate', help='YAML検証')
    validate_parser.add_argument('--all', action='store_true', help='全YAMLファイルを検証')
    validate_parser.add_argument('--table', type=str, help='特定テーブルのみ検証')
    validate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # テーブル生成コマンド
    generate_parser = subparsers.add_parser('generate', help='テーブル生成')
    generate_parser.add_argument('--all', action='store_true', help='全テーブルを生成')
    generate_parser.add_argument('--table', type=str, help='特定テーブルのみ生成')
    generate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 整合性チェックコマンド
    check_parser = subparsers.add_parser('check', help='整合性チェック')
    check_parser.add_argument('--all', action='store_true', help='全テーブルをチェック')
    check_parser.add_argument('--table', type=str, help='特定テーブルのみチェック')
    check_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 全処理実行コマンド
    all_parser = subparsers.add_parser('all', help='全処理実行（検証→生成→チェック）')
    all_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 共通オプション
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='ログレベル')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # 設定初期化
        config = Config()
        logger = get_logger(__name__)
        
        logger.info(f"データベースツール開始: {args.command}")
        
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


def execute_command(args, config: Config) -> bool:
    """コマンド実行"""
    
    if args.command == 'validate':
        return execute_validate(args, config)
    elif args.command == 'generate':
        return execute_generate(args, config)
    elif args.command == 'check':
        return execute_check(args, config)
    elif args.command == 'all':
        return execute_all(args, config)
    else:
        print(f"不明なコマンド: {args.command}")
        return False


def execute_validate(args, config: Config) -> bool:
    """YAML検証実行"""
    print("=== YAML検証 ===")
    
    validator = YAMLValidator(config)
    
    if args.all:
        return validator.validate_all(args.verbose)
    elif args.table:
        return validator.validate_single(args.table, args.verbose)
    else:
        print("--all または --table を指定してください")
        return False


def execute_generate(args, config: Config) -> bool:
    """テーブル生成実行"""
    print("=== テーブル生成 ===")
    
    generator = TableGenerator(config)
    
    if args.all:
        return generator.generate_all(args.verbose)
    elif args.table:
        return generator.generate(args.table, args.verbose)
    else:
        print("--all または --table を指定してください")
        return False


def execute_check(args, config: Config) -> bool:
    """整合性チェック実行"""
    print("=== 整合性チェック ===")
    
    checker = ConsistencyChecker(config)
    
    if args.all:
        return checker.check_all(args.verbose)
    elif args.table:
        return checker.check_single(args.table, args.verbose)
    else:
        print("--all または --table を指定してください")
        return False


def execute_all(args, config: Config) -> bool:
    """全処理実行"""
    print("=== 全処理実行 ===")
    
    # 1. YAML検証
    print("\n1. YAML検証を実行中...")
    validator = YAMLValidator(config)
    if not validator.validate_all(args.verbose):
        print("❌ YAML検証でエラーが発生しました。処理を中断します。")
        return False
    print("✅ YAML検証完了")
    
    # 2. テーブル生成
    print("\n2. テーブル生成を実行中...")
    generator = TableGenerator(config)
    if not generator.generate_all(args.verbose):
        print("❌ テーブル生成でエラーが発生しました。")
        # 生成エラーがあっても整合性チェックは実行
    print("✅ テーブル生成完了")
    
    # 3. 整合性チェック
    print("\n3. 整合性チェックを実行中...")
    checker = ConsistencyChecker(config)
    if not checker.check_all(args.verbose):
        print("❌ 整合性チェックでエラーが発見されました。")
        return False
    print("✅ 整合性チェック完了")
    
    print("\n🎉 全処理が正常に完了しました！")
    return True


if __name__ == '__main__':
    sys.exit(main())
