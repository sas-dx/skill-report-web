#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
データベース整合性チェッカー - YAMLフォーマット検証モジュール

テーブル詳細YAMLファイルが統一フォーマットに準拠しているかを検証します。
必須セクション（revision_history, overview, notes, business_rules）の存在と内容も検証します。
"""

import os
import sys
import yaml
import glob
from typing import Dict, List, Any, Tuple, Optional
from colorama import Fore, Style, init

# colorama初期化
init()

# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
TABLE_DETAILS_DIR = os.path.join(PROJECT_ROOT, "docs/design/database/table-details")
TEMPLATE_PATH = os.path.join(TABLE_DETAILS_DIR, "MST_TEMPLATE_details.yaml")

# 必須セクションの定義
REQUIRED_SECTIONS = {
    "revision_history": {
        "description": "変更履歴の追跡・監査証跡",
        "min_entries": 1,
        "error_message": "最低1エントリが必要です"
    },
    "overview": {
        "description": "テーブルの目的・設計意図の明確化",
        "min_length": 50,
        "error_message": "最低50文字以上の説明が必要です"
    },
    "notes": {
        "description": "運用・保守に必要な特記事項",
        "min_entries": 3,
        "error_message": "最低3項目以上の記載が必要です"
    },
    "business_rules": {
        "description": "業務ルール・制約の明文化",
        "min_entries": 3,
        "error_message": "最低3項目以上の記載が必要です"
    }
}


def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """YAMLファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{Fore.RED}エラー: {file_path} の読み込みに失敗しました: {e}{Style.RESET_ALL}")
        return {}


def validate_required_sections(yaml_data: Dict[str, Any], table_name: str, verbose: bool = False) -> Tuple[bool, List[str]]:
    """必須セクションの存在と内容を検証する"""
    is_valid = True
    errors = []

    if verbose:
        print(f"{Fore.BLUE}テーブル {table_name} の必須セクション検証を実行中...{Style.RESET_ALL}")

    for section, requirements in REQUIRED_SECTIONS.items():
        if section not in yaml_data:
            is_valid = False
            error_msg = f"必須セクション '{section}' が存在しません"
            errors.append(error_msg)
            if verbose:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            continue

        # セクション固有の検証
        if section == "revision_history":
            if not isinstance(yaml_data[section], list) or len(yaml_data[section]) < requirements["min_entries"]:
                is_valid = False
                error_msg = f"'{section}': {requirements['error_message']}"
                errors.append(error_msg)
                if verbose:
                    print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            elif verbose:
                print(f"{Fore.GREEN}✓ '{section}': {len(yaml_data[section])}エントリ存在します{Style.RESET_ALL}")

        elif section == "overview":
            overview_text = str(yaml_data[section])
            if len(overview_text) < requirements["min_length"]:
                is_valid = False
                error_msg = f"'{section}': {requirements['error_message']} (現在: {len(overview_text)}文字)"
                errors.append(error_msg)
                if verbose:
                    print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            elif verbose:
                print(f"{Fore.GREEN}✓ '{section}': {len(overview_text)}文字存在します{Style.RESET_ALL}")

        elif section in ["notes", "business_rules"]:
            if not isinstance(yaml_data[section], list) or len(yaml_data[section]) < requirements["min_entries"]:
                is_valid = False
                error_msg = f"'{section}': {requirements['error_message']}"
                errors.append(error_msg)
                if verbose:
                    print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            elif verbose:
                print(f"{Fore.GREEN}✓ '{section}': {len(yaml_data[section])}項目存在します{Style.RESET_ALL}")

    if is_valid and verbose:
        print(f"{Fore.GREEN}✓ テーブル {table_name} の必須セクション検証に成功しました{Style.RESET_ALL}")

    return is_valid, errors


def validate_table_yaml(table_name: str, verbose: bool = False) -> Dict[str, Any]:
    """特定のテーブルのYAMLを検証する"""
    yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
    
    if not os.path.exists(yaml_file):
        return {
            'valid': False,
            'file': yaml_file,
            'table': table_name,
            'errors': [f"ファイル {yaml_file} が存在しません"]
        }
    
    yaml_data = load_yaml_file(yaml_file)
    if not yaml_data:
        return {
            'valid': False,
            'file': yaml_file,
            'table': table_name,
            'errors': ["YAMLファイルの読み込みに失敗しました"]
        }
    
    is_valid, errors = validate_required_sections(yaml_data, table_name, verbose)
    
    return {
        'valid': is_valid,
        'file': yaml_file,
        'table': table_name,
        'errors': errors
    }


