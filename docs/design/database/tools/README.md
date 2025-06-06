# テーブル定義書作成ツール

このディレクトリには、データベーステーブルの設計・開発を支援する統合ツールが含まれています。

## 🚀 主要機能

### 1. テーブル定義書生成
YAMLファイルからMarkdown形式のテーブル定義書を自動生成

### 2. DDL生成
テーブル定義からCREATE TABLE文、インデックス、外部キー制約などのDDLを生成

### 3. INSERT文生成
サンプルデータからINSERT文を生成し、テストデータの投入を支援

## 📁 ツール構成

### table_generator/
**統合テーブル定義書作成パッケージ**

```
table_generator/
├── __init__.py              # パッケージ初期化
├── __main__.py              # メインエントリーポイント
├── core/                    # コア機能
│   ├── __init__.py
│   ├── config.py            # 設定管理
│   ├── logger.py            # 強化ログ機能（カラー出力対応）
│   └── models.py            # データモデル定義
├── data/                    # データ関連
│   ├── __init__.py
│   ├── faker_utils.py       # テストデータ生成
│   └── yaml_data_loader.py  # YAMLデータローダー
├── generators/              # 生成機能
│   ├── __init__.py
│   ├── common_columns.py    # 共通カラム生成
│   ├── ddl_generator.py     # DDL生成機能
│   ├── insert_generator.py  # INSERT文生成機能
│   └── table_definition_generator.py  # テーブル定義書生成
└── utils/                   # ユーティリティ
    ├── __init__.py
    ├── file_utils.py        # ファイル操作
    ├── sql_utils.py         # SQL関連ユーティリティ
    └── yaml_loader.py       # YAML読み込み
```

## 🛠️ 事前準備・インストール

### Python環境要件
- **Python 3.7以上**が必要です
- **pip**が利用可能であることを確認してください

### 環境確認
```bash
# Python環境確認
python3 --version

# pipの確認・更新
pip3 --version
pip3 install --upgrade pip
```

### 必要なPythonパッケージ
```bash
# 必要パッケージのインストール
pip3 install PyYAML

# インストール確認
python3 -c "import yaml; print('PyYAML installed successfully')"
```

### 動作環境
- **WSL:Ubuntu環境**での動作確認済み
- **Git bash環境**でのコマンド実行推奨
- **標準ライブラリ**：pathlib、datetime、typing（Python 3.7以降で利用可能）

## 🔧 使用方法

### 基本的な使用
```bash
cd ~/skill-report-web/docs/design/database/tools
python3 -m table_generator
```

### コマンドラインオプション

#### 基本オプション
```bash
# 全テーブル生成
python3 -m table_generator

# 個別テーブル生成
python3 -m table_generator --table MST_Employee

# 複数テーブル生成
python3 -m table_generator --table MST_Role,MST_Permission
```

#### 出力制御オプション
```bash
# 出力先ディレクトリ指定
python3 -m table_generator --output-dir custom/

# ベースディレクトリ指定
python3 -m table_generator --base-dir ~/custom/database/

# ドライラン（ファイルを実際には作成しない）
python3 -m table_generator --dry-run
```

#### ログ制御オプション
```bash
# 詳細ログ出力
python3 -m table_generator --verbose

# カラー出力無効
python3 -m table_generator --no-color
```

#### 組み合わせ例
```bash
# 特定テーブルを詳細ログ付きで生成
python3 -m table_generator --table MST_Employee --verbose

# 複数テーブルをカスタムディレクトリに出力
python3 -m table_generator --table MST_Role,MST_Permission --output-dir custom_tables/

# ドライランで全体確認
python3 -m table_generator --dry-run --verbose
```

## 📄 生成される出力ファイル

### 1. テーブル定義書 (Markdown)
- **場所**: `../tables/`
- **形式**: `テーブル定義書_{テーブル名}_{論理名}.md`
- **内容**: 
  - テーブル概要
  - カラム定義（業務カラム + 共通カラム）
  - インデックス定義
  - 外部キー制約
  - 制約条件

### 2. DDLファイル (SQL)
- **場所**: `../ddl/`
- **形式**: `{テーブル名}.sql`
- **内容**:
  - DROP TABLE文
  - CREATE TABLE文
  - インデックス作成文
  - 外部キー制約
  - 初期データINSERT文

### 3. サンプルデータ (SQL)
- **場所**: `../data/`
- **形式**: `{テーブル名}_sample_data.sql`
- **内容**:
  - INSERT文
  - データ型に応じた値フォーマット
  - 実行確認用クエリ

