#!/usr/bin/env python3
"""
全テーブルのカラム順序を最終検証するスクリプト（修正版）
MST_Employeeの主キーは'id'（UUIDプライマリキー）
"""

import os
import yaml
from pathlib import Path

def get_expected_primary_key(table_name):
    """テーブル名に基づいて期待される主キー名を返す"""
    # 特別なケース
    if table_name == 'MST_Employee':
        return 'id'  # MST_Employeeは'id'がプライマリキー
    elif table_name == 'MST_Tenant':
        return 'id'  # MST_Tenantも'id'がプライマリキー
    elif table_name == 'MST_UserAuth':
        return 'id'  # MST_UserAuthも'id'がプライマリキー
    
    # 一般的なパターン
    table_base = table_name.lower().replace('mst_', '').replace('trn_', '').replace('his_', '').replace('sys_', '').replace('wrk_', '')
    return f"{table_base}_id"

def validate_column_order(file_path):
    """単一テーブルのカラム順序を検証"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        table_name = data.get('table_name', '')
        columns = data.get('columns', [])
        
        if not columns:
            return table_name, 0, 0, "カラム定義なし"
        
        column_names = [col['name'] for col in columns]
        total_columns = len(column_names)
        
        # 期待される主キー名を取得
        expected_pk = get_expected_primary_key(table_name)
        
        score = 0
        issues = []
        
        # 1. 主キーが最初にあるかチェック
        if column_names and column_names[0] == expected_pk:
            score += 1
        else:
            if expected_pk in column_names:
                issues.append(f"主キー({expected_pk})が最初にない")
            else:
                issues.append(f"主キー({expected_pk})が存在しない")
        
        # 2. tenant_idが2番目にあるかチェック（マルチテナント対応テーブルの場合）
        if len(column_names) > 1:
            if 'tenant_id' in column_names:
                if column_names[1] == 'tenant_id':
                    score += 1
                else:
                    issues.append("tenant_idが2番目にない")
            else:
                score += 1  # tenant_idがないテーブルは問題なし
        
        # 3. UUIDフィールド（id）の位置チェック
        if 'id' in column_names and table_name != 'MST_Employee':
            # MST_Employee以外で'id'がある場合の位置チェック
            id_index = column_names.index('id')
            if 'tenant_id' in column_names:
                expected_id_pos = 2  # tenant_idの次
            else:
                expected_id_pos = 1  # 主キーの次
            
            if id_index == expected_id_pos:
                score += 1
            else:
                issues.append(f"UUID(id)が{expected_id_pos + 1}番目にない")
        else:
            score += 1  # idがないか、MST_Employeeの場合は問題なし
        
        # 4. ビジネスキーの位置チェック
        business_keys = [col for col in column_names if col.endswith('_code') or col.endswith('_name') and not col.startswith('full_name')]
        if business_keys:
            # 最初のビジネスキーの位置をチェック
            first_bk = business_keys[0]
            bk_index = column_names.index(first_bk)
            expected_bk_pos = 1 if table_name == 'MST_Employee' else (3 if 'tenant_id' in column_names and 'id' in column_names else 2)
            
            if bk_index <= expected_bk_pos + 2:  # 多少の余裕を持たせる
                score += 1
            else:
                issues.append(f"ビジネスキー({first_bk})の位置が不適切")
        else:
            score += 1  # ビジネスキーがない場合は問題なし
        
        # 5. is_deletedが後ろから3番目にあるかチェック
        if 'is_deleted' in column_names:
            is_deleted_index = column_names.index('is_deleted')
            if is_deleted_index == total_columns - 3:
                score += 1
            else:
                issues.append("is_deletedが後ろから3番目にない")
        else:
            issues.append("is_deletedが存在しない")
        
        # 6. created_atが後ろから2番目にあるかチェック
        if 'created_at' in column_names:
            created_at_index = column_names.index('created_at')
            if created_at_index == total_columns - 2:
                score += 1
            else:
                issues.append("created_atが後ろから2番目にない")
        else:
            issues.append("created_atが存在しない")
        
        # 7. updated_atが最後にあるかチェック
        if 'updated_at' in column_names:
            updated_at_index = column_names.index('updated_at')
            if updated_at_index == total_columns - 1:
                score += 1
            else:
                issues.append("updated_atが最後にない")
        else:
            issues.append("updated_atが存在しない")
        
        return table_name, score, 7, "; ".join(issues) if issues else "OK"
        
    except Exception as e:
        return os.path.basename(file_path), 0, 7, f"エラー: {str(e)}"

def main():
    """メイン処理"""
    print("🔍 全テーブルのカラム順序検証（修正版）")
    print("=" * 60)
    
    table_details_dir = Path("docs/design/database/table-details")
    yaml_files = list(table_details_dir.glob("テーブル詳細定義YAML_*.yaml"))
    
    if not yaml_files:
        print("❌ YAMLファイルが見つかりません")
        return
    
    results = []
    perfect_count = 0
    partial_count = 0
    error_count = 0
    
    for yaml_file in sorted(yaml_files):
        table_name, score, max_score, issues = validate_column_order(yaml_file)
        results.append((table_name, score, max_score, issues))
        
        # 結果表示
        if score == max_score:
            status = "✅"
            perfect_count += 1
        elif score >= max_score * 0.7:
            status = "⚠️ "
            partial_count += 1
        else:
            status = "❌"
            error_count += 1
        
        # テーブル名を短縮表示
        short_name = table_name.replace("テーブル詳細定義YAML_", "").replace(".yaml", "")
        print(f"{status} {short_name:<25} ({score}/{max_score}) カラム数: {len(yaml.safe_load(open(yaml_file, 'r', encoding='utf-8')).get('columns', []))}")
        
        if issues != "OK":
            print(f"     問題: {issues}")
    
    print("\n" + "=" * 60)
    print("📊 検証結果サマリー")
    print(f"✅ 完全準拠: {perfect_count}/{len(results)} テーブル")
    if partial_count > 0:
        print(f"⚠️  部分準拠: {partial_count}")
    if error_count > 0:
        print(f"❌ エラー: {error_count}")
    
    # 要修正項目の表示
    issues_found = [r for r in results if r[2] != "OK" and r[1] < r[2]]
    if issues_found:
        print(f"\n🔧 要修正項目:")
        for table_name, score, max_score, issues in issues_found:
            short_name = table_name.replace("テーブル詳細定義YAML_", "").replace(".yaml", "")
            print(f"   - {short_name}: {issues}")
    
    success_rate = (perfect_count / len(results)) * 100
    print(f"\n🎯 成功率: {success_rate:.1f}%")
    
    if success_rate >= 90:
        print("🎉 素晴らしい！ほぼ全てのテーブルが推奨順序に準拠しています")
    elif success_rate >= 80:
        print("👍 良好！大部分のテーブルが推奨順序に準拠しています")
    else:
        print("⚠️  改善が必要です")

if __name__ == "__main__":
    main()
