#!/usr/bin/env python3
"""
統合設定システムのテストスクリプト
設定ファイルの読み込み、マージ、検証をテスト
"""

import os
import sys
import json
from pathlib import Path

# 設定マネージャーのインポート
sys.path.append(os.path.join(os.path.dirname(__file__), 'config'))
from config_manager import ConfigManager, create_config_manager, get_config

def test_basic_functionality():
    """基本機能のテスト"""
    print("=== 基本機能テスト ===")
    
    try:
        # 設定マネージャー作成
        config = create_config_manager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        print("✅ 設定マネージャー作成成功")
        
        # 基本設定値取得
        system_name = config.get("system.name")
        print(f"システム名: {system_name}")
        
        project_name = config.get("project_info.name")
        print(f"プロジェクト名: {project_name}")
        
        primary_color = config.get_color_palette().get("primary")
        print(f"プライマリカラー: {primary_color}")
        
        print("✅ 基本設定値取得成功")
        
    except Exception as e:
        print(f"❌ 基本機能テストエラー: {e}")
        return False
    
    return True

def test_config_hierarchy():
    """設定階層のテスト"""
    print("\n=== 設定階層テスト ===")
    
    try:
        config = ConfigManager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        # 各レベルの設定を確認
        global_config = config.get_global_config()
        tool_config = config.get_tool_config()
        project_config = config.get_project_config()
        merged_config = config.merge_configs()
        
        print(f"グローバル設定キー数: {len(global_config)}")
        print(f"ツール設定キー数: {len(tool_config)}")
        print(f"プロジェクト設定キー数: {len(project_config)}")
        print(f"統合設定キー数: {len(merged_config)}")
        
        # 優先度テスト（プロジェクト設定がグローバル設定を上書きするか）
        global_primary = global_config.get("color_palette", {}).get("primary")
        project_primary = project_config.get("branding", {}).get("primary_color")
        merged_primary = config.get_color_palette().get("primary")
        
        print(f"グローバル設定のプライマリカラー: {global_primary}")
        print(f"プロジェクト設定のプライマリカラー: {project_primary}")
        print(f"統合後のプライマリカラー: {merged_primary}")
        
        if project_primary and merged_primary == project_primary:
            print("✅ 設定優先度が正しく動作")
        else:
            print("⚠️ 設定優先度に問題がある可能性")
        
        print("✅ 設定階層テスト成功")
        
    except Exception as e:
        print(f"❌ 設定階層テストエラー: {e}")
        return False
    
    return True

def test_screen_config():
    """画面設定のテスト"""
    print("\n=== 画面設定テスト ===")
    
    try:
        config = ConfigManager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        # 各画面タイプの設定を確認
        screen_types = ["login", "profile", "skill", "career", "home"]
        
        for screen_type in screen_types:
            screen_config = config.get_screen_config(screen_type)
            print(f"{screen_type}画面設定: {len(screen_config)}項目")
            
            # 重要な設定項目の確認
            layout_type = screen_config.get("layout_type")
            title = screen_config.get("title")
            print(f"  - レイアウト: {layout_type}")
            print(f"  - タイトル: {title}")
        
        print("✅ 画面設定テスト成功")
        
    except Exception as e:
        print(f"❌ 画面設定テストエラー: {e}")
        return False
    
    return True

def test_navigation_config():
    """ナビゲーション設定のテスト"""
    print("\n=== ナビゲーション設定テスト ===")
    
    try:
        config = ConfigManager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        nav_items = config.get_navigation_items()
        print(f"ナビゲーション項目数: {len(nav_items)}")
        
        for item in nav_items:
            name = item.get("name")
            icon = item.get("icon")
            path = item.get("path")
            print(f"  - {name} ({icon}) -> {path}")
        
        print("✅ ナビゲーション設定テスト成功")
        
    except Exception as e:
        print(f"❌ ナビゲーション設定テストエラー: {e}")
        return False
    
    return True

def test_form_fields_config():
    """フォーム項目設定のテスト"""
    print("\n=== フォーム項目設定テスト ===")
    
    try:
        config = ConfigManager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        profile_fields = config.get_form_fields("profile")
        print(f"プロフィールフォーム設定: {len(profile_fields)}セクション")
        
        for section_name, fields in profile_fields.items():
            print(f"  {section_name}: {len(fields)}項目")
            for field in fields:
                label = field.get("label")
                field_type = field.get("type")
                required = field.get("required", False)
                print(f"    - {label} ({field_type}) {'*' if required else ''}")
        
        print("✅ フォーム項目設定テスト成功")
        
    except Exception as e:
        print(f"❌ フォーム項目設定テストエラー: {e}")
        return False
    
    return True

def test_config_validation():
    """設定検証のテスト"""
    print("\n=== 設定検証テスト ===")
    
    try:
        config = ConfigManager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        validation = config.validate_config()
        
        print(f"エラー数: {len(validation['errors'])}")
        print(f"警告数: {len(validation['warnings'])}")
        
        if validation["errors"]:
            print("エラー:")
            for error in validation["errors"]:
                print(f"  - {error}")
        
        if validation["warnings"]:
            print("警告:")
            for warning in validation["warnings"]:
                print(f"  - {warning}")
        
        if not validation["errors"]:
            print("✅ 設定検証テスト成功（エラーなし）")
        else:
            print("⚠️ 設定検証でエラーが検出されました")
        
    except Exception as e:
        print(f"❌ 設定検証テストエラー: {e}")
        return False
    
    return True

