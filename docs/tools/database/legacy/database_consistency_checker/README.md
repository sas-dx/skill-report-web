# データベース整合性チェッカー

## 概要

年間スキル報告書WEB化PJTのデータベース設計における整合性チェック、YAML形式検証、サンプルデータ生成を行う統合ツールです。

## 🏗️ アーキテクチャ

```
database_consistency_checker/
├── __init__.py                          # パッケージ初期化
├── __main__.py                          # メインエントリーポイント
├── main.py                              # 旧メインファイル（互換性維持）
├── run_check.py                         # 実行スクリプト
├── install_git_hook.sh                  # Git pre-commitフック設定
├── checkers/                            # 各種チェッカー
│   ├── __init__.py
│   ├── table_existence_checker.py       # テーブル存在チェック
│   ├── column_consistency_checker.py    # カラム整合性チェック
│   ├── foreign_key_checker.py          # 外部キー整合性チェック
│   ├── naming_convention_checker.py     # 命名規則チェック
│   └── orphaned_files_checker.py       # 孤立ファイルチェック
├── core/                                # コア機能
│   ├── __init__.py
│   ├── config.py                        # 設定管理
│   └── logger.py                        # ログ管理
├── parsers/                             # パーサー
│   ├── __init__.py
│   ├── yaml_parser.py                   # YAML解析
│   ├── ddl_parser.py                    # DDL解析
│   └── markdown_parser.py               # Markdown解析
├── reporters/                           # レポート生成
│   ├── __init__.py
│   ├── console_reporter.py              # コンソール出力
│   ├── markdown_reporter.py             # Markdown出力
│   └── json_reporter.py                 # JSON出力
├── utils/                               # ユーティリティ
│   ├── __init__.py
│   ├── file_utils.py                    # ファイル操作
│   └── validation_utils.py              # 検証ユーティリティ
├── fixers/                              # 自動修正機能
│   ├── __init__.py
│   └── yaml_fixer.py                    # YAML自動修正
├── yaml_format_check.py                 # YAML形式チェック（基本版）
├── yaml_format_check_enhanced.py       # YAML形式チェック（拡張版）
├── yaml_format_check_integration.py    # YAML形式チェック（統合版）
├── sample_data_generator.py             # サンプルデータ生成（基本版）
├── sample_data_generator_enhanced.py   # サンプルデータ生成（拡張版）
├── docs/                                # ドキュメント
├── reports/                             # 生成レポート
└── test_reports/                        # テストレポート
```

## 🚀 主要機能

### 1. 📋 データベース整合性チェック
- **テーブル存在整合性**: YAML ↔ DDL ↔ 定義書の一致確認
- **カラム定義整合性**: データ型・制約・デフォルト値の一致確認
- **外部キー整合性**: 参照関係の妥当性確認
- **命名規則チェック**: プレフィックス・命名規則の準拠確認
- **孤立ファイル検出**: 不要・重複ファイルの検出

### 2. 🔍 YAML形式検証
- **必須セクション検証**: revision_history、overview、notes、business_rulesの存在・内容確認
- **構文チェック**: YAML構文の正確性確認
- **データ型検証**: カラム定義の妥当性確認
- **自動修正機能**: 軽微な問題の自動修正

### 3. 📊 サンプルデータINSERT文生成
- **YAML連携**: テーブル詳細定義YAMLの`sample_data`セクションからINSERT文生成
- **共通カラム自動補完**: id、created_at、updated_at、is_deletedの自動設定
- **複数テーブル対応**: 一括処理と個別処理の両方をサポート
- **統合ファイル出力**: 全テーブルのINSERT文をまとめたファイル生成

## 🛠️ 使用方法

### 基本的な使用方法

```bash
# 全チェック実行
python3 -m database_consistency_checker

# 特定のチェックのみ実行
python3 run_check.py --checks table_existence

# 特定テーブルのみチェック
python3 run_check.py --tables MST_Employee,MST_Department

# 詳細ログ付きで実行
python3 run_check.py --verbose

# レポート出力
python3 run_check.py --output-format markdown --output-file report.md
```

### コマンドラインオプション

