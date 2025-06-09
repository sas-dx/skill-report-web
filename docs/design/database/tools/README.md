# データベース設計ツール統合パッケージ

年間スキル報告書WEB化PJTのデータベース設計・管理を効率化する統合ツールセットです。

## 🎯 概要

このツールパッケージは、YAML詳細定義からテーブル定義書・DDL・サンプルデータを自動生成し、データベース設計の整合性を保証する統合システムです。

### 主要機能

- **📝 YAML詳細定義**: 構造化されたテーブル定義の作成・管理
- **🔄 自動生成**: Markdown定義書・DDL・サンプルデータの一括生成
- **✅ 整合性チェック**: 全ファイル間の整合性検証
- **🔍 品質保証**: 命名規則・データ型・外部キー制約の検証
- **📊 レポート生成**: 整合性チェック結果の詳細レポート

## 🏗️ アーキテクチャ

```
docs/design/database/tools/
├── 📁 shared/                    # 共通コンポーネント
│   ├── adapters/                 # アダプター層
│   ├── core/                     # コアロジック
│   └── generators/               # 生成エンジン
├── 📁 table_generator/           # テーブル生成ツール
├── 📁 consistency_checker/       # 整合性チェックツール
├── 📁 tests/                     # テストスイート
├── 📁 configs/                   # 設定ファイル
└── 📄 run_tests.py              # 統合テストランナー
```

## 🚀 クイックスタート

### 1. 環境セットアップ

```bash
# 仮想環境の作成・有効化
cd docs/design/database/tools
python3 -m venv test_env
source test_env/bin/activate

# 依存関係のインストール
pip install faker psutil pyyaml
```

### 2. 基本的な使用方法

#### テーブル生成
```bash
# 単一テーブル生成
python3 -m table_generator --table MST_Employee --verbose

# 複数テーブル生成
python3 -m table_generator --table MST_Employee,MST_Department

# カテゴリ別生成
python3 -m table_generator --table MST_* --verbose
```

#### 整合性チェック
```bash
# 全体整合性チェック
python3 database_consistency_checker/run_check.py --verbose

# 特定テーブルのみチェック
python3 database_consistency_checker/run_check.py --tables MST_Employee,MST_Department

# 特定のチェックのみ実行
python3 database_consistency_checker/run_check.py --checks table_existence,column_consistency
```

#### 統合テスト実行
```bash
# 全テスト実行
python3 run_tests.py --verbose

# 特定テストのみ実行
python3 run_tests.py --unit-only
python3 run_tests.py --integration-only
```

## 📋 YAML詳細定義の作成

### 基本構造

```yaml
# table-details/{テーブル名}_details.yaml
table_name: "MST_Employee"
logical_name: "社員基本情報"
category: "マスタ系"
priority: "最高"
requirement_id: "PRO.1-BASE.1"

columns:
  - name: "id"
    type: "VARCHAR(50)"
    nullable: false
    primary_key: true
    comment: "プライマリキー（UUID）"
    requirement_id: "PLT.1-WEB.1"
  
  - name: "tenant_id"
    type: "VARCHAR(50)"
    nullable: false
    comment: "マルチテナント識別子"
    requirement_id: "TNT.1-MGMT.1"

indexes:
  - name: "idx_employee_tenant"
    columns: ["tenant_id"]
    unique: false
    comment: "テナント別検索用インデックス"

foreign_keys:
  - name: "fk_employee_tenant"
    columns: ["tenant_id"]
    references:
      table: "MST_Tenant"
      columns: ["id"]
    on_update: "CASCADE"
    on_delete: "RESTRICT"
```

### テーブル命名規則

- **MST_**: マスタ系テーブル（ユーザー、ロール、部署、スキル階層等）
- **TRN_**: トランザクション系テーブル（スキル情報、目標進捗、案件実績等）
- **HIS_**: 履歴系テーブル（監査ログ、操作履歴等）
- **SYS_**: システム系テーブル（検索インデックス、システムログ、トークン等）
- **WRK_**: ワーク系テーブル（一括登録ジョブログ、バッチワーク等）
- **IF_**: インターフェイス系テーブル（外部連携・インポート/エクスポート用）

## 🔧 詳細機能

### テーブル生成ツール（table_generator）

#### 主要機能
- YAML詳細定義の解析・検証
- Markdown定義書の自動生成
- PostgreSQL DDLの生成
- サンプルデータの生成
- マルチテナント対応の自動実装

