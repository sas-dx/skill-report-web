#!/usr/bin/env python3
"""
MST_Employeeテーブル限定での統一設計ツール機能テスト
"""

import sys
import os
import yaml
import json
from pathlib import Path
from datetime import datetime

# プロジェクトルートを追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "docs" / "tools"))

def test_yaml_validation():
    """YAML検証機能のテスト"""
    print("=== MST_Employee YAML検証テスト ===")
    
    yaml_file = project_root / "docs" / "design" / "database" / "table-details" / "テーブル詳細定義YAML_MST_Employee.yaml"
    
    if not yaml_file.exists():
        print(f"❌ YAMLファイルが見つかりません: {yaml_file}")
        return False
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        print(f"✅ YAML構文チェック: OK")
        
        # 必須セクションチェック
        required_sections = ['revision_history', 'overview', 'notes', 'rules']
        missing_sections = []
        
        for section in required_sections:
            if section not in data:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"❌ 必須セクション不足: {missing_sections}")
            return False
        else:
            print(f"✅ 必須セクションチェック: OK")
        
        # 内容チェック
        if len(data.get('overview', '').strip()) < 50:
            print(f"❌ overview文字数不足: {len(data.get('overview', '').strip())}文字")
            return False
        else:
            print(f"✅ overview文字数チェック: OK ({len(data.get('overview', '').strip())}文字)")
        
        if len(data.get('notes', [])) < 3:
            print(f"❌ notes項目数不足: {len(data.get('notes', []))}項目")
            return False
        else:
            print(f"✅ notes項目数チェック: OK ({len(data.get('notes', []))}項目)")
        
        if len(data.get('rules', [])) < 3:
            print(f"❌ rules項目数不足: {len(data.get('rules', []))}項目")
            return False
        else:
            print(f"✅ rules項目数チェック: OK ({len(data.get('rules', []))}項目)")
        
        # カラム定義チェック
        columns = data.get('columns', [])
        if not columns:
            print(f"❌ カラム定義なし")
            return False
        
        print(f"✅ カラム定義チェック: OK ({len(columns)}カラム)")
        
        # 主キーチェック
        primary_keys = [col for col in columns if col.get('name') == 'id']
        if not primary_keys:
            print(f"❌ 主キー(id)が見つかりません")
            return False
        else:
            print(f"✅ 主キーチェック: OK")
        
        # テナントIDチェック
        tenant_columns = [col for col in columns if col.get('name') == 'tenant_id']
        if not tenant_columns:
            print(f"❌ tenant_idカラムが見つかりません")
            return False
        else:
            print(f"✅ tenant_idチェック: OK")
        
        print(f"✅ MST_Employee YAML検証: 全てOK")
        return True
        
    except yaml.YAMLError as e:
        print(f"❌ YAML構文エラー: {e}")
        return False
    except Exception as e:
        print(f"❌ 検証エラー: {e}")
        return False

def test_file_existence():
    """関連ファイル存在チェック"""
    print("\n=== MST_Employee 関連ファイル存在チェック ===")
    
    base_path = project_root / "docs" / "design" / "database"
    
    files_to_check = [
        ("YAML詳細定義", "table-details/テーブル詳細定義YAML_MST_Employee.yaml"),
        ("テーブル定義書", "tables/テーブル定義書_MST_Employee_社員基本情報.md"),
        ("DDLファイル", "ddl/MST_Employee.sql"),
        ("サンプルデータ", "data/MST_Employee_sample_data.sql")
    ]
    
    all_exist = True
    for file_type, file_path in files_to_check:
        full_path = base_path / file_path
        if full_path.exists():
            print(f"✅ {file_type}: 存在")
        else:
            print(f"❌ {file_type}: 不存在 ({full_path})")
            all_exist = False
    
    return all_exist

def test_data_consistency():
    """データ整合性チェック"""
    print("\n=== MST_Employee データ整合性チェック ===")
    
    base_path = project_root / "docs" / "design" / "database"
    yaml_file = base_path / "table-details" / "テーブル詳細定義YAML_MST_Employee.yaml"
    
    try:
        with open(yaml_file, 'r', encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
        
        # テーブル名整合性
        table_name = yaml_data.get('table_name')
        if table_name != 'MST_Employee':
            print(f"❌ テーブル名不整合: {table_name}")
            return False
        else:
            print(f"✅ テーブル名整合性: OK")
        
        # カテゴリチェック
        category = yaml_data.get('category')
        if category != 'マスタ系':
            print(f"❌ カテゴリ不整合: {category}")
            return False
        else:
            print(f"✅ カテゴリ整合性: OK")
        
        # 外部キー整合性
        foreign_keys = yaml_data.get('foreign_keys', [])
        expected_fks = ['MST_Department', 'MST_Position', 'MST_JobType', 'MST_Employee']
        
        referenced_tables = [fk['references']['table'] for fk in foreign_keys]
        for expected_table in expected_fks:
            if expected_table in referenced_tables:
                print(f"✅ 外部キー参照: {expected_table} OK")
            else:
                print(f"⚠️  外部キー参照: {expected_table} 未設定")
        
        print(f"✅ MST_Employee データ整合性: OK")
        return True
        
    except Exception as e:
        print(f"❌ 整合性チェックエラー: {e}")
        return False

def generate_test_report():
    """テスト結果レポート生成"""
    print("\n=== MST_Employee テスト結果レポート生成 ===")
    
    report = {
        "test_target": "MST_Employee",
        "test_date": datetime.now().isoformat(),
        "test_results": {
            "yaml_validation": test_yaml_validation(),
            "file_existence": test_file_existence(),
            "data_consistency": test_data_consistency()
        }
    }
    
    # 総合評価
    all_passed = all(report["test_results"].values())
    report["overall_result"] = "PASS" if all_passed else "FAIL"
    
    # レポートファイル保存
    report_file = project_root / f"mst_employee_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ テストレポート生成: {report_file}")
        print(f"📊 総合結果: {report['overall_result']}")
        
        return report
        
    except Exception as e:
        print(f"❌ レポート生成エラー: {e}")
        return None

if __name__ == "__main__":
    print("🚀 MST_Employee統一設計ツール機能テスト開始")
    print("=" * 60)
    
    # テスト実行
    report = generate_test_report()
    
    print("\n" + "=" * 60)
    if report and report["overall_result"] == "PASS":
        print("🎉 MST_Employee統一設計ツール機能テスト: 全て成功")
        sys.exit(0)
    else:
        print("❌ MST_Employee統一設計ツール機能テスト: 一部失敗")
        sys.exit(1)
