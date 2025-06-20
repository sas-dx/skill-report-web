"""
サンプルデータ生成機能の統合

YAML検証ツールにサンプルデータINSERT文生成機能を統合し、
検証プロセスの一部として実行できるようにします。

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-21
実装者: AI駆動開発チーム

機能：
- YAML検証後のサンプルデータ生成
- 依存関係を考慮した実行順序決定
- 検証ツールとの統合インターフェース
- エラーハンドリングと詳細レポート
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))

# パスを追加
sys.path.append(os.path.join(PROJECT_ROOT, "docs/design/database/tools"))

try:
    from shared.generators.sample_data_generator import SampleDataGenerator
    from shared.core.models import TableDefinition
except ImportError as e:
    print(f"モジュールのインポートに失敗しました: {e}")
    print("shared.generators.sample_data_generatorが利用できません")
    SampleDataGenerator = None
    TableDefinition = None


class SampleDataIntegration:
    """サンプルデータ生成統合クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
        
        # サンプルデータジェネレーターの初期化
        if SampleDataGenerator:
            config = {'verbose': verbose}
            self.generator = SampleDataGenerator(config)
        else:
            self.generator = None
            self.logger.warning("SampleDataGeneratorが利用できません")
    
    def _setup_logging(self):
        """ログ設定のセットアップ"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO if self.verbose else logging.WARNING)
    
    def is_available(self) -> bool:
        """サンプルデータ生成機能が利用可能かチェック"""
        return self.generator is not None
    
    def generate_sample_data_for_table(self, table_name: str) -> Dict[str, Any]:
        """
        単一テーブルのサンプルデータを生成
        
        Args:
            table_name: テーブル名
            
        Returns:
            Dict[str, Any]: 生成結果
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'SampleDataGeneratorが利用できません',
                'table_name': table_name,
                'sql_content': '',
                'record_count': 0
            }
        
        try:
            # TableDefinitionを作成
            table_def = TableDefinition(
                name=table_name,
                logical_name=f'{table_name}テーブル',
                category='不明',
                priority='中',
                requirement_id='PLT.1-WEB.1'
            )
            
            # サンプルデータ生成
            sql_content = self.generator.generate(table_def)
            
            # レコード数をカウント
            record_count = sql_content.count('INSERT INTO')
            
            return {
                'success': True,
                'table_name': table_name,
                'sql_content': sql_content,
                'record_count': record_count,
                'error': None
            }
            
        except Exception as e:
            error_msg = f"テーブル {table_name} のサンプルデータ生成に失敗: {str(e)}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'table_name': table_name,
                'sql_content': '',
                'record_count': 0
            }
    
    def generate_sample_data_for_tables(self, table_names: List[str]) -> Dict[str, Any]:
        """
        複数テーブルのサンプルデータを生成
        
        Args:
            table_names: テーブル名のリスト
            
        Returns:
            Dict[str, Any]: 生成結果
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'SampleDataGeneratorが利用できません',
                'total_tables': len(table_names),
                'generated_tables': 0,
                'total_records': 0,
                'execution_order': [],
                'tables': {},
                'errors': ['SampleDataGeneratorが利用できません']
            }
        
        try:
            # 複数テーブルのサンプルデータ生成
            result = self.generator.generate_sample_data_sql(table_names)
            
            if self.verbose:
                self.logger.info(f"サンプルデータ生成完了: {result['generated_tables']}/{result['total_tables']}テーブル")
            
            return result
            
        except Exception as e:
            error_msg = f"複数テーブルのサンプルデータ生成に失敗: {str(e)}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'total_tables': len(table_names),
                'generated_tables': 0,
                'total_records': 0,
                'execution_order': [],
                'tables': {},
                'errors': [error_msg]
            }
    
    def generate_all_sample_data(self) -> Dict[str, Any]:
        """
        全テーブルのサンプルデータを生成
        
        Returns:
            Dict[str, Any]: 生成結果
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'SampleDataGeneratorが利用できません',
                'total_tables': 0,
                'generated_tables': 0,
                'total_records': 0,
                'execution_order': [],
                'tables': {},
                'errors': ['SampleDataGeneratorが利用できません']
            }
        
        try:
            # 全テーブルのサンプルデータ生成
            result = self.generator.generate_sample_data_sql()
            
            if self.verbose:
                self.logger.info(f"全テーブルサンプルデータ生成完了: {result['generated_tables']}/{result['total_tables']}テーブル")
            
            return result
            
        except Exception as e:
            error_msg = f"全テーブルのサンプルデータ生成に失敗: {str(e)}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'total_tables': 0,
                'generated_tables': 0,
                'total_records': 0,
                'execution_order': [],
                'tables': {},
                'errors': [error_msg]
            }
    
    def save_sample_data_sql(self, result: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """
        サンプルデータSQLをファイルに保存
        
        Args:
            result: generate_sample_data_*の結果
            output_dir: 出力ディレクトリ
            
        Returns:
            Dict[str, Any]: 保存結果
        """
        save_result = {
            'success': True,
            'saved_files': [],
            'errors': []
        }
        
        try:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            if not result.get('success', False):
                save_result['success'] = False
                save_result['errors'].append('生成結果が失敗状態です')
                return save_result
            
            # 個別テーブルファイルの保存
            for table_name, table_data in result.get('tables', {}).items():
                try:
                    file_path = output_path / f"{table_name}_sample_data.sql"
                    
                    # SQL内容を構築
                    sql_lines = []
                    sql_lines.append(f"-- サンプルデータ INSERT文: {table_name}")
                    sql_lines.append(f"-- 生成日時: {result.get('timestamp', 'unknown')}")
                    sql_lines.append(f"-- レコード数: {table_data.get('records', 0)}")
                    sql_lines.append("")
                    sql_lines.append("BEGIN;")
                    sql_lines.append("")
                    
                    for stmt in table_data.get('statements', []):
                        sql_lines.append(stmt)
                    
                    sql_lines.append("")
                    sql_lines.append("COMMIT;")
                    sql_lines.append("")
                    sql_lines.append(f"-- {table_name} サンプルデータ終了")
                    
                    # ファイルに書き込み
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(sql_lines))
                    
                    save_result['saved_files'].append(str(file_path))
                    
                    if self.verbose:
                        self.logger.info(f"サンプルデータファイル保存: {file_path}")
                
                except Exception as e:
                    error_msg = f"テーブル {table_name} のファイル保存に失敗: {str(e)}"
                    save_result['errors'].append(error_msg)
                    self.logger.error(error_msg)
            
            # 統合ファイルの保存
            try:
                all_file_path = output_path / "all_sample_data.sql"
                
                sql_lines = []
                sql_lines.append("-- 全テーブル サンプルデータ INSERT文")
                sql_lines.append(f"-- 生成日時: {result.get('timestamp', 'unknown')}")
                sql_lines.append(f"-- 対象テーブル数: {result.get('total_tables', 0)}")
                sql_lines.append(f"-- 生成テーブル数: {result.get('generated_tables', 0)}")
                sql_lines.append(f"-- 総レコード数: {result.get('total_records', 0)}")
                sql_lines.append("")
                sql_lines.append("-- 実行順序:")
                for i, table_name in enumerate(result.get('execution_order', []), 1):
                    sql_lines.append(f"-- {i:2d}. {table_name}")
                sql_lines.append("")
                sql_lines.append("BEGIN;")
                sql_lines.append("")
                
                # 実行順序に従ってINSERT文を追加
                for table_name in result.get('execution_order', []):
                    if table_name in result.get('tables', {}):
                        table_data = result['tables'][table_name]
                        sql_lines.append(f"-- {table_name} ({table_data.get('records', 0)}件)")
                        for stmt in table_data.get('statements', []):
                            sql_lines.append(stmt)
                        sql_lines.append("")
                
                sql_lines.append("COMMIT;")
                sql_lines.append("")
                sql_lines.append("-- 全テーブル サンプルデータ終了")
                
                # ファイルに書き込み
                with open(all_file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(sql_lines))
                
                save_result['saved_files'].append(str(all_file_path))
                
                if self.verbose:
                    self.logger.info(f"統合サンプルデータファイル保存: {all_file_path}")
            
            except Exception as e:
                error_msg = f"統合ファイルの保存に失敗: {str(e)}"
                save_result['errors'].append(error_msg)
                self.logger.error(error_msg)
            
            # エラーがある場合は失敗とする
            if save_result['errors']:
                save_result['success'] = False
        
        except Exception as e:
            save_result['success'] = False
            save_result['errors'].append(f"ファイル保存処理に失敗: {str(e)}")
            self.logger.error(f"ファイル保存処理に失敗: {e}")
        
        return save_result
    
    def validate_and_generate(self, table_names: Optional[List[str]] = None, 
                            output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        検証とサンプルデータ生成を統合実行
        
        Args:
            table_names: 対象テーブル名のリスト（Noneの場合は全テーブル）
            output_dir: 出力ディレクトリ（Noneの場合は保存しない）
            
        Returns:
            Dict[str, Any]: 実行結果
        """
        result = {
            'success': True,
            'validation_available': True,
            'generation_available': self.is_available(),
            'generation_result': {},
            'save_result': {},
            'errors': []
        }
        
        try:
            # サンプルデータ生成
            if self.is_available():
                if table_names:
                    generation_result = self.generate_sample_data_for_tables(table_names)
                else:
                    generation_result = self.generate_all_sample_data()
                
                result['generation_result'] = generation_result
                
                if not generation_result.get('success', False):
                    result['success'] = False
                    result['errors'].extend(generation_result.get('errors', []))
                
                # ファイル保存
                if output_dir and generation_result.get('success', False):
                    save_result = self.save_sample_data_sql(generation_result, output_dir)
                    result['save_result'] = save_result
                    
                    if not save_result.get('success', False):
                        result['success'] = False
                        result['errors'].extend(save_result.get('errors', []))
            
            else:
                result['success'] = False
                result['errors'].append('SampleDataGeneratorが利用できません')
        
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"統合実行に失敗: {str(e)}")
            self.logger.error(f"統合実行に失敗: {e}")
        
        return result
    
    def print_summary(self, result: Dict[str, Any]):
        """結果サマリーを出力"""
        print("=== サンプルデータ生成統合結果 ===")
        
        if not result.get('generation_available', False):
            print("❌ サンプルデータ生成機能が利用できません")
            return
        
        generation_result = result.get('generation_result', {})
        
        print(f"✅ 生成成功: {generation_result.get('success', False)}")
        print(f"📊 対象テーブル数: {generation_result.get('total_tables', 0)}")
        print(f"📊 生成テーブル数: {generation_result.get('generated_tables', 0)}")
        print(f"📊 総レコード数: {generation_result.get('total_records', 0)}")
        
        execution_order = generation_result.get('execution_order', [])
        if execution_order:
            print(f"🔄 実行順序（最初の5テーブル）: {', '.join(execution_order[:5])}")
            if len(execution_order) > 5:
                print(f"    ... 他 {len(execution_order) - 5} テーブル")
        
        errors = generation_result.get('errors', [])
        if errors:
            print(f"❌ エラー数: {len(errors)}")
            for i, error in enumerate(errors[:3], 1):
                print(f"    {i}. {error}")
            if len(errors) > 3:
                print(f"    ... 他 {len(errors) - 3} エラー")
        
        save_result = result.get('save_result', {})
        if save_result:
            saved_files = save_result.get('saved_files', [])
            if saved_files:
                print(f"💾 保存ファイル数: {len(saved_files)}")
                for file_path in saved_files[:3]:
                    print(f"    - {file_path}")
                if len(saved_files) > 3:
                    print(f"    ... 他 {len(saved_files) - 3} ファイル")


def main():
    """メイン関数（テスト用）"""
    import argparse
    
    parser = argparse.ArgumentParser(description='サンプルデータ生成統合テスト')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--output-dir', help='出力ディレクトリ')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    args = parser.parse_args()
    
    # 統合クラスの初期化
    integration = SampleDataIntegration(verbose=args.verbose)
    
    # テーブル名の解析
    table_names = args.tables.split(',') if args.tables else None
    
    # 統合実行
    result = integration.validate_and_generate(table_names, args.output_dir)
    
    # 結果表示
    integration.print_summary(result)
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
