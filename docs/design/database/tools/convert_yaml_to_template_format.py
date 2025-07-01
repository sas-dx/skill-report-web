#!/usr/bin/env python3
"""
YAML形式変換スクリプト
既存のテーブル詳細定義YAMLを_TEMPLATE_details.yamlの形式に変換する

要求仕様ID: PLT.1-WEB.1
対応設計書: docs/design/database/tools/README.md
"""

import os
import yaml
import shutil
from datetime import datetime
from pathlib import Path

def convert_yaml_file(input_file_path, output_file_path=None):
    """
    YAMLファイルを_TEMPLATE形式に変換
    
    Args:
        input_file_path (str): 入力ファイルパス
        output_file_path (str): 出力ファイルパス（Noneの場合は上書き）
    """
    if output_file_path is None:
        output_file_path = input_file_path
    
    print(f"変換中: {input_file_path}")
    
    # バックアップ作成
    backup_path = f"{input_file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(input_file_path, backup_path)
    print(f"バックアップ作成: {backup_path}")
    
    # YAMLファイル読み込み
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # 新しい形式のデータ構造を作成
    converted_data = {}
    
    # 基本情報をコピー
    converted_data['table_name'] = data.get('table_name', '')
    converted_data['logical_name'] = data.get('logical_name', '')
    converted_data['category'] = data.get('category', '')
    
    # revision_historyをコピー（既存の形式を保持）
    if 'revision_history' in data:
        converted_data['revision_history'] = data['revision_history']
        # 変換履歴を追加
        converted_data['revision_history'].append({
            'version': f"{len(data['revision_history']) + 1}.0.0",
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '自動変換ツール',
            'changes': 'テンプレート形式への自動変換'
        })
    else:
        converted_data['revision_history'] = [{
            'version': '1.0.0',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '自動変換ツール',
            'changes': 'テンプレート形式への変換'
        }]
    
    # overviewをコピー
    converted_data['overview'] = data.get('overview', '')
    
    # columnsセクションの変換
    converted_data['columns'] = []
    
    # business_columnsから変換
    if 'business_columns' in data:
        for col in data['business_columns']:
            converted_col = {
                'name': col.get('name', ''),
                'logical': col.get('logical', ''),
                'type': col.get('type', ''),
                'length': col.get('length'),
                'null': col.get('null', True),
                'unique': col.get('unique', False),
                'encrypted': col.get('encrypted', False),
                'description': col.get('description', '')
            }
            
            # enum_valuesがある場合は追加
            if 'enum_values' in col:
                converted_col['enum_values'] = col['enum_values']
            
            # defaultがある場合は追加
            if 'default' in col:
                converted_col['default'] = col['default']
            
            # validationがある場合は追加
            if 'validation' in col:
                converted_col['validation'] = col['validation']
            
            converted_data['columns'].append(converted_col)
    
    # 既存のcolumnsセクションがある場合は、それも追加（重複チェック）
    if 'columns' in data:
        existing_names = {col['name'] for col in converted_data['columns']}
        for col in data['columns']:
            if col.get('name') not in existing_names:
                # フィールド名を変換
                converted_col = {
                    'name': col.get('name', ''),
                    'logical': col.get('logical', col.get('comment', '')),
                    'type': col.get('type', ''),
                    'length': col.get('length'),
                    'null': col.get('nullable', col.get('null', True)),
                    'unique': col.get('unique', False),
                    'encrypted': False,  # デフォルト値
                    'description': col.get('comment', col.get('description', ''))
                }
                
                # defaultがある場合は追加
                if 'default' in col:
                    converted_col['default'] = col['default']
                
                converted_data['columns'].append(converted_col)
    
    # indexesセクションの変換
    converted_data['indexes'] = []
    
    # business_indexesから変換
    if 'business_indexes' in data:
        for idx in data['business_indexes']:
            converted_idx = {
                'name': idx.get('name', ''),
                'columns': [[col] for col in idx.get('columns', [])],  # テンプレート形式に合わせる
                'unique': idx.get('unique', False),
                'description': idx.get('description', '')
            }
            converted_data['indexes'].append(converted_idx)
    
    # 既存のindexesセクションがある場合は追加
    if 'indexes' in data:
        existing_names = {idx['name'] for idx in converted_data['indexes']}
        for idx in data['indexes']:
            if idx.get('name') not in existing_names:
                converted_idx = {
                    'name': idx.get('name', ''),
                    'columns': [[col] for col in idx.get('columns', [])],
                    'unique': idx.get('unique', False),
                    'description': idx.get('comment', idx.get('description', ''))
                }
                converted_data['indexes'].append(converted_idx)
    
    # constraintsセクションの変換
    converted_data['constraints'] = []
    
    # business_constraintsから変換
    if 'business_constraints' in data:
        for const in data['business_constraints']:
            converted_const = {
                'name': const.get('name', ''),
                'type': const.get('type', ''),
                'description': const.get('description', '')
            }
            
            if 'columns' in const:
                converted_const['columns'] = [[col] for col in const['columns']]
            
            if 'condition' in const:
                converted_const['condition'] = const['condition']
            
            converted_data['constraints'].append(converted_const)
    
    # foreign_keysセクションの変換
    converted_data['foreign_keys'] = []
    
    if 'foreign_keys' in data:
        for fk in data['foreign_keys']:
            converted_fk = {
                'name': fk.get('name', ''),
                'columns': [[col] for col in fk.get('columns', [])],
                'references': {
                    'table': [fk.get('references', {}).get('table', '')],
                    'columns': fk.get('references', {}).get('columns', [])
                },
                'on_update': fk.get('on_update', 'CASCADE'),
                'on_delete': fk.get('on_delete', 'RESTRICT'),
                'comment': fk.get('comment', '外部キー制約')
            }
            converted_data['foreign_keys'].append(converted_fk)
    
    # sample_dataをコピー
    if 'sample_data' in data:
        converted_data['sample_data'] = data['sample_data']
    
    # notesセクションの変換
    notes = []
    if 'notes' in data:
        notes.extend(data['notes'])
    
    # business_rulesの内容をnotesに統合
    if 'business_rules' in data:
        notes.append("=== 業務ルール ===")
        notes.extend(data['business_rules'])
    
    # 最低3項目を保証
    while len(notes) < 3:
        notes.append(f"[特記事項{len(notes) + 1}]")
    
    converted_data['notes'] = notes
    
    # rulesセクションの作成
    rules = []
    if 'business_rules' in data:
        rules.extend(data['business_rules'])
    
    # 最低3項目を保証
    while len(rules) < 3:
        rules.append(f"[ルール{len(rules) + 1}]")
    
    converted_data['rules'] = rules
    
    # YAMLファイルとして出力
    with open(output_file_path, 'w', encoding='utf-8') as f:
        yaml.dump(converted_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"変換完了: {output_file_path}")
    return True

def main():
    """メイン処理"""
    table_details_dir = Path("docs/design/database/table-details")
    
    if not table_details_dir.exists():
        print(f"エラー: ディレクトリが存在しません: {table_details_dir}")
        return
    
    # _TEMPLATE_details.yamlを除く全YAMLファイルを処理
    yaml_files = [f for f in table_details_dir.glob("*.yaml") 
                  if f.name != "_TEMPLATE_details.yaml" and not f.name.endswith('.bak')]
    
    print(f"変換対象ファイル数: {len(yaml_files)}")
    
    success_count = 0
    error_count = 0
    
    for yaml_file in yaml_files:
        try:
            convert_yaml_file(str(yaml_file))
            success_count += 1
        except Exception as e:
            print(f"エラー: {yaml_file} - {str(e)}")
            error_count += 1
    
    print(f"\n変換結果:")
    print(f"成功: {success_count}ファイル")
    print(f"失敗: {error_count}ファイル")
    print(f"総計: {len(yaml_files)}ファイル")

if __name__ == "__main__":
    main()
