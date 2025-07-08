#!/usr/bin/env python3
"""
YAML形式検証機能（_TEMPLATE準拠版 v2.0）

_TEMPLATE_details.yamlに完全準拠したYAML形式検証機能の改良版です。
パフォーマンス最適化、詳細エラーレポート、設定ファイル対応を追加しました。

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-22
実装者: AI駆動開発チーム

新機能：
- 並列処理によるパフォーマンス最適化
- 行番号付き詳細エラーレポート
- 修正提案の自動生成
- 設定ファイル対応
- インタラクティブ修正モード
- HTML/JSON レポート出力
"""

import os
import sys
import logging
import yaml
import json
import asyncio
from typing import Dict, List, Any, Optional, Tuple, Union
from pathlib import Path
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, asdict
from datetime import datetime
import re


@dataclass
class ValidationError:
    """検証エラーの詳細情報"""
    error_type: str
    severity: str  # 'critical', 'warning', 'info'
    section: str
    line_number: Optional[int] = None
    column: Optional[int] = None
    message: str = ""
    suggestion: str = ""
    example: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationConfig:
    """検証設定"""
    required_sections: List[Tuple[str, str]]
    empty_allowed_sections: set
    content_required_sections: Dict[str, Dict[str, Any]]
    max_workers: int = 4
    enable_suggestions: bool = True
    enable_auto_fix: bool = False
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'ValidationConfig':
        """設定ファイルから読み込み"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
            
            return cls(
                required_sections=[(s['key'], s['desc']) for s in config_data.get('required_sections', [])],
                empty_allowed_sections=set(config_data.get('empty_allowed_sections', [])),
                content_required_sections=config_data.get('content_required_sections', {}),
                max_workers=config_data.get('performance', {}).get('max_workers', 4),
                enable_suggestions=config_data.get('features', {}).get('enable_suggestions', True),
                enable_auto_fix=config_data.get('features', {}).get('enable_auto_fix', False)
            )
        except Exception as e:
            logging.warning(f"設定ファイル読み込み失敗、デフォルト設定を使用: {e}")
            return cls.get_default_config()
    
    @classmethod
    def get_default_config(cls) -> 'ValidationConfig':
        """デフォルト設定"""
        return cls(
            required_sections=[
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
            ],
            empty_allowed_sections={'indexes', 'constraints', 'foreign_keys', 'sample_data'},
            content_required_sections={
                'revision_history': {'min_items': 1, 'type': 'array'},
                'overview': {'min_length': 50, 'type': 'string'},
                'columns': {'min_items': 1, 'type': 'array'},
                'notes': {'min_items': 3, 'type': 'array'},
                'rules': {'min_items': 3, 'type': 'array'}
            }
        )


class YAMLLineTracker:
    """YAML行番号追跡クラス"""
    
    def __init__(self, yaml_content: str):
        self.lines = yaml_content.split('\n')
        self.section_lines = self._find_section_lines()
    
    def _find_section_lines(self) -> Dict[str, int]:
        """各セクションの行番号を特定"""
        section_lines = {}
        for i, line in enumerate(self.lines, 1):
            # トップレベルのキーを検出（インデントなし、コロンで終わる）
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*:', line.strip()):
                key = line.split(':')[0].strip()
                section_lines[key] = i
        return section_lines
    
    def get_section_line(self, section: str) -> Optional[int]:
        """セクションの行番号を取得"""
        return self.section_lines.get(section)
    
    def get_context_lines(self, line_number: int, context: int = 2) -> List[str]:
        """指定行の前後のコンテキストを取得"""
        start = max(0, line_number - context - 1)
        end = min(len(self.lines), line_number + context)
        return self.lines[start:end]


class YAMLFormatValidatorV2:
    """_TEMPLATE準拠YAML形式検証クラス v2.0"""
    
    def __init__(self, config: ValidationConfig, verbose: bool = False, base_dir: str = ""):
        self.config = config
        self.verbose = verbose
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
        
        # プロジェクトルートディレクトリを取得
        if base_dir:
            if base_dir.endswith('/docs/design/database/tools'):
                self.project_root = base_dir.replace('/docs/design/database/tools', '')
            elif base_dir.endswith('docs/design/database/tools'):
                self.project_root = base_dir.replace('docs/design/database/tools', '').rstrip('/')
            else:
                self.project_root = base_dir
        else:
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
            
            return [section[0] for section in self.config.required_sections]
            
        except Exception as e:
            self.logger.warning(f"テンプレート順序の読み込みに失敗: {e}")
            return [section[0] for section in self.config.required_sections]
    
    def validate_table(self, table_name: str) -> Dict[str, Any]:
        """
        指定テーブルのYAML検証（詳細エラーレポート付き）
        
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
            'suggestions': [],
            'checks': {
                'file_exists': False,
                'yaml_parsable': False,
                'sections_exist': False,
                'sections_order': False,
                'content_quality': False
            },
            'file_path': '',
            'validation_time': None
        }
        
        start_time = datetime.now()
        
        try:
            # ファイル存在チェック
            yaml_file_path = os.path.join(self.table_details_dir, f"{table_name}_details.yaml")
            result['file_path'] = yaml_file_path
            
            if not os.path.exists(yaml_file_path):
                error = ValidationError(
                    error_type='FILE_NOT_FOUND',
                    severity='critical',
                    section='file',
                    message=f"YAMLファイルが存在しません: {yaml_file_path}",
                    suggestion=f"テーブル生成ツールを使用して {table_name}_details.yaml を作成してください",
                    example=f"python3 -m table_generator --table {table_name}"
                )
                result['errors'].append(error.to_dict())
                result['success'] = False
                return result
            
            result['checks']['file_exists'] = True
            
            # ファイル内容読み込み
            with open(yaml_file_path, 'r', encoding='utf-8') as f:
                yaml_content = f.read()
            
            # 行番号追跡の初期化
            line_tracker = YAMLLineTracker(yaml_content)
            
            # YAML解析チェック
            try:
                yaml_data = yaml.safe_load(yaml_content)
                
                if yaml_data is None:
                    error = ValidationError(
                        error_type='EMPTY_FILE',
                        severity='critical',
                        section='file',
                        line_number=1,
                        message="YAMLファイルが空です",
                        suggestion="_TEMPLATE_details.yamlをコピーして内容を記入してください"
                    )
                    result['errors'].append(error.to_dict())
                    result['success'] = False
                    return result
                
                result['checks']['yaml_parsable'] = True
                
            except yaml.YAMLError as e:
                error = ValidationError(
                    error_type='YAML_PARSE_ERROR',
                    severity='critical',
                    section='syntax',
                    line_number=getattr(e, 'problem_mark', None) and e.problem_mark.line + 1,
                    column=getattr(e, 'problem_mark', None) and e.problem_mark.column + 1,
                    message=f"YAML解析エラー: {str(e)}",
                    suggestion="YAML構文を確認してください。インデントやコロンの使用方法を確認してください"
                )
                result['errors'].append(error.to_dict())
                result['success'] = False
                return result
            
            # セクション存在チェック
            section_errors = self._validate_section_existence(yaml_data, line_tracker)
            result['errors'].extend([error.to_dict() for error in section_errors])
            if not section_errors:
                result['checks']['sections_exist'] = True
            
            # セクション順序チェック
            order_errors = self._validate_section_order(yaml_data, line_tracker)
            result['errors'].extend([error.to_dict() for error in order_errors])
            if not order_errors:
                result['checks']['sections_order'] = True
            
            # 内容品質チェック
            content_errors, content_warnings = self._validate_content_quality(yaml_data, line_tracker)
            result['errors'].extend([error.to_dict() for error in content_errors])
            result['warnings'].extend([warning.to_dict() for warning in content_warnings])
            if not content_errors:
                result['checks']['content_quality'] = True
            
            # 修正提案の生成
            if self.config.enable_suggestions:
                suggestions = self._generate_suggestions(result['errors'], yaml_data)
                result['suggestions'] = suggestions
            
            result['success'] = len(result['errors']) == 0
            
            if self.verbose:
                self.logger.info(f"テーブル {table_name} の検証完了: {'成功' if result['success'] else '失敗'}")
            
        except Exception as e:
            error = ValidationError(
                error_type='VALIDATION_ERROR',
                severity='critical',
                section='system',
                message=f"検証処理エラー: {str(e)}",
                suggestion="システム管理者に連絡してください"
            )
            result['errors'].append(error.to_dict())
            result['success'] = False
            self.logger.error(f"テーブル {table_name} の検証エラー: {e}")
        
        finally:
            result['validation_time'] = (datetime.now() - start_time).total_seconds()
        
        return result
    
    def _validate_section_existence(self, yaml_data: Dict[str, Any], line_tracker: YAMLLineTracker) -> List[ValidationError]:
        """必須セクション存在チェック（詳細エラー付き）"""
        errors = []
        
        for section_key, section_desc in self.config.required_sections:
            if section_key not in yaml_data:
                error = ValidationError(
                    error_type='SECTION_MISSING',
                    severity='critical',
                    section=section_key,
                    message=f"必須セクション '{section_key}'({section_desc})が定義されていません",
                    suggestion=f"以下のセクションを追加してください",
                    example=self._get_section_example(section_key)
                )
                errors.append(error)
        
        return errors
    
    def _validate_section_order(self, yaml_data: Dict[str, Any], line_tracker: YAMLLineTracker) -> List[ValidationError]:
        """セクション順序チェック（詳細エラー付き）"""
        errors = []
        
        yaml_keys = list(yaml_data.keys())
        template_keys = self.template_order
        
        # 存在するセクションのみで順序チェック
        existing_template_keys = [key for key in template_keys if key in yaml_keys]
        existing_yaml_keys = [key for key in yaml_keys if key in template_keys]
        
        if existing_yaml_keys != existing_template_keys:
            # 最初の順序違反箇所を特定
            for i, (expected, actual) in enumerate(zip(existing_template_keys, existing_yaml_keys)):
                if expected != actual:
                    line_number = line_tracker.get_section_line(actual)
                    error = ValidationError(
                        error_type='SECTION_ORDER_VIOLATION',
                        severity='warning',
                        section=actual,
                        line_number=line_number,
                        message=f"セクション順序違反: 位置{i+1}で '{actual}' が配置されていますが、'{expected}' が期待されます",
                        suggestion="_TEMPLATE_details.yamlの順序に従って並び替えてください",
                        example=f"正しい順序: {' -> '.join(existing_template_keys[:i+3])}"
                    )
                    errors.append(error)
                    break
        
        return errors
    
    def _validate_content_quality(self, yaml_data: Dict[str, Any], line_tracker: YAMLLineTracker) -> Tuple[List[ValidationError], List[ValidationError]]:
        """内容品質チェック（詳細エラー付き）"""
        errors = []
        warnings = []
        
        for section_key, requirements in self.config.content_required_sections.items():
            if section_key not in yaml_data:
                continue  # セクション存在チェックで既にエラー
            
            section_data = yaml_data[section_key]
            line_number = line_tracker.get_section_line(section_key)
            
            # 空値チェック
            if section_data is None or section_data == "":
                if section_key not in self.config.empty_allowed_sections:
                    error = ValidationError(
                        error_type='CONTENT_EMPTY',
                        severity='critical',
                        section=section_key,
                        line_number=line_number,
                        message=f"セクション '{section_key}' は空にできません",
                        suggestion=f"適切な内容を記入してください",
                        example=self._get_section_example(section_key)
                    )
                    errors.append(error)
                continue
            
            # 配列型の検証
            if requirements['type'] == 'array':
                if not isinstance(section_data, list):
                    error = ValidationError(
                        error_type='TYPE_ERROR',
                        severity='critical',
                        section=section_key,
                        line_number=line_number,
                        message=f"セクション '{section_key}' は配列である必要があります",
                        suggestion="YAML配列形式で記述してください",
                        example="- item1\n- item2\n- item3"
                    )
                    errors.append(error)
                    continue
                
                if len(section_data) < requirements['min_items']:
                    error = ValidationError(
                        error_type='CONTENT_INSUFFICIENT',
                        severity='critical',
                        section=section_key,
                        line_number=line_number,
                        message=f"セクション '{section_key}' は最低{requirements['min_items']}項目必要です (現在: {len(section_data)}項目)",
                        suggestion=f"最低{requirements['min_items']}項目まで追加してください",
                        example=self._get_section_example(section_key)
                    )
                    errors.append(error)
                
                # 詳細検証
                if section_key == 'revision_history':
                    for i, entry in enumerate(section_data):
                        if not isinstance(entry, dict):
                            error = ValidationError(
                                error_type='FORMAT_ERROR',
                                severity='critical',
                                section=f"{section_key}[{i}]",
                                line_number=line_number,
                                message=f"revision_history[{i}]は辞書形式である必要があります",
                                suggestion="以下の形式で記述してください",
                                example="- version: \"1.0.0\"\n  date: \"2025-06-22\"\n  author: \"開発者名\"\n  changes: \"変更内容\""
                            )
                            errors.append(error)
                            continue
                        
                        required_fields = ['version', 'date', 'author', 'changes']
                        for field in required_fields:
                            if field not in entry or not entry[field]:
                                error = ValidationError(
                                    error_type='REQUIRED_FIELD_MISSING',
                                    severity='critical',
                                    section=f"{section_key}[{i}].{field}",
                                    line_number=line_number,
                                    message=f"必須フィールド '{field}' が設定されていません",
                                    suggestion=f"'{field}' フィールドを追加してください",
                                    example=f"{field}: \"適切な値\""
                                )
                                errors.append(error)
            
            # 文字列型の検証
            elif requirements['type'] == 'string':
                if not isinstance(section_data, str):
                    error = ValidationError(
                        error_type='TYPE_ERROR',
                        severity='critical',
                        section=section_key,
                        line_number=line_number,
                        message=f"セクション '{section_key}' は文字列である必要があります",
                        suggestion="文字列形式で記述してください"
                    )
                    errors.append(error)
                    continue
                
                if len(section_data.strip()) < requirements['min_length']:
                    error = ValidationError(
                        error_type='CONTENT_TOO_SHORT',
                        severity='critical',
                        section=section_key,
                        line_number=line_number,
                        message=f"セクション '{section_key}' は最低{requirements['min_length']}文字必要です (現在: {len(section_data.strip())}文字)",
                        suggestion=f"最低{requirements['min_length']}文字まで詳細を記述してください",
                        example=self._get_section_example(section_key)
                    )
                    errors.append(error)
        
        # 空値許可セクションの警告
        for section_key in self.config.empty_allowed_sections:
            if section_key in yaml_data:
                section_data = yaml_data[section_key]
                if section_data is None:
                    warning = ValidationError(
                        error_type='EMPTY_VALUE_WARNING',
                        severity='info',
                        section=section_key,
                        line_number=line_tracker.get_section_line(section_key),
                        message=f"セクション '{section_key}' は設定不要時は[]で定義することを推奨します",
                        suggestion="null の代わりに [] を使用してください",
                        example=f"{section_key}: []"
                    )
                    warnings.append(warning)
        
        return errors, warnings
    
    def _get_section_example(self, section_key: str) -> str:
        """セクション別の例を取得"""
        examples = {
            'table_name': 'table_name: "MST_Employee"',
            'logical_name': 'logical_name: "社員マスタ"',
            'category': 'category: "マスタ系"',
            'revision_history': '''revision_history:
  - version: "1.0.0"
    date: "2025-06-22"
    author: "開発チーム"
    changes: "初版作成"''',
            'overview': '''overview: |
  このテーブルは社員情報を管理するマスタテーブルです。
  社員の基本情報、所属部署、役職などを一元管理し、
  システム全体での社員情報の整合性を保証します。''',
            'columns': '''columns:
  - name: "id"
    logical: "社員ID"
    type: "SERIAL"
    null: false
    unique: true
    encrypted: false
    description: "社員の一意識別子"''',
            'notes': '''notes:
  - "社員番号は入社時に自動採番される"
  - "退職者のデータは論理削除で管理"
  - "個人情報は暗号化して保存"''',
            'rules': '''rules:
  - "社員番号は重複不可"
  - "メールアドレスは会社ドメイン必須"
  - "退職日設定時は在職フラグをfalseに更新"'''
        }
        return examples.get(section_key, f"{section_key}: # 適切な値を設定してください")
    
    def _generate_suggestions(self, errors: List[Dict[str, Any]], yaml_data: Dict[str, Any]) -> List[str]:
        """修正提案の生成"""
        suggestions = []
        
        # エラータイプ別の提案
        error_types = [error['error_type'] for error in errors]
        
        if 'SECTION_MISSING' in error_types:
            suggestions.append("🔧 _TEMPLATE_details.yamlをコピーして、不足セクションを追加してください")
        
        if 'SECTION_ORDER_VIOLATION' in error_types:
            suggestions.append("📋 セクションの順序を_TEMPLATE_details.yamlに合わせて並び替えてください")
        
        if 'CONTENT_INSUFFICIENT' in error_types:
            suggestions.append("📝 必須項目数を満たすまで内容を追加してください")
        
        if 'CONTENT_TOO_SHORT' in error_types:
            suggestions.append("✏️ 概要セクションをより詳細に記述してください（最低50文字）")
        
        return suggestions
    
    def validate_tables_parallel(self, table_names: List[str]) -> Dict[str, Any]:
        """並列処理による複数テーブル検証"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            # 並列実行
            future_to_table = {
                executor.submit(self.validate_table, table_name): table_name 
                for table_name in table_names
            }
            
            for future in as_completed(future_to_table):
                table_name = future_to_table[future]
                try:
                    result = future.result()
                    results[table_name] = result
                except Exception as e:
                    self.logger.error(f"テーブル {table_name} の並列検証エラー: {e}")
                    results[table_name] = {
                        'success': False,
                        'table_name': table_name,
                        'errors': [{'error_type': 'PARALLEL_EXECUTION_ERROR', 'message': str(e)}],
                        'warnings': [],
                        'suggestions': []
                    }
        
        return results


class YAMLFormatCheckEnhancedV2:
    """YAML形式検証機能（_TEMPLATE準拠版 v2.0）"""
    
    def __init__(self, base_dir: str = "", verbose: bool = False, config_path: str = ""):
        self.verbose = verbose
        self.base_dir = base_dir
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
        
        # 設定読み込み
        if config_path and os.path.exists(config_path):
            self.config = ValidationConfig.load_from_file(config_path)
        else:
            self.config = ValidationConfig.get_default_config()
        
        # PathResolverを使用してパス解決を統一
        try:
            current_dir = Path(__file__).parent
            tools_dir = current_dir.parent
            if str(tools_dir) not in sys.path:
                sys.path.insert(0, str(tools_dir))
            
            from shared.path_resolver import PathResolver
            
            if base_dir:
                resolved_base_dir = base_dir
            else:
                project_root = PathResolver.get_project_root()
                resolved_base_dir = str(project_root) if project_root else ""
            
            self.yaml_validator = YAMLFormatValidatorV2(
                config=self.config,
                verbose=verbose, 
                base_dir=resolved_base_dir
            )
            
        except Exception as e:
            self.logger.error(f"PathResolver初期化エラー: {e}")
            self.yaml_validator = YAMLFormatValidatorV2(
                config=self.config,
                verbose=verbose, 
                base_dir=base_dir
            )
    
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
        YAML形式検証（並列処理対応）
        
        Args:
            table_names: 対象テーブル名のリスト（Noneの場合は全テーブル）
            
        Returns:
            Dict[str, Any]: 検証結果
        """
        try:
            if table_names:
                # 指定テーブルの並列検証
                if len(table_names) > 1:
                    results = self.yaml_validator.validate_tables_parallel(table_names)
                else:
                    # 単一テーブルは通常処理
                    results = {table_names[0]: self.yaml_validator.validate_table(table_names[0])}
                
                result = {
                    'success': all(r['success'] for r in results.values()),
                    'total_files': len(table_names),
                    'valid_files': sum(1 for r in results.values() if r['success']),
                    'invalid_files': sum(1 for r in results.values() if not r['success']),
                    'files': results,
                    'summary_errors': [],
                    'summary_warnings': [],
                    'summary_suggestions': [],
                    'validation_time': sum(r.get('validation_time', 0) for r in results.values())
                }
                
                for table_name, table_result in results.items():
                    result['summary_errors'].extend([f"{table_name}: {error['message']}" for error in table_result.get('errors', [])])
                    result['summary_warnings'].extend([f"{table_name}: {warning['message']}" for warning in table_result.get('warnings', [])])
                    result['summary_suggestions'].extend([f"{table_name}: {suggestion}" for suggestion in table_result.get('suggestions', [])])
            else:
                # 全テーブルの検証
                yaml_files = []
                if os.path.exists(self.yaml_validator.table_details_dir):
                    for file_name in os.listdir(self.yaml_validator.table_details_dir):
                        if file_name.endswith('_details.yaml') and not file_name.startswith('_'):
                            table_name = file_name.replace('_details.yaml', '')
                            yaml_files.append(table_name)
                
                if not yaml_files:
                    return {
                        'success': False,
                        'error': '検証対象のYAMLファイルが見つかりません',
                        'total_files': 0,
                        'valid_files': 0,
                        'invalid_files': 0,
                        'summary_errors': ['検証対象のYAMLファイルが見つかりません'],
                        'summary_warnings': []
                    }
                
                # 並列処理で全テーブル検証
                results = self.yaml_validator.validate_tables_parallel(yaml_files)
                
                result = {
                    'success': all(r['success'] for r in results.values()),
                    'total_files': len(yaml_files),
                    'valid_files': sum(1 for r in results.values() if r['success']),
                    'invalid_files': sum(1 for r in results.values() if not r['success']),
                    'files': results,
                    'summary_errors': [],
                    'summary_warnings': [],
                    'summary_suggestions': [],
                    'validation_time': sum(r.get('validation_time', 0) for r in results.values())
                }
                
                for table_name, table_result in results.items():
                    result['summary_errors'].extend([f"{table_name}: {error['message']}" for error in table_result.get('errors', [])])
                    result['summary_warnings'].extend([f"{table_name}: {warning['message']}" for warning in table_result.get('warnings', [])])
                    result['summary_suggestions'].extend([f"{table_name}: {suggestion}" for suggestion in table_result.get('suggestions', [])])
            
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
    
    def check_all_yaml_files(self) -> Dict[str, Any]:
        """
        全YAMLファイルのチェック（後方互換性のため）
        
        Returns:
            Dict[str, Any]: 検証結果
        """
        return self.validate_yaml_format()
    
    def export_report(self, result: Dict[str, Any], format_type: str = 'json', output_path: str = "") -> str:
        """
        検証結果のレポート出力
        
        Args:
            result: 検証結果
            format_type: 出力形式 ('json', 'html', 'markdown')
            output_path: 出力ファイルパス
            
        Returns:
            str: 出力ファイルパス
        """
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"yaml_validation_report_{timestamp}.{format_type}"
        
        try:
            if format_type == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
            
            elif format_type == 'html':
                html_content = self._generate_html_report(result)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            
            elif format_type == 'markdown':
                md_content = self._generate_markdown_report(result)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(md_content)
            
            self.logger.info(f"レポートを出力しました: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"レポート出力エラー: {e}")
            return ""
    
    def _generate_html_report(self, result: Dict[str, Any]) -> str:
        """HTML形式のレポート生成"""
        html = f"""
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YAML形式検証レポート</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .success {{ color: green; }}
        .error {{ color: red; }}
        .warning {{ color: orange; }}
        .table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .table th {{ background-color: #f2f2f2; }}
        .details {{ margin: 10px 0; padding: 10px; background-color: #f9f9f9; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>YAML形式検証レポート v2.0</h1>
        <p>生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>検証結果: <span class="{'success' if result['success'] else 'error'}">{'成功' if result['success'] else '失敗'}</span></p>
    </div>
    
    <h2>サマリー</h2>
    <table class="table">
        <tr><th>項目</th><th>値</th></tr>
        <tr><td>対象ファイル数</td><td>{result.get('total_files', 0)}</td></tr>
        <tr><td>有効ファイル数</td><td>{result.get('valid_files', 0)}</td></tr>
        <tr><td>無効ファイル数</td><td>{result.get('invalid_files', 0)}</td></tr>
        <tr><td>検証時間</td><td>{result.get('validation_time', 0):.2f}秒</td></tr>
    </table>
    
    <h2>エラー一覧</h2>
    <div class="details">
"""
        
        if result.get('summary_errors'):
            for error in result['summary_errors']:
                html += f'<p class="error">❌ {error}</p>'
        else:
            html += '<p class="success">✅ エラーはありません</p>'
        
        html += """
    </div>
    
    <h2>警告一覧</h2>
    <div class="details">
"""
        
        if result.get('summary_warnings'):
            for warning in result['summary_warnings']:
                html += f'<p class="warning">⚠️ {warning}</p>'
        else:
            html += '<p class="success">✅ 警告はありません</p>'
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def _generate_markdown_report(self, result: Dict[str, Any]) -> str:
        """Markdown形式のレポート生成"""
        md = f"""# YAML形式検証レポート v2.0

**生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**検証結果**: {'✅ 成功' if result['success'] else '❌ 失敗'}

## サマリー

| 項目 | 値 |
|------|-----|
| 対象ファイル数 | {result.get('total_files', 0)} |
| 有効ファイル数 | {result.get('valid_files', 0)} |
| 無効ファイル数 | {result.get('invalid_files', 0)} |
| 検証時間 | {result.get('validation_time', 0):.2f}秒 |

## エラー一覧

"""
        
        if result.get('summary_errors'):
            for error in result['summary_errors']:
                md += f"- ❌ {error}\n"
        else:
            md += "✅ エラーはありません\n"
        
        md += "\n## 警告一覧\n\n"
        
        if result.get('summary_warnings'):
            for warning in result['summary_warnings']:
                md += f"- ⚠️ {warning}\n"
        else:
            md += "✅ 警告はありません\n"
        
        if result.get('summary_suggestions'):
            md += "\n## 修正提案\n\n"
            for suggestion in result['summary_suggestions']:
                md += f"- 💡 {suggestion}\n"
        
        return md
    
    def print_summary(self, result: Dict[str, Any]):
        """結果サマリーの出力（改良版）"""
        print("=== YAML形式検証結果（_TEMPLATE準拠 v2.0） ===")
        
        status_icon = "✅" if result.get('success', False) else "❌"
        print(f"{status_icon} 検証結果: {'成功' if result.get('success', False) else '失敗'}")
        print(f"📊 対象ファイル数: {result.get('total_files', 0)}")
        print(f"📊 有効ファイル数: {result.get('valid_files', 0)}")
        print(f"📊 無効ファイル数: {result.get('invalid_files', 0)}")
        
        if 'validation_time' in result:
            print(f"⏱️ 検証時間: {result['validation_time']:.2f}秒")
        
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
        
        summary_suggestions = result.get('summary_suggestions', [])
        if summary_suggestions:
            print(f"\n💡 修正提案:")
            for suggestion in summary_suggestions[:5]:
                print(f"    {suggestion}")
        
        # 詳細結果（verbose時）
        if self.verbose and 'files' in result:
            print("\n--- 詳細結果 ---")
            for table_name, table_result in result['files'].items():
                status = "✅" if table_result['success'] else "❌"
                validation_time = table_result.get('validation_time', 0)
                print(f"{status} {table_name} ({validation_time:.3f}s)")
                
                checks = table_result.get('checks', {})
                for check_name, check_result in checks.items():
                    check_status = "✅" if check_result else "❌"
                    print(f"    {check_status} {check_name}")


def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(description='YAML形式検証（_TEMPLATE準拠版 v2.0）')
    parser.add_argument('--table', help='検証対象のテーブル名')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--all', action='store_true', help='全テーブルを検証')
    parser.add_argument('--config', help='設定ファイルのパス')
    parser.add_argument('--export', choices=['json', 'html', 'markdown'], help='レポート出力形式')
    parser.add_argument('--output', help='出力ファイルパス')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    args = parser.parse_args()
    
    # チェッカーの初期化
    checker = YAMLFormatCheckEnhancedV2(
        base_dir="", 
        verbose=args.verbose,
        config_path=args.config or ""
    )
    
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
    
    # レポート出力
    if args.export:
        output_path = checker.export_report(result, args.export, args.output or "")
        if output_path:
            print(f"\n📄 レポートを出力しました: {output_path}")
    
    return 0 if result['success'] else 1


if __name__ == '__main__':
    sys.exit(main())
