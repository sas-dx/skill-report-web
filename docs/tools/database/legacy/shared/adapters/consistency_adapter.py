"""
整合性チェックアダプター

データベース整合性チェック機能のアダプターです。
各種データソース間の整合性検証を提供します。
"""

from typing import Dict, List, Any, Optional, Tuple
from .base_adapter import BaseAdapter
from ..core.exceptions import ValidationError, ConversionError


class ConsistencyCheckAdapter(BaseAdapter):
    """整合性チェックアダプター"""
    
    def __init__(self, config):
        """
        整合性チェックアダプターを初期化
        
        Args:
            config: データベースツール設定
        """
        super().__init__(config)
        self.check_results = []
    
    def validate_input(self, data: Any) -> bool:
        """
        整合性チェック対象データの検証
        
        Args:
            data: 検証対象データ
            
        Returns:
            bool: 検証結果
            
        Raises:
            ValidationError: 検証エラー時
        """
        try:
            if not isinstance(data, dict):
                raise ValidationError("Consistency check data must be a dictionary")
            
            # 必須フィールドの確認
            required_fields = ['tables', 'check_types']
            for field in required_fields:
                if field not in data:
                    raise ValidationError(f"Required field '{field}' is missing")
            
            # テーブルデータの検証
            tables = data.get('tables', {})
            if not isinstance(tables, dict):
                raise ValidationError("tables must be a dictionary")
            
            # チェックタイプの検証
            check_types = data.get('check_types', [])
            if not isinstance(check_types, list):
                raise ValidationError("check_types must be a list")
            
            self.log_operation("validate_input", {
                "table_count": len(tables),
                "check_types": check_types
            })
            return True
            
        except Exception as e:
            self.handle_error(e, "consistency check data validation")
    
    def transform_data(self, data: Any) -> Dict[str, Any]:
        """
        整合性チェックデータの変換
        
        Args:
            data: 変換対象データ
            
        Returns:
            Dict[str, Any]: 正規化された整合性チェックデータ
            
        Raises:
            ConversionError: 変換エラー時
        """
        try:
            if not self.validate_input(data):
                raise ConversionError("Invalid input data")
            
            # データの正規化
            normalized_data = {
                'tables': self._normalize_table_data(data['tables']),
                'check_types': data.get('check_types', []),
                'options': data.get('options', {}),
                'metadata': {
                    'timestamp': data.get('timestamp'),
                    'source': data.get('source', 'unknown')
                }
            }
            
            self.log_operation("transform_data", {
                "table_count": len(normalized_data['tables']),
                "check_types": normalized_data['check_types']
            })
            return normalized_data
            
        except Exception as e:
            self.handle_error(e, "consistency check data transformation")
    
    def _normalize_table_data(self, tables: Dict[str, Any]) -> Dict[str, Any]:
        """
        テーブルデータの正規化
        
        Args:
            tables: テーブルデータ
            
        Returns:
            Dict[str, Any]: 正規化されたテーブルデータ
        """
        normalized_tables = {}
        
        for table_name, table_data in tables.items():
            normalized_tables[table_name] = {
                'yaml_definition': table_data.get('yaml_definition'),
                'ddl_definition': table_data.get('ddl_definition'),
                'markdown_definition': table_data.get('markdown_definition'),
                'metadata': {
                    'last_modified': table_data.get('last_modified'),
                    'source_files': table_data.get('source_files', [])
                }
            }
        
        return normalized_tables
    
    def check_table_existence_consistency(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        テーブル存在整合性チェック
        
        Args:
            data: 整合性チェックデータ
            
        Returns:
            List[Dict[str, Any]]: チェック結果リスト
        """
        try:
            results = []
            tables = data.get('tables', {})
            
            for table_name, table_data in tables.items():
                result = {
                    'table_name': table_name,
                    'check_type': 'table_existence',
                    'status': 'success',
                    'issues': []
                }
                
                # YAML定義の存在チェック
                if not table_data.get('yaml_definition'):
                    result['issues'].append({
                        'severity': 'error',
                        'message': f"YAML definition missing for table {table_name}"
                    })
                    result['status'] = 'error'
                
                # DDL定義の存在チェック
                if not table_data.get('ddl_definition'):
                    result['issues'].append({
                        'severity': 'warning',
                        'message': f"DDL definition missing for table {table_name}"
                    })
                    if result['status'] != 'error':
                        result['status'] = 'warning'
                
                # Markdown定義の存在チェック
                if not table_data.get('markdown_definition'):
                    result['issues'].append({
                        'severity': 'info',
                        'message': f"Markdown definition missing for table {table_name}"
                    })
                    if result['status'] == 'success':
                        result['status'] = 'info'
                
                results.append(result)
            
            self.log_operation("check_table_existence_consistency", {
                "checked_tables": len(tables),
                "issues_found": sum(len(r['issues']) for r in results)
            })
            
            return results
            
        except Exception as e:
            self.handle_error(e, "table existence consistency check")
    
    def check_column_definition_consistency(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        カラム定義整合性チェック
        
        Args:
            data: 整合性チェックデータ
            
        Returns:
            List[Dict[str, Any]]: チェック結果リスト
        """
        try:
            results = []
            tables = data.get('tables', {})
            
            for table_name, table_data in tables.items():
                result = {
                    'table_name': table_name,
                    'check_type': 'column_definition',
                    'status': 'success',
                    'issues': []
                }
                
                yaml_def = table_data.get('yaml_definition')
                ddl_def = table_data.get('ddl_definition')
                
                if yaml_def and ddl_def:
                    # カラム定義の比較
                    yaml_columns = self._extract_columns_from_yaml(yaml_def)
                    ddl_columns = self._extract_columns_from_ddl(ddl_def)
                    
                    # カラム数の比較
                    if len(yaml_columns) != len(ddl_columns):
                        result['issues'].append({
                            'severity': 'error',
                            'message': f"Column count mismatch: YAML({len(yaml_columns)}) vs DDL({len(ddl_columns)})"
                        })
                        result['status'] = 'error'
                    
                    # 個別カラムの比較
                    for yaml_col in yaml_columns:
                        ddl_col = next((c for c in ddl_columns if c['name'] == yaml_col['name']), None)
                        if not ddl_col:
                            result['issues'].append({
                                'severity': 'error',
                                'message': f"Column '{yaml_col['name']}' exists in YAML but not in DDL"
                            })
                            result['status'] = 'error'
                        else:
                            # データ型の比較
                            if yaml_col['type'] != ddl_col['type']:
                                result['issues'].append({
                                    'severity': 'warning',
                                    'message': f"Column '{yaml_col['name']}' type mismatch: YAML({yaml_col['type']}) vs DDL({ddl_col['type']})"
                                })
                                if result['status'] == 'success':
                                    result['status'] = 'warning'
                
                results.append(result)
            
            self.log_operation("check_column_definition_consistency", {
                "checked_tables": len(tables),
                "issues_found": sum(len(r['issues']) for r in results)
            })
            
            return results
            
        except Exception as e:
            self.handle_error(e, "column definition consistency check")
    
    def _extract_columns_from_yaml(self, yaml_definition: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        YAML定義からカラム情報を抽出
        
        Args:
            yaml_definition: YAML定義データ
            
        Returns:
            List[Dict[str, Any]]: カラム情報リスト
        """
        return yaml_definition.get('columns', [])
    
    def _extract_columns_from_ddl(self, ddl_definition: str) -> List[Dict[str, Any]]:
        """
        DDL定義からカラム情報を抽出
        
        Args:
            ddl_definition: DDL文字列
            
        Returns:
            List[Dict[str, Any]]: カラム情報リスト
        """
        # 簡易的な実装（実際にはDDLParserを使用）
        columns = []
        # DDL解析ロジックの実装が必要
        return columns
    
    def generate_consistency_report(self, check_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        整合性チェック結果レポートの生成
        
        Args:
            check_results: チェック結果リスト
            
        Returns:
            Dict[str, Any]: 整合性レポート
        """
        try:
            total_checks = len(check_results)
            error_count = sum(1 for r in check_results if r['status'] == 'error')
            warning_count = sum(1 for r in check_results if r['status'] == 'warning')
            success_count = sum(1 for r in check_results if r['status'] == 'success')
            
            report = {
                'summary': {
                    'total_checks': total_checks,
                    'success_count': success_count,
                    'warning_count': warning_count,
                    'error_count': error_count,
                    'success_rate': (success_count / total_checks * 100) if total_checks > 0 else 0
                },
                'details': check_results,
                'recommendations': self._generate_recommendations(check_results)
            }
            
            self.log_operation("generate_consistency_report", {
                "total_checks": total_checks,
                "error_count": error_count,
                "warning_count": warning_count
            })
            
            return report
            
        except Exception as e:
            self.handle_error(e, "consistency report generation")
    
    def _generate_recommendations(self, check_results: List[Dict[str, Any]]) -> List[str]:
        """
        改善提案の生成
        
        Args:
            check_results: チェック結果リスト
            
        Returns:
            List[str]: 改善提案リスト
        """
        recommendations = []
        
        error_count = sum(1 for r in check_results if r['status'] == 'error')
        warning_count = sum(1 for r in check_results if r['status'] == 'warning')
        
        if error_count > 0:
            recommendations.append(f"{error_count}件の重大な整合性エラーがあります。優先的に修正してください。")
        
        if warning_count > 0:
            recommendations.append(f"{warning_count}件の警告があります。可能な限り修正することを推奨します。")
        
        if error_count == 0 and warning_count == 0:
            recommendations.append("整合性チェックに合格しています。良好な状態です。")
        
        return recommendations
