# YAML検証ツール統合ガイド（正確なデータベース整合性チェッカー統合対応版）

## 概要

このドキュメントは、YAML検証ツール（yaml_validator）を他のデータベース設計ツールと統合する方法について説明します。特に、データベース整合性チェッカー（database_consistency_checker）との正確な統合に焦点を当て、現在の実装状況に基づいた実用的な統合を実現します。

## 🚨 重要な統合修正事項（実装ベース）

### 現在の実装状況分析
1. **既存統合の問題点**: 
   - `yaml_format_check.py`は独立したモジュールとして実装済み
   - `__main__.py`では`check_yaml_format`関数を直接インポートして使用
   - 共通ライブラリとの統合は部分的（パーサーのみ）
   - 必須セクション検証は実装済みだが、統合APIが不統一

2. **実際の統合状況**:
   - ✅ YAMLフォーマット検証: 実装済み（`yaml_format_check.py`）
   - ✅ 必須セクション検証: 実装済み（🔴絶対省略禁止セクション対応）
   - ✅ データベース整合性チェッカー統合: 実装済み（`__main__.py`）
   - 🔄 共通ライブラリ完全統合: 部分的実装
   - ❌ 統合API統一: 未実装

### 修正された統合方針
- **現実的統合**: 既存実装を活用した段階的統合
- **API統一**: 統合結果形式の標準化
- **必須セクション強制**: 🔴絶対省略禁止セクションの厳格な検証維持
- **エラーハンドリング改善**: 一貫したエラー処理とレポート形式

## 統合対象ツール

### 1. データベース整合性チェッカー（database_consistency_checker）
- **統合方法**: 直接インポート統合（`from yaml_format_check import check_yaml_format`）
- **呼び出し方法**: `ConsistencyCheckService._check_yaml_format()`メソッド
- **統合レベル**: 機能レベル統合（既存実装ベース）
- **統合状況**: ✅ 実装済み（v2.1.0 - 現在の実装）
- **改善点**: API統一、エラーハンドリング強化

### 2. テーブル生成ツール（table_generator）
- **統合方法**: 生成前の事前検証として統合
- **呼び出し方法**: validate_yaml_format()関数
- **統合レベル**: プロセス統合
- **統合状況**: 🔄 計画中（v2.2.0予定）

### 3. CI/CDパイプライン
- **統合方法**: Git pre-commitフック + GitHub Actions
- **呼び出し方法**: install_git_hook.sh + workflow統合
- **統合レベル**: ワークフロー統合
- **統合状況**: ✅ 実装済み（スタンドアロン版）

## 統合実装詳細（現在の実装ベース）

### database_consistency_checkerとの統合

#### 現在の統合ファイル構成
```
database_consistency_checker/
├── __main__.py                        # メインモジュール（✅ 統合済み）
├── yaml_format_check.py              # YAML検証モジュール（✅ 実装済み）
└── required_sections_guide.md        # 必須セクションガイド（✅ 実装済み）

yaml_validator/
├── validate_yaml_format.py           # スタンドアロン検証（✅ 実装済み）
├── install_git_hook.sh              # Git統合（✅ 実装済み）
└── README_REQUIRED_SECTIONS.md      # 必須セクション詳細（✅ 実装済み）
```

#### 現在の統合API仕様

