"""
Markdownジェネレーター

TableDefinitionからMarkdownテーブル定義書を生成する
"""

from typing import Dict, List, Any, Optional
import logging
from datetime import datetime

from ..core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition

logger = logging.getLogger(__name__)


class MarkdownGenerator:
    """Markdownジェネレーター"""
    
    def __init__(self):
        """初期化"""
        pass
    
    def generate(self, table_definition: TableDefinition) -> str:
        """
        TableDefinitionからMarkdownを生成
        
        Args:
            table_definition: テーブル定義
            
        Returns:
            str: Markdown内容
        """
        try:
            lines = []
            
            # ヘッダー
            lines.append(f"# テーブル定義書_{table_definition.table_name}_{table_definition.logical_name}")
            lines.append("")
            
            # テーブル情報
            lines.append("## テーブル情報")
            lines.append("")
            lines.append("| 項目 | 内容 |")
            lines.append("|------|------|")
            lines.append(f"| テーブル名 | {table_definition.table_name} |")
            lines.append(f"| 論理名 | {table_definition.logical_name} |")
            lines.append(f"| カテゴリ | {table_definition.category} |")
            lines.append(f"| 優先度 | {table_definition.priority} |")
            lines.append(f"| 要求仕様ID | {table_definition.requirement_id} |")
            lines.append("")
            
            # カラム定義
            lines.append("## カラム定義")
            lines.append("")
            lines.append("| カラム名 | データ型 | NULL許可 | 主キー | デフォルト値 | 説明 | 要求仕様ID |")
            lines.append("|----------|----------|----------|--------|--------------|------|-------------|")
            
            for column in table_definition.columns:
                null_allowed = "YES" if column.nullable else "NO"
                primary_key = "YES" if column.primary_key else "NO"
                default_value = column.default_value if column.default_value else "-"
                
                lines.append(f"| {column.name} | {column.data_type} | {null_allowed} | {primary_key} | {default_value} | {column.comment} | {column.requirement_id} |")
            
            lines.append("")
            
            # インデックス定義
            if table_definition.indexes:
                lines.append("## インデックス定義")
                lines.append("")
                lines.append("| インデックス名 | 対象カラム | ユニーク | 説明 |")
                lines.append("|----------------|------------|----------|------|")
                
                for index in table_definition.indexes:
                    unique = "YES" if index.unique else "NO"
                    columns_str = ", ".join(index.columns)
                    lines.append(f"| {index.name} | {columns_str} | {unique} | {index.comment} |")
                
                lines.append("")
            
            # 外部キー定義
            if table_definition.foreign_keys:
                lines.append("## 外部キー定義")
                lines.append("")
                lines.append("| 外部キー名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 |")
                lines.append("|------------|--------|--------------|------------|--------|--------|")
                
                for fk in table_definition.foreign_keys:
                    columns_str = ", ".join(fk.columns)
                    ref_columns_str = ", ".join(fk.references_columns)
                    lines.append(f"| {fk.name} | {columns_str} | {fk.references_table} | {ref_columns_str} | {fk.on_update} | {fk.on_delete} |")
                
                lines.append("")
            
            # フッター
            lines.append("---")
            lines.append(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            lines.append("")
            
            return "\n".join(lines)
            
        except Exception as e:
            logger.error(f"Markdown生成エラー: {e}")
            raise
