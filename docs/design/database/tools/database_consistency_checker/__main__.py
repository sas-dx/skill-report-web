#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
データベース整合性チェックツール - 共通ライブラリ対応メインエントリーポイント

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

共通ライブラリを使用したデータベース設計の整合性チェック
"""

import sys
import argparse
from pathlib import Path
import logging
from typing import List, Dict, Any

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 共通ライブラリをインポート
try:
    from shared.core.config import get_config, DatabaseToolsConfig
    from shared.parsers.yaml_parser import YamlParser
    from shared.parsers.ddl_parser import DDLParser
    from shared.parsers.markdown_parser import MarkdownParser
    from shared.core.exceptions import (
        DatabaseToolsException, 
        ParsingError, 
        ValidationError
    )
except ImportError:
    # フォールバック: 相対パスでインポート
    import sys
    from pathlib import Path
    tools_dir = Path(__file__).parent.parent
    sys.path.insert(0, str(tools_dir))
    
    from shared.core.config import get_config, DatabaseToolsConfig
    from shared.parsers.yaml_parser import YamlParser
    from shared.parsers.ddl_parser import DDLParser
    from shared.parsers.markdown_parser import MarkdownParser
    from shared.core.exceptions import (
        DatabaseToolsException, 
        ParsingError, 
        ValidationError
    )

# YAMLフォーマット検証モジュールをインポート
try:
    from .yaml_format_check import check_yaml_format, check_yaml_format_enhanced
    from .sample_data_generator import generate_sample_data_sql, validate_and_generate
    from .yaml_format_check_enhanced import IntegratedValidator
    from .sample_data_generator_enhanced import EnhancedSampleDataGenerator
except ImportError:
    # 相対インポートが失敗した場合の絶対インポート
    import sys
    from pathlib import Path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    from yaml_format_check import check_yaml_format, check_yaml_format_enhanced
    from sample_data_generator import generate_sample_data_sql, validate_and_generate
    from yaml_format_check_enhanced import IntegratedValidator
    from sample_data_generator_enhanced import EnhancedSampleDataGenerator


def setup_logger(verbose: bool = False):
    """ログ設定"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


