# YAML検証ツール統合ガイド

## 概要

このドキュメントは、YAML検証ツール（`yaml_validator`）とデータベース整合性チェッカー（`database_consistency_checker`）の統合について説明します。

## 統合アーキテクチャ

### 1. ツール構成
```
docs/design/database/tools/
├── yaml_validator/                    # YAML検証ツール（独立）
│   ├── validate_yaml_format.py       # メイン検証スクリプト
│   ├── install_git_hook.sh           # Git フック設定
│   ├── README.md                     # 使用方法
│   └── README_REQUIRED_SECTIONS.md   # 必須セクション詳細
├── database_consistency_checker/      # データベース整合性チェッカー
│   ├── __main__.py                   # メインエントリーポイント
│   ├── run_check.py                  # 実行スクリプト
│   ├── yaml_format_check.py          # YAML形式チェック（統合）
│   ├── yaml_format_check_integration.py # 統合ロジック
│   ├── required_sections_guide.md    # 必須セクションガイド
│   └── install_git_hook.sh           # Git フック設定（統合版）
└── shared/                           # 共通ユーティリティ
    └── generators/
        └── ddl_generator.py          # DDL生成ツール
```

### 2. 統合方式
- **独立実行**: `yaml_validator` は単独で実行可能
- **統合実行**: `database_consistency_checker` から YAML検証を呼び出し
- **共通基盤**: 検証ロジックは共通化、インターフェースのみ分離
- **Git フック統合**: 統合版のGit フックを推奨

## 使用方法

### 1. 推奨：統合実行（データベース整合性チェッカー経由）

#### 全体チェック（YAML検証含む）
```bash
cd docs/design/database/tools
python database_consistency_checker/run_check.py --verbose
```

#### YAML形式チェックのみ
```bash
python database_consistency_checker/run_check.py --checks yaml_format --verbose
```

#### 特定テーブルのYAML検証
```bash
python database_consistency_checker/run_check.py --tables MST_Employee --checks yaml_format --verbose
```

#### 必須セクションのみ検証
```bash
python database_consistency_checker/run_check.py --checks yaml_format --required-sections-only --verbose
```

#### Git フック設定（統合版）
```bash
cd docs/design/database/tools/database_consistency_checker
./install_git_hook.sh
```

### 2. 独立実行（YAML検証のみ）

#### 全テーブル検証
```bash
cd docs/design/database/tools/yaml_validator
python validate_yaml_format.py --all --verbose
```

#### 特定テーブル検証
```bash
python validate_yaml_format.py --table MST_Employee --verbose
```

#### 必須セクションのみ検証
```bash
python validate_yaml_format.py --check-required-only
```

## 検証項目

### 1. 必須セクション検証
以下の4つのセクションは**絶対省略禁止**：

| セクション | 目的 | 最低要件 | 重要度 |
|------------|------|----------|---------|
| `revision_history` | 変更履歴追跡・監査証跡 | 最低1エントリ必須 | 🔴 **必須** |
| `overview` | テーブル目的・設計意図明確化 | 最低50文字必須 | 🔴 **必須** |
| `notes` | 運用・保守・セキュリティ考慮点 | 最低3項目必須 | 🔴 **必須** |
| `business_rules` | 業務ルール・制約明文化 | 最低3項目必須 | 🔴 **必須** |

### 2. 構造検証
- YAML構文の正当性
- 必須フィールドの存在確認
- データ型の妥当性
- 外部キー参照の整合性

### 3. 命名規則検証
- テーブル名プレフィックス（MST_, TRN_, HIS_, SYS_, WRK_）
- カラム名の命名規則
- インデックス名の命名規則

### 4. 品質基準検証
- `overview`セクションの文字数（最低50文字）
- `notes`セクションの項目数（最低3項目）
- `business_rules`セクションの項目数（最低3項目）
- `revision_history`の形式と内容

## エラー処理・レポート

### 1. エラーレベル
- **CRITICAL**: 必須セクション不足等の致命的問題（コミット拒否）
- **ERROR**: 構文エラー、参照整合性エラー等の重要問題
- **WARNING**: 推奨事項違反、潜在的問題
- **INFO**: 情報提供、改善提案

### 2. 出力形式
- **コンソール**: リアルタイム進捗・結果表示
- **JSON**: 機械可読形式（CI/CD統合用）
- **Markdown**: 人間可読レポート形式

### 3. 統合レポート例
```json
{
  "summary": {
    "total_tables": 42,
    "passed": 38,
    "failed": 4,
    "warnings": 8,
    "critical_errors": 2
  },
  "results": {
    "MST_Employee": {
      "status": "PASSED",
      "checks": {
        "required_sections": "PASSED",
        "yaml_syntax": "PASSED",
        "naming_convention": "PASSED",
        "quality_standards": "PASSED"
      }
    },
    "MST_Department": {
      "status": "FAILED",
      "checks": {
        "required_sections": "CRITICAL",
        "yaml_syntax": "PASSED",
        "naming_convention": "WARNING",
        "quality_standards": "ERROR"
      },
      "errors": [
        {
          "level": "CRITICAL",
          "message": "Missing required section: business_rules",
          "section": "business_rules"
        },
        {
          "level": "ERROR", 
          "message": "overview section too short (25 chars, minimum 50 required)",
          "section": "overview"
        }
      ],
      "warnings": [
        {
          "level": "WARNING",
          "message": "Index name should follow convention: idx_department_name",
          "section": "indexes"
        }
      ]
    }
  }
}
```

