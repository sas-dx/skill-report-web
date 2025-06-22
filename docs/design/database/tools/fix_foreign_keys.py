#!/usr/bin/env python3
"""
外部キー定義修正スクリプト
YAMLファイルの外部キー定義を標準化する
"""

import os
import yaml
import sys
from pathlib import Path
from typing import Dict, Any, List

def fix_foreign_key_definition(fk_def: Dict[str, Any]) -> Dict[str, Any]:
    """
    外部キー定義を標準化する
    
    Args:
        fk_def: 外部キー定義辞書
        
    Returns:
        修正された外部キー定義
    """
    fixed_fk = {}
    
    # 名前は必須
    if 'name' in fk_def:
        fixed_fk['name'] = fk_def['name']
    else:
        fixed_fk['name'] = "fk_unknown"
    
    # columnsフィールドの修正
    if 'columns' in fk_def and fk_def['columns']:
        fixed_fk['columns'] = fk_def['columns']
    elif 'column' in fk_def:
        # 単数形から複数形に変換
        fixed_fk['columns'] = [fk_def['column']]
    else:
        # デフォルト値を設定
        fixed_fk['columns'] = ["column_name"]
    
    # referencesフィールドの修正
    if 'references' in fk_def and isinstance(fk_def['references'], dict):
        fixed_fk['references'] = fk_def['references']
        
        # references内のtableとcolumnsを確認
        if 'table' not in fixed_fk['references']:
            fixed_fk['references']['table'] = "REFERENCE_TABLE"
        
        if 'columns' not in fixed_fk['references']:
            if 'column' in fixed_fk['references']:
                fixed_fk['references']['columns'] = [fixed_fk['references']['column']]
                del fixed_fk['references']['column']
            else:
                fixed_fk['references']['columns'] = ["reference_column"]
    elif 'reference_table' in fk_def:
        # 古い形式から新しい形式に変換
        fixed_fk['references'] = {
            'table': fk_def['reference_table'],
            'columns': fk_def.get('reference_columns', ["reference_column"])
        }
    else:
        # デフォルト値を設定
        fixed_fk['references'] = {
            'table': "REFERENCE_TABLE",
            'columns': ["reference_column"]
        }
    
    # その他のフィールド
    fixed_fk['on_update'] = fk_def.get('on_update', 'RESTRICT')
    fixed_fk['on_delete'] = fk_def.get('on_delete', 'RESTRICT')
    fixed_fk['comment'] = fk_def.get('comment', '外部キー制約')
    
    return fixed_fk

def fix_yaml_file(file_path: Path) -> bool:
    """
    YAMLファイルの外部キー定義を修正する
    
    Args:
        file_path: YAMLファイルのパス
        
    Returns:
        修正が行われた場合True
    """
    try:
        # YAMLファイルを読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'foreign_keys' not in data:
            return False
        
        # 外部キー定義が存在しない場合はスキップ
        if not data['foreign_keys']:
            return False
        
        modified = False
        fixed_foreign_keys = []
        
        for fk_def in data['foreign_keys']:
            if not isinstance(fk_def, dict):
                continue
                
            # 外部キー定義を修正
            fixed_fk = fix_foreign_key_definition(fk_def)
            fixed_foreign_keys.append(fixed_fk)
            
            # 変更があったかチェック
            if fixed_fk != fk_def:
                modified = True
        
        if modified:
            # 修正された外部キー定義を設定
            data['foreign_keys'] = fixed_foreign_keys
            
            # ファイルに書き戻し
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            print(f"✅ 修正完了: {file_path.name}")
            return True
        else:
            print(f"ℹ️  修正不要: {file_path.name}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {file_path.name} - {e}")
        return False

def main():
    """メイン処理"""
    # ベースディレクトリの設定
    script_dir = Path(__file__).parent
    base_dir = script_dir.parent.parent.parent
    yaml_dir = base_dir / "design" / "database" / "table-details"
    
    if not yaml_dir.exists():
        print(f"❌ YAMLディレクトリが見つかりません: {yaml_dir}")
        sys.exit(1)
    
    print("🔧 外部キー定義修正スクリプト開始")
    print(f"📁 対象ディレクトリ: {yaml_dir}")
    
    # YAMLファイルを検索
    yaml_files = list(yaml_dir.glob("*_details.yaml"))
    
    if not yaml_files:
        print("❌ YAMLファイルが見つかりません")
        sys.exit(1)
    
    print(f"📄 対象ファイル数: {len(yaml_files)}")
    
    # 各ファイルを処理
    modified_count = 0
    error_count = 0
    
    for yaml_file in sorted(yaml_files):
        try:
            if fix_yaml_file(yaml_file):
                modified_count += 1
        except Exception as e:
            print(f"❌ 処理エラー: {yaml_file.name} - {e}")
            error_count += 1
    
    # 結果表示
    print("\n" + "="*50)
    print("🎯 外部キー定義修正完了")
    print(f"📊 処理結果:")
    print(f"   - 総ファイル数: {len(yaml_files)}")
    print(f"   - 修正ファイル数: {modified_count}")
    print(f"   - エラーファイル数: {error_count}")
    print(f"   - 修正不要ファイル数: {len(yaml_files) - modified_count - error_count}")
    
    if error_count > 0:
        print(f"\n⚠️  {error_count}件のエラーが発生しました")
        sys.exit(1)
    else:
        print("\n✅ 全ての処理が正常に完了しました")

if __name__ == "__main__":
    main()
