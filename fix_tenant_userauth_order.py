#!/usr/bin/env python3
"""
MST_TenantとMST_UserAuthのカラム順序を完全に修正
推奨順序: 1.主キー 2.tenant_id 3.UUID(id) 4.その他...
"""

import yaml
import shutil
from datetime import datetime

def backup_file(file_path):
    """ファイルをバックアップ"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def fix_mst_tenant_complete():
    """MST_Tenantの完全修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Tenant.yaml"
    
    print(f"🔧 MST_Tenant完全修正中...")
    backup_path = backup_file(file_path)
    print(f"📦 バックアップ: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    columns = data.get('columns', [])
    column_names = [col['name'] for col in columns]
    print(f"   現在の順序: {column_names[:5]}...")
    
    # カラムを分類
    id_column = None
    tenant_id_column = None
    other_columns = []
    
    for col in columns:
        if col['name'] == 'id':
            id_column = col
        elif col['name'] == 'tenant_id':
            tenant_id_column = col
        else:
            other_columns.append(col)
    
    # 推奨順序で再配置: 1.id(主キー) 2.tenant_id 3.その他
    new_columns = []
    if id_column:
        new_columns.append(id_column)
    if tenant_id_column:
        new_columns.append(tenant_id_column)
    new_columns.extend(other_columns)
    
    data['columns'] = new_columns
    
    # 改版履歴を更新
    if 'revision_history' not in data:
        data['revision_history'] = []
    
    data['revision_history'].append({
        'version': f"9.0.{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': '完全カラム順序修正ツール',
        'changes': '推奨カラム順序（1.主キー 2.tenant_id 3.その他）に完全修正'
    })
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    new_order = [col['name'] for col in data['columns']]
    print(f"   修正後順序: {new_order[:5]}...")
    print("✅ MST_Tenant完全修正完了")

def fix_mst_userauth_complete():
    """MST_UserAuthの完全修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_UserAuth.yaml"
    
    print(f"🔧 MST_UserAuth完全修正中...")
    backup_path = backup_file(file_path)
    print(f"📦 バックアップ: {backup_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    columns = data.get('columns', [])
    column_names = [col['name'] for col in columns]
    print(f"   現在の順序: {column_names[:5]}...")
    
    # カラムを分類
    id_column = None
    tenant_id_column = None
    userauth_id_column = None
    other_columns = []
    
    for col in columns:
        if col['name'] == 'id':
            id_column = col
        elif col['name'] == 'tenant_id':
            tenant_id_column = col
        elif col['name'] == 'userauth_id':
            userauth_id_column = col
        else:
            other_columns.append(col)
    
    # 推奨順序で再配置: 1.id(UUID) 2.tenant_id 3.userauth_id(主キー) 4.その他
    new_columns = []
    if id_column:
        new_columns.append(id_column)
    if tenant_id_column:
        new_columns.append(tenant_id_column)
    if userauth_id_column:
        new_columns.append(userauth_id_column)
    new_columns.extend(other_columns)
    
    data['columns'] = new_columns
    
    # 改版履歴を更新
    if 'revision_history' not in data:
        data['revision_history'] = []
    
    data['revision_history'].append({
        'version': f"9.0.{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': '完全カラム順序修正ツール',
        'changes': '推奨カラム順序（1.UUID 2.tenant_id 3.主キー 4.その他）に完全修正'
    })
    
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    new_order = [col['name'] for col in data['columns']]
    print(f"   修正後順序: {new_order[:5]}...")
    print("✅ MST_UserAuth完全修正完了")

def main():
    """メイン処理"""
    print("🔧 MST_Tenant・MST_UserAuth完全修正開始")
    print("=" * 60)
    
    fix_mst_tenant_complete()
    print()
    fix_mst_userauth_complete()
    
    print("\n" + "=" * 60)
    print("🎉 完全修正が完了しました！")

if __name__ == "__main__":
    main()
