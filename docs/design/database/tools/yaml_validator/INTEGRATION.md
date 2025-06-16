# YAML検証ツール統合ガイド

## 概要

このドキュメントは、YAML検証ツール（yaml_validator）とデータベース整合性チェッカー（database_consistency_checker）の統合について説明します。

## 統合アーキテクチャ

### 統合方針
- **基本検証**: `check_yaml_format()` - 従来の基本的なYAMLフォーマット検証
- **拡張検証**: `check_yaml_format_enhanced()` - 必須セクション詳細対応・要求仕様ID検証
- **統合API**: database_consistency_checkerから両方の検証機能を利用可能

### ファイル構成
```
docs/design/database/tools/
├── yaml_validator/
│   ├── INTEGRATION.md                    # 本ファイル
│   ├── README.md                         # YAML検証ツール基本ガイド
│   ├── README_REQUIRED_SECTIONS.md      # 必須セクション詳細ガイド
│   ├── validate_yaml_format.py          # スタンドアロン検証ツール
│   └── install_git_hook.sh              # Git pre-commitフック設定
└── database_consistency_checker/
    ├── yaml_format_check.py             # 統合YAML検証モジュール
    ├── yaml_format_check_integration.py # 統合API実装
    └── __main__.py                       # メインエントリーポイント
```

## 統合API仕様

### 基本検証API

#### `check_yaml_format(tables=None, verbose=False)`

**目的**: 基本的なYAMLフォーマット検証と必須セクション存在確認

**パラメータ**:
- `tables` (list, optional): 検証対象テーブル名リスト（Noneで全テーブル）
- `verbose` (bool): 詳細ログ出力フラグ

**戻り値**:
```python
{
    'success': bool,           # 全体の成功/失敗
    'total': int,             # 総テーブル数
    'valid': int,             # 検証成功テーブル数
    'invalid': int,           # 検証失敗テーブル数
    'results': [              # 個別テーブル結果
        {
            'valid': bool,        # 検証結果
            'file': str,          # YAMLファイルパス
            'table': str,         # テーブル名
            'errors': list        # エラーメッセージリスト
        }
    ]
}
```

**使用例**:
```python
from yaml_format_check import check_yaml_format

# 全テーブル検証
result = check_yaml_format(verbose=True)

# 特定テーブル検証
result = check_yaml_format(tables=['MST_Employee', 'MST_Department'])

if not result['success']:
    print(f"検証失敗: {result['invalid']}テーブル")
    for table_result in result['results']:
        if not table_result['valid']:
            print(f"- {table_result['table']}: {table_result['errors']}")
```

### 拡張検証API

#### `check_yaml_format_enhanced(tables=None, verbose=False)`

**目的**: 詳細なYAMLフォーマット検証・必須セクション内容検証・要求仕様ID検証

**パラメータ**:
- `tables` (list, optional): 検証対象テーブル名リスト（Noneで全テーブル）
- `verbose` (bool): 詳細ログ出力フラグ

**戻り値**:
```python
{
    'success': bool,           # 全体の成功/失敗
    'total': int,             # 総テーブル数
    'valid': int,             # 検証成功テーブル数
    'invalid': int,           # 検証失敗テーブル数
    'warning': int,           # 警告ありテーブル数
    'results': [              # 個別テーブル結果
        {
            'valid': bool,            # 検証結果
            'file': str,              # YAMLファイルパス
            'table': str,             # テーブル名
            'errors': list,           # エラーメッセージリスト
            'warnings': list,         # 警告メッセージリスト
            'required_sections': {    # 必須セクション検証結果
                'revision_history': bool,
                'overview': bool,
                'notes': bool,
                'business_rules': bool
            },
            'format_issues': list,    # フォーマット問題リスト
            'requirement_id_issues': list  # 要求仕様ID問題リスト
        }
    ],
    'summary': {              # 検証サマリー
        'critical_errors': int,       # 🔴 必須セクション不備数
        'format_errors': int,         # フォーマットエラー数
        'requirement_errors': int,    # 要求仕様IDエラー数
        'execution_time': float       # 実行時間（秒）
    }
}
```

