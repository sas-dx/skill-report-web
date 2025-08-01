# 🔗 設計統合ツール - 依存関係マップ

## エグゼクティブサマリー

この文書は設計統合ツールの詳細な依存関係マップを定義します。モジュール間の依存関係、外部ライブラリ依存、循環依存の回避戦略、依存性注入パターンを提供し、保守性・テスト容易性・拡張性の高いアーキテクチャを実現します。明確な依存関係管理により、モジュールの独立性を保ちながら、効率的な開発とデバッグを支援します。

## 🎯 依存関係管理の基本原則

### 設計原則
- **単方向依存**: 循環依存の完全排除
- **レイヤー分離**: 上位レイヤーから下位レイヤーへの依存のみ
- **依存性注入**: インターフェースベースの疎結合設計
- **最小依存**: 必要最小限の依存関係
- **明示的依存**: 隠れた依存関係の排除

### 依存関係の種類
- **コンパイル時依存**: import文による静的依存
- **実行時依存**: 動的ロード・プラグインシステム
- **設定依存**: 設定ファイルによる動的依存
- **外部依存**: サードパーティライブラリ依存

## 🏗️ レイヤー別依存関係

### 1. Interface Layer（インターフェース層）

#### CLI Interface Dependencies
```python
# cli/main.py
dependencies = {
    "direct": [
        "click",                    # CLIフレームワーク
        "rich",                     # リッチテキスト出力
        "core.config",              # 設定管理
        "core.logger",              # ログ出力
        "modules.database_manager", # データベース管理
        "modules.api_manager",      # API管理
        "modules.screen_manager",   # 画面管理
    ],
    "indirect": [
        "core.exceptions",          # 例外処理（modules経由）
        "core.models",              # データモデル（modules経由）
        "shared.*",                 # 共有コンポーネント（modules経由）
    ]
}
```

#### Web UI Dependencies
```python
# web/app.py
dependencies = {
    "direct": [
        "fastapi",                  # Webフレームワーク
        "uvicorn",                  # ASGIサーバー
        "jinja2",                   # テンプレートエンジン
        "core.config",              # 設定管理
        "core.logger",              # ログ出力
        "modules.*",                # 全モジュール
    ],
    "indirect": [
        "shared.*",                 # 共有コンポーネント（modules経由）
        "infrastructure.*",         # インフラ（modules経由）
    ]
}
```

### 2. Core Layer（コア層）

#### Config Manager Dependencies
```python
# core/config.py
dependencies = {
    "external": [
        "yaml",                     # YAML解析
        "os",                       # 環境変数
        "pathlib",                  # パス操作
        "typing",                   # 型ヒント
    ],
    "internal": [],                 # 他の内部モジュールに依存しない
}
```

#### Logger System Dependencies
```python
# core/logger.py
dependencies = {
    "external": [
        "logging",                  # 標準ログ
        "json",                     # JSON出力
        "datetime",                 # タイムスタンプ
        "structlog",                # 構造化ログ
    ],
    "internal": [
        "core.config",              # 設定取得
    ]
}
```

#### Exception Handler Dependencies
```python
# core/exceptions.py
dependencies = {
    "external": [
        "traceback",                # スタックトレース
        "typing",                   # 型ヒント
    ],
    "internal": [
        "core.logger",              # ログ出力
    ]
}
```

#### Models Manager Dependencies
```python
# core/models.py
dependencies = {
    "external": [
        "dataclasses",              # データクラス
        "typing",                   # 型ヒント
        "datetime",                 # 日時型
        "uuid",                     # UUID生成
        "enum",                     # 列挙型
        "pydantic",                 # データ検証
    ],
    "internal": [],                 # 他の内部モジュールに依存しない
}
```

### 3. Module Layer（モジュール層）

#### Database Manager Dependencies
```python
# modules/database_manager.py
dependencies = {
    "core": [
        "core.config",              # 設定管理
        "core.logger",              # ログ出力
        "core.exceptions",          # 例外処理
        "core.models",              # データモデル
    ],
    "shared": [
        "shared.parsers.yaml_parser",       # YAML解析
        "shared.generators.ddl_generator",  # DDL生成
        "shared.validators.yaml_validator", # YAML検証
        "shared.utils.file_utils",          # ファイル操作
    ],
    "infrastructure": [
        "infrastructure.cache.cache_manager",       # キャッシュ
        "infrastructure.parallel.parallel_processor", # 並列処理
    ],
    "external": [
        "sqlalchemy",               # SQL生成
        "psycopg2",                 # PostgreSQL接続
    ]
}
```

