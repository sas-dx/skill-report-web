# データベース設計ツール統合システム

## 概要

年間スキル報告書WEB化PJTにおけるデータベース設計・開発を効率化するための統合ツールシステムです。YAML詳細定義からテーブル定義書・DDL・サンプルデータの自動生成と、データベース設計の整合性チェックを提供します。

## 要求仕様ID

- **PLT.1-WEB.1**: システム基盤要件（データベース設計ツール）
- **TNT.1-MGMT**: マルチテナント基盤要件（テナント分離対応）

## システム構成

```
docs/design/database/tools/
├── README.md                           # 本ファイル
├── __init__.py                         # パッケージ初期化
├── run_tests.py                        # テスト実行スクリプト
├── shared/                             # 共通ライブラリ
│   ├── core/                          # コア機能
│   │   ├── config.py                  # 統合設定管理
│   │   ├── exceptions.py              # 例外定義
│   │   └── models.py                  # データモデル
│   ├── parsers/                       # パーサー群
│   │   ├── yaml_parser.py             # YAML解析
│   │   ├── ddl_parser.py              # DDL解析
│   │   └── markdown_parser.py         # Markdown解析
│   ├── generators/                    # ジェネレーター群
│   │   ├── ddl_generator.py           # DDL生成
│   │   ├── markdown_generator.py      # Markdown生成
│   │   └── sample_data_generator.py   # サンプルデータ生成
│   └── utils/                         # ユーティリティ
│       ├── file_utils.py              # ファイル操作
│       ├── validation_utils.py        # バリデーション
│       └── faker_utils.py             # テストデータ生成
├── table_generator/                   # テーブル生成ツール
│   ├── __main__.py                    # メインエントリーポイント
│   └── ...                           # 個別実装
├── database_consistency_checker/      # 整合性チェックツール
│   ├── __main__.py                    # メインエントリーポイント
│   └── ...                           # 個別実装
├── tests/                             # テストスイート
│   ├── test_table_generator.py        # テーブル生成テスト
│   ├── test_consistency_checker.py    # 整合性チェックテスト
│   └── fixtures/                      # テストデータ
└── docs/                              # ドキュメント
    ├── table_generator_guide.md       # テーブル生成ツールガイド
    ├── consistency_checker_guide.md   # 整合性チェックツールガイド
    └── development_guide.md           # 開発者ガイド
```

## 主要機能

### 1. テーブル生成ツール（table_generator）

YAML詳細定義からテーブル定義書・DDL・サンプルデータを自動生成します。

#### 主要機能
- **YAML詳細定義解析**: テーブル構造・制約・インデックス定義の読み込み
- **DDL自動生成**: PostgreSQL対応のCREATE TABLE文生成
- **Markdown定義書生成**: 人間が読みやすいテーブル定義書作成
- **サンプルデータ生成**: 業務に即したテストデータ作成
- **マルチテナント対応**: 全テーブルでtenant_id分離実装

#### 使用方法
```bash
# 全テーブル生成
cd ~/skill-report-web/docs/design/database/tools
python3 -m table_generator

# 個別テーブル生成
python3 -m table_generator --table MST_Employee

# 複数テーブル生成
python3 -m table_generator --table MST_Employee,MST_Department,MST_Position

# 詳細ログ出力
python3 -m table_generator --verbose

# ドライラン（実際にはファイル作成しない）
python3 -m table_generator --dry-run
```

### 2. データベース整合性チェックツール（database_consistency_checker）

データベース設計の整合性を多角的にチェックし、品質を保証します。

#### 主要機能
- **テーブル存在整合性**: YAML・DDL・Markdownファイル間の整合性確認
- **カラム定義整合性**: データ型・制約・NULL許可の一致確認
- **外部キー整合性**: 参照関係の妥当性チェック
- **データ型整合性**: YAML↔DDL間のデータ型完全一致確認
- **命名規則チェック**: テーブル・カラム命名規則の準拠確認
- **孤立ファイル検出**: 未使用・重複ファイルの特定

