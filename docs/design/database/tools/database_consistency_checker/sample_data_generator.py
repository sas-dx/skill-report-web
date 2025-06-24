#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
サンプルデータINSERT文生成モジュール

テーブル詳細YAMLファイルのsample_dataセクションを使用して、
PostgreSQL用のINSERT文を生成します。
"""

import os
import sys
import yaml
import glob
from typing import Dict, List, Any, Optional
from colorama import Fore, Style, init

# colorama初期化
init()

# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))
TABLE_DETAILS_DIR = os.path.join(PROJECT_ROOT, "docs/design/database/table-details")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "docs/design/database/data")


def load_yaml_file(file_path: str) -> Dict[str, Any]:
    """YAMLファイルを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"{Fore.RED}エラー: {file_path} の読み込みに失敗しました: {e}{Style.RESET_ALL}")
        return {}


def format_value_for_sql(value: Any, col_type: str) -> str:
    """値をSQL用にフォーマット"""
    if value is None:
        return "NULL"
    
    # 文字列型の場合
    if col_type.startswith('VARCHAR') or col_type.startswith('TEXT') or col_type.startswith('CHAR'):
        # シングルクォートをエスケープ
        escaped_value = str(value).replace("'", "''")
        return f"'{escaped_value}'"
    
    # 数値型の場合
    elif col_type.startswith('INT') or col_type.startswith('BIGINT') or col_type.startswith('DECIMAL') or col_type.startswith('FLOAT'):
        return str(value)
    
    # ブール型の場合
    elif col_type == 'BOOLEAN':
        return 'TRUE' if value else 'FALSE'
    
    # 日付・時刻型の場合
    elif col_type in ['DATE', 'DATETIME', 'TIMESTAMP']:
        return f"'{value}'"
    
    # その他の場合は文字列として扱う
    else:
        escaped_value = str(value).replace("'", "''")
        return f"'{escaped_value}'"


def generate_insert_statements(table_name: str, yaml_data: Dict[str, Any], verbose: bool = False) -> List[str]:
    """テーブルのINSERT文を生成"""
    insert_statements = []
    
    # sample_dataの存在確認
    if 'sample_data' not in yaml_data:
        if verbose:
            print(f"{Fore.YELLOW}⚠️ テーブル {table_name}: sample_dataセクションが存在しません{Style.RESET_ALL}")
        return []
    
    sample_data = yaml_data['sample_data']
    if not isinstance(sample_data, list) or len(sample_data) == 0:
        if verbose:
            print(f"{Fore.YELLOW}⚠️ テーブル {table_name}: sample_dataが空です{Style.RESET_ALL}")
        return []
    
    # カラム定義の取得（columns形式とbusiness_columns形式の両方に対応）
    columns = yaml_data.get('columns', [])
    business_columns = yaml_data.get('business_columns', [])
    
    if not columns and not business_columns:
        if verbose:
            print(f"{Fore.RED}❌ テーブル {table_name}: カラム定義が存在しません{Style.RESET_ALL}")
        return []
    
    # カラム情報のマッピング作成
    column_info = {}
    
    # columns形式の処理
    for col in columns:
        if isinstance(col, dict):
            col_name = col.get('name')
            col_type = col.get('type', '').upper()
            if col_name:
                column_info[col_name] = col_type
    
    # business_columns形式の処理
    for col in business_columns:
        if isinstance(col, dict):
            col_name = col.get('name')
            col_type = col.get('type', '').upper()
            # lengthがある場合は型に追加
            length = col.get('length')
            if length and col_type in ['VARCHAR', 'CHAR', 'DECIMAL']:
                col_type = f"{col_type}({length})"
            if col_name:
                column_info[col_name] = col_type
    
    # 共通カラム（id, created_at, updated_at, is_deleted）を追加
    if 'id' not in column_info:
        column_info['id'] = 'VARCHAR(50)'
    if 'created_at' not in column_info:
        column_info['created_at'] = 'TIMESTAMP'
    if 'updated_at' not in column_info:
        column_info['updated_at'] = 'TIMESTAMP'
    if 'is_deleted' not in column_info:
        column_info['is_deleted'] = 'BOOLEAN'
    
    # 各レコードのINSERT文生成
    for i, record in enumerate(sample_data):
        if not isinstance(record, dict):
            if verbose:
                print(f"{Fore.RED}❌ テーブル {table_name}: sample_data[{i}]が辞書形式ではありません{Style.RESET_ALL}")
            continue
        
        # カラム名と値のリストを作成
        columns_list = []
        values_list = []
        
        # sample_dataの値を追加
        for col_name, value in record.items():
            if col_name in column_info:
                columns_list.append(col_name)
                col_type = column_info[col_name]
                formatted_value = format_value_for_sql(value, col_type)
                values_list.append(formatted_value)
        
        # 共通カラムのデフォルト値を追加（sample_dataに含まれていない場合）
        import uuid
        from datetime import datetime
        
        if 'id' not in record and 'id' in column_info:
            columns_list.append('id')
            # テーブル名の先頭3文字 + UUID短縮形でIDを生成
            table_prefix = table_name[:3].lower()
            short_uuid = str(uuid.uuid4())[:8]
            generated_id = f"{table_prefix}_{short_uuid}"
            values_list.append(f"'{generated_id}'")
        
        if 'created_at' not in record and 'created_at' in column_info:
            columns_list.append('created_at')
            values_list.append('CURRENT_TIMESTAMP')
        
        if 'updated_at' not in record and 'updated_at' in column_info:
            columns_list.append('updated_at')
            values_list.append('CURRENT_TIMESTAMP')
        
        if 'is_deleted' not in record and 'is_deleted' in column_info:
            columns_list.append('is_deleted')
            values_list.append('FALSE')
        
        if columns_list and values_list:
            columns_str = ', '.join(columns_list)
            values_str = ', '.join(values_list)
            insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
            insert_statements.append(insert_sql)
    
    if verbose and insert_statements:
        print(f"{Fore.GREEN}✓ テーブル {table_name}: {len(insert_statements)}件のINSERT文を生成しました{Style.RESET_ALL}")
    
    return insert_statements


