#!/usr/bin/env python3
"""
MST_Certification テーブルのカラム順序統一スクリプト

要求されたカラム順序:
1. certification_id      # 主キー（最優先）
2. tenant_id            # テナントID（マルチテナント対応）
3. id                   # UUID（セカンダリキー）
4. certification_code   # ビジネスキー
5. certification_name   # 基本情報
6. certification_name_en
7. issuer
8. issuer_country
9. certification_category
10. certification_level
... (その他のビジネス属性)
21. is_deleted          # システム属性
22. created_at
23. updated_at
"""

import yaml
import os
from datetime import datetime

def fix_certification_column_order():
    yaml_file = "docs/design/database/table-details/テーブル詳細定義YAML_MST_Certification.yaml"
    
    # バックアップ作成
    backup_file = f"{yaml_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.system(f"cp '{yaml_file}' '{backup_file}'")
    print(f"📁 バックアップ作成: {backup_file}")
    
    # YAMLファイル読み込み
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    print("🔧 MST_Certification カラム順序統一開始")
    
    # 現在のカラムを辞書化（名前をキーとして）
    current_columns = {col['name']: col for col in data['columns']}
    print(f"📊 現在のカラム数: {len(current_columns)}")
    
    # certification_id カラムを追加（主キー）
    certification_id_column = {
        'name': 'certification_id',
        'logical': '資格ID',
        'type': 'INTEGER',
        'length': None,
        'null': False,
        'unique': False,
        'encrypted': False,
        'description': '資格ID（主キー、AUTO_INCREMENT）',
        'default': None,
        'primary_key': True,
        'auto_increment': True
    }
    
    # id カラムの主キー設定を解除
    if 'id' in current_columns:
        current_columns['id']['primary_key'] = False
        current_columns['id']['unique'] = True  # UUIDとして一意性は保持
        print("✅ id カラムの主キー設定を解除、unique設定に変更")
    
    # 要求されたカラム順序を定義
    desired_order = [
        'certification_id',      # 1. 主キー（最優先）
        'tenant_id',            # 2. テナントID（マルチテナント対応）
        'id',                   # 3. UUID（セカンダリキー）
        'certification_code',   # 4. ビジネスキー
        'certification_name',   # 5. 基本情報
        'certification_name_en', # 6.
        'issuer',               # 7.
        'issuer_country',       # 8.
        'certification_category', # 9.
        'certification_level',  # 10.
        'description',          # 11. その他のビジネス属性
        'skill_category_id',    # 12.
        'official_url',         # 13.
        'exam_fee',             # 14.
        'exam_format',          # 15.
        'exam_language',        # 16.
        'is_recommended',       # 17.
        'renewal_required',     # 18.
        'renewal_requirements', # 19.
        'validity_period_months', # 20.
        'is_active',            # 21.
        'is_deleted',           # 22. システム属性
        'created_at',           # 23.
        'updated_at'            # 24.
    ]
    
    # 新しいカラム順序でカラムリストを再構築
    new_columns = []
    
    # certification_id を最初に追加
    new_columns.append(certification_id_column)
    print("✅ certification_id カラムを主キーとして追加")
    
    # 指定された順序でカラムを追加
    for col_name in desired_order[1:]:  # certification_id は既に追加済み
        if col_name in current_columns:
            new_columns.append(current_columns[col_name])
        else:
            print(f"⚠️ カラム '{col_name}' が見つかりません")
    
    # 順序に含まれていないカラムがあれば最後に追加
    for col_name, col_data in current_columns.items():
        if col_name not in desired_order:
            new_columns.append(col_data)
            print(f"📝 順序外カラム '{col_name}' を最後に追加")
    
    # カラムリストを更新
    data['columns'] = new_columns
    
    # 改版履歴更新
    new_version = {
        'version': '4.0.20250624',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'author': 'カラム順序統一ツール',
        'changes': 'certification_id を主キーとして復活、指定されたカラム順序に統一'
    }
    data['revision_history'].append(new_version)
    
    print(f"📊 修正後カラム数: {len(new_columns)}")
    
    # ファイル保存
    with open(yaml_file, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"✅ 修正完了: {yaml_file}")
    
    # カラム順序の確認表示
    print("\n📋 新しいカラム順序:")
    for i, col in enumerate(new_columns, 1):
        pk_mark = " (PK)" if col.get('primary_key') else ""
        unique_mark = " (UNIQUE)" if col.get('unique') else ""
        print(f"{i:2d}. {col['name']}{pk_mark}{unique_mark}")
    
    return True

if __name__ == "__main__":
    try:
        success = fix_certification_column_order()
        if success:
            print("\n🎉 MST_Certification カラム順序統一が正常に完了しました！")
            print("\n📋 次のステップ:")
            print("1. python3 docs/design/database/tools/generate_table_direct.py --table MST_Certification --verbose")
            print("2. 生成されたファイルの確認")
            print("3. 他のテーブルへの同様の修正適用")
        else:
            print("\n❌ 修正中にエラーが発生しました")
    except Exception as e:
        print(f"\n💥 エラー: {e}")
