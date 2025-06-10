"""
データベースツール統合テストスイート実行スクリプト

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-08
実装者: AI Assistant

テストスイート実行機能：
- ユニットテスト実行
- 統合テスト実行
- パフォーマンステスト実行
- テストレポート生成
"""

import unittest
import sys
import os
import argparse
import time
from pathlib import Path
from typing import List, Optional
import json

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


class TestRunner:
    """テスト実行管理クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.test_results = {}
        self.start_time = None
        self.end_time = None
    
    def run_unit_tests(self) -> bool:
        """ユニットテスト実行"""
        print("🧪 ユニットテスト実行中...")
        
        # テストディスカバリー
        loader = unittest.TestLoader()
        suite = loader.discover(
            start_dir=str(project_root / 'tests' / 'unit'),
            pattern='test_*.py',
            top_level_dir=str(project_root)
        )
        
        # テスト実行
        runner = unittest.TextTestRunner(
            verbosity=2 if self.verbose else 1,
            stream=sys.stdout
        )
        
        result = runner.run(suite)
        
        self.test_results['unit_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped),
            'success': result.wasSuccessful()
        }
        
        return result.wasSuccessful()
    
    def run_integration_tests(self) -> bool:
        """統合テスト実行"""
        print("🔗 統合テスト実行中...")
        
        # テストディスカバリー
        loader = unittest.TestLoader()
        suite = loader.discover(
            start_dir=str(project_root / 'tests' / 'integration'),
            pattern='test_*.py',
            top_level_dir=str(project_root)
        )
        
        # テスト実行
        runner = unittest.TextTestRunner(
            verbosity=2 if self.verbose else 1,
            stream=sys.stdout
        )
        
        result = runner.run(suite)
        
        self.test_results['integration_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped),
            'success': result.wasSuccessful()
        }
        
        return result.wasSuccessful()
    
    def run_performance_tests(self) -> bool:
        """パフォーマンステスト実行"""
        print("⚡ パフォーマンステスト実行中...")
        
        # psutilの可用性チェック
        try:
            import psutil
            psutil_available = True
        except ImportError:
            print("⚠️  psutilが利用できません。パフォーマンステストをスキップします。")
            print("   インストール: pip install psutil")
            psutil_available = False
        
        if not psutil_available:
            self.test_results['performance_tests'] = {
                'tests_run': 0,
                'failures': 0,
                'errors': 0,
                'skipped': 1,
                'success': True,
                'message': 'psutil not available'
            }
            return True
        
        # テストディスカバリー
        loader = unittest.TestLoader()
        suite = loader.discover(
            start_dir=str(project_root / 'tests' / 'performance'),
            pattern='test_*.py',
            top_level_dir=str(project_root)
        )
        
        # テスト実行
        runner = unittest.TextTestRunner(
            verbosity=2 if self.verbose else 1,
            stream=sys.stdout
        )
        
        result = runner.run(suite)
        
        self.test_results['performance_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'skipped': len(result.skipped),
            'success': result.wasSuccessful()
        }
        
        return result.wasSuccessful()
    
    def run_all_tests(self) -> bool:
        """全テスト実行"""
        print("🚀 データベースツール統合テストスイート開始")
        print("=" * 60)
        
        self.start_time = time.time()
        
        # 各テストスイート実行
        unit_success = self.run_unit_tests()
        print()
        
        integration_success = self.run_integration_tests()
        print()
        
        performance_success = self.run_performance_tests()
        print()
        
        self.end_time = time.time()
        
        # 結果サマリー出力
        self._print_summary()
        
        # 全テストが成功したかどうか
        return unit_success and integration_success and performance_success
    
    def run_specific_tests(self, test_patterns: List[str]) -> bool:
        """特定のテストパターン実行"""
        print(f"🎯 特定テスト実行: {', '.join(test_patterns)}")
        print("=" * 60)
        
        self.start_time = time.time()
        
        all_success = True
        
        for pattern in test_patterns:
            print(f"\n📋 テストパターン実行: {pattern}")
            
            # テストディスカバリー
            loader = unittest.TestLoader()
            suite = loader.discover(
                start_dir=str(project_root / 'tests'),
                pattern=pattern,
                top_level_dir=str(project_root)
            )
            
            # テスト実行
            runner = unittest.TextTestRunner(
                verbosity=2 if self.verbose else 1,
                stream=sys.stdout
            )
            
            result = runner.run(suite)
            
            self.test_results[f'pattern_{pattern}'] = {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'skipped': len(result.skipped),
                'success': result.wasSuccessful()
            }
            
            if not result.wasSuccessful():
                all_success = False
        
        self.end_time = time.time()
        
        # 結果サマリー出力
        self._print_summary()
        
        return all_success
    
    def _print_summary(self):
        """テスト結果サマリー出力"""
        print("=" * 60)
        print("📊 テスト実行結果サマリー")
        print("=" * 60)
        
        total_tests = 0
        total_failures = 0
        total_errors = 0
        total_skipped = 0
        all_success = True
        
        for test_type, results in self.test_results.items():
            status = "✅ PASS" if results['success'] else "❌ FAIL"
            print(f"{test_type:20} {status:8} "
                  f"実行:{results['tests_run']:3d} "
                  f"失敗:{results['failures']:3d} "
                  f"エラー:{results['errors']:3d} "
                  f"スキップ:{results['skipped']:3d}")
            
            total_tests += results['tests_run']
            total_failures += results['failures']
            total_errors += results['errors']
            total_skipped += results['skipped']
            
            if not results['success']:
                all_success = False
        
        print("-" * 60)
        overall_status = "✅ 全テスト成功" if all_success else "❌ テスト失敗あり"
        print(f"{'総合結果':20} {overall_status:8} "
              f"実行:{total_tests:3d} "
              f"失敗:{total_failures:3d} "
              f"エラー:{total_errors:3d} "
              f"スキップ:{total_skipped:3d}")
        
        if self.start_time and self.end_time:
            execution_time = self.end_time - self.start_time
            print(f"\n⏱️  総実行時間: {execution_time:.2f}秒")
        
        # 詳細結果をJSONファイルに出力
        self._save_results_to_file()
    
    def _save_results_to_file(self):
        """テスト結果をファイルに保存"""
        results_file = project_root / 'test_results.json'
        
        detailed_results = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'execution_time': self.end_time - self.start_time if self.start_time and self.end_time else 0,
            'results': self.test_results
        }
        
        try:
            with open(results_file, 'w', encoding='utf-8') as f:
                json.dump(detailed_results, f, indent=2, ensure_ascii=False)
            print(f"\n📄 詳細結果を保存: {results_file}")
        except Exception as e:
            print(f"⚠️  結果ファイル保存に失敗: {e}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description='データベースツール統合テストスイート',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python run_tests.py                    # 全テスト実行
  python run_tests.py --unit             # ユニットテストのみ
  python run_tests.py --integration      # 統合テストのみ
  python run_tests.py --performance      # パフォーマンステストのみ
  python run_tests.py --pattern "test_*" # 特定パターンのテスト
  python run_tests.py --verbose          # 詳細出力
        """
    )
    
    parser.add_argument(
        '--unit', 
        action='store_true',
        help='ユニットテストのみ実行'
    )
    
    parser.add_argument(
        '--integration',
        action='store_true', 
        help='統合テストのみ実行'
    )
    
    parser.add_argument(
        '--performance',
        action='store_true',
        help='パフォーマンステストのみ実行'
    )
    
    parser.add_argument(
        '--pattern',
        nargs='+',
        help='特定のテストパターンを実行'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細出力'
    )
    
    args = parser.parse_args()
    
    # テストランナー初期化
    runner = TestRunner(verbose=args.verbose)
    
    # テスト実行
    success = True
    
    if args.unit:
        success = runner.run_unit_tests()
    elif args.integration:
        success = runner.run_integration_tests()
    elif args.performance:
        success = runner.run_performance_tests()
    elif args.pattern:
        success = runner.run_specific_tests(args.pattern)
    else:
        success = runner.run_all_tests()
    
    # 終了コード設定
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
