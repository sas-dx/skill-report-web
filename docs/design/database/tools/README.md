# テーブル定義書作成ツール

このディレクトリには、テーブル定義書作成に関するツールが統合されています。

## ツール構成

### 1. create_table_definitions.py
**単体完結版テーブル定義書生成スクリプト（v12.0）**

- **機能**: YAMLファイルからMarkdown形式のテーブル定義書とDDLを生成
- **特徴**: 
  - カラー出力対応
  - 詳細診断機能
  - エラーハンドリング強化
  - 単体ファイルで完結
- **使用方法**:
  ```bash
  cd /home/kurosawa/skill-report-web/docs/design/database/tools
  python3 create_table_definitions.py
  
  # 個別テーブル生成
  python3 create_table_definitions.py --table MST_Employee
  
  # ドライラン
  python3 create_table_definitions.py --dry-run
  ```

### 2. table_generator/
**モジュール化されたテーブル定義書作成パッケージ**

- **機能**: 拡張性を重視したパッケージ構造
- **特徴**:
  - 再利用可能なモジュール設計
  - 他のスクリプトから利用可能
  - カスタマイズ容易
- **構成**:
  ```
  table_generator/
  ├── core/           # コア機能
  │   ├── config.py   # 設定管理
  │   ├── logger.py   # ログ機能
  │   └── models.py   # データモデル
  ├── data/           # データ関連
  │   └── faker_utils.py  # テストデータ生成
  ├── generators/     # 生成機能
  │   └── common_columns.py  # 共通カラム生成
  └── utils/          # ユーティリティ
      ├── file_utils.py    # ファイル操作
      ├── sql_utils.py     # SQL関連
      └── yaml_loader.py   # YAML読み込み
  ```

## 推奨使用方法

### 日常的な使用
**create_table_definitions.py** を使用することを推奨します。
- 即座に利用可能
- 豊富な機能（カラー出力、診断機能）
- コマンドライン引数対応

### 開発・カスタマイズ
**table_generator/** パッケージを使用してください。
- 他のスクリプトから再利用
- 機能拡張・カスタマイズ
- モジュール単位での利用

## 関連ファイル

- `../entity_relationships.yaml` - エンティティ関連定義
- `../テーブル一覧.md` - テーブル一覧
- `../table-details/*.yaml` - 各テーブルの詳細定義
- `../tables/` - 生成されたテーブル定義書
- `../ddl/` - 生成されたDDLファイル

## 更新履歴

- 2025-06-04: ツール統合・重複解消
- 2025-06-01: create_table_definitions.py v12.0 完全統合版
