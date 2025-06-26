#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
データベース整合性チェックツール - 統合データモデルサービス

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

統合データモデルを使用したデータベース整合性チェックサービス
レガシーモデルの依存関係を除去し、統合データモデルのみを使用
"""

from typing import List, Dict, Any, Optional, Set, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum

# 統合データモデルのインポート
from ...shared.core.models import (
    TableDefinition,
    ColumnDefinition,
    IndexDefinition,
    ForeignKeyDefinition,
    CheckResult,
    CheckStatus,
    create_table_definition_from_yaml
)

# 統合パーサーのインポート
from ...shared.parsers.yaml_parser import YamlParser
from ...shared.parsers.ddl_parser import DDLParser
from ...shared.parsers.markdown_parser import MarkdownParser

logger = logging.getLogger(__name__)


class CheckType(Enum):
    """チェック種別"""
    TABLE_EXISTENCE = "table_existence"
    COLUMN_CONSISTENCY = "column_consistency"
    FOREIGN_KEY_CONSISTENCY = "foreign_key_consistency"
    DATA_TYPE_CONSISTENCY = "data_type_consistency"
    ORPHANED_FILES = "orphaned_files"
    NAMING_CONVENTION = "naming_convention"


@dataclass
class ConsistencyIssue:
    """整合性問題の詳細"""
    check_type: CheckType
    severity: str  # "error", "warning", "info"
    table_name: str
    column_name: Optional[str] = None
    message: str = ""
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}


class DatabaseConsistencyService:
    """
    統合データモデルを使用するデータベース整合性チェックサービス
    
    統合データモデルとパーサーを使用してデータベース整合性をチェック
    """
    
    def __init__(self):
        self.yaml_parser = YamlParser()
        self.ddl_parser = DDLParser()
        self.markdown_parser = MarkdownParser()
        self.issues: List[ConsistencyIssue] = []
    
    def load_table_definitions_from_yaml(self, yaml_dir: Path) -> Dict[str, TableDefinition]:
        """YAML詳細定義ディレクトリから全テーブル定義を読み込み"""
        table_definitions = {}
        
        try:
            for yaml_file in yaml_dir.glob("*_details.yaml"):
                table_name = yaml_file.stem.replace("_details", "")
                try:
                    yaml_data = self.yaml_parser.parse_file(yaml_file)
                    table_def = create_table_definition_from_yaml(yaml_data)
                    table_definitions[table_name] = table_def
                    logger.debug(f"YAML定義読み込み完了: {table_name}")
                except Exception as e:
                    logger.error(f"YAML読み込みエラー: {yaml_file} - {e}")
                    self.add_issue(CheckType.TABLE_EXISTENCE, "error", table_name, 
                                 message=f"YAML読み込みエラー: {e}")
        
        except Exception as e:
            logger.error(f"YAMLディレクトリ読み込みエラー: {yaml_dir} - {e}")
        
        return table_definitions
    
    def load_ddl_definitions(self, ddl_dir: Path) -> Dict[str, TableDefinition]:
        """DDLディレクトリから全テーブル定義を読み込み"""
        ddl_definitions = {}
        
        try:
            for ddl_file in ddl_dir.glob("*.sql"):
                if ddl_file.name.startswith("------------"):
                    continue  # テンプレートファイルをスキップ
                
                table_name = ddl_file.stem
                try:
                    ddl_content = ddl_file.read_text(encoding='utf-8')
                    table_def = self.ddl_parser.parse_ddl(ddl_content, table_name)
                    ddl_definitions[table_name] = table_def
                    logger.debug(f"DDL定義読み込み完了: {table_name}")
                except Exception as e:
                    logger.error(f"DDL読み込みエラー: {ddl_file} - {e}")
                    self.add_issue(CheckType.TABLE_EXISTENCE, "error", table_name,
                                 message=f"DDL読み込みエラー: {e}")
        
        except Exception as e:
            logger.error(f"DDLディレクトリ読み込みエラー: {ddl_dir} - {e}")
        
        return ddl_definitions
    
    def load_markdown_definitions(self, markdown_dir: Path) -> Dict[str, TableDefinition]:
        """Markdownディレクトリから全テーブル定義を読み込み"""
        markdown_definitions = {}
        
        try:
            for md_file in markdown_dir.glob("テーブル定義書_*.md"):
                try:
                    # ファイル名からテーブル名を抽出
                    filename_parts = md_file.stem.split("_")
                    if len(filename_parts) >= 2:
                        table_name = filename_parts[1]
                        
                        md_content = md_file.read_text(encoding='utf-8')
                        table_def = self.markdown_parser.parse_markdown(md_content, table_name)
                        markdown_definitions[table_name] = table_def
                        logger.debug(f"Markdown定義読み込み完了: {table_name}")
                except Exception as e:
                    logger.error(f"Markdown読み込みエラー: {md_file} - {e}")
                    # テーブル名が特定できない場合は汎用エラー
                    self.add_issue(CheckType.TABLE_EXISTENCE, "error", "unknown",
                                 message=f"Markdown読み込みエラー: {e}")
        
        except Exception as e:
            logger.error(f"Markdownディレクトリ読み込みエラー: {markdown_dir} - {e}")
        
        return markdown_definitions
    
    def check_table_existence_consistency(self, yaml_defs: Dict[str, TableDefinition], 
                                        ddl_defs: Dict[str, TableDefinition],
                                        markdown_defs: Dict[str, TableDefinition]) -> CheckResult:
        """テーブル存在整合性チェック"""
        result = CheckResult(check_name="table_existence")
        
        all_tables = set(yaml_defs.keys()) | set(ddl_defs.keys()) | set(markdown_defs.keys())
        
        for table_name in all_tables:
            yaml_exists = table_name in yaml_defs
            ddl_exists = table_name in ddl_defs
            markdown_exists = table_name in markdown_defs
            
            if not yaml_exists:
                self.add_issue(CheckType.TABLE_EXISTENCE, "error", table_name,
                             message="YAML詳細定義が存在しません")
                result.add_error(f"{table_name}: YAML詳細定義が存在しません")
            
            if not ddl_exists:
                self.add_issue(CheckType.TABLE_EXISTENCE, "error", table_name,
                             message="DDLファイルが存在しません")
                result.add_error(f"{table_name}: DDLファイルが存在しません")
            
            if not markdown_exists:
                self.add_issue(CheckType.TABLE_EXISTENCE, "warning", table_name,
                             message="Markdownファイルが存在しません")
                result.add_warning(f"{table_name}: Markdownファイルが存在しません")
        
        if result.errors:
            result.set_failed()
        else:
            result.set_success()
        
        return result
    
    def check_column_consistency(self, yaml_defs: Dict[str, TableDefinition],
                               ddl_defs: Dict[str, TableDefinition]) -> CheckResult:
        """カラム定義整合性チェック"""
        result = CheckResult(check_name="column_consistency")
        
        common_tables = set(yaml_defs.keys()) & set(ddl_defs.keys())
        
        for table_name in common_tables:
            yaml_table = yaml_defs[table_name]
            ddl_table = ddl_defs[table_name]
            
            # カラム名の比較
            yaml_columns = {col.name: col for col in yaml_table.columns}
            ddl_columns = {col.name: col for col in ddl_table.columns}
            
            yaml_col_names = set(yaml_columns.keys())
            ddl_col_names = set(ddl_columns.keys())
            
            # YAML にのみ存在するカラム
            yaml_only = yaml_col_names - ddl_col_names
            for col_name in yaml_only:
                self.add_issue(CheckType.COLUMN_CONSISTENCY, "error", table_name, col_name,
                             message="YAMLにのみ存在するカラムです")
                result.add_error(f"{table_name}.{col_name}: YAMLにのみ存在")
            
            # DDL にのみ存在するカラム
            ddl_only = ddl_col_names - yaml_col_names
            for col_name in ddl_only:
                self.add_issue(CheckType.COLUMN_CONSISTENCY, "error", table_name, col_name,
                             message="DDLにのみ存在するカラムです")
                result.add_error(f"{table_name}.{col_name}: DDLにのみ存在")
            
            # 共通カラムの詳細比較
            common_columns = yaml_col_names & ddl_col_names
            for col_name in common_columns:
                yaml_col = yaml_columns[col_name]
                ddl_col = ddl_columns[col_name]
                
                # データ型比較
                if yaml_col.type != ddl_col.type:
                    self.add_issue(CheckType.DATA_TYPE_CONSISTENCY, "error", table_name, col_name,
                                 message=f"データ型不一致: YAML({yaml_col.type}) ≠ DDL({ddl_col.type})")
                    result.add_error(f"{table_name}.{col_name}: データ型不一致")
                
                # NULL制約比較
                if yaml_col.nullable != ddl_col.nullable:
                    self.add_issue(CheckType.COLUMN_CONSISTENCY, "error", table_name, col_name,
                                 message=f"NULL制約不一致: YAML({yaml_col.nullable}) ≠ DDL({ddl_col.nullable})")
                    result.add_error(f"{table_name}.{col_name}: NULL制約不一致")
                
                # プライマリキー比較
                if yaml_col.primary_key != ddl_col.primary_key:
                    self.add_issue(CheckType.COLUMN_CONSISTENCY, "error", table_name, col_name,
                                 message=f"プライマリキー設定不一致: YAML({yaml_col.primary_key}) ≠ DDL({ddl_col.primary_key})")
                    result.add_error(f"{table_name}.{col_name}: プライマリキー設定不一致")
        
        if result.errors:
            result.set_failed()
        else:
            result.set_success()
        
        return result
    
    def check_foreign_key_consistency(self, yaml_defs: Dict[str, TableDefinition]) -> CheckResult:
        """外部キー整合性チェック"""
        result = CheckResult(check_name="foreign_key_consistency")
        
        for table_name, table_def in yaml_defs.items():
            for fk in table_def.foreign_keys:
                ref_table = fk.references.get("table")
                ref_columns = fk.references.get("columns", [])
                
                # 参照先テーブルの存在チェック
                if ref_table not in yaml_defs:
                    self.add_issue(CheckType.FOREIGN_KEY_CONSISTENCY, "error", table_name,
                                 message=f"外部キー {fk.name} の参照先テーブル '{ref_table}' が存在しません")
                    result.add_error(f"{table_name}: 参照先テーブル '{ref_table}' が存在しません")
                    continue
                
                # 参照先カラムの存在チェック
                ref_table_def = yaml_defs[ref_table]
                ref_table_columns = {col.name: col for col in ref_table_def.columns}
                
                for ref_col in ref_columns:
                    if ref_col not in ref_table_columns:
                        self.add_issue(CheckType.FOREIGN_KEY_CONSISTENCY, "error", table_name,
                                     message=f"外部キー {fk.name} の参照先カラム '{ref_table}.{ref_col}' が存在しません")
                        result.add_error(f"{table_name}: 参照先カラム '{ref_table}.{ref_col}' が存在しません")
                
                # データ型整合性チェック
                source_columns = {col.name: col for col in table_def.columns}
                for i, source_col_name in enumerate(fk.columns):
                    if i < len(ref_columns):
                        ref_col_name = ref_columns[i]
                        if (source_col_name in source_columns and 
                            ref_col_name in ref_table_columns):
                            source_col = source_columns[source_col_name]
                            ref_col = ref_table_columns[ref_col_name]
                            
                            if source_col.type != ref_col.type:
                                self.add_issue(CheckType.FOREIGN_KEY_CONSISTENCY, "warning", table_name,
                                             message=f"外部キー {fk.name} のデータ型不一致: {source_col.type} ≠ {ref_col.type}")
                                result.add_warning(f"{table_name}: 外部キーデータ型不一致")
        
        if result.errors:
            result.set_failed()
        else:
            result.set_success()
        
        return result
    
    def check_naming_convention(self, yaml_defs: Dict[str, TableDefinition]) -> CheckResult:
        """命名規則チェック"""
        result = CheckResult(check_name="naming_convention")
        
        valid_prefixes = ["MST_", "TRN_", "HIS_", "SYS_", "WRK_", "IF_"]
        
        for table_name, table_def in yaml_defs.items():
            # テーブル名プレフィックスチェック
            if not any(table_name.startswith(prefix) for prefix in valid_prefixes):
                self.add_issue(CheckType.NAMING_CONVENTION, "warning", table_name,
                             message=f"テーブル名が命名規則に従っていません。有効なプレフィックス: {valid_prefixes}")
                result.add_warning(f"{table_name}: 命名規則違反")
            
            # カラム名チェック（基本的なルール）
            for col in table_def.columns:
                # 予約語チェック（簡易版）
                reserved_words = ["order", "group", "select", "from", "where"]
                if col.name.lower() in reserved_words:
                    self.add_issue(CheckType.NAMING_CONVENTION, "warning", table_name, col.name,
                                 message="予約語がカラム名に使用されています")
                    result.add_warning(f"{table_name}.{col.name}: 予約語使用")
        
        if result.errors:
            result.set_failed()
        else:
            result.set_success()
        
        return result
    
    def check_orphaned_files(self, yaml_dir: Path, ddl_dir: Path, markdown_dir: Path) -> CheckResult:
        """孤立ファイル検出"""
        result = CheckResult(check_name="orphaned_files")
        
        # 各ディレクトリのファイル一覧取得
        yaml_files = {f.stem.replace("_details", "") for f in yaml_dir.glob("*_details.yaml")}
        ddl_files = {f.stem for f in ddl_dir.glob("*.sql") if not f.name.startswith("------------")}
        markdown_files = set()
        
        for md_file in markdown_dir.glob("テーブル定義書_*.md"):
            filename_parts = md_file.stem.split("_")
            if len(filename_parts) >= 2:
                markdown_files.add(filename_parts[1])
        
        all_tables = yaml_files | ddl_files | markdown_files
        
        # 孤立ファイル検出
        for table_name in all_tables:
            file_count = sum([
                table_name in yaml_files,
                table_name in ddl_files,
                table_name in markdown_files
            ])
            
            if file_count == 1:
                file_types = []
                if table_name in yaml_files:
                    file_types.append("YAML")
                if table_name in ddl_files:
                    file_types.append("DDL")
                if table_name in markdown_files:
                    file_types.append("Markdown")
                
                self.add_issue(CheckType.ORPHANED_FILES, "warning", table_name,
                             message=f"孤立ファイル: {', '.join(file_types)}のみ存在")
                result.add_warning(f"{table_name}: 孤立ファイル ({', '.join(file_types)})")
        
        result.set_success()  # 孤立ファイルは警告レベル
        return result
    
    def run_all_checks(self, yaml_dir: Path, ddl_dir: Path, markdown_dir: Path, 
                      check_types: Optional[List[CheckType]] = None) -> List[CheckResult]:
        """全チェックの実行"""
        self.issues.clear()
        results = []
        
        if check_types is None:
            check_types = list(CheckType)
        
        # データ読み込み
        yaml_defs = self.load_table_definitions_from_yaml(yaml_dir)
        ddl_defs = self.load_ddl_definitions(ddl_dir)
        markdown_defs = self.load_markdown_definitions(markdown_dir)
        
        # 各チェックの実行
        if CheckType.TABLE_EXISTENCE in check_types:
            result = self.check_table_existence_consistency(yaml_defs, ddl_defs, markdown_defs)
            results.append(result)
        
        if CheckType.COLUMN_CONSISTENCY in check_types:
            result = self.check_column_consistency(yaml_defs, ddl_defs)
            results.append(result)
        
        if CheckType.FOREIGN_KEY_CONSISTENCY in check_types:
            result = self.check_foreign_key_consistency(yaml_defs)
            results.append(result)
        
        if CheckType.NAMING_CONVENTION in check_types:
            result = self.check_naming_convention(yaml_defs)
            results.append(result)
        
        if CheckType.ORPHANED_FILES in check_types:
            result = self.check_orphaned_files(yaml_dir, ddl_dir, markdown_dir)
            results.append(result)
        
        return results
    
    def add_issue(self, check_type: CheckType, severity: str, table_name: str, 
                 column_name: Optional[str] = None, message: str = "", 
                 details: Optional[Dict[str, Any]] = None):
        """問題の追加"""
        issue = ConsistencyIssue(
            check_type=check_type,
            severity=severity,
            table_name=table_name,
            column_name=column_name,
            message=message,
            details=details or {}
        )
        self.issues.append(issue)
    
    def get_issues_by_severity(self, severity: str) -> List[ConsistencyIssue]:
        """重要度別問題取得"""
        return [issue for issue in self.issues if issue.severity == severity]
    
    def get_issues_by_table(self, table_name: str) -> List[ConsistencyIssue]:
        """テーブル別問題取得"""
        return [issue for issue in self.issues if issue.table_name == table_name]
    
    def get_summary(self, results: List[CheckResult]) -> Dict[str, Any]:
        """チェック結果サマリー"""
        total_checks = len(results)
        passed_checks = len([r for r in results if r.is_success()])
        failed_checks = total_checks - passed_checks
        
        total_errors = sum(len(r.errors) for r in results)
        total_warnings = sum(len(r.warnings) for r in results)
        
        error_issues = self.get_issues_by_severity("error")
        warning_issues = self.get_issues_by_severity("warning")
        
        return {
            "total_checks": total_checks,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "success_rate": (passed_checks / total_checks * 100) if total_checks > 0 else 0,
            "total_errors": total_errors,
            "total_warnings": total_warnings,
            "total_issues": len(self.issues),
            "error_issues": len(error_issues),
            "warning_issues": len(warning_issues),
            "issues_by_type": {
                check_type.value: len([i for i in self.issues if i.check_type == check_type])
                for check_type in CheckType
            }
        }


# 便利関数
def create_consistency_service() -> DatabaseConsistencyService:
    """整合性チェックサービスのファクトリー関数"""
    return DatabaseConsistencyService()


def run_consistency_check(yaml_dir: Path, ddl_dir: Path, markdown_dir: Path,
                         check_types: Optional[List[CheckType]] = None) -> Tuple[List[CheckResult], List[ConsistencyIssue]]:
    """整合性チェック実行の便利関数"""
    service = create_consistency_service()
    results = service.run_all_checks(yaml_dir, ddl_dir, markdown_dir, check_types)
    return results, service.issues
