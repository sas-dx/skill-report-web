#!/usr/bin/env python3
"""
カラム順序統一の結果を検証するスクリプト
"""

import os
import yaml

def validate_column_order(file_path):
    """カラム順序が正しいかチェック"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not data or 'columns' not in data:
            return False, "columnsセクションが見つかりません"
        
        table_name = data.get('table_name', '')
        if not table_name:
            return False, "table_nameが見つかりません"
        
        columns = data['columns']
        column_names = [col['name'] for col in columns]
        
        # 期待される順序をチェック
        issues = []
        
        # 1. 主キー（{table_name}_id）が最初にあるかチェック
        table_prefix = table_name.replace("MST_", "").replace("TRN_", "").replace("HIS_", "").replace("SYS_", "").replace("WRK_", "")
        expected_primary_key = f"{table_prefix.lower()}_id"
        
        if column_names and column_names[0] != expected_primary_key:
            # 主キーが存在するかチェック
            if expected_primary_key in column_names:
                issues.append(f"主キー '{expected_primary_key}' が最初の位置にありません（現在位置: {column_names.index(expected_primary_key) + 1}）")
        
        # 2. tenant_idが2番目にあるかチェック（存在する場合）
        if "tenant_id" in column_names:
            tenant_id_pos = column_names.index("tenant_id")
            if tenant_id_pos != 1:
                issues.append(f"tenant_id が2番目の位置にありません（現在位置: {tenant_id_pos + 1}）")
        
        # 3. 論理削除フラグが最後から3番目以内にあるかチェック
        if "is_deleted" in column_names:
            is_deleted_pos = column_names.index("is_deleted")
            if is_deleted_pos < len(column_names) - 3:
                issues.append(f"is_deleted が最後から3番目以内にありません（現在位置: {is_deleted_pos + 1}/{len(column_names)}）")
        
        # 4. created_atが最後から2番目にあるかチェック
        if "created_at" in column_names:
            created_at_pos = column_names.index("created_at")
            if created_at_pos != len(column_names) - 2:
                issues.append(f"created_at が最後から2番目にありません（現在位置: {created_at_pos + 1}/{len(column_names)}）")
        
        # 5. updated_atが最後にあるかチェック
        if "updated_at" in column_names:
            updated_at_pos = column_names.index("updated_at")
            if updated_at_pos != len(column_names) - 1:
                issues.append(f"updated_at が最後にありません（現在位置: {updated_at_pos + 1}/{len(column_names)}）")
        
        if issues:
            return False, "; ".join(issues)
        
        return True, f"カラム順序は正しいです（{len(column_names)}カラム）"
        
    except Exception as e:
        return False, f"エラー: {str(e)}"

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
    
    print(f"検証対象ファイル数: {len(yaml_files)}")
    print("=" * 80)
    
    success_count = 0
    error_count = 0
    
    for yaml_file in yaml_files:
        file_name = os.path.basename(yaml_file)
        is_valid, message = validate_column_order(yaml_file)
        
        if is_valid:
            print(f"✅ {file_name}: {message}")
            success_count += 1
        else:
            print(f"❌ {file_name}: {message}")
            error_count += 1
    
    print("\n" + "=" * 80)
    print(f"検証結果:")
    print(f"  ✅ 正常: {success_count} ファイル")
    print(f"  ❌ 問題: {error_count} ファイル")
    print(f"  📊 合計: {len(yaml_files)} ファイル")
    
    if error_count == 0:
        print("\n🎉 全てのファイルでカラム順序が正しく統一されています！")
    else:
        print(f"\n⚠️  {error_count} ファイルで問題が見つかりました。")

if __name__ == "__main__":
    main()