#### API Manager Dependencies
```python
# modules/api_manager.py
dependencies = {
    "core": [
        "core.config",
        "core.logger",
        "core.exceptions",
        "core.models",
    ],
    "shared": [
        "shared.parsers.openapi_parser",    # OpenAPI解析
        "shared.parsers.json_parser",       # JSON解析
        "shared.generators.openapi_generator", # OpenAPI生成
        "shared.validators.schema_validator", # スキーマ検証
    ],
    "infrastructure": [
        "infrastructure.cache.cache_manager",
        "infrastructure.monitoring.metrics_collector",
    ],
    "external": [
        "openapi3",                 # OpenAPI処理
        "jsonschema",               # JSONスキーマ検証
        "requests",                 # HTTP通信
    ]
}
```

#### Screen Manager Dependencies
```python
# modules/screen_manager.py
dependencies = {
    "core": [
        "core.config",
        "core.logger",
        "core.exceptions",
        "core.models",
    ],
    "shared": [
        "shared.parsers.markdown_parser",   # Markdown解析
        "shared.parsers.yaml_parser",       # YAML解析
        "shared.generators.html_generator", # HTML生成
        "shared.validators.consistency_validator", # 整合性検証
    ],
    "infrastructure": [
        "infrastructure.cache.cache_manager",
    ],
    "external": [
        "markdown",                 # Markdown処理
        "beautifulsoup4",           # HTML解析
        "pillow",                   # 画像処理
    ]
}
```

#### Integration Checker Dependencies
```python
# modules/integration_checker.py
dependencies = {
    "core": [
        "core.config",
        "core.logger",
        "core.exceptions",
        "core.models",
    ],
    "modules": [
        "modules.database_manager", # データベース情報取得
        "modules.api_manager",      # API情報取得
        "modules.screen_manager",   # 画面情報取得
    ],
    "shared": [
        "shared.validators.consistency_validator",
        "shared.utils.string_utils",
    ],
    "infrastructure": [
        "infrastructure.parallel.parallel_processor",
    ]
}
```

### 4. Shared Layer（共有層）

#### Parsers System Dependencies
```python
# shared/parsers/yaml_parser.py
dependencies = {
    "core": [
        "core.logger",
        "core.exceptions",
        "core.models",
    ],
    "shared": [
        "shared.parsers.base_parser",       # ベースクラス
        "shared.utils.file_utils",          # ファイル操作
    ],
    "external": [
        "yaml",                     # YAML解析
        "ruamel.yaml",              # 高機能YAML解析
    ]
}

# shared/parsers/openapi_parser.py
dependencies = {
    "core": [
        "core.logger",
        "core.exceptions",
        "core.models",
    ],
    "shared": [
        "shared.parsers.base_parser",
        "shared.parsers.json_parser",
    ],
    "external": [
        "openapi3",                 # OpenAPI解析
        "jsonref",                  # JSON参照解決
    ]
}
```

#### Generators System Dependencies
```python
# shared/generators/ddl_generator.py
dependencies = {
    "core": [
        "core.logger",
        "core.exceptions",
        "core.models",
    ],
    "shared": [
        "shared.generators.base_generator", # ベースクラス
        "shared.utils.string_utils",        # 文字列操作
    ],
    "external": [
        "jinja2",                   # テンプレートエンジン
        "sqlalchemy",               # SQL生成
    ]
}
```

#### Validators System Dependencies
```python
# shared/validators/yaml_validator.py
dependencies = {
    "core": [
        "core.logger",
        "core.exceptions",
        "core.models",
    ],
    "shared": [
        "shared.validators.base_validator", # ベースクラス
    ],
    "external": [
        "cerberus",                 # スキーマ検証
        "jsonschema",               # JSONスキーマ検証
    ]
}
```

### 5. Infrastructure Layer（インフラ層）

#### Cache Manager Dependencies
```python
# infrastructure/cache/cache_manager.py
dependencies = {
    "core": [
        "core.config",
        "core.logger",
        "core.exceptions",
    ],
    "infrastructure": [
        "infrastructure.cache.memory_cache",    # メモリキャッシュ
        "infrastructure.cache.redis_cache",     # Redisキャッシュ
    ],
    "external": [
        "redis",                    # Redis接続
        "pickle",                   # オブジェクトシリアライズ
    ]
}
```

