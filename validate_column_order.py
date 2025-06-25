#!/usr/bin/env python3
"""
カラム順序統一後の検証スクリプト
"""

import os
import yaml
from typing import Dict, List

def validate_column_order():
    """全テーブルのカラム順序を検証"""
    yaml_dir = "docs/design/database/table-details"
    
    yaml_files = [f for f in os.listdir(yaml_dir) 
                 if f.startswith('テーブル詳細定義YAML_') and f.endswith('.yaml') 
                 and 'backup' not in f and 'TEMPLATE' not in f]
    
    print("🔍 カラム順序検証開始")
    print("="*60)
    
    issues = []
    
    for filename in sorted(yaml_files):
        file_path = os.path.join(yaml_dir, filename)
        table_name = filename.replace('テーブル詳細定義YAML_', '').replace('.yaml', '')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if 'columns' not in data:
            continue
            
        columns = [col['name'] for col in data['columns']]
        
        # 期待される主キー名
        if table_name.startswith('MST_'):
            expected_pk = f"{table_name[4:].lower()}_id"
        elif table_name.startswith('TRN_'):
            expected_pk = f"{table_name[4:].lower()}_id"
        elif table_name.startswith('HIS_'):
            expected_pk = f"{table_name[4:].lower()}_id"
        elif table_name.startswith('SYS_'):
            expected_pk = f"{table_name[4:].lower()}_id"
        elif table_name.startswith('WRK_'):
            expected_pk = f"{table_name[4:].lower()}_id"
        else:
            expected_pk = f"{table_name.lower()}_id"
        
        # 検証項目
        table_issues = []
        
        # 1. 主キーの存在と位置
        if expected_pk not in columns:
            if 'id' in columns:
                if columns[0] != 'id':
                    table_issues.append(f"❌ 主キー(id)が1番目にない: {columns[0]}")
            else:
                table_issues.append(f"❌ 主キー({expected_pk} or id)が存在しない")
        else:
            if columns[0] != expected_pk:
                table_issues.append(f"❌ 主キー({expected_pk})が1番目にない: {columns[0]}")
        
        # 2. tenant_idの存在と位置
        if 'tenant_id' not in columns:
            table_issues.append("⚠️  tenant_idが存在しない（マルチテナント対応未完了）")
        else:
            tenant_pos = columns.index('tenant_id')
            if tenant_pos != 1:
                table_issues.append(f"❌ tenant_idが2番目にない: {tenant_pos + 1}番目")
        
        # 3. 標準カラムの位置
        standard_cols = ['is_deleted', 'created_at', 'updated_at']
        for i, std_col in enumerate(standard_cols):
            if std_col in columns:
                expected_pos = len(columns) - len(standard_cols) + i
                actual_pos = columns.index(std_col)
                if actual_pos != expected_pos:
                    table_issues.append(f"❌ {std_col}の位置が不正: {actual_pos + 1}番目 (期待: {expected_pos + 1}番目)")
        
        # 結果表示
        if table_issues:
            print(f"\n📋 {table_name}")
            print(f"   カラム数: {len(columns)}")
            print(f"   先頭5カラム: {columns[:5]}")
            print(f"   末尾3カラム: {columns[-3:]}")
            for issue in table_issues:
                print(f"   {issue}")
            issues.extend(table_issues)
        else:
            print(f"✅ {table_name}: OK")
    
    print("\n" + "="*60)
    print(f"📊 検証結果サマリー")
    print(f"✅ 問題なし: {len(yaml_files) - len([f for f in yaml_files if any(issue.startswith(f'📋 {f.replace("テーブル詳細定義YAML_", "").replace(".yaml", "")}') for issue in [str(i) for i in issues])])}テーブル")
    print(f"❌ 問題あり: {len([f for f in yaml_files if any(issue.startswith(f'📋 {f.replace("テーブル詳細定義YAML_", "").replace(".yaml", "")}') for issue in [str(i) for i in issues])])}テーブル")
    print(f"⚠️  総問題数: {len(issues)}")
    print("="*60)

if __name__ == "__main__":
    validate_column_order()
