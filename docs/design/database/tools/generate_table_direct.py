#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成の直接実行スクリプト

table_generatorのmain.pyが不足しているため、
TableDefinitionGeneratorを直接実行するスクリプト
"""

import sys
from pathlib import Path

# ツールディレクトリをパスに追加
tools_dir = Path(__file__).parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

from table_generator.generators.table_definition_generator import TableDefinitionGenerator

def main():
    """メイン処理"""
    import argparse
    
    parser = argparse.ArgumentParser(description='テーブル定義書生成ツール')
    parser.add_argument('--table', type=str, help='生成対象テーブル名')
    parser.add_argument('--verbose', action='store_true', help='詳細ログ出力')
    parser.add_argument('--dry-run', action='store_true', help='ドライラン実行')
    
    args = parser.parse_args()
    
    try:
        # ベースディレクトリを設定（toolsディレクトリの親）
        base_dir = tools_dir.parent
        
        # テーブル生成器を初期化
        generator = TableDefinitionGenerator(base_dir=str(base_dir))
        
        # テーブル名が指定されている場合
        if args.table:
            table_names = [args.table]
        else:
            table_names = None
        
        # テーブル定義書を生成
        result = generator.generate_files(
            table_names=table_names,
            dry_run=args.dry_run
        )
        
        if result.success:
            print(f"✅ 処理が正常に完了しました")
            print(f"📁 生成ファイル数: {len(result.generated_files)}")
            if args.verbose:
                for file_path in result.generated_files:
                    print(f"  - {file_path}")
        else:
            print(f"❌ 処理でエラーが発生しました: {result.error_message}")
            if result.errors:
                for error in result.errors:
                    print(f"  - {error}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ 実行エラー: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
