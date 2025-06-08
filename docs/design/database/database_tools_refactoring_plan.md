# データベースツール統合リファクタリング計画

## 現状分析

### 1. 現在のツール構成

#### table_generator
```
table_generator/
├── core/
│   ├── config.py          # 統合設定へのラッパー
│   ├── logger.py          # ログ管理
│   └── models.py          # データモデル
├── data/
│   ├── faker_utils.py     # テストデータ生成
│   └── yaml_data_loader.py
├── generators/
│   ├── ddl_generator.py   # DDL生成
│   ├── insert_generator.py
│   └── table_definition_generator.py
└── utils/
    ├── file_utils.py
    ├── sql_utils.py
    └── yaml_loader.py
```

#### database_consistency_checker
```
database_consistency_checker/
├── core/
│   ├── config.py          # 統合設定へのラッパー
│   ├── logger.py          # ログ管理
│   ├── models.py          # データモデル（重複多数）
│   └── report_builder.py
├── checkers/             # 15個のチェッカー
├── fixers/               # 修正提案生成
├── parsers/              # 5個のパーサー
├── reporters/            # 3個のレポーター
└── utils/
    └── report_manager.py
```

#### shared/
```
shared/
└── core/
    └── config.py         # 統合設定システム
```

### 2. 問題点の特定

#### A. コード重複
- **models.py**: 両ツールで類似のデータモデルが重複定義
- **logger.py**: ログ機能が各ツールで独立実装
- **config.py**: 統合設定へのラッパーが各ツールで個別実装
- **yaml_loader.py**: YAML読み込み機能が重複

#### B. 依存関係の複雑化
- 各ツールが独自の設定ラッパーを持つ
- 統合設定への依存が間接的
- パーサー機能の重複（DDL、YAML）

#### C. 保守性の問題
- 機能追加時に複数箇所の修正が必要
- テストコードの重複
- ドキュメントの分散

## リファクタリング戦略

### Phase 1: 共通基盤の統合（優先度：最高）

#### 1.1 共通データモデルの統合
```
shared/
├── core/
│   ├── config.py         # 既存の統合設定
│   ├── models.py         # 統合データモデル
│   ├── logger.py         # 統合ログシステム
│   └── exceptions.py     # 統一例外クラス
├── parsers/
│   ├── yaml_parser.py    # 統合YAMLパーサー
│   ├── ddl_parser.py     # 統合DDLパーサー
│   └── base_parser.py    # パーサー基底クラス
├── utils/
│   ├── file_utils.py     # ファイル操作ユーティリティ
│   ├── sql_utils.py      # SQL関連ユーティリティ
│   └── validation.py     # 共通バリデーション
└── types/
    ├── __init__.py
    ├── table_types.py    # テーブル関連型定義
    ├── check_types.py    # チェック関連型定義
    └── report_types.py   # レポート関連型定義
```

#### 1.2 統合データモデル設計
```python
# shared/core/models.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Union
from enum import Enum

# 基底クラス
@dataclass
class BaseModel:
    """全データモデルの基底クラス"""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """辞書形式に変換"""
        pass
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """辞書から生成"""
        pass

# テーブル関連モデル
@dataclass
class ColumnDefinition(BaseModel):
    """統合カラム定義"""
    name: str
    logical_name: str = ""
    data_type: str = ""
    length: Optional[int] = None
    nullable: bool = True
    primary_key: bool = False
    foreign_key: bool = False
    default_value: Optional[str] = None
    comment: str = ""
    requirement_id: str = ""  # 要求仕様ID対応

@dataclass
class TableDefinition(BaseModel):
    """統合テーブル定義"""
    table_name: str
    logical_name: str
    category: str
    priority: str = "中"
    requirement_id: str = ""
    columns: List[ColumnDefinition] = field(default_factory=list)
    indexes: List['IndexDefinition'] = field(default_factory=list)
    foreign_keys: List['ForeignKeyDefinition'] = field(default_factory=list)
    constraints: List['ConstraintDefinition'] = field(default_factory=list)

# チェック関連モデル
@dataclass
class CheckResult(BaseModel):
    """統合チェック結果"""
    check_name: str
    table_name: str
    severity: 'CheckSeverity'
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    requirement_id: str = ""

# レポート関連モデル
@dataclass
class GenerationReport(BaseModel):
    """生成レポート"""
    generated_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
```

