#!/usr/bin/env python3
"""
データベース整合性チェックツール - 実行スクリプト

使用方法:
    python run_check.py [オプション]
"""

import sys
from pathlib import Path

# パスの設定
current_dir = Path(__file__).parent
tools_dir = current_dir.parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# メイン関数をインポートして実行
from database_consistency_checker.main import main

if __name__ == "__main__":
    sys.exit(main())
