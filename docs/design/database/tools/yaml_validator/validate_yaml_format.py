#!/usr/bin/env python3
"""
YAML形式検証ツール（サンプルデータ生成統合版）

テーブル詳細定義YAMLファイルの形式検証を行い、
必要に応じてサンプルデータINSERT文を生成します。

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-21
実装者: AI駆動開発チーム

機能：
- YAML形式の検証
- 必須セクションの存在確認
- サンプルデータINSERT文の生成
- 検証結果の詳細レポート
"""

import os
import sys
import argparse
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# プロジェクトルートディレクトリを取得
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../../.."))

# パスを追加
sys.path.append(os.path.join(PROJECT_ROOT, "docs/design/database/tools"))

try:
    from sample_data_integration import SampleDataIntegration
except ImportError as e:
    print(f"サンプルデータ統合モジュールのインポートに失敗: {e}")
    SampleDataIntegration = None

import yaml


class YAMLFormatValidator:
    """YAML形式検証クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
        
        # 必須セクション定義
        self.required_sections = {
            'table_name': '物理テーブル名',
            'logical_name': '論理テーブル名',
            'category': 'テーブル分類',
            'revision_history': '改版履歴（絶対省略禁止）',
            'overview': 'テーブル概要（絶対省略禁止）',
            'columns': 'カラム定義',
            'notes': '特記事項（絶対省略禁止）',
            'business_rules': '業務ルール（絶対省略禁止）'
        }
        
        # 推奨セクション定義
        self.recommended_sections = {
            'priority': '優先度',
            'requirement_id': '要求仕様ID',
            'indexes': 'インデックス定義',
            'foreign_keys': '外部キー定義',
            'sample_data': 'サンプルデータ'
        }
        
        # サンプルデータ統合機能
        if SampleDataIntegration:
            self.sample_data_integration = SampleDataIntegration(verbose=verbose)
        else:
            self.sample_data_integration = None
    
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
    
    def validate_yaml_file(self, file_path: str) -> Dict[str, Any]:
        """
        YAMLファイルの検証
        
        Args:
            file_path: YAMLファイルのパス
            
        Returns:
            Dict[str, Any]: 検証結果
        """
        result = {
            'file_path': file_path,
            'success': True,
            'errors': [],
            'warnings': [],
            'missing_required': [],
            'missing_recommended': [],
            'yaml_data': None,
            'table_name': None
        }
        
        try:
            # ファイル存在確認
            if not os.path.exists(file_path):
                result['success'] = False
                result['errors'].append(f"ファイルが存在しません: {file_path}")
                return result
            
            # YAML読み込み
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)
            
            if not yaml_data:
                result['success'] = False
                result['errors'].append("YAMLファイルが空または無効です")
                return result
            
            result['yaml_data'] = yaml_data
            result['table_name'] = yaml_data.get('table_name', 'unknown')
            
            # 必須セクションの確認
            for section, description in self.required_sections.items():
                if section not in yaml_data:
                    result['missing_required'].append(f"{section} ({description})")
                    result['success'] = False
                elif not yaml_data[section]:
                    result['missing_required'].append(f"{section} ({description}) - 空の値")
                    result['success'] = False
            
            # 推奨セクションの確認
            for section, description in self.recommended_sections.items():
                if section not in yaml_data:
                    result['missing_recommended'].append(f"{section} ({description})")
                    result['warnings'].append(f"推奨セクション不足: {section}")
            
            # 特別な検証ルール
            self._validate_special_rules(yaml_data, result)
            
            if self.verbose:
                self.logger.info(f"YAML検証完了: {file_path} - {'成功' if result['success'] else '失敗'}")
        
        except yaml.YAMLError as e:
            result['success'] = False
            result['errors'].append(f"YAML構文エラー: {str(e)}")
        except Exception as e:
            result['success'] = False
            result['errors'].append(f"検証エラー: {str(e)}")
        
        return result
    
    def _validate_special_rules(self, yaml_data: Dict[str, Any], result: Dict[str, Any]):
        """特別な検証ルールの適用"""
        
        # revision_historyの詳細チェック
        if 'revision_history' in yaml_data:
            revision_history = yaml_data['revision_history']
            if isinstance(revision_history, list) and len(revision_history) > 0:
                for i, entry in enumerate(revision_history):
                    if not isinstance(entry, dict):
                        result['errors'].append(f"revision_history[{i}]: 辞書形式である必要があります")
                        result['success'] = False
                        continue
                    
                    required_fields = ['version', 'date', 'author', 'changes']
                    for field in required_fields:
                        if field not in entry:
                            result['errors'].append(f"revision_history[{i}]: {field}フィールドが必要です")
                            result['success'] = False
            else:
                result['errors'].append("revision_history: 最低1エントリが必要です")
                result['success'] = False
        
        # overviewの文字数チェック
        if 'overview' in yaml_data:
            overview = yaml_data['overview']
            if isinstance(overview, str) and len(overview.strip()) < 50:
                result['warnings'].append("overview: 50文字以上の記述を推奨します")
        
        # notesの項目数チェック
        if 'notes' in yaml_data:
            notes = yaml_data['notes']
            if isinstance(notes, list) and len(notes) < 3:
                result['warnings'].append("notes: 最低3項目の記述を推奨します")
        
        # business_rulesの項目数チェック
        if 'business_rules' in yaml_data:
            business_rules = yaml_data['business_rules']
            if isinstance(business_rules, list) and len(business_rules) < 3:
                result['warnings'].append("business_rules: 最低3項目の記述を推奨します")
        
        # columnsの検証
        if 'columns' in yaml_data:
            columns = yaml_data['columns']
            if not isinstance(columns, list) or len(columns) == 0:
                result['errors'].append("columns: 最低1つのカラム定義が必要です")
                result['success'] = False
            else:
                for i, column in enumerate(columns):
                    if not isinstance(column, dict):
                        result['errors'].append(f"columns[{i}]: 辞書形式である必要があります")
                        result['success'] = False
                        continue
                    
                    required_fields = ['name', 'type', 'nullable', 'comment']
                    for field in required_fields:
                        if field not in column:
                            result['errors'].append(f"columns[{i}]: {field}フィールドが必要です")
                            result['success'] = False
    
    def validate_table(self, table_name: str) -> Dict[str, Any]:
        """
        テーブル名を指定してYAML検証
        
        Args:
            table_name: テーブル名
            
        Returns:
            Dict[str, Any]: 検証結果
        """
        table_details_dir = os.path.join(PROJECT_ROOT, "docs/design/database/table-details")
        yaml_file = os.path.join(table_details_dir, f"{table_name}_details.yaml")
        
        return self.validate_yaml_file(yaml_file)
    
    def validate_all_tables(self) -> Dict[str, Any]:
        """
        全テーブルのYAML検証
        
        Returns:
            Dict[str, Any]: 検証結果
        """
        table_details_dir = os.path.join(PROJECT_ROOT, "docs/design/database/table-details")
        
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
            # YAMLファイルを検索
            yaml_files = []
            for file_path in Path(table_details_dir).glob("*_details.yaml"):
                if file_path.name != "MST_TEMPLATE_details.yaml":  # テンプレートファイルは除外
                    yaml_files.append(str(file_path))
            
            result['total_files'] = len(yaml_files)
            
            # 各ファイルを検証
            for yaml_file in yaml_files:
                file_result = self.validate_yaml_file(yaml_file)
                table_name = file_result.get('table_name', Path(yaml_file).stem.replace('_details', ''))
                result['files'][table_name] = file_result
                
                if file_result['success']:
                    result['valid_files'] += 1
                else:
                    result['invalid_files'] += 1
                    result['success'] = False
                
                # エラー・警告の集約
                result['summary_errors'].extend([f"{table_name}: {error}" for error in file_result['errors']])
                result['summary_warnings'].extend([f"{table_name}: {warning}" for warning in file_result['warnings']])
            
            if self.verbose:
                self.logger.info(f"全テーブル検証完了: {result['valid_files']}/{result['total_files']}ファイル成功")
        
        except Exception as e:
            result['success'] = False
            result['summary_errors'].append(f"全テーブル検証エラー: {str(e)}")
        
        return result
    
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
        if not self.sample_data_integration:
            return {
                'success': False,
                'error': 'サンプルデータ生成機能が利用できません',
                'generation_available': False
            }
        
        return self.sample_data_integration.validate_and_generate(table_names, output_dir)
    
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
            if table_names:
                # 指定テーブルの検証
                validation_results = {}
                for table_name in table_names:
                    validation_results[table_name] = self.validate_table(table_name)
                
                result['validation_result'] = {
                    'success': all(r['success'] for r in validation_results.values()),
                    'files': validation_results,
                    'total_files': len(table_names),
                    'valid_files': sum(1 for r in validation_results.values() if r['success']),
                    'invalid_files': sum(1 for r in validation_results.values() if not r['success'])
                }
            else:
                # 全テーブルの検証
                result['validation_result'] = self.validate_all_tables()
            
            if not result['validation_result']['success']:
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
    
    def print_validation_summary(self, result: Dict[str, Any]):
        """検証結果サマリーの出力"""
        print("=== YAML形式検証結果 ===")
        
        validation_result = result.get('validation_result', {})
        
        print(f"✅ 検証成功: {validation_result.get('success', False)}")
        print(f"📊 対象ファイル数: {validation_result.get('total_files', 0)}")
        print(f"📊 有効ファイル数: {validation_result.get('valid_files', 0)}")
        print(f"📊 無効ファイル数: {validation_result.get('invalid_files', 0)}")
        
        # エラーサマリー
        summary_errors = validation_result.get('summary_errors', [])
        if summary_errors:
            print(f"❌ エラー数: {len(summary_errors)}")
            for i, error in enumerate(summary_errors[:5], 1):
                print(f"    {i}. {error}")
            if len(summary_errors) > 5:
                print(f"    ... 他 {len(summary_errors) - 5} エラー")
        
        # 警告サマリー
        summary_warnings = validation_result.get('summary_warnings', [])
        if summary_warnings:
            print(f"⚠️ 警告数: {len(summary_warnings)}")
            for i, warning in enumerate(summary_warnings[:3], 1):
                print(f"    {i}. {warning}")
            if len(summary_warnings) > 3:
                print(f"    ... 他 {len(summary_warnings) - 3} 警告")
        
        # サンプルデータ生成結果
        sample_data_result = result.get('sample_data_result', {})
        if sample_data_result:
            print("\n=== サンプルデータ生成結果 ===")
            if self.sample_data_integration:
                self.sample_data_integration.print_summary(sample_data_result)
            else:
                print("❌ サンプルデータ生成機能が利用できません")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='YAML形式検証ツール（サンプルデータ生成統合版）')
    parser.add_argument('--table', help='検証対象のテーブル名')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--all', action='store_true', help='全テーブルを検証')
    parser.add_argument('--check-required-only', action='store_true', help='必須セクションのみチェック')
    parser.add_argument('--generate-sample-data', action='store_true', help='サンプルデータを生成')
    parser.add_argument('--output-dir', help='サンプルデータ出力ディレクトリ')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    args = parser.parse_args()
    
    # バリデーターの初期化
    validator = YAMLFormatValidator(verbose=args.verbose)
    
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
    result = validator.validate_and_generate(
        table_names=table_names,
        output_dir=args.output_dir,
        generate_sample_data=args.generate_sample_data
    )
    
    # 結果表示
    validator.print_validation_summary(result)
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
