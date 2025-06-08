"""
テーブル定義アダプター

テーブル定義データの変換・検証を行うアダプターです。
YAML、DDL、Markdownの各形式間でのデータ変換を提供します。
"""

from typing import Dict, List, Any, Optional
from .base_adapter import BaseAdapter
from ..core.exceptions import ValidationError, ConversionError
from ..parsers.yaml_parser import YamlParser
from ..parsers.ddl_parser import DDLParser
from ..parsers.markdown_parser import MarkdownParser


class TableDefinitionAdapter(BaseAdapter):
    """テーブル定義アダプター"""
    
    def __init__(self, config):
        """
        テーブル定義アダプターを初期化
        
        Args:
            config: データベースツール設定
        """
        super().__init__(config)
        self.yaml_parser = YamlParser(config)
        self.ddl_parser = DDLParser(config)
        self.markdown_parser = MarkdownParser(config)
    
    def validate_input(self, data: Any) -> bool:
        """
        テーブル定義データの検証
        
        Args:
            data: 検証対象のテーブル定義データ
            
        Returns:
            bool: 検証結果
            
        Raises:
            ValidationError: 検証エラー時
        """
        try:
            if not isinstance(data, dict):
                raise ValidationError("Table definition must be a dictionary")
            
            # 必須フィールドの確認
            required_fields = ['table_name', 'logical_name', 'columns']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Required field '{field}' is missing")
            
            # テーブル名の検証
            if not data['table_name'] or not isinstance(data['table_name'], str):
                raise ValidationError("table_name must be a non-empty string")
            
            # カラム定義の検証
            columns = data.get('columns', [])
            if not isinstance(columns, list) or len(columns) == 0:
                raise ValidationError("columns must be a non-empty list")
            
            for i, column in enumerate(columns):
                self._validate_column_definition(column, i)
            
            self.log_operation("validate_input", {"table_name": data.get('table_name')})
            return True
            
        except Exception as e:
            self.handle_error(e, "table definition validation")
    
    def _validate_column_definition(self, column: Dict[str, Any], index: int) -> None:
        """
        カラム定義の検証
        
        Args:
            column: カラム定義
            index: カラムインデックス
            
        Raises:
            ValidationError: 検証エラー時
        """
        if not isinstance(column, dict):
            raise ValidationError(f"Column {index} must be a dictionary")
        
        required_column_fields = ['name', 'type']
        for field in required_column_fields:
            if field not in column:
                raise ValidationError(f"Column {index}: Required field '{field}' is missing")
        
        if not column['name'] or not isinstance(column['name'], str):
            raise ValidationError(f"Column {index}: name must be a non-empty string")
        
        if not column['type'] or not isinstance(column['type'], str):
            raise ValidationError(f"Column {index}: type must be a non-empty string")
    
    def transform_data(self, data: Any) -> Dict[str, Any]:
        """
        テーブル定義データの変換
        
        Args:
            data: 変換対象データ
            
        Returns:
            Dict[str, Any]: 正規化されたテーブル定義データ
            
        Raises:
            ConversionError: 変換エラー時
        """
        try:
            if not self.validate_input(data):
                raise ConversionError("Invalid input data")
            
            # データの正規化
            normalized_data = {
                'table_name': data['table_name'],
                'logical_name': data.get('logical_name', ''),
                'category': data.get('category', ''),
                'priority': data.get('priority', '中'),
                'requirement_id': data.get('requirement_id', ''),
                'columns': self._normalize_columns(data['columns']),
                'indexes': data.get('indexes', []),
                'foreign_keys': data.get('foreign_keys', []),
                'constraints': data.get('constraints', []),
                'comment': data.get('comment', '')
            }
            
            self.log_operation("transform_data", {"table_name": normalized_data['table_name']})
            return normalized_data
            
        except Exception as e:
            self.handle_error(e, "table definition transformation")
    
    def _normalize_columns(self, columns: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        カラム定義の正規化
        
        Args:
            columns: カラム定義リスト
            
        Returns:
            List[Dict[str, Any]]: 正規化されたカラム定義リスト
        """
        normalized_columns = []
        
        for column in columns:
            normalized_column = {
                'name': column['name'],
                'type': column['type'],
                'nullable': column.get('nullable', True),
                'primary_key': column.get('primary_key', False),
                'unique': column.get('unique', False),
                'default': column.get('default'),
                'comment': column.get('comment', ''),
                'requirement_id': column.get('requirement_id', '')
            }
            normalized_columns.append(normalized_column)
        
        return normalized_columns
    
    def convert_yaml_to_ddl(self, yaml_data: Dict[str, Any]) -> str:
        """
        YAML形式からDDL形式への変換
        
        Args:
            yaml_data: YAML形式のテーブル定義
            
        Returns:
            str: DDL文字列
        """
        try:
            normalized_data = self.transform_data(yaml_data)
            ddl_content = self._generate_ddl_from_normalized_data(normalized_data)
            
            self.log_operation("convert_yaml_to_ddl", {
                "table_name": normalized_data['table_name']
            })
            return ddl_content
            
        except Exception as e:
            self.handle_error(e, "YAML to DDL conversion")
    
    def convert_yaml_to_markdown(self, yaml_data: Dict[str, Any]) -> str:
        """
        YAML形式からMarkdown形式への変換
        
        Args:
            yaml_data: YAML形式のテーブル定義
            
        Returns:
            str: Markdown文字列
        """
        try:
            normalized_data = self.transform_data(yaml_data)
            markdown_content = self._generate_markdown_from_normalized_data(normalized_data)
            
            self.log_operation("convert_yaml_to_markdown", {
                "table_name": normalized_data['table_name']
            })
            return markdown_content
            
        except Exception as e:
            self.handle_error(e, "YAML to Markdown conversion")
    
    def _generate_ddl_from_normalized_data(self, data: Dict[str, Any]) -> str:
        """
        正規化データからDDL生成
        
        Args:
            data: 正規化されたテーブル定義データ
            
        Returns:
            str: DDL文字列
        """
        # DDL生成ロジックの実装
        # 実際の実装では、DDLGeneratorを使用
        return f"-- DDL for {data['table_name']}\n-- Generated by TableDefinitionAdapter"
    
    def _generate_markdown_from_normalized_data(self, data: Dict[str, Any]) -> str:
        """
        正規化データからMarkdown生成
        
        Args:
            data: 正規化されたテーブル定義データ
            
        Returns:
            str: Markdown文字列
        """
        # Markdown生成ロジックの実装
        # 実際の実装では、MarkdownGeneratorを使用
        return f"# {data['logical_name']}\n\n## テーブル名: {data['table_name']}"
