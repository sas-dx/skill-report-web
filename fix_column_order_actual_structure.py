#!/usr/bin/env python3
"""
実際のテーブル構造に基づいてカラム順序を修正
実在するカラムのみを対象とした現実的な順序修正
"""

import os
import yaml
import shutil
from pathlib import Path
from datetime import datetime

def fix_column_order_realistic(file_path):
    """実際のカラム構成に基づいてカラム順序を修正"""
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
        
        # 推奨順序の定義（実際に存在するカラムのみ）
        priority_order = [
            # 1. 主キー候補（実際に存在するもの）
            'id',  # UUID主キー
            
            # 2. テナントID（存在する場合）
            'tenant_id',
            
            # 3. ビジネスキー（テーブル固有）
            'employee_code', 'department_code', 'position_code', 'role_code',
            'skill_code', 'certification_code', 'job_type_code',
            
            # 4. 名称系フィールド
            'full_name', 'name', 'display_name', 'title',
            'full_name_kana', 'name_kana',
            
            # 5. 基本属性（よく使われるもの）
            'email', 'description', 'status', 'type', 'category',
        ]
        
        # 終了部分のカラム（固定順序）
        end_order = ['is_deleted', 'created_at', 'updated_at']
        
        # 1. 優先順序のカラムを配置
        for priority_name in priority_order:
            for i, col in enumerate(remaining_columns):
                if col.get('name', '') == priority_name:
                    ordered_columns.append(col)
                    remaining_columns.pop(i)
                    break
        
        # 2. 終了部分のカラムを分離
        end_columns = []
        for end_name in end_order:
            for i, col in enumerate(remaining_columns):
                if col.get('name', '') == end_name:
                    end_columns.append(col)
                    remaining_columns.pop(i)
                    break
        
        # 3. 残りのカラム（その他）を追加
        ordered_columns.extend(remaining_columns)
        
        # 4. 終了部分を追加
        ordered_columns.extend(end_columns)
        
        # カラム順序を更新
        data['columns'] = ordered_columns
        
        # revision_historyを更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        data['revision_history'].append({
            'version': f'12.0.{datetime.now().strftime("%Y%m%d_%H%M%S")}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '現実的カラム順序修正ツール',
            'changes': '実際に存在するカラムに基づいて現実的な順序に修正（id→tenant_id→ビジネスキー→名称→その他→終了部分）'
        })
        
        # バックアップ作成
        backup_path = f"{file_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        
        # ファイル保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # 修正内容を報告
        first_five = [col.get('name', '') for col in ordered_columns[:5]]
        last_three = [col.get('name', '') for col in ordered_columns[-3:]]
        
        return True, f"修正完了 - 先頭5: {first_five}, 末尾3: {last_three}"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("🔧 実際のテーブル構造に基づいてカラム順序を現実的に修正")
    print("=" * 70)
    
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
        
        success, message = fix_column_order_realistic(yaml_file)
        
        if success:
            print(f"✅ {table_name:<30} {message}")
            success_count += 1
        elif "スキップ" in message:
            print(f"⏭️  {table_name:<30} {message}")
            skip_count += 1
        else:
            print(f"❌ {table_name:<30} {message}")
            error_count += 1
    
    print("\n" + "=" * 70)
    print("📊 修正結果サマリー")
    print(f"✅ 修正完了: {success_count} テーブル")
    print(f"⏭️  スキップ: {skip_count} テーブル")
    print(f"❌ エラー: {error_count} テーブル")
    print(f"📁 合計: {success_count + skip_count + error_count} テーブル")
    
    if success_count > 0:
        print(f"\n🎉 {success_count}個のテーブルのカラム順序を現実的な構造に基づいて修正しました！")
        print("📝 各ファイルのバックアップが作成されました")
        print("\n📋 修正された順序:")
        print("   1. id (UUID主キー)")
        print("   2. tenant_id (存在する場合)")
        print("   3. ビジネスキー (employee_code等)")
        print("   4. 名称系フィールド (full_name等)")
        print("   5. その他の属性")
        print("   6. is_deleted")
        print("   7. created_at")
        print("   8. updated_at")

if __name__ == "__main__":
    main()
