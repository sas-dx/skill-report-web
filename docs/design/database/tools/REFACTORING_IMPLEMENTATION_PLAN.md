# データベース整合性チェックツール リファクタリング実装計画

## 現状分析

### 問題点の特定

#### 1. アダプター層の重複・分散
- **table_generator/core/adapters.py**: `TableGeneratorService`
- **database_consistency_checker/core/adapters.py**: `DatabaseConsistencyService`
- **shared/adapters/table_adapter.py**: `TableDefinitionAdapter`
- **shared/adapters/consistency_adapter.py**: `ConsistencyAdapter`

**問題**: 同様の機能が複数箇所に分散し、保守性が低下

#### 2. データモデルの不統一
- 各アダプターが独自のデータ構造を使用
- 統合データモデル（shared/core/models）の活用が不十分
- レガシーモデルとの混在

#### 3. 責任の曖昧さ
- ビジネスロジックとデータアクセスが混在
- 各サービスが直接パーサー・ジェネレーターを呼び出し
- 統一されたインターフェースの欠如

### 現在のアーキテクチャ
```
Tools/
├── table_generator/
│   └── core/adapters.py (TableGeneratorService)
├── database_consistency_checker/
│   └── core/adapters.py (DatabaseConsistencyService)
└── shared/
    ├── adapters/
    │   ├── table_adapter.py (TableDefinitionAdapter)
    │   └── consistency_adapter.py (ConsistencyAdapter)
    ├── parsers/ (YamlParser, DDLParser, MarkdownParser)
    ├── generators/ (DDLGenerator, MarkdownGenerator, SampleDataGenerator)
    └── checkers/ (AdvancedConsistencyChecker)
```

## リファクタリング目標

### 1. 統一されたアーキテクチャ
- **単一責任原則**: 各コンポーネントが明確な責任を持つ
- **依存性逆転**: 高レベルモジュールが低レベルモジュールに依存しない
- **インターフェース分離**: 必要な機能のみを公開

### 2. 統合データモデルの完全活用
- 全てのコンポーネントで統合データモデルを使用
- レガシーモデルの完全除去
- 型安全性の向上

### 3. 保守性・拡張性の向上
- コードの重複排除
- 設定の一元化
- テスタビリティの向上

## 新アーキテクチャ設計

### レイヤー構成
```
Application Layer (アプリケーション層)
├── TableGeneratorApplication
└── ConsistencyCheckerApplication

Domain Layer (ドメイン層)
├── Services/
│   ├── TableDefinitionService
│   ├── FileGenerationService
│   └── ConsistencyCheckService
└── Models/ (統合データモデル)

Infrastructure Layer (インフラ層)
├── Adapters/
│   ├── FileSystemAdapter
│   ├── YamlAdapter
│   ├── DDLAdapter
│   └── MarkdownAdapter
├── Parsers/
├── Generators/
└── Checkers/
```

### 統合アダプター設計

#### 1. 統合ファイルシステムアダプター
```python
class UnifiedFileSystemAdapter:
    """統合ファイルシステムアダプター"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.yaml_parser = YamlParser()
        self.ddl_parser = DDLParser()
        self.markdown_parser = MarkdownParser()
    
    def load_table_definition(self, source_type: str, source_path: Path) -> TableDefinition:
        """統一されたテーブル定義読み込み"""
        
    def save_generated_content(self, content_type: str, content: str, output_path: Path) -> None:
        """統一されたコンテンツ保存"""
        
    def discover_table_files(self, directory: Path) -> Dict[str, List[Path]]:
        """テーブル関連ファイルの自動発見"""
```

#### 2. 統合データ変換アダプター
```python
class UnifiedDataTransformAdapter:
    """統合データ変換アダプター"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.ddl_generator = DDLGenerator()
        self.markdown_generator = MarkdownGenerator()
        self.sample_data_generator = SampleDataGenerator()
    
    def transform_to_ddl(self, table_def: TableDefinition) -> str:
        """DDL生成"""
        
    def transform_to_markdown(self, table_def: TableDefinition) -> str:
        """Markdown生成"""
        
    def transform_to_sample_data(self, table_def: TableDefinition) -> str:
        """サンプルデータ生成"""
```

