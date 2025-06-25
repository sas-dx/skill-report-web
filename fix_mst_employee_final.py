#!/usr/bin/env python3
"""
MST_Employeeの主キー順序を正しく修正するスクリプト
実際の主キーは'id'（UUIDプライマリキー）
"""

import yaml
import shutil
from datetime import datetime

def fix_mst_employee():
    """MST_Employeeテーブルの主キー順序を修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Employee.yaml"
    
    # バックアップ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"📦 MST_Employee バックアップ: {backup_path}")
    
    # YAMLファイル読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    columns = data['columns']
    col_dict = {col['name']: col for col in columns}
    
    # 正しい順序で並び替え
    ordered_columns = []
    used_columns = set()
    
    # 1. 主キー（id - UUIDプライマリキー）
    if 'id' in col_dict:
        ordered_columns.append(col_dict['id'])
        used_columns.add('id')
        print("   🔑 主キー: id (UUID)")
    
    # 2. ビジネスキー（employee_code）
    if 'employee_code' in col_dict:
        ordered_columns.append(col_dict['employee_code'])
        used_columns.add('employee_code')
        print("   🔖 ビジネスキー: employee_code")
    
    # 3. 名称系フィールド
    name_fields = ['full_name', 'full_name_kana', 'email']
    for field in name_fields:
        if field in col_dict and field not in used_columns:
            ordered_columns.append(col_dict[field])
            used_columns.add(field)
            print(f"   📝 名称: {field}")
    
    # 4. 基本属性（個人情報）
    personal_fields = ['birth_date', 'gender', 'phone']
    for field in personal_fields:
        if field in col_dict and field not in used_columns:
            ordered_columns.append(col_dict[field])
            used_columns.add(field)
            print(f"   👤 個人情報: {field}")
    
    # 5. 雇用関連情報
    employment_fields = ['hire_date', 'employment_status', 'employee_status']
    for field in employment_fields:
        if field in col_dict and field not in used_columns:
            ordered_columns.append(col_dict[field])
            used_columns.add(field)
            print(f"   💼 雇用情報: {field}")
    
    # 6. 組織関連情報
    org_fields = ['department_id', 'position_id', 'job_type_id', 'manager_id']
    for field in org_fields:
        if field in col_dict and field not in used_columns:
            ordered_columns.append(col_dict[field])
            used_columns.add(field)
            print(f"   🏢 組織情報: {field}")
    
    # 7. その他の属性
    standard_cols = {'is_deleted', 'created_at', 'updated_at'}
    other_cols = [col['name'] for col in columns if col['name'] not in used_columns and col['name'] not in standard_cols]
    
    for col_name in sorted(other_cols):
        ordered_columns.append(col_dict[col_name])
        used_columns.add(col_name)
        print(f"   📄 その他: {col_name}")
    
    # 8. 標準カラム
    for std_col in ['is_deleted', 'created_at', 'updated_at']:
        if std_col in col_dict:
            ordered_columns.append(col_dict[std_col])
            used_columns.add(std_col)
            print(f"   🔧 標準: {std_col}")
    
    data['columns'] = ordered_columns
    
    # 改版履歴更新
    if 'revision_history' not in data:
        data['revision_history'] = []
    
    data['revision_history'].append({
        'version': f'7.0.{timestamp}',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': 'カラム順序最終修正ツール',
        'changes': '主キー（id）を先頭に移動し、推奨カラム順序に最終修正'
    })
    
    # ファイル書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, 
                 sort_keys=False, width=1000)
    
    print(f"✅ MST_Employee最終修正完了")

if __name__ == "__main__":
    print("🔧 MST_Employee最終修正中...")
    print("=" * 50)
    
    fix_mst_employee()
    
    print("\n🎉 MST_Employee修正が完了しました！")