#### 生成される出力ファイル
- **Markdown定義書**: `tables/テーブル定義書_{テーブル名}_{論理名}.md`
- **DDLファイル**: `ddl/{テーブル名}.sql`
- **サンプルデータ**: `data/{テーブル名}_sample_data.sql`

#### 使用例
```bash
# 詳細ログ付きで生成
python3 -m table_generator --table MST_Employee --verbose

# 出力ディレクトリ指定
python3 -m table_generator --table MST_Employee --output-dir custom_output

# 特定フォーマットのみ生成
python3 -m table_generator --table MST_Employee --ddl-only
```

### 整合性チェックツール（consistency_checker）

#### チェック項目
- ✅ **テーブル存在整合性**: 全ソース間でのテーブル定義一致
- ✅ **カラム定義整合性**: YAML ↔ DDL ↔ 定義書の整合性
- ✅ **外部キー整合性**: 参照関係の妥当性チェック
- ✅ **データ型整合性**: DDLとYAML間のデータ型完全一致・互換性チェック
- ✅ **孤立ファイル検出**: 未使用・重複ファイルの特定
- ✅ **命名規則チェック**: プレフィックス・命名規則の準拠確認

#### 使用例
```bash
# 全体チェック（推奨）
python3 database_consistency_checker/run_check.py --verbose

# レポート出力
python3 database_consistency_checker/run_check.py --verbose --output-format markdown --output-file report.md

# 特定チェックのみ
python3 database_consistency_checker/run_check.py --checks table_existence,foreign_key_consistency

# 修正提案付き
python3 database_consistency_checker/run_check.py --suggest-fixes
```

## 📊 品質保証・テスト

### テスト構成
- **ユニットテスト**: 個別コンポーネントの動作検証（72テスト）
- **統合テスト**: ツール間連携の検証（4テスト）
- **パフォーマンステスト**: 大量データ処理の性能検証

### テスト実行
```bash
# 全テスト実行
python3 run_tests.py --verbose

# 特定テストカテゴリのみ
python3 run_tests.py --unit-only
python3 run_tests.py --integration-only
python3 run_tests.py --performance-only

# テスト結果の詳細出力
python3 run_tests.py --verbose --output-json
```

### 品質指標
- **整合性チェック通過率**: 100%維持（必須）
- **要求仕様ID対応率**: 100%（全テーブル・全カラム）
- **命名規則準拠率**: 100%（プレフィックス・命名規則）
- **テストカバレッジ**: 80%以上
- **マルチテナント対応率**: 100%（全テーブル）

## 🔄 開発ワークフロー

### 新規テーブル追加時の標準フロー

```bash
# 1. 要求仕様ID確認・割当
# 要求仕様書で対応するIDを確認

# 2. YAML詳細定義作成
# table-details/{テーブル名}_details.yamlを作成

# 3. テーブル一覧.md更新
# 新規テーブルをテーブル一覧に追加

# 4. 自動生成実行
python3 -m table_generator --table NEW_TABLE --verbose

# 5. 個別整合性チェック
python3 database_consistency_checker/run_check.py --tables NEW_TABLE

# 6. 全体整合性確認
python3 database_consistency_checker/run_check.py --verbose

# 7. Git コミット
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
python3 database_consistency_checker/run_check.py --checks foreign_key_consistency

# 5. 関連テーブルの整合性確認
python3 database_consistency_checker/run_check.py --tables MODIFIED_TABLE,RELATED_TABLE

# 6. Git コミット
git add .
git commit -m "🔧 fix: MODIFIED_TABLEテーブル修正

要求仕様ID: XXX.X-XXX.X
- カラム追加/修正: {変更内容}
- 影響範囲: {関連テーブル・機能}
- 破壊的変更: なし/あり（詳細）
- 整合性チェック通過確認"
```

## 🛠️ 設定・カスタマイズ

### 設定ファイル

#### configs/database_tools_config.yaml
```yaml
# データベース設定
database:
  type: "postgresql"
  charset: "UTF8"
  collation: "ja_JP.UTF-8"

# 生成設定
generation:
  include_drop_statements: true
  include_comments: true
  include_sample_data: true
  sample_data_rows: 10

# 検証設定
validation:
  enforce_naming_convention: true
  require_tenant_id: true
  require_primary_key: true
  max_table_name_length: 63
  max_column_name_length: 63

# パフォーマンス設定
performance:
  batch_size: 100
  max_concurrent_operations: 4
  timeout_seconds: 30
```