#### 使用方法
```bash
# 全体整合性チェック
cd ~/skill-report-web/docs/design/database/tools
python3 -m database_consistency_checker

# 個別テーブルチェック
python3 -m database_consistency_checker --tables MST_Employee,MST_Department

# 特定チェックのみ実行
python3 -m database_consistency_checker --checks table_existence,column_consistency

# 詳細ログ出力
python3 -m database_consistency_checker --verbose

# 結果をファイル出力
python3 -m database_consistency_checker --output-file consistency_report.md --output-format markdown
```

## 設定管理

### 統合設定（shared/core/config.py）

両ツールの設定を統合管理し、一貫した動作を保証します。

#### 主要設定項目
```python
# 基本設定
base_dir: プロジェクトルートディレクトリ
encoding: ファイルエンコーディング（utf-8）
log_level: ログレベル（INFO/DEBUG/WARNING/ERROR）

# ディレクトリ設定
table_details_dir: YAML詳細定義ディレクトリ
ddl_dir: DDLファイル出力ディレクトリ
tables_dir: テーブル定義書出力ディレクトリ
data_dir: サンプルデータ出力ディレクトリ

# テーブル生成設定
default_sample_count: デフォルトサンプルデータ件数（10件）
faker_locale: テストデータ生成ロケール（ja_JP）
company_domain: 会社ドメイン（company.com）

# 整合性チェック設定
report_formats: レポート形式（CONSOLE, MARKDOWN, JSON）
check_types: 実行するチェック種別
auto_fix_enabled: 自動修正機能（false）
```

#### 環境変数による設定上書き
```bash
# ベースディレクトリ
export DB_TOOLS_BASE_DIR=/path/to/project

# ログレベル
export DB_TOOLS_LOG_LEVEL=DEBUG

# サンプルデータ件数
export DB_TOOLS_SAMPLE_COUNT=50

# バックアップ有効化
export DB_TOOLS_BACKUP_ENABLED=true

# Fakerロケール
export TABLE_GEN_FAKER_LOCALE=ja_JP

# 会社ドメイン
export TABLE_GEN_COMPANY_DOMAIN=example.com
```

## 開発フロー

### 新規テーブル追加時の標準フロー

```bash
# 1. 要求仕様ID確認・割当
# 要求仕様書で対応するIDを確認

# 2. YAML詳細定義作成
# table-details/{テーブル名}_details.yamlを作成

# 3. テーブル一覧.md更新
# 新規テーブルをテーブル一覧に追加

# 4. 自動生成実行
cd ~/skill-report-web/docs/design/database/tools
python3 -m table_generator --table NEW_TABLE --verbose

# 5. 個別整合性チェック
python3 -m database_consistency_checker --tables NEW_TABLE

# 6. 全体整合性確認
python3 -m database_consistency_checker --verbose

# 7. 設計レビュー実施
# 業務要件・非機能要件・マルチテナント対応の確認

# 8. Git コミット
cd ~/skill-report-web
git add .
git commit -m "🆕 feat: NEW_TABLEテーブル追加

要求仕様ID: XXX.X-XXX.X
- YAML詳細定義作成
- 自動生成ツールによる定義書・DDL・サンプルデータ生成
- 整合性チェック通過確認
- マルチテナント対応実装"
```

### 既存テーブル修正時の標準フロー

```bash
# 1. 影響範囲調査
# 修正対象テーブルの参照関係・依存関係を確認

# 2. YAML詳細定義修正
# table-details/{テーブル名}_details.yamlを更新

# 3. 該当テーブルのみ再生成
python3 -m table_generator --table MODIFIED_TABLE --verbose

# 4. 影響範囲チェック
python3 -m database_consistency_checker --checks foreign_key_consistency

# 5. 関連テーブルの整合性確認
python3 -m database_consistency_checker --tables MODIFIED_TABLE,RELATED_TABLE

# 6. 破壊的変更チェック
# 既存データ・既存機能への影響を確認

# 7. Git コミット
git add .
git commit -m "🔧 fix: MODIFIED_TABLEテーブル修正

要求仕様ID: XXX.X-XXX.X
- カラム追加/修正: {変更内容}
- 影響範囲: {関連テーブル・機能}
- 破壊的変更: なし/あり（詳細）
- 整合性チェック通過確認"
```

