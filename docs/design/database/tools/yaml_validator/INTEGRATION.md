# YAML検証ツール統合ガイド

このドキュメントでは、YAML検証ツールを既存のデータベース整合性チェックシステムに統合する方法について説明します。

## 概要

YAML検証ツール（`validate_yaml_format.py`）は、テーブル詳細YAML定義ファイルの必須セクション（`revision_history`, `overview`, `notes`, `business_rules`）の存在と内容を検証するツールです。このツールを既存のデータベース整合性チェックシステムに統合することで、テーブル定義の品質を自動的に検証することができます。

## 統合アーキテクチャ

```
database_consistency_checker/
├── __main__.py                    # メインエントリーポイント
├── yaml_format_check.py           # YAML検証モジュール（統合版）
├── yaml_format_check_integration.py # 統合インターフェース
└── [その他の既存チェックモジュール]

yaml_validator/
├── validate_yaml_format.py        # スタンドアロン版YAML検証ツール
├── install_git_hook.sh           # Git pre-commitフック
└── README_REQUIRED_SECTIONS.md   # 必須セクションガイド
```

## 統合方法

### 1. データベース整合性チェッカーとの統合

#### 1.1 統合版YAML検証モジュール

`database_consistency_checker/yaml_format_check.py`を以下の内容で更新します：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
データベース整合性チェッカー - YAML形式検証モジュール

テーブル詳細YAML定義ファイルの必須セクション（revision_history, overview, notes, business_rules）の
存在と内容を検証するモジュールです。
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from colorama import Fore, Style, init

# colorama初期化
init(autoreset=True)

# 基本パス設定
BASE_DIR = Path(__file__).parent.parent
YAML_VALIDATOR_DIR = BASE_DIR / "yaml_validator"
TABLE_DETAILS_DIR = BASE_DIR / "table-details"

# yaml_validatorモジュールのパスを追加
sys.path.insert(0, str(YAML_VALIDATOR_DIR))

try:
    from validate_yaml_format import (
        REQUIRED_SECTIONS, load_yaml_file, validate_required_sections
    )
except ImportError:
    print(f"{Fore.RED}エラー: yaml_validatorモジュールが見つかりません。{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}ヒント: {YAML_VALIDATOR_DIR}/validate_yaml_format.py が存在するか確認してください。{Style.RESET_ALL}")
    sys.exit(1)

def check_yaml_format_for_table(table_name: str, verbose: bool = False) -> Dict[str, Any]:
    """
    特定のテーブルのYAML形式を検証する
    
    Args:
        table_name (str): テーブル名
        verbose (bool): 詳細出力フラグ
        
    Returns:
        Dict[str, Any]: 検証結果
    """
    yaml_file = TABLE_DETAILS_DIR / f"{table_name}_details.yaml"
    
    if not yaml_file.exists():
        return {
            "table_name": table_name,
            "file_path": str(yaml_file),
            "valid": False,
            "level": "error",
            "message": f"YAMLファイルが存在しません: {yaml_file}",
            "details": {}
        }
    
    # YAMLファイルを読み込み
    yaml_data = load_yaml_file(str(yaml_file))
    if not yaml_data:
        return {
            "table_name": table_name,
            "file_path": str(yaml_file),
            "valid": False,
            "level": "error",
            "message": "YAMLファイルの読み込みに失敗しました",
            "details": {}
        }
    
    # 必須セクション検証
    is_valid, errors = validate_required_sections(yaml_data, table_name, verbose)
    
    # 詳細結果の構築
    details = {}
    for section in REQUIRED_SECTIONS.keys():
        if section in yaml_data:
            if section == "revision_history":
                details[section] = {
                    "exists": True,
                    "count": len(yaml_data[section]) if isinstance(yaml_data[section], list) else 0,
                    "valid": section not in [e.split("'")[1] for e in errors if "'" in e]
                }
            elif section == "overview":
                details[section] = {
                    "exists": True,
                    "length": len(str(yaml_data[section])),
                    "valid": section not in [e.split("'")[1] for e in errors if "'" in e]
                }
            elif section in ["notes", "business_rules"]:
                details[section] = {
                    "exists": True,
                    "count": len(yaml_data[section]) if isinstance(yaml_data[section], list) else 0,
                    "valid": section not in [e.split("'")[1] for e in errors if "'" in e]
                }
        else:
            details[section] = {
                "exists": False,
                "valid": False
            }
    
    return {
        "table_name": table_name,
        "file_path": str(yaml_file),
        "valid": is_valid,
        "level": "error" if not is_valid else "info",
        "message": "検証成功" if is_valid else f"検証失敗: {len(errors)}個のエラー",
        "errors": errors,
        "details": details
    }

