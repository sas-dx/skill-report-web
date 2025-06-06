#!/usr/bin/env python3
"""
パス計算テスト
"""
from pathlib import Path

print('=== パス計算テスト ===')
print('Current file:', __file__)
print('Current file path:', Path(__file__))
print()

print('=== 現在の計算方法 ===')
current_dir = Path(__file__).parent.parent.parent
print('parent.parent.parent:', current_dir.resolve())
print('テーブル一覧.md path:', current_dir.resolve() / 'テーブル一覧.md')
print('File exists:', (current_dir.resolve() / 'テーブル一覧.md').exists())
print()

print('=== 正しい計算方法 ===')
# tools/database_consistency_checker/test_path.py から database/ へ
correct_dir = Path(__file__).parent.parent.parent.parent
print('parent.parent.parent.parent:', correct_dir.resolve())
print('テーブル一覧.md path:', correct_dir.resolve() / 'テーブル一覧.md')
print('File exists:', (correct_dir.resolve() / 'テーブル一覧.md').exists())
print()

print('=== ディレクトリ構造確認 ===')
base_path = Path(__file__).parent
for i in range(6):
    print(f'parent x {i}:', base_path.resolve())
    if (base_path / 'テーブル一覧.md').exists():
        print(f'  -> テーブル一覧.md found at parent x {i}!')
    base_path = base_path.parent