## 品質保証

### 自動チェック項目

#### 1. テーブル存在整合性チェック
- ✅ YAML詳細定義ファイルの存在確認
- ✅ DDLファイルの存在確認
- ✅ Markdownファイルの存在確認
- ✅ テーブル一覧.mdとの整合性確認

#### 2. カラム定義整合性チェック
- ✅ YAML ↔ DDL間のカラム定義一致確認
- ✅ データ型の完全一致・互換性チェック
- ✅ NULL制約の整合性確認
- ✅ デフォルト値の比較
- ✅ 主キー・外部キー制約の整合性

#### 3. 外部キー整合性チェック
- ✅ 参照先テーブルの存在確認
- ✅ 参照先カラムのデータ型一致確認
- ✅ CASCADE/RESTRICT設定の妥当性確認
- ✅ 循環参照の検出

#### 4. 命名規則チェック
- ✅ テーブル名プレフィックス準拠確認（MST_, TRN_, HIS_, SYS_, WRK_, IF_）
- ✅ カラム名命名規則準拠確認
- ✅ インデックス名命名規則準拠確認
- ✅ 制約名命名規則準拠確認

#### 5. マルチテナント対応チェック
- ✅ 全テーブルでのtenant_idカラム存在確認
- ✅ テナントIDを含む複合インデックス確認
- ✅ 外部キー制約でのテナント分離確認

### 品質指標・成功基準

#### 設計品質指標
- **整合性チェック通過率**: 100%維持（必須）
- **要求仕様ID対応率**: 100%（全テーブル・全カラム）
- **命名規則準拠率**: 100%（プレフィックス・命名規則）
- **ドキュメント自動生成率**: 95%以上
- **マルチテナント対応率**: 100%（全テーブル）

#### 開発効率指標
- **新規テーブル追加時間**: 30分以内（設計〜生成〜チェック完了）
- **既存テーブル修正時間**: 15分以内（修正〜チェック完了）
- **整合性チェック実行時間**: 5分以内（全テーブル）
- **エラー修正時間**: 問題発見から修正完了まで1時間以内
- **自動生成成功率**: 95%以上（エラーなしでの生成）

## テスト

### テスト実行

```bash
# 全テスト実行
cd ~/skill-report-web/docs/design/database/tools
python3 run_tests.py

# 個別テスト実行
python3 -m pytest tests/test_table_generator.py -v
python3 -m pytest tests/test_consistency_checker.py -v

# カバレッジ付きテスト実行
python3 -m pytest --cov=shared --cov=table_generator --cov=database_consistency_checker --cov-report=html
```

### テスト構成
- **ユニットテスト**: 各コンポーネントの個別機能テスト
- **統合テスト**: ツール間連携・ファイル入出力テスト
- **エンドツーエンドテスト**: 実際のワークフローテスト
- **パフォーマンステスト**: 大量データでの処理時間測定

## トラブルシューティング

### よくある問題と解決方法

#### 1. 整合性チェックエラー
```bash
# 問題: テーブル存在整合性エラー
❌ MST_Department: DDLファイルが存在しません

# 解決方法
# 1. エラー詳細確認
python3 -m database_consistency_checker --verbose --tables MST_Department

# 2. 個別ファイル確認
ls -la table-details/MST_Department_details.yaml
ls -la ddl/MST_Department.sql
ls -la tables/テーブル定義書_MST_Department_*.md

# 3. 再生成実行
python3 -m table_generator --table MST_Department --verbose

# 4. 再チェック
python3 -m database_consistency_checker --tables MST_Department
```

