"""
YAML詳細定義ファイルパーサー
テーブル詳細定義YAMLファイルの解析機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

import yaml
from typing import List, Dict, Any, Optional
from pathlib import Path

from .base_parser import BaseParser
from ..core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition
from ..core.exceptions import ParsingError, ValidationError


class YamlParser(BaseParser):
    """YAML詳細定義ファイルパーサー"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self._required_fields = ['table_name', 'logical_name', 'columns']
        self._optional_fields = ['category', 'priority', 'requirement_id', 'indexes', 'foreign_keys', 'constraints']
    
    def parse(self, source: Any) -> TableDefinition:
        """
        YAML詳細定義ファイルを解析
        
        Args:
            source: YAMLファイルパス または YAML文字列
            
        Returns:
            TableDefinition: テーブル定義オブジェクト
            
        Raises:
            ParsingError: 解析エラー
        """
        self._log_parsing_start(source)
        
        try:
            # YAML データの読み込み
            yaml_data = self._load_yaml_data(source)
            
            # 必須フィールドの検証
            self._validate_required_fields(yaml_data, source)
            
            # TableDefinition オブジェクトの構築
            table_def = self._build_table_definition(yaml_data)
            
            # 検証実行
            if self._validation_enabled:
                validation_results = self.validate(table_def)
                self._log_validation_results(validation_results)
                
                # エラーがある場合は例外発生
                error_results = [r for r in validation_results if r.status == "error"]
                if error_results and self._strict_mode:
                    error_messages = [r.message for r in error_results]
                    raise ValidationError(
                        f"YAML検証エラー: {'; '.join(error_messages)}",
                        details={"validation_errors": error_results}
                    )
            
            self._log_parsing_complete(source, 1)
            return table_def
            
        except yaml.YAMLError as e:
            raise self._handle_parsing_error(e, source, "YAML構文エラー")
        except Exception as e:
            raise self._handle_parsing_error(e, source, "YAML解析エラー")
    
    def _load_yaml_data(self, source: Any) -> Dict[str, Any]:
        """YAML データの読み込み"""
        if isinstance(source, (str, Path)):
            # ファイルパスの場合
            file_path = Path(source)
            if not file_path.exists():
                raise ParsingError(f"YAMLファイルが見つかりません: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # 文字列の場合
            return yaml.safe_load(str(source))
    
    def _validate_required_fields(self, yaml_data: Dict[str, Any], source: Any):
        """必須フィールドの検証"""
        missing_fields = []
        for field in self._required_fields:
            if field not in yaml_data or yaml_data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            raise ParsingError(
                f"必須フィールドが不足しています: {', '.join(missing_fields)}",
                file_path=str(source) if isinstance(source, (str, Path)) else None,
                details={"missing_fields": missing_fields}
            )
    
    def _build_table_definition(self, yaml_data: Dict[str, Any]) -> TableDefinition:
        """TableDefinition オブジェクトの構築"""
        # 基本情報
        table_def = TableDefinition(
            name=yaml_data['table_name'],
            logical_name=yaml_data['logical_name'],
            category=yaml_data.get('category', ''),
            priority=yaml_data.get('priority', ''),
            requirement_id=yaml_data.get('requirement_id', ''),
            comment=yaml_data.get('comment', ''),
            columns=[],
            indexes=[],
            foreign_keys=[]
        )
        
        # カラム定義の構築
        columns_data = yaml_data.get('columns', [])
        for col_data in columns_data:
            column = self._build_column_definition(col_data)
            table_def.columns.append(column)
        
        # インデックス定義の構築
        indexes_data = yaml_data.get('indexes', [])
        for idx_data in indexes_data:
            index = self._build_index_definition(idx_data)
            table_def.indexes.append(index)
        
        # 外部キー定義の構築
        foreign_keys_data = yaml_data.get('foreign_keys', [])
        for fk_data in foreign_keys_data:
            foreign_key = self._build_foreign_key_definition(fk_data)
            table_def.foreign_keys.append(foreign_key)
        
        return table_def
    
    def _build_column_definition(self, col_data: Dict[str, Any]) -> ColumnDefinition:
        """ColumnDefinition オブジェクトの構築"""
        return ColumnDefinition(
            name=col_data.get('name', ''),
            type=col_data.get('type', ''),
            nullable=col_data.get('nullable', True),
            primary_key=col_data.get('primary_key', False),
            unique=col_data.get('unique', False),
            default=col_data.get('default'),
            comment=col_data.get('comment', ''),
            requirement_id=col_data.get('requirement_id', ''),
            length=col_data.get('length'),
            precision=col_data.get('precision'),
            scale=col_data.get('scale')
        )
    
    def _build_index_definition(self, idx_data: Dict[str, Any]) -> IndexDefinition:
        """IndexDefinition オブジェクトの構築"""
        return IndexDefinition(
            name=idx_data.get('name', ''),
            columns=idx_data.get('columns', []),
            unique=idx_data.get('unique', False),
            comment=idx_data.get('comment', ''),
            type=idx_data.get('type', 'btree')
        )
    
    def _build_foreign_key_definition(self, fk_data: Dict[str, Any]) -> ForeignKeyDefinition:
        """ForeignKeyDefinition オブジェクトの構築"""
        references = fk_data.get('references', {})
        
        return ForeignKeyDefinition(
            name=fk_data.get('name', ''),
            columns=fk_data.get('columns', []),
            references=references,
            on_update=fk_data.get('on_update', 'RESTRICT'),
            on_delete=fk_data.get('on_delete', 'RESTRICT')
        )
    
    def _validate_yaml_structure(self, yaml_data: Dict[str, Any]) -> List[str]:
        """YAML構造の詳細検証"""
        errors = []
        
        # カラム定義の検証
        columns = yaml_data.get('columns', [])
        if not isinstance(columns, list):
            errors.append("columns は配列である必要があります")
        else:
            for i, col in enumerate(columns):
                if not isinstance(col, dict):
                    errors.append(f"columns[{i}] は辞書である必要があります")
                    continue
                
                # 必須カラムフィールドの検証
                required_col_fields = ['name', 'type']
                for field in required_col_fields:
                    if field not in col:
                        errors.append(f"columns[{i}] に必須フィールド '{field}' がありません")
        
        # インデックス定義の検証
        indexes = yaml_data.get('indexes', [])
        if indexes and not isinstance(indexes, list):
            errors.append("indexes は配列である必要があります")
        
        # 外部キー定義の検証
        foreign_keys = yaml_data.get('foreign_keys', [])
        if foreign_keys and not isinstance(foreign_keys, list):
            errors.append("foreign_keys は配列である必要があります")
        
        return errors
    
    def validate(self, result: TableDefinition) -> List:
        """YAML固有の検証を追加"""
        # 基底クラスの検証を実行
        validation_results = super().validate(result)
        
        # YAML固有の検証を追加
        yaml_specific_results = self._validate_yaml_specific(result)
        validation_results.extend(yaml_specific_results)
        
        return validation_results
    
    def _validate_yaml_specific(self, table: TableDefinition) -> List:
        """YAML固有の検証"""
        from ..core.models import CheckResult
        
        results = []
        
        # テーブル命名規則の検証
        if not table.name.isupper():
            results.append(CheckResult(
                check_type="yaml_validation",
                table_name=table.name,
                status="warning",
                message="テーブル名は大文字で記述することを推奨します",
                details={"table": table.name}
            ))
        
        # プレフィックスの検証
        valid_prefixes = ['MST_', 'TRN_', 'HIS_', 'SYS_', 'WRK_', 'IF_']
        if not any(table.name.startswith(prefix) for prefix in valid_prefixes):
            results.append(CheckResult(
                check_type="yaml_validation",
                table_name=table.name,
                status="warning",
                message=f"テーブル名は適切なプレフィックス ({', '.join(valid_prefixes)}) で始めることを推奨します",
                details={"table": table.name, "valid_prefixes": valid_prefixes}
            ))
        
        # 要求仕様IDの検証
        if not table.requirement_id:
            results.append(CheckResult(
                check_type="yaml_validation",
                table_name=table.name,
                status="warning",
                message="要求仕様IDが設定されていません",
                details={"table": table.name}
            ))
        
        # カラムの要求仕様ID検証
        for column in table.columns:
            if not column.requirement_id:
                results.append(CheckResult(
                    check_type="yaml_validation",
                    table_name=table.name,
                    status="info",
                    message="カラムに要求仕様IDが設定されていません",
                    details={"table": table.name, "column": column.name}
                ))
        
        return results


# パーサーファクトリーへの登録
from .base_parser import ParserFactory
ParserFactory.register_parser('.yaml', YamlParser)
ParserFactory.register_parser('.yml', YamlParser)


# 便利関数
def parse_yaml_file(file_path: str, config=None, validate: bool = True) -> TableDefinition:
    """
    YAML詳細定義ファイルを解析する便利関数
    
    Args:
        file_path: YAMLファイルパス
        config: 設定オブジェクト
        validate: 検証を実行するかどうか
        
    Returns:
        TableDefinition: テーブル定義オブジェクト
        
    Raises:
        ParsingError: 解析エラー
    """
    parser = YamlParser(config)
    parser.set_validation_enabled(validate)
    return parser.parse(file_path)


def parse_yaml_string(yaml_string: str, config=None, validate: bool = True) -> TableDefinition:
    """
    YAML文字列を解析する便利関数
    
    Args:
        yaml_string: YAML文字列
        config: 設定オブジェクト
        validate: 検証を実行するかどうか
        
    Returns:
        TableDefinition: テーブル定義オブジェクト
        
    Raises:
        ParsingError: 解析エラー
    """
    parser = YamlParser(config)
    parser.set_validation_enabled(validate)
    return parser.parse(yaml_string)
