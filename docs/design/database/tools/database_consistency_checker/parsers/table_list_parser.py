"""
データベース整合性チェックツール - テーブル一覧.md解析
"""
import re
from pathlib import Path
from typing import List, Dict, Optional
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
        テーブル一覧.mdファイルを解析
        
        Args:
            file_path: ファイルパス
            
        Returns:
            テーブル一覧エントリのリスト
        """
        if not file_path.exists():
            self.logger.error(f"テーブル一覧ファイルが見つかりません: {file_path}")
            return []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_markdown_table(content)
            
        except Exception as e:
            self.logger.error(f"テーブル一覧ファイルの読み込みエラー: {e}")
            return []
    
    def _parse_markdown_table(self, content: str) -> List[TableListEntry]:
        """
        Markdownテーブルを解析
        
        Args:
            content: ファイル内容
            
        Returns:
            テーブル一覧エントリのリスト
        """
        entries = []
        
        # テーブル行を抽出（|で始まり|で終わる行）
        table_lines = []
        in_table = False
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('|') and line.endswith('|'):
                if 'テーブルID' in line or 'table_id' in line.lower():
                    in_table = True
                    continue  # ヘッダー行をスキップ
                elif line.startswith('|---') or line.startswith('|--'):
                    continue  # 区切り行をスキップ
                elif in_table:
                    table_lines.append(line)
            elif in_table and line == '':
                # 空行でテーブル終了
                break
        
        # 各行を解析
        for line_num, line in enumerate(table_lines, 1):
            try:
                entry = self._parse_table_row(line)
                if entry:
                    entries.append(entry)
            except Exception as e:
                self.logger.warning(f"テーブル一覧の行解析エラー (行{line_num}): {e}")
                continue
        
        self.logger.info(f"テーブル一覧から {len(entries)} 件のテーブルを解析しました")
        return entries
    
    def _parse_table_row(self, line: str) -> Optional[TableListEntry]:
        """
        テーブル行を解析
        
        Args:
            line: テーブル行
            
        Returns:
            テーブル一覧エントリ
        """
        # |で分割してセルを取得
        cells = [cell.strip() for cell in line.split('|')[1:-1]]  # 最初と最後の空要素を除去
        
        if len(cells) < 4:
            return None
        
        # 基本情報の抽出
        table_id = cells[0] if len(cells) > 0 else ""
        category = cells[1] if len(cells) > 1 else ""
        table_name = cells[2] if len(cells) > 2 else ""
        logical_name = cells[3] if len(cells) > 3 else ""
        
        # 優先度の抽出（7番目のカラム）
        priority = cells[7] if len(cells) > 7 else "中"
        
        # 個人情報含有の判定（16番目のカラム）
        personal_info = False
        if len(cells) > 15:
            personal_info_text = cells[15].lower()
            personal_info = personal_info_text in ['あり', 'true', 'yes', '○']
        
        # 暗号化要否の判定（18番目のカラム）
        encryption_required = False
        if len(cells) > 17:
            encryption_text = cells[17].lower()
            encryption_required = encryption_text in ['要', 'required', 'true', 'yes', '○']
        
        return TableListEntry(
            table_id=table_id,
            category=category,
            table_name=table_name,
            logical_name=logical_name,
            priority=priority,
            personal_info=personal_info,
            encryption_required=encryption_required
        )
    
    def get_table_names(self, entries: List[TableListEntry]) -> List[str]:
        """
        テーブル名のリストを取得
        
        Args:
            entries: テーブル一覧エントリ
            
        Returns:
            テーブル名のリスト
        """
        return [entry.table_name for entry in entries if entry.table_name]
    
    def get_tables_by_category(self, entries: List[TableListEntry]) -> Dict[str, List[str]]:
        """
        カテゴリ別のテーブル名を取得
        
        Args:
            entries: テーブル一覧エントリ
            
        Returns:
            カテゴリ別テーブル名辞書
        """
        category_tables = {}
        
        for entry in entries:
            if entry.category not in category_tables:
                category_tables[entry.category] = []
            category_tables[entry.category].append(entry.table_name)
        
        return category_tables
    
    def get_high_priority_tables(self, entries: List[TableListEntry]) -> List[str]:
        """
        高優先度テーブルを取得
        
        Args:
            entries: テーブル一覧エントリ
            
        Returns:
            高優先度テーブル名のリスト
        """
        high_priority = ['最高', '高', 'high', 'critical']
        return [
            entry.table_name for entry in entries 
            if entry.priority.lower() in [p.lower() for p in high_priority]
        ]
    
    def get_personal_info_tables(self, entries: List[TableListEntry]) -> List[str]:
        """
        個人情報含有テーブルを取得
        
        Args:
            entries: テーブル一覧エントリ
            
        Returns:
            個人情報含有テーブル名のリスト
        """
        return [entry.table_name for entry in entries if entry.personal_info]
    
    def get_encryption_required_tables(self, entries: List[TableListEntry]) -> List[str]:
        """
        暗号化要求テーブルを取得
        
        Args:
            entries: テーブル一覧エントリ
            
        Returns:
            暗号化要求テーブル名のリスト
        """
        return [entry.table_name for entry in entries if entry.encryption_required]
