#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - 統合データモデルサービス

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

統合データモデルを使用したテーブル生成サービス
レガシーモデルの依存関係を除去し、統合データモデルのみを使用
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

# 統合データモデルのインポート
from ...shared.core.models import (
    TableDefinition,
    ColumnDefinition,
    IndexDefinition,
    ForeignKeyDefinition,
    GenerationResult,
    GenerationStatus,
    create_table_definition_from_yaml
)

# 統合パーサーのインポート
from ...shared.parsers.yaml_parser import YamlParser

# 統合ジェネレーターのインポート
from ...shared.generators.ddl_generator import DDLGenerator
from ...shared.generators.markdown_generator import MarkdownGenerator
from ...shared.generators.sample_data_generator import SampleDataGenerator

logger = logging.getLogger(__name__)


class TableGeneratorService:
    """
    統合データモデルを使用するテーブル生成サービス
    
    統合データモデルとジェネレーターを使用してテーブル関連ファイルを生成
    """
    
    def __init__(self):
        self.yaml_parser = YamlParser()
        self.ddl_generator = DDLGenerator()
        self.markdown_generator = MarkdownGenerator()
        self.sample_data_generator = SampleDataGenerator()
    
    def load_table_definition_from_yaml(self, yaml_file: Path) -> TableDefinition:
        """YAMLファイルから統合テーブル定義を読み込み"""
        try:
            yaml_data = self.yaml_parser.parse_file(yaml_file)
            return create_table_definition_from_yaml(yaml_data)
        except Exception as e:
            logger.error(f"YAML読み込みエラー: {yaml_file} - {e}")
            raise
    
    def generate_table_files(self, table_def: TableDefinition, output_dirs: Dict[str, Path]) -> GenerationResult:
        """統合テーブル定義からファイル生成"""
        try:
            result = GenerationResult(table_name=table_def.name)
            
            # DDLファイル生成
            if 'ddl' in output_dirs:
                ddl_content = self.ddl_generator.generate(table_def)
                ddl_file = output_dirs['ddl'] / f"{table_def.name}.sql"
                ddl_file.parent.mkdir(parents=True, exist_ok=True)
                ddl_file.write_text(ddl_content, encoding='utf-8')
                result.add_generated_file(ddl_file)
                logger.info(f"DDLファイル生成完了: {ddl_file}")
            
            # Markdownファイル生成
            if 'tables' in output_dirs:
                markdown_content = self.markdown_generator.generate(table_def)
                markdown_file = output_dirs['tables'] / f"テーブル定義書_{table_def.name}_{table_def.logical_name}.md"
                markdown_file.parent.mkdir(parents=True, exist_ok=True)
                markdown_file.write_text(markdown_content, encoding='utf-8')
                result.add_generated_file(markdown_file)
                logger.info(f"Markdownファイル生成完了: {markdown_file}")
            
            # サンプルデータファイル生成
            if 'data' in output_dirs:
                sample_data_content = self.sample_data_generator.generate(table_def)
                sample_data_file = output_dirs['data'] / f"{table_def.name}_sample_data.sql"
                sample_data_file.parent.mkdir(parents=True, exist_ok=True)
                sample_data_file.write_text(sample_data_content, encoding='utf-8')
                result.add_generated_file(sample_data_file)
                logger.info(f"サンプルデータファイル生成完了: {sample_data_file}")
            
            result.set_success()
            logger.info(f"テーブル生成完了: {table_def.name}")
            return result
            
        except Exception as e:
            logger.error(f"テーブル生成エラー: {table_def.name} - {e}")
            result = GenerationResult(table_name=table_def.name)
            result.add_error(str(e))
            result.set_failed()
            return result
    
    def process_table(self, table_name: str, yaml_dir: Path, output_dirs: Dict[str, Path]) -> GenerationResult:
        """テーブル処理のメインエントリーポイント"""
        try:
            # YAML詳細定義ファイルの読み込み
            yaml_file = yaml_dir / f"{table_name}_details.yaml"
            if not yaml_file.exists():
                result = GenerationResult(table_name=table_name)
                result.add_error(f"YAML詳細定義ファイルが見つかりません: {yaml_file}")
                result.set_failed()
                return result
            
            # 統合テーブル定義の読み込み
            table_def = self.load_table_definition_from_yaml(yaml_file)
            
            # ファイル生成
            return self.generate_table_files(table_def, output_dirs)
            
        except Exception as e:
            logger.error(f"テーブル処理エラー: {table_name} - {e}")
            result = GenerationResult(table_name=table_name)
            result.add_error(str(e))
            result.set_failed()
            return result
    
    def process_multiple_tables(self, table_names: List[str], yaml_dir: Path, output_dirs: Dict[str, Path]) -> List[GenerationResult]:
        """複数テーブルの一括処理"""
        results = []
        
        for table_name in table_names:
            try:
                result = self.process_table(table_name, yaml_dir, output_dirs)
                results.append(result)
                
                if result.is_success():
                    logger.info(f"テーブル処理成功: {table_name}")
                else:
                    logger.warning(f"テーブル処理失敗: {table_name} - {result.errors}")
                    
            except Exception as e:
                logger.error(f"テーブル処理例外: {table_name} - {e}")
                result = GenerationResult(table_name=table_name)
                result.add_error(str(e))
                result.set_failed()
                results.append(result)
        
        return results
    
    def validate_table_definition(self, table_def: TableDefinition) -> List[str]:
        """テーブル定義の妥当性検証"""
        errors = []
        
        try:
            # 基本項目チェック
            if not table_def.name:
                errors.append("テーブル名が設定されていません")
            
            if not table_def.logical_name:
                errors.append("論理名が設定されていません")
            
            if not table_def.columns:
                errors.append("カラム定義が存在しません")
            
            # プライマリキーチェック
            primary_keys = [col for col in table_def.columns if col.primary_key]
            if not primary_keys:
                errors.append("プライマリキーが定義されていません")
            
            # カラム名重複チェック
            column_names = [col.name for col in table_def.columns]
            if len(column_names) != len(set(column_names)):
                errors.append("重複するカラム名が存在します")
            
            # 外部キー参照チェック
            for fk in table_def.foreign_keys:
                if not fk.references.get("table"):
                    errors.append(f"外部キー {fk.name} の参照テーブルが設定されていません")
                
                if not fk.references.get("columns"):
                    errors.append(f"外部キー {fk.name} の参照カラムが設定されていません")
            
            # インデックス定義チェック
            for idx in table_def.indexes:
                if not idx.columns:
                    errors.append(f"インデックス {idx.name} のカラムが設定されていません")
                
                # インデックス対象カラムの存在チェック
                for col_name in idx.columns:
                    if col_name not in column_names:
                        errors.append(f"インデックス {idx.name} の対象カラム {col_name} が存在しません")
            
        except Exception as e:
            errors.append(f"検証処理中にエラーが発生しました: {e}")
        
        return errors
    
    def get_generation_summary(self, results: List[GenerationResult]) -> Dict[str, Any]:
        """生成結果のサマリー作成"""
        total_tables = len(results)
        successful_tables = len([r for r in results if r.is_success()])
        failed_tables = total_tables - successful_tables
        
        all_errors = []
        all_warnings = []
        all_generated_files = []
        
        for result in results:
            all_errors.extend(result.errors)
            all_warnings.extend(result.warnings)
            all_generated_files.extend([str(f) for f in result.generated_files])
        
        return {
            "total_tables": total_tables,
            "successful_tables": successful_tables,
            "failed_tables": failed_tables,
            "success_rate": (successful_tables / total_tables * 100) if total_tables > 0 else 0,
            "total_generated_files": len(all_generated_files),
            "total_errors": len(all_errors),
            "total_warnings": len(all_warnings),
            "generated_files": all_generated_files,
            "errors": all_errors,
            "warnings": all_warnings
        }


# 便利関数
def create_table_generator_service() -> TableGeneratorService:
    """テーブル生成サービスのファクトリー関数"""
    return TableGeneratorService()


def process_single_table(table_name: str, yaml_dir: Path, output_dirs: Dict[str, Path]) -> GenerationResult:
    """単一テーブル処理の便利関数"""
    service = create_table_generator_service()
    return service.process_table(table_name, yaml_dir, output_dirs)


def process_tables_batch(table_names: List[str], yaml_dir: Path, output_dirs: Dict[str, Path]) -> List[GenerationResult]:
    """複数テーブル一括処理の便利関数"""
    service = create_table_generator_service()
    return service.process_multiple_tables(table_names, yaml_dir, output_dirs)
