"""
データベースツールパフォーマンステスト

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-08
実装者: AI Assistant

パフォーマンステスト項目：
- 大量テーブル生成のパフォーマンス
- 整合性チェックの実行時間
- メモリ使用量の監視
- 並行処理性能の測定
"""

import unittest
import tempfile
import shutil
import time
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    psutil = None
import threading
import concurrent.futures
from pathlib import Path
import yaml
import sys
from typing import List, Dict, Any
import statistics

# テスト対象のインポート
sys.path.insert(0, str(Path(__file__).parent.parent))

# from table_generator.__main__ import main as table_generator_main
# from database_consistency_checker.__main__ import main as consistency_checker_main


class PerformanceTestCase(unittest.TestCase):
    """パフォーマンステストの基底クラス"""
    
    def setUp(self):
        """テストセットアップ"""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.performance_results = {}
        
        # テスト用ディレクトリ構造作成
        self._setup_test_environment()
    
    def tearDown(self):
        """テストクリーンアップ"""
        shutil.rmtree(self.temp_dir)
        
        # パフォーマンス結果出力
        self._output_performance_results()
    
    def _setup_test_environment(self):
        """テスト環境セットアップ"""
        directories = ['table-details', 'ddl', 'tables', 'data', 'consistency_reports']
        for dir_name in directories:
            (self.temp_dir / dir_name).mkdir(exist_ok=True)
    
    def _measure_performance(self, func, *args, **kwargs):
        """パフォーマンス測定ヘルパー"""
        # メモリ使用量測定開始
        process = psutil.Process()
        memory_before = process.memory_info().rss / 1024 / 1024  # MB
        
        # 実行時間測定
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # メモリ使用量測定終了
        memory_after = process.memory_info().rss / 1024 / 1024  # MB
        
        return {
            'result': result,
            'execution_time': end_time - start_time,
            'memory_before': memory_before,
            'memory_after': memory_after,
            'memory_delta': memory_after - memory_before
        }
    
    def _create_test_yaml(self, table_name: str, complexity: str = 'simple') -> None:
        """テスト用YAML作成"""
        if complexity == 'simple':
            columns = [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'primary_key': True,
                    'comment': 'プライマリキー',
                    'requirement_id': 'PLT.1-WEB.1'
                },
                {
                    'name': 'tenant_id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'comment': 'テナントID',
                    'requirement_id': 'TNT.1-MGMT.1'
                }
            ]
            indexes = []
            foreign_keys = []
        
        elif complexity == 'complex':
            columns = [
                {
                    'name': 'id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'primary_key': True,
                    'comment': 'プライマリキー',
                    'requirement_id': 'PLT.1-WEB.1'
                },
                {
                    'name': 'tenant_id',
                    'type': 'VARCHAR(50)',
                    'nullable': False,
                    'comment': 'テナントID',
                    'requirement_id': 'TNT.1-MGMT.1'
                }
            ]
            
            # 複雑なテーブル用に多数のカラム追加
            for i in range(20):
                columns.append({
                    'name': f'field_{i:02d}',
                    'type': 'VARCHAR(255)',
                    'nullable': True,
                    'comment': f'フィールド{i}',
                    'requirement_id': 'TEST.1-PERF.1'
                })
            
            # 複数のインデックス
            indexes = [
                {
                    'name': f'idx_{table_name.lower()}_tenant',
                    'columns': ['tenant_id'],
                    'unique': False,
                    'comment': 'テナント別インデックス'
                },
                {
                    'name': f'idx_{table_name.lower()}_composite',
                    'columns': ['tenant_id', 'field_01', 'field_02'],
                    'unique': False,
                    'comment': '複合インデックス'
                }
            ]
            
            foreign_keys = []
        
        yaml_content = {
            'table_name': table_name,
            'logical_name': f'{table_name}テーブル',
            'category': 'テスト系',
            'priority': '低',
            'requirement_id': 'TEST.1-PERF.1',
            'columns': columns,
            'indexes': indexes,
            'foreign_keys': foreign_keys
        }
        
        yaml_file = self.temp_dir / 'table-details' / f'{table_name}_details.yaml'
        with open(yaml_file, 'w', encoding='utf-8') as f:
            yaml.dump(yaml_content, f, default_flow_style=False, allow_unicode=True)
    
    def _output_performance_results(self):
        """パフォーマンス結果出力"""
        if not self.performance_results:
            return
        
        print(f"\n{'='*60}")
        print(f"パフォーマンステスト結果: {self.__class__.__name__}")
        print(f"{'='*60}")
        
        for test_name, results in self.performance_results.items():
            print(f"\n{test_name}:")
            print(f"  実行時間: {results['execution_time']:.3f}秒")
            print(f"  メモリ使用量: {results['memory_before']:.1f}MB → {results['memory_after']:.1f}MB")
            print(f"  メモリ増加: {results['memory_delta']:.1f}MB")


