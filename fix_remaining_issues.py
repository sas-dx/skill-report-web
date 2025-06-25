#!/usr/bin/env python3
"""
残りの問題を修正するスクリプト
MST_Employee, MST_RolePermissionの主キー順序問題を解決
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
    
    # 1. 主キー（employee_id）
    if 'employee_id' in col_dict:
        ordered_columns.append(col_dict['employee_id'])
        used_columns.add('employee_id')
        print("   🔑 主キー: employee_id")
    
    # 2. テナントID
    if 'tenant_id' in col_dict:
        ordered_columns.append(col_dict['tenant_id'])
        used_columns.add('tenant_id')
        print("   🏢 テナント: tenant_id")
    
    # 3. UUID
    if 'id' in col_dict:
        ordered_columns.append(col_dict['id'])
        used_columns.add('id')
        print("   🆔 UUID: id")
    
    # 4. ビジネスキー
    business_keys = ['emp_no', 'employee_code']
    for key in business_keys:
        if key in col_dict and key not in used_columns:
            ordered_columns.append(col_dict[key])
            used_columns.add(key)
            print(f"   🔖 ビジネスキー: {key}")
    
    # 5. 名称系
    name_fields = ['first_name', 'last_name', 'full_name', 'email']
    for field in name_fields:
        if field in col_dict and field not in used_columns:
            ordered_columns.append(col_dict[field])
            used_columns.add(field)
            print(f"   📝 名称: {field}")
    
    # 6. その他の属性
    standard_cols = {'is_deleted', 'created_at', 'updated_at'}
    other_cols = [col['name'] for col in columns if col['name'] not in used_columns and col['name'] not in standard_cols]
    
    for col_name in sorted(other_cols):
        ordered_columns.append(col_dict[col_name])
        used_columns.add(col_name)
        print(f"   📄 その他: {col_name}")
    
    # 7. 標準カラム
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
        'version': f'6.1.{timestamp}',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': 'カラム順序修正ツール',
        'changes': '主キー（employee_id）を先頭に移動し、推奨カラム順序に修正'
    })
    
    # ファイル書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, 
                 sort_keys=False, width=1000)
    
    print(f"✅ MST_Employee修正完了")

def fix_mst_role_permission():
    """MST_RolePermissionテーブルの主キー順序を修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_RolePermission.yaml"
    
    # バックアップ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"📦 MST_RolePermission バックアップ: {backup_path}")
    
    # YAMLファイル読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    columns = data['columns']
    col_dict = {col['name']: col for col in columns}
    
    # 正しい順序で並び替え
    ordered_columns = []
    used_columns = set()
    
    # 1. 主キー（role_permission_id）
    if 'role_permission_id' in col_dict:
        ordered_columns.append(col_dict['role_permission_id'])
        used_columns.add('role_permission_id')
        print("   🔑 主キー: role_permission_id")
    
    # 2. テナントID
    if 'tenant_id' in col_dict:
        ordered_columns.append(col_dict['tenant_id'])
        used_columns.add('tenant_id')
        print("   🏢 テナント: tenant_id")
    
    # 3. UUID
    if 'id' in col_dict:
        ordered_columns.append(col_dict['id'])
        used_columns.add('id')
        print("   🆔 UUID: id")
    
    # 4. 外部キー
    fk_fields = ['role_id', 'permission_id']
    for field in fk_fields:
        if field in col_dict and field not in used_columns:
            ordered_columns.append(col_dict[field])
            used_columns.add(field)
            print(f"   🔗 外部キー: {field}")
    
    # 5. その他の属性
    standard_cols = {'is_deleted', 'created_at', 'updated_at'}
    other_cols = [col['name'] for col in columns if col['name'] not in used_columns and col['name'] not in standard_cols]
    
    for col_name in sorted(other_cols):
        ordered_columns.append(col_dict[col_name])
        used_columns.add(col_name)
        print(f"   📄 その他: {col_name}")
    
    # 6. 標準カラム
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
        'version': f'6.1.{timestamp}',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': 'カラム順序修正ツール',
        'changes': '主キー（role_permission_id）を先頭に移動し、推奨カラム順序に修正'
    })
    
    # ファイル書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, 
                 sort_keys=False, width=1000)
    
    print(f"✅ MST_RolePermission修正完了")

if __name__ == "__main__":
    print("🔧 残りの問題を修正中...")
    print("=" * 50)
    
    print("\n📋 MST_Employee修正:")
    fix_mst_employee()
    
    print("\n📋 MST_RolePermission修正:")
    fix_mst_role_permission()
    
    print("\n🎉 全ての修正が完了しました！")