def check_yaml_format(tables: Optional[List[str]] = None, verbose: bool = False) -> Dict[str, Any]:
    """
    YAML形式検証を実行する
    
    Args:
        tables (Optional[List[str]]): 検証対象のテーブル名リスト（Noneの場合は全テーブル）
        verbose (bool): 詳細出力フラグ
        
    Returns:
        Dict[str, Any]: 検証結果
    """
    if verbose:
        print(f"{Fore.CYAN}=== YAML形式検証開始 ==={Style.RESET_ALL}")
    
    # 検証対象テーブルの決定
    if tables:
        target_tables = tables
    else:
        # 全テーブルを対象とする
        yaml_files = list(TABLE_DETAILS_DIR.glob("*_details.yaml"))
        target_tables = [
            f.stem.replace("_details", "") 
            for f in yaml_files 
            if f.stem != "MST_TEMPLATE_details"
        ]
    
    if verbose:
        print(f"{Fore.BLUE}検証対象テーブル: {len(target_tables)}個{Style.RESET_ALL}")
        for table in target_tables:
            print(f"  - {table}")
    
    # 各テーブルの検証実行
    results = []
    valid_count = 0
    error_count = 0
    
    for table_name in target_tables:
        if verbose:
            print(f"\n{Fore.BLUE}テーブル {table_name} の検証中...{Style.RESET_ALL}")
        
        result = check_yaml_format_for_table(table_name, verbose)
        results.append(result)
        
        if result["valid"]:
            valid_count += 1
            if verbose:
                print(f"{Fore.GREEN}✓ {table_name}: 検証成功{Style.RESET_ALL}")
        else:
            error_count += 1
            if verbose:
                print(f"{Fore.RED}❌ {table_name}: {result['message']}{Style.RESET_ALL}")
                for error in result.get("errors", []):
                    print(f"{Fore.RED}   - {error}{Style.RESET_ALL}")
    
    # 全体結果の判定
    all_valid = error_count == 0
    
    if verbose:
        print(f"\n{Fore.CYAN}=== YAML形式検証結果 ==={Style.RESET_ALL}")
        print(f"総テーブル数: {len(results)}")
        print(f"検証成功: {valid_count}")
        print(f"検証失敗: {error_count}")
        
        if error_count > 0:
            print(f"\n{Fore.RED}検証失敗テーブル:{Style.RESET_ALL}")
            for result in results:
                if not result["valid"]:
                    print(f"  {Fore.RED}❌ {result['table_name']}{Style.RESET_ALL}")
    
    return {
        "check_name": "yaml_format_check",
        "description": "テーブル詳細YAML定義ファイルの必須セクション検証",
        "valid": all_valid,
        "level": "error" if error_count > 0 else "info",
        "summary": {
            "total": len(results),
            "valid": valid_count,
            "invalid": error_count
        },
        "results": results
    }

def main():
    """メイン関数（スタンドアロン実行用）"""
    import argparse
    
    parser = argparse.ArgumentParser(description='YAML形式検証（データベース整合性チェッカー統合版）')
    parser.add_argument('--tables', help='カンマ区切りのテーブル名リスト')
    parser.add_argument('--verbose', action='store_true', help='詳細なログを出力')
    args = parser.parse_args()
    
    tables = args.tables.split(',') if args.tables else None
    result = check_yaml_format(tables, args.verbose)
    
    return 0 if result['valid'] else 1

