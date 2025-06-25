# データベース設計ツール統合エコシステム

## エグゼクティブサマリー

この統合ツールエコシステムは、年間スキル報告書WEB化プロジェクトのデータベース設計・管理・品質保証を自動化する包括的なソリューションです。YAML統一フォーマット、自動生成機能、整合性チェック、パフォーマンス最適化を提供し、効率的で保守性の高いデータベース開発を支援します。モジュラー設計により拡張性と再利用性を確保し、他プロジェクトでも活用可能な汎用的なツールセットとして構築されています。

## 🚀 主要機能

### 1. 統合ツールエコシステム
- **YAML統一フォーマット**: 全テーブル定義の標準化
- **自動生成機能**: DDL・定義書・サンプルデータの一括生成
- **整合性チェック**: 全ファイル間の整合性検証
- **品質保証**: 必須セクション・命名規則の自動検証

### 2. 主要ツール
- **database_consistency_checker**: 整合性チェック・品質保証
- **table_generator**: テーブル定義・DDL・ドキュメント生成
- **shared**: 共通ライブラリ・ユーティリティ
- **tests**: 包括的テストスイート

### 3. 高度な機能
- **並列処理**: 大量データの高速処理
- **キャッシュ機能**: パフォーマンス最適化
- **メトリクス収集**: 品質・パフォーマンス監視
- **エラー修復**: 自動修復提案機能

## 📁 ディレクトリ構造

```
docs/design/database/tools/
├── README.md                           # 本ファイル
├── main.py                            # 統合エントリーポイント
├── __init__.py                        # パッケージ初期化
│
├── database_consistency_checker/      # 整合性チェックツール
│   ├── main.py                       # メインエントリーポイント
│   ├── run_check.py                  # 実行スクリプト
│   ├── checkers/                     # チェック機能
│   ├── parsers/                      # パーサー機能
│   ├── reporters/                    # レポート生成
│   ├── fixers/                       # 自動修復機能
│   └── utils/                        # ユーティリティ
│
├── table_generator/                   # テーブル生成ツール
│   ├── main.py                       # メインエントリーポイント
│   ├── generators/                   # 生成機能
│   ├── data/                         # データ処理
│   ├── core/                         # コア機能
│   └── utils/                        # ユーティリティ
│
├── shared/                           # 共通ライブラリ
│   ├── core/                         # コア機能
│   ├── utils/                        # ユーティリティ
│   ├── parsers/                      # 統一パーサー
│   ├── generators/                   # 統一ジェネレーター
│   ├── checkers/                     # 統一チェッカー
│   ├── adapters/                     # アダプター
│   ├── performance/                  # パフォーマンス最適化
│   └── monitoring/                   # 監視・メトリクス
│
├── tests/                            # テストスイート
│   ├── unit/                         # ユニットテスト
│   ├── integration/                  # 統合テスト
│   └── performance/                  # パフォーマンステスト
│
├── archive/                          # アーカイブファイル
│   └── reports/                      # 過去のレポート
│
└── venv/                             # Python仮想環境
```

## 🛠️ セットアップ・インストール

### 前提条件
- Python 3.8以上
- pip (Python package installer)

### インストール手順

```bash
# 1. ツールディレクトリに移動
cd docs/design/database/tools

# 2. 仮想環境作成（初回のみ）
python3 -m venv venv

# 3. 仮想環境アクティベート
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows

# 4. 依存関係インストール
pip install -r requirements.txt

# 5. 環境確認
python main.py --help
```

### 依存関係
```
PyYAML>=6.0
Jinja2>=3.1.0
Faker>=18.0.0
colorama>=0.4.6
tqdm>=4.65.0
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
```

## 🚀 使用方法

### 基本的な使用方法

#### 1. 統合ツール実行
```bash
# 全機能を統合実行
python main.py --all

# 特定機能のみ実行
python main.py --check-only
python main.py --generate-only
```

#### 2. 整合性チェック実行
```bash
# 基本チェック
python database_consistency_checker/run_check.py

# 詳細チェック（全項目）
python database_consistency_checker/yaml_format_check_enhanced.py --all --verbose

# 特定テーブルのチェック
python database_consistency_checker/run_check.py --table MST_Employee
```

#### 3. テーブル生成
```bash
# 特定テーブルの生成
python -m table_generator --table MST_Employee --verbose

# 全テーブルの一括生成
python -m table_generator --all

# DDLのみ生成
python -m table_generator --table MST_Employee --ddl-only
```

#### 4. サンプルデータ生成
```bash
# サンプルデータ生成
python database_consistency_checker/sample_data_generator.py --verbose

# 拡張サンプルデータ生成
python database_consistency_checker/sample_data_generator_enhanced.py
```

### 高度な使用方法

#### 1. カスタム設定
```bash
# 設定ファイルを指定
python main.py --config custom_config.yaml

# 出力ディレクトリを指定
python main.py --output-dir /path/to/output
```

#### 2. 並列処理
```bash
# 並列処理で高速実行
python main.py --parallel --workers 4

# 大量データ処理
python main.py --batch-size 100
```

