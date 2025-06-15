# YAML検証ツール

テーブル詳細YAML定義ファイルの必須セクションを検証するツールです。

## 概要

このツールは、テーブル詳細YAML定義ファイル（`docs/design/database/table-details/`内の`*_details.yaml`ファイル）の必須セクション（`revision_history`, `overview`, `notes`, `business_rules`）の存在と内容を検証します。

品質管理・監査・運用保守の観点から、これらの必須セクションは**絶対に省略禁止**です。これらのセクションが欠けているテーブル定義は、自動検証ツールによって拒否され、コミットできません。

## 必須セクション

以下の4つのセクションは絶対に省略禁止です：

1. **revision_history（改版履歴）**: 変更管理・監査の基盤となる重要情報
2. **overview（概要・目的）**: テーブルの存在理由と使用方法を明確にする基本情報
3. **notes（特記事項）**: 運用・保守・セキュリティに関わる重要な補足情報
4. **business_rules（業務ルール）**: データの整合性と業務要件を保証するための制約条件

詳細な要件と例については、[README_REQUIRED_SECTIONS.md](./README_REQUIRED_SECTIONS.md)を参照してください。

## インストール

### 依存関係

- Python 3.8以上
- PyYAML
- colorama（カラー出力用）

```bash
pip install pyyaml colorama
```

### Git pre-commitフックのインストール

コミット時に自動的にYAML検証を実行するGit pre-commitフックをインストールすることができます：

```bash
# Git pre-commitフックのインストール
./install_git_hook.sh
```

これにより、コミット時に変更されたYAMLファイルが自動的に検証され、検証に失敗した場合はコミットが中止されます。

## 使用方法

### 単一テーブルの検証

```bash
python validate_yaml_format.py --table MST_Employee
```

### 全テーブルの検証

```bash
python validate_yaml_format.py --all
```

### 詳細出力

```bash
python validate_yaml_format.py --table MST_Employee --verbose
```

### ヘルプ

```bash
python validate_yaml_format.py --help
```

## 検証基準

各必須セクションは以下の基準で検証されます：

| セクション | 検証基準 | エラーメッセージ |
|------------|----------|----------------|
| revision_history | リスト型で最低1エントリ以上 | revision_historyセクションには最低1エントリが必要です |
| overview | 文字列型で最低50文字以上 | overviewセクションは最低50文字以上必要です |
| notes | リスト型で最低3項目以上 | notesセクションには最低3項目が必要です |
| business_rules | リスト型で最低3項目以上 | business_rulesセクションには最低3項目が必要です |

## 出力例

### 成功時

```
テーブル MST_Employee の検証を実行中...
✅ revision_history: OK (1 エントリ)
✅ overview: OK (512 文字)
✅ notes: OK (6 項目)
✅ business_rules: OK (7 項目)
✅ テーブル MST_Employee の検証に成功しました。
```

### 失敗時

```
テーブル MST_Department の検証を実行中...
❌ revision_history: エラー - revision_historyセクションが見つかりません
❌ overview: エラー - overviewセクションが見つかりません
✅ notes: OK (4 項目)
⚠️ business_rules: 警告 - business_rulesセクションには最低3項目が必要です (現在: 2項目)
❌ テーブル MST_Department の検証に失敗しました。
```

## データベース整合性チェッカーとの統合

このツールは、データベース整合性チェッカーと統合することができます。詳細については、[INTEGRATION.md](./INTEGRATION.md)を参照してください。

## カスタマイズ

### 検証基準の調整

必要に応じて、`validate_yaml_format.py`の`VALIDATION_CRITERIA`を調整することができます：

```python
# 検証基準の設定
VALIDATION_CRITERIA = {
    "revision_history": {
        "min_entries": 1,  # 最低エントリ数
        "required_fields": ["version", "date", "author", "changes"]  # 必須フィールド
    },
    "overview": {
        "min_length": 50  # 最低文字数
    },
    "notes": {
        "min_items": 3  # 最低項目数
    },
    "business_rules": {
        "min_items": 3  # 最低項目数
    }
}
```

## トラブルシューティング

### よくある問題と解決方法

1. **YAMLファイルが見つからない**
   - 原因: ファイルパスが正しくない
   - 解決: テーブル名が正しいか確認し、ファイルが`docs/design/database/table-details/`内にあることを確認

2. **YAML構文エラー**
   - 原因: YAMLファイルの構文が正しくない
   - 解決: YAMLの構文を確認し、インデントやコロンの使用が正しいことを確認

3. **依存関係エラー**
   - 原因: 必要なパッケージがインストールされていない
   - 解決: `pip install pyyaml colorama`を実行

## 貢献

このツールは、データベース設計の品質向上を目的としています。改善提案やバグ報告は歓迎します。

## ライセンス

社内利用限定