### Phase 2: パーサー統合（優先度：高）

#### 2.1 統合パーサーアーキテクチャ
```python
# shared/parsers/base_parser.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from ..core.models import BaseModel

class BaseParser(ABC):
    """パーサー基底クラス"""
    
    def __init__(self, config):
        self.config = config
        self.logger = get_logger(__name__)
    
    @abstractmethod
    def parse(self, source: Any) -> BaseModel:
        """解析実行"""
        pass
    
    def validate(self, result: BaseModel) -> List[str]:
        """解析結果の検証"""
        pass

# shared/parsers/yaml_parser.py
class UnifiedYAMLParser(BaseParser):
    """統合YAMLパーサー"""
    
    def parse_table_detail(self, yaml_path: Path) -> TableDefinition:
        """テーブル詳細YAML解析"""
        pass
    
    def parse_entity_relationships(self, yaml_path: Path) -> List[EntityRelationship]:
        """エンティティ関連YAML解析"""
        pass

# shared/parsers/ddl_parser.py
class UnifiedDDLParser(BaseParser):
    """統合DDLパーサー"""
    
    def parse_create_table(self, ddl_content: str) -> TableDefinition:
        """CREATE TABLE文解析"""
        pass
    
    def parse_indexes(self, ddl_content: str) -> List[IndexDefinition]:
        """インデックス定義解析"""
        pass
```

#### 2.2 パーサー統合による効果
- **コード削減**: 重複パーサーコードの統合
- **一貫性向上**: 解析ロジックの統一
- **保守性向上**: 単一箇所での修正対応

### Phase 3: ツール固有機能の最適化（優先度：中）

#### 3.1 table_generator リファクタリング
```
table_generator/
├── __init__.py
├── __main__.py
├── README.md
├── generators/
│   ├── __init__.py
│   ├── ddl_generator.py      # DDL生成（共通パーサー使用）
│   ├── markdown_generator.py # Markdown生成
│   ├── insert_generator.py   # INSERT文生成
│   └── report_generator.py   # 生成レポート
├── data/
│   ├── __init__.py
│   ├── faker_factory.py      # Fakerファクトリー
│   └── sample_data_generator.py
└── cli/
    ├── __init__.py
    └── commands.py           # CLI コマンド
```

#### 3.2 database_consistency_checker リファクタリング
```
database_consistency_checker/
├── __init__.py
├── main.py
├── README.md
├── checkers/
│   ├── __init__.py
│   ├── base_checker.py       # チェッカー基底クラス
│   ├── table_checker.py      # テーブル関連チェック
│   ├── column_checker.py     # カラム関連チェック
│   ├── constraint_checker.py # 制約関連チェック
│   └── compliance_checker.py # コンプライアンスチェック
├── fixers/
│   ├── __init__.py
│   ├── base_fixer.py         # 修正提案基底クラス
│   └── auto_fixer.py         # 自動修正機能
├── reporters/
│   ├── __init__.py
│   ├── base_reporter.py      # レポーター基底クラス
│   ├── console_reporter.py
│   ├── markdown_reporter.py
│   └── json_reporter.py
└── cli/
    ├── __init__.py
    └── commands.py           # CLI コマンド
```

### Phase 4: 統合CLI・API設計（優先度：中）

