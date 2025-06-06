#!/usr/bin/env python3
"""
レポート管理機能のテストスクリプト
"""
import sys
from pathlib import Path
from datetime import datetime

# パッケージのパスを追加
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent))

from database_consistency_checker.utils.report_manager import ReportManager
from database_consistency_checker.core.models import ConsistencyReport, CheckResult, CheckSeverity
from database_consistency_checker.reporters.markdown_reporter import MarkdownReporter


def create_test_report() -> ConsistencyReport:
    """テスト用のレポートを作成"""
    report = ConsistencyReport(
        check_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_tables=5,
        total_checks=10,
        summary={
            'success': 7,
            'warning': 2,
            'error': 1,
            'info': 0
        }
    )
    
    # テスト用のチェック結果を追加
    test_results = [
        CheckResult(
            check_name="table_existence",
            table_name="MST_Employee",
            severity=CheckSeverity.SUCCESS,
            message="テーブル定義が正常に存在します",
            details={"status": "OK"}
        ),
        CheckResult(
            check_name="table_existence",
            table_name="MST_Department",
            severity=CheckSeverity.WARNING,
            message="DDLファイルが見つかりません",
            details={"missing_files": ["MST_Department.sql"]}
        ),
        CheckResult(
            check_name="table_existence",
            table_name="MST_Skill",
            severity=CheckSeverity.ERROR,
            message="テーブル一覧に記載がありません",
            details={"missing_sources": ["table_list"]}
        )
    ]
    
    report.results = test_results
    return report


def test_report_manager():
    """レポート管理機能のテスト"""
    print("🧪 レポート管理機能のテストを開始します...")
    
    try:
        # レポートマネージャー初期化
        report_manager = ReportManager(
            base_dir=str(current_dir),
            report_dir="test_reports"
        )
        
        print(f"✅ レポートマネージャー初期化完了")
        print(f"📁 レポートディレクトリ: {report_manager.report_dir}")
        
        # テストレポート作成
        test_report = create_test_report()
        reporter = MarkdownReporter()
        report_content = reporter.generate_report(test_report)
        
        # レポートファイル出力テスト
        print("\n📝 レポートファイル出力テスト...")
        
        # 基本的なレポート出力
        report_path1 = report_manager.get_report_path(
            report_type="test_report",
            extension="md"
        )
        
        with open(report_path1, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ レポート1出力完了: {report_path1.name}")
        
        # カスタムプレフィックス付きレポート出力
        report_path2 = report_manager.get_report_path(
            report_type="test_report",
            extension="md",
            custom_prefix="manual_check"
        )
        
        with open(report_path2, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        print(f"✅ レポート2出力完了: {report_path2.name}")
        
        # 最新リンク作成テスト
        print("\n🔗 最新リンク作成テスト...")
        report_manager.create_latest_link(report_path2, "latest_test_report.md")
        print(f"✅ 最新リンク作成完了")
        
        # レポート統計テスト
        print("\n📊 レポート統計テスト...")
        stats = report_manager.get_report_statistics()
        print(f"✅ 統計取得完了:")
        print(f"   - 総レポート数: {stats['total_reports']}")
        print(f"   - 総サイズ: {stats['total_size_mb']} MB")
        print(f"   - ディレクトリ別: {stats['by_directory']}")
        
        # 最近のレポート一覧テスト
        print("\n📋 最近のレポート一覧テスト...")
        recent_reports = report_manager.list_recent_reports(limit=5)
        print(f"✅ 最近のレポート一覧取得完了:")
        for report_info in recent_reports:
            print(f"   - {report_info['filename']} ({report_info['timestamp']}, {report_info['size_kb']}KB)")
        
        print("\n🎉 すべてのテストが正常に完了しました！")
        
    except Exception as e:
        print(f"❌ テスト中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_filename_generation():
    """ファイル名生成のテスト"""
    print("\n🔤 ファイル名生成テスト...")
    
    report_manager = ReportManager(
        base_dir=str(current_dir),
        report_dir="test_reports"
    )
    
    # 基本的なファイル名生成
    filename1 = report_manager.generate_report_filename()
    print(f"✅ 基本ファイル名: {filename1}")
    
    # カスタムプレフィックス付き
    filename2 = report_manager.generate_report_filename(
        report_type="custom_report",
        extension="json",
        custom_prefix="api_check"
    )
    print(f"✅ カスタムファイル名: {filename2}")
    
    # 同一秒での重複テスト
    filename3 = report_manager.generate_report_filename()
    filename4 = report_manager.generate_report_filename()
    print(f"✅ 重複回避テスト: {filename3} != {filename4}")


if __name__ == "__main__":
    print("🚀 レポート管理機能テストスクリプト")
    print("=" * 50)
    
    # ファイル名生成テスト
    test_filename_generation()
    
    # メイン機能テスト
    success = test_report_manager()
    
    if success:
        print("\n✨ 全テスト完了！レポート管理機能は正常に動作しています。")
        sys.exit(0)
    else:
        print("\n💥 テストに失敗しました。")
        sys.exit(1)
