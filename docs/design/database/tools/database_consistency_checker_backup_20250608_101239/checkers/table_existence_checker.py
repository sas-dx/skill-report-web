"""
データベース整合性チェックツール - テーブル存在チェック
"""
from pathlib import Path
from typing import List, Dict, Set, Optional
from core.models import CheckResult, CheckSeverity, TableListEntry
from core.logger import ConsistencyLogger
from parsers.table_list_parser import TableListParser
from parsers.entity_yaml_parser import EntityYamlParser
from parsers.ddl_parser import DDLParser


class TableExistenceChecker:
    """テーブル存在整合性チェック"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        """
        チェッカー初期化
        
        Args:
            logger: ログ機能
        """
        self.logger = logger or ConsistencyLogger()
        self.table_list_parser = TableListParser(logger)
        self.entity_parser = EntityYamlParser(logger)
        self.ddl_parser = DDLParser(self.logger)
    
    def check_table_existence(
        self,
        table_list_file: Path,
        entity_file: Path,
        ddl_dir: Path,
        table_details_dir: Path,
        target_tables: List[str] = None
    ) -> List[CheckResult]:
        """
        テーブル存在整合性をチェック
        
        Args:
            table_list_file: テーブル一覧ファイル
            entity_file: エンティティ関連ファイル
            ddl_dir: DDLディレクトリ
            table_details_dir: テーブル詳細ディレクトリ
            target_tables: 対象テーブル（指定時のみチェック）
            
        Returns:
            チェック結果のリスト
        """
        results = []
        
        self.logger.section("テーブル存在整合性チェック")
        
        # 各ソースからテーブル名を取得
        table_list_tables = self._get_table_list_tables(table_list_file)
        entity_tables = self._get_entity_tables(entity_file)
        ddl_tables = self._get_ddl_tables(ddl_dir)
        detail_tables = self._get_detail_tables(table_details_dir)
        
        # 対象テーブルでフィルタリング
        if target_tables:
            table_list_tables = {t for t in table_list_tables if t in target_tables}
            entity_tables = {t for t in entity_tables if t in target_tables}
            ddl_tables = {t for t in ddl_tables if t in target_tables}
            detail_tables = {t for t in detail_tables if t in target_tables}
        
        # 全テーブルの統合
        all_tables = table_list_tables | entity_tables | ddl_tables | detail_tables
        
        self.logger.info(f"チェック対象テーブル数: {len(all_tables)}")
        
        # 各テーブルの存在チェック
        for i, table_name in enumerate(sorted(all_tables), 1):
            self.logger.progress(i, len(all_tables), f"チェック中: {table_name}")
            
            table_results = self._check_single_table_existence(
                table_name,
                table_list_tables,
                entity_tables,
                ddl_tables,
                detail_tables
            )
            results.extend(table_results)
        
        # サマリー情報
        error_count = sum(1 for r in results if r.severity == CheckSeverity.ERROR)
        warning_count = sum(1 for r in results if r.severity == CheckSeverity.WARNING)
        
        self.logger.info(f"テーブル存在チェック完了: エラー {error_count}件, 警告 {warning_count}件")
        
        return results
    
    def _get_table_list_tables(self, file_path: Path) -> Set[str]:
        """テーブル一覧からテーブル名を取得"""
        if not file_path.exists():
            self.logger.warning(f"テーブル一覧ファイルが見つかりません: {file_path}")
            return set()
        
        entries = self.table_list_parser.parse_file(file_path)
        return set(self.table_list_parser.get_table_names(entries))
    
    def _get_entity_tables(self, file_path: Path) -> Set[str]:
        """エンティティ関連ファイルからテーブル名を取得"""
        if not file_path.exists():
            self.logger.warning(f"エンティティ関連ファイルが見つかりません: {file_path}")
            return set()
        
        data = self.entity_parser.parse_file(file_path)
        return set(self.entity_parser.get_entity_names(data))
    
    def _get_ddl_tables(self, ddl_dir: Path) -> Set[str]:
        """DDLディレクトリからテーブル名を取得"""
        if not ddl_dir.exists():
            self.logger.warning(f"DDLディレクトリが見つかりません: {ddl_dir}")
            return set()
        
        tables = set()
        ddl_files = list(ddl_dir.glob("*.sql"))
        
        for ddl_file in ddl_files:
            # 特殊ファイルをスキップ
            if ddl_file.name in ['all_tables.sql', '------------.sql']:
                continue
            
            table_name = self.ddl_parser.get_table_name_from_file(ddl_file)
            if table_name:
                tables.add(table_name)
        
        return tables
    
    def _get_detail_tables(self, details_dir: Path) -> Set[str]:
        """テーブル詳細ディレクトリからテーブル名を取得"""
        if not details_dir.exists():
            self.logger.warning(f"テーブル詳細ディレクトリが見つかりません: {details_dir}")
            return set()
        
        tables = set()
        yaml_files = list(details_dir.glob("*.yaml"))
        
        for yaml_file in yaml_files:
            # テンプレートファイルをスキップ
            if yaml_file.name.startswith('_TEMPLATE_'):
                continue
            
            # ファイル名からテーブル名を抽出
            table_name = yaml_file.stem.replace('_details', '')
            tables.add(table_name)
        
        return tables
    
    def _check_single_table_existence(
        self,
        table_name: str,
        table_list_tables: Set[str],
        entity_tables: Set[str],
        ddl_tables: Set[str],
        detail_tables: Set[str]
    ) -> List[CheckResult]:
        """単一テーブルの存在チェック"""
        results = []
        
        # 各ソースでの存在確認
        in_table_list = table_name in table_list_tables
        in_entity = table_name in entity_tables
        in_ddl = table_name in ddl_tables
        in_details = table_name in detail_tables
        
        # 存在パターンの分析
        existence_pattern = {
            'table_list': in_table_list,
            'entity': in_entity,
            'ddl': in_ddl,
            'details': in_details
        }
        
        missing_sources = [source for source, exists in existence_pattern.items() if not exists]
        present_sources = [source for source, exists in existence_pattern.items() if exists]
        
        if missing_sources:
            if len(missing_sources) == len(existence_pattern):
                # 全てのソースに存在しない（通常は発生しない）
                results.append(CheckResult(
                    check_name="table_existence",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="テーブルがどのソースにも存在しません",
                    details={
                        'existence_pattern': existence_pattern,
                        'missing_sources': missing_sources,
                        'present_sources': present_sources
                    }
                ))
            else:
                # 具体的な不整合メッセージを生成
                detailed_message = self._generate_detailed_existence_message(
                    table_name, existence_pattern, missing_sources, present_sources
                )
                
                # 重要度を判定
                severity = self._determine_existence_severity(missing_sources)
                
                results.append(CheckResult(
                    check_name="table_existence",
                    table_name=table_name,
                    severity=severity,
                    message=detailed_message,
                    details={
                        'existence_pattern': existence_pattern,
                        'missing_sources': missing_sources,
                        'present_sources': present_sources,
                        'expected_files': self._get_expected_files(table_name, missing_sources),
                        'fix_suggestions': self._get_existence_fix_suggestions(table_name, missing_sources)
                    }
                ))
        else:
            # 全てのソースに存在する
            results.append(CheckResult(
                check_name="table_existence",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message="全てのソースに存在します",
                details={
                    'existence_pattern': existence_pattern,
                    'all_sources_present': True
                }
            ))
        
        return results
    
    def _generate_detailed_existence_message(
        self,
        table_name: str,
        existence_pattern: Dict[str, bool],
        missing_sources: List[str],
        present_sources: List[str]
    ) -> str:
        """詳細な存在チェックメッセージを生成"""
        source_names = {
            'table_list': 'テーブル一覧.md',
            'entity': 'entity_relationships.yaml',
            'ddl': 'DDLファイル',
            'details': 'テーブル詳細YAML'
        }
        
        # 存在する場所と存在しない場所を明確に示す
        present_list = [source_names[source] for source in present_sources]
        missing_list = [source_names[source] for source in missing_sources]
        
        message_parts = []
        
        if present_list:
            message_parts.append(f"存在: {', '.join(present_list)}")
        
        if missing_list:
            message_parts.append(f"不足: {', '.join(missing_list)}")
        
        return f"テーブル定義の不整合 - {' | '.join(message_parts)}"
    
    def _determine_existence_severity(self, missing_sources: List[str]) -> CheckSeverity:
        """存在チェックの重要度を判定"""
        # テーブル一覧またはDDLファイルが不足している場合はエラー
        if 'table_list' in missing_sources or 'ddl' in missing_sources:
            return CheckSeverity.ERROR
        
        # その他の場合は警告
        return CheckSeverity.WARNING
    
    def _get_expected_files(self, table_name: str, missing_sources: List[str]) -> Dict[str, str]:
        """期待されるファイル名を取得"""
        expected_files = {}
        
        if 'ddl' in missing_sources:
            expected_files['ddl'] = f"{table_name}.sql"
        
        if 'details' in missing_sources:
            expected_files['details'] = f"{table_name}_details.yaml"
        
        return expected_files
    
    def _get_existence_fix_suggestions(self, table_name: str, missing_sources: List[str]) -> List[str]:
        """存在チェックの修正提案を生成"""
        suggestions = []
        
        if 'table_list' in missing_sources:
            suggestions.append(f"テーブル一覧.mdに'{table_name}'を追加してください")
        
        if 'ddl' in missing_sources:
            suggestions.append(f"DDLファイル'{table_name}.sql'を作成してください")
        
        if 'details' in missing_sources:
            suggestions.append(f"テーブル詳細YAML'{table_name}_details.yaml'を作成してください")
        
        if 'entity' in missing_sources:
            suggestions.append(f"entity_relationships.yamlに'{table_name}'の関連定義を追加してください")
        
        return suggestions
    
    def get_orphaned_files(
        self,
        table_list_file: Path,
        ddl_dir: Path,
        table_details_dir: Path
    ) -> Dict[str, List[str]]:
        """
        孤立ファイルを検出
        
        Args:
            table_list_file: テーブル一覧ファイル
            ddl_dir: DDLディレクトリ
            table_details_dir: テーブル詳細ディレクトリ
            
        Returns:
            孤立ファイルの辞書
        """
        orphaned = {
            'ddl_files': [],
            'detail_files': []
        }
        
        # テーブル一覧からテーブル名を取得
        table_list_tables = self._get_table_list_tables(table_list_file)
        
        # DDLファイルの孤立チェック
        ddl_files = list(ddl_dir.glob("*.sql"))
        for ddl_file in ddl_files:
            if ddl_file.name in ['all_tables.sql', '------------.sql']:
                continue
            
            table_name = self.ddl_parser.get_table_name_from_file(ddl_file)
            if table_name and table_name not in table_list_tables:
                orphaned['ddl_files'].append(ddl_file.name)
        
        # 詳細定義ファイルの孤立チェック
        yaml_files = list(table_details_dir.glob("*.yaml"))
        for yaml_file in yaml_files:
            if yaml_file.name.startswith('_TEMPLATE_'):
                continue
            
            table_name = yaml_file.stem.replace('_details', '')
            if table_name not in table_list_tables:
                orphaned['detail_files'].append(yaml_file.name)
        
        return orphaned