def check_yaml_format(tables=None, verbose=False):
    """
    テーブル詳細YAMLファイルのフォーマットを検証する（基本版）
    
    Args:
        tables (list): 検証対象のテーブル名リスト（Noneの場合は全テーブル）
        verbose (bool): 詳細なログを出力するかどうか
        
    Returns:
        dict: 検証結果
    """
    results = []
    
    if tables:
        # 指定されたテーブルのみ検証
        for table in tables:
            result = validate_table_yaml(table, verbose)
            results.append(result)
    else:
        # 全テーブルを検証
        yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
        for yaml_file in yaml_files:
            table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
            if table_name == "MST_TEMPLATE":  # テンプレートファイルはスキップ
                continue
            
            if verbose:
                print(f"\n{Fore.BLUE}テーブル {table_name} の検証を開始...{Style.RESET_ALL}")
            
            result = validate_table_yaml(table_name, verbose)
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
                    print(f"  {Fore.RED}❌ {result['table']}{Style.RESET_ALL}")
                    for error in result['errors']:
                        print(f"    - {error}")
    
    # エラーがある場合の詳細表示
    if invalid_count > 0 and not verbose:
        print(f"{Fore.RED}以下のテーブルの検証に失敗しました:{Style.RESET_ALL}")
        for result in results:
            if not result['valid']:
                print(f"{Fore.RED}  - {result['table']}{Style.RESET_ALL}")
                for error in result['errors']:
                    print(f"    {Fore.RED}- {error}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}詳細なガイドラインは docs/design/database/tools/database_consistency_checker/required_sections_guide.md を参照してください。{Style.RESET_ALL}")
    
    return {
        'success': invalid_count == 0,
        'total': len(results),
        'valid': valid_count,
        'invalid': invalid_count,
        'results': results
    }


def check_yaml_format_enhanced(tables=None, verbose=False):
    """
    拡張YAMLフォーマット検証（必須セクション詳細対応）
    
    Args:
        tables (list): 検証対象のテーブル名リスト（Noneの場合は全テーブル）
        verbose (bool): 詳細なログを出力するかどうか
        
    Returns:
        dict: 拡張検証結果
        {
            'success': bool,           # 全体の成功/失敗
            'total': int,             # 総テーブル数
            'valid': int,             # 検証成功テーブル数
            'invalid': int,           # 検証失敗テーブル数
            'warning': int,           # 警告ありテーブル数
            'results': [              # 個別テーブル結果
                {
                    'valid': bool,            # 検証結果
                    'file': str,              # YAMLファイルパス
                    'table': str,             # テーブル名
                    'errors': list,           # エラーメッセージリスト
                    'warnings': list,         # 警告メッセージリスト
                    'required_sections': {    # 必須セクション検証結果
                        'revision_history': bool,
                        'overview': bool,
                        'notes': bool,
                        'business_rules': bool
                    },
                    'format_issues': list,    # フォーマット問題リスト
                    'requirement_id_issues': list  # 要求仕様ID問題リスト
                }
            ],
            'summary': {              # 検証サマリー
                'critical_errors': int,       # 🔴 必須セクション不備数
                'format_errors': int,         # フォーマットエラー数
                'requirement_errors': int,    # 要求仕様IDエラー数
                'execution_time': float       # 実行時間（秒）
            }
        }
    """
    import time
    start_time = time.time()
    
    results = []
    critical_errors = 0
    format_errors = 0
    requirement_errors = 0
    warning_count = 0
    
    if tables:
        # 指定されたテーブルのみ検証
        for table in tables:
            result = validate_table_yaml_enhanced(table, verbose)
            results.append(result)
            
            # エラー分類
            if not result['valid']:
                # 必須セクション不備をカウント
                for section, valid in result['required_sections'].items():
                    if not valid:
                        critical_errors += 1
                        break
                
                format_errors += len(result['format_issues'])
                requirement_errors += len(result['requirement_id_issues'])
            
            if result['warnings']:
                warning_count += 1
    else:
        # 全テーブルを検証
        yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
        for yaml_file in yaml_files:
            table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
            if table_name == "MST_TEMPLATE":  # テンプレートファイルはスキップ
                continue
            
            if verbose:
                print(f"\n{Fore.BLUE}テーブル {table_name} の検証を開始...{Style.RESET_ALL}")
            
            result = validate_table_yaml_enhanced(table_name, verbose)
            results.append(result)
            
            # エラー分類
            if not result['valid']:
                # 必須セクション不備をカウント
                for section, valid in result['required_sections'].items():
                    if not valid:
                        critical_errors += 1
                        break
                
                format_errors += len(result['format_issues'])
                requirement_errors += len(result['requirement_id_issues'])
            
            if result['warnings']:
                warning_count += 1
    
    # 結果サマリー
    valid_count = sum(1 for r in results if r['valid'])
    invalid_count = len(results) - valid_count
    execution_time = time.time() - start_time
    
    if verbose:
        print(f"\n{Fore.CYAN}=== YAMLフォーマット検証結果（拡張版） ==={Style.RESET_ALL}")
        print(f"総ファイル数: {len(results)}")
        print(f"有効: {valid_count}")
        print(f"無効: {invalid_count}")
        print(f"警告: {warning_count}")
        print(f"🔴 必須セクション不備: {critical_errors}テーブル")
        print(f"⏱️ 実行時間: {execution_time:.2f}秒")
        
        if invalid_count > 0:
            print(f"\n{Fore.RED}無効なファイル:{Style.RESET_ALL}")
            for result in results:
                if not result['valid']:
                    print(f"  {Fore.RED}❌ {result['table']}{Style.RESET_ALL}")
                    
                    # 必須セクション不備の詳細表示
                    for section, valid in result['required_sections'].items():
                        if not valid:
                            print(f"    🔴 {section}: 不備（絶対省略禁止）")
                    
                    # その他のエラー
                    for error in result['errors']:
                        print(f"    - {error}")
    
    # エラーがある場合の詳細表示
    if invalid_count > 0 and not verbose:
        print(f"{Fore.RED}以下のテーブルの検証に失敗しました:{Style.RESET_ALL}")
        for result in results:
            if not result['valid']:
                print(f"{Fore.RED}  - {result['table']}{Style.RESET_ALL}")
                
                # 必須セクション不備を優先表示
                critical_issues = []
                for section, valid in result['required_sections'].items():
                    if not valid:
                        critical_issues.append(f"🔴 {section}（絶対省略禁止）")
                
                if critical_issues:
                    for issue in critical_issues:
                        print(f"    {Fore.RED}{issue}{Style.RESET_ALL}")
                
                # その他のエラー
                for error in result['errors']:
                    print(f"    {Fore.RED}- {error}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}詳細なガイドラインは docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md を参照してください。{Style.RESET_ALL}")
    
    return {
        'success': invalid_count == 0,
        'total': len(results),
        'valid': valid_count,
        'invalid': invalid_count,
        'warning': warning_count,
        'results': results,
        'summary': {
            'critical_errors': critical_errors,
            'format_errors': format_errors,
            'requirement_errors': requirement_errors,
            'execution_time': execution_time
        }
    }


