"""
データベース整合性チェックツール - メインチェッカー
"""
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple
import logging
import yaml
import re
from datetime import datetime

# パス解決のセットアップ
_current_dir = Path(__file__).parent
_tools_dir = _current_dir.parent.parent
if str(_tools_dir) not in sys.path:
    sys.path.insert(0, str(_tools_dir))

# 絶対インポートを使用
from database_consistency_checker.core.models import (
    CheckResult, CheckSeverity, ConsistencyReport, CheckSummary,
    create_info_result, create_warning_result, create_error_result,
    create_success_result
)
from database_consistency_checker.core.config import Config
from database_consistency_checker.yaml_format_check_enhanced import YAMLFormatCheckEnhanced
from shared.path_resolver import PathResolver

class ConsistencyChecker:
    """データベース整合性チェックのメインエンジン"""
    
    def __init__(self, config: Config, check_config: Optional[Any] = None):
        """
        チェッカー初期化
        
        Args:
            config: 統合設定
            check_config: チェック実行設定
        """
        self.config = config
        self.check_config = check_config
        self.logger = logging.getLogger(__name__)
        # PathResolverは静的メソッドのみなのでインスタンス化不要
        
        # テーブル情報を格納
        self.tables: Dict[str, Dict[str, Any]] = {}
        self.yaml_data: Dict[str, Dict[str, Any]] = {}
        self.ddl_data: Dict[str, str] = {}
        self.definition_data: Dict[str, str] = {}
        
        # 除外テーブルリストを設定
        self.excluded_tables = set(config.default_excluded_tables)
        if check_config and hasattr(check_config, 'excluded_tables') and check_config.excluded_tables:
            self.excluded_tables.update(check_config.excluded_tables)
        
    def _load_table_data(self) -> None:
        """テーブルデータを読み込む"""
        self.logger.info("テーブルデータの読み込みを開始")
        
        # YAMLファイルの読み込み
        yaml_dir = PathResolver.get_table_details_dir()
        if yaml_dir.exists():
            for yaml_file in yaml_dir.glob("*.yaml"):
                table_name = yaml_file.stem.replace("_details", "")
                
                # 除外テーブルをスキップ
                if table_name in self.excluded_tables:
                    self.logger.debug(f"除外テーブルをスキップ: {table_name}")
                    continue
                
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        self.yaml_data[table_name] = yaml.safe_load(f)
                        self.tables[table_name] = {"yaml": True}
                except Exception as e:
                    self.logger.error(f"YAMLファイル読み込みエラー {yaml_file}: {e}")
        
        # DDLファイルの読み込み
        ddl_dir = PathResolver.get_ddl_dir()
        if ddl_dir.exists():
            for ddl_file in ddl_dir.glob("*.sql"):
                if ddl_file.name == "all_tables.sql":
                    continue
                table_name = ddl_file.stem
                
                # 除外テーブルをスキップ
                if table_name in self.excluded_tables:
                    self.logger.debug(f"除外テーブルをスキップ: {table_name}")
                    continue
                
                try:
                    with open(ddl_file, 'r', encoding='utf-8') as f:
                        self.ddl_data[table_name] = f.read()
                        if table_name in self.tables:
                            self.tables[table_name]["ddl"] = True
                        else:
                            self.tables[table_name] = {"ddl": True}
                except Exception as e:
                    self.logger.error(f"DDLファイル読み込みエラー {ddl_file}: {e}")
        
        # 定義書ファイルの読み込み
        definition_dir = PathResolver.get_tables_dir()
        if definition_dir.exists():
            for def_file in definition_dir.glob("テーブル定義書_*.md"):
                # ファイル名からテーブル名を抽出
                match = re.match(r"テーブル定義書_(.+?)_.*\.md", def_file.name)
                if match:
                    table_name = match.group(1)
                    
                    # 除外テーブルをスキップ
                    if table_name in self.excluded_tables:
                        self.logger.debug(f"除外テーブルをスキップ: {table_name}")
                        continue
                    
                    try:
                        with open(def_file, 'r', encoding='utf-8') as f:
                            self.definition_data[table_name] = f.read()
                            if table_name in self.tables:
                                self.tables[table_name]["definition"] = True
                            else:
                                self.tables[table_name] = {"definition": True}
                    except Exception as e:
                        self.logger.error(f"定義書ファイル読み込みエラー {def_file}: {e}")
        
        excluded_count = len(self.excluded_tables)
        self.logger.info(f"読み込み完了: {len(self.tables)}テーブル (除外: {excluded_count}テーブル)")
        if self.excluded_tables:
            self.logger.info(f"除外テーブル: {', '.join(sorted(self.excluded_tables))}")
    
    def _check_table_existence(self) -> List[CheckResult]:
        """テーブル存在確認チェック"""
        results = []
        
        for table_name, files in self.tables.items():
            missing_files = []
            
            if not files.get("yaml"):
                missing_files.append("YAML詳細定義")
            if not files.get("ddl"):
                missing_files.append("DDL")
            if not files.get("definition"):
                missing_files.append("テーブル定義書")
            
            if missing_files:
                results.append(create_warning_result(
                    check_name="table_existence",
                    message=f"{table_name}: 不足ファイル - {', '.join(missing_files)}",
                    metadata={
                        "table": table_name,
                        "missing_files": missing_files
                    }
                ))
            else:
                results.append(create_success_result(
                    check_name="table_existence",
                    message=f"{table_name}: 全ファイル存在確認OK"
                ))
        
        return results
    
    def _check_column_consistency(self) -> List[CheckResult]:
        """カラム整合性チェック"""
        results = []
        
        for table_name in self.tables:
            if table_name not in self.yaml_data:
                continue
                
            yaml_columns = set()
            if "columns" in self.yaml_data[table_name]:
                yaml_columns = {col["name"] for col in self.yaml_data[table_name]["columns"]}
            
            # DDLからカラムを抽出
            ddl_columns = set()
            if table_name in self.ddl_data:
                ddl_content = self.ddl_data[table_name]
                # 簡易的なカラム抽出（CREATE TABLE文から）
                column_pattern = r'^\s*(\w+)\s+\w+.*(?:,|$)'
                for line in ddl_content.split('\n'):
                    if 'CREATE TABLE' in line or 'PRIMARY KEY' in line or 'FOREIGN KEY' in line:
                        continue
                    match = re.match(column_pattern, line)
                    if match:
                        ddl_columns.add(match.group(1))
            
            # 差分チェック
            if yaml_columns and ddl_columns:
                yaml_only = yaml_columns - ddl_columns
                ddl_only = ddl_columns - yaml_columns
                
                if yaml_only or ddl_only:
                    details = {}
                    if yaml_only:
                        details["yaml_only"] = list(yaml_only)
                    if ddl_only:
                        details["ddl_only"] = list(ddl_only)
                    
                    results.append(create_warning_result(
                        check_name="column_consistency",
                        message=f"{table_name}: カラム定義の不一致",
                        metadata=details
                    ))
                else:
                    results.append(create_success_result(
                        check_name="column_consistency",
                        message=f"{table_name}: カラム定義一致"
                    ))
        
        return results
    
    def _check_foreign_keys(self) -> List[CheckResult]:
        """外部キー整合性チェック"""
        results = []
        
        for table_name, yaml_data in self.yaml_data.items():
            if "foreign_keys" not in yaml_data:
                continue
            
            for fk in yaml_data["foreign_keys"]:
                ref_table = fk.get("references", {}).get("table")
                ref_columns = fk.get("references", {}).get("columns", [])
                
                # ref_tableがリストの場合は最初の要素を使用
                if isinstance(ref_table, list):
                    ref_table = ref_table[0] if ref_table else None
                
                if ref_table and ref_table not in self.tables:
                    results.append(create_error_result(
                        check_name="foreign_key_consistency",
                        message=f"{table_name}: 参照先テーブル '{ref_table}' が存在しません",
                        metadata={
                            "table": table_name,
                            "foreign_key": fk.get("name"),
                            "missing_table": ref_table
                        }
                    ))
                elif ref_table in self.yaml_data:
                    # 参照先カラムの存在確認
                    ref_yaml = self.yaml_data[ref_table]
                    
                    # columnsとbusiness_columnsの両方からカラム名を取得
                    ref_column_names = set()
                    
                    # 標準のcolumnsセクション
                    if "columns" in ref_yaml:
                        ref_column_names.update(col["name"] for col in ref_yaml["columns"])
                    
                    # business_columnsセクション
                    if "business_columns" in ref_yaml:
                        ref_column_names.update(col["name"] for col in ref_yaml["business_columns"])
                    
                    missing_columns = [col for col in ref_columns if col not in ref_column_names]
                    if missing_columns:
                        results.append(create_error_result(
                            check_name="foreign_key_consistency",
                            message=f"{table_name}: 参照先カラムが存在しません",
                            metadata={
                                "table": table_name,
                                "foreign_key": fk.get("name"),
                                "reference_table": ref_table,
                                "missing_columns": missing_columns,
                                "available_columns": list(ref_column_names)
                            }
                        ))
                    else:
                        results.append(create_success_result(
                            check_name="foreign_key_consistency",
                            message=f"{table_name}: 外部キー '{fk.get('name')}' OK"
                        ))
        
        return results
    
    def _check_naming_conventions(self) -> List[CheckResult]:
        """命名規則チェック"""
        results = []
        
        # テーブル名の命名規則チェック
        table_pattern = re.compile(r'^(MST|TRN|HIS|SYS|WRK)_[A-Z][a-zA-Z0-9]*$')
        
        for table_name in self.tables:
            if not table_pattern.match(table_name):
                results.append(create_warning_result(
                    check_name="naming_convention",
                    message=f"{table_name}: テーブル名が命名規則に準拠していません",
                    metadata={
                        "table": table_name,
                        "expected_pattern": "PREFIX_TableName (PREFIX: MST/TRN/HIS/SYS/WRK)"
                    }
                ))
            else:
                results.append(create_success_result(
                    check_name="naming_convention",
                    message=f"{table_name}: テーブル名命名規則OK"
                ))
        
        # カラム名の命名規則チェック
        column_pattern = re.compile(r'^[a-z][a-z0-9_]*$')
        
        for table_name, yaml_data in self.yaml_data.items():
            if "columns" not in yaml_data:
                continue
            
            invalid_columns = []
            for column in yaml_data["columns"]:
                column_name = column.get("name", "")
                if not column_pattern.match(column_name):
                    invalid_columns.append(column_name)
            
            if invalid_columns:
                results.append(create_warning_result(
                    check_name="naming_convention",
                    message=f"{table_name}: カラム名が命名規則に準拠していません",
                    metadata={
                        "table": table_name,
                        "invalid_columns": invalid_columns,
                        "expected_pattern": "snake_case (小文字とアンダースコア)"
                    }
                ))
        
        return results
    
    def _check_yaml_format(self) -> List[CheckResult]:
        """YAML形式・必須セクションチェック"""
        results = []
        
        try:
            # YAMLFormatCheckEnhancedを初期化（configのベースディレクトリを使用）
            yaml_checker = YAMLFormatCheckEnhanced(
                base_dir=str(self.config.base_dir),
                verbose=getattr(self.check_config, 'verbose', False)
            )
            
            # 対象テーブルの設定
            target_tables = None
            if self.check_config and hasattr(self.check_config, 'target_tables'):
                target_tables = self.check_config.target_tables
            
            # デバッグ情報を出力
            if getattr(self.check_config, 'verbose', False):
                self.logger.info(f"YAML検証ベースディレクトリ: {self.config.base_dir}")
                self.logger.info(f"テーブル詳細ディレクトリ: {PathResolver.get_table_details_dir()}")
                self.logger.info(f"対象テーブル: {target_tables}")
            
            # YAML検証実行
            yaml_results = yaml_checker.validate_yaml_format(target_tables)
            
            # 結果をConsistencyCheckerの形式に変換
            if isinstance(yaml_results, dict) and 'files' in yaml_results:
                # 正常な結果の場合
                for table_name, table_result in yaml_results['files'].items():
                    if table_result['success']:
                        results.append(create_success_result(
                            check_name="yaml_format",
                            message=f"{table_name}: YAML形式・必須セクション検証OK"
                        ))
                    else:
                        # エラーの重要度を判定
                        has_critical_errors = any(
                            'revision_history' in error or 'overview' in error or 
                            'notes' in error or 'rules' in error
                            for error in table_result['errors']
                        )
                        
                        severity_func = create_error_result if has_critical_errors else create_warning_result
                        
                        results.append(severity_func(
                            check_name="yaml_format",
                            message=f"{table_name}: YAML形式・必須セクション検証エラー",
                            metadata={
                                "table": table_name,
                                "errors": table_result['errors'],
                                "warnings": table_result.get('warnings', [])
                            }
                        ))
            else:
                # エラーが発生した場合
                error_msg = yaml_results.get('error', 'YAML検証で不明なエラーが発生しました') if isinstance(yaml_results, dict) else str(yaml_results)
                results.append(create_error_result(
                    check_name="yaml_format",
                    message=f"YAML検証エラー: {error_msg}",
                    metadata={"error": error_msg}
                ))
            
        except Exception as e:
            self.logger.error(f"YAML形式チェックエラー: {e}")
            results.append(create_error_result(
                check_name="yaml_format",
                message=f"YAML形式チェック実行エラー: {e}",
                metadata={"error": str(e)}
            ))
        
        return results
    
    def run_all_checks(self) -> ConsistencyReport:
        """
        全ての整合性チェックを実行
        
        Returns:
            整合性チェックレポート
        """
        self.logger.info("整合性チェック開始")
        
        # データ読み込み
        self._load_table_data()
        
        # 各種チェックを実行
        results = []
        
        # テーブル存在確認
        results.extend(self._check_table_existence())
        
        # YAML形式・必須セクションチェック
        results.extend(self._check_yaml_format())
        
        # カラム整合性チェック
        results.extend(self._check_column_consistency())
        
        # 外部キー整合性チェック
        results.extend(self._check_foreign_keys())
        
        # 命名規則チェック
        results.extend(self._check_naming_conventions())
        
        # サマリー集計
        summary = {
            'success': sum(1 for r in results if r.severity == CheckSeverity.SUCCESS),
            'info': sum(1 for r in results if r.severity == CheckSeverity.INFO),
            'warning': sum(1 for r in results if r.severity == CheckSeverity.WARNING),
            'error': sum(1 for r in results if r.severity == CheckSeverity.ERROR)
        }
        
        # ConsistencyReportを作成
        report = ConsistencyReport()
        report.summary = summary
        report.results = results
        report.tables = list(self.tables.keys())
        report.fix_suggestions = self._generate_fix_suggestions(results)
        report.metadata = {'tool_version': '1.0.0'}
        report.generated_at = datetime.now()
        report.check_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report.total_tables = len(self.tables)
        report.total_checks = len(results)
        
        self.logger.info(f"整合性チェック完了: {len(self.tables)}テーブル, {len(results)}チェック")
        return report
    
    def _generate_fix_suggestions(self, results: List[CheckResult]) -> List[Dict[str, Any]]:
        """修正提案を生成"""
        suggestions = []
        
        for result in results:
            if result.severity in [CheckSeverity.WARNING, CheckSeverity.ERROR]:
                if result.check_name == "table_existence":
                    missing_files = result.metadata.get("missing_files", [])
                    table = result.metadata.get("table", "")
                    
                    for file_type in missing_files:
                        if file_type == "YAML詳細定義":
                            suggestions.append({
                                "table": table,
                                "issue": f"{file_type}が不足",
                                "suggestion": f"python3 -m table_generator --table {table} --generate yaml",
                                "severity": "warning"
                            })
                        elif file_type == "DDL":
                            suggestions.append({
                                "table": table,
                                "issue": f"{file_type}が不足",
                                "suggestion": f"python3 -m table_generator --table {table} --generate ddl",
                                "severity": "warning"
                            })
                        elif file_type == "テーブル定義書":
                            suggestions.append({
                                "table": table,
                                "issue": f"{file_type}が不足",
                                "suggestion": f"python3 -m table_generator --table {table} --generate definition",
                                "severity": "warning"
                            })
                
                elif result.check_name == "foreign_key_consistency":
                    suggestions.append({
                        "table": result.metadata.get("table", ""),
                        "issue": result.message,
                        "suggestion": "参照先テーブルまたはカラムを作成するか、外部キー定義を修正してください",
                        "severity": "error"
                    })
        
        return suggestions
    
    def run_specific_checks(self, check_names: List[str]) -> ConsistencyReport:
        """
        指定されたチェックのみを実行
        
        Args:
            check_names: 実行するチェック名のリスト
            
        Returns:
            整合性チェックレポート
        """
        # 現在は全チェックを実行
        return self.run_all_checks()
    
    def get_available_checks(self) -> List[str]:
        """利用可能なチェック名のリストを取得"""
        return [
            "table_existence",
            "yaml_format",
            "column_consistency", 
            "foreign_key_consistency",
            "naming_convention"
        ]
    
    def validate_check_names(self, check_names: List[str]) -> List[str]:
        """
        チェック名の妥当性を検証
        
        Args:
            check_names: チェック名のリスト
            
        Returns:
            無効なチェック名のリスト
        """
        available_checks = self.get_available_checks()
        return [name for name in check_names if name not in available_checks]
