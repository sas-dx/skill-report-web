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
from docs.design.database.tools.shared.core.config import Config
from docs.design.database.tools.shared.parsers.yaml_parser import YamlParser
from docs.design.database.tools.shared.parsers.ddl_parser import DDLParser
from docs.design.database.tools.shared.parsers.markdown_parser import MarkdownParser
from docs.design.database.tools.shared.core.exceptions import (
    DatabaseToolsError, 
    ParsingError, 
    ValidationError
)


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
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # パーサーの初期化
        self.yaml_parser = YamlParser(config.to_dict())
        self.ddl_parser = DDLParser(config.to_dict())
        self.markdown_parser = MarkdownParser(config.to_dict())
        
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
                yaml_files = list(self.config.yaml_dir.glob("*_details.yaml"))
                target_tables = [f.stem.replace("_details", "") for f in yaml_files]
            
            if not target_tables:
                self.logger.warning("チェック対象テーブルが見つかりません")
                return results
            
            self.logger.info(f"チェック対象テーブル: {', '.join(target_tables)}")
            
            # 各チェック実行
            check_methods = [
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
            yaml_file = self.config.yaml_dir / f"{table_name}_details.yaml"
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
                yaml_file = self.config.yaml_dir / f"{table_name}_details.yaml"
                if not yaml_file.exists():
                    continue
                
                yaml_table_def = self.yaml_parser.parse_file(yaml_file)
                
                # DDLファイル読み込み
                ddl_file = self.config.ddl_dir / f"{table_name}.sql"
                if not ddl_file.exists():
                    continue
                
                ddl_table_def = self.ddl_parser.parse_file(ddl_file)
                
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
                        
                        # データ型比較
                        if yaml_col.data_type != ddl_col.data_type:
                            error_msg = f"{table_name}.{col_name}: データ型不一致 YAML({yaml_col.data_type}) ≠ DDL({ddl_col.data_type})"
                            result['errors'].append(error_msg)
                            result['status'] = 'FAIL'
                            table_result['column_mismatches'].append({
                                'column': col_name,
                                'issue': 'data_type_mismatch',
                                'yaml_type': yaml_col.data_type,
                                'ddl_type': ddl_col.data_type
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
                yaml_file = self.config.yaml_dir / f"{table_name}_details.yaml"
                if not yaml_file.exists():
                    continue
                
                yaml_table_def = self.yaml_parser.parse_file(yaml_file)
                
                table_result = {
                    'table_name': table_name,
                    'foreign_key_issues': []
                }
                
                # 外部キー制約チェック
                for fk in yaml_table_def.foreign_keys:
                    # 参照先テーブルの存在確認
                    ref_table_yaml = self.config.yaml_dir / f"{fk.references_table}_details.yaml"
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
        help='実行するチェック（カンマ区切りで複数指定可能）'
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
    
    args = parser.parse_args()
    
    try:
        # ログ設定
        setup_logger(args.verbose)
        logger = logging.getLogger(__name__)
        
        # 設定読み込み
        config_path = Path(args.config)
        if not config_path.exists():
            # デフォルト設定ファイルパスを試行
            default_config = Path(__file__).parent / 'config.yaml'
            if default_config.exists():
                config_path = default_config
            else:
                config = Config()
                config_path = None
        
        if config_path:
            config = Config.from_yaml(config_path)
        else:
            config = Config()
        
        # 出力ディレクトリの設定
        if not hasattr(config, 'ddl_dir'):
            config.ddl_dir = config.output_dir / 'ddl'
        if not hasattr(config, 'tables_dir'):
            config.tables_dir = config.output_dir / 'tables'
        
        logger.info("データベース整合性チェック開始（共通ライブラリ対応版）")
        if config_path:
            logger.info(f"設定ファイル: {config_path}")
        logger.info(f"YAML詳細定義ディレクトリ: {config.yaml_dir}")
        logger.info(f"出力ディレクトリ: {config.output_dir}")
        
        # チェック対象テーブル決定
        target_tables = None
        if args.tables:
            target_tables = [t.strip() for t in args.tables.split(',')]
        
        # 整合性チェック実行
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
