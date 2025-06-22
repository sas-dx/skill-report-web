#!/usr/bin/env python3
"""
YAML形式検証機能（_TEMPLATE準拠版）

_TEMPLATE_details.yamlに完全準拠したYAML形式検証機能です。
yaml_validatorから移行され、database_consistency_checkerに統合されました。

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-22
実装者: AI駆動開発チーム

機能：
- _TEMPLATE_details.yamlベースの厳密な検証
- 必須セクション存在確認（11セクション）
- セクション順序チェック
- 内容品質検証
- 詳細エラーレポート
"""

import os
import sys
import logging
import yaml
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import argparse


class YAMLFormatValidator:
    """_TEMPLATE準拠YAML形式検証クラス"""
    
    # _TEMPLATE準拠の必須セクション定義（順序固定）
    REQUIRED_SECTIONS = [
        ('table_name', '物理テーブル名'),
        ('logical_name', '論理テーブル名'),
        ('category', 'テーブル分類'),
        ('revision_history', '改版履歴（🔴絶対省略禁止）'),
        ('overview', 'テーブル概要（🔴絶対省略禁止）'),
        ('columns', 'カラム定義'),
        ('indexes', 'インデックス定義'),
        ('constraints', '制約定義'),
        ('foreign_keys', '外部キー定義'),
        ('sample_data', 'サンプルデータ'),
        ('notes', '特記事項（🔴絶対省略禁止）'),
        ('rules', '業務ルール（🔴絶対省略禁止）')
    ]
    
    # 空値許可セクション（設定不要時は空配列/空文字列で定義）
    EMPTY_ALLOWED_SECTIONS = {
        'indexes', 'constraints', 'foreign_keys', 'sample_data'
    }
    
    # 必須内容検証セクション
    CONTENT_REQUIRED_SECTIONS = {
        'revision_history': {'min_items': 1, 'type': 'array'},
        'overview': {'min_length': 50, 'type': 'string'},
        'columns': {'min_items': 1, 'type': 'array'},
        'notes': {'min_items': 3, 'type': 'array'},
        'rules': {'min_items': 3, 'type': 'array'}
    }
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
        
        # プロジェクトルートディレクトリを取得
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(script_dir, "../../../../.."))
        self.table_details_dir = os.path.join(self.project_root, "docs/design/database/table-details")
        self.template_path = os.path.join(self.table_details_dir, "_TEMPLATE_details.yaml")
        
        # テンプレートから標準順序を読み込み
        self.template_order = self._load_template_order()
    
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
    
    def _load_template_order(self) -> List[str]:
        """_TEMPLATE_details.yamlから標準順序を取得"""
        try:
            if os.path.exists(self.template_path):
                with open(self.template_path, 'r', encoding='utf-8') as f:
                    template_data = yaml.safe_load(f)
                    if template_data:
                        return list(template_data.keys())
            
            # テンプレートが読み込めない場合はデフォルト順序を使用
            return [section[0] for section in self.REQUIRED_SECTIONS]
            
        except Exception as e:
            self.logger.warning(f"テンプレート順序の読み込みに失敗: {e}")
            return [section[0] for section in self.REQUIRED_SECTIONS]
    
    def validate_table(self, table_name: str) -> Dict[str, Any]:
        """
        指定テーブルのYAML検証
        
        Args:
            table_name: テーブル名
            
        Returns:
            Dict[str, Any]: 検証結果
        """
        result = {
            'success': True,
            'table_name': table_name,
            'errors': [],
            'warnings': [],
            'checks': {
                'file_exists': False,
                'yaml_parsable': False,
                'sections_exist': False,
                'sections_order': False,
                'content_quality': False
            }
        }
        
        try:
            # ファイル存在チェック
            yaml_file_path = os.path.join(self.table_details_dir, f"{table_name}_details.yaml")
            
            if not os.path.exists(yaml_file_path):
                result['success'] = False
                result['errors'].append(f"YAMLファイルが存在しません: {yaml_file_path}")
                return result
            
            result['checks']['file_exists'] = True
            
            # YAML解析チェック
            try:
                with open(yaml_file_path, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                
                if yaml_data is None:
                    result['success'] = False
                    result['errors'].append("YAMLファイルが空です")
                    return result
                
                result['checks']['yaml_parsable'] = True
                
            except yaml.YAMLError as e:
                result['success'] = False
                result['errors'].append(f"YAML解析エラー: {str(e)}")
                return result
            
            # セクション存在チェック
            section_errors = self._validate_section_existence(yaml_data)
            if section_errors:
                result['success'] = False
                result['errors'].extend(section_errors)
            else:
                result['checks']['sections_exist'] = True
            
            # セクション順序チェック
            order_errors = self._validate_section_order(yaml_data)
            if order_errors:
                result['success'] = False
                result['errors'].extend(order_errors)
            else:
                result['checks']['sections_order'] = True
            
            # 内容品質チェック
            content_errors, content_warnings = self._validate_content_quality(yaml_data)
            if content_errors:
                result['success'] = False
                result['errors'].extend(content_errors)
            else:
                result['checks']['content_quality'] = True
            
            result['warnings'].extend(content_warnings)
            
            if self.verbose:
                self.logger.info(f"テーブル {table_name} の検証完了: {'成功' if result['success'] else '失敗'}")
            
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"検証処理エラー: {str(e)}")
            self.logger.error(f"テーブル {table_name} の検証エラー: {e}")
        
        return result
    
    def _validate_section_existence(self, yaml_data: Dict[str, Any]) -> List[str]:
        """必須セクション存在チェック"""
        errors = []
        
        for section_key, section_desc in self.REQUIRED_SECTIONS:
            if section_key not in yaml_data:
                errors.append(f"❌ セクション不足: '{section_key}'({section_desc})が定義されていません")
        
        return errors
    
    def _validate_section_order(self, yaml_data: Dict[str, Any]) -> List[str]:
        """セクション順序チェック"""
        errors = []
        
        yaml_keys = list(yaml_data.keys())
        template_keys = self.template_order
        
        # 存在するセクションのみで順序チェック
        existing_template_keys = [key for key in template_keys if key in yaml_keys]
        existing_yaml_keys = [key for key in yaml_keys if key in template_keys]
        
        if existing_yaml_keys != existing_template_keys:
            errors.append("❌ セクション順序違反: _TEMPLATE_details.yamlの順序に従ってください")
            
            # 詳細な順序違反情報
            for i, (expected, actual) in enumerate(zip(existing_template_keys, existing_yaml_keys)):
                if expected != actual:
                    errors.append(f"    位置{i+1}: 期待='{expected}', 実際='{actual}'")
                    break
        
        return errors
    
    def _validate_content_quality(self, yaml_data: Dict[str, Any]) -> Tuple[List[str], List[str]]:
        """内容品質チェック"""
        errors = []
        warnings = []
        
        for section_key, requirements in self.CONTENT_REQUIRED_SECTIONS.items():
            if section_key not in yaml_data:
                continue  # セクション存在チェックで既にエラー
            
            section_data = yaml_data[section_key]
            
            # 空値チェック
            if section_data is None or section_data == "":
                if section_key not in self.EMPTY_ALLOWED_SECTIONS:
                    errors.append(f"❌ 内容不足: '{section_key}'は空にできません")
                continue
            
            # 配列型の検証
            if requirements['type'] == 'array':
                if not isinstance(section_data, list):
                    errors.append(f"❌ 型エラー: '{section_key}'は配列である必要があります")
                    continue
                
                if len(section_data) < requirements['min_items']:
                    errors.append(f"❌ 内容不足: '{section_key}'は最低{requirements['min_items']}項目必要です (現在: {len(section_data)}項目)")
                
                # revision_historyの詳細チェック
                if section_key == 'revision_history':
                    for i, entry in enumerate(section_data):
                        if not isinstance(entry, dict):
                            errors.append(f"❌ 形式エラー: revision_history[{i}]は辞書形式である必要があります")
                            continue
                        
                        required_fields = ['version', 'date', 'author', 'changes']
                        for field in required_fields:
                            if field not in entry or not entry[field]:
                                errors.append(f"❌ 必須フィールド不足: revision_history[{i}].{field}が設定されていません")
                
                # columnsの詳細チェック
                elif section_key == 'columns':
                    for i, column in enumerate(section_data):
                        if not isinstance(column, dict):
                            errors.append(f"❌ 形式エラー: columns[{i}]は辞書形式である必要があります")
                            continue
                        
                        required_fields = ['name', 'logical', 'type', 'null', 'unique', 'encrypted', 'description']
                        for field in required_fields:
                            if field not in column:
                                errors.append(f"❌ 必須フィールド不足: columns[{i}].{field}が設定されていません")
            
            # 文字列型の検証
            elif requirements['type'] == 'string':
                if not isinstance(section_data, str):
                    errors.append(f"❌ 型エラー: '{section_key}'は文字列である必要があります")
                    continue
                
                if len(section_data.strip()) < requirements['min_length']:
                    errors.append(f"❌ 内容不足: '{section_key}'は最低{requirements['min_length']}文字必要です (現在: {len(section_data.strip())}文字)")
        
        # 空値許可セクションの警告
        for section_key in self.EMPTY_ALLOWED_SECTIONS:
            if section_key in yaml_data:
                section_data = yaml_data[section_key]
                if section_data is None:
                    warnings.append(f"⚠️ 空値推奨: '{section_key}'は設定不要時は[]で定義してください")
        
        return errors, warnings
    
    def validate_all_tables(self) -> Dict[str, Any]:
        """全テーブルのYAML検証"""
        result = {
            'success': True,
            'total_files': 0,
            'valid_files': 0,
            'invalid_files': 0,
            'files': {},
            'summary_errors': [],
            'summary_warnings': []
        }
        
        try:
            # YAMLファイル一覧を取得
            yaml_files = []
            if os.path.exists(self.table_details_dir):
                for file_name in os.listdir(self.table_details_dir):
                    if file_name.endswith('_details.yaml') and not file_name.startswith('_'):
                        table_name = file_name.replace('_details.yaml', '')
                        yaml_files.append(table_name)
            
            result['total_files'] = len(yaml_files)
            
            if not yaml_files:
                result['success'] = False
                result['summary_errors'].append("検証対象のYAMLファイルが見つかりません")
                return result
            
            # 各テーブルを検証
            for table_name in sorted(yaml_files):
                table_result = self.validate_table(table_name)
                result['files'][table_name] = table_result
                
                if table_result['success']:
                    result['valid_files'] += 1
                else:
                    result['invalid_files'] += 1
                    result['summary_errors'].extend([f"{table_name}: {error}" for error in table_result['errors']])
                
                result['summary_warnings'].extend([f"{table_name}: {warning}" for warning in table_result['warnings']])
            
            result['success'] = result['invalid_files'] == 0
            
            if self.verbose:
                self.logger.info(f"全テーブル検証完了: {result['valid_files']}/{result['total_files']}ファイル成功")
            
        except Exception as e:
            result['success'] = False
            result['summary_errors'].append(f"全テーブル検証エラー: {str(e)}")
            self.logger.error(f"全テーブル検証エラー: {e}")
        
        return result


