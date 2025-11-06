#!/usr/bin/env python3
"""
統一設計ツール - 汎用データベーステーブル検証スクリプト
MST_Employeeテストをベースに汎用化
"""

import sys
import os
import yaml
import json
from pathlib import Path
from datetime import datetime
import argparse

# プロジェクトルートを追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "docs" / "tools"))

class DatabaseTableValidator:
    """データベーステーブル検証クラス"""
    
    def __init__(self, table_name):
        self.table_name = table_name
        self.project_root = project_root
        self.base_path = self.project_root / "docs" / "design" / "database"
        self.yaml_file = self.base_path / "table-details" / f"テーブル詳細定義YAML_{table_name}.yaml"
        self.test_results = {}
        
    def test_yaml_validation(self):
        """YAML検証機能のテスト"""
        print(f"=== {self.table_name} YAML検証テスト ===")
        
        if not self.yaml_file.exists():
            print(f"❌ YAMLファイルが見つかりません: {self.yaml_file}")
            return False
        
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
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
            overview_length = len(data.get('overview', '').strip())
            if overview_length < 50:
                print(f"❌ overview文字数不足: {overview_length}文字")
                return False
            else:
                print(f"✅ overview文字数チェック: OK ({overview_length}文字)")
            
            notes_count = len(data.get('notes', []))
            if notes_count < 3:
                print(f"❌ notes項目数不足: {notes_count}項目")
                return False
            else:
                print(f"✅ notes項目数チェック: OK ({notes_count}項目)")
            
            rules_count = len(data.get('rules', []))
            if rules_count < 3:
                print(f"❌ rules項目数不足: {rules_count}項目")
                return False
            else:
                print(f"✅ rules項目数チェック: OK ({rules_count}項目)")
            
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
            
            # テナントIDチェック（マルチテナント対応テーブルの場合）
            tenant_columns = [col for col in columns if col.get('name') == 'tenant_id']
            if tenant_columns:
                print(f"✅ tenant_idチェック: OK（マルチテナント対応）")
            else:
                print(f"⚠️  tenant_idチェック: 未設定（シングルテナント）")
            
            # 品質スコア計算
            quality_score = self._calculate_quality_score(data)
            print(f"📊 品質スコア: {quality_score}/100")
            
            print(f"✅ {self.table_name} YAML検証: 全てOK")
            return True
            
        except yaml.YAMLError as e:
            print(f"❌ YAML構文エラー: {e}")
            return False
        except Exception as e:
            print(f"❌ 検証エラー: {e}")
            return False

    def test_file_existence(self):
        """関連ファイル存在チェック"""
        print(f"\n=== {self.table_name} 関連ファイル存在チェック ===")
        
        # テーブル名から論理名を推定（簡易版）
        logical_name_map = {
            'MST_Employee': '社員基本情報',
            'MST_Department': '部署マスタ',
            'MST_Position': '役職マスタ',
            'MST_JobType': '職種マスタ',
            'MST_Skill': 'スキルマスタ',
            'MST_SkillCategory': 'スキルカテゴリマスタ'
        }
        logical_name = logical_name_map.get(self.table_name, 'テーブル')
        
        files_to_check = [
            ("YAML詳細定義", f"table-details/テーブル詳細定義YAML_{self.table_name}.yaml"),
            ("テーブル定義書", f"tables/テーブル定義書_{self.table_name}_{logical_name}.md"),
            ("DDLファイル", f"ddl/{self.table_name}.sql"),
            ("サンプルデータ", f"data/{self.table_name}_sample_data.sql")
        ]
        
        all_exist = True
        existing_files = 0
        for file_type, file_path in files_to_check:
            full_path = self.base_path / file_path
            if full_path.exists():
                print(f"✅ {file_type}: 存在")
                existing_files += 1
            else:
                print(f"❌ {file_type}: 不存在 ({full_path})")
                all_exist = False
        
        print(f"📊 ファイル存在率: {existing_files}/{len(files_to_check)} ({existing_files/len(files_to_check)*100:.1f}%)")
        return all_exist

    def test_data_consistency(self):
        """データ整合性チェック"""
        print(f"\n=== {self.table_name} データ整合性チェック ===")
        
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            
            # テーブル名整合性
            table_name = yaml_data.get('table_name')
            if table_name != self.table_name:
                print(f"❌ テーブル名不整合: {table_name}")
                return False
            else:
                print(f"✅ テーブル名整合性: OK")
            
            # カテゴリチェック
            category = yaml_data.get('category')
            expected_categories = ['マスタ系', 'トランザクション系', '履歴系', 'システム系', 'ワーク系']
            if category in expected_categories:
                print(f"✅ カテゴリ整合性: OK ({category})")
            else:
                print(f"❌ カテゴリ不整合: {category}")
                return False
            
            # 外部キー整合性
            foreign_keys = yaml_data.get('foreign_keys', [])
            if foreign_keys:
                referenced_tables = [fk['references']['table'] for fk in foreign_keys]
                print(f"✅ 外部キー参照: {len(referenced_tables)}個のテーブル参照")
                for table in referenced_tables:
                    print(f"  - {table}")
            else:
                print(f"⚠️  外部キー参照: なし")
            
            # 要求仕様ID整合性
            requirement_id = yaml_data.get('requirement_id')
            if requirement_id:
                print(f"✅ 要求仕様ID: {requirement_id}")
            else:
                print(f"⚠️  要求仕様ID: 未設定")
            
            print(f"✅ {self.table_name} データ整合性: OK")
            return True
            
        except Exception as e:
            print(f"❌ 整合性チェックエラー: {e}")
            return False

    def _calculate_quality_score(self, data):
        """品質スコア計算（100点満点）"""
        score = 0
        
        # 必須セクション存在（40点）
        required_sections = ['revision_history', 'overview', 'notes', 'rules']
        for section in required_sections:
            if section in data:
                score += 10
        
        # 内容品質（30点）
        if len(data.get('overview', '').strip()) >= 50:
            score += 10
        if len(data.get('notes', [])) >= 3:
            score += 10
        if len(data.get('rules', [])) >= 3:
            score += 10
        
        # カラム定義品質（20点）
        columns = data.get('columns', [])
        if columns:
            score += 10
            # 主キー存在
            if any(col.get('name') == 'id' for col in columns):
                score += 5
            # 適切なカラム数（5個以上）
            if len(columns) >= 5:
                score += 5
        
        # 外部キー・インデックス（10点）
        if data.get('foreign_keys'):
            score += 5
        if data.get('indexes'):
            score += 5
        
        return min(score, 100)

    def generate_test_report(self):
        """テスト結果レポート生成"""
        print(f"\n=== {self.table_name} テスト結果レポート生成 ===")
        
        yaml_result = self.test_yaml_validation()
        file_result = self.test_file_existence()
        consistency_result = self.test_data_consistency()
        
        report = {
            "test_target": self.table_name,
            "test_date": datetime.now().isoformat(),
            "test_results": {
                "yaml_validation": yaml_result,
                "file_existence": file_result,
                "data_consistency": consistency_result
            }
        }
        
        # 総合評価
        all_passed = all(report["test_results"].values())
        report["overall_result"] = "PASS" if all_passed else "FAIL"
        
        # レポートファイル保存
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = self.project_root / f"{self.table_name.lower()}_test_report_{timestamp}.json"
        
        try:
            with open(report_file, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"✅ テストレポート生成: {report_file}")
            print(f"📊 総合結果: {report['overall_result']}")
            
            return report
            
        except Exception as e:
            print(f"❌ レポート生成エラー: {e}")
            return None

