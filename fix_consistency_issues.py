#!/usr/bin/env python3
"""
整合性問題の修正スクリプト
"""

import os
import re
import glob
import yaml
from pathlib import Path

def fix_template_issue():
    """テンプレートファイルの不整合を修正"""
    print("🔧 テンプレートファイルの不整合を修正中...")
    
    # _TEMPLATEのYAMLファイルを探す
    yaml_dir = Path("docs/design/database/table-details")
    template_files = list(yaml_dir.glob("*_TEMPLATE*.yaml"))
    
    if template_files:
        template_file = template_files[0]
        print(f"  📄 テンプレートファイル発見: {template_file.name}")
        
        # YAMLファイルを読み込み
        with open(template_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # table_nameを修正
        if data and 'table_name' in data:
            old_name = data['table_name']
            data['table_name'] = 'MST_TEMPLATE'
            
            # ファイルを更新
            with open(template_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"  ✅ テーブル名を修正: {old_name} → MST_TEMPLATE")
    
    # サンプルデータファイルも確認・修正
    data_dir = Path("docs/design/database/data")
    sample_files = list(data_dir.glob("*TEMPLATE*_sample_data.sql"))
    
    for sample_file in sample_files:
        print(f"  📄 サンプルデータファイル: {sample_file.name}")
        
        with open(sample_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # INSERT文のテーブル名を修正
        content = re.sub(r'INSERT\s+INTO\s+_TEMPLATE', 'INSERT INTO MST_TEMPLATE', content, flags=re.IGNORECASE)
        
        with open(sample_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  ✅ サンプルデータのテーブル名を修正")

def fix_trn_table_columns():
    """TRNテーブルのcreated_by, updated_byカラムを追加"""
    print("🔧 TRNテーブルのカラム定義を修正中...")
    
    trn_tables = [
        'TRN_SkillRecord',
        'TRN_EmployeeSkillGrade', 
        'TRN_SkillEvidence',
        'TRN_PDU',
        'TRN_Notification',
        'TRN_TrainingHistory',
        'TRN_ProjectRecord',
        'TRN_GoalProgress'
    ]
    
    yaml_dir = Path("docs/design/database/table-details")
    
    for table_name in trn_tables:
        yaml_files = list(yaml_dir.glob(f"*{table_name}*.yaml"))
        
        if yaml_files:
            yaml_file = yaml_files[0]
            print(f"  📄 処理中: {table_name}")
            
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                
                if data and 'columns' in data:
                    columns = data['columns']
                    
                    # created_by, updated_byカラムが存在するかチェック
                    column_names = [col['name'] for col in columns]
                    
                    needs_update = False
                    
                    if 'created_by' not in column_names:
                        # created_byカラムを追加（updated_atの前に挿入）
                        insert_index = len(columns)
                        for i, col in enumerate(columns):
                            if col['name'] == 'updated_at':
                                insert_index = i
                                break
                        
                        created_by_col = {
                            'name': 'created_by',
                            'type': 'VARCHAR(50)',
                            'nullable': True,
                            'primary_key': False,
                            'unique': False,
                            'default': None,
                            'comment': '作成者ID',
                            'requirement_id': 'SYS.1-AUDIT.1'
                        }
                        
                        columns.insert(insert_index, created_by_col)
                        needs_update = True
                        print(f"    ✅ created_byカラムを追加")
                    
                    if 'updated_by' not in column_names:
                        # updated_byカラムを追加（updated_atの前に挿入）
                        insert_index = len(columns)
                        for i, col in enumerate(columns):
                            if col['name'] == 'updated_at':
                                insert_index = i
                                break
                        
                        updated_by_col = {
                            'name': 'updated_by',
                            'type': 'VARCHAR(50)',
                            'nullable': True,
                            'primary_key': False,
                            'unique': False,
                            'default': None,
                            'comment': '更新者ID',
                            'requirement_id': 'SYS.1-AUDIT.1'
                        }
                        
                        columns.insert(insert_index, updated_by_col)
                        needs_update = True
                        print(f"    ✅ updated_byカラムを追加")
                    
                    if needs_update:
                        # ファイルを更新
                        with open(yaml_file, 'w', encoding='utf-8') as f:
                            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                        
                        print(f"    💾 {table_name} のYAML定義を更新")
                    else:
                        print(f"    ℹ️ {table_name} は既に正しい定義")
                        
            except Exception as e:
                print(f"    ❌ {table_name} の処理でエラー: {e}")

def main():
    """メイン処理"""
    print("=" * 80)
    print("整合性問題の修正")
    print("=" * 80)
    
    # テンプレートファイルの修正
    fix_template_issue()
    print()
    
    # TRNテーブルのカラム修正
    fix_trn_table_columns()
    print()
    
    print("✅ 整合性問題の修正が完了しました！")
    print("次に table_generator を実行して全テーブルを再生成してください。")

if __name__ == "__main__":
    main()
