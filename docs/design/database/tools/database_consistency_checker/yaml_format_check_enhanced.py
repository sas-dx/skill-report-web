#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAMLフォーマット検証統合モジュール（改良版）

database_consistency_checkerにYAMLフォーマット検証機能を統合し、
サンプルデータINSERT文生成機能も含めた包括的な検証ツールです。

改良点：
- サンプルデータ生成機能の統合
- より詳細な検証レポート
- 統合的なエラーハンドリング
- 実行順序の最適化
"""

import sys
import os
import argparse
import logging
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# 基本パス
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
YAML_VALIDATOR_DIR = os.path.join(BASE_DIR, 'tools/yaml_validator')
sys.path.append(YAML_VALIDATOR_DIR)

# モジュールインポート
try:
    from validate_yaml_format import (
        load_yaml, validate_yaml_structure, TEMPLATE_PATH, TABLE_DETAILS_DIR
    )
    yaml_validator_available = True
except ImportError as e:
    yaml_validator_available = False
    print(f"警告: yaml_validatorモジュールが見つかりません。YAMLフォーマット検証は無効になります。")
    print(f"詳細: {e}")
    print(f"検索パス: {YAML_VALIDATOR_DIR}")

# サンプルデータ生成モジュール
try:
    from sample_data_generator_enhanced import EnhancedSampleDataGenerator
    sample_generator_available = True
except ImportError:
    sample_generator_available = False
    print("警告: sample_data_generator_enhancedモジュールが見つかりません。サンプルデータ生成は無効になります。")


class IntegratedValidator:
    """統合検証クラス"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.logger = self._setup_logger()
    
    def _setup_logger(self) -> logging.Logger:
        """ログ設定"""
        level = logging.DEBUG if self.verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        return logging.getLogger(__name__)
    
    def run_comprehensive_validation(self, tables: Optional[List[str]] = None) -> Dict[str, Any]:
        """包括的な検証を実行"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'success': True,
            'yaml_validation': {},
            'sample_data_generation': {},
            'summary': {},
            'errors': [],
            'warnings': []
        }
        
        self.logger.info("=== 包括的検証開始 ===")
        
        # 1. YAMLフォーマット検証
        if yaml_validator_available:
            self.logger.info("YAMLフォーマット検証を実行中...")
            yaml_results = self._validate_yaml_format(tables)
            results['yaml_validation'] = yaml_results
            
            if not yaml_results.get('success', False):
                results['success'] = False
                results['errors'].extend(yaml_results.get('errors', []))
        else:
            results['warnings'].append("YAMLフォーマット検証がスキップされました（モジュール不足）")
        
        # 2. サンプルデータ生成検証
        if sample_generator_available:
            self.logger.info("サンプルデータ生成検証を実行中...")
            sample_results = self._validate_sample_data_generation(tables)
            results['sample_data_generation'] = sample_results
            
            if not sample_results.get('success', False):
                results['warnings'].extend(sample_results.get('errors', []))
        else:
            results['warnings'].append("サンプルデータ生成検証がスキップされました（モジュール不足）")
        
        # 3. 統合サマリー生成
        results['summary'] = self._generate_summary(results)
        
        self.logger.info("=== 包括的検証完了 ===")
        
        return results
    
    def _validate_yaml_format(self, tables: Optional[List[str]] = None) -> Dict[str, Any]:
        """YAMLフォーマット検証"""
        if not yaml_validator_available:
            return {
                'success': False,
                'error': 'yaml_validatorモジュールが利用できません',
                'results': []
            }
        
        # テンプレートの読み込み
        template_data = load_yaml(TEMPLATE_PATH)
        if not template_data:
            return {
                'success': False,
                'error': 'テンプレートファイルの読み込みに失敗しました',
                'results': []
            }
        
        # 検証対象ファイルの特定
        target_files = self._get_target_files(tables)
        
        # 検証実行
        results = []
        for file_path in target_files:
            yaml_data = load_yaml(file_path)
            if yaml_data:
                result = validate_yaml_structure(yaml_data, template_data, file_path, self.verbose)
                results.append(result)
        
        # 結果サマリー
        valid_count = sum(1 for r in results if r['valid'])
        invalid_count = len(results) - valid_count
        warning_count = sum(1 for r in results if r['warnings'])
        
        return {
            'success': invalid_count == 0,
            'total': len(results),
            'valid': valid_count,
            'invalid': invalid_count,
            'with_warnings': warning_count,
            'results': results,
            'errors': [f"{r['file']}: {', '.join(r['errors'])}" for r in results if not r['valid']]
        }
    
    def _validate_sample_data_generation(self, tables: Optional[List[str]] = None) -> Dict[str, Any]:
        """サンプルデータ生成検証"""
        if not sample_generator_available:
            return {
                'success': False,
                'error': 'sample_data_generator_enhancedモジュールが利用できません',
                'results': {}
            }
        
        try:
            generator = EnhancedSampleDataGenerator(self.verbose)
            results = generator.generate_sample_data_sql(tables)
            return results
        except Exception as e:
            return {
                'success': False,
                'error': f'サンプルデータ生成中にエラーが発生しました: {str(e)}',
                'results': {}
            }
    
    def _get_target_files(self, tables: Optional[List[str]] = None) -> List[str]:
        """検証対象ファイルを取得"""
        target_files = []
        
        if tables:
            for table in tables:
                file_path = os.path.join(TABLE_DETAILS_DIR, f"{table}_details.yaml")
                if os.path.exists(file_path):
                    target_files.append(file_path)
                else:
                    self.logger.warning(f"{file_path} が見つかりません")
        else:
            for filename in os.listdir(TABLE_DETAILS_DIR):
                if filename.endswith('_details.yaml') and filename != 'MST_TEMPLATE_details.yaml':
                    target_files.append(os.path.join(TABLE_DETAILS_DIR, filename))
        
        return target_files
    
    def _generate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """統合サマリーを生成"""
        summary = {
            'overall_success': results['success'],
            'total_errors': len(results['errors']),
            'total_warnings': len(results['warnings']),
            'yaml_validation_status': 'success' if results['yaml_validation'].get('success', False) else 'failed',
            'sample_data_generation_status': 'success' if results['sample_data_generation'].get('success', False) else 'failed',
            'recommendations': []
        }
        
        # 推奨事項の生成
        if results['yaml_validation'].get('invalid', 0) > 0:
            summary['recommendations'].append("YAMLフォーマットエラーを修正してください")
        
        if results['yaml_validation'].get('with_warnings', 0) > 0:
            summary['recommendations'].append("YAML警告を確認し、必要に応じて修正してください")
        
        if not results['sample_data_generation'].get('success', False):
            summary['recommendations'].append("サンプルデータ生成エラーを確認してください")
        
        if results['sample_data_generation'].get('total_records', 0) == 0:
            summary['recommendations'].append("サンプルデータが生成されていません。sample_dataセクションを確認してください")
        
        return summary
    
    def generate_report(self, results: Dict[str, Any], format_type: str = 'text') -> str:
        """検証レポートを生成"""
        if format_type == 'json':
            return json.dumps(results, indent=2, ensure_ascii=False)
        
        elif format_type == 'markdown':
            return self._generate_markdown_report(results)
        
        else:  # text
            return self._generate_text_report(results)
    
    def _generate_text_report(self, results: Dict[str, Any]) -> str:
        """テキスト形式のレポートを生成"""
        report = []
        report.append("=== 包括的検証レポート ===")
        report.append(f"実行日時: {results['timestamp']}")
        report.append(f"総合結果: {'成功' if results['success'] else '失敗'}")
        report.append("")
        
        # YAMLフォーマット検証結果
        yaml_results = results.get('yaml_validation', {})
        if yaml_results:
            report.append("--- YAMLフォーマット検証 ---")
            report.append(f"総ファイル数: {yaml_results.get('total', 0)}")
            report.append(f"有効: {yaml_results.get('valid', 0)}")
            report.append(f"無効: {yaml_results.get('invalid', 0)}")
            report.append(f"警告あり: {yaml_results.get('with_warnings', 0)}")
            report.append("")
        
        # サンプルデータ生成結果
        sample_results = results.get('sample_data_generation', {})
        if sample_results:
            report.append("--- サンプルデータ生成 ---")
            report.append(f"対象テーブル数: {sample_results.get('total_tables', 0)}")
            report.append(f"生成成功テーブル数: {sample_results.get('generated_tables', 0)}")
            report.append(f"総レコード数: {sample_results.get('total_records', 0)}")
            report.append(f"実行順序: {', '.join(sample_results.get('execution_order', []))}")
            report.append("")
        
        # エラー・警告
        if results['errors']:
            report.append("--- エラー ---")
            for error in results['errors']:
                report.append(f"❌ {error}")
            report.append("")
        
        if results['warnings']:
            report.append("--- 警告 ---")
            for warning in results['warnings']:
                report.append(f"⚠️ {warning}")
            report.append("")
        
        # 推奨事項
        summary = results.get('summary', {})
        if summary.get('recommendations'):
            report.append("--- 推奨事項 ---")
            for rec in summary['recommendations']:
                report.append(f"💡 {rec}")
            report.append("")
        
        return "\n".join(report)
    
    def _generate_markdown_report(self, results: Dict[str, Any]) -> str:
        """Markdown形式のレポートを生成"""
        report = []
        report.append("# 包括的検証レポート")
        report.append("")
        report.append(f"**実行日時**: {results['timestamp']}")
        report.append(f"**総合結果**: {'✅ 成功' if results['success'] else '❌ 失敗'}")
        report.append("")
        
        # YAMLフォーマット検証結果
        yaml_results = results.get('yaml_validation', {})
        if yaml_results:
            report.append("## YAMLフォーマット検証")
            report.append("")
            report.append("| 項目 | 値 |")
            report.append("|------|-----|")
            report.append(f"| 総ファイル数 | {yaml_results.get('total', 0)} |")
            report.append(f"| 有効 | {yaml_results.get('valid', 0)} |")
            report.append(f"| 無効 | {yaml_results.get('invalid', 0)} |")
            report.append(f"| 警告あり | {yaml_results.get('with_warnings', 0)} |")
            report.append("")
        
        # サンプルデータ生成結果
        sample_results = results.get('sample_data_generation', {})
        if sample_results:
            report.append("## サンプルデータ生成")
            report.append("")
            report.append("| 項目 | 値 |")
            report.append("|------|-----|")
            report.append(f"| 対象テーブル数 | {sample_results.get('total_tables', 0)} |")
            report.append(f"| 生成成功テーブル数 | {sample_results.get('generated_tables', 0)} |")
            report.append(f"| 総レコード数 | {sample_results.get('total_records', 0)} |")
            report.append(f"| 実行順序 | {', '.join(sample_results.get('execution_order', []))} |")
            report.append("")
        
        # エラー・警告
        if results['errors']:
            report.append("## エラー")
            report.append("")
            for error in results['errors']:
                report.append(f"- ❌ {error}")
            report.append("")
        
        if results['warnings']:
            report.append("## 警告")
            report.append("")
            for warning in results['warnings']:
                report.append(f"- ⚠️ {warning}")
            report.append("")
        
        # 推奨事項
        summary = results.get('summary', {})
        if summary.get('recommendations'):
            report.append("## 推奨事項")
            report.append("")
            for rec in summary['recommendations']:
                report.append(f"- 💡 {rec}")
            report.append("")
        
        return "\n".join(report)


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='包括的YAML検証・サンプルデータ生成ツール（改良版）')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    parser.add_argument('--output-format', choices=['text', 'json', 'markdown'], default='text', help='出力形式')
    parser.add_argument('--output-file', help='結果出力ファイル')
    parser.add_argument('--yaml-only', action='store_true', help='YAMLフォーマット検証のみ実行')
    parser.add_argument('--sample-only', action='store_true', help='サンプルデータ生成のみ実行')
    args = parser.parse_args()
    
    tables = args.tables.split(',') if args.tables else None
    
    validator = IntegratedValidator(args.verbose)
    
    # 実行モードの決定
    if args.yaml_only:
        result = {'yaml_validation': validator._validate_yaml_format(tables)}
        result['success'] = result['yaml_validation'].get('success', False)
    elif args.sample_only:
        result = {'sample_data_generation': validator._validate_sample_data_generation(tables)}
        result['success'] = result['sample_data_generation'].get('success', False)
    else:
        result = validator.run_comprehensive_validation(tables)
    
    # 結果出力
    output = validator.generate_report(result, args.output_format)
    
    if args.output_file:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"結果を {args.output_file} に出力しました")
    else:
        print(output)
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