**使用例**:
```python
from yaml_format_check import check_yaml_format_enhanced

# 拡張検証実行
result = check_yaml_format_enhanced(verbose=True)

# 結果分析
print(f"🔴 必須セクション不備: {result['summary']['critical_errors']}テーブル")
print(f"⚠️ フォーマット問題: {result['summary']['format_errors']}件")
print(f"📋 要求仕様ID問題: {result['summary']['requirement_errors']}件")
print(f"⏱️ 実行時間: {result['summary']['execution_time']:.2f}秒")

# 必須セクション不備の詳細確認
for table_result in result['results']:
    if not table_result['valid']:
        critical_issues = [
            section for section, valid in table_result['required_sections'].items()
            if not valid
        ]
        if critical_issues:
            print(f"🔴 {table_result['table']}: {', '.join(critical_issues)} 不備")
```

## database_consistency_checkerとの統合

### 統合実装

database_consistency_checkerでは、YAML検証機能が以下のように統合されています：

#### 統合モジュール構成
```
database_consistency_checker/
├── __main__.py                       # メインエントリーポイント
├── yaml_format_check.py             # YAML検証モジュール（統合版）
└── yaml_format_check_integration.py # 統合API実装
```

#### 統合API実装

`yaml_format_check.py`では、以下の2つの主要な検証関数を提供：

```python
# 基本検証
def check_yaml_format(tables=None, verbose=False):
    """基本的なYAMLフォーマット検証と必須セクション存在確認"""
    # 実装詳細は yaml_format_check.py を参照

# 拡張検証  
def check_yaml_format_enhanced(tables=None, verbose=False):
    """詳細なYAMLフォーマット検証・必須セクション内容検証・要求仕様ID検証"""
    # 実装詳細は yaml_format_check.py を参照
```

#### database_consistency_checkerでの呼び出し

`__main__.py`では、以下のチェック名で統合されています：

- **`yaml_format`**: 基本的なYAMLフォーマット検証
- **`yaml_format_enhanced`**: 拡張YAML検証（必須セクション詳細・要求仕様ID検証）

### 統合コマンド実行例

```bash
# 基本的なYAML検証
cd docs/design/database/tools
python3 -m database_consistency_checker --checks yaml_format --tables MST_Employee

# 拡張YAML検証
python3 -m database_consistency_checker --checks yaml_format_enhanced --tables MST_Employee

# 詳細ログ付きでYAML検証
python3 -m database_consistency_checker --checks yaml_format --verbose

# 複数テーブルの検証
python3 -m database_consistency_checker --checks yaml_format --tables MST_Employee,MST_Department

# 全テーブルの拡張検証
python3 -m database_consistency_checker --checks yaml_format_enhanced --verbose

# 直接実行（スタンドアロン）
python3 database_consistency_checker/yaml_format_check.py --tables MST_Employee --verbose
```

### 実行結果例

#### 成功時
```
2025-06-17 04:32:51 - __main__ - INFO - データベース整合性チェック開始
2025-06-17 04:32:51 - __main__ - INFO - チェック実行: yaml_format

=== データベース整合性チェック結果 ===
総チェック数: 1
成功: 1
失敗: 0
警告: 0

✅ すべてのチェックが正常に完了しました
```

#### 失敗時
```
以下のテーブルの検証に失敗しました:
  - MST_Employee
    🔴 revision_history（絶対省略禁止）
    🔴 overview（絶対省略禁止）
    - カラム employee_code: 要求仕様ID未設定

詳細なガイドラインは docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md を参照してください。

=== データベース整合性チェック結果 ===
総チェック数: 1
成功: 0
失敗: 1
警告: 0

❌ 整合性エラーが検出されました
```

## 必須セクション検証詳細

### 🔴 絶対省略禁止セクション

以下の4つのセクションは品質管理・監査・運用保守の観点から**絶対省略禁止**です：

| セクション | 目的 | 最低要件 | 検証内容 |
|------------|------|----------|----------|
| `revision_history` | 変更履歴の追跡・監査証跡 | 最低1エントリ | リスト形式・エントリ数確認 |
| `overview` | テーブルの目的・設計意図の明確化 | 最低50文字 | 文字数・内容の妥当性 |
| `notes` | 運用・保守に必要な特記事項 | 最低3項目 | リスト形式・項目数確認 |
| `business_rules` | 業務ルール・制約の明文化 | 最低3項目 | リスト形式・項目数確認 |

### 検証エラー例

