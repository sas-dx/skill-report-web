"""
統合データ変換アダプター

全てのデータ変換処理を統一するアダプター
- YAML ↔ DDL ↔ Markdown の相互変換
- データ型変換・正規化
- フォーマット統一
- バリデーション統合
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass
import logging
import re

from ...core.exceptions import ValidationError, DataTransformError
from ...core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition
from ...parsers.yaml_parser import YamlParser
from ...parsers.ddl_parser import DDLParser
from ...parsers.markdown_parser import MarkdownParser
from ...generators.ddl_generator import DDLGenerator
from ...generators.markdown_generator import MarkdownGenerator
from ...generators.sample_data_generator import SampleDataGenerator

logger = logging.getLogger(__name__)


@dataclass
class TransformResult:
    """変換結果"""
    success: bool
    data: Any
    errors: List[str]
    warnings: List[str]


@dataclass
class ValidationResult:
    """バリデーション結果"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


class UnifiedDataTransformAdapter:
    """統合データ変換アダプター"""
    
    def __init__(self):
        """初期化"""
        self.yaml_parser = YamlParser()
        self.ddl_parser = DDLParser()
        self.markdown_parser = MarkdownParser()
        self.ddl_generator = DDLGenerator()
        self.markdown_generator = MarkdownGenerator()
        self.sample_data_generator = SampleDataGenerator()
        
        # データ型マッピング
        self.data_type_mappings = self._initialize_data_type_mappings()
    
    def _initialize_data_type_mappings(self) -> Dict[str, Dict[str, str]]:
        """データ型マッピングを初期化"""
        return {
            'postgresql_to_standard': {
                'SERIAL': 'INTEGER',
                'BIGSERIAL': 'BIGINT',
                'TEXT': 'VARCHAR',
                'BOOLEAN': 'BOOLEAN',
                'TIMESTAMP': 'TIMESTAMP',
                'DATE': 'DATE',
                'TIME': 'TIME',
                'NUMERIC': 'DECIMAL',
                'REAL': 'FLOAT',
                'DOUBLE PRECISION': 'DOUBLE',
                'SMALLINT': 'SMALLINT',
                'INTEGER': 'INTEGER',
                'BIGINT': 'BIGINT'
            },
            'standard_to_postgresql': {
                'INTEGER': 'INTEGER',
                'BIGINT': 'BIGINT',
                'VARCHAR': 'VARCHAR',
                'TEXT': 'TEXT',
                'BOOLEAN': 'BOOLEAN',
                'TIMESTAMP': 'TIMESTAMP',
                'DATE': 'DATE',
                'TIME': 'TIME',
                'DECIMAL': 'NUMERIC',
                'FLOAT': 'REAL',
                'DOUBLE': 'DOUBLE PRECISION',
                'SMALLINT': 'SMALLINT'
            }
        }
    
    # ===== YAML → 他形式変換 =====
    
    def yaml_to_table_definition(self, yaml_data: Dict[str, Any]) -> TransformResult:
        """
        YAMLデータをTableDefinitionオブジェクトに変換
        
        Args:
            yaml_data: YAMLデータ
            
        Returns:
            TransformResult: 変換結果
        """
        try:
            errors = []
            warnings = []
            
            # 必須フィールドの検証
            required_fields = ['table_name', 'logical_name', 'columns']
            for field in required_fields:
                if field not in yaml_data:
                    errors.append(f"必須フィールドが不足しています: {field}")
            
            if errors:
                return TransformResult(False, None, errors, warnings)
            
            # TableDefinitionオブジェクトを作成
            from ...core.models import create_table_definition_from_yaml
            table_def = create_table_definition_from_yaml(yaml_data)
            
            # データ型の正規化
            for column in table_def.columns:
                normalized_type = self._normalize_data_type(column.data_type)
                if normalized_type != column.data_type:
                    warnings.append(f"データ型を正規化しました: {column.name} {column.data_type} → {normalized_type}")
                    column.data_type = normalized_type
            
            return TransformResult(True, table_def, errors, warnings)
            
        except Exception as e:
            logger.error(f"YAML→TableDefinition変換エラー: {e}")
            return TransformResult(False, None, [str(e)], [])
    
    def yaml_to_ddl(self, yaml_data: Dict[str, Any]) -> TransformResult:
        """
        YAMLデータをDDLに変換
        
        Args:
            yaml_data: YAMLデータ
            
        Returns:
            TransformResult: 変換結果
        """
        try:
            # まずTableDefinitionに変換
            table_result = self.yaml_to_table_definition(yaml_data)
            if not table_result.success:
                return table_result
            
            # DDLを生成
            ddl_content = self.ddl_generator.generate(table_result.data)
            
            return TransformResult(True, ddl_content, table_result.errors, table_result.warnings)
            
        except Exception as e:
            logger.error(f"YAML→DDL変換エラー: {e}")
            return TransformResult(False, None, [str(e)], [])
    
    def yaml_to_markdown(self, yaml_data: Dict[str, Any]) -> TransformResult:
        """
        YAMLデータをMarkdownに変換
        
        Args:
            yaml_data: YAMLデータ
            
        Returns:
            TransformResult: 変換結果
        """
        try:
            # まずTableDefinitionに変換
            table_result = self.yaml_to_table_definition(yaml_data)
            if not table_result.success:
                return table_result
            
            # Markdownを生成
            markdown_content = self.markdown_generator.generate(table_result.data)
            
            return TransformResult(True, markdown_content, table_result.errors, table_result.warnings)
            
        except Exception as e:
            logger.error(f"YAML→Markdown変換エラー: {e}")
            return TransformResult(False, None, [str(e)], [])
    
    # ===== DDL → 他形式変換 =====
    
    def ddl_to_table_definition(self, ddl_content: str) -> TransformResult:
        """
        DDLをTableDefinitionオブジェクトに変換
        
        Args:
            ddl_content: DDL内容
            
        Returns:
            TransformResult: 変換結果
        """
        try:
            errors = []
            warnings = []
            
            # DDLを解析
            parsed_ddl = self.ddl_parser.parse(ddl_content)
            
            if not parsed_ddl:
                return TransformResult(False, None, ["DDLの解析に失敗しました"], [])
            
            # TableDefinitionオブジェクトを作成
            table_def = self._create_table_definition_from_ddl(parsed_ddl)
            
            return TransformResult(True, table_def, errors, warnings)
            
        except Exception as e:
            logger.error(f"DDL→TableDefinition変換エラー: {e}")
            return TransformResult(False, None, [str(e)], [])
    
    def ddl_to_yaml(self, ddl_content: str) -> TransformResult:
        """
        DDLをYAMLに変換
        
        Args:
            ddl_content: DDL内容
            
        Returns:
            TransformResult: 変換結果
        """
        try:
            # まずTableDefinitionに変換
            table_result = self.ddl_to_table_definition(ddl_content)
            if not table_result.success:
                return table_result
            
            # YAMLデータを生成
            yaml_data = table_result.data.to_dict()
            
            return TransformResult(True, yaml_data, table_result.errors, table_result.warnings)
            
        except Exception as e:
            logger.error(f"DDL→YAML変換エラー: {e}")
            return TransformResult(False, None, [str(e)], [])
    
    # ===== Markdown → 他形式変換 =====
    
    def markdown_to_table_definition(self, markdown_content: str) -> TransformResult:
        """
        MarkdownをTableDefinitionオブジェクトに変換
        
        Args:
            markdown_content: Markdown内容
            
        Returns:
            TransformResult: 変換結果
        """
        try:
            errors = []
            warnings = []
            
            # Markdownを解析
            parsed_markdown = self.markdown_parser.parse_content(markdown_content)
            
            if not parsed_markdown:
                return TransformResult(False, None, ["Markdownの解析に失敗しました"], [])
            
            # TableDefinitionオブジェクトを作成
            table_def = self._create_table_definition_from_markdown(parsed_markdown)
            
            return TransformResult(True, table_def, errors, warnings)
            
        except Exception as e:
            logger.error(f"Markdown→TableDefinition変換エラー: {e}")
            return TransformResult(False, None, [str(e)], [])
    
    # ===== データ整合性チェック =====
    
    def validate_data_consistency(self, yaml_data: Dict[str, Any], ddl_content: str, 
                                 markdown_content: str = None) -> ValidationResult:
        """
        YAML、DDL、Markdownの整合性をチェック
        
        Args:
            yaml_data: YAMLデータ
            ddl_content: DDL内容
            markdown_content: Markdown内容（オプション）
            
        Returns:
            ValidationResult: バリデーション結果
        """
        try:
            errors = []
            warnings = []
            
            # YAML → TableDefinition
            yaml_result = self.yaml_to_table_definition(yaml_data)
            if not yaml_result.success:
                errors.extend([f"YAML: {e}" for e in yaml_result.errors])
                return ValidationResult(False, errors, warnings)
            
            yaml_table = yaml_result.data
            
            # DDL → TableDefinition
            ddl_result = self.ddl_to_table_definition(ddl_content)
            if not ddl_result.success:
                errors.extend([f"DDL: {e}" for e in ddl_result.errors])
                return ValidationResult(False, errors, warnings)
            
            ddl_table = ddl_result.data
            
            # テーブル名の整合性チェック
            if yaml_table.table_name != ddl_table.table_name:
                errors.append(f"テーブル名が一致しません: YAML({yaml_table.table_name}) ≠ DDL({ddl_table.table_name})")
            
            # カラム定義の整合性チェック
            yaml_columns = {col.name: col for col in yaml_table.columns}
            ddl_columns = {col.name: col for col in ddl_table.columns}
            
            # カラム存在チェック
            yaml_col_names = set(yaml_columns.keys())
            ddl_col_names = set(ddl_columns.keys())
            
            missing_in_ddl = yaml_col_names - ddl_col_names
            missing_in_yaml = ddl_col_names - yaml_col_names
            
            for col_name in missing_in_ddl:
                errors.append(f"カラム '{col_name}' がDDLに存在しません")
            
            for col_name in missing_in_yaml:
                errors.append(f"カラム '{col_name}' がYAMLに存在しません")
            
            # 共通カラムの詳細チェック
            common_columns = yaml_col_names & ddl_col_names
            for col_name in common_columns:
                yaml_col = yaml_columns[col_name]
                ddl_col = ddl_columns[col_name]
                
                # データ型チェック
                if not self._are_data_types_compatible(yaml_col.data_type, ddl_col.data_type):
                    errors.append(f"カラム '{col_name}' のデータ型が一致しません: YAML({yaml_col.data_type}) ≠ DDL({ddl_col.data_type})")
                
                # NULL制約チェック
                if yaml_col.nullable != ddl_col.nullable:
                    errors.append(f"カラム '{col_name}' のNULL制約が一致しません: YAML({yaml_col.nullable}) ≠ DDL({ddl_col.nullable})")
                
                # デフォルト値チェック
                if yaml_col.default_value != ddl_col.default_value:
                    warnings.append(f"カラム '{col_name}' のデフォルト値が一致しません: YAML({yaml_col.default_value}) ≠ DDL({ddl_col.default_value})")
            
            # インデックス整合性チェック
            yaml_indexes = {idx.name: idx for idx in yaml_table.indexes}
            ddl_indexes = {idx.name: idx for idx in ddl_table.indexes}
            
            yaml_idx_names = set(yaml_indexes.keys())
            ddl_idx_names = set(ddl_indexes.keys())
            
            missing_idx_in_ddl = yaml_idx_names - ddl_idx_names
            missing_idx_in_yaml = ddl_idx_names - yaml_idx_names
            
            for idx_name in missing_idx_in_ddl:
                warnings.append(f"インデックス '{idx_name}' がDDLに存在しません")
            
            for idx_name in missing_idx_in_yaml:
                warnings.append(f"インデックス '{idx_name}' がYAMLに存在しません")
            
            # Markdownチェック（提供されている場合）
            if markdown_content:
                markdown_result = self.markdown_to_table_definition(markdown_content)
                if markdown_result.success:
                    markdown_table = markdown_result.data
                    
                    # Markdownとの基本整合性チェック
                    if yaml_table.table_name != markdown_table.table_name:
                        warnings.append(f"Markdownのテーブル名が一致しません: YAML({yaml_table.table_name}) ≠ Markdown({markdown_table.table_name})")
                    
                    if yaml_table.logical_name != markdown_table.logical_name:
                        warnings.append(f"Markdownの論理名が一致しません: YAML({yaml_table.logical_name}) ≠ Markdown({markdown_table.logical_name})")
            
            is_valid = len(errors) == 0
            return ValidationResult(is_valid, errors, warnings)
            
        except Exception as e:
            logger.error(f"データ整合性チェックエラー: {e}")
            return ValidationResult(False, [str(e)], [])
    
    # ===== データ型変換・正規化 =====
    
    def _normalize_data_type(self, data_type: str) -> str:
        """
        データ型を正規化
        
        Args:
            data_type: データ型
            
        Returns:
            str: 正規化されたデータ型
        """
        # 大文字に変換
        normalized = data_type.upper().strip()
        
        # 括弧内の数値を保持しながら正規化
        if '(' in normalized:
            base_type = normalized.split('(')[0]
            params = normalized.split('(')[1].rstrip(')')
            
            # 標準的なデータ型にマッピング
            if base_type in self.data_type_mappings['postgresql_to_standard']:
                base_type = self.data_type_mappings['postgresql_to_standard'][base_type]
            
            return f"{base_type}({params})"
        else:
            # パラメータなしのデータ型
            if normalized in self.data_type_mappings['postgresql_to_standard']:
                return self.data_type_mappings['postgresql_to_standard'][normalized]
            
            return normalized
    
    def _are_data_types_compatible(self, type1: str, type2: str) -> bool:
        """
        データ型の互換性をチェック
        
        Args:
            type1: データ型1
            type2: データ型2
            
        Returns:
            bool: 互換性があるかどうか
        """
        # 正規化して比較
        norm_type1 = self._normalize_data_type(type1)
        norm_type2 = self._normalize_data_type(type2)
        
        if norm_type1 == norm_type2:
            return True
        
        # 互換性のあるデータ型のペア
        compatible_pairs = [
            ('TEXT', 'VARCHAR'),
            ('INTEGER', 'SERIAL'),
            ('BIGINT', 'BIGSERIAL'),
            ('NUMERIC', 'DECIMAL'),
            ('REAL', 'FLOAT'),
            ('DOUBLE PRECISION', 'DOUBLE')
        ]
        
        for pair in compatible_pairs:
            if (norm_type1 in pair and norm_type2 in pair):
                return True
        
        return False
    
    # ===== ヘルパーメソッド =====
    
    def _create_table_definition_from_ddl(self, parsed_ddl: Dict[str, Any]) -> TableDefinition:
        """DDL解析結果からTableDefinitionを作成"""
        # 実装は既存のDDLParserの結果を使用
        # ここでは簡略化した実装を示す
        
        table_name = parsed_ddl.get('table_name', '')
        logical_name = parsed_ddl.get('comment', table_name)
        
        columns = []
        for col_data in parsed_ddl.get('columns', []):
            column = ColumnDefinition(
                name=col_data['name'],
                data_type=col_data['type'],
                nullable=not col_data.get('not_null', False),
                primary_key=col_data.get('primary_key', False),
                default_value=col_data.get('default'),
                comment=col_data.get('comment', ''),
                requirement_id=''  # DDLからは取得できない
            )
            columns.append(column)
        
        indexes = []
        for idx_data in parsed_ddl.get('indexes', []):
            index = IndexDefinition(
                name=idx_data['name'],
                columns=idx_data['columns'],
                unique=idx_data.get('unique', False),
                comment=idx_data.get('comment', '')
            )
            indexes.append(index)
        
        foreign_keys = []
        for fk_data in parsed_ddl.get('foreign_keys', []):
            foreign_key = ForeignKeyDefinition(
                name=fk_data['name'],
                columns=fk_data['columns'],
                references_table=fk_data['references']['table'],
                references_columns=fk_data['references']['columns'],
                on_update=fk_data.get('on_update', 'NO ACTION'),
                on_delete=fk_data.get('on_delete', 'NO ACTION')
            )
            foreign_keys.append(foreign_key)
        
        return TableDefinition(
            table_name=table_name,
            logical_name=logical_name,
            category='',  # DDLからは取得できない
            priority='',  # DDLからは取得できない
            requirement_id='',  # DDLからは取得できない
            columns=columns,
            indexes=indexes,
            foreign_keys=foreign_keys
        )
    
    def _create_table_definition_from_markdown(self, parsed_markdown: Dict[str, Any]) -> TableDefinition:
        """Markdown解析結果からTableDefinitionを作成"""
        # 実装は既存のMarkdownParserの結果を使用
        # ここでは簡略化した実装を示す
        
        table_name = parsed_markdown.get('table_name', '')
        logical_name = parsed_markdown.get('logical_name', table_name)
        
        columns = []
        for col_data in parsed_markdown.get('columns', []):
            column = ColumnDefinition(
                name=col_data['name'],
                data_type=col_data['type'],
                nullable=col_data.get('nullable', True),
                primary_key=col_data.get('primary_key', False),
                default_value=col_data.get('default'),
                comment=col_data.get('comment', ''),
                requirement_id=col_data.get('requirement_id', '')
            )
            columns.append(column)
        
        return TableDefinition(
            table_name=table_name,
            logical_name=logical_name,
            category=parsed_markdown.get('category', ''),
            priority=parsed_markdown.get('priority', ''),
            requirement_id=parsed_markdown.get('requirement_id', ''),
            columns=columns,
            indexes=[],  # Markdownからは詳細なインデックス情報は取得困難
            foreign_keys=[]  # Markdownからは詳細な外部キー情報は取得困難
        )
    
    # ===== サンプルデータ生成 =====
    
    def generate_sample_data(self, table_definition: TableDefinition, 
                           record_count: int = 10) -> TransformResult:
        """
        テーブル定義からサンプルデータを生成
        
        Args:
            table_definition: テーブル定義
            record_count: 生成するレコード数
            
        Returns:
            TransformResult: 変換結果
        """
        try:
            sample_data = self.sample_data_generator.generate_sample_data(
                table_definition, record_count
            )
            
            return TransformResult(True, sample_data, [], [])
            
        except Exception as e:
            logger.error(f"サンプルデータ生成エラー: {e}")
            return TransformResult(False, None, [str(e)], [])
    
    # ===== バッチ変換 =====
    
    def batch_transform(self, source_format: str, target_format: str, 
                       data_list: List[Any]) -> List[TransformResult]:
        """
        バッチ変換処理
        
        Args:
            source_format: 変換元フォーマット（yaml, ddl, markdown）
            target_format: 変換先フォーマット（yaml, ddl, markdown）
            data_list: 変換対象データのリスト
            
        Returns:
            List[TransformResult]: 変換結果のリスト
        """
        results = []
        
        for data in data_list:
            try:
                if source_format == 'yaml' and target_format == 'ddl':
                    result = self.yaml_to_ddl(data)
                elif source_format == 'yaml' and target_format == 'markdown':
                    result = self.yaml_to_markdown(data)
                elif source_format == 'ddl' and target_format == 'yaml':
                    result = self.ddl_to_yaml(data)
                elif source_format == 'markdown' and target_format == 'yaml':
                    markdown_result = self.markdown_to_table_definition(data)
                    if markdown_result.success:
                        yaml_data = markdown_result.data.to_dict()
                        result = TransformResult(True, yaml_data, [], [])
                    else:
                        result = markdown_result
                else:
                    result = TransformResult(False, None, [f"サポートされていない変換: {source_format} → {target_format}"], [])
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"バッチ変換エラー: {source_format} → {target_format}, {e}")
                results.append(TransformResult(False, None, [str(e)], []))
        
        return results
    
    # ===== テスト用メソッド =====
    
    def transform_yaml_to_ddl(self, yaml_data: Dict[str, Any]) -> str:
        """
        YAMLデータをDDLに変換（テスト用簡易メソッド）
        
        Args:
            yaml_data: YAMLデータ
            
        Returns:
            str: DDL内容
            
        Raises:
            DataTransformError: 変換エラー
        """
        result = self.yaml_to_ddl(yaml_data)
        if not result.success:
            raise DataTransformError(f"YAML→DDL変換に失敗しました: {', '.join(result.errors)}")
        return result.data
    
    def transform_ddl_to_yaml(self, ddl_content: str) -> Dict[str, Any]:
        """
        DDLをYAMLデータに変換（テスト用簡易メソッド）
        
        Args:
            ddl_content: DDL内容
            
        Returns:
            Dict[str, Any]: YAMLデータ
            
        Raises:
            DataTransformError: 変換エラー
        """
        result = self.ddl_to_yaml(ddl_content)
        if not result.success:
            raise DataTransformError(f"DDL→YAML変換に失敗しました: {', '.join(result.errors)}")
        return result.data
    
    def normalize_data_type(self, data_type: str) -> str:
        """
        データ型を正規化（テスト用公開メソッド）
        
        Args:
            data_type: データ型
            
        Returns:
            str: 正規化されたデータ型
        """
        return self._normalize_data_type(data_type)
    
    def check_data_type_compatibility(self, type1: str, type2: str) -> bool:
        """
        データ型の互換性をチェック（テスト用公開メソッド）
        
        Args:
            type1: データ型1
            type2: データ型2
            
        Returns:
            bool: 互換性があるかどうか
        """
        return self._are_data_types_compatible(type1, type2)
    
    def _validate_table_name(self, table_name: str) -> bool:
        """
        テーブル名のバリデーション
        
        Args:
            table_name: テーブル名
            
        Returns:
            bool: 有効なテーブル名かどうか
        """
        if not table_name:
            return False
        
        # プレフィックスチェック
        valid_prefixes = ['MST_', 'TRN_', 'HIS_', 'SYS_', 'WRK_', 'IF_']
        if not any(table_name.startswith(prefix) for prefix in valid_prefixes):
            return False
        
        # 大文字チェック
        if table_name != table_name.upper():
            return False
        
        return True
    
    def _normalize_data_type(self, data_type: str) -> str:
        """
        データ型の正規化
        
        Args:
            data_type: データ型
            
        Returns:
            str: 正規化されたデータ型
        """
        if not data_type:
            return data_type
        
        # 大文字に変換
        normalized = data_type.upper()
        
        # 基本的な正規化マッピング
        type_mapping = {
            'INT': 'INTEGER',
            'BOOL': 'BOOLEAN',
            'DATETIME': 'TIMESTAMP'
        }
        
        # 括弧を含む型の処理
        for old_type, new_type in type_mapping.items():
            if normalized.startswith(old_type):
                return normalized.replace(old_type, new_type, 1)
        
        return normalized
    
    def create_table_definition_from_yaml(self, yaml_data: Dict[str, Any]) -> TableDefinition:
        """
        YAMLデータからTableDefinitionを作成（テスト用簡易メソッド）
        
        Args:
            yaml_data: YAMLデータ
            
        Returns:
            TableDefinition: テーブル定義オブジェクト
            
        Raises:
            DataTransformError: 変換エラー
        """
        result = self.yaml_to_table_definition(yaml_data)
        if not result.success:
            raise DataTransformError(f"YAML→TableDefinition変換に失敗しました: {', '.join(result.errors)}")
        return result.data
    
    def validate_consistency(self, yaml_data: Dict[str, Any], ddl_content: str) -> ValidationResult:
        """
        データ整合性をチェック（テスト用簡易メソッド）
        
        Args:
            yaml_data: YAMLデータ
            ddl_content: DDL内容
            
        Returns:
            ValidationResult: バリデーション結果
        """
        return self.validate_data_consistency(yaml_data, ddl_content)
    
    def dict_to_table_definition(self, data: Dict[str, Any]) -> TableDefinition:
        """
        辞書データからTableDefinitionオブジェクトを作成
        
        Args:
            data: 辞書データ
            
        Returns:
            TableDefinition: テーブル定義オブジェクト
            
        Raises:
            DataTransformError: 変換エラー
        """
        try:
            # 必須フィールドの検証
            required_fields = ['table_name', 'logical_name', 'columns']
            for field in required_fields:
                if field not in data:
                    raise DataTransformError(f"必須フィールドが不足しています: {field}")
            
            # カラム定義の変換
            columns = []
            for col_data in data['columns']:
                column = ColumnDefinition(
                    name=col_data['name'],
                    type=col_data.get('type', col_data.get('data_type', '')),
                    nullable=col_data.get('nullable', True),
                    primary_key=col_data.get('primary_key', False),
                    unique=col_data.get('unique', False),
                    default=col_data.get('default', col_data.get('default_value')),
                    comment=col_data.get('comment', ''),
                    requirement_id=col_data.get('requirement_id', '')
                )
                columns.append(column)
            
            # インデックス定義の変換
            indexes = []
            for idx_data in data.get('indexes', []):
                index = IndexDefinition(
                    name=idx_data['name'],
                    columns=idx_data['columns'],
                    unique=idx_data.get('unique', False),
                    comment=idx_data.get('comment', ''),
                    type=idx_data.get('type', 'btree')
                )
                indexes.append(index)
            
            # 外部キー定義の変換
            foreign_keys = []
            for fk_data in data.get('foreign_keys', []):
                references = fk_data.get('references', {})
                foreign_key = ForeignKeyDefinition(
                    name=fk_data.get('name', ''),
                    columns=fk_data['columns'],
                    references_table=references.get('table', ''),
                    references_columns=references.get('columns', []),
                    on_update=fk_data.get('on_update', 'NO ACTION'),
                    on_delete=fk_data.get('on_delete', 'NO ACTION'),
                    comment=fk_data.get('comment', '')
                )
                foreign_keys.append(foreign_key)
            
            # TableDefinitionオブジェクトの作成
            table_def = TableDefinition(
                name=data['table_name'],
                logical_name=data['logical_name'],
                category=data.get('category', ''),
                priority=data.get('priority', ''),
                requirement_id=data.get('requirement_id', ''),
                comment=data.get('comment', ''),
                columns=columns,
                indexes=indexes,
                foreign_keys=foreign_keys
            )
            
            return table_def
            
        except Exception as e:
            logger.error(f"辞書→TableDefinition変換エラー: {e}")
            raise DataTransformError(f"辞書→TableDefinition変換に失敗しました: {str(e)}")
