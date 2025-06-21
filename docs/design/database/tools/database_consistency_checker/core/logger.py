"""
データベース整合性チェックツール - ログ機能
"""
import sys
from datetime import datetime
from typing import Dict, List, Optional
from shared.core.models import CheckStatus, CheckSeverity


class ConsistencyLogger:
    """整合性チェック用ログ機能"""
    
    # カラーコード
    COLORS = {
        CheckSeverity.INFO: '\033[94m',     # 青
        CheckSeverity.WARNING: '\033[93m',  # 黄
        CheckSeverity.ERROR: '\033[91m',    # 赤
        CheckSeverity.CRITICAL: '\033[91m', # 赤
        'RESET': '\033[0m',
        'BOLD': '\033[1m',
        'HEADER': '\033[95m'  # マゼンタ
    }
    
    # 絵文字
    ICONS = {
        CheckSeverity.INFO: 'ℹ️',
        CheckSeverity.WARNING: '⚠️',
        CheckSeverity.ERROR: '❌',
        CheckSeverity.CRITICAL: '🚨'
    }
    
    def __init__(self, enable_color: bool = True, verbose: bool = False):
        """
        ログ初期化
        
        Args:
            enable_color: カラー出力を有効にするか
            verbose: 詳細ログを出力するか
        """
        self.enable_color = enable_color and sys.stdout.isatty()
        self.verbose = verbose
        self.log_history: List[Dict] = []
        self.stats = {
            CheckSeverity.INFO: 0,
            CheckSeverity.WARNING: 0,
            CheckSeverity.ERROR: 0,
            CheckSeverity.CRITICAL: 0
        }
    
    def _colorize(self, text: str, severity: CheckSeverity) -> str:
        """
        テキストに色を付ける
        
        Args:
            text: テキスト
            severity: 重要度
            
        Returns:
            色付きテキスト
        """
        if not self.enable_color:
            return text
        
        color = self.COLORS.get(severity, '')
        reset = self.COLORS['RESET']
        return f"{color}{text}{reset}"
    
    def _get_icon(self, severity: CheckSeverity) -> str:
        """
        重要度に応じたアイコンを取得
        
        Args:
            severity: 重要度
            
        Returns:
            アイコン文字列
        """
        return self.ICONS.get(severity, '')
    
    def log(self, severity: CheckSeverity, message: str, table_name: str = "", details: Optional[Dict] = None):
        """
        ログ出力
        
        Args:
            severity: 重要度
            message: メッセージ
            table_name: テーブル名
            details: 詳細情報
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        icon = self._get_icon(severity)
        
        # ログエントリ作成
        log_entry = {
            'timestamp': timestamp,
            'severity': severity,
            'message': message,
            'table_name': table_name,
            'details': details or {}
        }
        self.log_history.append(log_entry)
        self.stats[severity] += 1
        
        # コンソール出力
        if table_name:
            formatted_message = f"{icon} [{table_name}] {message}"
        else:
            formatted_message = f"{icon} {message}"
        
        colored_message = self._colorize(formatted_message, severity)
        
        if self.verbose or severity in [CheckSeverity.ERROR, CheckSeverity.WARNING, CheckSeverity.CRITICAL]:
            print(f"[{timestamp}] {colored_message}")
            
            # 詳細情報の出力
            if details and self.verbose:
                for key, value in details.items():
                    detail_text = f"  └─ {key}: {value}"
                    print(self._colorize(detail_text, CheckSeverity.INFO))
        elif severity == CheckSeverity.INFO and not self.verbose:
            # 情報時は簡潔に表示
            print(colored_message)
    
    def success(self, message: str, table_name: str = "", details: Optional[Dict] = None):
        """成功ログ"""
        self.log(CheckSeverity.SUCCESS, message, table_name, details)
    
    def warning(self, message: str, table_name: str = "", details: Optional[Dict] = None):
        """警告ログ"""
        self.log(CheckSeverity.WARNING, message, table_name, details)
    
    def error(self, message: str, table_name: str = "", details: Optional[Dict] = None):
        """エラーログ"""
        self.log(CheckSeverity.ERROR, message, table_name, details)
    
    def info(self, message: str, table_name: str = "", details: Optional[Dict] = None):
        """情報ログ"""
        self.log(CheckSeverity.INFO, message, table_name, details)
    
    def header(self, message: str):
        """ヘッダーログ"""
        if self.enable_color:
            header_color = self.COLORS['HEADER'] + self.COLORS['BOLD']
            reset = self.COLORS['RESET']
            print(f"\n{header_color}{'='*60}")
            print(f"{message}")
            print(f"{'='*60}{reset}\n")
        else:
            print(f"\n{'='*60}")
            print(f"{message}")
            print(f"{'='*60}\n")
    
    def section(self, message: str):
        """セクションログ"""
        if self.enable_color:
            section_color = self.COLORS[CheckSeverity.INFO] + self.COLORS['BOLD']
            reset = self.COLORS['RESET']
            print(f"\n{section_color}--- {message} ---{reset}")
        else:
            print(f"\n--- {message} ---")
    
    def progress(self, current: int, total: int, message: str = ""):
        """進捗表示"""
        if not self.verbose:
            return
        
        percentage = (current / total) * 100 if total > 0 else 0
        bar_length = 30
        filled_length = int(bar_length * current // total) if total > 0 else 0
        
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        progress_text = f"進捗: |{bar}| {current}/{total} ({percentage:.1f}%)"
        if message:
            progress_text += f" - {message}"
        
        print(f"\r{progress_text}", end='', flush=True)
        
        if current == total:
            print()  # 改行
    
    def print_summary(self):
        """統計サマリーの出力"""
        self.header("チェック結果サマリー")
        
        total_checks = sum(self.stats.values())
        
        print(f"総チェック数: {total_checks}")
        
        for severity, count in self.stats.items():
            if count > 0:
                icon = self._get_icon(severity)
                colored_text = self._colorize(f"{icon} {severity.value.upper()}: {count}件", severity)
                print(colored_text)
        
        # エラー率の計算
        if total_checks > 0:
            error_rate = (self.stats[CheckSeverity.ERROR] / total_checks) * 100
            warning_rate = (self.stats[CheckSeverity.WARNING] / total_checks) * 100
            
            print(f"\nエラー率: {error_rate:.1f}%")
            print(f"警告率: {warning_rate:.1f}%")
    
    def get_log_history(self) -> List[Dict]:
        """ログ履歴を取得"""
        return self.log_history.copy()
    
    def get_stats(self) -> Dict[CheckSeverity, int]:
        """統計情報を取得"""
        return self.stats.copy()
    
    def clear_logs(self):
        """ログ履歴をクリア"""
        self.log_history.clear()
        self.stats = {
            CheckSeverity.INFO: 0,
            CheckSeverity.WARNING: 0,
            CheckSeverity.ERROR: 0,
            CheckSeverity.CRITICAL: 0
        }
