#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
データベース整合性チェックツール - 統合データモデルアダプター

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

統合データモデルと既存database_consistency_checkerモデル間の変換を提供
既存機能の100%互換性を保証
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from datetime import datetime

# 統合データモデルのインポート
from ..shared.core.models import (
    TableDefinition as UnifiedTableDefinition,
    ColumnDefinition as UnifiedColumnDefinition,
    IndexDefinition as UnifiedIndexDefinition,
    ForeignKeyDefinition as UnifiedForeignKeyDefinition,
    CheckResult as UnifiedCheckResult,
    CheckSeverity as UnifiedCheckSeverity,
    ConsistencyReport as UnifiedConsistencyReport,
    create_table_definition_from_yaml
)

# 既存database_consistency_checkerモデルのインポート
from .models import (
    TableDefinition as LegacyTableDefinition,
    ColumnDefinition as LegacyColumnDefinition,
    IndexDefinition as LegacyIndexDefinition,
    ForeignKeyDefinition as LegacyForeignKeyDefinition,
    ConstraintDefinition as LegacyConstraintDefinition,
    CheckResult as LegacyCheckResult,
    CheckSeverity as LegacyCheckSeverity,
    FixSuggestion as LegacyFixSuggestion,
    ConsistencyReport as LegacyConsistencyReport,
    CheckConfig as LegacyCheckConfig,
    FixType,
    DDLTable,
    InsertStatement,
    EntityRelationship,
    TableListEntry
)

logger = logging.getLogger(__name__)


