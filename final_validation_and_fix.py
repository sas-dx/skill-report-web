#!/usr/bin/env python3
"""
全テーブルの最終検証と修正スクリプト
推奨カラム順序に従って全テーブルを統一
"""

import os
import yaml
import glob
from datetime import datetime

def get_recommended_order():
    """推奨カラム順序を返す"""
    return [
        # 1. 主キー（AUTO_INCREMENT）
        'id',
        # 2. テナントID（マルチテナント対応）
        'tenant_id', 
        # 3. ビジネスキー（コード等）
        'code', 'emp_no', 'skill_code', 'category_code', 'dept_code', 'position_code',
        'certification_code', 'grade_code', 'plan_code', 'project_code', 'training_code',
        'batch_id', 'job_id', 'notification_id', 'config_key',
        # 4. 名称系フィールド
        'name', 'skill_name', 'category_name', 'dept_name', 'position_name',
        'certification_name', 'grade_name', 'plan_name', 'project_name', 'training_name',
        'title', 'subject', 'message',
        # 5. 基本属性（その他すべて）
        # ... (アルファベット順)
        # n-2. 論理削除フラグ
        'is_deleted',
        # n-1. 作成日時
        'created_at',
        # n. 更新日時
        'updated_at'
    ]

def categorize_columns(columns):
    """カラムをカテゴリ別に分類"""
    recommended = get_recommended_order()
    
    # カラム名のリストを作成
    column_names = [col['name'] for col in columns]
    column_dict = {col['name']: col for col in columns}
    
    categorized = {
        'primary_key': [],
        'tenant_id': [],
        'business_keys': [],
        'name_fields': [],
        'basic_attributes': [],
        'end_fields': []
    }
    
    # 1. 主キー
    if 'id' in column_dict:
        categorized['primary_key'].append('id')
    
    # 2. テナントID
    if 'tenant_id' in column_dict:
        categorized['tenant_id'].append('tenant_id')
    
    # 3. ビジネスキー
    business_key_patterns = ['code', 'emp_no', 'skill_code', 'category_code', 'dept_code', 
                           'position_code', 'certification_code', 'grade_code', 'plan_code',
                           'project_code', 'training_code', 'batch_id', 'job_id', 
                           'notification_id', 'config_key']
    
    for pattern in business_key_patterns:
        if pattern in column_names:
            categorized['business_keys'].append(pattern)
    
    # 4. 名称系フィールド
    name_patterns = ['name', 'skill_name', 'category_name', 'dept_name', 'position_name',
                    'certification_name', 'grade_name', 'plan_name', 'project_name', 
                    'training_name', 'title', 'subject', 'message']
    
    for pattern in name_patterns:
        if pattern in column_names:
            categorized['name_fields'].append(pattern)
    
    # 6. 終了フィールド
    end_patterns = ['is_deleted', 'created_at', 'updated_at']
    for pattern in end_patterns:
        if pattern in column_names:
            categorized['end_fields'].append(pattern)
    
    # 5. 基本属性（その他すべて）
    used_columns = (categorized['primary_key'] + categorized['tenant_id'] + 
                   categorized['business_keys'] + categorized['name_fields'] + 
                   categorized['end_fields'])
    
    for col_name in sorted(column_names):
        if col_name not in used_columns:
            categorized['basic_attributes'].append(col_name)
    
    return categorized, column_dict

def fix_table_column_order(file_path):
    """テーブルのカラム順序を修正"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            return False, "columnsセクションが見つかりません"
        
        columns = data['columns']
        table_name = data.get('table_name', 'Unknown')
        
        # 現在のカラム順序を確認
        current_order = [col['name'] for col in columns]
        
        # カラムを分類
        categorized, column_dict = categorize_columns(columns)
        
        # 新しい順序でカラムを並び替え
        new_order = []
        
        # 順序通りに追加
        for category in ['primary_key', 'tenant_id', 'business_keys', 'name_fields', 'basic_attributes', 'end_fields']:
            for col_name in categorized[category]:
                if col_name in column_dict:
                    new_order.append(column_dict[col_name])
        
        # カラム順序を更新
        data['columns'] = new_order
        
        # revision_historyを更新
        if 'revision_history' not in data:
            data['revision_history'] = []
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        data['revision_history'].append({
            'version': f'FINAL.{timestamp}',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'author': '最終カラム順序統一ツール',
            'changes': '推奨カラム順序テンプレートに従って最終統一'
        })
        
        # YAML保存
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        new_column_order = [col['name'] for col in new_order]
        
        return True, f"修正完了: {current_order[:3]} -> {new_column_order[:3]}"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

def validate_and_fix_all_tables():
    """全テーブルの検証と修正"""
    table_dir = "docs/design/database/table-details"
    pattern = os.path.join(table_dir, "テーブル詳細定義YAML_*.yaml")
    files = glob.glob(pattern)
    
    if not files:
        print("❌ テーブル定義ファイルが見つかりません")
        return
    
    print(f"📋 {len(files)}個のテーブル定義ファイルを検証・修正します\n")
    
    success_count = 0
    error_count = 0
    
    for file_path in sorted(files):
        filename = os.path.basename(file_path)
        table_name = filename.replace('テーブル詳細定義YAML_', '').replace('.yaml', '')
        
        print(f"🔧 {table_name}を処理中...")
        
        success, message = fix_table_column_order(file_path)
        
        if success:
            print(f"  ✅ {message}")
            success_count += 1
        else:
            print(f"  ❌ {message}")
            error_count += 1
    
    print(f"\n📊 処理結果:")
    print(f"  ✅ 成功: {success_count}個")
    print(f"  ❌ エラー: {error_count}個")
    
    if error_count == 0:
        print("\n🎉 全テーブルのカラム順序統一が完了しました！")
    else:
        print(f"\n⚠️  {error_count}個のテーブルでエラーが発生しました")

def main():
    """メイン処理"""
    print("全テーブルの最終検証と修正を開始...")
    print("推奨カラム順序:")
    print("1. {table_name}_id (主キー)")
    print("2. tenant_id (テナントID)")
    print("3. {business_key} (ビジネスキー)")
    print("4. {name_fields} (名称系)")
    print("5. {basic_attributes} (基本属性)")
    print("n-2. is_deleted (論理削除)")
    print("n-1. created_at (作成日時)")
    print("n. updated_at (更新日時)")
    print()
    
    validate_and_fix_all_tables()

if __name__ == "__main__":
    main()
