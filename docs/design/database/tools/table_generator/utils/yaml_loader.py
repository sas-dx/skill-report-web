#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - YAML読み込みユーティリティ

YAML形式のテーブル定義ファイルの読み込み・解析機能を提供します。

対応要求仕様ID: PLT.2-TOOL.1
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from shared.core.logger import DatabaseToolsLogger
from shared.core.models import TableDefinition, ColumnDefinition, IndexDefinition, ForeignKeyDefinition, BusinessColumnDefinition, ConstraintDefinition


class YamlLoader:
    """YAML読み込みクラス
    
    テーブル定義YAMLファイルの読み込み・解析機能を提供します。
    エラーハンドリングと型変換も含みます。
    """
    
    def __init__(self, logger: DatabaseToolsLogger = None):
        """初期化
        
        Args:
            logger (DatabaseToolsLogger, optional): ログ出力インスタンス
        """
        self.logger = logger or DatabaseToolsLogger()
    
    def load_yaml_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """YAMLファイルを読み込み
        
        Args:
            file_path (Path): YAMLファイルパス
            
        Returns:
            Optional[Dict[str, Any]]: 読み込み結果（失敗時はNone）
        """
        try:
            if not file_path.exists():
                self.logger.warning(f"YAMLファイルが存在しません: {file_path}")
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data is None:
                self.logger.warning(f"YAMLファイルが空です: {file_path}")
                return {}
            
            return data
            
        except yaml.YAMLError as e:
            self.logger.error(f"YAML解析エラー ({file_path}): {e}")
            return None
        except Exception as e:
            self.logger.error(f"ファイル読み込みエラー ({file_path}): {e}")
            return None
    
    def parse_table_definition(self, yaml_data: Dict[str, Any]) -> Optional[TableDefinition]:
        """YAML データをTableDefinitionオブジェクトに変換
        
        Args:
            yaml_data (Dict[str, Any]): YAMLデータ
            
        Returns:
            Optional[TableDefinition]: テーブル定義オブジェクト（失敗時はNone）
        """
        try:
            # 必須フィールドチェック
            if 'table_name' not in yaml_data:
                self.logger.error("table_nameが定義されていません")
                return None
            
            if 'logical_name' not in yaml_data:
                self.logger.error("logical_nameが定義されていません")
                return None
            
            # 基本情報
            table_def = TableDefinition(
                name=yaml_data['table_name'],
                logical_name=yaml_data['logical_name'],
                category=yaml_data.get('category', ''),
                priority=yaml_data.get('priority', 'medium'),
                requirement_id=yaml_data.get('requirement_id', ''),
                comment=yaml_data.get('comment', yaml_data.get('overview', ''))
            )
            
            # overviewフィールドを保存
            if 'overview' in yaml_data:
                table_def.overview = yaml_data['overview']
            
            # 業務カラム定義（columnsフィールドを優先）
            if 'columns' in yaml_data:
                table_def.business_columns = self._parse_columns(yaml_data['columns'])
            elif 'business_columns' in yaml_data:
                table_def.business_columns = self._parse_columns(yaml_data['business_columns'])
            else:
                table_def.business_columns = []
            
            # インデックス定義
            if 'indexes' in yaml_data:
                table_def.business_indexes = self._parse_indexes(yaml_data['indexes'])
            elif 'business_indexes' in yaml_data:
                table_def.business_indexes = self._parse_indexes(yaml_data['business_indexes'])
            
            # 外部キー定義
            if 'foreign_keys' in yaml_data:
                table_def.foreign_keys = self._parse_foreign_keys(yaml_data['foreign_keys'])
            
            # 制約定義
            if 'constraints' in yaml_data:
                table_def.constraints = self._parse_constraints(yaml_data['constraints'])
            elif 'business_constraints' in yaml_data:
                table_def.business_constraints = self._parse_constraints(yaml_data['business_constraints'])
            
            # サンプルデータ
            if 'sample_data' in yaml_data:
                table_def.sample_data = yaml_data['sample_data']
            
            # 初期値データ
            if 'initial_data' in yaml_data:
                table_def.initial_data = yaml_data['initial_data']
            
            # その他の情報
            table_def.notes = yaml_data.get('notes', [])
            table_def.business_rules = yaml_data.get('business_rules', [])
            table_def.revision_history = yaml_data.get('revision_history', [])
            table_def.sample_data_config = yaml_data.get('sample_data_config')
            table_def.data_generation_rules = yaml_data.get('data_generation_rules')
            
            return table_def
            
        except Exception as e:
            self.logger.error(f"テーブル定義解析エラー: {e}")
            return None
    
    def _parse_columns(self, columns_data: List[Dict[str, Any]]) -> List[BusinessColumnDefinition]:
        """カラム定義を解析
        
        Args:
            columns_data (List[Dict[str, Any]]): カラム定義データ
            
        Returns:
            List[BusinessColumnDefinition]: カラム定義リスト
        """
        columns = []
        
        for col_data in columns_data:
            try:
                # データ型の処理（lengthがある場合は結合）
                data_type = col_data['type']
                if 'length' in col_data and col_data['length'] is not None:
                    if ',' in str(col_data['length']):  # DECIMAL(10,2)のような場合
                        data_type = f"{data_type}({col_data['length']})"
                    else:
                        data_type = f"{data_type}({col_data['length']})"
                
                # nullable の処理（'null'フィールドを使用）
                nullable = col_data.get('null', col_data.get('nullable', True))
                
                # コメントの処理（'logical'フィールドを優先、なければ'description'）
                comment = col_data.get('logical', col_data.get('description', col_data.get('comment', '')))
                
                column = BusinessColumnDefinition(
                    name=col_data['name'],
                    data_type=data_type,
                    nullable=nullable,
                    primary=col_data.get('primary_key', False),
                    unique=col_data.get('unique', False),
                    default=col_data.get('default'),
                    comment=comment,
                    requirement_id=col_data.get('requirement_id')
                )
                
                # ENUM値の処理
                if 'enum_values' in col_data:
                    column.enum_values = col_data['enum_values']
                columns.append(column)
                
            except KeyError as e:
                self.logger.error(f"カラム定義に必須フィールドがありません: {e}")
            except Exception as e:
                self.logger.error(f"カラム定義解析エラー: {e}")
        
        return columns
    
    def _parse_indexes(self, indexes_data: List[Dict[str, Any]]) -> List[IndexDefinition]:
        """インデックス定義を解析
        
        Args:
            indexes_data (List[Dict[str, Any]]): インデックス定義データ
            
        Returns:
            List[IndexDefinition]: インデックス定義リスト
        """
        indexes = []
        
        for idx_data in indexes_data:
            try:
                index = IndexDefinition(
                    name=idx_data['name'],
                    columns=idx_data['columns'],
                    unique=idx_data.get('unique', False),
                    comment=idx_data.get('comment', '')
                )
                indexes.append(index)
                
            except KeyError as e:
                self.logger.error(f"インデックス定義に必須フィールドがありません: {e}")
            except Exception as e:
                self.logger.error(f"インデックス定義解析エラー: {e}")
        
        return indexes
    
    def _parse_foreign_keys(self, fks_data: List[Dict[str, Any]]) -> List[ForeignKeyDefinition]:
        """外部キー定義を解析
        
        Args:
            fks_data (List[Dict[str, Any]]): 外部キー定義データ
            
        Returns:
            List[ForeignKeyDefinition]: 外部キー定義リスト
        """
        foreign_keys = []
        
        for fk_data in fks_data:
            try:
                # YAMLの構造に合わせて解析
                columns = fk_data.get('columns', [])
                references = fk_data.get('references', {})
                
                if not columns or not references:
                    self.logger.error(f"外部キー定義に必須フィールドがありません: columns または references")
                    continue
                
                # カラム名の取得（ネストした配列に対応）
                if isinstance(columns[0], list):
                    column = columns[0][0] if columns[0] else ''
                else:
                    column = columns[0] if columns else ''
                
                # 参照テーブル名の取得（ネストした配列に対応）
                reference_table_data = references.get('table', '')
                if isinstance(reference_table_data, list):
                    reference_table = reference_table_data[0] if reference_table_data else ''
                else:
                    reference_table = reference_table_data
                
                # 参照カラム名の取得
                reference_columns = references.get('columns', [])
                reference_column = reference_columns[0] if reference_columns else ''
                
                fk = ForeignKeyDefinition(
                    name=fk_data['name'],
                    columns=[column],
                    column=column,  # 旧形式との互換性
                    reference_table=reference_table,  # 旧形式との互換性
                    reference_column=reference_column,  # 旧形式との互換性
                    references={
                        'table': reference_table,
                        'columns': [reference_column]
                    },
                    on_update=fk_data.get('on_update', 'CASCADE'),
                    on_delete=fk_data.get('on_delete', 'CASCADE'),
                    comment=fk_data.get('comment', '')
                )
                foreign_keys.append(fk)
                
            except KeyError as e:
                self.logger.error(f"外部キー定義に必須フィールドがありません: {e}")
            except Exception as e:
                self.logger.error(f"外部キー定義解析エラー: {e}")
        
        return foreign_keys
    
    def _parse_constraints(self, constraints_data: List[Dict[str, Any]]) -> List[ConstraintDefinition]:
        """制約定義を解析
        
        Args:
            constraints_data (List[Dict[str, Any]]): 制約定義データ
            
        Returns:
            List[ConstraintDefinition]: 制約定義リスト
        """
        constraints = []
        
        for const_data in constraints_data:
            try:
                constraint = ConstraintDefinition(
                    name=const_data['name'],
                    type=const_data['type'],
                    columns=const_data.get('columns', []),
                    condition=const_data.get('condition', ''),
                    comment=const_data.get('comment', const_data.get('description', ''))
                )
                constraints.append(constraint)
                
            except KeyError as e:
                self.logger.error(f"制約定義に必須フィールドがありません: {e}")
            except Exception as e:
                self.logger.error(f"制約定義解析エラー: {e}")
        
        return constraints
    
    def validate_yaml_structure(self, yaml_data: Dict[str, Any]) -> bool:
        """YAML構造の妥当性をチェック
        
        Args:
            yaml_data (Dict[str, Any]): YAMLデータ
            
        Returns:
            bool: 妥当性チェック結果
        """
        try:
            # 必須フィールドチェック
            required_fields = ['table_name', 'logical_name']
            for field in required_fields:
                if field not in yaml_data:
                    self.logger.error(f"必須フィールドが不足: {field}")
                    return False
            
            # カラム定義チェック
            if 'business_columns' in yaml_data:
                if not isinstance(yaml_data['business_columns'], list):
                    self.logger.error("business_columnsはリスト形式である必要があります")
                    return False
                
                for i, col in enumerate(yaml_data['business_columns']):
                    if not isinstance(col, dict):
                        self.logger.error(f"カラム定義{i}は辞書形式である必要があります")
                        return False
                    
                    required_col_fields = ['name', 'type']
                    for field in required_col_fields:
                        if field not in col:
                            self.logger.error(f"カラム定義{i}に必須フィールドが不足: {field}")
                            return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"YAML構造チェックエラー: {e}")
            return False
    
    def get_table_list_from_markdown(self, md_file_path: Path) -> Dict[str, Dict[str, Any]]:
        """テーブル一覧.mdからテーブル情報を読み込み
        
        Args:
            md_file_path (Path): テーブル一覧.mdファイルパス
            
        Returns:
            Dict[str, Dict[str, Any]]: テーブル情報辞書
        """
        try:
            if not md_file_path.exists():
                self.logger.error(f"テーブル一覧ファイルが見つかりません: {md_file_path}")
                return {}
            
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tables = {}
            lines = content.split('\n')
            in_table = False
            
            for line in lines:
                # テーブルヘッダーを検出
                if '| テーブルID |' in line and 'テーブル名' in line:
                    in_table = True
                    continue
                
                # テーブル区切り行をスキップ
                if in_table and line.startswith('|---'):
                    continue
                
                # テーブル終了を検出
                if in_table and (line.strip() == '' or not line.startswith('|')):
                    in_table = False
                    continue
                
                # テーブル行を解析
                if in_table and line.startswith('| TBL-'):
                    parts = [part.strip() for part in line.split('|')]
                    if len(parts) >= 5:
                        table_id = parts[1]
                        category = parts[2]
                        table_name = parts[3]
                        logical_name = parts[4]
                        
                        tables[table_name] = {
                            'table_id': table_id,
                            'category': category,
                            'logical_name': logical_name,
                            'table_name': table_name
                        }
            
            return tables
            
        except Exception as e:
            self.logger.error(f"テーブル一覧読み込みエラー: {e}")
            return {}