#### 4.1 統合CLIアーキテクチャ
```python
# tools/cli/main.py
import click
from .table_generator_commands import table_gen_group
from .consistency_checker_commands import check_group

@click.group()
@click.option('--config', help='設定ファイルパス')
@click.option('--verbose', is_flag=True, help='詳細ログ出力')
@click.pass_context
def cli(ctx, config, verbose):
    """データベースツール統合CLI"""
    ctx.ensure_object(dict)
    ctx.obj['config'] = config
    ctx.obj['verbose'] = verbose

cli.add_command(table_gen_group, name='generate')
cli.add_command(check_group, name='check')

if __name__ == '__main__':
    cli()
```

#### 4.2 使用例
```bash
# テーブル生成
python -m tools generate table MST_Employee --verbose

# 整合性チェック
python -m tools check all --output-format markdown

# 統合実行
python -m tools generate table MST_Employee && python -m tools check table MST_Employee
```

### Phase 5: テスト統合・品質保証（優先度：中）

#### 5.1 統合テスト戦略
```
tests/
├── unit/
│   ├── shared/
│   │   ├── test_models.py
│   │   ├── test_parsers.py
│   │   └── test_config.py
│   ├── table_generator/
│   │   └── test_generators.py
│   └── consistency_checker/
│       └── test_checkers.py
├── integration/
│   ├── test_end_to_end.py
│   └── test_tool_integration.py
├── fixtures/
│   ├── sample_yaml/
│   ├── sample_ddl/
│   └── expected_outputs/
└── conftest.py
```

#### 5.2 品質保証指標
- **テストカバレッジ**: 90%以上
- **静的解析**: flake8, mypy, black準拠
- **パフォーマンス**: 大規模テーブル（100テーブル）での実行時間5分以内
- **メモリ使用量**: 1GB以内

## 実装計画

### Week 1-2: Phase 1 実装
- [ ] 統合データモデル設計・実装
- [ ] 統合ログシステム実装
- [ ] 統合設定システム拡張
- [ ] 基本的な単体テスト作成

### Week 3-4: Phase 2 実装
- [ ] 統合パーサー実装
- [ ] 既存パーサーからの移行
- [ ] パーサー統合テスト
- [ ] 既存機能の動作確認

### Week 5-6: Phase 3 実装
- [ ] table_generator リファクタリング
- [ ] database_consistency_checker リファクタリング
- [ ] 機能テスト・回帰テスト
- [ ] パフォーマンステスト

### Week 7-8: Phase 4-5 実装
- [ ] 統合CLI実装
- [ ] 統合テストスイート構築
- [ ] ドキュメント更新
- [ ] 最終的な品質保証

## 期待効果

### 1. 開発効率向上
- **コード重複削減**: 30-40%のコード削減
- **機能追加速度**: 新機能開発時間50%短縮
- **バグ修正効率**: 単一箇所修正による影響範囲の明確化

### 2. 保守性向上
- **統一アーキテクチャ**: 一貫した設計パターン
- **テスト効率**: 統合テストによる品質保証
- **ドキュメント統合**: 単一ドキュメントでの管理

### 3. 拡張性向上
- **新ツール追加**: 共通基盤の再利用
- **機能拡張**: プラグインアーキテクチャ対応
- **API化**: 外部システムとの連携対応

## リスク管理

### 技術リスク
- **既存機能の破壊**: 段階的移行による影響最小化
- **パフォーマンス劣化**: ベンチマークテストによる監視
- **互換性問題**: 後方互換性の維持

### プロジェクトリスク
- **スケジュール遅延**: 週次進捗確認による早期対応
- **品質低下**: 継続的テストによる品質保証
- **チーム負荷**: 段階的実装による負荷分散

## 成功指標

### 定量指標
- **コード行数削減**: 30%以上
- **テストカバレッジ**: 90%以上
- **実行時間**: 既存比120%以内
- **メモリ使用量**: 既存比110%以内

### 定性指標
- **開発者満足度**: 4.0/5.0以上
- **保守性**: コードレビュー時間50%短縮
- **拡張性**: 新機能追加時間50%短縮

この統合リファクタリング計画により、データベースツールの効率性・保守性・拡張性を大幅に向上させ、AI駆動開発の知見獲得と実用的システム完成の両立を実現します。
