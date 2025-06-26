"""
YAML統一パーサー

YAMLファイルの解析と検証を行う
"""

import yaml
from typing import Dict, Any, List
from pathlib import Path

from .base_parser import BaseParser
from ..core import ValidationResult, ParseError, YamlUtils


class YamlParser(BaseParser):
    """YAML専用パーサー"""
    
    def __init__(self):
        super().__init__("yaml")
        self.required_sections = [
            'revision_history',
            'overview', 
            'notes',
            'rules'
        ]
    
    def get_supported_extensions(self) -> List[str]:
        """サポートする拡張子"""
        return ['.yaml', '.yml']
    
    def parse(self, file_path: str) -> Dict[str, Any]:
        """
        YAMLファイルを解析
        
        Args:
            file_path: YAMLファイルパス
            
        Returns:
            解析されたデータ
            
        Raises:
            ParseError: 解析エラー
        """
        self._validate_file_exists(file_path)
        self._validate_file_readable(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if data is None:
                raise ParseError(f"YAMLファイルが空です: {file_path}", file_path)
            
            if not isinstance(data, dict):
                raise ParseError(f"YAMLファイルのルートは辞書である必要があります: {file_path}", file_path)
            
            self.logger.debug(f"YAML解析完了: {file_path}")
            return data
            
        except yaml.YAMLError as e:
            raise ParseError(f"YAML解析エラー: {str(e)}", file_path)
        except Exception as e:
            raise ParseError(f"ファイル読み込みエラー: {str(e)}", file_path)
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """
        YAMLデータの妥当性を検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            検証結果
        """
        result = ValidationResult(is_valid=True)
        
        # 必須セクションの存在チェック
        for section in self.required_sections:
            if section not in data:
                result.add_error(f"必須セクション '{section}' が存在しません")
        
        # 各セクションの詳細検証
        self._validate_revision_history(data, result)
        self._validate_overview(data, result)
        self._validate_notes(data, result)
        self._validate_rules(data, result)
        self._validate_columns(data, result)
        
        return result
    
    def _validate_revision_history(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """改版履歴の検証"""
        if 'revision_history' not in data:
            return
        
        history = data['revision_history']
        if not isinstance(history, list):
            result.add_error("revision_history はリスト形式である必要があります")
            return
        
        if len(history) == 0:
            result.add_error("revision_history は最低1エントリ必要です")
            return
        
        for i, entry in enumerate(history):
            if not isinstance(entry, dict):
                result.add_error(f"revision_history[{i}] は辞書形式である必要があります")
                continue
            
            required_fields = ['version', 'date', 'author', 'changes']
            for field in required_fields:
                if field not in entry:
                    result.add_error(f"revision_history[{i}] に必須フィールド '{field}' がありません")
    
    def _validate_overview(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """概要の検証"""
        if 'overview' not in data:
            return
        
        overview = data['overview']
        if not isinstance(overview, str):
            result.add_error("overview は文字列である必要があります")
            return
        
        if len(overview.strip()) < 50:
            result.add_error(f"overview は最低50文字以上必要です (現在: {len(overview.strip())}文字)")
    
    def _validate_notes(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """特記事項の検証"""
        if 'notes' not in data:
            return
        
        notes = data['notes']
        if not isinstance(notes, list):
            result.add_error("notes はリスト形式である必要があります")
            return
        
        if len(notes) < 3:
            result.add_error(f"notes は最低3項目必要です (現在: {len(notes)}項目)")
    
    def _validate_rules(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """業務ルールの検証"""
        if 'rules' not in data:
            return
        
        rules = data['rules']
        if not isinstance(rules, list):
            result.add_error("rules はリスト形式である必要があります")
            return
        
        if len(rules) < 3:
            result.add_error(f"rules は最低3項目必要です (現在: {len(rules)}項目)")
    
    def _validate_columns(self, data: Dict[str, Any], result: ValidationResult) -> None:
        """カラム定義の検証"""
        if 'columns' not in data:
            return
        
        columns = data['columns']
        if not isinstance(columns, list):
            result.add_error("columns はリスト形式である必要があります")
            return
        
        if len(columns) == 0:
            result.add_error("columns は最低1つのカラム定義が必要です")
            return
        
        for i, column in enumerate(columns):
            if not isinstance(column, dict):
                result.add_error(f"columns[{i}] は辞書形式である必要があります")
                continue
            
            required_fields = ['name', 'type', 'nullable', 'comment']
            for field in required_fields:
                if field not in column:
                    result.add_error(f"columns[{i}] に必須フィールド '{field}' がありません")
    
    def validate_table_definition(self, file_path: str) -> ValidationResult:
        """
        テーブル定義YAMLの包括的検証
        
        Args:
            file_path: YAMLファイルパス
            
        Returns:
            検証結果
        """
        try:
            data = self.parse(file_path)
            result = self.validate(data)
            result.file_path = file_path
            return result
        except ParseError as e:
            result = ValidationResult(is_valid=False, file_path=file_path)
            result.add_error(str(e))
            return result
    
    def extract_table_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        テーブル情報を抽出
        
        Args:
            data: YAMLデータ
            
        Returns:
            テーブル情報
        """
        return {
            'table_name': data.get('table_name', ''),
            'logical_name': data.get('logical_name', ''),
            'category': data.get('category', ''),
            'priority': data.get('priority', ''),
            'requirement_id': data.get('requirement_id', ''),
            'comment': data.get('comment', ''),
            'column_count': len(data.get('columns', [])),
            'index_count': len(data.get('indexes', [])),
            'foreign_key_count': len(data.get('foreign_keys', []))
        }
    
    def get_validation_summary(self, file_path: str) -> Dict[str, Any]:
        """
        検証結果のサマリーを取得
        
        Args:
            file_path: YAMLファイルパス
            
        Returns:
            検証サマリー
        """
        result = self.validate_table_definition(file_path)
        
        summary = {
            'file_path': file_path,
            'is_valid': result.is_valid,
            'error_count': len(result.errors),
            'warning_count': len(result.warnings),
            'errors': result.errors,
            'warnings': result.warnings
        }
        
        if result.is_valid:
            try:
                data = self.parse(file_path)
                summary['table_info'] = self.extract_table_info(data)
            except:
                pass
        
        return summary
