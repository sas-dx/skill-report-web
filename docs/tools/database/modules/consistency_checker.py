"""
整合性チェックモジュール
要求仕様ID: PLT.1-WEB.1

全ファイル間の整合性をチェックします：
1. テーブル存在整合性（YAML ↔ DDL ↔ Markdown）
2. カラム定義整合性
3. 外部キー整合性
4. データ型整合性
"""

import os
import yaml
import re
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
from dataclasses import dataclass

from core.config import Config
from core.logger import setup_logger
from core.exceptions import DatabaseToolsError


@dataclass
class ConsistencyResult:
    """整合性チェック結果"""
    is_consistent: bool
    table_name: str
    errors: List[str]
    warnings: List[str]


class ConsistencyChecker:
    """整合性チェッククラス"""
    
    def __init__(self, config: Config):
        """初期化"""
        self.config = config
        self.logger = setup_logger(__name__, config.log_level)
        
        # ディレクトリパス
        self.yaml_dir = Path(config.table_details_dir)
        self.ddl_dir = Path(config.ddl_dir)
        self.tables_dir = Path(config.tables_dir)
        self.data_dir = Path(config.data_dir)
    
    def check_all(self, verbose: bool = False) -> bool:
        """全テーブルの整合性チェック"""
        self.logger.info("全テーブルの整合性チェックを開始します")
        
        # 全テーブル名取得
        table_names = self._get_all_table_names()
        if not table_names:
            self.logger.warning("チェック対象のテーブルが見つかりません")
            return True
        
        all_consistent = True
        results = []
        
        for table_name in table_names:
            result = self._check_table_consistency(table_name, verbose)
            results.append(result)
            
            if not result.is_consistent:
                all_consistent = False
        
        # 外部キー参照整合性チェック
        fk_result = self._check_foreign_key_references(table_names, verbose)
        if not fk_result:
            all_consistent = False
        
        # 結果サマリー
        self._print_summary(results, verbose)
        
        return all_consistent
    
    def check_single(self, table_name: str, verbose: bool = False) -> bool:
        """特定テーブルの整合性チェック"""
        self.logger.info(f"テーブル {table_name} の整合性チェックを開始します")
        
        result = self._check_table_consistency(table_name, verbose)
        
        if verbose:
            self._print_result(result)
        
        return result.is_consistent
    
    def _get_all_table_names(self) -> Set[str]:
        """全テーブル名取得"""
        table_names = set()
        
        # YAMLファイルから取得
        if self.yaml_dir.exists():
            for yaml_file in self.yaml_dir.glob("*.yaml"):
                table_name = self._extract_table_name_from_yaml(yaml_file.name)
                if table_name:
                    table_names.add(table_name)
        
        # DDLファイルから取得
        if self.ddl_dir.exists():
            for ddl_file in self.ddl_dir.glob("*.sql"):
                table_name = ddl_file.stem
                if table_name and not table_name.endswith("_sample"):
                    table_names.add(table_name)
        
        # Markdownファイルから取得
        if self.tables_dir.exists():
            for md_file in self.tables_dir.glob("*.md"):
                table_name = self._extract_table_name_from_markdown(md_file.name)
                if table_name:
                    table_names.add(table_name)
        
        return table_names
    
    def _check_table_consistency(self, table_name: str, verbose: bool) -> ConsistencyResult:
        """テーブル整合性チェック"""
        errors = []
        warnings = []
        
        try:
            # ファイル存在チェック
            yaml_file = self.yaml_dir / f"テーブル詳細定義YAML_{table_name}.yaml"
            ddl_file = self.ddl_dir / f"{table_name}.sql"
            
            # YAMLファイル存在チェック
            if not yaml_file.exists():
                errors.append(f"YAMLファイルが存在しません: {yaml_file}")
                return ConsistencyResult(False, table_name, errors, warnings)
            
            # YAMLデータ読み込み
            yaml_data = self._load_yaml_data(yaml_file)
            if not yaml_data:
                errors.append("YAMLファイルの読み込みに失敗しました")
                return ConsistencyResult(False, table_name, errors, warnings)
            
            # DDLファイル存在チェック
            if not ddl_file.exists():
                errors.append(f"DDLファイルが存在しません: {ddl_file}")
            else:
                # DDL整合性チェック
                self._check_ddl_consistency(table_name, yaml_data, ddl_file, errors, warnings)
            
            # Markdownファイル存在チェック
            logical_name = yaml_data.get('logical_name', table_name)
            md_file = self.tables_dir / f"テーブル定義書_{table_name}_{logical_name}.md"
            if not md_file.exists():
                warnings.append(f"Markdownファイルが存在しません: {md_file}")
            else:
                # Markdown整合性チェック
                self._check_markdown_consistency(table_name, yaml_data, md_file, errors, warnings)
            
            # サンプルデータファイルチェック
            sample_file = self.data_dir / f"{table_name}_sample.sql"
            if yaml_data.get('sample_data') and not sample_file.exists():
                warnings.append(f"サンプルデータファイルが存在しません: {sample_file}")
            
        except Exception as e:
            errors.append(f"整合性チェック中にエラーが発生しました: {e}")
        
        is_consistent = len(errors) == 0
        return ConsistencyResult(is_consistent, table_name, errors, warnings)
    
    def _check_ddl_consistency(self, table_name: str, yaml_data: Dict[str, Any], 
                              ddl_file: Path, errors: List[str], warnings: List[str]):
        """DDL整合性チェック"""
        try:
            with open(ddl_file, 'r', encoding='utf-8') as f:
                ddl_content = f.read()
            
            # テーブル名チェック
            if f"CREATE TABLE {table_name}" not in ddl_content:
                errors.append(f"DDLにテーブル作成文が見つかりません: {table_name}")
                return
            
            # カラム定義チェック
            yaml_columns = yaml_data.get('columns', [])
            for column in yaml_columns:
                col_name = column.get('name', '')
                col_type = column.get('type', '')
                
                if not col_name:
                    continue
                
                # カラム存在チェック
                if col_name not in ddl_content:
                    errors.append(f"DDLにカラムが見つかりません: {col_name}")
                    continue
                
                # データ型チェック（簡易）
                if col_type and col_type not in ddl_content:
                    warnings.append(f"DDLのデータ型が一致しない可能性があります: {col_name} ({col_type})")
            
            # インデックスチェック
            yaml_indexes = yaml_data.get('indexes', [])
            for index in yaml_indexes:
                index_name = index.get('name', '')
                if index_name and f"CREATE INDEX {index_name}" not in ddl_content and f"CREATE UNIQUE INDEX {index_name}" not in ddl_content:
                    warnings.append(f"DDLにインデックスが見つかりません: {index_name}")
            
            # 外部キーチェック
            yaml_fks = yaml_data.get('foreign_keys', [])
            for fk in yaml_fks:
                fk_name = fk.get('name', '')
                if fk_name and f"CONSTRAINT {fk_name}" not in ddl_content:
                    warnings.append(f"DDLに外部キー制約が見つかりません: {fk_name}")
            
        except Exception as e:
            errors.append(f"DDL整合性チェックエラー: {e}")
    
    def _check_markdown_consistency(self, table_name: str, yaml_data: Dict[str, Any], 
                                   md_file: Path, errors: List[str], warnings: List[str]):
        """Markdown整合性チェック"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            # テーブル名チェック
            if table_name not in md_content:
                warnings.append(f"Markdownにテーブル名が見つかりません: {table_name}")
            
            # 論理名チェック
            logical_name = yaml_data.get('logical_name', '')
            if logical_name and logical_name not in md_content:
                warnings.append(f"Markdownに論理名が見つかりません: {logical_name}")
            
            # カラム定義チェック（簡易）
            yaml_columns = yaml_data.get('columns', [])
            for column in yaml_columns:
                col_name = column.get('name', '')
                if col_name and col_name not in md_content:
                    warnings.append(f"Markdownにカラムが見つかりません: {col_name}")
            
        except Exception as e:
            warnings.append(f"Markdown整合性チェックエラー: {e}")
    
    def _check_foreign_key_references(self, table_names: Set[str], verbose: bool) -> bool:
        """外部キー参照整合性チェック"""
        self.logger.info("外部キー参照整合性チェックを開始します")
        
        all_valid = True
        
        for table_name in table_names:
            yaml_file = self.yaml_dir / f"テーブル詳細定義YAML_{table_name}.yaml"
            if not yaml_file.exists():
                continue
            
            yaml_data = self._load_yaml_data(yaml_file)
            if not yaml_data:
                continue
            
            foreign_keys = yaml_data.get('foreign_keys', [])
            for fk in foreign_keys:
                ref_table = fk.get('references', {}).get('table', '')
                if ref_table and ref_table not in table_names:
                    if verbose:
                        print(f"❌ 外部キー参照エラー: {table_name} -> {ref_table} (参照先テーブルが存在しません)")
                    all_valid = False
        
        return all_valid
    
    def _load_yaml_data(self, yaml_file: Path) -> Optional[Dict[str, Any]]:
        """YAMLデータ読み込み"""
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"YAMLファイル読み込みエラー: {e}")
            return None
    
    def _extract_table_name_from_yaml(self, filename: str) -> Optional[str]:
        """YAMLファイル名からテーブル名を抽出"""
        if filename.startswith("テーブル詳細定義YAML_") and filename.endswith(".yaml"):
            return filename[len("テーブル詳細定義YAML_"):-len(".yaml")]
        return None
    
    def _extract_table_name_from_markdown(self, filename: str) -> Optional[str]:
        """Markdownファイル名からテーブル名を抽出"""
        if filename.startswith("テーブル定義書_") and filename.endswith(".md"):
            # テーブル定義書_{table_name}_{logical_name}.md の形式
            parts = filename[len("テーブル定義書_"):-len(".md")].split("_", 1)
            if parts:
                return parts[0]
        return None
    
    def _print_summary(self, results: List[ConsistencyResult], verbose: bool):
        """結果サマリー出力"""
        total_tables = len(results)
        consistent_tables = sum(1 for r in results if r.is_consistent)
        inconsistent_tables = total_tables - consistent_tables
        
        print(f"\n=== 整合性チェック結果サマリー ===")
        print(f"総テーブル数: {total_tables}")
        print(f"✅ 整合性OK: {consistent_tables}")
        print(f"❌ 整合性NG: {inconsistent_tables}")
        
        if inconsistent_tables > 0:
            print(f"\n=== 整合性エラーテーブル一覧 ===")
            for result in results:
                if not result.is_consistent:
                    print(f"❌ {result.table_name}")
                    if verbose:
                        for error in result.errors:
                            print(f"   - {error}")
        
        if verbose:
            print(f"\n=== 詳細結果 ===")
            for result in results:
                self._print_result(result)
    
    def _print_result(self, result: ConsistencyResult):
        """個別結果出力"""
        status = "✅ 整合性OK" if result.is_consistent else "❌ 整合性NG"
        print(f"\n{status}: {result.table_name}")
        
        if result.errors:
            print("  エラー:")
            for error in result.errors:
                print(f"    - {error}")
        
        if result.warnings:
            print("  警告:")
            for warning in result.warnings:
                print(f"    - {warning}")