## CI/CD統合

### 1. Git フック統合（推奨：統合版）
```bash
# 統合版 pre-commit フック設定
cd docs/design/database/tools/database_consistency_checker
./install_git_hook.sh

# 手動でのコミット前チェック
git add .
python run_check.py --checks yaml_format --verbose
git commit -m "feat: テーブル定義更新"
```

### 2. GitHub Actions統合例
```yaml
name: Database Schema Validation

on:
  push:
    paths:
      - 'docs/design/database/table-details/*.yaml'
  pull_request:
    paths:
      - 'docs/design/database/table-details/*.yaml'

jobs:
  validate-schema:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v3
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          cd docs/design/database/tools
          pip install pyyaml
      
      - name: Validate YAML format and database consistency
        run: |
          cd docs/design/database/tools
          python database_consistency_checker/run_check.py --checks yaml_format --verbose --output-format json --output-file validation_results.json
      
      - name: Upload validation results
        uses: actions/upload-artifact@v3
        with:
          name: validation-results
          path: docs/design/database/tools/validation_results.json
        if: always()
      
      - name: Fail on critical errors
        run: |
          cd docs/design/database/tools
          python -c "
          import json
          with open('validation_results.json') as f:
              results = json.load(f)
          critical_errors = sum(1 for r in results.get('results', {}).values() 
                               if any(e.get('level') == 'CRITICAL' for e in r.get('errors', [])))
          if critical_errors > 0:
              print(f'Critical errors found: {critical_errors}')
              exit(1)
          "
```

## 統合実装詳細

### 1. メインモジュール統合（`run_check.py`）

YAML検証チェックの統合:
```python
def _check_yaml_format(self, target_tables: List[str]) -> Dict[str, Any]:
    """YAML形式検証チェック（統合版）"""
    from .yaml_format_check_integration import run_yaml_format_check
    
    result = {
        'check_name': 'yaml_format',
        'description': 'YAML形式・必須セクション検証チェック',
        'status': 'PASS',
        'errors': [],
        'warnings': [],
        'details': [],
        'critical_errors': 0
    }
    
    try:
        yaml_result = run_yaml_format_check(
            base_dir=self.config.base_dir,
            tables=target_tables,
            verbose=self.verbose,
            check_required_only=getattr(self.config, 'required_sections_only', False)
        )
        
        # 結果の統合処理
        critical_count = 0
        for table_result in yaml_result.get('results', []):
            if not table_result.get('valid', True):
                # 必須セクション不足はCRITICALエラー
                if 'required section' in table_result.get('message', '').lower():
                    critical_count += 1
                    error_msg = f"CRITICAL: {table_result['table_name']}: {table_result['message']}"
                    result['errors'].append(error_msg)
                else:
                    error_msg = f"ERROR: {table_result['table_name']}: {table_result['message']}"
                    result['errors'].append(error_msg)
        
        result['critical_errors'] = critical_count
        result['status'] = 'FAIL' if (result['errors'] or critical_count > 0) else 'PASS'
        result['details'] = yaml_result.get('results', [])
        
    except Exception as e:
        error_msg = f"YAML形式検証中にエラーが発生: {str(e)}"
        result['errors'].append(error_msg)
        result['status'] = 'FAIL'
    
    return result
```

### 2. 統合インターフェース（`yaml_format_check_integration.py`）