#### Parallel Processor Dependencies
```python
# infrastructure/parallel/parallel_processor.py
dependencies = {
    "core": [
        "core.config",
        "core.logger",
        "core.exceptions",
    ],
    "external": [
        "concurrent.futures",       # 並列処理
        "multiprocessing",          # プロセス並列
        "asyncio",                  # 非同期処理
    ]
}
```

## 🔄 依存関係フロー図

### 全体依存関係フロー
```
┌─────────────────────────────────────────────────────────────┐
│                    Dependency Flow                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ CLI Interface│    │   Web UI    │    │  Plugin API │     │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │
│         │                  │                  │            │
│         └──────────────────┼──────────────────┘            │
│                            │                               │
│  ┌─────────────────────────▼─────────────────────────┐     │
│  │                Module Layer                       │     │
│  │  ┌─────────────┬─────────────┬─────────────┐     │     │
│  │  │  Database   │     API     │   Screen    │     │     │
│  │  │   Manager   │   Manager   │   Manager   │     │     │
│  │  └─────────────┴─────────────┴─────────────┘     │     │
│  │  ┌─────────────┬─────────────┬─────────────┐     │     │
│  │  │Integration  │   Design    │   Report    │     │     │
│  │  │  Checker    │ Generator   │ Generator   │     │     │
│  │  └─────────────┴─────────────┴─────────────┘     │     │
│  └─────────────────────┬─────────────────────────────┘     │
│                        │                                   │
│  ┌─────────────────────▼─────────────────────────┐         │
│  │                 Core Layer                    │         │
│  │  ┌─────────────┬─────────────┬─────────────┐ │         │
│  │  │   Config    │   Logger    │ Exceptions  │ │         │
│  │  │  Manager    │   System    │  Handler    │ │         │
│  │  └─────────────┴─────────────┴─────────────┘ │         │
│  │  ┌─────────────┬─────────────┬─────────────┐ │         │
│  │  │   Models    │  Registry   │             │ │         │
│  │  │  Manager    │   System    │             │ │         │
│  │  └─────────────┴─────────────┴─────────────┘ │         │
│  └─────────────────────┬─────────────────────────┘         │
│                        │                                   │
│  ┌─────────────────────▼─────────────────────────┐         │
│  │                Shared Layer                   │         │
│  │  ┌─────────────┬─────────────┬─────────────┐ │         │
│  │  │   Parsers   │ Generators  │ Validators  │ │         │
│  │  │   System    │   System    │   System    │ │         │
│  │  └─────────────┴─────────────┴─────────────┘ │         │
│  │  ┌─────────────┬─────────────┬─────────────┐ │         │
│  │  │ Utilities   │             │             │ │         │
│  │  │   System    │             │             │ │         │
│  │  └─────────────┴─────────────┴─────────────┘ │         │
│  └─────────────────────┬─────────────────────────┘         │
│                        │                                   │
│  ┌─────────────────────▼─────────────────────────┐         │
│  │            Infrastructure Layer               │         │
│  │  ┌─────────────┬─────────────┬─────────────┐ │         │
│  │  │   Cache     │ Parallel    │ Monitoring  │ │         │
│  │  │  Manager    │ Processor   │   System    │ │         │
│  │  └─────────────┴─────────────┴─────────────┘ │         │
│  │  ┌─────────────┬─────────────┬─────────────┐ │         │
│  │  │  Storage    │             │             │ │         │
│  │  │  Manager    │             │             │ │         │
│  │  └─────────────┴─────────────┴─────────────┘ │         │
│  └─────────────────────┬─────────────────────────┘         │
│                        │                                   │
│  ┌─────────────────────▼─────────────────────────┐         │
│  │            External Dependencies              │         │
│  │  ┌─────────────┬─────────────┬─────────────┐ │         │
│  │  │   Python    │  Database   │   Network   │ │         │
│  │  │  Standard   │  Drivers    │ Libraries   │ │         │
│  │  │  Library    │             │             │ │         │
│  │  └─────────────┴─────────────┴─────────────┘ │         │
│  └─────────────────────────────────────────────────┘         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 📦 外部依存関係管理

### 必須外部ライブラリ
```python
# requirements.txt
CORE_DEPENDENCIES = {
    # コア機能
    "pydantic>=2.0.0",          # データ検証・シリアライズ
    "click>=8.0.0",             # CLIフレームワーク
    "rich>=13.0.0",             # リッチテキスト出力
    "structlog>=23.0.0",        # 構造化ログ
    "PyYAML>=6.0.0",            # YAML処理
    "ruamel.yaml>=0.17.0",      # 高機能YAML処理
    
    # Web UI
    "fastapi>=0.100.0",         # Webフレームワーク
    "uvicorn>=0.22.0",          # ASGIサーバー
    "jinja2>=3.1.0",            # テンプレートエンジン
    
    # データベース
    "sqlalchemy>=2.0.0",        # ORM・SQL生成
    "psycopg2-binary>=2.9.0",   # PostgreSQL接続
    
    # API処理
    "openapi3>=1.8.0",          # OpenAPI処理
    "jsonschema>=4.17.0",       # JSONスキーマ検証
    "requests>=2.31.0",         # HTTP通信
    
    # 検証・解析
    "cerberus>=1.3.0",          # スキーマ検証
    "markdown>=3.4.0",          # Markdown処理
    "beautifulsoup4>=4.12.0",   # HTML解析
    
    # キャッシュ・並列処理
    "redis>=4.5.0",             # Redis接続
    "aioredis>=2.0.0",          # 非同期Redis
}