## 🛠️ 開発・カスタマイズ

### パッケージ直接利用
```python
from table_generator.generators.table_definition_generator import TableDefinitionGenerator
from table_generator.generators.ddl_generator import DDLGenerator
from table_generator.generators.insert_generator import InsertGenerator
from table_generator.core.logger import EnhancedLogger

# ログ初期化
logger = EnhancedLogger(enable_color=True)

# テーブル定義書生成
table_gen = TableDefinitionGenerator(logger=logger)
table_gen.generate_files()

# DDL生成
ddl_gen = DDLGenerator(logger=logger)
ddl_content = ddl_gen.generate_table_ddl(table_definition)

# INSERT文生成
insert_gen = InsertGenerator(logger=logger)
insert_content = insert_gen.generate_insert_sql(table_definition)
```

### カスタムジェネレーター作成
```python
from table_generator.core.models import TableDefinition
from table_generator.core.logger import EnhancedLogger

class CustomGenerator:
    def __init__(self, logger: EnhancedLogger = None):
        self.logger = logger or EnhancedLogger()
    
    def generate_custom_output(self, table_def: TableDefinition):
        # カスタム処理を実装
        pass
```

## 📋 機能詳細

### DDL生成機能
- **CREATE TABLE文**: データ型、制約、文字セット対応
- **インデックス**: 通常・ユニークインデックス
- **外部キー制約**: 参照整合性、CASCADE設定
- **マイグレーション**: スキーマ変更DDL生成
- **データベース管理**: DB作成、ユーザー作成、ビュー、ストアドプロシージャ

### INSERT文生成機能
- **データ型対応**: VARCHAR、INT、DATE、BOOLEAN等の適切なフォーマット
- **NULL値処理**: NULL値の適切な出力
- **エスケープ処理**: シングルクォートのエスケープ
- **一括INSERT**: 複数テーブルの一括処理

### ログ機能
- **カラー出力**: ログレベル別の色分け表示
- **ログ履歴**: 実行ログの保持・統計
- **レベル制御**: INFO、WARNING、ERROR、SUCCESS
- **出力制御**: カラー有効/無効、詳細レベル

## 📚 関連ファイル

### 入力ファイル
- `../entity_relationships.yaml` - エンティティ関連定義
- `../テーブル一覧.md` - テーブル一覧
- `../table-details/*.yaml` - 各テーブルの詳細定義

### 出力ディレクトリ
- `../tables/` - 生成されたテーブル定義書
- `../ddl/` - 生成されたDDLファイル
- `../data/` - 生成されたサンプルデータ

## 🔄 更新履歴

- **2025-06-04**: README.md更新 - 現在のツール構成に合わせて全面見直し
- **2025-06-04**: DDL生成機能追加 - CREATE TABLE、インデックス、外部キー対応
- **2025-06-04**: INSERT文生成機能追加 - サンプルデータからINSERT文生成
- **2025-06-04**: ログ機能強化 - カラー出力、ログ履歴、統計機能追加
- **2025-06-04**: __main__.py追加 - モジュール実行対応
- **2025-06-04**: ツール統合・重複解消 - 冗長ファイル削除、table_generatorパッケージに統一

## 🚨 注意事項

### 実行前チェック
```bash
# 作業ディレクトリの確認
pwd
# ~/skill-report-web/docs/design/database/tools であることを確認

# 必要ファイルの存在確認
ls -la ../table-details/
ls -la table_generator/
```

### ファイル依存関係
- **YAMLファイル**：既存の`../table-details/*.yaml`形式に準拠
- **共通カラム定義**：`table_generator/generators/common_columns.py`で管理
- **出力先ディレクトリ**：自動作成されます（../tables/, ../ddl/, ../data/）

### パフォーマンス・トラブルシューティング
- **大量テーブル処理時**：`--verbose`オプションで進捗確認推奨
- **事前確認**：`--dry-run`オプションで実行内容を確認
- **エラー時**：`--verbose`オプションで詳細ログを確認
- **権限エラー**：出力先ディレクトリの書き込み権限を確認

### よくある問題と解決方法
```bash
# ModuleNotFoundError: No module named 'yaml'
pip3 install PyYAML

# Permission denied エラー
chmod +x table_generator/__main__.py

# パスが見つからないエラー
cd ~/skill-report-web/docs/design/database/tools
pwd  # 現在位置を確認
```