```python
import os
import sys
from typing import Dict, List, Optional, Any

def run_yaml_format_check(
    base_dir: str, 
    tables: Optional[List[str]] = None, 
    verbose: bool = False,
    check_required_only: bool = False
) -> Dict[str, Any]:
    """YAML形式検証チェックを実行する（統合版）"""
    
    # yaml_validatorモジュールのパスを追加
    yaml_validator_path = os.path.join(base_dir, 'tools', 'yaml_validator')
    if yaml_validator_path not in sys.path:
        sys.path.insert(0, yaml_validator_path)
    
    try:
        # yaml_validatorから検証機能をインポート
        from validate_yaml_format import validate_table_yaml, get_table_yaml_files
        
        results = {
            "valid": True,
            "errors": [],
            "results": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "critical": 0
            }
        }
        
        # 対象テーブルの決定
        if tables:
            yaml_files = []
            for table in tables:
                yaml_file = os.path.join(base_dir, 'table-details', f'{table}_details.yaml')
                if os.path.exists(yaml_file):
                    yaml_files.append((table, yaml_file))
        else:
            yaml_files = get_table_yaml_files(base_dir)
        
        results["summary"]["total"] = len(yaml_files)
        
        # 各テーブルの検証実行
        for table_name, yaml_file in yaml_files:
            try:
                table_result = validate_table_yaml(
                    table_name, 
                    yaml_file, 
                    verbose=verbose,
                    check_required_only=check_required_only
                )
                
                results["results"].append(table_result)
                
                if table_result.get("valid", True):
                    results["summary"]["passed"] += 1
                else:
                    results["summary"]["failed"] += 1
                    results["valid"] = False
                    
                    # 必須セクション不足はCRITICALエラー
                    if "required section" in table_result.get("message", "").lower():
                        results["summary"]["critical"] += 1
                        
            except Exception as e:
                error_result = {
                    "table_name": table_name,
                    "valid": False,
                    "message": f"検証中にエラーが発生: {str(e)}",
                    "errors": [str(e)]
                }
                results["results"].append(error_result)
                results["summary"]["failed"] += 1
                results["valid"] = False
        
        return results
        
    except ImportError as e:
        return {
            "valid": False,
            "errors": [f"yaml_validatorモジュールのインポートエラー: {str(e)}"],
            "results": [],
            "summary": {"total": 0, "passed": 0, "failed": 0, "critical": 0}
        }
    finally:
        # パスをクリーンアップ
        if yaml_validator_path in sys.path:
            sys.path.remove(yaml_validator_path)

def get_table_yaml_files(base_dir: str) -> List[tuple]:
    """テーブル詳細YAMLファイルの一覧を取得"""
    yaml_files = []
    table_details_dir = os.path.join(base_dir, 'table-details')
    
    if os.path.exists(table_details_dir):
        for filename in os.listdir(table_details_dir):
            if filename.endswith('_details.yaml') and not filename.startswith('MST_TEMPLATE'):
                table_name = filename.replace('_details.yaml', '')
                yaml_file = os.path.join(table_details_dir, filename)
                yaml_files.append((table_name, yaml_file))
    
    return sorted(yaml_files)
```

## トラブルシューティング

### 1. よくあるエラー

#### 必須セクション不足（CRITICAL）
```
CRITICAL: MST_Department: Missing required section: business_rules
```
**解決方法**: 
1. `docs/design/database/tools/database_consistency_checker/required_sections_guide.md` を参照
2. MST_TEMPLATE_details.yaml を参考に必須セクションを追加
3. 最低要件を満たす内容を記述

#### YAML構文エラー
```
ERROR: YAML syntax error: mapping values are not allowed here
```
**解決方法**: 
1. インデント（スペース2文字）を確認
2. コロン後のスペースを確認
3. 文字列の引用符を確認

#### 品質基準未達
```
ERROR: overview section too short (25 chars, minimum 50 required)
```
**解決方法**: 
1. overviewセクションを最低50文字以上で記述
2. テーブルの目的と使用コンテキストを明確に説明

### 2. デバッグ方法

#### 詳細ログ出力
```bash
python database_consistency_checker/run_check.py --tables MST_Employee --checks yaml_format --verbose
```

#### 必須セクションのみチェック
```bash
python database_consistency_checker/run_check.py --tables MST_Employee --checks yaml_format --required-sections-only --verbose
```

#### JSON出力での詳細確認
```bash
python database_consistency_checker/run_check.py --checks yaml_format --output-format json --output-file debug_results.json
cat debug_results.json | jq '.results.MST_Employee'
```

### 3. 緊急時対応

#### Git フック無効化（一時的）
```bash
# 緊急時のみ使用
git commit --no-verify -m "緊急修正: 詳細は後で対応"
```

#### 段階的修正
```bash
# 1. 必須セクション不足のテーブルを特定
python database_consistency_checker/run_check.py --checks yaml_format --required-sections-only

# 2. 一つずつ修正
python database_consistency_checker/run_check.py --tables MST_Employee --checks yaml_format --verbose

# 3. 全体チェック
python database_consistency_checker/run_check.py --checks yaml_format --verbose
```

## 開発・保守

### 1. 新しい検証ルール追加
1. `yaml_validator/validate_yaml_format.py` の `validate_table_yaml()` 関数を拡張
2. `database_consistency_checker/yaml_format_check.py` の統合ロジックを更新
3. テストケースを追加
4. ドキュメントを更新

### 2. 統合ポイント拡張
1. `database_consistency_checker/yaml_format_check_integration.py` を修正
2. 新しいチェック項目を `run_check.py` に追加
3. 統合テストを実行

### 3. パフォーマンス最適化
- 並列処理の導入（複数テーブル同時検証）
- キャッシュ機能の実装（YAML解析結果）
- 差分チェックの最適化（変更されたファイルのみ）

## 関連ドキュメント

- [YAML検証ツール README](README.md)
- [必須セクション詳細ガイド](README_REQUIRED_SECTIONS.md)
- [データベース整合性チェッカー 必須セクションガイド](../database_consistency_checker/required_sections_guide.md)
- [データベース設計ガイドライン](../../../.clinerules/08-database-design-guidelines.md)
- [データベース整合性チェッカー](../database_consistency_checker/README.md)

---

このガイドに従って、YAML検証ツールとデータベース整合性チェッカーの統合を効果的に活用してください。統合版の使用を強く推奨します。