| オプション | 説明 | 例 |
|------------|------|-----|
| `--checks` | 実行するチェック項目を指定 | `--checks table_existence,yaml_format` |
| `--tables` | 対象テーブルを指定 | `--tables MST_Employee,MST_Department` |
| `--verbose` | 詳細ログを出力 | `--verbose` |
| `--output-format` | 出力形式（console/markdown/json） | `--output-format markdown` |
| `--output-file` | 出力ファイル名 | `--output-file report.md` |
| `--enhanced` | 拡張機能を使用 | `--enhanced` |
| `--fix` | 自動修正を実行 | `--fix` |

### 利用可能なチェック項目

| チェック項目 | 説明 |
|--------------|------|
| `table_existence` | テーブル存在整合性チェック |
| `column_consistency` | カラム定義整合性チェック |
| `foreign_key_consistency` | 外部キー整合性チェック |
| `naming_convention` | 命名規則チェック |
| `orphaned_files` | 孤立ファイル検出 |
| `yaml_format` | YAML形式検証 |
| `sample_data_generation` | サンプルデータ生成 |

## 🚨 必須セクション - 省略禁止

テーブル詳細YAML定義ファイルには、以下の4つのセクションが**絶対に必須**です。これらのセクションが欠けている場合、自動検証ツールによってコミットが拒否されます。

### 1. revision_history（改版履歴）- 【絶対省略禁止】

#### 目的
- 変更管理・監査の基盤となる重要情報
- テーブル定義の変更履歴を時系列で記録
- 変更の理由・影響範囲を明確化
- 監査要件への対応

#### 必須要素
- **バージョン番号**: セマンティックバージョニング（Major.Minor.Patch）
- **日付**: YYYY-MM-DD形式
- **変更者**: 担当者名または担当チーム名
- **変更内容**: 具体的な変更内容の説明

#### 記述スタイル
- 最新の変更を先頭に追加（降順）
- 変更内容は具体的かつ簡潔に
- 影響範囲や変更理由も記載

#### 最低要件
- **最低1エントリ必須**

#### 例
```yaml
revision_history:
  - version: "1.2.0"
    date: "2025-06-12"
    author: "開発チーム"
    changes: "カラム追加 - manager_id, job_type_idを追加（組織階層管理機能対応）"
  - version: "1.1.0"
    date: "2025-05-20"
    author: "開発チーム"
    changes: "インデックス追加 - 検索性能改善のためemployee_statusにインデックス追加"
  - version: "1.0.0"
    date: "2025-05-01"
    author: "開発チーム"
    changes: "初版作成 - MST_Employeeテーブルの詳細定義"
```

### 2. overview（概要・目的）- 【絶対省略禁止】

#### 目的
- テーブルの存在理由と使用方法を明確にする基本情報
- 設計意図の明確化
- 他テーブルとの関係性の説明
- 業務コンテキストの共有

#### 必須要素
- **テーブルの目的**: このテーブルが存在する理由
- **主な機能**: テーブルが提供する主要な機能
- **関連する業務プロセス**: このテーブルが関わる業務フロー
- **他テーブルとの関係**: 主要な関連テーブルとの関係性

#### 記述スタイル
- 箇条書きと説明文の組み合わせ
- 業務用語と技術用語のバランス
- 第三者が理解できる明確な説明

#### 最低要件
- **最低50文字以上必須**

#### 例
```yaml
overview: |
  組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブル。
  
  主な目的：
  - 社員の基本情報（氏名、連絡先、入社日等）の管理
  - 組織構造（部署、役職、上司関係）の管理
  - 認証・権限管理のためのユーザー情報提供
  - 人事システムとの連携データ基盤
  
  このテーブルは年間スキル報告書システムの中核となるマスタデータであり、
  スキル管理、目標管理、作業実績管理の全ての機能で参照される。
```

### 3. notes（特記事項）- 【絶対省略禁止】

#### 目的
- 運用・保守・セキュリティに関わる重要な補足情報
- 特殊な制約条件や考慮点の明文化
- 将来の拡張・変更時の注意点
- 監査・セキュリティ要件の記録

#### 必須要素
- **運用上の注意点**: 運用時に考慮すべき事項
- **セキュリティ要件**: 暗号化、アクセス制御等
- **特殊な制約**: 通常と異なる制約条件
- **関連システム連携**: 外部システムとの連携ポイント

#### 記述スタイル
- 箇条書きで簡潔に記述
- 重要度の高い項目から順に記載
- 具体的な例や条件を含める

#### 最低要件
- **最低3項目以上必須**

