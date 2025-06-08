# データベース整合性チェックツール リファクタリング計画

## 現状分析

### 既存構造の確認結果
```
docs/design/database/tools/
├── shared/                          # ✅ 共通ライブラリ（既存）
│   ├── core/
│   │   ├── config.py               # ✅ 統合設定管理
│   │   └── exceptions.py           # ✅ 共通例外クラス
│   ├── parsers/                    # ✅ 共通パーサー
│   │   ├── yaml_parser.py
│   │   ├── ddl_parser.py
│   │   └── markdown_parser.py
│   └── generators/                 # ✅ 共通ジェネレーター
│       ├── ddl_generator.py
│       ├── markdown_generator.py
│       └── sample_data_generator.py
├── table_generator/                # ✅ 既に共通ライブラリ使用
│   ├── __main__.py                # ✅ 共通ライブラリ対応済み
│   └── core/
│       └── adapters.py            # 🔄 リファクタリング対象
├── database_consistency_checker/   # ✅ 既に共通ライブラリ使用
│   ├── __main__.py                # ✅ 共通ライブラリ対応済み
│   └── core/
│       └── adapters.py            # 🔄 リファクタリング対象
└── tests/                          # ✅ テスト構造は良好
    ├── unit/
    ├── integration/
    └── performance/
```

### 現状の問題点

1. **個別config.pyファイルの不在**: 両ツールにconfig.pyが存在しない（共通設定を使用中）
2. **adapters.pyの重複**: 両ツールに類似のアダプター実装が存在
3. **チェック機能の分散**: 整合性チェック機能が単一ツールに集中
4. **テスト構造の改善余地**: より包括的なテスト体系が必要

## リファクタリング戦略

### Phase 1: アダプター層の統合 🎯 **最優先**

#### 1.1 共通アダプター基盤の作成
```python
# shared/adapters/base_adapter.py
class BaseAdapter:
    """アダプター基底クラス"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def validate_input(self, data: Any) -> bool:
        """入力データ検証"""
        raise NotImplementedError
    
    def transform_data(self, data: Any) -> Any:
        """データ変換"""
        raise NotImplementedError

# shared/adapters/table_adapter.py
class TableDefinitionAdapter(BaseAdapter):
    """テーブル定義アダプター"""
    
    def yaml_to_internal(self, yaml_data: dict) -> TableDefinition:
        """YAML → 内部形式変換"""
        pass
    
    def internal_to_ddl(self, table_def: TableDefinition) -> str:
        """内部形式 → DDL変換"""
        pass
    
    def internal_to_markdown(self, table_def: TableDefinition) -> str:
        """内部形式 → Markdown変換"""
        pass

# shared/adapters/consistency_adapter.py
class ConsistencyCheckAdapter(BaseAdapter):
    """整合性チェックアダプター"""
    
    def compare_definitions(self, source: TableDefinition, target: TableDefinition) -> ComparisonResult:
        """定義比較"""
        pass
    
    def validate_foreign_keys(self, table_def: TableDefinition, all_tables: List[TableDefinition]) -> ValidationResult:
        """外部キー検証"""
        pass
```

#### 1.2 既存アダプターの移行
- `table_generator/core/adapters.py` → `shared/adapters/table_adapter.py`
- `database_consistency_checker/core/adapters.py` → `shared/adapters/consistency_adapter.py`

### Phase 2: チェック機能の拡張 🔧

#### 2.1 新しいチェック機能の追加
```python
# shared/checkers/advanced_consistency_checker.py
class AdvancedConsistencyChecker:
    """高度な整合性チェック"""
    
    def check_performance_implications(self, table_def: TableDefinition) -> PerformanceReport:
        """パフォーマンス影響チェック"""
        pass
    
    def check_security_compliance(self, table_def: TableDefinition) -> SecurityReport:
        """セキュリティ準拠チェック"""
        pass
    
    def check_multitenant_compliance(self, table_def: TableDefinition) -> MultitenantReport:
        """マルチテナント準拠チェック"""
        pass

# shared/checkers/cross_reference_checker.py
class CrossReferenceChecker:
    """相互参照チェック"""
    
    def check_circular_dependencies(self, tables: List[TableDefinition]) -> CircularDependencyReport:
        """循環依存チェック"""
        pass
    
    def check_orphaned_references(self, tables: List[TableDefinition]) -> OrphanedReferenceReport:
        """孤立参照チェック"""
        pass
```

#### 2.2 レポート機能の強化
```python
# shared/reporters/
├── base_reporter.py          # レポーター基底クラス
├── text_reporter.py          # テキスト形式レポート
├── json_reporter.py          # JSON形式レポート
├── markdown_reporter.py      # Markdown形式レポート
├── html_reporter.py          # HTML形式レポート
└── excel_reporter.py         # Excel形式レポート
```

### Phase 3: テスト体系の強化 🧪

