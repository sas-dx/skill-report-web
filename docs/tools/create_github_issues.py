#!/usr/bin/env python3
"""
統一設計ツール完成 - GitHub Issues自動作成スクリプト

このスクリプトは統一設計ツール完成に向けた10個のIssueを
GitHub APIを使用して自動作成します。

使用方法:
    python create_github_issues.py --token YOUR_GITHUB_TOKEN --repo owner/repo

要求仕様ID: PLT.1-WEB.1
"""

import argparse
import json
import requests
import sys
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class GitHubIssueCreator:
    """GitHub Issue自動作成クラス"""
    
    def __init__(self, token: str, repo: str):
        """
        初期化
        
        Args:
            token: GitHub Personal Access Token
            repo: リポジトリ名 (owner/repo形式)
        """
        self.token = token
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{repo}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        }
    
    def create_labels(self) -> bool:
        """
        必要なラベルを作成
        
        Returns:
            bool: 成功時True
        """
        labels = [
            # Priority Labels
            {"name": "priority: critical", "color": "d73a49", "description": "最優先タスク"},
            {"name": "priority: high", "color": "f66a0a", "description": "高優先タスク"},
            {"name": "priority: medium", "color": "fbca04", "description": "中優先タスク"},
            {"name": "priority: low", "color": "0e8a16", "description": "低優先タスク"},
            
            # Category Labels
            {"name": "category: ai", "color": "7057ff", "description": "AI駆動機能"},
            {"name": "category: config", "color": "0052cc", "description": "設定システム"},
            {"name": "category: integration", "color": "54aeff", "description": "統合実行"},
            {"name": "category: web-ui", "color": "ff69b4", "description": "Web UIダッシュボード"},
            {"name": "category: testing", "color": "6f42c1", "description": "テスト・品質保証"},
            {"name": "category: docs", "color": "8b4513", "description": "ドキュメント"},
            
            # Status Labels
            {"name": "status: ready", "color": "0e8a16", "description": "着手可能"},
            {"name": "status: in-progress", "color": "fbca04", "description": "作業中"},
            {"name": "status: blocked", "color": "d73a49", "description": "ブロック中"},
            {"name": "status: review", "color": "0052cc", "description": "レビュー待ち"},
        ]
        
        print("🏷️ ラベル作成中...")
        for label in labels:
            try:
                response = requests.post(
                    f"{self.base_url}/labels",
                    headers=self.headers,
                    json=label
                )
                if response.status_code == 201:
                    print(f"  ✅ ラベル作成成功: {label['name']}")
                elif response.status_code == 422:
                    print(f"  ⚠️ ラベル既存: {label['name']}")
                else:
                    print(f"  ❌ ラベル作成失敗: {label['name']} - {response.status_code}")
            except Exception as e:
                print(f"  ❌ エラー: {label['name']} - {e}")
        
        return True
    
    def create_milestones(self) -> Dict[str, int]:
        """
        マイルストーンを作成
        
        Returns:
            Dict[str, int]: マイルストーン名とIDのマッピング
        """
        today = datetime.now()
        milestones = [
            {
                "title": "AI機能完成",
                "description": "AI駆動機能（analytics.py, dashboard.py, プロンプトテンプレート）の完全実装",
                "due_on": (today + timedelta(days=2)).isoformat() + "Z"
            },
            {
                "title": "統合システム完成",
                "description": "統合実行システム・設定システム・CLIコマンドの完成",
                "due_on": (today + timedelta(days=5)).isoformat() + "Z"
            },
            {
                "title": "品質保証完成",
                "description": "Web UI・テスト・ドキュメントの完成、本格運用可能レベル到達",
                "due_on": (today + timedelta(days=7)).isoformat() + "Z"
            }
        ]
        
        milestone_map = {}
        print("📅 マイルストーン作成中...")
        
        for milestone in milestones:
            try:
                response = requests.post(
                    f"{self.base_url}/milestones",
                    headers=self.headers,
                    json=milestone
                )
                if response.status_code == 201:
                    milestone_data = response.json()
                    milestone_map[milestone["title"]] = milestone_data["number"]
                    print(f"  ✅ マイルストーン作成成功: {milestone['title']}")
                else:
                    print(f"  ❌ マイルストーン作成失敗: {milestone['title']} - {response.status_code}")
            except Exception as e:
                print(f"  ❌ エラー: {milestone['title']} - {e}")
        
        return milestone_map
    
    def get_issue_templates(self, milestone_map: Dict[str, int]) -> List[Dict]:
        """
        Issue作成用のテンプレートを取得
        
        Args:
            milestone_map: マイルストーン名とIDのマッピング
            
        Returns:
            List[Dict]: Issue作成用データのリスト
        """
        return [
            {
                "title": "[AI] リアルタイム分析機能の実装 (analytics.py)",
                "body": """## 📋 概要
統一設計ツールのAI駆動機能として、リアルタイム分析機能を実装します。

## 🎯 要求仕様ID
- PLT.1-WEB.1
- 設計書: docs/design/architecture/技術スタック設計書.md

## 📝 実装内容

### 対象ファイル
- `docs/tools/unified/ai/analytics.py`

### 実装機能
1. **リアルタイムファイル監視**
   - ファイル変更の自動検知（watchdog使用）
   - 変更内容の分析
   - 影響範囲の特定

2. **品質メトリクス分析**
   - コード品質スコア計算
   - 設計書整合性チェック
   - 要求仕様ID追跡

3. **パフォーマンス分析**
   - 処理時間測定
   - メモリ使用量監視
   - ボトルネック特定

4. **統合分析レポート**
   - 総合品質スコア
   - 改善提案
   - トレンド分析

## ✅ 受入条件
- [ ] `analytics.py` ファイル作成
- [ ] リアルタイム分析機能実装
- [ ] 品質メトリクス計算機能
- [ ] パフォーマンス分析機能
- [ ] 統合レポート生成機能
- [ ] テストケース作成
- [ ] ドキュメント更新

## 🔗 関連Issue
- 依存: なし
- 関連: Issue #2 (AI dashboard.py 実装)

## 📅 期限・工数
- **期限**: 2日以内（最優先タスク）
- **工数**: 1.5日""",
                "labels": ["priority: critical", "category: ai", "status: ready", "enhancement"],
                "milestone": milestone_map.get("AI機能完成")
            },
            {
                "title": "[AI] Web UIダッシュボード機能の実装 (dashboard.py)",
                "body": """## 📋 概要
統一設計ツールのWeb UIダッシュボード機能を実装します。

## 🎯 要求仕様ID
- PLT.1-WEB.1
- 設計書: docs/design/architecture/技術スタック設計書.md

## 📝 実装内容

### 対象ファイル
- `docs/tools/unified/ai/dashboard.py`

### 実装機能
1. **Flask Webアプリケーション**
   - Webサーバー起動
   - ルーティング設定
   - テンプレートエンジン

2. **リアルタイムダッシュボード**
   - 分析結果表示
   - 進捗状況可視化
   - インタラクティブUI

3. **WebSocket通信**
   - リアルタイム更新
   - 双方向通信
   - 状態同期

4. **REST API**
   - データ取得API
   - 設定変更API
   - 実行制御API

## ✅ 受入条件
- [ ] `dashboard.py` ファイル作成
- [ ] Flask アプリケーション実装
- [ ] WebSocket通信機能
- [ ] リアルタイム更新機能
- [ ] REST API実装
- [ ] HTMLテンプレート作成
- [ ] CSS・JavaScript実装
- [ ] テストケース作成

## 🔗 関連Issue
- 依存: Issue #1 (analytics.py)
- 関連: Issue #8 (Web UIダッシュボード)

## 📅 期限・工数
- **期限**: 2日以内
- **工数**: 2日""",
                "labels": ["priority: critical", "category: ai", "status: ready", "enhancement"],
                "milestone": milestone_map.get("AI機能完成")
            },
            {
                "title": "[AI] プロンプトテンプレートの作成",
                "body": """## 📋 概要
AI駆動設計書生成用のプロンプトテンプレートを作成します。

## 🎯 要求仕様ID
- PLT.1-WEB.1
- 設計書: docs/design/architecture/技術スタック設計書.md

## 📝 実装内容

### 対象ディレクトリ
- `docs/tools/unified/ai/prompts/`

### 作成ファイル
1. **database_design.txt** - データベース設計書生成用
2. **api_specification.txt** - API仕様書生成用
3. **screen_design.txt** - 画面設計書生成用
4. **test_scenario.txt** - テストシナリオ生成用
5. **code_review.txt** - コードレビュー用

## ✅ 受入条件
- [ ] `prompts/` ディレクトリ作成
- [ ] 5つのプロンプトテンプレート作成
- [ ] プロンプト品質テスト
- [ ] 使用方法ドキュメント作成

## 📅 期限・工数
- **期限**: 1日以内
- **工数**: 0.5日""",
                "labels": ["priority: critical", "category: ai", "status: ready", "enhancement"],
                "milestone": milestone_map.get("AI機能完成")
            },
            {
                "title": "[Integration] メインエントリーポイント実装 (__main__.py)",
                "body": """## 📋 概要
統一設計ツールのメインエントリーポイントを実装します。

## 🎯 要求仕様ID
- PLT.1-WEB.1
- 設計書: docs/design/architecture/技術スタック設計書.md

## 📝 実装内容

### 対象ファイル
- `docs/tools/unified/__main__.py`

### 実装機能
1. **CLI引数解析** - argparse使用
2. **基本コマンド** - init, run, status, help
3. **設定管理** - 設定ファイル読み込み
4. **エラーハンドリング** - 例外処理・ログ出力

## ✅ 受入条件
- [ ] `__main__.py` ファイル作成
- [ ] CLI引数解析機能
- [ ] 基本コマンド実装
- [ ] 設定管理機能
- [ ] エラーハンドリング
- [ ] テストケース作成

## 📅 期限・工数
- **期限**: 2日以内
- **工数**: 1日""",
                "labels": ["priority: critical", "category: integration", "status: ready", "enhancement"],
                "milestone": milestone_map.get("AI機能完成")
            },
            {
                "title": "[Config] 統合設定システムの完成",
                "body": """## 📋 概要
統合設定システムを完成させ、全ツールの設定を統一管理します。

## 🎯 要求仕様ID
- PLT.1-WEB.1

## 📝 実装内容
1. **プロジェクト固有設定詳細化**
2. **AI統合設定**
3. **設定バリデーション強化**

## ✅ 受入条件
- [ ] プロジェクト固有設定の詳細化
- [ ] AI統合設定ファイル作成
- [ ] 設定バリデーション強化
- [ ] テストケース作成

## 📅 期限・工数
- **期限**: 3日以内
- **工数**: 1日""",
                "labels": ["priority: high", "category: config", "status: ready", "enhancement"],
                "milestone": milestone_map.get("統合システム完成")
            },
            {
                "title": "[Integration] 統合実行システムの実装",
                "body": """## 📋 概要
全ツールを統合実行するシステムを実装します。

## 📝 実装内容
1. **統合実行エンジン**
2. **段階的実行制御**
3. **エラーハンドリング・ロールバック**
4. **実行結果管理**

## ✅ 受入条件
- [ ] 統合実行エンジン実装
- [ ] 段階的実行制御
- [ ] エラーハンドリング機能
- [ ] 実行結果管理

## 📅 期限・工数
- **期限**: 5日以内
- **工数**: 2日""",
                "labels": ["priority: high", "category: integration", "status: ready", "enhancement"],
                "milestone": milestone_map.get("統合システム完成")
            },
            {
                "title": "[Integration] CLIコマンドシステムの実装",
                "body": """## 📋 概要
CLIコマンドシステムを実装し、コマンドライン操作を充実させます。

## 📝 実装内容
1. **基本コマンド** - init, run, status, config
2. **サブコマンド** - database, ai, web等
3. **オプション機能** - verbose, dry-run等

## ✅ 受入条件
- [ ] 基本コマンド実装
- [ ] サブコマンド対応
- [ ] オプション機能実装
- [ ] テストケース作成

## 📅 期限・工数
- **期限**: 5日以内
- **工数**: 1.5日""",
                "labels": ["priority: high", "category: integration", "status: ready", "enhancement"],
                "milestone": milestone_map.get("統合システム完成")
            },
            {
                "title": "[Web UI] Flaskダッシュボードの実装",
                "body": """## 📋 概要
Flask Webアプリケーションとしてダッシュボードを実装します。

## 📝 実装内容
1. **Flask アプリケーション**
2. **HTMLテンプレート**
3. **CSS・JavaScript**
4. **API エンドポイント**

## ✅ 受入条件
- [ ] Flask アプリケーション実装
- [ ] HTMLテンプレート作成
- [ ] CSS・JavaScript実装
- [ ] API エンドポイント実装

## 📅 期限・工数
- **期限**: 7日以内
- **工数**: 2日""",
                "labels": ["priority: medium", "category: web-ui", "status: ready", "enhancement"],
                "milestone": milestone_map.get("品質保証完成")
            },
            {
                "title": "[Testing] 包括的テストスイートの実装",
                "body": """## 📋 概要
包括的なテストスイートを実装し、品質保証を強化します。

## 📝 実装内容
1. **ユニットテスト**
2. **統合テスト**
3. **E2Eテスト**
4. **CI/CD統合**

## ✅ 受入条件
- [ ] ユニットテスト実装
- [ ] 統合テスト実装
- [ ] E2Eテスト実装
- [ ] カバレッジ80%以上

## 📅 期限・工数
- **期限**: 7日以内
- **工数**: 2日""",
                "labels": ["priority: medium", "category: testing", "status: ready", "enhancement"],
                "milestone": milestone_map.get("品質保証完成")
            },
            {
                "title": "[Docs] 詳細ドキュメントの作成",
                "body": """## 📋 概要
統一設計ツールの詳細ドキュメントを作成します。

## 📝 実装内容
1. **詳細使用方法**
2. **チュートリアル**
3. **API リファレンス**
4. **実行例・サンプル**

## ✅ 受入条件
- [ ] README.md 詳細化
- [ ] TUTORIAL.md 作成
- [ ] API_REFERENCE.md 作成
- [ ] EXAMPLES.md 作成

## 📅 期限・工数
- **期限**: 7日以内
- **工数**: 1日""",
                "labels": ["priority: low", "category: docs", "status: ready", "documentation"],
                "milestone": milestone_map.get("品質保証完成")
            }
        ]
    
    def create_issues(self, issues: List[Dict]) -> List[int]:
        """
        Issueを作成
        
        Args:
            issues: Issue作成用データのリスト
            
        Returns:
            List[int]: 作成されたIssue番号のリスト
        """
        created_issues = []
        print("📝 Issue作成中...")
        
        for i, issue in enumerate(issues, 1):
            try:
                response = requests.post(
                    f"{self.base_url}/issues",
                    headers=self.headers,
                    json=issue
                )
                if response.status_code == 201:
                    issue_data = response.json()
                    created_issues.append(issue_data["number"])
                    print(f"  ✅ Issue #{i} 作成成功: {issue['title']}")
                else:
                    print(f"  ❌ Issue #{i} 作成失敗: {issue['title']} - {response.status_code}")
                    print(f"     レスポンス: {response.text}")
            except Exception as e:
                print(f"  ❌ エラー: Issue #{i} - {e}")
        
        return created_issues
    
    def run(self) -> bool:
        """
        全体実行
        
        Returns:
            bool: 成功時True
        """
        print("🚀 統一設計ツール GitHub Issues 自動作成開始")
        print(f"📍 対象リポジトリ: {self.repo}")
        print()
        
        # 1. ラベル作成
        if not self.create_labels():
            print("❌ ラベル作成に失敗しました")
            return False
        print()
        
        # 2. マイルストーン作成
        milestone_map = self.create_milestones()
        if not milestone_map:
            print("❌ マイルストーン作成に失敗しました")
            return False
        print()
        
        # 3. Issue作成
        issues = self.get_issue_templates(milestone_map)
        created_issues = self.create_issues(issues)
        print()
        
        # 4. 結果表示
        print("🎯 作成結果:")
        print(f"  📊 作成されたIssue数: {len(created_issues)}/10")
        print(f"  🏷️ 作成されたラベル数: 14")
        print(f"  📅 作成されたマイルストーン数: {len(milestone_map)}")
        print()
        
        if len(created_issues) == 10:
            print("✅ 全てのIssueが正常に作成されました！")
            print("🔗 次のステップ:")
            print("  1. GitHub Project Board作成")
            print("  2. Issue間の依存関係設定")
            print("  3. 開発開始！")
            return True
        else:
            print("⚠️ 一部のIssue作成に失敗しました")
            return False

def main():
    """メイン関数"""
    parser = argparse.ArgumentParser(
        description="統一設計ツール完成 - GitHub Issues自動作成"
    )
    parser.add_argument(
        "--token",
        required=True,
        help="GitHub Personal Access Token"
    )
    parser.add_argument(
        "--repo",
        required=True,
        help="リポジトリ名 (owner/repo形式)"
    )
    
    args = parser.parse_args()
    
    # Issue作成実行
    creator = GitHubIssueCreator(args.token, args.repo)
    success = creator.run()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
