#!/usr/bin/env python3
"""
YAML形式検証機能（統合版）

database_consistency_checkerに統合されたYAML形式検証機能です。
yaml_validatorから移行された機能を含みます。

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-21
実装者: AI駆動開発チーム

機能：
- YAML形式の検証
- 必須セクションの存在確認
- サンプルデータ生成統合
- 整合性チェックとの連携
"""

import os
import sys
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))

# パスを追加
sys.path.append(os.path.join(PROJECT_ROOT, "docs/design/database/tools"))

try:
    from shared.checkers.yaml_format_validator import YAMLFormatValidator
    from shared.generators.sample_data_generator import SampleDataGenerator
    from shared.core.models import TableDefinition
except ImportError as e:
    print(f"モジュールのインポートに失敗しました: {e}")
    YAMLFormatValidator = None
    SampleDataGenerator = None
    TableDefinition = None

import yaml


class YAMLFormatCheckEnhanced:
    """YAML形式検証機能（統合版）"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
        
        # YAML検証機能
        if YAMLFormatValidator:
            self.yaml_validator = YAMLFormatValidator(verbose=verbose)
        else:
            self.yaml_validator = None
            self.logger.warning("YAMLFormatValidatorが利用できません")
        
        # サンプルデータ生成機能
        if SampleDataGenerator:
            config = {'verbose': verbose}
            self.sample_data_generator = SampleDataGenerator(config)
        else:
            self.sample_data_generator = None
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
        """機能が利用可能かチェック"""
        return self.yaml_validator is not None
    
    def validate_yaml_format(self, table_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        YAML形式検証
        
        Args:
            table_names: 対象テーブル名のリスト（Noneの場合は全テーブル）
            
        Returns:
            Dict[str, Any]: 検証結果
        """
        if not self.is_available():
            return {
                'success': False,
                'error': 'YAMLFormatValidatorが利用できません',
                'validation_available': False
            }
        
        try:
            if table_names:
                # 指定テーブルの検証
                results = {}
                for table_name in table_names:
                    results[table_name] = self.yaml_validator.validate_table(table_name)
                
                result = {
                    'success': all(r['success'] for r in results.values()),
                    'total_files': len(table_names),
                    'valid_files': sum(1 for r in results.values() if r['success']),
                    'invalid_files': sum(1 for r in results.values() if not r['success']),
                    'files': results,
                    'summary_errors': [],
                    'summary_warnings': []
                }
                
                for table_name, table_result in results.items():
                    result['summary_errors'].extend([f"{table_name}: {error}" for error in table_result['errors']])
                    result['summary_warnings'].extend([f"{table_name}: {warning}" for warning in table_result['warnings']])
            else:
                # 全テーブルの検証
                result = self.yaml_validator.validate_all_tables()
            
            result['validation_available'] = True
            
            if self.verbose:
                self.logger.info(f"YAML形式検証完了: {result['valid_files']}/{result['total_files']}ファイル成功")
            
            return result
            
        except Exception as e:
            error_msg = f"YAML形式検証に失敗: {str(e)}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'validation_available': True,
                'total_files': 0,
                'valid_files': 0,
                'invalid_files': 0,
                'summary_errors': [error_msg],
                'summary_warnings': []
            }
    
    def generate_sample_data(self, table_names: Optional[List[str]] = None, 
                           output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        サンプルデータ生成
        
        Args:
            table_names: 対象テーブル名のリスト（Noneの場合は全テーブル）
            output_dir: 出力ディレクトリ（Noneの場合は保存しない）
            
        Returns:
            Dict[str, Any]: 生成結果
        """
        if not self.sample_data_generator:
            return {
                'success': False,
                'error': 'SampleDataGeneratorが利用できません',
                'generation_available': False
            }
        
        try:
            # サンプルデータ生成
            if table_names:
                generation_result = self.sample_data_generator.generate_sample_data_sql(table_names)
            else:
                generation_result = self.sample_data_generator.generate_sample_data_sql()
            
            # ファイル保存
            if output_dir and generation_result.get('success', False):
                save_result = self._save_sample_data_sql(generation_result, output_dir)
                generation_result['save_result'] = save_result
                
                if not save_result.get('success', False):
                    generation_result['success'] = False
                    generation_result.setdefault('errors', []).extend(save_result.get('errors', []))
            
            generation_result['generation_available'] = True
            
            if self.verbose:
                self.logger.info(f"サンプルデータ生成完了: {generation_result.get('generated_tables', 0)}/{generation_result.get('total_tables', 0)}テーブル")
            
            return generation_result
            
        except Exception as e:
            error_msg = f"サンプルデータ生成に失敗: {str(e)}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'generation_available': True,
                'total_tables': 0,
                'generated_tables': 0,
                'total_records': 0,
                'errors': [error_msg]
            }
    
    def _save_sample_data_sql(self, result: Dict[str, Any], output_dir: str) -> Dict[str, Any]:
        """
        サンプルデータSQLをファイルに保存
        
        Args:
            result: generate_sample_data_sqlの結果
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
                            output_dir: Optional[str] = None,
                            generate_sample_data: bool = False) -> Dict[str, Any]:
        """
        検証とサンプルデータ生成の統合実行
        
        Args:
            table_names: 対象テーブル名のリスト（Noneの場合は全テーブル）
            output_dir: サンプルデータ出力ディレクトリ
            generate_sample_data: サンプルデータ生成フラグ
            
        Returns:
            Dict[str, Any]: 実行結果
        """
        result = {
            'success': True,
            'validation_result': {},
            'sample_data_result': {},
            'errors': []
        }
        
        try:
            # YAML検証
            validation_result = self.validate_yaml_format(table_names)
            result['validation_result'] = validation_result
            
            if not validation_result.get('success', False):
                result['success'] = False
                result['errors'].append('YAML検証に失敗しました')
            
            # サンプルデータ生成
            if generate_sample_data:
                sample_data_result = self.generate_sample_data(table_names, output_dir)
                result['sample_data_result'] = sample_data_result
                
                if not sample_data_result.get('success', False):
                    result['success'] = False
                    result['errors'].extend(sample_data_result.get('errors', []))
        
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"統合実行エラー: {str(e)}")
            self.logger.error(f"統合実行エラー: {e}")
        
        return result
    
    def print_summary(self, result: Dict[str, Any]):
        """結果サマリーの出力"""
        print("=== YAML形式検証・サンプルデータ生成結果 ===")
        
        # YAML検証結果
        validation_result = result.get('validation_result', {})
        if validation_result:
            print("--- YAML形式検証 ---")
            print(f"✅ 検証成功: {validation_result.get('success', False)}")
            print(f"📊 対象ファイル数: {validation_result.get('total_files', 0)}")
            print(f"📊 有効ファイル数: {validation_result.get('valid_files', 0)}")
            print(f"📊 無効ファイル数: {validation_result.get('invalid_files', 0)}")
            
            summary_errors = validation_result.get('summary_errors', [])
            if summary_errors:
                print(f"❌ エラー数: {len(summary_errors)}")
                for i, error in enumerate(summary_errors[:3], 1):
                    print(f"    {i}. {error}")
                if len(summary_errors) > 3:
                    print(f"    ... 他 {len(summary_errors) - 3} エラー")
        
        # サンプルデータ生成結果
        sample_data_result = result.get('sample_data_result', {})
        if sample_data_result:
            print("\n--- サンプルデータ生成 ---")
            print(f"✅ 生成成功: {sample_data_result.get('success', False)}")
            print(f"📊 対象テーブル数: {sample_data_result.get('total_tables', 0)}")
            print(f"📊 生成テーブル数: {sample_data_result.get('generated_tables', 0)}")
            print(f"📊 総レコード数: {sample_data_result.get('total_records', 0)}")
            
            save_result = sample_data_result.get('save_result', {})
            if save_result:
                saved_files = save_result.get('saved_files', [])
                if saved_files:
                    print(f"💾 保存ファイル数: {len(saved_files)}")
                    for file_path in saved_files:
                        print(f"    - {file_path}")


def main():
    """メイン関数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YAML形式検証・サンプルデータ生成（統合版）')
    parser.add_argument('--table', help='検証対象のテーブル名')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--all', action='store_true', help='全テーブルを検証')
    parser.add_argument('--generate-sample-data', action='store_true', help='サンプルデータを生成')
    parser.add_argument('--output-dir', help='サンプルデータ出力ディレクトリ')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    args = parser.parse_args()
    
    # チェッカーの初期化
    checker = YAMLFormatCheckEnhanced(verbose=args.verbose)
    
    # 対象テーブルの決定
    table_names = None
    if args.table:
        table_names = [args.table]
    elif args.tables:
        table_names = [name.strip() for name in args.tables.split(',')]
    elif not args.all:
        # デフォルトは全テーブル
        args.all = True
    
    # 統合実行
    result = checker.validate_and_generate(
        table_names=table_names,
        output_dir=args.output_dir,
        generate_sample_data=args.generate_sample_data
    )
    
    # 結果表示
    checker.print_summary(result)
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
