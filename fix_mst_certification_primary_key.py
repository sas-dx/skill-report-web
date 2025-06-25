#!/usr/bin/env python3
"""
MST_Certification テーブルの主キー問題修正スクリプト

問題:
- id と certification_id の両方が存在
- certification_id が primary_key: true になっている
- 正しくは id が UUID 主キーであるべき

修正内容:
1. certification_id カラムを削除
2. id を primary_key: true に設定
3. カラム順序を調整
"""

import yaml
import os
from datetime import datetime

def fix_mst_certification_yaml():
    yaml_file = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Certification.yaml"
    
    # バックアップ作成
    backup_file = f"{yaml_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.system(f"cp '{yaml_file}' '{backup_file}'")
    print(f"📁 バックアップ作成: {backup_file}")
    
    # YAMLファイル読み込み
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    print("🔧 MST_Certification 主キー問題修正開始")
    
    # 現在のカラム数
    original_count = len(data['columns'])
    print(f"📊 修正前カラム数: {original_count}")
    
    # certification_id カラムを削除
    data['columns'] = [col for col in data['columns'] if col['name'] != 'certification_id']
    
    # id カラムを主キーに設定
    for col in data['columns']:
        if col['name'] == 'id':
            col['primary_key'] = True
            col['unique'] = False  # 主キーなので unique は不要
            print(f"✅ id カラムを主キーに設定")
            break
    
    # カラム順序を調整（id を最初に）
    id_column = None
    other_columns = []
    
    for col in data['columns']:
        if col['name'] == 'id':
            id_column = col
        else:
            other_columns.append(col)
    
    if id_column:
        data['columns'] = [id_column] + other_columns
        print(f"✅ カラム順序調整完了（id を最初に配置）")
    
    # 改版履歴更新
    new_version = {
        'version': '3.2.20250624',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': '主キー修正ツール',
        'changes': 'certification_id カラム削除、id を正しい主キーに設定'
    }
    data['revision_history'].append(new_version)
    
    # 修正後のカラム数
    final_count = len(data['columns'])
    print(f"📊 修正後カラム数: {final_count}")
    print(f"📝 削除されたカラム数: {original_count - final_count}")
    
    # ファイル保存
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ 修正完了: {yaml_file}")
    
    return True

if __name__ == "__main__":
    try:
        success = fix_mst_certification_yaml()
        if success:
            print("\n🎉 MST_Certification 主キー修正が正常に完了しました！")
            print("\n📋 次のステップ:")
            print("1. python3 docs/design/database/tools/generate_table_direct.py --table MST_Certification --verbose")
            print("2. 生成されたファイルの確認")
        else:
            print("\n❌ 修正中にエラーが発生しました")
    except Exception as e:
        print(f"\n💥 エラー: {e}")
