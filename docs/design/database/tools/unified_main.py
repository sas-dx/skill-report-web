#!/usr/bin/env python3
"""
統一データベースツール - メインエントリーポイント

全ての機能を統合したコマンドラインインターフェース
"""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from core import setup_logger, ToolConfig, ValidationError, GenerationError
from parsers import create_parser
from generators import create_generator
from shared.monitoring import MetricsCollector


def setup_argument_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを設定"""
    parser = argparse.ArgumentParser(
        description="統一データベースツール - YAML/DDL/Markdown変換・検証ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # YAMLからDDL生成
  python unified_main.py generate --input table.yaml --output table.sql --format ddl
  
  # YAMLからMarkdown生成
  python unified_main.py generate --input table.yaml --output table.md --format markdown
  
  # YAML検証
  python unified_main.py validate --input table.yaml
  
  # 整合性チェック
  python unified_main.py check --yaml-dir table-details --ddl-dir ddl --md-dir tables
  
  # 一括生成
  python unified_main.py batch --input-dir table-details --output-dir output --formats ddl,markdown
        """
    )
    
    # サブコマンド
    subparsers = parser.add_subparsers(dest='command', help='実行するコマンド')
    
    # generate サブコマンド
    generate_parser = subparsers.add_parser('generate', help='ファイル生成')
    generate_parser.add_argument('--input', '-i', required=True, help='入力ファイルパス')
    generate_parser.add_argument('--output', '-o', required=True, help='出力ファイルパス')
    generate_parser.add_argument('--format', '-f', required=True, 
                                choices=['ddl', 'sql', 'markdown', 'md'], help='出力形式')
    generate_parser.add_argument('--db-type', default='postgresql', 
                                choices=['postgresql', 'mysql', 'sqlite'], help='データベースタイプ')
    generate_parser.add_argument('--no-comments', action='store_true', help='コメント除外')
    generate_parser.add_argument('--no-indexes', action='store_true', help='インデックス除外')
    generate_parser.add_argument('--table-style', default='standard',
                                choices=['standard', 'compact'], help='テーブルスタイル')
    
    # validate サブコマンド
    validate_parser = subparsers.add_parser('validate', help='ファイル検証')
    validate_parser.add_argument('--input', '-i', required=True, help='検証対象ファイル')
    validate_parser.add_argument('--strict', action='store_true', help='厳密検証モード')
    
    # check サブコマンド
    check_parser = subparsers.add_parser('check', help='整合性チェック')
    check_parser.add_argument('--yaml-dir', required=True, help='YAMLディレクトリ')
    check_parser.add_argument('--ddl-dir', help='DDLディレクトリ')
    check_parser.add_argument('--md-dir', help='Markdownディレクトリ')
    check_parser.add_argument('--fix', action='store_true', help='自動修正実行')
    
    # batch サブコマンド
    batch_parser = subparsers.add_parser('batch', help='一括処理')
    batch_parser.add_argument('--input-dir', '-i', required=True, help='入力ディレクトリ')
    batch_parser.add_argument('--output-dir', '-o', required=True, help='出力ディレクトリ')
    batch_parser.add_argument('--formats', '-f', required=True, help='出力形式（カンマ区切り）')
    batch_parser.add_argument('--pattern', default='*.yaml', help='入力ファイルパターン')
    batch_parser.add_argument('--parallel', action='store_true', help='並列処理実行')
    
    # 共通オプション
    parser.add_argument('--verbose', '-v', action='store_true', help='詳細ログ出力')
    parser.add_argument('--quiet', '-q', action='store_true', help='エラーのみ出力')
    parser.add_argument('--config', help='設定ファイルパス')
    parser.add_argument('--metrics', action='store_true', help='メトリクス収集')
    
    return parser


def execute_generate_command(args) -> int:
    """generate コマンドを実行"""
    try:
        # パーサー作成
        parser = create_parser(args.input)
        
        # データ解析
        data = parser.parse(args.input)
        
        # ジェネレーター作成
        generator = create_generator(args.format)
        
        # 生成オプション設定
        options = {
            'db_type': args.db_type,
            'include_comments': not args.no_comments,
            'include_indexes': not args.no_indexes,
            'table_style': args.table_style
        }
        
        # ファイル生成
        success = generator.generate(data, args.output, **options)
        
        if success:
            print(f"✅ ファイルを生成しました: {args.output}")
            return 0
        else:
            print(f"❌ ファイル生成に失敗しました: {args.output}")
            return 1
            
    except (ValidationError, GenerationError) as e:
        print(f"❌ エラー: {e}")
        return 1
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return 1


