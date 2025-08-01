#!/usr/bin/env python3
"""
テーブル生成ツールのエントリーポイント

このモジュールにより、以下の実行方法が可能になります：
- python -m table_generator
- python table_generator/__main__.py
"""

import sys
from pathlib import Path

# ツールディレクトリをパスに追加
tools_dir = Path(__file__).parent.parent
if str(tools_dir) not in sys.path:
    sys.path.insert(0, str(tools_dir))

# メイン関数をインポートして実行
from table_generator.main import main

if __name__ == "__main__":
    sys.exit(main())