### 環境変数
```bash
# データベース接続
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=skill_report
export DB_USER=postgres
export DB_PASSWORD=password

# ツール設定
export TOOLS_BASE_DIR=/path/to/tools
export TOOLS_LOG_LEVEL=INFO
export TOOLS_OUTPUT_FORMAT=markdown
```

## 📈 パフォーマンス・スケーラビリティ

### パフォーマンス指標
- **新規テーブル追加時間**: 30分以内（設計〜生成〜チェック完了）
- **既存テーブル修正時間**: 15分以内（修正〜チェック完了）
- **整合性チェック実行時間**: 5分以内（全テーブル）
- **自動生成成功率**: 95%以上（エラーなしでの生成）

### 大量データ対応
- **バッチ処理**: 100テーブル単位での一括処理
- **並列処理**: 最大4並列での生成・チェック
- **メモリ最適化**: ストリーミング処理による省メモリ実装

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. 整合性チェックエラー
```bash
# 問題: テーブル存在整合性エラー
❌ MST_Department: DDLファイルが存在しません

# 解決方法
python run_check.py --verbose --tables MST_Department
python3 -m table_generator --table MST_Department --verbose
python run_check.py --tables MST_Department
```

#### 2. YAML構文エラー
```bash
# 問題: YAML解析エラー
❌ YAML解析エラー: mapping values are not allowed here

# 解決方法
python3 -c "import yaml; yaml.safe_load(open('table-details/MST_Employee_details.yaml'))"
# インデント・構文を修正後
python3 -m table_generator --table MST_Employee --verbose
```

#### 3. 外部キー制約エラー
```bash
# 問題: 外部キー制約違反
❌ 参照先テーブル 'MST_Department' が存在しません

# 解決方法
python3 -m table_generator --table MST_Department
python3 -m table_generator --table MST_Employee
python run_check.py --checks foreign_key_consistency
```

### 緊急時対応フロー
1. **問題発見** → 影響範囲特定
2. **根本原因分析** → ログ・エラーメッセージ確認
3. **応急処置** → サービス継続のための一時対応
4. **恒久対策** → YAML修正・再生成・整合性確認
5. **再発防止策** → チェック項目追加・手順見直し

## 📚 関連ドキュメント

### 内部ドキュメント
- **テーブル一覧**: `docs/design/database/テーブル一覧.md`
- **エンティティ関連図**: `docs/design/database/エンティティ関連図.md`
- **整合性チェックツール**: `consistency_checker/README.md`
- **テーブル生成ツール**: `table_generator/README.md`

### 設計ガイドライン
- **データベース設計ガイドライン**: `.clinerules/08-database-design-guidelines.md`
- **マルチテナント開発**: `.clinerules/06-multitenant-development.md`
- **バックエンド設計**: `.clinerules/04-backend-guidelines.md`

### 外部参照
- **PostgreSQL公式ドキュメント**: https://www.postgresql.org/docs/
- **Prisma公式ドキュメント**: https://www.prisma.io/docs/

## 🤝 コントリビューション

### 開発環境セットアップ
```bash
# リポジトリクローン
git clone <repository-url>
cd skill-report-web/docs/design/database/tools

# 仮想環境セットアップ
python3 -m venv dev_env
source dev_env/bin/activate
pip install -r requirements-dev.txt

# テスト実行
python3 run_tests.py --verbose
```

### コーディング規約
- **Python**: PEP 8準拠
- **YAML**: 2スペースインデント
- **コメント**: 日本語での詳細説明
- **ログ**: 構造化ログ（JSON形式）

### プルリクエスト
1. **機能ブランチ作成**: `feature/database-tool-enhancement`
2. **テスト実装**: 新機能に対応するテストケース追加
3. **ドキュメント更新**: README・コメントの更新
4. **整合性チェック**: 全テスト通過確認

## 📄 ライセンス

このプロジェクトは年間スキル報告書WEB化PJTの一部として開発されています。

---

## 🔄 更新履歴

### v1.2.0 (2025-06-10)
- ✨ データ型整合性チェック機能追加
- 🔧 パフォーマンステスト環境改善
- 📚 README.md包括的更新
- 🐛 孤立ファイル検出ロジック修正

### v1.1.0 (2025-06-06)
- ✨ 統合テストスイート実装
- 🔧 YAML解析エンジン強化
- 📊 レポート生成機能追加

### v1.0.0 (2025-06-01)
- 🎉 初回リリース
- ✨ テーブル生成・整合性チェック基本機能
- 📝 YAML詳細定義システム実装

---

**📞 サポート**: 技術的な質問や問題については、プロジェクトチームまでお問い合わせください。
