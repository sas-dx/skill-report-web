#!/usr/bin/env python3
"""
全テーブルのカラム順序統一スクリプト
推奨する統一カラム順序テンプレートに従って全YAMLファイルを修正
"""

import os
import yaml
import shutil
from datetime import datetime
from typing import Dict, List, Any

def backup_files():
    """全YAMLファイルのバックアップを作成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    yaml_dir = "docs/design/database/table-details"
    
    yaml_files = [f for f in os.listdir(yaml_dir) 
                 if f.startswith('テーブル詳細定義YAML_') and f.endswith('.yaml') 
                 and 'backup' not in f and 'TEMPLATE' not in f]
    
    print(f"📦 バックアップ作成中... (タイムスタンプ: {timestamp})")
    
    for filename in yaml_files:
        source = os.path.join(yaml_dir, filename)
        backup = os.path.join(yaml_dir, f"{filename}.backup.{timestamp}")
        shutil.copy2(source, backup)
        print(f"   ✅ {filename}")
    
    print(f"📦 バックアップ完了: {len(yaml_files)}ファイル")
    return timestamp

def get_expected_primary_key(table_name: str) -> str:
    """テーブル名から期待される主キー名を取得"""
    if table_name.startswith('MST_'):
        return f"{table_name[4:].lower()}_id"
    elif table_name.startswith('TRN_'):
        return f"{table_name[4:].lower()}_id"
    elif table_name.startswith('HIS_'):
        return f"{table_name[4:].lower()}_id"
    elif table_name.startswith('SYS_'):
        return f"{table_name[4:].lower()}_id"
    elif table_name.startswith('WRK_'):
        return f"{table_name[4:].lower()}_id"
    else:
        return f"{table_name.lower()}_id"

def reorder_columns(columns: List[Dict], table_name: str) -> List[Dict]:
    """カラムを推奨順序に並び替え"""
    
    # カラム名でインデックス作成
    col_dict = {col['name']: col for col in columns}
    col_names = [col['name'] for col in columns]
    
    # 期待される主キー名
    expected_pk = get_expected_primary_key(table_name)
    
    # 新しい順序でカラムを配置
    ordered_columns = []
    used_columns = set()
    
    # 1. 主キー（{table_name}_id または id）
    if expected_pk in col_dict:
        ordered_columns.append(col_dict[expected_pk])
        used_columns.add(expected_pk)
        print(f"   🔑 主キー: {expected_pk}")
    elif 'id' in col_dict:
        ordered_columns.append(col_dict['id'])
        used_columns.add('id')
        print(f"   🔑 主キー: id")
    
    # 2. tenant_id（マルチテナント対応）
    if 'tenant_id' in col_dict:
        ordered_columns.append(col_dict['tenant_id'])
        used_columns.add('tenant_id')
        print(f"   🏢 テナントID: tenant_id")
    
    # 3. UUID（idが主キーでない場合）
    if expected_pk != 'id' and 'id' in col_dict and 'id' not in used_columns:
        ordered_columns.append(col_dict['id'])
        used_columns.add('id')
        print(f"   🆔 UUID: id")
    
    # 4. ビジネスキー（_code, _name等）
    business_keys = []
    for col_name in col_names:
        if col_name not in used_columns:
            if (col_name.endswith('_code') or col_name.endswith('_number') or 
                col_name.endswith('_key') or col_name == 'code' or col_name == 'number'):
                business_keys.append(col_name)
    
    for key in sorted(business_keys):
        ordered_columns.append(col_dict[key])
        used_columns.add(key)
        print(f"   🔖 ビジネスキー: {key}")
    
    # 5. 名称系フィールド
    name_fields = []
    for col_name in col_names:
        if col_name not in used_columns:
            if (col_name.endswith('_name') or col_name.endswith('_title') or 
                col_name == 'name' or col_name == 'title' or col_name == 'full_name' or
                col_name.endswith('_name_en') or col_name.endswith('_name_kana')):
                name_fields.append(col_name)
    
    for field in sorted(name_fields):
        ordered_columns.append(col_dict[field])
        used_columns.add(field)
        print(f"   📝 名称: {field}")
    
    # 6. その他の基本属性（標準カラム以外）
    standard_cols = {'is_deleted', 'created_at', 'updated_at'}
    other_cols = []
    for col_name in col_names:
        if col_name not in used_columns and col_name not in standard_cols:
            other_cols.append(col_name)
    
    for col in sorted(other_cols):
        ordered_columns.append(col_dict[col])
        used_columns.add(col)
    
    # 7. 標準カラム（末尾）
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
    
    return ordered_columns

def update_revision_history(data: Dict[str, Any]) -> None:
    """改版履歴を更新"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if 'revision_history' not in data:
        data['revision_history'] = []
    
    # 新しい改版履歴を追加
    new_version = {
        'version': f'5.0.{timestamp}',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': '統一カラム順序修正ツール',
        'changes': 'カラム順序を統一テンプレート（Phase 1）に従って自動修正'
    }
    
    data['revision_history'].append(new_version)

def fix_column_order():
    """全テーブルのカラム順序を修正"""
    yaml_dir = "docs/design/database/table-details"
    
    yaml_files = [f for f in os.listdir(yaml_dir) 
                 if f.startswith('テーブル詳細定義YAML_') and f.endswith('.yaml') 
                 and 'backup' not in f and 'TEMPLATE' not in f]
    
    print("🔧 カラム順序統一開始")
    print("="*60)
    
    # バックアップ作成
    backup_timestamp = backup_files()
    
    print("\n🔄 カラム順序修正中...")
    print("="*60)
    
    success_count = 0
    error_count = 0
    
    for filename in sorted(yaml_files):
        file_path = os.path.join(yaml_dir, filename)
        table_name = filename.replace('テーブル詳細定義YAML_', '').replace('.yaml', '')
        
        print(f"\n📋 {table_name}")
        
        try:
            # YAMLファイル読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if 'columns' not in data:
                print(f"   ⚠️  columnsセクションが存在しません")
                continue
            
            # カラム順序を修正
            original_count = len(data['columns'])
            data['columns'] = reorder_columns(data['columns'], table_name)
            new_count = len(data['columns'])
            
            if original_count != new_count:
                print(f"   ❌ カラム数が変更されました: {original_count} → {new_count}")
                error_count += 1
                continue
            
            # 改版履歴を更新
            update_revision_history(data)
            
            # YAMLファイル書き込み
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, 
                         sort_keys=False, width=1000)
            
            print(f"   ✅ 修正完了: {new_count}カラム")
            success_count += 1
            
        except Exception as e:
            print(f"   ❌ エラー: {str(e)}")
            error_count += 1
    
    print("\n" + "="*60)
    print(f"📊 修正結果サマリー")
    print(f"✅ 成功: {success_count}テーブル")
    print(f"❌ エラー: {error_count}テーブル")
    print(f"📦 バックアップ: {backup_timestamp}")
    print("="*60)
    
    if error_count == 0:
        print("🎉 全テーブルのカラム順序統一が完了しました！")
    else:
        print("⚠️  一部のテーブルでエラーが発生しました。バックアップから復旧可能です。")

if __name__ == "__main__":
    fix_column_order()
