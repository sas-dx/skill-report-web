#!/usr/bin/env python3
"""
MST_Tenantテーブルのカラム順序修正スクリプト
tenant_idの重複問題を解決し、正しいカラム順序に修正
"""

import yaml
import shutil
from datetime import datetime

def fix_mst_tenant():
    """MST_Tenantテーブルのカラム順序を修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Tenant.yaml"
    
    # バックアップ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"📦 バックアップ作成: {backup_path}")
    
    # YAMLファイル読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 現在のカラム情報を取得
    columns = data['columns']
    print(f"📋 現在のカラム数: {len(columns)}")
    
    # カラム名でインデックス作成（重複チェック）
    col_dict = {}
    duplicates = []
    
    for i, col in enumerate(columns):
        col_name = col['name']
        if col_name in col_dict:
            duplicates.append(col_name)
            print(f"⚠️  重複カラム発見: {col_name} (位置: {col_dict[col_name]}, {i})")
        else:
            col_dict[col_name] = i
    
    if duplicates:
        print(f"🔧 重複カラムを除去: {duplicates}")
        # 重複を除去（最初の定義を保持）
        seen = set()
        unique_columns = []
        for col in columns:
            if col['name'] not in seen:
                unique_columns.append(col)
                seen.add(col['name'])
        columns = unique_columns
        print(f"📋 重複除去後のカラム数: {len(columns)}")
    
    # カラム名でインデックス再作成
    col_dict = {col['name']: col for col in columns}
    col_names = [col['name'] for col in columns]
    
    # 推奨順序でカラムを並び替え
    ordered_columns = []
    used_columns = set()
    
    print("\n🔄 カラム順序修正中...")
    
    # 1. 主キー（tenant_id）
    if 'tenant_id' in col_dict:
        ordered_columns.append(col_dict['tenant_id'])
        used_columns.add('tenant_id')
        print(f"   🔑 主キー: tenant_id")
    
    # 2. UUID（id）
    if 'id' in col_dict:
        ordered_columns.append(col_dict['id'])
        used_columns.add('id')
        print(f"   🆔 UUID: id")
    
    # 3. ビジネスキー
    business_keys = ['tenant_code', 'country_code', 'currency_code', 'phone_number', 'postal_code']
    for key in business_keys:
        if key in col_dict and key not in used_columns:
            ordered_columns.append(col_dict[key])
            used_columns.add(key)
            print(f"   🔖 ビジネスキー: {key}")
    
    # 4. 名称系フィールド
    name_fields = ['tenant_name', 'tenant_name_en', 'tenant_short_name', 'domain_name']
    for field in name_fields:
        if field in col_dict and field not in used_columns:
            ordered_columns.append(col_dict[field])
            used_columns.add(field)
            print(f"   📝 名称: {field}")
    
    # 5. その他の基本属性（標準カラム以外）
    standard_cols = {'is_deleted', 'created_at', 'updated_at'}
    other_cols = []
    for col_name in col_names:
        if col_name not in used_columns and col_name not in standard_cols:
            other_cols.append(col_name)
    
    # アルファベット順でソート
    for col in sorted(other_cols):
        ordered_columns.append(col_dict[col])
        used_columns.add(col)
        print(f"   📄 その他: {col}")
    
    # 6. 標準カラム（末尾）
    if 'is_deleted' in col_dict:
        ordered_columns.append(col_dict['is_deleted'])
        used_columns.add('is_deleted')
        print(f"   🗑️  論理削除: is_deleted")
    
    if 'created_at' in col_dict:
        ordered_columns.append(col_dict['created_at'])
        used_columns.add('created_at')
        print(f"   📅 作成日時: created_at")
    
    if 'updated_at' in col_dict:
        ordered_columns.append(col_dict['updated_at'])
        used_columns.add('updated_at')
        print(f"   🔄 更新日時: updated_at")
    
    # 未処理のカラムがあれば警告
    missing = set(col_names) - used_columns
    if missing:
        print(f"   ⚠️  未処理カラム: {missing}")
        for col in missing:
            ordered_columns.append(col_dict[col])
    
    # カラム順序を更新
    data['columns'] = ordered_columns
    
    # 改版履歴を更新
    if 'revision_history' not in data:
        data['revision_history'] = []
    
    new_version = {
        'version': f'5.1.{timestamp}',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': 'MST_Tenant修正ツール',
        'changes': 'tenant_id重複問題を解決し、カラム順序を統一テンプレートに従って修正'
    }
    
    data['revision_history'].append(new_version)
    
    # YAMLファイル書き込み
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, 
                 sort_keys=False, width=1000)
    
    print(f"\n✅ 修正完了")
    print(f"📊 最終カラム数: {len(ordered_columns)}")
    print(f"📦 バックアップ: {backup_path}")

if __name__ == "__main__":
    fix_mst_tenant()