```python
# database_consistency_checker/yaml_format_check.py（現在の実装）
def check_yaml_format(tables=None, verbose=False):
    """
    テーブル詳細YAMLファイルのフォーマットを検証する
    
    Args:
        tables (list): 検証対象のテーブル名リスト（Noneの場合は全テーブル）
        verbose (bool): 詳細なログを出力するかどうか
        
    Returns:
        dict: 検証結果
        {
            'success': bool,        # 全体の成功/失敗
            'total': int,          # 総テーブル数
            'valid': int,          # 検証成功テーブル数
            'invalid': int,        # 検証失敗テーブル数
            'results': [           # 個別テーブル結果
                {
                    'valid': bool,     # 検証結果
                    'file': str,       # YAMLファイルパス
                    'table': str,      # テーブル名
                    'errors': list     # エラーメッセージリスト
                }
            ]
        }
    """

# database_consistency_checker/__main__.py での統合（現在の実装）
class ConsistencyCheckService:
    """整合性チェックサービス - 現在の実装版"""
    
    def _check_yaml_format(self, target_tables: List[str]) -> Dict[str, Any]:
        """
        YAMLフォーマット検証チェック（現在の統合実装）
        """
        result = {
            'check_name': 'yaml_format',
            'description': 'YAMLフォーマット・必須セクション検証',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        try:
            # 既存のYAMLフォーマット検証実行
            yaml_check_result = check_yaml_format(tables=target_tables, verbose=False)
            
            # 結果を整合性チェック形式に変換
            if not yaml_check_result['success']:
                result['status'] = 'FAIL'
                
                for yaml_result in yaml_check_result['results']:
                    if not yaml_result['valid']:
                        table_detail = {
                            'table_name': yaml_result['table'],
                            'yaml_format_issues': yaml_result['errors']
                        }
                        result['details'].append(table_detail)
                        
                        # エラーメッセージを追加
                        for error in yaml_result['errors']:
                            error_msg = f"{yaml_result['table']}: {error}"
                            result['errors'].append(error_msg)
            
            # 成功した場合の詳細情報
            if result['status'] == 'PASS':
                result['details'].append({
                    'note': f"全{yaml_check_result['valid']}テーブルのYAMLフォーマット検証に成功しました"
                })
            
        except Exception as e:
            error_msg = f"YAMLフォーマット検証中にエラーが発生: {str(e)}"
            result['errors'].append(error_msg)
            result['status'] = 'FAIL'
            self.logger.error(error_msg)
        
        return result
```

#### 改善された統合API仕様（提案）

