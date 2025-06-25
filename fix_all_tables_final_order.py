#!/usr/bin/env python3
"""
全テーブルのカラム順序を要求された順序に修正
{table_name}_id → tenant_id → id → その他 → is_deleted → created_at → updated_at
"""

import os
import yaml
import shutil
from pathlib import Path
from datetime import datetime

def fix_column_order(file_path):
    """カラム順序を修正"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        table_name = data.get('table_name', '')
        columns = data.get('columns', [])
        
        if not columns:
            return False, "カラムが定義されていません"
        
        # 特殊テーブルの処理
        if table_name in ['MST_Tenant', 'MST_UserAuth', '_TEMPLATE']:
            return False, f"{table_name}は特殊テーブルのためスキップ"
        
        # MST_RolePermissionの特殊処理
        if table_name == 'MST_RolePermission':
            # id → tenant_id → その他 → is_deleted → created_at → updated_at
            fixed_columns = []
            other_columns = []
            end_columns = []
            
            for col in columns:
                name = col.get('name', '')
                if name == 'id':
                    fixed_columns.insert(0, col)  # 1番目
                elif name == 'tenant_id':
                    if len(fixed_columns) == 1:
                        fixed_columns.append(col)  # 2番目
                    else:
                        fixed_columns.insert(1, col)
                elif name in ['is_deleted', 'created_at', 'updated_at']:
                    end_columns.append(col)
                else:
                    other_columns.append(col)
            
            # 終了部分を正しい順序で並べ替え
            end_columns_ordered = []
            for end_name in ['is_deleted', 'created_at', 'updated_at']:
                for col in end_columns:
                    if col.get('name') == end_name:
                        end_columns_ordered.append(col)
                        break
            
            data['columns'] = fixed_columns + other_columns + end_columns_ordered
            
        else:
            # 標準テーブルの処理
            table_prefix = table_name.lower()
            expected_primary_key = f"{table_prefix}_id"
            
            primary_key_col = None
            tenant_id_col = None
            uuid_col = None
            other_columns = []
            end_columns = []
            
            # カラムを分類
            for col in columns:
                name = col.get('name', '')
                if name == expected_primary_key:
                    primary_key_col = col
                elif name == 'tenant_id':
                    tenant_id_col = col
                elif name == 'id':
                    uuid_col = col
                elif name in ['is_deleted', 'created_at', 'updated_at']:
                    end_columns.append(col)
                else:
                    other_columns.append(col)
            
            # 終了部分を正しい順序で並べ替え
            end_columns_ordered = []
            for end_name in ['is_deleted', 'created_at', 'updated_at']:
                for col in end_columns:
                    if col.get('name') == end_name:
                        end_columns_ordered.append(col)
                        break
            
            # 新しい順序で組み立て
            new_columns = []
            
            # 1. 主キー
            if primary_key_col:
                new_columns.append(primary_key_col)
            
            # 2. tenant_id
            if tenant_id_col:
                new_columns.append(tenant_id_col)
            
            # 3. UUID(id)
            if uuid_col:
                new_columns.append(uuid_col)
            
            # 4. その他のカラム
            new_columns.extend(other_columns)
            
            # 5. 終了部分
            new_columns.extend(end_columns_ordered)
            
            data['columns'] = new_columns
        
        # revision_historyを更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f'10.0.{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '最終カラム順序統一ツール',
            'changes': '要求仕様に従って主キー→tenant_id→UUID→その他の順序に最終修正'
        })
        
        # バックアップ作成
        backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        
        # ファイル保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return True, "修正完了"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("🔧 全テーブルのカラム順序を要求順序に修正")
    print("=" * 60)
    
    table_details_dir = Path("docs/design/database/table-details")
    
    if not table_details_dir.exists():
        print("❌ table-detailsディレクトリが見つかりません")
        return
    
    yaml_files = list(table_details_dir.glob("テーブル詳細定義YAML_*.yaml"))
    
    if not yaml_files:
        print("❌ YAMLファイルが見つかりません")
        return
    
    success_count = 0
    skip_count = 0
    error_count = 0
    
    for yaml_file in sorted(yaml_files):
        table_name = yaml_file.stem.replace("テーブル詳細定義YAML_", "")
        
        success, message = fix_column_order(yaml_file)
        
        if success:
            print(f"✅ {table_name:<30} {message}")
            success_count += 1
        elif "スキップ" in message:
            print(f"⏭️  {table_name:<30} {message}")
            skip_count += 1
        else:
            print(f"❌ {table_name:<30} {message}")
            error_count += 1
    
    print("\n" + "=" * 60)
    print("📊 修正結果サマリー")
    print(f"✅ 修正完了: {success_count} テーブル")
    print(f"⏭️  スキップ: {skip_count} テーブル")
    print(f"❌ エラー: {error_count} テーブル")
    print(f"📁 合計: {success_count + skip_count + error_count} テーブル")
    
    if success_count > 0:
        print(f"\n🎉 {success_count}個のテーブルのカラム順序を要求仕様に従って修正しました！")
        print("📝 各ファイルのバックアップが作成されました")

if __name__ == "__main__":
    main()
