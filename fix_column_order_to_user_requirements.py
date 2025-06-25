#!/usr/bin/env python3
"""
全テーブルのカラム順序をユーザー要求に従って修正するスクリプト

要求された順序:
1. id (UUID主キー - 実際の主キー)
2. tenant_id (テナントID - 存在する場合)
3. {business_key} (ビジネスキー - コード等)
4. {name_fields} (名称系フィールド)
5. {basic_attributes} (基本属性)
...
n-2. is_deleted (論理削除フラグ)
n-1. created_at (作成日時)
n. updated_at (更新日時)
"""

import os
import yaml
import shutil
from datetime import datetime
from pathlib import Path

def backup_file(file_path):
    """ファイルのバックアップを作成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy2(file_path, backup_path)
    return backup_path

def get_column_priority(column_name, table_name):
    """カラムの優先度を返す（数値が小さいほど前に配置）"""
    
    # 1. id (UUID主キー) - 最優先
    if column_name == 'id':
        return (1, column_name)
    
    # 2. tenant_id - 2番目
    if column_name == 'tenant_id':
        return (2, column_name)
    
    # 3. ビジネスキー（コード系）
    business_key_patterns = [
        '_code', '_no', '_number', 'employee_code', 'tenant_code', 
        'skill_code', 'department_code', 'position_code', 'job_type_code',
        'certification_code', 'role_code', 'permission_code'
    ]
    for pattern in business_key_patterns:
        if pattern in column_name:
            return (3, column_name)
    
    # 4. 名称系フィールド
    name_patterns = [
        'name', 'title', 'label', 'display_name', 'full_name', 
        'short_name', 'description', 'comment'
    ]
    for pattern in name_patterns:
        if pattern in column_name:
            return (4, column_name)
    
    # 5. 終了部分の特別なカラム
    if column_name == 'is_deleted':
        return (998, column_name)
    if column_name == 'created_at':
        return (999, column_name)
    if column_name == 'updated_at':
        return (1000, column_name)
    
    # 6. その他の属性（アルファベット順）
    return (500, column_name)

def reorder_columns(columns):
    """カラムを要求された順序に並び替え"""
    # カラム名を取得（columnsがリストの場合とdictの場合に対応）
    if isinstance(columns, list):
        column_items = [(col.get('name', ''), col) for col in columns]
    else:
        column_items = [(name, col) for name, col in columns.items()]
    
    # 優先度でソート
    sorted_columns = sorted(column_items, key=lambda x: get_column_priority(x[0], ''))
    
    # 元の形式に戻す
    if isinstance(columns, list):
        return [col for _, col in sorted_columns]
    else:
        return {name: col for name, col in sorted_columns}

def update_revision_history(data):
    """改版履歴を更新"""
    if 'revision_history' not in data:
        data['revision_history'] = []
    
    new_entry = {
        'version': f"13.0.{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': 'ユーザー要求対応カラム順序修正ツール',
        'changes': 'ユーザー要求に従ってカラム順序を統一（id→tenant_id→ビジネスキー→名称→その他→終了部分）'
    }
    
    data['revision_history'].append(new_entry)

def process_yaml_file(file_path):
    """YAMLファイルを処理してカラム順序を修正"""
    try:
        # バックアップ作成
        backup_path = backup_file(file_path)
        print(f"📁 バックアップ作成: {backup_path}")
        
        # YAMLファイル読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            print(f"⚠️  スキップ: columnsセクションが見つかりません - {file_path}")
            return False
        
        # カラム順序を修正
        original_columns = data['columns'].copy()
        data['columns'] = reorder_columns(data['columns'])
        
        # 改版履歴を更新
        update_revision_history(data)
        
        # YAMLファイル書き込み
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # 変更内容を表示
        original_order = [col.get('name', '') for col in original_columns]
        new_order = [col.get('name', '') for col in data['columns']]
        
        if original_order != new_order:
            print(f"✅ 修正完了: {os.path.basename(file_path)}")
            print(f"   変更前: {' → '.join(original_order[:5])}...")
            print(f"   変更後: {' → '.join(new_order[:5])}...")
            return True
        else:
            print(f"✅ 変更なし: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {file_path} - {str(e)}")
        return False

def main():
    """メイン処理"""
    print("=" * 70)
    print("🔧 ユーザー要求対応: 全テーブルカラム順序統一修正")
    print("=" * 70)
    
    # テーブル詳細定義ディレクトリ
    table_details_dir = Path("docs/design/database/table-details")
    
    if not table_details_dir.exists():
        print(f"❌ ディレクトリが見つかりません: {table_details_dir}")
        return
    
    # YAMLファイルを取得（バックアップファイルを除外）
    yaml_files = [
        f for f in table_details_dir.glob("*.yaml") 
        if not f.name.endswith('.backup') and 'backup' not in f.name
        and not f.name.startswith('_TEMPLATE')
        and not f.name.startswith('TEMPLATE')
    ]
    
    if not yaml_files:
        print(f"❌ YAMLファイルが見つかりません: {table_details_dir}")
        return
    
    print(f"📋 対象ファイル数: {len(yaml_files)}")
    print()
    
    # 各ファイルを処理
    modified_count = 0
    for yaml_file in sorted(yaml_files):
        if process_yaml_file(yaml_file):
            modified_count += 1
    
    print()
    print("=" * 70)
    print("📊 修正結果サマリー")
    print("=" * 70)
    print(f"✅ 修正完了: {modified_count}/{len(yaml_files)} ファイル")
    print(f"📁 バックアップ: docs/design/database/table-details/*.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    print()
    print("🎯 ユーザー要求に従ったカラム順序:")
    print("   1. id (UUID主キー)")
    print("   2. tenant_id (存在する場合)")
    print("   3. ビジネスキー (コード等)")
    print("   4. 名称系フィールド")
    print("   5. その他の属性")
    print("   6. is_deleted (末尾から3番目)")
    print("   7. created_at (末尾から2番目)")
    print("   8. updated_at (末尾)")

if __name__ == "__main__":
    main()
