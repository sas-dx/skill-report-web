"""
データベース整合性チェックツール - テーブル存在チェック
"""
from pathlib import Path
from typing import List, Dict, Set, Optional
from ..core.models import CheckResult, CheckSeverity, TableListEntry
from ..core.logger import ConsistencyLogger
from ..parsers.table_list_parser import TableListParser
from ..parsers.entity_yaml_parser import EntityYamlParser
from ..parsers.ddl_parser import DDLParser


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
        self.ddl_parser = DDLParser(logger)
    
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
        
        if missing_sources:
            if len(missing_sources) == len(existence_pattern):
                # 全てのソースに存在しない（通常は発生しない）
                results.append(CheckResult(
                    check_name="table_existence",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="テーブルがどのソースにも存在しません",
                    details=existence_pattern
                ))
            elif 'table_list' in missing_sources:
                # テーブル一覧に存在しない
                results.append(CheckResult(
                    check_name="table_existence",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="テーブル一覧.mdに定義されていません",
                    details={'missing_sources': missing_sources}
                ))
            elif 'ddl' in missing_sources:
                # DDLファイルが存在しない
                results.append(CheckResult(
                    check_name="table_existence",
                    table_name=table_name,
                    severity=CheckSeverity.ERROR,
                    message="DDLファイルが存在しません",
                    details={'missing_sources': missing_sources}
                ))
            elif 'details' in missing_sources:
                # 詳細定義ファイルが存在しない
                results.append(CheckResult(
                    check_name="table_existence",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message="テーブル詳細定義ファイルが存在しません",
                    details={'missing_sources': missing_sources}
                ))
            elif 'entity' in missing_sources:
                # エンティティ関連定義に存在しない
                results.append(CheckResult(
                    check_name="table_existence",
                    table_name=table_name,
                    severity=CheckSeverity.WARNING,
                    message="エンティティ関連定義に存在しません",
                    details={'missing_sources': missing_sources}
                ))
        else:
            # 全てのソースに存在する
            results.append(CheckResult(
                check_name="table_existence",
                table_name=table_name,
                severity=CheckSeverity.SUCCESS,
                message="全てのソースに存在します",
                details=existence_pattern
            ))
        
        return results
    
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
