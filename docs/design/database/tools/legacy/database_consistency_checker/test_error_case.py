#!/usr/bin/env python3
"""
YAML形式検証機能 v2.0 エラーケーステスト

不正なYAMLファイルでの動作確認を行います。
"""

import os
import sys
import tempfile
from pathlib import Path

# パス設定
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from yaml_format_check_enhanced_v2 import YAMLFormatCheckEnhancedV2


def create_invalid_yaml_file():
    """不正なYAMLファイルを作成"""
    invalid_yaml_content = """
# 不正なYAMLファイル（必須セクション不足）
table_name: "TEST_Invalid"
logical_name: "テスト用不正テーブル"
category: "テスト系"

# revision_history セクションが不足
# overview セクションが不足

columns:
  - name: "id"
    type: "INTEGER"
    nullable: false
    primary_key: true
    comment: "ID"

# notes セクションが不足
# rules セクションが不足
"""
    
    # 一時ファイルを作成
    temp_dir = Path("../../table-details")
    temp_file = temp_dir / "TEST_Invalid_details.yaml"
    
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(invalid_yaml_content)
    
    return temp_file


def test_error_detection():
    """エラー検出テスト"""
    print("=== エラー検出テスト ===")
    
    # 不正なYAMLファイルを作成
    invalid_file = create_invalid_yaml_file()
    
    try:
        checker = YAMLFormatCheckEnhancedV2(verbose=True)
        
        # 不正なファイルを検証
        result = checker.validate_yaml_format(table_names=['TEST_Invalid'])
        
        print(f"検証結果: {'成功' if result['success'] else '失敗'}")
        print(f"対象ファイル数: {result['total_files']}")
        print(f"有効ファイル数: {result['valid_files']}")
        print(f"無効ファイル数: {result['invalid_files']}")
        
        if result.get('summary_errors'):
            print(f"\n検出されたエラー数: {len(result['summary_errors'])}")
            for i, error in enumerate(result['summary_errors'], 1):
                print(f"  {i}. {error}")
        
        if result.get('summary_suggestions'):
            print(f"\n修正提案数: {len(result['summary_suggestions'])}")
            for i, suggestion in enumerate(result['summary_suggestions'], 1):
                print(f"  💡 {i}. {suggestion}")
        
        # エラーレポートを出力
        report_path = checker.export_report(result, 'markdown')
        if report_path:
            print(f"\nエラーレポート出力: {report_path}")
        
        return result
        
    finally:
        # 一時ファイルを削除
        if invalid_file.exists():
            invalid_file.unlink()
            print(f"\n一時ファイルを削除: {invalid_file}")


def main():
    """メインテスト実行"""
    print("🚀 YAML形式検証機能 v2.0 エラーケーステスト開始")
    print("=" * 50)
    
    try:
        test_error_detection()
        
        print("\n" + "=" * 50)
        print("✅ エラーケーステスト完了")
        
    except Exception as e:
        print(f"\n❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
