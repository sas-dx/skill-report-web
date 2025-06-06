# データベース整合性チェックツール

データベース設計ドキュメント間の整合性をチェックするツールです。

## 概要

このツールは以下のファイル間の整合性をチェックします：

1. **テーブル一覧.md** (手動作成)
2. **entity_relationships.yaml** (手動作成)
3. **エンティティ関連図.mdl** (手動作成)
4. **テーブル定義詳細YAML** (手動作成)
5. **テーブル定義書** (自動作成) ⚠️ **手動編集禁止**
6. **DDL** (自動作成) ⚠️ **手動編集禁止**
7. **INSERT文** (自動作成) ⚠️ **手動編集禁止**

## ⚠️ 重要な注意事項

### 手動編集禁止ファイル

以下のファイルは**自動生成されるため、手動での編集は絶対に禁止**です：

- **テーブル定義書** (`tables/テーブル定義書_*.md`)
- **DDLファイル** (`ddl/*.sql`)
- **INSERT文** (`data/*_sample_data.sql`)

これらのファイルを手動で編集した場合：
- 🚨 次回の自動生成時に変更が上書きされます
- 🚨 データベース設計の整合性が保てなくなります
- 🚨 チーム開発での混乱を招きます

**変更が必要な場合は、必ず手動作成ファイル（テーブル一覧.md、entity_relationships.yaml、テーブル定義詳細YAML）を修正してから自動生成を実行してください。**

## 機能

### 現在実装済み
- ✅ テーブル存在整合性チェック
- ✅ 孤立ファイル検出
- ✅ カラム定義整合性チェック
- ✅ 外部キー整合性チェック
- ✅ **データ型整合性チェック** (v1.2.0で追加)
  - DDLとYAML間のデータ型完全一致・互換性チェック
  - カラム定義の詳細比較（長さ制約、NULL制約、デフォルト値、ENUM値）
  - データ型互換性マッピングによる柔軟なチェック
- ✅ コンソール/Markdown/JSON形式でのレポート出力
- ✅ 詳細ログ機能
- ✅ **レポート出力管理機能** (v1.1.0で追加)
  - タイムスタンプ付きファイル名でユニーク性担保
  - 最新レポートへの自動リンク作成
  - 古いレポートの自動クリーンアップ
  - レポート統計情報の取得
- ✅ **YAMLフォーマット整合性チェック** (v1.3.0で追加)
  - テーブル定義詳細YAMLファイルの標準テンプレート準拠確認
  - 必須フィールドの存在チェック
  - データ型・制約の妥当性検証
  - YAMLフォーマット・構造の検証

### 将来実装予定

#### Phase 1（短期：1-2ヶ月）🔥 最高優先度
- 🔄 **制約整合性チェック**
  - PRIMARY KEY制約の整合性確認（DDL vs YAML）
  - UNIQUE制約の整合性確認
  - CHECK制約の整合性確認
  - インデックス定義の整合性確認（名前、カラム、ユニーク性）
  - 外部キー制約の詳細確認（ON UPDATE/DELETE動作）

- 🔄 **修正提案機能**
  - 検出された問題に対する具体的な修正方法の提案
  - DDL修正コマンドの自動生成
  - YAML修正内容の提案
  - 段階的修正手順の提示
  - バックアップ推奨の警告表示

#### Phase 2（中期：3-4ヶ月）⚡ 高優先度
- 🔄 **ビジネスルール整合性チェック**
  - テーブル間の論理的整合性確認
  - 必須カラムの存在確認（created_at, updated_at等）
  - 命名規則の準拠確認（テーブル名、カラム名）
  - カテゴリ分類の妥当性確認

- 🔄 **データ品質チェック**
  - サンプルデータの妥当性確認
  - ENUM値の実際の使用状況確認
  - NULL制約の実データとの整合性
  - デフォルト値の妥当性確認

#### Phase 3（長期：5-6ヶ月）⭐ 中優先度
- 🔄 **パフォーマンス影響分析**
  - インデックス効率性の分析
  - クエリパフォーマンス予測
  - データ量に基づく設計妥当性確認
  - ストレージ使用量予測

- 🔄 **自動修正機能**
  - 軽微な問題の自動修正
  - 修正前後の差分表示
  - 修正履歴の記録
  - ロールバック機能

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

# カラム整合性チェックのみ
python run_check.py --checks column_consistency

# 外部キー整合性チェックのみ
python run_check.py --checks foreign_key_consistency

# データ型整合性チェックのみ
python run_check.py --checks data_type_consistency

# YAMLフォーマット整合性チェックのみ
python run_check.py --checks yaml_format_consistency

# 複数のチェックを指定
python run_check.py --checks table_existence column_consistency foreign_key_consistency data_type_consistency yaml_format_consistency
```

### レポート管理機能 (v1.1.0で追加)

```bash
# レポート出力ディレクトリを指定
python run_check.py --output-format markdown --report-dir custom_reports