OPTIONAL_DEPENDENCIES = {
    # AI機能（オプション）
    "openai>=1.0.0",            # OpenAI API
    "anthropic>=0.3.0",         # Anthropic API
    
    # 画像処理（オプション）
    "pillow>=10.0.0",           # 画像処理
    
    # 高度な解析（オプション）
    "pandas>=2.0.0",            # データ解析
    "numpy>=1.24.0",            # 数値計算
}

DEVELOPMENT_DEPENDENCIES = {
    # テスト
    "pytest>=7.4.0",            # テストフレームワーク
    "pytest-cov>=4.1.0",        # カバレッジ測定
    "pytest-asyncio>=0.21.0",   # 非同期テスト
    "pytest-mock>=3.11.0",      # モック機能
    
    # 品質管理
    "black>=23.0.0",            # コードフォーマッター
    "isort>=5.12.0",            # import整理
    "flake8>=6.0.0",            # 静的解析
    "mypy>=1.4.0",              # 型チェック
    
    # ドキュメント
    "sphinx>=7.0.0",            # ドキュメント生成
    "sphinx-rtd-theme>=1.3.0",  # ドキュメントテーマ
}
```

### 依存関係の競合回避
```python
# 依存関係競合の管理
DEPENDENCY_CONFLICTS = {
    "pydantic": {
        "version_constraint": ">=2.0.0,<3.0.0",
        "reason": "v2の新機能を使用、v3は破壊的変更予定",
        "alternatives": ["dataclasses", "attrs"],
    },
    "sqlalchemy": {
        "version_constraint": ">=2.0.0,<3.0.0",
        "reason": "v2の新しいクエリ構文を使用",
        "alternatives": ["raw SQL", "peewee"],
    },
    "fastapi": {
        "version_constraint": ">=0.100.0,<1.0.0",
        "reason": "安定版を使用、1.0は破壊的変更の可能性",
        "alternatives": ["flask", "django"],
    }
}
```

## 🔄 循環依存の回避戦略

### 循環依存の検出
```python
# 循環依存検出ツール
def detect_circular_dependencies():
    """循環依存を検出する"""
    dependency_graph = build_dependency_graph()
    cycles = find_cycles(dependency_graph)
    
    if cycles:
        logger.error(f"循環依存が検出されました: {cycles}")
        raise CircularDependencyError(cycles)
    
    return True

def build_dependency_graph():
    """依存関係グラフを構築"""
    graph = {}
    for module in get_all_modules():
        graph[module] = get_module_dependencies(module)
    return graph
```

### 循環依存回避パターン

#### 1. 依存性注入パターン
```python
# 悪い例：直接依存
class DatabaseManager:
    def __init__(self):
        self.api_manager = APIManager()  # 直接依存

class APIManager:
    def __init__(self):
        self.database_manager = DatabaseManager()  # 循環依存！

# 良い例：依存性注入
class DatabaseManager:
    def __init__(self, api_manager: Optional[APIManager] = None):
        self._api_manager = api_manager
    
    def set_api_manager(self, api_manager: APIManager):
        self._api_manager = api_manager

