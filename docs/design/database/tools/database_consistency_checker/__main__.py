#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
データベース整合性チェックツール - 統合データモデル対応メインエントリーポイント

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-08
実装者: AI駆動開発チーム

統合データモデルを使用したデータベース整合性チェック
既存機能の100%互換性を保証
"""

import sys
import argparse
from pathlib import Path
import logging
from datetime import datetime

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# 統合データモデル対応のアダプターをインポート
from docs.design.database.tools.database_consistency_checker.core.adapters import (
    create_legacy_compatible_checker,
    UnifiedConsistencyCheckerService
)
from docs.design.database.tools.database_consistency_checker.core.models import CheckConfig
from docs.design.database.tools.database_consistency_checker.utils.logger import setup_logger


def main():
    """メイン処理 - 統合データモデル強制適用版"""
    parser = argparse.ArgumentParser(
        description='データベース整合性チェックツール - 統合データモデル対応版',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全体整合性チェック（統合データモデル使用）
  python run_check.py
  
  # 特定テーブルのみチェック
  python run_check.py --tables MST_Employee,MST_Role
  
  # 統合モデル強制使用
  python run_check.py --unified-model
  
  # 既存互換モード（レガシーサポート）
  python run_check.py --legacy-mode
  
  # 詳細ログ出力
  python run_check.py --verbose
  
  # レポート出力
  python run_check.py --output-format markdown --output-file report.md
        """
    )
    
    parser.add_argument(
        '--tables',
        type=str,
        help='チェック対象テーブル名（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--checks',
        type=str,
        help='実行するチェック項目（カンマ区切りで複数指定可能）'
    )
    
    parser.add_argument(
        '--base-dir',
        type=str,
        default='.',
        help='ベースディレクトリ（デフォルト: カレントディレクトリ）'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='詳細ログ出力'
    )
    
    parser.add_argument(
        '--output-format',
        choices=['console', 'markdown', 'json'],
        default='console',
        help='出力形式（デフォルト: console）'
    )
    
    parser.add_argument(
        '--output-file',
        type=str,
        help='出力ファイルパス'
    )
    
    parser.add_argument(
        '--unified-model',
        action='store_true',
        help='統合データモデル強制使用（デフォルト）'
    )
    
    parser.add_argument(
        '--legacy-mode',
        action='store_true',
        help='既存互換モード（レガシーサポート）'
    )
    
    parser.add_argument(
        '--suggest-fixes',
        action='store_true',
        help='修正提案を生成'
    )
    
    parser.add_argument(
        '--auto-apply',
        action='store_true',
        help='修正提案を自動適用（危険）'
    )
    
    args = parser.parse_args()
    
    try:
        # ログ設定
        setup_logger(args.verbose)
        logger = logging.getLogger(__name__)
        
        logger.info("データベース整合性チェックツール開始（統合データモデル対応版）")
        logger.info(f"ベースディレクトリ: {args.base_dir}")
        
        # 処理モード決定（統合データモデルをデフォルトに）
        use_unified_model = not args.legacy_mode  # レガシーモード指定時のみ既存モード
        
        if use_unified_model:
            logger.info("統合データモデルを使用します")
            service = UnifiedConsistencyCheckerService()
        else:
            logger.info("既存互換モードを使用します")
            service = create_legacy_compatible_checker()
        
        # チェック設定作成
        config = CheckConfig(
            suggest_fixes=args.suggest_fixes,
            auto_apply=args.auto_apply,
            verbose=args.verbose,
            target_tables=args.tables.split(',') if args.tables else [],
            base_dir=args.base_dir,
            output_format=args.output_format,
            output_file=args.output_file
        )
        
        # 整合性チェック実行
        if use_unified_model:
            # 統合データモデルで処理
            base_dir = Path(args.base_dir)
            report = service.check_consistency_with_unified_model(base_dir)
            
            # 統合レポートを既存形式に変換（表示用）
            from docs.design.database.tools.database_consistency_checker.core.adapters import ConsistencyCheckerAdapter
            adapter = ConsistencyCheckerAdapter()
            legacy_report = adapter.unified_to_legacy_report(report)
        else:
            # 既存互換モードで処理
            legacy_report = service.check_consistency(config)
        
        # 結果出力
        output_report(legacy_report, args, use_unified_model)
        
        # 終了コード決定
        error_count = legacy_report.summary.get('error', 0)
        warning_count = legacy_report.summary.get('warning', 0)
        
        logger.info("データベース整合性チェックツール完了")
        
        if error_count > 0:
            return 1  # エラーあり
        elif warning_count > 0:
            return 2  # 警告あり
        else:
            return 0  # 正常
        
    except Exception as e:
        print(f"予期しないエラーが発生しました: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


def output_report(report, args, use_unified_model):
    """レポート出力"""
    if args.output_format == 'console':
        output_console_report(report, use_unified_model)
    elif args.output_format == 'markdown':
        output_markdown_report(report, args.output_file, use_unified_model)
    elif args.output_format == 'json':
        output_json_report(report, args.output_file, use_unified_model)


def output_console_report(report, use_unified_model):
    """コンソール形式でレポート出力"""
    print(f"\n=== データベース整合性チェック結果 ===")
    print(f"チェック日時: {report.check_date}")
    print(f"対象テーブル数: {report.total_tables}")
    print(f"総チェック数: {report.total_checks}")
    print(f"使用モデル: {'統合データモデル' if use_unified_model else '既存互換モード'}")
    
    # サマリー表示
    summary = report.summary
    print(f"\n=== チェック結果サマリー ===")
    print(f"成功: {summary.get('success', 0)}")
    print(f"情報: {summary.get('info', 0)}")
    print(f"警告: {summary.get('warning', 0)}")
    print(f"エラー: {summary.get('error', 0)}")
    
    # エラー・警告詳細
    if summary.get('error', 0) > 0 or summary.get('warning', 0) > 0:
        print(f"\n=== 詳細結果 ===")
        for result in report.results:
            if result.severity.value in ['error', 'warning']:
                severity_mark = "❌" if result.severity.value == 'error' else "⚠️"
                print(f"{severity_mark} [{result.table_name}] {result.message}")
                if result.file_path:
                    print(f"   ファイル: {result.file_path}")
    
    # 修正提案
    if report.fix_suggestions:
        print(f"\n=== 修正提案 ===")
        for fix in report.fix_suggestions:
            print(f"🔧 [{fix.table_name}] {fix.description}")


def output_markdown_report(report, output_file, use_unified_model):
    """Markdown形式でレポート出力"""
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"consistency_report_{timestamp}.md"
    
    content = f"""# データベース整合性チェック結果

## 基本情報
- **チェック日時**: {report.check_date}
- **対象テーブル数**: {report.total_tables}
- **総チェック数**: {report.total_checks}
- **使用モデル**: {'統合データモデル' if use_unified_model else '既存互換モード'}

## チェック結果サマリー
| 結果 | 件数 |
|------|------|
| 成功 | {report.summary.get('success', 0)} |
| 情報 | {report.summary.get('info', 0)} |
| 警告 | {report.summary.get('warning', 0)} |
| エラー | {report.summary.get('error', 0)} |

## 詳細結果
"""
    
    for result in report.results:
        severity_icon = {
            'success': '✅',
            'info': 'ℹ️',
            'warning': '⚠️',
            'error': '❌'
        }.get(result.severity.value, '❓')
        
        content += f"### {severity_icon} {result.table_name} - {result.check_name}\n"
        content += f"**メッセージ**: {result.message}\n\n"
        if result.file_path:
            content += f"**ファイル**: `{result.file_path}`\n\n"
    
    # 修正提案
    if report.fix_suggestions:
        content += "\n## 修正提案\n"
        for fix in report.fix_suggestions:
            content += f"### 🔧 {fix.table_name}\n"
            content += f"**説明**: {fix.description}\n\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"レポートを出力しました: {output_file}")


def output_json_report(report, output_file, use_unified_model):
    """JSON形式でレポート出力"""
    import json
    
    if not output_file:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"consistency_report_{timestamp}.json"
    
    # レポートをJSON形式に変換
    report_data = {
        "check_date": report.check_date,
        "total_tables": report.total_tables,
        "total_checks": report.total_checks,
        "use_unified_model": use_unified_model,
        "summary": report.summary,
        "results": [
            {
                "check_name": r.check_name,
                "table_name": r.table_name,
                "severity": r.severity.value,
                "message": r.message,
                "file_path": r.file_path,
                "line_number": r.line_number,
                "details": r.details
            }
            for r in report.results
        ],
        "fix_suggestions": [
            {
                "fix_type": f.fix_type.value,
                "table_name": f.table_name,
                "description": f.description,
                "fix_content": f.fix_content,
                "file_path": f.file_path,
                "backup_required": f.backup_required,
                "critical": f.critical
            }
            for f in report.fix_suggestions
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report_data, f, ensure_ascii=False, indent=2)
    
    print(f"レポートを出力しました: {output_file}")


if __name__ == '__main__':
    sys.exit(main())
