"""
高度な整合性チェッカー

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/tools/REFACTORING_PLAN.md
実装日: 2025-06-08
実装者: AI Assistant
"""

import re
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass

from .base_checker import BaseChecker, CheckResult as BaseCheckResult
from ..core.models import TableDefinition, ColumnDefinition, CheckResult, CheckStatus, CheckResultSummary
from ..core.config import DatabaseToolsConfig


@dataclass
class DataTypeCompatibility:
    """データ型互換性情報"""
    source_type: str
    target_type: str
    is_compatible: bool
    conversion_required: bool
    risk_level: str  # 'low', 'medium', 'high'
    notes: str


class AdvancedConsistencyChecker(BaseChecker):
    """高度な整合性チェッカー"""
    
    def __init__(self, config_or_path):
        # 文字列パスまたはConfigオブジェクトを受け入れる
        if isinstance(config_or_path, str):
            from pathlib import Path
            from ..core.config import DatabaseToolsConfig
            config = DatabaseToolsConfig(base_dir=Path(config_or_path))
        else:
            config = config_or_path
        
        super().__init__(config)
        self._data_type_mappings = self._initialize_data_type_mappings()
        self._naming_patterns = self._initialize_naming_patterns()
    
    def get_checker_name(self) -> str:
        return "高度整合性チェック"
    
    def check_table(self, table_def: TableDefinition) -> List[CheckResult]:
        """単一テーブルの高度整合性チェック"""
        if not self._validate_table_definition(table_def):
            return []
        
        results = []
        
        # データ型整合性チェック
        results.extend(self._check_data_type_consistency(table_def))
        
        # 命名規則チェック
        results.extend(self._check_naming_conventions(table_def))
        
        # 制約整合性チェック
        results.extend(self._check_constraint_consistency(table_def))
        
        # インデックス最適化チェック
        results.extend(self._check_index_optimization(table_def))
        
        # パフォーマンス影響チェック
        results.extend(self._check_performance_impact(table_def))
        
        return results
    
    def _check_data_type_consistency(self, table_def: TableDefinition) -> List[CheckResult]:
        """データ型整合性チェック"""
        results = []
        
        for column in table_def.columns:
            # データ型の妥当性チェック
            type_result = self._validate_data_type(table_def.name, column)
            if type_result:
                results.append(type_result)
            
            # 長さ制約の妥当性チェック
            length_result = self._validate_length_constraints(table_def.name, column)
            if length_result:
                results.append(length_result)
            
            # デフォルト値の妥当性チェック
            default_result = self._validate_default_value(table_def.name, column)
            if default_result:
                results.append(default_result)
        
        return results
    
    def _check_naming_conventions(self, table_def: TableDefinition) -> List[CheckResult]:
        """命名規則チェック"""
        results = []
        
        # テーブル名チェック
        table_result = self._check_table_naming(table_def)
        if table_result:
            results.append(table_result)
        
        # カラム名チェック
        for column in table_def.columns:
            column_result = self._check_column_naming(table_def.name, column)
            if column_result:
                results.append(column_result)
        
        # インデックス名チェック
        if hasattr(table_def, 'indexes') and table_def.indexes:
            for index in table_def.indexes:
                index_result = self._check_index_naming(table_def.name, index)
                if index_result:
                    results.append(index_result)
        
        return results
    
    def _check_constraint_consistency(self, table_def: TableDefinition) -> List[BaseCheckResult]:
        """制約整合性チェック"""
        results = []
        
        # 主キー制約チェック
        pk_result = self._check_primary_key_constraints(table_def)
        if pk_result:
            results.append(pk_result)
        
        # 外部キー制約チェック
        if hasattr(table_def, 'foreign_keys') and table_def.foreign_keys:
            for fk in table_def.foreign_keys:
                fk_result = self._check_foreign_key_constraint(table_def.name, fk)
                if fk_result:
                    results.append(fk_result)
        
        # 一意制約チェック
        unique_result = self._check_unique_constraints(table_def)
        if unique_result:
            results.append(unique_result)
        
        # チェック制約チェック
        check_result = self._check_check_constraints(table_def)
        if check_result:
            results.append(check_result)
        
        return results
    
    def _check_index_optimization(self, table_def: TableDefinition) -> List[CheckResult]:
        """インデックス最適化チェック"""
        results = []
        
        if not hasattr(table_def, 'indexes') or not table_def.indexes:
            # 基本的なインデックスが不足している場合の警告
            if self._needs_basic_indexes(table_def):
                results.append(self._create_result(
                    table_def.name,
                    'warning',
                    '基本的なインデックスが不足している可能性があります',
                    details={'recommendation': '頻繁に検索されるカラムにインデックスを追加することを検討してください'},
                    severity='warning'
                ))
            return results
        
        # 重複インデックスチェック
        duplicate_result = self._check_duplicate_indexes(table_def)
        if duplicate_result:
            results.append(duplicate_result)
        
        # 未使用インデックスチェック
        unused_result = self._check_unused_indexes(table_def)
        if unused_result:
            results.append(unused_result)
        
        # 複合インデックスの順序チェック
        order_result = self._check_composite_index_order(table_def)
        if order_result:
            results.append(order_result)
        
        return results
    
    def _check_performance_impact(self, table_def: TableDefinition) -> List[CheckResult]:
        """パフォーマンス影響チェック"""
        results = []
        
        # 大きなテーブルサイズの警告
        size_result = self._check_table_size_impact(table_def)
        if size_result:
            results.append(size_result)
        
        # カラム数の妥当性チェック
        column_count_result = self._check_column_count(table_def)
        if column_count_result:
            results.append(column_count_result)
        
        # データ型のパフォーマンス影響チェック
        type_performance_result = self._check_data_type_performance(table_def)
        if type_performance_result:
            results.append(type_performance_result)
        
        return results
    
    def _validate_data_type(self, table_name: str, column: ColumnDefinition) -> Optional[CheckResult]:
        """データ型の妥当性検証"""
        if not column.type:
            return self._create_result(
                table_name,
                'error',
                f'カラム {column.name} のデータ型が定義されていません',
                severity='error'
            )
        
        # PostgreSQL標準データ型チェック
        valid_types = {
            'VARCHAR', 'TEXT', 'INTEGER', 'BIGINT', 'SMALLINT', 'DECIMAL', 'NUMERIC',
            'REAL', 'DOUBLE PRECISION', 'BOOLEAN', 'DATE', 'TIME', 'TIMESTAMP',
            'TIMESTAMPTZ', 'UUID', 'JSON', 'JSONB', 'BYTEA', 'SERIAL', 'BIGSERIAL'
        }
        
        base_type = re.sub(r'\([^)]*\)', '', column.type.upper())
        if base_type not in valid_types:
            return self._create_result(
                table_name,
                'warning',
                f'カラム {column.name} のデータ型 {column.type} は標準的でない可能性があります',
                details={'suggested_types': list(valid_types)},
                severity='warning'
            )
        
        return None
    
    def _validate_length_constraints(self, table_name: str, column: ColumnDefinition) -> Optional[CheckResult]:
        """長さ制約の妥当性検証"""
        if 'VARCHAR' in column.type.upper():
            # VARCHAR長さの妥当性チェック
            match = re.search(r'VARCHAR\((\d+)\)', column.type.upper())
            if match:
                length = int(match.group(1))
                if length > 4000:
                    return self._create_result(
                        table_name,
                        'warning',
                        f'カラム {column.name} のVARCHAR長({length})が大きすぎます。TEXTの使用を検討してください',
                        details={'current_length': length, 'recommendation': 'TEXT型への変更'},
                        severity='warning'
                    )
                elif length < 10 and column.name.lower() not in ['id', 'code', 'flag']:
                    return self._create_result(
                        table_name,
                        'info',
                        f'カラム {column.name} のVARCHAR長({length})が短い可能性があります',
                        details={'current_length': length},
                        severity='info'
                    )
        
        return None
    
    def _validate_default_value(self, table_name: str, column: ColumnDefinition) -> Optional[CheckResult]:
        """デフォルト値の妥当性検証"""
        if not hasattr(column, 'default') or not column.default:
            return None
        
        # データ型とデフォルト値の整合性チェック
        if 'INTEGER' in column.type.upper() or 'BIGINT' in column.type.upper():
            try:
                int(column.default)
            except ValueError:
                return self._create_result(
                    table_name,
                    'error',
                    f'カラム {column.name} の整数型デフォルト値 {column.default} が不正です',
                    severity='error'
                )
        
        elif 'BOOLEAN' in column.type.upper():
            if column.default.upper() not in ['TRUE', 'FALSE', '0', '1']:
                return self._create_result(
                    table_name,
                    'error',
                    f'カラム {column.name} のブール型デフォルト値 {column.default} が不正です',
                    severity='error'
                )
        
        return None
    
    def _check_table_naming(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """テーブル命名規則チェック"""
        table_name = table_def.name
        
        # プレフィックスチェック
        valid_prefixes = ['MST_', 'TRN_', 'HIS_', 'SYS_', 'WRK_', 'IF_']
        if not any(table_name.startswith(prefix) for prefix in valid_prefixes):
            return self._create_result(
                table_name,
                'warning',
                f'テーブル名 {table_name} が命名規則に従っていません',
                details={
                    'valid_prefixes': valid_prefixes,
                    'recommendation': '適切なプレフィックスを追加してください'
                },
                severity='warning'
            )
        
        # 長さチェック
        if len(table_name) > 63:  # PostgreSQL制限
            return self._create_result(
                table_name,
                'error',
                f'テーブル名 {table_name} が長すぎます（{len(table_name)}文字）',
                details={'max_length': 63},
                severity='error'
            )
        
        return None
    
    def _check_column_naming(self, table_name: str, column: ColumnDefinition) -> Optional[CheckResult]:
        """カラム命名規則チェック"""
        column_name = column.name
        
        # 予約語チェック
        reserved_words = {
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'ORDER', 'GROUP',
            'HAVING', 'JOIN', 'UNION', 'CREATE', 'ALTER', 'DROP', 'INDEX', 'TABLE'
        }
        
        if column_name.upper() in reserved_words:
            return self._create_result(
                table_name,
                'error',
                f'カラム名 {column_name} はSQL予約語です',
                details={'reserved_word': column_name.upper()},
                severity='error'
            )
        
        # スネークケースチェック
        if not re.match(r'^[a-z][a-z0-9_]*$', column_name):
            return self._create_result(
                table_name,
                'warning',
                f'カラム名 {column_name} がスネークケース規則に従っていません',
                details={'recommendation': '小文字とアンダースコアのみ使用してください'},
                severity='warning'
            )
        
        return None
    
    def _check_index_naming(self, table_name: str, index: Any) -> Optional[CheckResult]:
        """インデックス命名規則チェック"""
        if not hasattr(index, 'name') or not index.name:
            return self._create_result(
                table_name,
                'warning',
                'インデックス名が定義されていません',
                severity='warning'
            )
        
        index_name = index.name
        
        # インデックス命名パターンチェック
        if not re.match(r'^idx_[a-z0-9_]+$', index_name):
            return self._create_result(
                table_name,
                'warning',
                f'インデックス名 {index_name} が命名規則に従っていません',
                details={'pattern': 'idx_テーブル名_カラム名'},
                severity='warning'
            )
        
        return None
    
    def _needs_basic_indexes(self, table_def: TableDefinition) -> bool:
        """基本的なインデックスが必要かチェック"""
        # 外部キーカラムや頻繁に検索されそうなカラムをチェック
        search_columns = ['tenant_id', 'user_id', 'emp_no', 'email', 'created_at']
        
        for column in table_def.columns:
            if any(search_col in column.name.lower() for search_col in search_columns):
                return True
        
        return False
    
    def _check_duplicate_indexes(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """重複インデックスチェック"""
        if not hasattr(table_def, 'indexes') or len(table_def.indexes) < 2:
            return None
        
        index_columns = []
        for index in table_def.indexes:
            if hasattr(index, 'columns'):
                columns_key = tuple(sorted(index.columns))
                if columns_key in index_columns:
                    return self._create_result(
                        table_def.name,
                        'warning',
                        '重複するインデックスが存在します',
                        details={'duplicate_columns': list(columns_key)},
                        severity='warning'
                    )
                index_columns.append(columns_key)
        
        return None
    
    def _check_unused_indexes(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """未使用インデックスチェック（ヒューリスティック）"""
        # 実際の使用統計は取得できないため、命名パターンから推測
        if not hasattr(table_def, 'indexes'):
            return None
        
        suspicious_indexes = []
        for index in table_def.indexes:
            if hasattr(index, 'name') and 'temp' in index.name.lower():
                suspicious_indexes.append(index.name)
        
        if suspicious_indexes:
            return self._create_result(
                table_def.name,
                'info',
                '一時的なインデックスが存在します',
                details={'suspicious_indexes': suspicious_indexes},
                severity='info'
            )
        
        return None
    
    def _check_composite_index_order(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """複合インデックスの順序チェック"""
        # 複合インデックスの効率的な順序をチェック
        # 実装は簡略化
        return None
    
    def _check_table_size_impact(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """テーブルサイズ影響チェック"""
        # カラム数とデータ型からサイズを推定
        estimated_row_size = 0
        large_columns = []
        
        for column in table_def.columns:
            if 'TEXT' in column.type.upper():
                estimated_row_size += 1000  # 推定値
                large_columns.append(column.name)
            elif 'VARCHAR' in column.type.upper():
                match = re.search(r'VARCHAR\((\d+)\)', column.type.upper())
                if match:
                    length = int(match.group(1))
                    estimated_row_size += length
                    if length > 500:
                        large_columns.append(column.name)
        
        if estimated_row_size > 8000:  # PostgreSQLページサイズ考慮
            return self._create_result(
                table_def.name,
                'warning',
                f'推定行サイズが大きいです（約{estimated_row_size}バイト）',
                details={
                    'estimated_size': estimated_row_size,
                    'large_columns': large_columns,
                    'recommendation': '大きなカラムの分離を検討してください'
                },
                severity='warning'
            )
        
        return None
    
    def _check_column_count(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """カラム数チェック"""
        column_count = len(table_def.columns)
        
        if column_count > 50:
            return self._create_result(
                table_def.name,
                'warning',
                f'カラム数が多すぎます（{column_count}カラム）',
                details={
                    'column_count': column_count,
                    'recommendation': 'テーブル分割を検討してください'
                },
                severity='warning'
            )
        elif column_count < 3:
            return self._create_result(
                table_def.name,
                'info',
                f'カラム数が少ないです（{column_count}カラム）',
                details={'column_count': column_count},
                severity='info'
            )
        
        return None
    
    def _check_data_type_performance(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """データ型パフォーマンス影響チェック"""
        performance_issues = []
        
        for column in table_def.columns:
            # DECIMAL vs NUMERIC vs REAL のパフォーマンス比較
            if 'DECIMAL' in column.type.upper() or 'NUMERIC' in column.type.upper():
                performance_issues.append({
                    'column': column.name,
                    'issue': 'DECIMAL/NUMERIC型は計算が重い',
                    'recommendation': '精度が不要な場合はREALまたはDOUBLE PRECISIONを検討'
                })
        
        if performance_issues:
            return self._create_result(
                table_def.name,
                'info',
                'パフォーマンスに影響する可能性のあるデータ型があります',
                details={'issues': performance_issues},
                severity='info'
            )
        
        return None
    
    def _initialize_data_type_mappings(self) -> Dict[str, DataTypeCompatibility]:
        """データ型マッピングの初期化"""
        # 簡略化された実装
        return {}
    
    def _initialize_naming_patterns(self) -> Dict[str, str]:
        """命名パターンの初期化"""
        return {
            'table_prefix': r'^(MST_|TRN_|HIS_|SYS_|WRK_|IF_)',
            'column_snake_case': r'^[a-z][a-z0-9_]*$',
            'index_pattern': r'^idx_[a-z0-9_]+$'
        }
    
    def _create_result(self, table_name: str, status: str, message: str, 
                      details: dict = None, severity: str = 'info') -> CheckResult:
        """CheckResultオブジェクトを作成"""
        status_enum = CheckStatus.ERROR if status == 'error' else \
                     CheckStatus.WARNING if status == 'warning' else \
                     CheckStatus.SUCCESS
        
        return CheckResult(
            check_type='advanced_check',
            table_name=table_name,
            status=status_enum,
            message=message,
            severity=severity,
            details=details
        )
    
    def _check_primary_key_constraints(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """主キー制約チェック"""
        pk_columns = [col for col in table_def.columns if getattr(col, 'primary_key', False)]
        
        if not pk_columns:
            return self._create_result(
                table_def.name,
                'error',
                '主キーが定義されていません',
                details={'recommendation': 'id カラムを主キーとして追加してください'},
                severity='error'
            )
        
        if len(pk_columns) > 1:
            return self._create_result(
                table_def.name,
                'info',
                f'複合主キーが定義されています（{len(pk_columns)}カラム）',
                details={'pk_columns': [col.name for col in pk_columns]},
                severity='info'
            )
        
        return None
    
    def _check_foreign_key_constraint(self, table_name: str, fk: Any) -> Optional[CheckResult]:
        """外部キー制約チェック"""
        # 外部キー制約の妥当性をチェック
        # 実装は簡略化
        return None
    
    def _check_unique_constraints(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """一意制約チェック"""
        unique_columns = [col for col in table_def.columns if getattr(col, 'unique', False)]
        
        if len(unique_columns) > 5:
            return self._create_result(
                table_def.name,
                'warning',
                f'一意制約が多すぎます（{len(unique_columns)}カラム）',
                details={
                    'unique_columns': [col.name for col in unique_columns],
                    'recommendation': '本当に必要な一意制約か確認してください'
                },
                severity='warning'
            )
        
        return None
    
    def _check_check_constraints(self, table_def: TableDefinition) -> Optional[CheckResult]:
        """チェック制約チェック"""
        # チェック制約の妥当性をチェック
        # 実装は簡略化
        return None
    
    def check(self, table_names: List[str] = None) -> CheckResult:
        """整合性チェック実行"""
        from pathlib import Path
        import yaml
        import glob
        
        errors = []
        warnings = []
        
        if table_names is None:
            # 全テーブルをチェック
            table_names = self._get_all_table_names()
        
        for table_name in table_names:
            # ファイル存在チェック
            yaml_path = self.config.table_details_dir / f'{table_name}_details.yaml'
            ddl_path = self.config.ddl_dir / f'{table_name}.sql'
            
            # YAML詳細定義ファイルチェック
            if not yaml_path.exists():
                errors.append(CheckResult(
                    check_type='file_existence',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'{table_name}: YAML詳細定義ファイルが存在しません',
                    severity='error'
                ))
                continue
            
            # DDLファイルチェック
            if not ddl_path.exists():
                errors.append(CheckResult(
                    check_type='file_existence',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'{table_name}: DDLファイルが存在しません',
                    severity='error'
                ))
                continue
            
            # Markdownファイルチェック（glob検索）
            md_files = glob.glob(str(self.config.tables_dir / f'テーブル定義書_{table_name}_*.md'))
            if not md_files:
                errors.append(CheckResult(
                    check_type='file_existence',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'{table_name}: Markdown定義書が存在しません',
                    severity='error'
                ))
                continue
            
            # YAMLファイルを読み込んでテーブル定義を作成
            try:
                with open(yaml_path, 'r', encoding='utf-8') as f:
                    yaml_data = yaml.safe_load(f)
                
                # DDLファイルも読み込んで比較
                with open(ddl_path, 'r', encoding='utf-8') as f:
                    ddl_content = f.read()
                
                # カラム定義の整合性チェック
                column_errors = self._check_column_consistency(table_name, yaml_data, ddl_content)
                errors.extend(column_errors)
                
                # 外部キー整合性チェック
                if 'foreign_keys' in yaml_data:
                    fk_errors = self._check_foreign_key_consistency(table_name, yaml_data)
                    errors.extend(fk_errors)
                    
            except Exception as e:
                errors.append(CheckResult(
                    check_type='yaml_parsing',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'{table_name}: YAML解析エラー: {str(e)}',
                    severity='error'
                ))
        
        # 孤立ファイルチェック
        if table_names is None:  # 全体チェック時のみ
            orphan_warnings = self._check_orphaned_files()
            warnings.extend(orphan_warnings)
        
        # 結果をまとめる
        is_valid = len(errors) == 0
        
        return CheckResult(
            check_type='comprehensive',
            table_name='all' if table_names is None else ','.join(table_names),
            status=CheckStatus.SUCCESS if is_valid else CheckStatus.ERROR,
            message='整合性チェック完了',
            severity='info' if is_valid else 'error',
            details={'errors': errors, 'warnings': warnings},
            is_valid=is_valid,
            errors=errors,
            warnings=warnings
        )
    
    def check_table_name(self, table_name: str) -> CheckResult:
        """テーブル名の妥当性チェック"""
        errors = []
        
        # プレフィックスチェック
        valid_prefixes = ['MST_', 'TRN_', 'HIS_', 'SYS_', 'WRK_', 'IF_']
        has_valid_prefix = any(table_name.startswith(prefix) for prefix in valid_prefixes)
        
        # 特別なケース: プレフィックスのみの場合は無効
        if table_name in valid_prefixes or table_name.endswith('_'):
            has_valid_prefix = False
        
        if not has_valid_prefix:
            errors.append(CheckResult(
                check_type='naming_convention',
                table_name=table_name,
                status=CheckStatus.ERROR,
                message=f'テーブル名 {table_name} が命名規則に従っていません',
                severity='error'
            ))
        
        # 長さチェック
        if len(table_name) > 63:
            errors.append(CheckResult(
                check_type='naming_convention',
                table_name=table_name,
                status=CheckStatus.ERROR,
                message=f'テーブル名 {table_name} が長すぎます（{len(table_name)}文字）',
                severity='error'
            ))
        
        is_valid = len(errors) == 0
        return CheckResult(
            check_type='table_naming',
            table_name=table_name,
            status=CheckStatus.SUCCESS if is_valid else CheckStatus.ERROR,
            message='テーブル名チェック完了',
            severity='info' if is_valid else 'error',
            is_valid=is_valid,
            errors=errors
        )
    
    def check_column_name(self, column_name: str) -> CheckResult:
        """カラム名の妥当性チェック"""
        errors = []
        
        # 予約語チェック
        reserved_words = {
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'ORDER', 'GROUP',
            'HAVING', 'JOIN', 'UNION', 'CREATE', 'ALTER', 'DROP', 'INDEX', 'TABLE'
        }
        
        if column_name.upper() in reserved_words:
            errors.append(CheckResult(
                check_type='naming_convention',
                table_name='',
                status=CheckStatus.ERROR,
                message=f'カラム名 {column_name} はSQL予約語です',
                severity='error'
            ))
        
        # スネークケースチェック
        if not re.match(r'^[a-z][a-z0-9_]*$', column_name):
            errors.append(CheckResult(
                check_type='naming_convention',
                table_name='',
                status=CheckStatus.ERROR,
                message=f'カラム名 {column_name} がスネークケース規則に従っていません',
                severity='error'
            ))
        
        is_valid = len(errors) == 0
        return CheckResult(
            check_type='column_naming',
            table_name='',
            status=CheckStatus.SUCCESS if is_valid else CheckStatus.ERROR,
            message='カラム名チェック完了',
            severity='info' if is_valid else 'error',
            is_valid=is_valid,
            errors=errors
        )
    
    def _get_all_table_names(self) -> List[str]:
        """全テーブル名を取得"""
        table_names = []
        yaml_dir = self.config.table_details_dir
        
        if yaml_dir.exists():
            for yaml_file in yaml_dir.glob('*_details.yaml'):
                table_name = yaml_file.stem.replace('_details', '')
                table_names.append(table_name)
        
        return table_names
    
    def _create_table_definition_from_yaml(self, yaml_data: dict) -> Optional[TableDefinition]:
        """YAMLデータからTableDefinitionを作成"""
        try:
            columns = []
            for col_data in yaml_data.get('columns', []):
                column = ColumnDefinition(
                    name=col_data.get('name'),
                    type=col_data.get('type'),
                    nullable=col_data.get('nullable', True),
                    primary_key=col_data.get('primary_key', False),
                    unique=col_data.get('unique', False),
                    default=col_data.get('default'),
                    comment=col_data.get('comment', ''),
                    requirement_id=col_data.get('requirement_id')
                )
                columns.append(column)
            
            table_def = TableDefinition(
                name=yaml_data.get('table_name'),
                logical_name=yaml_data.get('logical_name'),
                columns=columns,
                category=yaml_data.get('category'),
                priority=yaml_data.get('priority'),
                requirement_id=yaml_data.get('requirement_id')
            )
            
            # インデックスと外部キーも設定
            if 'indexes' in yaml_data:
                table_def.indexes = yaml_data['indexes']
            if 'foreign_keys' in yaml_data:
                table_def.foreign_keys = yaml_data['foreign_keys']
            
            return table_def
            
        except Exception as e:
            return None
    
    def _check_orphaned_files(self) -> List[CheckResult]:
        """孤立ファイルチェック"""
        from pathlib import Path
        import glob
        
        warnings = []
        
        # 各ディレクトリのファイルを取得
        yaml_files = set()
        ddl_files = set()
        md_files = set()
        
        yaml_dir = self.config.table_details_dir
        ddl_dir = self.config.ddl_dir
        tables_dir = self.config.tables_dir
        
        # YAMLファイルからテーブル名を抽出
        if yaml_dir.exists():
            for yaml_file in yaml_dir.glob('*_details.yaml'):
                table_name = yaml_file.stem.replace('_details', '')
                yaml_files.add(table_name)
        
        # DDLファイルからテーブル名を抽出
        if ddl_dir.exists():
            for ddl_file in ddl_dir.glob('*.sql'):
                table_name = ddl_file.stem
                ddl_files.add(table_name)
        
        # Markdownファイルからテーブル名を抽出
        if tables_dir.exists():
            for md_file in tables_dir.glob('テーブル定義書_*.md'):
                # ファイル名からテーブル名を抽出（簡略化）
                parts = md_file.stem.split('_')
                if len(parts) >= 3:
                    table_name = parts[1]  # テーブル定義書_MST_Employee_社員基本情報.md -> MST_Employee
                    md_files.add(table_name)
        
        # 孤立ファイルを検出
        all_tables = yaml_files | ddl_files | md_files
        
        for table_name in all_tables:
            if table_name in yaml_files and table_name not in ddl_files:
                warnings.append(CheckResult(
                    check_type='orphaned_files',
                    table_name=table_name,
                    status=CheckStatus.WARNING,
                    message=f'孤立したYAML詳細定義ファイル: {table_name}',
                    severity='warning'
                ))
            
            if table_name in ddl_files and table_name not in yaml_files:
                warnings.append(CheckResult(
                    check_type='orphaned_files',
                    table_name=table_name,
                    status=CheckStatus.WARNING,
                    message=f'孤立したDDLファイル: {table_name}',
                    severity='warning'
                ))
            
            if table_name in md_files and table_name not in yaml_files:
                warnings.append(CheckResult(
                    check_type='orphaned_files',
                    table_name=table_name,
                    status=CheckStatus.WARNING,
                    message=f'孤立したMarkdown定義書: {table_name}',
                    severity='warning'
                ))
        
        return warnings
    
    def _check_column_consistency(self, table_name: str, yaml_data: dict, ddl_content: str) -> List[CheckResult]:
        """カラム定義の整合性チェック"""
        errors = []
        
        yaml_columns = yaml_data.get('columns', [])
        
        # DDLからカラム情報を抽出（簡略化）
        ddl_columns = self._parse_ddl_columns(ddl_content)
        
        for yaml_col in yaml_columns:
            col_name = yaml_col.get('name')
            yaml_type = yaml_col.get('type', '').upper()
            yaml_nullable = yaml_col.get('nullable', True)
            
            # DDLに対応するカラムがあるかチェック
            ddl_col = ddl_columns.get(col_name)
            if not ddl_col:
                continue  # DDLにカラムがない場合はスキップ
            
            ddl_type = ddl_col.get('type', '').upper()
            ddl_nullable = ddl_col.get('nullable', True)
            
            # データ型の比較
            if yaml_type != ddl_type:
                errors.append(CheckResult(
                    check_type='column_consistency',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'カラム {col_name} のデータ型が一致しません: YAML({yaml_type}) ≠ DDL({ddl_type})',
                    severity='error'
                ))
            
            # NULL制約の比較
            if yaml_nullable != ddl_nullable:
                errors.append(CheckResult(
                    check_type='column_consistency',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'カラム {col_name} のNULL制約が一致しません: YAML({yaml_nullable}) ≠ DDL({ddl_nullable})',
                    severity='error'
                ))
        
        return errors
    
    def _parse_ddl_columns(self, ddl_content: str) -> Dict[str, Dict[str, Any]]:
        """DDLからカラム情報を抽出"""
        columns = {}
        
        # CREATE TABLE文を抽出
        create_match = re.search(r'CREATE TABLE\s+\w+\s*\((.*?)\);', ddl_content, re.DOTALL | re.IGNORECASE)
        if not create_match:
            return columns
        
        table_def = create_match.group(1)
        
        # カラム定義を行ごとに分割
        lines = [line.strip() for line in table_def.split('\n') if line.strip()]
        
        for line in lines:
            # 制約行やコメント行をスキップ
            if (line.upper().startswith(('UNIQUE', 'PRIMARY KEY', 'FOREIGN KEY', 'CONSTRAINT', '--')) or
                'REFERENCES' in line.upper()):
                continue
            
            # カラム定義を解析
            parts = line.rstrip(',').split()
            if len(parts) >= 2:
                col_name = parts[0].strip()
                col_type = parts[1].strip()
                
                # NULL制約をチェック
                nullable = 'NOT NULL' not in line.upper()
                
                columns[col_name] = {
                    'type': col_type,
                    'nullable': nullable
                }
        
        return columns
    
    def _check_foreign_key_consistency(self, table_name: str, yaml_data: dict) -> List[CheckResult]:
        """外部キー整合性チェック"""
        errors = []
        
        foreign_keys = yaml_data.get('foreign_keys', [])
        
        for fk in foreign_keys:
            ref_table = fk.get('references', {}).get('table')
            ref_columns = fk.get('references', {}).get('columns', [])
            fk_columns = fk.get('columns', [])
            
            if not ref_table:
                continue
            
            # 参照先テーブルのYAMLファイルをチェック
            ref_yaml_path = self.config.table_details_dir / f'{ref_table}_details.yaml'
            if not ref_yaml_path.exists():
                errors.append(CheckResult(
                    check_type='foreign_key_consistency',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'参照先テーブル {ref_table} が存在しません',
                    severity='error'
                ))
                continue
            
            # 参照先テーブルの定義を読み込み
            try:
                import yaml
                with open(ref_yaml_path, 'r', encoding='utf-8') as f:
                    ref_yaml_data = yaml.safe_load(f)
                
                ref_table_columns = {col['name']: col for col in ref_yaml_data.get('columns', [])}
                
                # 参照先カラムの存在とデータ型チェック
                for i, ref_col_name in enumerate(ref_columns):
                    if ref_col_name not in ref_table_columns:
                        errors.append(CheckResult(
                            check_type='foreign_key_consistency',
                            table_name=table_name,
                            status=CheckStatus.ERROR,
                            message=f'参照先カラム {ref_table}.{ref_col_name} が存在しません',
                            severity='error'
                        ))
                        continue
                    
                    # データ型の一致チェック
                    if i < len(fk_columns):
                        fk_col_name = fk_columns[i]
                        
                        # 現在のテーブルのカラム定義を取得
                        current_columns = {col['name']: col for col in yaml_data.get('columns', [])}
                        if fk_col_name in current_columns:
                            fk_col_type = current_columns[fk_col_name].get('type', '').upper()
                            ref_col_type = ref_table_columns[ref_col_name].get('type', '').upper()
                            
                            if fk_col_type != ref_col_type:
                                errors.append(CheckResult(
                                    check_type='foreign_key_consistency',
                                    table_name=table_name,
                                    status=CheckStatus.ERROR,
                                    message=f'参照先カラムのデータ型が一致しません: {fk_col_name}({fk_col_type}) → {ref_table}.{ref_col_name}({ref_col_type})',
                                    severity='error'
                                ))
                
            except Exception as e:
                errors.append(CheckResult(
                    check_type='foreign_key_consistency',
                    table_name=table_name,
                    status=CheckStatus.ERROR,
                    message=f'参照先テーブル {ref_table} の読み込みエラー: {str(e)}',
                    severity='error'
                ))
        
        return errors
