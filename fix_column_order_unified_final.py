#!/usr/bin/env python3
"""
全テーブルのYAMLファイルでカラム順序を統一するスクリプト

統一カラム順序:
1. {table_name}_id    # 主キー（AUTO_INCREMENT）
2. tenant_id          # テナントID（マルチテナント対応）
3. id                 # UUID（グローバル識別子）
4. {business_key}     # ビジネスキー（コード等）
5. {name_fields}      # 名称系フィールド
6. {basic_attributes} # 基本属性
...
n-2. is_deleted       # 論理削除フラグ
n-1. created_at       # 作成日時
n.   updated_at       # 更新日時
"""

import os
import yaml
import shutil
from datetime import datetime

def backup_file(file_path):
    """ファイルのバックアップを作成"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup.{timestamp}"
    shutil.copy2(file_path, backup_path)
    print(f"バックアップ作成: {backup_path}")
    return backup_path

def get_column_priority(column_name, table_name):
    """カラムの優先順位を返す"""
    # 主キー（AUTO_INCREMENT）
    if column_name == f"{table_name.lower()}_id":
        return (1, column_name)
    
    # テナントID
    if column_name == "tenant_id":
        return (2, column_name)
    
    # UUID（グローバル識別子）
    if column_name == "id":
        return (3, column_name)
    
    # ビジネスキー（コード系）
    code_patterns = ["_code", "_key", "_no", "employee_code", "skill_code", "role_code", 
                     "department_code", "position_code", "certification_code", "category_code",
                     "job_type_code", "grade_code", "program_code", "template_code"]
    if any(column_name.endswith(pattern) for pattern in code_patterns):
        return (4, column_name)
    
    # 名称系フィールド
    name_patterns = ["name", "title", "label", "display_name", "full_name", "short_name"]
    if any(pattern in column_name for pattern in name_patterns):
        return (5, column_name)
    
    # 論理削除フラグ（最後から2番目）
    if column_name == "is_deleted":
        return (998, column_name)
    
    # 作成日時（最後から1番目）
    if column_name == "created_at":
        return (999, column_name)
    
    # 更新日時（最後）
    if column_name == "updated_at":
        return (1000, column_name)
    
    # その他の基本属性
    return (100, column_name)

def reorder_columns(columns, table_name):
    """カラムを指定された順序で並び替え"""
    # テーブル名からプレフィックスを抽出
    table_prefix = table_name.replace("MST_", "").replace("TRN_", "").replace("HIS_", "").replace("SYS_", "").replace("WRK_", "")
    
    # カラムを優先順位でソート
    sorted_columns = sorted(columns, key=lambda col: get_column_priority(col['name'], table_prefix))
    
    return sorted_columns

def fix_yaml_file(file_path):
    """YAMLファイルのカラム順序を修正"""
    try:
        print(f"\n処理中: {file_path}")
        
        # バックアップ作成
        backup_file(file_path)
        
        # YAMLファイル読み込み
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            print(f"  スキップ: columnsセクションが見つかりません")
            return False
        
        # テーブル名取得
        table_name = data.get('table_name', '')
        if not table_name:
            print(f"  エラー: table_nameが見つかりません")
            return False
        
        # カラム順序を修正
        original_columns = data['columns']
        reordered_columns = reorder_columns(original_columns, table_name)
        
        # 変更があるかチェック
        if original_columns == reordered_columns:
            print(f"  変更なし: カラム順序は既に正しいです")
            return True
        
        # カラム順序を更新
        data['columns'] = reordered_columns
        
        # YAMLファイル書き込み
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        print(f"  完了: カラム順序を修正しました")
        
        # 修正内容を表示
        print(f"  カラム順序:")
        for i, col in enumerate(reordered_columns, 1):
            print(f"    {i:2d}. {col['name']}")
        
        return True
        
    except Exception as e:
        print(f"  エラー: {str(e)}")
        return False

def main():
    """メイン処理"""
    yaml_dir = "docs/design/database/table-details"
    
    if not os.path.exists(yaml_dir):
        print(f"エラー: ディレクトリが見つかりません: {yaml_dir}")
        return
    
    # YAMLファイル一覧取得（バックアップファイルを除外）
    yaml_files = []
    for file in os.listdir(yaml_dir):
        if file.endswith('.yaml') and not file.endswith('.backup') and not 'backup' in file:
            if file.startswith('テーブル詳細定義YAML_') and not file == 'テーブル詳細定義YAML_TEMPLATE.yaml':
                yaml_files.append(os.path.join(yaml_dir, file))
    
    yaml_files.sort()
    
    print(f"対象ファイル数: {len(yaml_files)}")
    print("=" * 80)
    
    success_count = 0
    error_count = 0
    
    for yaml_file in yaml_files:
        if fix_yaml_file(yaml_file):
            success_count += 1
        else:
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"処理完了:")
    print(f"  成功: {success_count} ファイル")
    print(f"  エラー: {error_count} ファイル")
    print(f"  合計: {len(yaml_files)} ファイル")

if __name__ == "__main__":
    main()
