"""
YAMLフォーマット整合性チェッカー
テーブル定義詳細YAMLファイルの標準テンプレート準拠確認
"""
import os
import yaml
from typing import Dict, List, Any, Optional, Tuple
from ..core.models import CheckResult, CheckStatus


class YamlFormatChecker:
    """YAMLフォーマット整合性チェッカー"""
    
    # YAMLテンプレート定義
    YAML_TEMPLATES = {
        'DETAILED': {
            'name': '詳細版テンプレート',
            'required_sections': [
                'table_name', 'logical_name', 'category', 'overview',
                'business_columns', 'sample_data'
            ],
            'recommended_sections': [
                'revision_history', 'business_indexes', 'business_constraints',
                'foreign_keys', 'notes', 'business_rules'
            ],
            'column_key': 'business_columns',
            'index_key': 'business_indexes',
            'constraint_key': 'business_constraints'
        },
        'STANDARD': {
            'name': '標準版テンプレート',
            'required_sections': [
                'table_name', 'logical_name', 'category', 'description',
                'columns', 'sample_data'
            ],
            'recommended_sections': [
                'requirement_ids', 'related_tables', 'indexes', 'constraints',
                'foreign_keys', 'performance_requirements', 'data_volume',
                'security', 'operational', 'notes'
            ],
            'column_key': 'columns',
            'index_key': 'indexes',
            'constraint_key': 'constraints'
        }
    }
    
    # 許可されるデータ型
    VALID_DATA_TYPES = [
        'VARCHAR', 'TEXT', 'INTEGER', 'BIGINT', 'BOOLEAN', 
        'TIMESTAMP', 'DATE', 'DECIMAL', 'ENUM', 'JSON', 'FLOAT', 'DOUBLE'
    ]
    
    # 許可されるカテゴリ
    VALID_CATEGORIES = ['マスタ系', 'トランザクション系', '履歴系', 'システム系', 'ワーク系', 'インターフェイス系']
    
    def __init__(self, base_dir: str):
        """
        初期化
        
        Args:
            base_dir: ベースディレクトリパス
        """
        self.base_dir = base_dir
        self.table_details_dir = os.path.join(base_dir, "table-details")
        
    def check_yaml_format_consistency(self, table_names: Optional[List[str]] = None) -> List[CheckResult]:
        """
        YAMLフォーマット整合性チェック実行
        
        Args:
            table_names: チェック対象テーブル名リスト（Noneの場合は全テーブル）
            
        Returns:
            チェック結果リスト
        """
        results = []
        
        if not os.path.exists(self.table_details_dir):
            return [CheckResult(
                table_name="SYSTEM",
                check_type="yaml_format_consistency",
                status=CheckStatus.ERROR,
                message=f"テーブル詳細ディレクトリが存在しません: {self.table_details_dir}"
            )]
        
        # YAMLファイル一覧取得
        yaml_files = [f for f in os.listdir(self.table_details_dir) if f.endswith('_details.yaml')]
        
        if not yaml_files:
            return [CheckResult(
                table_name="SYSTEM",
                check_type="yaml_format_consistency",
                status=CheckStatus.WARNING,
                message="テーブル詳細YAMLファイルが見つかりません"
            )]
        
        for yaml_file in yaml_files:
            table_name = yaml_file.replace('_details.yaml', '')
            
            # 特定テーブルのみチェックする場合のフィルタリング
            if table_names and table_name not in table_names:
                continue
                
            yaml_path = os.path.join(self.table_details_dir, yaml_file)
            results.extend(self._check_single_yaml_file(table_name, yaml_path))
        
        return results
    
    def _check_single_yaml_file(self, table_name: str, yaml_path: str) -> List[CheckResult]:
        """
        単一YAMLファイルのフォーマットチェック
        
        Args:
            table_name: テーブル名
            yaml_path: YAMLファイルパス
            
        Returns:
            チェック結果リスト
        """
        results = []
        
        try:
            # YAMLファイル読み込み
            with open(yaml_path, 'r', encoding='utf-8') as f:
                yaml_content = yaml.safe_load(f)
                
            if not yaml_content:
                return [CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.ERROR,
                    message="YAMLファイルが空または読み込めません"
                )]
            
            # テンプレートパターン検出
            template_type = self._detect_template_pattern(yaml_content)
            template_config = self.YAML_TEMPLATES.get(template_type)
            
            if not template_config:
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.WARNING,
                    message=f"未知のテンプレートパターンです: {template_type}"
                ))
                return results
            
            # 各種チェック実行
            results.extend(self._check_required_sections(table_name, yaml_content, template_config))
            results.extend(self._check_recommended_sections(table_name, yaml_content, template_config))
            results.extend(self._check_section_structure(table_name, yaml_content, template_config))
            results.extend(self._check_data_types(table_name, yaml_content, template_config))
            results.extend(self._check_enum_values(table_name, yaml_content, template_config))
            
            # 成功メッセージ（エラーがない場合）
            error_count = sum(1 for r in results if r.status == CheckStatus.ERROR)
            if error_count == 0:
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.SUCCESS,
                    message=f"{template_config['name']}準拠OK"
                ))
                
        except yaml.YAMLError as e:
            results.append(CheckResult(
                table_name=table_name,
                check_type="yaml_format_consistency",
                status=CheckStatus.ERROR,
                message=f"YAML解析エラー: {str(e)}"
            ))
        except Exception as e:
            results.append(CheckResult(
                table_name=table_name,
                check_type="yaml_format_consistency",
                status=CheckStatus.ERROR,
                message=f"ファイル読み込みエラー: {str(e)}"
            ))
        
        return results
    
    def _detect_template_pattern(self, yaml_content: Dict[str, Any]) -> str:
        """
        テンプレートパターン検出
        
        Args:
            yaml_content: YAML内容
            
        Returns:
            テンプレートタイプ
        """
        if 'business_columns' in yaml_content:
            return 'DETAILED'
        elif 'columns' in yaml_content:
            return 'STANDARD'
        else:
            return 'UNKNOWN'
    
    def _check_required_sections(self, table_name: str, yaml_content: Dict[str, Any], 
                               template_config: Dict[str, Any]) -> List[CheckResult]:
        """
        必須セクション存在確認
        
        Args:
            table_name: テーブル名
            yaml_content: YAML内容
            template_config: テンプレート設定
            
        Returns:
            チェック結果リスト
        """
        results = []
        required_sections = template_config['required_sections']
        
        for section in required_sections:
            if section not in yaml_content:
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.ERROR,
                    message=f"必須セクション '{section}' が存在しません"
                ))
            elif yaml_content[section] is None or yaml_content[section] == '':
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.WARNING,
                    message=f"必須セクション '{section}' が空です"
                ))
        
        return results
    
    def _check_recommended_sections(self, table_name: str, yaml_content: Dict[str, Any], 
                                  template_config: Dict[str, Any]) -> List[CheckResult]:
        """
        推奨セクション存在確認
        
        Args:
            table_name: テーブル名
            yaml_content: YAML内容
            template_config: テンプレート設定
            
        Returns:
            チェック結果リスト
        """
        results = []
        recommended_sections = template_config['recommended_sections']
        
        for section in recommended_sections:
            if section not in yaml_content:
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.WARNING,
                    message=f"推奨セクション '{section}' が存在しません"
                ))
        
        return results
    
    def _check_section_structure(self, table_name: str, yaml_content: Dict[str, Any], 
                               template_config: Dict[str, Any]) -> List[CheckResult]:
        """
        セクション内構造確認
        
        Args:
            table_name: テーブル名
            yaml_content: YAML内容
            template_config: テンプレート設定
            
        Returns:
            チェック結果リスト
        """
        results = []
        
        # カラム定義構造チェック
        column_key = template_config['column_key']
        if column_key in yaml_content and yaml_content[column_key]:
            results.extend(self._check_column_structure(table_name, yaml_content[column_key]))
        
        # インデックス定義構造チェック
        index_key = template_config['index_key']
        if index_key in yaml_content and yaml_content[index_key]:
            results.extend(self._check_index_structure(table_name, yaml_content[index_key]))
        
        # 制約定義構造チェック
        constraint_key = template_config['constraint_key']
        if constraint_key in yaml_content and yaml_content[constraint_key]:
            results.extend(self._check_constraint_structure(table_name, yaml_content[constraint_key]))
        
        return results
    
    def _check_column_structure(self, table_name: str, columns: List[Dict[str, Any]]) -> List[CheckResult]:
        """
        カラム定義構造チェック
        
        Args:
            table_name: テーブル名
            columns: カラム定義リスト
            
        Returns:
            チェック結果リスト
        """
        results = []
        
        if not isinstance(columns, list):
            return [CheckResult(
                table_name=table_name,
                check_type="yaml_format_consistency",
                status=CheckStatus.ERROR,
                message="カラム定義は配列である必要があります"
            )]
        
        for i, column in enumerate(columns):
            if not isinstance(column, dict):
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.ERROR,
                    message=f"カラム定義[{i}]は辞書である必要があります"
                ))
                continue
            
            # 必須フィールドチェック
            required_fields = ['name']
            for field in required_fields:
                if field not in column:
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.ERROR,
                        message=f"カラム定義[{i}]: 必須フィールド '{field}' が存在しません"
                    ))
            
            # 推奨フィールドチェック
            recommended_fields = ['logical_name', 'data_type', 'description']
            for field in recommended_fields:
                if field not in column:
                    column_name = column.get('name', f'カラム[{i}]')
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.WARNING,
                        message=f"カラム '{column_name}': 推奨フィールド '{field}' が存在しません"
                    ))
        
        return results
    
    def _check_index_structure(self, table_name: str, indexes: List[Dict[str, Any]]) -> List[CheckResult]:
        """
        インデックス定義構造チェック
        
        Args:
            table_name: テーブル名
            indexes: インデックス定義リスト
            
        Returns:
            チェック結果リスト
        """
        results = []
        
        if not isinstance(indexes, list):
            return [CheckResult(
                table_name=table_name,
                check_type="yaml_format_consistency",
                status=CheckStatus.ERROR,
                message="インデックス定義は配列である必要があります"
            )]
        
        for i, index in enumerate(indexes):
            if not isinstance(index, dict):
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.ERROR,
                    message=f"インデックス定義[{i}]は辞書である必要があります"
                ))
                continue
            
            # 必須フィールドチェック
            required_fields = ['name', 'columns']
            for field in required_fields:
                if field not in index:
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.ERROR,
                        message=f"インデックス定義[{i}]: 必須フィールド '{field}' が存在しません"
                    ))
            
            # columns配列チェック
            if 'columns' in index and not isinstance(index['columns'], list):
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.ERROR,
                    message=f"インデックス定義[{i}]: 'columns'は配列である必要があります"
                ))
        
        return results
    
    def _check_constraint_structure(self, table_name: str, constraints: List[Dict[str, Any]]) -> List[CheckResult]:
        """
        制約定義構造チェック
        
        Args:
            table_name: テーブル名
            constraints: 制約定義リスト
            
        Returns:
            チェック結果リスト
        """
        results = []
        
        if not isinstance(constraints, list):
            return [CheckResult(
                table_name=table_name,
                check_type="yaml_format_consistency",
                status=CheckStatus.ERROR,
                message="制約定義は配列である必要があります"
            )]
        
        for i, constraint in enumerate(constraints):
            if not isinstance(constraint, dict):
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.ERROR,
                    message=f"制約定義[{i}]は辞書である必要があります"
                ))
                continue
            
            # 必須フィールドチェック
            required_fields = ['name', 'type']
            for field in required_fields:
                if field not in constraint:
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.ERROR,
                        message=f"制約定義[{i}]: 必須フィールド '{field}' が存在しません"
                    ))
        
        return results
    
    def _check_data_types(self, table_name: str, yaml_content: Dict[str, Any], 
                         template_config: Dict[str, Any]) -> List[CheckResult]:
        """
        データ型妥当性確認
        
        Args:
            table_name: テーブル名
            yaml_content: YAML内容
            template_config: テンプレート設定
            
        Returns:
            チェック結果リスト
        """
        results = []
        column_key = template_config['column_key']
        
        if column_key not in yaml_content or not yaml_content[column_key]:
            return results
        
        columns = yaml_content[column_key]
        if not isinstance(columns, list):
            return results
        
        for column in columns:
            if not isinstance(column, dict):
                continue
                
            column_name = column.get('name', 'unknown')
            data_type = column.get('data_type') or column.get('type')
            
            if data_type:
                # データ型の基本部分を抽出（長さ指定を除く）
                base_type = data_type.split('(')[0].upper()
                
                if base_type not in self.VALID_DATA_TYPES:
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.ERROR,
                        message=f"カラム '{column_name}': 無効なデータ型 '{data_type}'"
                    ))
        
        return results
    
    def _check_enum_values(self, table_name: str, yaml_content: Dict[str, Any], 
                          template_config: Dict[str, Any]) -> List[CheckResult]:
        """
        ENUM値妥当性確認
        
        Args:
            table_name: テーブル名
            yaml_content: YAML内容
            template_config: テンプレート設定
            
        Returns:
            チェック結果リスト
        """
        results = []
        column_key = template_config['column_key']
        
        if column_key not in yaml_content or not yaml_content[column_key]:
            return results
        
        columns = yaml_content[column_key]
        if not isinstance(columns, list):
            return results
        
        for column in columns:
            if not isinstance(column, dict):
                continue
                
            column_name = column.get('name', 'unknown')
            data_type = column.get('data_type') or column.get('type')
            
            if data_type and data_type.upper() == 'ENUM':
                enum_values = column.get('enum_values')
                
                if not enum_values:
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.ERROR,
                        message=f"カラム '{column_name}': ENUM型には 'enum_values' が必要です"
                    ))
                elif not isinstance(enum_values, list):
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.ERROR,
                        message=f"カラム '{column_name}': 'enum_values' は配列である必要があります"
                    ))
                elif len(enum_values) == 0:
                    results.append(CheckResult(
                        table_name=table_name,
                        check_type="yaml_format_consistency",
                        status=CheckStatus.WARNING,
                        message=f"カラム '{column_name}': 'enum_values' が空です"
                    ))
        
        # カテゴリ値チェック
        if 'category' in yaml_content:
            category = yaml_content['category']
            if category not in self.VALID_CATEGORIES:
                results.append(CheckResult(
                    table_name=table_name,
                    check_type="yaml_format_consistency",
                    status=CheckStatus.ERROR,
                    message=f"無効なカテゴリ値: '{category}'. 有効な値: {', '.join(self.VALID_CATEGORIES)}"
                ))
        
        return results
    
    def suggest_missing_sections(self, table_name: str, yaml_content: Dict[str, Any]) -> List[str]:
        """
        不足セクション提案
        
        Args:
            table_name: テーブル名
            yaml_content: YAML内容
            
        Returns:
            提案リスト
        """
        suggestions = []
        template_type = self._detect_template_pattern(yaml_content)
        template_config = self.YAML_TEMPLATES.get(template_type)
        
        if not template_config:
            return suggestions
        
        # 不足している推奨セクションを提案
        for section in template_config['recommended_sections']:
            if section not in yaml_content:
                suggestions.append(f"推奨セクション '{section}' の追加を検討してください")
        
        return suggestions
