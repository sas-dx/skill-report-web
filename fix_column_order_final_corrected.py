#!/usr/bin/env python3
"""
全テーブルのカラム順序を要求された順序に修正（実際のカラム構成に基づく）
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
        
        # 現在のカラム名を確認
        column_names = [col.get('name', '') for col in columns]
        
        # 実際に存在するカラムに基づいて順序を決定
        ordered_columns = []
        remaining_columns = columns.copy()
        
        # 1. 主キー（{table_name}_id または id）
        table_prefix = table_name.lower()
        expected_primary_key = f"{table_prefix}_id"
        
        # 主キーを探す
        primary_key_found = False
        for i, col in enumerate(remaining_columns):
            name = col.get('name', '')
            if name == expected_primary_key or (name == 'id' and not primary_key_found):
                ordered_columns.append(col)
                remaining_columns.pop(i)
                primary_key_found = True
                break
        
        # 2. tenant_id（存在する場合）
        for i, col in enumerate(remaining_columns):
            if col.get('name', '') == 'tenant_id':
                ordered_columns.append(col)
                remaining_columns.pop(i)
                break
        
        # 3. id（主キーでない場合のUUID）
        if not primary_key_found:
            for i, col in enumerate(remaining_columns):
                if col.get('name', '') == 'id':
                    ordered_columns.append(col)
                    remaining_columns.pop(i)
                    break
        
        # 4. 終了部分のカラムを分離
        end_columns = []
        for end_name in ['is_deleted', 'created_at', 'updated_at']:
            for i, col in enumerate(remaining_columns):
                if col.get('name', '') == end_name:
                    end_columns.append(col)
                    remaining_columns.pop(i)
                    break
        
        # 5. 残りのカラム（その他）
        ordered_columns.extend(remaining_columns)
        
        # 6. 終了部分を追加
        ordered_columns.extend(end_columns)
        
        # カラム順序を更新
        data['columns'] = ordered_columns
        
        # revision_historyを更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f'11.0.{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '最終カラム順序修正ツール（実構成対応版）',
            'changes': '実際のカラム構成に基づいて主キー→tenant_id→その他→終了部分の順序に修正'
        })
        
        # バックアップ作成
        backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        
        # ファイル保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # 修正内容を報告
        first_three = [col.get('name', '') for col in ordered_columns[:3]]
        last_three = [col.get('name', '') for col in ordered_columns[-3:]]
        
        return True, f"修正完了 - 先頭3: {first_three}, 末尾3: {last_three}"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("🔧 全テーブルのカラム順序を実際の構成に基づいて修正")
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
        print(f"\n🎉 {success_count}個のテーブルのカラム順序を実際の構成に基づいて修正しました！")
        print("📝 各ファイルのバックアップが作成されました")

if __name__ == "__main__":
    main()