if __name__ == '__main__':
    sys.exit(main())
```

#### 1.2 統合インターフェースモジュール

`database_consistency_checker/yaml_format_check_integration.py`を以下の内容で作成します：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
YAML形式検証統合インターフェース

データベース整合性チェッカーのメインシステムとYAML検証モジュールを
統合するためのインターフェースモジュールです。
"""

from typing import Dict, List, Any, Optional
from .yaml_format_check import check_yaml_format

def run_yaml_format_check(base_dir, tables: Optional[List[str]] = None, verbose: bool = False) -> Dict[str, Any]:
    """
    YAML形式検証チェックを実行する
    
    Args:
        base_dir: 基準ディレクトリ（互換性のため）
        tables (Optional[List[str]]): 検証対象のテーブル名リスト
        verbose (bool): 詳細出力フラグ
        
    Returns:
        Dict[str, Any]: 検証結果
    """
    return check_yaml_format(tables, verbose)

# エイリアス（既存コードとの互換性のため）
yaml_format_check = run_yaml_format_check
```

#### 1.3 メインモジュールへの統合

`database_consistency_checker/__main__.py`に以下の変更を加えます：

```python
# 既存のインポート文に追加
from .yaml_format_check_integration import run_yaml_format_check

# AVAILABLE_CHECKSに追加
AVAILABLE_CHECKS = {
    # 既存のチェック
    "table_existence": "テーブル存在整合性チェック",
    "column_definition": "カラム定義整合性チェック", 
    "foreign_key_consistency": "外部キー整合性チェック",
    # 新規追加
    "yaml_format": "YAML形式検証チェック"
}

# CHECK_FUNCTIONSに追加
CHECK_FUNCTIONS = {
    # 既存の関数
    "table_existence": run_table_existence_check,
    "column_definition": run_column_definition_check,
    "foreign_key_consistency": run_foreign_key_consistency_check,
    # 新規追加
    "yaml_format": run_yaml_format_check
}

# DEFAULT_CHECKSに追加（オプション）
DEFAULT_CHECKS = [
    "table_existence",
    "column_definition", 
    "foreign_key_consistency",
    "yaml_format"  # デフォルトで実行する場合
]
```

### 2. Git pre-commitフックとの統合

#### 2.1 統合版pre-commitフック

`.git/hooks/pre-commit`ファイルを以下の内容で作成します：

```bash
#!/bin/bash

# YAML検証ツール統合版 Git pre-commitフック

# プロジェクトルートディレクトリを取得
PROJECT_ROOT=$(git rev-parse --show-toplevel)
YAML_VALIDATOR_DIR="$PROJECT_ROOT/docs/design/database/tools/yaml_validator"
DB_CHECKER_DIR="$PROJECT_ROOT/docs/design/database/tools"

# 変更されたYAMLファイルを取得
CHANGED_YAML_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep "table-details/.*_details\.yaml$")

if [ -z "$CHANGED_YAML_FILES" ]; then
    echo "テーブル詳細YAMLファイルの変更はありません。"
    exit 0
fi

echo "🔍 変更されたテーブル詳細YAMLファイルの検証を実行中..."

# 変更されたテーブル名を抽出
CHANGED_TABLES=""
for file in $CHANGED_YAML_FILES; do
    table_name=$(basename "$file" "_details.yaml")
    if [ -z "$CHANGED_TABLES" ]; then
        CHANGED_TABLES="$table_name"
    else
        CHANGED_TABLES="$CHANGED_TABLES,$table_name"
    fi
done

echo "検証対象テーブル: $CHANGED_TABLES"

# データベース整合性チェッカー経由でYAML検証を実行
cd "$DB_CHECKER_DIR"
python -m database_consistency_checker --checks yaml_format --tables "$CHANGED_TABLES" --verbose

YAML_CHECK_RESULT=$?

if [ $YAML_CHECK_RESULT -ne 0 ]; then
    echo ""
    echo "❌ YAML形式検証に失敗しました。"
    echo ""
    echo "修正方法:"
    echo "1. エラーメッセージを確認し、必須セクションを追加・修正してください"
    echo "2. 詳細なガイドラインは以下を参照してください:"
    echo "   docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md"
    echo ""
    echo "検証をスキップしてコミットする場合（緊急時のみ）:"
    echo "   git commit --no-verify"
    echo ""
    exit 1
fi

echo "✅ YAML形式検証に成功しました。"
exit 0
```

