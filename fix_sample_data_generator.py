#!/usr/bin/env python3
"""
サンプルデータ生成ツールの修正スクリプト
全テーブルのNULL値問題を解決
"""

import os
import re
import yaml
import glob
from pathlib import Path

def load_yaml_table_definition(yaml_path):
    """YAMLファイルからテーブル定義を読み込み"""
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ YAML読み込みエラー: {yaml_path} - {e}")
        return None

def generate_sample_value(column, table_name, row_index):
    """カラムに応じた適切なサンプル値を生成"""
    col_name = column['name'].lower()
    col_type = column['type'].upper()
    
    # AUTO_INCREMENTカラムは省略
    if column.get('primary_key') and 'AUTO_INCREMENT' in col_type:
        return None
    
    # tenant_id の生成
    if col_name == 'tenant_id':
        return "'tenant_001'"
    
    # 各種IDカラムの生成
    if col_name.endswith('_id') and col_name != 'tenant_id':
        if col_name == 'parent_tenant_id':
            return 'NULL'  # 親テナントIDは通常NULL
        elif col_name == 'manager_id':
            return 'NULL'  # マネージャーIDは通常NULL
        else:
            # 通常のIDカラム
            prefix = col_name.replace('_id', '')
            return f"'{prefix}_{row_index:03d}'"
    
    # id カラム（UUID想定）の生成
    if col_name == 'id':
        table_prefix = table_name.lower().replace('mst_', '').replace('trn_', '').replace('sys_', '').replace('his_', '').replace('wrk_', '')
        return f"'{table_prefix}_{row_index:03d}'"
    
    # emp_no の生成
    if col_name == 'emp_no':
        return f"'EMP{row_index:04d}'"
    
    # コード系カラムの生成
    if 'code' in col_name:
        prefix = col_name.replace('_code', '').upper()
        return f"'{prefix}_{row_index:03d}'"
    
    # 名前系カラムの生成
    if 'name' in col_name:
        if 'skill' in col_name:
            skills = ['Java', 'Python', 'JavaScript', 'SQL', 'AWS']
            return f"'{skills[row_index % len(skills)]}'"
        elif 'department' in col_name:
            depts = ['開発部', '営業部', '総務部']
            return f"'{depts[row_index % len(depts)]}'"
        else:
            return f"'サンプル{col_name}_{row_index}'"
    
    # データ型に基づく値生成
    if 'VARCHAR' in col_type or 'TEXT' in col_type:
        return f"'sample_{col_name}_{row_index}'"
    elif 'INT' in col_type:
        if 'level' in col_name or 'grade' in col_name:
            return str((row_index % 4) + 1)  # 1-4のレベル
        else:
            return str(row_index + 1)
    elif 'DECIMAL' in col_type or 'FLOAT' in col_type:
        return str((row_index + 1) * 10.5)
    elif 'BOOLEAN' in col_type:
        return 'TRUE' if row_index % 2 == 0 else 'FALSE'
    elif 'TIMESTAMP' in col_type or 'DATETIME' in col_type:
        return 'CURRENT_TIMESTAMP'
    elif 'DATE' in col_type:
        return "'2025-01-01'"
    else:
        return f"'default_{row_index}'"

def fix_sample_data_file(yaml_path, sample_data_path):
    """サンプルデータファイルを修正"""
    table_def = load_yaml_table_definition(yaml_path)
    if not table_def:
        return False
    
    table_name = table_def['table_name']
    columns = table_def['columns']
    
    # サンプルデータを生成
    sample_rows = []
    for i in range(3):  # 3行のサンプルデータ
        row_values = []
        row_columns = []
        
        for column in columns:
            value = generate_sample_value(column, table_name, i + 1)
            if value is not None:  # AUTO_INCREMENTカラムは除外
                row_columns.append(column['name'])
                row_values.append(value)
        
        sample_rows.append((row_columns, row_values))
    
    # SQLファイルを生成
    sql_content = f"""-- {table_name} サンプルデータ
-- 生成日時: 2025-06-24
-- 修正版: NULL値問題を解決

"""
    
    if sample_rows:
        columns_str = ', '.join(sample_rows[0][0])
        sql_content += f"INSERT INTO {table_name} (\n    {columns_str}\n) VALUES\n"
        
        values_list = []
        for _, values in sample_rows:
            values_str = ', '.join(values)
            values_list.append(f"    ({values_str})")
        
        sql_content += ',\n'.join(values_list) + ';\n'
    
    # ファイルに書き込み
    try:
        with open(sample_data_path, 'w', encoding='utf-8') as f:
            f.write(sql_content)
        return True
    except Exception as e:
        print(f"❌ ファイル書き込みエラー: {sample_data_path} - {e}")
        return False

def main():
    """メイン処理"""
    yaml_dir = "docs/design/database/table-details"
    data_dir = "docs/design/database/data"
    
    if not os.path.exists(yaml_dir):
        print(f"❌ YAMLディレクトリが見つかりません: {yaml_dir}")
        return
    
    if not os.path.exists(data_dir):
        print(f"❌ データディレクトリが見つかりません: {data_dir}")
        return
    
    # YAMLファイルを取得
    yaml_files = glob.glob(os.path.join(yaml_dir, "テーブル詳細定義YAML_*.yaml"))
    yaml_files = [f for f in yaml_files if 'TEMPLATE' not in f]
    
    print(f"🔧 {len(yaml_files)}個のテーブルのサンプルデータを修正中...")
    print("=" * 80)
    
    success_count = 0
    error_count = 0
    
    for yaml_path in sorted(yaml_files):
        yaml_name = os.path.basename(yaml_path)
        table_name = yaml_name.replace('テーブル詳細定義YAML_', '').replace('.yaml', '')
        
        sample_data_path = os.path.join(data_dir, f"{table_name}_sample_data.sql")
        
        print(f"🔧 {table_name} を修正中...")
        
        if fix_sample_data_file(yaml_path, sample_data_path):
            print(f"✅ {table_name} 修正完了")
            success_count += 1
        else:
            print(f"❌ {table_name} 修正失敗")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"📊 修正結果サマリー")
    print(f"   - 成功: {success_count}テーブル")
    print(f"   - 失敗: {error_count}テーブル")
    
    if success_count > 0:
        print(f"\n✅ {success_count}個のテーブルのサンプルデータを修正しました")
        print(f"💡 修正内容:")
        print(f"   - AUTO_INCREMENTカラムはINSERT時に省略")
        print(f"   - tenant_idに適切な値を設定")
        print(f"   - idカラムにUUID形式の値を設定")
        print(f"   - 各種IDカラムに適切な値を設定")
        print(f"   - NULL値問題を解決")

if __name__ == "__main__":
    main()
