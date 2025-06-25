#!/usr/bin/env python3
"""
特殊ケース修正 - tenant_idが存在しないテーブルの対応
"""

import os
import yaml
import glob
from datetime import datetime

def fix_mst_employee():
    """MST_Employeeテーブルの特殊修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Employee.yaml"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            return False, "columnsセクションが見つかりません"
        
        columns = data['columns']
        
        # tenant_idカラムを追加（2番目の位置に）
        tenant_id_column = {
            'name': 'tenant_id',
            'logical': 'テナントID',
            'type': 'VARCHAR(50)',
            'length': None,
            'null': False,
            'unique': False,
            'encrypted': False,
            'description': 'テナントID（マルチテナント対応）'
        }
        
        # 現在のカラム順序を確認
        column_names = [col['name'] for col in columns]
        
        if 'tenant_id' not in column_names:
            # tenant_idを2番目に挿入
            columns.insert(1, tenant_id_column)
            print(f"  ✅ tenant_idカラムを追加しました")
        
        # カラム順序を再調整
        # 1. id (主キー)
        # 2. tenant_id (テナントID) - 追加済み
        # 3. employee_code (ビジネスキー)
        # 4. full_name, full_name_kana (名称系)
        # 5. その他の基本属性
        # n-2. is_deleted
        # n-1. created_at
        # n. updated_at
        
        desired_order = [
            'id', 'tenant_id', 'employee_code', 'full_name', 'full_name_kana',
            'email', 'phone', 'birth_date', 'gender', 'hire_date',
            'department_id', 'position_id', 'job_type_id', 'manager_id',
            'employment_status', 'employee_status',
            'is_deleted', 'created_at', 'updated_at'
        ]
        
        # カラムを辞書形式で管理
        column_dict = {col['name']: col for col in columns}
        
        # 新しい順序でカラムを再構築
        new_columns = []
        for col_name in desired_order:
            if col_name in column_dict:
                new_columns.append(column_dict[col_name])
        
        # 順序リストにないカラムがあれば末尾に追加
        for col in columns:
            if col['name'] not in desired_order:
                new_columns.append(col)
        
        data['columns'] = new_columns
        
        # バージョン履歴を更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f'SPECIAL.{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '特殊ケース修正ツール',
            'changes': 'tenant_idカラム追加とカラム順序の最終調整'
        })
        
        # ファイルを保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return True, f"MST_Employee修正完了"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def fix_sys_systemlog():
    """SYS_SystemLogテーブルの特殊修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_SYS_SystemLog.yaml"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            return False, "columnsセクションが見つかりません"
        
        columns = data['columns']
        column_names = [col['name'] for col in columns]
        
        # tenant_idが存在するかチェック
        if 'tenant_id' not in column_names:
            # tenant_idカラムを追加（2番目の位置に）
            tenant_id_column = {
                'name': 'tenant_id',
                'logical': 'テナントID',
                'type': 'VARCHAR(50)',
                'length': None,
                'null': True,  # システムログは全体ログの場合もあるためNULL許可
                'unique': False,
                'encrypted': False,
                'description': 'テナントID（マルチテナント対応、システム全体ログの場合はNULL）'
            }
            columns.insert(1, tenant_id_column)
            print(f"  ✅ tenant_idカラムを追加しました")
        
        # カラム順序を調整
        column_dict = {col['name']: col for col in columns}
        
        # SYS_SystemLog用の順序
        desired_order = [
            'id', 'tenant_id', 'log_level', 'message', 'component_name',
            'user_id', 'session_id', 'request_id', 'error_code', 'stack_trace',
            'execution_time', 'memory_usage', 'cpu_usage', 'request_url',
            'request_method', 'request_headers', 'request_body', 'response_status',
            'response_headers', 'response_body', 'client_ip', 'user_agent',
            'is_deleted', 'created_at', 'updated_at'
        ]
        
        new_columns = []
        for col_name in desired_order:
            if col_name in column_dict:
                new_columns.append(column_dict[col_name])
        
        # 順序リストにないカラムがあれば末尾に追加
        for col in columns:
            if col['name'] not in desired_order:
                new_columns.append(col)
        
        data['columns'] = new_columns
        
        # バージョン履歴を更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f'SPECIAL.{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '特殊ケース修正ツール',
            'changes': 'tenant_idカラム追加とカラム順序の最終調整'
        })
        
        # ファイルを保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return True, f"SYS_SystemLog修正完了"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("🔧 特殊ケース修正を開始...")
    print("=" * 50)
    
    # MST_Employee修正
    print("🔧 MST_Employeeを修正中...")
    success, result = fix_mst_employee()
    if success:
        print(f"  ✅ {result}")
    else:
        print(f"  ❌ {result}")
    
    print()
    
    # SYS_SystemLog修正
    print("🔧 SYS_SystemLogを修正中...")
    success, result = fix_sys_systemlog()
    if success:
        print(f"  ✅ {result}")
    else:
        print(f"  ❌ {result}")
    
    print()
    print("🎉 特殊ケース修正完了！")

if __name__ == "__main__":
    main()
