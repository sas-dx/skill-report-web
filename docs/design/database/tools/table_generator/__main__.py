#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成ツール - メインエントリーポイント

使用方法:
    python3 -m table_generator
    python3 -m table_generator --table MST_Employee
    python3 -m table_generator --dry-run
"""

import sys
import argparse
from pathlib import Path

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from table_generator.core.logger import EnhancedLogger
from table_generator.generators.table_definition_generator import TableDefinitionGenerator


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="テーブル定義書生成ツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全テーブル生成
  python3 -m table_generator
  
  # 個別テーブル生成
  python3 -m table_generator --table MST_Employee
  python3 -m table_generator --table MST_Role,MST_Permission
  
  # 出力先指定
  python3 -m table_generator --table MST_Employee --output-dir custom/
  
  # ドライラン
  python3 -m table_generator --dry-run
        """
    )
    
    parser.add_argument(
        '--table', '-t',
        help='生成対象テーブル名（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        help='出力先ディレクトリ'
    )
    
    parser.add_argument(
        '--base-dir', '-b',
        help='ベースディレクトリ（デフォルト: 親ディレクトリ）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='ドライラン（ファイルを実際には作成しない）'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='カラー出力を無効化'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細ログを出力'
    )
    
    args = parser.parse_args()
    
    try:
        # ベースディレクトリの設定（親ディレクトリ = database/）
        base_dir = args.base_dir or str(Path(__file__).parent.parent.parent)
        
        # ログ設定
        logger = EnhancedLogger(enable_color=not args.no_color)
        
        # ジェネレーター初期化
        generator = TableDefinitionGenerator(
            base_dir=base_dir,
            logger=logger
        )
        
        # 対象テーブル決定
        target_tables = None
        if args.table:
            target_tables = [t.strip() for t in args.table.split(',')]
        
        # 生成実行
        generator.generate_files(
            table_names=target_tables,
            output_dir=args.output_dir,
            dry_run=args.dry_run
        )
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
