#!/usr/bin/env python3
"""
YAML構造修正スクリプト
- indexesとforeign_keysのcolumns構造を修正
- 二重リスト構造を単一リスト構造に変換
"""

import os
import yaml
import glob
from datetime import datetime

def fix_yaml_structure(file_path):
    """YAML構造を修正"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        modified = False
        
        # indexesセクションの修正
        if 'indexes' in data and isinstance(data['indexes'], list):
            for index in data['indexes']:
                if 'columns' in index and isinstance(index['columns'], list):
                    # 二重リスト構造を単一リスト構造に変換
                    new_columns = []
                    for col in index['columns']:
                        if isinstance(col, list) and len(col) > 0:
                            new_columns.append(col[0])  # 最初の要素を取得
                        elif isinstance(col, str):
                            new_columns.append(col)
                    
                    if new_columns != index['columns']:
                        index['columns'] = new_columns
                        modified = True
        
        # foreign_keysセクションの修正
        if 'foreign_keys' in data and isinstance(data['foreign_keys'], list):
            for fk in data['foreign_keys']:
                # columnsの修正
                if 'columns' in fk and isinstance(fk['columns'], list):
                    new_columns = []
                    for col in fk['columns']:
                        if isinstance(col, list) and len(col) > 0:
                            new_columns.append(col[0])
                        elif isinstance(col, str):
                            new_columns.append(col)
                    
                    if new_columns != fk['columns']:
                        fk['columns'] = new_columns
                        modified = True
                
                # referencesの修正
                if 'references' in fk:
                    ref = fk['references']
                    
                    # tableの修正
                    if 'table' in ref and isinstance(ref['table'], list):
                        if len(ref['table']) > 0:
                            ref['table'] = ref['table'][0]
                            modified = True
                    
                    # columnsの修正
                    if 'columns' in ref and isinstance(ref['columns'], list):
                        new_ref_columns = []
                        for col in ref['columns']:
                            if isinstance(col, list) and len(col) > 0:
                                new_ref_columns.append(col[0])
                            elif isinstance(col, str):
                                new_ref_columns.append(col)
                        
                        if new_ref_columns != ref['columns']:
                            ref['columns'] = new_ref_columns
                            modified = True
        
        # 修正があった場合のみファイルを更新
        if modified:
            # バックアップ作成
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"{file_path}.backup.{timestamp}"
            os.rename(file_path, backup_path)
            
            # 修正版を保存
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"✅ 修正完了: {os.path.basename(file_path)}")
            return True
        else:
            print(f"⏭️  修正不要: {os.path.basename(file_path)}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {os.path.basename(file_path)} - {str(e)}")
        return False

def main():
    """メイン処理"""
    print("🔧 YAML構造修正スクリプト開始")
    
    # YAMLファイルを検索
    yaml_pattern = "docs/design/database/table-details/テーブル詳細定義YAML_*.yaml"
    yaml_files = glob.glob(yaml_pattern)
    
    if not yaml_files:
        print(f"❌ YAMLファイルが見つかりません: {yaml_pattern}")
        return
    
    print(f"📁 対象ファイル数: {len(yaml_files)}")
    
    success_count = 0
    error_count = 0
    
    for yaml_file in sorted(yaml_files):
        if fix_yaml_structure(yaml_file):
            success_count += 1
        else:
            error_count += 1
    
    print(f"\n📊 処理結果:")
    print(f"   - 総ファイル数: {len(yaml_files)}")
    print(f"   - 修正ファイル数: {success_count}")
    print(f"   - エラー数: {error_count}")
    
    if error_count == 0:
        print("✅ 全ての修正が完了しました")
    else:
        print(f"⚠️  {error_count}件のエラーが発生しました")

if __name__ == "__main__":
    main()
