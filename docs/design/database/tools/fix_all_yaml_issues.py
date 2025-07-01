#!/usr/bin/env python3
"""
YAML問題統合修正スクリプト
全てのYAMLファイルの問題を一括で修正する
"""

import os
import sys
import subprocess
from pathlib import Path

def run_script(script_path: Path, description: str) -> bool:
    """
    スクリプトを実行する
    
    Args:
        script_path: スクリプトのパス
        description: スクリプトの説明
        
    Returns:
        成功した場合True
    """
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        # 標準出力を表示
        if result.stdout:
            print(result.stdout)
        
        # エラー出力を表示
        if result.stderr:
            print("⚠️ エラー出力:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} 完了")
            return True
        else:
            print(f"❌ {description} 失敗 (終了コード: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {description} 実行エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🔧 YAML問題統合修正スクリプト開始")
    print("="*60)
    
    # スクリプトディレクトリ
    script_dir = Path(__file__).parent
    
    # 実行するスクリプトのリスト
    scripts = [
        {
            'path': script_dir / 'fix_missing_columns.py',
            'description': '不足columnsセクション修正'
        },
        {
            'path': script_dir / 'fix_foreign_keys.py',
            'description': '外部キー定義修正'
        }
    ]
    
    # 各スクリプトを順次実行
    success_count = 0
    total_count = len(scripts)
    
    for script_info in scripts:
        script_path = script_info['path']
        description = script_info['description']
        
        if not script_path.exists():
            print(f"❌ スクリプトが見つかりません: {script_path}")
            continue
        
        if run_script(script_path, description):
            success_count += 1
    
    # 最終結果
    print(f"\n{'='*60}")
    print("🎯 統合修正完了")
    print(f"📊 実行結果:")
    print(f"   - 総スクリプト数: {total_count}")
    print(f"   - 成功スクリプト数: {success_count}")
    print(f"   - 失敗スクリプト数: {total_count - success_count}")
    
    if success_count == total_count:
        print("\n✅ 全ての修正が正常に完了しました")
        print("\n🔍 次のステップ:")
        print("   1. 整合性チェックを再実行してください")
        print("   2. python3 -m database_consistency_checker --verbose")
        return 0
    else:
        print(f"\n⚠️  {total_count - success_count}件のスクリプトが失敗しました")
        return 1

if __name__ == "__main__":
    sys.exit(main())