def execute_validate_command(args) -> int:
    """validate コマンドを実行"""
    try:
        # パーサー作成
        parser = create_parser(args.input)
        
        # データ解析・検証
        data = parser.parse(args.input)
        validation_result = parser.validate(data)
        
        if validation_result.is_valid:
            print(f"✅ 検証成功: {args.input}")
            return 0
        else:
            print(f"❌ 検証失敗: {args.input}")
            for error in validation_result.errors:
                print(f"  - {error}")
            return 1
            
    except ValidationError as e:
        print(f"❌ 検証エラー: {e}")
        return 1
    except Exception as e:
        print(f"❌ 予期しないエラー: {e}")
        return 1


def execute_check_command(args) -> int:
    """check コマンドを実行"""
    try:
        from database_consistency_checker.main import main as consistency_main
        
        # 整合性チェック実行
        check_args = [
            '--yaml-dir', args.yaml_dir,
            '--verbose' if args.verbose else '--quiet'
        ]
        
        if args.ddl_dir:
            check_args.extend(['--ddl-dir', args.ddl_dir])
        if args.md_dir:
            check_args.extend(['--md-dir', args.md_dir])
        if args.fix:
            check_args.append('--fix')
        
        return consistency_main(check_args)
        
    except Exception as e:
        print(f"❌ 整合性チェックエラー: {e}")
        return 1


def execute_batch_command(args) -> int:
    """batch コマンドを実行"""
    try:
        input_dir = Path(args.input_dir)
        output_dir = Path(args.output_dir)
        formats = [f.strip() for f in args.formats.split(',')]
        
        # 出力ディレクトリ作成
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 入力ファイル検索
        input_files = list(input_dir.glob(args.pattern))
        if not input_files:
            print(f"❌ 入力ファイルが見つかりません: {input_dir}/{args.pattern}")
            return 1
        
        print(f"📁 {len(input_files)}個のファイルを処理します...")
        
        success_count = 0
        error_count = 0
        
        for input_file in input_files:
            try:
                # パーサー作成
                parser = create_parser(str(input_file))
                data = parser.parse(str(input_file))
                
                # 各形式で生成
                for format_type in formats:
                    try:
                        generator = create_generator(format_type)
                        output_filename = generator.get_output_filename(data, format_type)
                        output_path = output_dir / output_filename
                        
                        success = generator.generate(data, str(output_path))
                        if success:
                            success_count += 1
                            print(f"  ✅ {input_file.name} -> {output_filename}")
                        else:
                            error_count += 1
                            print(f"  ❌ {input_file.name} -> {output_filename} (生成失敗)")
                            
                    except Exception as e:
                        error_count += 1
                        print(f"  ❌ {input_file.name} -> {format_type} (エラー: {e})")
                        
            except Exception as e:
                error_count += 1
                print(f"  ❌ {input_file.name} (解析エラー: {e})")
        
        print(f"\n📊 処理結果: 成功 {success_count}件, エラー {error_count}件")
        return 0 if error_count == 0 else 1
        
    except Exception as e:
        print(f"❌ 一括処理エラー: {e}")
        return 1


def main(argv: Optional[List[str]] = None) -> int:
    """メイン関数"""
    parser = setup_argument_parser()
    args = parser.parse_args(argv)
    
    # ログ設定
    log_level = 'DEBUG' if args.verbose else 'ERROR' if args.quiet else 'INFO'
    logger = setup_logger('unified_tool', log_level)
    
    # 設定読み込み
    config = ToolConfig()
    if args.config:
        config.load_from_file(args.config)
    
    # メトリクス収集開始
    metrics = None
    if args.metrics:
        metrics = MetricsCollector()
        metrics.start_collection()
    
    try:
        # コマンド実行
        if args.command == 'generate':
            result = execute_generate_command(args)
        elif args.command == 'validate':
            result = execute_validate_command(args)
        elif args.command == 'check':
            result = execute_check_command(args)
        elif args.command == 'batch':
            result = execute_batch_command(args)
        else:
            parser.print_help()
            result = 1
        
        return result
        
    finally:
        # メトリクス収集終了
        if metrics:
            metrics.stop_collection()
            if args.verbose:
                print("\n📊 実行メトリクス:")
                for key, value in metrics.get_summary().items():
                    print(f"  {key}: {value}")


if __name__ == '__main__':
    sys.exit(main())