#### 2.2 インストールスクリプトの更新

`yaml_validator/install_git_hook.sh`を以下の内容で更新します：

```bash
#!/bin/bash

# YAML検証ツール統合版 Git pre-commitフックインストールスクリプト

set -e

# プロジェクトルートディレクトリを取得
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
PRE_COMMIT_HOOK="$HOOKS_DIR/pre-commit"

echo "🔧 YAML検証ツール統合版 Git pre-commitフックをインストール中..."

# .git/hooksディレクトリの存在確認
if [ ! -d "$HOOKS_DIR" ]; then
    echo "❌ エラー: .git/hooksディレクトリが見つかりません。"
    echo "   Gitリポジトリのルートディレクトリで実行してください。"
    exit 1
fi

# 既存のpre-commitフックのバックアップ
if [ -f "$PRE_COMMIT_HOOK" ]; then
    echo "📋 既存のpre-commitフックをバックアップ中..."
    cp "$PRE_COMMIT_HOOK" "$PRE_COMMIT_HOOK.backup.$(date +%Y%m%d_%H%M%S)"
fi

# 統合版pre-commitフックの作成
cat > "$PRE_COMMIT_HOOK" << 'EOF'
#!/bin/bash

# YAML検証ツール統合版 Git pre-commitフック

# プロジェクトルートディレクトリを取得
PROJECT_ROOT=$(git rev-parse --show-toplevel)
DB_CHECKER_DIR="$PROJECT_ROOT/docs/design/database/tools"

# 変更されたYAMLファイルを取得
CHANGED_YAML_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep "table-details/.*_details\.yaml$")

if [ -z "$CHANGED_YAML_FILES" ]; then
    exit 0
fi

echo "🔍 変更されたテーブル詳細YAMLファイルの検証を実行中..."

# 変更されたテーブル名を抽出
CHANGED_TABLES=""
for file in $CHANGED_YAML_FILES; do
    table_name=$(basename "$file" "_details.yaml")
    if [ -z "$CHANGED_TABLES" ]; then
        CHANGED_TABLES="$table_name"
    else
        CHANGED_TABLES="$CHANGED_TABLES,$table_name"
    fi
done

echo "検証対象テーブル: $CHANGED_TABLES"

# データベース整合性チェッカー経由でYAML検証を実行
cd "$DB_CHECKER_DIR"
python -m database_consistency_checker --checks yaml_format --tables "$CHANGED_TABLES"

YAML_CHECK_RESULT=$?

if [ $YAML_CHECK_RESULT -ne 0 ]; then
    echo ""
    echo "❌ YAML形式検証に失敗しました。"
    echo ""
    echo "修正方法:"
    echo "1. エラーメッセージを確認し、必須セクションを追加・修正してください"
    echo "2. 詳細なガイドラインは以下を参照してください:"
    echo "   docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md"
    echo ""
    echo "検証をスキップしてコミットする場合（緊急時のみ）:"
    echo "   git commit --no-verify"
    echo ""
    exit 1
fi

echo "✅ YAML形式検証に成功しました。"
exit 0
EOF

# 実行権限を付与
chmod +x "$PRE_COMMIT_HOOK"

echo "✅ YAML検証ツール統合版 Git pre-commitフックのインストールが完了しました。"
echo ""
echo "📝 使用方法:"
echo "   - テーブル詳細YAMLファイルを編集してコミットすると、自動的に検証が実行されます"
echo "   - 検証をスキップする場合: git commit --no-verify"
echo ""
echo "🔧 手動検証コマンド:"
echo "   cd docs/design/database/tools"
echo "   python -m database_consistency_checker --checks yaml_format"
echo ""
```

