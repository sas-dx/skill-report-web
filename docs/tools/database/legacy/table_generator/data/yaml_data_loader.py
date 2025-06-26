#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAMLデータローダークラス

このモジュールは、YAML形式のテーブル定義ファイルを読み込み、
データ構造に変換する機能を提供します。
"""

import sys
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import re

# パッケージのパスを追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.core.logger import DatabaseToolsLogger, get_logger
from shared.core.models import (
    TableDefinition, ColumnDefinition, IndexDefinition, 
    ForeignKeyDefinition, ConstraintDefinition, ProcessingResult
)
from table_generator.utils.yaml_loader import YamlLoader
from shared.utils.file_utils import FileManager as FileUtils


class YamlDataLoader:
    """YAMLデータローダークラス
    
    YAML形式のテーブル定義ファイルを読み込み、
    TableDefinitionオブジェクトに変換します。
    """
    
    def __init__(self, base_dir: str = None, logger: DatabaseToolsLogger = None):
        """初期化
        
        Args:
            base_dir (str, optional): ベースディレクトリパス
            logger (DatabaseToolsLogger, optional): ログ出力インスタンス
        """
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.logger = logger or get_logger(__name__)
        self.yaml_loader = YamlLoader(logger=self.logger)
        self.file_utils = FileUtils(logger=self.logger)
        
        # ディレクトリパス
        self.table_details_dir = self.base_dir / "table-details"
        self.tables_list_file = self.base_dir / "テーブル一覧.md"
        
        self.logger.info("YamlDataLoader が初期化されました")
    
    def load_table_definition(self, table_name: str) -> Optional[TableDefinition]:
        """指定されたテーブルの定義を読み込み
        
        Args:
            table_name (str): テーブル名
            
        Returns:
            Optional[TableDefinition]: テーブル定義オブジェクト
        """
        try:
            yaml_file = self.table_details_dir / f"{table_name}.yaml"
            
            if not yaml_file.exists():
                self.logger.error(f"YAML定義ファイルが見つかりません: {yaml_file}")
                return None
            
            # YAMLファイルを読み込み
            yaml_data = self.yaml_loader.load_yaml_file(yaml_file)
            if not yaml_data:
                self.logger.error(f"YAML定義の読み込みに失敗: {yaml_file}")
                return None
            
            # バリデーション
            if not self._validate_yaml_structure(yaml_data, table_name):
                return None
            
            # TableDefinitionオブジェクトに変換
            table_def = self.yaml_loader.parse_table_definition(yaml_data)
            if not table_def:
                self.logger.error(f"テーブル定義の解析に失敗: {table_name}")
                return None
            
            # 追加バリデーション
            if not self._validate_table_definition(table_def):
                return None
            
            self.logger.success(f"✅ テーブル定義を読み込みました: {table_name}")
            return table_def
            
        except Exception as e:
            self.logger.error(f"テーブル定義の読み込みでエラー: {table_name} - {str(e)}")
            return None
    
    def load_all_table_definitions(self, table_names: Optional[List[str]] = None) -> Dict[str, TableDefinition]:
        """すべてのテーブル定義を読み込み
        
        Args:
            table_names (List[str], optional): 読み込み対象テーブル名リスト
            
        Returns:
            Dict[str, TableDefinition]: テーブル名をキーとした定義辞書
        """
        table_definitions = {}
        
        try:
            # 対象テーブルリストを取得
            if table_names:
                target_tables = table_names
            else:
                target_tables = self._get_all_table_names()
            
            if not target_tables:
                self.logger.warning("読み込み対象のテーブルが見つかりません")
                return table_definitions
            
            self.logger.info(f"📋 {len(target_tables)} 個のテーブル定義を読み込み開始")
            
            # 各テーブルの定義を読み込み
            for table_name in target_tables:
                table_def = self.load_table_definition(table_name)
                if table_def:
                    table_definitions[table_name] = table_def
                else:
                    self.logger.warning(f"⚠️ {table_name} の読み込みをスキップしました")
            
            self.logger.success(f"🎉 {len(table_definitions)} 個のテーブル定義を読み込み完了")
            
        except Exception as e:
            self.logger.error(f"テーブル定義の一括読み込みでエラー: {str(e)}")
        
        return table_definitions
    
    def _get_all_table_names(self) -> List[str]:
        """すべてのテーブル名を取得
        
        Returns:
            List[str]: テーブル名リスト
        """
        table_names = []
        
        try:
            # table-detailsディレクトリからYAMLファイルを検索
            if self.table_details_dir.exists():
                yaml_files = self.file_utils.find_files_by_extension(
                    self.table_details_dir, ['.yaml', '.yml'], recursive=False
                )
                
                for yaml_file in yaml_files:
                    table_name = yaml_file.stem
                    table_names.append(table_name)
            
            # テーブル一覧.mdからも取得（補完用）
            if self.tables_list_file.exists():
                md_tables = self._extract_table_names_from_markdown()
                for table_name in md_tables:
                    if table_name not in table_names:
                        table_names.append(table_name)
            
            table_names.sort()  # アルファベット順にソート
            
        except Exception as e:
            self.logger.error(f"テーブル名の取得でエラー: {str(e)}")
        
        return table_names
    
    def _extract_table_names_from_markdown(self) -> List[str]:
        """Markdownファイルからテーブル名を抽出
        
        Returns:
            List[str]: テーブル名リスト
        """
        table_names = []
        
        try:
            content = self.file_utils.read_file(self.tables_list_file)
            if not content:
                return table_names
            
            # テーブル名のパターンを検索（| テーブル名 | の形式）
            pattern = r'\|\s*([A-Z][A-Z0-9_]+)\s*\|'
            matches = re.findall(pattern, content)
            
            for match in matches:
                if match not in ['テーブル名', 'TABLE_NAME']:  # ヘッダー行を除外
                    table_names.append(match)
            
        except Exception as e:
            self.logger.error(f"Markdownからのテーブル名抽出でエラー: {str(e)}")
        
        return table_names
    
    def _validate_yaml_structure(self, yaml_data: Dict[str, Any], table_name: str) -> bool:
        """YAML構造の妥当性をチェック
        
        Args:
            yaml_data (Dict[str, Any]): YAMLデータ
            table_name (str): テーブル名
            
        Returns:
            bool: 妥当性チェック結果
        """
        try:
            # 必須フィールドのチェック
            required_fields = ['table_name', 'logical_name']
            for field in required_fields:
                if field not in yaml_data:
                    self.logger.error(f"必須フィールドが不足: {field} in {table_name}")
                    return False
            
            # 説明フィールドのチェック（commentまたはdescription）
            if 'comment' not in yaml_data and 'description' not in yaml_data:
                self.logger.warning(f"commentまたはdescriptionフィールドがありません: {table_name}")
            
            # テーブル名の一致チェック
            if yaml_data['table_name'] != table_name:
                self.logger.warning(f"ファイル名とテーブル名が不一致: {table_name} != {yaml_data['table_name']}")
            
            # columnsの存在チェック（business_columnsまたはcolumns）
            columns_data = yaml_data.get('columns') or yaml_data.get('business_columns')
            if not columns_data:
                self.logger.error(f"columnsまたはbusiness_columnsが定義されていません: {table_name}")
                return False
            
            if not isinstance(columns_data, list):
                self.logger.error(f"columnsがリスト形式ではありません: {table_name}")
                return False
            
            if len(columns_data) == 0:
                self.logger.error(f"columnsが空です: {table_name}")
                return False
            
            # カラム定義の基本チェック
            for i, column in enumerate(columns_data):
                if not self._validate_column_structure(column, table_name, i):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"YAML構造バリデーションでエラー: {table_name} - {str(e)}")
            return False
    
    def _validate_column_structure(self, column: Dict[str, Any], table_name: str, index: int) -> bool:
        """カラム構造の妥当性をチェック
        
        Args:
            column (Dict[str, Any]): カラム定義
            table_name (str): テーブル名
            index (int): カラムインデックス
            
        Returns:
            bool: 妥当性チェック結果
        """
        try:
            # 必須フィールドのチェック（typeまたはdata_type）
            required_fields = ['name']
            for field in required_fields:
                if field not in column:
                    self.logger.error(f"カラム{index}に必須フィールドが不足: {field} in {table_name}")
                    return False
            
            # データ型フィールドの存在チェック
            if 'type' not in column and 'data_type' not in column:
                self.logger.error(f"カラム{index}にtypeまたはdata_typeフィールドが不足: {table_name}")
                return False
            
            # カラム名の形式チェック
            column_name = column['name']
            if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', column_name):
                self.logger.error(f"カラム名の形式が不正: {column_name} in {table_name}")
                return False
            
            # データ型の形式チェック
            data_type = column.get('type') or column.get('data_type')
            if not isinstance(data_type, str) or len(data_type.strip()) == 0:
                self.logger.error(f"データ型が不正: {data_type} in {table_name}.{column_name}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"カラム構造バリデーションでエラー: {table_name} - {str(e)}")
            return False
    
    def _validate_table_definition(self, table_def: TableDefinition) -> bool:
        """テーブル定義の妥当性をチェック
        
        Args:
            table_def (TableDefinition): テーブル定義
            
        Returns:
            bool: 妥当性チェック結果
        """
        try:
            # 基本情報のチェック
            if not table_def.table_name or len(table_def.table_name.strip()) == 0:
                self.logger.error("テーブル名が空です")
                return False
            
            if not table_def.logical_name or len(table_def.logical_name.strip()) == 0:
                self.logger.error(f"論理名が空です: {table_def.table_name}")
                return False
            
            # カラム定義のチェック
            if not table_def.business_columns:
                self.logger.error(f"ビジネスカラムが定義されていません: {table_def.table_name}")
                return False
            
            # 重複カラム名のチェック
            column_names = [col.name for col in table_def.business_columns]
            if len(column_names) != len(set(column_names)):
                duplicates = [name for name in column_names if column_names.count(name) > 1]
                self.logger.error(f"重複するカラム名があります: {duplicates} in {table_def.table_name}")
                return False
            
            # プライマリキーのチェック
            primary_columns = [col for col in table_def.business_columns if col.primary]
            if len(primary_columns) == 0:
                self.logger.warning(f"プライマリキーが定義されていません: {table_def.table_name}")
            
            # 外部キーの参照整合性チェック（基本的なもの）
            if table_def.foreign_keys:
                for fk in table_def.foreign_keys:
                    if not self._validate_foreign_key(fk, table_def):
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"テーブル定義バリデーションでエラー: {str(e)}")
            return False
    
    def _validate_foreign_key(self, fk: ForeignKeyDefinition, table_def: TableDefinition) -> bool:
        """外部キーの妥当性をチェック
        
        Args:
            fk (ForeignKeyDefinition): 外部キー定義
            table_def (TableDefinition): テーブル定義
            
        Returns:
            bool: 妥当性チェック結果
        """
        try:
            # 参照元カラムの存在チェック
            column_names = [col.name for col in table_def.business_columns]
            if fk.column not in column_names:
                self.logger.error(f"外部キーの参照元カラムが存在しません: {fk.column} in {table_def.table_name}")
                return False
            
            # 基本的な命名規則チェック
            if not fk.name or len(fk.name.strip()) == 0:
                self.logger.error(f"外部キー名が空です: {table_def.table_name}")
                return False
            
            if not fk.reference_table or len(fk.reference_table.strip()) == 0:
                self.logger.error(f"参照テーブル名が空です: {fk.name} in {table_def.table_name}")
                return False
            
            if not fk.reference_column or len(fk.reference_column.strip()) == 0:
                self.logger.error(f"参照カラム名が空です: {fk.name} in {table_def.table_name}")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"外部キーバリデーションでエラー: {str(e)}")
            return False
    
    def validate_all_definitions(self, table_definitions: Dict[str, TableDefinition]) -> ProcessingResult:
        """すべてのテーブル定義の相互参照チェック
        
        Args:
            table_definitions (Dict[str, TableDefinition]): テーブル定義辞書
            
        Returns:
            ProcessingResult: バリデーション結果
        """
        result = ProcessingResult()
        
        try:
            self.logger.header("🔍 テーブル定義の相互参照チェックを開始")
            
            # 外部キーの参照整合性チェック
            for table_name, table_def in table_definitions.items():
                if table_def.foreign_keys:
                    for fk in table_def.foreign_keys:
                        if not self._check_foreign_key_reference(fk, table_definitions, table_name):
                            result.errors.append(f"{table_name}: 外部キー {fk.name} の参照先が不正")
            
            # 循環参照のチェック
            circular_refs = self._check_circular_references(table_definitions)
            if circular_refs:
                result.errors.extend([f"循環参照を検出: {ref}" for ref in circular_refs])
            
            result.success = len(result.errors) == 0
            
            if result.success:
                self.logger.success("✅ すべてのテーブル定義が正常です")
            else:
                self.logger.error(f"❌ {len(result.errors)} 個のエラーが見つかりました")
                for error in result.errors:
                    self.logger.error(f"  - {error}")
            
        except Exception as e:
            result.success = False
            result.error_message = f"相互参照チェックでエラー: {str(e)}"
            self.logger.error(result.error_message)
        
        return result
    
    def _check_foreign_key_reference(self, fk: ForeignKeyDefinition, 
                                   table_definitions: Dict[str, TableDefinition], 
                                   source_table: str) -> bool:
        """外部キーの参照先チェック
        
        Args:
            fk (ForeignKeyDefinition): 外部キー定義
            table_definitions (Dict[str, TableDefinition]): テーブル定義辞書
            source_table (str): 参照元テーブル名
            
        Returns:
            bool: 参照先が正常な場合True
        """
        # 参照先テーブルの存在チェック
        if fk.reference_table not in table_definitions:
            self.logger.error(f"参照先テーブルが存在しません: {fk.reference_table} (from {source_table}.{fk.column})")
            return False
        
        # 参照先カラムの存在チェック
        ref_table_def = table_definitions[fk.reference_table]
        ref_column_names = [col.name for col in ref_table_def.business_columns]
        
        if fk.reference_column not in ref_column_names:
            self.logger.error(f"参照先カラムが存在しません: {fk.reference_table}.{fk.reference_column} (from {source_table}.{fk.column})")
            return False
        
        return True
    
    def _check_circular_references(self, table_definitions: Dict[str, TableDefinition]) -> List[str]:
        """循環参照のチェック
        
        Args:
            table_definitions (Dict[str, TableDefinition]): テーブル定義辞書
            
        Returns:
            List[str]: 循環参照のパスリスト
        """
        circular_refs = []
        
        def find_path(current_table: str, target_table: str, path: List[str]) -> bool:
            if current_table == target_table and len(path) > 1:
                return True
            
            if current_table in path:
                return False
            
            if current_table not in table_definitions:
                return False
            
            table_def = table_definitions[current_table]
            if not table_def.foreign_keys:
                return False
            
            new_path = path + [current_table]
            
            for fk in table_def.foreign_keys:
                if find_path(fk.reference_table, target_table, new_path):
                    return True
            
            return False
        
        # 各テーブルから自分自身への循環参照をチェック
        for table_name in table_definitions.keys():
            if find_path(table_name, table_name, []):
                circular_refs.append(table_name)
        
        return circular_refs
    
    def get_table_statistics(self, table_definitions: Dict[str, TableDefinition]) -> Dict[str, Any]:
        """テーブル定義の統計情報を取得
        
        Args:
            table_definitions (Dict[str, TableDefinition]): テーブル定義辞書
            
        Returns:
            Dict[str, Any]: 統計情報
        """
        stats = {
            'total_tables': len(table_definitions),
            'total_columns': 0,
            'total_indexes': 0,
            'total_foreign_keys': 0,
            'table_types': {},
            'column_types': {},
            'tables_with_primary_key': 0,
            'tables_without_primary_key': []
        }
        
        for table_name, table_def in table_definitions.items():
            # カラム数
            stats['total_columns'] += len(table_def.business_columns)
            
            # インデックス数
            if table_def.business_indexes:
                stats['total_indexes'] += len(table_def.business_indexes)
            
            # 外部キー数
            if table_def.foreign_keys:
                stats['total_foreign_keys'] += len(table_def.foreign_keys)
            
            # テーブル種別
            if table_name.startswith('MST_'):
                table_type = 'マスタ'
            elif table_name.startswith('TRN_'):
                table_type = 'トランザクション'
            else:
                table_type = 'その他'
            
            stats['table_types'][table_type] = stats['table_types'].get(table_type, 0) + 1
            
            # プライマリキーの有無
            has_primary = any(col.primary for col in table_def.business_columns)
            if has_primary:
                stats['tables_with_primary_key'] += 1
            else:
                stats['tables_without_primary_key'].append(table_name)
            
            # カラム型の統計
            for col in table_def.business_columns:
                base_type = col.data_type.split('(')[0].upper()
                stats['column_types'][base_type] = stats['column_types'].get(base_type, 0) + 1
        
        return stats
