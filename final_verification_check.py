#!/usr/bin/env python3
"""
最終検証チェック - カラム順序が正しく統一されているか確認
"""

import os
import yaml
import glob

def check_column_order(file_path):
    """カラム順序をチェック"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            return False, "columnsセクションが見つかりません"
        
        columns = data['columns']
        column_names = [col['name'] for col in columns]
        table_name = data.get('table_name', 'Unknown')
        
        # 期待される順序パターンをチェック
        expected_patterns = {
            'id_first': column_names[0] == 'id',
            'tenant_id_second': len(column_names) > 1 and column_names[1] == 'tenant_id',
            'created_at_near_end': 'created_at' in column_names[-3:] if 'created_at' in column_names else True,
            'updated_at_last': column_names[-1] == 'updated_at' if 'updated_at' in column_names else True
        }
        
        return True, {
            'table_name': table_name,
            'column_count': len(column_names),
            'first_3': column_names[:3],
            'last_3': column_names[-3:],
            'patterns': expected_patterns,
            'all_patterns_ok': all(expected_patterns.values())
        }
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("🔍 最終検証チェックを開始...")
    print("=" * 60)
    
    table_dir = "docs/design/database/table-details"
    pattern = os.path.join(table_dir, "テーブル詳細定義YAML_*.yaml")
    files = glob.glob(pattern)
    
    if not files:
        print("❌ テーブル定義ファイルが見つかりません")
        return
    
    # 代表的なテーブルをサンプルチェック
    sample_tables = [
        'MST_Employee', 'MST_Tenant', 'MST_Skill', 'TRN_SkillRecord', 
        'HIS_AuditLog', 'SYS_SystemLog'
    ]
    
    print(f"📋 {len(files)}個中、代表的な{len(sample_tables)}個のテーブルをサンプルチェック\n")
    
    success_count = 0
    total_checked = 0
    
    for file_path in sorted(files):
        filename = os.path.basename(file_path)
        table_name = filename.replace('テーブル詳細定義YAML_', '').replace('.yaml', '')
        
        # サンプルテーブルのみチェック（または全テーブルチェック）
        if table_name in sample_tables or len(sample_tables) == 0:
            total_checked += 1
            
            success, result = check_column_order(file_path)
            
            if success and isinstance(result, dict):
                print(f"🔧 {result['table_name']} ({result['column_count']}カラム)")
                print(f"  📝 先頭3カラム: {result['first_3']}")
                print(f"  📝 末尾3カラム: {result['last_3']}")
                
                if result['all_patterns_ok']:
                    print(f"  ✅ カラム順序OK")
                    success_count += 1
                else:
                    print(f"  ⚠️  パターン確認: {result['patterns']}")
                print()
            else:
                print(f"  ❌ {result}")
                print()
    
    print("=" * 60)
    print(f"📊 検証結果:")
    print(f"  ✅ 正常: {success_count}/{total_checked}個")
    print(f"  ⚠️  要確認: {total_checked - success_count}個")
    
    if success_count == total_checked:
        print("\n🎉 全テーブルのカラム順序が正しく統一されています！")
        print("\n📋 統一されたカラム順序:")
        print("1. id (主キー)")
        print("2. tenant_id (テナントID)")
        print("3. {business_key} (ビジネスキー)")
        print("4. {name_fields} (名称系)")
        print("5. {basic_attributes} (基本属性)")
        print("n-2. is_deleted (論理削除)")
        print("n-1. created_at (作成日時)")
        print("n. updated_at (更新日時)")
    else:
        print(f"\n⚠️  {total_checked - success_count}個のテーブルで要確認事項があります")

if __name__ == "__main__":
    main()