### 3. CI/CD統合

#### 3.1 GitHub Actions統合

`.github/workflows/database-validation.yml`を以下の内容で作成します：

```yaml
name: Database Validation

on:
  push:
    branches: [ main, develop ]
    paths:
      - 'docs/design/database/table-details/**'
      - 'docs/design/database/tools/**'
  pull_request:
    branches: [ main, develop ]
    paths:
      - 'docs/design/database/table-details/**'
      - 'docs/design/database/tools/**'

jobs:
  yaml-validation:
    runs-on: ubuntu-latest
    name: YAML形式検証
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pyyaml colorama
          
      - name: Run YAML format validation
        run: |
          cd docs/design/database/tools
          python -m database_consistency_checker --checks yaml_format --verbose
          
      - name: Run full database consistency check
        run: |
          cd docs/design/database/tools
          python -m database_consistency_checker --verbose
```

## 使用例

### 1. 開発時の検証

```bash
# 特定のテーブルのYAML検証
cd docs/design/database/tools
python -m database_consistency_checker --checks yaml_format --tables MST_Employee

# 全テーブルのYAML検証
python -m database_consistency_checker --checks yaml_format

# 詳細出力付きで検証
python -m database_consistency_checker --checks yaml_format --verbose
```

### 2. 全体整合性チェックの一部として実行

```bash
# 全チェック実行（YAML検証も含む）
cd docs/design/database/tools
python -m database_consistency_checker

# 特定のチェックのみ実行
python -m database_consistency_checker --checks yaml_format,table_existence

# 特定のテーブルのみ全チェック実行
python -m database_consistency_checker --tables MST_Employee,MST_Department
```

### 3. スタンドアロン実行

```bash
# yaml_validatorツールを直接実行
python docs/design/database/tools/yaml_validator/validate_yaml_format.py --table MST_Employee --verbose

# 統合版モジュールを直接実行
python docs/design/database/tools/database_consistency_checker/yaml_format_check.py --tables MST_Employee --verbose
```

## トラブルシューティング

### 1. インポートエラーの解決

```bash
# 依存パッケージのインストール
pip install pyyaml colorama

# Pythonパスの確認
export PYTHONPATH="${PYTHONPATH}:/path/to/project/docs/design/database/tools"
```

### 2. 検証エラーの修正

検証エラーが発生した場合の対応手順：

1. **エラーメッセージの確認**: 具体的にどのセクションでエラーが発生しているかを確認
2. **必須セクションの追加**: 不足しているセクションを追加
3. **内容の充実**: 最低要件を満たすように内容を追加・修正
4. **再検証**: 修正後に再度検証を実行

### 3. Git pre-commitフックの問題

```bash
# フックの再インストール
docs/design/database/tools/yaml_validator/install_git_hook.sh

# フックの手動確認
.git/hooks/pre-commit

# フックのスキップ（緊急時のみ）
git commit --no-verify -m "緊急修正"
```

## まとめ

この統合ガイドにより、YAML検証ツールがデータベース整合性チェックシステムの一部として統合され、以下の利点が得られます：

1. **統一されたインターフェース**: 単一のコマンドで全ての整合性チェックを実行
2. **自動化された品質保証**: Git pre-commitフックとCI/CDによる自動検証
3. **一貫した出力形式**: 他のチェック結果と統一された形式での結果出力
4. **柔軟な実行オプション**: 特定のテーブルやチェック項目のみの実行が可能

必須セクション（`revision_history`, `overview`, `notes`, `business_rules`）の適切な記述により、テーブル定義の品質と保守性が大幅に向上します。
