"""
データベースツール統合テストスイート

要求仕様ID: PLT.1-WEB.1, SKL.1-HIER.1
設計書: docs/design/database/08-database-design-guidelines.md
実装日: 2025-06-08
実装者: AI Assistant

このモジュールは以下のテスト機能を提供します：
- 統合データモデルのテスト
- 整合性チェック機能のテスト
- ツール間連携のテスト
- パフォーマンステスト
"""

import sys
import os
from pathlib import Path

# テストルートディレクトリをPythonパスに追加
TEST_ROOT = Path(__file__).parent
TOOLS_ROOT = TEST_ROOT.parent
sys.path.insert(0, str(TOOLS_ROOT))

# テスト共通設定
TEST_CONFIG = {
    'fixtures_dir': TEST_ROOT / 'fixtures',
    'sample_yaml_dir': TEST_ROOT / 'fixtures' / 'sample_yaml',
    'sample_ddl_dir': TEST_ROOT / 'fixtures' / 'sample_ddl',
    'expected_outputs_dir': TEST_ROOT / 'fixtures' / 'expected_outputs',
    'temp_dir': TEST_ROOT / 'temp',
    'verbose': True
}

# テスト用の一時ディレクトリ作成
TEST_CONFIG['temp_dir'].mkdir(exist_ok=True)

__version__ = "1.0.0"
__author__ = "Database Tools Team"