#### 例
```yaml
notes:
  - "個人情報（氏名、氏名カナ、電話番号、生年月日）は暗号化対象"
  - "論理削除は is_deleted フラグで管理"
  - "manager_idによる自己参照で組織階層を表現"
  - "人事システムとの連携でマスタデータを同期"
  - "認証・権限管理システムの基盤テーブル"
  - "スキル管理・目標管理・作業実績管理の全機能で参照される"
```

### 4. business_rules（業務ルール）- 【絶対省略禁止】

#### 目的
- データの整合性と業務要件を保証するための制約条件
- 業務固有のルールの明文化
- 実装時の制約条件の明確化
- 要件トレーサビリティの確保

#### 必須要素
- **一意性制約**: 一意であるべき項目とその理由
- **参照整合性**: 外部キー制約の詳細
- **業務固有ルール**: 特定の業務ドメインに関するルール
- **データ検証ルール**: 入力値の検証条件

#### 記述スタイル
- 箇条書きで明確に記述
- 「〜すべき」「〜である」等の断定的な表現
- 具体的な条件や例外を含める

#### 最低要件
- **最低3項目以上必須**

#### 例
```yaml
business_rules:
  - "社員番号（employee_code）は一意で変更不可"
  - "メールアドレス（email）は認証用のため一意制約必須"
  - "在籍状況（employee_status）がRETIREDの場合、論理削除フラグをtrueに設定"
  - "直属の上司（manager_id）は同一部署内の上位役職者のみ設定可能"
  - "雇用形態（employment_status）に応じた権限・機能制限を適用"
  - "個人情報の暗号化は法的要件に基づく必須対応"
  - "監査証跡として作成日時・更新日時は自動設定"
```

### 必須セクション検証

```bash
# 特定テーブルの必須セクション検証
python3 run_check.py --checks yaml_format --tables MST_Employee --verbose

# 全テーブルの必須セクション検証
python3 run_check.py --checks yaml_format --verbose

# 必須セクション不備の詳細確認
python3 run_check.py --checks yaml_format --enhanced
```

## 📊 サンプルデータINSERT文生成ツール

### 概要

テーブル詳細定義YAMLファイルの`sample_data`セクションを使用して、PostgreSQL用のINSERT文を自動生成するツールです。

### 機能

- YAMLファイルの`sample_data`セクションからINSERT文を生成
- 共通カラム（id, created_at, updated_at, is_deleted）の自動補完
- 複数テーブルの一括処理
- 個別ファイルと統合ファイルの両方を出力
- データ型に応じた適切な値フォーマット
- 詳細なログ出力とエラーハンドリング

### 使用方法

#### 基本的な使用方法

```bash
# 全テーブルのサンプルデータINSERT文を生成
python3 sample_data_generator_enhanced.py

# 詳細ログ付きで実行
python3 sample_data_generator_enhanced.py --verbose

# 特定のテーブルのみ生成
python3 sample_data_generator_enhanced.py --tables MST_Employee

# 複数テーブルを指定
python3 sample_data_generator_enhanced.py --tables MST_Employee,MST_Department --verbose

# 検証機能付きで実行
python3 sample_data_generator_enhanced.py --validate --verbose
```

#### コマンドラインオプション

| オプション | 説明 | 例 |
|------------|------|-----|
| `--tables` | 対象テーブルをカンマ区切りで指定 | `--tables MST_Employee,MST_Department` |
| `--verbose` | 詳細なログを出力 | `--verbose` |
| `--validate` | 検証機能も同時実行 | `--validate` |
| `--enhanced` | 拡張機能を使用 | `--enhanced` |

### 出力ファイル

#### 個別ファイル
- **場所**: `docs/design/database/data/sample_data_{テーブル名}.sql`
- **内容**: 各テーブル専用のINSERT文

#### 統合ファイル
- **場所**: `docs/design/database/data/sample_data_all.sql`
- **内容**: 全テーブルのINSERT文をまとめたファイル

### YAMLファイルの要件

#### 必須セクション
- `sample_data`: サンプルデータの配列
- `columns` または `business_columns`: カラム定義

#### sample_dataの形式
```yaml
sample_data:
  - id: "emp_001"
    employee_code: "EMP000001"
    full_name: "山田太郎"
    email: "yamada.taro@example.com"
    # その他のカラム...
  
  - id: "emp_002"
    employee_code: "EMP000002"
    full_name: "佐藤花子"
    email: "sato.hanako@example.com"
    # その他のカラム...
```

