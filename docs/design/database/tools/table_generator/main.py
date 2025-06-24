#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツールのメイン実行モジュール

YAMLファイルからテーブル定義書・DDL・サンプルデータを生成するメイン処理
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.core.logger import get_logger
from table_generator.generators.table_definition_generator import TableDefinitionGenerator


def parse_arguments():
    """コマンドライン引数を解析"""
    parser = argparse.ArgumentParser(
        description="YAMLファイルからテーブル定義書・DDL・サンプルデータを生成"
    )
    
    parser.add_argument(
        "--table", "-t",
        type=str,
        help="生成対象のテーブル名（指定しない場合は全テーブル）"
    )
    
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="全テーブルを対象に生成"
    )
    
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="出力先ディレクトリ（指定しない場合はデフォルト）"
    )
    
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="ドライラン実行（ファイル出力なし）"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="詳細ログ出力"
    )
    
    return parser.parse_args()


def main():
    """メイン実行関数"""
    try:
        # 引数解析
        args = parse_arguments()
        
        # ログ設定
        logger = get_logger()
        if args.verbose:
            logger.info("詳細ログモードで実行します")
        
        # ベースディレクトリを設定（toolsディレクトリの親の親）
        base_dir = Path(__file__).parent.parent.parent
        
        # テーブル生成器を初期化
        generator = TableDefinitionGenerator(
            base_dir=str(base_dir),
            logger=logger
        )
        
        # 対象テーブルを決定
        table_names = None
        if args.table:
            table_names = [args.table]
            logger.info(f"指定テーブル: {args.table}")
        elif args.all:
            logger.info("全テーブルを対象に生成します")
        else:
            logger.info("全テーブルを対象に生成します（デフォルト）")
        
        # 生成実行
        result = generator.generate_files(
            table_names=table_names,
            output_dir=args.output,
            dry_run=args.dry_run
        )
        
        # 結果出力
        if result.success:
            logger.info("🎉 テーブル生成が正常に完了しました！")
            return 0
        else:
            logger.error("💥 テーブル生成でエラーが発生しました")
            if result.error_message:
                logger.error(f"エラー詳細: {result.error_message}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("⏹️ ユーザーによって中断されました")
        return 130
    except Exception as e:
        logger.error(f"❌ 予期しないエラーが発生しました: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
