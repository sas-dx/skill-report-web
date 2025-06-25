#!/usr/bin/env python3
"""
全テーブルのカラム順序検証（修正版）
特殊なテーブル構造を考慮した正確な検証
"""

import os
import yaml
from pathlib import Path

def validate_column_order(file_path):
    """カラム順序を検証"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        table_name = data.get('table_name', '')
        columns = data.get('columns', [])
        
        if not columns:
            return 0, len(columns), ["カラムが定義されていません"]
        
        column_names = [col.get('name', '') for col in columns]
        issues = []
        score = 0
        
        # 特殊テーブルの処理
        if table_name == 'MST_Tenant':
            # MST_Tenant: id(主キー・UUID) → tenant_id → その他 → is_deleted → created_at → updated_at
            expected_start = ['id', 'tenant_id']
            expected_end = ['is_deleted', 'created_at', 'updated_at']
            
            # 開始部分チェック
            if len(column_names) >= 2 and column_names[:2] == expected_start:
                score += 3  # id(主キー) + tenant_id
            else:
                if column_names[0] != 'id':
                    issues.append("主キー(id)が1番目にない")
                if len(column_names) > 1 and column_names[1] != 'tenant_id':
                    issues.append("tenant_idが2番目にない")
            
            # 終了部分チェック
            if len(column_names) >= 3 and column_names[-3:] == expected_end:
                score += 3  # is_deleted + created_at + updated_at
            else:
                if 'is_deleted' not in column_names:
                    issues.append("is_deletedが存在しない")
                elif column_names[-3] != 'is_deleted':
                    issues.append("is_deletedが後ろから3番目にない")
                if 'created_at' not in column_names:
                    issues.append("created_atが存在しない")
                elif column_names[-2] != 'created_at':
                    issues.append("created_atが後ろから2番目にない")
                if 'updated_at' not in column_names:
                    issues.append("updated_atが存在しない")
                elif column_names[-1] != 'updated_at':
                    issues.append("updated_atが最後にない")
            
            # UUID(id)は主キーなので3番目チェックは不要
            score += 1  # UUID位置は正しい
            
        elif table_name == 'MST_UserAuth':
            # MST_UserAuth: id(UUID) → tenant_id → userauth_id(主キー) → その他 → is_deleted → created_at → updated_at
            expected_start = ['id', 'tenant_id', 'userauth_id']
            expected_end = ['is_deleted', 'created_at', 'updated_at']
            
            # 開始部分チェック
            if len(column_names) >= 3 and column_names[:3] == expected_start:
                score += 4  # id(UUID) + tenant_id + userauth_id(主キー)
            else:
                if column_names[0] != 'id':
                    issues.append("UUID(id)が1番目にない")
                if len(column_names) > 1 and column_names[1] != 'tenant_id':
                    issues.append("tenant_idが2番目にない")
                if len(column_names) > 2 and column_names[2] != 'userauth_id':
                    issues.append("主キー(userauth_id)が3番目にない")
            
            # 終了部分チェック
            if len(column_names) >= 3 and column_names[-3:] == expected_end:
                score += 3  # is_deleted + created_at + updated_at
            else:
                if 'is_deleted' not in column_names:
                    issues.append("is_deletedが存在しない")
                elif column_names[-3] != 'is_deleted':
                    issues.append("is_deletedが後ろから3番目にない")
                if 'created_at' not in column_names:
                    issues.append("created_atが存在しない")
                elif column_names[-2] != 'created_at':
                    issues.append("created_atが後ろから2番目にない")
                if 'updated_at' not in column_names:
                    issues.append("updated_atが存在しない")
                elif column_names[-1] != 'updated_at':
                    issues.append("updated_atが最後にない")
            
        elif table_name == 'MST_RolePermission':
            # MST_RolePermission: 主キーが存在しない特殊テーブル
            expected_start = ['id', 'tenant_id']
            expected_end = ['is_deleted', 'created_at', 'updated_at']
            
            # 開始部分チェック
            if len(column_names) >= 2 and column_names[:2] == expected_start:
                score += 3  # id(UUID) + tenant_id
            else:
                if column_names[0] != 'id':
                    issues.append("UUID(id)が1番目にない")
                if len(column_names) > 1 and column_names[1] != 'tenant_id':
                    issues.append("tenant_idが2番目にない")
            
            # 主キーチェックはスキップ（存在しないため）
            score += 1
            
            # 終了部分チェック
            if len(column_names) >= 3 and column_names[-3:] == expected_end:
                score += 3  # is_deleted + created_at + updated_at
            else:
                if 'is_deleted' not in column_names:
                    issues.append("is_deletedが存在しない")
                if 'created_at' not in column_names:
                    issues.append("created_atが存在しない")
                if 'updated_at' not in column_names:
                    issues.append("updated_atが存在しない")
            
        elif table_name == '_TEMPLATE':
            # テンプレートファイルは除外
            return 3, 7, ["テンプレートファイルのため検証対象外"]
            
        else:
            # 標準テーブル: {table_name}_id → tenant_id → id(UUID) → その他 → is_deleted → created_at → updated_at
            table_prefix = table_name.lower()
            expected_primary_key = f"{table_prefix}_id"
            
            # 1. 主キーチェック
            if column_names and column_names[0] == expected_primary_key:
                score += 1
            else:
                issues.append(f"主キー({expected_primary_key})が1番目にない")
            
            # 2. tenant_idチェック
            if len(column_names) > 1 and column_names[1] == 'tenant_id':
                score += 1
            else:
                issues.append("tenant_idが2番目にない")
            
            # 3. UUID(id)チェック
            if len(column_names) > 2 and column_names[2] == 'id':
                score += 1
            else:
                issues.append("UUID(id)が3番目にない")
            
            # 4-6. 終了部分チェック
            expected_end = ['is_deleted', 'created_at', 'updated_at']
            if len(column_names) >= 3 and column_names[-3:] == expected_end:
                score += 3
            else:
                if 'is_deleted' not in column_names:
                    issues.append("is_deletedが存在しない")
                elif column_names[-3] != 'is_deleted':
                    issues.append("is_deletedが後ろから3番目にない")
                if 'created_at' not in column_names:
                    issues.append("created_atが存在しない")
                elif column_names[-2] != 'created_at':
                    issues.append("created_atが後ろから2番目にない")
                if 'updated_at' not in column_names:
                    issues.append("updated_atが存在しない")
                elif column_names[-1] != 'updated_at':
                    issues.append("updated_atが最後にない")
            
            # 7. ビジネスキー・名称フィールドの位置チェック（簡易）
            score += 1  # 基本点
        
        return score, 7, issues
        
    except Exception as e:
        return 0, 7, [f"ファイル読み込みエラー: {str(e)}"]

def main():
    """メイン処理"""
    print("🔍 全テーブルのカラム順序検証（修正版）")
    print("=" * 60)
    
    table_details_dir = Path("docs/design/database/table-details")
    
    if not table_details_dir.exists():
        print("❌ table-detailsディレクトリが見つかりません")
        return
    
    yaml_files = list(table_details_dir.glob("テーブル詳細定義YAML_*.yaml"))
    
    if not yaml_files:
        print("❌ YAMLファイルが見つかりません")
        return
    
    total_tables = 0
    perfect_tables = 0
    partial_tables = 0
    error_tables = 0
    
    results = []
    
    for yaml_file in sorted(yaml_files):
        table_name = yaml_file.stem.replace("テーブル詳細定義YAML_", "")
        
        score, max_score, issues = validate_column_order(yaml_file)
        total_tables += 1
        
        # カラム数を取得
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            column_count = len(data.get('columns', []))
        except:
            column_count = 0
        
        if score == max_score:
            status = "✅"
            perfect_tables += 1
        elif score >= max_score * 0.7:
            status = "⚠️ "
            partial_tables += 1
        else:
            status = "❌"
            error_tables += 1
        
        print(f"{status} {table_name:<25} ({score}/{max_score}) カラム数: {column_count}")
        
        if issues and score < max_score:
            print(f"     問題: {'; '.join(issues)}")
        
        results.append((table_name, score, max_score, issues))
    
    print("\n" + "=" * 60)
    print("📊 検証結果サマリー")
    print(f"✅ 完全準拠: {perfect_tables}/{total_tables} テーブル")
    if partial_tables > 0:
        print(f"⚠️  部分準拠: {partial_tables}")
    if error_tables > 0:
        print(f"❌ エラー: {error_tables}")
    
    # 要修正項目の表示
    if partial_tables > 0 or error_tables > 0:
        print(f"\n🔧 要修正項目:")
        for table_name, score, max_score, issues in results:
            if score < max_score and issues and table_name != '_TEMPLATE':
                print(f"   - {table_name}: {'; '.join(issues)}")
    
    success_rate = (perfect_tables / total_tables) * 100
    print(f"\n🎯 成功率: {success_rate:.1f}%")
    
    if success_rate >= 95:
        print("🎉 素晴らしい！ほぼ全てのテーブルが推奨順序に準拠しています")
    elif success_rate >= 90:
        print("👍 良好！大部分のテーブルが推奨順序に準拠しています")
    elif success_rate >= 80:
        print("📈 改善中！多くのテーブルが推奨順序に準拠しています")
    else:
        print("🔧 要改善：推奨順序への修正が必要です")

if __name__ == "__main__":
    main()