#### 3. 品質チェック
```bash
# 厳密な品質チェック
python database_consistency_checker/run_check.py --strict

# 修復提案付きチェック
python database_consistency_checker/run_check.py --fix-suggestions
```

## 📊 主要コマンド一覧

### 整合性チェック関連
```bash
# YAML形式チェック
python database_consistency_checker/yaml_format_check_enhanced.py --all

# テーブル存在整合性チェック
python database_consistency_checker/checkers/table_existence_checker.py

# 外部キー整合性チェック
python database_consistency_checker/checkers/foreign_key_checker.py

# 全体整合性チェック
python database_consistency_checker/run_check.py --comprehensive
```

### 生成関連
```bash
# DDL生成
python table_generator/generators/ddl_generator.py --table MST_Employee

# Markdown定義書生成
python table_generator/generators/table_definition_generator.py --table MST_Employee

# サンプルデータ生成
python table_generator/generators/insert_generator.py --table MST_Employee
```

### テスト関連
```bash
# 全テスト実行
python run_all_tests.py

# ユニットテスト
pytest tests/unit/ -v

# 統合テスト
pytest tests/integration/ -v

# カバレッジ付きテスト
pytest tests/ --cov=. --cov-report=html
```

## 🔧 設定・カスタマイズ

### 設定ファイル
主要な設定は `shared/core/config.py` で管理されています。

```python
# 基本設定
DEFAULT_CONFIG = {
    'database': {
        'type': 'postgresql',
        'encoding': 'utf-8'
    },
    'output': {
        'ddl_dir': '../ddl',
        'tables_dir': '../tables',
        'yaml_dir': '../table-details'
    },
    'validation': {
        'strict_mode': True,
        'required_sections': ['revision_history', 'overview', 'notes', 'rules']
    }
}
```

### カスタマイズ例
```python
# カスタム設定ファイル作成
custom_config = {
    'validation': {
        'strict_mode': False,
        'custom_rules': ['business_rule_1', 'business_rule_2']
    },
    'generation': {
        'include_sample_data': True,
        'sample_data_count': 10
    }
}
```

## 📈 パフォーマンス最適化

### 並列処理設定
```python
# 並列処理設定
PARALLEL_CONFIG = {
    'max_workers': 4,
    'chunk_size': 10,
    'timeout': 300
}
```

### キャッシュ設定
```python
# キャッシュ設定
CACHE_CONFIG = {
    'enabled': True,
    'ttl': 3600,  # 1時間
    'max_size': 1000
}
```

## 🧪 テスト・品質保証

### テスト実行
```bash
# 全テスト実行
pytest tests/ -v

# 特定テストのみ
pytest tests/unit/test_yaml_parser.py -v

# カバレッジレポート生成
pytest tests/ --cov=. --cov-report=html --cov-report=term
```

### 品質チェック
```bash
# コード品質チェック
flake8 .

# 型チェック
mypy .

# コードフォーマット
black .
```

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. YAML形式エラー
```bash
# エラー: YAML構文エラー
# 解決: YAML検証ツール実行
python database_consistency_checker/yaml_format_check_enhanced.py --table TABLE_NAME
```

#### 2. 必須セクション不足
```bash
# エラー: 必須セクション 'overview' が存在しません
# 解決: YAMLファイルに必須セクションを追加
```

#### 3. 整合性エラー
```bash
# エラー: テーブル存在整合性エラー
# 解決: 整合性チェック実行
python database_consistency_checker/run_check.py --fix-suggestions
```

#### 4. パフォーマンス問題
```bash
# 解決: 並列処理・キャッシュ有効化
python main.py --parallel --cache-enabled
```

### ログ・デバッグ
```bash
# デバッグモード実行
python main.py --debug --verbose

# ログファイル確認
tail -f logs/database_tools.log
```

## 📚 開発・拡張

### 新機能追加
1. `shared/` ディレクトリに共通機能を追加
2. 各ツールディレクトリに特化機能を追加
3. テストケースを `tests/` に追加
4. ドキュメントを更新

### コントリビューション
1. フォーク・ブランチ作成
2. 機能実装・テスト追加
3. コード品質チェック実行
4. プルリクエスト作成

## 📄 ライセンス・サポート

### ライセンス
このツールセットは内部プロジェクト用として開発されています。

### サポート・問い合わせ
- 開発チーム: 黒澤 (@yusuke-kurosawa)
- プロジェクト: 年間スキル報告書WEB化PJT

## 🔄 更新履歴

### v2.0.0 (2025-06-26)
- 🎉 **大規模リファクタリング完了**
- ✨ 統合ツールエコシステム構築
- 🚀 パフォーマンス最適化（並列処理・キャッシュ）
- 🧪 包括的テストスイート追加
- 📊 メトリクス収集・監視機能追加

### v1.x.x (2025-05-xx)
- 基本的なYAMLチェック・生成機能
- 個別ツールの開発・改善

---

**🎯 このツールエコシステムにより、効率的で品質の高いデータベース設計・開発を実現してください。**
