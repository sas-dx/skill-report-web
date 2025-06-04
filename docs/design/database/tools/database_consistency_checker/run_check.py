"""
データベース整合性チェックツール - 実行スクリプト
"""
import sys
from pathlib import Path

# パッケージのパスを追加
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent))

from database_consistency_checker.main import main

if __name__ == "__main__":
    main()
