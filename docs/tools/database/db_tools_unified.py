#!/usr/bin/env python3
"""
統合データベースツール - メインエントリーポイント
要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1

このツールは以下の機能を統合して提供します：
1. YAML検証（必須セクション検証）
2. テーブル生成（DDL・定義書・サンプルデータ）
3. 整合性チェック（全ファイル間の整合性確認）
4. サンプルデータINSERT文生成
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import List, Optional, Dict, Any

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.config import Config
from core.logger import setup_logger
from core.exceptions import DatabaseToolsError
from modules.yaml_validator import YAMLValidator
from modules.table_generator import TableGenerator
from modules.consistency_checker import ConsistencyChecker
from modules.sample_data_generator import SampleDataGenerator


class DatabaseToolsUnified:
    """統合データベースツール"""
    
    def __init__(self, config: Config):
        """初期化"""
        self.config = config
        self.logger = setup_logger(__name__, config.log_level)
        
        # 各モジュールの初期化
        self.yaml_validator = YAMLValidator(config)
        self.table_generator = TableGenerator(config)
        self.consistency_checker = ConsistencyChecker(config)
        self.sample_data_generator = SampleDataGenerator(config)
    
    def validate_yaml(self, target: Optional[str] = None, verbose: bool = False) -> bool:
        """YAML検証実行"""
        self.logger.info("YAML検証を開始します")
        
        try:
            if target == "all":
                result = self.yaml_validator.validate_all(verbose=verbose)
            elif target:
                result = self.yaml_validator.validate_single(target, verbose=verbose)
            else:
                result = self.yaml_validator.validate_all(verbose=verbose)
            
            if result:
                self.logger.info("YAML検証が完了しました")
            else:
                self.logger.error("YAML検証でエラーが発生しました")
            
            return result
            
        except Exception as e:
            self.logger.error(f"YAML検証中にエラーが発生しました: {e}")
            return False
    
    def generate_table(self, table_name: str, verbose: bool = False) -> bool:
        """テーブル生成実行"""
        self.logger.info(f"テーブル生成を開始します: {table_name}")
        
        try:
            result = self.table_generator.generate(table_name, verbose=verbose)
            
            if result:
                self.logger.info(f"テーブル生成が完了しました: {table_name}")
            else:
                self.logger.error(f"テーブル生成でエラーが発生しました: {table_name}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"テーブル生成中にエラーが発生しました: {e}")
            return False
    
    def check_consistency(self, verbose: bool = False) -> bool:
        """整合性チェック実行"""
        self.logger.info("整合性チェックを開始します")
        
        try:
            result = self.consistency_checker.check_all(verbose=verbose)
            
            if result:
                self.logger.info("整合性チェックが完了しました")
            else:
                self.logger.error("整合性チェックでエラーが発生しました")
            
            return result
            
        except Exception as e:
            self.logger.error(f"整合性チェック中にエラーが発生しました: {e}")
            return False
    
    def generate_sample_data(self, verbose: bool = False) -> bool:
        """サンプルデータ生成実行"""
        self.logger.info("サンプルデータ生成を開始します")
        
        try:
            result = self.sample_data_generator.generate_all(verbose=verbose)
            
            if result:
                self.logger.info("サンプルデータ生成が完了しました")
            else:
                self.logger.error("サンプルデータ生成でエラーが発生しました")
            
            return result
            
        except Exception as e:
            self.logger.error(f"サンプルデータ生成中にエラーが発生しました: {e}")
            return False
    
    def run_all(self, verbose: bool = False) -> bool:
        """全機能実行"""
        self.logger.info("全機能の実行を開始します")
        
        success = True
        
        # 1. YAML検証
        if not self.validate_yaml("all", verbose):
            success = False
        
        # 2. 整合性チェック
        if not self.check_consistency(verbose):
            success = False
        
        # 3. サンプルデータ生成
        if not self.generate_sample_data(verbose):
            success = False
        
        if success:
            self.logger.info("全機能の実行が完了しました")
        else:
            self.logger.error("一部の機能でエラーが発生しました")
        
        return success


def create_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを作成"""
    parser = argparse.ArgumentParser(
        description="統合データベースツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # YAML検証（全ファイル）
  python db_tools_unified.py validate --all --verbose
  
  # 特定テーブルの生成
  python db_tools_unified.py generate --table MST_Employee --verbose
  
  # 整合性チェック
  python db_tools_unified.py check --verbose
  
  # サンプルデータ生成
  python db_tools_unified.py sample --verbose
  
  # 全機能実行
  python db_tools_unified.py all --verbose
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='実行するコマンド')
    
    # YAML検証コマンド
    validate_parser = subparsers.add_parser('validate', help='YAML検証')
    validate_parser.add_argument('--all', action='store_true', help='全YAMLファイルを検証')
    validate_parser.add_argument('--table', type=str, help='特定テーブルのYAMLを検証')
    validate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # テーブル生成コマンド
    generate_parser = subparsers.add_parser('generate', help='テーブル生成')
    generate_parser.add_argument('--table', type=str, required=True, help='生成するテーブル名')
    generate_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 整合性チェックコマンド
    check_parser = subparsers.add_parser('check', help='整合性チェック')
    check_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # サンプルデータ生成コマンド
    sample_parser = subparsers.add_parser('sample', help='サンプルデータ生成')
    sample_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 全機能実行コマンド
    all_parser = subparsers.add_parser('all', help='全機能実行')
    all_parser.add_argument('--verbose', action='store_true', help='詳細出力')
    
    # 共通オプション
    parser.add_argument('--config', type=str, help='設定ファイルパス')
    parser.add_argument('--log-level', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], 
                       default='INFO', help='ログレベル')
    
    return parser


def main():
    """メイン関数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # 設定の初期化
        config = Config(
            config_file=args.config,
            log_level=args.log_level
        )
        
        # ツールの初期化
        tools = DatabaseToolsUnified(config)
        
        # コマンド実行
        success = False
        
        if args.command == 'validate':
            target = "all" if args.all else args.table
            success = tools.validate_yaml(target, args.verbose)
            
        elif args.command == 'generate':
            success = tools.generate_table(args.table, args.verbose)
            
        elif args.command == 'check':
            success = tools.check_consistency(args.verbose)
            
        elif args.command == 'sample':
            success = tools.generate_sample_data(args.verbose)
            
        elif args.command == 'all':
            success = tools.run_all(args.verbose)
        
        return 0 if success else 1
        
    except DatabaseToolsError as e:
        print(f"エラー: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