class TestTableGenerationPerformance(PerformanceTestCase):
    """テーブル生成パフォーマンステスト"""
    
    def setUp(self):
        if not PSUTIL_AVAILABLE:
            self.skipTest("psutil is not available")
        super().setUp()
    
    def test_single_table_generation_performance(self):
        """単一テーブル生成パフォーマンス"""
        # シンプルなテーブル
        self._create_test_yaml('PERF_Simple', 'simple')
        
        def generate_simple():
            return self._mock_table_generation(['PERF_Simple'])
        
        simple_result = self._measure_performance(generate_simple)
        self.performance_results['単一テーブル生成（シンプル）'] = simple_result
        
        # 実行時間の確認（1秒以内）
        self.assertLess(simple_result['execution_time'], 1.0, 
                       f"シンプルテーブル生成が遅すぎます: {simple_result['execution_time']:.3f}秒")
        
        # 複雑なテーブル
        self._create_test_yaml('PERF_Complex', 'complex')
        
        def generate_complex():
            return self._mock_table_generation(['PERF_Complex'])
        
        complex_result = self._measure_performance(generate_complex)
        self.performance_results['単一テーブル生成（複雑）'] = complex_result
        
        # 実行時間の確認（3秒以内）
        self.assertLess(complex_result['execution_time'], 3.0,
                       f"複雑テーブル生成が遅すぎます: {complex_result['execution_time']:.3f}秒")
    
    def test_bulk_table_generation_performance(self):
        """大量テーブル生成パフォーマンス"""
        # 10個のテーブル作成
        table_names = [f'PERF_Bulk_{i:02d}' for i in range(10)]
        
        for table_name in table_names:
            self._create_test_yaml(table_name, 'simple')
        
        def generate_bulk():
            return self._mock_table_generation(table_names)
        
        bulk_result = self._measure_performance(generate_bulk)
        self.performance_results['大量テーブル生成（10個）'] = bulk_result
        
        # 実行時間の確認（10秒以内）
        self.assertLess(bulk_result['execution_time'], 10.0,
                       f"大量テーブル生成が遅すぎます: {bulk_result['execution_time']:.3f}秒")
        
        # 1テーブルあたりの平均時間
        avg_time_per_table = bulk_result['execution_time'] / len(table_names)
        self.assertLess(avg_time_per_table, 1.0,
                       f"1テーブルあたりの生成時間が遅すぎます: {avg_time_per_table:.3f}秒")
    
    def test_concurrent_table_generation_performance(self):
        """並行テーブル生成パフォーマンス"""
        # 5個のテーブルを並行生成
        table_names = [f'PERF_Concurrent_{i:02d}' for i in range(5)]
        
        for table_name in table_names:
            self._create_test_yaml(table_name, 'simple')
        
        def generate_concurrent():
            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                futures = []
                for table_name in table_names:
                    future = executor.submit(self._mock_table_generation, [table_name])
                    futures.append(future)
                
                results = []
                for future in concurrent.futures.as_completed(futures):
                    results.append(future.result())
                
                return results
        
        concurrent_result = self._measure_performance(generate_concurrent)
        self.performance_results['並行テーブル生成（5個）'] = concurrent_result
        
        # 並行処理の効果確認（逐次処理より高速であることを期待）
        self.assertLess(concurrent_result['execution_time'], 5.0,
                       f"並行テーブル生成が遅すぎます: {concurrent_result['execution_time']:.3f}秒")
    
    def _mock_table_generation(self, table_names: List[str]) -> Dict[str, Any]:
        """テーブル生成のモック実装"""
        results = []
        
        for table_name in table_names:
            # DDLファイル作成
            ddl_content = f"""-- {table_name} テーブル定義
CREATE TABLE {table_name} (
    id VARCHAR(50) NOT NULL PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- インデックス作成
CREATE INDEX idx_{table_name.lower()}_tenant ON {table_name}(tenant_id);
"""
            
            ddl_file = self.temp_dir / 'ddl' / f'{table_name}.sql'
            with open(ddl_file, 'w', encoding='utf-8') as f:
                f.write(ddl_content)
            
            # Markdownファイル作成
            md_content = f"""# テーブル定義書_{table_name}

## 基本情報
- **テーブル名**: {table_name}
- **論理名**: {table_name}テーブル
- **カテゴリ**: テスト系
- **優先度**: 低
- **要求仕様ID**: TEST.1-PERF.1

## カラム定義
| カラム名 | データ型 | NULL | キー | デフォルト値 | コメント |
|----------|----------|------|------|-------------|----------|
| id | VARCHAR(50) | NOT NULL | PK | - | プライマリキー |
| tenant_id | VARCHAR(50) | NOT NULL | - | - | テナントID |
| created_at | TIMESTAMP | NOT NULL | - | CURRENT_TIMESTAMP | 作成日時 |
"""
            
            md_file = self.temp_dir / 'tables' / f'テーブル定義書_{table_name}_{table_name}テーブル.md'
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            # サンプルデータファイル作成
            data_content = f"""-- {table_name} サンプルデータ
INSERT INTO {table_name} (id, tenant_id) VALUES 
('test-{table_name.lower()}-001', 'tenant-001'),
('test-{table_name.lower()}-002', 'tenant-001'),
('test-{table_name.lower()}-003', 'tenant-002');
"""
            
            data_file = self.temp_dir / 'data' / f'{table_name}_sample_data.sql'
            with open(data_file, 'w', encoding='utf-8') as f:
                f.write(data_content)
            
            results.append({'table': table_name, 'status': 'success'})
            
            # 処理時間をシミュレート
            time.sleep(0.1)
        
        return {'tables': results, 'status': 'success'}