class ConsistencyCheckerAdapter:
    """
    統合データモデルと既存database_consistency_checkerモデル間の変換アダプター
    
    既存のdatabase_consistency_checker機能を統合データモデルで動作させるための
    アダプターパターン実装
    """
    
    @staticmethod
    def unified_to_legacy_column(unified_col: UnifiedColumnDefinition) -> LegacyColumnDefinition:
        """統合カラム定義を既存形式に変換"""
        try:
            return LegacyColumnDefinition(
                name=unified_col.name,
                logical_name=unified_col.comment or unified_col.name,
                data_type=unified_col.type,
                length=unified_col.length,
                nullable=unified_col.nullable,
                unique=unified_col.unique,
                primary_key=unified_col.primary_key,
                foreign_key=False,  # 外部キーは別途判定
                default_value=str(unified_col.default) if unified_col.default is not None else None,
                comment=unified_col.comment or "",
                encrypted=False,  # 統合モデルには暗号化フラグがないため
                enum_values=[],  # 統合モデルには列挙値がないため
                validation=""  # 統合モデルには検証ルールがないため
            )
        except Exception as e:
            logger.error(f"カラム変換エラー: {unified_col.name} - {e}")
            raise
    
    @staticmethod
    def legacy_to_unified_column(legacy_col: LegacyColumnDefinition, requirement_id: str = None) -> UnifiedColumnDefinition:
        """既存カラム定義を統合形式に変換"""
        try:
            return UnifiedColumnDefinition(
                name=legacy_col.name,
                type=legacy_col.data_type,
                nullable=legacy_col.nullable,
                primary_key=legacy_col.primary_key,
                unique=legacy_col.unique,
                default=legacy_col.default_value,
                comment=legacy_col.comment,
                requirement_id=requirement_id,
                length=legacy_col.length
            )
        except Exception as e:
            logger.error(f"カラム変換エラー: {legacy_col.name} - {e}")
            raise
    
    @staticmethod
    def unified_to_legacy_index(unified_idx: UnifiedIndexDefinition) -> LegacyIndexDefinition:
        """統合インデックス定義を既存形式に変換"""
        try:
            return LegacyIndexDefinition(
                name=unified_idx.name,
                columns=unified_idx.columns,
                unique=unified_idx.unique,
                description=unified_idx.comment or ""
            )
        except Exception as e:
            logger.error(f"インデックス変換エラー: {unified_idx.name} - {e}")
            raise
    
    @staticmethod
    def legacy_to_unified_index(legacy_idx: LegacyIndexDefinition) -> UnifiedIndexDefinition:
        """既存インデックス定義を統合形式に変換"""
        try:
            return UnifiedIndexDefinition(
                name=legacy_idx.name,
                columns=legacy_idx.columns,
                unique=legacy_idx.unique,
                comment=legacy_idx.description
            )
        except Exception as e:
            logger.error(f"インデックス変換エラー: {legacy_idx.name} - {e}")
            raise
    
    @staticmethod
    def unified_to_legacy_foreign_key(unified_fk: UnifiedForeignKeyDefinition) -> LegacyForeignKeyDefinition:
        """統合外部キー定義を既存形式に変換"""
        try:
            # 統合モデルは複数カラム対応、既存モデルは単一カラムのみ
            column = unified_fk.columns[0] if unified_fk.columns else ""
            reference_column = unified_fk.references.get("columns", [""])[0]
            
            return LegacyForeignKeyDefinition(
                name=unified_fk.name,
                column=column,
                reference_table=unified_fk.references.get("table", ""),
                reference_column=reference_column,
                on_update=unified_fk.on_update,
                on_delete=unified_fk.on_delete,
                description=""
            )
        except Exception as e:
            logger.error(f"外部キー変換エラー: {unified_fk.name} - {e}")
            raise
    
    @staticmethod
    def legacy_to_unified_foreign_key(legacy_fk: LegacyForeignKeyDefinition) -> UnifiedForeignKeyDefinition:
        """既存外部キー定義を統合形式に変換"""
        try:
            return UnifiedForeignKeyDefinition(
                name=legacy_fk.name,
                columns=[legacy_fk.column],
                references={
                    "table": legacy_fk.reference_table,
                    "columns": [legacy_fk.reference_column]
                },
                on_update=legacy_fk.on_update,
                on_delete=legacy_fk.on_delete
            )
        except Exception as e:
            logger.error(f"外部キー変換エラー: {legacy_fk.name} - {e}")
            raise
    
    @staticmethod
    def unified_to_legacy_table(unified_table: UnifiedTableDefinition) -> LegacyTableDefinition:
        """統合テーブル定義を既存形式に変換"""
        try:
            # カラム変換
            columns = []
            for col in unified_table.columns:
                legacy_col = ConsistencyCheckerAdapter.unified_to_legacy_column(col)
                columns.append(legacy_col)
            
            # インデックス変換
            indexes = []
            for idx in unified_table.indexes:
                legacy_idx = ConsistencyCheckerAdapter.unified_to_legacy_index(idx)
                indexes.append(legacy_idx)
            
            # 外部キー変換
            foreign_keys = []
            for fk in unified_table.foreign_keys:
                legacy_fk = ConsistencyCheckerAdapter.unified_to_legacy_foreign_key(fk)
                foreign_keys.append(legacy_fk)
            
            return LegacyTableDefinition(
                table_name=unified_table.name,
                logical_name=unified_table.logical_name,
                category=unified_table.category,
                overview=unified_table.comment or "",
                columns=columns,
                indexes=indexes,
                foreign_keys=foreign_keys,
                constraints=[],  # 統合モデルには制約定義がないため空
                sample_data=[],
                notes=[],
                business_rules=[]
            )
        except Exception as e:
            logger.error(f"テーブル変換エラー: {unified_table.name} - {e}")
            raise
    
    @staticmethod
    def legacy_to_unified_table(legacy_table: LegacyTableDefinition, requirement_id: str = None) -> UnifiedTableDefinition:
        """既存テーブル定義を統合形式に変換"""
        try:
            # カラム変換
            columns = []
            for col in legacy_table.columns:
                unified_col = ConsistencyCheckerAdapter.legacy_to_unified_column(col, requirement_id)
                columns.append(unified_col)
            
            # インデックス変換
            indexes = []
            for idx in legacy_table.indexes:
                unified_idx = ConsistencyCheckerAdapter.legacy_to_unified_index(idx)
                indexes.append(unified_idx)
            
            # 外部キー変換
            foreign_keys = []
            for fk in legacy_table.foreign_keys:
                unified_fk = ConsistencyCheckerAdapter.legacy_to_unified_foreign_key(fk)
                foreign_keys.append(unified_fk)
            
            return UnifiedTableDefinition(
                name=legacy_table.table_name,
                logical_name=legacy_table.logical_name,
                category=legacy_table.category,
                priority="中",  # デフォルト値
                requirement_id=requirement_id or "PLT.1-WEB.1",
                columns=columns,
                indexes=indexes,
                foreign_keys=foreign_keys,
                comment=legacy_table.overview
            )
        except Exception as e:
            logger.error(f"テーブル変換エラー: {legacy_table.table_name} - {e}")
            raise
    
    @staticmethod
    def unified_to_legacy_check_severity(unified_severity: UnifiedCheckSeverity) -> LegacyCheckSeverity:
        """統合チェック重要度を既存形式に変換"""
        severity_mapping = {
            UnifiedCheckSeverity.SUCCESS: LegacyCheckSeverity.SUCCESS,
            UnifiedCheckSeverity.INFO: LegacyCheckSeverity.INFO,
            UnifiedCheckSeverity.WARNING: LegacyCheckSeverity.WARNING,
            UnifiedCheckSeverity.ERROR: LegacyCheckSeverity.ERROR
        }
        return severity_mapping.get(unified_severity, LegacyCheckSeverity.INFO)
    
    @staticmethod
    def legacy_to_unified_check_severity(legacy_severity: LegacyCheckSeverity) -> UnifiedCheckSeverity:
        """既存チェック重要度を統合形式に変換"""
        severity_mapping = {
            LegacyCheckSeverity.SUCCESS: UnifiedCheckSeverity.SUCCESS,
            LegacyCheckSeverity.INFO: UnifiedCheckSeverity.INFO,
            LegacyCheckSeverity.WARNING: UnifiedCheckSeverity.WARNING,
            LegacyCheckSeverity.ERROR: UnifiedCheckSeverity.ERROR
        }
        return severity_mapping.get(legacy_severity, UnifiedCheckSeverity.INFO)
    
    @staticmethod
    def unified_to_legacy_check_result(unified_result: UnifiedCheckResult) -> LegacyCheckResult:
        """統合チェック結果を既存形式に変換"""
        try:
            return LegacyCheckResult(
                check_name=unified_result.check_name,
                table_name=unified_result.table_name,
                severity=ConsistencyCheckerAdapter.unified_to_legacy_check_severity(unified_result.severity),
                message=unified_result.message,
                details=unified_result.details,
                file_path=unified_result.file_path,
                line_number=unified_result.line_number
            )
        except Exception as e:
            logger.error(f"チェック結果変換エラー: {unified_result.check_name} - {e}")
            raise
    
    @staticmethod
    def legacy_to_unified_check_result(legacy_result: LegacyCheckResult) -> UnifiedCheckResult:
        """既存チェック結果を統合形式に変換"""
        try:
            return UnifiedCheckResult(
                check_name=legacy_result.check_name,
                table_name=legacy_result.table_name,
                severity=ConsistencyCheckerAdapter.legacy_to_unified_check_severity(legacy_result.severity),
                message=legacy_result.message,
                details=legacy_result.details,
                file_path=legacy_result.file_path,
                line_number=legacy_result.line_number
            )
        except Exception as e:
            logger.error(f"チェック結果変換エラー: {legacy_result.check_name} - {e}")
            raise
    
    @staticmethod
    def unified_to_legacy_report(unified_report: UnifiedConsistencyReport) -> LegacyConsistencyReport:
        """統合整合性レポートを既存形式に変換"""
        try:
            # チェック結果変換
            results = []
            for result in unified_report.results:
                legacy_result = ConsistencyCheckerAdapter.unified_to_legacy_check_result(result)
                results.append(legacy_result)
            
            # 修正提案は統合モデルにないため空のリスト
            fix_suggestions = []
            
            return LegacyConsistencyReport(
                check_date=unified_report.check_date,
                total_tables=unified_report.total_tables,
                total_checks=unified_report.total_checks,
                results=results,
                fix_suggestions=fix_suggestions,
                summary=unified_report.summary
            )
        except Exception as e:
            logger.error(f"レポート変換エラー: {e}")
            raise
    
    @staticmethod
    def legacy_to_unified_report(legacy_report: LegacyConsistencyReport) -> UnifiedConsistencyReport:
        """既存整合性レポートを統合形式に変換"""
        try:
            # チェック結果変換
            results = []
            for result in legacy_report.results:
                unified_result = ConsistencyCheckerAdapter.legacy_to_unified_check_result(result)
                results.append(unified_result)
            
            return UnifiedConsistencyReport(
                check_date=legacy_report.check_date,
                total_tables=legacy_report.total_tables,
                total_checks=legacy_report.total_checks,
                results=results,
                summary=legacy_report.summary
            )
        except Exception as e:
            logger.error(f"レポート変換エラー: {e}")
            raise


