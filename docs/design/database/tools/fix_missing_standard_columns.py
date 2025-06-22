#!/usr/bin/env python3
"""
不足している標準カラム（id, is_deleted等）をYAMLファイルに追加するスクリプト
"""

import os
import yaml
import glob
from pathlib import Path

def load_yaml_safe(file_path):
    """YAMLファイルを安全に読み込み"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"❌ YAML読み込みエラー: {file_path} - {e}")
        return None

def save_yaml_safe(file_path, data):
    """YAMLファイルを安全に保存"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return True
    except Exception as e:
        print(f"❌ YAML保存エラー: {file_path} - {e}")
        return False

def add_missing_standard_columns(yaml_data, table_name):
    """標準カラムを追加"""
    if 'columns' not in yaml_data:
        yaml_data['columns'] = []
    
    columns = yaml_data['columns']
    existing_columns = {col['name'] for col in columns}
    
    # 標準カラムの定義
    standard_columns = [
        {
            'name': 'id',
            'type': 'VARCHAR(50)',
            'nullable': False,
            'primary_key': False,
            'unique': True,
            'default': None,
            'comment': 'プライマリキー（UUID）',
            'requirement_id': 'PLT.1-WEB.1'
        },
        {
            'name': 'is_deleted',
            'type': 'BOOLEAN',
            'nullable': False,
            'primary_key': False,
            'unique': False,
            'default': 'False',
            'comment': '論理削除フラグ',
            'requirement_id': 'PLT.1-WEB.1'
        }
    ]
    
    added_columns = []
    for std_col in standard_columns:
        if std_col['name'] not in existing_columns:
            # 適切な位置に挿入（主キーの後、created_atの前）
            insert_index = len(columns)
            for i, col in enumerate(columns):
                if col['name'] in ['created_at', 'updated_at']:
                    insert_index = i
                    break
            
            columns.insert(insert_index, std_col)
            added_columns.append(std_col['name'])
    
    return added_columns

def fix_foreign_keys(yaml_data):
    """外部キー制約の修正"""
    if 'foreign_keys' not in yaml_data:
        return []
    
    fixed_fks = []
    for fk in yaml_data['foreign_keys']:
        if fk.get('columns') == ['user_id'] and fk.get('references', {}).get('columns') == ['reference_column']:
            # MST_UserAuthへの正しい参照に修正
            fk['references']['columns'] = ['user_id']
            fixed_fks.append(fk['name'])
    
    return fixed_fks

def main():
    print("🔧 標準カラム追加スクリプト開始")
    
    # 対象ディレクトリ
    table_details_dir = Path(__file__).parent.parent / "table-details"
    print(f"📁 対象ディレクトリ: {table_details_dir}")
    
    if not table_details_dir.exists():
        print(f"❌ ディレクトリが存在しません: {table_details_dir}")
        return
    
    # YAMLファイルを取得
    yaml_files = list(table_details_dir.glob("*_details.yaml"))
    print(f"📄 対象ファイル数: {len(yaml_files)}")
    
    total_files = 0
    fixed_files = 0
    error_files = 0
    
    for yaml_file in yaml_files:
        total_files += 1
        
        # テンプレートファイルはスキップ
        if "TEMPLATE" in yaml_file.name:
            print(f"ℹ️  スキップ: {yaml_file.name} (テンプレートファイル)")
            continue
        
        # YAMLファイルを読み込み
        yaml_data = load_yaml_safe(yaml_file)
        if yaml_data is None:
            error_files += 1
            continue
        
        table_name = yaml_data.get('table_name', yaml_file.stem.replace('_details', ''))
        
        # 標準カラムを追加
        added_columns = add_missing_standard_columns(yaml_data, table_name)
        
        # 外部キー制約を修正
        fixed_fks = fix_foreign_keys(yaml_data)
        
        if added_columns or fixed_fks:
            # ファイルを保存
            if save_yaml_safe(yaml_file, yaml_data):
                fixed_files += 1
                changes = []
                if added_columns:
                    changes.append(f"カラム追加: {', '.join(added_columns)}")
                if fixed_fks:
                    changes.append(f"外部キー修正: {', '.join(fixed_fks)}")
                print(f"✅ 修正完了: {yaml_file.name} - {'; '.join(changes)}")
            else:
                error_files += 1
        else:
            print(f"ℹ️  修正不要: {yaml_file.name}")
    
    print("\n" + "="*50)
    print("🎯 標準カラム追加完了")
    print(f"📊 処理結果:")
    print(f"   - 総ファイル数: {total_files}")
    print(f"   - 修正ファイル数: {fixed_files}")
    print(f"   - エラーファイル数: {error_files}")
    print(f"   - 修正不要ファイル数: {total_files - fixed_files - error_files}")
    
    if error_files == 0:
        print("\n✅ 全ての処理が正常に完了しました")
    else:
        print(f"\n⚠️  {error_files}個のファイルでエラーが発生しました")

if __name__ == "__main__":
    main()