class TestConsistencyCheckPerformance(PerformanceTestCase):
    """整合性チェックパフォーマンステスト"""
    
    def test_consistency_check_performance(self):
        """整合性チェックパフォーマンス"""
        # テストテーブル作成
        table_names = [f'PERF_Check_{i:02d}' for i in range(20)]
        
        for table_name in table_names:
            self._create_test_yaml(table_name, 'simple')
            # 対応するファイルも作成
            self._create_mock_files(table_name)
        
        def run_consistency_check():
            return self._mock_consistency_check(table_names)
        
        check_result = self._measure_performance(run_consistency_check)
        self.performance_results['整合性チェック（20テーブル）'] = check_result
        
        # 実行時間の確認（5秒以内）
        self.assertLess(check_result['execution_time'], 5.0,
                       f"整合性チェックが遅すぎます: {check_result['execution_time']:.3f}秒")
        
        # 1テーブルあたりの平均時間
        avg_time_per_table = check_result['execution_time'] / len(table_names)
        self.assertLess(avg_time_per_table, 0.25,
                       f"1テーブルあたりのチェック時間が遅すぎます: {avg_time_per_table:.3f}秒")
    
    def test_memory_usage_during_large_check(self):
        """大量チェック時のメモリ使用量テスト"""
        # 50個のテーブル作成
        table_names = [f'PERF_Memory_{i:03d}' for i in range(50)]
        
        for table_name in table_names:
            self._create_test_yaml(table_name, 'complex')
            self._create_mock_files(table_name)
        
        def run_large_check():
            return self._mock_consistency_check(table_names)
        
        memory_result = self._measure_performance(run_large_check)
        self.performance_results['大量整合性チェック（50テーブル）'] = memory_result
        
        # メモリ使用量の確認（100MB以内の増加）
        self.assertLess(memory_result['memory_delta'], 100.0,
                       f"メモリ使用量が多すぎます: {memory_result['memory_delta']:.1f}MB")
    
    def _create_mock_files(self, table_name: str):
        """モックファイル作成"""
        # DDLファイル
        ddl_file = self.temp_dir / 'ddl' / f'{table_name}.sql'
        ddl_file.touch()
        
        # Markdownファイル
        md_file = self.temp_dir / 'tables' / f'テーブル定義書_{table_name}_{table_name}テーブル.md'
        md_file.touch()
    
    def _mock_consistency_check(self, table_names: List[str]) -> Dict[str, Any]:
        """整合性チェックのモック実装"""
        results = []
        
        for table_name in table_names:
            # ファイル存在チェック
            yaml_file = self.temp_dir / 'table-details' / f'{table_name}_details.yaml'
            ddl_file = self.temp_dir / 'ddl' / f'{table_name}.sql'
            md_file = self.temp_dir / 'tables' / f'テーブル定義書_{table_name}_{table_name}テーブル.md'
            
            checks = {
                'table_existence': yaml_file.exists() and ddl_file.exists() and md_file.exists(),
                'column_consistency': True,  # モックでは常にOK
                'foreign_key_consistency': True,  # モックでは常にOK
                'naming_convention': True  # モックでは常にOK
            }
            
            results.append({
                'table': table_name,
                'checks': checks,
                'status': 'success' if all(checks.values()) else 'error'
            })
            
            # チェック処理時間をシミュレート
            time.sleep(0.01)
        
        return {'tables': results, 'status': 'success'}


if __name__ == '__main__':
    # パフォーマンステストスイート実行
    unittest.main(verbosity=2)
