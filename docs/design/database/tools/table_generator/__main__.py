#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 共通ライブラリ対応メインエントリーポイント

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

共通ライブラリを使用したテーブル定義書・DDL・サンプルデータの自動生成
"""

import sys
import argparse
from pathlib import Path
import logging

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 共通ライブラリをインポート
from docs.design.database.tools.shared.core.config import get_config, DatabaseToolsConfig
from docs.design.database.tools.shared.parsers.yaml_parser import YamlParser
from docs.design.database.tools.shared.generators.ddl_generator import DDLGenerator
from docs.design.database.tools.shared.generators.markdown_generator import MarkdownGenerator
from docs.design.database.tools.shared.generators.sample_data_generator import SampleDataGenerator
from docs.design.database.tools.shared.core.exceptions import (
    DatabaseToolsError, 
    ParsingError, 
    GenerationError
)


def setup_logger(verbose: bool = False):
    """ログ設定"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


class TableGeneratorService:
    """テーブル生成サービス - 共通ライブラリ使用版"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # パーサーとジェネレーターの初期化
        self.yaml_parser = YamlParser(config.to_dict())
        self.ddl_generator = DDLGenerator(config.to_dict())
        self.markdown_generator = MarkdownGenerator(config.to_dict())
        self.sample_data_generator = SampleDataGenerator(config.to_dict())
    
    def process_table(self, table_name: str) -> dict:
        """テーブル処理実行"""
        result = {
            'table_name': table_name,
            'success': False,
            'files_generated': [],
            'errors': []
        }
        
        try:
            self.logger.info(f"テーブル処理開始: {table_name}")
            
            # YAML詳細定義の読み込み
            yaml_file = self.config.table_details_dir / f"{table_name}_details.yaml"
            if not yaml_file.exists():
                raise ParsingError(f"YAML詳細定義ファイルが見つかりません: {yaml_file}")
            
            # テーブル定義の解析
            table_def = self.yaml_parser.parse_file(yaml_file)
            self.logger.debug(f"テーブル定義解析完了: {table_def.name}")
            
            # 出力ディレクトリの作成
            self._ensure_output_directories()
            
            # DDLファイル生成
            ddl_content = self.ddl_generator.generate(table_def)
            ddl_file = self.config.ddl_dir / f"{table_name}.sql"
            ddl_file.write_text(ddl_content, encoding='utf-8')
            result['files_generated'].append(str(ddl_file))
            self.logger.info(f"DDLファイル生成完了: {ddl_file}")
            
            # Markdownファイル生成
            markdown_content = self.markdown_generator.generate(table_def)
            logical_name = table_def.logical_name or table_def.name
            markdown_file = self.config.tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
            markdown_file.write_text(markdown_content, encoding='utf-8')
            result['files_generated'].append(str(markdown_file))
            self.logger.info(f"Markdownファイル生成完了: {markdown_file}")
            
            # サンプルデータファイル生成
            sample_data_content = self.sample_data_generator.generate(table_def)
            sample_data_file = self.config.data_dir / f"{table_name}_sample_data.sql"
            sample_data_file.write_text(sample_data_content, encoding='utf-8')
            result['files_generated'].append(str(sample_data_file))
            self.logger.info(f"サンプルデータファイル生成完了: {sample_data_file}")
            
            result['success'] = True
            self.logger.info(f"テーブル処理完了: {table_name}")
            
        except Exception as e:
            error_msg = f"テーブル処理エラー: {table_name} - {str(e)}"
            self.logger.error(error_msg)
            result['errors'].append(error_msg)
            
        return result
    
    def _ensure_output_directories(self):
        """出力ディレクトリの作成"""
        directories = [
            self.config.ddl_dir,
            self.config.tables_dir,
            self.config.data_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='テーブル生成ツール - 共通ライブラリ対応版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全テーブル生成
  python3 -m table_generator
  
  # 個別テーブル生成
  python3 -m table_generator --table MST_Employee
  python3 -m table_generator --table MST_Role,MST_Permission
  
  # 詳細ログ出力
  python3 -m table_generator --verbose
        """
    )
    
    parser.add_argument(
        '--table', '-t',
        type=str,
        help='処理対象テーブル名（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        default='config.yaml',
        help='設定ファイルパス（デフォルト: config.yaml）'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細ログ出力'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        help='出力ディレクトリ（設定ファイルの値を上書き）'
    )
    
    parser.add_argument(
        '--yaml-dir', '-y',
        type=str,
        help='YAML詳細定義ディレクトリ（設定ファイルの値を上書き）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='ドライラン（ファイルを実際には作成しない）'
    )
    
    args = parser.parse_args()
    
    try:
        # ログ設定
        setup_logger(args.verbose)
        logger = logging.getLogger(__name__)
        
        # 統合設定を使用
        config = get_config()
        
        # コマンドライン引数で設定を上書き（必要に応じて）
        if args.verbose:
            config.verbose = True
        
        logger.info("テーブル生成ツール開始（共通ライブラリ対応版）")
        logger.info(f"ベースディレクトリ: {config.base_dir}")
        logger.info(f"YAML詳細定義ディレクトリ: {config.table_details_dir}")
        logger.info(f"DDLディレクトリ: {config.ddl_dir}")
        logger.info(f"テーブル定義書ディレクトリ: {config.tables_dir}")
        logger.info(f"サンプルデータディレクトリ: {config.data_dir}")
        
        # 処理対象テーブル決定
        if args.table:
            target_tables = [t.strip() for t in args.table.split(',')]
        else:
            # 全テーブル処理の場合、YAML詳細定義ディレクトリから取得
            yaml_files = list(config.table_details_dir.glob("*_details.yaml"))
            target_tables = [f.stem.replace("_details", "") for f in yaml_files]
        
        if not target_tables:
            logger.warning("処理対象テーブルが見つかりません")
            return 0
        
        logger.info(f"処理対象テーブル: {', '.join(target_tables)}")
        
        if args.dry_run:
            print(f"\n=== ドライラン結果 ===")
            print(f"処理対象テーブル数: {len(target_tables)}")
            print(f"対象テーブル: {', '.join(target_tables)}")
            logger.info("ドライラン完了")
            return 0
        
        # テーブル処理サービス初期化
        service = TableGeneratorService(config)
        
        # テーブル処理実行
        results = []
        for table_name in target_tables:
            result = service.process_table(table_name)
            results.append(result)
        
        # 結果サマリー出力
        total_tables = len(results)
        success_count = sum(1 for r in results if r['success'])
        error_count = total_tables - success_count
        
        print(f"\n=== 処理結果サマリー ===")
        print(f"処理対象テーブル数: {total_tables}")
        print(f"成功: {success_count}")
        print(f"エラー: {error_count}")
        
        if success_count > 0:
            print(f"\n=== 生成ファイル ===")
            for result in results:
                if result['success']:
                    print(f"テーブル: {result['table_name']}")
                    for file_path in result['files_generated']:
                        print(f"  - {file_path}")
        
        if error_count > 0:
            print(f"\n=== エラー詳細 ===")
            for result in results:
                if not result['success']:
                    print(f"テーブル: {result['table_name']}")
                    for error in result['errors']:
                        print(f"  - {error}")
        
        logger.info("テーブル生成ツール完了")
        return 0 if error_count == 0 else 1
        
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