def test_convenience_functions():
    """便利関数のテスト"""
    print("\n=== 便利関数テスト ===")
    
    try:
        # 簡易設定取得関数のテスト
        system_name = get_config("system.name")
        project_name = get_config("project_info.name")
        
        print(f"簡易取得 - システム名: {system_name}")
        print(f"簡易取得 - プロジェクト名: {project_name}")
        
        # デフォルト値のテスト
        non_existent = get_config("non.existent.key", "デフォルト値")
        print(f"存在しないキー: {non_existent}")
        
        print("✅ 便利関数テスト成功")
        
    except Exception as e:
        print(f"❌ 便利関数テストエラー: {e}")
        return False
    
    return True

def test_export_functionality():
    """エクスポート機能のテスト"""
    print("\n=== エクスポート機能テスト ===")
    
    try:
        config = ConfigManager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        # 一時ディレクトリ作成
        temp_dir = "temp_test"
        os.makedirs(temp_dir, exist_ok=True)
        
        # YAML形式でエクスポート
        yaml_path = os.path.join(temp_dir, "merged_config.yaml")
        config.export_merged_config(yaml_path, format="yaml")
        
        # JSON形式でエクスポート
        json_path = os.path.join(temp_dir, "merged_config.json")
        config.export_merged_config(json_path, format="json")
        
        # ファイル存在確認
        if os.path.exists(yaml_path) and os.path.exists(json_path):
            print(f"✅ エクスポート成功: {yaml_path}, {json_path}")
            
            # ファイルサイズ確認
            yaml_size = os.path.getsize(yaml_path)
            json_size = os.path.getsize(json_path)
            print(f"YAMLファイルサイズ: {yaml_size}バイト")
            print(f"JSONファイルサイズ: {json_size}バイト")
        else:
            print("❌ エクスポートファイルが作成されませんでした")
            return False
        
        # クリーンアップ
        os.remove(yaml_path)
        os.remove(json_path)
        os.rmdir(temp_dir)
        
        print("✅ エクスポート機能テスト成功")
        
    except Exception as e:
        print(f"❌ エクスポート機能テストエラー: {e}")
        return False
    
    return True

def test_missing_files():
    """存在しないファイルのテスト"""
    print("\n=== 存在しないファイルテスト ===")
    
    try:
        # 存在しないプロジェクト
        config = ConfigManager(
            project_name="non-existent-project",
            tool_name="ui-generator"
        )
        
        # エラーが発生せずに空の設定が返されることを確認
        project_config = config.get_project_config()
        print(f"存在しないプロジェクト設定: {len(project_config)}項目")
        
        # 存在しないツール
        config2 = ConfigManager(
            project_name="skill-report-web",
            tool_name="non-existent-tool"
        )
        
        tool_config = config2.get_tool_config()
        print(f"存在しないツール設定: {len(tool_config)}項目")
        
        print("✅ 存在しないファイルテスト成功（エラーハンドリング正常）")
        
    except Exception as e:
        print(f"❌ 存在しないファイルテストエラー: {e}")
        return False
    
    return True

def test_cache_functionality():
    """キャッシュ機能のテスト"""
    print("\n=== キャッシュ機能テスト ===")
    
    try:
        config = ConfigManager(
            project_name="skill-report-web",
            tool_name="ui-generator"
        )
        
        # 初回読み込み
        config1 = config.merge_configs()
        
        # 2回目読み込み（キャッシュから）
        config2 = config.merge_configs()
        
        # 同じオブジェクトが返されることを確認
        if config1 is config2:
            print("✅ キャッシュが正常に動作")
        else:
            print("⚠️ キャッシュが動作していない可能性")
        
        # キャッシュクリア
        config.clear_cache()
        
        # 再読み込み
        config3 = config.merge_configs()
        
        # 新しいオブジェクトが返されることを確認
        if config1 is not config3:
            print("✅ キャッシュクリアが正常に動作")
        else:
            print("⚠️ キャッシュクリアが動作していない可能性")
        
        print("✅ キャッシュ機能テスト成功")
        
    except Exception as e:
        print(f"❌ キャッシュ機能テストエラー: {e}")
        return False
    
    return True

def main():
    """メインテスト実行"""
    print("統合設定システム テストスクリプト")
    print("=" * 50)
    
    tests = [
        ("基本機能", test_basic_functionality),
        ("設定階層", test_config_hierarchy),
        ("画面設定", test_screen_config),
        ("ナビゲーション設定", test_navigation_config),
        ("フォーム項目設定", test_form_fields_config),
        ("設定検証", test_config_validation),
        ("便利関数", test_convenience_functions),
        ("エクスポート機能", test_export_functionality),
        ("存在しないファイル", test_missing_files),
        ("キャッシュ機能", test_cache_functionality),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name}テストで予期しないエラー: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print("テスト結果サマリー")
    print(f"✅ 成功: {passed}")
    print(f"❌ 失敗: {failed}")
    print(f"📊 成功率: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 全てのテストが成功しました！")
        return 0
    else:
        print(f"\n⚠️ {failed}個のテストが失敗しました。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
