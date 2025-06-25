#!/usr/bin/env python3
"""
最後の残りテーブルを修正するスクリプト
- MST_Tenant: 主キー(id)を最初に移動
- MST_UserAuth: 主キー(id)を最初に移動
- MST_RolePermission: 主キー追加
"""

import yaml
import shutil
from datetime import datetime
from pathlib import Path

def backup_file(file_path):
    """ファイルをバックアップ"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def fix_mst_tenant():
    """MST_Tenantの主キー順序を修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Tenant.yaml"
    
    print(f"🔧 MST_Tenant修正中...")
    backup_path = backup_file(file_path)
    print(f"📦 MST_Tenant バックアップ: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    columns = data.get('columns', [])
    if not columns:
        print("❌ カラム定義が見つかりません")
        return
    
    # 現在のカラム順序を確認
    column_names = [col['name'] for col in columns]
    print(f"   現在の順序: {column_names[:5]}...")
    
    # idカラムを見つけて最初に移動
    id_column = None
    other_columns = []
    
    for col in columns:
        if col['name'] == 'id':
            id_column = col
        else:
            other_columns.append(col)
    
    if id_column:
        # idを最初に配置
        data['columns'] = [id_column] + other_columns
        
        # 改版履歴を更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f"8.0.{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '最終カラム順序修正ツール',
            'changes': '主キー（id）を先頭に移動し、推奨カラム順序に最終修正'
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        new_order = [col['name'] for col in data['columns']]
        print(f"   修正後順序: {new_order[:5]}...")
        print("✅ MST_Tenant修正完了")
    else:
        print("❌ idカラムが見つかりません")

def fix_mst_userauth():
    """MST_UserAuthの主キー順序を修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_UserAuth.yaml"
    
    print(f"🔧 MST_UserAuth修正中...")
    backup_path = backup_file(file_path)
    print(f"📦 MST_UserAuth バックアップ: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    columns = data.get('columns', [])
    if not columns:
        print("❌ カラム定義が見つかりません")
        return
    
    # 現在のカラム順序を確認
    column_names = [col['name'] for col in columns]
    print(f"   現在の順序: {column_names[:5]}...")
    
    # idカラムを見つけて最初に移動
    id_column = None
    other_columns = []
    
    for col in columns:
        if col['name'] == 'id':
            id_column = col
        else:
            other_columns.append(col)
    
    if id_column:
        # idを最初に配置
        data['columns'] = [id_column] + other_columns
        
        # 改版履歴を更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f"8.0.{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '最終カラム順序修正ツール',
            'changes': '主キー（id）を先頭に移動し、推奨カラム順序に最終修正'
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        new_order = [col['name'] for col in data['columns']]
        print(f"   修正後順序: {new_order[:5]}...")
        print("✅ MST_UserAuth修正完了")
    else:
        print("❌ idカラムが見つかりません")

def fix_mst_rolepermission():
    """MST_RolePermissionに主キーを追加"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_RolePermission.yaml"
    
    print(f"🔧 MST_RolePermission修正中...")
    backup_path = backup_file(file_path)
    print(f"📦 MST_RolePermission バックアップ: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    columns = data.get('columns', [])
    column_names = [col['name'] for col in columns]
    
    # 主キーが存在しない場合は追加
    if 'rolepermission_id' not in column_names and 'id' not in column_names:
        # 主キーカラムを作成
        pk_column = {
            'name': 'rolepermission_id',
            'logical': 'ロール権限ID（主キー）',
            'type': 'SERIAL',
            'length': None,
            'null': False,
            'unique': False,
            'encrypted': False,
            'description': 'ロール権限ID（主キー・自動採番）'
        }
        
        # 主キーを最初に挿入
        data['columns'] = [pk_column] + columns
        
        # 改版履歴を更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f"8.0.{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '最終カラム順序修正ツール',
            'changes': '主キー（rolepermission_id）を追加し、推奨カラム順序に修正'
        })
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print("✅ MST_RolePermission修正完了（主キー追加）")
    else:
        print("✅ MST_RolePermission主キーは既に存在")

def main():
    """メイン処理"""
    print("🔧 最終残りテーブル修正開始")
    print("=" * 50)
    
    # 各テーブルを修正
    fix_mst_tenant()
    print()
    fix_mst_userauth()
    print()
    fix_mst_rolepermission()
    
    print("\n" + "=" * 50)
    print("🎉 最終修正が完了しました！")

if __name__ == "__main__":
    main()