```python
# database_consistency_checker/yaml_format_check.py（改善版）
def check_yaml_format_enhanced(tables=None, verbose=False):
    """
    拡張YAMLフォーマット検証（必須セクション詳細対応）
    
    Args:
        tables (list): 検証対象のテーブル名リスト（Noneの場合は全テーブル）
        verbose (bool): 詳細なログを出力するかどうか
        
    Returns:
        dict: 拡張検証結果
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
    """
    
    import time
    start_time = time.time()
    
    results = []
    critical_errors = 0
    format_errors = 0
    requirement_errors = 0
    warning_count = 0
    
    if tables:
        # 指定されたテーブルのみ検証
        for table in tables:
            result = validate_table_yaml_enhanced(table, verbose)
            results.append(result)
            
            # エラー分類
            if not result['valid']:
                # 必須セクション不備をカウント
                for section, valid in result['required_sections'].items():
                    if not valid:
                        critical_errors += 1
                        break
                
                format_errors += len(result['format_issues'])
                requirement_errors += len(result['requirement_id_issues'])
            
            if result['warnings']:
                warning_count += 1
    else:
        # 全テーブルを検証
        yaml_files = glob.glob(os.path.join(TABLE_DETAILS_DIR, "*_details.yaml"))
        for yaml_file in yaml_files:
            table_name = os.path.basename(yaml_file).replace("_details.yaml", "")
            if table_name == "MST_TEMPLATE":  # テンプレートファイルはスキップ
                continue
            
            if verbose:
                print(f"\n{Fore.BLUE}テーブル {table_name} の検証を開始...{Style.RESET_ALL}")
            
            result = validate_table_yaml_enhanced(table_name, verbose)
            results.append(result)
            
            # エラー分類
            if not result['valid']:
                # 必須セクション不備をカウント
                for section, valid in result['required_sections'].items():
                    if not valid:
                        critical_errors += 1
                        break
                
                format_errors += len(result['format_issues'])
                requirement_errors += len(result['requirement_id_issues'])
            
            if result['warnings']:
                warning_count += 1
    
    # 結果サマリー
    valid_count = sum(1 for r in results if r['valid'])
    invalid_count = len(results) - valid_count
    execution_time = time.time() - start_time
    
    if verbose:
        print(f"\n{Fore.CYAN}=== YAMLフォーマット検証結果（拡張版） ==={Style.RESET_ALL}")
        print(f"総ファイル数: {len(results)}")
        print(f"有効: {valid_count}")
        print(f"無効: {invalid_count}")
        print(f"警告: {warning_count}")
        print(f"🔴 必須セクション不備: {critical_errors}テーブル")
        print(f"⏱️ 実行時間: {execution_time:.2f}秒")
        
        if invalid_count > 0:
            print(f"\n{Fore.RED}無効なファイル:{Style.RESET_ALL}")
            for result in results:
                if not result['valid']:
                    print(f"  {Fore.RED}❌ {result['table']}{Style.RESET_ALL}")
                    
                    # 必須セクション不備の詳細表示
                    for section, valid in result['required_sections'].items():
                        if not valid:
                            print(f"    🔴 {section}: 不備（絶対省略禁止）")
                    
                    # その他のエラー
                    for error in result['errors']:
                        print(f"    - {error}")
    
    # エラーがある場合の詳細表示
    if invalid_count > 0 and not verbose:
        print(f"{Fore.RED}以下のテーブルの検証に失敗しました:{Style.RESET_ALL}")
        for result in results:
            if not result['valid']:
                print(f"{Fore.RED}  - {result['table']}{Style.RESET_ALL}")
                
                # 必須セクション不備を優先表示
                critical_issues = []
                for section, valid in result['required_sections'].items():
                    if not valid:
                        critical_issues.append(f"🔴 {section}（絶対省略禁止）")
                
                if critical_issues:
                    for issue in critical_issues:
                        print(f"    {Fore.RED}{issue}{Style.RESET_ALL}")
                
                # その他のエラー
                for error in result['errors']:
                    print(f"    {Fore.RED}- {error}{Style.RESET_ALL}")
        
        print(f"{Fore.YELLOW}詳細なガイドラインは docs/design/database/tools/yaml_validator/README_REQUIRED_SECTIONS.md を参照してください。{Style.RESET_ALL}")
    
    return {
        'success': invalid_count == 0,
        'total': len(results),
        'valid': valid_count,
        'invalid': invalid_count,
        'warning': warning_count,
        'results': results,
        'summary': {
            'critical_errors': critical_errors,
            'format_errors': format_errors,
            'requirement_errors': requirement_errors,
            'execution_time': execution_time
        }
    }


def validate_table_yaml_enhanced(table_name: str, verbose: bool = False) -> Dict[str, Any]:
    """拡張テーブルYAML検証"""
    yaml_file = os.path.join(TABLE_DETAILS_DIR, f"{table_name}_details.yaml")
    
    result = {
        'valid': True,
        'file': yaml_file,
        'table': table_name,
        'errors': [],
        'warnings': [],
        'required_sections': {
            'revision_history': False,
            'overview': False,
            'notes': False,
            'business_rules': False
        },
        'format_issues': [],
        'requirement_id_issues': []
    }
    
    if not os.path.exists(yaml_file):
        result['valid'] = False
        result['errors'].append(f"ファイル {yaml_file} が存在しません")
        return result
    
    yaml_data = load_yaml_file(yaml_file)
    if not yaml_data:
        result['valid'] = False
        result['errors'].append("YAMLファイルの読み込みに失敗しました")
        return result
    
    # 必須セクション検証
    is_valid, errors = validate_required_sections(yaml_data, table_name, verbose)
    if not is_valid:
        result['valid'] = False
        result['errors'].extend(errors)
    
    # 必須セクション個別チェック
    for section in REQUIRED_SECTIONS.keys():
        if section in yaml_data:
            if section == "revision_history":
                result['required_sections'][section] = (
                    isinstance(yaml_data[section], list) and 
                    len(yaml_data[section]) >= REQUIRED_SECTIONS[section]["min_entries"]
                )
            elif section == "overview":
                result['required_sections'][section] = (
                    len(str(yaml_data[section])) >= REQUIRED_SECTIONS[section]["min_length"]
                )
            elif section in ["notes", "business_rules"]:
                result['required_sections'][section] = (
                    isinstance(yaml_data[section], list) and 
                    len(yaml_data[section]) >= REQUIRED_SECTIONS[section]["min_entries"]
                )
    
    # フォーマット検証（基本的なYAML構文チェック）
    try:
        # インデント統一チェック
        with open(yaml_file, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if line.strip() and line.startswith('\t'):
                    result['format_issues'].append(f"行{i}: タブ文字使用（スペース2文字推奨）")
                    result['warnings'].append(f"行{i}: インデント不統一")
    except Exception as e:
        result['format_issues'].append(f"ファイル読み込みエラー: {str(e)}")
    
    # 要求仕様ID検証
    if 'columns' in yaml_data and isinstance(yaml_data['columns'], list):
        for col in yaml_data['columns']:
            if isinstance(col, dict):
                col_name = col.get('name', 'unknown')
                requirement_id = col.get('requirement_id', '')
                
                if not requirement_id:
                    result['requirement_id_issues'].append(f"カラム {col_name}: 要求仕様ID未設定")
                    result['warnings'].append(f"カラム {col_name}: 要求仕様ID未設定")
                elif not _validate_requirement_id_format(requirement_id):
                    result['requirement_id_issues'].append(f"カラム {col_name}: 要求仕様ID形式エラー ({requirement_id})")
                    result['warnings'].append(f"カラム {col_name}: 要求仕様ID形式エラー")
    
    # 警告がある場合でも、必須セクション不備がなければ有効とする
    if result['warnings'] and result['valid']:
        # 必須セクション不備がある場合のみ無効とする
        has_critical_error = not all(result['required_sections'].values())
        if has_critical_error:
            result['valid'] = False
    
    return result


def _validate_requirement_id_format(requirement_id: str) -> bool:
    """要求仕様ID形式検証"""
    import re
    # カテゴリ.シリーズ-機能 形式（例: PRO.1-BASE.1）
    pattern = r'^[A-Z]{3}\.\d+-[A-Z]+\.\d+$'
    return bool(re.match(pattern, requirement_id))


# database_consistency_checker/__main__.py での改善された統合
class ConsistencyCheckService:
    """整合性チェックサービス - 改善された統合版"""
    
    def _check_yaml_format(self, target_tables: List[str]) -> Dict[str, Any]:
        """
        YAMLフォーマット検証チェック（改善された統合実装）
        """
        result = {
            'check_name': 'yaml_format',
            'description': 'YAMLフォーマット・必須セクション検証（拡張版）',
            'status': 'PASS',
            'errors': [],
            'warnings': [],
            'details': []
        }
        
        try:
            # 拡張YAMLフォーマット検証実行
            yaml_check_result = check_yaml_format_enhanced(tables=target_tables, verbose=False)
            
            # 結果を整合性チェック形式に変換
            if not yaml_check_result['success']:
                result['status'] = 'FAIL'
                
                # 🔴 必須セクション不備の重要度を最高に設定
                critical_errors = yaml_check_result['summary']['critical_errors']
                if critical_errors > 0:
                    result['errors'].append(
                        f"🔴 必須セクション不備: {critical_errors}テーブル "
                        f"（revision_history, overview, notes, business_rules は絶対省略禁止）"
                    )
                
                # 個別テーブルエラーの詳細化
                for table_result in yaml_check_result['results']:
                    if not table_result['valid']:
                        table_detail = {
                            'table_name': table_result['table'],
                            'yaml_file': table_result['file'],
                            'critical_issues': [],  # 🔴 必須セクション不備
                            'format_issues': table_result['format_issues'],
                            'requirement_issues': table_result['requirement_id_issues']
                        }
                        
                        # 必須セクション不備の詳細化
                        for section, valid in table_result['required_sections'].items():
                            if not valid:
                                table_detail['critical_issues'].append({
                                    'section': section,
                                    'severity': 'CRITICAL',
                                    'message': f"🔴 {section}セクションが存在しないか要件を満たしていません（絶対省略禁止）"
                                })
                        
                        result['details'].append(table_detail)
                        
                        # エラーメッセージを追加
                        for error in table_result['errors']:
                            error_msg = f"{table_result['table']}: {error}"
                            result['errors'].append(error_msg)
            
            # 成功した場合の詳細情報
            if result['status'] == 'PASS':
                result['details'].append({
                    'summary': f"✅ 全{yaml_check_result['valid']}テーブルのYAML検証に成功",
                    'execution_time': yaml_check_result['summary']['execution_time'],
                    'validated_sections': list(REQUIRED_SECTIONS.keys())
                })
            
            # 警告がある場合
            if yaml_check_result['warning'] > 0:
                if result['status'] == 'PASS':
                    result['status'] = 'WARNING'
                result['warnings'].append(
                    f"⚠️ 警告あり: {yaml_check_result['warning']}テーブル"
                )
            
        except Exception as e:
            error_msg = f"YAML検証統合中にエラーが発生: {str(e)}"
            result['errors'].append(error_msg)
            result['status'] = 'FAIL'
            self.logger.error(error_msg, exc_info=True)
        
        return result
```

