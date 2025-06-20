#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル定義書生成メインクラス

このモジュールは、YAMLファイルからMarkdown形式のテーブル定義書とDDLを生成する
メイン処理を提供します。
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from shared.core.logger import DatabaseToolsLogger, get_logger
from shared.core.config import DatabaseToolsConfig
from shared.core.models import TableDefinition, GenerationResult, ProcessingResult
from table_generator.utils.yaml_loader import YamlLoader
from table_generator.utils.file_utils import FileUtils
from table_generator.utils.sql_utils import SqlUtils
from table_generator.generators.common_columns import CommonColumns
from table_generator.generators.ddl_generator import DDLGenerator
from table_generator.generators.insert_generator import InsertGenerator
from table_generator.data.faker_utils import FakerUtils


class TableDefinitionGenerator:
    """テーブル定義書生成メインクラス
    
    YAMLファイルからテーブル定義を読み込み、Markdown形式の定義書と
    DDLファイルを生成する統合処理を提供します。
    """
    
    def __init__(self, base_dir: str = None, logger: DatabaseToolsLogger = None):
        """初期化
        
        Args:
            base_dir (str, optional): ベースディレクトリパス
            logger (DatabaseToolsLogger, optional): ログ出力インスタンス
        """
        self.config = DatabaseToolsConfig(base_dir=base_dir)
        self.logger = logger or get_logger()
        self.yaml_loader = YamlLoader(logger=self.logger)
        self.file_utils = FileUtils(logger=self.logger)
        self.sql_utils = SqlUtils(logger=self.logger)
        self.ddl_generator = DDLGenerator(logger=self.logger)
        self.insert_generator = InsertGenerator(logger=self.logger)
        self.faker_utils = FakerUtils(logger=self.logger)
        
        # 必要なディレクトリを作成
        self.config.ensure_directories()
        
        self.logger.info("TableDefinitionGenerator が初期化されました")
    
    def generate_files(self, table_names: Optional[List[str]] = None, 
                      output_dir: Optional[str] = None, 
                      dry_run: bool = False) -> GenerationResult:
        """テーブル定義書とDDLファイルを生成
        
        Args:
            table_names (List[str], optional): 生成対象テーブル名リスト
            output_dir (str, optional): 出力先ディレクトリ
            dry_run (bool): ドライラン実行フラグ
            
        Returns:
            GenerationResult: 処理結果
        """
        result = GenerationResult(
            table_name="multiple_tables"
        )
        
        try:
            self.logger.header("🚀 テーブル定義書生成を開始します")
            
            # テーブル一覧を取得
            table_list = self._get_table_list(table_names)
            if not table_list:
                self.logger.error("生成対象のテーブルが見つかりません")
                result.success = False
                result.error_message = "生成対象のテーブルが見つかりません"
                return result
            
            self.logger.info(f"📋 生成対象テーブル数: {len(table_list)}")
            
            # 各テーブルの処理
            for table_name, table_info in table_list.items():
                self.logger.section(f"📝 {table_name} の処理を開始")
                
                try:
                    # テーブル定義を生成
                    table_result = self._process_table(
                        table_name, table_info, output_dir, dry_run
                    )
                    
                    if table_result.success:
                        result.processed_files.extend(table_result.processed_files)
                        result.generated_files.extend(table_result.generated_files)
                        self.logger.success(f"✅ {table_name} の処理が完了しました")
                    else:
                        result.errors.append(f"{table_name}: {table_result.error_message}")
                        self.logger.error(f"❌ {table_name} の処理でエラーが発生: {table_result.error_message}")
                        
                except Exception as e:
                    error_msg = f"{table_name} の処理中にエラーが発生: {str(e)}"
                    result.errors.append(error_msg)
                    self.logger.error(f"❌ {error_msg}")
            
            # 結果サマリー
            result.success = len(result.errors) == 0
            self._log_summary(result, dry_run)
            
        except Exception as e:
            result.success = False
            result.error_message = f"生成処理でエラーが発生: {str(e)}"
            self.logger.error(f"❌ {result.error_message}")
        
        return result
    
    def _get_table_list(self, table_names: Optional[List[str]] = None) -> Dict[str, Dict[str, Any]]:
        """テーブル一覧を取得
        
        Args:
            table_names (List[str], optional): 指定テーブル名リスト
            
        Returns:
            Dict[str, Dict[str, Any]]: テーブル一覧辞書
        """
        try:
            # テーブル一覧.mdから読み込み
            table_list_file = self.config.get_table_list_file()
            if not table_list_file.exists():
                self.logger.warning(f"テーブル一覧ファイルが見つかりません: {table_list_file}")
                return {}
            
            all_tables = self.yaml_loader.get_table_list_from_markdown(table_list_file)
            
            # 指定されたテーブルのみフィルタリング
            if table_names:
                filtered_tables = {}
                for table_name in table_names:
                    if table_name in all_tables:
                        filtered_tables[table_name] = all_tables[table_name]
                    else:
                        self.logger.warning(f"指定されたテーブルが見つかりません: {table_name}")
                return filtered_tables
            
            return all_tables
            
        except Exception as e:
            self.logger.error(f"テーブル一覧の取得でエラー: {str(e)}")
            return {}
    
    def _process_table(self, table_name: str, table_info: Dict[str, Any], 
                      output_dir: Optional[str], dry_run: bool) -> ProcessingResult:
        """個別テーブルの処理
        
        Args:
            table_name (str): テーブル名
            table_info (Dict[str, Any]): テーブル情報
            output_dir (str, optional): 出力先ディレクトリ
            dry_run (bool): ドライラン実行フラグ
            
        Returns:
            ProcessingResult: 処理結果
        """
        result = ProcessingResult(
            table_name=table_name,
            logical_name=table_info.get('logical_name', ''),
            success=True,
            has_yaml=False
        )
        
        try:
            # YAML定義ファイルを読み込み
            yaml_file = self.config.get_details_dir() / f"{table_name}_details.yaml"
            if not yaml_file.exists():
                result.success = False
                result.error_message = f"YAML定義ファイルが見つかりません: {yaml_file}"
                return result
            
            # テーブル定義を解析
            yaml_data = self.yaml_loader.load_yaml_file(yaml_file)
            if not yaml_data:
                result.success = False
                result.error_message = f"YAML定義の読み込みに失敗: {yaml_file}"
                return result
            
            table_def = self.yaml_loader.parse_table_definition(yaml_data)
            if not table_def:
                result.success = False
                result.error_message = f"テーブル定義の解析に失敗: {table_name}"
                return result
            
            # 共通カラムを追加
            self._add_common_columns(table_def)
            
            # Markdown定義書を生成
            markdown_content = self._generate_markdown_definition(table_def, table_info)
            
            # DDLを生成
            ddl_content = self.ddl_generator.generate_table_ddl(table_def)
            
            # INSERT文を生成
            insert_content = self.insert_generator.generate_insert_sql(table_def)
            
            if not dry_run:
                # ファイルを出力
                self._write_output_files(table_name, table_def, markdown_content, ddl_content, insert_content, output_dir, result)
            else:
                self.logger.info(f"🔍 [DRY RUN] {table_name} の出力をスキップしました")
                result.generated_files.append(f"[DRY RUN] {table_name}.md")
                result.generated_files.append(f"[DRY RUN] {table_name}.sql")
                result.generated_files.append(f"[DRY RUN] {table_name}_sample_data.sql")
            
            result.success = True
            
        except Exception as e:
            result.success = False
            result.error_message = str(e)
        
        return result
    
    def _add_common_columns(self, table_def: TableDefinition):
        """共通カラムを追加
        
        Args:
            table_def (TableDefinition): テーブル定義
        """
        # テーブル種別に応じて共通カラムを追加
        if table_def.table_name.startswith('MST_'):
            # マスタテーブル
            common_cols = CommonColumns.get_master_table_columns()
        elif table_def.table_name.startswith('TRN_'):
            # トランザクションテーブル
            common_cols = CommonColumns.get_all_common_columns(table_def.table_name)
        else:
            # その他
            common_cols = CommonColumns.get_base_columns()
        
        # 既存カラムと重複しないように追加
        existing_names = {col.name for col in table_def.business_columns}
        for common_col in common_cols:
            if common_col.name not in existing_names:
                table_def.business_columns.append(common_col)
    
    def _generate_markdown_definition(self, table_def: TableDefinition, 
                                    table_info: Dict[str, Any]) -> str:
        """Markdown形式のテーブル定義書を生成
        
        Args:
            table_def (TableDefinition): テーブル定義
            table_info (Dict[str, Any]): テーブル情報
            
        Returns:
            str: Markdown形式の定義書
        """
        lines = []
        
        # ヘッダー
        lines.append(f"# テーブル定義書: {table_def.table_name}")
        lines.append("")
        
        # 基本情報
        lines.append("## 基本情報")
        lines.append("")
        lines.append("| 項目 | 値 |")
        lines.append("|------|-----|")
        lines.append(f"| テーブル名 | {table_def.table_name} |")
        lines.append(f"| 論理名 | {table_def.logical_name} |")
        lines.append(f"| カテゴリ | {getattr(table_def, 'category', 'マスタ系')} |")
        lines.append(f"| 生成日時 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |")
        lines.append("")
        
        # 概要
        lines.append("## 概要")
        lines.append("")
        if hasattr(table_def, 'overview') and table_def.overview:
            lines.append(table_def.overview)
        else:
            lines.append(table_def.description)
        lines.append("")
        lines.append("")
        
        # カラム定義
        lines.append("## カラム定義")
        lines.append("")
        lines.append("| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |")
        lines.append("|----------|--------|----------|------|------|------------|------|")
        
        for col in table_def.business_columns:
            null_str = "○" if col.null else "×"
            default_str = str(col.default) if col.default is not None else ""
            length_str = str(col.length) if hasattr(col, 'length') and col.length else ""
            logical_name = getattr(col, 'logical', col.name)
            lines.append(f"| {col.name} | {logical_name} | {col.data_type} | {length_str} | {null_str} | {default_str} | {col.description} |")
        
        lines.append("")
        
        # インデックス
        if table_def.business_indexes:
            lines.append("## インデックス")
            lines.append("")
            lines.append("| インデックス名 | カラム | ユニーク | 説明 |")
            lines.append("|----------------|--------|----------|------|")
            
            for idx in table_def.business_indexes:
                unique_str = "○" if idx.unique else "×"
                columns_str = ", ".join(idx.columns)
                lines.append(f"| {idx.name} | {columns_str} | {unique_str} | {idx.description} |")
            
            lines.append("")
        
        # 外部キー
        if table_def.foreign_keys:
            lines.append("## 外部キー")
            lines.append("")
            lines.append("| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |")
            lines.append("|--------|--------|--------------|------------|--------|--------|------|")
            
            for fk in table_def.foreign_keys:
                on_update = getattr(fk, 'on_update', 'CASCADE')
                on_delete = getattr(fk, 'on_delete', 'RESTRICT')
                lines.append(f"| {fk.name} | {fk.column} | {fk.reference_table} | {fk.reference_column} | {on_update} | {on_delete} | {fk.description} |")
            
            lines.append("")
        
        # 制約
        if hasattr(table_def, 'business_constraints') and table_def.business_constraints:
            lines.append("## 制約")
            lines.append("")
            lines.append("| 制約名 | 種別 | 条件 | 説明 |")
            lines.append("|--------|------|------|------|")
            
            for constraint in table_def.business_constraints:
                constraint_type = getattr(constraint, 'type', 'CHECK')
                condition = getattr(constraint, 'condition', '')
                lines.append(f"| {constraint.name} | {constraint_type} | {condition} | {constraint.description} |")
            
            lines.append("")
        
        # サンプルデータ
        if hasattr(table_def, 'sample_data') and table_def.sample_data:
            lines.append("## サンプルデータ")
            lines.append("")
            
            # サンプルデータのヘッダーを動的に生成
            if table_def.sample_data:
                sample_keys = list(table_def.sample_data[0].keys())
                header = "| " + " | ".join(sample_keys) + " |"
                separator = "|" + "------|" * len(sample_keys)
                lines.append(header)
                lines.append(separator)
                
                for sample in table_def.sample_data:
                    row_values = [str(sample.get(key, '')) for key in sample_keys]
                    row = "| " + " | ".join(row_values) + " |"
                    lines.append(row)
                
                lines.append("")
        
        # 特記事項
        if table_def.notes:
            lines.append("## 特記事項")
            lines.append("")
            for note in table_def.notes:
                lines.append(f"- {note}")
            lines.append("")
        
        # 業務ルール
        if table_def.business_rules:
            lines.append("## 業務ルール")
            lines.append("")
            for rule in table_def.business_rules:
                lines.append(f"- {rule}")
            lines.append("")
        
        # 改版履歴
        if hasattr(table_def, 'revision_history') and table_def.revision_history:
            lines.append("## 改版履歴")
            lines.append("")
            lines.append("| バージョン | 更新日 | 更新者 | 変更内容 |")
            lines.append("|------------|--------|--------|----------|")
            
            for revision in table_def.revision_history:
                version = revision.get('version', '')
                date = revision.get('date', '')
                author = revision.get('author', '')
                changes = revision.get('changes', '')
                lines.append(f"| {version} | {date} | {author} | {changes} |")
            
            lines.append("")
        
        return "\n".join(lines)
    
    def _write_output_files(self, table_name: str, table_def: TableDefinition, 
                           markdown_content: str, ddl_content: str, insert_content: str,
                           output_dir: Optional[str], result: ProcessingResult):
        """出力ファイルを書き込み
        
        Args:
            table_name (str): テーブル名
            markdown_content (str): Markdown内容
            ddl_content (str): DDL内容
            output_dir (str, optional): 出力先ディレクトリ
            result (ProcessingResult): 処理結果
        """
        try:
            # 出力ディレクトリを決定
            if output_dir:
                tables_dir = Path(output_dir) / "tables"
                ddl_dir = Path(output_dir) / "ddl"
                data_dir = Path(output_dir) / "data"
            else:
                tables_dir = self.config.get_tables_dir()
                ddl_dir = self.config.get_ddl_dir()
                data_dir = self.config.get_base_dir() / "data"
            
            # ディレクトリを作成
            self.file_utils.ensure_directories([tables_dir, ddl_dir, data_dir])
            
            # Markdownファイルを出力（要求されている形式のファイル名）
            logical_name = getattr(table_def, 'logical_name', table_name)
            md_file = tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
            if self.file_utils.write_file(md_file, markdown_content):
                result.generated_files.append(str(md_file))
                self.logger.info(f"📄 Markdown定義書を出力: {md_file}")
            
            # DDLファイルを出力
            sql_file = ddl_dir / f"{table_name}.sql"
            if self.file_utils.write_file(sql_file, ddl_content):
                result.generated_files.append(str(sql_file))
                self.logger.info(f"🗃️ DDLファイルを出力: {sql_file}")
            
            # INSERT文ファイルを出力
            insert_file = data_dir / f"{table_name}_sample_data.sql"
            if self.file_utils.write_file(insert_file, insert_content):
                result.generated_files.append(str(insert_file))
                self.logger.info(f"📊 INSERT文ファイルを出力: {insert_file}")
                
        except Exception as e:
            raise Exception(f"ファイル出力でエラー: {str(e)}")
    
    def _log_summary(self, result: ProcessingResult, dry_run: bool):
        """処理結果サマリーをログ出力
        
        Args:
            result (ProcessingResult): 処理結果
            dry_run (bool): ドライラン実行フラグ
        """
        self.logger.header("📊 処理結果サマリー")
        
        if dry_run:
            self.logger.info("🔍 ドライラン実行")
        
        self.logger.info(f"📁 生成ファイル数: {len(result.generated_files)}")
        self.logger.info(f"⚠️ エラー数: {len(result.errors)}")
        
        if result.errors:
            self.logger.section("❌ エラー詳細")
            for error in result.errors:
                self.logger.error(f"  - {error}")
        
        if result.success:
            self.logger.success("🎉 すべての処理が正常に完了しました！")
        else:
            self.logger.error("💥 一部の処理でエラーが発生しました")
    
    def generate_sample_data(self, table_name: str, count: int = 10) -> List[Dict[str, Any]]:
        """サンプルデータを生成
        
        Args:
            table_name (str): テーブル名
            count (int): 生成件数
            
        Returns:
            List[Dict[str, Any]]: サンプルデータリスト
        """
        try:
            # YAML定義ファイルを読み込み
            yaml_file = self.config.get_details_dir() / f"{table_name}_details.yaml"
            if not yaml_file.exists():
                self.logger.error(f"YAML定義ファイルが見つかりません: {yaml_file}")
                return []
            
            yaml_data = self.yaml_loader.load_yaml_file(yaml_file)
            table_def = self.yaml_loader.parse_table_definition(yaml_data)
            
            if not table_def:
                self.logger.error(f"テーブル定義の解析に失敗: {table_name}")
                return []
            
            # サンプルデータを生成
            sample_data = []
            for i in range(count):
                row_data = {}
                for col in table_def.business_columns:
                    # カラムの型に応じてデータを生成
                    row_data[col.name] = self._generate_column_data(col, i)
                sample_data.append(row_data)
            
            return sample_data
            
        except Exception as e:
            self.logger.error(f"サンプルデータ生成でエラー: {str(e)}")
            return []
    
    def _generate_column_data(self, column, index: int):
        """カラムデータを生成
        
        Args:
            column: カラム定義
            index (int): インデックス
            
        Returns:
            Any: 生成されたデータ
        """
        # データ型に応じて生成
        if column.data_type.upper().startswith('VARCHAR'):
            return self.faker_utils.generate_by_type('text')
        elif column.data_type.upper().startswith('INT'):
            return index + 1
        elif column.data_type.upper().startswith('DATE'):
            return self.faker_utils.generate_by_type('date')
        elif column.data_type.upper().startswith('TIMESTAMP'):
            return self.faker_utils.generate_by_type('datetime')
        else:
            return f"sample_{index}"