# レポート保持期間を設定（デフォルト: 30日）
python run_check.py --output-format markdown --keep-reports 7

# 最大レポート数を設定（デフォルト: 100件）
python run_check.py --output-format markdown --max-reports 50

# カスタムプレフィックスを指定
python run_check.py --output-format markdown --report-prefix "manual_check"

# 自動クリーンアップを無効化
python run_check.py --output-format markdown --no-cleanup

# 詳細なレポート統計を表示
python run_check.py --output-format markdown --verbose
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
├── details/
│   ├── MST_Employee_details.yaml
│   └── ...
└── tools/database_consistency_checker/
    └── reports/                    # レポート出力ディレクトリ (v1.1.0で追加)
        ├── 20250606_200710_consistency_report.md  # タイムスタンプ付きレポート
        ├── latest_consistency_report.md           # 最新レポートリンク
        ├── daily/                                 # 日次レポート用
        ├── manual/                                # 手動実行レポート用
        └── archive/                               # アーカイブ用
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

### 3. データ型整合性チェック (v1.2.0で追加)

DDLファイルとYAML詳細定義間のデータ型整合性をチェックします：

**チェック項目：**
- データ型の完全一致・互換性チェック
- 長さ制約の比較（VARCHAR(50) vs VARCHAR(100)等）
- NULL制約の整合性（NOT NULL vs NULL許可）
- デフォルト値の比較
- ENUM値の整合性

**エラー例：**
- ❌ カラム 'name' のデータ型が一致しません: DDL(VARCHAR(100)) ≠ YAML(VARCHAR(50))
- ❌ カラム 'status' のENUM値が一致しません
- ❌ カラム 'age' の長さ制約が一致しません

**警告例：**
- ⚠️ カラム 'description' のデータ型が互換性のある型で異なります: DDL(TEXT) vs YAML(VARCHAR)
- ⚠️ カラム 'is_active' のNULL制約が一致しません
- ⚠️ カラム 'created_at' のデフォルト値が一致しません

**成功例：**
- ✅ カラム 'id' のデータ型整合性OK: VARCHAR(50)
- ✅ MST_Employee: データ型整合性チェック完了 (12カラム確認済み)

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

### レポート管理機能の出力例 (v1.1.0で追加)

```
📄 レポートを出力しました: /path/to/reports/20250606_200710_consistency_report.md
🔗 最新レポートリンク: /path/to/reports/latest_consistency_report.md
📊 レポート統計: 総数15件, 総サイズ4.2MB
```

**詳細モード（--verbose）での出力例：**
```
📊 レポート統計詳細:
   - 総レポート数: 15件
   - 総サイズ: 4.2MB
   - ディレクトリ別統計:
     * main: 10件 (2.8MB)
     * daily: 3件 (0.9MB)
     * manual: 2件 (0.5MB)
     * archive: 0件 (0.0MB)
   - 最古のレポート: 2025-05-15 (22日前)
   - 最新のレポート: 2025-06-06 (今日)
⚠️ レポートクリーンアップ: 5件の古いレポートを削除しました
```

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

### v1.3.0 (2025-06-06)
- 🚀 **YAMLフォーマット整合性チェック機能を追加**
- テーブル定義詳細YAMLファイルの標準テンプレート準拠確認
- 必須フィールドの存在チェック（table_name, description, columns等）
- データ型・制約の妥当性検証
- YAMLフォーマット・構造の検証
- YamlFormatCheckerクラスの実装
- `--checks yaml_format_consistency`オプションの追加
- 将来実装予定をPhase別に再整理（短期・中期・長期）

### v1.2.0 (2025-06-06)
- 🚀 **データ型整合性チェック機能を追加**
- DDLとYAML間のデータ型完全一致・互換性チェック
- カラム定義の詳細比較（長さ制約、NULL制約、デフォルト値、ENUM値）
- データ型互換性マッピングによる柔軟なチェック
- DataTypeConsistencyCheckerクラスの実装
- `--checks data_type_consistency`オプションの追加
- 包括的なエラー・警告・成功メッセージの提供

### v1.1.0 (2025-06-06)
- 🚀 **レポート出力管理機能を追加**
- タイムスタンプ付きファイル名でユニーク性担保
- 最新レポートへの自動リンク作成機能
- 古いレポートの自動クリーンアップ機能
- レポート統計情報の取得機能
- 新しいコマンドライン引数の追加（--report-dir, --keep-reports等）
- ReportManagerクラスによる統合レポート管理
- reports/ディレクトリ構造の自動作成

### v1.0.0 (2025-06-04)
- 初回リリース
- テーブル存在整合性チェック機能
- 孤立ファイル検出機能
- コンソール/Markdown/JSON出力対応

## サポート

問題や要望がある場合は、開発チームまでお問い合わせください。
