"""
設計統合ツール - レポート生成モジュール
要求仕様ID: PLT.1-WEB.1

設計統合の結果をレポート形式で出力する機能を提供します。
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

from ..core.config import DesignIntegrationConfig
from ..core.exceptions import DesignIntegrationError
from ..core.logger import get_logger


class ReportGenerator:
    """レポート生成クラス"""
    
    def __init__(self, config: DesignIntegrationConfig):
        """
        初期化
        
        Args:
            config: 設計統合ツール設定
        """
        self.config = config
        self.logger = get_logger(__name__)
        
        # レポート出力ディレクトリ
        self.reports_dir = config.project_root / "docs" / "tools" / "reports"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_integration_report(
        self,
        database_stats: Dict[str, Any],
        api_stats: Dict[str, Any],
        screen_stats: Dict[str, Any],
        validation_results: Dict[str, Any],
        output_format: str = "markdown"
    ) -> str:
        """
        統合レポートを生成
        
        Args:
            database_stats: データベース統計情報
            api_stats: API統計情報
            screen_stats: 画面統計情報
            validation_results: 検証結果
            output_format: 出力形式 ("markdown", "json", "html")
            
        Returns:
            生成されたレポートファイルのパス
        """
        self.logger.info("統合レポートの生成を開始")
        
        try:
            # レポートデータの構築
            report_data = self._build_report_data(
                database_stats, api_stats, screen_stats, validation_results
            )
            
            # 出力形式に応じてレポート生成
            if output_format.lower() == "markdown":
                report_path = self._generate_markdown_report(report_data)
            elif output_format.lower() == "json":
                report_path = self._generate_json_report(report_data)
            elif output_format.lower() == "html":
                report_path = self._generate_html_report(report_data)
            else:
                raise DesignIntegrationError(f"サポートされていない出力形式: {output_format}")
            
            self.logger.info(f"統合レポートが生成されました: {report_path}")
            return str(report_path)
            
        except Exception as e:
            self.logger.error(f"統合レポート生成エラー: {e}")
            raise DesignIntegrationError(f"統合レポート生成に失敗しました: {e}")
    
    def _build_report_data(
        self,
        database_stats: Dict[str, Any],
        api_stats: Dict[str, Any],
        screen_stats: Dict[str, Any],
        validation_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        レポートデータを構築
        
        Args:
            database_stats: データベース統計情報
            api_stats: API統計情報
            screen_stats: 画面統計情報
            validation_results: 検証結果
            
        Returns:
            レポートデータ辞書
        """
        timestamp = datetime.now().isoformat()
        
        return {
            "metadata": {
                "generated_at": timestamp,
                "project_name": "年間スキル報告書WEB化PJT",
                "tool_version": "1.0.0",
                "report_type": "設計統合レポート"
            },
            "summary": {
                "total_tables": database_stats.get('total_tables', 0),
                "total_apis": api_stats.get('total_apis', 0),
                "total_screens": screen_stats.get('total_screens', 0),
                "validation_success_rate": self._calculate_success_rate(validation_results),
                "issues_count": self._count_total_issues(database_stats, api_stats, screen_stats)
            },
            "database": database_stats,
            "api": api_stats,
            "screens": screen_stats,
            "validation": validation_results,
            "recommendations": self._generate_recommendations(
                database_stats, api_stats, screen_stats, validation_results
            )
        }
    
    def _calculate_success_rate(self, validation_results: Dict[str, Any]) -> float:
        """
        検証成功率を計算
        
        Args:
            validation_results: 検証結果
            
        Returns:
            成功率（0.0-1.0）
        """
        try:
            total_validations = 0
            successful_validations = 0
            
            for category, results in validation_results.items():
                if isinstance(results, dict):
                    if 'success' in results:
                        total_validations += 1
                        if results['success']:
                            successful_validations += 1
                    elif 'total' in results and 'success' in results:
                        total_validations += results['total']
                        successful_validations += results['success']
            
            return successful_validations / total_validations if total_validations > 0 else 0.0
            
        except Exception:
            return 0.0
    
    def _count_total_issues(
        self,
        database_stats: Dict[str, Any],
        api_stats: Dict[str, Any],
        screen_stats: Dict[str, Any]
    ) -> int:
        """
        総問題数を計算
        
        Args:
            database_stats: データベース統計情報
            api_stats: API統計情報
            screen_stats: 画面統計情報
            
        Returns:
            総問題数
        """
        total_issues = 0
        
        total_issues += database_stats.get('tables_with_issues', 0)
        total_issues += api_stats.get('apis_with_issues', 0)
        total_issues += screen_stats.get('screens_with_issues', 0)
        
        return total_issues
    
    def _generate_recommendations(
        self,
        database_stats: Dict[str, Any],
        api_stats: Dict[str, Any],
        screen_stats: Dict[str, Any],
        validation_results: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        改善提案を生成
        
        Args:
            database_stats: データベース統計情報
            api_stats: API統計情報
            screen_stats: 画面統計情報
            validation_results: 検証結果
            
        Returns:
            改善提案のリスト
        """
        recommendations = []
        
        # データベース関連の提案
        if database_stats.get('tables_with_issues', 0) > 0:
            recommendations.append({
                "category": "データベース",
                "priority": "高",
                "title": "テーブル設計の問題解決",
                "description": f"{database_stats['tables_with_issues']}個のテーブルに問題があります。YAML形式の検証と必須セクションの確認を実施してください。"
            })
        
        # API関連の提案
        if api_stats.get('apis_with_issues', 0) > 0:
            recommendations.append({
                "category": "API",
                "priority": "高",
                "title": "API設計の問題解決",
                "description": f"{api_stats['apis_with_issues']}個のAPIに問題があります。エンドポイント形式とレスポンス定義を確認してください。"
            })
        
        # 画面関連の提案
        if screen_stats.get('screens_with_issues', 0) > 0:
            recommendations.append({
                "category": "画面",
                "priority": "高",
                "title": "画面設計の問題解決",
                "description": f"{screen_stats['screens_with_issues']}個の画面に問題があります。コンポーネント定義とレスポンシブ対応を確認してください。"
            })
        
        # レスポンシブ対応の提案
        total_screens = screen_stats.get('total_screens', 0)
        responsive_screens = screen_stats.get('responsive_screens', 0)
        if total_screens > 0 and responsive_screens / total_screens < 0.8:
            recommendations.append({
                "category": "画面",
                "priority": "中",
                "title": "レスポンシブ対応の強化",
                "description": f"レスポンシブ対応率が{responsive_screens/total_screens:.1%}です。全画面でのレスポンシブ対応を推奨します。"
            })
        
        # 要求仕様ID対応の提案
        for stats_name, stats in [("データベース", database_stats), ("API", api_stats), ("画面", screen_stats)]:
            req_coverage = stats.get('requirement_coverage', {})
            if not req_coverage:
                recommendations.append({
                    "category": stats_name,
                    "priority": "中",
                    "title": "要求仕様ID対応の強化",
                    "description": f"{stats_name}設計で要求仕様IDの対応が不十分です。全設計要素に要求仕様IDを明記してください。"
                })
        
        return recommendations
    
    def _generate_markdown_report(self, report_data: Dict[str, Any]) -> Path:
        """
        Markdownレポートを生成
        
        Args:
            report_data: レポートデータ
            
        Returns:
            生成されたレポートファイルのパス
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.reports_dir / f"design_integration_report_{timestamp}.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self._build_markdown_content(report_data))
        
        return report_path
    
    def _build_markdown_content(self, report_data: Dict[str, Any]) -> str:
        """
        Markdownコンテンツを構築
        
        Args:
            report_data: レポートデータ
            
        Returns:
            Markdownコンテンツ
        """
        metadata = report_data['metadata']
        summary = report_data['summary']
        database = report_data['database']
        api = report_data['api']
        screens = report_data['screens']
        recommendations = report_data['recommendations']
        
        content = f"""# 設計統合レポート

## エグゼクティブサマリー

このレポートは{metadata['project_name']}の設計統合状況を包括的に分析した結果です。データベース設計、API設計、画面設計の統計情報と検証結果を提供し、品質向上のための具体的な改善提案を含んでいます。現在の設計品質と整合性を評価し、プロジェクト成功に向けた次のアクションプランを明確に示しています。

## 基本情報

- **生成日時**: {metadata['generated_at']}
- **プロジェクト**: {metadata['project_name']}
- **ツールバージョン**: {metadata['tool_version']}
- **レポート種別**: {metadata['report_type']}

## 概要

| 項目 | 値 |
|------|-----|
| 総テーブル数 | {summary['total_tables']} |
| 総API数 | {summary['total_apis']} |
| 総画面数 | {summary['total_screens']} |
| 検証成功率 | {summary['validation_success_rate']:.1%} |
| 問題件数 | {summary['issues_count']} |

## データベース設計

### 統計情報

- **総テーブル数**: {database.get('total_tables', 0)}
- **マスタテーブル**: {database.get('master_tables', 0)}
- **トランザクションテーブル**: {database.get('transaction_tables', 0)}
- **履歴テーブル**: {database.get('history_tables', 0)}
- **システムテーブル**: {database.get('system_tables', 0)}
- **総カラム数**: {database.get('total_columns', 0)}
- **問題のあるテーブル**: {database.get('tables_with_issues', 0)}

### カテゴリ別分布

"""
        
        # データベースカテゴリ別分布
        tables_by_category = database.get('tables_by_category', {})
        for category, count in tables_by_category.items():
            content += f"- **{category}**: {count}テーブル\n"
        
        content += f"""

## API設計

### 統計情報

- **総API数**: {api.get('total_apis', 0)}
- **問題のあるAPI**: {api.get('apis_with_issues', 0)}

### HTTPメソッド別分布

"""
        
        # APIメソッド別分布
        methods = api.get('methods', {})
        for method, count in methods.items():
            content += f"- **{method}**: {count}API\n"
        
        content += f"""

### エンドポイントカテゴリ別分布

"""
        
        # エンドポイントカテゴリ別分布
        endpoints_by_category = api.get('endpoints_by_category', {})
        for category, count in endpoints_by_category.items():
            content += f"- **{category}**: {count}API\n"
        
        content += f"""

## 画面設計

### 統計情報

- **総画面数**: {screens.get('total_screens', 0)}
- **総コンポーネント数**: {screens.get('total_components', 0)}
- **レスポンシブ対応画面**: {screens.get('responsive_screens', 0)}
- **問題のある画面**: {screens.get('screens_with_issues', 0)}

### カテゴリ別分布

"""
        
        # 画面カテゴリ別分布
        screens_by_category = screens.get('screens_by_category', {})
        for category, count in screens_by_category.items():
            content += f"- **{category}**: {count}画面\n"
        
        content += """

## 改善提案

"""
        
        # 改善提案
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                content += f"""
### {i}. {rec['title']} (優先度: {rec['priority']})

**カテゴリ**: {rec['category']}

{rec['description']}

"""
        else:
            content += "現在、特に改善が必要な項目はありません。\n"
        
        content += f"""

## 次のアクション

1. **問題解決**: 検出された{summary['issues_count']}件の問題を優先的に解決
2. **品質向上**: 検証成功率{summary['validation_success_rate']:.1%}の向上を目指す
3. **継続的改善**: 定期的な設計統合チェックの実施

---

*このレポートは設計統合ツールにより自動生成されました。*
"""
        
        return content
    
    def _generate_json_report(self, report_data: Dict[str, Any]) -> Path:
        """
        JSONレポートを生成
        
        Args:
            report_data: レポートデータ
            
        Returns:
            生成されたレポートファイルのパス
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.reports_dir / f"design_integration_report_{timestamp}.json"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        return report_path
    
    def _generate_html_report(self, report_data: Dict[str, Any]) -> Path:
        """
        HTMLレポートを生成
        
        Args:
            report_data: レポートデータ
            
        Returns:
            生成されたレポートファイルのパス
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.reports_dir / f"design_integration_report_{timestamp}.html"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self._build_html_content(report_data))
        
        return report_path
    
    def _build_html_content(self, report_data: Dict[str, Any]) -> str:
        """
        HTMLコンテンツを構築
        
        Args:
            report_data: レポートデータ
            
        Returns:
            HTMLコンテンツ
        """
        metadata = report_data['metadata']
        summary = report_data['summary']
        
        return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>設計統合レポート - {metadata['project_name']}</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; line-height: 1.6; }}
        .header {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 30px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }}
        .card {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric {{ text-align: center; }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
        .metric-label {{ color: #6c757d; margin-top: 5px; }}
        .section {{ margin-bottom: 40px; }}
        h1 {{ color: #343a40; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #495057; border-bottom: 1px solid #dee2e6; padding-bottom: 5px; }}
        .recommendations {{ background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; padding: 20px; }}
        .recommendation {{ margin-bottom: 15px; padding: 10px; background: white; border-radius: 4px; }}
        .priority-high {{ border-left: 4px solid #dc3545; }}
        .priority-medium {{ border-left: 4px solid #ffc107; }}
        .priority-low {{ border-left: 4px solid #28a745; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>設計統合レポート</h1>
        <p><strong>プロジェクト:</strong> {metadata['project_name']}</p>
        <p><strong>生成日時:</strong> {metadata['generated_at']}</p>
    </div>
    
    <div class="summary">
        <div class="card metric">
            <div class="metric-value">{summary['total_tables']}</div>
            <div class="metric-label">総テーブル数</div>
        </div>
        <div class="card metric">
            <div class="metric-value">{summary['total_apis']}</div>
            <div class="metric-label">総API数</div>
        </div>
        <div class="card metric">
            <div class="metric-value">{summary['total_screens']}</div>
            <div class="metric-label">総画面数</div>
        </div>
        <div class="card metric">
            <div class="metric-value">{summary['validation_success_rate']:.1%}</div>
            <div class="metric-label">検証成功率</div>
        </div>
        <div class="card metric">
            <div class="metric-value">{summary['issues_count']}</div>
            <div class="metric-label">問題件数</div>
        </div>
    </div>
    
    <div class="section">
        <h2>改善提案</h2>
        <div class="recommendations">
"""
        
        # 改善提案をHTMLで追加
        recommendations = report_data['recommendations']
        if recommendations:
            for rec in recommendations:
                priority_class = f"priority-{rec['priority'].lower()}"
                content += f"""
            <div class="recommendation {priority_class}">
                <h3>{rec['title']}</h3>
                <p><strong>カテゴリ:</strong> {rec['category']} | <strong>優先度:</strong> {rec['priority']}</p>
                <p>{rec['description']}</p>
            </div>
"""
        else:
            content += "<p>現在、特に改善が必要な項目はありません。</p>"
        
        content += """
        </div>
    </div>
    
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6; color: #6c757d; text-align: center;">
        <p>このレポートは設計統合ツールにより自動生成されました。</p>
    </footer>
</body>
</html>"""
        
        return content
