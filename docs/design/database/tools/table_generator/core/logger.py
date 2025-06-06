#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テーブル生成ツール - ログ機能

カラー出力対応の強化されたログ機能を提供します。

対応要求仕様ID: PLT.2-TOOL.1
"""

from enum import Enum
from typing import List, Tuple


class Colors:
    """カラー出力用定数クラス"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class LogLevel(Enum):
    """ログレベル列挙型"""
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"


class EnhancedLogger:
    """強化されたログ出力クラス
    
    カラー出力対応のログ機能を提供します。
    ログレベルに応じた色分け表示と、ログ履歴の保持機能があります。
    
    Attributes:
        enable_color (bool): カラー出力の有効/無効
        logs (List[Tuple[LogLevel, str]]): ログ履歴
    """
    
    def __init__(self, enable_color: bool = True):
        """初期化
        
        Args:
            enable_color (bool): カラー出力を有効にするかどうか
        """
        self.enable_color = enable_color
        self.logs: List[Tuple[LogLevel, str]] = []
    
    def _colorize(self, text: str, color: str) -> str:
        """テキストに色を付ける
        
        Args:
            text (str): 対象テキスト
            color (str): カラーコード
            
        Returns:
            str: カラー付きテキスト
        """
        if not self.enable_color:
            return text
        return f"{color}{text}{Colors.END}"
    
    def info(self, message: str):
        """情報ログ出力
        
        Args:
            message (str): ログメッセージ
        """
        colored_msg = self._colorize(f"ℹ️  {message}", Colors.BLUE)
        print(colored_msg)
        self.logs.append((LogLevel.INFO, message))
    
    def warning(self, message: str):
        """警告ログ出力
        
        Args:
            message (str): ログメッセージ
        """
        colored_msg = self._colorize(f"⚠️  {message}", Colors.YELLOW)
        print(colored_msg)
        self.logs.append((LogLevel.WARNING, message))
    
    def error(self, message: str):
        """エラーログ出力
        
        Args:
            message (str): ログメッセージ
        """
        colored_msg = self._colorize(f"❌ {message}", Colors.RED)
        print(colored_msg)
        self.logs.append((LogLevel.ERROR, message))
    
    def success(self, message: str):
        """成功ログ出力
        
        Args:
            message (str): ログメッセージ
        """
        colored_msg = self._colorize(f"✅ {message}", Colors.GREEN)
        print(colored_msg)
        self.logs.append((LogLevel.SUCCESS, message))
    
    def header(self, message: str):
        """ヘッダーログ出力
        
        Args:
            message (str): ヘッダーメッセージ
        """
        colored_msg = self._colorize(f"\n🚀 {message}", Colors.CYAN + Colors.BOLD)
        print(colored_msg)
        print(self._colorize("=" * 80, Colors.CYAN))
    
    def section(self, message: str):
        """セクションログ出力
        
        Args:
            message (str): セクションメッセージ
        """
        colored_msg = self._colorize(f"\n📋 {message}", Colors.MAGENTA + Colors.BOLD)
        print(colored_msg)
        print(self._colorize("-" * 60, Colors.MAGENTA))
    
    def get_logs(self) -> List[Tuple[LogLevel, str]]:
        """ログ履歴を取得
        
        Returns:
            List[Tuple[LogLevel, str]]: ログ履歴のリスト
        """
        return self.logs.copy()
    
    def clear_logs(self):
        """ログ履歴をクリア"""
        self.logs.clear()
    
    def get_error_count(self) -> int:
        """エラーログの件数を取得
        
        Returns:
            int: エラーログの件数
        """
        return len([log for log in self.logs if log[0] == LogLevel.ERROR])
    
    def get_warning_count(self) -> int:
        """警告ログの件数を取得
        
        Returns:
            int: 警告ログの件数
        """
        return len([log for log in self.logs if log[0] == LogLevel.WARNING])
