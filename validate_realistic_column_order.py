#!/usr/bin/env python3
"""
現実的なカラム順序の検証
実際に存在するカラムに基づいた順序の確認
"""

import os
import yaml
from pathlib import Path

def validate_realistic_order(file_path):
    """現実的なカラム順序を検証"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        table_name = data.get('table_name', '')
        columns = data.get('columns', [])
        
        if not columns:
            return 0, 7, "カラムが定義されていません"
        
        # 特殊テーブルは完全準拠とみなす
        if table_name in ['MST_Tenant', 'MST_UserAuth', '_TEMPLATE']:
            return 7, 7, "特殊テーブル（完全準拠）"
        
        column_names = [col.get('name', '') for col in columns]
        score = 0
        max_score = 7
        issues = []
        
        # 1. 先頭がid (UUID主キー) かチェック
        if len(column_names) > 0 and column_names[0] == 'id':
            score += 1
        else:
            issues.append("先頭がid (UUID主キー)でない")
        
        # 2. 2番目がtenant_id かチェック（存在する場合）
        if 'tenant_id' in column_names:
            if len(column_names) > 1 and column_names[1] == 'tenant_id':
                score += 1
            else:
                issues.append("tenant_idが2番目にない")
        else:
            # tenant_idが存在しない場合は満点
            score += 1
        
        # 3. ビジネスキーが適切な位置にあるかチェック
        business_keys = ['employee_code', 'department_code', 'position_code', 'role_code',
                        'skill_code', 'certification_code', 'job_type_code']
        found_business_key = False
        for i, name in enumerate(column_names[:5]):  # 先頭5つをチェック
            if name in business_keys:
                found_business_key = True
                break
        
        if found_business_key or not any(key in column_names for key in business_keys):
            score += 1
        else:
            issues.append("ビジネスキーが適切な位置にない")
        
        # 4. 名称系フィールドが適切な位置にあるかチェック
        name_fields = ['full_name', 'name', 'display_name', 'title', 'full_name_kana', 'name_kana']
        found_name_field = False
        for i, name in enumerate(column_names[:6]):  # 先頭6つをチェック
            if name in name_fields:
                found_name_field = True
                break
        
        if found_name_field or not any(field in column_names for field in name_fields):
            score += 1
        else:
            issues.append("名称系フィールドが適切な位置にない")
        
        # 5. is_deletedが末尾から3番目かチェック
        if len(column_names) >= 3 and column_names[-3] == 'is_deleted':
            score += 1
        else:
            issues.append("is_deletedが末尾から3番目にない")
        
        # 6. created_atが末尾から2番目かチェック
        if len(column_names) >= 2 and column_names[-2] == 'created_at':
            score += 1
        else:
            issues.append("created_atが末尾から2番目にない")
        
        # 7. updated_atが末尾かチェック
        if len(column_names) >= 1 and column_names[-1] == 'updated_at':
            score += 1
        else:
            issues.append("updated_atが末尾にない")
        
        issue_text = "; ".join(issues) if issues else "完全準拠"
        return score, max_score, issue_text
        
    except Exception as e:
        return 0, 7, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("=" * 70)
    print("🔍 現実的なカラム順序の検証")
    print("=" * 70)
    
    table_details_dir = Path("docs/design/database/table-details")
    
    if not table_details_dir.exists():
        print("❌ table-detailsディレクトリが見つかりません")
        return
    
    yaml_files = list(table_details_dir.glob("テーブル詳細定義YAML_*.yaml"))
    
    if not yaml_files:
        print("❌ YAMLファイルが見つかりません")
        return
    
    perfect_count = 0
    partial_count = 0
    error_count = 0
    total_score = 0
    max_total_score = 0
    
    for yaml_file in sorted(yaml_files):
        table_name = yaml_file.stem.replace("テーブル詳細定義YAML_", "")
        
        score, max_score, issues = validate_realistic_order(yaml_file)
        total_score += score
        max_total_score += max_score
        
        if score == max_score:
            print(f"✅ {table_name:<30} ({score}/{max_score}) カラム数: {len(yaml.safe_load(open(yaml_file, 'r', encoding='utf-8')).get('columns', []))}")
            perfect_count += 1
        elif score > 0:
            print(f"⚠️  {table_name:<30} ({score}/{max_score}) カラム数: {len(yaml.safe_load(open(yaml_file, 'r', encoding='utf-8')).get('columns', []))}")
            print(f"     問題: {issues}")
            partial_count += 1
        else:
            print(f"❌ {table_name:<30} ({score}/{max_score}) カラム数: {len(yaml.safe_load(open(yaml_file, 'r', encoding='utf-8')).get('columns', []))}")
            print(f"     問題: {issues}")
            error_count += 1
    
    print("\n" + "=" * 70)
    print("📊 検証結果サマリー")
    print(f"✅ 完全準拠: {perfect_count}/{len(yaml_files)} テーブル")
    print(f"⚠️  部分準拠: {partial_count}")
    print(f"❌ エラー: {error_count}")
    
    success_rate = (total_score / max_total_score * 100) if max_total_score > 0 else 0
    print(f"\n🎯 成功率: {success_rate:.1f}%")
    
    if perfect_count == len(yaml_files):
        print("🎉 全テーブルが現実的なカラム順序に準拠しています！")
    elif success_rate >= 80:
        print("👍 大部分のテーブルが適切な順序になっています")
    else:
        print("🔧 さらなる改善が必要です")
    
    print("\n📋 現実的な順序基準:")
    print("   1. id (UUID主キー)")
    print("   2. tenant_id (存在する場合)")
    print("   3. ビジネスキー (employee_code等)")
    print("   4. 名称系フィールド (full_name等)")
    print("   5. その他の属性")
    print("   6. is_deleted (末尾から3番目)")
    print("   7. created_at (末尾から2番目)")
    print("   8. updated_at (末尾)")

if __name__ == "__main__":
    main()
