"""
テーブル一覧解析機能
"""
import re
from pathlib import Path
from typing import List, Optional
from ..core.models import TableListEntry
from ..core.logger import ConsistencyLogger


class TableListParser:
    """テーブル一覧.mdファイルの解析"""
    
    def __init__(self, logger: Optional[ConsistencyLogger] = None):
        """
        パーサー初期化
        
        Args:
            logger: ログ機能
        """
        self.logger = logger or ConsistencyLogger()
    
    def parse_file(self, file_path: Path) -> List[TableListEntry]:
        """
        テーブル一覧ファイルを解析
        
        Args:
            file_path: テーブル一覧ファイルのパス
            
        Returns:
            テーブル一覧エントリのリスト
        """
        if not file_path.exists():
            self.logger.warning(f"テーブル一覧ファイルが見つかりません: {file_path}")
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_content(content)
            
        except Exception as e:
            self.logger.error(f"テーブル一覧ファイル解析エラー: {file_path} - {e}")
            return []
    
    def _parse_content(self, content: str) -> List[TableListEntry]:
        """
        テーブル一覧の内容を解析
        
        Args:
            content: ファイル内容
            
        Returns:
            テーブル一覧エントリのリスト
        """
        entries = []
        
        # マークダウンテーブルの行を抽出
        lines = content.split('\n')
        in_table = False
        header_found = False
        
        for line in lines:
            line = line.strip()
            
            # テーブルの開始を検出
            if '|' in line and ('テーブル名' in line or 'Table' in line):
                in_table = True
                header_found = True
                continue
            
            # ヘッダー区切り行をスキップ
            if in_table and header_found and re.match(r'^\|[\s\-\|]+\|$', line):
                continue
            
            # テーブル行を解析
            if in_table and line.startswith('|') and line.endswith('|'):
                entry = self._parse_table_row(line)
                if entry:
                    entries.append(entry)
            elif in_table and not line:
                # 空行でテーブル終了
                in_table = False
                header_found = False
        
        return entries
    
    def _parse_table_row(self, line: str) -> Optional[TableListEntry]:
        """
        テーブル行を解析
        
        Args:
            line: テーブル行
            
        Returns:
            テーブル一覧エントリ
        """
        try:
            # パイプで分割
            parts = [part.strip() for part in line.split('|')]
            
            # 最初と最後の空要素を除去
            if parts and not parts[0]:
                parts = parts[1:]
            if parts and not parts[-1]:
                parts = parts[:-1]
            
            if len(parts) < 2:
                return None
            
            table_name = parts[0].strip()
            description = parts[1].strip() if len(parts) > 1 else ""
            
            # テーブル名が空の場合はスキップ
            if not table_name or table_name in ['テーブル名', 'Table Name', 'Table']:
                return None
            
            return TableListEntry(
                table_name=table_name,
                description=description
            )
            
        except Exception as e:
            self.logger.warning(f"テーブル行解析エラー: {line} - {e}")
            return None
    
    def get_table_names(self, entries: List[TableListEntry]) -> List[str]:
        """
        テーブル名のリストを取得
        
        Args:
            entries: テーブル一覧エントリのリスト
            
        Returns:
            テーブル名のリスト
        """
        return [entry.table_name for entry in entries if entry.table_name]
    
    def find_table_by_name(self, entries: List[TableListEntry], table_name: str) -> Optional[TableListEntry]:
        """
        テーブル名でエントリを検索
        
        Args:
            entries: テーブル一覧エントリのリスト
            table_name: 検索するテーブル名
            
        Returns:
            見つかったテーブル一覧エントリ
        """
        for entry in entries:
            if entry.table_name == table_name:
                return entry
        return None
    
    def validate_table_names(self, entries: List[TableListEntry]) -> List[str]:
        """
        テーブル名の妥当性をチェック
        
        Args:
            entries: テーブル一覧エントリのリスト
            
        Returns:
            無効なテーブル名のリスト
        """
        invalid_names = []
        
        for entry in entries:
            table_name = entry.table_name
            
            # テーブル名の命名規則チェック
            if not re.match(r'^[A-Za-z][A-Za-z0-9_]*$', table_name):
                invalid_names.append(table_name)
        
        return invalid_names
    
    def get_statistics(self, entries: List[TableListEntry]) -> dict:
        """
        統計情報を取得
        
        Args:
            entries: テーブル一覧エントリのリスト
            
        Returns:
            統計情報
        """
        return {
            'total_tables': len(entries),
            'tables_with_description': sum(1 for e in entries if e.description),
            'tables_without_description': sum(1 for e in entries if not e.description),
            'table_name_prefixes': self._analyze_prefixes(entries)
        }
    
    def _analyze_prefixes(self, entries: List[TableListEntry]) -> dict:
        """
        テーブル名のプレフィックスを分析
        
        Args:
            entries: テーブル一覧エントリのリスト
            
        Returns:
            プレフィックス統計
        """
        prefixes = {}
        
        for entry in entries:
            table_name = entry.table_name
            
            # アンダースコアで分割してプレフィックスを抽出
            parts = table_name.split('_')
            if len(parts) > 1:
                prefix = parts[0]
                if prefix in prefixes:
                    prefixes[prefix] += 1
                else:
                    prefixes[prefix] = 1
        
        return prefixes
