#!/usr/bin/env python3
"""
全テーブルのカラム順序をチェックし、推奨順序との差異を特定するスクリプト
"""

import yaml
import os
import glob
from typing import List, Dict, Any

def get_recommended_order() -> List[str]:
    """推奨カラム順序のパターンを定義"""
    return [
        # 1. 主キー
        'id',
        # 2. ビジネスキー（各テーブル固有）
        '_code', '_number', '_key',
        # 3. 基本情報
        'name', 'title', 'description', 'logical_name',
        # 4. 関連ID（外部キー）
        '_id',
        # 5. ステータス・フラグ
        'status', 'type', 'category', 'level', 'grade',
        # 6. その他のデータ
        'value', 'amount', 'count', 'date', 'time',
        # 7. システム項目（最後）
        'is_active', 'is_deleted', 'created_at', 'updated_at'
    ]

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

def check_table_column_order(yaml_file: str) -> Dict[str, Any]:
    """テーブルのカラム順序をチェック"""
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        table_name = data.get('table_name', 'UNKNOWN')
        columns = data.get('columns', [])
        
        if not columns:
            return {
                'table_name': table_name,
                'file': yaml_file,
                'status': 'ERROR',
                'message': 'カラム定義が見つかりません'
            }
        
        # 現在の順序
        current_order = [col['name'] for col in columns]
        
        # 推奨順序
        recommended_columns = get_recommended_column_order(columns)
        recommended_order = [col['name'] for col in recommended_columns]
        
        # 順序が一致するかチェック
        is_correct_order = current_order == recommended_order
        
        result = {
            'table_name': table_name,
            'file': yaml_file,
            'status': 'OK' if is_correct_order else 'NEEDS_FIX',
            'current_order': current_order,
            'recommended_order': recommended_order,
            'columns_count': len(columns)
        }
        
        if not is_correct_order:
            # 差異の詳細
            differences = []
            for i, (current, recommended) in enumerate(zip(current_order, recommended_order)):
                if current != recommended:
                    differences.append({
                        'position': i,
                        'current': current,
                        'recommended': recommended
                    })
            result['differences'] = differences
        
        return result
        
    except Exception as e:
        return {
            'table_name': 'UNKNOWN',
            'file': yaml_file,
            'status': 'ERROR',
            'message': f'ファイル読み込みエラー: {str(e)}'
        }

def main():
    """メイン処理"""
    yaml_files = glob.glob('docs/design/database/table-details/テーブル詳細定義YAML_*.yaml')
    yaml_files = [f for f in yaml_files if 'TEMPLATE' not in f]
    yaml_files.sort()
    
    print(f"📊 全テーブルカラム順序チェック開始 (対象: {len(yaml_files)}テーブル)")
    print("=" * 80)
    
    results = []
    needs_fix = []
    errors = []
    
    for yaml_file in yaml_files:
        result = check_table_column_order(yaml_file)
        results.append(result)
        
        if result['status'] == 'NEEDS_FIX':
            needs_fix.append(result)
        elif result['status'] == 'ERROR':
            errors.append(result)
    
    # 結果サマリー
    print(f"\n📈 チェック結果サマリー:")
    print(f"  ✅ 正常: {len([r for r in results if r['status'] == 'OK'])}テーブル")
    print(f"  🔧 修正必要: {len(needs_fix)}テーブル")
    print(f"  ❌ エラー: {len(errors)}テーブル")
    
    # 修正が必要なテーブル詳細
    if needs_fix:
        print(f"\n🔧 修正が必要なテーブル:")
        for result in needs_fix:
            print(f"\n  📋 {result['table_name']}")
            print(f"     ファイル: {result['file']}")
            print(f"     カラム数: {result['columns_count']}")
            
            if 'differences' in result:
                print(f"     差異数: {len(result['differences'])}")
                for diff in result['differences'][:3]:  # 最初の3つだけ表示
                    print(f"       位置{diff['position']}: {diff['current']} → {diff['recommended']}")
                if len(result['differences']) > 3:
                    print(f"       ... 他{len(result['differences']) - 3}件")
    
    # エラーテーブル
    if errors:
        print(f"\n❌ エラーが発生したテーブル:")
        for result in errors:
            print(f"  📋 {result['table_name']}: {result['message']}")
    
    # 修正対象テーブルリスト出力
    if needs_fix:
        print(f"\n📝 修正対象テーブルリスト:")
        for result in needs_fix:
            print(f"  - {result['table_name']}")
    
    print(f"\n✨ チェック完了!")
    return len(needs_fix)

if __name__ == '__main__':
    exit_code = main()
    exit(exit_code)
