# 統合設計ツール共通機能リファクタリング計画

## エグゼクティブサマリー

統合設計ツールエコシステムにおける各設計ツール（データベース・API・画面・テスト）の共通機能を統一管理するためのリファクタリング計画です。現在データベース設計ツールの `shared/` ディレクトリに分散している共通機能を、統合設計ツールレベルの `docs/tools/shared/` に昇格させ、全設計ツールで再利用可能な統一基盤を構築します。これにより、コードの重複削減、保守性向上、新ツール開発の効率化を実現し、統合設計プラットフォームとしての一貫性を確保します。

## 🎯 リファクタリングの目的・背景

### 現在の課題
- **機能重複**: 各設計ツールで同様の機能が重複実装される可能性
- **保守性**: 共通機能の修正が各ツールに波及しない
- **一貫性**: ツール間でのインターフェース・動作の不統一
- **開発効率**: 新ツール開発時の共通機能再実装コスト

### リファクタリングの目的
- **共通基盤統一**: 全設計ツールで使用する共通機能の統一管理
- **コード重複削減**: DRY原則に基づく効率的なコード管理
- **保守性向上**: 共通機能の一元管理による保守コスト削減
- **開発効率化**: 新ツール開発時の共通機能再利用

## 📁 現在の構造と課題

### 現在の構造
```
docs/tools/
├── database/
│   ├── shared/                      # データベース専用共通機能
│   │   ├── core/                    # コア機能
│   │   ├── utils/                   # ユーティリティ
│   │   ├── parsers/                 # パーサー
│   │   ├── generators/              # ジェネレーター
│   │   ├── plugins/                 # プラグイン
│   │   ├── performance/             # パフォーマンス
│   │   ├── monitoring/              # 監視
│   │   └── ai/                      # AI支援
│   ├── database_consistency_checker/
│   └── table_generator/
├── api/                             # 将来実装
├── screens/                         # 将来実装
└── testing/                         # 将来実装
```

### 課題
- **スコープ限定**: `database/shared/` はデータベース設計ツール専用
- **再利用困難**: 他の設計ツールからの利用が困難
- **重複実装リスク**: API・画面・テスト設計ツールで同様機能の重複実装
- **統一性欠如**: ツール間でのインターフェース・設定の不統一

## 🏗️ 目標アーキテクチャ

### リファクタリング後の構造
```
docs/tools/
├── shared/                          # 統合設計ツール共通機能
│   ├── core/                        # コア機能（全ツール共通）
│   │   ├── config.py                # 統一設定管理
│   │   ├── logger.py                # 統一ログ管理
│   │   ├── exceptions.py            # 統一例外管理
│   │   ├── models.py                # 統一データモデル
│   │   └── registry.py              # ツール登録・管理
│   ├── utils/                       # ユーティリティ（全ツール共通）
│   │   ├── file_utils.py            # ファイル操作
│   │   ├── validation.py            # バリデーション
│   │   ├── yaml_utils.py            # YAML操作
│   │   └── markdown_utils.py        # Markdown操作
│   ├── parsers/                     # パーサー基盤
│   │   ├── base_parser.py           # パーサー基底クラス
│   │   ├── yaml_parser.py           # YAML汎用パーサー
│   │   ├── json_parser.py           # JSON汎用パーサー
│   │   └── markdown_parser.py       # Markdown汎用パーサー
│   ├── generators/                  # ジェネレーター基盤
│   │   ├── base_generator.py        # ジェネレーター基底クラス
│   │   ├── template_engine.py       # テンプレートエンジン
│   │   ├── code_generator.py        # コード生成基盤
│   │   └── document_generator.py    # ドキュメント生成基盤
│   ├── plugins/                     # プラグインシステム
│   │   ├── plugin_manager.py        # プラグイン管理
│   │   ├── registry.py              # プラグイン登録
│   │   ├── decorators.py            # プラグインデコレーター
│   │   └── hooks.py                 # フック機能
│   ├── quality/                     # 品質保証機能
│   │   ├── consistency_checker.py   # 整合性チェック基盤
│   │   ├── validation_engine.py     # バリデーションエンジン
│   │   ├── quality_metrics.py       # 品質メトリクス
│   │   └── report_generator.py      # 品質レポート生成
│   ├── integration/                 # ツール間連携
│   │   ├── workflow_engine.py       # ワークフローエンジン
│   │   ├── dependency_resolver.py   # 依存関係解決
│   │   ├── change_tracker.py        # 変更追跡
│   │   └── sync_manager.py          # 同期管理
│   ├── performance/                 # パフォーマンス機能
│   │   ├── parallel_processor.py    # 並列処理
│   │   ├── cache_manager.py         # キャッシュ管理
│   │   ├── memory_optimizer.py      # メモリ最適化
│   │   └── profiler.py              # プロファイラー
│   ├── monitoring/                  # 監視・メトリクス
│   │   ├── metrics_collector.py     # メトリクス収集
│   │   ├── health_checker.py        # ヘルスチェック
│   │   ├── alert_manager.py         # アラート管理
│   │   └── dashboard.py             # ダッシュボード
│   ├── ai/                          # AI支援機能
│   │   ├── code_assistant.py        # コード生成支援
│   │   ├── design_advisor.py        # 設計アドバイザー
│   │   ├── quality_analyzer.py      # 品質分析
│   │   └── optimization_engine.py   # 最適化エンジン
│   └── web/                         # Web UI基盤
│       ├── app_framework.py         # Webアプリフレームワーク
│       ├── api_server.py            # APIサーバー
│       ├── ui_components.py         # UIコンポーネント
│       └── dashboard_engine.py      # ダッシュボードエンジン
├── database/                        # データベース設計ツール
│   ├── database_consistency_checker/
│   ├── table_generator/
│   └── db_specific/                 # DB固有機能のみ
├── api/                             # API設計ツール
│   ├── openapi_generator/
│   ├── mock_server/
│   └── api_specific/                # API固有機能のみ
├── screens/                         # 画面設計ツール
│   ├── component_generator/
│   ├── storybook_generator/
│   └── ui_specific/                 # UI固有機能のみ
└── testing/                         # テスト設計ツール
    ├── test_case_generator/
    ├── e2e_generator/
    └── test_specific/               # テスト固有機能のみ
```