```
🔴 MST_Employee: 必須セクション不備
  - revision_history: 最低1エントリが必要です
  - overview: 最低50文字以上の説明が必要です (現在: 25文字)
  - notes: 最低3項目以上の記載が必要です
  - business_rules: 最低3項目以上の記載が必要です
```

## 要求仕様ID検証

### 検証対象
- **テーブルレベル**: `requirement_id`フィールド
- **カラムレベル**: 各カラムの`requirement_id`フィールド

### 形式要件
- **パターン**: `[カテゴリ].[シリーズ]-[機能].[番号]`
- **例**: `PRO.1-BASE.1`, `SKL.2-HIER.3`, `ACC.1-AUTH.2`

### 有効なカテゴリ
- **PLT**: Platform (システム基盤要件)
- **ACC**: Access Control (ユーザー権限管理)
- **PRO**: Profile (個人プロフィール管理)
- **SKL**: Skill (スキル情報管理)
- **CAR**: Career (目標・キャリア管理)
- **WPM**: Work Performance Mgmt (作業実績管理)
- **TRN**: Training (研修・セミナー管理)
- **RPT**: Report (レポート出力)
- **NTF**: Notification (通知・連携サービス)

### 検証エラー例

```
⚠️ MST_Employee: 要求仕様ID問題
  - カラム employee_code: 要求仕様ID未設定
  - カラム full_name: 要求仕様ID形式エラー (PRO-BASE-1)
  - カラム email: 要求仕様ID形式エラー (ACC.AUTH.1)
```

## Git統合

### pre-commitフック設定

```bash
# Git pre-commitフック設定
cd docs/design/database/tools/yaml_validator
./install_git_hook.sh
```

### フック動作
- **コミット前**: 変更されたYAMLファイルの自動検証
- **検証失敗**: コミット拒否・エラー詳細表示
- **検証成功**: 正常コミット実行

### フック設定例

```bash
#!/bin/sh
# Git pre-commit hook for YAML validation

# 変更されたYAMLファイルを取得
changed_yaml_files=$(git diff --cached --name-only --diff-filter=ACM | grep "_details\.yaml$")

if [ -n "$changed_yaml_files" ]; then
    echo "🔍 YAML検証を実行中..."
    
    # テーブル名を抽出
    tables=""
    for file in $changed_yaml_files; do
        table_name=$(basename "$file" "_details.yaml")
        if [ "$table_name" != "MST_TEMPLATE" ]; then
            if [ -z "$tables" ]; then
                tables="$table_name"
            else
                tables="$tables,$table_name"
            fi
        fi
    done
    
    if [ -n "$tables" ]; then
        # YAML検証実行
        python docs/design/database/tools/database_consistency_checker/yaml_format_check.py --tables "$tables"
        
        if [ $? -ne 0 ]; then
            echo "❌ YAML検証に失敗しました。コミットを中止します。"
            echo "詳細は docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md を参照してください。"
            exit 1
        fi
        
        echo "✅ YAML検証に成功しました。"
    fi
fi

exit 0
```

## 運用ガイドライン

### 日常的な使用

#### 1. 新規テーブル作成時
```bash
# 1. テンプレートからYAML作成
cp docs/design/database/table-details/MST_TEMPLATE_details.yaml \
   docs/design/database/table-details/NEW_TABLE_details.yaml

# 2. 必須セクション編集
# - revision_history: 初版エントリ追加
# - overview: テーブルの目的・概要記述（50文字以上）
# - notes: 運用・保守の特記事項（3項目以上）
# - business_rules: 業務ルール・制約（3項目以上）

# 3. YAML検証実行
python docs/design/database/tools/database_consistency_checker/yaml_format_check.py --tables NEW_TABLE --verbose

# 4. 拡張検証実行
python -c "
from docs.design.database.tools.database_consistency_checker.yaml_format_check import check_yaml_format_enhanced
result = check_yaml_format_enhanced(tables=['NEW_TABLE'], verbose=True)
print(f'検証結果: {\"成功\" if result[\"success\"] else \"失敗\"}')
"
```

#### 2. 既存テーブル修正時
```bash
# 1. 修正前の検証
python docs/design/database/tools/database_consistency_checker/yaml_format_check.py --tables MODIFIED_TABLE

# 2. YAML修正
# - revision_history: 新しい変更エントリ追加
# - 必要に応じて他のセクションも更新

# 3. 修正後の検証
python docs/design/database/tools/database_consistency_checker/yaml_format_check.py --tables MODIFIED_TABLE --verbose

# 4. 統合整合性チェック
python -m database_consistency_checker --tables MODIFIED_TABLE
```

