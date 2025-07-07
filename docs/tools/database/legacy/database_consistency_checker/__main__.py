#!/usr/bin/env python3
"""
データベース整合性チェッカー - メインエントリーポイント

このモジュールは python -m database_consistency_checker で実行される際のエントリーポイントです。
"""

import sys
import os

# パッケージのルートディレクトリをPythonパスに追加
current_dir = os.path.dirname(os.path.abspath(__file__))
tools_dir = os.path.dirname(current_dir)
sys.path.insert(0, tools_dir)

from database_consistency_checker.main import main

if __name__ == "__main__":
    main()
