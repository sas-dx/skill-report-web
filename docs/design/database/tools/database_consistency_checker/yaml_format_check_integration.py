#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAMLフォーマット検証統合パッチ

このスクリプトは、database_consistency_checkerにYAMLフォーマット検証機能を統合するためのパッチです。
__main__.pyを直接修正せずに、追加の機能として提供します。

使用方法:
  python yaml_format_check_integration.py [options]
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# 基本パス
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(os.path.join(BASE_DIR, 'tools/yaml_validator'))

# yaml_validatorモジュールをインポート
try:
    from validate_yaml_format import (
        load_yaml, validate_yaml_structure, TEMPLATE_PATH, TABLE_DETAILS_DIR
    )
    yaml_validator_available = True
except ImportError:
    yaml_validator_available = False
    print("警告: yaml_validatorモジュールが見つかりません。YAMLフォーマット検証は無効になります。")

def setup_logger(verbose=False):
    """ログ設定"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)

def check_yaml_format(tables=None, verbose=False):
    """
    テーブル詳細YAMLファイルのフォーマットを検証する
    
    Args:
        tables (list): 検証対象のテーブル名リスト（Noneの場合は全テーブル）
        verbose (bool): 詳細なログを出力するかどうか
        
    Returns:
        dict: 検証結果
    """
    logger = setup_logger(verbose)
    
    if not yaml_validator_available:
        logger.warning("yaml_validatorモジュールが利用できないため、YAMLフォーマット検証をスキップします")
        return {
            'success': True,
            'error': 'yaml_validatorモジュールが利用できません',
            'results': []
        }
    
    # テンプレートの読み込み
    template_data = load_yaml(TEMPLATE_PATH)
    if not template_data:
        logger.error("テンプレートファイルの読み込みに失敗しました")
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
                logger.warning(f"{file_path} が見つかりません")
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
    warning_count = sum(1 for r in results if r['warnings'])
    
    logger.info(f"=== YAMLフォーマット検証結果 ===")
    logger.info(f"総ファイル数: {len(results)}")
    logger.info(f"有効: {valid_count}")
    logger.info(f"無効: {invalid_count}")
    logger.info(f"警告あり: {warning_count}")
    
    if invalid_count > 0:
        logger.error("無効なファイル:")
        for result in results:
            if not result['valid']:
                logger.error(f"  ❌ {result['file']}")
                for error in result['errors']:
                    logger.error(f"    - {error}")
    
    return {
        'success': invalid_count == 0,
        'total': len(results),
        'valid': valid_count,
        'invalid': invalid_count,
        'with_warnings': warning_count,
        'results': results
    }

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='テーブル詳細YAMLフォーマット検証統合パッチ')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    parser.add_argument('--output-format', choices=['text', 'json', 'markdown'], default='text', help='出力形式')
    parser.add_argument('--output-file', help='結果出力ファイル')
    args = parser.parse_args()
    
    tables = args.tables.split(',') if args.tables else None
    result = check_yaml_format(tables, args.verbose)
    
    # 結果出力
    if args.output_format == 'json':
        import json
        output = json.dumps(result, indent=2, ensure_ascii=False)
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            print(output)
    elif args.output_format == 'markdown':
        output = "# YAMLフォーマット検証結果\n\n"
        output += f"- 総ファイル数: {result['total']}\n"
        output += f"- 有効: {result['valid']}\n"
        output += f"- 無効: {result['invalid']}\n"
        output += f"- 警告あり: {result['with_warnings']}\n\n"
        
        if result['invalid'] > 0:
            output += "## 無効なファイル\n\n"
            for r in result['results']:
                if not r['valid']:
                    output += f"### {r['file']}\n\n"
                    output += "#### エラー\n\n"
                    for error in r['errors']:
                        output += f"- {error}\n"
                    output += "\n"
        
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(output)
        else:
            print(output)
    else:
        # テキスト形式（デフォルト）
        if args.output_file:
            with open(args.output_file, 'w', encoding='utf-8') as f:
                f.write(f"=== YAMLフォーマット検証結果 ===\n")
                f.write(f"総ファイル数: {result['total']}\n")
                f.write(f"有効: {result['valid']}\n")
                f.write(f"無効: {result['invalid']}\n")
                f.write(f"警告あり: {result['with_warnings']}\n\n")
                
                if result['invalid'] > 0:
                    f.write("無効なファイル:\n")
                    for r in result['results']:
                        if not r['valid']:
                            f.write(f"  ❌ {r['file']}\n")
                            for error in r['errors']:
                                f.write(f"    - {error}\n")
        
    return 0 if result['success'] else 1

if __name__ == '__main__':
    sys.exit(main())
