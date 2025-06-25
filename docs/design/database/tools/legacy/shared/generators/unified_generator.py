"""
統合ジェネレーター - DDL・定義書・サンプルデータの統一生成
全ジェネレーターを統合した包括的な生成機能

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-26
実装者: AI駆動開発チーム
"""

from typing import Optional, Dict, Any, List, Union
from pathlib import Path
from datetime import datetime
import json

from .base_generator import BaseGenerator
from ..core.models import TableDefinition, GenerationResult, ColumnDefinition
from ..core.config import Config
from ..core.logger import get_logger
from ..core.exceptions import GenerationError
from ..utils.file_utils import FileUtils

logger = get_logger(__name__)


class UnifiedGenerator(BaseGenerator):
    """統合ジェネレーター - DDL・定義書・サンプルデータの統一生成"""
    
    def __init__(self, config: Optional[Config] = None):
        """初期化"""
        super().__init__(config)
        self.file_utils = FileUtils(config)
        self.generators = {
            'ddl': self._generate_ddl,
            'markdown': self._generate_markdown,
            'sample_data': self._generate_sample_data,
            'yaml': self._generate_yaml
        }
    
    def generate(self, table_def: TableDefinition, output_path: Path) -> GenerationResult:
        """統合生成実行"""
        try:
            if not self.can_generate(table_def):
                return self._create_error_result(
                    f"生成不可: テーブル定義が無効です",
                    "TableDefinitionが無効またはtable_nameが空です"
                )
            
            self._ensure_output_directory(output_path)
            
            # 全形式の生成
            results = {}
            for format_name, generator_func in self.generators.items():
                try:
                    result = generator_func(table_def, output_path)
                    results[format_name] = result
                    self.logger.info(f"{format_name}生成完了: {table_def.table_name}")
                except Exception as e:
                    self.logger.error(f"{format_name}生成エラー: {e}")
                    results[format_name] = str(e)
            
            return self._create_success_result(
                f"統合生成完了: {table_def.table_name}",
                output_path
            )
            
        except Exception as e:
            raise self._handle_generation_error(e, table_def.table_name)
    
    def generate_single_format(self, table_def: TableDefinition, output_path: Path, format_type: str) -> GenerationResult:
        """単一形式の生成"""
        try:
            if format_type not in self.generators:
                return self._create_error_result(
                    f"サポートされていない形式: {format_type}",
                    f"利用可能な形式: {list(self.generators.keys())}"
                )
            
            self._ensure_output_directory(output_path)
            
            generator_func = self.generators[format_type]
            result = generator_func(table_def, output_path)
            
            return self._create_success_result(
                f"{format_type}生成完了: {table_def.table_name}",
                output_path
            )
            
        except Exception as e:
            raise self._handle_generation_error(e, table_def.table_name)
    
    def get_output_extension(self) -> str:
        """出力ファイル拡張子を取得（統合生成では使用しない）"""
        return ""
    
    def _generate_ddl(self, table_def: TableDefinition, output_path: Path) -> str:
        """DDL生成"""
        ddl_lines = []
        
        # CREATE TABLE文の開始
        ddl_lines.append(f"-- テーブル: {table_def.table_name}")
        ddl_lines.append(f"-- 論理名: {table_def.logical_name}")
        ddl_lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        ddl_lines.append("")
        ddl_lines.append(f"CREATE TABLE {table_def.table_name} (")
        
        # カラム定義
        column_lines = []
        for column in table_def.columns:
            line = f"    {column.name} {column.data_type}"
            
            if not column.nullable:
                line += " NOT NULL"
            
            if column.default:
                line += f" DEFAULT {column.default}"
            
            if column.primary_key:
                line += " PRIMARY KEY"
            
            if column.unique:
                line += " UNIQUE"
            
            if column.comment:
                line += f" -- {column.comment}"
            
            column_lines.append(line)
        
        ddl_lines.append(",\n".join(column_lines))
        ddl_lines.append(");")
        
        # インデックス定義
        if table_def.indexes:
            ddl_lines.append("")
            ddl_lines.append("-- インデックス定義")
            for index in table_def.indexes:
                unique_keyword = "UNIQUE " if index.unique else ""
                columns_str = ", ".join(index.columns)
                ddl_lines.append(f"CREATE {unique_keyword}INDEX {index.name} ON {table_def.table_name} ({columns_str});")
        
        # 外部キー定義
        if table_def.foreign_keys:
            ddl_lines.append("")
            ddl_lines.append("-- 外部キー定義")
            for fk in table_def.foreign_keys:
                columns_str = ", ".join(fk.columns)
                ref_columns_str = ", ".join(fk.reference_columns)
                ddl_lines.append(f"ALTER TABLE {table_def.table_name}")
                ddl_lines.append(f"    ADD CONSTRAINT {fk.name}")
                ddl_lines.append(f"    FOREIGN KEY ({columns_str})")
                ddl_lines.append(f"    REFERENCES {fk.reference_table} ({ref_columns_str})")
                ddl_lines.append(f"    ON UPDATE {fk.on_update} ON DELETE {fk.on_delete};")
        
        ddl_content = "\n".join(ddl_lines)
        
        # ファイル出力
        ddl_file = output_path / f"{table_def.table_name}.sql"
        with open(ddl_file, 'w', encoding=self.config.tool.encoding) as f:
            f.write(ddl_content)
        
        return str(ddl_file)
    
    def _generate_markdown(self, table_def: TableDefinition, output_path: Path) -> str:
        """Markdown定義書生成"""
        md_lines = []
        
        # ヘッダー
        md_lines.append(f"# テーブル定義書: {table_def.table_name}")
        md_lines.append("")
        md_lines.append("## 基本情報")
        md_lines.append("")
        md_lines.append(f"- **物理名**: {table_def.table_name}")
        md_lines.append(f"- **論理名**: {table_def.logical_name}")
        md_lines.append(f"- **カテゴリ**: {table_def.category}")
        md_lines.append(f"- **優先度**: {table_def.priority}")
        md_lines.append(f"- **要求仕様ID**: {table_def.requirement_id}")
        md_lines.append(f"- **生成日時**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_lines.append("")
        
        # 概要
        if table_def.overview:
            md_lines.append("## 概要")
            md_lines.append("")
            md_lines.append(table_def.overview)
            md_lines.append("")
        
        # カラム定義
        md_lines.append("## カラム定義")
        md_lines.append("")
        md_lines.append("| カラム名 | データ型 | NULL許可 | 主キー | 一意制約 | デフォルト値 | コメント |")
        md_lines.append("|----------|----------|----------|--------|----------|--------------|----------|")
        
        for column in table_def.columns:
            nullable = "○" if column.nullable else "×"
            primary_key = "○" if column.primary_key else ""
            unique = "○" if column.unique else ""
            default = column.default or ""
            comment = column.comment or ""
            
            md_lines.append(f"| {column.name} | {column.data_type} | {nullable} | {primary_key} | {unique} | {default} | {comment} |")
        
        md_lines.append("")
        
        # インデックス定義
        if table_def.indexes:
            md_lines.append("## インデックス定義")
            md_lines.append("")
            md_lines.append("| インデックス名 | カラム | 一意制約 | コメント |")
            md_lines.append("|----------------|--------|----------|----------|")
            
            for index in table_def.indexes:
                columns_str = ", ".join(index.columns)
                unique = "○" if index.unique else ""
                comment = index.comment or ""
                
                md_lines.append(f"| {index.name} | {columns_str} | {unique} | {comment} |")
            
            md_lines.append("")
        
        # 外部キー定義
        if table_def.foreign_keys:
            md_lines.append("## 外部キー定義")
            md_lines.append("")
            md_lines.append("| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | コメント |")
            md_lines.append("|--------|--------|--------------|------------|--------|--------|----------|")
            
            for fk in table_def.foreign_keys:
                columns_str = ", ".join(fk.columns)
                ref_columns_str = ", ".join(fk.reference_columns)
                comment = fk.comment or ""
                
                md_lines.append(f"| {fk.name} | {columns_str} | {fk.reference_table} | {ref_columns_str} | {fk.on_update} | {fk.on_delete} | {comment} |")
            
            md_lines.append("")
        
        # 特記事項
        if table_def.notes:
            md_lines.append("## 特記事項")
            md_lines.append("")
            for note in table_def.notes:
                md_lines.append(f"- {note}")
            md_lines.append("")
        
        # 業務ルール
        if table_def.rules:
            md_lines.append("## 業務ルール")
            md_lines.append("")
            for rule in table_def.rules:
                md_lines.append(f"- {rule}")
            md_lines.append("")
        
        md_content = "\n".join(md_lines)
        
        # ファイル出力
        md_file = output_path / f"テーブル定義書_{table_def.table_name}_{table_def.logical_name}.md"
        with open(md_file, 'w', encoding=self.config.tool.encoding) as f:
            f.write(md_content)
        
        return str(md_file)
    
    def _generate_sample_data(self, table_def: TableDefinition, output_path: Path) -> str:
        """サンプルデータ生成"""
        insert_lines = []
        
        # ヘッダー
        insert_lines.append(f"-- サンプルデータ: {table_def.table_name}")
        insert_lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        insert_lines.append("")
        
        # カラム名リスト
        column_names = [col.name for col in table_def.columns]
        columns_str = ", ".join(column_names)
        
        # サンプルデータ生成
        sample_values = []
        for i in range(3):  # 3件のサンプルデータ
            values = []
            for column in table_def.columns:
                value = self._generate_sample_value(column, i + 1)
                values.append(value)
            sample_values.append(f"({', '.join(values)})")
        
        # INSERT文生成
        insert_lines.append(f"INSERT INTO {table_def.table_name} ({columns_str}) VALUES")
        insert_lines.append(",\n".join(sample_values) + ";")
        
        insert_content = "\n".join(insert_lines)
        
        # ファイル出力
        insert_file = output_path / f"{table_def.table_name}_sample_data.sql"
        with open(insert_file, 'w', encoding=self.config.tool.encoding) as f:
            f.write(insert_content)
        
        return str(insert_file)
    
    def _generate_yaml(self, table_def: TableDefinition, output_path: Path) -> str:
        """YAML定義生成"""
        yaml_data = {
            'table_name': table_def.table_name,
            'logical_name': table_def.logical_name,
            'category': table_def.category,
            'priority': table_def.priority,
            'requirement_id': table_def.requirement_id,
            'comment': table_def.comment,
            'revision_history': table_def.revision_history or [
                {
                    'version': '1.0.0',
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'author': 'AI駆動開発チーム',
                    'changes': '自動生成による初版作成'
                }
            ],
            'overview': table_def.overview or f'{table_def.logical_name}の管理を行うテーブルです。',
            'columns': [],
            'indexes': [],
            'foreign_keys': [],
            'notes': table_def.notes or [
                '運用・保守に関する重要な注意事項',
                'セキュリティ・暗号化に関する考慮事項',
                'パフォーマンス・最適化に関する考慮事項'
            ],
            'rules': table_def.rules or [
                'データの一意性・整合性に関するルール',
                '業務制約・ビジネスロジックに関するルール',
                '運用ルール・メンテナンス要件に関するルール'
            ]
        }
        
        # カラム定義
        for column in table_def.columns:
            col_data = {
                'name': column.name,
                'type': column.data_type,
                'nullable': column.nullable,
                'comment': column.comment
            }
            if column.primary_key:
                col_data['primary_key'] = True
            if column.unique:
                col_data['unique'] = True
            if column.default:
                col_data['default'] = column.default
            if column.requirement_id:
                col_data['requirement_id'] = column.requirement_id
            
            yaml_data['columns'].append(col_data)
        
        # インデックス定義
        for index in table_def.indexes:
            idx_data = {
                'name': index.name,
                'columns': index.columns,
                'unique': index.unique,
                'comment': index.comment
            }
            yaml_data['indexes'].append(idx_data)
        
        # 外部キー定義
        for fk in table_def.foreign_keys:
            fk_data = {
                'name': fk.name,
                'columns': fk.columns,
                'references': {
                    'table': fk.reference_table,
                    'columns': fk.reference_columns
                },
                'on_update': fk.on_update,
                'on_delete': fk.on_delete,
                'comment': fk.comment
            }
            yaml_data['foreign_keys'].append(fk_data)
        
        # YAML文字列生成
        import yaml
        yaml_content = yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
        
        # ファイル出力
        yaml_file = output_path / f"テーブル詳細定義YAML_{table_def.table_name}.yaml"
        with open(yaml_file, 'w', encoding=self.config.tool.encoding) as f:
            f.write(yaml_content)
        
        return str(yaml_file)
    
    def _generate_sample_value(self, column: ColumnDefinition, index: int) -> str:
        """サンプル値生成"""
        data_type = column.data_type.upper()
        
        if 'INT' in data_type or 'SERIAL' in data_type:
            return str(index)
        elif 'VARCHAR' in data_type or 'TEXT' in data_type:
            if 'ID' in column.name.upper():
                return f"'{column.name}_{index:03d}'"
            elif 'NAME' in column.name.upper():
                return f"'サンプル名_{index}'"
            elif 'EMAIL' in column.name.upper():
                return f"'sample{index}@example.com'"
            else:
                return f"'サンプル値_{index}'"
        elif 'TIMESTAMP' in data_type or 'DATETIME' in data_type:
            return 'CURRENT_TIMESTAMP'
        elif 'DATE' in data_type:
            return 'CURRENT_DATE'
        elif 'BOOLEAN' in data_type or 'BOOL' in data_type:
            return 'true' if index % 2 == 1 else 'false'
        else:
            return f"'値_{index}'"
    
    def get_supported_formats(self) -> List[str]:
        """サポートする生成形式を取得"""
        return list(self.generators.keys())
