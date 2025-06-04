#!/usr/bin/env python3
"""
データベース整合性チェックツールのテストスクリプト
"""
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from database_consistency_checker.core.config import Config
from database_consistency_checker.core.models import CheckConfig
from database_consistency_checker.checkers.consistency_checker import ConsistencyChecker
from database_consistency_checker.reporters.console_reporter import ConsoleReporter


def test_column_parser():
    """カラムパーサーのテスト"""
    print("=== カラムパーサーテスト ===")
    
    from database_consistency_checker.parsers.column_parser import ColumnParser
    
    # DDLファイルのテスト
    ddl_path = Path("skill-report-web/docs/design/database/ddl/MST_Employee.sql")
    if ddl_path.exists():
        parser = ColumnParser()
        schema = parser.parse_ddl_file(ddl_path)
        
        if schema:
            print(f"✓ DDL解析成功: {schema.table_name}")
            print(f"  カラム数: {len(schema.columns)}")
            print(f"  外部キー数: {len(schema.foreign_keys)}")
            print(f"  インデックス数: {len(schema.indexes)}")
            
            # カラム詳細表示
            for col_name, col_def in list(schema.columns.items())[:3]:  # 最初の3つのみ
                print(f"  カラム: {col_name} - {col_def.get_full_type()}")
        else:
            print("✗ DDL解析失敗")
    else:
        print(f"✗ DDLファイルが見つかりません: {ddl_path}")


def test_consistency_checker():
    """整合性チェッカーのテスト"""
    print("\n=== 整合性チェッカーテスト ===")
    
    # 設定の作成
    base_dir = Path("skill-report-web/docs/design/database")
    config = Config(
        table_list_file=base_dir / "テーブル一覧.md",
        entity_relationships_file=base_dir / "entity_relationships.yaml",
        ddl_dir=base_dir / "ddl",
        table_details_dir=base_dir / "table-details",
        output_dir=base_dir / "tools" / "output"
    )
    
    check_config = CheckConfig(
        target_tables=["MST_Employee"],  # テスト対象を限定
        verbose=True
    )
    
    # チェッカーの実行
    checker = ConsistencyChecker(config, check_config)
    
    try:
        # 利用可能なチェック一覧を表示
        available_checks = checker.get_available_checks()
        print(f"利用可能なチェック: {', '.join(available_checks)}")
        
        # カラム整合性チェックのみ実行
        print("\n--- カラム整合性チェック実行 ---")
        report = checker.run_specific_checks(["column_consistency"])
        
        # 結果表示
        reporter = ConsoleReporter()
        reporter.generate_report(report)
        
        print(f"\n✓ チェック完了: {len(report.results)}件の結果")
        
    except Exception as e:
        print(f"✗ チェック実行エラー: {e}")
        import traceback
        traceback.print_exc()


def test_foreign_key_checker():
    """外部キーチェッカーのテスト"""
    print("\n=== 外部キーチェッカーテスト ===")
    
    from database_consistency_checker.checkers.foreign_key_checker import ForeignKeyChecker
    
    base_dir = Path("skill-report-web/docs/design/database")
    entity_yaml_path = base_dir / "entity_relationships.yaml"
    ddl_dir = base_dir / "ddl"
    yaml_details_dir = base_dir / "table-details"
    
    if entity_yaml_path.exists():
        checker = ForeignKeyChecker()
        
        try:
            results = checker.check_foreign_key_consistency(
                entity_yaml_path=entity_yaml_path,
                ddl_dir=ddl_dir,
                yaml_details_dir=yaml_details_dir
            )
            
            print(f"✓ 外部キーチェック完了: {len(results)}件の結果")
            
            # エラーと警告の数を表示
            errors = sum(1 for r in results if r.severity.value == "error")
            warnings = sum(1 for r in results if r.severity.value == "warning")
            print(f"  エラー: {errors}件, 警告: {warnings}件")
            
        except Exception as e:
            print(f"✗ 外部キーチェックエラー: {e}")
    else:
        print(f"✗ entity_relationships.yamlが見つかりません: {entity_yaml_path}")


def main():
    """メインテスト実行"""
    print("データベース整合性チェックツール - テスト実行")
    print("=" * 50)
    
    # 各テストを実行
    test_column_parser()
    test_consistency_checker()
    test_foreign_key_checker()
    
    print("\n" + "=" * 50)
    print("テスト完了")


if __name__ == "__main__":
    main()
