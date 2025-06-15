#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
テーブル詳細YAML定義ファイルの必須セクション検証ツール

このスクリプトは、テーブル詳細YAML定義ファイルに必須セクション
（revision_history, overview, notes, business_rules）が存在するかどうかを
検証します。

使用方法:
    # 特定テーブルの検証
    python validate_yaml_format.py --table MST_Employee

    # 全テーブルの検証
    python validate_yaml_format.py --all

    # 詳細出力モード
    python validate_yaml_format.py --table MST_Employee --verbose
"""

import os
import sys
import yaml
import argparse
import glob
from typing import Dict, List, Any, Tuple, Optional


# 色付き出力用
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../.."))
TABLE_DETAILS_DIR = os.path.join(PROJECT_ROOT, "docs/design/database/table-details")


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
        print(f"{Colors.RED}エラー: {file_path} の読み込みに失敗しました: {e}{Colors.ENDC}")
        return {}


def validate_required_sections(yaml_data: Dict[str, Any], table_name: str, verbose: bool = False) -> Tuple[bool, List[str]]:
    """必須セクションの存在と内容を検証する"""
    is_valid = True
    errors = []

    if verbose:
        print(f"{Colors.BLUE}テーブル {table_name} の必須セクション検証を実行中...{Colors.ENDC}")

    for section, requirements in REQUIRED_SECTIONS.items():
        if section not in yaml_data:
            is_valid = False
            error_msg = f"必須セクション '{section}' が存在しません"
            errors.append(error_msg)
            if verbose:
                print(f"{Colors.RED}❌ {error_msg}{Colors.ENDC}")
            continue

        # セクション固有の検証
        if section == "revision_history":
            if not isinstance(yaml_data[section], list) or len(yaml_data[section]) < requirements["min_entries"]:
                is_valid = False
                error_msg = f"'{section}': {requirements['error_message']}"
                errors.append(error_msg)
                if verbose:
                    print(f"{Colors.RED}❌ {error_msg}{Colors.ENDC}")
            elif verbose:
                print(f"{Colors.GREEN}✓ '{section}': {len(yaml_data[section])}エントリ存在します{Colors.ENDC}")

        elif section == "overview":
            overview_text = str(yaml_data[section])
            if len(overview_text) < requirements["min_length"]:
                is_valid = False
                error_msg = f"'{section}': {requirements['error_message']} (現在: {len(overview_text)}文字)"
                errors.append(error_msg)
                if verbose:
                    print(f"{Colors.RED}❌ {error_msg}{Colors.ENDC}")
            elif verbose:
                print(f"{Colors.GREEN}✓ '{section}': {len(overview_text)}文字存在します{Colors.ENDC}")

        elif section in ["notes", "business_rules"]:
            if not isinstance(yaml_data[section], list) or len(yaml_data[section]) < requirements["min_entries"]:
                is_valid = False
                error_msg = f"'{section}': {requirements['error_message']}"
                errors.append(error_msg)
                if verbose:
                    print(f"{Colors.RED}❌ {error_msg}{Colors.ENDC}")
            elif verbose:
                print(f"{Colors.GREEN}✓ '{section}': {len(yaml_data[section])}項目存在します{Colors.ENDC}")

    if is_valid and verbose:
        print(f"{Colors.GREEN}✓ テーブル {table_name} の必須セクション検証に成功しました{Colors.ENDC}")

    return is_valid, errors


def validate_table(table_name: str, verbose: bool = False) -> bool:
    """特定のテーブルを検証する"""
    yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
    
    if not os.path.exists(yaml_file):
        print(f"{Colors.RED}エラー: {yaml_file} が存在しません{Colors.ENDC}")
        return False
    
    yaml_data = load_yaml_file(yaml_file)
    if not yaml_data:
        return False
    
    is_valid, errors = validate_required_sections(yaml_data, table_name, verbose)
    
    if not is_valid:
        print(f"{Colors.RED}エラー: テーブル {table_name} の必須セクション検証に失敗しました{Colors.ENDC}")
        if not verbose:  # verboseモードでない場合のみ、ここでエラーを表示
            for error in errors:
                print(f"{Colors.RED}  - {error}{Colors.ENDC}")
        print(f"{Colors.YELLOW}詳細なガイドラインは docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md を参照してください。{Colors.ENDC}")
        return False
    
    return True


def validate_all_tables(verbose: bool = False) -> bool:
    """全てのテーブルを検証する"""
    yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
    if not yaml_files:
        print(f"{Colors.RED}エラー: {TABLE_DETAILS_DIR} にYAMLファイルが見つかりません{Colors.ENDC}")
        return False
    
    all_valid = True
    failed_tables = []
    
    for yaml_file in yaml_files:
        table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
        if table_name == "MST_TEMPLATE":  # テンプレートファイルはスキップ
            continue
        
        if verbose:
            print(f"\n{Colors.BLUE}テーブル {table_name} の検証を開始...{Colors.ENDC}")
        
        is_valid = validate_table(table_name, verbose)
        if not is_valid:
            all_valid = False
            failed_tables.append(table_name)
    
    if all_valid:
        print(f"{Colors.GREEN}全てのテーブル詳細YAML定義ファイルの必須セクション検証に成功しました{Colors.ENDC}")
    else:
        print(f"{Colors.RED}以下のテーブルの検証に失敗しました:{Colors.ENDC}")
        for table in failed_tables:
            print(f"{Colors.RED}  - {table}{Colors.ENDC}")
        print(f"{Colors.YELLOW}詳細なガイドラインは docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md を参照してください。{Colors.ENDC}")
    
    return all_valid


def main():
    parser = argparse.ArgumentParser(description='テーブル詳細YAML定義ファイルの必須セクション検証ツール')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--table', help='検証対象のテーブル名')
    group.add_argument('--all', action='store_true', help='全テーブルを検証')
    parser.add_argument('--verbose', action='store_true', help='詳細な出力を表示')
    
    args = parser.parse_args()
    
    if args.table:
        success = validate_table(args.table, args.verbose)
    else:
        success = validate_all_tables(args.verbose)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