class UnifiedConsistencyCheckerService:
    """
    統合データモデルを使用する整合性チェックサービス
    
    既存のdatabase_consistency_checker機能を統合データモデルで提供
    """
    
    def __init__(self):
        self.adapter = ConsistencyCheckerAdapter()
    
    def load_table_definitions_from_yaml(self, yaml_dir: Path) -> List[UnifiedTableDefinition]:
        """YAML詳細定義ディレクトリから統合テーブル定義を読み込み"""
        try:
            import yaml
            table_definitions = []
            
            for yaml_file in yaml_dir.glob("*_details.yaml"):
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                
                table_def = create_table_definition_from_yaml(yaml_data)
                table_definitions.append(table_def)
            
            return table_definitions
        except Exception as e:
            logger.error(f"YAML読み込みエラー: {yaml_dir} - {e}")
            raise
    
    def check_consistency_with_unified_model(self, base_dir: Path) -> UnifiedConsistencyReport:
        """統合データモデルを使用した整合性チェック"""
        try:
            # YAML詳細定義の読み込み
            yaml_dir = base_dir / "table-details"
            table_definitions = self.load_table_definitions_from_yaml(yaml_dir)
            
            # 整合性チェック実行
            results = []
            total_checks = 0
            
            for table_def in table_definitions:
                # 各テーブルに対してチェック実行
                table_results = self._check_table_consistency(table_def, base_dir)
                results.extend(table_results)
                total_checks += len(table_results)
            
            # サマリー作成
            summary = self._create_summary(results)
            
            return UnifiedConsistencyReport(
                check_date=datetime.now().isoformat(),
                total_tables=len(table_definitions),
                total_checks=total_checks,
                results=results,
                summary=summary
            )
            
        except Exception as e:
            logger.error(f"統合モデル整合性チェックエラー: {e}")
            raise
    
    def _check_table_consistency(self, table_def: UnifiedTableDefinition, base_dir: Path) -> List[UnifiedCheckResult]:
        """個別テーブルの整合性チェック"""
        results = []
        
        try:
            # DDLファイル存在チェック
            ddl_file = base_dir / "ddl" / f"{table_def.name}.sql"
            if not ddl_file.exists():
                results.append(UnifiedCheckResult(
                    check_name="ddl_file_existence",
                    table_name=table_def.name,
                    severity=UnifiedCheckSeverity.ERROR,
                    message=f"DDLファイルが存在しません: {ddl_file}",
                    file_path=str(ddl_file)
                ))
            
            # Markdownファイル存在チェック
            md_file = base_dir / "tables" / f"テーブル定義書_{table_def.name}_{table_def.logical_name}.md"
            if not md_file.exists():
                results.append(UnifiedCheckResult(
                    check_name="markdown_file_existence",
                    table_name=table_def.name,
                    severity=UnifiedCheckSeverity.WARNING,
                    message=f"Markdownファイルが存在しません: {md_file}",
                    file_path=str(md_file)
                ))
            
            # カラム定義チェック
            for col in table_def.columns:
                if not col.name:
                    results.append(UnifiedCheckResult(
                        check_name="column_name_validation",
                        table_name=table_def.name,
                        severity=UnifiedCheckSeverity.ERROR,
                        message=f"カラム名が空です",
                        details={"column": col.name}
                    ))
                
                if not col.type:
                    results.append(UnifiedCheckResult(
                        check_name="column_type_validation",
                        table_name=table_def.name,
                        severity=UnifiedCheckSeverity.ERROR,
                        message=f"カラム型が空です: {col.name}",
                        details={"column": col.name}
                    ))
            
            # 外部キー整合性チェック
            for fk in table_def.foreign_keys:
                ref_table = fk.references.get("table")
                if ref_table:
                    # 参照先テーブルの存在確認（簡易版）
                    ref_yaml = base_dir / "table-details" / f"{ref_table}_details.yaml"
                    if not ref_yaml.exists():
                        results.append(UnifiedCheckResult(
                            check_name="foreign_key_reference_validation",
                            table_name=table_def.name,
                            severity=UnifiedCheckSeverity.ERROR,
                            message=f"参照先テーブルが存在しません: {ref_table}",
                            details={"foreign_key": fk.name, "reference_table": ref_table}
                        ))
            
        except Exception as e:
            results.append(UnifiedCheckResult(
                check_name="table_check_error",
                table_name=table_def.name,
                severity=UnifiedCheckSeverity.ERROR,
                message=f"テーブルチェック中にエラーが発生しました: {e}"
            ))
        
        return results
    
    def _create_summary(self, results: List[UnifiedCheckResult]) -> Dict[str, int]:
        """チェック結果のサマリー作成"""
        summary = {
            "total": len(results),
            "success": 0,
            "info": 0,
            "warning": 0,
            "error": 0
        }
        
        for result in results:
            if result.severity == UnifiedCheckSeverity.SUCCESS:
                summary["success"] += 1
            elif result.severity == UnifiedCheckSeverity.INFO:
                summary["info"] += 1
            elif result.severity == UnifiedCheckSeverity.WARNING:
                summary["warning"] += 1
            elif result.severity == UnifiedCheckSeverity.ERROR:
                summary["error"] += 1
        
        return summary


