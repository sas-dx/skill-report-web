"""
DDLジェネレーター
テーブル定義からDDL（SQL）ファイルを生成する機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム
"""

from typing import List, Optional
from datetime import datetime

from .base_generator import BaseGenerator
from ..core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition


class DdlGenerator(BaseGenerator):
    """DDLジェネレーター"""
    
    def __init__(self, config=None):
        super().__init__(config)
        self.database_type = self.config.get('database_type', 'postgresql')
        self.include_comments = self.config.get('include_comments', True)
        self.include_indexes = self.config.get('include_indexes', True)
        self.include_foreign_keys = self.config.get('include_foreign_keys', True)
        self.include_drop_statements = self.config.get('include_drop_statements', False)
    
    def generate(self, table_def: TableDefinition, output_path: Optional[str] = None) -> str:
        """
        テーブル定義からDDLを生成
        
        Args:
            table_def: テーブル定義オブジェクト
            output_path: 出力ファイルパス（未使用）
            
        Returns:
            str: 生成されたDDL
        """
        self._log_generation_start(table_def)
        
        try:
            ddl_parts = []
            
            # ヘッダーコメント
            ddl_parts.append(self._generate_header_comment(table_def))
            
            # DROP文（オプション）
            if self.include_drop_statements:
                ddl_parts.append(self._generate_drop_statements(table_def))
            
            # CREATE TABLE文
            ddl_parts.append(self._generate_create_table(table_def))
            
            # インデックス作成文
            if self.include_indexes and table_def.indexes:
                ddl_parts.append(self._generate_indexes(table_def))
            
            # 外部キー制約
            if self.include_foreign_keys and table_def.foreign_keys:
                ddl_parts.append(self._generate_foreign_keys(table_def))
            
            # テーブルコメント
            if self.include_comments and table_def.comment:
                ddl_parts.append(self._generate_table_comment(table_def))
            
            # カラムコメント
            if self.include_comments:
                column_comments = self._generate_column_comments(table_def)
                if column_comments:
                    ddl_parts.append(column_comments)
            
            ddl_content = '\n\n'.join(filter(None, ddl_parts))
            
            self._log_generation_complete(table_def)
            return ddl_content
            
        except Exception as e:
            raise self._handle_generation_error(e, table_def, "DDL生成エラー")
    
    def get_file_extension(self) -> str:
        """ファイル拡張子を取得"""
        return '.sql'
    
    def _generate_header_comment(self, table_def: TableDefinition) -> str:
        """ヘッダーコメントの生成"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        lines = [
            "-- " + "=" * 70,
            f"-- テーブル定義: {table_def.name}",
            f"-- 論理名: {table_def.logical_name}",
            f"-- カテゴリ: {table_def.category}",
            f"-- 要求仕様ID: {table_def.requirement_id}",
            f"-- 生成日時: {timestamp}",
            "-- " + "=" * 70
        ]
        
        return '\n'.join(lines)
    
    def _generate_drop_statements(self, table_def: TableDefinition) -> str:
        """DROP文の生成"""
        lines = [
            "-- テーブル削除（存在する場合）",
            f"DROP TABLE IF EXISTS {table_def.name} CASCADE;"
        ]
        
        return '\n'.join(lines)
    
    def _generate_create_table(self, table_def: TableDefinition) -> str:
        """CREATE TABLE文の生成"""
        lines = [
            f"-- テーブル作成: {table_def.name}",
            f"CREATE TABLE {table_def.name} ("
        ]
        
        # カラム定義
        column_definitions = []
        for column in table_def.columns:
            column_def = self._generate_column_definition(column)
            column_definitions.append(f"    {column_def}")
        
        # 制約定義
        constraints = self._generate_table_constraints(table_def)
        if constraints:
            column_definitions.extend([f"    {constraint}" for constraint in constraints])
        
        lines.append(',\n'.join(column_definitions))
        lines.append(");")
        
        return '\n'.join(lines)
    
    def _generate_column_definition(self, column: ColumnDefinition) -> str:
        """カラム定義の生成"""
        parts = [column.name, column.type]
        
        # NOT NULL制約
        if not column.nullable:
            parts.append("NOT NULL")
        
        # デフォルト値
        if column.default is not None:
            if isinstance(column.default, str) and not column.default.upper().startswith(('CURRENT_', 'NOW()')):
                parts.append(f"DEFAULT '{column.default}'")
            else:
                parts.append(f"DEFAULT {column.default}")
        
        # AUTO INCREMENT（PostgreSQLの場合はSERIAL型で対応）
        if column.auto_increment and self.database_type == 'postgresql':
            # SERIAL型の場合は既に型で指定済み
            pass
        elif column.auto_increment and self.database_type == 'mysql':
            parts.append("AUTO_INCREMENT")
        
        # CHECK制約
        if column.check_constraint:
            parts.append(f"CHECK ({column.check_constraint})")
        
        return ' '.join(parts)
    
    def _generate_table_constraints(self, table_def: TableDefinition) -> List[str]:
        """テーブル制約の生成"""
        constraints = []
        
        # プライマリキー制約
        pk_columns = [col.name for col in table_def.columns if col.primary_key]
        if pk_columns:
            pk_name = f"pk_{table_def.name.lower()}"
            constraints.append(f"CONSTRAINT {pk_name} PRIMARY KEY ({', '.join(pk_columns)})")
        
        # ユニーク制約
        unique_columns = [col.name for col in table_def.columns if col.unique and not col.primary_key]
        for col_name in unique_columns:
            uk_name = f"uk_{table_def.name.lower()}_{col_name.lower()}"
            constraints.append(f"CONSTRAINT {uk_name} UNIQUE ({col_name})")
        
        return constraints
    
    def _generate_indexes(self, table_def: TableDefinition) -> str:
        """インデックス作成文の生成"""
        lines = [f"-- インデックス作成: {table_def.name}"]
        
        for index in table_def.indexes:
            index_sql = self._generate_index_definition(table_def.name, index)
            lines.append(index_sql)
        
        return '\n'.join(lines)
    
    def _generate_index_definition(self, table_name: str, index: IndexDefinition) -> str:
        """インデックス定義の生成"""
        index_type = "UNIQUE INDEX" if index.unique else "INDEX"
        columns = ', '.join(index.columns)
        
        sql = f"CREATE {index_type} {index.name} ON {table_name} ({columns})"
        
        # PostgreSQLの場合のインデックスタイプ指定
        if self.database_type == 'postgresql' and index.type and index.type != 'btree':
            sql += f" USING {index.type}"
        
        sql += ";"
        
        # コメント
        if index.comment:
            sql += f" -- {index.comment}"
        
        return sql
    
    def _generate_foreign_keys(self, table_def: TableDefinition) -> str:
        """外部キー制約の生成"""
        lines = [f"-- 外部キー制約: {table_def.name}"]
        
        for fk in table_def.foreign_keys:
            fk_sql = self._generate_foreign_key_definition(table_def.name, fk)
            lines.append(fk_sql)
        
        return '\n'.join(lines)
    
    def _generate_foreign_key_definition(self, table_name: str, fk: ForeignKeyDefinition) -> str:
        """外部キー定義の生成"""
        columns = ', '.join(fk.columns)
        ref_columns = ', '.join(fk.references_columns)
        
        sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {fk.name} "
        sql += f"FOREIGN KEY ({columns}) REFERENCES {fk.references_table} ({ref_columns})"
        
        # ON UPDATE/DELETE アクション
        if fk.on_update and fk.on_update != 'RESTRICT':
            sql += f" ON UPDATE {fk.on_update}"
        
        if fk.on_delete and fk.on_delete != 'RESTRICT':
            sql += f" ON DELETE {fk.on_delete}"
        
        sql += ";"
        
        # コメント
        if fk.comment:
            sql += f" -- {fk.comment}"
        
        return sql
    
    def _generate_table_comment(self, table_def: TableDefinition) -> str:
        """テーブルコメントの生成"""
        if self.database_type == 'postgresql':
            return f"COMMENT ON TABLE {table_def.name} IS '{table_def.comment}';"
        elif self.database_type == 'mysql':
            # MySQLの場合はCREATE TABLE文でCOMMENTを指定
            return f"ALTER TABLE {table_def.name} COMMENT = '{table_def.comment}';"
        else:
            return f"-- テーブルコメント: {table_def.comment}"
    
    def _generate_column_comments(self, table_def: TableDefinition) -> str:
        """カラムコメントの生成"""
        lines = [f"-- カラムコメント: {table_def.name}"]
        
        for column in table_def.columns:
            if column.comment:
                if self.database_type == 'postgresql':
                    comment_sql = f"COMMENT ON COLUMN {table_def.name}.{column.name} IS '{column.comment}';"
                elif self.database_type == 'mysql':
                    comment_sql = f"ALTER TABLE {table_def.name} MODIFY {column.name} {column.type} COMMENT '{column.comment}';"
                else:
                    comment_sql = f"-- {column.name}: {column.comment}"
                
                lines.append(comment_sql)
        
        return '\n'.join(lines) if len(lines) > 1 else ""
    
    def _generate_filename(self, table_def: TableDefinition) -> str:
        """ファイル名の生成（オーバーライド）"""
        return f"{table_def.name}.sql"


# ジェネレーターファクトリーへの登録
from .base_generator import GeneratorFactory
GeneratorFactory.register_generator('.sql', DdlGenerator)


# 便利関数
def generate_ddl(table_def: TableDefinition, config=None) -> str:
    """
    テーブル定義からDDLを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        config: 設定オブジェクト
        
    Returns:
        str: 生成されたDDL
    """
    generator = DdlGenerator(config)
    return generator.generate(table_def)


def generate_ddl_file(table_def: TableDefinition, output_path: str, config=None) -> None:
    """
    テーブル定義からDDLファイルを生成する便利関数
    
    Args:
        table_def: テーブル定義オブジェクト
        output_path: 出力ファイルパス
        config: 設定オブジェクト
    """
    generator = DdlGenerator(config)
    generator.generate_to_file(table_def, output_path)
