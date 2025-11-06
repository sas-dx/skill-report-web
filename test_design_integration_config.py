#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設計統合ツール - 統合設定システムテスト
汎用的な設定システムと設計統合ツールの統合テスト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートを追加
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "docs" / "tools" / "design-integration"))

def test_config_system_integration():
    """設定システム統合テスト"""
    print("=== 設計統合ツール - 統合設定システムテスト ===\n")
    
    try:
        # 1. 設計統合ツール設定管理のインポート
        print("1. 設計統合ツール設定管理のインポート...")
        from config_manager import DesignIntegrationConfigManager
        print("✅ インポート成功")
        
        # 2. 設定管理インスタンス作成
        print("\n2. 設定管理インスタンス作成...")
        config_manager = DesignIntegrationConfigManager("skill-report-web")
        print("✅ インスタンス作成成功")
        
        # 3. 設定読み込み
        print("\n3. 設定読み込み...")
        config = config_manager.load_config()
        print(f"✅ 設定読み込み成功")
        print(f"   プロジェクト名: {config.project_name}")
        print(f"   ツール名: {config.tool_name}")
        print(f"   バージョン: {config.version}")
        
        # 4. パス設定確認
        print("\n4. パス設定確認...")
        paths = {
            'design_root': config_manager.get_path('design_root'),
            'database_specs': config_manager.get_path('database_specs'),
            'api_specs': config_manager.get_path('api_specs'),
            'screen_specs': config_manager.get_path('screen_specs'),
            'output_root': config_manager.get_path('output_root'),
            'backup_root': config_manager.get_path('backup_root')
        }
        
        for path_name, path_value in paths.items():
            print(f"   {path_name}: {path_value}")
        print("✅ パス設定確認完了")
        
        # 5. 機能設定確認
        print("\n5. 機能設定確認...")
        features = [
            ('core.database_management', 'データベース管理'),
            ('core.api_management', 'API管理'),
            ('core.screen_management', '画面管理'),
            ('core.integration_checking', '統合チェック'),
            ('core.report_generation', 'レポート生成'),
            ('advanced.ai_recommendations', 'AI推奨'),
            ('advanced.auto_generation', '自動生成'),
            ('experimental.machine_learning_validation', '機械学習検証')
        ]
        
        for feature_path, feature_name in features:
            enabled = config_manager.is_feature_enabled(feature_path)
            status = "✅ 有効" if enabled else "❌ 無効"
            print(f"   {feature_name}: {status}")
        
        # 6. 個別設定取得テスト
        print("\n6. 個別設定取得テスト...")
        
        # データベース設定
        db_config = config_manager.get_database_config()
        print(f"   データベース設定: {len(db_config)} 項目")
        
        # API設定
        api_config = config_manager.get_api_config()
        print(f"   API設定: {len(api_config)} 項目")
        
        # 画面設定
        screen_config = config_manager.get_screen_config()
        print(f"   画面設定: {len(screen_config)} 項目")
        
        # 品質設定
        quality_config = config_manager.get_quality_config()
        print(f"   品質設定: {len(quality_config)} 項目")
        
        # 統合設定
        integration_config = config_manager.get_integration_config()
        print(f"   統合設定: {len(integration_config)} 項目")
        
        # レポート設定
        reporting_config = config_manager.get_reporting_config()
        print(f"   レポート設定: {len(reporting_config)} 項目")
        
        print("✅ 個別設定取得完了")
        
        # 7. 設定検証
        print("\n7. 設定検証...")
        errors = config_manager.validate_config()
        if errors:
            print("⚠️ 検証エラー:")
            for error in errors:
                print(f"     - {error}")
        else:
            print("✅ 設定検証OK")
        
        # 8. ディレクトリ作成テスト
        print("\n8. ディレクトリ作成テスト...")
        config_manager.create_directories()
        print("✅ 必要なディレクトリを作成しました")
        
        # 9. 設定詳細表示
        print("\n9. 設定詳細表示...")
        print("--- データベース設定詳細 ---")
        db_config = config_manager.get_database_config()
        if 'validation' in db_config:
            validation = db_config['validation']
            print(f"   必須カラム: {validation.get('required_columns', [])}")
            print(f"   禁止カラム名: {validation.get('forbidden_column_names', [])}")
            print(f"   最大カラム数: {validation.get('max_table_columns', 'N/A')}")
            print(f"   主キー必須: {validation.get('require_primary_key', False)}")
        
        print("\n--- API設定詳細 ---")
        api_config = config_manager.get_api_config()
        if 'validation' in api_config:
            validation = api_config['validation']
            print(f"   必須ヘッダー: {validation.get('required_headers', [])}")
            print(f"   レスポンス形式: {validation.get('response_format', 'N/A')}")
            print(f"   エラー形式: {validation.get('error_format', 'N/A')}")
            print(f"   ページネーション必須: {validation.get('require_pagination', False)}")
        
        print("\n--- 品質基準詳細 ---")
        quality_config = config_manager.get_quality_config()
        if 'documentation' in quality_config:
            doc_quality = quality_config['documentation']
            print(f"   完全性閾値: {doc_quality.get('completeness_threshold', 'N/A')}%")
            print(f"   一貫性閾値: {doc_quality.get('consistency_threshold', 'N/A')}%")
            print(f"   トレーサビリティ閾値: {doc_quality.get('traceability_threshold', 'N/A')}%")
        
        print("\n✅ 全テスト完了")
        return True
        
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("設計統合ツール設定管理が正しくセットアップされていません")
        return False
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_config_file_existence():
    """設定ファイル存在確認"""
    print("\n=== 設定ファイル存在確認 ===")
    
    config_files = [
        "config/global/default.yaml",
        "config/global/design-integration.yaml",
        "config/tools/ui-generator.yaml",
        "config/tools/design-integration.yaml",
        "config/projects/skill-report-web.yaml",
        "config/config_manager.py"
    ]
    
    all_exist = True
    for config_file in config_files:
        file_path = PROJECT_ROOT / config_file
        if file_path.exists():
            print(f"✅ {config_file}")
        else:
            print(f"❌ {config_file} (存在しません)")
            all_exist = False
    
    return all_exist

