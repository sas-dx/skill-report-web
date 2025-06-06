#!/usr/bin/env python3
"""
相対インポートを絶対インポートに一括変換するスクリプト
"""
import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """ファイル内の相対インポートを修正"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 相対インポートのパターンを検索・置換
        patterns = [
            (r'from \.\.core\.', 'from core.'),
            (r'from \.\.parsers\.', 'from parsers.'),
            (r'from \.\.checkers\.', 'from checkers.'),
            (r'from \.\.reporters\.', 'from reporters.'),
            (r'from \.\.utils\.', 'from utils.'),
            (r'from \.core\.', 'from core.'),
            (r'from \.parsers\.', 'from parsers.'),
            (r'from \.checkers\.', 'from checkers.'),
            (r'from \.reporters\.', 'from reporters.'),
            (r'from \.utils\.', 'from utils.'),
        ]
        
        modified = False
        for pattern, replacement in patterns:
            new_content = re.sub(pattern, replacement, content)
            if new_content != content:
                content = new_content
                modified = True
        
        if modified:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"修正: {file_path}")
            return True
        else:
            print(f"変更なし: {file_path}")
            return False
            
    except Exception as e:
        print(f"エラー: {file_path} - {e}")
        return False

def main():
    """メイン処理"""
    base_dir = Path(__file__).parent
    
    # 対象ディレクトリ
    target_dirs = ['checkers', 'parsers', 'reporters', 'core', 'utils']
    
    total_files = 0
    modified_files = 0
    
    for dir_name in target_dirs:
        dir_path = base_dir / dir_name
        if not dir_path.exists():
            continue
            
        for py_file in dir_path.glob('*.py'):
            if py_file.name == '__init__.py':
                continue
                
            total_files += 1
            if fix_imports_in_file(py_file):
                modified_files += 1
    
    print(f"\n完了: {total_files}ファイル中{modified_files}ファイルを修正")

if __name__ == '__main__':
    main()