### 自動補完される共通カラム

以下のカラムは`sample_data`に含まれていない場合、自動的に補完されます：

| カラム | 自動設定値 | 説明 |
|--------|------------|------|
| `id` | `{テーブル接頭辞}_{UUID8桁}` | プライマリキー |
| `created_at` | `CURRENT_TIMESTAMP` | 作成日時 |
| `updated_at` | `CURRENT_TIMESTAMP` | 更新日時 |
| `is_deleted` | `FALSE` | 論理削除フラグ |

### データ型別フォーマット

| データ型 | フォーマット | 例 |
|----------|--------------|-----|
| VARCHAR, TEXT, CHAR | シングルクォートで囲む | `'山田太郎'` |
| INTEGER, BIGINT, DECIMAL, FLOAT | 数値のまま | `123`, `45.67` |
| BOOLEAN | TRUE/FALSE | `TRUE`, `FALSE` |
| DATE, DATETIME, TIMESTAMP | シングルクォートで囲む | `'2020-04-01'` |
| NULL値 | NULL | `NULL` |

### 実行例

#### 単一テーブルの生成
```bash
$ python3 sample_data_generator_enhanced.py --tables MST_Employee --verbose

テーブル MST_Employee のサンプルデータ処理を開始...
✓ テーブル MST_Employee: 2件のINSERT文を生成しました
✓ ファイル出力: /path/to/sample_data_MST_Employee.sql
✓ 統合ファイル出力: /path/to/sample_data_all.sql

=== サンプルデータINSERT文生成結果 ===
対象テーブル数: 1
生成成功テーブル数: 1
総レコード数: 2
エラー数: 0
```

#### 全テーブルの生成
```bash
$ python3 sample_data_generator_enhanced.py --verbose

# 51テーブルの処理結果...

=== サンプルデータINSERT文生成結果 ===
対象テーブル数: 51
生成成功テーブル数: 51
総レコード数: 137
エラー数: 0
```

### 生成されるINSERT文の例

```sql
-- サンプルデータ INSERT文: MST_Employee
-- 生成日時: 2025-06-20 00:14:17
-- レコード数: 2

INSERT INTO MST_Employee (id, employee_code, full_name, full_name_kana, email, phone, hire_date, birth_date, gender, department_id, position_id, job_type_id, employment_status, manager_id, employee_status, is_deleted, created_at, updated_at) VALUES ('emp_001', 'EMP000001', '山田太郎', 'ヤマダタロウ', 'yamada.taro@example.com', '090-1234-5678', '2020-04-01', '1990-01-15', 'M', 'dept_001', 'pos_003', 'job_001', 'FULL_TIME', 'emp_002', 'ACTIVE', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

INSERT INTO MST_Employee (id, employee_code, full_name, full_name_kana, email, phone, hire_date, birth_date, gender, department_id, position_id, job_type_id, employment_status, manager_id, employee_status, is_deleted, created_at, updated_at) VALUES ('emp_002', 'EMP000002', '佐藤花子', 'サトウハナコ', 'sato.hanako@example.com', '090-2345-6789', '2018-04-01', '1985-03-20', 'F', 'dept_001', 'pos_002', 'job_001', 'FULL_TIME', NULL, 'ACTIVE', FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- MST_Employee サンプルデータ終了
```

### エラーハンドリング

#### よくあるエラーと対処法

##### 1. YAMLファイルが存在しない
```
❌ ファイル /path/to/MST_Table_details.yaml が存在しません
```
**対処法**: 指定したテーブル名のYAMLファイルが存在するか確認してください。

##### 2. sample_dataセクションが存在しない
```
⚠️ テーブル MST_Table: sample_dataセクションが存在しません
```
**対処法**: YAMLファイルに`sample_data`セクションを追加してください。

##### 3. カラム定義が存在しない
```
❌ テーブル MST_Table: カラム定義が存在しません
```
**対処法**: YAMLファイルに`columns`または`business_columns`セクションを追加してください。

## 🔧 Git pre-commitフック設定

コミット前に自動的に整合性チェックを実行するGit pre-commitフックを設定できます。

```bash
# Git pre-commitフックのインストール
cd docs/design/database/tools/database_consistency_checker
./install_git_hook.sh
```

## 📈 実行例