class YAMLFormatCheckEnhanced:
    """YAML形式検証機能（_TEMPLATE準拠版）"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
        
        # YAML検証機能
        self.yaml_validator = YAMLFormatValidator(verbose=verbose)
    
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
    
    def validate_yaml_format(self, table_names: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        YAML形式検証
        
        Args:
            table_names: 対象テーブル名のリスト（Noneの場合は全テーブル）
            
        Returns:
            Dict[str, Any]: 検証結果
        """
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
            
            if self.verbose:
                self.logger.info(f"YAML形式検証完了: {result['valid_files']}/{result['total_files']}ファイル成功")
            
            return result
            
        except Exception as e:
            error_msg = f"YAML形式検証に失敗: {str(e)}"
            self.logger.error(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'total_files': 0,
                'valid_files': 0,
                'invalid_files': 0,
                'summary_errors': [error_msg],
                'summary_warnings': []
            }
    
    def print_summary(self, result: Dict[str, Any]):
        """結果サマリーの出力"""
        print("=== YAML形式検証結果（_TEMPLATE準拠） ===")
        
        print(f"✅ 検証成功: {result.get('success', False)}")
        print(f"📊 対象ファイル数: {result.get('total_files', 0)}")
        print(f"📊 有効ファイル数: {result.get('valid_files', 0)}")
        print(f"📊 無効ファイル数: {result.get('invalid_files', 0)}")
        
        summary_errors = result.get('summary_errors', [])
        if summary_errors:
            print(f"\n❌ エラー数: {len(summary_errors)}")
            for i, error in enumerate(summary_errors[:10], 1):
                print(f"    {i}. {error}")
            if len(summary_errors) > 10:
                print(f"    ... 他 {len(summary_errors) - 10} エラー")
        
        summary_warnings = result.get('summary_warnings', [])
        if summary_warnings:
            print(f"\n⚠️ 警告数: {len(summary_warnings)}")
            for i, warning in enumerate(summary_warnings[:5], 1):
                print(f"    {i}. {warning}")
            if len(summary_warnings) > 5:
                print(f"    ... 他 {len(summary_warnings) - 5} 警告")
        
        # 詳細結果（verbose時）
        if self.verbose and 'files' in result:
            print("\n--- 詳細結果 ---")
            for table_name, table_result in result['files'].items():
                status = "✅" if table_result['success'] else "❌"
                print(f"{status} {table_name}")
                
                checks = table_result.get('checks', {})
                for check_name, check_result in checks.items():
                    check_status = "✅" if check_result else "❌"
                    print(f"    {check_status} {check_name}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='YAML形式検証（_TEMPLATE準拠版）')
    parser.add_argument('--table', help='検証対象のテーブル名')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--all', action='store_true', help='全テーブルを検証')
    parser.add_argument('--check-required-only', action='store_true', help='必須セクション不備の詳細確認')
    parser.add_argument('--template-compliance', action='store_true', help='テンプレート準拠チェック')
    parser.add_argument('--order-check', action='store_true', help='順序チェックのみ')
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
    
    # 検証実行
    result = checker.validate_yaml_format(table_names=table_names)
    
    # 結果表示
    checker.print_summary(result)
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