#### 3. 統合整合性チェックアダプター
```python
class UnifiedConsistencyAdapter:
    """統合整合性チェックアダプター"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.advanced_checker = AdvancedConsistencyChecker()
    
    def check_table_existence(self, table_definitions: Dict[str, Dict[str, TableDefinition]]) -> CheckResult:
        """テーブル存在整合性チェック"""
        
    def check_column_consistency(self, yaml_defs: Dict[str, TableDefinition], ddl_defs: Dict[str, TableDefinition]) -> CheckResult:
        """カラム整合性チェック"""
        
    def check_foreign_key_consistency(self, table_definitions: Dict[str, TableDefinition]) -> CheckResult:
        """外部キー整合性チェック"""
```

### ドメインサービス設計

#### 1. テーブル定義サービス
```python
class TableDefinitionService:
    """テーブル定義ドメインサービス"""
    
    def __init__(self, file_adapter: UnifiedFileSystemAdapter):
        self.file_adapter = file_adapter
    
    def load_table_definitions_from_directory(self, directory: Path, source_type: str) -> Dict[str, TableDefinition]:
        """ディレクトリからテーブル定義を一括読み込み"""
        
    def validate_table_definition(self, table_def: TableDefinition) -> ValidationResult:
        """テーブル定義の妥当性検証"""
        
    def normalize_table_definition(self, table_def: TableDefinition) -> TableDefinition:
        """テーブル定義の正規化"""
```

#### 2. ファイル生成サービス
```python
class FileGenerationService:
    """ファイル生成ドメインサービス"""
    
    def __init__(self, transform_adapter: UnifiedDataTransformAdapter, file_adapter: UnifiedFileSystemAdapter):
        self.transform_adapter = transform_adapter
        self.file_adapter = file_adapter
    
    def generate_table_files(self, table_def: TableDefinition, output_config: OutputConfig) -> GenerationResult:
        """テーブル関連ファイルの生成"""
        
    def generate_multiple_tables(self, table_definitions: Dict[str, TableDefinition], output_config: OutputConfig) -> List[GenerationResult]:
        """複数テーブルの一括生成"""
```

#### 3. 整合性チェックサービス
```python
class ConsistencyCheckService:
    """整合性チェックドメインサービス"""
    
    def __init__(self, consistency_adapter: UnifiedConsistencyAdapter, table_service: TableDefinitionService):
        self.consistency_adapter = consistency_adapter
        self.table_service = table_service
    
    def run_comprehensive_check(self, directories: DirectoryConfig, check_types: List[CheckType]) -> ConsistencyReport:
        """包括的整合性チェック"""
        
    def generate_consistency_report(self, check_results: List[CheckResult]) -> ConsistencyReport:
        """整合性レポート生成"""
```

### アプリケーション層設計

#### 1. テーブル生成アプリケーション
```python
class TableGeneratorApplication:
    """テーブル生成アプリケーション"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.file_adapter = UnifiedFileSystemAdapter(config)
        self.transform_adapter = UnifiedDataTransformAdapter(config)
        self.table_service = TableDefinitionService(self.file_adapter)
        self.generation_service = FileGenerationService(self.transform_adapter, self.file_adapter)
    
    def process_table(self, table_name: str, options: ProcessingOptions) -> GenerationResult:
        """単一テーブル処理"""
        
    def process_multiple_tables(self, table_names: List[str], options: ProcessingOptions) -> List[GenerationResult]:
        """複数テーブル処理"""
        
    def process_all_tables(self, options: ProcessingOptions) -> List[GenerationResult]:
        """全テーブル処理"""
```

#### 2. 整合性チェックアプリケーション
```python
class ConsistencyCheckerApplication:
    """整合性チェックアプリケーション"""
    
    def __init__(self, config: DatabaseToolsConfig):
        self.config = config
        self.file_adapter = UnifiedFileSystemAdapter(config)
        self.consistency_adapter = UnifiedConsistencyAdapter(config)
        self.table_service = TableDefinitionService(self.file_adapter)
        self.check_service = ConsistencyCheckService(self.consistency_adapter, self.table_service)
    
    def run_checks(self, check_options: CheckOptions) -> ConsistencyReport:
        """整合性チェック実行"""
        
    def generate_report(self, report_options: ReportOptions) -> str:
        """レポート生成"""
```

