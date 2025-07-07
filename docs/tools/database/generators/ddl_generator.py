"""
DDL統一ジェネレーター

YAMLデータからDDL（SQL）ファイルを生成
"""

from typing import Dict, Any, List
from datetime import datetime

from .base_generator import BaseGenerator
from ..core import ValidationResult, GenerationError


class DdlGenerator(BaseGenerator):
    """DDL専用ジェネレーター"""
    
    def __init__(self):
        super().__init__("ddl")
        self.sql_templates = {
            'postgresql': self._get_postgresql_templates(),
            'mysql': self._get_mysql_templates(),
            'sqlite': self._get_sqlite_templates()
        }
    
    def get_supported_formats(self) -> List[str]:
        """サポートする出力形式"""
        return ['sql', 'ddl']
    
    def generate(self, data: Dict[str, Any], output_path: str, **kwargs) -> bool:
        """
        YAMLデータからDDLファイルを生成
        
        Args:
            data: YAML解析データ
            output_path: 出力ファイルパス
            **kwargs: 追加オプション
                - db_type: データベースタイプ (postgresql, mysql, sqlite)
                - include_comments: コメント含有フラグ
                - include_indexes: インデックス含有フラグ
                
        Returns:
            生成成功フラグ
            
        Raises:
            GenerationError: 生成エラー
        """
        # データ検証
        validation_result = self.validate_data(data)
        if not validation_result.is_valid:
            raise GenerationError(f"データ検証エラー: {validation_result.get_error_summary()}")
        
        # 出力パス検証
        self._validate_output_path(output_path)
        self._validate_file_writable(output_path)
        
        # オプション取得
        db_type = kwargs.get('db_type', 'postgresql').lower()
        include_comments = kwargs.get('include_comments', True)
        include_indexes = kwargs.get('include_indexes', True)
        
        if db_type not in self.sql_templates:
            raise GenerationError(f"サポートされていないデータベースタイプ: {db_type}")
        
        try:
            # DDL生成
            ddl_content = self._generate_ddl(data, db_type, include_comments, include_indexes)
            
            # バックアップ作成
            self._backup_existing_file(output_path)
            
            # ファイル書き込み
            self._write_file(output_path, ddl_content)
            
            self.logger.info(f"DDLファイルを生成: {output_path}")
            return True
            
        except Exception as e:
            if isinstance(e, GenerationError):
                raise
            raise GenerationError(f"DDL生成エラー: {str(e)}")
    
    def validate_data(self, data: Dict[str, Any]) -> ValidationResult:
        """
        生成用データの妥当性を検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            検証結果
        """
        result = ValidationResult(is_valid=True)
        
        # 必須フィールドの検証
        required_fields = ['table_name', 'columns']
        for field in required_fields:
            if field not in data:
                result.add_error(f"必須フィールドが不足: {field}")
        
        # テーブル名の検証
        table_name = data.get('table_name', '')
        if not table_name:
            result.add_error("テーブル名が空です")
        elif not self._is_valid_identifier(table_name):
            result.add_error(f"無効なテーブル名: {table_name}")
        
        # カラム定義の検証
        columns = data.get('columns', [])
        if not isinstance(columns, list):
            result.add_error("カラム定義はリスト形式である必要があります")
        elif len(columns) == 0:
            result.add_error("最低1つのカラム定義が必要です")
        else:
            self._validate_columns(columns, result)
        
        return result
    
    def _generate_ddl(self, data: Dict[str, Any], db_type: str, include_comments: bool, include_indexes: bool) -> str:
        """DDL文を生成"""
        templates = self.sql_templates[db_type]
        
        # ヘッダーコメント
        header = self._generate_header_comment(data, db_type)
        
        # CREATE TABLE文
        create_table = self._generate_create_table(data, templates, include_comments)
        
        # インデックス文
        indexes = ""
        if include_indexes and data.get('indexes'):
            indexes = self._generate_indexes(data, templates)
        
        # 外部キー制約
        foreign_keys = ""
        if data.get('foreign_keys'):
            foreign_keys = self._generate_foreign_keys(data, templates)
        
        # DDL文を結合
        ddl_parts = [header, create_table]
        if indexes:
            ddl_parts.append(indexes)
        if foreign_keys:
            ddl_parts.append(foreign_keys)
        
        return "\n\n".join(ddl_parts) + "\n"
    
    def _generate_header_comment(self, data: Dict[str, Any], db_type: str) -> str:
        """ヘッダーコメントを生成"""
        table_name = data.get('table_name', '')
        logical_name = data.get('logical_name', '')
        comment = data.get('comment', '')
        
        header = f"""-- ============================================
-- テーブル定義: {table_name}
-- 論理名: {logical_name}
-- 説明: {comment}
-- データベース: {db_type.upper()}
-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ============================================"""
        
        return header
    
    def _generate_create_table(self, data: Dict[str, Any], templates: Dict[str, str], include_comments: bool) -> str:
        """CREATE TABLE文を生成"""
        table_name = data['table_name']
        columns = data['columns']
        
        # カラム定義を生成
        column_definitions = []
        for column in columns:
            col_def = self._generate_column_definition(column, templates)
            column_definitions.append(f"    {col_def}")
        
        # 制約を生成
        constraints = []
        
        # 主キー制約
        primary_keys = [col['name'] for col in columns if col.get('primary_key', False)]
        if primary_keys:
            pk_constraint = f"    PRIMARY KEY ({', '.join(primary_keys)})"
            constraints.append(pk_constraint)
        
        # 一意制約
        for column in columns:
            if column.get('unique', False) and not column.get('primary_key', False):
                unique_constraint = f"    UNIQUE ({column['name']})"
                constraints.append(unique_constraint)
        
        # CREATE TABLE文を構築
        all_definitions = column_definitions + constraints
        create_table = f"""CREATE TABLE {table_name} (
{',\n'.join(all_definitions)}
)"""
        
        # テーブルコメント
        if include_comments and data.get('comment'):
            table_comment = templates['table_comment'].format(
                table_name=table_name,
                comment=data['comment']
            )
            create_table += f";\n\n{table_comment}"
        else:
            create_table += ";"
        
        return create_table
    
    def _generate_column_definition(self, column: Dict[str, Any], templates: Dict[str, str]) -> str:
        """カラム定義を生成"""
        name = column['name']
        data_type = column['type']
        nullable = column.get('nullable', True)
        default = column.get('default')
        
        # データ型
        col_def = f"{name} {data_type}"
        
        # NULL制約
        if not nullable:
            col_def += " NOT NULL"
        
        # デフォルト値
        if default is not None:
            if isinstance(default, str) and not default.upper().startswith(('CURRENT_', 'NOW()', 'UUID_')):
                col_def += f" DEFAULT '{default}'"
            else:
                col_def += f" DEFAULT {default}"
        
        return col_def
    
    def _generate_indexes(self, data: Dict[str, Any], templates: Dict[str, str]) -> str:
        """インデックス文を生成"""
        table_name = data['table_name']
        indexes = data.get('indexes', [])
        
        index_statements = []
        for index in indexes:
            index_name = index.get('name', f"idx_{table_name}_{index['columns'][0]}")
            columns = index['columns']
            unique = index.get('unique', False)
            
            index_type = "UNIQUE INDEX" if unique else "INDEX"
            index_stmt = f"CREATE {index_type} {index_name} ON {table_name} ({', '.join(columns)});"
            
            if index.get('comment'):
                index_stmt += f" -- {index['comment']}"
            
            index_statements.append(index_stmt)
        
        return "\n".join(index_statements)
    
    def _generate_foreign_keys(self, data: Dict[str, Any], templates: Dict[str, str]) -> str:
        """外部キー制約を生成"""
        table_name = data['table_name']
        foreign_keys = data.get('foreign_keys', [])
        
        fk_statements = []
        for fk in foreign_keys:
            fk_name = fk.get('name', f"fk_{table_name}_{fk['columns'][0]}")
            columns = fk['columns']
            ref_table = fk['references']['table']
            ref_columns = fk['references']['columns']
            on_update = fk.get('on_update', 'RESTRICT')
            on_delete = fk.get('on_delete', 'RESTRICT')
            
            fk_stmt = f"""ALTER TABLE {table_name} 
    ADD CONSTRAINT {fk_name} 
    FOREIGN KEY ({', '.join(columns)}) 
    REFERENCES {ref_table} ({', '.join(ref_columns)})
    ON UPDATE {on_update} 
    ON DELETE {on_delete};"""
            
            if fk.get('comment'):
                fk_stmt += f" -- {fk['comment']}"
            
            fk_statements.append(fk_stmt)
        
        return "\n\n".join(fk_statements)
    
    def _validate_columns(self, columns: List[Dict[str, Any]], result: ValidationResult) -> None:
        """カラム定義の検証"""
        column_names = set()
        
        for i, column in enumerate(columns):
            if not isinstance(column, dict):
                result.add_error(f"カラム[{i}]は辞書形式である必要があります")
                continue
            
            # 必須フィールドの検証
            required_fields = ['name', 'type']
            for field in required_fields:
                if field not in column:
                    result.add_error(f"カラム[{i}]に必須フィールド '{field}' がありません")
            
            # カラム名の検証
            column_name = column.get('name', '')
            if not column_name:
                result.add_error(f"カラム[{i}]の名前が空です")
            elif not self._is_valid_identifier(column_name):
                result.add_error(f"カラム[{i}]の名前が無効: {column_name}")
            elif column_name in column_names:
                result.add_error(f"カラム名が重複: {column_name}")
            else:
                column_names.add(column_name)
            
            # データ型の検証
            data_type = column.get('type', '')
            if not data_type:
                result.add_error(f"カラム[{i}]のデータ型が空です")
    
    def _is_valid_identifier(self, identifier: str) -> bool:
        """SQL識別子の妥当性をチェック"""
        if not identifier:
            return False
        
        # 基本的なチェック（英数字とアンダースコア）
        import re
        return bool(re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', identifier))
    
    def _get_postgresql_templates(self) -> Dict[str, str]:
        """PostgreSQL用テンプレート"""
        return {
            'table_comment': "COMMENT ON TABLE {table_name} IS '{comment}';",
            'column_comment': "COMMENT ON COLUMN {table_name}.{column_name} IS '{comment}';",
            'data_types': {
                'INTEGER': 'INTEGER',
                'BIGINT': 'BIGINT',
                'VARCHAR': 'VARCHAR',
                'TEXT': 'TEXT',
                'TIMESTAMP': 'TIMESTAMP',
                'DATE': 'DATE',
                'BOOLEAN': 'BOOLEAN',
                'DECIMAL': 'DECIMAL',
                'UUID': 'UUID'
            }
        }
    
    def _get_mysql_templates(self) -> Dict[str, str]:
        """MySQL用テンプレート"""
        return {
            'table_comment': "ALTER TABLE {table_name} COMMENT = '{comment}';",
            'column_comment': "ALTER TABLE {table_name} MODIFY {column_name} {data_type} COMMENT '{comment}';",
            'data_types': {
                'INTEGER': 'INT',
                'BIGINT': 'BIGINT',
                'VARCHAR': 'VARCHAR',
                'TEXT': 'TEXT',
                'TIMESTAMP': 'TIMESTAMP',
                'DATE': 'DATE',
                'BOOLEAN': 'BOOLEAN',
                'DECIMAL': 'DECIMAL',
                'UUID': 'CHAR(36)'
            }
        }
    
    def _get_sqlite_templates(self) -> Dict[str, str]:
        """SQLite用テンプレート"""
        return {
            'table_comment': "-- Table comment: {comment}",
            'column_comment': "-- Column comment: {comment}",
            'data_types': {
                'INTEGER': 'INTEGER',
                'BIGINT': 'INTEGER',
                'VARCHAR': 'TEXT',
                'TEXT': 'TEXT',
                'TIMESTAMP': 'TEXT',
                'DATE': 'TEXT',
                'BOOLEAN': 'INTEGER',
                'DECIMAL': 'REAL',
                'UUID': 'TEXT'
            }
        }
    
    def get_output_filename(self, data: Dict[str, Any], format_type: str) -> str:
        """出力ファイル名を生成"""
        table_name = data.get('table_name', 'unknown')
        return f"{table_name}.sql"
