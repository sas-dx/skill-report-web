#!/usr/bin/env python3
"""
MST_Tenantテーブルの特殊ケースを修正するスクリプト
MST_Tenantテーブルではtenant_idが実質的な主キーなので、順序を調整
"""

import os
import yaml
from datetime import datetime

def fix_mst_tenant_column_order():
    """MST_Tenantテーブルのカラム順序を修正"""
    file_path = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Tenant.yaml"
    
    if not os.path.exists(file_path):
        print(f"エラー: ファイルが見つかりません: {file_path}")
        return False
    
    # バックアップ作成
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"バックアップ作成: {backup_path}")
        
        # YAML読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            print("エラー: columnsセクションが見つかりません")
            return False
        
        columns = data['columns']
        
        # 現在のカラム順序を確認
        current_order = [col['name'] for col in columns]
        print(f"現在のカラム順序: {current_order[:5]}...")
        
        # MST_Tenantの特殊な順序を定義
        # 1. tenant_id (実質的な主キー)
        # 2. id (UUID)
        # 3. tenant_code (ビジネスキー)
        # 4. その他のカラム...
        # n-2. is_deleted
        # n-1. created_at
        # n. updated_at
        
        # カラムを辞書形式で管理
        column_dict = {col['name']: col for col in columns}
        
        # 新しい順序でカラムを並び替え
        new_order = []
        
        # 1. tenant_id (実質的な主キー)
        if 'tenant_id' in column_dict:
            new_order.append(column_dict['tenant_id'])
        
        # 2. id (UUID)
        if 'id' in column_dict:
            new_order.append(column_dict['id'])
        
        # 3. tenant_code (ビジネスキー)
        if 'tenant_code' in column_dict:
            new_order.append(column_dict['tenant_code'])
        
        # 4. domain_name (重要なビジネスキー)
        if 'domain_name' in column_dict:
            new_order.append(column_dict['domain_name'])
        
        # 5. 名称系フィールド
        name_fields = ['tenant_name', 'tenant_name_en', 'tenant_short_name']
        for field in name_fields:
            if field in column_dict:
                new_order.append(column_dict[field])
        
        # 6. 基本属性（アルファベット順）
        basic_fields = []
        for col_name in sorted(column_dict.keys()):
            if col_name not in ['tenant_id', 'id', 'tenant_code', 'domain_name'] + name_fields + ['is_deleted', 'created_at', 'updated_at']:
                basic_fields.append(col_name)
        
        for field in basic_fields:
            new_order.append(column_dict[field])
        
        # 7. 終了部分
        end_fields = ['is_deleted', 'created_at', 'updated_at']
        for field in end_fields:
            if field in column_dict:
                new_order.append(column_dict[field])
        
        # カラム順序を更新
        data['columns'] = new_order
        
        # revision_historyを更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f'10.0.{timestamp}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': 'MST_Tenant特殊ケース修正ツール',
            'changes': 'MST_Tenantテーブルの特殊ケース対応：tenant_idを実質的な主キーとして先頭に配置'
        })
        
        # YAML保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        new_column_order = [col['name'] for col in new_order]
        print(f"修正後のカラム順序: {new_column_order[:5]}...")
        print(f"✅ MST_Tenantテーブルのカラム順序を修正しました")
        
        return True
        
    except Exception as e:
        print(f"エラー: {str(e)}")
        return False

def main():
    """メイン処理"""
    print("MST_Tenantテーブルの特殊ケース修正を開始...")
    
    success = fix_mst_tenant_column_order()
    
    if success:
        print("\n🎉 MST_Tenantテーブルの修正が完了しました！")
    else:
        print("\n❌ 修正に失敗しました")

if __name__ == "__main__":
    main()
