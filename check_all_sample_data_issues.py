#!/usr/bin/env python3
"""
全テーブルのサンプルデータファイルでNULL値問題を検出するスクリプト
"""

import os
import re
import glob
from pathlib import Path

def check_sample_data_file(file_path):
    """サンプルデータファイルの問題をチェック"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # INSERT文を抽出
        insert_pattern = r'INSERT INTO\s+(\w+)\s*\((.*?)\)\s*VALUES\s*(.*?)(?=;|\Z)'
        matches = re.findall(insert_pattern, content, re.DOTALL | re.IGNORECASE)
        
        for table_name, columns_str, values_str in matches:
            # カラム名を抽出
            columns = [col.strip() for col in columns_str.split(',')]
            
            # VALUES部分を解析
            values_pattern = r'\((.*?)\)'
            value_rows = re.findall(values_pattern, values_str, re.DOTALL)
            
            for i, row in enumerate(value_rows):
                values = [val.strip() for val in row.split(',')]
                
                # カラム数と値数の一致チェック
                if len(columns) != len(values):
                    issues.append(f"行{i+1}: カラム数({len(columns)})と値数({len(values)})が不一致")
                    continue
                
                # NULL値チェック
                for j, (col, val) in enumerate(zip(columns, values)):
                    if val.upper() == 'NULL':
                        # 主キーや必須カラムの可能性をチェック
                        col_lower = col.lower()
                        if any(keyword in col_lower for keyword in ['id', 'tenant_id', 'emp_no']):
                            issues.append(f"行{i+1}: 必須カラム '{col}' にNULL値")
                        elif col_lower.endswith('_id') and not col_lower.startswith('parent_'):
                            issues.append(f"行{i+1}: IDカラム '{col}' にNULL値")
    
    except Exception as e:
        issues.append(f"ファイル読み込みエラー: {str(e)}")
    
    return issues

def main():
    """メイン処理"""
    data_dir = "docs/design/database/data"
    
    if not os.path.exists(data_dir):
        print(f"❌ データディレクトリが見つかりません: {data_dir}")
        return
    
    # サンプルデータファイルを取得
    sample_files = glob.glob(os.path.join(data_dir, "*_sample_data.sql"))
    
    print(f"🔍 {len(sample_files)}個のサンプルデータファイルをチェック中...")
    print("=" * 80)
    
    total_issues = 0
    problematic_files = []
    
    for file_path in sorted(sample_files):
        file_name = os.path.basename(file_path)
        table_name = file_name.replace("_sample_data.sql", "")
        
        issues = check_sample_data_file(file_path)
        
        if issues:
            print(f"\n❌ {table_name}")
            print(f"   ファイル: {file_name}")
            for issue in issues:
                print(f"   - {issue}")
            total_issues += len(issues)
            problematic_files.append(table_name)
        else:
            print(f"✅ {table_name}")
    
    print("\n" + "=" * 80)
    print(f"📊 チェック結果サマリー")
    print(f"   - 総ファイル数: {len(sample_files)}")
    print(f"   - 問題のあるファイル数: {len(problematic_files)}")
    print(f"   - 総問題数: {total_issues}")
    
    if problematic_files:
        print(f"\n🚨 問題のあるテーブル:")
        for table in problematic_files:
            print(f"   - {table}")
        
        print(f"\n💡 推奨対応:")
        print(f"   1. サンプルデータ生成ツールの修正")
        print(f"   2. 必須カラムの適切な値生成")
        print(f"   3. AUTO_INCREMENTカラムの扱い改善")
        print(f"   4. UUIDカラムの自動生成実装")
    else:
        print(f"\n✅ 全てのサンプルデータファイルに問題はありません")

if __name__ == "__main__":
    main()
