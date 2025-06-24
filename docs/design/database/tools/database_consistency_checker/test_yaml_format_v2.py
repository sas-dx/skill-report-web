#!/usr/bin/env python3
"""
YAML形式検証機能 v2.0 テストスクリプト

yaml_format_check_enhanced_v2.py の動作検証を行います。

実行方法:
python3 test_yaml_format_v2.py
"""

import os
import sys
import time
from pathlib import Path

# パス設定
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from yaml_format_check_enhanced_v2 import YAMLFormatCheckEnhancedV2


def test_single_table():
    """単一テーブルの検証テスト"""
    print("=== 単一テーブル検証テスト ===")
    
    checker = YAMLFormatCheckEnhancedV2(verbose=True)
    
    # 存在するテーブルをテスト
    result = checker.validate_yaml_format(table_names=['MST_Employee'])
    
    print(f"検証結果: {'成功' if result['success'] else '失敗'}")
    print(f"対象ファイル数: {result['total_files']}")
    print(f"有効ファイル数: {result['valid_files']}")
    print(f"検証時間: {result.get('validation_time', 0):.3f}秒")
    
    if result.get('summary_errors'):
        print(f"エラー数: {len(result['summary_errors'])}")
        for i, error in enumerate(result['summary_errors'][:3], 1):
            print(f"  {i}. {error}")
    
    return result


def test_multiple_tables():
    """複数テーブルの並列検証テスト"""
    print("\n=== 複数テーブル並列検証テスト ===")
    
    checker = YAMLFormatCheckEnhancedV2(verbose=True)
    
    # 複数テーブルをテスト
    test_tables = ['MST_Employee', 'MST_Department', 'TRN_SkillRecord']
    
    start_time = time.time()
    result = checker.validate_yaml_format(table_names=test_tables)
    end_time = time.time()
    
    print(f"検証結果: {'成功' if result['success'] else '失敗'}")
    print(f"対象ファイル数: {result['total_files']}")
    print(f"有効ファイル数: {result['valid_files']}")
    print(f"無効ファイル数: {result['invalid_files']}")
    print(f"検証時間: {end_time - start_time:.3f}秒")
    
    if result.get('summary_suggestions'):
        print(f"修正提案数: {len(result['summary_suggestions'])}")
        for suggestion in result['summary_suggestions'][:3]:
            print(f"  💡 {suggestion}")
    
    return result


def test_all_tables():
    """全テーブルの検証テスト"""
    print("\n=== 全テーブル検証テスト ===")
    
    checker = YAMLFormatCheckEnhancedV2(verbose=False)  # verboseをfalseにして出力を抑制
    
    start_time = time.time()
    result = checker.validate_yaml_format()  # 全テーブル
    end_time = time.time()
    
    print(f"検証結果: {'成功' if result['success'] else '失敗'}")
    print(f"対象ファイル数: {result['total_files']}")
    print(f"有効ファイル数: {result['valid_files']}")
    print(f"無効ファイル数: {result['invalid_files']}")
    print(f"検証時間: {end_time - start_time:.3f}秒")
    
    if result['total_files'] > 0:
        success_rate = (result['valid_files'] / result['total_files']) * 100
        print(f"成功率: {success_rate:.1f}%")
    
    return result


def test_config_file():
    """設定ファイルを使用した検証テスト"""
    print("\n=== 設定ファイル使用テスト ===")
    
    config_path = current_dir / "validation_config.yaml"
    
    if config_path.exists():
        checker = YAMLFormatCheckEnhancedV2(
            verbose=True, 
            config_path=str(config_path)
        )
        
        result = checker.validate_yaml_format(table_names=['MST_Employee'])
        
        print(f"設定ファイル: {config_path}")
        print(f"検証結果: {'成功' if result['success'] else '失敗'}")
        
        return result
    else:
        print(f"設定ファイルが見つかりません: {config_path}")
        return None


def test_report_export():
    """レポート出力テスト"""
    print("\n=== レポート出力テスト ===")
    
    checker = YAMLFormatCheckEnhancedV2(verbose=True)
    
    # 検証実行
    result = checker.validate_yaml_format(table_names=['MST_Employee', 'MST_Department'])
    
    # 各形式でレポート出力
    formats = ['json', 'html', 'markdown']
    output_files = []
    
    for format_type in formats:
        output_path = checker.export_report(result, format_type)
        if output_path:
            output_files.append(output_path)
            print(f"✅ {format_type.upper()}レポート出力: {output_path}")
        else:
            print(f"❌ {format_type.upper()}レポート出力失敗")
    
    return output_files


def test_performance_comparison():
    """パフォーマンス比較テスト"""
    print("\n=== パフォーマンス比較テスト ===")
    
    # v1（従来版）のインポート
    try:
        from yaml_format_check_enhanced import YAMLFormatCheckEnhanced as V1Checker
        v1_available = True
    except ImportError:
        print("⚠️ v1チェッカーが利用できません")
        v1_available = False
    
    test_tables = ['MST_Employee', 'MST_Department', 'TRN_SkillRecord', 'MST_Position', 'MST_SkillCategory']
    
    # v2（新版）のテスト
    print("v2.0 (並列処理版) テスト:")
    v2_checker = YAMLFormatCheckEnhancedV2(verbose=False)
    
    start_time = time.time()
    v2_result = v2_checker.validate_yaml_format(table_names=test_tables)
    v2_time = time.time() - start_time
    
    print(f"  検証時間: {v2_time:.3f}秒")
    print(f"  対象ファイル数: {v2_result['total_files']}")
    print(f"  成功率: {(v2_result['valid_files']/v2_result['total_files']*100):.1f}%")
    
    # v1との比較（利用可能な場合）
    if v1_available:
        print("\nv1.0 (従来版) テスト:")
        v1_checker = V1Checker(verbose=False)
        
        start_time = time.time()
        v1_result = v1_checker.validate_yaml_format(table_names=test_tables)
        v1_time = time.time() - start_time
        
        print(f"  検証時間: {v1_time:.3f}秒")
        print(f"  対象ファイル数: {v1_result['total_files']}")
        print(f"  成功率: {(v1_result['valid_files']/v1_result['total_files']*100):.1f}%")
        
        # パフォーマンス改善率
        if v1_time > 0:
            improvement = ((v1_time - v2_time) / v1_time) * 100
            print(f"\n📈 パフォーマンス改善: {improvement:.1f}%")
    
    return v2_time


def main():
    """メインテスト実行"""
    print("🚀 YAML形式検証機能 v2.0 動作検証開始")
    print("=" * 50)
    
    try:
        # 各テストを実行
        test_single_table()
        test_multiple_tables()
        test_all_tables()
        test_config_file()
        test_report_export()
        test_performance_comparison()
        
        print("\n" + "=" * 50)
        print("✅ 全テスト完了")
        
    except Exception as e:
        print(f"\n❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
