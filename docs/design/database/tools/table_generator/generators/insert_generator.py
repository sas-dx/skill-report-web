#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
INSERT文生成クラス

YAMLファイルのサンプルデータからINSERT文を生成する機能を提供します。

対応要求仕様ID: PLT.2-TOOL.1
"""

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from table_generator.core.logger import EnhancedLogger
from table_generator.core.models import TableDefinition, ColumnDefinition


class InsertGenerator:
    """INSERT文生成クラス
    
    テーブル定義とサンプルデータからINSERT文を生成します。
    """
    
    def __init__(self, logger: EnhancedLogger = None):
        """初期化
        
        Args:
            logger (EnhancedLogger, optional): ログ出力インスタンス
        """
        self.logger = logger or EnhancedLogger()
    
    def generate_insert_sql(self, table_def: TableDefinition) -> str:
        """INSERT文を生成
        
        Args:
            table_def (TableDefinition): テーブル定義
            
        Returns:
            str: INSERT文
        """
        try:
            if not table_def.sample_data:
                self.logger.warning(f"サンプルデータが定義されていません: {table_def.table_name}")
                return self._generate_empty_insert_comment(table_def)
            
            lines = []
            
            # ヘッダーコメント
            lines.append(f"-- {table_def.table_name} ({table_def.logical_name}) サンプルデータ")
            lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")
            
            # カラム一覧を取得
            all_columns = self._get_all_columns(table_def)
            column_names = [col.name for col in all_columns]
            
            # INSERT文のヘッダー
            lines.append(f"INSERT INTO {table_def.table_name} (")
            
            # カラム名を4つずつ改行して整形
            column_chunks = [column_names[i:i+4] for i in range(0, len(column_names), 4)]
            for i, chunk in enumerate(column_chunks):
                indent = "    "
                if i == len(column_chunks) - 1:  # 最後のチャンク
                    lines.append(f"{indent}{', '.join(chunk)}")
                else:
                    lines.append(f"{indent}{', '.join(chunk)},")
            
            lines.append(") VALUES")
            
            # データ行を生成
            value_lines = []
            for i, sample_row in enumerate(table_def.sample_data):
                values = []
                for col in all_columns:
                    value = self._format_column_value(col, sample_row.get(col.name))
                    values.append(value)
                
                # 値を4つずつ改行して整形
                value_chunks = [values[i:i+4] for i in range(0, len(values), 4)]
                value_line_parts = []
                for chunk in value_chunks:
                    value_line_parts.append(", ".join(chunk))
                
                value_line = ",\n     ".join(value_line_parts)
                
                if i == len(table_def.sample_data) - 1:  # 最後の行
                    value_lines.append(f"    ({value_line})")
                else:
                    value_lines.append(f"    ({value_line}),")
            
            lines.extend(value_lines)
            lines.append(";")
            lines.append("")
            
            # 実行確認用のコメント
            lines.append("-- 実行確認用クエリ")
            lines.append(f"-- SELECT * FROM {table_def.table_name} ORDER BY created_at DESC;")
            lines.append("")
            
            return "\n".join(lines)
            
        except Exception as e:
            self.logger.error(f"INSERT文生成でエラー: {str(e)}")
            return self._generate_error_comment(table_def, str(e))
    
    def _get_all_columns(self, table_def: TableDefinition) -> List[ColumnDefinition]:
        """全カラム（業務カラム + 共通カラム）を取得
        
        Args:
            table_def (TableDefinition): テーブル定義
            
        Returns:
            List[ColumnDefinition]: 全カラムリスト
        """
        return table_def.business_columns
    
    def _format_column_value(self, column: ColumnDefinition, value: Any) -> str:
        """カラム値をSQL形式にフォーマット
        
        Args:
            column (ColumnDefinition): カラム定義
            value (Any): 値
            
        Returns:
            str: フォーマット済み値
        """
        if value is None:
            return "NULL"
        
        # データ型に応じてフォーマット
        data_type = column.data_type.upper()
        
        if data_type.startswith('VARCHAR') or data_type.startswith('TEXT') or data_type == 'ENUM':
            # 文字列型：シングルクォートで囲む
            escaped_value = str(value).replace("'", "''")  # シングルクォートをエスケープ
            return f"'{escaped_value}'"
        
        elif data_type in ['DATE', 'DATETIME', 'TIMESTAMP']:
            # 日付型：シングルクォートで囲む
            return f"'{value}'"
        
        elif data_type.startswith('INT') or data_type.startswith('BIGINT') or data_type.startswith('DECIMAL'):
            # 数値型：そのまま
            return str(value)
        
        elif data_type == 'BOOLEAN':
            # ブール型
            if isinstance(value, bool):
                return "TRUE" if value else "FALSE"
            elif str(value).lower() in ['true', '1', 'yes']:
                return "TRUE"
            else:
                return "FALSE"
        
        else:
            # その他：文字列として扱う
            escaped_value = str(value).replace("'", "''")
            return f"'{escaped_value}'"
    
    def _generate_empty_insert_comment(self, table_def: TableDefinition) -> str:
        """サンプルデータが無い場合のコメントを生成
        
        Args:
            table_def (TableDefinition): テーブル定義
            
        Returns:
            str: コメント
        """
        lines = [
            f"-- {table_def.table_name} ({table_def.logical_name}) サンプルデータ",
            f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "-- サンプルデータが定義されていません。",
            f"-- {table_def.table_name}_details.yaml ファイルの sample_data セクションに",
            "-- サンプルデータを追加してください。",
            "",
            "-- 例:",
            "-- sample_data:",
            "--   - column1: value1",
            "--     column2: value2",
            "",
        ]
        return "\n".join(lines)
    
    def _generate_error_comment(self, table_def: TableDefinition, error_msg: str) -> str:
        """エラー時のコメントを生成
        
        Args:
            table_def (TableDefinition): テーブル定義
            error_msg (str): エラーメッセージ
            
        Returns:
            str: エラーコメント
        """
        lines = [
            f"-- {table_def.table_name} ({table_def.logical_name}) サンプルデータ",
            f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "-- INSERT文生成でエラーが発生しました:",
            f"-- {error_msg}",
            "",
            "-- YAMLファイルの sample_data セクションを確認してください。",
            "",
        ]
        return "\n".join(lines)
    
    def generate_batch_insert_sql(self, table_defs: List[TableDefinition]) -> str:
        """複数テーブルのINSERT文を一括生成
        
        Args:
            table_defs (List[TableDefinition]): テーブル定義リスト
            
        Returns:
            str: 一括INSERT文
        """
        lines = []
        
        # ヘッダー
        lines.append("-- 複数テーブル サンプルデータ一括INSERT")
        lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("-- 実行前に外部キー制約を無効化することを推奨")
        lines.append("-- SET FOREIGN_KEY_CHECKS = 0;")
        lines.append("")
        
        # 各テーブルのINSERT文
        for table_def in table_defs:
            lines.append("-- " + "="*80)
            lines.append(self.generate_insert_sql(table_def))
            lines.append("")
        
        # フッター
        lines.append("-- 実行後に外部キー制約を有効化")
        lines.append("-- SET FOREIGN_KEY_CHECKS = 1;")
        lines.append("")
        
        return "\n".join(lines)
