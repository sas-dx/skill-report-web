"""
統合パーサー - YAML・DDL・定義書の統一解析
全パーサーを統合した包括的な解析機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

from typing import Optional, Dict, Any, List, Union
from pathlib import Path
import yaml
import re

from .base_parser import BaseParser
from ..core.models import TableDefinition, CheckResult, ColumnDefinition, IndexDefinition, ForeignKeyDefinition
from ..core.config import Config
from ..core.logger import get_logger
from ..core.exceptions import ParsingError, ValidationError
from ..utils.file_utils import FileUtils

logger = get_logger(__name__)


class UnifiedParser(BaseParser):
    """統合パーサー - YAML・DDL・定義書の統一解析"""
    
    def __init__(self, config: Optional[Config] = None):
        """初期化"""
        super().__init__(config)
        self.file_utils = FileUtils(config)
        self.supported_formats = {
            '.yaml': self._parse_yaml,
            '.yml': self._parse_yaml,
            '.sql': self._parse_ddl,
            '.md': self._parse_markdown
        }
    
    def parse(self, source: Path) -> TableDefinition:
        """統合解析実行"""
        try:
            self._validate_file_exists(source)
            self._validate_file_readable(source)
            
            # ファイル形式に応じた解析
            extension = source.suffix.lower()
            if extension not in self.supported_formats:
                raise ParsingError(f"サポートされていないファイル形式: {extension}")
            
            parser_func = self.supported_formats[extension]
            table_def = parser_func(source)
            
            self.logger.info(f"解析完了: {source} -> {table_def.table_name}")
            return table_def
            
        except Exception as e:
            raise self._handle_parsing_error(e, source)
    
    def validate(self, source: Path) -> List[CheckResult]:
        """統合バリデーション実行"""
        results = []
        
        try:
            # 基本ファイルチェック
            self._validate_file_exists(source)
            self._validate_file_readable(source)
            
            # 形式別バリデーション
            extension = source.suffix.lower()
            if extension == '.yaml' or extension == '.yml':
                results.extend(self._validate_yaml(source))
            elif extension == '.sql':
                results.extend(self._validate_ddl(source))
            elif extension == '.md':
                results.extend(self._validate_markdown(source))
            
            if not results:
                results.append(self._create_success_result(
                    f"バリデーション成功: {source.name}"
                ))
                
        except Exception as e:
            results.append(self._create_error_result(
                f"バリデーションエラー: {str(e)}",
                details=str(e)
            ))
        
        return results
    
    def get_supported_extensions(self) -> List[str]:
        """サポートするファイル拡張子を取得"""
        return list(self.supported_formats.keys())
    
    def _parse_yaml(self, yaml_path: Path) -> TableDefinition:
        """YAML形式の解析"""
        try:
            with open(yaml_path, 'r', encoding=self.config.tool.encoding) as f:
                data = yaml.safe_load(f)
            
            if not data:
                raise ParsingError("YAMLファイルが空です")
            
            # 必須フィールドの確認
            required_fields = ['table_name', 'logical_name', 'columns']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"必須フィールドが不足: {field}")
            
            # TableDefinition作成
            table_def = TableDefinition(
                table_name=data['table_name'],
                logical_name=data['logical_name'],
                category=data.get('category', ''),
                priority=data.get('priority', '中'),
                requirement_id=data.get('requirement_id', ''),
                comment=data.get('comment', ''),
                overview=data.get('overview', ''),
                notes=data.get('notes', []),
                rules=data.get('rules', []),
                revision_history=data.get('revision_history', [])
            )
            
            # カラム定義の解析
            for col_data in data.get('columns', []):
                column = self._parse_column_from_yaml(col_data)
                table_def.columns.append(column)
            
            # インデックス定義の解析
            for idx_data in data.get('indexes', []):
                index = self._parse_index_from_yaml(idx_data)
                table_def.indexes.append(index)
            
            # 外部キー定義の解析
            for fk_data in data.get('foreign_keys', []):
                foreign_key = self._parse_foreign_key_from_yaml(fk_data)
                table_def.foreign_keys.append(foreign_key)
            
            return table_def
            
        except yaml.YAMLError as e:
            raise ParsingError(f"YAML解析エラー: {e}")
        except Exception as e:
            raise ParsingError(f"YAML処理エラー: {e}")
    
    def _parse_ddl(self, ddl_path: Path) -> TableDefinition:
        """DDL形式の解析"""
        try:
            with open(ddl_path, 'r', encoding=self.config.tool.encoding) as f:
                ddl_content = f.read()
            
            # CREATE TABLE文の抽出
            create_table_pattern = r'CREATE\s+TABLE\s+(\w+)\s*\((.*?)\);'
            match = re.search(create_table_pattern, ddl_content, re.DOTALL | re.IGNORECASE)
            
            if not match:
                raise ParsingError("CREATE TABLE文が見つかりません")
            
            table_name = match.group(1)
            columns_section = match.group(2)
            
            # TableDefinition作成
            table_def = TableDefinition(
                table_name=table_name,
                logical_name=table_name,  # DDLからは論理名を取得できないため物理名を使用
                category='',
                priority='中',
                requirement_id='',
                comment=f'DDLから生成: {table_name}'
            )
            
            # カラム定義の解析
            columns = self._parse_columns_from_ddl(columns_section)
            table_def.columns.extend(columns)
            
            # インデックス定義の解析
            indexes = self._parse_indexes_from_ddl(ddl_content, table_name)
            table_def.indexes.extend(indexes)
            
            return table_def
            
        except Exception as e:
            raise ParsingError(f"DDL処理エラー: {e}")
    
    def _parse_markdown(self, md_path: Path) -> TableDefinition:
        """Markdown形式の解析"""
        try:
            with open(md_path, 'r', encoding=self.config.tool.encoding) as f:
                content = f.read()
            
            # テーブル名の抽出（ファイル名から推測）
            table_name = md_path.stem.replace('テーブル定義書_', '').split('_')[0]
            
            # TableDefinition作成（基本情報のみ）
            table_def = TableDefinition(
                table_name=table_name,
                logical_name=table_name,
                category='',
                priority='中',
                requirement_id='',
                comment=f'Markdownから生成: {table_name}'
            )
            
            # Markdownからの詳細解析は今後の拡張で実装
            self.logger.warning(f"Markdown解析は基本情報のみ: {md_path}")
            
            return table_def
            
        except Exception as e:
            raise ParsingError(f"Markdown処理エラー: {e}")
    
    def _parse_column_from_yaml(self, col_data: Dict[str, Any]) -> ColumnDefinition:
        """YAMLからカラム定義を解析"""
        return ColumnDefinition(
            name=col_data['name'],
            data_type=col_data['type'],
            nullable=col_data.get('nullable', True),
            primary_key=col_data.get('primary_key', False),
            unique=col_data.get('unique', False),
            default=col_data.get('default'),
            comment=col_data.get('comment', ''),
            requirement_id=col_data.get('requirement_id', '')
        )
    
    def _parse_index_from_yaml(self, idx_data: Dict[str, Any]) -> IndexDefinition:
        """YAMLからインデックス定義を解析"""
        return IndexDefinition(
            name=idx_data['name'],
            columns=idx_data['columns'],
            unique=idx_data.get('unique', False),
            comment=idx_data.get('comment', '')
        )
    
    def _parse_foreign_key_from_yaml(self, fk_data: Dict[str, Any]) -> ForeignKeyDefinition:
        """YAMLから外部キー定義を解析"""
        references = fk_data['references']
        return ForeignKeyDefinition(
            name=fk_data['name'],
            columns=fk_data['columns'],
            reference_table=references['table'],
            reference_columns=references['columns'],
            on_update=fk_data.get('on_update', 'RESTRICT'),
            on_delete=fk_data.get('on_delete', 'RESTRICT'),
            comment=fk_data.get('comment', '')
        )
    
    def _parse_columns_from_ddl(self, columns_section: str) -> List[ColumnDefinition]:
        """DDLからカラム定義を解析"""
        columns = []
        
        # カラム定義の正規表現パターン
        column_pattern = r'(\w+)\s+([^,\n]+?)(?:,|\s*$)'
        matches = re.findall(column_pattern, columns_section, re.MULTILINE)
        
        for name, definition in matches:
            # 基本的なカラム情報を抽出
            data_type = definition.strip().split()[0]
            nullable = 'NOT NULL' not in definition.upper()
            primary_key = 'PRIMARY KEY' in definition.upper()
            unique = 'UNIQUE' in definition.upper()
            
            column = ColumnDefinition(
                name=name,
                data_type=data_type,
                nullable=nullable,
                primary_key=primary_key,
                unique=unique,
                comment=f'DDLから生成: {name}'
            )
            columns.append(column)
        
        return columns
    
    def _parse_indexes_from_ddl(self, ddl_content: str, table_name: str) -> List[IndexDefinition]:
        """DDLからインデックス定義を解析"""
        indexes = []
        
        # CREATE INDEX文の抽出
        index_pattern = r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(\w+)\s+ON\s+' + table_name + r'\s*\((.*?)\);'
        matches = re.findall(index_pattern, ddl_content, re.IGNORECASE)
        
        for name, columns_str in matches:
            columns = [col.strip() for col in columns_str.split(',')]
            unique = 'UNIQUE' in ddl_content.upper()
            
            index = IndexDefinition(
                name=name,
                columns=columns,
                unique=unique,
                comment=f'DDLから生成: {name}'
            )
            indexes.append(index)
        
        return indexes
    
    def _validate_yaml(self, yaml_path: Path) -> List[CheckResult]:
        """YAML形式のバリデーション"""
        results = []
        
        try:
            with open(yaml_path, 'r', encoding=self.config.tool.encoding) as f:
                data = yaml.safe_load(f)
            
            # 必須セクションチェック
            required_sections = ['revision_history', 'overview', 'notes', 'rules']
            for section in required_sections:
                if section not in data:
                    results.append(self._create_error_result(
                        f"必須セクション不足: {section}",
                        details=f"🔴 {section} セクションは絶対省略禁止です"
                    ))
                elif section == 'overview' and len(str(data[section])) < 50:
                    results.append(self._create_error_result(
                        f"overview文字数不足: {len(str(data[section]))}文字",
                        details="最低50文字以上の説明が必要です"
                    ))
                elif section in ['notes', 'rules'] and len(data[section]) < 3:
                    results.append(self._create_error_result(
                        f"{section}項目数不足: {len(data[section])}項目",
                        details="最低3項目以上が必要です"
                    ))
            
            # 必須フィールドチェック
            required_fields = ['table_name', 'logical_name', 'columns']
            for field in required_fields:
                if field not in data:
                    results.append(self._create_error_result(
                        f"必須フィールド不足: {field}"
                    ))
            
        except yaml.YAMLError as e:
            results.append(self._create_error_result(
                f"YAML構文エラー: {str(e)}"
            ))
        except Exception as e:
            results.append(self._create_error_result(
                f"YAMLバリデーションエラー: {str(e)}"
            ))
        
        return results
    
    def _validate_ddl(self, ddl_path: Path) -> List[CheckResult]:
        """DDL形式のバリデーション"""
        results = []
        
        try:
            with open(ddl_path, 'r', encoding=self.config.tool.encoding) as f:
                content = f.read()
            
            # CREATE TABLE文の存在チェック
            if not re.search(r'CREATE\s+TABLE', content, re.IGNORECASE):
                results.append(self._create_error_result(
                    "CREATE TABLE文が見つかりません"
                ))
            
        except Exception as e:
            results.append(self._create_error_result(
                f"DDLバリデーションエラー: {str(e)}"
            ))
        
        return results
    
    def _validate_markdown(self, md_path: Path) -> List[CheckResult]:
        """Markdown形式のバリデーション"""
        results = []
        
        try:
            with open(md_path, 'r', encoding=self.config.tool.encoding) as f:
                content = f.read()
            
            # 基本的な内容チェック
            if len(content.strip()) == 0:
                results.append(self._create_error_result(
                    "Markdownファイルが空です"
                ))
            
        except Exception as e:
            results.append(self._create_error_result(
                f"Markdownバリデーションエラー: {str(e)}"
            ))
        
        return results
