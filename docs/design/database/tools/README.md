# テーブル定義書作成ツール

このディレクトリには、テーブル定義書作成に関するツールが統合されています。

## ツール構成

### table_generator/
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

## 使用方法

### 基本的な使用
```bash
cd /home/kurosawa/skill-report-web/docs/design/database/tools
python3 -m table_generator
```

### オプション付き実行
```bash
# 個別テーブル生成
python3 -m table_generator --table MST_Employee

# 複数テーブル生成
python3 -m table_generator --table MST_Role,MST_Permission

# ドライラン
python3 -m table_generator --dry-run

# 詳細ログ
python3 -m table_generator --verbose

# カラー出力無効
python3 -m table_generator --no-color
```

### 開発・カスタマイズ
**table_generator/** パッケージを直接利用：
```python
from table_generator.generators.table_definition_generator import TableDefinitionGenerator
from table_generator.core.logger import Logger

logger = Logger()
generator = TableDefinitionGenerator(logger=logger)
generator.generate_files()
```

## 関連ファイル

- `../entity_relationships.yaml` - エンティティ関連定義
- `../テーブル一覧.md` - テーブル一覧
- `../table-details/*.yaml` - 各テーブルの詳細定義
- `../tables/` - 生成されたテーブル定義書
- `../ddl/` - 生成されたDDLファイル

## 更新履歴

- 2025-06-04: 冗長ファイル削除・table_generatorパッケージに統一
- 2025-06-04: __main__.py追加・モジュール実行対応
- 2025-06-04: ツール統合・重複解消
