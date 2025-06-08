#!/usr/bin/env python3
"""
データベースツールテスト実行スクリプト

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-08
実装者: AI Assistant

テスト実行機能：
- ユニットテスト実行
- 統合テスト実行
- パフォーマンステスト実行
- カバレッジレポート生成
- テスト結果レポート出力
"""

import sys
import subprocess
import argparse
import time
from pathlib import Path
from typing import List, Dict, Any
import json


class TestRunner:
    """テスト実行管理クラス"""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.test_dir = base_dir / 'tests'
        self.results = {}
    
    def run_unit_tests(self, verbose: bool = False) -> Dict[str, Any]:
        """ユニットテスト実行"""
        print("🧪 ユニットテスト実行中...")
        
        unit_test_dir = self.test_dir / 'unit'
        if not unit_test_dir.exists():
            return {'status': 'skipped', 'reason': 'ユニットテストディレクトリが存在しません'}
        
        try:
            cmd = [
                sys.executable, '-m', 'unittest', 'discover',
                '-s', str(unit_test_dir),
                '-p', 'test_*.py'
            ]
            
            if verbose:
                cmd.append('-v')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.base_dir
            )
            
            return {
                'status': 'success' if result.returncode == 0 else 'failed',
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': 0  # 実際の実装では時間測定
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def run_integration_tests(self, verbose: bool = False) -> Dict[str, Any]:
        """統合テスト実行"""
        print("🔗 統合テスト実行中...")
        
        integration_test_dir = self.test_dir / 'integration'
        if not integration_test_dir.exists():
            return {'status': 'skipped', 'reason': '統合テストディレクトリが存在しません'}
        
        try:
            cmd = [
                sys.executable, '-m', 'unittest', 'discover',
                '-s', str(integration_test_dir),
                '-p', 'test_*.py'
            ]
            
            if verbose:
                cmd.append('-v')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.base_dir
            )
            
            return {
                'status': 'success' if result.returncode == 0 else 'failed',
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': 0
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def run_performance_tests(self, verbose: bool = False) -> Dict[str, Any]:
        """パフォーマンステスト実行"""
        print("⚡ パフォーマンステスト実行中...")
        
        performance_test_dir = self.test_dir / 'performance'
        if not performance_test_dir.exists():
            return {'status': 'skipped', 'reason': 'パフォーマンステストディレクトリが存在しません'}
        
        try:
            cmd = [
                sys.executable, '-m', 'unittest', 'discover',
                '-s', str(performance_test_dir),
                '-p', 'test_*.py'
            ]
            
            if verbose:
                cmd.append('-v')
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.base_dir
            )
            
            return {
                'status': 'success' if result.returncode == 0 else 'failed',
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'duration': 0
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def run_coverage_analysis(self) -> Dict[str, Any]:
        """カバレッジ分析実行"""
        print("📊 カバレッジ分析実行中...")
        
        try:
            # coverage.pyがインストールされているかチェック
            subprocess.run([sys.executable, '-m', 'coverage', '--version'], 
                         capture_output=True, check=True)
            
            # カバレッジ測定付きでテスト実行
            coverage_cmd = [
                sys.executable, '-m', 'coverage', 'run',
                '--source', str(self.base_dir),
                '--omit', f'{self.test_dir}/*',
                '-m', 'unittest', 'discover',
                '-s', str(self.test_dir),
                '-p', 'test_*.py'
            ]
            
            result = subprocess.run(
                coverage_cmd,
                capture_output=True,
                text=True,
                cwd=self.base_dir
            )
            
            if result.returncode != 0:
                return {
                    'status': 'failed',
                    'error': 'カバレッジ測定付きテスト実行に失敗',
                    'stderr': result.stderr
                }
            
            # カバレッジレポート生成
            report_cmd = [sys.executable, '-m', 'coverage', 'report']
            report_result = subprocess.run(
                report_cmd,
                capture_output=True,
                text=True,
                cwd=self.base_dir
            )
            
            # HTMLレポート生成
            html_cmd = [sys.executable, '-m', 'coverage', 'html', '-d', 'htmlcov']
            subprocess.run(html_cmd, cwd=self.base_dir)
            
            return {
                'status': 'success',
                'report': report_result.stdout,
                'html_report': 'htmlcov/index.html'
            }
            
        except subprocess.CalledProcessError:
            return {
                'status': 'skipped',
                'reason': 'coverage.pyがインストールされていません'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def generate_test_report(self, output_file: str = None) -> str:
        """テスト結果レポート生成"""
        report_lines = []
        report_lines.append("# データベースツール テスト実行結果")
        report_lines.append("")
        report_lines.append(f"実行日時: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # 各テストの結果
        for test_type, result in self.results.items():
            report_lines.append(f"## {test_type}")
            
            if result['status'] == 'success':
                report_lines.append("✅ **成功**")
            elif result['status'] == 'failed':
                report_lines.append("❌ **失敗**")
            elif result['status'] == 'skipped':
                report_lines.append("⏭️ **スキップ**")
                report_lines.append(f"理由: {result.get('reason', '不明')}")
            elif result['status'] == 'error':
                report_lines.append("💥 **エラー**")
                report_lines.append(f"エラー: {result.get('error', '不明')}")
            
            if 'duration' in result:
                report_lines.append(f"実行時間: {result['duration']:.2f}秒")
            
            if result['status'] in ['failed', 'error'] and 'stderr' in result:
                report_lines.append("")
                report_lines.append("### エラー詳細")
                report_lines.append("```")
                report_lines.append(result['stderr'])
                report_lines.append("```")
            
            report_lines.append("")
        
        # カバレッジ情報
        if 'coverage' in self.results:
            coverage_result = self.results['coverage']
            if coverage_result['status'] == 'success':
                report_lines.append("## カバレッジ")
                report_lines.append("```")
                report_lines.append(coverage_result['report'])
                report_lines.append("```")
                report_lines.append("")
                report_lines.append(f"HTMLレポート: {coverage_result['html_report']}")
                report_lines.append("")
        
        # 総合結果
        report_lines.append("## 総合結果")
        
        success_count = sum(1 for r in self.results.values() if r['status'] == 'success')
        total_count = len(self.results)
        
        if success_count == total_count:
            report_lines.append("🎉 **全テスト成功**")
        else:
            failed_count = sum(1 for r in self.results.values() if r['status'] == 'failed')
            error_count = sum(1 for r in self.results.values() if r['status'] == 'error')
            skipped_count = sum(1 for r in self.results.values() if r['status'] == 'skipped')
            
            report_lines.append(f"📊 **テスト結果サマリー**")
            report_lines.append(f"- 成功: {success_count}")
            report_lines.append(f"- 失敗: {failed_count}")
            report_lines.append(f"- エラー: {error_count}")
            report_lines.append(f"- スキップ: {skipped_count}")
        
        report_content = "\n".join(report_lines)
        
        # ファイル出力
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"📄 テストレポートを出力しました: {output_file}")
        
        return report_content
    
    def run_all_tests(self, verbose: bool = False, coverage: bool = False, 
                     output_report: str = None) -> Dict[str, Any]:
        """全テスト実行"""
        print("🚀 データベースツール テスト実行開始")
        print("=" * 60)
        
        start_time = time.time()
        
        # ユニットテスト実行
        self.results['ユニットテスト'] = self.run_unit_tests(verbose)
        
        # 統合テスト実行
        self.results['統合テスト'] = self.run_integration_tests(verbose)
        
        # パフォーマンステスト実行
        self.results['パフォーマンステスト'] = self.run_performance_tests(verbose)
        
        # カバレッジ分析
        if coverage:
            self.results['coverage'] = self.run_coverage_analysis()
        
        end_time = time.time()
        total_duration = end_time - start_time
        
        print("=" * 60)
        print(f"⏱️ 総実行時間: {total_duration:.2f}秒")
        
        # レポート生成
        if output_report:
            self.generate_test_report(output_report)
        
        # 結果サマリー表示
        self._print_summary()
        
        return self.results
    
    def _print_summary(self):
        """結果サマリー表示"""
        print("\n📋 テスト結果サマリー:")
        
        for test_type, result in self.results.items():
            if test_type == 'coverage':
                continue
                
            status_emoji = {
                'success': '✅',
                'failed': '❌',
                'skipped': '⏭️',
                'error': '💥'
            }
            
            emoji = status_emoji.get(result['status'], '❓')
            print(f"  {emoji} {test_type}: {result['status']}")
        
        # 総合判定
        failed_tests = [name for name, result in self.results.items() 
                       if result['status'] in ['failed', 'error'] and name != 'coverage']
        
        if failed_tests:
            print(f"\n❌ 失敗したテスト: {', '.join(failed_tests)}")
            return False
        else:
            print("\n🎉 全テスト成功!")
            return True


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='データベースツール テスト実行')
    
    parser.add_argument('--unit', action='store_true', 
                       help='ユニットテストのみ実行')
    parser.add_argument('--integration', action='store_true', 
                       help='統合テストのみ実行')
    parser.add_argument('--performance', action='store_true', 
                       help='パフォーマンステストのみ実行')
    parser.add_argument('--coverage', action='store_true', 
                       help='カバレッジ分析を実行')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='詳細出力')
    parser.add_argument('--output-report', '-o', type=str, 
                       help='テストレポート出力ファイル')
    
    args = parser.parse_args()
    
    # 実行ディレクトリ設定
    base_dir = Path(__file__).parent
    runner = TestRunner(base_dir)
    
    # 個別テスト実行
    if args.unit:
        result = runner.run_unit_tests(args.verbose)
        runner.results['ユニットテスト'] = result
    elif args.integration:
        result = runner.run_integration_tests(args.verbose)
        runner.results['統合テスト'] = result
    elif args.performance:
        result = runner.run_performance_tests(args.verbose)
        runner.results['パフォーマンステスト'] = result
    else:
        # 全テスト実行
        runner.run_all_tests(args.verbose, args.coverage, args.output_report)
        return
    
    # 個別実行時のレポート生成
    if args.output_report:
        runner.generate_test_report(args.output_report)
    
    # 結果表示
    runner._print_summary()


if __name__ == '__main__':
    main()