class APIManager:
    def __init__(self, database_manager: Optional[DatabaseManager] = None):
        self._database_manager = database_manager
    
    def set_database_manager(self, database_manager: DatabaseManager):
        self._database_manager = database_manager
```

#### 2. イベント駆動パターン
```python
# イベントシステムによる疎結合
class EventBus:
    def __init__(self):
        self._subscribers = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
    
    def publish(self, event_type: str, data: Any):
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                handler(data)

# 使用例
class DatabaseManager:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    def update_table(self, table_data):
        # テーブル更新
        self.event_bus.publish("table_updated", table_data)

class APIManager:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.event_bus.subscribe("table_updated", self.on_table_updated)
    
    def on_table_updated(self, table_data):
        # テーブル更新に応じてAPI仕様を更新
        pass
```

#### 3. インターフェース分離パターン
```python
# インターフェース定義
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    @abstractmethod
    def get_table_info(self, table_name: str) -> Dict:
        pass

class APIInterface(ABC):
    @abstractmethod
    def get_endpoint_info(self, endpoint: str) -> Dict:
        pass

# 実装クラス
class DatabaseManager(DatabaseInterface):
    def get_table_info(self, table_name: str) -> Dict:
        # 実装
        pass

class APIManager(APIInterface):
    def get_endpoint_info(self, endpoint: str) -> Dict:
        # 実装
        pass

# 統合チェッカー（インターフェースに依存）
class IntegrationChecker:
    def __init__(self, 
                 database: DatabaseInterface, 
                 api: APIInterface):
        self.database = database
        self.api = api
```

## 🧪 依存関係のテスト戦略

### モック・スタブの活用
```python
# テスト用モック
class MockDatabaseManager:
    def __init__(self):
        self.tables = {}
    
    def get_table_info(self, table_name: str) -> Dict:
        return self.tables.get(table_name, {})
    
    def add_mock_table(self, table_name: str, table_info: Dict):
        self.tables[table_name] = table_info

# テストケース
def test_integration_checker():
    # モックオブジェクト作成
    mock_db = MockDatabaseManager()
    mock_api = MockAPIManager()
    
    # テストデータ設定
    mock_db.add_mock_table("users", {"columns": ["id", "name"]})
    mock_api.add_mock_endpoint("/users", {"parameters": ["id"]})
    
    # テスト実行
    checker = IntegrationChecker(mock_db, mock_api)
    result = checker.check_consistency()
    
    assert result.is_valid
```

### 依存関係の分離テスト
```python
# 依存関係を分離したユニットテスト
def test_database_manager_isolated():
    """DatabaseManagerを他の依存なしでテスト"""
    config = MockConfig()
    logger = MockLogger()
    
    db_manager = DatabaseManager(config, logger)
    
    # 外部依存なしでテスト可能
    result = db_manager.validate_yaml_file("test.yaml")
    assert result.is_valid
```

## 📊 依存関係メトリクス

### 測定指標
```python
DEPENDENCY_METRICS = {
    "afferent_coupling": {
        "description": "このモジュールに依存するモジュール数",
        "target": "< 5",
        "measurement": "incoming_dependencies_count",
    },
    "efferent_coupling": {
        "description": "このモジュールが依存するモジュール数", 
        "target": "< 10",
        "measurement": "outgoing_dependencies_count",
    },
    "instability": {
        "description": "変更の影響を受けやすさ",
        "target": "0.3 - 0.7",
        "formula": "efferent / (afferent + efferent)",
    },
    "abstractness": {
        "description": "抽象クラス・インターフェースの割合",
        "target": "> 0.5 (for core modules)",
        "formula": "abstract_classes / total_classes",
    }
}
```

### 依存関係監視
```python
def monitor_dependencies():
    """依存関係の健全性を監視"""
    metrics = calculate_dependency_metrics()
    
    for module, metric in metrics.items():
        if metric.instability > 0.8:
            logger.warning(f"モジュール {module} の不安定性が高い: {metric.instability}")
        
        if metric.efferent_coupling > 10:
            logger.warning(f"モジュール {module} の依存数が多い: {metric.efferent_coupling}")
```

---

この詳細な依存関係マップにより、保守性・テスト容易性・拡張性の高いアーキテクチャを実現し、循環依存を回避した健全なモジュール設計を確保します。
