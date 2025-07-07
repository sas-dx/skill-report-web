"""
テーブル生成モジュール
要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1

YAMLファイルからテーブル関連ファイルを生成します：
1. DDLファイル生成
2. Markdownテーブル定義書生成
3. サンプルデータ生成
"""

import os
import yaml
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from core.config import Config
from core.logger import setup_logger
from core.exceptions import DatabaseToolsError


class TableGenerator:
    """テーブル生成クラス"""
    
    def __init__(self, config: Config):
        """初期化"""
        self.config = config
        self.logger = setup_logger(__name__, config.log_level)
        
        # ディレクトリパス
        self.yaml_dir = Path(config.table_details_dir)
        self.ddl_dir = Path(config.ddl_dir)
        self.tables_dir = Path(config.tables_dir)
        self.data_dir = Path(config.data_dir)
        
        # ディレクトリ作成
        self._ensure_directories()
    
    def generate(self, table_name: str, verbose: bool = False) -> bool:
        """指定テーブルの生成"""
        self.logger.info(f"テーブル {table_name} の生成を開始します")
        
        try:
            # YAMLファイル読み込み
            yaml_data = self._load_yaml(table_name)
            if not yaml_data:
                return False
            
            # 各ファイル生成
            success = True
            
            # DDL生成
            if not self._generate_ddl(table_name, yaml_data, verbose):
                success = False
            
            # Markdown定義書生成
            if not self._generate_markdown(table_name, yaml_data, verbose):
                success = False
            
            # サンプルデータ生成
            if not self._generate_sample_data(table_name, yaml_data, verbose):
                success = False
            
            if success:
                self.logger.info(f"テーブル {table_name} の生成が完了しました")
            else:
                self.logger.error(f"テーブル {table_name} の生成でエラーが発生しました")
            
            return success
            
        except Exception as e:
            self.logger.error(f"テーブル生成中にエラーが発生しました: {e}")
            return False
    
    def generate_all(self, verbose: bool = False) -> bool:
        """全テーブルの生成"""
        self.logger.info("全テーブルの生成を開始します")
        
        yaml_files = list(self.yaml_dir.glob("*.yaml"))
        if not yaml_files:
            self.logger.warning(f"YAMLファイルが見つかりません: {self.yaml_dir}")
            return True
        
        success_count = 0
        total_count = len(yaml_files)
        
        for yaml_file in yaml_files:
            # ファイル名からテーブル名を抽出
            table_name = self._extract_table_name(yaml_file.name)
            if not table_name:
                continue
            
            if self.generate(table_name, verbose):
                success_count += 1
        
        self.logger.info(f"テーブル生成完了: {success_count}/{total_count}")
        return success_count == total_count
    
    def _load_yaml(self, table_name: str) -> Optional[Dict[str, Any]]:
        """YAMLファイル読み込み"""
        yaml_file = self.yaml_dir / f"テーブル詳細定義YAML_{table_name}.yaml"
        
        if not yaml_file.exists():
            self.logger.error(f"YAMLファイルが存在しません: {yaml_file}")
            return None
        
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"YAMLファイル読み込みエラー: {e}")
            return None
    
    def _generate_ddl(self, table_name: str, yaml_data: Dict[str, Any], verbose: bool) -> bool:
        """DDLファイル生成"""
        try:
            ddl_content = self._create_ddl_content(table_name, yaml_data)
            ddl_file = self.ddl_dir / f"{table_name}.sql"
            
            with open(ddl_file, 'w', encoding='utf-8') as f:
                f.write(ddl_content)
            
            if verbose:
                print(f"✅ DDL生成完了: {ddl_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"DDL生成エラー: {e}")
            return False
    
    def _generate_markdown(self, table_name: str, yaml_data: Dict[str, Any], verbose: bool) -> bool:
        """Markdown定義書生成"""
        try:
            markdown_content = self._create_markdown_content(table_name, yaml_data)
            logical_name = yaml_data.get('logical_name', table_name)
            markdown_file = self.tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
            
            with open(markdown_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            if verbose:
                print(f"✅ Markdown生成完了: {markdown_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Markdown生成エラー: {e}")
            return False
    
    def _generate_sample_data(self, table_name: str, yaml_data: Dict[str, Any], verbose: bool) -> bool:
        """サンプルデータ生成"""
        try:
            # サンプルデータがYAMLに定義されている場合のみ生成
            sample_data = yaml_data.get('sample_data')
            if not sample_data:
                if verbose:
                    print(f"⚠️  サンプルデータ未定義: {table_name}")
                return True
            
            insert_content = self._create_insert_content(table_name, yaml_data)
            insert_file = self.data_dir / f"{table_name}_sample.sql"
            
            with open(insert_file, 'w', encoding='utf-8') as f:
                f.write(insert_content)
            
            if verbose:
                print(f"✅ サンプルデータ生成完了: {insert_file}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"サンプルデータ生成エラー: {e}")
            return False
    
    def _create_ddl_content(self, table_name: str, yaml_data: Dict[str, Any]) -> str:
        """DDL内容作成"""
        lines = []
        
        # ヘッダーコメント
        lines.append(f"-- テーブル: {table_name}")
        lines.append(f"-- 論理名: {yaml_data.get('logical_name', '')}")
        lines.append(f"-- 要求仕様ID: {yaml_data.get('requirement_id', '')}")
        lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # CREATE TABLE文
        lines.append(f"CREATE TABLE {table_name} (")
        
        # カラム定義
        columns = yaml_data.get('columns', [])
        column_lines = []
        
        for column in columns:
            col_name = column.get('name', '')
            col_type = column.get('type', '')
            nullable = column.get('nullable', True)
            default = column.get('default')
            comment = column.get('comment', '')
            
            col_line = f"    {col_name} {col_type}"
            
            if not nullable:
                col_line += " NOT NULL"
            
            if default:
                col_line += f" DEFAULT {default}"
            
            column_lines.append(col_line)
        
        # 主キー定義
        primary_keys = [col['name'] for col in columns if col.get('primary_key')]
        if primary_keys:
            pk_line = f"    PRIMARY KEY ({', '.join(primary_keys)})"
            column_lines.append(pk_line)
        
        lines.append(',\n'.join(column_lines))
        lines.append(");")
        lines.append("")
        
        # インデックス定義
        indexes = yaml_data.get('indexes', [])
        for index in indexes:
            index_name = index.get('name', '')
            index_columns = index.get('columns', [])
            unique = index.get('unique', False)
            
            index_type = "UNIQUE INDEX" if unique else "INDEX"
            lines.append(f"CREATE {index_type} {index_name} ON {table_name} ({', '.join(index_columns)});")
        
        if indexes:
            lines.append("")
        
        # 外部キー定義
        foreign_keys = yaml_data.get('foreign_keys', [])
        for fk in foreign_keys:
            fk_name = fk.get('name', '')
            fk_columns = fk.get('columns', [])
            ref_table = fk.get('references', {}).get('table', '')
            ref_columns = fk.get('references', {}).get('columns', [])
            on_update = fk.get('on_update', 'RESTRICT')
            on_delete = fk.get('on_delete', 'RESTRICT')
            
            lines.append(f"ALTER TABLE {table_name}")
            lines.append(f"    ADD CONSTRAINT {fk_name}")
            lines.append(f"    FOREIGN KEY ({', '.join(fk_columns)})")
            lines.append(f"    REFERENCES {ref_table} ({', '.join(ref_columns)})")
            lines.append(f"    ON UPDATE {on_update} ON DELETE {on_delete};")
            lines.append("")
        
        # カラムコメント
        for column in columns:
            col_name = column.get('name', '')
            comment = column.get('comment', '')
            if comment:
                lines.append(f"COMMENT ON COLUMN {table_name}.{col_name} IS '{comment}';")
        
        # テーブルコメント
        table_comment = yaml_data.get('comment', '')
        if table_comment:
            lines.append(f"COMMENT ON TABLE {table_name} IS '{table_comment}';")
        
        return '\n'.join(lines)
    
    def _create_markdown_content(self, table_name: str, yaml_data: Dict[str, Any]) -> str:
        """Markdown内容作成"""
        lines = []
        
        logical_name = yaml_data.get('logical_name', table_name)
        
        # ヘッダー
        lines.append(f"# テーブル定義書: {table_name} ({logical_name})")
        lines.append("")
        
        # 基本情報
        lines.append("## 基本情報")
        lines.append("")
        lines.append("| 項目 | 値 |")
        lines.append("|------|-----|")
        lines.append(f"| テーブル名 | {table_name} |")
        lines.append(f"| 論理名 | {logical_name} |")
        lines.append(f"| カテゴリ | {yaml_data.get('category', '')} |")
        lines.append(f"| 優先度 | {yaml_data.get('priority', '')} |")
        lines.append(f"| 要求仕様ID | {yaml_data.get('requirement_id', '')} |")
        lines.append(f"| 生成日時 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |")
        lines.append("")
        
        # 概要
        overview = yaml_data.get('overview', '')
        if overview:
            lines.append("## 概要")
            lines.append("")
            lines.append(overview)
            lines.append("")
        
        # カラム定義
        columns = yaml_data.get('columns', [])
        if columns:
            lines.append("## カラム定義")
            lines.append("")
            lines.append("| カラム名 | データ型 | NULL許可 | 主キー | 一意制約 | デフォルト値 | 説明 |")
            lines.append("|----------|----------|----------|--------|----------|--------------|------|")
            
            for column in columns:
                name = column.get('name', '')
                data_type = column.get('type', '')
                nullable = "○" if column.get('nullable', True) else "×"
                primary_key = "○" if column.get('primary_key', False) else ""
                unique = "○" if column.get('unique', False) else ""
                default = column.get('default', '')
                comment = column.get('comment', '')
                
                lines.append(f"| {name} | {data_type} | {nullable} | {primary_key} | {unique} | {default} | {comment} |")
            
            lines.append("")
        
        # インデックス定義
        indexes = yaml_data.get('indexes', [])
        if indexes:
            lines.append("## インデックス定義")
            lines.append("")
            lines.append("| インデックス名 | カラム | 一意制約 | 説明 |")
            lines.append("|----------------|--------|----------|------|")
            
            for index in indexes:
                name = index.get('name', '')
                columns_str = ', '.join(index.get('columns', []))
                unique = "○" if index.get('unique', False) else ""
                comment = index.get('comment', '')
                
                lines.append(f"| {name} | {columns_str} | {unique} | {comment} |")
            
            lines.append("")
        
        # 外部キー定義
        foreign_keys = yaml_data.get('foreign_keys', [])
        if foreign_keys:
            lines.append("## 外部キー定義")
            lines.append("")
            lines.append("| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |")
            lines.append("|--------|--------|--------------|------------|--------|--------|------|")
            
            for fk in foreign_keys:
                name = fk.get('name', '')
                columns_str = ', '.join(fk.get('columns', []))
                ref_table = fk.get('references', {}).get('table', '')
                ref_columns_str = ', '.join(fk.get('references', {}).get('columns', []))
                on_update = fk.get('on_update', 'RESTRICT')
                on_delete = fk.get('on_delete', 'RESTRICT')
                comment = fk.get('comment', '')
                
                lines.append(f"| {name} | {columns_str} | {ref_table} | {ref_columns_str} | {on_update} | {on_delete} | {comment} |")
            
            lines.append("")
        
        # 特記事項
        notes = yaml_data.get('notes', [])
        if notes:
            lines.append("## 特記事項")
            lines.append("")
            for note in notes:
                lines.append(f"- {note}")
            lines.append("")
        
        # 業務ルール
        rules = yaml_data.get('rules', [])
        if rules:
            lines.append("## 業務ルール")
            lines.append("")
            for rule in rules:
                lines.append(f"- {rule}")
            lines.append("")
        
        # 改版履歴
        revision_history = yaml_data.get('revision_history', [])
        if revision_history:
            lines.append("## 改版履歴")
            lines.append("")
            lines.append("| バージョン | 日付 | 作成者 | 変更内容 |")
            lines.append("|------------|------|--------|----------|")
            
            for revision in revision_history:
                version = revision.get('version', '')
                date = revision.get('date', '')
                author = revision.get('author', '')
                changes = revision.get('changes', '')
                
                lines.append(f"| {version} | {date} | {author} | {changes} |")
            
            lines.append("")
        
        return '\n'.join(lines)
    
    def _create_insert_content(self, table_name: str, yaml_data: Dict[str, Any]) -> str:
        """INSERT文内容作成"""
        lines = []
        
        # ヘッダーコメント
        lines.append(f"-- サンプルデータ: {table_name}")
        lines.append(f"-- 生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        
        # サンプルデータ
        sample_data = yaml_data.get('sample_data', [])
        if not sample_data:
            lines.append(f"-- サンプルデータが定義されていません")
            return '\n'.join(lines)
        
        # カラム名取得
        columns = yaml_data.get('columns', [])
        column_names = [col['name'] for col in columns]
        
        if not isinstance(sample_data, list):
            sample_data = [sample_data]
        
        for data in sample_data:
            values = []
            for col_name in column_names:
                value = data.get(col_name, 'NULL')
                if value == 'NULL':
                    values.append('NULL')
                elif isinstance(value, str):
                    values.append(f"'{value}'")
                else:
                    values.append(str(value))
            
            insert_sql = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES ({', '.join(values)});"
            lines.append(insert_sql)
        
        return '\n'.join(lines)
    
    def _extract_table_name(self, filename: str) -> Optional[str]:
        """ファイル名からテーブル名を抽出"""
        # テーブル詳細定義YAML_{table_name}.yaml の形式
        if filename.startswith("テーブル詳細定義YAML_") and filename.endswith(".yaml"):
            return filename[len("テーブル詳細定義YAML_"):-len(".yaml")]
        return None
    
    def _ensure_directories(self):
        """必要なディレクトリを作成"""
        for directory in [self.ddl_dir, self.tables_dir, self.data_dir]:
            directory.mkdir(parents=True, exist_ok=True)