def generate_sample_data_sql(tables: Optional[List[str]] = None, verbose: bool = False) -> Dict[str, Any]:
    """サンプルデータINSERT文を生成"""
    results = {
        'success': True,
        'total_tables': 0,
        'generated_tables': 0,
        'total_records': 0,
        'tables': {},
        'errors': []
    }
    
    # 出力ディレクトリの作成
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if tables:
        # 指定されたテーブルのみ処理
        table_list = tables
    else:
        # 全テーブルを処理
        yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
        table_list = []
        for yaml_file in yaml_files:
            table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
            if table_name != "MST_TEMPLATE":  # テンプレートファイルはスキップ
                table_list.append(table_name)
    
    results['total_tables'] = len(table_list)
    
    # 各テーブルの処理
    all_insert_statements = []
    
    for table_name in table_list:
        if verbose:
            print(f"\n{Fore.BLUE}テーブル {table_name} のサンプルデータ処理を開始...{Style.RESET_ALL}")
        
        yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
        
        if not os.path.exists(yaml_file):
            error_msg = f"ファイル {yaml_file} が存在しません"
            results['errors'].append(error_msg)
            if verbose:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            continue
        
        yaml_data = load_yaml_file(yaml_file)
        if not yaml_data:
            error_msg = f"テーブル {table_name}: YAMLファイルの読み込みに失敗しました"
            results['errors'].append(error_msg)
            if verbose:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            continue
        
        # INSERT文生成
        insert_statements = generate_insert_statements(table_name, yaml_data, verbose)
        
        if insert_statements:
            results['generated_tables'] += 1
            results['total_records'] += len(insert_statements)
            results['tables'][table_name] = {
                'records': len(insert_statements),
                'statements': insert_statements
            }
            
            # 個別ファイルに出力
            output_file = os.path.join(OUTPUT_DIR, f"{table_name}_sample_data.sql")
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"-- サンプルデータ INSERT文: {table_name}\n")
                    f.write(f"-- 生成日時: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"-- レコード数: {len(insert_statements)}\n\n")
                    
                    for stmt in insert_statements:
                        f.write(stmt + "\n")
                    
                    f.write(f"\n-- {table_name} サンプルデータ終了\n")
                
                if verbose:
                    print(f"{Fore.GREEN}✓ ファイル出力: {output_file}{Style.RESET_ALL}")
                    
            except Exception as e:
                error_msg = f"テーブル {table_name}: ファイル出力に失敗しました: {str(e)}"
                results['errors'].append(error_msg)
                if verbose:
                    print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
            
            # 全体用のリストに追加
            all_insert_statements.extend([f"-- {table_name}"] + insert_statements + [""])
    
    # 全テーブル統合ファイルの出力
    if all_insert_statements:
        combined_file = os.path.join(OUTPUT_DIR, "sample_data_all.sql")
        try:
            with open(combined_file, 'w', encoding='utf-8') as f:
                f.write("-- 全テーブル サンプルデータ INSERT文\n")
                f.write(f"-- 生成日時: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"-- 対象テーブル数: {results['generated_tables']}\n")
                f.write(f"-- 総レコード数: {results['total_records']}\n\n")
                
                for stmt in all_insert_statements:
                    f.write(stmt + "\n")
                
                f.write("\n-- 全テーブル サンプルデータ終了\n")
            
            if verbose:
                print(f"\n{Fore.GREEN}✓ 統合ファイル出力: {combined_file}{Style.RESET_ALL}")
                
        except Exception as e:
            error_msg = f"統合ファイルの出力に失敗しました: {str(e)}"
            results['errors'].append(error_msg)
            if verbose:
                print(f"{Fore.RED}❌ {error_msg}{Style.RESET_ALL}")
    
    # 結果サマリー
    if results['errors']:
        results['success'] = False
    
    if verbose:
        print(f"\n{Fore.CYAN}=== サンプルデータINSERT文生成結果 ==={Style.RESET_ALL}")
        print(f"対象テーブル数: {results['total_tables']}")
        print(f"生成成功テーブル数: {results['generated_tables']}")
        print(f"総レコード数: {results['total_records']}")
        print(f"エラー数: {len(results['errors'])}")
        
        if results['errors']:
            print(f"\n{Fore.RED}エラー詳細:{Style.RESET_ALL}")
            for error in results['errors']:
                print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")
    
    return results


def validate_and_generate(tables: Optional[List[str]] = None, verbose: bool = False) -> Dict[str, Any]:
    """sample_data検証とINSERT文生成を統合実行"""
    try:
        from yaml_format_check import validate_sample_data_quality
    except ImportError:
        # 検証機能が利用できない場合は生成のみ実行
        if verbose:
            print(f"{Fore.YELLOW}⚠️ 検証機能が利用できません。生成のみ実行します。{Style.RESET_ALL}")
        return generate_sample_data_sql(tables, verbose)
    
    results = {
        'validation': {
            'success': True,
            'total_tables': 0,
            'valid_tables': 0,
            'errors': []
        },
        'generation': {
            'success': True,
            'total_tables': 0,
            'generated_tables': 0,
            'total_records': 0,
            'tables': {},
            'errors': []
        },
        'overall_success': True
    }
    
    if verbose:
        print(f"{Fore.CYAN}=== サンプルデータ検証・INSERT文生成 統合実行 ==={Style.RESET_ALL}")
    
    # 対象テーブルの決定
    if tables:
        table_list = tables
    else:
        yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
        table_list = []
        for yaml_file in yaml_files:
            table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
            if table_name != "MST_TEMPLATE":
                table_list.append(table_name)
    
    results['validation']['total_tables'] = len(table_list)
    results['generation']['total_tables'] = len(table_list)
    
    # 各テーブルの検証と生成
    valid_tables = []
    
    for table_name in table_list:
        if verbose:
            print(f"\n{Fore.BLUE}テーブル {table_name} の処理を開始...{Style.RESET_ALL}")
        
        yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
        
        if not os.path.exists(yaml_file):
            error_msg = f"ファイル {yaml_file} が存在しません"
            results['validation']['errors'].append(error_msg)
            results['generation']['errors'].append(error_msg)
            continue
        
        yaml_data = load_yaml_file(yaml_file)
        if not yaml_data:
            error_msg = f"テーブル {table_name}: YAMLファイルの読み込みに失敗しました"
            results['validation']['errors'].append(error_msg)
            results['generation']['errors'].append(error_msg)
            continue
        
        # sample_data検証
        is_valid, validation_errors = validate_sample_data_quality(yaml_data, table_name, verbose)
        
        if is_valid:
            results['validation']['valid_tables'] += 1
            valid_tables.append(table_name)
            
            if verbose:
                print(f"{Fore.GREEN}✓ テーブル {table_name}: sample_data検証成功{Style.RESET_ALL}")
        else:
            results['validation']['errors'].extend([f"{table_name}: {error}" for error in validation_errors])
            if verbose:
                print(f"{Fore.RED}❌ テーブル {table_name}: sample_data検証失敗{Style.RESET_ALL}")
                for error in validation_errors:
                    print(f"  {Fore.RED}- {error}{Style.RESET_ALL}")
    
    # 検証成功テーブルのINSERT文生成
    if valid_tables:
        if verbose:
            print(f"\n{Fore.BLUE}検証成功テーブルのINSERT文生成を開始...{Style.RESET_ALL}")
        
        generation_result = generate_sample_data_sql(valid_tables, verbose)
        results['generation'] = generation_result
    
    # 全体結果の判定
    results['validation']['success'] = len(results['validation']['errors']) == 0
    results['overall_success'] = results['validation']['success'] and results['generation']['success']
    
    if verbose:
        print(f"\n{Fore.CYAN}=== 統合実行結果サマリー ==={Style.RESET_ALL}")
        print(f"検証: {results['validation']['valid_tables']}/{results['validation']['total_tables']} テーブル成功")
        print(f"生成: {results['generation']['generated_tables']}/{results['generation']['total_tables']} テーブル成功")
        print(f"総レコード数: {results['generation']['total_records']}")
        print(f"全体成功: {'✓' if results['overall_success'] else '❌'}")
    
    return results


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='サンプルデータINSERT文生成')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    parser.add_argument('--validate', action='store_true', help='検証も同時実行')
    args = parser.parse_args()
    
    tables = args.tables.split(',') if args.tables else None
    
    if args.validate:
        result = validate_and_generate(tables, args.verbose)
        return 0 if result['overall_success'] else 1
    else:
        result = generate_sample_data_sql(tables, args.verbose)
        return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
