#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
データベース整合性チェッカー - YAMLフォーマット検証モジュール

テーブル詳細YAMLファイルが統一フォーマットに準拠しているかを検証します。
"""

import os
import sys
import yaml
from colorama import Fore, Style

# 基本パス
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(os.path.join(BASE_DIR, 'tools/yaml_validator'))

# yaml_validatorモジュールをインポート
try:
    from validate_yaml_format import (
        load_yaml, validate_yaml_structure, TEMPLATE_PATH, TABLE_DETAILS_DIR
    )
except ImportError:
    print(f"{Fore.RED}エラー: yaml_validatorモジュールが見つかりません。{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}ヒント: docs/design/database/tools/yaml_validator/validate_yaml_format.py が存在するか確認してください。{Style.RESET_ALL}")
    sys.exit(1)

def check_yaml_format(tables=None, verbose=False):
    """
    テーブル詳細YAMLファイルのフォーマットを検証する
    
    Args:
        tables (list): 検証対象のテーブル名リスト（Noneの場合は全テーブル）
        verbose (bool): 詳細なログを出力するかどうか
        
    Returns:
        dict: 検証結果
    """
    # テンプレートの読み込み
    template_data = load_yaml(TEMPLATE_PATH)
    if not template_data:
        print(f"{Fore.RED}エラー: テンプレートファイルの読み込みに失敗しました{Style.RESET_ALL}")
        return {
            'success': False,
            'error': 'テンプレートファイルの読み込みに失敗しました',
            'results': []
        }
    
    # 検証対象ファイルの特定
    target_files = []
    if tables:
        for table in tables:
            file_path = os.path.join(TABLE_DETAILS_DIR, f"{table}_details.yaml")
            if os.path.exists(file_path):
                target_files.append(file_path)
            else:
                print(f"{Fore.RED}エラー: {file_path} が見つかりません{Style.RESET_ALL}")
    else:
        for filename in os.listdir(TABLE_DETAILS_DIR):
            if filename.endswith('_details.yaml') and filename != 'MST_TEMPLATE_details.yaml':
                target_files.append(os.path.join(TABLE_DETAILS_DIR, filename))
    
    # 検証実行
    results = []
    for file_path in target_files:
        yaml_data = load_yaml(file_path)
        if yaml_data:
            result = validate_yaml_structure(yaml_data, template_data, file_path, verbose)
            results.append(result)
    
    # 結果サマリー
    valid_count = sum(1 for r in results if r['valid'])
    invalid_count = len(results) - valid_count
    
    if verbose:
        print(f"\n{Fore.CYAN}=== YAMLフォーマット検証結果 ==={Style.RESET_ALL}")
        print(f"総ファイル数: {len(results)}")
        print(f"有効: {valid_count}")
        print(f"無効: {invalid_count}")
        
        if invalid_count > 0:
            print(f"\n{Fore.RED}無効なファイル:{Style.RESET_ALL}")
            for result in results:
                if not result['valid']:
                    print(f"  {Fore.RED}❌ {result['file']}{Style.RESET_ALL}")
    
    return {
        'success': invalid_count == 0,
        'total': len(results),
        'valid': valid_count,
        'invalid': invalid_count,
        'results': results
    }

def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='テーブル詳細YAMLフォーマット検証')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    args = parser.parse_args()
    
    tables = args.tables.split(',') if args.tables else None
    result = check_yaml_format(tables, args.verbose)
    
    return 0 if result['success'] else 1

if __name__ == '__main__':
    sys.exit(main())
