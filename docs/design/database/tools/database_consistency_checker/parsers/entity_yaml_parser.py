"""
データベース整合性チェックツール - entity_relationships.yaml解析
"""
import yaml
from pathlib import Path
from typing import List, Dict, Optional, Any
from shared.core.models import EntityRelationship, TableDefinition, ColumnDefinition
from database_consistency_checker.core.logger import ConsistencyLogger


class EntityYamlParser:
    """entity_relationships.yamlファイルの解析"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        """
        パーサー初期化
        
        Args:
            logger: ログ機能
        """
        self.logger = logger or ConsistencyLogger()
    
    def parse_file(self, file_path: Path) -> Dict[str, Any]:
        """
        entity_relationships.yamlファイルを解析
        
        Args:
            file_path: ファイルパス
            
        Returns:
            解析結果辞書
        """
        if not file_path.exists():
            self.logger.error(f"エンティティ関連ファイルが見つかりません: {file_path}")
            return {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                self.logger.error("エンティティ関連ファイルが空です")
                return {}
            
            self.logger.info(f"エンティティ関連ファイルを解析しました: {file_path}")
            return data
            
        except yaml.YAMLError as e:
            self.logger.error(f"YAML解析エラー: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"エンティティ関連ファイルの読み込みエラー: {e}")
            return {}
    
    def get_entities(self, data: Dict[str, Any]) -> Dict[str, TableDefinition]:
        """
        エンティティ定義を取得
        
        Args:
            data: 解析済みYAMLデータ
            
        Returns:
            エンティティ定義辞書
        """
        entities = {}
        
        if 'entities' not in data:
            self.logger.warning("エンティティ定義が見つかりません")
            return entities
        
        for entity_name, entity_data in data['entities'].items():
            try:
                entity = self._parse_entity(entity_name, entity_data)
                entities[entity_name] = entity
            except Exception as e:
                self.logger.warning(f"エンティティ解析エラー [{entity_name}]: {e}")
                continue
        
        self.logger.info(f"{len(entities)} 個のエンティティを解析しました")
        return entities
    
    def get_relationships(self, data: Dict[str, Any]) -> List[EntityRelationship]:
        """
        関連定義を取得
        
        Args:
            data: 解析済みYAMLデータ
            
        Returns:
            関連定義のリスト
        """
        relationships = []
        
        if 'relationships' not in data:
            self.logger.warning("関連定義が見つかりません")
            return relationships
        
        for rel_data in data['relationships']:
            try:
                relationship = self._parse_relationship(rel_data)
                relationships.append(relationship)
            except Exception as e:
                self.logger.warning(f"関連定義解析エラー: {e}")
                continue
        
        self.logger.info(f"{len(relationships)} 個の関連を解析しました")
        return relationships
    
    def _parse_entity(self, entity_name: str, entity_data: Dict[str, Any]) -> TableDefinition:
        """
        エンティティ定義を解析
        
        Args:
            entity_name: エンティティ名
            entity_data: エンティティデータ
            
        Returns:
            テーブル定義
        """
        logical_name = entity_data.get('logical_name', '')
        category = entity_data.get('category', '')
        primary_key = entity_data.get('primary_key', 'id')
        
        # カラム定義の解析
        columns = []
        key_columns = entity_data.get('key_columns', [])
        
        for col_data in key_columns:
            column = self._parse_column(col_data)
            columns.append(column)
        
        return TableDefinition(
            table_name=entity_name,
            logical_name=logical_name,
            category=category,
            columns=columns
        )
    
    def _parse_column(self, col_data: Dict[str, Any]) -> ColumnDefinition:
        """
        カラム定義を解析
        
        Args:
            col_data: カラムデータ
            
        Returns:
            カラム定義
        """
        name = col_data.get('name', '')
        logical_name = col_data.get('logical', '')
        data_type = col_data.get('type', '')
        is_pk = col_data.get('is_pk', False)
        is_fk = col_data.get('is_fk', False)
        
        return ColumnDefinition(
            name=name,
            logical_name=logical_name,
            data_type=data_type,
            primary_key=is_pk,
            foreign_key=is_fk,
            nullable=not is_pk  # 主キーは非NULL
        )
    
    def _parse_relationship(self, rel_data: Dict[str, Any]) -> EntityRelationship:
        """
        関連定義を解析
        
        Args:
            rel_data: 関連データ
            
        Returns:
            関連定義
        """
        source = rel_data.get('source', '')
        target = rel_data.get('target', '')
        rel_type = rel_data.get('type', '')
        cardinality = rel_data.get('cardinality', '')
        foreign_key = rel_data.get('foreign_key', '')
        description = rel_data.get('description', '')
        
        return EntityRelationship(
            source=source,
            target=target,
            type=rel_type,
            cardinality=cardinality,
            foreign_key=foreign_key,
            description=description
        )
    
    def get_entity_names(self, data: Dict[str, Any]) -> List[str]:
        """
        エンティティ名のリストを取得
        
        Args:
            data: 解析済みYAMLデータ
            
        Returns:
            エンティティ名のリスト
        """
        if 'entities' not in data:
            return []
        
        return list(data['entities'].keys())
    
    def get_foreign_key_relationships(self, relationships: List[EntityRelationship]) -> Dict[str, List[str]]:
        """
        外部キー関係を取得
        
        Args:
            relationships: 関連定義のリスト
            
        Returns:
            テーブル名をキーとした参照先テーブルのリスト
        """
        fk_relationships = {}
        
        for rel in relationships:
            if rel.foreign_key and rel.source and rel.target:
                if rel.source not in fk_relationships:
                    fk_relationships[rel.source] = []
                fk_relationships[rel.source].append(rel.target)
        
        return fk_relationships
    
    def get_referenced_tables(self, relationships: List[EntityRelationship]) -> Dict[str, List[str]]:
        """
        参照されるテーブルを取得
        
        Args:
            relationships: 関連定義のリスト
            
        Returns:
            テーブル名をキーとした参照元テーブルのリスト
        """
        referenced_tables = {}
        
        for rel in relationships:
            if rel.foreign_key and rel.source and rel.target:
                if rel.target not in referenced_tables:
                    referenced_tables[rel.target] = []
                referenced_tables[rel.target].append(rel.source)
        
        return referenced_tables
    
    def validate_entity_structure(self, data: Dict[str, Any]) -> List[str]:
        """
        エンティティ構造の妥当性チェック
        
        Args:
            data: 解析済みYAMLデータ
            
        Returns:
            エラーメッセージのリスト
        """
        errors = []
        
        # 必須セクションの確認
        required_sections = ['metadata', 'entities', 'relationships']
        for section in required_sections:
            if section not in data:
                errors.append(f"必須セクション '{section}' が見つかりません")
        
        # エンティティの妥当性チェック
        if 'entities' in data:
            for entity_name, entity_data in data['entities'].items():
                if not isinstance(entity_data, dict):
                    errors.append(f"エンティティ '{entity_name}' の定義が不正です")
                    continue
                
                # 必須フィールドの確認
                required_fields = ['logical_name', 'category', 'primary_key']
                for field in required_fields:
                    if field not in entity_data:
                        errors.append(f"エンティティ '{entity_name}' に必須フィールド '{field}' がありません")
        
        # 関連の妥当性チェック
        if 'relationships' in data:
            entities = set(data.get('entities', {}).keys())
            
            for i, rel_data in enumerate(data['relationships']):
                if not isinstance(rel_data, dict):
                    errors.append(f"関連定義 {i+1} の形式が不正です")
                    continue
                
                source = rel_data.get('source')
                target = rel_data.get('target')
                
                if source and source not in entities:
                    errors.append(f"関連定義 {i+1}: 参照元エンティティ '{source}' が存在しません")
                
                if target and target not in entities:
                    errors.append(f"関連定義 {i+1}: 参照先エンティティ '{target}' が存在しません")
        
        return errors
