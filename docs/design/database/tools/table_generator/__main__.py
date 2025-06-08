#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 統合データモデル対応メインエントリーポイント

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

統合データモデルを使用したテーブル定義書・DDL・サンプルデータの自動生成
既存機能の100%互換性を保証
"""

import sys
import argparse
from pathlib import Path
import logging

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 統合データモデル対応のアダプターをインポート
from docs.design.database.tools.table_generator.core.adapters import (
    create_legacy_compatible_service,
    UnifiedTableGeneratorService
)
from docs.design.database.tools.table_generator.core.config import TableGeneratorConfig
from docs.design.database.tools.table_generator.utils.logger import setup_logger


def main():
    """メイン処理 - 統合データモデル強制適用版"""
    parser = argparse.ArgumentParser(
        description='テーブル生成ツール - 統合データモデル対応版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全テーブル生成（統合データモデル使用）
  python3 -m table_generator
  
  # 個別テーブル生成
  python3 -m table_generator --table MST_Employee
  python3 -m table_generator --table MST_Role,MST_Permission
  
  # 統合モデル強制使用
  python3 -m table_generator --unified-model
  
  # 既存互換モード（レガシーサポート）
  python3 -m table_generator --legacy-mode
        """
    )
    
    parser.add_argument(
        '--table', '-t',
        type=str,
        help='処理対象テーブル名（カンマ区切りで複数指定可能、*でワイルドカード指定可能）'
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
        '--unified-model',
        action='store_true',
        help='統合データモデル強制使用（デフォルト）'
    )
    
    parser.add_argument(
        '--legacy-mode',
        action='store_true',
        help='既存互換モード（レガシーサポート）'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='ドライラン（ファイルを実際には作成しない）'
    )
    
    args = parser.parse_args()
    
    try:
        # 設定読み込み
        config_path = Path(args.config)
        if not config_path.exists():
            # デフォルト設定ファイルパスを試行
            default_config = Path(__file__).parent / 'config.yaml'
            if default_config.exists():
                config_path = default_config
            else:
                # 設定ファイルがない場合はデフォルト設定を使用
                config = TableGeneratorConfig()
                config_path = None
        
        if config_path:
            config = TableGeneratorConfig.from_yaml(config_path)
        else:
            config = TableGeneratorConfig()
        
        # コマンドライン引数で設定を上書き
        if args.output_dir:
            config.output_dir = Path(args.output_dir)
        if args.yaml_dir:
            config.yaml_dir = Path(args.yaml_dir)
        if args.verbose:
            config.verbose = True
        
        # ログ設定
        setup_logger(config.verbose)
        logger = logging.getLogger(__name__)
        
        logger.info("テーブル生成ツール開始（統合データモデル対応版）")
        if config_path:
            logger.info(f"設定ファイル: {config_path}")
        logger.info(f"YAML詳細定義ディレクトリ: {config.yaml_dir}")
        logger.info(f"出力ディレクトリ: {config.output_dir}")
        
        # 処理モード決定（統合データモデルをデフォルトに）
        use_unified_model = not args.legacy_mode  # レガシーモード指定時のみ既存モード
        
        if use_unified_model:
            logger.info("統合データモデルを使用します")
            service = UnifiedTableGeneratorService()
        else:
            logger.info("既存互換モードを使用します")
            service = create_legacy_compatible_service()
        
        # 処理対象テーブル決定
        if args.table:
            target_tables = [t.strip() for t in args.table.split(',')]
        else:
            # 全テーブル処理の場合、YAML詳細定義ディレクトリから取得
            yaml_files = list(config.yaml_dir.glob("*_details.yaml"))
            target_tables = [f.stem.replace("_details", "") for f in yaml_files]
        
        if not target_tables:
            logger.warning("処理対象テーブルが見つかりません")
            return 0
        
        logger.info(f"処理対象テーブル: {', '.join(target_tables)}")
        
        # テーブル処理実行
        results = []
        for table_name in target_tables:
            logger.info(f"テーブル処理開始: {table_name}")
            
            if args.dry_run:
                logger.info(f"ドライラン: {table_name} の処理をスキップ")
                continue
            
            try:
                if use_unified_model:
                    # 統合データモデルで処理
                    result = service.process_table_with_unified_model(
                        table_name, config.yaml_dir, config.output_dir
                    )
                    # 統合結果を既存形式に変換（サマリー表示用）
                    from docs.design.database.tools.table_generator.core.adapters import TableGeneratorAdapter
                    adapter = TableGeneratorAdapter()
                    legacy_result = adapter.unified_to_legacy_result(result)
                    results.append(legacy_result)
                else:
                    # 既存互換モードで処理
                    result = service.process_table(
                        table_name, config.yaml_dir, config.output_dir
                    )
                    results.append(result)
                
                if result.success if hasattr(result, 'success') else result.is_success():
                    logger.info(f"テーブル処理完了: {table_name}")
                else:
                    logger.error(f"テーブル処理エラー: {table_name}")
                    
            except Exception as e:
                logger.error(f"テーブル処理中にエラーが発生: {table_name} - {e}")
                # エラー結果を作成
                from docs.design.database.tools.table_generator.core.models import ProcessingResult
                error_result = ProcessingResult(
                    table_name=table_name,
                    logical_name=table_name,
                    success=False,
                    has_yaml=False,
                    error_message=str(e)
                )
                results.append(error_result)
        
        # 結果サマリー出力
        if not args.dry_run:
            total_tables = len(results)
            success_count = sum(1 for r in results if r.success)
            error_count = total_tables - success_count
            
            print(f"\n=== 処理結果サマリー ===")
            print(f"処理対象テーブル数: {total_tables}")
            print(f"成功: {success_count}")
            print(f"エラー: {error_count}")
            print(f"使用モデル: {'統合データモデル' if use_unified_model else '既存互換モード'}")
            
            if error_count > 0:
                print(f"\n=== エラー詳細 ===")
                for result in results:
                    if not result.success:
                        print(f"テーブル: {result.table_name}")
                        if result.error_message:
                            print(f"  エラー: {result.error_message}")
                        if hasattr(result, 'errors') and result.errors:
                            for error in result.errors:
                                print(f"  - {error}")
            
            logger.info("テーブル生成ツール完了")
            return 0 if error_count == 0 else 1
        else:
            print(f"\n=== ドライラン結果 ===")
            print(f"処理対象テーブル数: {len(target_tables)}")
            print(f"対象テーブル: {', '.join(target_tables)}")
            print(f"使用モデル: {'統合データモデル' if use_unified_model else '既存互換モード'}")
            logger.info("ドライラン完了")
            return 0
        
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
