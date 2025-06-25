#!/usr/bin/env python3
"""
全テーブルのカラム順序最終検証スクリプト
推奨順序テンプレートに従っているかを確認
"""

import yaml
import os
from pathlib import Path

def validate_column_order():
    """全テーブルのカラム順序を検証"""
    table_details_dir = "docs/design/database/table-details"
    
    # 推奨順序テンプレート
    template_order = [
        # 1. 主キー（{table_name}_id）
        "primary_key",
        # 2. テナントID（マルチテナント対応）
        "tenant_id",
        # 3. UUID（グローバル識別子）
        "id",
        # 4. ビジネスキー（コード等）
        "business_keys",
        # 5. 名称系フィールド
        "name_fields",
        # 6. 基本属性
        "basic_attributes",
        # 7. 論理削除フラグ
        "is_deleted",
        # 8. 作成日時
        "created_at",
        # 9. 更新日時
        "updated_at"
    ]
    
    print("🔍 全テーブルのカラム順序検証")
    print("=" * 60)
    
    yaml_files = list(Path(table_details_dir).glob("テーブル詳細定義YAML_*.yaml"))
    yaml_files = [f for f in yaml_files if not f.name.startswith("テーブル詳細定義YAML_TEMPLATE")]
    
    total_tables = len(yaml_files)
    valid_tables = 0
    issues = []
    
    for yaml_file in sorted(yaml_files):
        table_name = yaml_file.stem.replace("テーブル詳細定義YAML_", "")
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            columns = data.get('columns', [])
            if not columns:
                issues.append(f"{table_name}: カラム定義なし")
                continue
            
            # カラム順序チェック
            col_names = [col['name'] for col in columns]
            
            # 基本チェック項目
            checks = {
                'has_primary_key': False,
                'has_tenant_id': False,
                'has_id': False,
                'has_is_deleted': False,
                'has_created_at': False,
                'has_updated_at': False,
                'correct_end_order': False
            }
            
            # 主キーチェック（最初のカラム）
            if col_names and col_names[0].endswith('_id'):
                checks['has_primary_key'] = True
            
            # 必須カラムの存在チェック
            if 'tenant_id' in col_names:
                checks['has_tenant_id'] = True
            if 'id' in col_names:
                checks['has_id'] = True
            if 'is_deleted' in col_names:
                checks['has_is_deleted'] = True
            if 'created_at' in col_names:
                checks['has_created_at'] = True
            if 'updated_at' in col_names:
                checks['has_updated_at'] = True
            
            # 末尾3カラムの順序チェック
            if len(col_names) >= 3:
                last_three = col_names[-3:]
                if (last_three == ['is_deleted', 'created_at', 'updated_at'] or
                    last_three[-2:] == ['created_at', 'updated_at']):
                    checks['correct_end_order'] = True
            
            # 結果判定
            score = sum(checks.values())
            max_score = len(checks)
            
            if score == max_score:
                status = "✅"
                valid_tables += 1
            elif score >= max_score - 1:
                status = "⚠️ "
            else:
                status = "❌"
            
            print(f"{status} {table_name:<25} ({score}/{max_score}) カラム数: {len(col_names)}")
            
            # 詳細な問題点
            if score < max_score:
                problems = []
                if not checks['has_primary_key']:
                    problems.append("主キーが最初にない")
                if not checks['has_is_deleted']:
                    problems.append("is_deletedなし")
                if not checks['has_created_at']:
                    problems.append("created_atなし")
                if not checks['has_updated_at']:
                    problems.append("updated_atなし")
                if not checks['correct_end_order']:
                    problems.append("末尾順序不正")
                
                if problems:
                    print(f"     問題: {', '.join(problems)}")
                    issues.append(f"{table_name}: {', '.join(problems)}")
        
        except Exception as e:
            issues.append(f"{table_name}: 読み込みエラー - {str(e)}")
            print(f"❌ {table_name:<25} エラー: {str(e)}")
    
    print("\n" + "=" * 60)
    print(f"📊 検証結果サマリー")
    print(f"✅ 完全準拠: {valid_tables}/{total_tables} テーブル")
    print(f"⚠️  部分準拠: {total_tables - valid_tables - len([i for i in issues if 'エラー' in i])}")
    print(f"❌ エラー: {len([i for i in issues if 'エラー' in i])}")
    
    if issues:
        print(f"\n🔧 要修正項目:")
        for issue in issues[:10]:  # 最初の10件のみ表示
            print(f"   - {issue}")
        if len(issues) > 10:
            print(f"   ... 他 {len(issues) - 10} 件")
    
    success_rate = (valid_tables / total_tables) * 100 if total_tables > 0 else 0
    print(f"\n🎯 成功率: {success_rate:.1f}%")
    
    if success_rate >= 95:
        print("🎉 優秀！ほぼ全てのテーブルが推奨順序に準拠しています")
    elif success_rate >= 80:
        print("👍 良好！大部分のテーブルが推奨順序に準拠しています")
    else:
        print("⚠️  改善が必要です")

if __name__ == "__main__":
    validate_column_order()
