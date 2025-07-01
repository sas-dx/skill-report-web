"""
データベース整合性チェックツール - ロガー設定
"""
import logging
import sys
from pathlib import Path
from typing import Optional


class ConsistencyLogger:
    """整合性チェック用ロガー"""
    
    @staticmethod
    def setup_logger(
        name: str = "consistency_checker",
        level: int = logging.INFO,
        log_file: Optional[Path] = None
    ) -> logging.Logger:
        """
        ロガーをセットアップ
        
        Args:
            name: ロガー名
            level: ログレベル
            log_file: ログファイルパス（指定しない場合はコンソールのみ）
            
        Returns:
            設定済みのロガー
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # 既存のハンドラーをクリア
        logger.handlers.clear()
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # コンソールハンドラー
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # ファイルハンドラー（指定された場合）
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name: str = "consistency_checker") -> logging.Logger:
        """
        既存のロガーを取得
        
        Args:
            name: ロガー名
            
        Returns:
            ロガー
        """
        return logging.getLogger(name)