def test_multiple_tables(table_names):
    """複数テーブルの一括テスト"""
    print("🚀 複数テーブル一括テスト開始")
    print("=" * 80)
    
    all_reports = []
    passed_count = 0
    
    for table_name in table_names:
        print(f"\n{'='*20} {table_name} テスト開始 {'='*20}")
        
        validator = DatabaseTableValidator(table_name)
        report = validator.generate_test_report()
        
        if report:
            all_reports.append(report)
            if report["overall_result"] == "PASS":
                passed_count += 1
        
        print(f"{'='*20} {table_name} テスト完了 {'='*20}")
    
    # 総合レポート生成
    summary_report = {
        "test_suite": "Multiple Tables Validation",
        "test_date": datetime.now().isoformat(),
        "total_tables": len(table_names),
        "passed_tables": passed_count,
        "failed_tables": len(table_names) - passed_count,
        "pass_rate": f"{passed_count/len(table_names)*100:.1f}%",
        "individual_results": all_reports
    }
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    summary_file = project_root / f"database_validation_summary_{timestamp}.json"
    
    try:
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_report, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎉 総合テスト完了")
        print(f"📊 合格率: {summary_report['pass_rate']}")
        print(f"📄 総合レポート: {summary_file}")
        
    except Exception as e:
        print(f"❌ 総合レポート生成エラー: {e}")
    
    return summary_report

def main():
    parser = argparse.ArgumentParser(description='統一設計ツール - データベーステーブル検証')
    parser.add_argument('--table', type=str, help='単一テーブル名')
    parser.add_argument('--phase1', action='store_true', help='Phase1テーブル群をテスト')
    parser.add_argument('--all', action='store_true', help='全テーブルをテスト')
    parser.add_argument('--tables', nargs='+', help='複数テーブル名を指定')
    
    args = parser.parse_args()
    
    if args.table:
        # 単一テーブルテスト
        print(f"🚀 {args.table} 統一設計ツール機能テスト開始")
        print("=" * 60)
        
        validator = DatabaseTableValidator(args.table)
        report = validator.generate_test_report()
        
        print("\n" + "=" * 60)
        if report and report["overall_result"] == "PASS":
            print(f"🎉 {args.table} 統一設計ツール機能テスト: 成功")
            sys.exit(0)
        else:
            print(f"❌ {args.table} 統一設計ツール機能テスト: 失敗")
            sys.exit(1)
    
    elif args.phase1:
        # Phase1テーブル群テスト
        phase1_tables = [
            'MST_Department',
            'MST_Position', 
            'MST_JobType',
            'MST_Skill',
            'MST_SkillCategory'
        ]
        
        summary = test_multiple_tables(phase1_tables)
        
        if summary and summary['failed_tables'] == 0:
            print(f"🎉 Phase1テーブル群テスト: 全て成功")
            sys.exit(0)
        else:
            print(f"❌ Phase1テーブル群テスト: 一部失敗")
            sys.exit(1)
    
    elif args.tables:
        # 指定テーブル群テスト
        summary = test_multiple_tables(args.tables)
        
        if summary and summary['failed_tables'] == 0:
            print(f"🎉 指定テーブル群テスト: 全て成功")
            sys.exit(0)
        else:
            print(f"❌ 指定テーブル群テスト: 一部失敗")
            sys.exit(1)
    
    else:
        print("使用方法:")
        print("  python test_database_validation_universal.py --table MST_Employee")
        print("  python test_database_validation_universal.py --phase1")
        print("  python test_database_validation_universal.py --tables MST_Employee MST_Department")
        sys.exit(1)

if __name__ == "__main__":
    main()
