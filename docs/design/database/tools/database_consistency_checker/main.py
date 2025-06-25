"""
データベース整合性チェックツール - メインエントリーポイント

要求仕様ID: PLT.1-WEB.1 (システム基盤要件)
実装日: 2025-06-25
実装者: AI駆動開発チーム
"""
import argparse
import sys
from pathlib import Path
from typing import List, Optional

# 共通ライブラリのインポート
from shared.core.config import get_config, create_check_config
from shared.core.logger import get_logger, get_performance_logger, setup_logging
from shared.core.models import CheckResult, CheckSeverity, ConsistencyReport
from shared.utils.file_utils import get_file_manager

# ツール固有のインポート
from database_consistency_checker.checkers.consistency_checker import ConsistencyChecker
from database_consistency_checker.reporters.console_reporter import ConsoleReporter
from database_consistency_checker.reporters.markdown_reporter import MarkdownReporter
from database_consistency_checker.reporters.json_reporter import JsonReporter
from database_consistency_checker.utils.report_manager import ReportManager
from database_consistency_checker.sample_data_generator_enhanced import EnhancedSampleDataGenerator as SampleDataGenerator
from database_consistency_checker.yaml_format_check_enhanced import YAMLFormatCheckEnhanced


def create_argument_parser() -> argparse.ArgumentParser:
    """コマンドライン引数パーサーを作成"""
    parser = argparse.ArgumentParser(
        description="データベース整合性チェックツール",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 全チェック実行
  python -m database_consistency_checker

  # 特定のテーブルのみチェック
  python -m database_consistency_checker --tables MST_Employee MST_Department

  # 修正提案付きでチェック
  python -m database_consistency_checker --suggest-fixes

  # 結果をMarkdown形式で出力
  python -m database_consistency_checker --output-format markdown --output-file report.md

  # 詳細ログ付きでチェック
  python -m database_consistency_checker --verbose

利用可能なチェック:
  - table_existence: テーブル存在確認
  - orphaned_files: 孤立ファイル検出
  - yaml_format_consistency: YAMLフォーマット整合性
  - column_consistency: カラム定義整合性
  - foreign_key_consistency: 外部キー整合性
  - data_type_consistency: データ型整合性
  - constraint_consistency: 制約整合性
  - fix_suggestions: 修正提案
  - multitenant_compliance: マルチテナント対応
  - requirement_traceability: 要求仕様ID追跡
  - performance_impact: パフォーマンス影響分析
  - sample_data_generation: サンプルデータINSERT文生成
        """
    )
    
    # 基本オプション
    parser.add_argument(
        "--base-dir",
        type=str,
        default="",
        help="ベースディレクトリ（デフォルト: 自動検出）"
    )
    
    parser.add_argument(
        "--tables",
        nargs="*",
        help="チェック対象テーブル（指定しない場合は全テーブル）"
    )
    
    parser.add_argument(
        "--checks",
        nargs="*",
        help="実行するチェック（指定しない場合は全チェック）"
    )
    
    # 修正提案オプション
    parser.add_argument(
        "--suggest-fixes",
        action="store_true",
        help="修正提案を生成"
    )
    
    parser.add_argument(
        "--fix-types",
        type=str,
        default="all",
        help="修正タイプ（ddl,yaml,insert,all）カンマ区切り"
    )
    
    parser.add_argument(
        "--auto-apply",
        action="store_true",
        help="修正を自動適用（危険）"
    )
    
    parser.add_argument(
        "--output-fixes",
        type=str,
        help="修正提案の出力先ディレクトリ"
    )
    
    # 出力オプション
    parser.add_argument(
        "--output-format",
        choices=["console", "markdown", "json"],
        default="console",
        help="出力形式"
    )
    
    parser.add_argument(
        "--output-file",
        type=str,
        help="出力ファイル（指定しない場合は標準出力）"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="詳細ログを出力"
    )
    
    # レポート管理オプション
    parser.add_argument(
        "--report-dir",
        type=str,
        default="reports",
        help="レポート出力ディレクトリ（デフォルト: reports）"
    )
    
    parser.add_argument(
        "--keep-reports",
        type=int,
        default=30,
        help="レポート保持日数（デフォルト: 30日）"
    )
    
    parser.add_argument(
        "--max-reports",
        type=int,
        default=100,
        help="最大レポート数（デフォルト: 100件）"
    )
    
    parser.add_argument(
        "--report-prefix",
        type=str,
        help="レポートファイルのカスタムプレフィックス"
    )
    
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="古いレポートの自動クリーンアップを無効化"
    )
    
    # サンプルデータ生成オプション
    parser.add_argument(
        "--generate-sample-data",
        action="store_true",
        help="サンプルデータINSERT文を生成"
    )
    
    parser.add_argument(
        "--validate-sample-data",
        action="store_true",
        help="サンプルデータ生成時に検証も実行"
    )
    
    # その他
    parser.add_argument(
        "--list-checks",
        action="store_true",
        help="利用可能なチェック一覧を表示"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Database Consistency Checker 1.0.0"
    )
    
    return parser


def main():
    """メイン関数"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # ログ設定の初期化
    logger = get_logger("consistency_checker")
    perf_logger = get_performance_logger("consistency_checker")
    
    # 設定の初期化
    try:
        config = get_config(args.base_dir)
        setup_logging(config)
        
        check_config = create_check_config(
            enabled_checks=args.checks or [],
            output_format=args.output_format,
            verbose=args.verbose
        )
        
        logger.log_tool_start("consistency_checker", 
                            base_dir=str(config.paths.base_dir),
                            tables=args.tables,
                            checks=args.checks)
        
    except Exception as e:
        print(f"❌ 設定初期化エラー: {e}", file=sys.stderr)
        sys.exit(1)
    
    # チェッカーの初期化
    try:
        checker = ConsistencyChecker(config, check_config)
    except Exception as e:
        logger.error(f"チェッカー初期化エラー: {e}")
        sys.exit(1)
    
    # 利用可能なチェック一覧の表示
    if args.list_checks:
        print("利用可能なチェック:")
        for check_name in checker.get_available_checks():
            print(f"  - {check_name}")
        return
    
    # チェック名の妥当性確認
    if args.checks:
        invalid_checks = checker.validate_check_names(args.checks)
        if invalid_checks:
            print(f"❌ 無効なチェック名: {', '.join(invalid_checks)}", file=sys.stderr)
            print("利用可能なチェック:")
            for check_name in checker.get_available_checks():
                print(f"  - {check_name}")
            sys.exit(1)
    
    # サンプルデータ生成の実行
    if args.generate_sample_data:
        try:
            generator = SampleDataGenerator(
                base_dir=config.base_dir,
                verbose=args.verbose
            )
            
            # 対象テーブルの設定
            target_tables = args.tables if args.tables else None
            
            # サンプルデータ生成実行
            generator.generate_all_sample_data(target_tables)
            
            # 検証も実行する場合
            if args.validate_sample_data:
                print("\n=== サンプルデータ検証実行 ===")
                if args.checks:
                    report = checker.run_specific_checks(args.checks)
                else:
                    report = checker.run_all_checks()
                
                # レポート出力
                output_report(report, check_config, config)
            
            return
            
        except Exception as e:
            print(f"❌ サンプルデータ生成エラー: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    # 通常のチェック実行
    try:
        if args.checks:
            report = checker.run_specific_checks(args.checks)
        else:
            report = checker.run_all_checks()
    except Exception as e:
        print(f"❌ チェック実行エラー: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    # レポート出力
    try:
        output_report(report, check_config, config) # config引数を追加
    except Exception as e:
        print(f"❌ レポート出力エラー: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 終了コードの決定
    if hasattr(report, 'summary'):
        if hasattr(report.summary, 'error_count'):
            # ConsistencyReportオブジェクトの場合
            error_count = report.summary.error_count + report.summary.critical_count
        else:
            # dictの場合
            error_count = report.summary.get('error', 0) + report.summary.get('critical', 0)
    else:
        error_count = 0
        
    if error_count > 0:
        sys.exit(1)  # エラーがある場合は非ゼロで終了
    else:
        sys.exit(0)  # 成功


def output_report(report, check_config, config): # config引数を追加
    """レポートを出力"""
    # レポーター初期化
    if check_config.output_format == "console":
        reporter = ConsoleReporter()
    elif check_config.output_format == "markdown":
        reporter = MarkdownReporter()
    elif check_config.output_format == "json":
        reporter = JsonReporter()
    else:
        raise ValueError(f"サポートされていない出力形式: {check_config.output_format}")
    
    # レポート生成
    output_content = reporter.generate_report(report)
    
    # レポート管理機能を使用
    if check_config.output_file:
        # 従来の方式（ユーザー指定ファイル）
        output_path = Path(check_config.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output_content)
        
        print(f"📄 レポートを出力しました: {output_path}")
    else:
        # 新しいレポート管理機能を使用
        if check_config.output_format != "console":
            # レポートマネージャー初期化
            report_manager = ReportManager(
                base_dir=config.base_dir,
                report_dir=check_config.report_dir
            )
            
            # レポートファイルパス取得
            report_path = report_manager.get_report_path(
                report_type="consistency_report",
                extension=_get_file_extension(check_config.output_format),
                custom_prefix=check_config.report_prefix
            )
            
            # レポート出力
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(output_content)
            
            # 最新レポートリンク作成
            link_name = f"latest_consistency_report.{_get_file_extension(check_config.output_format)}"
            report_manager.create_latest_link(report_path, link_name)
            
            # 古いレポートのクリーンアップ
            if check_config.auto_cleanup:
                try:
                    report_manager.cleanup_old_reports(
                        keep_days=check_config.keep_reports,
                        max_reports=check_config.max_reports
                    )
                except Exception as e:
                    if check_config.verbose:
                        print(f"⚠️ レポートクリーンアップエラー: {e}")
            
            print(f"📄 レポートを出力しました: {report_path}")
            print(f"🔗 最新レポートリンク: {report_manager.report_dir / link_name}")
            
            # レポート統計表示（詳細モード時）
            if check_config.verbose:
                stats = report_manager.get_report_statistics()
                print(f"📊 レポート統計: 総数{stats['total_reports']}件, 総サイズ{stats['total_size_mb']}MB")
        else:
            # コンソール出力（既に出力済み）
            pass


def _get_file_extension(output_format: str) -> str:
    """出力形式からファイル拡張子を取得"""
    extension_map = {
        "markdown": "md",
        "json": "json",
        "console": "txt"
    }
    return extension_map.get(output_format, "txt")


if __name__ == "__main__":
    main()
