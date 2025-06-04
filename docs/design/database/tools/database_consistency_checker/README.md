# データベース整合性チェックツール

データベース設計ドキュメント間の整合性をチェックするツールです。

## 概要

このツールは以下のファイル間の整合性をチェックします：

1. **テーブル一覧.md** (手動作成)
2. **entity_relationships.yaml** (手動作成)
3. **エンティティ関連図.mdl** (手動作成)
4. **テーブル定義詳細YAML** (手動作成)
5. **テーブル定義書** (自動作成)
6. **DDL** (自動作成)
7. **INSERT文** (自動作成)

## 機能

### 現在実装済み
- ✅ テーブル存在整合性チェック
- ✅ 孤立ファイル検出
- ✅ コンソール/Markdown/JSON形式でのレポート出力
- ✅ 詳細ログ機能

### 将来実装予定
- 🔄 カラム定義整合性チェック
- 🔄 外部キー整合性チェック
- 🔄 データ型整合性チェック
- 🔄 制約整合性チェック
- 🔄 修正提案機能

## インストール

```bash
# 必要なPythonパッケージをインストール
pip install pyyaml
```

## 使用方法

### 基本的な使用方法

```bash
# 全チェック実行
python run_check.py

# 特定のテーブルのみチェック
python run_check.py --tables MST_Employee MST_Department

# 詳細ログ付きでチェック
python run_check.py --verbose
```

### 出力形式の指定

```bash
# Markdown形式で出力
python run_check.py --output-format markdown --output-file report.md

# JSON形式で出力
python run_check.py --output-format json --output-file report.json

# コンソール出力（デフォルト）
python run_check.py --output-format console
```

### 特定のチェックのみ実行

```bash
# テーブル存在チェックのみ
python run_check.py --checks table_existence

# 孤立ファイルチェックのみ
python run_check.py --checks orphaned_files

# 複数のチェックを指定
python run_check.py --checks table_existence orphaned_files
```

### 利用可能なオプション

```bash
# ヘルプを表示
python run_check.py --help

# 利用可能なチェック一覧を表示
python run_check.py --list-checks

# バージョン情報を表示
python run_check.py --version
```

## ディレクトリ構造

ツールは以下のディレクトリ構造を前提としています：

```
docs/design/database/
├── テーブル一覧.md
├── entity_relationships.yaml
├── エンティティ関連図.mdl
├── tables/
│   ├── テーブル定義書_MST_Employee_社員基本情報.md
│   └── ...
├── ddl/
│   ├── MST_Employee.sql
│   └── ...
├── data/
│   ├── MST_Employee_sample_data.sql
│   └── ...
└── details/
    ├── MST_Employee_details.yaml
    └── ...
```

## チェック項目

### 1. テーブル存在整合性チェック

各テーブルが以下の全てのソースに存在するかをチェックします：

- テーブル一覧.md
- entity_relationships.yaml
- DDLファイル
- テーブル詳細定義ファイル

**エラー例：**
- ❌ テーブル一覧.mdに定義されていません
- ❌ DDLファイルが存在しません

**警告例：**
- ⚠️ エンティティ関連定義に存在しません
- ⚠️ テーブル詳細定義ファイルが存在しません

### 2. 孤立ファイル検出

テーブル一覧.mdに定義されていないファイルを検出します：

- 孤立DDLファイル
- 孤立詳細定義ファイル

## 出力例

### コンソール出力

```
🔍 データベース整合性チェック開始

📊 テーブル存在整合性チェック
✅ MST_Employee: 全てのソースに存在します
❌ MST_Department: DDLファイルが存在しません
⚠️ MST_Project: テーブル詳細定義ファイルが存在しません

🔍 孤立ファイルチェック
⚠️ 孤立ファイル: OLD_Table.sql

📈 結果サマリー:
  ✅ SUCCESS: 1件
  ⚠️ WARNING: 2件
  ❌ ERROR: 1件

🎯 総合判定:
  ❌ 修正が必要な問題があります
```

### Markdown出力

詳細な表形式のレポートが生成されます。

### JSON出力

プログラムで処理しやすい構造化データが出力されます。

## 設定

### 環境変数

- `DB_CONSISTENCY_BASE_DIR`: ベースディレクトリのパス
- `DB_CONSISTENCY_VERBOSE`: 詳細ログの有効化 (true/false)

### 設定ファイル

将来的に設定ファイル（YAML/JSON）での設定をサポート予定です。

## トラブルシューティング

### よくある問題

1. **ファイルが見つからない**
   ```
   ❌ 設定初期化エラー: 必要なファイル/ディレクトリが見つかりません
   ```
   → ディレクトリ構造を確認してください

2. **YAML解析エラー**
   ```
   ❌ YAML解析エラー: ...
   ```
   → YAMLファイルの構文を確認してください

3. **権限エラー**
   ```
   ❌ ファイルの読み込みエラー: Permission denied
   ```
   → ファイルの読み取り権限を確認してください

### デバッグ

詳細なエラー情報を取得するには `--verbose` オプションを使用してください：

```bash
python run_check.py --verbose
```

## 開発者向け情報

### アーキテクチャ

```
database_consistency_checker/
├── core/           # コア機能
│   ├── models.py   # データモデル
│   ├── config.py   # 設定管理
│   └── logger.py   # ログ機能
├── parsers/        # ファイル解析
│   ├── table_list_parser.py
│   ├── entity_yaml_parser.py
│   └── ddl_parser.py
├── checkers/       # チェック機能
│   ├── table_existence_checker.py
│   └── consistency_checker.py
├── reporters/      # レポート出力
│   ├── console_reporter.py
│   ├── markdown_reporter.py
│   └── json_reporter.py
└── main.py         # メインエントリーポイント
```

### 新しいチェック機能の追加

1. `checkers/` ディレクトリに新しいチェッカークラスを作成
2. `ConsistencyChecker` クラスに統合
3. `main.py` でコマンドライン引数を追加

### テスト

```bash
# 単体テスト実行（将来実装予定）
python -m pytest tests/

# 統合テスト実行（将来実装予定）
python -m pytest tests/integration/
```

## ライセンス

このツールは内部使用のために開発されました。

## 更新履歴

### v1.0.0 (2025-06-04)
- 初回リリース
- テーブル存在整合性チェック機能
- 孤立ファイル検出機能
- コンソール/Markdown/JSON出力対応

## サポート

問題や要望がある場合は、開発チームまでお問い合わせください。