### 基本的なチェック実行
```bash
$ python3 run_check.py --verbose

=== データベース整合性チェック開始 ===
対象テーブル数: 42

✓ テーブル存在整合性チェック: 42/42 テーブル通過
✓ カラム定義整合性チェック: 42/42 テーブル通過
✓ 外部キー整合性チェック: 15/15 関係通過
✓ 命名規則チェック: 42/42 テーブル通過
✓ YAML形式検証: 42/42 ファイル通過

=== チェック結果サマリー ===
総チェック項目数: 5
成功: 5
警告: 0
エラー: 0
```

### 特定テーブルのチェック
```bash
$ python3 run_check.py --tables MST_Employee --verbose

=== データベース整合性チェック開始 ===
対象テーブル: MST_Employee

✓ テーブル存在整合性: MST_Employee
  - YAML定義ファイル: 存在
  - DDLファイル: 存在
  - Markdown定義書: 存在

✓ カラム定義整合性: MST_Employee
  - 18カラム定義を確認
  - データ型一致: 18/18
  - 制約一致: 18/18

✓ YAML形式検証: MST_Employee
  - 必須セクション: 4/4 存在
  - revision_history: ✓ (3エントリ)
  - overview: ✓ (247文字)
  - notes: ✓ (6項目)
  - business_rules: ✓ (7項目)
```

### エラー検出例
```bash
$ python3 run_check.py --tables MST_Problem --verbose

=== データベース整合性チェック開始 ===
対象テーブル: MST_Problem

❌ テーブル存在整合性: MST_Problem
  - YAML定義ファイル: 存在
  - DDLファイル: ❌ 存在しません
  - Markdown定義書: 存在

⚠️ YAML形式検証: MST_Problem
  - 必須セクション: 2/4 存在
  - revision_history: ❌ セクションが存在しません
  - overview: ✓ (156文字)
  - notes: ❌ セクションが存在しません
  - business_rules: ✓ (4項目)

=== チェック結果サマリー ===
総チェック項目数: 5
成功: 2
警告: 1
エラー: 2
```

## 📊 レポート出力

### Markdown形式レポート
```bash
python3 run_check.py --output-format markdown --output-file consistency_report.md
```

### JSON形式レポート
```bash
python3 run_check.py --output-format json --output-file consistency_report.json
```

## 🛠️ 開発者向け情報

### 主要なクラス・関数

#### チェッカー
- `TableExistenceChecker`: テーブル存在整合性チェック
- `ColumnConsistencyChecker`: カラム定義整合性チェック
- `ForeignKeyChecker`: 外部キー整合性チェック
- `NamingConventionChecker`: 命名規則チェック
- `OrphanedFilesChecker`: 孤立ファイル検出

#### パーサー
- `YamlParser`: YAML解析
- `DdlParser`: DDL解析
- `MarkdownParser`: Markdown解析

#### レポーター
- `ConsoleReporter`: コンソール出力
- `MarkdownReporter`: Markdown出力
- `JsonReporter`: JSON出力

### 拡張ポイント
- 新しいチェッカーの追加
- カスタムレポーター の実装
- 新しいパーサーの追加
- 自動修正機能の拡張

## 🔗 関連ツール

- `table_generator`: テーブル定義書生成ツール
- `yaml_validator`: YAML検証ツール（統合済み）
- `database_tools`: データベース関連ツール群

## 📝 更新履歴

- **v2.0.0** (2025-06-21): 統合版リリース
  - サンプルデータ生成機能統合
  - 必須セクション詳細ガイドライン統合
  - 拡張版機能の統合
  - README.md統合・整理
- **v1.5.0** (2025-06-20): 拡張機能追加
  - サンプルデータINSERT文生成機能
  - YAML形式検証拡張
  - 自動修正機能追加
- **v1.0.0** (2025-06-01): 初版リリース
  - 基本的な整合性チェック機能
  - YAML形式検証
  - レポート出力機能

## 📞 サポート

問題や質問がある場合は、以下の方法でサポートを受けることができます：

1. **ログ確認**: `--verbose`オプションで詳細ログを確認
2. **設定確認**: `core/config.py`で設定を確認
3. **テストレポート**: `test_reports/`ディレクトリのテストレポートを確認
4. **ドキュメント**: `docs/`ディレクトリの詳細ドキュメントを参照

---

このツールは年間スキル報告書WEB化PJTのデータベース品質保証の中核を担っています。定期的な実行により、高品質なデータベース設計を維持してください。
