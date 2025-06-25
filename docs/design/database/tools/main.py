#!/usr/bin/env python3
"""
データベースツール統合エントリーポイント
全ツールの統一実行インターフェース

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-25
実装者: AI駆動開発チーム
"""

import sys
import argparse
from pathlib import Path
from typing import Optional, List

# 共通モジュール
from shared.core.logger import get_logger, setup_logging
from shared.core.config import get_config
from shared.core.exceptions import DatabaseToolsError

# 各ツールのメインモジュール
from database_consistency_checker.main import main as consistency_checker_main
from table_generator.main import main as table_generator_main

logger = get_logger(__name__)


def create_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを作成"""
    parser = argparse.ArgumentParser(
        description="データベースツール統合実行システム",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 整合性チェック実行
  python main.py consistency --all --verbose
  
  # テーブル生成実行
  python main.py generate --table MST_Employee --verbose
  
  # YAML検証のみ実行
  python main.py consistency --yaml-only --verbose
  
  # 全体統合チェック
  python main.py consistency --full-check --verbose
        """
    )
    
    # 共通オプション
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細ログを出力'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        help='設定ファイルパス'
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='ログレベル'
    )
    
    # サブコマンド
    subparsers = parser.add_subparsers(
        dest='command',
        help='実行するツール',
        required=True
    )
    
    # 整合性チェックサブコマンド
    consistency_parser = subparsers.add_parser(
        'consistency',
        help='データベース整合性チェック',
        description='YAML・DDL・定義書の整合性をチェック'
    )
    
    consistency_parser.add_argument(
        '--all',
        action='store_true',
        help='全チェックを実行'
    )
    
    consistency_parser.add_argument(
        '--yaml-only',
        action='store_true',
        help='YAML検証のみ実行'
    )
    
    consistency_parser.add_argument(
        '--table-existence',
        action='store_true',
        help='テーブル存在チェックのみ実行'
    )
    
    consistency_parser.add_argument(
        '--full-check',
        action='store_true',
        help='完全整合性チェック実行'
    )
    
    consistency_parser.add_argument(
        '--target-dir',
        type=str,
        help='チェック対象ディレクトリ'
    )
    
    # テーブル生成サブコマンド
    generate_parser = subparsers.add_parser(
        'generate',
        help='テーブル定義生成',
        description='YAMLからDDL・定義書・サンプルデータを生成'
    )
    
    generate_parser.add_argument(
        '--table',
        type=str,
        help='生成対象テーブル名'
    )
    
    generate_parser.add_argument(
        '--all-tables',
        action='store_true',
        help='全テーブルを生成'
    )
    
    generate_parser.add_argument(
        '--ddl-only',
        action='store_true',
        help='DDLのみ生成'
    )
    
    generate_parser.add_argument(
        '--docs-only',
        action='store_true',
        help='定義書のみ生成'
    )
    
    generate_parser.add_argument(
        '--sample-data-only',
        action='store_true',
        help='サンプルデータのみ生成'
    )
    
    generate_parser.add_argument(
        '--force',
        action='store_true',
        help='既存ファイルを強制上書き'
    )
    
    # バリデーションサブコマンド
    validate_parser = subparsers.add_parser(
        'validate',
        help='YAML形式バリデーション',
        description='YAML形式・必須セクションをバリデーション'
    )
    
    validate_parser.add_argument(
        '--file',
        type=str,
        help='バリデーション対象ファイル'
    )
    
    validate_parser.add_argument(
        '--directory',
        type=str,
        help='バリデーション対象ディレクトリ'
    )
    
    validate_parser.add_argument(
        '--strict',
        action='store_true',
        help='厳密モード（警告もエラーとして扱う）'
    )
    
    return parser


def setup_environment(args) -> None:
    """実行環境をセットアップ"""
    # ログ設定
    setup_logging(
        level=args.log_level,
        verbose=args.verbose
    )
    
    # 設定ファイル読み込み
    if args.config:
        config = get_config(args.config)
        logger.info(f"設定ファイルを読み込みました: {args.config}")
    else:
        config = get_config()
    
    logger.info("データベースツール統合システムを開始します")
    logger.debug(f"実行コマンド: {args.command}")
    logger.debug(f"ログレベル: {args.log_level}")


def execute_consistency_check(args) -> int:
    """整合性チェックを実行"""
    logger.info("整合性チェックを開始します")
    
    try:
        # 引数を整合性チェッカー用に変換
        checker_args = []
        
        if args.all:
            checker_args.append('--all')
        
        if args.yaml_only:
            checker_args.append('--yaml-only')
        
        if args.table_existence:
            checker_args.append('--table-existence')
        
        if args.full_check:
            checker_args.append('--full-check')
        
        if args.target_dir:
            checker_args.extend(['--target-dir', args.target_dir])
        
        if args.verbose:
            checker_args.append('--verbose')
        
        # 整合性チェッカー実行
        result = consistency_checker_main(checker_args)
        
        if result == 0:
            logger.info("整合性チェックが正常に完了しました")
        else:
            logger.error("整合性チェックでエラーが発生しました")
        
        return result
        
    except Exception as e:
        logger.error(f"整合性チェック実行エラー: {e}")
        return 1


