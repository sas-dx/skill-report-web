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
from table_generator.core import Logger
from table_generator.core import Adapters


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
        logger = Logger(enable_color=True)
        if args.verbose:
            logger.info("詳細ログモードで実行します")
        
        # ベースディレクトリを設定（toolsディレクトリの親の親）
        base_dir = Path(__file__).parent.parent.parent
        
        # テーブル生成サービスを初期化
        service = Adapters()
        
        # 出力ディレクトリを設定
        output_dirs = {
            'ddl': base_dir / 'ddl',
            'tables': base_dir / 'tables',
            'data': base_dir / 'data'
        }
        
        if args.output:
            output_base = Path(args.output)
            output_dirs = {
                'ddl': output_base / 'ddl',
                'tables': output_base / 'tables',
                'data': output_base / 'data'
            }
        
        yaml_dir = base_dir / 'table-details'
        
        # 対象テーブルを決定
        if args.table:
            table_names = [args.table]
            logger.info(f"指定テーブル: {args.table}")
            results = service.process_multiple_tables(table_names, yaml_dir, output_dirs)
        else:
            logger.info("全テーブルを対象に生成します")
            # テーブル一覧を取得
            table_names = []
            for yaml_file in yaml_dir.glob("*_details.yaml"):
                table_name = yaml_file.stem.replace("_details", "")
                table_names.append(table_name)
            
            if not table_names:
                logger.warning("処理対象のテーブルが見つかりませんでした")
                return 1
            
            results = service.process_multiple_tables(table_names, yaml_dir, output_dirs)
        
        # 結果サマリーを取得
        summary = service.get_generation_summary(results)
        
        # 結果出力
        logger.header("テーブル生成結果")
        logger.info(f"処理対象テーブル数: {summary['total_tables']}")
        logger.info(f"成功: {summary['successful_tables']}")
        logger.info(f"失敗: {summary['failed_tables']}")
        logger.info(f"成功率: {summary['success_rate']:.1f}%")
        logger.info(f"生成ファイル数: {summary['total_generated_files']}")
        
        if summary['total_errors'] > 0:
            logger.warning(f"エラー数: {summary['total_errors']}")
            for error in summary['errors'][:5]:  # 最初の5件のみ表示
                logger.error(f"  - {error}")
        
        if summary['failed_tables'] == 0:
            logger.success("🎉 テーブル生成が正常に完了しました！")
            return 0
        else:
            logger.error("💥 一部のテーブル生成でエラーが発生しました")
            return 1
            
    except KeyboardInterrupt:
        logger.info("⏹️ ユーザーによって中断されました")
        return 130
    except Exception as e:
        logger.error(f"❌ 予期しないエラーが発生しました: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