class ConsistencyCheckService:
    """整合性チェックサービス - 共通ライブラリ使用版"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # パーサーの初期化
        self.yaml_parser = YamlParser(config.to_dict())
        self.ddl_parser = DDLParser(config.to_dict())
        self.markdown_parser = MarkdownParser()
        
        # チェック結果
        self.check_results = []
    
    def run_all_checks(self, target_tables: List[str] = None) -> Dict[str, Any]:
        """全整合性チェック実行"""
        self.logger.info("整合性チェック開始")
        
        results = {
            'total_checks': 0,
            'passed_checks': 0,
            'failed_checks': 0,
            'warnings': 0,
            'errors': [],
            'details': []
        }
        
        try:
            # 対象テーブル決定
            if target_tables is None:
                yaml_files = list(self.config.table_details_dir.glob("*_details.yaml"))
                target_tables = [f.stem.replace("_details", "") for f in yaml_files]
            
            if not target_tables:
                self.logger.warning("チェック対象テーブルが見つかりません")
                return results
            
            self.logger.info(f"チェック対象テーブル: {', '.join(target_tables)}")
            
            # 各チェック実行
            check_methods = [
                ('yaml_format', self._check_yaml_format),
                ('table_existence', self._check_table_existence),
                ('column_consistency', self._check_column_consistency),
                ('foreign_key_consistency', self._check_foreign_key_consistency),
                ('data_type_consistency', self._check_data_type_consistency),
                ('naming_convention', self._check_naming_convention)
            ]
            
            for check_name, check_method in check_methods:
                self.logger.info(f"チェック実行: {check_name}")
                check_result = check_method(target_tables)
                results['details'].append(check_result)
                results['total_checks'] += 1
                
                if check_result['status'] == 'PASS':
                    results['passed_checks'] += 1
                elif check_result['status'] == 'FAIL':
                    results['failed_checks'] += 1
                    results['errors'].extend(check_result.get('errors', []))
                elif check_result['status'] == 'WARNING':
                    results['warnings'] += 1
            
            self.logger.info("整合性チェック完了")
            
        except Exception as e:
            error_msg = f"整合性チェック中にエラーが発生: {str(e)}"
            self.logger.error(error_msg)
            results['errors'].append(error_msg)
        
        return results
    
    def _check_yaml_format(self, target_tables: List[str]) -> Dict[str, Any]:
        """YAMLフォーマット検証チェック"""
        result = {
            'check_name': 'yaml_format',
            'description': 'YAMLフォーマット・必須セクション検証',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        try:
            # YAMLフォーマット検証実行
            yaml_check_result = check_yaml_format(tables=target_tables, verbose=False)
            
            # 結果を統合
            if not yaml_check_result['success']:
                result['status'] = 'FAIL'
                
                for yaml_result in yaml_check_result['results']:
                    if not yaml_result['valid']:
                        table_detail = {
                            'table_name': yaml_result['table'],
                            'yaml_format_issues': yaml_result['errors']
                        }
                        result['details'].append(table_detail)
                        
                        # エラーメッセージを追加
                        for error in yaml_result['errors']:
                            error_msg = f"{yaml_result['table']}: {error}"
                            result['errors'].append(error_msg)
            
            # 成功した場合の詳細情報
            if result['status'] == 'PASS':
                result['details'].append({
                    'note': f"全{yaml_check_result['valid']}テーブルのYAMLフォーマット検証に成功しました"
                })
            
        except Exception as e:
            error_msg = f"YAMLフォーマット検証中にエラーが発生: {str(e)}"
            result['errors'].append(error_msg)
            result['status'] = 'FAIL'
            self.logger.error(error_msg)
        
        return result
    
    def _check_yaml_format_enhanced(self, target_tables: List[str]) -> Dict[str, Any]:
        """拡張YAMLフォーマット検証チェック（必須セクション詳細対応）"""
        result = {
            'check_name': 'yaml_format_enhanced',
            'description': '拡張YAMLフォーマット・必須セクション詳細検証',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        try:
            # 拡張YAMLフォーマット検証実行
            yaml_check_result = check_yaml_format_enhanced(tables=target_tables, verbose=False)
            
            # 結果を統合
            if not yaml_check_result['success']:
                result['status'] = 'FAIL'
                
                for yaml_result in yaml_check_result['results']:
                    if not yaml_result['valid']:
                        table_detail = {
                            'table_name': yaml_result['table'],
                            'yaml_format_issues': yaml_result['errors'],
                            'yaml_warnings': yaml_result['warnings'],
                            'required_sections_status': yaml_result['required_sections'],
                            'format_issues': yaml_result['format_issues'],
                            'requirement_id_issues': yaml_result['requirement_id_issues']
                        }
                        result['details'].append(table_detail)
                        
                        # 必須セクション不備を優先的にエラーとして追加
                        critical_issues = [
                            section for section, valid in yaml_result['required_sections'].items()
                            if not valid
                        ]
                        if critical_issues:
                            error_msg = f"{yaml_result['table']}: 🔴 必須セクション不備 ({', '.join(critical_issues)})"
                            result['errors'].append(error_msg)
                        
                        # その他のエラー
                        for error in yaml_result['errors']:
                            error_msg = f"{yaml_result['table']}: {error}"
                            result['errors'].append(error_msg)
                        
                        # 警告
                        for warning in yaml_result['warnings']:
                            warning_msg = f"{yaml_result['table']}: {warning}"
                            result['warnings'].append(warning_msg)
            
            # 警告のみの場合
            elif yaml_check_result['warning'] > 0:
                result['status'] = 'WARNING'
                for yaml_result in yaml_check_result['results']:
                    if yaml_result['warnings']:
                        table_detail = {
                            'table_name': yaml_result['table'],
                            'yaml_warnings': yaml_result['warnings'],
                            'requirement_id_issues': yaml_result['requirement_id_issues']
                        }
                        result['details'].append(table_detail)
                        
                        for warning in yaml_result['warnings']:
                            warning_msg = f"{yaml_result['table']}: {warning}"
                            result['warnings'].append(warning_msg)
            
            # 成功した場合の詳細情報
            if result['status'] == 'PASS':
                summary = yaml_check_result['summary']
                result['details'].append({
                    'note': f"全{yaml_check_result['valid']}テーブルの拡張YAML検証に成功しました",
                    'execution_time': f"{summary['execution_time']:.2f}秒",
                    'critical_errors': summary['critical_errors'],
                    'format_errors': summary['format_errors'],
                    'requirement_errors': summary['requirement_errors']
                })
            
        except Exception as e:
            error_msg = f"拡張YAMLフォーマット検証中にエラーが発生: {str(e)}"
            result['errors'].append(error_msg)
            result['status'] = 'FAIL'
            self.logger.error(error_msg)
        
        return result
    
    def _check_table_existence(self, target_tables: List[str]) -> Dict[str, Any]:
        """テーブル存在整合性チェック"""
        result = {
            'check_name': 'table_existence',
            'description': 'テーブル存在整合性チェック',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        for table_name in target_tables:
            table_result = {
                'table_name': table_name,
                'yaml_exists': False,
                'ddl_exists': False,
                'markdown_exists': False
            }
            
            # YAMLファイル存在チェック
            yaml_file = self.config.table_details_dir / f"{table_name}_details.yaml"
            table_result['yaml_exists'] = yaml_file.exists()
            
            # DDLファイル存在チェック
            ddl_file = self.config.ddl_dir / f"{table_name}.sql"
            table_result['ddl_exists'] = ddl_file.exists()
            
            # Markdownファイル存在チェック
            markdown_files = list(self.config.tables_dir.glob(f"テーブル定義書_{table_name}_*.md"))
            table_result['markdown_exists'] = len(markdown_files) > 0
            
            # エラーチェック
            if not table_result['yaml_exists']:
                error_msg = f"{table_name}: YAML詳細定義ファイルが存在しません"
                result['errors'].append(error_msg)
                result['status'] = 'FAIL'
            
            if not table_result['ddl_exists']:
                error_msg = f"{table_name}: DDLファイルが存在しません"
                result['errors'].append(error_msg)
                result['status'] = 'FAIL'
            
            if not table_result['markdown_exists']:
                warning_msg = f"{table_name}: Markdownファイルが存在しません"
                result['warnings'].append(warning_msg)
                if result['status'] == 'PASS':
                    result['status'] = 'WARNING'
            
            result['details'].append(table_result)
        
        return result
    
    def _check_column_consistency(self, target_tables: List[str]) -> Dict[str, Any]:
        """カラム定義整合性チェック"""
        result = {
            'check_name': 'column_consistency',
            'description': 'カラム定義整合性チェック',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        for table_name in target_tables:
            try:
                # YAMLファイル読み込み
                yaml_file = self.config.table_details_dir / f"{table_name}_details.yaml"
                if not yaml_file.exists():
                    continue
                
                yaml_table_def = self.yaml_parser.parse(yaml_file)
                
                # DDLファイル読み込み
                ddl_file = self.config.ddl_dir / f"{table_name}.sql"
                if not ddl_file.exists():
                    continue
                
                ddl_table_defs = self.ddl_parser.parse(ddl_file)
                
                # DDLパーサーはリストを返すので、対象テーブルを検索
                ddl_table_def = None
                for table_def in ddl_table_defs:
                    if table_def.table_name == table_name:
                        ddl_table_def = table_def
                        break
                
                if ddl_table_def is None:
                    error_msg = f"{table_name}: DDLファイルに該当テーブルの定義が見つかりません"
                    result['errors'].append(error_msg)
                    result['status'] = 'FAIL'
                    continue
                
                # カラム比較
                yaml_columns = {col.name: col for col in yaml_table_def.columns}
                ddl_columns = {col.name: col for col in ddl_table_def.columns}
                
                table_result = {
                    'table_name': table_name,
                    'column_mismatches': []
                }
                
                # YAMLにあってDDLにないカラム
                for col_name in yaml_columns:
                    if col_name not in ddl_columns:
                        error_msg = f"{table_name}.{col_name}: DDLに定義されていません"
                        result['errors'].append(error_msg)
                        result['status'] = 'FAIL'
                        table_result['column_mismatches'].append({
                            'column': col_name,
                            'issue': 'missing_in_ddl'
                        })
                
                # DDLにあってYAMLにないカラム
                for col_name in ddl_columns:
                    if col_name not in yaml_columns:
                        error_msg = f"{table_name}.{col_name}: YAMLに定義されていません"
                        result['errors'].append(error_msg)
                        result['status'] = 'FAIL'
                        table_result['column_mismatches'].append({
                            'column': col_name,
                            'issue': 'missing_in_yaml'
                        })
                
                # 共通カラムの詳細比較
                for col_name in yaml_columns:
                    if col_name in ddl_columns:
                        yaml_col = yaml_columns[col_name]
                        ddl_col = ddl_columns[col_name]
                        
                        # データ型比較（DDLパーサーはtype属性、YAMLパーサーはdata_type属性を使用）
                        yaml_type = getattr(yaml_col, 'data_type', getattr(yaml_col, 'type', ''))
                        ddl_type = getattr(ddl_col, 'type', getattr(ddl_col, 'data_type', ''))
                        
                        if yaml_type != ddl_type:
                            error_msg = f"{table_name}.{col_name}: データ型不一致 YAML({yaml_type}) ≠ DDL({ddl_type})"
                            result['errors'].append(error_msg)
                            result['status'] = 'FAIL'
                            table_result['column_mismatches'].append({
                                'column': col_name,
                                'issue': 'data_type_mismatch',
                                'yaml_type': yaml_type,
                                'ddl_type': ddl_type
                            })
                        
                        # NULL制約比較
                        if yaml_col.nullable != ddl_col.nullable:
                            error_msg = f"{table_name}.{col_name}: NULL制約不一致 YAML({yaml_col.nullable}) ≠ DDL({ddl_col.nullable})"
                            result['errors'].append(error_msg)
                            result['status'] = 'FAIL'
                            table_result['column_mismatches'].append({
                                'column': col_name,
                                'issue': 'nullable_mismatch',
                                'yaml_nullable': yaml_col.nullable,
                                'ddl_nullable': ddl_col.nullable
                            })
                
                result['details'].append(table_result)
                
            except Exception as e:
                error_msg = f"{table_name}: カラム整合性チェック中にエラー - {str(e)}"
                result['errors'].append(error_msg)
                result['status'] = 'FAIL'
        
        return result
    
    def _check_foreign_key_consistency(self, target_tables: List[str]) -> Dict[str, Any]:
        """外部キー整合性チェック"""
        result = {
            'check_name': 'foreign_key_consistency',
            'description': '外部キー整合性チェック',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        # 実装は簡略化（実際の実装では外部キー制約の詳細チェックを行う）
        for table_name in target_tables:
            try:
                yaml_file = self.config.table_details_dir / f"{table_name}_details.yaml"
                if not yaml_file.exists():
                    continue
                
                yaml_table_def = self.yaml_parser.parse(yaml_file)
                
                table_result = {
                    'table_name': table_name,
                    'foreign_key_issues': []
                }
                
                # 外部キー制約チェック
                for fk in yaml_table_def.foreign_keys:
                    # 参照先テーブルの存在確認
                    ref_table_yaml = self.config.table_details_dir / f"{fk.references_table}_details.yaml"
                    if not ref_table_yaml.exists():
                        error_msg = f"{table_name}: 外部キー参照先テーブル '{fk.references_table}' が存在しません"
                        result['errors'].append(error_msg)
                        result['status'] = 'FAIL'
                        table_result['foreign_key_issues'].append({
                            'constraint_name': fk.name,
                            'issue': 'missing_reference_table',
                            'reference_table': fk.references_table
                        })
                
                result['details'].append(table_result)
                
            except Exception as e:
                error_msg = f"{table_name}: 外部キー整合性チェック中にエラー - {str(e)}"
                result['errors'].append(error_msg)
                result['status'] = 'FAIL'
        
        return result
    
    def _check_data_type_consistency(self, target_tables: List[str]) -> Dict[str, Any]:
        """データ型整合性チェック"""
        result = {
            'check_name': 'data_type_consistency',
            'description': 'データ型整合性チェック',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        # カラム整合性チェックに含まれるため、ここでは簡略化
        result['details'].append({
            'note': 'データ型整合性はカラム整合性チェックに含まれます'
        })
        
        return result
    
    def _check_naming_convention(self, target_tables: List[str]) -> Dict[str, Any]:
        """命名規則チェック"""
        result = {
            'check_name': 'naming_convention',
            'description': '命名規則チェック',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        valid_prefixes = ['MST_', 'TRN_', 'HIS_', 'SYS_', 'WRK_', 'IF_']
        
        for table_name in target_tables:
            table_result = {
                'table_name': table_name,
                'naming_issues': []
            }
            
            # テーブル名プレフィックスチェック
            if not any(table_name.startswith(prefix) for prefix in valid_prefixes):
                error_msg = f"{table_name}: 無効なテーブル名プレフィックス（有効: {', '.join(valid_prefixes)}）"
                result['errors'].append(error_msg)
                result['status'] = 'FAIL'
                table_result['naming_issues'].append({
                    'issue': 'invalid_table_prefix',
                    'expected_prefixes': valid_prefixes
                })
            
            result['details'].append(table_result)
        
        return result


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description='データベース整合性チェックツール - 共通ライブラリ対応版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全テーブルチェック
  python run_check.py
  
  # 個別テーブルチェック
  python run_check.py --tables MST_Employee,MST_Department
  
  # 特定チェックのみ実行
  python run_check.py --checks table_existence,column_consistency
  
  # 詳細ログ出力
  python run_check.py --verbose
        """
    )
    
    parser.add_argument(
        '--tables', '-t',
        type=str,
        help='チェック対象テーブル名（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--checks', '-c',
        type=str,
        help='実行するチェック（カンマ区切りで複数指定可能）\n利用可能: yaml_format,yaml_format_enhanced,table_existence,column_consistency,foreign_key_consistency,data_type_consistency,naming_convention'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='設定ファイルパス（デフォルト: config.yaml）'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細ログ出力'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['text', 'json', 'markdown'],
        default='text',
        help='出力形式（デフォルト: text）'
    )
    
    parser.add_argument(
        '--output-file', '-o',
        type=str,
        help='結果出力ファイル'
    )
    
    parser.add_argument(
        '--generate-sample-data',
        action='store_true',
        help='サンプルデータINSERT文を生成'
    )
    
    parser.add_argument(
        '--validate-sample-data',
        action='store_true',
        help='サンプルデータ検証とINSERT文生成を統合実行'
    )
    
    parser.add_argument(
        '--comprehensive-validation',
        action='store_true',
        help='包括的検証（YAML検証+サンプルデータ生成）を実行'
    )
    
    parser.add_argument(
        '--enhanced-sample-data',
        action='store_true',
        help='改良版サンプルデータINSERT文生成を実行'
    )
    
    args = parser.parse_args()
    
    try:
        # ログ設定
        setup_logger(args.verbose)
        logger = logging.getLogger(__name__)
        
        # 統合設定を使用
        config = get_config()
        
        logger.info("データベース整合性チェック開始（共通ライブラリ対応版）")
        logger.info(f"ベースディレクトリ: {config.base_dir}")
        logger.info(f"YAML詳細定義ディレクトリ: {config.table_details_dir}")
        logger.info(f"DDLディレクトリ: {config.ddl_dir}")
        logger.info(f"テーブル定義書ディレクトリ: {config.tables_dir}")
        
        # チェック対象テーブル決定
        target_tables = None
        if args.tables:
            target_tables = [t.strip() for t in args.tables.split(',')]
        
        # サンプルデータINSERT文生成
        if args.generate_sample_data:
            logger.info("サンプルデータINSERT文生成を開始")
            generation_result = generate_sample_data_sql(target_tables, args.verbose)
            
            if generation_result['success']:
                print(f"\n✅ サンプルデータINSERT文生成が完了しました")
                print(f"対象テーブル数: {generation_result['total_tables']}")
                print(f"生成成功テーブル数: {generation_result['generated_tables']}")
                print(f"総レコード数: {generation_result['total_records']}")
                print(f"出力ディレクトリ: docs/design/database/data/")
                
                if generation_result['errors']:
                    print(f"\n⚠️ エラーが発生したテーブル:")
                    for error in generation_result['errors']:
                        print(f"  - {error}")
            else:
                print(f"\n❌ サンプルデータINSERT文生成に失敗しました")
                for error in generation_result['errors']:
                    print(f"  - {error}")
            
            return 0 if generation_result['success'] else 1
        
        # サンプルデータ検証とINSERT文生成の統合実行
        if args.validate_sample_data:
            logger.info("サンプルデータ検証・INSERT文生成 統合実行を開始")
            validation_result = validate_and_generate(target_tables, args.verbose)
            
            if validation_result['overall_success']:
                print(f"\n✅ サンプルデータ検証・INSERT文生成が完了しました")
                print(f"検証: {validation_result['validation']['valid_tables']}/{validation_result['validation']['total_tables']} テーブル成功")
                print(f"生成: {validation_result['generation']['generated_tables']}/{validation_result['generation']['total_tables']} テーブル成功")
                print(f"総レコード数: {validation_result['generation']['total_records']}")
                print(f"出力ディレクトリ: docs/design/database/data/")
            else:
                print(f"\n❌ サンプルデータ検証・INSERT文生成に失敗しました")
                
                if validation_result['validation']['errors']:
                    print(f"\n検証エラー:")
                    for error in validation_result['validation']['errors']:
                        print(f"  - {error}")
                
                if validation_result['generation']['errors']:
                    print(f"\n生成エラー:")
                    for error in validation_result['generation']['errors']:
                        print(f"  - {error}")
            
            return 0 if validation_result['overall_success'] else 1
        
        # 包括的検証（YAML検証+サンプルデータ生成）
        if args.comprehensive_validation:
            logger.info("包括的検証（YAML検証+サンプルデータ生成）を開始")
            try:
                validator = IntegratedValidator(args.verbose)
                comprehensive_result = validator.run_comprehensive_validation(target_tables)
                
                # 結果出力
                output = validator.generate_report(comprehensive_result, args.output_format)
                
                if args.output_file:
                    with open(args.output_file, 'w', encoding='utf-8') as f:
                        f.write(output)
                    logger.info(f"結果を {args.output_file} に出力しました")
                else:
                    print(output)
                
                return 0 if comprehensive_result['success'] else 1
                
            except Exception as e:
                logger.error(f"包括的検証中にエラーが発生: {e}")
                return 1
        
        # 改良版サンプルデータINSERT文生成
        if args.enhanced_sample_data:
            logger.info("改良版サンプルデータINSERT文生成を開始")
            try:
                generator = EnhancedSampleDataGenerator(args.verbose)
                enhanced_result = generator.generate_sample_data_sql(target_tables)
                
                if enhanced_result['success']:
                    print(f"\n✅ 改良版サンプルデータINSERT文生成が完了しました")
                    print(f"対象テーブル数: {enhanced_result['total_tables']}")
                    print(f"生成成功テーブル数: {enhanced_result['generated_tables']}")
                    print(f"総レコード数: {enhanced_result['total_records']}")
                    print(f"実行順序: {', '.join(enhanced_result['execution_order'])}")
                    print(f"出力ディレクトリ: docs/design/database/data/")
                    
                    if enhanced_result['errors']:
                        print(f"\n⚠️ エラーが発生したテーブル:")
                        for error in enhanced_result['errors']:
                            print(f"  - {error}")
                else:
                    print(f"\n❌ 改良版サンプルデータINSERT文生成に失敗しました")
                    for error in enhanced_result['errors']:
                        print(f"  - {error}")
                
                return 0 if enhanced_result['success'] else 1
                
            except Exception as e:
                logger.error(f"改良版サンプルデータ生成中にエラーが発生: {e}")
                return 1
        
        # 特定チェックのみ実行する場合
        if args.checks:
            available_checks = ['yaml_format', 'yaml_format_enhanced', 'table_existence', 'column_consistency', 'foreign_key_consistency', 'data_type_consistency', 'naming_convention']
            requested_checks = [c.strip() for c in args.checks.split(',')]
            
            # 無効なチェック名をフィルタリング
            invalid_checks = [c for c in requested_checks if c not in available_checks]
            if invalid_checks:
                logger.error(f"無効なチェック名: {', '.join(invalid_checks)}")
                logger.error(f"利用可能なチェック: {', '.join(available_checks)}")
                return 1
            
            # 特定チェックのみ実行
            service = ConsistencyCheckService(config)
            results = {
                'total_checks': 0,
                'passed_checks': 0,
                'failed_checks': 0,
                'warnings': 0,
                'errors': [],
                'details': []
            }
            
            check_method_map = {
                'yaml_format': service._check_yaml_format,
                'yaml_format_enhanced': service._check_yaml_format_enhanced,
                'table_existence': service._check_table_existence,
                'column_consistency': service._check_column_consistency,
                'foreign_key_consistency': service._check_foreign_key_consistency,
                'data_type_consistency': service._check_data_type_consistency,
                'naming_convention': service._check_naming_convention
            }
            
            for check_name in requested_checks:
                logger.info(f"チェック実行: {check_name}")
                check_result = check_method_map[check_name](target_tables or [])
                results['details'].append(check_result)
                results['total_checks'] += 1
                
                if check_result['status'] == 'PASS':
                    results['passed_checks'] += 1
                elif check_result['status'] == 'FAIL':
                    results['failed_checks'] += 1
                    results['errors'].extend(check_result.get('errors', []))
                elif check_result['status'] == 'WARNING':
                    results['warnings'] += 1
        else:
            # 全チェック実行
            service = ConsistencyCheckService(config)
            results = service.run_all_checks(target_tables)
        
        # 結果出力
        if args.output_format == 'text':
            print(f"\n=== データベース整合性チェック結果 ===")
            print(f"総チェック数: {results['total_checks']}")
            print(f"成功: {results['passed_checks']}")
            print(f"失敗: {results['failed_checks']}")
            print(f"警告: {results['warnings']}")
            
            if results['errors']:
                print(f"\n=== エラー詳細 ===")
                for error in results['errors']:
                    print(f"❌ {error}")
            
            if results['failed_checks'] == 0 and results['warnings'] == 0:
                print(f"\n✅ すべてのチェックが正常に完了しました")
            elif results['failed_checks'] == 0:
                print(f"\n⚠️ 警告がありますが、重大な問題はありません")
            else:
                print(f"\n❌ 整合性エラーが検出されました")
        
        # ファイル出力
        if args.output_file:
            output_path = Path(args.output_file)
            if args.output_format == 'json':
                import json
                output_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
            else:
                # テキスト形式で出力
                output_content = f"データベース整合性チェック結果\n"
                output_content += f"総チェック数: {results['total_checks']}\n"
                output_content += f"成功: {results['passed_checks']}\n"
                output_content += f"失敗: {results['failed_checks']}\n"
                output_content += f"警告: {results['warnings']}\n\n"
                
                if results['errors']:
                    output_content += "エラー詳細:\n"
                    for error in results['errors']:
                        output_content += f"- {error}\n"
                
                output_path.write_text(output_content, encoding='utf-8')
            
            logger.info(f"結果をファイルに出力: {output_path}")
        
        logger.info("データベース整合性チェック完了")
        return 0 if results['failed_checks'] == 0 else 1
        
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
