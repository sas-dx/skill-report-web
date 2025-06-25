"""
統合バリデーションシステム
全ツールで使用する共通バリデーション機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-25
実装者: AI駆動開発チーム
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Union, Tuple
from datetime import datetime

from ..core.exceptions import ValidationError, YamlFormatError
from ..core.logger import get_logger

logger = get_logger(__name__)


class ValidationResult:
    """バリデーション結果クラス"""
    
    def __init__(self):
        self.is_valid = True
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.suggestions: List[str] = []
    
    def add_error(
        self, 
        message: str, 
        field: Optional[str] = None,
        value: Optional[Any] = None,
        error_code: Optional[str] = None
    ):
        """エラーを追加"""
        self.is_valid = False
        self.errors.append({
            'message': message,
            'field': field,
            'value': str(value) if value is not None else None,
            'error_code': error_code or 'VALIDATION_ERROR',
            'timestamp': datetime.now().isoformat()
        })
    
    def add_warning(
        self, 
        message: str, 
        field: Optional[str] = None,
        value: Optional[Any] = None
    ):
        """警告を追加"""
        self.warnings.append({
            'message': message,
            'field': field,
            'value': str(value) if value is not None else None,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_suggestion(self, suggestion: str):
        """修正提案を追加"""
        self.suggestions.append(suggestion)
    
    def to_dict(self) -> Dict[str, Any]:
        """結果を辞書形式で取得"""
        return {
            'is_valid': self.is_valid,
            'error_count': len(self.errors),
            'warning_count': len(self.warnings),
            'errors': self.errors,
            'warnings': self.warnings,
            'suggestions': self.suggestions
        }


class YamlValidator:
    """YAML形式バリデーター"""
    
    # 必須セクション定義
    REQUIRED_SECTIONS = {
        'revision_history': {
            'type': list,
            'min_items': 1,
            'description': '改版履歴（絶対省略禁止・最低1エントリ）'
        },
        'overview': {
            'type': str,
            'min_length': 50,
            'description': 'テーブル概要（絶対省略禁止・最低50文字）'
        },
        'notes': {
            'type': list,
            'min_items': 3,
            'description': '特記事項（絶対省略禁止・最低3項目）'
        },
        'rules': {
            'type': list,
            'min_items': 3,
            'description': '業務ルール（絶対省略禁止・最低3項目）'
        }
    }
    
    # 推奨セクション定義
    RECOMMENDED_SECTIONS = {
        'sample_data': {
            'type': list,
            'description': 'サンプルデータ（推奨）'
        }
    }
    
    def __init__(self):
        self.result = ValidationResult()
    
    def validate_yaml_structure(self, data: Dict[str, Any]) -> ValidationResult:
        """
        YAML構造をバリデーション
        
        Args:
            data: YAML内容
            
        Returns:
            ValidationResult: バリデーション結果
        """
        self.result = ValidationResult()
        
        # 必須セクションチェック
        self._validate_required_sections(data)
        
        # 推奨セクションチェック
        self._validate_recommended_sections(data)
        
        # テーブル固有バリデーション
        self._validate_table_specific(data)
        
        return self.result
    
    def _validate_required_sections(self, data: Dict[str, Any]):
        """必須セクションをバリデーション"""
        for section_name, requirements in self.REQUIRED_SECTIONS.items():
            if section_name not in data:
                self.result.add_error(
                    f"必須セクション '{section_name}' が存在しません",
                    field=section_name,
                    error_code="MISSING_REQUIRED_SECTION"
                )
                self.result.add_suggestion(
                    f"{requirements['description']}を追加してください"
                )
                continue
            
            section_data = data[section_name]
            
            # 型チェック
            if requirements['type'] == list and not isinstance(section_data, list):
                self.result.add_error(
                    f"'{section_name}': リスト形式である必要があります",
                    field=section_name,
                    value=type(section_data).__name__,
                    error_code="INVALID_TYPE"
                )
                continue
            
            if requirements['type'] == str and not isinstance(section_data, str):
                self.result.add_error(
                    f"'{section_name}': 文字列形式である必要があります",
                    field=section_name,
                    value=type(section_data).__name__,
                    error_code="INVALID_TYPE"
                )
                continue
            
            # 最小項目数チェック（リスト）
            if (requirements['type'] == list and 
                'min_items' in requirements and 
                len(section_data) < requirements['min_items']):
                self.result.add_error(
                    f"'{section_name}': 最低{requirements['min_items']}項目必要です（現在: {len(section_data)}項目）",
                    field=section_name,
                    value=len(section_data),
                    error_code="INSUFFICIENT_ITEMS"
                )
                self.result.add_suggestion(
                    f"{requirements['description']}に項目を追加してください"
                )
            
            # 最小文字数チェック（文字列）
            if (requirements['type'] == str and 
                'min_length' in requirements and 
                len(section_data.strip()) < requirements['min_length']):
                self.result.add_error(
                    f"'{section_name}': 最低{requirements['min_length']}文字以上の説明が必要です（現在: {len(section_data.strip())}文字）",
                    field=section_name,
                    value=len(section_data.strip()),
                    error_code="INSUFFICIENT_LENGTH"
                )
                self.result.add_suggestion(
                    f"{requirements['description']}をより詳細に記述してください"
                )
    
    def _validate_recommended_sections(self, data: Dict[str, Any]):
        """推奨セクションをバリデーション"""
        for section_name, requirements in self.RECOMMENDED_SECTIONS.items():
            if section_name not in data:
                self.result.add_warning(
                    f"推奨セクション '{section_name}' が存在しません",
                    field=section_name
                )
                self.result.add_suggestion(
                    f"{requirements['description']}の追加を検討してください"
                )
    
    def _validate_table_specific(self, data: Dict[str, Any]):
        """テーブル固有バリデーション"""
        # テーブル名チェック
        if 'table_name' in data:
            self._validate_table_name(data['table_name'])
        
        # カラム定義チェック
        if 'columns' in data:
            self._validate_columns(data['columns'])
        
        # インデックス定義チェック
        if 'indexes' in data:
            self._validate_indexes(data['indexes'])
        
        # 外部キー定義チェック
        if 'foreign_keys' in data:
            self._validate_foreign_keys(data['foreign_keys'])
    
    def _validate_table_name(self, table_name: str):
        """テーブル名をバリデーション"""
        if not table_name:
            self.result.add_error(
                "テーブル名が空です",
                field="table_name",
                error_code="EMPTY_TABLE_NAME"
            )
            return
        
        # 命名規則チェック（例：大文字・アンダースコア）
        if not re.match(r'^[A-Z][A-Z0-9_]*$', table_name):
            self.result.add_warning(
                f"テーブル名 '{table_name}' が命名規則に従っていません（大文字・アンダースコア推奨）",
                field="table_name",
                value=table_name
            )
            self.result.add_suggestion(
                "テーブル名は大文字とアンダースコアで構成してください（例：MST_Employee）"
            )
    
    def _validate_columns(self, columns: List[Dict[str, Any]]):
        """カラム定義をバリデーション"""
        if not isinstance(columns, list):
            self.result.add_error(
                "カラム定義はリスト形式である必要があります",
                field="columns",
                error_code="INVALID_COLUMNS_TYPE"
            )
            return
        
        if not columns:
            self.result.add_error(
                "カラム定義が空です",
                field="columns",
                error_code="EMPTY_COLUMNS"
            )
            return
        
        column_names = set()
        primary_key_count = 0
        
        for i, column in enumerate(columns):
            if not isinstance(column, dict):
                self.result.add_error(
                    f"カラム定義[{i}]は辞書形式である必要があります",
                    field=f"columns[{i}]",
                    error_code="INVALID_COLUMN_TYPE"
                )
                continue
            
            # 必須フィールドチェック
            required_fields = ['name', 'type', 'nullable', 'comment']
            for field in required_fields:
                if field not in column:
                    self.result.add_error(
                        f"カラム定義[{i}]に必須フィールド '{field}' がありません",
                        field=f"columns[{i}].{field}",
                        error_code="MISSING_COLUMN_FIELD"
                    )
            
            # カラム名重複チェック
            if 'name' in column:
                column_name = column['name']
                if column_name in column_names:
                    self.result.add_error(
                        f"カラム名 '{column_name}' が重複しています",
                        field=f"columns[{i}].name",
                        value=column_name,
                        error_code="DUPLICATE_COLUMN_NAME"
                    )
                column_names.add(column_name)
                
                # カラム名命名規則チェック
                if not re.match(r'^[a-z][a-z0-9_]*$', column_name):
                    self.result.add_warning(
                        f"カラム名 '{column_name}' が命名規則に従っていません（小文字・アンダースコア推奨）",
                        field=f"columns[{i}].name",
                        value=column_name
                    )
            
            # 主キーカウント
            if column.get('primary_key', False):
                primary_key_count += 1
        
        # 主キー存在チェック
        if primary_key_count == 0:
            self.result.add_warning(
                "主キーが定義されていません",
                field="columns"
            )
            self.result.add_suggestion(
                "主キーカラムを定義することを推奨します"
            )
    
    def _validate_indexes(self, indexes: List[Dict[str, Any]]):
        """インデックス定義をバリデーション"""
        if not isinstance(indexes, list):
            self.result.add_error(
                "インデックス定義はリスト形式である必要があります",
                field="indexes",
                error_code="INVALID_INDEXES_TYPE"
            )
            return
        
        index_names = set()
        
        for i, index in enumerate(indexes):
            if not isinstance(index, dict):
                self.result.add_error(
                    f"インデックス定義[{i}]は辞書形式である必要があります",
                    field=f"indexes[{i}]",
                    error_code="INVALID_INDEX_TYPE"
                )
                continue
            
            # 必須フィールドチェック
            required_fields = ['name', 'columns']
            for field in required_fields:
                if field not in index:
                    self.result.add_error(
                        f"インデックス定義[{i}]に必須フィールド '{field}' がありません",
                        field=f"indexes[{i}].{field}",
                        error_code="MISSING_INDEX_FIELD"
                    )
            
            # インデックス名重複チェック
            if 'name' in index:
                index_name = index['name']
                if index_name in index_names:
                    self.result.add_error(
                        f"インデックス名 '{index_name}' が重複しています",
                        field=f"indexes[{i}].name",
                        value=index_name,
                        error_code="DUPLICATE_INDEX_NAME"
                    )
                index_names.add(index_name)
    
    def _validate_foreign_keys(self, foreign_keys: List[Dict[str, Any]]):
        """外部キー定義をバリデーション"""
        if not isinstance(foreign_keys, list):
            self.result.add_error(
                "外部キー定義はリスト形式である必要があります",
                field="foreign_keys",
                error_code="INVALID_FOREIGN_KEYS_TYPE"
            )
            return
        
        fk_names = set()
        
        for i, fk in enumerate(foreign_keys):
            if not isinstance(fk, dict):
                self.result.add_error(
                    f"外部キー定義[{i}]は辞書形式である必要があります",
                    field=f"foreign_keys[{i}]",
                    error_code="INVALID_FOREIGN_KEY_TYPE"
                )
                continue
            
            # 必須フィールドチェック
            required_fields = ['name', 'columns', 'references']
            for field in required_fields:
                if field not in fk:
                    self.result.add_error(
                        f"外部キー定義[{i}]に必須フィールド '{field}' がありません",
                        field=f"foreign_keys[{i}].{field}",
                        error_code="MISSING_FOREIGN_KEY_FIELD"
                    )
            
            # 外部キー名重複チェック
            if 'name' in fk:
                fk_name = fk['name']
                if fk_name in fk_names:
                    self.result.add_error(
                        f"外部キー名 '{fk_name}' が重複しています",
                        field=f"foreign_keys[{i}].name",
                        value=fk_name,
                        error_code="DUPLICATE_FOREIGN_KEY_NAME"
                    )
                fk_names.add(fk_name)


class FilePathValidator:
    """ファイルパスバリデーター"""
    
    def __init__(self):
        self.result = ValidationResult()
    
    def validate_file_path(self, file_path: Union[str, Path]) -> ValidationResult:
        """
        ファイルパスをバリデーション
        
        Args:
            file_path: ファイルパス
            
        Returns:
            ValidationResult: バリデーション結果
        """
        self.result = ValidationResult()
        file_path = Path(file_path)
        
        # 存在チェック
        if not file_path.exists():
            self.result.add_error(
                f"ファイルが存在しません: {file_path}",
                field="file_path",
                value=str(file_path),
                error_code="FILE_NOT_FOUND"
            )
            self.result.add_suggestion(
                "ファイルパスが正しいか確認してください"
            )
            return self.result
        
        # ファイル形式チェック
        if file_path.is_dir():
            self.result.add_error(
                f"ディレクトリが指定されています: {file_path}",
                field="file_path",
                value=str(file_path),
                error_code="IS_DIRECTORY"
            )
            return self.result
        
        # 読み取り権限チェック
        if not os.access(file_path, os.R_OK):
            self.result.add_error(
                f"ファイル読み取り権限がありません: {file_path}",
                field="file_path",
                value=str(file_path),
                error_code="NO_READ_PERMISSION"
            )
            self.result.add_suggestion(
                "ファイルの読み取り権限を確認してください"
            )
        
        return self.result


class DataTypeValidator:
    """データ型バリデーター"""
    
    # サポートされるデータ型
    SUPPORTED_TYPES = {
        'VARCHAR', 'CHAR', 'TEXT', 'LONGTEXT',
        'INTEGER', 'BIGINT', 'SMALLINT', 'TINYINT',
        'DECIMAL', 'NUMERIC', 'FLOAT', 'DOUBLE',
        'DATE', 'TIME', 'DATETIME', 'TIMESTAMP',
        'BOOLEAN', 'BOOL',
        'JSON', 'JSONB',
        'BLOB', 'LONGBLOB'
    }
    
    def __init__(self):
        self.result = ValidationResult()
    
    def validate_data_type(self, data_type: str) -> ValidationResult:
        """
        データ型をバリデーション
        
        Args:
            data_type: データ型文字列
            
        Returns:
            ValidationResult: バリデーション結果
        """
        self.result = ValidationResult()
        
        if not data_type:
            self.result.add_error(
                "データ型が空です",
                field="data_type",
                error_code="EMPTY_DATA_TYPE"
            )
            return self.result
        
        # 基本型抽出（括弧内の長さ指定を除去）
        base_type = re.sub(r'\([^)]*\)', '', data_type.upper()).strip()
        
        if base_type not in self.SUPPORTED_TYPES:
            self.result.add_warning(
                f"サポートされていないデータ型: {data_type}",
                field="data_type",
                value=data_type
            )
            self.result.add_suggestion(
                f"サポートされるデータ型: {', '.join(sorted(self.SUPPORTED_TYPES))}"
            )
        
        # 長さ指定チェック
        if '(' in data_type and ')' in data_type:
            length_match = re.search(r'\((\d+)\)', data_type)
            if length_match:
                length = int(length_match.group(1))
                if base_type in ['VARCHAR', 'CHAR'] and length > 65535:
                    self.result.add_warning(
                        f"文字列型の長さが大きすぎます: {length}",
                        field="data_type",
                        value=data_type
                    )
                    self.result.add_suggestion(
                        "長い文字列にはTEXT型の使用を検討してください"
                    )
        
        return self.result


# 統合バリデーション関数
def validate_yaml_file(file_path: Union[str, Path]) -> ValidationResult:
    """
    YAMLファイルを包括的にバリデーション
    
    Args:
        file_path: YAMLファイルパス
        
    Returns:
        ValidationResult: バリデーション結果
    """
    from ..utils.file_utils import get_yaml_manager
    
    # ファイルパスバリデーション
    path_validator = FilePathValidator()
    result = path_validator.validate_file_path(file_path)
    
    if not result.is_valid:
        return result
    
    try:
        # YAMLファイル読み込み
        yaml_manager = get_yaml_manager()
        data = yaml_manager.read_yaml(file_path)
        
        # YAML構造バリデーション
        yaml_validator = YamlValidator()
        yaml_result = yaml_validator.validate_yaml_structure(data)
        
        # 結果統合
        result.errors.extend(yaml_result.errors)
        result.warnings.extend(yaml_result.warnings)
        result.suggestions.extend(yaml_result.suggestions)
        result.is_valid = result.is_valid and yaml_result.is_valid
        
        return result
        
    except Exception as e:
        result.add_error(
            f"YAMLファイル処理エラー: {e}",
            field="file_processing",
            error_code="YAML_PROCESSING_ERROR"
        )
        return result


def validate_table_definition(data: Dict[str, Any]) -> ValidationResult:
    """
    テーブル定義を包括的にバリデーション
    
    Args:
        data: テーブル定義データ
        
    Returns:
        ValidationResult: バリデーション結果
    """
    yaml_validator = YamlValidator()
    return yaml_validator.validate_yaml_structure(data)


def validate_data_types(columns: List[Dict[str, Any]]) -> ValidationResult:
    """
    カラムのデータ型を一括バリデーション
    
    Args:
        columns: カラム定義リスト
        
    Returns:
        ValidationResult: バリデーション結果
    """
    type_validator = DataTypeValidator()
    combined_result = ValidationResult()
    
    for i, column in enumerate(columns):
        if 'type' in column:
            result = type_validator.validate_data_type(column['type'])
            
            # フィールド名を調整
            for error in result.errors:
                error['field'] = f"columns[{i}].type"
            for warning in result.warnings:
                warning['field'] = f"columns[{i}].type"
            
            combined_result.errors.extend(result.errors)
            combined_result.warnings.extend(result.warnings)
            combined_result.suggestions.extend(result.suggestions)
            combined_result.is_valid = combined_result.is_valid and result.is_valid
    
    return combined_result