#### 使用例（現在の実装ベース）

```python
# 現在の統合版（実装済み）
from database_consistency_checker.yaml_format_check import check_yaml_format

# YAML検証実行
result = check_yaml_format(tables=['MST_Employee'], verbose=True)

# 結果確認
if result['success']:
    print(f"✅ 検証成功: {result['valid']}/{result['total']}テーブル")
else:
    print(f"❌ 検証失敗: {result['invalid']}/{result['total']}テーブル")
    
    # 個別エラーの詳細表示
    for table_result in result['results']:
        if not table_result['valid']:
            print(f"\n❌ {table_result['table']}:")
            for error in table_result['errors']:
                print(f"  - {error}")

# データベース整合性チェッカーでの統合実行
from database_consistency_checker.__main__ import ConsistencyCheckService
from shared.core.config import get_config

config = get_config()
service = ConsistencyCheckService(config)
consistency_result = service.run_all_checks(['MST_Employee'])

# YAML検証結果の抽出
yaml_check = next(
    (r for r in consistency_result['details'] if r['check_name'] == 'yaml_format'),
    None
)

if yaml_check:
    print(f"統合YAML検証結果: {yaml_check['status']}")
    if yaml_check['status'] == 'FAIL':
        print("🔴 必須セクション不備の修正が必要です")
        for error in yaml_check['errors']:
            print(f"  - {error}")

# 改善版（提案）
from database_consistency_checker.yaml_format_check import check_yaml_format_enhanced

# 拡張YAML検証実行
enhanced_result = check_yaml_format_enhanced(tables=['MST_Employee'], verbose=True)

# 拡張結果確認
if enhanced_result['success']:
    print(f"✅ 検証成功: {enhanced_result['valid']}/{enhanced_result['total']}テーブル")
    print(f"⏱️ 実行時間: {enhanced_result['summary']['execution_time']:.2f}秒")
else:
    print(f"❌ 検証失敗: {enhanced_result['invalid']}/{enhanced_result['total']}テーブル")
    
    # 🔴 必須セクション不備の重点表示
    critical_errors = enhanced_result['summary']['critical_errors']
    if critical_errors > 0:
        print(f"🔴 重要: {critical_errors}テーブルで必須セクション不備（絶対省略禁止）")
        print("   必須セクション: revision_history, overview, notes, business_rules")
        print("   修正方法: MST_TEMPLATE_details.yamlを参照してセクションを追加")
    
    # 個別エラーの詳細表示
    for table_result in enhanced_result['results']:
        if not table_result['valid']:
            print(f"\n❌ {table_result['table']}:")
            
            # 必須セクション不備の詳細
            for section, valid in table_result['required_sections'].items():
                if not valid:
                    print(f"  🔴 {section}: 不備（絶対省略禁止）")
            
            # フォーマット問題
            for issue in table_result['format_issues']:
                print(f"  ⚠️ フォーマット: {issue}")
            
            # 要求仕様ID問題
            for issue in table_result['requirement_id_issues']:
                print(f"  ⚠️ 要求仕様ID: {issue}")
```