#### 2. DDL生成エラー
```bash
# 問題: YAML構文エラー
❌ YAML解析エラー: mapping values are not allowed here

# 解決方法
# 1. YAML構文チェック
python3 -c "import yaml; yaml.safe_load(open('table-details/MST_Employee_details.yaml'))"

# 2. インデント・構文確認
# - インデントはスペース2文字で統一
# - コロン後にスペース必須
# - 文字列は引用符で囲む

# 3. 再生成実行
python3 -m table_generator --table MST_Employee --verbose
```

#### 3. パフォーマンス問題
```bash
# 問題: 処理時間が長い
⚠️ 整合性チェック実行時間: 10分 > 目標値 5分

# 解決方法
# 1. 並列処理有効化
export DB_TOOLS_PARALLEL_PROCESSING=true
export DB_TOOLS_MAX_WORKERS=8

# 2. キャッシュ有効化
export DB_TOOLS_CACHE_ENABLED=true

# 3. 個別テーブルでのテスト
python3 -m database_consistency_checker --tables MST_Employee
```

## 定期メンテナンス

### 月次作業
```bash
# 1. 全体整合性チェック実行
python3 -m database_consistency_checker --verbose --output-file monthly_check.log

# 2. 新規追加テーブルの品質確認
# 要求仕様IDとの対応確認
# 命名規則準拠確認
# マルチテナント対応確認

# 3. パフォーマンス監視
# 想定データ量との乖離チェック
# 応答時間の監視結果確認
# スロークエリの分析
```

### 四半期作業
```bash
# 1. 孤立ファイル・重複ファイルのクリーンアップ
python3 -m database_consistency_checker --checks orphaned_files
# 検出されたファイルの手動確認・削除

# 2. パフォーマンス要件の見直し
# 応答時間・データ量の再評価
# インデックス設計の最適化

# 3. セキュリティ監査
# 個人情報・機密情報含有テーブルの棚卸
# アクセス権限の見直し
```

## 関連ドキュメント

### 内部ドキュメント
- **テーブル一覧**: `docs/design/database/テーブル一覧.md`
- **エンティティ関連図**: `docs/design/database/エンティティ関連図.md`
- **データベース設計ガイドライン**: `.clinerules/08-database-design-guidelines.md`

### 外部参照
- **PostgreSQL公式ドキュメント**: https://www.postgresql.org/docs/
- **Prisma公式ドキュメント**: https://www.prisma.io/docs/
- **マルチテナント設計パターン**: `.clinerules/06-multitenant-development.md`

## 開発者向け情報

### 開発環境セットアップ
```bash
# 1. 仮想環境作成
cd ~/skill-report-web/docs/design/database/tools
python3 -m venv venv
source venv/bin/activate

# 2. 依存関係インストール
pip install -r requirements.txt

# 3. 開発用依存関係インストール
pip install -r requirements-dev.txt

# 4. テスト実行
python run_tests.py
```

### 新機能追加ガイドライン
1. **共通ライブラリ優先**: 新機能は可能な限り共通ライブラリ（shared/）に実装
2. **テスト駆動開発**: 新機能追加時は必ずテストを先に作成
3. **設定管理統合**: 新しい設定項目は統合設定（config.py）に追加
4. **ドキュメント更新**: 機能追加時は本READMEと関連ドキュメントを更新

### コントリビューション
- **コーディング規約**: `.clinerules/02-coding-standards.md`に準拠
- **Git ワークフロー**: `.clinerules/05-git-workflow.md`に準拠
- **要求仕様ID**: 全実装に要求仕様IDを明記
- **レビュープロセス**: Pull Request必須、コードレビュー実施

---

**実装日**: 2025-06-10  
**実装者**: AI駆動開発チーム  
**要求仕様ID**: PLT.1-WEB.1, TNT.1-MGMT  
**バージョン**: 2.0.0（共通ライブラリ統合版）