## 実装手順

### Phase 1: 統合アダプター実装 (1-2日)
1. **UnifiedFileSystemAdapter** の実装
   - 既存のファイル操作ロジックを統合
   - 統合データモデルへの完全移行
   - エラーハンドリングの統一

2. **UnifiedDataTransformAdapter** の実装
   - 既存のジェネレーター呼び出しを統合
   - 変換ロジックの一元化
   - 設定の統一

3. **UnifiedConsistencyAdapter** の実装
   - 既存のチェックロジックを統合
   - AdvancedConsistencyCheckerとの連携
   - チェック結果の統一

### Phase 2: ドメインサービス実装 (2-3日)
1. **TableDefinitionService** の実装
   - テーブル定義の読み込み・検証・正規化
   - ビジネスルールの実装
   - バリデーション強化

2. **FileGenerationService** の実装
   - ファイル生成の統一インターフェース
   - 生成結果の管理
   - エラー処理の改善

3. **ConsistencyCheckService** の実装
   - 整合性チェックの統一実行
   - レポート生成機能
   - 問題の分類・優先度付け

### Phase 3: アプリケーション層実装 (1-2日)
1. **TableGeneratorApplication** の実装
   - 既存のTableGeneratorServiceを置き換え
   - CLIインターフェースとの連携
   - 設定管理の改善

2. **ConsistencyCheckerApplication** の実装
   - 既存のDatabaseConsistencyServiceを置き換え
   - レポート出力機能の強化
   - パフォーマンス最適化

### Phase 4: 既存コードの移行・削除 (1日)
1. **レガシーアダプターの削除**
   - table_generator/core/adapters.py
   - database_consistency_checker/core/adapters.py
   - shared/adapters/table_adapter.py
   - shared/adapters/consistency_adapter.py

2. **インポート文の更新**
   - 全ての参照を新しいアダプターに変更
   - テストコードの更新
   - ドキュメントの更新

### Phase 5: テスト・検証 (1日)
1. **統合テストの実行**
   - 既存機能の動作確認
   - パフォーマンステスト
   - エラーケースの検証

2. **ドキュメント更新**
   - アーキテクチャドキュメント
   - 使用方法ガイド
   - 開発者向けドキュメント

## 期待される効果

### 1. 保守性の向上
- **コード重複の排除**: 40%のコード削減
- **統一されたインターフェース**: 学習コストの削減
- **明確な責任分離**: バグの局所化

### 2. 拡張性の向上
- **新機能追加の容易さ**: プラグイン形式での機能追加
- **設定の柔軟性**: 環境別設定の簡素化
- **テストの充実**: モックを使用した単体テスト

### 3. パフォーマンスの向上
- **効率的なファイル操作**: キャッシュ機能の統合
- **並列処理の最適化**: 複数テーブル処理の高速化
- **メモリ使用量の削減**: 不要なオブジェクト生成の排除

### 4. 品質の向上
- **型安全性**: 統合データモデルによる型チェック
- **エラーハンドリング**: 統一されたエラー処理
- **ログ出力**: 構造化ログによる問題追跡

## リスク管理

### 技術リスク
- **既存機能の破壊**: 段階的移行による影響最小化
- **パフォーマンス劣化**: ベンチマークテストによる検証
- **互換性問題**: 既存インターフェースの維持

### 対策
- **ブランチ戦略**: feature/refactoring-adapters での開発
- **テスト戦略**: 既存テストの維持 + 新規テスト追加
- **ロールバック計画**: 問題発生時の迅速な復旧手順

## 成功指標

### 定量指標
- **コード行数**: 30-40%削減
- **テストカバレッジ**: 90%以上維持
- **実行時間**: 既存機能で性能劣化なし
- **メモリ使用量**: 20%削減

### 定性指標
- **開発者体験**: 新機能追加の容易さ
- **保守性**: バグ修正の局所化
- **可読性**: コードレビューの効率化

この実装計画により、データベース整合性チェックツールの品質・保守性・拡張性を大幅に向上させることができます。
