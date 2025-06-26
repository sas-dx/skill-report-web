"""
YAML検証モジュール
要求仕様ID: PLT.1-WEB.1

YAML形式のテーブル定義ファイルの検証を行います：
1. 必須セクション検証（revision_history, overview, notes, rules）
2. フォーマット検証
3. データ型検証
4. 命名規則検証
"""

import os
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from core.config import Config
from core.logger import setup_logger
from core.exceptions import DatabaseToolsError


@dataclass
class ValidationResult:
    """検証結果"""
    is_valid: bool
    file_path: str
    errors: List[str]
    warnings: List[str]


class YAMLValidator:
    """YAML検証クラス"""
    
    # 必須セクション（絶対省略禁止）
    REQUIRED_SECTIONS = {
        'revision_history': '改版履歴（最低1エントリ必須）',
        'overview': 'テーブル概要（最低50文字必須）',
        'notes': '特記事項（最低3項目必須）',
        'rules': '業務ルール（最低3項目必須）'
    }
    
    # 推奨セクション
    RECOMMENDED_SECTIONS = {
        'table_name': 'テーブル名',
        'logical_name': '論理名',
        'columns': 'カラム定義',
        'indexes': 'インデックス定義',
        'foreign_keys': '外部キー定義'
    }
    
    def __init__(self, config: Config):
        """初期化"""
        self.config = config
        self.logger = setup_logger(__name__, config.log_level)
        self.yaml_dir = Path(config.table_details_dir)
    
    def validate_all(self, verbose: bool = False) -> bool:
        """全YAMLファイルの検証"""
        self.logger.info("全YAMLファイルの検証を開始します")
        
        if not self.yaml_dir.exists():
            self.logger.error(f"YAMLディレクトリが存在しません: {self.yaml_dir}")
            return False
        
        yaml_files = list(self.yaml_dir.glob("*.yaml"))
        if not yaml_files:
            self.logger.warning(f"YAMLファイルが見つかりません: {self.yaml_dir}")
            return True
        
        all_valid = True
        results = []
        
        for yaml_file in yaml_files:
            result = self._validate_file(yaml_file, verbose)
            results.append(result)
            
            if not result.is_valid:
                all_valid = False
        
        # 結果サマリー
        self._print_summary(results, verbose)
        
        return all_valid
    
    def validate_single(self, table_name: str, verbose: bool = False) -> bool:
        """特定テーブルのYAML検証"""
        self.logger.info(f"テーブル {table_name} のYAML検証を開始します")
        
        yaml_file = self.yaml_dir / f"テーブル詳細定義YAML_{table_name}.yaml"
        
        if not yaml_file.exists():
            self.logger.error(f"YAMLファイルが存在しません: {yaml_file}")
            return False
        
        result = self._validate_file(yaml_file, verbose)
        
        if verbose:
            self._print_result(result)
        
        return result.is_valid
    
    def _validate_file(self, yaml_file: Path, verbose: bool = False) -> ValidationResult:
        """単一YAMLファイルの検証"""
        errors = []
        warnings = []
        
        try:
            # YAMLファイル読み込み
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data is None:
                errors.append("YAMLファイルが空です")
                return ValidationResult(False, str(yaml_file), errors, warnings)
            
            # 必須セクション検証
            self._validate_required_sections(data, errors)
            
            # 各セクションの詳細検証
            self._validate_revision_history(data.get('revision_history'), errors)
            self._validate_overview(data.get('overview'), errors)
            self._validate_notes(data.get('notes'), errors)
            self._validate_rules(data.get('rules'), errors)
            self._validate_columns(data.get('columns'), errors, warnings)
            self._validate_indexes(data.get('indexes'), errors, warnings)
            self._validate_foreign_keys(data.get('foreign_keys'), errors, warnings)
            
            # 推奨セクション確認
            self._check_recommended_sections(data, warnings)
            
        except yaml.YAMLError as e:
            errors.append(f"YAML構文エラー: {e}")
        except Exception as e:
            errors.append(f"ファイル読み込みエラー: {e}")
        
        is_valid = len(errors) == 0
        return ValidationResult(is_valid, str(yaml_file), errors, warnings)
    
    def _validate_required_sections(self, data: Dict[str, Any], errors: List[str]):
        """必須セクション検証"""
        for section, description in self.REQUIRED_SECTIONS.items():
            if section not in data:
                errors.append(f"🔴 必須セクション '{section}' が存在しません ({description})")
            elif not data[section]:
                errors.append(f"🔴 必須セクション '{section}' が空です ({description})")
    
    def _validate_revision_history(self, revision_history: Any, errors: List[str]):
        """改版履歴検証"""
        if not revision_history:
            return
        
        if not isinstance(revision_history, list):
            errors.append("revision_history はリスト形式である必要があります")
            return
        
        if len(revision_history) == 0:
            errors.append("revision_history には最低1つのエントリが必要です")
            return
        
        required_fields = ['version', 'date', 'author', 'changes']
        for i, entry in enumerate(revision_history):
            if not isinstance(entry, dict):
                errors.append(f"revision_history[{i}] は辞書形式である必要があります")
                continue
            
            for field in required_fields:
                if field not in entry or not entry[field]:
                    errors.append(f"revision_history[{i}] に必須フィールド '{field}' がありません")
    
    def _validate_overview(self, overview: Any, errors: List[str]):
        """概要検証"""
        if not overview:
            return
        
        if not isinstance(overview, str):
            errors.append("overview は文字列である必要があります")
            return
        
        # 最低文字数チェック（50文字以上）
        if len(overview.strip()) < 50:
            errors.append(f"overview は最低50文字以上の説明が必要です (現在: {len(overview.strip())}文字)")
    
    def _validate_notes(self, notes: Any, errors: List[str]):
        """特記事項検証"""
        if not notes:
            return
        
        if not isinstance(notes, list):
            errors.append("notes はリスト形式である必要があります")
            return
        
        if len(notes) < 3:
            errors.append(f"notes には最低3つの項目が必要です (現在: {len(notes)}項目)")
        
        for i, note in enumerate(notes):
            if not isinstance(note, str) or not note.strip():
                errors.append(f"notes[{i}] は空でない文字列である必要があります")
    
    def _validate_rules(self, rules: Any, errors: List[str]):
        """業務ルール検証"""
        if not rules:
            return
        
        if not isinstance(rules, list):
            errors.append("rules はリスト形式である必要があります")
            return
        
        if len(rules) < 3:
            errors.append(f"rules には最低3つの項目が必要です (現在: {len(rules)}項目)")
        
        for i, rule in enumerate(rules):
            if not isinstance(rule, str) or not rule.strip():
                errors.append(f"rules[{i}] は空でない文字列である必要があります")
    
    def _validate_columns(self, columns: Any, errors: List[str], warnings: List[str]):
        """カラム定義検証"""
        if not columns:
            warnings.append("columns セクションが定義されていません")
            return
        
        if not isinstance(columns, list):
            errors.append("columns はリスト形式である必要があります")
            return
        
        required_fields = ['name', 'type', 'nullable', 'comment']
        for i, column in enumerate(columns):
            if not isinstance(column, dict):
                errors.append(f"columns[{i}] は辞書形式である必要があります")
                continue
            
            for field in required_fields:
                if field not in column:
                    errors.append(f"columns[{i}] に必須フィールド '{field}' がありません")
            
            # データ型検証
            if 'type' in column and column['type']:
                self._validate_data_type(column['type'], f"columns[{i}].type", errors)
    
    def _validate_indexes(self, indexes: Any, errors: List[str], warnings: List[str]):
        """インデックス定義検証"""
        if not indexes:
            return  # インデックスは任意
        
        if not isinstance(indexes, list):
            errors.append("indexes はリスト形式である必要があります")
            return
        
        for i, index in enumerate(indexes):
            if not isinstance(index, dict):
                errors.append(f"indexes[{i}] は辞書形式である必要があります")
                continue
            
            if 'name' not in index or not index['name']:
                errors.append(f"indexes[{i}] に name が必要です")
            
            if 'columns' not in index or not isinstance(index['columns'], list):
                errors.append(f"indexes[{i}] に columns (リスト) が必要です")
    
    def _validate_foreign_keys(self, foreign_keys: Any, errors: List[str], warnings: List[str]):
        """外部キー定義検証"""
        if not foreign_keys:
            return  # 外部キーは任意
        
        if not isinstance(foreign_keys, list):
            errors.append("foreign_keys はリスト形式である必要があります")
            return
        
        for i, fk in enumerate(foreign_keys):
            if not isinstance(fk, dict):
                errors.append(f"foreign_keys[{i}] は辞書形式である必要があります")
                continue
            
            required_fields = ['name', 'columns', 'references']
            for field in required_fields:
                if field not in fk:
                    errors.append(f"foreign_keys[{i}] に必須フィールド '{field}' がありません")
    
    def _validate_data_type(self, data_type: str, field_name: str, errors: List[str]):
        """データ型検証"""
        valid_types = [
            'INTEGER', 'BIGINT', 'SMALLINT', 'DECIMAL', 'NUMERIC',
            'VARCHAR', 'CHAR', 'TEXT', 'BOOLEAN', 'DATE', 'TIME',
            'TIMESTAMP', 'TIMESTAMPTZ', 'UUID', 'JSON', 'JSONB'
        ]
        
        # 基本型の抽出（括弧内の長さ指定を除去）
        base_type = data_type.split('(')[0].upper()
        
        if base_type not in valid_types:
            errors.append(f"{field_name}: 不正なデータ型 '{data_type}'")
    
    def _check_recommended_sections(self, data: Dict[str, Any], warnings: List[str]):
        """推奨セクション確認"""
        for section, description in self.RECOMMENDED_SECTIONS.items():
            if section not in data:
                warnings.append(f"推奨セクション '{section}' がありません ({description})")
    
    def _print_summary(self, results: List[ValidationResult], verbose: bool):
        """結果サマリー出力"""
        total_files = len(results)
        valid_files = sum(1 for r in results if r.is_valid)
        invalid_files = total_files - valid_files
        
        print(f"\n=== YAML検証結果サマリー ===")
        print(f"総ファイル数: {total_files}")
        print(f"✅ 正常: {valid_files}")
        print(f"❌ エラー: {invalid_files}")
        
        if invalid_files > 0:
            print(f"\n=== エラーファイル一覧 ===")
            for result in results:
                if not result.is_valid:
                    print(f"❌ {Path(result.file_path).name}")
                    if verbose:
                        for error in result.errors:
                            print(f"   - {error}")
        
        if verbose:
            print(f"\n=== 詳細結果 ===")
            for result in results:
                self._print_result(result)
    
    def _print_result(self, result: ValidationResult):
        """個別結果出力"""
        status = "✅ 正常" if result.is_valid else "❌ エラー"
        print(f"\n{status}: {Path(result.file_path).name}")
        
        if result.errors:
            print("  エラー:")
            for error in result.errors:
                print(f"    - {error}")
        
        if result.warnings:
            print("  警告:")
            for warning in result.warnings:
                print(f"    - {warning}")
