"""
DDLジェネレーター

TableDefinitionからDDL（CREATE TABLE文）を生成する
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition

logger = logging.getLogger(__name__)


class DDLGenerator:
    """DDLジェネレーター"""
    
    def __init__(self, config=None):
        """初期化
        
        Args:
            config: 設定辞書（オプション）
        """
        self.config = config or {}
    
    def generate(self, table_definition: TableDefinition) -> str:
        """
        TableDefinitionからDDLを生成
        
        Args:
            table_definition: テーブル定義
            
        Returns:
            str: DDL内容
        """
        try:
            lines = []
            
            # 設定オプションの取得
            include_comments = self.config.get('include_comments', True)
            include_drop_statements = self.config.get('include_drop_statements', False)
            include_indexes = self.config.get('include_indexes', True)
            include_foreign_keys = self.config.get('include_foreign_keys', True)
            database_type = self.config.get('database_type', 'postgresql')
            
            # ヘッダーコメント
            if include_comments:
                lines.append(f"-- {table_definition.table_name} ({table_definition.logical_name})")
                lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                lines.append(f"-- カテゴリ: {table_definition.category}")
                lines.append(f"-- 要求仕様ID: {table_definition.requirement_id}")
                lines.append("")
            
            # DROP文（オプション）
            if include_drop_statements:
                if database_type == 'postgresql':
                    lines.append(f"DROP TABLE IF EXISTS {table_definition.table_name} CASCADE;")
                else:
                    lines.append(f"DROP TABLE IF EXISTS {table_definition.table_name};")
                lines.append("")
            
            # CREATE TABLE文
            lines.append(f"CREATE TABLE {table_definition.table_name} (")
            
            # カラム定義
            column_lines = []
            for column in table_definition.columns:
                column_def = self._generate_column_definition(column)
                column_lines.append(f"    {column_def}")
            
            # 主キー制約
            primary_key_columns = [col.name for col in table_definition.columns if col.primary_key]
            if primary_key_columns:
                pk_constraint = f"PRIMARY KEY ({', '.join(primary_key_columns)})"
                column_lines.append(f"    {pk_constraint}")
            
            # カラム定義を結合
            lines.append(",\n".join(column_lines))
            lines.append(");")
            lines.append("")
            
            # インデックス作成
            if include_indexes and table_definition.indexes:
                if include_comments:
                    lines.append("-- インデックス作成")
                for index in table_definition.indexes:
                    index_ddl = self._generate_index_definition(table_definition.table_name, index)
                    lines.append(index_ddl)
                lines.append("")
            
            # 外部キー制約
            if include_foreign_keys and table_definition.foreign_keys:
                if include_comments:
                    lines.append("-- 外部キー制約")
                for fk in table_definition.foreign_keys:
                    fk_ddl = self._generate_foreign_key_definition(table_definition.table_name, fk)
                    lines.append(fk_ddl)
                lines.append("")
            
            # テーブルコメント
            if include_comments and table_definition.logical_name:
                if database_type == 'mysql':
                    # MySQLの場合はCREATE TABLE文内でCOMMENTを指定
                    pass  # 既にCREATE TABLE文で処理済み
                else:
                    # PostgreSQLの場合
                    comment_ddl = f"COMMENT ON TABLE {table_definition.table_name} IS '{table_definition.logical_name}';"
                    lines.append(comment_ddl)
                    lines.append("")
            
            # カラムコメント
            if include_comments:
                for column in table_definition.columns:
                    if column.comment:
                        if database_type == 'mysql':
                            # MySQLの場合はCREATE TABLE文内でCOMMENTを指定
                            pass  # 既にCREATE TABLE文で処理済み
                        else:
                            # PostgreSQLの場合
                            comment_ddl = f"COMMENT ON COLUMN {table_definition.table_name}.{column.name} IS '{column.comment}';"
                            lines.append(comment_ddl)
                
                if any(col.comment for col in table_definition.columns) and database_type != 'mysql':
                    lines.append("")
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"DDL生成エラー: {e}")
            raise
    
    def _generate_column_definition(self, column: ColumnDefinition) -> str:
        """
        カラム定義を生成
        
        Args:
            column: カラム定義
            
        Returns:
            str: カラム定義文字列
        """
        parts = [column.name, column.type]
        
        # NOT NULL制約
        if not column.nullable:
            parts.append("NOT NULL")
        
        # デフォルト値
        if column.default is not None:
            # 文字列の場合のみ.upper()を呼び出し
            if isinstance(column.default, str):
                if column.default.upper() in ['CURRENT_TIMESTAMP', 'NOW()', 'UUID_GENERATE_V4()']:
                    parts.append(f"DEFAULT {column.default}")
                elif column.default.lower() in ['true', 'false']:
                    # ブール値の場合
                    parts.append(f"DEFAULT {column.default.upper()}")
                else:
                    parts.append(f"DEFAULT '{column.default}'")
            elif isinstance(column.default, bool):
                # ブール値の場合
                parts.append(f"DEFAULT {str(column.default).upper()}")
            elif isinstance(column.default, (int, float)):
                # 数値の場合
                parts.append(f"DEFAULT {column.default}")
            else:
                # その他の場合は文字列として扱う
                parts.append(f"DEFAULT '{column.default}'")
        
        # MySQLのCOMMENT構文（設定に応じて）
        database_type = self.config.get('database_type', 'postgresql')
        include_comments = self.config.get('include_comments', True)
        if include_comments and database_type == 'mysql' and column.comment:
            parts.append(f"COMMENT '{column.comment}'")
        
        return " ".join(parts)
    
    def _generate_index_definition(self, table_name: str, index: IndexDefinition) -> str:
        """
        インデックス定義を生成
        
        Args:
            table_name: テーブル名
            index: インデックス定義
            
        Returns:
            str: インデックス定義文字列
        """
        index_type = "UNIQUE INDEX" if index.unique else "INDEX"
        columns_str = ", ".join(index.columns)
        
        ddl = f"CREATE {index_type} {index.name} ON {table_name} ({columns_str});"
        
        if index.comment:
            ddl += f" -- {index.comment}"
        
        return ddl
    
    def _generate_foreign_key_definition(self, table_name: str, fk: ForeignKeyDefinition) -> str:
        """
        外部キー定義を生成
        
        Args:
            table_name: テーブル名
            fk: 外部キー定義
            
        Returns:
            str: 外部キー定義文字列
        """
        columns_str = ", ".join(fk.columns)
        ref_columns_str = ", ".join(fk.references_columns)
        
        ddl = f"ALTER TABLE {table_name} ADD CONSTRAINT {fk.name} "
        ddl += f"FOREIGN KEY ({columns_str}) "
        ddl += f"REFERENCES {fk.references_table} ({ref_columns_str})"
        
        if fk.on_update and fk.on_update.upper() != 'NO ACTION':
            ddl += f" ON UPDATE {fk.on_update}"
        
        if fk.on_delete and fk.on_delete.upper() != 'NO ACTION':
            ddl += f" ON DELETE {fk.on_delete}"
        
        ddl += ";"
        
        return ddl
