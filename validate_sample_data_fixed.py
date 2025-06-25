#!/usr/bin/env python3
"""
YAML定義とサンプルデータの整合性チェック（修正版）
"""

import os
import re
import glob
import yaml
from pathlib import Path
from datetime import datetime

def load_yaml_definitions():
    """YAML定義ファイルを読み込み"""
    yaml_dir = Path("docs/design/database/table-details")
    yaml_files = list(yaml_dir.glob("テーブル詳細定義YAML_*.yaml"))
    
    tables = {}
    print("📂 YAML定義ファイルを読み込み中...")
    
    for yaml_file in yaml_files:
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                if data and 'table_name' in data:
                    table_name = data['table_name']
                    tables[table_name] = data
                    print(f"  ✅ {table_name}")
        except Exception as e:
            print(f"  ❌ {yaml_file.name}: {e}")
    
    print(f"📊 読み込み完了: {len(tables)} テーブル")
    return tables

def load_sample_data():
    """サンプルデータファイルを読み込み（修正版）"""
    data_dir = Path("docs/design/database/data")
    sql_files = list(data_dir.glob("*_sample_data.sql"))
    
    tables = {}
    print("📂 サンプルデータファイルを読み込み中...")
    
    for sql_file in sql_files:
        try:
            with open(sql_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # INSERT文の検索（改善版）
                insert_pattern = r'INSERT\s+INTO\s+(\w+)\s*\([^)]+\)\s*VALUES'
                matches = re.findall(insert_pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                
                if matches:
                    table_name = matches[0]
                    
                    # カラム名の抽出
                    column_pattern = r'INSERT\s+INTO\s+\w+\s*\(([^)]+)\)'
                    column_match = re.search(column_pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL)
                    
                    if column_match:
                        columns_text = column_match.group(1)
                        columns = [col.strip() for col in columns_text.split(',')]
                        columns = [col for col in columns if col]  # 空文字列を除去
                        
                        tables[table_name] = {
                            'columns': columns,
                            'file': sql_file.name
                        }
                        print(f"  ✅ {table_name}: {len(columns)} カラム")
                    else:
                        print(f"  ⚠️ {sql_file.name}: カラム定義が見つかりません")
                else:
                    print(f"  ⚠️ {sql_file.name}: INSERT文が見つかりません")
                    
        except Exception as e:
            print(f"  ❌ {sql_file.name}: {e}")
    
    print(f"📊 読み込み完了: {len(tables)} テーブル")
    return tables

def check_consistency(yaml_tables, sample_tables):
    """整合性チェック"""
    print("🔍 テーブル存在整合性をチェック中...")
    
    yaml_set = set(yaml_tables.keys())
    sample_set = set(sample_tables.keys())
    
    missing_sample = yaml_set - sample_set
    missing_yaml = sample_set - yaml_set
    
    print(f"  📊 YAML定義: {len(yaml_set)} テーブル")
    print(f"  📊 サンプルデータ: {len(sample_set)} テーブル")
    print(f"  ⚠️ サンプルデータ不足: {len(missing_sample)} テーブル")
    print(f"  ❌ YAML定義不足: {len(missing_yaml)} テーブル")
    
    # カラム整合性チェック
    print("🔍 カラム整合性をチェック中...")
    column_issues = []
    
    for table_name in yaml_set & sample_set:
        yaml_columns = [col['name'] for col in yaml_tables[table_name].get('columns', [])]
        sample_columns = sample_tables[table_name]['columns']
        
        yaml_col_set = set(yaml_columns)
        sample_col_set = set(sample_columns)
        
        missing_in_sample = yaml_col_set - sample_col_set
        extra_in_sample = sample_col_set - yaml_col_set
        
        if missing_in_sample or extra_in_sample:
            column_issues.append({
                'table': table_name,
                'missing_in_sample': missing_in_sample,
                'extra_in_sample': extra_in_sample
            })
    
    print(f"  📊 チェック完了: {len(yaml_set & sample_set)} テーブル")
    
    return {
        'missing_sample': missing_sample,
        'missing_yaml': missing_yaml,
        'column_issues': column_issues
    }

def generate_report(issues):
    """レポート生成"""
    print("📋 検証レポートを生成中...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"sample_data_consistency_report_{timestamp}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("サンプルデータ整合性チェックレポート\n")
        f.write("=" * 80 + "\n")
        f.write(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # サンプルデータ不足
        if issues['missing_sample']:
            f.write("⚠️ サンプルデータが不足しているテーブル:\n")
            for table in sorted(issues['missing_sample']):
                f.write(f"  - {table}\n")
            f.write("\n")
        
        # YAML定義不足
        if issues['missing_yaml']:
            f.write("❌ YAML定義が不足しているテーブル:\n")
            for table in sorted(issues['missing_yaml']):
                f.write(f"  - {table}\n")
            f.write("\n")
        
        # カラム整合性問題
        if issues['column_issues']:
            f.write("🔍 カラム整合性の問題:\n")
            for issue in issues['column_issues']:
                f.write(f"\n📋 テーブル: {issue['table']}\n")
                if issue['missing_in_sample']:
                    f.write("  ⚠️ サンプルデータに不足しているカラム:\n")
                    for col in sorted(issue['missing_in_sample']):
                        f.write(f"    - {col}\n")
                if issue['extra_in_sample']:
                    f.write("  ❌ サンプルデータに余分なカラム:\n")
                    for col in sorted(issue['extra_in_sample']):
                        f.write(f"    - {col}\n")
            f.write("\n")
    
    print(f"✅ 検証完了！レポートを保存しました: {report_file}")
    return report_file

def main():
    """メイン処理"""
    print("=" * 80)
    print("YAML vs サンプルデータ整合性チェック（修正版）")
    print("=" * 80)
    
    # データ読み込み
    yaml_tables = load_yaml_definitions()
    print()
    sample_tables = load_sample_data()
    print()
    
    # 整合性チェック
    issues = check_consistency(yaml_tables, sample_tables)
    print()
    
    # レポート生成
    report_file = generate_report(issues)
    print()
    
    # サマリー表示
    total_issues = len(issues['missing_sample']) + len(issues['missing_yaml']) + len(issues['column_issues'])
    errors = len(issues['missing_yaml']) + len(issues['column_issues'])
    warnings = len(issues['missing_sample'])
    
    print("=" * 80)
    print("📋 検証結果サマリー")
    print("=" * 80)
    print(f"総問題数: {total_issues}")
    print(f"  ❌ エラー: {errors}")
    print(f"  ⚠️ 警告: {warnings}")
    print()
    print(f"📄 詳細は {report_file} をご確認ください。")

if __name__ == "__main__":
    main()