#### 3.1 包括的テストスイートの構築
```python
# tests/unit/shared/
├── test_adapters.py          # アダプターテスト
├── test_checkers.py          # チェッカーテスト
├── test_reporters.py         # レポーターテスト
└── test_config.py            # 設定テスト

# tests/integration/
├── test_end_to_end.py        # エンドツーエンドテスト
├── test_tool_integration.py # ツール間連携テスト
└── test_performance.py      # パフォーマンステスト

# tests/fixtures/
├── sample_yaml/              # テスト用YAMLファイル
├── sample_ddl/               # テスト用DDLファイル
└── expected_outputs/         # 期待値ファイル
```

#### 3.2 テスト自動化の改善
```python
# tests/conftest.py
@pytest.fixture
def sample_table_definition():
    """サンプルテーブル定義"""
    return TableDefinition(
        name="MST_Employee",
        logical_name="社員基本情報",
        columns=[...],
        indexes=[...],
        foreign_keys=[...]
    )

@pytest.fixture
def temp_database_structure(tmp_path):
    """一時的なデータベース構造"""
    # テスト用ディレクトリ構造を作成
    pass
```

### Phase 4: 新機能の追加 ✨

#### 4.1 インタラクティブモードの実装
```python
# shared/interactive/
├── cli_interface.py          # CLIインターフェース
├── wizard.py                 # ウィザード機能
└── validation_helper.py      # 検証ヘルパー

# 使用例
python -m database_consistency_checker --interactive
> テーブル名を入力してください: MST_Employee
> チェック項目を選択してください:
  [1] 基本整合性チェック
  [2] パフォーマンスチェック
  [3] セキュリティチェック
  [4] すべて
```

#### 4.2 設定管理の改善
```python
# shared/config/
├── config_manager.py         # 設定管理
├── profile_manager.py        # プロファイル管理
└── validation_rules.py       # 検証ルール

# 設定プロファイル例
# profiles/development.yaml
database_tools:
  strict_mode: false
  performance_checks: false
  
# profiles/production.yaml
database_tools:
  strict_mode: true
  performance_checks: true
  security_checks: true
```

#### 4.3 CI/CD統合機能
```python
# shared/ci_cd/
├── github_actions.py         # GitHub Actions統合
├── jenkins_integration.py    # Jenkins統合
└── report_publisher.py       # レポート公開

# GitHub Actions例
name: Database Consistency Check
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run consistency check
        run: python -m database_consistency_checker --ci-mode --output-format json
```

## 実装優先順位

### 🎯 Phase 1: アダプター統合（1-2日）
1. **共通アダプター基盤作成**
   - `shared/adapters/base_adapter.py`
   - `shared/adapters/table_adapter.py`
   - `shared/adapters/consistency_adapter.py`

2. **既存アダプターの移行**
   - 既存の`adapters.py`を共通ライブラリに統合
   - 重複コードの除去
   - インターフェースの統一

3. **メインファイルの更新**
   - 新しいアダプターを使用するように更新
   - インポート文の修正

### 🔧 Phase 2: チェック機能拡張（2-3日）
1. **高度なチェック機能**
   - パフォーマンス影響チェック
   - セキュリティ準拠チェック
   - マルチテナント準拠チェック

2. **相互参照チェック**
   - 循環依存検出
   - 孤立参照検出
   - 整合性レポート

3. **レポート機能強化**
   - 複数形式対応
   - 詳細レポート
   - 可視化機能

### 🧪 Phase 3: テスト強化（1-2日）
1. **テストスイート拡張**
   - ユニットテスト追加
   - 統合テスト強化
   - パフォーマンステスト

2. **テストデータ整備**
   - フィクスチャ作成
   - サンプルデータ拡充
   - エッジケース対応

### ✨ Phase 4: 新機能追加（2-3日）
1. **インタラクティブモード**
   - CLIウィザード
   - 対話的検証
   - ヘルプ機能

2. **設定管理改善**
   - プロファイル機能
   - 環境別設定
   - 検証ルール

3. **CI/CD統合**
   - 自動化スクリプト
   - レポート統合
   - 通知機能

## 期待される効果

### 🚀 開発効率向上
- **コード重複削除**: 30%のコード削減
- **保守性向上**: 統一されたアーキテクチャ
- **テスト効率**: 自動化による品質保証

### 🔍 機能強化
- **包括的チェック**: より詳細な整合性検証
- **レポート充実**: 多様な出力形式
- **使いやすさ**: インタラクティブモード

### 🛡️ 品質向上
- **エラー検出**: 早期問題発見
- **標準化**: 一貫した品質基準
- **自動化**: 人的ミス削減

## 次のアクション

1. **Phase 1の実装開始**: アダプター統合から着手
2. **テスト環境準備**: 既存機能の動作確認
3. **段階的移行**: 機能ごとの段階的リファクタリング
4. **ドキュメント更新**: 変更に伴う文書更新

このリファクタリング計画により、より保守性が高く、機能豊富なデータベース整合性チェックツールを構築できます。
