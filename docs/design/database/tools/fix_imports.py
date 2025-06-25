#!/usr/bin/env python3
"""
インポート修正スクリプト
database_consistency_checker内のmodelsインポートをshared.core.modelsに統一
"""
import os
import re
from pathlib import Path

def fix_imports_in_file(file_path: Path):
    """ファイル内のインポートを修正"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # パターン1: from database_consistency_checker.core.models import ...
        pattern1 = r'from database_consistency_checker\.core\.models import ([^\n]+)'
        replacement1 = r'from shared.core.models import \1'
        content = re.sub(pattern1, replacement1, content)
        
        # パターン2: from .models import ...
        pattern2 = r'from \.models import ([^\n]+)'
        replacement2 = r'from shared.core.models import \1'
        content = re.sub(pattern2, replacement2, content)
        
        # パターン3: import database_consistency_checker.core.models
        pattern3 = r'import database_consistency_checker\.core\.models'
        replacement3 = r'import shared.core.models'
        content = re.sub(pattern3, replacement3, content)
        
        # パターン4: from database_consistency_checker.core import models
        pattern4 = r'from database_consistency_checker\.core import models'
        replacement4 = r'from shared.core import models'
        content = re.sub(pattern4, replacement4, content)
        
        # 変更があった場合のみファイルを更新
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 修正完了: {file_path}")
            return True
        else:
            print(f"⏭️ 変更なし: {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {file_path} - {e}")
        return False

def main():
    """メイン処理"""
    base_dir = Path(__file__).parent / "database_consistency_checker"
    
    if not base_dir.exists():
        print(f"❌ ディレクトリが見つかりません: {base_dir}")
        return
    
    # 対象ファイルを検索
    python_files = list(base_dir.rglob("*.py"))
    
    print(f"📁 対象ディレクトリ: {base_dir}")
    print(f"📄 対象ファイル数: {len(python_files)}")
    print()
    
    fixed_count = 0
    
    for file_path in python_files:
        if fix_imports_in_file(file_path):
            fixed_count += 1
    
    print()
    print(f"🎉 修正完了: {fixed_count}/{len(python_files)} ファイル")

if __name__ == "__main__":
    main()
