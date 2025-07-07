"""
YAML解析機能 - テーブル詳細定義の解析
"""
import yaml
import logging
from typing import List, Dict, Optional, Any
from pathlib import Path

from core.models import (
    ColumnDefinition, IndexDefinition, ForeignKeyDefinition,
    ConstraintDefinition, TableDefinition
)


class YAMLParser:
    """基本YAML解析クラス（既存機能との互換性維持）"""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def parse_yaml_file(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """YAMLファイルの基本解析（既存機能）"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"YAMLファイル解析エラー: {file_path} - {e}")
            return None


class EnhancedYAMLParser(YAMLParser):
    """拡張YAML解析クラス - データ型整合性チェック用"""
    
    def __init__(self, logger: logging.Logger):
        super().__init__(logger)
        self.data_type_mapping = self._init_data_type_mapping()
    
    def _init_data_type_mapping(self) -> Dict[str, str]:
        """YAML型からSQL型へのマッピング"""
        return {
            # 文字列型
            'VARCHAR': 'VARCHAR',
            'CHAR': 'CHAR',
            'TEXT': 'TEXT',
            'LONGTEXT': 'LONGTEXT',
            'MEDIUMTEXT': 'MEDIUMTEXT',
            'TINYTEXT': 'TINYTEXT',
            
            # 数値型
            'INTEGER': 'INT',
            'INT': 'INT',
            'BIGINT': 'BIGINT',
            'TINYINT': 'TINYINT',
            'SMALLINT': 'SMALLINT',
            'MEDIUMINT': 'MEDIUMINT',
            'DECIMAL': 'DECIMAL',
            'FLOAT': 'FLOAT',
            'DOUBLE': 'DOUBLE',
            
            # 日付時刻型
            'DATE': 'DATE',
            'DATETIME': 'DATETIME',
            'TIMESTAMP': 'TIMESTAMP',
            'TIME': 'TIME',
            'YEAR': 'YEAR',
            
            # その他
            'BOOLEAN': 'BOOLEAN',
            'BOOL': 'BOOLEAN',
            'ENUM': 'ENUM',
            'SET': 'SET',
            'JSON': 'JSON',
            
            # バイナリ型
            'BLOB': 'BLOB',
            'LONGBLOB': 'LONGBLOB',
            'MEDIUMBLOB': 'MEDIUMBLOB',
            'TINYBLOB': 'TINYBLOB',
        }
    
    def parse_table_definition(self, file_path: Path) -> Optional[TableDefinition]:
        """テーブル定義の詳細解析"""
        try:
            yaml_data = self.parse_yaml_file(file_path)
            if not yaml_data:
                return None
            
            # TableDefinitionオブジェクトを作成
            table_def = TableDefinition(
                table_name=yaml_data.get('table_name', ''),
                logical_name=yaml_data.get('logical_name', ''),
                category=yaml_data.get('category', ''),
                overview=yaml_data.get('overview', '')
            )
            
            # カラム定義を解析
            if 'business_columns' in yaml_data:
                table_def.columns = self._parse_business_columns(yaml_data['business_columns'])
            
            # インデックス定義を解析
            if 'business_indexes' in yaml_data:
                table_def.indexes = self._parse_business_indexes(yaml_data['business_indexes'])
            
            # 外部キー定義を解析
            if 'foreign_keys' in yaml_data:
                table_def.foreign_keys = self._parse_foreign_keys(yaml_data['foreign_keys'])
            
            # 制約定義を解析
            if 'business_constraints' in yaml_data:
                table_def.constraints = self._parse_business_constraints(yaml_data['business_constraints'])
            
            # サンプルデータを解析
            if 'sample_data' in yaml_data:
                table_def.sample_data = yaml_data['sample_data']
            
            # 特記事項を解析
            if 'notes' in yaml_data:
                table_def.notes = yaml_data['notes']
            
            # 業務ルールを解析
            if 'business_rules' in yaml_data:
                table_def.business_rules = yaml_data['business_rules']
            
            return table_def
            
        except Exception as e:
            self.logger.error(f"テーブル定義解析エラー: {file_path} - {e}")
            return None
    
    def _parse_business_columns(self, columns_data: List[Dict[str, Any]]) -> List[ColumnDefinition]:
        """business_columnsの解析"""
        columns = []
        
        for col_data in columns_data:
            try:
                column = ColumnDefinition(
                    name=col_data.get('name', ''),
                    logical_name=col_data.get('logical', ''),
                    comment=col_data.get('description', '')
                )
                
                # データ型を正規化
                raw_type = col_data.get('type', '').upper()
                column.data_type = self.normalize_data_type(raw_type)
                
                # 長さ制約
                if 'length' in col_data and col_data['length'] is not None:
                    column.length = col_data['length']
                
                # NULL制約
                column.nullable = col_data.get('null', True)
                
                # UNIQUE制約
                column.unique = col_data.get('unique', False)
                
                # 暗号化フラグ
                column.encrypted = col_data.get('encrypted', False)
                
                # ENUM値
                if 'enum_values' in col_data:
                    column.enum_values = col_data['enum_values']
                
                # デフォルト値
                if 'default' in col_data:
                    column.default_value = str(col_data['default'])
                
                columns.append(column)
                
            except Exception as e:
                self.logger.error(f"カラム定義解析エラー: {col_data} - {e}")
                continue
        
        return columns
    
    def _parse_business_indexes(self, indexes_data: List[Dict[str, Any]]) -> List[IndexDefinition]:
        """business_indexesの解析"""
        indexes = []
        
        for idx_data in indexes_data:
            try:
                index = IndexDefinition(
                    name=idx_data.get('name', ''),
                    columns=idx_data.get('columns', []),
                    unique=idx_data.get('unique', False),
                    description=idx_data.get('description', '')
                )
                indexes.append(index)
                
            except Exception as e:
                self.logger.error(f"インデックス定義解析エラー: {idx_data} - {e}")
                continue
        
        return indexes
    
    def _parse_foreign_keys(self, fk_data: List[Dict[str, Any]]) -> List[ForeignKeyDefinition]:
        """foreign_keysの解析"""
        foreign_keys = []
        
        for fk in fk_data:
            try:
                foreign_key = ForeignKeyDefinition(
                    name=fk.get('name', ''),
                    column=fk.get('column', ''),
                    reference_table=fk.get('reference_table', ''),
                    reference_column=fk.get('reference_column', ''),
                    on_update=fk.get('on_update', 'CASCADE'),
                    on_delete=fk.get('on_delete', 'RESTRICT'),
                    description=fk.get('description', '')
                )
                foreign_keys.append(foreign_key)
                
            except Exception as e:
                self.logger.error(f"外部キー定義解析エラー: {fk} - {e}")
                continue
        
        return foreign_keys
    
    def _parse_business_constraints(self, constraints_data: List[Dict[str, Any]]) -> List[ConstraintDefinition]:
        """business_constraintsの解析"""
        constraints = []
        
        for const_data in constraints_data:
            try:
                constraint = ConstraintDefinition(
                    name=const_data.get('name', ''),
                    type=const_data.get('type', ''),
                    columns=const_data.get('columns', []),
                    condition=const_data.get('condition', ''),
                    description=const_data.get('description', '')
                )
                constraints.append(constraint)
                
            except Exception as e:
                self.logger.error(f"制約定義解析エラー: {const_data} - {e}")
                continue
        
        return constraints
    
    def normalize_data_type(self, yaml_type: str) -> str:
        """YAML型からSQL型への正規化"""
        if not yaml_type:
            return ''
        
        # 基本的なマッピング
        base_type = yaml_type.upper()
        if base_type in self.data_type_mapping:
            return self.data_type_mapping[base_type]
        
        # 複合型の処理（例: VARCHAR(50) -> VARCHAR）
        for yaml_key, sql_type in self.data_type_mapping.items():
            if base_type.startswith(yaml_key):
                return sql_type
        
        # マッピングにない場合はそのまま返す
        return base_type
    
    def extract_data_type_details(self, column_data: Dict[str, Any]) -> Dict[str, Any]:
        """データ型の詳細情報を抽出"""
        details = {}
        
        raw_type = column_data.get('type', '').upper()
        details['base_type'] = self.normalize_data_type(raw_type)
        
        # 長さ制約
        if 'length' in column_data and column_data['length'] is not None:
            details['length'] = column_data['length']
        
        # ENUM値
        if 'enum_values' in column_data:
            details['enum_values'] = column_data['enum_values']
        
        # 精度・スケール（DECIMAL型など）
        if 'precision' in column_data:
            details['precision'] = column_data['precision']
        if 'scale' in column_data:
            details['scale'] = column_data['scale']
        
        return details
    
    def compare_column_types(self, yaml_column: Dict[str, Any], ddl_type_info: Dict[str, Any]) -> Dict[str, Any]:
        """YAMLとDDLのカラム型比較"""
        comparison = {
            'type_match': False,
            'length_match': True,
            'enum_match': True,
            'issues': []
        }
        
        yaml_details = self.extract_data_type_details(yaml_column)
        
        # 基本データ型の比較
        yaml_type = yaml_details.get('base_type', '').upper()
        ddl_type = ddl_type_info.get('type', '').upper()
        
        if yaml_type == ddl_type:
            comparison['type_match'] = True
        else:
            comparison['issues'].append(f"データ型不一致: YAML={yaml_type}, DDL={ddl_type}")
        
        # 長さ制約の比較
        yaml_length = yaml_details.get('length')
        ddl_length = ddl_type_info.get('length')
        
        if yaml_length is not None and ddl_length is not None:
            if yaml_length != ddl_length:
                comparison['length_match'] = False
                comparison['issues'].append(f"長さ不一致: YAML={yaml_length}, DDL={ddl_length}")
        elif yaml_length is not None or ddl_length is not None:
            comparison['length_match'] = False
            comparison['issues'].append(f"長さ定義不一致: YAML={yaml_length}, DDL={ddl_length}")
        
        # ENUM値の比較
        yaml_enum = yaml_details.get('enum_values', [])
        ddl_enum = ddl_type_info.get('enum_values', [])
        
        if yaml_enum or ddl_enum:
            if set(yaml_enum) != set(ddl_enum):
                comparison['enum_match'] = False
                comparison['issues'].append(f"ENUM値不一致: YAML={yaml_enum}, DDL={ddl_enum}")
        
        return comparison
    
    def validate_yaml_structure(self, yaml_data: Dict[str, Any]) -> List[str]:
        """YAML構造の妥当性検証"""
        issues = []
        
        # 必須フィールドのチェック
        required_fields = ['table_name', 'logical_name', 'category']
        for field in required_fields:
            if field not in yaml_data or not yaml_data[field]:
                issues.append(f"必須フィールドが不足: {field}")
        
        # business_columnsの検証
        if 'business_columns' in yaml_data:
            columns = yaml_data['business_columns']
            if not isinstance(columns, list):
                issues.append("business_columnsはリスト形式である必要があります")
            else:
                for i, col in enumerate(columns):
                    if not isinstance(col, dict):
                        issues.append(f"カラム定義{i}は辞書形式である必要があります")
                        continue
                    
                    # カラムの必須フィールド
                    col_required = ['name', 'type']
                    for field in col_required:
                        if field not in col or not col[field]:
                            issues.append(f"カラム{col.get('name', i)}の必須フィールドが不足: {field}")
        
        # foreign_keysの検証
        if 'foreign_keys' in yaml_data:
            fks = yaml_data['foreign_keys']
            if not isinstance(fks, list):
                issues.append("foreign_keysはリスト形式である必要があります")
            else:
                for i, fk in enumerate(fks):
                    if not isinstance(fk, dict):
                        issues.append(f"外部キー定義{i}は辞書形式である必要があります")
                        continue
                    
                    # 外部キーの必須フィールド
                    fk_required = ['name', 'column', 'reference_table', 'reference_column']
                    for field in fk_required:
                        if field not in fk or not fk[field]:
                            issues.append(f"外部キー{fk.get('name', i)}の必須フィールドが不足: {field}")
        
        return issues