#### 3. 定期的な全体検証
```bash
# 週次: 全テーブルの基本検証
python docs/design/database/tools/database_consistency_checker/yaml_format_check.py --verbose

# 月次: 拡張検証・詳細レポート
python -c "
from docs.design.database.tools.database_consistency_checker.yaml_format_check import check_yaml_format_enhanced
import json
result = check_yaml_format_enhanced(verbose=True)
with open('yaml_validation_report.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print('詳細レポートを yaml_validation_report.json に出力しました')
"
```

### トラブルシューティング

#### よくあるエラーと対処法

##### 1. 必須セクション不備
```
❌ エラー: 必須セクション 'revision_history' が存在しません
```

**対処法**:
```yaml
# revision_history セクションを追加
revision_history:
  - version: "1.0.0"
    date: "2025-06-17"
    author: "開発チーム"
    changes: "初版作成"
```

##### 2. overview文字数不足
```
❌ エラー: 'overview': 最低50文字以上の説明が必要です (現在: 25文字)
```

**対処法**:
```yaml
# overview を詳細に記述
overview: |
  このテーブルは組織に所属する全社員の基本的な個人情報と組織情報を一元管理するマスタテーブルです。
  主な目的は、社員の基本情報（氏名、連絡先、入社日等）の管理、組織構造（部署、役職、上司関係）の管理、
  認証・権限管理のためのユーザー情報提供、人事システムとの連携データ基盤として機能します。
```

##### 3. 要求仕様ID形式エラー
```
⚠️ 警告: カラム employee_code: 要求仕様ID形式エラー (PRO-BASE-1)
```

**対処法**:
```yaml
# 正しい形式に修正
columns:
  - name: "employee_code"
    type: "VARCHAR(30)"
    nullable: false
    comment: "社員番号"
    requirement_id: "PRO.1-BASE.1"  # 正しい形式
```

### パフォーマンス最適化

#### 大量テーブル検証時の最適化

```python
# バッチ処理での効率的な検証
from docs.design.database.tools.database_consistency_checker.yaml_format_check import check_yaml_format_enhanced
import glob
import os

def batch_validate_yaml():
    """大量テーブルの効率的な検証"""
    yaml_files = glob.glob("docs/design/database/table-details/*_details.yaml")
    table_names = [
        os.path.basename(f).replace("_details.yaml", "")
        for f in yaml_files
        if not f.endswith("MST_TEMPLATE_details.yaml")
    ]
    
    # 10テーブルずつバッチ処理
    batch_size = 10
    for i in range(0, len(table_names), batch_size):
        batch_tables = table_names[i:i+batch_size]
        print(f"バッチ {i//batch_size + 1}: {len(batch_tables)}テーブル検証中...")
        
        result = check_yaml_format_enhanced(tables=batch_tables, verbose=False)
        
        if not result['success']:
            print(f"  ❌ {result['invalid']}テーブルで検証失敗")
            for table_result in result['results']:
                if not table_result['valid']:
                    print(f"    - {table_result['table']}")
        else:
            print(f"  ✅ 全{len(batch_tables)}テーブル検証成功")

if __name__ == "__main__":
    batch_validate_yaml()
```

## 今後の拡張計画

### Phase 1: 基本統合（完了）
- ✅ 基本YAML検証機能の統合
- ✅ 必須セクション検証の実装
- ✅ database_consistency_checkerとの統合

### Phase 2: 拡張機能（完了）
- ✅ 拡張YAML検証API実装
- ✅ 要求仕様ID検証機能
- ✅ 詳細エラー分類・レポート機能
- ✅ Git pre-commitフック統合

### Phase 3: 高度な機能（計画中）
- 📋 YAML内容の意味的検証（業務ルールの妥当性チェック）
- 📋 テーブル間関係の整合性検証
- 📋 自動修正提案機能
- 📋 CI/CD統合・自動レポート生成

### Phase 4: 運用最適化（将来）
- 📋 パフォーマンス最適化・並列処理
- 📋 カスタムルール設定機能
- 📋 ダッシュボード・可視化機能
- 📋 外部ツール連携（Slack通知等）

---

このガイドに従って、YAML検証ツールとdatabase_consistency_checkerの統合を効果的に活用してください。
