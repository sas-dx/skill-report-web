#!/usr/bin/env python3
"""
全テーブルのカラム順序を推奨順序に修正するスクリプト
"""

import yaml
import os
import glob
import shutil
from typing import List, Dict, Any
from datetime import datetime

def categorize_column(column_name: str) -> tuple:
    """カラム名を分類して優先度を返す"""
    name = column_name.lower()
    
    # 1. 主キー
    if name == 'id':
        return (1, 0, column_name)
    
    # 2. ビジネスキー
    if any(suffix in name for suffix in ['_code', '_number', '_key']) and not name.endswith('_id'):
        return (2, 0, column_name)
    
    # 3. 基本情報
    if any(prefix in name for prefix in ['name', 'title', 'description', 'logical']):
        return (3, 0, column_name)
    
    # 4. 関連ID（外部キー）
    if name.endswith('_id') and name != 'id':
        return (4, 0, column_name)
    
    # 5. ステータス・フラグ
    if any(keyword in name for keyword in ['status', 'type', 'category', 'level', 'grade', 'priority']):
        return (5, 0, column_name)
    
    # 6. その他のデータ
    if any(keyword in name for keyword in ['value', 'amount', 'count', 'date', 'time', 'url', 'path', 'email', 'phone']):
        return (6, 0, column_name)
    
    # 7. システム項目
    system_columns = ['is_active', 'is_deleted', 'created_at', 'updated_at', 'created_by', 'updated_by']
    if name in system_columns:
        system_order = {
            'is_active': 0,
            'is_deleted': 1,
            'created_at': 2,
            'updated_at': 3,
            'created_by': 4,
            'updated_by': 5
        }
        return (7, system_order.get(name, 99), column_name)
    
    # その他
    return (6, 50, column_name)

def get_recommended_column_order(columns: List[Dict]) -> List[Dict]:
    """カラムリストを推奨順序でソート"""
    def sort_key(col):
        return categorize_column(col['name'])
    
    return sorted(columns, key=sort_key)

def fix_table_column_order(yaml_file: str, backup: bool = True) -> Dict[str, Any]:
    """テーブルのカラム順序を修正"""
    try:
        # バックアップ作成
        if backup:
            backup_file = f"{yaml_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copy2(yaml_file, backup_file)
            print(f"    📁 バックアップ作成: {backup_file}")
        
        # YAMLファイル読み込み
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        table_name = data.get('table_name', 'UNKNOWN')
        columns = data.get('columns', [])
        
        if not columns:
            return {
                'table_name': table_name,
                'status': 'ERROR',
                'message': 'カラム定義が見つかりません'
            }
        
        # 現在の順序
        current_order = [col['name'] for col in columns]
        
        # 推奨順序でソート
        recommended_columns = get_recommended_column_order(columns)
        recommended_order = [col['name'] for col in recommended_columns]
        
        # 順序が一致するかチェック
        if current_order == recommended_order:
            return {
                'table_name': table_name,
                'status': 'NO_CHANGE',
                'message': '既に正しい順序です'
            }
        
        # カラム順序を修正
        data['columns'] = recommended_columns
        
        # revision_historyを更新
        if 'revision_history' in data:
            new_version = {
                'version': f"3.1.{datetime.now().strftime('%Y%m%d')}",
                'date': datetime.now().strftime('%Y-%m-%d'),
                'author': '自動修正ツール',
                'changes': 'カラム順序を推奨順序に自動修正'
            }
            data['revision_history'].append(new_version)
        
        # YAMLファイル書き込み
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        return {
            'table_name': table_name,
            'status': 'FIXED',
            'current_order': current_order,
            'recommended_order': recommended_order,
            'columns_count': len(columns)
        }
        
    except Exception as e:
        return {
            'table_name': 'UNKNOWN',
            'status': 'ERROR',
            'message': f'修正エラー: {str(e)}'
        }

def main():
    """メイン処理"""
    yaml_files = glob.glob('docs/design/database/table-details/テーブル詳細定義YAML_*.yaml')
    yaml_files = [f for f in yaml_files if 'TEMPLATE' not in f]
    yaml_files.sort()
    
    print(f"🔧 全テーブルカラム順序修正開始 (対象: {len(yaml_files)}テーブル)")
    print("=" * 80)
    
    results = []
    fixed_count = 0
    error_count = 0
    no_change_count = 0
    
    for i, yaml_file in enumerate(yaml_files, 1):
        table_name = os.path.basename(yaml_file).replace('テーブル詳細定義YAML_', '').replace('.yaml', '')
        print(f"\n📋 [{i:2d}/{len(yaml_files)}] {table_name}")
        
        result = fix_table_column_order(yaml_file, backup=True)
        results.append(result)
        
        if result['status'] == 'FIXED':
            fixed_count += 1
            print(f"    ✅ 修正完了 (カラム数: {result['columns_count']})")
            print(f"    📝 順序変更: {len(result['current_order'])}カラム")
        elif result['status'] == 'NO_CHANGE':
            no_change_count += 1
            print(f"    ⏭️  変更なし")
        elif result['status'] == 'ERROR':
            error_count += 1
            print(f"    ❌ エラー: {result['message']}")
    
    # 結果サマリー
    print(f"\n📈 修正結果サマリー:")
    print(f"  ✅ 修正完了: {fixed_count}テーブル")
    print(f"  ⏭️  変更なし: {no_change_count}テーブル")
    print(f"  ❌ エラー: {error_count}テーブル")
    
    # 修正されたテーブルリスト
    if fixed_count > 0:
        print(f"\n🔧 修正されたテーブル:")
        for result in results:
            if result['status'] == 'FIXED':
                print(f"  - {result['table_name']}")
    
    # エラーテーブル
    if error_count > 0:
        print(f"\n❌ エラーが発生したテーブル:")
        for result in results:
            if result['status'] == 'ERROR':
                print(f"  - {result['table_name']}: {result['message']}")
    
    print(f"\n✨ 修正完了!")
    
    # 次のステップの案内
    if fixed_count > 0:
        print(f"\n📋 次のステップ:")
        print(f"  1. 修正されたテーブルのDDL・定義書・サンプルデータを再生成")
        print(f"  2. 整合性チェック実行")
        print(f"  3. Git コミット")
        print(f"\n💡 再生成コマンド例:")
        print(f"  python3 docs/design/database/tools/generate_table_direct.py --table MST_Certification --verbose")
        print(f"  python3 docs/design/database/tools/database_consistency_checker/run_check.py --verbose")
    
    return error_count

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
