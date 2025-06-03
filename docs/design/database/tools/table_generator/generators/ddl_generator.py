#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DDL生成クラス

このモジュールは、テーブル定義からDDL（Data Definition Language）を生成する
機能を提供します。
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from table_generator.core.logger import EnhancedLogger
from table_generator.core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition
from table_generator.utils.sql_utils import SqlUtils


class DDLGenerator:
    """DDL生成クラス
    
    テーブル定義からCREATE TABLE文、インデックス、外部キーなどの
    DDLを生成します。
    """
    
    def __init__(self, logger: EnhancedLogger = None):
        """初期化
        
        Args:
            logger (EnhancedLogger, optional): ログ出力インスタンス
        """
        self.logger = logger or EnhancedLogger()
        self.sql_utils = SqlUtils(logger=self.logger)
        
        self.logger.info("DDLGenerator が初期化されました")
    
    def generate_table_ddl(self, table_def: TableDefinition, 
                          charset: str = 'utf8mb4', 
                          collation: str = 'utf8mb4_unicode_ci') -> str:
        """テーブルのDDLを生成
        
        Args:
            table_def (TableDefinition): テーブル定義
            charset (str): 文字セット
            collation (str): 照合順序
            
        Returns:
            str: 生成されたDDL
        """
        ddl_lines = []
        
        # ヘッダーコメント
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append(f"-- テーブル: {table_def.table_name}")
        ddl_lines.append(f"-- 論理名: {table_def.logical_name}")
        ddl_lines.append(f"-- 説明: {table_def.description}")
        ddl_lines.append(f"-- 作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append("")
        
        # DROP TABLE文（存在する場合）
        drop_sql = self.sql_utils.generate_drop_table_sql(table_def.table_name, if_exists=True)
        ddl_lines.append(drop_sql)
        ddl_lines.append("")
        
        # CREATE TABLE文
        create_sql = self.sql_utils.generate_create_table_sql(
            table_def.table_name, 
            table_def.business_columns,
            charset=charset,
            collation=collation
        )
        ddl_lines.append(create_sql)
        ddl_lines.append("")
        
        # インデックス作成
        if table_def.business_indexes:
            ddl_lines.append("-- インデックス作成")
            for index in table_def.business_indexes:
                index_sql = self._generate_index_ddl(table_def.table_name, index)
                ddl_lines.append(index_sql)
            ddl_lines.append("")
        
        # 外部キー制約
        if table_def.foreign_keys:
            ddl_lines.append("-- 外部キー制約")
            for fk in table_def.foreign_keys:
                fk_sql = self._generate_foreign_key_ddl(table_def.table_name, fk)
                ddl_lines.append(fk_sql)
            ddl_lines.append("")
        
        # その他の制約
        if table_def.business_constraints:
            ddl_lines.append("-- その他の制約")
            for constraint in table_def.business_constraints:
                constraint_sql = self._generate_constraint_ddl(table_def.table_name, constraint)
                ddl_lines.append(constraint_sql)
            ddl_lines.append("")
        
        # 初期データ挿入
        if table_def.initial_data:
            ddl_lines.append("-- 初期データ挿入")
            insert_sql = self._generate_initial_data_ddl(table_def.table_name, table_def.initial_data)
            ddl_lines.extend(insert_sql)
            ddl_lines.append("")
        
        return "\n".join(ddl_lines)
    
    def _generate_index_ddl(self, table_name: str, index: IndexDefinition) -> str:
        """インデックスDDLを生成
        
        Args:
            table_name (str): テーブル名
            index (IndexDefinition): インデックス定義
            
        Returns:
            str: インデックスDDL
        """
        return self.sql_utils.generate_create_index_sql(
            table_name=table_name,
            index_name=index.name,
            columns=index.columns,
            unique=index.unique
        )
    
    def _generate_foreign_key_ddl(self, table_name: str, fk: ForeignKeyDefinition) -> str:
        """外部キーDDLを生成
        
        Args:
            table_name (str): テーブル名
            fk (ForeignKeyDefinition): 外部キー定義
            
        Returns:
            str: 外部キーDDL
        """
        return self.sql_utils.generate_add_foreign_key_sql(
            table_name=table_name,
            constraint_name=fk.name,
            column=fk.column,
            reference_table=fk.reference_table,
            reference_column=fk.reference_column,
            on_delete=getattr(fk, 'on_delete', 'RESTRICT'),
            on_update=getattr(fk, 'on_update', 'RESTRICT')
        )
    
    def _generate_constraint_ddl(self, table_name: str, constraint) -> str:
        """制約DDLを生成
        
        Args:
            table_name (str): テーブル名
            constraint: 制約定義
            
        Returns:
            str: 制約DDL
        """
        # 制約の種類に応じてDDLを生成
        if constraint.type.upper() == 'CHECK':
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint.name} CHECK ({constraint.definition});"
        elif constraint.type.upper() == 'UNIQUE':
            columns = ', '.join(constraint.columns) if hasattr(constraint, 'columns') else constraint.definition
            return f"ALTER TABLE {table_name} ADD CONSTRAINT {constraint.name} UNIQUE ({columns});"
        else:
            return f"-- 未対応の制約タイプ: {constraint.type}"
    
    def _generate_initial_data_ddl(self, table_name: str, initial_data: List[Dict[str, Any]]) -> List[str]:
        """初期データ挿入DDLを生成
        
        Args:
            table_name (str): テーブル名
            initial_data (List[Dict[str, Any]]): 初期データ
            
        Returns:
            List[str]: 初期データ挿入DDLリスト
        """
        if not initial_data:
            return []
        
        insert_sqls = self.sql_utils.generate_insert_sql(table_name, initial_data)
        return insert_sqls
    
    def generate_migration_ddl(self, old_table_def: TableDefinition, 
                              new_table_def: TableDefinition) -> str:
        """マイグレーションDDLを生成
        
        Args:
            old_table_def (TableDefinition): 旧テーブル定義
            new_table_def (TableDefinition): 新テーブル定義
            
        Returns:
            str: マイグレーションDDL
        """
        ddl_lines = []
        
        # ヘッダーコメント
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append(f"-- マイグレーション: {new_table_def.table_name}")
        ddl_lines.append(f"-- 作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append("")
        
        # カラムの変更を検出
        old_columns = {col.name: col for col in old_table_def.business_columns}
        new_columns = {col.name: col for col in new_table_def.business_columns}
        
        # 新規カラム
        for col_name, col_def in new_columns.items():
            if col_name not in old_columns:
                ddl_lines.append(f"-- 新規カラム追加: {col_name}")
                ddl_lines.append(self._generate_add_column_ddl(new_table_def.table_name, col_def))
                ddl_lines.append("")
        
        # 削除カラム
        for col_name in old_columns:
            if col_name not in new_columns:
                ddl_lines.append(f"-- カラム削除: {col_name}")
                ddl_lines.append(self._generate_drop_column_ddl(new_table_def.table_name, col_name))
                ddl_lines.append("")
        
        # 変更カラム
        for col_name, new_col in new_columns.items():
            if col_name in old_columns:
                old_col = old_columns[col_name]
                if self._is_column_changed(old_col, new_col):
                    ddl_lines.append(f"-- カラム変更: {col_name}")
                    ddl_lines.append(self._generate_modify_column_ddl(new_table_def.table_name, new_col))
                    ddl_lines.append("")
        
        return "\n".join(ddl_lines)
    
    def _generate_add_column_ddl(self, table_name: str, column: ColumnDefinition) -> str:
        """カラム追加DDLを生成
        
        Args:
            table_name (str): テーブル名
            column (ColumnDefinition): カラム定義
            
        Returns:
            str: カラム追加DDL
        """
        col_def = self.sql_utils._generate_column_definition(column)
        return f"ALTER TABLE {table_name} ADD COLUMN {col_def};"
    
    def _generate_drop_column_ddl(self, table_name: str, column_name: str) -> str:
        """カラム削除DDLを生成
        
        Args:
            table_name (str): テーブル名
            column_name (str): カラム名
            
        Returns:
            str: カラム削除DDL
        """
        return f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
    
    def _generate_modify_column_ddl(self, table_name: str, column: ColumnDefinition) -> str:
        """カラム変更DDLを生成
        
        Args:
            table_name (str): テーブル名
            column (ColumnDefinition): カラム定義
            
        Returns:
            str: カラム変更DDL
        """
        col_def = self.sql_utils._generate_column_definition(column)
        return f"ALTER TABLE {table_name} MODIFY COLUMN {col_def};"
    
    def _is_column_changed(self, old_col: ColumnDefinition, new_col: ColumnDefinition) -> bool:
        """カラムが変更されたかチェック
        
        Args:
            old_col (ColumnDefinition): 旧カラム定義
            new_col (ColumnDefinition): 新カラム定義
            
        Returns:
            bool: 変更されている場合True
        """
        return (
            old_col.data_type != new_col.data_type or
            old_col.null != new_col.null or
            old_col.default != new_col.default or
            old_col.description != new_col.description
        )
    
    def generate_database_ddl(self, database_name: str, charset: str = 'utf8mb4', 
                             collation: str = 'utf8mb4_unicode_ci') -> str:
        """データベース作成DDLを生成
        
        Args:
            database_name (str): データベース名
            charset (str): 文字セット
            collation (str): 照合順序
            
        Returns:
            str: データベース作成DDL
        """
        ddl_lines = []
        
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append(f"-- データベース作成: {database_name}")
        ddl_lines.append(f"-- 作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append("")
        
        ddl_lines.append(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        ddl_lines.append(f"  DEFAULT CHARACTER SET {charset}")
        ddl_lines.append(f"  DEFAULT COLLATE {collation};")
        ddl_lines.append("")
        ddl_lines.append(f"USE {database_name};")
        ddl_lines.append("")
        
        return "\n".join(ddl_lines)
    
    def generate_user_ddl(self, username: str, password: str, database_name: str, 
                         host: str = 'localhost') -> str:
        """ユーザー作成DDLを生成
        
        Args:
            username (str): ユーザー名
            password (str): パスワード
            database_name (str): データベース名
            host (str): ホスト名
            
        Returns:
            str: ユーザー作成DDL
        """
        ddl_lines = []
        
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append(f"-- ユーザー作成: {username}")
        ddl_lines.append(f"-- 作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append("")
        
        ddl_lines.append(f"CREATE USER IF NOT EXISTS '{username}'@'{host}' IDENTIFIED BY '{password}';")
        ddl_lines.append(f"GRANT ALL PRIVILEGES ON {database_name}.* TO '{username}'@'{host}';")
        ddl_lines.append("FLUSH PRIVILEGES;")
        ddl_lines.append("")
        
        return "\n".join(ddl_lines)
    
    def generate_view_ddl(self, view_name: str, select_sql: str, 
                         description: str = "") -> str:
        """ビュー作成DDLを生成
        
        Args:
            view_name (str): ビュー名
            select_sql (str): SELECT文
            description (str): 説明
            
        Returns:
            str: ビュー作成DDL
        """
        ddl_lines = []
        
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append(f"-- ビュー: {view_name}")
        if description:
            ddl_lines.append(f"-- 説明: {description}")
        ddl_lines.append(f"-- 作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append("")
        
        ddl_lines.append(f"DROP VIEW IF EXISTS {view_name};")
        ddl_lines.append("")
        ddl_lines.append(f"CREATE VIEW {view_name} AS")
        ddl_lines.append(select_sql)
        ddl_lines.append(";")
        ddl_lines.append("")
        
        return "\n".join(ddl_lines)
    
    def generate_procedure_ddl(self, procedure_name: str, parameters: List[str], 
                              body: str, description: str = "") -> str:
        """ストアドプロシージャ作成DDLを生成
        
        Args:
            procedure_name (str): プロシージャ名
            parameters (List[str]): パラメータリスト
            body (str): プロシージャ本体
            description (str): 説明
            
        Returns:
            str: ストアドプロシージャ作成DDL
        """
        ddl_lines = []
        
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append(f"-- ストアドプロシージャ: {procedure_name}")
        if description:
            ddl_lines.append(f"-- 説明: {description}")
        ddl_lines.append(f"-- 作成日: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_lines.append(f"-- ============================================")
        ddl_lines.append("")
        
        ddl_lines.append("DELIMITER //")
        ddl_lines.append("")
        ddl_lines.append(f"DROP PROCEDURE IF EXISTS {procedure_name}//")
        ddl_lines.append("")
        
        params_str = ", ".join(parameters) if parameters else ""
        ddl_lines.append(f"CREATE PROCEDURE {procedure_name}({params_str})")
        ddl_lines.append("BEGIN")
        ddl_lines.append(body)
        ddl_lines.append("END//")
        ddl_lines.append("")
        ddl_lines.append("DELIMITER ;")
        ddl_lines.append("")
        
        return "\n".join(ddl_lines)
