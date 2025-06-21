#!/usr/bin/env python3
"""
データベース設計ツール統合テストスイート実行スクリプト

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-21
実装者: AI Assistant

全テストスイートの統合実行：
- ユニットテスト
- 統合テスト
- パフォーマンステスト
- テストレポート生成
"""

import sys
import unittest
import time
from pathlib import Path
from typing import List, Dict, Any
import json

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# テストモジュールのインポート
try:
    from tests.unit.consistency_checker.test_consistency_checks import *
    from tests.unit.shared.test_shared_components import *
    from tests.integration.test_tool_integration import *
    from tests.performance.test_performance import *
except ImportError as e:
    print(f"警告: 一部のテストモジュールをインポートできませんでした: {e}")


class TestSuiteRunner:
    """テストスイート実行管理クラス"""
    
    def __init__(self):
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self) -> Dict[str, Any]:
        """全テストスイートを実行"""
        print("=" * 80)
        print("データベース設計ツール統合テストスイート実行開始")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # テストスイート定義
        test_suites = [
            ('ユニットテスト - 整合性チェック', self._run_consistency_checker_tests),
            ('ユニットテスト - 共有コンポーネント', self._run_shared_components_tests),
            ('統合テスト', self._run_integration_tests),
            ('パフォーマンステスト', self._run_performance_tests)
        ]
        
        # 各テストスイートを実行
        for suite_name, test_func in test_suites:
            print(f"\n{'-' * 60}")
            print(f"実行中: {suite_name}")
            print(f"{'-' * 60}")
            
            try:
                result = test_func()
                self.results[suite_name] = result
                print(f"✅ {suite_name}: 完了")
            except Exception as e:
                print(f"❌ {suite_name}: エラー - {str(e)}")
                self.results[suite_name] = {
                    'status': 'error',
                    'error': str(e),
                    'tests_run': 0,
                    'failures': 1,
                    'errors': 1
                }
        
        self.end_time = time.time()
        
        # 結果サマリー出力
        self._print_summary()
        
        # レポート生成
        self._generate_report()
        
        return self.results
    
    def _run_consistency_checker_tests(self) -> Dict[str, Any]:
        """整合性チェックテスト実行"""
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # テストクラスを追加
        test_classes = [
            'TestConsistencyChecker',
            'TestTableExistenceChecker',
            'TestColumnConsistencyChecker',
            'TestForeignKeyChecker',
            'TestNamingConventionChecker',
            'TestOrphanedFileChecker'
        ]
        
        for class_name in test_classes:
            try:
                test_class = globals().get(class_name)
                if test_class:
                    suite.addTests(loader.loadTestsFromTestCase(test_class))
            except Exception as e:
                print(f"警告: {class_name} をロードできませんでした: {e}")
        
        # テスト実行
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        return {
            'status': 'success' if result.wasSuccessful() else 'failure',
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0
        }
    
    def _run_shared_components_tests(self) -> Dict[str, Any]:
        """共有コンポーネントテスト実行"""
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # テストクラスを追加
        test_classes = [
            'TestDatabaseToolsConfig',
            'TestLogger',
            'TestYAMLParserAdvanced',
            'TestDDLParserAdvanced',
            'TestFilesystemAdapter',
            'TestDataTransformAdapter',
            'TestFileManager',
            'TestErrorHandlingIntegration'
        ]
        
        for class_name in test_classes:
            try:
                test_class = globals().get(class_name)
                if test_class:
                    suite.addTests(loader.loadTestsFromTestCase(test_class))
            except Exception as e:
                print(f"警告: {class_name} をロードできませんでした: {e}")
        
        # テスト実行
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        return {
            'status': 'success' if result.wasSuccessful() else 'failure',
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0
        }
    
    def _run_integration_tests(self) -> Dict[str, Any]:
        """統合テスト実行"""
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # 統合テストクラスを追加
        test_classes = [
            'TestToolIntegration',
            'TestEndToEndWorkflow',
            'TestCrossToolConsistency'
        ]
        
        for class_name in test_classes:
            try:
                test_class = globals().get(class_name)
                if test_class:
                    suite.addTests(loader.loadTestsFromTestCase(test_class))
            except Exception as e:
                print(f"警告: {class_name} をロードできませんでした: {e}")
        
        # テスト実行
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        return {
            'status': 'success' if result.wasSuccessful() else 'failure',
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0
        }
    
    def _run_performance_tests(self) -> Dict[str, Any]:
        """パフォーマンステスト実行"""
        try:
            import psutil
            psutil_available = True
        except ImportError:
            psutil_available = False
            print("警告: psutil が利用できないため、パフォーマンステストをスキップします")
        
        if not psutil_available:
            return {
                'status': 'skipped',
                'tests_run': 0,
                'failures': 0,
                'errors': 0,
                'skipped': 1,
                'reason': 'psutil not available'
            }
        
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        # パフォーマンステストクラスを追加
        test_classes = [
            'TestTableGenerationPerformance',
            'TestConsistencyCheckPerformance'
        ]
        
        for class_name in test_classes:
            try:
                test_class = globals().get(class_name)
                if test_class:
                    suite.addTests(loader.loadTestsFromTestCase(test_class))
            except Exception as e:
                print(f"警告: {class_name} をロードできませんでした: {e}")
        
        # テスト実行
        runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
        result = runner.run(suite)
        
        return {
            'status': 'success' if result.wasSuccessful() else 'failure',
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0
        }
    
    def _print_summary(self):
        """テスト結果サマリー出力"""
        print("\n" + "=" * 80)
        print("テスト実行結果サマリー")
        print("=" * 80)
        
        total_tests = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        
        for suite_name, result in self.results.items():
            status_icon = "✅" if result['status'] == 'success' else "❌" if result['status'] == 'error' else "⏭️"
            print(f"{status_icon} {suite_name}:")
            print(f"    実行: {result['tests_run']}, 失敗: {result['failures']}, エラー: {result['errors']}, スキップ: {result.get('skipped', 0)}")
            
            total_tests += result['tests_run']
            total_failures += result['failures']
            total_errors += result['errors']
            total_skipped += result.get('skipped', 0)
        
        print(f"\n📊 総合結果:")
        print(f"    総テスト数: {total_tests}")
        print(f"    成功: {total_tests - total_failures - total_errors}")
        print(f"    失敗: {total_failures}")
        print(f"    エラー: {total_errors}")
        print(f"    スキップ: {total_skipped}")
        
        execution_time = self.end_time - self.start_time
        print(f"    実行時間: {execution_time:.2f}秒")
        
        # 総合判定
        if total_failures == 0 and total_errors == 0:
            print(f"\n🎉 全テスト成功！")
        else:
            print(f"\n⚠️  一部テストに問題があります。詳細を確認してください。")
    
    def _generate_report(self):
        """テストレポート生成"""
        report_data = {
            'test_execution': {
                'start_time': self.start_time,
                'end_time': self.end_time,
                'duration': self.end_time - self.start_time,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            },
            'results': self.results,
            'summary': self._calculate_summary()
        }
        
        # JSONレポート生成
        report_file = project_root / 'test_execution_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 詳細レポートを生成しました: {report_file}")
    
    def _calculate_summary(self) -> Dict[str, Any]:
        """サマリー計算"""
        total_tests = sum(r['tests_run'] for r in self.results.values())
        total_failures = sum(r['failures'] for r in self.results.values())
        total_errors = sum(r['errors'] for r in self.results.values())
        total_skipped = sum(r.get('skipped', 0) for r in self.results.values())
        
        success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'total_failures': total_failures,
            'total_errors': total_errors,
            'total_skipped': total_skipped,
            'success_rate': round(success_rate, 2),
            'overall_status': 'success' if total_failures == 0 and total_errors == 0 else 'failure'
        }


def main():
    """メイン実行関数"""
    runner = TestSuiteRunner()
    results = runner.run_all_tests()
    
    # 終了コード設定
    summary = runner._calculate_summary()
    exit_code = 0 if summary['overall_status'] == 'success' else 1
    
    print(f"\n終了コード: {exit_code}")
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