### 統合チェック実行方法（現在の実装ベース）

#### 基本実行コマンド

```bash
# 全チェック実行（YAML検証含む・現在の実装）
cd docs/design/database/tools
python3 database_consistency_checker/__main__.py --verbose

# YAML検証のみ実行（統合版）
python3 database_consistency_checker/__main__.py --checks yaml_format --verbose

# 特定テーブルのYAML検証（統合版）
python3 database_consistency_checker/__main__.py --checks yaml_format --tables MST_Employee,MST_Department --verbose

# 必須セクション重点チェック（スタンドアロン）
python3 yaml_validator/validate_yaml_format.py --check-required-only --verbose

# 詳細レポート出力（統合版）
python3 database_consistency_checker/__main__.py --checks yaml_format --output-format markdown --output-file yaml_validation_report.md --verbose

# 直接YAML検証実行（現在の実装）
python3 database_consistency_checker/yaml_format_check.py --tables MST_Employee --verbose
```

#### 高度な実行オプション

```bash
# JSON形式での結果出力
python3 database_consistency_checker/__main__.py --checks yaml_format --output-format json --output-file validation_results.json

# 設定ファイル指定での実行
python3 database_consistency_checker/__main__.py --config custom_config.yaml --checks yaml_format --verbose

# 全テーブル一括検証
python3 database_consistency_checker/__main__.py --checks yaml_format --verbose

# 特定テーブルのみ検証
python3 database_consistency_checker/__main__.py --checks yaml_format --tables MST_Employee,MST_Department,MST_Tenant --verbose
```

#### 統合チェック結果例（現在の実装ベース）

```
🔍 データベース整合性チェック開始（現在の実装版 v2.1.0）
📂 ベースディレクトリ: /home/kurosawa/skill-report-web/docs/design/database
📂 YAML詳細定義: table-details/
📂 DDLディレクトリ: ddl/
📂 テーブル定義書: tables/