## 🔄 リファクタリング実施計画

### Phase 1: 共通基盤構築（優先度：最高）

#### 1.1 コア機能の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/core
mv docs/tools/database/shared/core/* docs/tools/shared/core/

# 対象ファイル
- config.py          # 統一設定管理
- logger.py          # 統一ログ管理
- exceptions.py      # 統一例外管理
- models.py          # 統一データモデル

# 新規作成
- registry.py        # ツール登録・管理
```

#### 1.2 ユーティリティの統一
```bash
# 実施内容
mkdir -p docs/tools/shared/utils
mv docs/tools/database/shared/utils/* docs/tools/shared/utils/

# 対象ファイル
- file_utils.py      # ファイル操作
- validation.py      # バリデーション

# 新規作成・拡張
- yaml_utils.py      # YAML操作（汎用化）
- markdown_utils.py  # Markdown操作（汎用化）
- json_utils.py      # JSON操作（新規）
```

#### 1.3 パーサー基盤の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/parsers
mv docs/tools/database/shared/parsers/* docs/tools/shared/parsers/

# 汎用化対象
- base_parser.py     # パーサー基底クラス
- yaml_parser.py     # YAML汎用パーサー
- markdown_parser.py # Markdown汎用パーサー

# 新規作成
- json_parser.py     # JSON汎用パーサー
- xml_parser.py      # XML汎用パーサー
```

### Phase 2: 高度機能の統一（優先度：高）

#### 2.1 ジェネレーター基盤の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/generators
mv docs/tools/database/shared/generators/* docs/tools/shared/generators/

# 汎用化対象
- base_generator.py    # ジェネレーター基底クラス
- template_engine.py   # テンプレートエンジン

# 新規作成
- code_generator.py    # コード生成基盤
- document_generator.py # ドキュメント生成基盤
```

#### 2.2 プラグインシステムの統一
```bash
# 実施内容
mkdir -p docs/tools/shared/plugins
mv docs/tools/database/shared/plugins/* docs/tools/shared/plugins/

# 汎用化対象
- plugin_manager.py  # プラグイン管理
- registry.py        # プラグイン登録
- decorators.py      # プラグインデコレーター

# 新規作成
- hooks.py           # フック機能
```

### Phase 3: 品質保証・統合機能（優先度：中）

#### 3.1 品質保証機能の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/quality

# 新規作成
- consistency_checker.py # 整合性チェック基盤
- validation_engine.py   # バリデーションエンジン
- quality_metrics.py     # 品質メトリクス
- report_generator.py    # 品質レポート生成
```

#### 3.2 ツール間連携機能
```bash
# 実施内容
mkdir -p docs/tools/shared/integration

# 新規作成
- workflow_engine.py     # ワークフローエンジン
- dependency_resolver.py # 依存関係解決
- change_tracker.py      # 変更追跡
- sync_manager.py        # 同期管理
```

### Phase 4: パフォーマンス・監視機能（優先度：中）

#### 4.1 パフォーマンス機能の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/performance
mv docs/tools/database/shared/performance/* docs/tools/shared/performance/

# 汎用化対象
- parallel_processor.py # 並列処理
- cache_manager.py      # キャッシュ管理

# 新規作成
- memory_optimizer.py   # メモリ最適化
- profiler.py           # プロファイラー
```

#### 4.2 監視機能の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/monitoring
mv docs/tools/database/shared/monitoring/* docs/tools/shared/monitoring/

# 汎用化対象
- metrics_collector.py  # メトリクス収集

# 新規作成
- health_checker.py     # ヘルスチェック
- alert_manager.py      # アラート管理
- dashboard.py          # ダッシュボード
```

### Phase 5: AI・Web UI機能（優先度：低）

#### 5.1 AI支援機能の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/ai
mv docs/tools/database/shared/ai/* docs/tools/shared/ai/

# 汎用化対象
- code_generator.py     # コード生成支援

# 新規作成
- design_advisor.py     # 設計アドバイザー
- quality_analyzer.py   # 品質分析
- optimization_engine.py # 最適化エンジン
```

#### 5.2 Web UI基盤の統一
```bash
# 実施内容
mkdir -p docs/tools/shared/web

# 新規作成
- app_framework.py      # Webアプリフレームワーク
- api_server.py         # APIサーバー
- ui_components.py      # UIコンポーネント
- dashboard_engine.py   # ダッシュボードエンジン
```

## 🔧 実装詳細

### 統一設定管理システム

#### docs/tools/shared/core/config.py
```python
"""統合設計ツール統一設定管理"""

from typing import Dict, Any, Optional
from pathlib import Path
import yaml
import os

class IntegratedToolsConfig:
    """統合設計ツール設定管理クラス"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path("docs/tools/config.yaml")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """設定ファイル読み込み"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return self._default_config()
    
    def _default_config(self) -> Dict[str, Any]:
        """デフォルト設定"""
        return {
            'tools': {
                'database': {
                    'enabled': True,
                    'yaml_format': 'unified',
                    'output_formats': ['ddl', 'markdown', 'json']
                },
                'api': {
                    'enabled': False,
                    'openapi_version': '3.0.3',
                    'output_formats': ['yaml', 'json', 'typescript']
                },
                'screens': {
                    'enabled': False,
                    'framework': 'react',
                    'output_formats': ['tsx', 'storybook', 'css']
                },
                'testing': {
                    'enabled': False,
                    'frameworks': ['jest', 'playwright'],
                    'output_formats': ['typescript', 'json']
                }
            },
            'quality': {
                'required_sections': ['revision_history', 'overview', 'notes', 'rules'],
                'validation_level': 'strict',
                'auto_fix': False
            },
            'integration': {
                'auto_sync': True,
                'dependency_check': True,
                'change_tracking': True
            },
            'performance': {
                'parallel_processing': True,
                'cache_enabled': True,
                'max_workers': 4
            }
        }
    
    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """特定ツールの設定取得"""
        return self.config.get('tools', {}).get(tool_name, {})
    
    def get_quality_config(self) -> Dict[str, Any]:
        """品質設定取得"""
        return self.config.get('quality', {})
    
    def get_integration_config(self) -> Dict[str, Any]:
        """統合設定取得"""
        return self.config.get('integration', {})
```

### 統一ツール登録システム

#### docs/tools/shared/core/registry.py
```python
"""統合設計ツール登録・管理システム"""

from typing import Dict, List, Type, Any, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class ToolType(Enum):
    """ツールタイプ"""
    DATABASE = "database"
    API = "api"
    SCREENS = "screens"
    TESTING = "testing"

@dataclass
class ToolInfo:
    """ツール情報"""
    name: str
    type: ToolType
    version: str
    description: str
    enabled: bool = True
    dependencies: List[str] = None

class DesignTool(ABC):
    """設計ツール基底クラス"""
    
    @abstractmethod
    def get_info(self) -> ToolInfo:
        """ツール情報取得"""
        pass
    
    @abstractmethod
    def validate_input(self, input_data: Any) -> bool:
        """入力データ検証"""
        pass
    
    @abstractmethod
    def generate_output(self, input_data: Any) -> Dict[str, Any]:
        """出力生成"""
        pass
    
    @abstractmethod
    def check_consistency(self, other_tools: List['DesignTool']) -> List[str]:
        """他ツールとの整合性チェック"""
        pass

class ToolRegistry:
    """ツール登録管理クラス"""
    
    def __init__(self):
        self._tools: Dict[str, DesignTool] = {}
        self._tool_info: Dict[str, ToolInfo] = {}
    
    def register_tool(self, tool: DesignTool) -> None:
        """ツール登録"""
        info = tool.get_info()
        self._tools[info.name] = tool
        self._tool_info[info.name] = info
    
    def get_tool(self, name: str) -> Optional[DesignTool]:
        """ツール取得"""
        return self._tools.get(name)
    
    def get_tools_by_type(self, tool_type: ToolType) -> List[DesignTool]:
        """タイプ別ツール取得"""
        return [
            tool for tool in self._tools.values()
            if tool.get_info().type == tool_type
        ]
    
    def get_enabled_tools(self) -> List[DesignTool]:
        """有効ツール取得"""
        return [
            tool for tool in self._tools.values()
            if tool.get_info().enabled
        ]
    
    def check_dependencies(self, tool_name: str) -> List[str]:
        """依存関係チェック"""
        info = self._tool_info.get(tool_name)
        if not info or not info.dependencies:
            return []
        
        missing = []
        for dep in info.dependencies:
            if dep not in self._tools:
                missing.append(dep)
        
        return missing

# グローバルレジストリインスタンス
tool_registry = ToolRegistry()
```

### 統一ワークフローエンジン

#### docs/tools/shared/integration/workflow_engine.py
```python
"""統合設計ツールワークフローエンジン"""

from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import asyncio
from ..core.registry import ToolRegistry, DesignTool

class WorkflowStatus(Enum):
    """ワークフロー状態"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class WorkflowStep:
    """ワークフローステップ"""
    name: str
    tool_name: str
    input_data: Any
    dependencies: List[str] = None
    condition: Optional[Callable] = None

@dataclass
class WorkflowResult:
    """ワークフロー結果"""
    step_name: str
    status: WorkflowStatus
    output_data: Any = None
    error_message: str = None

class WorkflowEngine:
    """ワークフローエンジン"""
    
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry
        self.workflows: Dict[str, List[WorkflowStep]] = {}
    
    def register_workflow(self, name: str, steps: List[WorkflowStep]) -> None:
        """ワークフロー登録"""
        self.workflows[name] = steps
    
    async def execute_workflow(self, name: str, initial_data: Any = None) -> List[WorkflowResult]:
        """ワークフロー実行"""
        if name not in self.workflows:
            raise ValueError(f"Workflow '{name}' not found")
        
        steps = self.workflows[name]
        results = []
        step_outputs = {}
        
        for step in steps:
            # 依存関係チェック
            if step.dependencies:
                for dep in step.dependencies:
                    if dep not in step_outputs:
                        results.append(WorkflowResult(
                            step_name=step.name,
                            status=WorkflowStatus.FAILED,
                            error_message=f"Dependency '{dep}' not satisfied"
                        ))
                        continue
            
            # 条件チェック
            if step.condition and not step.condition(step_outputs):
                results.append(WorkflowResult(
                    step_name=step.name,
                    status=WorkflowStatus.CANCELLED,
                    error_message="Condition not met"
                ))
                continue
            
            # ステップ実行
            try:
                tool = self.tool_registry.get_tool(step.tool_name)
                if not tool:
                    raise ValueError(f"Tool '{step.tool_name}' not found")
                
                # 入力データ準備
                input_data = step.input_data
                if step.dependencies:
                    # 依存ステップの出力をマージ
                    for dep in step.dependencies:
                        if isinstance(input_data, dict) and isinstance(step_outputs[dep], dict):
                            input_data.update(step_outputs[dep])
                
                # ツール実行
                output = tool.generate_output(input_data)
                step_outputs[step.name] = output
                
                results.append(WorkflowResult(
                    step_name=step.name,
                    status=WorkflowStatus.COMPLETED,
                    output_data=output
                ))
                
            except Exception as e:
                results.append(WorkflowResult(
                    step_name=step.name,
                    status=WorkflowStatus.FAILED,
                    error_message=str(e)
                ))
        
        return results

# 事前定義ワークフロー
def register_default_workflows(engine: WorkflowEngine) -> None:
    """デフォルトワークフロー登録"""
    
    # データベース → API → 画面 → テスト
    full_design_workflow = [
        WorkflowStep(
            name="database_design",
            tool_name="database",
            input_data={"source": "yaml_definitions"}
        ),
        WorkflowStep(
            name="api_design",
            tool_name="api",
            input_data={"source": "database_schema"},
            dependencies=["database_design"]
        ),
        WorkflowStep(
            name="screen_design",
            tool_name="screens",
            input_data={"source": "api_specification"},
            dependencies=["api_design"]
        ),
        WorkflowStep(
            name="test_design",
            tool_name="testing",
            input_data={"source": "all_designs"},
            dependencies=["database_design", "api_design", "screen_design"]
        )
    ]
    
    engine.register_workflow("full_design", full_design_workflow)
```

## 📊 移行スケジュール・マイルストーン

### Phase 1: 共通基盤構築（2025年7月第1週）
- **Week 1**: コア機能・ユーティリティの移行
- **Week 2**: パーサー基盤の統一・テスト
- **成果物**: 統一された基盤機能

### Phase 2: 高度機能の統一（2025年7月第2-3週）
- **Week 3**: ジェネレーター・プラグインシステム統一
- **Week 4**: 機能テスト・ドキュメント更新
- **成果物**: 拡張可能な統一プラットフォーム

### Phase 3: 品質保証・統合機能（2025年7月第4週-8月第1週）
- **Week 5**: 品質保証機能・ツール間連携機能実装
- **Week 6**: 統合テスト・品質検証
- **成果物**: 統合品質保証システム

### Phase 4: パフォーマンス・監視機能（2025年8月第2週）
- **Week 7**: パフォーマンス・監視機能統一
- **成果物**: 高性能統合プラットフォーム

### Phase 5: AI・Web UI機能（2025年8月第3-4週）
- **Week 8-9**: AI支援・Web UI基盤統一
- **成果物**: 次世代統合設計プラットフォーム

## 🔍 品質保証・テスト戦略

### 移行品質保証
- **機能テスト**: 既存機能の100%動作確認
- **統合テスト**: ツール間連携の動作確認
- **パフォーマンステスト**: 性能劣化の確認
- **後方互換性**: 既存インターフェースの維持確認

### 自動テストスイート
```bash
# 統合テスト実行
cd docs/tools
python -m pytest shared/tests/ --verbose

# 品質チェック
python shared/quality/quality_checker.py --all

# パフォーマンステスト
python shared/performance/performance_test.py --benchmark
```

## 📈 期待される効果・メリット

### 開発効率向上
- **コード重複削減**: 70%以上の共通機能統一
- **新ツール開発**: 50%以上の開発時間短縮
- **保守コスト**: 60%以上の保守コスト削減

### 品質向上
- **一貫性**: 100%の統一インターフェース
- **信頼性**: 統一テストによる品質保証
- **拡張性**: プラグインアーキテクチャによる柔軟性

### 運用効率化
- **統一管理**: 一元化された設定・監視
- **自動化**: ワークフローエンジンによる自動実行
- **可視化**: 統合ダッシュボードによる状況把握

## 🚀 実装開始準備

### 必要なアクション
1. **リファクタリング計画承認**: 開発チームでの計画レビュー・承認
2. **作業環境準備**: 開発環境・テスト環境の準備
3. **チーム体制**: 担当者アサイン・スケジュール調整
4. **品質基準**: 移行品質基準・テスト計画の策定

### 開始条件
- ✅ **現在のデータベースツール**: 安定動作確認済み
- ✅ **統合設計ツール基盤**: ディレクトリ構造確立済み
- 🚧 **リファクタリング計画**: 本計画の承認待ち
- ⏳ **実装リソース**: 開発リソース確保待ち

---

**🎯 統合設計ツール共通機能統一により、次世代設計自動化プラットフォームの基盤を確立**

**作成日**: 2025年6月27日  
**作成者**: 黒澤 (@yusuke-kurosawa)  
**プロジェクト**: 年間スキル報告書WEB化PJT