def execute_table_generation(args) -> int:
    """テーブル生成を実行"""
    logger.info("テーブル生成を開始します")
    
    try:
        # 引数をテーブル生成ツール用に変換
        generator_args = []
        
        if args.table:
            generator_args.extend(['--table', args.table])
        
        if args.all_tables:
            generator_args.append('--all-tables')
        
        if args.ddl_only:
            generator_args.append('--ddl-only')
        
        if args.docs_only:
            generator_args.append('--docs-only')
        
        if args.sample_data_only:
            generator_args.append('--sample-data-only')
        
        if args.force:
            generator_args.append('--force')
        
        if args.verbose:
            generator_args.append('--verbose')
        
        # テーブル生成ツール実行
        result = table_generator_main(generator_args)
        
        if result == 0:
            logger.info("テーブル生成が正常に完了しました")
        else:
            logger.error("テーブル生成でエラーが発生しました")
        
        return result
        
    except Exception as e:
        logger.error(f"テーブル生成実行エラー: {e}")
        return 1


def execute_validation(args) -> int:
    """YAML バリデーションを実行"""
    logger.info("YAML バリデーションを開始します")
    
    try:
        from shared.utils.validation import validate_yaml_file
        from shared.utils.file_utils import get_file_manager
        
        file_manager = get_file_manager()
        validation_errors = 0
        
        if args.file:
            # 単一ファイルバリデーション
            file_path = Path(args.file)
            logger.info(f"ファイルをバリデーション: {file_path}")
            
            result = validate_yaml_file(file_path)
            
            if not result.is_valid:
                validation_errors += 1
                logger.error(f"バリデーションエラー: {file_path}")
                for error in result.errors:
                    logger.error(f"  - {error['message']}")
            
            if result.warnings and args.strict:
                validation_errors += 1
                logger.error(f"バリデーション警告（厳密モード）: {file_path}")
                for warning in result.warnings:
                    logger.error(f"  - {warning['message']}")
            elif result.warnings:
                logger.warning(f"バリデーション警告: {file_path}")
                for warning in result.warnings:
                    logger.warning(f"  - {warning['message']}")
        
        elif args.directory:
            # ディレクトリ内全YAMLファイルバリデーション
            directory = Path(args.directory)
            logger.info(f"ディレクトリをバリデーション: {directory}")
            
            yaml_files = file_manager.find_files(directory, "*.yaml")
            yaml_files.extend(file_manager.find_files(directory, "*.yml"))
            
            for yaml_file in yaml_files:
                logger.debug(f"ファイルをバリデーション: {yaml_file}")
                
                result = validate_yaml_file(yaml_file)
                
                if not result.is_valid:
                    validation_errors += 1
                    logger.error(f"バリデーションエラー: {yaml_file}")
                    for error in result.errors:
                        logger.error(f"  - {error['message']}")
                
                if result.warnings and args.strict:
                    validation_errors += 1
                    logger.error(f"バリデーション警告（厳密モード）: {yaml_file}")
                    for warning in result.warnings:
                        logger.error(f"  - {warning['message']}")
                elif result.warnings:
                    logger.warning(f"バリデーション警告: {yaml_file}")
                    for warning in result.warnings:
                        logger.warning(f"  - {warning['message']}")
        
        else:
            logger.error("--file または --directory を指定してください")
            return 1
        
        if validation_errors > 0:
            logger.error(f"バリデーションエラー: {validation_errors}個のファイルでエラーが発生")
            return 1
        else:
            logger.info("バリデーションが正常に完了しました")
            return 0
        
    except Exception as e:
        logger.error(f"バリデーション実行エラー: {e}")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """メイン実行関数"""
    try:
        # コマンドライン引数解析
        parser = create_parser()
        args = parser.parse_args(argv)
        
        # 実行環境セットアップ
        setup_environment(args)
        
        # コマンド別実行
        if args.command == 'consistency':
            return execute_consistency_check(args)
        
        elif args.command == 'generate':
            return execute_table_generation(args)
        
        elif args.command == 'validate':
            return execute_validation(args)
        
        else:
            logger.error(f"未知のコマンド: {args.command}")
            return 1
    
    except KeyboardInterrupt:
        logger.info("ユーザーによって中断されました")
        return 130
    
    except DatabaseToolsError as e:
        logger.error(f"ツールエラー: {e}")
        return 1
    
    except Exception as e:
        logger.error(f"予期しないエラー: {e}")
        logger.debug("詳細なエラー情報:", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
