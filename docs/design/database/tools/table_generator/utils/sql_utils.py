#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - SQL生成ユーティリティ

SQL文生成の共通機能を提供します。

対応要求仕様ID: PLT.2-TOOL.1
"""

from typing import List, Dict, Any, Optional
from shared.core.logger import get_logger
from shared.core.models import ColumnDefinition


class SqlUtils:
    """SQL生成ユーティリティクラス
    
    DDL、DML、INSERT文などのSQL生成機能を提供します。
    """
    
    def __init__(self, logger=None):
        """初期化
        
        Args:
            logger (DatabaseToolsLogger, optional): ログ出力インスタンス
        """
        self.logger = logger or get_logger()
    
    def generate_create_table_sql(self, table_name: str, columns: List[ColumnDefinition], 
                                  charset: str = 'utf8mb4', collation: str = 'utf8mb4_unicode_ci') -> str:
        """CREATE TABLE文を生成
        
        Args:
            table_name (str): テーブル名
            columns (List[ColumnDefinition]): カラム定義リスト
            charset (str): 文字セット
            collation (str): 照合順序
            
        Returns:
            str: CREATE TABLE文
        """
        try:
            sql_lines = [f"CREATE TABLE {table_name} ("]
            
            column_definitions = []
            primary_keys = []
            
            for column in columns:
                col_def = self._generate_column_definition(column)
                column_definitions.append(f"    {col_def}")
                
                if column.primary:
                    primary_keys.append(column.name)
            
            # プライマリキー制約を追加
            if primary_keys:
                pk_def = f"    PRIMARY KEY ({', '.join(primary_keys)})"
                column_definitions.append(pk_def)
            
            sql_lines.append(',\n'.join(column_definitions))
            sql_lines.append(f") ENGINE=InnoDB DEFAULT CHARSET={charset} COLLATE={collation};")
            
            return '\n'.join(sql_lines)
            
        except Exception as e:
            self.logger.error(f"CREATE TABLE文生成エラー: {e}")
            return ""
    
    def _generate_column_definition(self, column: ColumnDefinition) -> str:
        """カラム定義文を生成
        
        Args:
            column (ColumnDefinition): カラム定義
            
        Returns:
            str: カラム定義文
        """
        col_type = column.data_type.upper()
        
        # 長さ指定
        if column.length and col_type in ['VARCHAR', 'CHAR', 'DECIMAL', 'NUMERIC']:
            col_type += f"({column.length})"
        
        col_def = f"{column.name} {col_type}"
        
        # NULL制約
        if not column.nullable:
            col_def += " NOT NULL"
        
        # デフォルト値
        if column.default is not None:
            if isinstance(column.default, str) and column.default.upper() not in ['CURRENT_TIMESTAMP', 'NULL']:
                col_def += f" DEFAULT '{column.default}'"
            else:
                col_def += f" DEFAULT {column.default}"
        
        # AUTO_INCREMENT（主キーかつINTEGER系の場合）
        if column.primary and col_type.startswith(('INT', 'BIGINT', 'SMALLINT')):
            col_def += " AUTO_INCREMENT"
        
        # コメント
        if column.description:
            escaped_desc = column.description.replace("'", "''")
            col_def += f" COMMENT '{escaped_desc}'"
        
        return col_def
    
    def generate_create_index_sql(self, table_name: str, index_name: str, 
                                  columns: List[str], unique: bool = False) -> str:
        """CREATE INDEX文を生成
        
        Args:
            table_name (str): テーブル名
            index_name (str): インデックス名
            columns (List[str]): カラム名リスト
            unique (bool): ユニークインデックスフラグ
            
        Returns:
            str: CREATE INDEX文
        """
        try:
            unique_str = "UNIQUE " if unique else ""
            columns_str = ", ".join(columns)
            
            return f"CREATE {unique_str}INDEX {index_name} ON {table_name} ({columns_str});"
            
        except Exception as e:
            self.logger.error(f"CREATE INDEX文生成エラー: {e}")
            return ""
    
    def generate_add_foreign_key_sql(self, table_name: str, constraint_name: str,
                                     column: str, reference_table: str, reference_column: str,
                                     on_update: str = "CASCADE", on_delete: str = "CASCADE") -> str:
        """ALTER TABLE ADD FOREIGN KEY文を生成
        
        Args:
            table_name (str): テーブル名
            constraint_name (str): 制約名
            column (str): カラム名
            reference_table (str): 参照テーブル名
            reference_column (str): 参照カラム名
            on_update (str): 更新時動作
            on_delete (str): 削除時動作
            
        Returns:
            str: ALTER TABLE ADD FOREIGN KEY文
        """
        try:
            sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint_name} "
            sql += f"FOREIGN KEY ({column}) REFERENCES {reference_table}({reference_column}) "
            sql += f"ON UPDATE {on_update} ON DELETE {on_delete};"
            
            return sql
            
        except Exception as e:
            self.logger.error(f"FOREIGN KEY文生成エラー: {e}")
            return ""
    
    def generate_insert_sql(self, table_name: str, data: List[Dict[str, Any]], 
                            batch_size: int = 1000) -> List[str]:
        """INSERT文を生成（バッチ対応）
        
        Args:
            table_name (str): テーブル名
            data (List[Dict[str, Any]]): 挿入データリスト
            batch_size (int): バッチサイズ
            
        Returns:
            List[str]: INSERT文のリスト
        """
        try:
            if not data:
                return []
            
            insert_statements = []
            
            # カラム名を取得（最初のデータから）
            columns = list(data[0].keys())
            columns_str = ", ".join(columns)
            
            # バッチごとに処理
            for i in range(0, len(data), batch_size):
                batch_data = data[i:i + batch_size]
                
                values_list = []
                for row in batch_data:
                    values = []
                    for col in columns:
                        value = row.get(col)
                        if value is None:
                            values.append("NULL")
                        elif isinstance(value, str):
                            escaped_value = value.replace("'", "''")
                            values.append(f"'{escaped_value}'")
                        elif isinstance(value, bool):
                            values.append("1" if value else "0")
                        else:
                            values.append(str(value))
                    
                    values_list.append(f"({', '.join(values)})")
                
                sql = f"INSERT INTO {table_name} ({columns_str}) VALUES\n"
                sql += ",\n".join(values_list) + ";"
                
                insert_statements.append(sql)
            
            return insert_statements
            
        except Exception as e:
            self.logger.error(f"INSERT文生成エラー: {e}")
            return []
    
    def generate_update_sql(self, table_name: str, set_data: Dict[str, Any], 
                            where_conditions: Dict[str, Any]) -> str:
        """UPDATE文を生成
        
        Args:
            table_name (str): テーブル名
            set_data (Dict[str, Any]): 更新データ
            where_conditions (Dict[str, Any]): WHERE条件
            
        Returns:
            str: UPDATE文
        """
        try:
            if not set_data:
                return ""
            
            # SET句を生成
            set_clauses = []
            for column, value in set_data.items():
                if value is None:
                    set_clauses.append(f"{column} = NULL")
                elif isinstance(value, str):
                    escaped_value = value.replace("'", "''")
                    set_clauses.append(f"{column} = '{escaped_value}'")
                elif isinstance(value, bool):
                    set_clauses.append(f"{column} = {'1' if value else '0'}")
                else:
                    set_clauses.append(f"{column} = {value}")
            
            sql = f"UPDATE {table_name} SET {', '.join(set_clauses)}"
            
            # WHERE句を生成
            if where_conditions:
                where_clauses = []
                for column, value in where_conditions.items():
                    if value is None:
                        where_clauses.append(f"{column} IS NULL")
                    elif isinstance(value, str):
                        escaped_value = value.replace("'", "''")
                        where_clauses.append(f"{column} = '{escaped_value}'")
                    elif isinstance(value, bool):
                        where_clauses.append(f"{column} = {'1' if value else '0'}")
                    else:
                        where_clauses.append(f"{column} = {value}")
                
                sql += f" WHERE {' AND '.join(where_clauses)}"
            
            sql += ";"
            return sql
            
        except Exception as e:
            self.logger.error(f"UPDATE文生成エラー: {e}")
            return ""
    
    def generate_delete_sql(self, table_name: str, where_conditions: Dict[str, Any]) -> str:
        """DELETE文を生成
        
        Args:
            table_name (str): テーブル名
            where_conditions (Dict[str, Any]): WHERE条件
            
        Returns:
            str: DELETE文
        """
        try:
            sql = f"DELETE FROM {table_name}"
            
            # WHERE句を生成
            if where_conditions:
                where_clauses = []
                for column, value in where_conditions.items():
                    if value is None:
                        where_clauses.append(f"{column} IS NULL")
                    elif isinstance(value, str):
                        escaped_value = value.replace("'", "''")
                        where_clauses.append(f"{column} = '{escaped_value}'")
                    elif isinstance(value, bool):
                        where_clauses.append(f"{column} = {'1' if value else '0'}")
                    else:
                        where_clauses.append(f"{column} = {value}")
                
                sql += f" WHERE {' AND '.join(where_clauses)}"
            
            sql += ";"
            return sql
            
        except Exception as e:
            self.logger.error(f"DELETE文生成エラー: {e}")
            return ""
    
    def generate_select_sql(self, table_name: str, columns: List[str] = None,
                            where_conditions: Dict[str, Any] = None,
                            order_by: List[str] = None, limit: int = None) -> str:
        """SELECT文を生成
        
        Args:
            table_name (str): テーブル名
            columns (List[str], optional): 選択カラムリスト
            where_conditions (Dict[str, Any], optional): WHERE条件
            order_by (List[str], optional): ORDER BY句
            limit (int, optional): LIMIT句
            
        Returns:
            str: SELECT文
        """
        try:
            # SELECT句
            if columns:
                columns_str = ", ".join(columns)
            else:
                columns_str = "*"
            
            sql = f"SELECT {columns_str} FROM {table_name}"
            
            # WHERE句
            if where_conditions:
                where_clauses = []
                for column, value in where_conditions.items():
                    if value is None:
                        where_clauses.append(f"{column} IS NULL")
                    elif isinstance(value, str):
                        escaped_value = value.replace("'", "''")
                        where_clauses.append(f"{column} = '{escaped_value}'")
                    elif isinstance(value, bool):
                        where_clauses.append(f"{column} = {'1' if value else '0'}")
                    else:
                        where_clauses.append(f"{column} = {value}")
                
                sql += f" WHERE {' AND '.join(where_clauses)}"
            
            # ORDER BY句
            if order_by:
                sql += f" ORDER BY {', '.join(order_by)}"
            
            # LIMIT句
            if limit:
                sql += f" LIMIT {limit}"
            
            sql += ";"
            return sql
            
        except Exception as e:
            self.logger.error(f"SELECT文生成エラー: {e}")
            return ""
    
    def escape_sql_string(self, value: str) -> str:
        """SQL文字列をエスケープ
        
        Args:
            value (str): エスケープ対象文字列
            
        Returns:
            str: エスケープ済み文字列
        """
        if value is None:
            return "NULL"
        
        # シングルクォートをエスケープ
        escaped = str(value).replace("'", "''")
        
        # バックスラッシュをエスケープ
        escaped = escaped.replace("\\", "\\\\")
        
        return f"'{escaped}'"
    
    def format_sql(self, sql: str, indent: str = "    ") -> str:
        """SQL文を整形
        
        Args:
            sql (str): 整形対象SQL文
            indent (str): インデント文字列
            
        Returns:
            str: 整形済みSQL文
        """
        try:
            # 基本的なSQL整形
            keywords = ['SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'HAVING', 'LIMIT',
                       'INSERT INTO', 'VALUES', 'UPDATE', 'SET', 'DELETE FROM',
                       'CREATE TABLE', 'ALTER TABLE', 'DROP TABLE']
            
            formatted_sql = sql
            
            for keyword in keywords:
                formatted_sql = formatted_sql.replace(keyword, f"\n{keyword}")
            
            # インデントを追加
            lines = formatted_sql.split('\n')
            formatted_lines = []
            
            for line in lines:
                stripped_line = line.strip()
                if stripped_line:
                    if any(stripped_line.startswith(kw) for kw in keywords):
                        formatted_lines.append(stripped_line)
                    else:
                        formatted_lines.append(f"{indent}{stripped_line}")
            
            return '\n'.join(formatted_lines)
            
        except Exception as e:
            self.logger.error(f"SQL整形エラー: {e}")
            return sql
    
    def generate_drop_table_sql(self, table_name: str, if_exists: bool = True) -> str:
        """DROP TABLE文を生成
        
        Args:
            table_name (str): テーブル名
            if_exists (bool): IF EXISTSフラグ
            
        Returns:
            str: DROP TABLE文
        """
        try:
            if_exists_str = "IF EXISTS " if if_exists else ""
            return f"DROP TABLE {if_exists_str}{table_name};"
            
        except Exception as e:
            self.logger.error(f"DROP TABLE文生成エラー: {e}")
            return ""
    
    def generate_truncate_table_sql(self, table_name: str) -> str:
        """TRUNCATE TABLE文を生成
        
        Args:
            table_name (str): テーブル名
            
        Returns:
            str: TRUNCATE TABLE文
        """
        return f"TRUNCATE TABLE {table_name};"