def validate_table_yaml_enhanced(table_name: str, verbose: bool = False) -> Dict[str, Any]:
    """拡張テーブルYAML検証"""
    yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
    
    result = {
        'valid': True,
        'file': yaml_file,
        'table': table_name,
        'errors': [],
        'warnings': [],
        'required_sections': {
            'revision_history': False,
            'overview': False,
            'notes': False,
            'business_rules': False
        },
        'format_issues': [],
        'requirement_id_issues': []
    }
    
    if not os.path.exists(yaml_file):
        result['valid'] = False
        result['errors'].append(f"ファイル {yaml_file} が存在しません")
        return result
    
    yaml_data = load_yaml_file(yaml_file)
    if not yaml_data:
        result['valid'] = False
        result['errors'].append("YAMLファイルの読み込みに失敗しました")
        return result
    
    # 必須セクション検証
    is_valid, errors = validate_required_sections(yaml_data, table_name, verbose)
    if not is_valid:
        result['valid'] = False
        result['errors'].extend(errors)
    
    # 必須セクション個別チェック
    for section in REQUIRED_SECTIONS.keys():
        if section in yaml_data:
            if section == "revision_history":
                result['required_sections'][section] = (
                    isinstance(yaml_data[section], list) and 
                    len(yaml_data[section]) >= REQUIRED_SECTIONS[section]["min_entries"]
                )
            elif section == "overview":
                result['required_sections'][section] = (
                    len(str(yaml_data[section])) >= REQUIRED_SECTIONS[section]["min_length"]
                )
            elif section in ["notes", "business_rules"]:
                result['required_sections'][section] = (
                    isinstance(yaml_data[section], list) and 
                    len(yaml_data[section]) >= REQUIRED_SECTIONS[section]["min_entries"]
                )
    
    # フォーマット検証（基本的なYAML構文チェック）
    try:
        # インデント統一チェック
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if line.strip() and line.startswith('\t'):
                    result['format_issues'].append(f"行{i}: タブ文字使用（スペース2文字推奨）")
                    result['warnings'].append(f"行{i}: インデント不統一")
    except Exception as e:
        result['format_issues'].append(f"ファイル読み込みエラー: {str(e)}")
    
    # 要求仕様ID検証
    if 'columns' in yaml_data and isinstance(yaml_data['columns'], list):
        for col in yaml_data['columns']:
            if isinstance(col, dict):
                col_name = col.get('name', 'unknown')
                requirement_id = col.get('requirement_id', '')
                
                if not requirement_id:
                    result['requirement_id_issues'].append(f"カラム {col_name}: 要求仕様ID未設定")
                    result['warnings'].append(f"カラム {col_name}: 要求仕様ID未設定")
                elif not _validate_requirement_id_format(requirement_id):
                    result['requirement_id_issues'].append(f"カラム {col_name}: 要求仕様ID形式エラー ({requirement_id})")
                    result['warnings'].append(f"カラム {col_name}: 要求仕様ID形式エラー")
    
    # 警告がある場合でも、必須セクション不備がなければ有効とする
    if result['warnings'] and result['valid']:
        # 必須セクション不備がある場合のみ無効とする
        has_critical_error = not all(result['required_sections'].values())
        if has_critical_error:
            result['valid'] = False
    
    return result


def _validate_requirement_id_format(requirement_id: str) -> bool:
    """要求仕様ID形式検証"""
    import re
    # カテゴリ.シリーズ-機能 形式（例: PRO.1-BASE.1）
    pattern = r'^[A-Z]{3}\.\d+-[A-Z]+\.\d+$'
    return bool(re.match(pattern, requirement_id))


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
