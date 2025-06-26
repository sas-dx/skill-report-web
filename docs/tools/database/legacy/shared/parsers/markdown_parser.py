"""
Markdownパーサー

Markdownファイルの解析を行う
"""

import re
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

from ..core.exceptions import ParsingError

logger = logging.getLogger(__name__)


class MarkdownParser:
    """Markdownパーサー"""
    
    def __init__(self):
        """初期化"""
        pass
    
    def parse_file(self, file_path: str) -> Dict[str, Any]:
        """
        Markdownファイルを解析
        
        Args:
            file_path: ファイルパス
            
        Returns:
            Dict[str, Any]: 解析結果
            
        Raises:
            ParseError: 解析エラー
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self.parse_content(content)
            
        except Exception as e:
            logger.error(f"Markdownファイル解析エラー: {file_path}, {e}")
            raise ParsingError(f"Markdownファイル解析に失敗しました: {e}")
    
    def parse_content(self, content: str) -> Dict[str, Any]:
        """
        Markdownコンテンツを解析
        
        Args:
            content: Markdownコンテンツ
            
        Returns:
            Dict[str, Any]: 解析結果
        """
        try:
            result = {
                'table_name': '',
                'logical_name': '',
                'category': '',
                'priority': '',
                'requirement_id': '',
                'columns': []
            }
            
            lines = content.split('\n')
            
            # テーブル名と論理名を抽出
            for line in lines:
                if line.startswith('# テーブル定義書'):
                    # テーブル定義書_MST_Employee_社員基本情報
                    parts = line.split('_')
                    if len(parts) >= 3:
                        result['table_name'] = parts[1]
                        result['logical_name'] = '_'.join(parts[2:])
                    break
            
            # テーブル情報を抽出
            in_table_info = False
            for line in lines:
                if '## テーブル情報' in line:
                    in_table_info = True
                    continue
                
                if in_table_info and line.startswith('|'):
                    # テーブル情報の行を解析
                    if 'カテゴリ' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            result['category'] = parts[2].strip()
                    elif '優先度' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            result['priority'] = parts[2].strip()
                    elif '要求仕様ID' in line:
                        parts = line.split('|')
                        if len(parts) >= 3:
                            result['requirement_id'] = parts[2].strip()
                
                if in_table_info and line.startswith('##') and 'テーブル情報' not in line:
                    in_table_info = False
            
            # カラム定義を抽出
            in_column_table = False
            for line in lines:
                if '## カラム定義' in line:
                    in_column_table = True
                    continue
                
                if in_column_table and line.startswith('|') and not line.startswith('|---'):
                    # ヘッダー行をスキップ
                    if 'カラム名' in line:
                        continue
                    
                    # カラム定義行を解析
                    parts = [part.strip() for part in line.split('|')[1:-1]]  # 最初と最後の空要素を除去
                    
                    if len(parts) >= 6:
                        column = {
                            'name': parts[0],
                            'type': parts[1],
                            'nullable': parts[2].lower() not in ['not null', 'no', 'false'],
                            'primary_key': parts[3].lower() in ['yes', 'true', 'pk'],
                            'default': parts[4] if parts[4] and parts[4] != '-' else None,
                            'comment': parts[5],
                            'requirement_id': parts[6] if len(parts) > 6 else ''
                        }
                        result['columns'].append(column)
                
                if in_column_table and line.startswith('##') and 'カラム定義' not in line:
                    in_column_table = False
            
            return result
            
        except Exception as e:
            logger.error(f"Markdownコンテンツ解析エラー: {e}")
            raise ParsingError(f"Markdownコンテンツ解析に失敗しました: {e}")
