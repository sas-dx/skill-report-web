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
from shared.core.models import TableDefinition, GenerationResult, ProcessingResult, BusinessColumnDefinition
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
        # base_dirをPathオブジェクトに変換
        base_path = Path(base_dir) if base_dir else None
        self.config = DatabaseToolsConfig(base_dir=base_path)
        self.logger = logger or get_logger()
        self.yaml_loader = YamlLoader(logger=self.logger)
        self.file_utils = FileUtils(logger=self.logger)
        self.sql_utils = SqlUtils(logger=self.logger)
        self.ddl_generator = DDLGenerator(logger=self.logger)
        self.insert_generator = InsertGenerator(logger=self.logger)
        self.faker_utils = FakerUtils(logger=self.logger)
        
        # 必要なディレクトリを作成
        self.config._ensure_directories()
        
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
            self.logger.info("🚀 テーブル定義書生成を開始します")
            
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
                self.logger.info(f"📝 {table_name} の処理を開始")
                
                try:
                    # テーブル定義を生成
                    table_result = self._process_table(
                        table_name, table_info, output_dir, dry_run
                    )
                    
                    if table_result.success:
                        result.processed_files.extend(table_result.processed_files)
                        result.generated_files.extend(table_result.generated_files)
                        self.logger.info(f"✅ {table_name} の処理が完了しました")
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
            # 指定されたテーブルがある場合は、直接YAMLファイルから情報を取得
            if table_names:
                filtered_tables = {}
                for table_name in table_names:
                    yaml_file = self.config.get_details_dir() / f"{table_name}_details.yaml"
                    if yaml_file.exists():
                        yaml_data = self.yaml_loader.load_yaml_file(yaml_file)
                        if yaml_data:
                            filtered_tables[table_name] = {
                                'table_name': yaml_data.get('table_name', table_name),
                                'logical_name': yaml_data.get('logical_name', ''),
                                'category': yaml_data.get('category', ''),
                                'priority': yaml_data.get('priority', 'medium')
                            }
                        else:
                            self.logger.warning(f"YAMLファイルの読み込みに失敗: {yaml_file}")
                    else:
                        self.logger.warning(f"指定されたテーブルのYAMLファイルが見つかりません: {yaml_file}")
                return filtered_tables
            
            # 全テーブルの場合は、table-detailsディレクトリから取得
            all_tables = {}
            details_dir = self.config.get_details_dir()
            if details_dir.exists():
                for yaml_file in details_dir.glob("*_details.yaml"):
                    table_name = yaml_file.stem.replace("_details", "")
                    yaml_data = self.yaml_loader.load_yaml_file(yaml_file)
                    if yaml_data:
                        all_tables[table_name] = {
                            'table_name': yaml_data.get('table_name', table_name),
                            'logical_name': yaml_data.get('logical_name', ''),
                            'category': yaml_data.get('category', ''),
                            'priority': yaml_data.get('priority', 'medium')
                        }
            
            # フォールバック: テーブル一覧.mdから読み込み
            if not all_tables:
                table_list_file = self.config.get_table_list_file()
                if table_list_file.exists():
                    all_tables = self.yaml_loader.get_table_list_from_markdown(table_list_file)
                else:
                    self.logger.warning(f"テーブル一覧ファイルが見つかりません: {table_list_file}")
            
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
        if table_def.name.startswith('MST_'):
            # マスタテーブル
            common_cols = CommonColumns.get_master_table_columns()
        elif table_def.name.startswith('TRN_'):
            # トランザクションテーブル
            common_cols = CommonColumns.get_all_common_columns(table_def.name)
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
        """Markdown形式のテーブル定義書を生成（MST_Department形式）
        
        Args:
            table_def (TableDefinition): テーブル定義
            table_info (Dict[str, Any]): テーブル情報
            
        Returns:
            str: Markdown形式の定義書（MST_Department形式）
        """
        lines = []
        
        # ヘッダー
        logical_name = getattr(table_def, 'logical_name', table_def.name)
        lines.append(f"# テーブル定義書: {table_def.name}")
        lines.append("")
        
        # 基本情報テーブル
        lines.append("## 基本情報")
        lines.append("")
        lines.append("| 項目 | 値 |")
        lines.append("|------|-----|")
        lines.append(f"| テーブル名 | {table_def.name} |")
        lines.append(f"| 論理名 | {logical_name} |")
        
        category = getattr(table_def, 'category', 'マスタ系')
        lines.append(f"| カテゴリ | {category} |")
        lines.append(f"| 生成日時 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |")
        lines.append("")
        
        # 概要セクション
        lines.append("## 概要")
        lines.append("")
        
        # 概要文を生成（YAMLのoverviewフィールドをそのまま使用）
        if hasattr(table_def, 'overview') and table_def.overview:
            # YAMLのoverviewフィールドをそのまま出力
            overview_lines = table_def.overview.strip().split('\n')
            for line in overview_lines:
                if line.strip():  # 空行でない場合のみ追加
                    lines.append(line.strip())
            lines.append("")
        else:
            # overviewがない場合のフォールバック
            lines.append(f"{table_def.name}（{logical_name}）は、{table_def.comment}")
            lines.append("")
            lines.append("主な目的：")
            lines.append(f"- {logical_name}の基本情報管理")
            lines.append(f"- データの整合性・一意性保証")
            lines.append(f"- 関連システムとの連携データ提供")
            lines.append("")
            lines.append(f"このテーブルは、年間スキル報告書システムの{category}データとして、")
            lines.append("組織運営の様々な業務プロセスの基盤となる重要なマスタデータです。")
            lines.append("")
        
        lines.append("")
        
        # カラム定義テーブル
        lines.append("## カラム定義")
        lines.append("")
        lines.append("| カラム名 | 論理名 | データ型 | 長さ | NULL | デフォルト | 説明 |")
        lines.append("|----------|--------|----------|------|------|------------|------|")
        
        for col in table_def.business_columns:
            # データ型と長さを分離
            data_type = col.data_type
            length = ""
            if "(" in data_type and ")" in data_type:
                type_part = data_type.split("(")[0]
                length_part = data_type.split("(")[1].split(")")[0]
                data_type = type_part
                length = length_part
            
            # NULL許可
            null_allowed = "○" if col.nullable else "×"
            
            # デフォルト値
            default_value = ""
            if col.default is not None:
                default_value = str(col.default)
            
            # 論理名（コメントから抽出）
            logical_col_name = getattr(col, 'comment', col.name)
            if '（' in logical_col_name:
                logical_col_name = logical_col_name.split('（')[0]
            
            lines.append(f"| {col.name} | {logical_col_name} | {data_type} | {length} | {null_allowed} | {default_value} | {getattr(col, 'comment', '')} |")
        
        lines.append("")
        
        # インデックステーブル
        if table_def.business_indexes:
            lines.append("## インデックス")
            lines.append("")
            lines.append("| インデックス名 | カラム | ユニーク | 説明 |")
            lines.append("|----------------|--------|----------|------|")
            
            for idx in table_def.business_indexes:
                columns_str = ", ".join(idx.columns)
                unique_str = "○" if idx.unique else "×"
                lines.append(f"| {idx.name} | {columns_str} | {unique_str} | {idx.comment} |")
            
            lines.append("")
        
        # 外部キーテーブル
        if table_def.foreign_keys:
            lines.append("## 外部キー")
            lines.append("")
            lines.append("| 制約名 | カラム | 参照テーブル | 参照カラム | 更新時 | 削除時 | 説明 |")
            lines.append("|--------|--------|--------------|------------|--------|--------|------|")
            
            for fk in table_def.foreign_keys:
                on_update = getattr(fk, 'on_update', 'CASCADE')
                on_delete = getattr(fk, 'on_delete', 'RESTRICT')
                lines.append(f"| {fk.name} | {fk.column} | {fk.reference_table} | {fk.reference_column} | {on_update} | {on_delete} | {fk.comment} |")
            
            lines.append("")
        
        # 制約テーブル（チェック制約など）
        lines.append("## 制約")
        lines.append("")
        lines.append("| 制約名 | 種別 | 条件 | 説明 |")
        lines.append("|--------|------|------|------|")
        
        # 主キー制約
        primary_cols = [col for col in table_def.business_columns if hasattr(col, 'primary') and col.primary]
        if primary_cols:
            pk_names = ", ".join([col.name for col in primary_cols])
            lines.append(f"| pk_{table_def.name.lower()} | PRIMARY KEY | {pk_names} | 主キー制約 |")
        
        # 一意制約
        unique_cols = [col for col in table_def.business_columns if hasattr(col, 'unique') and col.unique]
        for col in unique_cols:
            lines.append(f"| uk_{col.name} | UNIQUE |  | {col.name}一意制約 |")
        
        # その他の制約（例：チェック制約）
        for col in table_def.business_columns:
            if 'level' in col.name.lower() and 'INT' in col.data_type.upper():
                lines.append(f"| chk_{col.name} | CHECK | {col.name} > 0 | {col.name}正値チェック制約 |")
            elif 'status' in col.name.lower() or 'type' in col.name.lower():
                lines.append(f"| chk_{col.name} | CHECK | {col.name} IN (...) | {col.name}値チェック制約 |")
        
        lines.append("")
        
        # サンプルデータテーブル
        if hasattr(table_def, 'sample_data') and table_def.sample_data:
            lines.append("## サンプルデータ")
            lines.append("")
            
            # ヘッダー行を作成
            sample_data = table_def.sample_data
            if sample_data:
                # 最初のサンプルデータからカラム名を取得
                first_sample = sample_data[0]
                header_cols = list(first_sample.keys())
                
                # ヘッダー
                header_line = "| " + " | ".join(header_cols) + " |"
                lines.append(header_line)
                
                # セパレータ
                separator_line = "|" + "|".join(["------" for _ in header_cols]) + "|"
                lines.append(separator_line)
                
                # データ行（最大3件）
                for i, sample in enumerate(sample_data[:3]):
                    values = []
                    for col in header_cols:
                        value = sample.get(col, "")
                        if value is None:
                            value = "None"
                        values.append(str(value))
                    data_line = "| " + " | ".join(values) + " |"
                    lines.append(data_line)
            
            lines.append("")
        
        # 特記事項
        lines.append("## 特記事項")
        lines.append("")
        if hasattr(table_def, 'notes') and table_def.notes:
            for note in table_def.notes:
                lines.append(f"- {note}")
        else:
            lines.append("- データの整合性・一意性制約を適切に設定")
            lines.append("- パフォーマンス最適化のためのインデックス設計")
            lines.append("- 関連システムとの連携を考慮したデータ構造")
        lines.append("")
        
        # 業務ルール
        lines.append("## 業務ルール")
        lines.append("")
        if hasattr(table_def, 'business_rules') and table_def.business_rules:
            for rule in table_def.business_rules:
                lines.append(f"- {rule}")
        else:
            lines.append("- 主キーの一意性は必須で変更不可")
            lines.append("- 外部キー制約による参照整合性の保証")
            lines.append("- 論理削除による履歴データの保持")
        lines.append("")
        
        # 改版履歴テーブル
        lines.append("## 改版履歴")
        lines.append("")
        lines.append("| バージョン | 更新日 | 更新者 | 変更内容 |")
        lines.append("|------------|--------|--------|----------|")
        
        if hasattr(table_def, 'revision_history') and table_def.revision_history:
            for revision in table_def.revision_history:
                version = revision.get('version', '1.0.0')
                date = revision.get('date', datetime.now().strftime('%Y-%m-%d'))
                author = revision.get('author', '開発チーム')
                changes = revision.get('changes', 'テーブル定義')
                lines.append(f"| {version} | {date} | {author} | {changes} |")
        else:
            lines.append(f"| 1.0.0 | {datetime.now().strftime('%Y-%m-%d')} | 開発チーム | 初版作成 - {logical_name}テーブルの詳細定義 |")
        
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
                data_dir = self.config.data_dir
            
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
        self.logger.info("📊 処理結果サマリー")
        
        if dry_run:
            self.logger.info("🔍 ドライラン実行")
        
        self.logger.info(f"📁 生成ファイル数: {len(result.generated_files)}")
        self.logger.info(f"⚠️ エラー数: {len(result.errors)}")
        
        if result.errors:
            self.logger.info("❌ エラー詳細")
            for error in result.errors:
                self.logger.error(f"  - {error}")
        
        if result.success:
            self.logger.info("🎉 すべての処理が正常に完了しました！")
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