def test_directory_structure():
    """ディレクトリ構造確認"""
    print("\n=== ディレクトリ構造確認 ===")
    
    required_dirs = [
        "config",
        "config/global",
        "config/tools",
        "config/projects",
        "docs/design",
        "docs/design/database",
        "docs/design/api",
        "docs/design/screens",
        "docs/tools/design-integration"
    ]
    
    all_exist = True
    for directory in required_dirs:
        dir_path = PROJECT_ROOT / directory
        if dir_path.exists() and dir_path.is_dir():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ (存在しません)")
            all_exist = False
    
    return all_exist

def main():
    """メインテスト実行"""
    print("設計統合ツール - 統合設定システムテスト開始")
    print("=" * 60)
    
    # 1. ディレクトリ構造確認
    dir_ok = test_directory_structure()
    
    # 2. 設定ファイル存在確認
    files_ok = test_config_file_existence()
    
    # 3. 統合テスト実行
    if dir_ok and files_ok:
        integration_ok = test_config_system_integration()
    else:
        print("\n❌ 前提条件が満たされていないため、統合テストをスキップします")
        integration_ok = False
    
    # 結果サマリー
    print("\n" + "=" * 60)
    print("テスト結果サマリー:")
    print(f"  ディレクトリ構造: {'✅ OK' if dir_ok else '❌ NG'}")
    print(f"  設定ファイル: {'✅ OK' if files_ok else '❌ NG'}")
    print(f"  統合テスト: {'✅ OK' if integration_ok else '❌ NG'}")
    
    if dir_ok and files_ok and integration_ok:
        print("\n🎉 全テスト成功！設計統合ツールの設定システムが正常に動作しています。")
        return True
    else:
        print("\n⚠️ 一部テストが失敗しました。設定を確認してください。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