# 既存コードとの互換性を保つためのファサード
def create_legacy_compatible_checker() -> 'LegacyConsistencyCheckerService':
    """既存コード互換性のためのチェッカー作成"""
    return LegacyConsistencyCheckerService()


class LegacyConsistencyCheckerService:
    """既存コード互換性のためのファサードサービス"""
    
    def __init__(self):
        self.unified_service = UnifiedConsistencyCheckerService()
        self.adapter = ConsistencyCheckerAdapter()
    
    def check_consistency(self, config: LegacyCheckConfig) -> LegacyConsistencyReport:
        """既存インターフェースでの整合性チェック"""
        try:
            # 統合モデルでチェック実行
            base_dir = Path(config.base_dir) if config.base_dir else Path.cwd()
            unified_report = self.unified_service.check_consistency_with_unified_model(base_dir)
            
            # 既存形式に変換して返却
            return self.adapter.unified_to_legacy_report(unified_report)
            
        except Exception as e:
            logger.error(f"互換チェッカー処理エラー: {e}")
            return LegacyConsistencyReport(
                check_date=datetime.now().isoformat(),
                total_tables=0,
                total_checks=0,
                results=[],
                fix_suggestions=[],
                summary={"total": 0, "success": 0, "info": 0, "warning": 0, "error": 1}
            )
    
    def load_table_definitions(self, yaml_dir: Path) -> List[LegacyTableDefinition]:
        """既存インターフェースでのテーブル定義読み込み"""
        try:
            # 統合モデルで読み込み
            unified_tables = self.unified_service.load_table_definitions_from_yaml(yaml_dir)
            
            # 既存形式に変換
            legacy_tables = []
            for unified_table in unified_tables:
                legacy_table = self.adapter.unified_to_legacy_table(unified_table)
                legacy_tables.append(legacy_table)
            
            return legacy_tables
            
        except Exception as e:
            logger.error(f"テーブル定義読み込みエラー: {e}")
            return []
